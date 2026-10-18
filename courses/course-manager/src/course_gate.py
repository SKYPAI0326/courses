from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, MutableMapping, Sequence

from src.course_contract import (
    ContractStateError,
    block_gate,
    validate_contract,
)
from src.course_evidence import ConsumedEvidence, consume_evidence_reference


@dataclass(frozen=True)
class GateValidationIssue:
    code: str
    path: str
    message: str


GateValidator = Callable[
    [Mapping[str, Any], Mapping[str, list[Any]]], list[GateValidationIssue]
]

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
    allowed_kinds = G5_ARTIFACT_KINDS | {
        "full_course_production", "independent_course_trial", "production_role_roster"
    }
    extras = sorted(set(evidence) - allowed_kinds)
    if extras:
        issues.append(GateValidationIssue("extra_artifact_evidence", "$.evidence", f"G5 rejects unbound evidence kind(s): {', '.join(extras)}"))
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
    issues.extend(_validate_g5_artifact_bindings(record, assets, evidence))
    return issues


def _artifact_items(
    evidence: Mapping[str, list[Any]], kind: str
) -> list[ConsumedEvidence]:
    return [item for item in evidence.get(kind, []) if isinstance(item, ConsumedEvidence)]


def _validate_g5_artifact_bindings(
    record: Mapping[str, Any],
    assets: Mapping[str, Any],
    evidence: Mapping[str, list[Any]],
) -> list[GateValidationIssue]:
    expected: list[tuple[str, str, str, str, str]] = []
    for unit in record.get("units", []):
        if not isinstance(unit, Mapping):
            continue
        unit_id = str(unit.get("unit_id", ""))
        expected.append(("lesson_source", "unit_id", unit_id, "", str(unit.get("lesson_sha256", ""))))
        expected.append(("learner_page", "unit_id", unit_id, str(unit.get("html_path", "")), str(unit.get("html_sha256", ""))))
    for asset in assets.get("assets", []):
        if not isinstance(asset, Mapping):
            continue
        source = asset.get("source")
        open_test = asset.get("open_test")
        if isinstance(source, Mapping) and isinstance(open_test, Mapping):
            expected.append(("course_asset", "asset_id", str(asset.get("id", "")), str(source.get("uri", "")), str(open_test.get("sha256", ""))))
    for check in record.get("dependency_checks", []):
        if isinstance(check, Mapping):
            key = f"{check.get('from_unit')}->{check.get('to_unit')}"
            expected.append(("dependency_artifact", "dependency", key, str(check.get("artifact", "")), str(check.get("sha256", ""))))
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
        candidates = []
        for item in _artifact_items(evidence, kind):
            metadata = item.reference.get("metadata")
            if isinstance(metadata, Mapping) and metadata.get(metadata_key) == metadata_value:
                candidates.append(item)
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

    supplied = {
        str(item.reference.get("id"))
        for kind in G5_ARTIFACT_KINDS
        for item in _artifact_items(evidence, kind)
    }
    if supplied != matched:
        issues.append(GateValidationIssue("extra_artifact_evidence", "$.evidence", "G5 rejects unbound or extra artifact evidence"))
    return issues


