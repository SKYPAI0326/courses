from __future__ import annotations

import copy
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, MutableMapping

from src.course_content import SHA256_PATTERN, validate_lesson_record
from src.course_contract import ContractStateError, block_gate
from src.course_evidence import materialize_json_evidence
from src.course_gate import validate_and_transition_gate


def _route_content_to_g3(
    contract: MutableMapping[str, Any],
    record: Mapping[str, Any],
    record_path: str,
    sha256: str,
    actor: str,
    at: str,
    *,
    workspace_root: Path | str,
) -> str:
    gates = contract.get("gates")
    if not isinstance(gates, Mapping) or any(
        gates.get(gate_id, {}).get("status") != "PASS"
        for gate_id in ("G0", "G1", "G2")
    ):
        raise ContractStateError("G3 content requires G0, G1, and G2 PASS")
    if gates.get("G3", {}).get("status") != "IN_PROGRESS":
        raise ContractStateError("content routing requires G3 IN_PROGRESS")
    relative_path = PurePosixPath(record_path)
    if (
        not record_path.strip()
        or relative_path.is_absolute()
        or ".." in relative_path.parts
    ):
        raise ContractStateError("lesson record path must be a safe relative path")
    if not SHA256_PATTERN.fullmatch(sha256):
        raise ContractStateError(
            "lesson record SHA-256 must be 64 lowercase hex characters"
        )

    issues = validate_lesson_record(record)
    unit_id = (
        record.get("unit_id")
        if isinstance(record.get("unit_id"), str)
        else "invalid-unit"
    )
    evidence_id = f"g3-{unit_id}"
    contract["G3_lesson_design"] = {
        "record_path": record_path,
        "sha256": sha256,
        "unit_id": unit_id,
        "validation_issue_codes": [issue.code for issue in issues],
    }
    gates["G3"]["evidence"].append(
        {
            "kind": "lesson_record",
            "path": record_path,
            "sha256": sha256,
            "maturity": "STATIC_VALIDATED",
            "validation_issue_codes": [issue.code for issue in issues],
        }
    )
    if issues:
        block_gate(
            contract,
            "G3",
            "lesson validation failed: "
            + ", ".join(sorted({issue.code for issue in issues})),
            actor,
            at,
        )
        return "BLOCKED"

    if any(
        isinstance(item, Mapping) and item.get("id") == evidence_id
        for item in contract["evidence_index"]
    ):
        raise ContractStateError(f"lesson evidence id already exists: {evidence_id}")
    reference = materialize_json_evidence(
        workspace_root,
        evidence_id=evidence_id,
        gate_id="G3",
        kind="lesson_record",
        relative_path=record_path,
        value=record,
    )
    contract["G3_lesson_design"]["sha256"] = reference["sha256"]
    gates["G3"]["evidence"][-1]["sha256"] = reference["sha256"]
    contract["evidence_index"].append(reference)

    return validate_and_transition_gate(
        contract,
        "G3",
        [evidence_id],
        workspace_root,
        actor,
        at,
    )


def route_content_to_g3(
    contract: MutableMapping[str, Any],
    record: Mapping[str, Any],
    record_path: str,
    sha256: str,
    actor: str,
    at: str,
    *,
    workspace_root: Path | str,
) -> str:
    staged = copy.deepcopy(contract)
    result = _route_content_to_g3(
        staged,
        record,
        record_path,
        sha256,
        actor,
        at,
        workspace_root=workspace_root,
    )
    contract.clear()
    contract.update(staged)
    return result
