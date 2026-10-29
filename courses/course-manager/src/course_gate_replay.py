from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Callable, Mapping

from src.course_contract import ContractStateError
from src.course_gate_validators import GATE_REGISTRY


def replay_passed_gate(
    contract: Mapping[str, Any],
    gate_id: str,
    workspace_root: Path | str,
    transition: Callable[..., str],
) -> str:
    """Replay a historical PASS without mutating its authoritative contract."""

    if gate_id not in GATE_REGISTRY:
        raise ContractStateError(f"unknown Gate: {gate_id}")
    gate = contract.get("gates", {}).get(gate_id)
    if not isinstance(gate, Mapping) or gate.get("status") != "PASS":
        raise ContractStateError(f"{gate_id} is not in PASS state")
    events = [
        event
        for event in gate.get("evidence", [])
        if isinstance(event, Mapping)
        and event.get("kind") == "gate_validation"
        and event.get("outcome") == "PASS"
    ]
    if not events:
        raise ContractStateError(f"{gate_id} has no PASS evidence event")
    evidence_ids = events[-1].get("evidence_ids")
    if not isinstance(evidence_ids, list) or not evidence_ids:
        raise ContractStateError(f"{gate_id} PASS event has no replayable evidence ids")

    staged = copy.deepcopy(dict(contract))
    staged["gates"][gate_id]["status"] = "IN_PROGRESS"
    gate_number = int(gate_id[1:])
    for downstream in (f"G{index}" for index in range(gate_number + 1, 7)):
        staged["gates"][downstream]["status"] = "STALE"
    if gate_id != "G6":
        staged["external_actions"] = []
    if gate_id in {"G4", "G5"}:
        staged["consumed_trial_receipts"] = []

    return transition(
        staged,
        gate_id,
        list(evidence_ids),
        workspace_root,
        "course-proof-replay",
        "2026-10-19T00:00:00+08:00",
    )
