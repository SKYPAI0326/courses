from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, MutableMapping, Sequence

from src.course_contract import (
    ContractStateError,
    _commit_gate_pass,
    block_gate,
    validate_contract,
)
from src.course_evidence import verify_evidence_reference


@dataclass(frozen=True)
class GateValidationIssue:
    code: str
    path: str
    message: str


GateValidator = Callable[
    [Mapping[str, Any], Mapping[str, list[Any]]], list[GateValidationIssue]
]


@dataclass(frozen=True)
class GateRule:
    validator_id: str
    required_kinds: frozenset[str]
    validator: GateValidator


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_requirements(
    contract: Mapping[str, Any], evidence: Mapping[str, list[Any]]
) -> list[GateValidationIssue]:
    records = evidence.get("requirements_record", [])
    if len(records) != 1 or not isinstance(records[0], Mapping):
        return [
            GateValidationIssue(
                "invalid_requirements_record",
                "$.evidence.requirements_record",
                "G0 requires exactly one requirements record object",
            )
        ]
    record = records[0]
    if record != contract.get("G0_requirements"):
        return [
            GateValidationIssue(
                "requirements_evidence_mismatch",
                "$.G0_requirements",
                "requirements evidence must exactly match the governed G0 payload",
            )
        ]
    result = record.get("observable_result", record.get("observable_outcome"))
    if not _text(record.get("learner_context")) or not _text(result):
        return [
            GateValidationIssue(
                "incomplete_requirements_record",
                "$.evidence.requirements_record",
                "requirements must define learner_context and an observable result",
            )
        ]
    return []


def _coerce_issues(issues: Sequence[Any]) -> list[GateValidationIssue]:
    return [
        GateValidationIssue(
            str(getattr(issue, "code", "validation_failed")),
            str(getattr(issue, "path", "$")),
            str(getattr(issue, "message", issue)),
        )
        for issue in issues
    ]


def _validate_research(
    contract: Mapping[str, Any], evidence: Mapping[str, list[Any]]
) -> list[GateValidationIssue]:
    from src.course_research import validate_research_record

    records = evidence.get("research_record", [])
    if len(records) != 1 or not isinstance(records[0], Mapping):
        return [
            GateValidationIssue(
                "invalid_research_record",
                "$.evidence.research_record",
                "G1 requires exactly one research record object",
            )
        ]
    value = records[0]
    if isinstance(value.get("record"), Mapping):
        record = value["record"]
        adaptation = value.get("adaptation")
    else:
        record = value
        adaptation = contract.get("adaptation")
    if not isinstance(adaptation, Mapping):
        return [
            GateValidationIssue(
                "adaptation_required",
                "$.adaptation",
                "G1 research validation requires the governed adaptation record",
            )
        ]
    return _coerce_issues(validate_research_record(record, adaptation))


def _validate_blueprint(
    contract: Mapping[str, Any], evidence: Mapping[str, list[Any]]
) -> list[GateValidationIssue]:
    records = evidence.get("course_blueprint", [])
    if len(records) != 1 or not isinstance(records[0], Mapping):
        return [
            GateValidationIssue(
                "invalid_course_blueprint",
                "$.evidence.course_blueprint",
                "G2 requires exactly one course blueprint object",
            )
        ]
    units = records[0].get("units")
    if not isinstance(units, list) or not units:
        return [
            GateValidationIssue(
                "blueprint_units_required",
                "$.evidence.course_blueprint.units",
                "course blueprint requires at least one unit",
            )
        ]
    seen: set[str] = set()
    issues: list[GateValidationIssue] = []
    for index, unit in enumerate(units):
        path = f"$.evidence.course_blueprint.units[{index}]"
        if not isinstance(unit, Mapping):
            issues.append(GateValidationIssue("invalid_blueprint_unit", path, "unit must be an object"))
            continue
        unit_id = unit.get("id")
        if not _text(unit_id) or unit_id in seen:
            issues.append(
                GateValidationIssue(
                    "invalid_blueprint_unit",
                    f"{path}.id",
                    "unit id must contain text and be unique",
                )
            )
        else:
            seen.add(unit_id)
        for field in ("outcome", "workflow_fingerprint"):
            if not _text(unit.get(field)):
                issues.append(
                    GateValidationIssue(
                        "invalid_blueprint_unit",
                        f"{path}.{field}",
                        f"unit {field} must contain text",
                    )
                )
    return issues


