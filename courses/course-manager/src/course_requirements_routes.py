from __future__ import annotations

import copy
from pathlib import PurePosixPath
from typing import Any, Mapping, MutableMapping

from src.course_contract import ContractStateError
from src.course_evidence import materialize_json_evidence
from src.course_gate import validate_and_transition_gate


def _route_requirements_to_g0(contract: MutableMapping[str, Any], record: Mapping[str, Any], record_path: str, actor: str, at: str, *, workspace_root) -> str:
    gates = contract.get("gates")
    if not isinstance(gates, Mapping) or gates.get("G0", {}).get("status") != "IN_PROGRESS":
        raise ContractStateError("requirements routing requires G0 IN_PROGRESS")
    path = PurePosixPath(record_path)
    if not record_path.strip() or path.is_absolute() or ".." in path.parts:
        raise ContractStateError("requirements record path must be a safe relative path")
    requirements_id = record.get("requirements_id")
    evidence_id = f"g0-{requirements_id}" if isinstance(requirements_id, str) else "g0-invalid-requirements"
    if any(isinstance(item, Mapping) and item.get("id") == evidence_id for item in contract.get("evidence_index", [])):
        raise ContractStateError(f"requirements evidence id already exists: {evidence_id}")
    contract["G0_requirements"] = copy.deepcopy(dict(record))
    reference = materialize_json_evidence(
        workspace_root, evidence_id=evidence_id, gate_id="G0", kind="requirements_record",
        relative_path=record_path, value=record,
    )
    contract["evidence_index"].append(reference)
    return validate_and_transition_gate(contract, "G0", [evidence_id], workspace_root, actor, at)


def route_requirements_to_g0(contract: MutableMapping[str, Any], record: Mapping[str, Any], record_path: str, actor: str, at: str, *, workspace_root) -> str:
    staged = copy.deepcopy(contract)
    result = _route_requirements_to_g0(staged, record, record_path, actor, at, workspace_root=workspace_root)
    contract.clear()
    contract.update(staged)
    return result
