from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Sequence

from src.course_contract import ContractStateError
from src.course_evidence import canonical_json_bytes, register_evidence_file
from src.course_gate import validate_and_transition_gate
from src.course_governance import consume_passed_gate, single_governed_value


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _route_full_production_to_g5(
    contract: MutableMapping[str, Any],
    record: Mapping[str, Any],
    evidence_refs: Sequence[Mapping[str, Any]],
    actor: str,
    at: str,
    *,
    workspace_root: Path | str,
    blueprint: Mapping[str, Any],
    lessons: Sequence[Mapping[str, Any]],
    assets: Mapping[str, Any],
    pilot: Mapping[str, Any],
    production_role_evidence_id: str,
    production_record_path: str,
    trial_evidence_id: str,
    trial_receipt_evidence_id: str,
) -> str:
    if not evidence_refs:
        raise ValueError("G5 routing requires production evidence references")
    governed_blueprint, _ = single_governed_value(
        contract, "G2", "course_blueprint", workspace_root
    )
    governed_lessons = [
        item.value for item in consume_passed_gate(contract, "G3", workspace_root)
        if item.reference.get("kind") == "lesson_record"
    ]
    if blueprint != governed_blueprint or list(lessons) != governed_lessons:
        return "BLOCKED"
    evidence_index = contract.get("evidence_index")
    if not isinstance(evidence_index, list):
        raise ContractStateError("contract evidence index is missing")
    existing_ids = {
        item.get("id")
        for item in evidence_index
        if isinstance(item, Mapping) and _text(item.get("id"))
    }
    production_ids: list[str] = []
    staged_refs: list[dict[str, Any]] = []
    for index, ref in enumerate(evidence_refs):
        if not isinstance(ref, Mapping):
            raise ValueError(f"production evidence {index} must be an object")
        evidence_id = ref.get("id")
        if (
            not _text(evidence_id)
            or evidence_id in existing_ids
            or evidence_id in production_ids
            or not _text(ref.get("kind"))
            or not _text(ref.get("path"))
        ):
            raise ValueError(f"invalid or duplicate G5 production evidence at index {index}")
        registered = register_evidence_file(
            workspace_root,
            evidence_id=evidence_id,
            gate_id="G5",
            kind=str(ref["kind"]),
            relative_path=str(ref["path"]),
            maturity=ref.get("maturity") if _text(ref.get("maturity")) else None,
            metadata=ref.get("metadata") if isinstance(ref.get("metadata"), Mapping) else None,
        )
        production_ids.append(evidence_id)
        staged_refs.append(registered)

    governance = contract.get("governance")
    roster_binding = governance.get("production_role_roster") if isinstance(governance, Mapping) else None
    if (
        not isinstance(roster_binding, Mapping)
        or production_role_evidence_id != roster_binding.get("evidence_id")
        or production_role_evidence_id not in existing_ids
    ):
        raise ContractStateError("G5 must use the exact indexed governed production role roster")

    trial = record.get("full_course_trial")
    if not isinstance(trial, Mapping):
        raise ValueError("G5 routing requires a full-course trial record")
    trial_reference = next(
        (item for item in evidence_index if isinstance(item, Mapping) and item.get("id") == trial_evidence_id),
        None,
    )
    receipt_reference = next(
        (item for item in evidence_index if isinstance(item, Mapping) and item.get("id") == trial_receipt_evidence_id),
        None,
    )
    if (
        not isinstance(trial_reference, Mapping)
        or trial_reference.get("gate") != "G5"
        or trial_reference.get("kind") != "independent_course_trial"
    ):
        raise ContractStateError("G5 requires an existing typed full-course trial reference")
    if (
        not isinstance(receipt_reference, Mapping)
        or receipt_reference.get("gate") != "G5"
        or receipt_reference.get("kind") != "independent_trial_receipt"
    ):
        raise ContractStateError("G5 requires an existing authority-issued trial receipt")
    bundle = {
        "record": dict(record),
        "blueprint": dict(governed_blueprint),
        "lessons": [dict(item) for item in governed_lessons],
        "assets": dict(assets),
        "pilot": dict(pilot),
    }
    digest = hashlib.sha256(canonical_json_bytes(bundle)).hexdigest()
    record_id = f"g5-full-production-{digest[:12]}"
    if record_id in existing_ids or record_id in production_ids:
        raise ContractStateError(f"full production evidence id already exists: {record_id}")
    record_reference = register_evidence_file(
        workspace_root,
        evidence_id=record_id,
        gate_id="G5",
        kind="full_course_production",
        relative_path=production_record_path,
        maturity="EXECUTION_VALIDATED",
    )
    if record_reference["sha256"] != digest:
        raise ContractStateError(
            "registered full-production file does not match the supplied validation inputs"
        )
    staged_refs.append(record_reference)
    evidence_index.extend(staged_refs)
    return validate_and_transition_gate(
        contract,
        "G5",
        [*production_ids, record_id, trial_evidence_id, trial_receipt_evidence_id],
        workspace_root,
        actor,
        at,
    )


def route_full_production_to_g5(
    contract: MutableMapping[str, Any], record: Mapping[str, Any],
    evidence_refs: Sequence[Mapping[str, Any]], actor: str, at: str, *,
    workspace_root: Path | str, blueprint: Mapping[str, Any],
    lessons: Sequence[Mapping[str, Any]], assets: Mapping[str, Any],
    pilot: Mapping[str, Any], production_role_evidence_id: str,
    production_record_path: str, trial_evidence_id: str,
    trial_receipt_evidence_id: str,
) -> str:
    staged = copy.deepcopy(contract)
    result = _route_full_production_to_g5(
        staged, record, evidence_refs, actor, at,
        workspace_root=workspace_root, blueprint=blueprint, lessons=lessons,
        assets=assets, pilot=pilot,
        production_role_evidence_id=production_role_evidence_id,
        production_record_path=production_record_path,
        trial_evidence_id=trial_evidence_id,
        trial_receipt_evidence_id=trial_receipt_evidence_id,
    )
    if result == "PASS":
        contract.clear()
        contract.update(staged)
    return result
