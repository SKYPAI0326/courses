from __future__ import annotations

import copy
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, MutableMapping, Sequence

from src.course_content import SHA256_PATTERN, validate_lesson_collection
from src.course_contract import ContractStateError
from src.course_evidence import materialize_json_evidence
from src.course_gate import validate_and_transition_gate
from src.course_governance import single_governed_value


def _route_content_to_g3(
    contract: MutableMapping[str, Any], records: Sequence[Mapping[str, Any]],
    record_paths: Sequence[str], sha256s: Sequence[str], actor: str, at: str,
    *, workspace_root: Path | str,
) -> str:
    gates = contract.get("gates")
    if not isinstance(gates, Mapping) or any(
        gates.get(gate_id, {}).get("status") != "PASS"
        for gate_id in ("G0", "G1", "G2")
    ):
        raise ContractStateError("G3 content requires G0, G1, and G2 PASS")
    if gates.get("G3", {}).get("status") != "IN_PROGRESS":
        raise ContractStateError("content routing requires G3 IN_PROGRESS")
    if not records or not (len(records) == len(record_paths) == len(sha256s)):
        raise ContractStateError("G3 requires aligned lesson records, paths, and hashes")
    for record_path, sha256 in zip(record_paths, sha256s):
        relative_path = PurePosixPath(record_path)
        if not record_path.strip() or relative_path.is_absolute() or ".." in relative_path.parts:
            raise ContractStateError("lesson record path must be a safe relative path")
        if not SHA256_PATTERN.fullmatch(sha256):
            raise ContractStateError("lesson record SHA-256 must be 64 lowercase hex characters")
    blueprint, _ = single_governed_value(contract, "G2", "course_blueprint", workspace_root)
    if not isinstance(blueprint, Mapping) or blueprint != contract.get("G2_architecture"):
        return "BLOCKED"
    if validate_lesson_collection(records, blueprint):
        return "BLOCKED"
    references: list[dict[str, Any]] = []
    evidence_ids: list[str] = []
    for record, path in zip(records, record_paths):
        unit_id = str(record["unit_id"])
        evidence_id = f"g3-{unit_id}"
        if any(isinstance(item, Mapping) and item.get("id") == evidence_id for item in contract["evidence_index"]):
            raise ContractStateError(f"lesson evidence id already exists: {evidence_id}")
        reference = materialize_json_evidence(
            workspace_root, evidence_id=evidence_id, gate_id="G3",
            kind="lesson_record", relative_path=path, value=record,
        )
        references.append(reference)
        evidence_ids.append(evidence_id)
    contract["evidence_index"].extend(references)
    contract["G3_lesson_design"] = {
        "records": [
            {"record_path": path, "sha256": reference["sha256"], "unit_id": record["unit_id"]}
            for record, path, reference in zip(records, record_paths, references)
        ]
    }
    return validate_and_transition_gate(contract, "G3", evidence_ids, workspace_root, actor, at)


def route_content_to_g3(
    contract: MutableMapping[str, Any],
    record: Mapping[str, Any] | Sequence[Mapping[str, Any]],
    record_path: str | Sequence[str],
    sha256: str | Sequence[str],
    actor: str,
    at: str,
    *,
    workspace_root: Path | str,
) -> str:
    staged = copy.deepcopy(contract)
    result = _route_content_to_g3(
        staged,
        list(record) if isinstance(record, (list, tuple)) else [record],
        list(record_path) if isinstance(record_path, (list, tuple)) else [record_path],
        list(sha256) if isinstance(sha256, (list, tuple)) else [sha256],
        actor,
        at,
        workspace_root=workspace_root,
    )
    if result == "PASS":
        contract.clear()
        contract.update(staged)
    return result
