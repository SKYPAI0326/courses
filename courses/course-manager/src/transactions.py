from __future__ import annotations

import copy
import errno
import hashlib
import json
import os
import secrets
import stat
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, MutableMapping, Sequence

try:  # Windows and other unsupported hosts must fail closed at call time.
    import fcntl
except ImportError:  # pragma: no cover - exercised only on unsupported platforms
    fcntl = None  # type: ignore[assignment]


class TransactionError(RuntimeError):
    pass


class UnsupportedPlatformError(TransactionError):
    pass


class UnsafeContractPathError(TransactionError):
    pass


class RevisionConflictError(TransactionError):
    pass


class LockTimeoutError(TransactionError):
    pass


class TransactionCommittedDurabilityError(TransactionError):
    """The rename committed, but directory durability could not be confirmed."""

    committed = True

    def __init__(
        self, path: Path | str, contract: MutableMapping[str, Any], cause: OSError
    ) -> None:
        self.path = Path(path)
        self.contract = copy.deepcopy(dict(contract))
        self.revision = self.contract.get("revision")
        self.cause = cause
        super().__init__(
            f"contract revision {self.revision} was already committed at {self.path}, "
            "but directory fsync failed; durability is uncertain and callers must "
            "not retry automatically"
        )


ContractOperation = Callable[[MutableMapping[str, Any]], Any]


@dataclass(frozen=True)
class _ResolutionIntent:
    gate_id: str
    blocker_id: str
    resolution: str
    evidence_ids: tuple[str, ...]
    actor: str
    at: str
    workspace_root: Path


def _require_supported_platform() -> None:
    if (
        os.name != "posix"
        or fcntl is None
        or not hasattr(os, "O_NOFOLLOW")
        or not hasattr(os, "O_DIRECTORY")
    ):
        raise UnsupportedPlatformError(
            "contract transactions require POSIX flock, O_NOFOLLOW, and O_DIRECTORY"
        )


def _absolute_path_without_symlinks(path: Path) -> Path:
    candidate = path if path.is_absolute() else Path.cwd() / path
    candidate = Path(os.path.abspath(candidate))
    if candidate.name in {"", ".", ".."}:
        raise UnsafeContractPathError("contract path must name a file")
    current = Path(candidate.anchor)
    for part in candidate.parts[1:]:
        current = current / part
        if current.is_symlink():
            # macOS exposes root-owned compatibility aliases such as /var ->
            # /private/var.  They are outside the caller-controlled path while
            # symlinks at any deeper component can redirect the transaction.
            if current.parent == Path(candidate.anchor):
                continue
            raise UnsafeContractPathError(
                f"contract path must not contain symbolic links: {current}"
            )
    return candidate


def _open_regular_at(parent_fd: int, name: str, flags: int, mode: int = 0o600) -> int:
    try:
        descriptor = os.open(
            name,
            flags | os.O_NOFOLLOW,
            mode,
            dir_fd=parent_fd,
        )
    except OSError as error:
        if error.errno in {errno.ELOOP, errno.ENOTDIR}:
            raise UnsafeContractPathError(
                f"transaction path is not a regular non-symlink file: {name}"
            ) from error
        raise
    if not stat.S_ISREG(os.fstat(descriptor).st_mode):
        os.close(descriptor)
        raise UnsafeContractPathError(f"transaction path is not a regular file: {name}")
    return descriptor


def _acquire_lock(lock_fd: int, timeout: float) -> None:
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout < 0:
        raise ValueError("lock_timeout must be a non-negative number")
    deadline = time.monotonic() + float(timeout)
    while True:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except BlockingIOError as error:
            if time.monotonic() >= deadline:
                raise LockTimeoutError(
                    f"timed out after {float(timeout):g}s waiting for contract lock"
                ) from error
            time.sleep(min(0.01, max(0.0, deadline - time.monotonic())))