def _validate_release(
    contract: Mapping[str, Any], evidence: Mapping[str, list[Any]]
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
        candidates = []
        for item in _artifact_items(evidence, "release_check"):
            metadata = item.reference.get("metadata")
            if isinstance(metadata, Mapping) and metadata.get("check_id") == check_id:
                candidates.append(item)
        if len(candidates) != 1:
            issues.append(GateValidationIssue("release_check_evidence_missing", f"$.checks.{check_id}", "each G6 check requires exactly one replayable typed evidence file"))
            continue
        item = candidates[0]
        matched.add(str(item.reference.get("id")))
        declared = check["evidence"]
        if item.reference.get("path") != declared.get("path") or item.sha256 != declared.get("sha256"):
            issues.append(GateValidationIssue("release_check_evidence_mismatch", f"$.checks.{check_id}.evidence", "G6 check path/hash must match the consumed evidence file"))
    supplied = {str(item.reference.get("id")) for item in _artifact_items(evidence, "release_check")}
    if supplied != matched:
        issues.append(GateValidationIssue("extra_release_check_evidence", "$.evidence.release_check", "G6 rejects extra or unbound release-check evidence"))
    return issues


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


def _consume_json(
    workspace_root: Path | str, reference: Mapping[str, Any], gate_id: str
) -> ConsumedEvidence:
    try:
        return consume_evidence_reference(
            workspace_root, reference, expected_gate=gate_id, parse_json=True
        )
    except (OSError, ValueError) as error:
        raise ContractStateError(f"invalid Gate evidence: {error}") from error


def _governed_roster_reference(contract: Mapping[str, Any]) -> Mapping[str, Any]:
    governance = contract.get("governance")
    binding = governance.get("production_role_roster") if isinstance(governance, Mapping) else None
    if not isinstance(binding, Mapping):
        raise ContractStateError("G4/G5 requires a governed production role roster")
    evidence_id = binding.get("evidence_id")
    references = _indexed_references(contract, [str(evidence_id)])
    reference = references[0]
    if (
        reference.get("kind") != "production_role_roster"
        or reference.get("gate") != "G0"
        or reference.get("sha256") != binding.get("sha256")
    ):
        raise ContractStateError("governed production role roster binding does not match its typed reference")
    return reference


def _validate_trial_receipt_binding(
    gate_id: str,
    values_by_kind: Mapping[str, list[Any]],
    consumed: Sequence[ConsumedEvidence],
    roster_sha256: str,
) -> list[GateValidationIssue]:
    trials = values_by_kind.get("independent_course_trial", [])
    refs = [item for item in consumed if item.reference.get("kind") == "independent_course_trial"]
    if len(trials) != 1 or len(refs) != 1 or not isinstance(trials[0], Mapping):
        return []
    trial = trials[0]
    metadata = refs[0].reference.get("metadata")
    participant = trial.get("participant")
    allowed_inputs = trial.get("allowed_inputs")
    hashes = sorted(
        str(item.get("sha256")) for item in allowed_inputs
        if isinstance(allowed_inputs, list) and isinstance(item, Mapping) and _text(item.get("sha256"))
    )
    context_id = trial.get("isolated_context_id")
    expected = {
        "runner_id": participant.get("id") if isinstance(participant, Mapping) else None,
        "session_id": context_id,
        "isolated_context_id": context_id,
        "roster_sha256": roster_sha256,
        "learner_input_hashes": hashes,
    }
    if not isinstance(metadata, Mapping) or any(metadata.get(key) != value for key, value in expected.items()):
        return [GateValidationIssue("trial_receipt_binding_mismatch", "$.evidence.independent_course_trial.metadata", f"{gate_id} trial receipt must bind roster, runner/session/context, and learner-visible input hashes")]
    return []


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
    consumed: list[ConsumedEvidence] = []
    for reference in references:
        kind = str(reference.get("kind"))
        parse_json = kind not in G5_ARTIFACT_KINDS and kind != "release_check"
        try:
            item = consume_evidence_reference(
                workspace_root, reference, expected_gate=gate_id, parse_json=parse_json
            )
        except (OSError, ValueError) as error:
            raise ContractStateError(f"invalid Gate evidence: {error}") from error
        consumed.append(item)
        values_by_kind.setdefault(kind, []).append(item.value if parse_json else item)

    if gate_id in {"G4", "G5"}:
        roster_reference = _governed_roster_reference(contract)
        roster = _consume_json(workspace_root, roster_reference, "G0")
        consumed.append(roster)
        values_by_kind.setdefault("production_role_roster", []).append(roster.value)

    rule = GATE_REGISTRY[gate_id]
    missing_kinds = sorted(rule.required_kinds - set(values_by_kind))
    if missing_kinds:
        raise ContractStateError(
            f"{gate_id} requires evidence kind(s): {', '.join(missing_kinds)}"
        )

    issues: list[GateValidationIssue] = []
    if gate_id in {"G4", "G5"}:
        binding = contract["governance"]["production_role_roster"]
        issues.extend(_validate_trial_receipt_binding(gate_id, values_by_kind, consumed, str(binding["sha256"])))
    issues.extend(rule.validator(contract, values_by_kind))
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

    gate_number = int(gate_id[1:])
    for prior in (f"G{index}" for index in range(gate_number)):
        if contract["gates"][prior].get("status") != "PASS":
            raise ContractStateError(f"{gate_id} requires {prior} PASS")
    record = contract["gates"][gate_id]
    if record.get("status") != "IN_PROGRESS":
        raise ContractStateError(f"cannot pass a gate in {record.get('status')!r} state")
    blockers = [
        risk for risk in record.get("risks", [])
        if isinstance(risk, Mapping) and risk.get("blocking") is True and risk.get("resolved") is not True
    ]
    if blockers:
        raise ContractStateError(f"{gate_id} has unresolved blocking risks")
    record["status"] = "PASS"
    revision = record.get("source_revision")
    record["source_revision"] = revision + 1 if isinstance(revision, int) else 1
    record["evidence"].append(
        {
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
    )
    return "PASS"
