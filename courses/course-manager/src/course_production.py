from __future__ import annotations

import copy
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Sequence

from src.course_contract import ContractStateError
from src.course_evidence import (
    canonical_json_bytes,
    register_evidence_file,
)
from src.course_validation import (
    evidence_maturity,
    production_role_ids,
    validate_trial_context_is_new,
    validate_trial_record,
)


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
RISK_FIELDS = (
    "failure_cost",
    "tool_uncertainty",
    "asset_dependency",
    "layout_complexity",
    "downstream_dependency",
)


@dataclass(frozen=True)
class ProductionIssue:
    code: str
    path: str
    message: str
    return_gate: str = "G4"


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _issue(
    issues: list[ProductionIssue], code: str, path: str, message: str
) -> None:
    issues.append(ProductionIssue(code, path, message, "G4"))


def _require_text_fields(
    value: Any,
    fields: tuple[str, ...],
    path: str,
    code: str,
    issues: list[ProductionIssue],
) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        _issue(issues, code, path, f"{path} must be an object")
        return None
    for field in fields:
        if not _text(value.get(field)):
            _issue(issues, code, f"{path}.{field}", f"{field} must contain text")
    return value


def select_pilot_unit(blueprint: Mapping[str, Any]) -> str:
    units = blueprint.get("units")
    if not isinstance(units, list) or not units:
        raise ValueError("blueprint requires at least one unit")
    candidates: list[tuple[tuple[int | float, ...], str]] = []
    for index, unit in enumerate(units):
        if not isinstance(unit, Mapping):
            raise ValueError(f"blueprint unit {index} must be an object")
        unit_id = unit.get("id")
        if not isinstance(unit_id, str) or not ID_PATTERN.fullmatch(unit_id):
            raise ValueError(f"blueprint unit {index} has an invalid id")
        risk = unit.get("risk")
        if not isinstance(risk, Mapping):
            raise ValueError(f"blueprint unit {unit_id} requires a risk record")
        values: list[int | float] = []
        for field in RISK_FIELDS:
            value = risk.get(field)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"blueprint unit {unit_id} risk {field} must be numeric")
            values.append(value)
        candidates.append((tuple(values), unit_id))
    return max(candidates, key=lambda item: (item[0], item[1]))[1]


def validate_asset_manifest(manifest: Mapping[str, Any]) -> list[ProductionIssue]:
    issues: list[ProductionIssue] = []
    if manifest.get("schema_version") != 1:
        _issue(
            issues,
            "unsupported_asset_schema",
            "$.schema_version",
            "asset manifest schema_version must be 1",
        )
    assets = manifest.get("assets")
    if not isinstance(assets, list) or not assets:
        _issue(issues, "assets_required", "$.assets", "asset manifest must list assets")
        return issues
    seen: set[str] = set()
    required_fields = (
        "id",
        "learner_label",
        "purpose",
        "source",
        "rights",
        "version",
        "access",
        "open_test",
    )
    for index, asset in enumerate(assets):
        path = f"$.assets[{index}]"
        if not isinstance(asset, Mapping):
            _issue(issues, "incomplete_asset", path, "asset must be an object")
            continue
        for field in required_fields:
            if field not in asset:
                _issue(
                    issues,
                    "incomplete_asset",
                    f"{path}.{field}",
                    f"asset is missing {field}",
                )
        asset_id = asset.get("id")
        if not isinstance(asset_id, str) or not ID_PATTERN.fullmatch(asset_id):
            _issue(issues, "incomplete_asset", f"{path}.id", "asset id is invalid")
        elif asset_id in seen:
            _issue(issues, "duplicate_asset", f"{path}.id", "asset id is duplicated")
        else:
            seen.add(asset_id)
        for field in ("learner_label", "purpose", "version"):
            if not _text(asset.get(field)):
                _issue(
                    issues,
                    "incomplete_asset",
                    f"{path}.{field}",
                    f"asset {field} must contain text",
                )
        _require_text_fields(
            asset.get("source"),
            ("type", "uri", "retrieved_at"),
            f"{path}.source",
            "incomplete_asset",
            issues,
        )
        rights = _require_text_fields(
            asset.get("rights"),
            ("status", "basis"),
            f"{path}.rights",
            "incomplete_asset",
            issues,
        )
        if rights is not None and rights.get("status") != "CLEARED":
            _issue(
                issues,
                "asset_rights_not_cleared",
                f"{path}.rights.status",
                "asset rights must be CLEARED before learner use",
            )
        _require_text_fields(
            asset.get("access"),
            ("method", "learner_path", "backup"),
            f"{path}.access",
            "incomplete_asset",
            issues,
        )
        open_test = _require_text_fields(
            asset.get("open_test"),
            ("tested_at", "actor", "result", "sha256"),
            f"{path}.open_test",
            "incomplete_asset",
            issues,
        )
        if open_test is not None:
            if open_test.get("result") != "PASS":
                _issue(
                    issues,
                    "asset_open_failed",
                    f"{path}.open_test.result",
                    "asset must open successfully from the learner path",
                )
            if not SHA256_PATTERN.fullmatch(str(open_test.get("sha256", ""))):
                _issue(
                    issues,
                    "incomplete_asset",
                    f"{path}.open_test.sha256",
                    "asset open test must identify the tested file hash",
                )
    return issues


