from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


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
MATERIAL_UNKNOWN_PATTERN = re.compile(
    r"(?:帳號|權限|裝置|設備|瀏覽器|工具|素材|檔案|資料欄位|成果|交付物|語系|地區|"
    r"account|permission|device|browser|tool|material|asset|artifact|deliverable|locale)",
    re.IGNORECASE,
)
NON_MATERIAL_FALLBACK_PATTERN = re.compile(
    r"(?:若.+(?:改|使用|提供)|備援(?:方式|路徑|工具)|替代(?:方式|路徑|工具)|fallback|alternative)",
    re.IGNORECASE,
)

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


def validate_requirements_record(record: Mapping[str, Any]) -> list[RequirementsIssue]:
    issues: list[RequirementsIssue] = []
    if not isinstance(record, Mapping):
        return [RequirementsIssue("invalid_requirements_record", "$", "requirements record must be an object")]
    for field in sorted(set(record) - set(REQUIREMENTS_REQUIRED_FIELDS)):
        _issue(issues, "unsupported_field", f"$.{field}", f"canonical G0 does not allow {field}")
    for field in REQUIREMENTS_REQUIRED_FIELDS:
        if field not in record:
            _issue(issues, "missing_field", f"$.{field}", f"requirements record is missing {field}")
    if record.get("schema_version") != 1:
        _issue(issues, "unsupported_schema_version", "$.schema_version", "schema_version must be 1")
    seen: set[str] = set()
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
                if status not in {"OPEN", "RESOLVED"}:
                    _issue(issues, "invalid_unknown_status", f"{path}.status", "unknown status must be OPEN or RESOLVED")
                question = str(mapped.get("question", ""))
                resolution = str(mapped.get("resolution", ""))
                unknown_text = f"{question} {resolution}"
                material_by_content = (
                    MATERIAL_UNKNOWN_PATTERN.search(unknown_text) is not None
                    and NON_MATERIAL_FALLBACK_PATTERN.search(resolution) is None
                )
                if status != "RESOLVED" and (
                    mapped.get("material") is True or material_by_content
                ):
                    _issue(issues, "material_unknown", path, "an unresolved material unknown blocks G0")
    return issues


__all__ = [
    "REQUIREMENTS_REQUIRED_FIELDS",
    "RequirementsIssue",
    "validate_requirements_record",
]
