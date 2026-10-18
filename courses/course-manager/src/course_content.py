from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, MutableMapping, Sequence

from src.course_contract import ContractStateError, block_gate
from src.course_evidence import materialize_json_evidence


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
PLACEHOLDER_PATTERN = re.compile(
    r"(?:\bTODO\b|\bTBD\b|lorem ipsum|\[需補資料|待補(?:充|寫|資料)?|此處放|placeholder)",
    re.IGNORECASE,
)
INTERNAL_FILENAME_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_-])(?:CH\d+(?:-\d+)*|PRAC\d+)\.md(?![A-Za-z0-9_-])",
    re.IGNORECASE,
)

REQUIRED_SECTIONS = (
    "schema_version",
    "unit_id",
    "learner_outcome",
    "context",
    "inputs",
    "deliverable",
    "explanation",
    "full_demonstration",
    "guided_practice",
    "independent_practice",
    "checks",
    "recovery",
    "transfer",
    "asset_references",
    "editorial_evidence",
)


@dataclass(frozen=True)
class ContentIssue:
    code: str
    path: str
    message: str
    return_gate: str = "G3"


def _has_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _issue(
    issues: list[ContentIssue], code: str, path: str, message: str
) -> None:
    issues.append(ContentIssue(code, path, message, "G3"))


def _require_mapping_texts(
    value: Any,
    fields: Sequence[str],
    path: str,
    code: str,
    issues: list[ContentIssue],
) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        _issue(issues, code, path, f"{path} must be an object")
        return None
    for field in fields:
        if not _has_text(value.get(field)):
            _issue(
                issues,
                code,
                f"{path}.{field}",
                f"{field} must explain the learner-visible content",
            )
    return value


def _require_text_list(
    value: Any,
    path: str,
    code: str,
    issues: list[ContentIssue],
) -> list[str]:
    if not isinstance(value, list) or not value or not all(_has_text(item) for item in value):
        _issue(issues, code, path, "a non-empty list of meaningful text is required")
        return []
    return value


def _validate_instruction(
    instruction: Any, path: str, issues: list[ContentIssue]
) -> None:
    _require_mapping_texts(
        instruction,
        ("purpose", "start_state", "action", "expected_result"),
        path,
        "incomplete_instruction",
        issues,
    )


