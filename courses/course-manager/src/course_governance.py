from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from src.course_contract import ContractStateError
from src.course_evidence import ConsumedEvidence, consume_evidence_reference


def passed_gate_references(
    contract: Mapping[str, Any], gate_id: str
) -> list[Mapping[str, Any]]:
    gates = contract.get("gates")
    gate = gates.get(gate_id) if isinstance(gates, Mapping) else None
    if not isinstance(gate, Mapping) or gate.get("status") != "PASS":
        raise ContractStateError(f"{gate_id} must be PASS before governed replay")
    passes = [
        event for event in gate.get("evidence", [])
        if isinstance(event, Mapping)
        and event.get("kind") == "gate_validation"
        and event.get("outcome") == "PASS"
    ]
    if len(passes) != 1:
        raise ContractStateError(f"{gate_id} requires exactly one canonical PASS event")
    ids = passes[0].get("evidence_ids")
    if not isinstance(ids, list) or not ids or any(not isinstance(item, str) for item in ids):
        raise ContractStateError(f"{gate_id} PASS event has invalid evidence ids")
    index = contract.get("evidence_index")
    by_id = {
        item.get("id"): item for item in index or []
        if isinstance(item, Mapping) and isinstance(item.get("id"), str)
    }
    refs: list[Mapping[str, Any]] = []
    for evidence_id in ids:
        reference = by_id.get(evidence_id)
        if not isinstance(reference, Mapping) or reference.get("gate") != gate_id:
            raise ContractStateError(
                f"{gate_id} canonical evidence is missing or has the wrong Gate: {evidence_id}"
            )
        refs.append(reference)
    return refs


def consume_passed_gate(
    contract: Mapping[str, Any], gate_id: str, workspace_root: Path | str
) -> list[ConsumedEvidence]:
    consumed: list[ConsumedEvidence] = []
    for reference in passed_gate_references(contract, gate_id):
        try:
            consumed.append(
                consume_evidence_reference(
                    workspace_root, reference, expected_gate=gate_id, parse_json=True
                )
            )
        except (OSError, ValueError) as error:
            raise ContractStateError(
                f"invalid governed {gate_id} evidence: {error}"
            ) from error
    return consumed


def single_governed_value(
    contract: Mapping[str, Any], gate_id: str, kind: str, workspace_root: Path | str
) -> tuple[Any, ConsumedEvidence]:
    matches = [
        item for item in consume_passed_gate(contract, gate_id, workspace_root)
        if item.reference.get("kind") == kind
    ]
    if len(matches) != 1:
        raise ContractStateError(
            f"{gate_id} requires exactly one governed {kind} evidence record"
        )
    return matches[0].value, matches[0]


def governed_dependencies(
    contract: Mapping[str, Any], gate_id: str, workspace_root: Path | str
) -> dict[str, list[ConsumedEvidence]]:
    if gate_id == "G2":
        return {
            "governed_g0": consume_passed_gate(contract, "G0", workspace_root),
            "governed_g1_reference": [
                ConsumedEvidence(
                    reference=reference,
                    data=b"",
                    sha256=str(reference["sha256"]),
                    value=None,
                )
                for reference in passed_gate_references(contract, "G1")
            ]
        }
    priors = {"G3": ("G2",), "G5": ("G0", "G2", "G3")}.get(gate_id, ())
    return {
        f"governed_{prior.lower()}": consume_passed_gate(
            contract, prior, workspace_root
        )
        for prior in priors
    }
