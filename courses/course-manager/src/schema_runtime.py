from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class SchemaRuntimeIssue:
    code: str
    path: str
    message: str


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, Mapping)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def _resolve(root: Mapping[str, Any], reference: str) -> Mapping[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported schema reference: {reference}")
    value: Any = root
    for part in reference[2:].split("/"):
        value = value[part.replace("~1", "/").replace("~0", "~")]
    if not isinstance(value, Mapping):
        raise ValueError(f"schema reference does not resolve to an object: {reference}")
    return value


def _validate(
    value: Any,
    schema: Mapping[str, Any],
    root: Mapping[str, Any],
    path: str,
    issues: list[SchemaRuntimeIssue],
) -> None:
    if "$ref" in schema:
        _validate(value, _resolve(root, str(schema["$ref"])), root, path, issues)
        return
    if "oneOf" in schema:
        alternatives = schema["oneOf"]
        matches = 0
        for alternative in alternatives if isinstance(alternatives, list) else []:
            candidate: list[SchemaRuntimeIssue] = []
            if isinstance(alternative, Mapping):
                _validate(value, alternative, root, path, candidate)
            if not candidate:
                matches += 1
        if matches != 1:
            issues.append(SchemaRuntimeIssue("schema_one_of", path, "value must match exactly one allowed shape"))
        return
    if "const" in schema and value != schema["const"]:
        issues.append(SchemaRuntimeIssue("schema_const", path, f"value must equal {schema['const']!r}"))
    if "enum" in schema and value not in schema["enum"]:
        issues.append(SchemaRuntimeIssue("schema_enum", path, "value is not in the allowed enum"))
    expected = schema.get("type")
    if expected is not None:
        types = [expected] if isinstance(expected, str) else list(expected)
        if not any(_matches_type(value, item) for item in types):
            issues.append(SchemaRuntimeIssue("schema_type", path, f"value must have type {expected}"))
            return
    if isinstance(value, Mapping):
        required = schema.get("required", [])
        for key in required if isinstance(required, list) else []:
            if key not in value:
                issues.append(SchemaRuntimeIssue("schema_required", f"{path}.{key}", "required field is missing"))
        properties = schema.get("properties", {})
        if isinstance(properties, Mapping):
            if schema.get("additionalProperties") is False:
                for key in value:
                    if key not in properties:
                        issues.append(SchemaRuntimeIssue("schema_additional_property", f"{path}.{key}", "field is not allowed by the canonical schema"))
            for key, child in properties.items():
                if key in value and isinstance(child, Mapping):
                    _validate(value[key], child, root, f"{path}.{key}", issues)
    if isinstance(value, list):
        minimum = schema.get("minItems")
        if isinstance(minimum, int) and len(value) < minimum:
            issues.append(SchemaRuntimeIssue("schema_min_items", path, f"list requires at least {minimum} item(s)"))
        if schema.get("uniqueItems") is True:
            encoded = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in value]
            if len(set(encoded)) != len(encoded):
                issues.append(SchemaRuntimeIssue("schema_unique_items", path, "list items must be unique"))
        item_schema = schema.get("items")
        if isinstance(item_schema, Mapping):
            for index, item in enumerate(value):
                _validate(item, item_schema, root, f"{path}[{index}]", issues)
    if isinstance(value, str):
        minimum = schema.get("minLength")
        if isinstance(minimum, int) and len(value) < minimum:
            issues.append(SchemaRuntimeIssue("schema_min_length", path, f"text requires at least {minimum} character(s)"))
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.search(pattern, value) is None:
            issues.append(SchemaRuntimeIssue("schema_pattern", path, "text does not match the required pattern"))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        if isinstance(minimum, (int, float)) and value < minimum:
            issues.append(SchemaRuntimeIssue("schema_minimum", path, f"number must be at least {minimum}"))


def validate_schema_file(filename: str, value: Any) -> list[SchemaRuntimeIssue]:
    schema_path = Path(__file__).resolve().parents[1] / "contracts" / filename
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    issues: list[SchemaRuntimeIssue] = []
    _validate(value, schema, schema, "$", issues)
    return issues


__all__ = ["SchemaRuntimeIssue", "validate_schema_file"]
