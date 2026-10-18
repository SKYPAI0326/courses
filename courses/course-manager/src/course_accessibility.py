from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from src.schema_runtime import validate_schema_file


BASIC_ACCESSIBILITY_CRITERIA = (
    "keyboard",
    "focus",
    "reading-order",
    "horizontal-overflow",
)

WCAG_22_AA_CRITERIA = {
    criterion_id: level
    for level, criterion_ids in (
        ("A", (
            "1.1.1", "1.2.1", "1.2.2", "1.2.3", "1.3.1", "1.3.2", "1.3.3",
            "1.4.1", "1.4.2", "2.1.1", "2.1.2", "2.1.4", "2.2.1", "2.2.2",
            "2.3.1", "2.4.1", "2.4.2", "2.4.3", "2.4.4", "2.5.1", "2.5.2",
            "2.5.3", "2.5.4", "3.1.1", "3.2.1", "3.2.2", "3.2.6", "3.3.1",
            "3.3.2", "3.3.7", "4.1.2",
        )),
        ("AA", (
            "1.2.4", "1.2.5", "1.3.4", "1.3.5", "1.4.3", "1.4.4", "1.4.5",
            "1.4.10", "1.4.11", "1.4.12", "1.4.13", "2.4.5", "2.4.6", "2.4.7",
            "2.4.11", "2.5.7", "2.5.8", "3.1.2", "3.2.3", "3.2.4", "3.3.3",
            "3.3.4", "3.3.8", "4.1.3",
        )),
    )
    for criterion_id in criterion_ids
}


@dataclass(frozen=True)
class AccessibilityIssue:
    code: str
    path: str
    message: str
    return_gate: str = "G4"


def _issue(
    issues: list[AccessibilityIssue], code: str, path: str, message: str, gate: str
) -> None:
    issues.append(AccessibilityIssue(code, path, message, gate))


def _pairs(values: Any, left: str, right: str) -> list[tuple[Any, Any]]:
    if not isinstance(values, list):
        return []
    return [
        (item.get(left), item.get(right))
        for item in values
        if isinstance(item, Mapping)
    ]


def validate_accessibility_binding(
    declared: Any,
    consumed_reference: Mapping[str, Any],
    report: Mapping[str, Any],
) -> list[AccessibilityIssue]:
    gate = str(consumed_reference.get("gate", "G4"))
    issues: list[AccessibilityIssue] = []
    if not isinstance(declared, Mapping):
        _issue(
            issues,
            "accessibility_report_binding_mismatch",
            "$.accessibility_report",
            "production record must declare the consumed accessibility report",
            gate,
        )
        return issues
    expected = {
        "evidence_id": consumed_reference.get("id"),
        "path": consumed_reference.get("path"),
        "sha256": consumed_reference.get("sha256"),
        "claim_scope": (
            report.get("claim", {}).get("scope")
            if isinstance(report.get("claim"), Mapping)
            else None
        ),
    }
    if dict(declared) != expected or report.get("report_id") != consumed_reference.get("id"):
        _issue(
            issues,
            "accessibility_report_binding_mismatch",
            "$.accessibility_report",
            "declared report id, path, hash, claim, and report identity must match consumed evidence",
            gate,
        )
    return issues