def _validate_visual_decision(
    decision: Any, issues: list[ProductionIssue]
) -> None:
    if not isinstance(decision, Mapping):
        _issue(
            issues,
            "incomplete_visual_decision",
            "$.visual_decision",
            "course-specific visual decision is required",
        )
        return
    inputs = decision.get("inputs")
    if not isinstance(inputs, Mapping):
        _issue(
            issues,
            "incomplete_visual_decision",
            "$.visual_decision.inputs",
            "visual inputs must be an object",
        )
    else:
        for field in ("topic", "learner", "task", "content_density"):
            if not _text(inputs.get(field)):
                _issue(
                    issues,
                    "incomplete_visual_decision",
                    f"$.visual_decision.inputs.{field}",
                    f"visual decision must consider {field}",
                )
        devices = inputs.get("primary_devices")
        if not isinstance(devices, list) or not devices or not all(_text(item) for item in devices):
            _issue(
                issues,
                "incomplete_visual_decision",
                "$.visual_decision.inputs.primary_devices",
                "visual decision must consider learner devices",
            )
    _require_text_fields(
        decision.get("decisions"),
        ("layout_rationale", "navigation", "typography", "color", "responsive_strategy"),
        "$.visual_decision.decisions",
        "incomplete_visual_decision",
        issues,
    )


