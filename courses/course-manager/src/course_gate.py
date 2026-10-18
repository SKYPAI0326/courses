from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, MutableMapping, Sequence

from src.course_contract import ContractStateError, block_gate, validate_contract
from src.course_evidence import ConsumedEvidence, consume_evidence_reference
from src.course_gate_failure import route_failed_validation
from src.course_gate_validators import G5_ARTIFACT_KINDS, GATE_REGISTRY
from src.course_runner_authority import consume_trial_inputs

SECURITY_BOUNDARY_CODES = frozenset(
    {
        "invalid_independent_trial_receipt",
        "runner_authority_required",
        "invalid_trial_receipt_context",
        "invalid_receipt",
        "invalid_authority_binding",
        "authority_unavailable",
        "authority_binding_mismatch",
        "invalid_receipt_signature",
        "wrong_receipt_authority",
        "receipt_replay",
        "contract_replay",
        "evidence_set_replay",
        "receipt_ledger_invalid",
        "trial_binding_mismatch",
        "roster_binding_mismatch",
        "input_binding_mismatch",
        "participant_binding_mismatch",
        "runner_binding_mismatch",
        "runner_not_independent",
        "pilot_actor_roster_mismatch",
    }
)


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _indexed_references(
    contract: Mapping[str, Any], evidence_ids: Sequence[str]
) -> list[Mapping[str, Any]]:
    if not evidence_ids or any(not _text(item) for item in evidence_ids):
        raise ContractStateError("Gate transition requires at least one evidence id")
    if len(set(evidence_ids)) != len(evidence_ids):
        raise ContractStateError("Gate transition evidence ids must be unique")
    index = contract.get("evidence_index")
    if not isinstance(index, list):
        raise ContractStateError("contract evidence index is missing")
    by_id = {
        item.get("id"): item
        for item in index
        if isinstance(item, Mapping) and _text(item.get("id"))
    }
    missing = [item for item in evidence_ids if item not in by_id]
    if missing:
        raise ContractStateError(
            "Gate transition references unindexed evidence: " + ", ".join(missing)
        )
    return [by_id[item] for item in evidence_ids]


def _consume(
    workspace_root: Path | str,
    reference: Mapping[str, Any],
    gate_id: str,
    *,
    parse_json: bool,
) -> ConsumedEvidence:
    try:
        return consume_evidence_reference(
            workspace_root,
            reference,
            expected_gate=gate_id,
            parse_json=parse_json,
        )
    except (OSError, ValueError) as error:
        raise ContractStateError(f"invalid Gate evidence: {error}") from error


def _governed_roster_reference(contract: Mapping[str, Any]) -> Mapping[str, Any]:
    governance = contract.get("governance")
    binding = governance.get("production_role_roster") if isinstance(governance, Mapping) else None
    if not isinstance(binding, Mapping):
        raise ContractStateError("G4/G5 requires a governed production role roster")
    references = _indexed_references(contract, [str(binding.get("evidence_id"))])
    reference = references[0]
    if (
        reference.get("kind") != "production_role_roster"
        or reference.get("gate") != "G0"
        or reference.get("sha256") != binding.get("sha256")
    ):
        raise ContractStateError(
            "governed production role roster binding does not match its typed reference"
        )
    return reference