def validate_accessibility_report(
    report: Mapping[str, Any],
    *,
    expected_gate: str,
    expected_pages: Sequence[Mapping[str, str]],
) -> list[AccessibilityIssue]:
    issues = [
        AccessibilityIssue(issue.code, issue.path, issue.message, expected_gate)
        for issue in validate_schema_file(
            "course-accessibility-report.schema.json", report
        )
    ]
    if report.get("schema_version") != 1:
        _issue(issues, "unsupported_accessibility_schema", "$.schema_version", "accessibility report schema_version must be 1", expected_gate)
    if report.get("gate_scope") != expected_gate:
        _issue(issues, "accessibility_gate_scope_mismatch", "$.gate_scope", "report gate scope must match the consuming Gate", expected_gate)
    expected_scope = "representative_page" if expected_gate == "G4" else "full_course"
    if report.get("coverage_scope") != expected_scope:
        _issue(issues, "accessibility_claim_scope_mismatch", "$.coverage_scope", f"{expected_gate} accessibility coverage must be {expected_scope}", expected_gate)

    pages = _pairs(report.get("pages"), "id", "path")
    wanted_pages = _pairs(list(expected_pages), "id", "path")
    if len(pages) != len(set(pages)) or set(pages) != set(wanted_pages):
        _issue(issues, "accessibility_page_coverage_mismatch", "$.pages", "accessibility report must cover the exact learner page id/path set", expected_gate)
    page_ids = {item[0] for item in pages}

    claim = report.get("claim")
    scope = claim.get("scope") if isinstance(claim, Mapping) else None
    if scope == "basic_accessibility_smoke":
        if claim != {
            "scope": "basic_accessibility_smoke",
            "standard": "COURSE_ACCESSIBILITY_SMOKE",
            "version": "1.0",
            "level": "basic",
        }:
            _issue(issues, "accessibility_claim_invalid", "$.claim", "basic smoke must use the basic smoke standard and cannot claim WCAG conformance", expected_gate)
        required_criteria = {item: "basic" for item in BASIC_ACCESSIBILITY_CRITERIA}
    elif scope == "wcag_2_2_aa":
        if claim != {"scope": "wcag_2_2_aa", "standard": "WCAG", "version": "2.2", "level": "AA"}:
            _issue(issues, "accessibility_claim_invalid", "$.claim", "WCAG claim must be exactly WCAG 2.2 level AA", expected_gate)
        required_criteria = dict(WCAG_22_AA_CRITERIA)
    else:
        required_criteria = {}
        _issue(issues, "accessibility_claim_invalid", "$.claim.scope", "unknown accessibility claim scope", expected_gate)

    criteria = _pairs(report.get("applicable_criteria"), "criterion_id", "level")
    criterion_ids = [item[0] for item in criteria]
    if len(criterion_ids) != len(set(criterion_ids)) or dict(criteria) != required_criteria:
        _issue(issues, "accessibility_criteria_incomplete", "$.applicable_criteria", "claim must list every and only applicable criterion with its canonical level", expected_gate)

    method_pages: dict[str, set[str]] = {"automated_checks": set(), "manual_checks": set()}
    passing_pairs: set[tuple[str, str]] = set()
    check_ids: set[str] = set()
    for method in method_pages:
        checks = report.get(method)
        if isinstance(checks, list):
            for index, check in enumerate(checks):
                if not isinstance(check, Mapping):
                    continue
                check_id = check.get("check_id")
                if check_id in check_ids:
                    _issue(issues, "accessibility_duplicate_check_id", f"$.{method}[{index}].check_id", "check_id must be unique across the report", expected_gate)
                elif isinstance(check_id, str):
                    check_ids.add(check_id)
                page_id = check.get("page_id")
                criterion_id = check.get("criterion_id")
                status = check.get("status")
                if page_id not in page_ids:
                    _issue(issues, "accessibility_check_page_invalid", f"$.{method}[{index}].page_id", "check must bind one governed page", expected_gate)
                else:
                    method_pages[method].add(str(page_id))
                if criterion_id not in required_criteria:
                    _issue(issues, "accessibility_unknown_criterion", f"$.{method}[{index}].criterion_id", "check references a criterion outside the claim", expected_gate)
                elif status == "PASS" and page_id in page_ids:
                    passing_pairs.add((str(page_id), str(criterion_id)))
                if status in {"FAIL", "NOT_TESTED"}:
                    _issue(issues, "accessibility_criterion_untested" if status == "NOT_TESTED" else "accessibility_criterion_failed", f"$.{method}[{index}]", f"criterion {criterion_id} on page {page_id} has result {status}", expected_gate)
        if method_pages[method] != page_ids:
            code = "accessibility_automated_checks_incomplete" if method == "automated_checks" else "accessibility_manual_checks_incomplete"
            _issue(issues, code, f"$.{method}", f"{method} must include results for every claimed page", expected_gate)
    missing_pairs = {
        (str(page_id), str(criterion_id))
        for page_id in page_ids
        for criterion_id in required_criteria
    } - passing_pairs
    if missing_pairs:
        _issue(issues, "accessibility_criterion_untested", "$.applicable_criteria", "every governed page and applicable criterion requires a passing result", expected_gate)

    findings = report.get("findings")
    if isinstance(findings, list):
        for index, finding in enumerate(findings):
            if not isinstance(finding, Mapping):
                continue
            if not set(finding.get("page_ids", [])).issubset(page_ids):
                _issue(issues, "accessibility_finding_scope_invalid", f"$.findings[{index}].page_ids", "finding page ids must belong to the report", expected_gate)
            if not set(finding.get("criterion_ids", [])).issubset(required_criteria):
                _issue(issues, "accessibility_finding_scope_invalid", f"$.findings[{index}].criterion_ids", "finding criteria must belong to the claim", expected_gate)
            if finding.get("severity") in {"HIGH", "SERIOUS", "CRITICAL"} and finding.get("status") != "RESOLVED":
                _issue(issues, "accessibility_unresolved_blocker", f"$.findings[{index}]", "high, serious, or critical findings must be resolved", expected_gate)
    return issues
