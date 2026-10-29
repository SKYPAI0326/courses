from __future__ import annotations

import copy
from pathlib import PurePosixPath
from typing import Any, Mapping, MutableMapping

from src.course_contract import ContractStateError
from src.course_evidence import materialize_json_evidence
from src.course_gate import validate_and_transition_gate


def _route_blueprint_to_g2(contract: MutableMapping[str, Any], record: Mapping[str, Any], record_path: str, actor: str, at: str, *, workspace_root) -> str:
    gates = contract.get("gates")
    if not isinstance(gates, Mapping) or any(gates.get(gate, {}).get("status") != "PASS" for gate in ("G0", "G1")):
        raise ContractStateError("blueprint routing requires G0 and G1 PASS")
    if gates.get("G2", {}).get("status") != "IN_PROGRESS":
        raise ContractStateError("blueprint routing requires G2 IN_PROGRESS")
    path = PurePosixPath(record_path)
    if not record_path.strip() or path.is_absolute() or ".." in path.parts:
        raise ContractStateError("blueprint record path must be a safe relative path")
    blueprint_id = record.get("blueprint_id")
    evidence_id = f"g2-{blueprint_id}" if isinstance(blueprint_id, str) else "g2-invalid-blueprint"
    if any(isinstance(item, Mapping) and item.get("id") == evidence_id for item in contract.get("evidence_index", [])):
        raise ContractStateError(f"blueprint evidence id already exists: {evidence_id}")
    contract["G2_architecture"] = copy.deepcopy(dict(record))
    reference = materialize_json_evidence(
        workspace_root, evidence_id=evidence_id, gate_id="G2", kind="course_blueprint",
        relative_path=record_path, value=record,
    )
    contract["evidence_index"].append(reference)
    return validate_and_transition_gate(contract, "G2", [evidence_id], workspace_root, actor, at)


def route_blueprint_to_g2(contract: MutableMapping[str, Any], record: Mapping[str, Any], record_path: str, actor: str, at: str, *, workspace_root) -> str:
    staged = copy.deepcopy(contract)
    result = _route_blueprint_to_g2(staged, record, record_path, actor, at, workspace_root=workspace_root)
    contract.clear()
    contract.update(staged)
    return result
