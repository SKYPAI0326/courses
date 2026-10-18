from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from src.schema_runtime import validate_schema_file


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VAGUE_VALUES = {
    "一般", "一般學員", "所有人", "任何人", "任何工具", "不限", "待確認", "未知",
    "完成課程", "了解概念", "學會內容", "general", "everyone", "any", "any tool",
    "unknown", "tbd", "todo",
}
VAGUE_PREFIXES = (
    "一般學員", "所有人", "任何人", "任何工具", "待確認", "未知",
    "完成課程", "了解概念", "學會內容", "general learner", "everyone",
    "any tool", "unknown", "tbd", "todo",
)
MATERIAL_DOMAINS = frozenset(
    {"tools", "accounts", "permissions", "device", "materials", "artifact", "time", "locale"}
)
REQUIREMENTS_PROSE_POLICY = {
    ("target_profile", "learner"): "required_text",
    ("target_profile", "baseline"): "required_text",
    ("target_profile", "prerequisites", "*"): "required_text_list_item",
    ("work_context", "situation"): "required_text",
    ("work_context", "problem"): "required_text",
    ("work_context", "use"): "required_text",
    ("final_artifact", "name"): "required_text",
    ("final_artifact", "format"): "required_text",
    ("final_artifact", "observable_result"): "required_text",
    ("final_artifact", "use"): "required_text",
    ("delivery", "mode"): "required_text",
    ("delivery", "break_buffer_policy"): "required_text",
    ("environment", "tools", "*"): "required_text_list_item",
    ("environment", "accounts", "*"): "required_text_list_item",
    ("environment", "permissions", "*"): "required_text_list_item",
    ("environment", "device"): "required_text",
    ("environment", "locale"): "required_text",
    ("constraints", "*", "description"): "required_text",
    ("constraints", "*", "impact"): "required_text",
    ("acceptance_criteria", "*", "statement"): "required_text",
    ("acceptance_criteria", "*", "capabilities", "*", "statement"): "required_text",
    ("known_facts", "*"): "required_text_list_item",
    ("assumptions", "*", "statement"): "required_text",
    ("assumptions", "*", "validation_plan"): "required_text",
    ("unknowns", "*", "question"): "required_text",
    ("unknowns", "*", "resolution"): "required_text",
    ("unknowns", "*", "fallback", "description"): "required_text",
    ("decisions", "*", "decision"): "required_text",
    ("decisions", "*", "rationale"): "required_text",
}

REQUIREMENTS_REQUIRED_FIELDS = (
    "schema_version", "requirements_id", "target_profile", "work_context",
    "final_artifact", "delivery", "environment", "constraints",
    "acceptance_criteria", "known_facts", "assumptions", "unknowns", "decisions",
)


@dataclass(frozen=True)
class RequirementsIssue:
    code: str
    path: str
    message: str
    return_gate: str = "G0"


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _meaningful(value: Any) -> bool:
    if not _text(value):
        return False
    normalized = value.strip().casefold()
    return normalized not in VAGUE_VALUES and not normalized.startswith(VAGUE_PREFIXES)


def _issue(issues: list[RequirementsIssue], code: str, path: str, message: str) -> None:
    issues.append(RequirementsIssue(code, path, message))


def _mapping_fields(value: Any, fields: Sequence[str], path: str, issues: list[RequirementsIssue]) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        _issue(issues, "incomplete_requirements", path, f"{path} must be an object")
        return None
    for field in fields:
        if not _meaningful(value.get(field)):
            code = "vague_requirement" if _text(value.get(field)) else "incomplete_requirements"
            _issue(issues, code, f"{path}.{field}", f"{field} must describe the real learner, work, result, or constraint")
    return value


def _text_list(value: Any, path: str, issues: list[RequirementsIssue]) -> list[str]:
    if not isinstance(value, list) or not value:
        _issue(issues, "incomplete_requirements", path, "a concrete text list is required")
        return []
    if any(not _meaningful(item) for item in value):
        _issue(issues, "vague_requirement", path, "generic or empty list items cannot establish G0")
        return []
    return list(value)


def _stable_id(value: Any, path: str, seen: set[str], issues: list[RequirementsIssue]) -> str | None:
    if not isinstance(value, str) or ID_PATTERN.fullmatch(value) is None:
        _issue(issues, "invalid_id", path, "stable ids use lowercase letters, digits, and hyphens")
        return None
    if value in seen:
        _issue(issues, "duplicate_id", path, f"duplicate stable id: {value}")
        return None
    seen.add(value)
    return value