def validate_pilot_record(
    record: Mapping[str, Any],
    lesson_record: Mapping[str, Any],
    asset_manifest: Mapping[str, Any],
) -> list[ProductionIssue]:
    issues = validate_asset_manifest(asset_manifest)
    if record.get("schema_version") != 1:
        _issue(
            issues,
            "unsupported_pilot_schema",
            "$.schema_version",
            "pilot record schema_version must be 1",
        )
    unit_id = record.get("unit_id")
    if unit_id != lesson_record.get("unit_id") or not isinstance(unit_id, str):
        _issue(
            issues,
            "pilot_unit_mismatch",
            "$.unit_id",
            "pilot unit must match the lesson record",
        )
    if not _text(record.get("trial_context_id")):
        _issue(
            issues,
            "pilot_trial_context_required",
            "$.trial_context_id",
            "pilot must bind the isolated independent trial context",
        )
    for field in ("lesson_sha256", "html_sha256"):
        if not SHA256_PATTERN.fullmatch(str(record.get(field, ""))):
            _issue(
                issues,
                "pilot_hash_required",
                f"$.{field}",
                f"{field} must be a lowercase SHA-256",
            )
    if not _text(record.get("html_path")):
        _issue(issues, "html_path_required", "$.html_path", "pilot HTML path is required")

    asset_ids = record.get("asset_ids")
    lesson_asset_ids = lesson_record.get("asset_references")
    manifest_assets = asset_manifest.get("assets")
    known_asset_ids = {
        item.get("id")
        for item in manifest_assets
        if isinstance(manifest_assets, list) and isinstance(item, Mapping)
    } if isinstance(manifest_assets, list) else set()
    if not isinstance(asset_ids, list) or not asset_ids:
        _issue(issues, "pilot_assets_required", "$.asset_ids", "pilot must use lesson assets")
    else:
        expected = set(lesson_asset_ids) if isinstance(lesson_asset_ids, list) else set()
        if set(asset_ids) != expected or not set(asset_ids).issubset(known_asset_ids):
            _issue(
                issues,
                "pilot_asset_mismatch",
                "$.asset_ids",
                "pilot assets must match lesson references and the asset manifest",
            )

    _validate_visual_decision(record.get("visual_decision"), issues)

    fidelity = record.get("content_fidelity")
    if not isinstance(fidelity, Mapping):
        _issue(
            issues,
            "content_fidelity_failed",
            "$.content_fidelity",
            "content fidelity evidence is required",
        )
    else:
        source_hash = fidelity.get("source_sha256")
        rendered_hash = fidelity.get("rendered_source_sha256")
        atoms = fidelity.get("teaching_atoms")
        if (
            source_hash != record.get("lesson_sha256")
            or rendered_hash != source_hash
            or not isinstance(atoms, list)
            or not atoms
            or fidelity.get("result") != "PASS"
        ):
            _issue(
                issues,
                "content_fidelity_failed",
                "$.content_fidelity",
                "rendered pilot must preserve the reviewed lesson source and teaching atoms",
            )

    render = _require_text_fields(
        record.get("render"),
        ("browser", "tested_at", "result"),
        "$.render",
        "render_evidence_required",
        issues,
    )
    if render is not None:
        screenshots = render.get("screenshots")
        if not isinstance(screenshots, list) or not screenshots or not all(
            _text(item) for item in screenshots
        ):
            _issue(
                issues,
                "render_evidence_required",
                "$.render.screenshots",
                "real browser screenshots are required",
            )
        if render.get("result") != "PASS":
            _issue(
                issues,
                "render_evidence_required",
                "$.render.result",
                "browser render must pass",
            )

    devices = record.get("devices")
    if not isinstance(devices, Mapping):
        _issue(
            issues,
            "device_evidence_required",
            "$.devices",
            "mobile, tablet, and desktop evidence is required",
        )
    else:
        for device in ("mobile", "tablet", "desktop"):
            result = devices.get(device)
            if (
                not isinstance(result, Mapping)
                or not _text(result.get("viewport"))
                or result.get("core_path_result") != "PASS"
                or result.get("horizontal_overflow") is not False
            ):
                _issue(
                    issues,
                    "device_evidence_required",
                    f"$.devices.{device}",
                    f"{device} must pass the core path without horizontal overflow",
                )

    accessibility = record.get("accessibility")
    if not isinstance(accessibility, Mapping):
        _issue(
            issues,
            "manual_accessibility_required",
            "$.accessibility",
            "automated and manual accessibility evidence is required",
        )
    else:
        automated = _require_text_fields(
            accessibility.get("automated"),
            ("tool", "result", "report_path"),
            "$.accessibility.automated",
            "automated_accessibility_required",
            issues,
        )
        if automated is not None and automated.get("result") != "PASS":
            _issue(
                issues,
                "automated_accessibility_required",
                "$.accessibility.automated.result",
                "automated accessibility check must pass",
            )
        manual = _require_text_fields(
            accessibility.get("manual"),
            (
                "evaluator_id",
                "keyboard_result",
                "focus_result",
                "reading_sequence_result",
                "notes",
            ),
            "$.accessibility.manual",
            "manual_accessibility_required",
            issues,
        )
        if manual is not None and any(
            manual.get(field) != "PASS"
            for field in ("keyboard_result", "focus_result", "reading_sequence_result")
        ):
            _issue(
                issues,
                "manual_accessibility_required",
                "$.accessibility.manual",
                "keyboard, focus, and reading sequence must all pass manual evaluation",
            )

    _require_text_fields(
        record.get("navigation"),
        ("entry", "previous", "next"),
        "$.navigation",
        "navigation_evidence_required",
        issues,
    )
    return issues


def _full_issue(
    issues: list[ProductionIssue],
    code: str,
    path: str,
    message: str,
    return_gate: str = "G5",
) -> None:
    issues.append(ProductionIssue(code, path, message, return_gate))


def _record_map(
    values: Any,
    id_field: str,
    path: str,
    code: str,
    issues: list[ProductionIssue],
) -> dict[str, Mapping[str, Any]]:
    if not isinstance(values, list):
        _full_issue(issues, code, path, f"{path} must be a list")
        return {}
    result: dict[str, Mapping[str, Any]] = {}
    for index, value in enumerate(values):
        item_path = f"{path}[{index}]"
        if not isinstance(value, Mapping):
            _full_issue(issues, code, item_path, "record must be an object")
            continue
        item_id = value.get(id_field)
        if not _text(item_id):
            _full_issue(issues, code, f"{item_path}.{id_field}", f"{id_field} is required")
        elif item_id in result:
            _full_issue(issues, code, f"{item_path}.{id_field}", f"duplicate {id_field}: {item_id}")
        else:
            result[item_id] = value
    return result