def _validate_lessons(
    contract: Mapping[str, Any], evidence: Mapping[str, list[Any]]
) -> list[GateValidationIssue]:
    from src.course_content import validate_lesson_record

    records = evidence.get("lesson_record", [])
    if not records:
        return [
            GateValidationIssue(
                "lesson_record_required",
                "$.evidence.lesson_record",
                "G3 requires at least one lesson record",
            )
        ]
    issues: list[GateValidationIssue] = []
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            issues.append(
                GateValidationIssue(
                    "invalid_lesson_record",
                    f"$.evidence.lesson_record[{index}]",
                    "lesson record must be an object",
                )
            )
            continue
        issues.extend(_coerce_issues(validate_lesson_record(record)))
    return issues


def _single_mapping(
    evidence: Mapping[str, list[Any]], kind: str
) -> tuple[Mapping[str, Any] | None, list[GateValidationIssue]]:
    values = evidence.get(kind, [])
    if len(values) != 1 or not isinstance(values[0], Mapping):
        return None, [
            GateValidationIssue(
                f"invalid_{kind}",
                f"$.evidence.{kind}",
                f"Gate requires exactly one {kind} object",
            )
        ]
    return values[0], []


def _validate_g4(
    contract: Mapping[str, Any], evidence: Mapping[str, list[Any]]
) -> list[GateValidationIssue]:
    from src.course_production import validate_pilot_record
    from src.course_validation import evidence_maturity, validate_trial_record

    pilot_bundle, issues = _single_mapping(evidence, "pilot_record")
    trial, trial_shape = _single_mapping(evidence, "independent_course_trial")
    roster, roster_shape = _single_mapping(evidence, "production_role_roster")
    issues.extend(trial_shape)
    issues.extend(roster_shape)
    if trial is not None and roster is not None:
        try:
            issues.extend(
                _coerce_issues(
                    validate_trial_record(trial, roster, "representative_unit")
                )
            )
        except ValueError as error:
            issues.append(
                GateValidationIssue(
                    "production_role_roster_invalid",
                    "$.evidence.production_role_roster",
                    str(error),
                )
            )
        if evidence_maturity(trial) != "INDEPENDENT_AI_VERIFIED":
            issues.append(
                GateValidationIssue(
                    "independent_participant_required",
                    "$.evidence.independent_course_trial.participant.type",
                    "G4 requires a passing independent AI learner trial",
                )
            )
    if pilot_bundle is not None:
        pilot = pilot_bundle.get("pilot")
        lesson = pilot_bundle.get("lesson")
        assets = pilot_bundle.get("asset_manifest")
        if not all(isinstance(item, Mapping) for item in (pilot, lesson, assets)):
            issues.append(
                GateValidationIssue(
                    "invalid_pilot_bundle",
                    "$.evidence.pilot_record",
                    "pilot evidence must contain pilot, lesson, and asset_manifest objects",
                )
            )
        else:
            issues.extend(_coerce_issues(validate_pilot_record(pilot, lesson, assets)))
            if trial is not None and pilot.get("trial_context_id") != trial.get(
                "isolated_context_id"
            ):
                issues.append(
                    GateValidationIssue(
                        "pilot_trial_context_mismatch",
                        "$.evidence.pilot_record.pilot.trial_context_id",
                        "pilot record must bind the exact independent trial context",
                    )
                )
    return issues


def _validate_g5(
    contract: Mapping[str, Any], evidence: Mapping[str, list[Any]]
) -> list[GateValidationIssue]:
    from src.course_production import validate_full_production

    bundle, issues = _single_mapping(evidence, "full_course_production")
    trial, trial_shape = _single_mapping(evidence, "independent_course_trial")
    roster, roster_shape = _single_mapping(evidence, "production_role_roster")
    issues.extend(trial_shape)
    issues.extend(roster_shape)
    if bundle is None or trial is None or roster is None:
        return issues
    record = bundle.get("record")
    blueprint = bundle.get("blueprint")
    lessons = bundle.get("lessons")
    assets = bundle.get("assets")
    pilot = bundle.get("pilot")
    if (
        not isinstance(record, Mapping)
        or not isinstance(blueprint, Mapping)
        or not isinstance(lessons, list)
        or not all(isinstance(item, Mapping) for item in lessons)
        or not isinstance(assets, Mapping)
        or not isinstance(pilot, Mapping)
    ):
        issues.append(
            GateValidationIssue(
                "invalid_full_production_bundle",
                "$.evidence.full_course_production",
                "full production evidence requires record, blueprint, lessons, assets, and pilot",
            )
        )
        return issues
    issues.extend(
        _coerce_issues(
            validate_full_production(
                record,
                blueprint,
                lessons,
                assets,
                pilot,
                trial,
                production_roles=roster,
            )
        )
    )
    return issues


