from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Sequence

from src.course_contract import (
    GATE_ORDER,
    ContractStateError,
    record_change,
    record_gate_blocker,
)
from src.course_evidence import ConsumedEvidence


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _receipt_ledger_record(
    contract: MutableMapping[str, Any],
    gate_id: str,
    values_by_kind: Mapping[str, list[Any]],
    at: str,
) -> tuple[list[Any], dict[str, str], dict[str, str]]:
    receipts = values_by_kind.get("independent_trial_receipt", [])
    if len(receipts) != 1 or not isinstance(receipts[0], Mapping):
        raise ContractStateError("Gate transition requires one consumed trial receipt")
    receipt = receipts[0]
    receipt_id = receipt.get("receipt_id")
    nonce = receipt.get("nonce")
    if not _text(receipt_id) or not _text(nonce):
        raise ContractStateError("consumed trial receipt identity is invalid")
    ledger = contract.get("consumed_trial_receipts")
    if not isinstance(ledger, list):
        raise ContractStateError("contract receipt ledger is invalid")
    ledger_record = {
        "receipt_id": str(receipt_id),
        "nonce": str(nonce),
        "gate": gate_id,
        "consumed_at": at,
    }
    event_record = {"receipt_id": str(receipt_id), "nonce": str(nonce)}
    return ledger, ledger_record, event_record


def route_failed_validation(
    contract: MutableMapping[str, Any],
    source_gate: str,
    issues: Sequence[Any],
    validator_id: str,
    evidence_ids: Sequence[str],
    consumed: Sequence[ConsumedEvidence],
    consumed_inputs: Sequence[ConsumedEvidence],
    values_by_kind: Mapping[str, list[Any]],
    actor: str,
    at: str,
) -> bool:
    """Route an explicitly attributed failure to its earliest prior Gate."""

    source_index = GATE_ORDER.index(source_gate)
    issue_records: list[dict[str, str]] = []
    prior_return_gates: list[str] = []
    for issue in issues:
        candidate = getattr(issue, "return_gate", None)
        if candidate not in GATE_ORDER or GATE_ORDER.index(candidate) > source_index:
            candidate = source_gate
        if GATE_ORDER.index(candidate) < source_index:
            prior_return_gates.append(candidate)
        issue_records.append(
            {
                "code": str(issue.code),
                "path": str(issue.path),
                "message": str(issue.message),
                "return_gate": candidate,
            }
        )
    if not prior_return_gates:
        return False

    return_gate = min(prior_return_gates, key=GATE_ORDER.index)
    summary = "; ".join(
        f"{item['path']}: {item['message']}" for item in issue_records[:5]
    )
    reason = f"{validator_id} failed at {source_gate}; return to {return_gate}: {summary}"

    receipt_ledger: list[Any] | None = None
    ledger_record: dict[str, str] | None = None
    event_receipt: dict[str, str] | None = None
    if source_gate in {"G4", "G5"}:
        receipt_ledger, ledger_record, event_receipt = _receipt_ledger_record(
            contract, source_gate, values_by_kind, at
        )

    record_change(contract, return_gate, reason, actor, at, semantic=True)
    blocker_id = record_gate_blocker(contract, return_gate, reason, actor, at)
    event: dict[str, Any] = {
        "kind": "gate_validation",
        "outcome": "FAIL",
        "validator_id": validator_id,
        "source_gate": source_gate,
        "return_gate": return_gate,
        "blocker_id": blocker_id,
        "actor": actor,
        "at": at,
        "issues": issue_records,
        "evidence_ids": list(evidence_ids),
        "consumed_evidence": [
            {"id": item.reference["id"], "sha256": item.sha256}
            for item in consumed
        ],
    }
    trials = values_by_kind.get("independent_course_trial", [])
    if len(trials) == 1 and isinstance(trials[0], Mapping):
        result = trials[0].get("result")
        if isinstance(result, Mapping):
            event["trial_result"] = dict(result)
    if consumed_inputs:
        event["consumed_inputs"] = [
            {"path": item.reference["path"], "sha256": item.sha256}
            for item in consumed_inputs
        ]
    if receipt_ledger is not None and ledger_record is not None and event_receipt is not None:
        receipt_ledger.append(ledger_record)
        event["consumed_receipt"] = event_receipt
    contract["gates"][return_gate]["evidence"].append(event)
    return True
