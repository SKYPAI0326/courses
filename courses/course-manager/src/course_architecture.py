from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from src.schema_runtime import validate_schema_file


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
NON_EXECUTABLE = {"介紹", "完成示範", "講解概念", "練習", "評量", "todo", "tbd"}
NON_EXECUTABLE_PATTERN = re.compile(
    r"(?:\bTODO\b|\bTBD\b|待補(?:充|寫|資料)?|之後補|此處放|placeholder)",
    re.IGNORECASE,
)
BLUEPRINT_REQUIRED_FIELDS = (
    "schema_version", "blueprint_id", "requirements_id", "decision_narrative",
    "outcomes", "criteria", "units", "duration", "materials", "risks",
)
BLUEPRINT_OPTIONAL_FIELDS = frozenset({"course_id", "final_acceptance"})


@dataclass(frozen=True)
class ArchitectureIssue:
    code: str
    path: str
    message: str
    return_gate: str = "G2"


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _concrete(value: Any) -> bool:
    if not _text(value):
        return False
    normalized = value.strip().casefold()
    return (
        normalized not in NON_EXECUTABLE
        and not normalized.startswith("介紹 ")
        and NON_EXECUTABLE_PATTERN.search(value) is None
    )


def _issue(issues: list[ArchitectureIssue], code: str, path: str, message: str, gate: str = "G2") -> None:
    issues.append(ArchitectureIssue(code, path, message, gate))


def _records(value: Any, id_field: str, path: str, issues: list[ArchitectureIssue]) -> dict[str, Mapping[str, Any]]:
    if not isinstance(value, list) or not value:
        _issue(issues, "missing_blueprint_section", path, f"{path} must be a non-empty list")
        return {}
    result: dict[str, Mapping[str, Any]] = {}
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, Mapping):
            _issue(issues, "invalid_blueprint_record", item_path, "record must be an object")
            continue
        item_id = item.get(id_field)
        if not isinstance(item_id, str) or ID_PATTERN.fullmatch(item_id) is None:
            _issue(issues, "invalid_id", f"{item_path}.{id_field}", "stable id is invalid")
        elif item_id in result:
            _issue(issues, "duplicate_id", f"{item_path}.{id_field}", f"duplicate stable id: {item_id}")
        else:
            result[item_id] = item
    return result


