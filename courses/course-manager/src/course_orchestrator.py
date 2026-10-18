from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

from src.course_contract import GATE_ORDER, ContractStateError, begin_gate, load_contract
from src.course_evidence import canonical_json_bytes
from src.course_gate import validate_and_transition_gate
from src.transactions import TransactionError, mutate_contract_atomic


class OrchestrationError(RuntimeError):
    pass


PRODUCERS = {
    "G0": "course-run",
    "G1": "course-researcher",
    "G2": "course-pm",
    "G3": "course-designer",
    "G4": "build-course-page",
    "G5": "course-run",
    "G6": "course-ops",
}


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _write_json_atomic(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _latest_gate_timestamp(contract: Mapping[str, Any], gate_id: str) -> str | None:
    gate = contract.get("gates", {}).get(gate_id, {})
    evidence = gate.get("evidence", []) if isinstance(gate, Mapping) else []
    for event in reversed(evidence):
        if isinstance(event, Mapping) and _text(event.get("at")):
            return str(event["at"])
    return None


def _envelope_for_contract(
    contract_path: Path,
    workspace_root: Path,
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    gates = contract.get("gates")
    if not isinstance(gates, Mapping):
        raise OrchestrationError("contract gates are unavailable")
    current = next(
        (gate_id for gate_id in GATE_ORDER if gates.get(gate_id, {}).get("status") != "PASS"),
        None,
    )
    if current is None:
        action = "PAUSE"
        reason = "EXTERNAL_ACTION_AUTHORIZATION_REQUIRED"
        producer = "course-ops"
        requires_user_input = True
        gate_status = "PASS"
        timestamp = _latest_gate_timestamp(contract, "G6")
        gate_id = "G6"
    else:
        gate_id = current
        gate = gates[gate_id]
        gate_status = str(gate.get("status"))
        producer = PRODUCERS[gate_id]
        timestamp = _latest_gate_timestamp(contract, gate_id)
        if gate_status == "IN_PROGRESS":
            action = "DISPATCH_GATE"
            reason = "GATE_READY"
            requires_user_input = False
        elif gate_status == "BLOCKED":
            action = "PAUSE"
            reason = "EVIDENCE_INSUFFICIENT"
            requires_user_input = True
        else:
            raise OrchestrationError(
                f"orchestrator snapshot requires active or blocked Gate, got {gate_id} {gate_status}"
            )
    basis = {
        "contract_instance_id": contract.get("contract_instance_id"),
        "contract_revision": contract.get("revision"),
        "gate_id": gate_id,
        "gate_status": gate_status,
        "action": action,
        "reason": reason,
    }
    envelope_id = "dispatch-" + hashlib.sha256(canonical_json_bytes(basis)).hexdigest()[:24]
    return {
        "schema_version": 1,
        "id": envelope_id,
        "contract_instance_id": contract.get("contract_instance_id"),
        "contract_revision": contract.get("revision"),
        "contract_path": str(contract_path),
        "workspace_root": str(workspace_root),
        "gate_id": gate_id,
        "gate_status": gate_status,
        "producer": producer,
        "action": action,
        "reason": reason,
        "requires_user_input": requires_user_input,
        "at": timestamp,
    }


def _persist_envelope(state_root: Path, envelope: dict[str, Any]) -> dict[str, Any]:
    if state_root.exists() and not state_root.is_dir():
        raise OrchestrationError("state root must be a directory or absent")
    path = state_root / "dispatch" / f"{envelope['id']}.json"
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != envelope:
            raise OrchestrationError(f"dispatch envelope collision: {envelope['id']}")
        return existing
    _write_json_atomic(path, envelope)
    return envelope


def _resume_mutation(contract: dict[str, Any], actor: str, at: str) -> None:
    for gate_id in GATE_ORDER:
        status = contract["gates"][gate_id]["status"]
        if status == "PASS":
            continue
        risks = contract["gates"][gate_id].get("risks", [])
        resolved_blocked = status == "BLOCKED" and not any(
            isinstance(risk, Mapping)
            and risk.get("blocking") is True
            and risk.get("resolved") is not True
            for risk in risks
        )
        if status in {"NOT_STARTED", "FAIL", "STALE"} or resolved_blocked:
            begin_gate(contract, gate_id, actor, at)
        return


def resume_course(
    contract_path: Path | str,
    workspace_root: Path | str,
    state_root: Path | str,
    *,
    actor: str,
    at: str,
    expected_revision: int | None = None,
) -> dict[str, Any]:
    if not _text(actor) or not _text(at):
        raise OrchestrationError("resume requires actor and timestamp")
    path = Path(contract_path).absolute()
    workspace = Path(workspace_root).absolute()
    state = Path(state_root).absolute()
    contract = load_contract(path)
    first_open = next(
        (gate_id for gate_id in GATE_ORDER if contract["gates"][gate_id]["status"] != "PASS"),
        None,
    )
    first_status = (
        contract["gates"][first_open]["status"] if first_open is not None else None
    )
    first_risks = (
        contract["gates"][first_open].get("risks", [])
        if first_open is not None
        else []
    )
    resolved_blocked = first_status == "BLOCKED" and not any(
        isinstance(risk, Mapping)
        and risk.get("blocking") is True
        and risk.get("resolved") is not True
        for risk in first_risks
    )
    if first_status in {"NOT_STARTED", "FAIL", "STALE"} or resolved_blocked:
        try:
            contract = mutate_contract_atomic(
                path,
                lambda value: _resume_mutation(value, actor, at),
                expected_revision=expected_revision,
            )
        except TransactionError as error:
            raise OrchestrationError(str(error)) from error
    elif expected_revision is not None and contract.get("revision") != expected_revision:
        raise OrchestrationError(
            f"expected contract revision {expected_revision}, got {contract.get('revision')}"
        )
    return _persist_envelope(state, _envelope_for_contract(path, workspace, contract))


def _pass_evidence_ids(contract: Mapping[str, Any], gate_id: str) -> tuple[str, ...] | None:
    evidence = contract.get("gates", {}).get(gate_id, {}).get("evidence", [])
    if not isinstance(evidence, list):
        return None
    for event in reversed(evidence):
        if (
            isinstance(event, Mapping)
            and event.get("kind") == "gate_validation"
            and event.get("outcome") == "PASS"
            and isinstance(event.get("evidence_ids"), list)
        ):
            return tuple(event["evidence_ids"])
    return None


def complete_gate(
    contract_path: Path | str,
    workspace_root: Path | str,
    state_root: Path | str,
    gate_id: str,
    evidence_ids: Sequence[str],
    *,
    actor: str,
    at: str,
    expected_revision: int | None = None,
) -> dict[str, Any]:
    if gate_id not in GATE_ORDER:
        raise OrchestrationError(f"unknown Gate: {gate_id}")
    if not evidence_ids or any(not _text(item) for item in evidence_ids):
        raise OrchestrationError("complete requires one or more evidence ids")
    path = Path(contract_path).absolute()
    workspace = Path(workspace_root).absolute()
    state = Path(state_root).absolute()
    current = load_contract(path)
    status = current["gates"][gate_id]["status"]
    if status == "PASS":
        if _pass_evidence_ids(current, gate_id) != tuple(evidence_ids):
            raise OrchestrationError(
                f"{gate_id} already passed with a different evidence request"
            )
        if expected_revision is not None and current.get("revision") != expected_revision:
            raise OrchestrationError(
                f"expected contract revision {expected_revision}, got {current.get('revision')}"
            )
        return _persist_envelope(
            state, _envelope_for_contract(path, workspace, current)
        )
    if status != "IN_PROGRESS":
        raise OrchestrationError(f"cannot complete {gate_id} in {status!r} state")

    def validate_and_advance(contract: dict[str, Any]) -> None:
        result = validate_and_transition_gate(
            contract, gate_id, evidence_ids, workspace, actor, at
        )
        if result != "PASS":
            return
        index = GATE_ORDER.index(gate_id)
        if index + 1 < len(GATE_ORDER):
            begin_gate(contract, GATE_ORDER[index + 1], actor, at)

    try:
        committed = mutate_contract_atomic(
            path,
            validate_and_advance,
            expected_revision=expected_revision,
        )
    except (ContractStateError, TransactionError, OSError, ValueError) as error:
        raise OrchestrationError(str(error)) from error
    return _persist_envelope(
        state, _envelope_for_contract(path, workspace, committed)
    )


def validate_repair_fix_authority(proof: Mapping[str, Any]) -> None:
    """Validate the minimum pre-fix proof; no repair mutation is authorized here."""

    required_hashes = ("approved_plan_sha256", "backup_manifest_sha256")
    for field in required_hashes:
        value = proof.get(field)
        if not isinstance(value, str) or len(value) != 64:
            raise OrchestrationError(f"repair fix requires {field}")
    before_hashes = proof.get("before_hashes")
    if not isinstance(before_hashes, Mapping) or not before_hashes:
        raise OrchestrationError("repair fix requires before_hashes")
    if any(not _text(path) or not isinstance(digest, str) or len(digest) != 64 for path, digest in before_hashes.items()):
        raise OrchestrationError("repair before_hashes are invalid")
    restore = proof.get("isolated_restore_proof")
    if not isinstance(restore, Mapping) or restore.get("verified") is not True:
        raise OrchestrationError("repair fix requires isolated_restore_proof")
    if restore.get("restored_hashes") != before_hashes:
        raise OrchestrationError("repair restore proof does not match before_hashes")


def dispatch_repair_fix(proof: Mapping[str, Any]) -> None:
    validate_repair_fix_authority(proof)
    raise OrchestrationError(
        "repair fix transaction is not implemented; Task 8 integration is BLOCKED"
    )