def _walk_strings(value: Any, path: str = "$"):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, Mapping):
        for key, item in value.items():
            yield from _walk_strings(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk_strings(item, f"{path}[{index}]")


def validate_lesson_record(record: Mapping[str, Any]) -> list[ContentIssue]:
    issues: list[ContentIssue] = []
    for section in REQUIRED_SECTIONS:
        if section not in record:
            _issue(
                issues,
                "missing_section",
                f"$.{section}",
                f"lesson record is missing {section}",
            )
    if record.get("schema_version") != 1:
        _issue(
            issues,
            "unsupported_schema_version",
            "$.schema_version",
            "schema_version must be 1",
        )
    unit_id = record.get("unit_id")
    if not isinstance(unit_id, str) or not ID_PATTERN.fullmatch(unit_id):
        _issue(
            issues,
            "invalid_unit_id",
            "$.unit_id",
            "unit_id must use lowercase letters, digits, and hyphens",
        )

    _require_mapping_texts(
        record.get("learner_outcome"),
        ("statement", "evidence"),
        "$.learner_outcome",
        "incomplete_learner_outcome",
        issues,
    )
    _require_mapping_texts(
        record.get("context"),
        ("situation", "purpose", "prior_result"),
        "$.context",
        "incomplete_context",
        issues,
    )

    inputs = record.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        _issue(issues, "inputs_required", "$.inputs", "at least one usable input is required")
    else:
        seen_input_ids: set[str] = set()
        for index, item in enumerate(inputs):
            path = f"$.inputs[{index}]"
            mapped = _require_mapping_texts(
                item,
                ("id", "label", "source", "ready_check"),
                path,
                "incomplete_input",
                issues,
            )
            if mapped is not None:
                item_id = mapped.get("id")
                if not isinstance(item_id, str) or not ID_PATTERN.fullmatch(item_id):
                    _issue(issues, "invalid_input_id", f"{path}.id", "input id is invalid")
                elif item_id in seen_input_ids:
                    _issue(issues, "duplicate_input_id", f"{path}.id", "input id is duplicated")
                else:
                    seen_input_ids.add(item_id)

    deliverable = _require_mapping_texts(
        record.get("deliverable"),
        ("name", "format", "use"),
        "$.deliverable",
        "incomplete_deliverable",
        issues,
    )
    if deliverable is not None:
        _require_text_list(
            deliverable.get("acceptance_criteria"),
            "$.deliverable.acceptance_criteria",
            "deliverable_criteria_required",
            issues,
        )

    _require_mapping_texts(
        record.get("explanation"),
        ("prose",),
        "$.explanation",
        "explanation_required",
        issues,
    )

    demonstration = record.get("full_demonstration")
    if not isinstance(demonstration, Mapping):
        _issue(
            issues,
            "incomplete_demonstration",
            "$.full_demonstration",
            "full demonstration must be an object",
        )
    else:
        _require_mapping_texts(
            demonstration.get("input"),
            ("description", "value"),
            "$.full_demonstration.input",
            "incomplete_demonstration",
            issues,
        )
        if not _has_text(demonstration.get("rationale")):
            _issue(
                issues,
                "incomplete_demonstration",
                "$.full_demonstration.rationale",
                "demonstration must explain the decision rationale",
            )
        actions = demonstration.get("actions")
        if not isinstance(actions, list) or not actions:
            _issue(
                issues,
                "incomplete_demonstration",
                "$.full_demonstration.actions",
                "demonstration requires at least one complete action",
            )
        else:
            for index, action in enumerate(actions):
                before = len(issues)
                _validate_instruction(action, f"$.full_demonstration.actions[{index}]", issues)
                for issue_index in range(before, len(issues)):
                    issue = issues[issue_index]
                    issues[issue_index] = ContentIssue(
                        "incomplete_demonstration",
                        issue.path,
                        issue.message,
                        issue.return_gate,
                    )
        _require_mapping_texts(
            demonstration.get("result"),
            ("description", "artifact_ref"),
            "$.full_demonstration.result",
            "incomplete_demonstration",
            issues,
        )
        verification = demonstration.get("verification")
        if not isinstance(verification, list) or not verification:
            _issue(
                issues,
                "incomplete_demonstration",
                "$.full_demonstration.verification",
                "demonstration requires observable verification",
            )
        else:
            for index, item in enumerate(verification):
                _require_mapping_texts(
                    item,
                    ("criterion", "observable_result"),
                    f"$.full_demonstration.verification[{index}]",
                    "incomplete_demonstration",
                    issues,
                )

    guided = record.get("guided_practice")
    guided_record = _require_mapping_texts(
        guided,
        ("purpose", "start_state"),
        "$.guided_practice",
        "incomplete_guided_practice",
        issues,
    )
    if guided_record is not None:
        steps = guided_record.get("steps")
        if not isinstance(steps, list) or not steps:
            _issue(
                issues,
                "incomplete_guided_practice",
                "$.guided_practice.steps",
                "guided practice requires at least one instruction",
            )
        else:
            for index, step in enumerate(steps):
                _validate_instruction(step, f"$.guided_practice.steps[{index}]", issues)
        checks = guided_record.get("checks")
        if not isinstance(checks, list) or not checks:
            _issue(
                issues,
                "guided_check_required",
                "$.guided_practice.checks",
                "guided practice requires a visible check and recovery reference",
            )
        else:
            for index, item in enumerate(checks):
                _require_mapping_texts(
                    item,
                    ("expected_result", "recovery_ref"),
                    f"$.guided_practice.checks[{index}]",
                    "guided_check_required",
                    issues,
                )
        _require_text_list(
            guided_record.get("recovery_refs"),
            "$.guided_practice.recovery_refs",
            "recovery_required",
            issues,
        )

    independent = record.get("independent_practice")
    independent_record = _require_mapping_texts(
        independent,
        ("context", "decision_required", "verification"),
        "$.independent_practice",
        "incomplete_independent_practice",
        issues,
    )
    if independent_record is not None:
        _require_text_list(
            independent_record.get("changed_conditions"),
            "$.independent_practice.changed_conditions",
            "independent_transfer_required",
            issues,
        )
        if not _has_text(independent_record.get("deliverable")):
            _issue(
                issues,
                "independent_deliverable_required",
                "$.independent_practice.deliverable",
                "independent practice must produce a real learner deliverable",
            )
        _require_text_list(
            independent_record.get("acceptance_criteria"),
            "$.independent_practice.acceptance_criteria",
            "independent_acceptance_required",
            issues,
        )

    checks = record.get("checks")
    if not isinstance(checks, list) or not checks:
        _issue(issues, "checks_required", "$.checks", "learner-visible checks are required")
    else:
        for index, item in enumerate(checks):
            _require_mapping_texts(
                item,
                ("id", "target", "expected_result", "on_failure"),
                f"$.checks[{index}]",
                "incomplete_check",
                issues,
            )

    recovery = record.get("recovery")
    recovery_ids: set[str] = set()
    if not isinstance(recovery, list) or not recovery:
        _issue(
            issues,
            "recovery_required",
            "$.recovery",
            "at least one concrete recovery path is required",
        )
    else:
        for index, item in enumerate(recovery):
            path = f"$.recovery[{index}]"
            mapped = _require_mapping_texts(
                item,
                ("id", "symptom", "cause", "action", "expected_result"),
                path,
                "incomplete_recovery",
                issues,
            )
            if mapped is not None and isinstance(mapped.get("id"), str):
                recovery_ids.add(mapped["id"])
    if guided_record is not None and isinstance(guided_record.get("recovery_refs"), list):
        unknown = sorted(set(guided_record["recovery_refs"]) - recovery_ids)
        if unknown:
            _issue(
                issues,
                "unknown_recovery_reference",
                "$.guided_practice.recovery_refs",
                "unknown recovery ids: " + ", ".join(unknown),
            )

    _require_mapping_texts(
        record.get("transfer"),
        ("new_context", "method", "limits"),
        "$.transfer",
        "transfer_required",
        issues,
    )
    _require_text_list(
        record.get("asset_references"),
        "$.asset_references",
        "asset_reference_required",
        issues,
    )

    editorial = _require_mapping_texts(
        record.get("editorial_evidence"),
        ("reviewer_id", "source_sha256", "notes"),
        "$.editorial_evidence",
        "editorial_evidence_required",
        issues,
    )
    if editorial is not None:
        if not SHA256_PATTERN.fullmatch(str(editorial.get("source_sha256", ""))):
            _issue(
                issues,
                "editorial_evidence_required",
                "$.editorial_evidence.source_sha256",
                "editorial evidence must identify the reviewed source hash",
            )
        for field in (
            "continuity_passed",
            "learner_readable",
            "internal_labels_removed",
        ):
            if editorial.get(field) is not True:
                _issue(
                    issues,
                    "editorial_evidence_failed",
                    f"$.editorial_evidence.{field}",
                    f"editorial review did not pass {field}",
                )

    for path, text in _walk_strings(record):
        if PLACEHOLDER_PATTERN.search(text):
            _issue(
                issues,
                "placeholder_prose",
                path,
                "learner content contains a placeholder instead of finished teaching prose",
            )
        if INTERNAL_FILENAME_PATTERN.search(text):
            _issue(
                issues,
                "internal_filename",
                path,
                "learner content exposes an internal coded filename",
            )
    return issues


def route_content_to_g3(
    contract: MutableMapping[str, Any],
    record: Mapping[str, Any],
    record_path: str,
    sha256: str,
    actor: str,
    at: str,
    *,
    workspace_root: Path | str,
) -> str:
    gates = contract.get("gates")
    if not isinstance(gates, Mapping) or any(
        gates.get(gate_id, {}).get("status") != "PASS" for gate_id in ("G0", "G1", "G2")
    ):
        raise ContractStateError("G3 content requires G0, G1, and G2 PASS")
    if gates.get("G3", {}).get("status") != "IN_PROGRESS":
        raise ContractStateError("content routing requires G3 IN_PROGRESS")
    relative_path = PurePosixPath(record_path)
    if not record_path.strip() or relative_path.is_absolute() or ".." in relative_path.parts:
        raise ContractStateError("lesson record path must be a safe relative path")
    if not SHA256_PATTERN.fullmatch(sha256):
        raise ContractStateError("lesson record SHA-256 must be 64 lowercase hex characters")

    issues = validate_lesson_record(record)
    unit_id = record.get("unit_id") if isinstance(record.get("unit_id"), str) else "invalid-unit"
    evidence_id = f"g3-{unit_id}"
    contract["G3_lesson_design"] = {
        "record_path": record_path,
        "sha256": sha256,
        "unit_id": unit_id,
        "validation_issue_codes": [issue.code for issue in issues],
    }
    gates["G3"]["evidence"].append(
        {
            "kind": "lesson_record",
            "path": record_path,
            "sha256": sha256,
            "maturity": "STATIC_VALIDATED",
            "validation_issue_codes": [issue.code for issue in issues],
        }
    )
    if issues:
        block_gate(
            contract,
            "G3",
            "lesson validation failed: "
            + ", ".join(sorted({issue.code for issue in issues})),
            actor,
            at,
        )
        return "BLOCKED"

    if any(
        isinstance(item, Mapping) and item.get("id") == evidence_id
        for item in contract["evidence_index"]
    ):
        raise ContractStateError(f"lesson evidence id already exists: {evidence_id}")
    reference = materialize_json_evidence(
        workspace_root,
        evidence_id=evidence_id,
        gate_id="G3",
        kind="lesson_record",
        relative_path=record_path,
        value=record,
    )
    contract["G3_lesson_design"]["sha256"] = reference["sha256"]
    gates["G3"]["evidence"][-1]["sha256"] = reference["sha256"]
    contract["evidence_index"].append(reference)
    from src.course_gate import validate_and_transition_gate

    return validate_and_transition_gate(
        contract,
        "G3",
        [evidence_id],
        workspace_root,
        actor,
        at,
    )