def validate_and_transition_gate(
    contract: MutableMapping[str, Any],
    gate_id: str,
    evidence_ids: Sequence[str],
    workspace_root: Path | str,
    actor: str,
    at: str,
) -> str:
    if gate_id not in GATE_REGISTRY:
        raise ContractStateError(f"unknown Gate: {gate_id}")
    if not _text(actor) or not _text(at):
        raise ContractStateError("Gate transition requires actor and timestamp")
    contract_issues = validate_contract(contract)
    if contract_issues:
        details = "; ".join(
            f"{issue.path}: {issue.message}" for issue in contract_issues
        )
        raise ContractStateError(f"refusing to transition invalid contract: {details}")

    references = _indexed_references(contract, evidence_ids)
    values_by_kind: dict[str, list[Any]] = {}
    consumed_by_kind: dict[str, list[ConsumedEvidence]] = {}
    consumed: list[ConsumedEvidence] = []
    consumed_inputs: list[ConsumedEvidence] = []
    for reference in references:
        kind = str(reference.get("kind"))
        parse_json = kind not in G5_ARTIFACT_KINDS and kind != "release_check"
        item = _consume(
            workspace_root, reference, gate_id, parse_json=parse_json
        )
        consumed.append(item)
        consumed_by_kind.setdefault(kind, []).append(item)
        values_by_kind.setdefault(kind, []).append(item.value if parse_json else item)

    if gate_id in {"G4", "G5"}:
        if not isinstance(contract.get("contract_instance_id"), str):
            raise ContractStateError(
                "G4/G5 requires a trusted contract_instance_id; legacy contract is fail-closed"
            )
        trials = values_by_kind.get("independent_course_trial", [])
        if len(trials) == 1 and isinstance(trials[0], Mapping):
            try:
                consumed_inputs = consume_trial_inputs(workspace_root, trials[0])
            except ContractStateError as error:
                raise ContractStateError(f"invalid Gate learner input: {error}") from error
            consumed_by_kind["learner_visible_input"] = consumed_inputs
        roster_reference = _governed_roster_reference(contract)
        roster = _consume(
            workspace_root, roster_reference, "G0", parse_json=True
        )
        consumed.append(roster)
        consumed_by_kind.setdefault("production_role_roster", []).append(roster)
        values_by_kind.setdefault("production_role_roster", []).append(roster.value)

    rule = GATE_REGISTRY[gate_id]
    missing_kinds = sorted(rule.required_kinds - set(values_by_kind))
    if missing_kinds:
        raise ContractStateError(
            f"{gate_id} requires evidence kind(s): {', '.join(missing_kinds)}"
        )
    issues = rule.validator(contract, values_by_kind, consumed_by_kind, workspace_root)
    if issues:
        summary = "; ".join(f"{issue.path}: {issue.message}" for issue in issues[:5])
        if any(issue.code in SECURITY_BOUNDARY_CODES for issue in issues):
            raise ContractStateError(
                f"{rule.validator_id} rejected security evidence: {summary}"
            )
        if route_failed_validation(
            contract,
            gate_id,
            issues,
            rule.validator_id,
            evidence_ids,
            consumed,
            consumed_inputs,
            values_by_kind,
            actor,
            at,
        ):
            return "BLOCKED"
        block_gate(
            contract,
            gate_id,
            f"{rule.validator_id} failed: {summary}",
            actor,
            at,
        )
        return "BLOCKED"

    gate_number = int(gate_id[1:])
    for prior in (f"G{index}" for index in range(gate_number)):
        if contract["gates"][prior].get("status") != "PASS":
            raise ContractStateError(f"{gate_id} requires {prior} PASS")
    record = contract["gates"][gate_id]
    if record.get("status") != "IN_PROGRESS":
        raise ContractStateError(
            f"cannot pass a gate in {record.get('status')!r} state"
        )
    blockers = [
        risk
        for risk in record.get("risks", [])
        if isinstance(risk, Mapping)
        and risk.get("blocking") is True
        and risk.get("resolved") is not True
    ]
    if blockers:
        raise ContractStateError(f"{gate_id} has unresolved blocking risks")
    record["status"] = "PASS"
    revision = record.get("source_revision")
    record["source_revision"] = revision + 1 if isinstance(revision, int) else 1
    event = {
        "kind": "gate_validation",
        "outcome": "PASS",
        "validator_id": rule.validator_id,
        "actor": actor,
        "at": at,
        "evidence_ids": list(evidence_ids),
        "consumed_evidence": [
            {"id": item.reference["id"], "sha256": item.sha256}
            for item in consumed
        ],
    }
    if consumed_inputs:
        event["consumed_inputs"] = [
            {"path": item.reference["path"], "sha256": item.sha256}
            for item in consumed_inputs
        ]
    if gate_id in {"G4", "G5"}:
        receipts = values_by_kind.get("independent_trial_receipt", [])
        if len(receipts) != 1 or not isinstance(receipts[0], Mapping):
            raise ContractStateError("Gate PASS requires one consumed trial receipt")
        receipt = receipts[0]
        ledger = contract.get("consumed_trial_receipts")
        if not isinstance(ledger, list):
            raise ContractStateError("contract receipt ledger is invalid")
        ledger.append(
            {
                "receipt_id": receipt["receipt_id"],
                "nonce": receipt["nonce"],
                "gate": gate_id,
                "consumed_at": at,
            }
        )
        event["consumed_receipt"] = {
            "receipt_id": receipt["receipt_id"],
            "nonce": receipt["nonce"],
        }
    record["evidence"].append(event)
    return "PASS"
