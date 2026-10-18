from __future__ import annotations

import copy
import errno
import hashlib
import json
import os
import secrets
import stat
import time
from pathlib import Path
from typing import Any, Callable, MutableMapping

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


class _TrackedContract(dict[str, Any]):
    """A transaction-local dict carrying non-serialized domain transition intents."""

    def __init__(self, value: dict[str, Any]) -> None:
        super().__init__(value)
        self.blocker_resolution_transitions: list[tuple[str, str, str]] = []

    def _record_blocker_resolution_transition(
        self, gate_id: str, blocker_id: str, resolution_id: str
    ) -> None:
        self.blocker_resolution_transitions.append(
            (gate_id, blocker_id, resolution_id)
        )


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
    before: MutableMapping[str, Any], after: MutableMapping[str, Any]
) -> None:
    """Protect proposal identity while leaving Task 4 lifecycle state mutable.

    Existing actions cannot be removed or reordered.  Proposal/basis fields and
    an issued authorization are immutable; status and future execution metadata
    remain mutable so the release lifecycle can advance transactionally.
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
        old_authorization = old.get("authorization")
        if old_authorization is not None and new.get("authorization") != old_authorization:
            raise TransactionError(
                "append-only authorization history changed at "
                f"$.external_actions[{index}].authorization"
            )


def _verify_resolution_event(
    gate_id: str,
    blocker_id: str,
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
        and event.get("blocker_id") == blocker_id
    ]
    if len(matches) != 1:
        raise TransactionError(
            f"blocker resolution history is incomplete at $.gates.{gate_id}"
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
            f"blocker resolution history is incomplete at $.gates.{gate_id}"
        )
    payload = {
        "blocker_id": blocker_id,
        "resolution": event.get("resolution"),
        "evidence_ids": event.get("evidence_ids"),
        "actor": event.get("actor"),
        "at": event.get("at"),
    }
    expected_id = (
        "resolution-"
        + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()[:24]
    )
    if resolution_id != expected_id:
        raise TransactionError(
            f"blocker resolution history id is invalid at $.gates.{gate_id}"
        )


def _require_gate_history(
    before: MutableMapping[str, Any],
    after: MutableMapping[str, Any],
    authorized_resolutions: list[tuple[str, str, str]],
) -> None:
    old_gates = before.get("gates")
    new_gates = after.get("gates")
    if not isinstance(old_gates, dict) or not isinstance(new_gates, dict):
        raise TransactionError("append-only history is invalid at $.gates")
    authorized = set(authorized_resolutions)
    if len(authorized) != len(authorized_resolutions):
        raise TransactionError("duplicate blocker resolution API transition")
    used: set[tuple[str, str, str]] = set()
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
            transition = (gate_id, str(old_risk.get("id")), str(resolution_id))
            if (
                new_risk != expected
                or not isinstance(resolution_id, str)
                or transition not in authorized
            ):
                raise TransactionError(
                    "unresolved blocker may be resolved only through the resolution API "
                    f"at $.gates.{gate_id}.risks[{index}]"
                )
            _verify_resolution_event(
                gate_id,
                str(old_risk.get("id")),
                resolution_id,
                appended_events,
            )
            used.add(transition)
    if used != authorized:
        raise TransactionError(
            "blocker resolution API transition did not resolve an existing blocker"
        )


def _require_append_only_history(
    before: MutableMapping[str, Any],
    after: MutableMapping[str, Any],
    authorized_resolutions: list[tuple[str, str, str]],
) -> None:
    for field in (
        "changes",
        "evidence_archive",
        "evidence_index",
        "consumed_trial_receipts",
    ):
        _require_append_only_prefix(before, after, field)
    _require_external_action_history(before, after)
    _require_gate_history(before, after, authorized_resolutions)


def mutate_contract_atomic(
    path: Path | str,
    operation: ContractOperation,
    *,
    expected_revision: int | None = None,
    lock_timeout: float = 10.0,
) -> dict[str, Any]:
    """Apply one validated, history-preserving mutation under a POSIX lock."""

    _require_supported_platform()
    if not callable(operation):
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
        contract = _TrackedContract(loaded_contract)

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

        operation(contract)
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
                contract.blocker_resolution_transitions,
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