def _normalized_prose(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return "".join(character for character in normalized if character.isalpha())


def _similar_boilerplate(left: str, right: str) -> bool:
    if min(len(left), len(right)) < 16:
        return False
    if min(len(left), len(right)) / max(len(left), len(right)) < 0.85:
        return False
    left_grams = {left[index:index + 3] for index in range(len(left) - 2)}
    right_grams = {right[index:index + 3] for index in range(len(right) - 2)}
    return bool(left_grams | right_grams) and len(left_grams & right_grams) / len(left_grams | right_grams) >= 0.9


def _prose_values(value: Any, path: str = "$", selector: tuple[str, ...] = ()):
    if isinstance(value, str) and selector in REQUIREMENTS_PROSE_POLICY:
        yield path, value
    elif isinstance(value, Mapping):
        for key, child in value.items():
            yield from _prose_values(child, f"{path}.{key}", selector + (str(key),))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _prose_values(child, f"{path}[{index}]", selector + ("*",))


def _validate_prose_distinctness(record: Mapping[str, Any], issues: list[RequirementsIssue]) -> None:
    owners: dict[str, str] = {}
    for path, text in _prose_values(record):
        normalized = _normalized_prose(text)
        if len(normalized) < 16:
            continue
        if re.fullmatch(r"(.{16,}?)\1+", normalized):
            _issue(issues, "padded_requirement", path, "repeated text cannot satisfy a requirement field")
        duplicate_path = next(
            (owner_path for prior, owner_path in owners.items() if _similar_boilerplate(normalized, prior)),
            None,
        )
        if duplicate_path is not None:
            _issue(issues, "duplicate_requirement_text", path, f"requirement prose duplicates {duplicate_path}")
        owners[normalized] = path


def validate_requirements_record(
    record: Mapping[str, Any],
    verified_support_records: Mapping[str, Mapping[str, Any]] | None = None,
) -> list[RequirementsIssue]:
    issues: list[RequirementsIssue] = []
    if not isinstance(record, Mapping):
        return [RequirementsIssue("invalid_requirements_record", "$", "requirements record must be an object")]
    issues.extend(
        RequirementsIssue(issue.code, issue.path, issue.message)
        for issue in validate_schema_file("course-requirements-record.schema.json", record)
    )
    for field in sorted(set(record) - set(REQUIREMENTS_REQUIRED_FIELDS)):
        _issue(issues, "unsupported_field", f"$.{field}", f"canonical G0 does not allow {field}")
    for field in REQUIREMENTS_REQUIRED_FIELDS:
        if field not in record:
            _issue(issues, "missing_field", f"$.{field}", f"requirements record is missing {field}")
    if record.get("schema_version") != 1:
        _issue(issues, "unsupported_schema_version", "$.schema_version", "schema_version must be 1")
    seen: set[str] = set()
    _validate_prose_distinctness(record, issues)
    _stable_id(record.get("requirements_id"), "$.requirements_id", seen, issues)

    target = _mapping_fields(record.get("target_profile"), ("learner", "baseline"), "$.target_profile", issues)
    if target is not None:
        _stable_id(target.get("id"), "$.target_profile.id", seen, issues)
        _text_list(target.get("prerequisites"), "$.target_profile.prerequisites", issues)
    _mapping_fields(record.get("work_context"), ("situation", "problem", "use"), "$.work_context", issues)
    _mapping_fields(record.get("final_artifact"), ("name", "format", "observable_result", "use"), "$.final_artifact", issues)

    delivery = _mapping_fields(record.get("delivery"), ("mode", "break_buffer_policy"), "$.delivery", issues)
    if delivery is not None and (
        not isinstance(delivery.get("available_minutes"), int)
        or isinstance(delivery.get("available_minutes"), bool)
        or delivery["available_minutes"] <= 0
    ):
        _issue(issues, "invalid_available_time", "$.delivery.available_minutes", "available_minutes must be a positive integer")

    environment = _mapping_fields(record.get("environment"), ("device", "locale"), "$.environment", issues)
    if environment is not None:
        for field in ("tools", "accounts", "permissions"):
            _text_list(environment.get(field), f"$.environment.{field}", issues)

    constraints = record.get("constraints")
    if not isinstance(constraints, list) or not constraints:
        _issue(issues, "incomplete_requirements", "$.constraints", "at least one real constraint is required")
    else:
        for index, constraint in enumerate(constraints):
            path = f"$.constraints[{index}]"
            item = _mapping_fields(constraint, ("description", "impact"), path, issues)
            if item is not None:
                _stable_id(item.get("id"), f"{path}.id", seen, issues)

    criteria = record.get("acceptance_criteria")
    if not isinstance(criteria, list) or not criteria:
        _issue(issues, "acceptance_criteria_required", "$.acceptance_criteria", "observable acceptance criteria are required")
    else:
        for index, criterion in enumerate(criteria):
            path = f"$.acceptance_criteria[{index}]"
            item = _mapping_fields(criterion, ("statement",), path, issues)
            if item is None:
                continue
            _stable_id(item.get("id"), f"{path}.id", seen, issues)
            capabilities = item.get("capabilities")
            if not isinstance(capabilities, list) or not capabilities:
                _issue(issues, "capabilities_required", f"{path}.capabilities", "each criterion requires observable child capabilities")
                continue
            for capability_index, capability in enumerate(capabilities):
                capability_path = f"{path}.capabilities[{capability_index}]"
                mapped = _mapping_fields(capability, ("statement",), capability_path, issues)
                if mapped is not None:
                    _stable_id(mapped.get("id"), f"{capability_path}.id", seen, issues)

    _text_list(record.get("known_facts"), "$.known_facts", issues)
    for collection, fields in (
        ("assumptions", ("statement", "validation_plan")),
        ("unknowns", ("question", "resolution")),
        ("decisions", ("decision", "rationale")),
    ):
        values = record.get(collection)
        if not isinstance(values, list) or not values:
            _issue(issues, "incomplete_requirements", f"$.{collection}", f"{collection} must record at least one concrete item")
            continue
        for index, value in enumerate(values):
            path = f"$.{collection}[{index}]"
            mapped = _mapping_fields(value, fields, path, issues)
            if mapped is None:
                continue
            _stable_id(mapped.get("id"), f"{path}.id", seen, issues)
            if collection in {"assumptions", "unknowns"} and not isinstance(mapped.get("material"), bool):
                _issue(issues, "invalid_materiality", f"{path}.material", "material must be a boolean decision")
            if collection == "unknowns":
                status = mapped.get("status")
                if status not in {"OPEN", "DEFERRED", "RESOLVED"}:
                    _issue(issues, "invalid_unknown_status", f"{path}.status", "unknown status must be OPEN, DEFERRED, or RESOLVED")
                domains = mapped.get("impact_domains")
                derived_material = isinstance(domains, list) and bool(set(domains) & MATERIAL_DOMAINS)
                fallback = mapped.get("fallback")
                support = (
                    verified_support_records.get(str(fallback.get("evidence_ref")))
                    if isinstance(fallback, Mapping) and verified_support_records is not None
                    else None
                )
                acceptance_ids = fallback.get("acceptance_criterion_ids") if isinstance(fallback, Mapping) else None
                known_criteria = {
                    item.get("id") for item in record.get("acceptance_criteria", [])
                    if isinstance(item, Mapping)
                }
                fallback_valid = (
                    isinstance(fallback, Mapping)
                    and _meaningful(fallback.get("description"))
                    and fallback.get("verification_status") == "VERIFIED_FALLBACK"
                    and isinstance(fallback.get("evidence_ref"), str)
                    and ID_PATTERN.fullmatch(fallback["evidence_ref"]) is not None
                    and fallback.get("preserves_acceptance") is True
                    and isinstance(support, Mapping)
                    and support.get("support_id") == fallback.get("evidence_ref")
                    and support.get("requirements_id") == record.get("requirements_id")
                    and support.get("unknown_id") == mapped.get("id")
                    and support.get("fallback_id") == fallback.get("fallback_id")
                    and support.get("acceptance_criterion_ids") == acceptance_ids
                    and support.get("preserved_acceptance_ids") == acceptance_ids
                    and isinstance(acceptance_ids, list) and bool(acceptance_ids)
                    and set(acceptance_ids).issubset(known_criteria)
                    and isinstance(support.get("alternative_path"), Mapping)
                    and support["alternative_path"].get("description") == fallback.get("description")
                )
                if fallback is not None and not fallback_valid:
                    _issue(issues, "invalid_fallback", f"{path}.fallback", "fallback must be verified, evidenced, and preserve acceptance")
                if status != "RESOLVED" and not fallback_valid:
                    _issue(issues, "unresolved_unknown", path, "an unresolved unknown requires a governed verified fallback")
                    if derived_material:
                        _issue(issues, "material_unknown", path, "an unresolved material unknown blocks G0")
    return issues


__all__ = [
    "REQUIREMENTS_PROSE_POLICY",
    "REQUIREMENTS_REQUIRED_FIELDS",
    "RequirementsIssue",
    "validate_requirements_record",
]
