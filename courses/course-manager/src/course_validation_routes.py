from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Sequence

from src.course_contract import ContractStateError
from src.course_gate import validate_and_transition_gate


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _route_verified_trial_to_gate(
    contract: MutableMapping[str, Any],
    gate_id: str,
    production_evidence_ids: Sequence[str],
    trial_evidence_id: str,
    trial_receipt_evidence_id: str,
    actor: str,
    at: str,
    *,
    workspace_root: Path | str,
) -> str:
    if gate_id not in {"G4", "G5"}:
        raise ValueError("independent course trials may pass only G4 or G5")
    if not production_evidence_ids or any(not _text(item) for item in production_evidence_ids):
        raise ValueError("production evidence is required before a trial can pass a gate")
    evidence_index = contract.get("evidence_index")
    if not isinstance(evidence_index, list):
        raise ContractStateError("contract evidence index is missing")
    indexed = {
        item.get("id"): item
        for item in evidence_index
        if isinstance(item, Mapping) and _text(item.get("id"))
    }
    requested_ids = [*production_evidence_ids, trial_evidence_id, trial_receipt_evidence_id]
    missing = [item for item in requested_ids if item not in indexed]
    if missing:
        raise ContractStateError(
            f"trial route references unindexed production evidence: {', '.join(missing)}"
        )
    governance = contract.get("governance")
    roster_binding = governance.get("production_role_roster") if isinstance(governance, Mapping) else None
    if not isinstance(roster_binding, Mapping):
        raise ContractStateError("trial route requires a governed production role roster")
    roster_id = roster_binding.get("evidence_id")
    supplied_rosters = [
        item for item in production_evidence_ids
        if isinstance(indexed.get(item), Mapping) and indexed[item].get("kind") == "production_role_roster"
    ]
    if supplied_rosters != [roster_id]:
        raise ContractStateError("trial route must use the exact governed production role roster")
    transition_ids = [item for item in production_evidence_ids if item != roster_id]
    accessibility_ids = [
        str(item_id)
        for item_id, reference in indexed.items()
        if isinstance(reference, Mapping)
        and reference.get("gate") == gate_id
        and reference.get("kind") == "accessibility_report"
    ]
    if len(accessibility_ids) != 1:
        raise ContractStateError(
            "trial route requires exactly one typed accessibility report"
        )
    if accessibility_ids[0] not in transition_ids:
        transition_ids.append(accessibility_ids[0])
    transfer_artifact_ids = [
        str(item_id)
        for item_id, reference in indexed.items()
        if isinstance(reference, Mapping)
        and reference.get("gate") == gate_id
        and reference.get("kind") == "trial_transfer_artifact"
    ]
    for item_id in transfer_artifact_ids:
        if item_id not in transition_ids:
            transition_ids.append(item_id)
    trial_reference = indexed.get(trial_evidence_id)
    receipt_reference = indexed.get(trial_receipt_evidence_id)
    if (
        not isinstance(trial_reference, Mapping)
        or trial_reference.get("gate") != gate_id
        or trial_reference.get("kind") != "independent_course_trial"
    ):
        raise ContractStateError("trial route requires an existing typed trial reference")
    if (
        not isinstance(receipt_reference, Mapping)
        or receipt_reference.get("gate") != gate_id
        or receipt_reference.get("kind") != "independent_trial_receipt"
    ):
        raise ContractStateError("trial route requires an existing authority-issued receipt reference")
    wrong_gate = [item for item in transition_ids if indexed[item].get("gate") != gate_id]
    if wrong_gate:
        raise ContractStateError(
            f"production evidence belongs to another gate: {', '.join(wrong_gate)}"
        )

    return validate_and_transition_gate(
        contract,
        gate_id,
        [*transition_ids, trial_evidence_id, trial_receipt_evidence_id],
        workspace_root,
        actor,
        at,
    )


def route_verified_trial_to_gate(
    contract: MutableMapping[str, Any], gate_id: str,
    production_evidence_ids: Sequence[str], trial_evidence_id: str,
    trial_receipt_evidence_id: str,
    actor: str, at: str, *, workspace_root: Path | str,
) -> str:
    staged = copy.deepcopy(contract)
    result = _route_verified_trial_to_gate(
        staged, gate_id, production_evidence_ids, trial_evidence_id,
        trial_receipt_evidence_id, actor, at, workspace_root=workspace_root,
    )
    contract.clear()
    contract.update(staged)
    return result
