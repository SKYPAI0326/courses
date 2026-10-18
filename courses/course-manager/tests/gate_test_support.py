from __future__ import annotations

from typing import Any, MutableMapping, Sequence

from src.course_contract import ContractStateError


def _commit_gate_pass(
    contract: MutableMapping[str, Any],
    gate_id: str,
    evidence_ids: Sequence[str],
    validator_id: str,
    actor: str,
    at: str,
) -> None:
    """Test-only prerequisite fixture; production PASS uses course_gate."""
    if not evidence_ids:
        raise ContractStateError("test Gate fixture requires evidence")
    gate_number = int(gate_id[1:])
    for index in range(gate_number):
        if contract["gates"][f"G{index}"]["status"] != "PASS":
            raise ContractStateError("test Gate fixture requires previous PASS")
    record = contract["gates"][gate_id]
    if record.get("status") != "IN_PROGRESS":
        raise ContractStateError("test Gate fixture requires IN_PROGRESS")
    if any(
        isinstance(item, dict)
        and item.get("blocking") is True
        and item.get("resolved") is not True
        for item in record.get("risks", [])
    ):
        raise ContractStateError("test Gate fixture refuses unresolved blockers")
    indexed = {
        item.get("id"): item
        for item in contract.get("evidence_index", [])
        if isinstance(item, dict)
    }
    if any(evidence_id not in indexed for evidence_id in evidence_ids):
        raise ContractStateError("test Gate fixture requires indexed evidence")
    if any(indexed[evidence_id].get("gate") != gate_id for evidence_id in evidence_ids):
        raise ContractStateError("test Gate fixture requires same-Gate evidence")
    record["status"] = "PASS"
    revision = record.get("source_revision")
    record["source_revision"] = revision + 1 if isinstance(revision, int) else 1
    record["evidence"].append(
        {
            "kind": "gate_validation",
            "outcome": "PASS",
            "validator_id": validator_id,
            "actor": actor,
            "at": at,
            "evidence_ids": list(evidence_ids),
        }
    )
