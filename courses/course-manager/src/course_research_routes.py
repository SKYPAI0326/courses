from __future__ import annotations

import copy
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, MutableMapping

from src.course_contract import ContractStateError, block_gate
from src.course_evidence import materialize_json_evidence
from src.course_gate import validate_and_transition_gate
from src.course_research import validate_research_record


def _route_research_to_gate(
    contract: MutableMapping[str, Any],
    record: Mapping[str, Any],
    adaptation: Mapping[str, Any],
    record_path: str,
    evidence_sha256: str,
    actor: str,
    at: str,
    *,
    workspace_root: Path | str,
) -> str:
    gates = contract.get("gates")
    if not isinstance(gates, Mapping) or gates.get("G0", {}).get("status") != "PASS":
        raise ContractStateError("G1 research requires G0 PASS")
    if gates.get("G1", {}).get("status") != "IN_PROGRESS":
        raise ContractStateError("research routing requires G1 IN_PROGRESS")

    relative_path = PurePosixPath(record_path)
    if (
        not record_path.strip()
        or relative_path.is_absolute()
        or ".." in relative_path.parts
    ):
        raise ContractStateError("research record path must be a safe relative path")
    issues = validate_research_record(record, adaptation)
    contract["G1_research"] = {
        "record_path": record_path,
        "sha256": evidence_sha256,
        "validation_issue_codes": [issue.code for issue in issues],
    }
    contract["adaptation"] = copy.deepcopy(dict(adaptation))
    gates["G1"]["evidence"].append(
        {
            "kind": "research_record",
            "path": record_path,
            "sha256": evidence_sha256,
            "maturity": "STATIC_VALIDATED",
            "validation_issue_codes": [issue.code for issue in issues],
        }
    )

    if issues:
        issue_codes = ", ".join(sorted({issue.code for issue in issues}))
        block_gate(
            contract,
            "G1",
            f"research validation failed: {issue_codes}",
            actor,
            at,
        )
        return "BLOCKED"

    reference = materialize_json_evidence(
        workspace_root,
        evidence_id="g1-research",
        gate_id="G1",
        kind="research_record",
        relative_path=record_path,
        value=record,
    )
    contract["G1_research"]["sha256"] = reference["sha256"]
    gates["G1"]["evidence"][-1]["sha256"] = reference["sha256"]
    contract["evidence_index"].append(reference)

    return validate_and_transition_gate(
        contract,
        "G1",
        ["g1-research"],
        workspace_root,
        actor,
        at,
    )


def route_research_to_gate(
    contract: MutableMapping[str, Any],
    record: Mapping[str, Any],
    adaptation: Mapping[str, Any],
    record_path: str,
    evidence_sha256: str,
    actor: str,
    at: str,
    *,
    workspace_root: Path | str,
) -> str:
    staged = copy.deepcopy(contract)
    result = _route_research_to_gate(
        staged,
        record,
        adaptation,
        record_path,
        evidence_sha256,
        actor,
        at,
        workspace_root=workspace_root,
    )
    contract.clear()
    contract.update(staged)
    return result
