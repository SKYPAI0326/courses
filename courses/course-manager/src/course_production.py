from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping


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