def validate_full_production(
    record: Mapping[str, Any],
    blueprint: Mapping[str, Any],
    lessons: Sequence[Mapping[str, Any]],
    assets: Mapping[str, Any],
    pilot: Mapping[str, Any],
    trial: Mapping[str, Any],
    *,
    production_roles: Mapping[str, Any] | None = None,
) -> list[ProductionIssue]:
    issues: list[ProductionIssue] = []
    if record.get("schema_version") != 1:
        _full_issue(
            issues,
            "unsupported_production_schema",
            "$.schema_version",
            "full production schema_version must be 1",
        )
    if not _text(record.get("course_id")):
        _full_issue(issues, "production_identity_missing", "$.course_id", "course id is required")

    authors = record.get("production_authors")
    if not isinstance(authors, list) or not authors or not all(_text(item) for item in authors):
        _full_issue(
            issues,
            "production_identity_missing",
            "$.production_authors",
            "production authors are required to prove trial independence",
        )
        authors = []

    trial_roles: Sequence[str] | Mapping[str, Any] = authors
    if production_roles is not None:
        try:
            governed_role_ids = production_role_ids(production_roles)
        except ValueError as error:
            _full_issue(
                issues,
                "production_role_roster_invalid",
                "$.production_roles",
                str(error),
            )
            governed_role_ids = ()
        governed_authors = production_roles.get("authors")
        if (
            not isinstance(governed_authors, list)
            or set(authors) != set(governed_authors)
        ):
            _full_issue(
                issues,
                "production_role_roster_mismatch",
                "$.production_authors",
                "self-declared production authors must match the governed role roster",
            )
        trial_roles = governed_role_ids

    blueprint_units = _record_map(
        blueprint.get("units"), "id", "$.blueprint.units", "production_unit_coverage", issues
    )
    lesson_units = _record_map(
        list(lessons), "unit_id", "$.lessons", "production_unit_coverage", issues
    )
    production_units = _record_map(
        record.get("units"), "unit_id", "$.units", "production_unit_coverage", issues
    )
    expected_ids = list(blueprint_units)
    if set(production_units) != set(blueprint_units) or set(lesson_units) != set(blueprint_units):
        _full_issue(
            issues,
            "production_unit_coverage",
            "$.units",
            "production and reviewed lessons must cover every blueprint unit exactly once",
        )

    asset_records = assets.get("assets")
    known_assets = {
        item.get("id")
        for item in asset_records
        if isinstance(asset_records, list) and isinstance(item, Mapping) and _text(item.get("id"))
    } if isinstance(asset_records, list) else set()
    if validate_asset_manifest(assets):
        _full_issue(
            issues,
            "production_asset_coverage",
            "$.assets",
            "full production requires a valid, open-tested asset manifest",
            "G4",
        )

    learning_signatures: dict[tuple[str, str], str] = {}
    for index, unit_id in enumerate(expected_ids):
        blueprint_unit = blueprint_units[unit_id]
        production_unit = production_units.get(unit_id)
        lesson = lesson_units.get(unit_id)
        if production_unit is None or lesson is None:
            continue
        path = f"$.units[{unit_id}]"
        expected_assets = blueprint_unit.get("asset_ids")
        lesson_assets = lesson.get("asset_references")
        produced_assets = production_unit.get("asset_ids")
        if (
            not isinstance(expected_assets, list)
            or not isinstance(lesson_assets, list)
            or not isinstance(produced_assets, list)
            or set(expected_assets) != set(lesson_assets)
            or set(expected_assets) != set(produced_assets)
            or not set(produced_assets).issubset(known_assets)
        ):
            _full_issue(
                issues,
                "production_asset_coverage",
                f"{path}.asset_ids",
                "unit assets must match blueprint, reviewed lesson, and asset manifest",
                "G4",
            )
        outcome = production_unit.get("outcome")
        workflow = production_unit.get("workflow_fingerprint")
        if (
            outcome != blueprint_unit.get("outcome")
            or outcome != lesson.get("outcome")
            or workflow != blueprint_unit.get("workflow_fingerprint")
            or workflow != lesson.get("workflow_fingerprint")
        ):
            _full_issue(
                issues,
                "production_content_mismatch",
                path,
                "produced unit outcome and workflow must match the reviewed blueprint and lesson",
                "G3",
            )
        if _text(outcome) and _text(workflow):
            signature = (outcome.strip().casefold(), workflow.strip().casefold())
            if signature in learning_signatures:
                _full_issue(
                    issues,
                    "duplicate_unit_learning",
                    path,
                    f"unit repeats the outcome and workflow of {learning_signatures[signature]}",
                    "G2",
                )
            else:
                learning_signatures[signature] = unit_id
        for field in ("lesson_sha256", "html_sha256"):
            if not SHA256_PATTERN.fullmatch(str(production_unit.get(field, ""))):
                _full_issue(
                    issues,
                    "production_file_evidence_missing",
                    f"{path}.{field}",
                    f"{field} must be a lowercase SHA-256",
                )
        if not _text(production_unit.get("html_path")):
            _full_issue(
                issues,
                "production_file_evidence_missing",
                f"{path}.html_path",
                "learner HTML path is required",
            )
        expected_dependencies = blueprint_unit.get("depends_on")
        if (
            not isinstance(expected_dependencies, list)
            or production_unit.get("depends_on") != expected_dependencies
            or lesson.get("depends_on") != expected_dependencies
        ):
            _full_issue(
                issues,
                "dependency_continuity_failed",
                f"{path}.depends_on",
                "unit dependencies must match the blueprint and reviewed lesson",
            )
        previous_id = None if index == 0 else expected_ids[index - 1]
        next_id = None if index == len(expected_ids) - 1 else expected_ids[index + 1]
        if production_unit.get("previous") != previous_id or production_unit.get("next") != next_id:
            _full_issue(
                issues,
                "navigation_incomplete",
                path,
                "each unit must link to the expected previous and next unit",
            )

    navigation = record.get("navigation")
    if (
        not isinstance(navigation, Mapping)
        or not _text(navigation.get("entry"))
        or navigation.get("order") != expected_ids
        or not _text(navigation.get("completion"))
    ):
        _full_issue(
            issues,
            "navigation_incomplete",
            "$.navigation",
            "course entry, exact unit order, and completion destination are required",
        )

    checks = record.get("dependency_checks")
    valid_checks: set[tuple[str, str]] = set()
    if isinstance(checks, list):
        for index, check in enumerate(checks):
            if (
                isinstance(check, Mapping)
                and _text(check.get("from_unit"))
                and _text(check.get("to_unit"))
                and _text(check.get("artifact"))
                and check.get("result") == "PASS"
            ):
                valid_checks.add((check["from_unit"], check["to_unit"]))
            else:
                _full_issue(
                    issues,
                    "dependency_continuity_failed",
                    f"$.dependency_checks[{index}]",
                    "dependency check requires both units, a real artifact, and PASS",
                )
    else:
        _full_issue(
            issues,
            "dependency_continuity_failed",
            "$.dependency_checks",
            "cross-unit dependency checks are required",
        )
    expected_edges = {
        (dependency, unit_id)
        for unit_id, unit in blueprint_units.items()
        for dependency in unit.get("depends_on", [])
        if isinstance(dependency, str)
    }
    if valid_checks != expected_edges:
        _full_issue(
            issues,
            "dependency_continuity_failed",
            "$.dependency_checks",
            "every blueprint dependency must be demonstrated by a passing artifact handoff",
        )

    pilot_unit = pilot.get("unit_id")
    if pilot_unit not in production_units:
        _full_issue(
            issues,
            "pilot_not_integrated",
            "$.pilot.unit_id",
            "the passed representative unit must be included in full production",
            "G4",
        )
    g4_context = record.get("g4_trial_context_id")
    if not _text(g4_context) or pilot.get("trial_context_id") != g4_context:
        _full_issue(
            issues,
            "g5_trial_context_invalid",
            "$.g4_trial_context_id",
            "full production must identify the exact G4 trial context",
            "G4",
        )

    if record.get("full_course_trial") != trial:
        _full_issue(
            issues,
            "g5_trial_context_invalid",
            "$.full_course_trial",
            "embedded full-course trial must match the validated trial record",
        )
    trial_issues = validate_trial_record(trial, trial_roles, "full_course")
    for issue in trial_issues:
        _full_issue(
            issues,
            issue.code,
            f"$.full_course_trial{issue.path[1:]}",
            issue.message,
            issue.return_gate,
        )
    if evidence_maturity(trial) != "INDEPENDENT_AI_VERIFIED":
        _full_issue(
            issues,
            "independent_participant_required",
            "$.full_course_trial.participant.type",
            "G5 requires a passing independent AI learner trial",
        )
    for issue in validate_trial_context_is_new(trial, (str(g4_context or ""),)):
        _full_issue(
            issues,
            issue.code,
            f"$.full_course_trial{issue.path[1:]}",
            issue.message,
            issue.return_gate,
        )

    expected_acceptance = blueprint.get("final_acceptance")
    final_artifact = record.get("final_artifact")
    acceptance_ok = isinstance(expected_acceptance, Mapping) and isinstance(final_artifact, Mapping)
    if acceptance_ok:
        acceptance = final_artifact.get("acceptance")
        expected_criteria = expected_acceptance.get("criteria_ids")
        acceptance_ok = (
            final_artifact.get("outcome_id") == expected_acceptance.get("outcome_id")
            and _text(final_artifact.get("path"))
            and SHA256_PATTERN.fullmatch(str(final_artifact.get("sha256", ""))) is not None
            and isinstance(expected_criteria, list)
            and isinstance(acceptance, list)
        )
        if acceptance_ok:
            results = {
                item.get("criterion_id"): item
                for item in acceptance
                if isinstance(item, Mapping) and _text(item.get("criterion_id"))
            }
            acceptance_ok = (
                set(results) == set(expected_criteria)
                and all(
                    item.get("result") == "PASS" and _text(item.get("evidence"))
                    for item in results.values()
                )
            )
    if not acceptance_ok:
        _full_issue(
            issues,
            "g0_acceptance_mismatch",
            "$.final_artifact",
            "final artifact must match the G0 outcome and pass every acceptance criterion",
            "G0",
        )

    validation = record.get("validation")
    if not isinstance(validation, Mapping) or any(
        not _text(validation.get(field))
        for field in ("validator_id", "validated_at")
    ) or validation.get("status") != "PASS":
        _full_issue(
            issues,
            "production_validation_missing",
            "$.validation",
            "full production requires a named validator and PASS timestamp",
        )
    return issues


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
    trial_record_path: str,
) -> str:
    if not evidence_refs:
        raise ValueError("G5 routing requires production evidence references")
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
    bundle = {
        "record": dict(record),
        "blueprint": dict(blueprint),
        "lessons": [dict(item) for item in lessons],
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
    trial_digest = hashlib.sha256(canonical_json_bytes(trial)).hexdigest()
    trial_id = f"g5-independent-trial-{trial_digest[:12]}"
    if trial_id in existing_ids or trial_id in production_ids or trial_id == record_id:
        raise ContractStateError(f"full-course trial evidence id already exists: {trial_id}")
    participant = trial.get("participant")
    allowed_inputs = trial.get("allowed_inputs")
    learner_input_hashes = sorted(
        str(item.get("sha256")) for item in allowed_inputs
        if isinstance(allowed_inputs, list) and isinstance(item, Mapping) and _text(item.get("sha256"))
    )
    context_id = trial.get("isolated_context_id")
    trial_reference = register_evidence_file(
        workspace_root,
        evidence_id=trial_id,
        gate_id="G5",
        kind="independent_course_trial",
        relative_path=trial_record_path,
        maturity=evidence_maturity(trial),
        metadata={
            "scope": "full_course",
            "participant_id": participant.get("id") if isinstance(participant, Mapping) else None,
            "runner_id": participant.get("id") if isinstance(participant, Mapping) else None,
            "session_id": context_id,
            "isolated_context_id": context_id,
            "roster_sha256": roster_binding.get("sha256"),
            "learner_input_hashes": learner_input_hashes,
        },
    )
    if trial_reference["sha256"] != trial_digest:
        raise ContractStateError(
            "registered full-course trial file does not match the production record"
        )
    staged_refs.extend([record_reference, trial_reference])
    evidence_index.extend(staged_refs)
    from src.course_gate import validate_and_transition_gate

    return validate_and_transition_gate(
        contract,
        "G5",
        [
            *production_ids,
            record_id,
            trial_id,
        ],
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
    production_record_path: str, trial_record_path: str,
) -> str:
    staged = copy.deepcopy(contract)
    result = _route_full_production_to_g5(
        staged, record, evidence_refs, actor, at,
        workspace_root=workspace_root, blueprint=blueprint, lessons=lessons,
        assets=assets, pilot=pilot,
        production_role_evidence_id=production_role_evidence_id,
        production_record_path=production_record_path,
        trial_record_path=trial_record_path,
    )
    contract.clear()
    contract.update(staged)
    return result
