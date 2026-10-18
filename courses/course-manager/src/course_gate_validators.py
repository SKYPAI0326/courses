from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from src.course_evidence import ConsumedEvidence
from src.course_runner_authority import verify_trial_receipt


@dataclass(frozen=True)
class GateValidationIssue:
    code: str
    path: str
    message: str


ConsumedByKind = Mapping[str, list[ConsumedEvidence]]
EvidenceValues = Mapping[str, list[Any]]
GateValidator = Callable[
    [Mapping[str, Any], EvidenceValues, ConsumedByKind, Path | str],
    list[GateValidationIssue],
]


@dataclass(frozen=True)
class GateRule:
    validator_id: str
    required_kinds: frozenset[str]
    validator: GateValidator


G5_ARTIFACT_KINDS = frozenset(
    {
        "lesson_source",
        "learner_page",
        "course_asset",
        "dependency_artifact",
        "navigation_artifact",
        "final_artifact",
    }
)


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _coerce_issues(issues: Sequence[Any]) -> list[GateValidationIssue]:
    return [
        GateValidationIssue(
            str(getattr(issue, "code", "validation_failed")),
            str(getattr(issue, "path", "$")),
            str(getattr(issue, "message", issue)),
        )
        for issue in issues
    ]


def _single_mapping(
    evidence: EvidenceValues, kind: str
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


def _validate_requirements(
    contract: Mapping[str, Any], evidence: EvidenceValues, consumed: ConsumedByKind,
    workspace_root: Path | str,
) -> list[GateValidationIssue]:
    record, issues = _single_mapping(evidence, "requirements_record")
    if record is None:
        return issues
    if record != contract.get("G0_requirements"):
        issues.append(GateValidationIssue("requirements_evidence_mismatch", "$.G0_requirements", "requirements evidence must exactly match the governed G0 payload"))
    result = record.get("observable_result", record.get("observable_outcome"))
    if not _text(record.get("learner_context")) or not _text(result):
        issues.append(GateValidationIssue("incomplete_requirements_record", "$.evidence.requirements_record", "requirements must define learner_context and an observable result"))
    return issues


def _validate_research(
    contract: Mapping[str, Any], evidence: EvidenceValues, consumed: ConsumedByKind,
    workspace_root: Path | str,
) -> list[GateValidationIssue]:
    from src.course_research import validate_research_record

    value, issues = _single_mapping(evidence, "research_record")
    if value is None:
        return issues
    if isinstance(value.get("record"), Mapping):
        record = value["record"]
        adaptation = value.get("adaptation")
    else:
        record = value
        adaptation = contract.get("adaptation")
    if not isinstance(adaptation, Mapping):
        return [GateValidationIssue("adaptation_required", "$.adaptation", "G1 research validation requires the governed adaptation record")]
    return _coerce_issues(validate_research_record(record, adaptation))


def _validate_blueprint(
    contract: Mapping[str, Any], evidence: EvidenceValues, consumed: ConsumedByKind,
    workspace_root: Path | str,
) -> list[GateValidationIssue]:
    record, issues = _single_mapping(evidence, "course_blueprint")
    if record is None:
        return issues
    units = record.get("units")
    if not isinstance(units, list) or not units:
        return [GateValidationIssue("blueprint_units_required", "$.evidence.course_blueprint.units", "course blueprint requires at least one unit")]
    seen: set[str] = set()
    for index, unit in enumerate(units):
        path = f"$.evidence.course_blueprint.units[{index}]"
        if not isinstance(unit, Mapping):
            issues.append(GateValidationIssue("invalid_blueprint_unit", path, "unit must be an object"))
            continue
        unit_id = unit.get("id")
        if not _text(unit_id) or unit_id in seen:
            issues.append(GateValidationIssue("invalid_blueprint_unit", f"{path}.id", "unit id must contain text and be unique"))
        else:
            seen.add(str(unit_id))
        for field in ("outcome", "workflow_fingerprint"):
            if not _text(unit.get(field)):
                issues.append(GateValidationIssue("invalid_blueprint_unit", f"{path}.{field}", f"unit {field} must contain text"))
    return issues


def _validate_lessons(
    contract: Mapping[str, Any], evidence: EvidenceValues, consumed: ConsumedByKind,
    workspace_root: Path | str,
) -> list[GateValidationIssue]:
    from src.course_content import validate_lesson_record

    records = evidence.get("lesson_record", [])
    if not records:
        return [GateValidationIssue("lesson_record_required", "$.evidence.lesson_record", "G3 requires at least one lesson record")]
    issues: list[GateValidationIssue] = []
    for index, record in enumerate(records):
        if not isinstance(record, Mapping):
            issues.append(GateValidationIssue("invalid_lesson_record", f"$.evidence.lesson_record[{index}]", "lesson record must be an object"))
        else:
            issues.extend(_coerce_issues(validate_lesson_record(record)))
    return issues


def _validate_receipt(
    contract: Mapping[str, Any],
    gate_id: str,
    evidence: EvidenceValues,
    consumed: ConsumedByKind,
    workspace_root: Path | str,
) -> list[GateValidationIssue]:
    receipt, issues = _single_mapping(evidence, "independent_trial_receipt")
    trials = consumed.get("independent_course_trial", [])
    rosters = consumed.get("production_role_roster", [])
    governance = contract.get("governance")
    authority = governance.get("runner_authority") if isinstance(governance, Mapping) else None
    if receipt is None:
        return issues
    if not isinstance(authority, Mapping):
        issues.append(GateValidationIssue("runner_authority_required", "$.governance.runner_authority", "G4/G5 requires a pre-bound runner authority"))
        return issues
    if len(trials) != 1 or len(rosters) != 1:
        issues.append(GateValidationIssue("invalid_trial_receipt_context", "$.evidence.independent_trial_receipt", "receipt validation requires exactly one consumed trial and roster"))
        return issues
    for issue in verify_trial_receipt(
        receipt, authority,
        learner_inputs=list(consumed.get("learner_visible_input", [])),
        gate_id=gate_id, trial=trials[0], roster=rosters[0]
    ):
        issues.append(GateValidationIssue(issue.code, "$.evidence.independent_trial_receipt", issue.message))
    return issues


def _validate_g4(
    contract: Mapping[str, Any], evidence: EvidenceValues, consumed: ConsumedByKind,
    workspace_root: Path | str,
) -> list[GateValidationIssue]:
    from src.course_production import validate_pilot_record
    from src.course_validation import evidence_maturity, validate_trial_record

    pilot_bundle, issues = _single_mapping(evidence, "pilot_record")
    trial, trial_shape = _single_mapping(evidence, "independent_course_trial")
    roster, roster_shape = _single_mapping(evidence, "production_role_roster")
    issues.extend(trial_shape)
    issues.extend(roster_shape)
    issues.extend(_validate_receipt(contract, "G4", evidence, consumed, workspace_root))
    if trial is not None and roster is not None:
        try:
            issues.extend(_coerce_issues(validate_trial_record(trial, roster, "representative_unit")))
        except ValueError as error:
            issues.append(GateValidationIssue("production_role_roster_invalid", "$.evidence.production_role_roster", str(error)))
        if evidence_maturity(trial) != "INDEPENDENT_AI_VERIFIED":
            issues.append(GateValidationIssue("independent_participant_required", "$.evidence.independent_course_trial.participant.type", "G4 requires a passing independent AI learner trial"))
    if pilot_bundle is None:
        return issues
    pilot = pilot_bundle.get("pilot")
    lesson = pilot_bundle.get("lesson")
    assets = pilot_bundle.get("asset_manifest")
    if not all(isinstance(item, Mapping) for item in (pilot, lesson, assets)):
        issues.append(GateValidationIssue("invalid_pilot_bundle", "$.evidence.pilot_record", "pilot evidence must contain pilot, lesson, and asset_manifest objects"))
        return issues
    issues.extend(_coerce_issues(validate_pilot_record(pilot, lesson, assets)))
    if trial is not None and pilot.get("trial_context_id") != trial.get("isolated_context_id"):
        issues.append(GateValidationIssue("pilot_trial_context_mismatch", "$.evidence.pilot_record.pilot.trial_context_id", "pilot record must bind the exact independent trial context"))
    authors = roster.get("authors") if isinstance(roster, Mapping) else None
    actors = pilot.get("production_actor_ids")
    if not isinstance(authors, list) or not isinstance(actors, list) or set(actors) != set(authors):
        issues.append(GateValidationIssue("pilot_actor_roster_mismatch", "$.evidence.pilot_record.pilot.production_actor_ids", "pilot production actors must exactly match the governed author roster"))
    return issues


def _artifact_items(consumed: ConsumedByKind, kind: str) -> list[ConsumedEvidence]:
    return list(consumed.get(kind, []))


def _validate_g5_artifact_bindings(
    record: Mapping[str, Any], assets: Mapping[str, Any], consumed: ConsumedByKind
) -> list[GateValidationIssue]:
    expected: list[tuple[str, str, str, str, str]] = []
    for unit in record.get("units", []):
        if isinstance(unit, Mapping):
            unit_id = str(unit.get("unit_id", ""))
            expected.append(("lesson_source", "unit_id", unit_id, "", str(unit.get("lesson_sha256", ""))))
            expected.append(("learner_page", "unit_id", unit_id, str(unit.get("html_path", "")), str(unit.get("html_sha256", ""))))
    for asset in assets.get("assets", []):
        if isinstance(asset, Mapping) and isinstance(asset.get("source"), Mapping) and isinstance(asset.get("open_test"), Mapping):
            expected.append(("course_asset", "asset_id", str(asset.get("id", "")), str(asset["source"].get("uri", "")), str(asset["open_test"].get("sha256", ""))))
    for check in record.get("dependency_checks", []):
        if isinstance(check, Mapping):
            expected.append(("dependency_artifact", "dependency", f"{check.get('from_unit')}->{check.get('to_unit')}", str(check.get("artifact", "")), str(check.get("sha256", ""))))
    navigation = record.get("navigation")
    if isinstance(navigation, Mapping):
        for role in ("entry", "completion"):
            expected.append(("navigation_artifact", "role", role, str(navigation.get(role, "")), str(navigation.get(f"{role}_sha256", ""))))
    final = record.get("final_artifact")
    if isinstance(final, Mapping):
        expected.append(("final_artifact", "role", "final", str(final.get("path", "")), str(final.get("sha256", ""))))
    issues: list[GateValidationIssue] = []
    matched: set[str] = set()
    for kind, metadata_key, metadata_value, path, digest in expected:
        candidates = [
            item for item in _artifact_items(consumed, kind)
            if isinstance(item.reference.get("metadata"), Mapping)
            and item.reference["metadata"].get(metadata_key) == metadata_value
        ]
        label = f"{kind}:{metadata_value}"
        if len(candidates) != 1:
            issues.append(GateValidationIssue("artifact_binding_mismatch", f"$.evidence.{label}", "every production artifact requires exactly one typed evidence reference"))
            continue
        item = candidates[0]
        matched.add(str(item.reference.get("id")))
        if path and item.reference.get("path") != path:
            issues.append(GateValidationIssue("artifact_path_mismatch", f"$.evidence.{label}.path", "artifact evidence path does not match the production record"))
        if digest and item.sha256 != digest:
            issues.append(GateValidationIssue("artifact_hash_mismatch", f"$.evidence.{label}.sha256", "artifact evidence hash does not match the production record"))
    supplied = {str(item.reference.get("id")) for kind in G5_ARTIFACT_KINDS for item in _artifact_items(consumed, kind)}
    if supplied != matched:
        issues.append(GateValidationIssue("extra_artifact_evidence", "$.evidence", "G5 rejects unbound or extra artifact evidence"))
    return issues


def _validate_g5(
    contract: Mapping[str, Any], evidence: EvidenceValues, consumed: ConsumedByKind,
    workspace_root: Path | str,
) -> list[GateValidationIssue]:
    from src.course_production import validate_full_production

    bundle, issues = _single_mapping(evidence, "full_course_production")
    allowed = G5_ARTIFACT_KINDS | {"full_course_production", "independent_course_trial", "independent_trial_receipt", "production_role_roster"}
    extras = sorted(set(evidence) - allowed)
    if extras:
        issues.append(GateValidationIssue("extra_artifact_evidence", "$.evidence", f"G5 rejects unbound evidence kind(s): {', '.join(extras)}"))
    trial, trial_shape = _single_mapping(evidence, "independent_course_trial")
    roster, roster_shape = _single_mapping(evidence, "production_role_roster")
    issues.extend(trial_shape)
    issues.extend(roster_shape)
    issues.extend(_validate_receipt(contract, "G5", evidence, consumed, workspace_root))
    if bundle is None or trial is None or roster is None:
        return issues
    record, blueprint, lessons = bundle.get("record"), bundle.get("blueprint"), bundle.get("lessons")
    assets, pilot = bundle.get("assets"), bundle.get("pilot")
    if not isinstance(record, Mapping) or not isinstance(blueprint, Mapping) or not isinstance(lessons, list) or not all(isinstance(item, Mapping) for item in lessons) or not isinstance(assets, Mapping) or not isinstance(pilot, Mapping):
        issues.append(GateValidationIssue("invalid_full_production_bundle", "$.evidence.full_course_production", "full production evidence requires record, blueprint, lessons, assets, and pilot"))
        return issues
    issues.extend(_coerce_issues(validate_full_production(record, blueprint, lessons, assets, pilot, trial, production_roles=roster)))
    issues.extend(_validate_g5_artifact_bindings(record, assets, consumed))
    return issues


def _validate_release(
    contract: Mapping[str, Any], evidence: EvidenceValues, consumed: ConsumedByKind,
    workspace_root: Path | str,
) -> list[GateValidationIssue]:
    from src.course_release import validate_release_record

    record, issues = _single_mapping(evidence, "release_record")
    if record is None:
        return issues
    issues.extend(_coerce_issues(validate_release_record(record)))
    matched: set[str] = set()
    for check in record.get("checks", []):
        if not isinstance(check, Mapping) or not isinstance(check.get("evidence"), Mapping):
            continue
        check_id = str(check.get("id", ""))
        candidates = [
            item for item in _artifact_items(consumed, "release_check")
            if isinstance(item.reference.get("metadata"), Mapping)
            and item.reference["metadata"].get("check_id") == check_id
        ]
        if len(candidates) != 1:
            issues.append(GateValidationIssue("release_check_evidence_missing", f"$.checks.{check_id}", "each G6 check requires exactly one replayable typed evidence file"))
            continue
        item = candidates[0]
        matched.add(str(item.reference.get("id")))
        declared = check["evidence"]
        if item.reference.get("path") != declared.get("path") or item.sha256 != declared.get("sha256"):
            issues.append(GateValidationIssue("release_check_evidence_mismatch", f"$.checks.{check_id}.evidence", "G6 check path/hash must match the consumed evidence file"))
    supplied = {str(item.reference.get("id")) for item in _artifact_items(consumed, "release_check")}
    if supplied != matched:
        issues.append(GateValidationIssue("extra_release_check_evidence", "$.evidence.release_check", "G6 rejects extra or unbound release-check evidence"))
    return issues


GATE_REGISTRY: dict[str, GateRule] = {
    "G0": GateRule("course-requirements-validator", frozenset({"requirements_record"}), _validate_requirements),
    "G1": GateRule("course-research-record-validator", frozenset({"research_record"}), _validate_research),
    "G2": GateRule("course-blueprint-validator", frozenset({"course_blueprint"}), _validate_blueprint),
    "G3": GateRule("course-lesson-record-validator", frozenset({"lesson_record"}), _validate_lessons),
    "G4": GateRule("course-pilot-and-independent-trial-validator", frozenset({"pilot_record", "independent_course_trial", "independent_trial_receipt", "production_role_roster"}), _validate_g4),
    "G5": GateRule("course-full-production-validator", frozenset({"full_course_production", "independent_course_trial", "independent_trial_receipt", "production_role_roster"}), _validate_g5),
    "G6": GateRule("course-release-record-validator", frozenset({"release_record"}), _validate_release),
}