def _string_list(value: Any, path: str, issues: list[ArchitectureIssue], code: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(_concrete(item) for item in value):
        _issue(issues, code, path, "a non-empty list of concrete statements is required")
        return []
    return list(value)


def _reference_list(
    value: Any, path: str, issues: list[ArchitectureIssue], code: str
) -> list[str]:
    refs = _string_list(value, path, issues, code)
    if refs and (
        len(set(refs)) != len(refs)
        or any(ID_PATTERN.fullmatch(ref) is None for ref in refs)
    ):
        duplicate = len(set(refs)) != len(refs)
        _issue(
            issues,
            "duplicate_reference" if duplicate else "invalid_id",
            path,
            "stable reference lists require unique lowercase IDs",
        )
        return []
    return refs


def _require_fields(value: Any, fields: Sequence[str], path: str, issues: list[ArchitectureIssue]) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        _issue(issues, "non_executable_unit", path, f"{path} must be an object")
        return None
    for field in fields:
        if not _concrete(value.get(field)):
            _issue(issues, "non_executable_unit", f"{path}.{field}", f"{field} must describe executable teaching")
    return value


def _capability_pairs(requirements: Mapping[str, Any]) -> dict[str, str]:
    pairs: dict[str, str] = {}
    criteria = requirements.get("acceptance_criteria")
    if isinstance(criteria, list):
        for criterion in criteria:
            if not isinstance(criterion, Mapping) or not _text(criterion.get("id")):
                continue
            capabilities = criterion.get("capabilities")
            if not isinstance(capabilities, list):
                continue
            for capability in capabilities:
                if isinstance(capability, Mapping) and _text(capability.get("id")):
                    pairs[str(capability["id"])] = str(criterion["id"])
    return pairs


def _has_cycle(units: Mapping[str, Mapping[str, Any]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(unit_id: str) -> bool:
        if unit_id in visiting:
            return True
        if unit_id in visited:
            return False
        visiting.add(unit_id)
        dependencies = units[unit_id].get("prerequisite_unit_ids")
        if isinstance(dependencies, list):
            for dependency in dependencies:
                if dependency in units and visit(dependency):
                    return True
        visiting.remove(unit_id)
        visited.add(unit_id)
        return False

    return any(visit(unit_id) for unit_id in units)


def _disconnected_units(units: Mapping[str, Mapping[str, Any]]) -> set[str]:
    """Return units outside the dependency graph component containing the first unit."""
    if not units:
        return set()
    neighbours = {unit_id: set() for unit_id in units}
    for unit_id, unit in units.items():
        dependencies = unit.get("prerequisite_unit_ids")
        if not isinstance(dependencies, list):
            continue
        for dependency in dependencies:
            if dependency in units:
                neighbours[unit_id].add(dependency)
                neighbours[dependency].add(unit_id)
    pending = [next(iter(units))]
    connected: set[str] = set()
    while pending:
        unit_id = pending.pop()
        if unit_id in connected:
            continue
        connected.add(unit_id)
        pending.extend(neighbours[unit_id] - connected)
    return set(units) - connected


def validate_course_blueprint(
    record: Mapping[str, Any],
    requirements: Mapping[str, Any],
    known_g1_evidence_ids: set[str] | frozenset[str] | None = None,
) -> list[ArchitectureIssue]:
    issues: list[ArchitectureIssue] = []
    if not isinstance(record, Mapping):
        return [ArchitectureIssue("invalid_blueprint", "$", "blueprint must be an object")]
    issues.extend(
        ArchitectureIssue(issue.code, issue.path, issue.message)
        for issue in validate_schema_file("course-blueprint-record.schema.json", record)
    )
    allowed_fields = set(BLUEPRINT_REQUIRED_FIELDS) | set(BLUEPRINT_OPTIONAL_FIELDS)
    for field in sorted(set(record) - allowed_fields):
        _issue(issues, "unsupported_field", f"$.{field}", f"canonical G2 does not allow {field}")
    for field in BLUEPRINT_REQUIRED_FIELDS:
        if field not in record:
            _issue(issues, "missing_blueprint_section", f"$.{field}", f"blueprint is missing {field}")
    if record.get("schema_version") != 1:
        _issue(issues, "unsupported_schema_version", "$.schema_version", "schema_version must be 1")
    for field in ("blueprint_id", "requirements_id"):
        if not isinstance(record.get(field), str) or ID_PATTERN.fullmatch(str(record.get(field))) is None:
            _issue(issues, "invalid_id", f"$.{field}", f"{field} must be a stable id")
    if record.get("requirements_id") != requirements.get("requirements_id"):
        _issue(issues, "requirements_mismatch", "$.requirements_id", "blueprint must bind the exact G0 requirements")

    narrative = record.get("decision_narrative")
    if not isinstance(narrative, Mapping):
        _issue(issues, "decision_narrative_required", "$.decision_narrative", "one reasoned main path is required")
    else:
        for field in ("recommended_path", "rationale", "constraint_fit"):
            if not _concrete(narrative.get(field)):
                _issue(issues, "decision_narrative_required", f"$.decision_narrative.{field}", "decision narrative must explain the recommended path")
        narrative_refs = _reference_list(narrative.get("g1_evidence_refs"), "$.decision_narrative.g1_evidence_refs", issues, "evidence_reference_required")
        if known_g1_evidence_ids is not None and any(ref not in known_g1_evidence_ids for ref in narrative_refs):
            _issue(issues, "unknown_g1_evidence", "$.decision_narrative.g1_evidence_refs", "decision narrative references evidence outside the governed G1 PASS set")

    outcomes = _records(record.get("outcomes"), "id", "$.outcomes", issues)
    criteria = _records(record.get("criteria"), "id", "$.criteria", issues)
    units = _records(record.get("units"), "id", "$.units", issues)
    capability_pairs = _capability_pairs(requirements)
    criterion_capabilities: dict[str, str] = {}

    for outcome_id, outcome in outcomes.items():
        if not _concrete(outcome.get("statement")):
            _issue(issues, "orphan_outcome", f"$.outcomes.{outcome_id}.statement", "outcome requires observable performance")
        refs = _reference_list(
            outcome.get("criterion_ids"),
            f"$.outcomes.{outcome_id}.criterion_ids",
            issues,
            "orphan_outcome",
        )
        if not refs:
            _issue(issues, "orphan_outcome", f"$.outcomes.{outcome_id}.criterion_ids", "outcome requires at least one child criterion")
        elif any(ref not in criteria for ref in refs):
            _issue(issues, "unknown_reference", f"$.outcomes.{outcome_id}.criterion_ids", "outcome references an unknown criterion")

    for criterion_id, criterion in criteria.items():
        for field in ("statement", "assessment_evidence"):
            if not _concrete(criterion.get(field)):
                _issue(issues, "incomplete_criterion", f"$.criteria.{criterion_id}.{field}", "criterion requires observable assessment evidence")
        outcome_id = criterion.get("outcome_id")
        capability_id = criterion.get("capability_id")
        g0_id = criterion.get("g0_criterion_id")
        if outcome_id not in outcomes:
            _issue(issues, "unknown_reference", f"$.criteria.{criterion_id}.outcome_id", "criterion references an unknown outcome")
        elif criterion_id not in outcomes[outcome_id].get("criterion_ids", []):
            _issue(issues, "orphan_criterion", f"$.criteria.{criterion_id}", "criterion is not owned by its outcome")
        if capability_id not in capability_pairs or capability_pairs.get(str(capability_id)) != g0_id:
            _issue(issues, "unknown_reference", f"$.criteria.{criterion_id}.capability_id", "criterion must bind one exact G0 child capability")
        elif capability_id in criterion_capabilities:
            _issue(issues, "duplicate_capability_mapping", f"$.criteria.{criterion_id}.capability_id", "a child capability may not be claimed by multiple criteria")
        else:
            criterion_capabilities[str(capability_id)] = criterion_id
    for capability_id in sorted(set(capability_pairs) - set(criterion_capabilities)):
        _issue(issues, "uncovered_capability", "$.criteria", f"G0 child capability has no G2 criterion: {capability_id}")

    used_outcomes: set[str] = set()
    used_criteria: set[str] = set()
    used_capabilities: set[str] = set()
    capability_unit_owner: dict[str, str] = {}
    workflow_owner: dict[str, str] = {}
    for unit_id, unit in units.items():
        base = f"$.units.{unit_id}"
        for field in ("title", "context", "output", "teaching_approach"):
            if not _concrete(unit.get(field)):
                _issue(issues, "non_executable_unit", f"{base}.{field}", f"unit {field} must be concrete")
        for field in ("outcome_ids", "criterion_ids", "capability_ids", "materials", "g1_evidence_refs"):
            refs = (
                _string_list(unit.get(field), f"{base}.{field}", issues, "non_executable_unit")
                if field == "materials"
                else _reference_list(unit.get(field), f"{base}.{field}", issues, "non_executable_unit")
            )
            if field == "outcome_ids":
                used_outcomes.update(refs)
                if any(ref not in outcomes for ref in refs):
                    _issue(issues, "unknown_reference", f"{base}.{field}", "unit references an unknown outcome")
            elif field == "criterion_ids":
                used_criteria.update(refs)
                if any(ref not in criteria for ref in refs):
                    _issue(issues, "unknown_reference", f"{base}.{field}", "unit references an unknown criterion")
            elif field == "capability_ids":
                used_capabilities.update(refs)
                if any(ref not in capability_pairs for ref in refs):
                    _issue(issues, "unknown_reference", f"{base}.{field}", "unit references an unknown capability")
                for capability_id in refs:
                    if capability_id in capability_unit_owner:
                        _issue(
                            issues,
                            "duplicate_unit_coverage",
                            f"{base}.{field}",
                            f"child capability is already owned by {capability_unit_owner[capability_id]}",
                        )
                    else:
                        capability_unit_owner[capability_id] = unit_id
            elif field == "g1_evidence_refs" and known_g1_evidence_ids is not None:
                if any(ref not in known_g1_evidence_ids for ref in refs):
                    _issue(issues, "unknown_g1_evidence", f"{base}.{field}", "unit references evidence outside the governed G1 PASS set")
        unit_outcomes = set(unit.get("outcome_ids", [])) if isinstance(unit.get("outcome_ids"), list) else set()
        unit_criteria = set(unit.get("criterion_ids", [])) if isinstance(unit.get("criterion_ids"), list) else set()
        unit_capabilities = set(unit.get("capability_ids", [])) if isinstance(unit.get("capability_ids"), list) else set()
        expected_pairs = {
            (str(criteria[criterion_id].get("outcome_id")), str(criteria[criterion_id].get("capability_id")))
            for criterion_id in unit_criteria
            if criterion_id in criteria
        }
        if (
            {outcome_id for outcome_id, _ in expected_pairs} != unit_outcomes
            or {capability_id for _, capability_id in expected_pairs} != unit_capabilities
        ):
            _issue(
                issues,
                "inconsistent_unit_coverage",
                base,
                "unit outcome, criterion, and child capability references must describe the same coverage rows",
            )
        dependencies = unit.get("prerequisite_unit_ids")
        if not isinstance(dependencies, list) or any(not _text(item) for item in dependencies):
            _issue(issues, "invalid_dependency", f"{base}.prerequisite_unit_ids", "dependencies must be a list of stable unit ids")
        elif any(item not in units for item in dependencies):
            _issue(issues, "unknown_reference", f"{base}.prerequisite_unit_ids", "unit references an unknown prerequisite")
        elif unit_id in dependencies:
            _issue(issues, "dependency_cycle", f"{base}.prerequisite_unit_ids", "unit cannot depend on itself")
        worked = _require_fields(unit.get("worked_example_plan"), ("input", "rationale", "result", "verification"), f"{base}.worked_example_plan", issues)
        if worked is not None:
            _string_list(worked.get("actions"), f"{base}.worked_example_plan.actions", issues, "non_executable_unit")
        _require_fields(unit.get("guided_practice"), ("activity", "feedback", "check", "recovery"), f"{base}.guided_practice", issues)
        independent = _require_fields(unit.get("independent_practice"), ("decision", "deliverable", "check", "recovery"), f"{base}.independent_practice", issues)
        if independent is not None:
            _string_list(independent.get("changed_conditions"), f"{base}.independent_practice.changed_conditions", issues, "non_executable_unit")
        evidence = unit.get("assessment_evidence")
        if not isinstance(evidence, list) or not evidence:
            _issue(issues, "assessment_evidence_required", f"{base}.assessment_evidence", "unit requires criterion-level assessment evidence")
        else:
            assessed_criteria: set[str] = set()
            for index, item in enumerate(evidence):
                criterion_id = item.get("criterion_id") if isinstance(item, Mapping) else None
                if (
                    not isinstance(item, Mapping)
                    or criterion_id not in unit.get("criterion_ids", [])
                    or not _concrete(item.get("evidence"))
                    or criterion_id in assessed_criteria
                ):
                    _issue(issues, "assessment_evidence_required", f"{base}.assessment_evidence[{index}]", "assessment evidence must bind a unit criterion")
                elif isinstance(criterion_id, str):
                    assessed_criteria.add(criterion_id)
            if assessed_criteria != unit_criteria:
                _issue(
                    issues,
                    "assessment_evidence_required",
                    f"{base}.assessment_evidence",
                    "every unit criterion requires exactly one assessment evidence record",
                )
        duration = unit.get("duration_minutes")
        if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
            _issue(issues, "invalid_duration", f"{base}.duration_minutes", "unit duration must be a positive integer")
        workflow = unit.get("workflow_fingerprint")
        if not isinstance(workflow, str) or ID_PATTERN.fullmatch(workflow) is None:
            _issue(issues, "invalid_workflow", f"{base}.workflow_fingerprint", "workflow fingerprint must be stable and descriptive")
        elif workflow in workflow_owner:
            _issue(issues, "duplicate_workflow", f"{base}.workflow_fingerprint", f"unit repeats the workflow of {workflow_owner[workflow]}")
        else:
            workflow_owner[workflow] = unit_id

    if _has_cycle(units):
        _issue(issues, "dependency_cycle", "$.units", "unit dependency graph contains a cycle")
    for unit_id in sorted(_disconnected_units(units)):
        _issue(issues, "orphan_unit", "$.units", f"unit is disconnected from the course dependency graph: {unit_id}")
    for missing in sorted(set(outcomes) - used_outcomes):
        _issue(issues, "orphan_outcome", "$.units", f"outcome is not taught by any unit: {missing}")
    for missing in sorted(set(criteria) - used_criteria):
        _issue(issues, "orphan_criterion", "$.units", f"criterion is not assessed by any unit: {missing}")
    for missing in sorted(set(capability_pairs) - used_capabilities):
        _issue(issues, "uncovered_capability", "$.units", f"child capability is not taught by any unit: {missing}")

    duration = record.get("duration")
    if not isinstance(duration, Mapping):
        _issue(issues, "duration_mismatch", "$.duration", "duration policy is required")
    else:
        available = duration.get("available_minutes")
        break_minutes = duration.get("break_minutes")
        buffer_minutes = duration.get("buffer_minutes")
        delivery = requirements.get("delivery")
        g0_available = delivery.get("available_minutes") if isinstance(delivery, Mapping) else None
        unit_minutes = sum(
            item.get("duration_minutes", 0) for item in units.values()
            if isinstance(item.get("duration_minutes"), int) and not isinstance(item.get("duration_minutes"), bool)
        )
        if (
            not isinstance(available, int) or not isinstance(break_minutes, int)
            or not isinstance(buffer_minutes, int)
            or isinstance(available, bool) or isinstance(break_minutes, bool) or isinstance(buffer_minutes, bool)
            or break_minutes < 0 or buffer_minutes < 0
            or available != g0_available or unit_minutes + break_minutes + buffer_minutes != available
        ):
            _issue(issues, "duration_mismatch", "$.duration", "unit, break, and buffer minutes must exactly fit G0 available time")
        policy = duration.get("policy")
        policy_text = policy.casefold() if isinstance(policy, str) else ""
        explains_break = "休息" in policy_text or "break" in policy_text
        explains_buffer = "緩衝" in policy_text or "buffer" in policy_text
        if not _concrete(policy) or not explains_break or not explains_buffer:
            _issue(issues, "duration_policy_required", "$.duration.policy", "break and buffer use must be explicit")

    _string_list(record.get("materials"), "$.materials", issues, "materials_required")
    risks = record.get("risks")
    if not isinstance(risks, list) or not risks:
        _issue(issues, "risks_required", "$.risks", "material risks and recovery ownership are required")
    else:
        seen_risks: set[str] = set()
        for index, risk in enumerate(risks):
            path = f"$.risks[{index}]"
            if not isinstance(risk, Mapping):
                _issue(issues, "risks_required", path, "risk must be an object")
                continue
            risk_id = risk.get("id")
            if not isinstance(risk_id, str) or ID_PATTERN.fullmatch(risk_id) is None or risk_id in seen_risks:
                _issue(issues, "invalid_id", f"{path}.id", "risk id must be unique and stable")
            else:
                seen_risks.add(risk_id)
            for field in ("description", "owner_gate", "mitigation"):
                if not _concrete(risk.get(field)):
                    _issue(issues, "risks_required", f"{path}.{field}", "risk must explain impact, owner, and mitigation")
    return issues


def validate_learning_coverage(requirements: Mapping[str, Any], blueprint: Mapping[str, Any], lessons: Sequence[Mapping[str, Any]], production: Mapping[str, Any]) -> list[ArchitectureIssue]:
    issues: list[ArchitectureIssue] = []
    capabilities = _capability_pairs(requirements)
    criteria = {
        str(item.get("capability_id")): item for item in blueprint.get("criteria", [])
        if isinstance(item, Mapping) and _text(item.get("capability_id"))
    }
    units = {
        capability_id: unit for unit in blueprint.get("units", []) if isinstance(unit, Mapping)
        for capability_id in unit.get("capability_ids", []) if isinstance(capability_id, str)
    }
    lesson_by_unit = {
        str(item.get("unit_id")): item for item in lessons
        if isinstance(item, Mapping) and _text(item.get("unit_id"))
    }
    rows = production.get("learning_coverage")
    production_rows: dict[str, Mapping[str, Any]] = {}
    final_artifact = production.get("final_artifact")
    artifact_evidence_ids = {
        str(item.get("criterion_id"))
        for item in final_artifact.get("acceptance", [])
        if isinstance(item, Mapping) and _text(item.get("criterion_id"))
    } if isinstance(final_artifact, Mapping) else set()
    trial = production.get("full_course_trial")
    trial_evidence_ids = {
        f"action-{item.get('sequence')}"
        for item in trial.get("actions", [])
        if isinstance(item, Mapping)
        and isinstance(item.get("sequence"), int)
    } if isinstance(trial, Mapping) else set()
    if not isinstance(rows, list):
        _issue(issues, "coverage_matrix_required", "$.production.learning_coverage", "G5 requires a criterion-level coverage matrix", "G5")
        rows = []
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping) or not _text(row.get("capability_id")):
            _issue(issues, "invalid_coverage_row", f"$.production.learning_coverage[{index}]", "coverage row requires a child capability id", "G5")
            continue
        capability_id = str(row["capability_id"])
        if capability_id in production_rows:
            _issue(issues, "duplicate_coverage", f"$.production.learning_coverage[{index}].capability_id", "child capability has duplicate G5 coverage", "G5")
        else:
            production_rows[capability_id] = row

    for capability_id, g0_criterion_id in capabilities.items():
        criterion = criteria.get(capability_id)
        unit = units.get(capability_id)
        if criterion is None or unit is None:
            _issue(issues, "uncovered_capability", "$.blueprint", f"child capability lacks G2 criterion or unit: {capability_id}")
            continue
        unit_id = str(unit.get("id"))
        criterion_id = str(criterion.get("id"))
        outcome_id = str(criterion.get("outcome_id"))
        lesson = lesson_by_unit.get(unit_id)
        lesson_rows = lesson.get("learning_coverage") if isinstance(lesson, Mapping) else None
        matching_lesson = [
            row for row in lesson_rows or [] if isinstance(row, Mapping)
            and row.get("capability_id") == capability_id
            and row.get("criterion_id") == criterion_id and row.get("outcome_id") == outcome_id
        ]
        lesson_atoms = {
            "teaching_evidence": {key for key in ("explanation", "full_demonstration") if isinstance(lesson, Mapping) and isinstance(lesson.get(key), Mapping)},
            "practice_evidence": {key for key in ("guided_practice", "independent_practice") if isinstance(lesson, Mapping) and isinstance(lesson.get(key), Mapping)},
            "assessment_evidence": ({"checks"} if isinstance(lesson, Mapping) and isinstance(lesson.get("checks"), list) and lesson.get("checks") else set()) | {
                str(item.get("id")) for item in lesson.get("checks", [])
                if isinstance(lesson, Mapping) and isinstance(item, Mapping) and _text(item.get("id"))
            },
        }
        lesson_evidence_valid = len(matching_lesson) == 1 and all(
            isinstance(matching_lesson[0].get(field), list)
            and bool(matching_lesson[0].get(field))
            and set(matching_lesson[0][field]).issubset(lesson_atoms[field])
            for field in ("teaching_evidence", "practice_evidence", "assessment_evidence")
        )
        if not lesson_evidence_valid:
            _issue(issues, "incomplete_lesson_coverage", f"$.lessons.{unit_id}", f"G3 must teach, practise, and assess {capability_id}", "G3")
        row = production_rows.get(capability_id)
        expected = {
            "g0_criterion_id": g0_criterion_id, "capability_id": capability_id,
            "outcome_id": outcome_id, "criterion_id": criterion_id, "unit_id": unit_id,
            "lesson_unit_id": unit_id, "artifact_criterion_id": g0_criterion_id,
        }
        if row is None:
            _issue(issues, "uncovered_capability", "$.production.learning_coverage", f"G5 lacks artifact and trial evidence for {capability_id}", "G5")
        elif (
            any(row.get(field) != value for field, value in expected.items())
            or row.get("artifact_evidence_id") not in artifact_evidence_ids
            or row.get("trial_evidence_id") not in trial_evidence_ids
        ):
            _issue(issues, "invalid_coverage_row", "$.production.learning_coverage", f"G5 coverage chain is incomplete for {capability_id}", "G5")
    for capability_id in sorted(set(production_rows) - set(capabilities)):
        _issue(issues, "unknown_reference", "$.production.learning_coverage", f"coverage references unknown capability: {capability_id}", "G5")
    return issues


def validate_downstream_learning_coverage(
    blueprint: Mapping[str, Any],
    lessons: Sequence[Mapping[str, Any]],
    production: Mapping[str, Any],
) -> list[ArchitectureIssue]:
    """Validate G2→G3→G5 after G2 has already bound each G0 child capability."""
    grouped: dict[str, list[dict[str, str]]] = {}
    for criterion in blueprint.get("criteria", []):
        if not isinstance(criterion, Mapping):
            continue
        g0_id = criterion.get("g0_criterion_id")
        capability_id = criterion.get("capability_id")
        if _text(g0_id) and _text(capability_id):
            grouped.setdefault(str(g0_id), []).append(
                {"id": str(capability_id), "statement": "bound by validated G2 criterion"}
            )
    requirements = {
        "acceptance_criteria": [
            {"id": criterion_id, "capabilities": capabilities}
            for criterion_id, capabilities in grouped.items()
        ]
    }
    return validate_learning_coverage(requirements, blueprint, lessons, production)


__all__ = [
    "ArchitectureIssue",
    "BLUEPRINT_OPTIONAL_FIELDS",
    "BLUEPRINT_REQUIRED_FIELDS",
    "validate_course_blueprint",
    "validate_downstream_learning_coverage",
    "validate_learning_coverage",
]