def _load_from_fd(descriptor: int) -> dict[str, Any]:
    with os.fdopen(os.dup(descriptor), "r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TransactionError("course contract root must be an object")
    return value


def _write_atomic_at(
    parent_fd: int,
    name: str,
    contract: dict[str, Any],
    contract_path: Path,
) -> None:
    temporary_name: str | None = None
    temporary_fd: int | None = None
    for _ in range(100):
        candidate = f".{name}.{secrets.token_hex(8)}.tmp"
        try:
            temporary_fd = _open_regular_at(
                parent_fd, candidate, os.O_WRONLY | os.O_CREAT | os.O_EXCL
            )
        except FileExistsError:
            continue
        temporary_name = candidate
        break
    if temporary_fd is None or temporary_name is None:
        raise TransactionError("could not allocate a same-directory transaction file")
    try:
        with os.fdopen(temporary_fd, "w", encoding="utf-8") as handle:
            json.dump(contract, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        temporary_fd = None
        os.replace(
            temporary_name,
            name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        temporary_name = None
        try:
            os.fsync(parent_fd)
        except OSError as error:
            raise TransactionCommittedDurabilityError(
                contract_path, contract, error
            ) from error
    finally:
        if temporary_fd is not None:
            os.close(temporary_fd)
        if temporary_name is not None:
            try:
                os.unlink(temporary_name, dir_fd=parent_fd)
            except FileNotFoundError:
                pass


def _validation_error(contract: MutableMapping[str, Any]) -> str | None:
    from src.course_contract import validate_contract

    issues = validate_contract(contract)
    if not issues:
        return None
    return "; ".join(f"{issue.path}: {issue.message}" for issue in issues)


def _require_append_only_prefix(
    before: MutableMapping[str, Any],
    after: MutableMapping[str, Any],
    field: str,
) -> None:
    old = before.get(field)
    new = after.get(field)
    if not isinstance(old, list) or not isinstance(new, list):
        raise TransactionError(f"append-only history is invalid at $.{field}")
    if len(new) < len(old) or new[: len(old)] != old:
        raise TransactionError(f"append-only history changed at $.{field}")


def _require_external_action_history(
    before: MutableMapping[str, Any],
    after: MutableMapping[str, Any],
    external_transition: tuple[str, str, str] | None,
) -> None:
    """Protect proposal identity while leaving Task 4 lifecycle state mutable.

    Existing actions cannot be removed or reordered. Proposal/basis fields and
    an issued authorization are immutable. Status may advance only along the
    governed single-use lifecycle.
    """

    old_actions = before.get("external_actions")
    new_actions = after.get("external_actions")
    if not isinstance(old_actions, list) or not isinstance(new_actions, list):
        raise TransactionError("append-only history is invalid at $.external_actions")
    if len(new_actions) < len(old_actions):
        raise TransactionError("append-only history changed at $.external_actions")
    immutable_fields = {
        "id",
        "kind",
        "manifest_path",
        "manifest_sha256",
        "proposed_by",
        "proposed_at",
    }
    allowed_transitions = {
        "PUBLISH_APPROVAL_REQUIRED": {"PUBLISH_APPROVAL_REQUIRED", "AUTHORIZED"},
        "AUTHORIZED": {"AUTHORIZED", "EXECUTING", "INVALIDATED"},
        "EXECUTING": {"CONSUMED", "FAILED"},
        "CONSUMED": {"CONSUMED"},
        "FAILED": {"FAILED"},
        "INVALIDATED": {"INVALIDATED"},
    }
    for index, old in enumerate(old_actions):
        new = new_actions[index]
        if not isinstance(old, dict) or not isinstance(new, dict):
            raise TransactionError(
                f"append-only history changed at $.external_actions[{index}]"
            )
        if any(new.get(field) != old.get(field) for field in immutable_fields):
            raise TransactionError(
                f"append-only history changed at $.external_actions[{index}]"
            )
        old_status = old.get("status")
        new_status = new.get("status")
        if new_status not in allowed_transitions.get(old_status, set()):
            raise TransactionError(
                "external action lifecycle moved backward or skipped a state at "
                f"$.external_actions[{index}].status"
            )
        if new_status != old_status:
            permitted_automatic = (
                old_status == "AUTHORIZED" and new_status == "INVALIDATED"
            )
            permitted_dedicated = external_transition == (
                str(old.get("id")), str(old_status), str(new_status)
            )
            if not permitted_automatic and not permitted_dedicated:
                raise TransactionError(
                    "external action lifecycle may advance only through its "
                    "dedicated atomic transaction API"
                )
        old_authorization = old.get("authorization")
        if old_authorization is not None and new.get("authorization") != old_authorization:
            raise TransactionError(
                "append-only authorization history changed at "
                f"$.external_actions[{index}].authorization"
            )
        for field in ("approval_basis_sha256", "authorized_revision"):
            if old.get(field) is not None and new.get(field) != old.get(field):
                raise TransactionError(
                    "append-only authorization history changed at "
                    f"$.external_actions[{index}].{field}"
                )
        if old.get("status") in {"CONSUMED", "FAILED", "INVALIDATED"} and new != old:
            raise TransactionError(
                f"terminal external action changed at $.external_actions[{index}]"
            )


def _invalidate_or_block_live_authorizations(
    before: MutableMapping[str, Any], after: MutableMapping[str, Any]
) -> None:
    old_actions = before.get("external_actions")
    new_actions = after.get("external_actions")
    if not isinstance(old_actions, list) or not isinstance(new_actions, list):
        return
    for index, old in enumerate(old_actions):
        if index >= len(new_actions) or not isinstance(old, dict) or not isinstance(new_actions[index], dict):
            continue
        new = new_actions[index]
        if old.get("status") == "AUTHORIZED" and new.get("status") == "AUTHORIZED":
            new["status"] = "INVALIDATED"
        elif old.get("status") == "EXECUTING" and new.get("status") == "EXECUTING":
            raise TransactionError(
                "contract mutation is prohibited while an external action is executing"
            )


def _verify_resolution_event(
    intent: _ResolutionIntent,
    resolution_id: str,
    appended_events: list[Any],
) -> None:
    from src.course_evidence import canonical_json_bytes

    matches = [
        event
        for event in appended_events
        if isinstance(event, dict)
        and event.get("kind") == "gate_blocker_resolution"
        and event.get("id") == resolution_id
        and event.get("blocker_id") == intent.blocker_id
    ]
    if len(matches) != 1:
        raise TransactionError(
            f"blocker resolution history is incomplete at $.gates.{intent.gate_id}"
        )
    event = matches[0]
    required_fields = {
        "id",
        "kind",
        "blocker_id",
        "resolution",
        "evidence_ids",
        "consumed_evidence",
        "actor",
        "at",
    }
    if set(event) != required_fields:
        raise TransactionError(
            f"blocker resolution history is incomplete at $.gates.{intent.gate_id}"
        )
    payload = {
        "blocker_id": intent.blocker_id,
        "resolution": event.get("resolution"),
        "evidence_ids": event.get("evidence_ids"),
        "actor": event.get("actor"),
        "at": event.get("at"),
    }
    if payload != {
        "blocker_id": intent.blocker_id,
        "resolution": intent.resolution,
        "evidence_ids": list(intent.evidence_ids),
        "actor": intent.actor,
        "at": intent.at,
    }:
        raise TransactionError(
            "blocker resolution history does not match the dedicated atomic "
            f"resolution request at $.gates.{intent.gate_id}"
        )
    expected_id = (
        "resolution-"
        + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()[:24]
    )
    if resolution_id != expected_id:
        raise TransactionError(
            f"blocker resolution history id is invalid at $.gates.{intent.gate_id}"
        )


def _require_gate_history(
    before: MutableMapping[str, Any],
    after: MutableMapping[str, Any],
    resolution_intent: _ResolutionIntent | None,
) -> None:
    old_gates = before.get("gates")
    new_gates = after.get("gates")
    if not isinstance(old_gates, dict) or not isinstance(new_gates, dict):
        raise TransactionError("append-only history is invalid at $.gates")
    used_resolution = False
    for gate_id, old_gate in old_gates.items():
        new_gate = new_gates.get(gate_id)
        if not isinstance(old_gate, dict) or not isinstance(new_gate, dict):
            raise TransactionError(f"append-only history changed at $.gates.{gate_id}")
        old_events = old_gate.get("evidence")
        new_events = new_gate.get("evidence")
        if not isinstance(old_events, list) or not isinstance(new_events, list):
            raise TransactionError(
                f"append-only history is invalid at $.gates.{gate_id}.evidence"
            )
        if len(new_events) < len(old_events) or new_events[: len(old_events)] != old_events:
            raise TransactionError(
                f"append-only history changed at $.gates.{gate_id}.evidence"
            )
        appended_events = new_events[len(old_events) :]
        old_risks = old_gate.get("risks")
        new_risks = new_gate.get("risks")
        if not isinstance(old_risks, list) or not isinstance(new_risks, list):
            raise TransactionError(
                f"append-only history is invalid at $.gates.{gate_id}.risks"
            )
        if len(new_risks) < len(old_risks):
            raise TransactionError(
                f"append-only history changed at $.gates.{gate_id}.risks"
            )
        for index, old_risk in enumerate(old_risks):
            new_risk = new_risks[index]
            if not isinstance(old_risk, dict) or not isinstance(new_risk, dict):
                if new_risk != old_risk:
                    raise TransactionError(
                        f"append-only history changed at $.gates.{gate_id}.risks[{index}]"
                    )
                continue
            if (
                old_risk.get("id") != new_risk.get("id")
                or old_risk.get("kind") != new_risk.get("kind")
            ):
                raise TransactionError(
                    f"append-only history changed at $.gates.{gate_id}.risks[{index}]"
                )
            if old_risk.get("kind") != "gate_blocker":
                continue
            if old_risk.get("resolved") is True:
                if new_risk != old_risk:
                    raise TransactionError(
                        "resolved blocker history changed at "
                        f"$.gates.{gate_id}.risks[{index}]"
                    )
                continue
            if new_risk == old_risk:
                continue
            expected = dict(old_risk)
            resolution_id = new_risk.get("resolution_id")
            expected["resolved"] = True
            expected["resolution_id"] = resolution_id
            if (
                new_risk != expected
                or not isinstance(resolution_id, str)
                or resolution_intent is None
                or resolution_intent.gate_id != gate_id
                or resolution_intent.blocker_id != old_risk.get("id")
                or used_resolution
            ):
                raise TransactionError(
                    "unresolved blocker may be resolved only through the dedicated "
                    "atomic resolution API "
                    f"at $.gates.{gate_id}.risks[{index}]"
                )
            _verify_resolution_event(
                resolution_intent,
                resolution_id,
                appended_events,
            )
            used_resolution = True
    if resolution_intent is not None and not used_resolution:
        raise TransactionError(
            "dedicated atomic resolution API did not resolve the requested blocker"
        )


def _require_append_only_history(
    before: MutableMapping[str, Any],
    after: MutableMapping[str, Any],
    resolution_intent: _ResolutionIntent | None,
    external_transition: tuple[str, str, str] | None,
) -> None:
    if before.get("contract_instance_id") != after.get("contract_instance_id"):
        raise TransactionError("immutable contract_instance_id changed")
    if before.get("identity") != after.get("identity"):
        raise TransactionError("immutable contract identity changed")
    if before.get("governance") != after.get("governance"):
        raise TransactionError("immutable contract governance changed")
    for field in (
        "changes",
        "evidence_archive",
        "evidence_index",
        "consumed_trial_receipts",
    ):
        _require_append_only_prefix(before, after, field)
    _require_external_action_history(before, after, external_transition)
    _require_gate_history(before, after, resolution_intent)


def _run_contract_transaction(
    path: Path | str,
    operation: ContractOperation | None,
    *,
    expected_revision: int | None = None,
    lock_timeout: float = 10.0,
    resolution_intent: _ResolutionIntent | None = None,
    external_transition: tuple[str, str, str] | None = None,
) -> dict[str, Any]:
    _require_supported_platform()
    if (operation is None) == (resolution_intent is None):
        raise TransactionError(
            "transaction control flow requires exactly one mutation mode"
        )
    if resolution_intent is not None and external_transition is not None:
        raise TransactionError("transaction control flow modes cannot be combined")
    if operation is not None and not callable(operation):
        raise TypeError("operation must be callable")
    if expected_revision is not None and (
        isinstance(expected_revision, bool)
        or not isinstance(expected_revision, int)
        or expected_revision < 0
    ):
        raise ValueError("expected_revision must be a non-negative integer")

    contract_path = _absolute_path_without_symlinks(Path(path))
    parent_fd = os.open(
        contract_path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    )
    lock_fd: int | None = None
    contract_fd: int | None = None
    try:
        lock_name = f".{contract_path.name}.lock"
        for attempt in range(5):
            try:
                lock_fd = _open_regular_at(
                    parent_fd, lock_name, os.O_RDWR | os.O_CREAT, mode=0o600
                )
                break
            except FileNotFoundError:
                if attempt == 4:
                    raise
                time.sleep(0.001)
        if lock_fd is None:  # defensive; the bounded loop either opens or raises
            raise TransactionError("could not open contract lock file")
        _acquire_lock(lock_fd, lock_timeout)
        contract_fd = _open_regular_at(parent_fd, contract_path.name, os.O_RDONLY)
        loaded_contract = _load_from_fd(contract_fd)
        before = copy.deepcopy(loaded_contract)
        contract = loaded_contract

        schema_version = contract.get("schema_version")
        original_revision = contract.get("revision")
        legacy = schema_version in {1, 2} and original_revision is None
        if not legacy:
            if (
                isinstance(original_revision, bool)
                or not isinstance(original_revision, int)
                or original_revision < 0
            ):
                raise TransactionError("contract revision must be a non-negative integer")
            details = _validation_error(contract)
            if details:
                raise TransactionError(f"refusing to mutate invalid contract: {details}")
            base_revision = original_revision
        else:
            base_revision = -1

        if expected_revision is not None and base_revision != expected_revision:
            raise RevisionConflictError(
                f"revision conflict: expected {expected_revision}, found {base_revision}"
            )

        if resolution_intent is None:
            assert operation is not None
            operation(contract)
        else:
            from src.course_contract import resolve_gate_blocker

            resolve_gate_blocker(
                contract,
                resolution_intent.gate_id,
                resolution_intent.blocker_id,
                resolution_intent.resolution,
                list(resolution_intent.evidence_ids),
                resolution_intent.actor,
                resolution_intent.at,
                workspace_root=resolution_intent.workspace_root,
            )
        _invalidate_or_block_live_authorizations(before, contract)
        after_operation_revision = contract.get("revision")
        if legacy:
            if after_operation_revision not in {None, 0}:
                raise TransactionError("legacy migration attempted to own contract revision")
        elif after_operation_revision != base_revision:
            raise TransactionError(
                "operation changed revision; the transaction is the single revision owner"
            )
        contract["revision"] = base_revision + 1

        if not legacy:
            _require_append_only_history(
                before,
                contract,
                resolution_intent,
                external_transition,
            )
        details = _validation_error(contract)
        if details:
            raise TransactionError(f"mutation produced an invalid contract: {details}")

        committed = copy.deepcopy(dict(contract))
        _write_atomic_at(parent_fd, contract_path.name, committed, contract_path)
        return committed
    finally:
        if contract_fd is not None:
            os.close(contract_fd)
        if lock_fd is not None:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            finally:
                os.close(lock_fd)
        os.close(parent_fd)


def mutate_contract_atomic(
    path: Path | str,
    operation: ContractOperation,
    *,
    expected_revision: int | None = None,
    lock_timeout: float = 10.0,
) -> dict[str, Any]:
    """Apply a mutation; existing blocker resolution is always forbidden."""

    return _run_contract_transaction(
        path,
        operation,
        expected_revision=expected_revision,
        lock_timeout=lock_timeout,
    )


def authorize_external_action_atomic(
    path: Path | str,
    action_id: str,
    receipt: Mapping[str, Any],
    authorized_at: str,
    *,
    expected_revision: int | None = None,
    lock_timeout: float = 10.0,
) -> dict[str, Any]:
    from src.course_contract import authorize_external_action

    return _run_contract_transaction(
        path,
        lambda contract: authorize_external_action(
            contract, action_id, receipt, authorized_at
        ),
        expected_revision=expected_revision,
        lock_timeout=lock_timeout,
        external_transition=(action_id, "PUBLISH_APPROVAL_REQUIRED", "AUTHORIZED"),
    )


def begin_external_action_execution_atomic(
    path: Path | str,
    action_id: str,
    manifest_sha256: str,
    proposal_revision: int,
    at: str,
    *,
    expected_revision: int | None = None,
    lock_timeout: float = 10.0,
) -> dict[str, Any]:
    from src.course_contract import begin_external_action_execution

    return _run_contract_transaction(
        path,
        lambda contract: begin_external_action_execution(
            contract, action_id, manifest_sha256, proposal_revision, at
        ),
        expected_revision=expected_revision,
        lock_timeout=lock_timeout,
        external_transition=(action_id, "AUTHORIZED", "EXECUTING"),
    )


def finish_external_action_execution_atomic(
    path: Path | str,
    action_id: str,
    status: str,
    modified_targets: Sequence[str],
    at: str,
    error: str | None = None,
    *,
    expected_revision: int | None = None,
    lock_timeout: float = 10.0,
) -> dict[str, Any]:
    from src.course_contract import finish_external_action_execution

    if status not in {"CONSUMED", "FAILED"}:
        raise ValueError("external action terminal status must be CONSUMED or FAILED")
    return _run_contract_transaction(
        path,
        lambda contract: finish_external_action_execution(
            contract, action_id, status, modified_targets, at, error
        ),
        expected_revision=expected_revision,
        lock_timeout=lock_timeout,
        external_transition=(action_id, "EXECUTING", status),
    )


def resolve_gate_blocker_atomic(
    path: Path | str,
    gate_id: str,
    blocker_id: str,
    resolution: str,
    evidence_ids: Sequence[str],
    actor: str,
    at: str,
    *,
    workspace_root: Path | str | None = None,
    expected_revision: int | None = None,
    lock_timeout: float = 10.0,
) -> dict[str, Any]:
    """Resolve exactly one existing blocker inside the transaction control flow."""

    evidence_id_list = list(evidence_ids)
    evidence_root = (
        Path(workspace_root) if workspace_root is not None else Path(path).parent
    )
    intent = _ResolutionIntent(
        gate_id=gate_id,
        blocker_id=blocker_id,
        resolution=resolution,
        evidence_ids=tuple(evidence_id_list),
        actor=actor,
        at=at,
        workspace_root=evidence_root,
    )

    return _run_contract_transaction(
        path,
        None,
        expected_revision=expected_revision,
        lock_timeout=lock_timeout,
        resolution_intent=intent,
    )
