from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import Any, Mapping


_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_REQUIRED_SECTIONS = (
    "schema_version",
    "research_questions",
    "sources",
    "claims",
    "conflicts",
    "unknowns",
    "representative_task",
    "hands_on_record",
    "design_implications",
    "maintenance",
)


@dataclass(frozen=True)
class ResearchIssue:
    code: str
    path: str
    message: str


def _missing_text(value: Any) -> bool:
    return not isinstance(value, str) or not value.strip()


def _require_stable_id(
    item: Mapping[str, Any], path: str, issues: list[ResearchIssue]
) -> str | None:
    value = item.get("id")
    if not isinstance(value, str) or not _ID_PATTERN.fullmatch(value):
        issues.append(
            ResearchIssue("invalid_id", f"{path}.id", "a stable lowercase-hyphen id is required")
        )
        return None
    return value


def _require_text_fields(
    item: Mapping[str, Any],
    fields: tuple[str, ...],
    path: str,
    issues: list[ResearchIssue],
) -> None:
    for field in fields:
        if _missing_text(item.get(field)):
            issues.append(
                ResearchIssue(
                    "missing_required_field",
                    f"{path}.{field}",
                    f"{field} must contain text",
                )
            )


def validate_research_record(
    record: Mapping[str, Any], adaptation: Mapping[str, Any]
) -> list[ResearchIssue]:
    issues: list[ResearchIssue] = []
    for section in _REQUIRED_SECTIONS:
        if section not in record:
            issues.append(
                ResearchIssue(
                    "missing_section", f"$.{section}", f"missing research section: {section}"
                )
            )
    if record.get("schema_version") != 1:
        issues.append(
            ResearchIssue(
                "unsupported_schema_version",
                "$.schema_version",
                "schema_version must be 1",
            )
        )

    questions = record.get("research_questions")
    if not isinstance(questions, list) or not questions:
        issues.append(
            ResearchIssue(
                "research_questions_required",
                "$.research_questions",
                "at least one decision-linked research question is required",
            )
        )
    else:
        for index, question in enumerate(questions):
            path = f"$.research_questions[{index}]"
            if not isinstance(question, Mapping):
                issues.append(ResearchIssue("invalid_record", path, "question must be an object"))
                continue
            _require_stable_id(question, path, issues)
            _require_text_fields(question, ("question", "decision_use"), path, issues)

    sources = record.get("sources")
    source_ids: set[str] = set()
    if not isinstance(sources, list):
        issues.append(ResearchIssue("invalid_sources", "$.sources", "sources must be a list"))
        sources = []
    for index, source in enumerate(sources):
        path = f"$.sources[{index}]"
        if not isinstance(source, Mapping):
            issues.append(ResearchIssue("invalid_record", path, "source must be an object"))
            continue
        source_id = _require_stable_id(source, path, issues)
        if source_id:
            source_ids.add(source_id)
        for field, code in (
            ("title", "source_title_required"),
            ("url", "source_url_required"),
            ("source_type", "source_type_required"),
            ("retrieved_at", "source_date_required"),
            ("version", "source_version_required"),
            ("context", "source_context_required"),
        ):
            if _missing_text(source.get(field)):
                issues.append(
                    ResearchIssue(code, f"{path}.{field}", f"source {field} is required")
                )

    claims = record.get("claims")
    claim_ids: set[str] = set()
    if not isinstance(claims, list) or not claims:
        issues.append(
            ResearchIssue(
                "claims_required", "$.claims", "at least one evidence-backed claim is required"
            )
        )
        claims = []
    for index, claim in enumerate(claims):
        path = f"$.claims[{index}]"
        if not isinstance(claim, Mapping):
            issues.append(ResearchIssue("invalid_record", path, "claim must be an object"))
            continue
        claim_id = _require_stable_id(claim, path, issues)
        if claim_id:
            claim_ids.add(claim_id)
        _require_text_fields(claim, ("statement", "confidence"), path, issues)
        refs = claim.get("source_ids")
        if not isinstance(refs, list) or not refs:
            issues.append(
                ResearchIssue(
                    "claim_source_required",
                    f"{path}.source_ids",
                    "claim must reference at least one source",
                )
            )
            refs = []
        unknown_refs = [ref for ref in refs if ref not in source_ids]
        if unknown_refs:
            issues.append(
                ResearchIssue(
                    "unknown_claim_source",
                    f"{path}.source_ids",
                    f"unknown source ids: {', '.join(map(str, unknown_refs))}",
                )
            )

    hands_on = record.get("hands_on_record")
    hands_on_id: str | None = None
    tool_dependency_high = adaptation.get("tool_dependency") == "high"
    if isinstance(hands_on, Mapping):
        hands_on_id = _require_stable_id(hands_on, "$.hands_on_record", issues)
    if tool_dependency_high:
        if not isinstance(hands_on, Mapping) or hands_on.get("executed") is not True:
            issues.append(
                ResearchIssue(
                    "hands_on_required",
                    "$.hands_on_record",
                    "high tool dependency requires an executed representative task",
                )
            )
        else:
            for field in ("environment", "input", "result", "failure_notes", "limitations"):
                if field not in hands_on:
                    issues.append(
                        ResearchIssue(
                            "missing_hands_on_field",
                            f"$.hands_on_record.{field}",
                            f"hands-on evidence requires {field}",
                        )
                    )
            environment = hands_on.get("environment")
            if not isinstance(environment, Mapping) or not environment:
                issues.append(
                    ResearchIssue(
                        "missing_hands_on_field",
                        "$.hands_on_record.environment",
                        "hands-on environment must identify the tested context",
                    )
                )
            if _missing_text(hands_on.get("input")):
                issues.append(
                    ResearchIssue(
                        "missing_hands_on_field",
                        "$.hands_on_record.input",
                        "hands-on input must be recorded",
                    )
                )
            result = hands_on.get("result")
            if not isinstance(result, Mapping) or result.get("status") not in {
                "SUCCEEDED",
                "FAILED",
            }:
                issues.append(
                    ResearchIssue(
                        "missing_hands_on_field",
                        "$.hands_on_record.result.status",
                        "hands-on result status must be SUCCEEDED or FAILED",
                    )
                )
            elif result.get("status") == "FAILED":
                if not hands_on.get("failure_notes"):
                    issues.append(
                        ResearchIssue(
                            "failure_notes_required",
                            "$.hands_on_record.failure_notes",
                            "failed execution requires failure notes",
                        )
                    )
                issues.append(
                    ResearchIssue(
                        "hands_on_failed",
                        "$.hands_on_record.result.status",
                        "failed hands-on evidence is valid but blocks research readiness",
                    )
                )
            if not isinstance(hands_on.get("limitations"), list):
                issues.append(
                    ResearchIssue(
                        "missing_hands_on_field",
                        "$.hands_on_record.limitations",
                        "hands-on limitations must be recorded as a list",
                    )
                )

    implications = record.get("design_implications")
    implication_refs: set[str] = set()
    if not isinstance(implications, list) or not implications:
        issues.append(
            ResearchIssue(
                "design_implication_required",
                "$.design_implications",
                "research must produce at least one design implication",
            )
        )
        implications = []
    valid_evidence_ids = claim_ids | ({hands_on_id} if hands_on_id else set())
    for index, implication in enumerate(implications):
        path = f"$.design_implications[{index}]"
        if not isinstance(implication, Mapping):
            issues.append(
                ResearchIssue("invalid_record", path, "design implication must be an object")
            )
            continue
        _require_stable_id(implication, path, issues)
        _require_text_fields(implication, ("decision", "rationale"), path, issues)
        refs = implication.get("evidence_refs")
        if not isinstance(refs, list) or not refs:
            issues.append(
                ResearchIssue(
                    "implication_evidence_required",
                    f"{path}.evidence_refs",
                    "design implication must reference claim or hands-on evidence",
                )
            )
            continue
        implication_refs.update(refs)
        unknown_refs = [ref for ref in refs if ref not in valid_evidence_ids]
        if unknown_refs:
            issues.append(
                ResearchIssue(
                    "unknown_implication_evidence",
                    f"{path}.evidence_refs",
                    f"unknown claim or hands-on ids: {', '.join(map(str, unknown_refs))}",
                )
            )

    for claim_id in claim_ids:
        if claim_id not in implication_refs:
            issues.append(
                ResearchIssue(
                    "claim_without_design_implication",
                    "$.design_implications",
                    f"claim {claim_id} is not used by a design implication",
                )
            )
    if tool_dependency_high and hands_on_id and hands_on_id not in implication_refs:
        issues.append(
            ResearchIssue(
                "hands_on_without_design_implication",
                "$.design_implications",
                "hands-on evidence must change or confirm a course design decision",
            )
        )

    conflicts = record.get("conflicts")
    if not isinstance(conflicts, list):
        issues.append(
            ResearchIssue("invalid_conflicts", "$.conflicts", "conflicts must be a list")
        )
    else:
        for index, conflict in enumerate(conflicts):
            path = f"$.conflicts[{index}]"
            if not isinstance(conflict, Mapping):
                issues.append(ResearchIssue("invalid_record", path, "conflict must be an object"))
                continue
            _require_stable_id(conflict, path, issues)
            _require_text_fields(conflict, ("description", "handling"), path, issues)
            refs = conflict.get("claim_ids")
            if not isinstance(refs, list) or not refs:
                issues.append(
                    ResearchIssue(
                        "conflict_claims_required",
                        f"{path}.claim_ids",
                        "conflict must reference affected claims",
                    )
                )

    unknowns = record.get("unknowns")
    if not isinstance(unknowns, list):
        issues.append(ResearchIssue("invalid_unknowns", "$.unknowns", "unknowns must be a list"))
    else:
        for index, unknown in enumerate(unknowns):
            path = f"$.unknowns[{index}]"
            if not isinstance(unknown, Mapping):
                issues.append(ResearchIssue("invalid_record", path, "unknown must be an object"))
                continue
            _require_stable_id(unknown, path, issues)
            _require_text_fields(unknown, ("question", "impact"), path, issues)
            if unknown.get("blocking") is True:
                issues.append(
                    ResearchIssue(
                        "blocking_unknown",
                        path,
                        "blocking unknown must be resolved before research is ready",
                    )
                )

    if adaptation.get("volatility") == "high":
        maintenance = record.get("maintenance")
        if not isinstance(maintenance, Mapping):
            issues.append(
                ResearchIssue(
                    "maintenance_required",
                    "$.maintenance",
                    "high volatility requires maintenance ownership",
                )
            )
        else:
            review_due = maintenance.get("review_due")
            if _missing_text(review_due):
                issues.append(
                    ResearchIssue(
                        "review_due_required",
                        "$.maintenance.review_due",
                        "high volatility requires a review due date",
                    )
                )
            else:
                try:
                    date.fromisoformat(review_due)
                except (TypeError, ValueError):
                    issues.append(
                        ResearchIssue(
                            "invalid_review_due",
                            "$.maintenance.review_due",
                            "review due date must use ISO YYYY-MM-DD",
                        )
                    )
            if _missing_text(maintenance.get("owner")):
                issues.append(
                    ResearchIssue(
                        "review_owner_required",
                        "$.maintenance.owner",
                        "high volatility requires a review owner",
                    )
                )

    return issues


def research_ready(record: Mapping[str, Any], adaptation: Mapping[str, Any]) -> bool:
    return not validate_research_record(record, adaptation)
