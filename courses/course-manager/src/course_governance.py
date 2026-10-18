from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from src.course_contract import ContractStateError
from src.course_evidence import ConsumedEvidence, consume_evidence_reference

PASS_BINDING_FIELDS = frozenset({"id", "gate", "kind", "path", "sha256"})


def _pass_event(contract: Mapping[str, Any], gate_id: str) -> Mapping[str, Any]:
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
    if not passes:
        raise ContractStateError(f"{gate_id} requires a canonical PASS event")
    return passes[-1]


def passed_gate_references(
    contract: Mapping[str, Any], gate_id: str
) -> list[Mapping[str, Any]]:
    event = _pass_event(contract, gate_id)
    ids = event.get("evidence_ids")
    consumed_ids = event.get("consumed_evidence_ids")
    consumed = event.get("consumed_evidence")
    if (
        not isinstance(ids, list) or not ids or len(set(ids)) != len(ids)
        or any(not isinstance(item, str) for item in ids)
        or not isinstance(consumed_ids, list) or not consumed_ids
        or any(not isinstance(item, str) for item in consumed_ids)
        or len(set(consumed_ids)) != len(consumed_ids)
        or not isinstance(consumed, list) or not consumed
    ):
        raise ContractStateError(f"{gate_id} PASS event has invalid evidence ids")
    index = contract.get("evidence_index")
    by_id = {
        item.get("id"): item for item in index or []
        if isinstance(item, Mapping) and isinstance(item.get("id"), str)
    }
    bound: dict[str, Mapping[str, Any]] = {}
    for item in consumed:
        if (
            not isinstance(item, Mapping)
            or set(item) != PASS_BINDING_FIELDS
            or not isinstance(item.get("id"), str)
            or item["id"] in bound
        ):
            raise ContractStateError(f"{gate_id} PASS event has invalid consumed evidence bindings")
        indexed = by_id.get(item["id"])
        if not isinstance(indexed, Mapping) or any(indexed.get(field) != item.get(field) for field in PASS_BINDING_FIELDS):
            raise ContractStateError(f"{gate_id} PASS evidence binding no longer matches the index: {item['id']}")
        bound[item["id"]] = indexed
    if set(bound) != set(consumed_ids):
        raise ContractStateError(f"{gate_id} PASS event has missing or extra consumed evidence bindings")
    same_gate_ids = {evidence_id for evidence_id, item in bound.items() if item.get("gate") == gate_id}
    if same_gate_ids != set(ids):
        raise ContractStateError(f"{gate_id} PASS event has missing or extra canonical evidence bindings")
    refs: list[Mapping[str, Any]] = []
    for evidence_id in ids:
        reference = bound.get(evidence_id)
        if not isinstance(reference, Mapping) or reference.get("gate") != gate_id:
            raise ContractStateError(
                f"{gate_id} canonical evidence is missing or has the wrong Gate: {evidence_id}"
            )
        refs.append(reference)
    return refs


def consume_passed_gate(
    contract: Mapping[str, Any], gate_id: str, workspace_root: Path | str
) -> list[ConsumedEvidence]:
    direct = passed_gate_references(contract, gate_id)
    event = _pass_event(contract, gate_id)
    index = {
        item.get("id"): item for item in contract.get("evidence_index", [])
        if isinstance(item, Mapping) and isinstance(item.get("id"), str)
    }
    replayed: dict[str, ConsumedEvidence] = {}
    for binding in event["consumed_evidence"]:
        reference = index[binding["id"]]
        try:
            replayed[str(reference["id"])] = consume_evidence_reference(
                workspace_root, reference,
                expected_gate=str(reference["gate"]), parse_json=True,
            )
        except (OSError, ValueError) as error:
            raise ContractStateError(
                f"invalid governed {gate_id} evidence: {error}"
            ) from error
    return [replayed[str(reference["id"])] for reference in direct]


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
            "governed_g1_reference": consume_passed_gate(contract, "G1", workspace_root),
        }
    priors = {"G3": ("G2",), "G5": ("G0", "G2", "G3")}.get(gate_id, ())
    return {
        f"governed_{prior.lower()}": consume_passed_gate(
            contract, prior, workspace_root
        )
        for prior in priors
    }