def _validate_release(
    contract: Mapping[str, Any], evidence: Mapping[str, list[Any]]
) -> list[GateValidationIssue]:
    from src.course_release import validate_release_record

    record, issues = _single_mapping(evidence, "release_record")
    if record is None:
        return issues
    return _coerce_issues(validate_release_record(record))


GATE_REGISTRY: dict[str, GateRule] = {
    "G0": GateRule(
        "course-requirements-validator",
        frozenset({"requirements_record"}),
        _validate_requirements,
    ),
    "G1": GateRule(
        "course-research-record-validator",
        frozenset({"research_record"}),
        _validate_research,
    ),
    "G2": GateRule(
        "course-blueprint-validator",
        frozenset({"course_blueprint"}),
        _validate_blueprint,
    ),
    "G3": GateRule(
        "course-lesson-record-validator",
        frozenset({"lesson_record"}),
        _validate_lessons,
    ),
    "G4": GateRule(
        "course-pilot-and-independent-trial-validator",
        frozenset({"pilot_record", "independent_course_trial", "production_role_roster"}),
        _validate_g4,
    ),
    "G5": GateRule(
        "course-full-production-validator",
        frozenset(
            {"full_course_production", "independent_course_trial", "production_role_roster"}
        ),
        _validate_g5,
    ),
    "G6": GateRule(
        "course-release-record-validator",
        frozenset({"release_record"}),
        _validate_release,
    ),
}


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


def _read_verified_json(
    workspace_root: Path | str, reference: Mapping[str, Any], gate_id: str
) -> Any:
    issues = verify_evidence_reference(
        workspace_root, reference, expected_gate=gate_id
    )
    if issues:
        details = "; ".join(
            f"{issue.code} {issue.path}: {issue.message}" for issue in issues
        )
        raise ContractStateError(f"invalid Gate evidence: {details}")

    path = Path(workspace_root).resolve(strict=True) / str(reference["path"])
    try:
        encoded = path.read_bytes()
    except OSError as error:
        raise ContractStateError(f"could not consume Gate evidence: {error}") from error
    digest = hashlib.sha256(encoded).hexdigest()
    if digest != reference.get("sha256"):
        raise ContractStateError(
            f"evidence sha256 changed while consuming {reference.get('id')}"
        )
    try:
        value = json.loads(encoded)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractStateError(
            f"Gate evidence {reference.get('id')} must be valid UTF-8 JSON"
        ) from error

    replay_issues = verify_evidence_reference(
        workspace_root, reference, expected_gate=gate_id
    )
    if replay_issues:
        details = "; ".join(
            f"{issue.code} {issue.path}: {issue.message}" for issue in replay_issues
        )
        raise ContractStateError(
            f"Gate evidence changed during transition: {details}"
        )
    return value


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
    for reference in references:
        value = _read_verified_json(workspace_root, reference, gate_id)
        values_by_kind.setdefault(str(reference.get("kind")), []).append(value)

    rule = GATE_REGISTRY[gate_id]
    missing_kinds = sorted(rule.required_kinds - set(values_by_kind))
    if missing_kinds:
        raise ContractStateError(
            f"{gate_id} requires evidence kind(s): {', '.join(missing_kinds)}"
        )

    issues = rule.validator(contract, values_by_kind)
    if issues:
        summary = "; ".join(f"{issue.path}: {issue.message}" for issue in issues[:5])
        block_gate(
            contract,
            gate_id,
            f"{rule.validator_id} failed: {summary}",
            actor,
            at,
        )
        return "BLOCKED"

    _commit_gate_pass(
        contract,
        gate_id,
        evidence_ids,
        rule.validator_id,
        actor,
        at,
    )
    return "PASS"
