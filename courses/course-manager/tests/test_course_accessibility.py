import copy
import hashlib
import json
import unittest

from src.course_accessibility import (
    BASIC_ACCESSIBILITY_CRITERIA,
    WCAG_22_AA_CRITERIA,
    validate_accessibility_binding,
    validate_accessibility_report,
)


class CourseAccessibilityTests(unittest.TestCase):
    def basic_report(self, *, gate_scope="G4", pages=None):
        pages = pages or [
            {"id": "unit-1", "path": "courses/demo/unit-1.html"}
        ]
        return {
            "schema_version": 1,
            "report_id": "accessibility-g4-unit-1",
            "gate_scope": gate_scope,
            "coverage_scope": (
                "representative_page" if gate_scope == "G4" else "full_course"
            ),
            "claim": {
                "scope": "basic_accessibility_smoke",
                "standard": "COURSE_ACCESSIBILITY_SMOKE",
                "version": "1.0",
                "level": "basic",
            },
            "pages": copy.deepcopy(pages),
            "applicable_criteria": [
                {"criterion_id": criterion_id, "level": "basic"}
                for criterion_id in BASIC_ACCESSIBILITY_CRITERIA
            ],
            "automated_checks": [
                {
                    "check_id": f"auto-overflow-{page['id']}",
                    "method": "automated",
                    "tool": "Playwright",
                    "tool_version": "1.56.1",
                    "user_agent": "Chromium 141",
                    "page_id": page["id"],
                    "criterion_id": "horizontal-overflow",
                    "status": "PASS",
                    "evidence": "scrollWidth did not exceed clientWidth at tested viewports",
                }
                for page in pages
            ],
            "manual_checks": [
                {
                    "check_id": f"manual-{criterion_id}-{page['id']}",
                    "method": "manual",
                    "evaluator_id": "accessibility-review-1",
                    "method_description": "keyboard traversal and DOM reading-order inspection",
                    "user_agent": "Safari 20",
                    "assistive_technology": ["VoiceOver 17"],
                    "page_id": page["id"],
                    "criterion_id": criterion_id,
                    "status": "PASS",
                    "evidence": f"Observed {criterion_id} on {page['id']}",
                }
                for page in pages
                for criterion_id in BASIC_ACCESSIBILITY_CRITERIA
                if criterion_id != "horizontal-overflow"
            ],
            "findings": [],
        }

    def wcag_report(self):
        report = self.basic_report(
            gate_scope="G5",
            pages=[
                {"id": "course-entry", "path": "courses/demo/index.html"},
                {"id": "unit-1", "path": "courses/demo/unit-1.html"},
                {"id": "course-completion", "path": "courses/demo/complete.html"},
            ],
        )
        report["report_id"] = "accessibility-g5-wcag"
        report["claim"] = {
            "scope": "wcag_2_2_aa",
            "standard": "WCAG",
            "version": "2.2",
            "level": "AA",
        }
        report["applicable_criteria"] = [
            {"criterion_id": criterion_id, "level": level}
            for criterion_id, level in WCAG_22_AA_CRITERIA.items()
        ]
        report["automated_checks"] = [
            {
                "check_id": f"auto-{criterion_id.replace('.', '-')}-{page['id']}",
                "method": "automated", "tool": "axe-core", "tool_version": "4.10.2",
                "user_agent": "Chromium 141", "page_id": page["id"],
                "criterion_id": criterion_id, "status": "PASS",
                "evidence": f"Automated assertion for {criterion_id} on {page['id']}",
            }
            for page in report["pages"]
            for criterion_id in WCAG_22_AA_CRITERIA
        ]
        report["manual_checks"] = [
            {
                "check_id": f"manual-{criterion_id.replace('.', '-')}-{page['id']}",
                "method": "manual", "evaluator_id": "accessibility-review-1",
                "method_description": "manual WCAG inspection", "user_agent": "Safari 20",
                "assistive_technology": ["VoiceOver 17"], "page_id": page["id"],
                "criterion_id": criterion_id, "status": "PASS",
                "evidence": f"Manual assertion for {criterion_id} on {page['id']}",
            }
            for page in report["pages"]
            for criterion_id in WCAG_22_AA_CRITERIA
        ]
        return report

    def test_basic_smoke_is_distinct_from_wcag_claim(self):
        report = self.basic_report()
        self.assertEqual(
            validate_accessibility_report(
                report,
                expected_gate="G4",
                expected_pages=report["pages"],
            ),
            [],
        )

        report["claim"] = {
            "scope": "wcag_2_2_aa",
            "standard": "WCAG",
            "version": "2.2",
            "level": "AA",
        }
        self.assertIn(
            "accessibility_criteria_incomplete",
            {
                issue.code
                for issue in validate_accessibility_report(
                    report, expected_gate="G4", expected_pages=report["pages"]
                )
            },
        )

    def test_g4_and_g5_require_exact_page_coverage(self):
        report = self.basic_report(gate_scope="G5")
        expected_pages = [
            {"id": "course-entry", "path": "courses/demo/index.html"},
            {"id": "unit-1", "path": "courses/demo/unit-1.html"},
            {"id": "unit-2", "path": "courses/demo/unit-2.html"},
            {"id": "course-completion", "path": "courses/demo/complete.html"},
        ]
        self.assertIn(
            "accessibility_page_coverage_mismatch",
            {
                issue.code
                for issue in validate_accessibility_report(
                    report, expected_gate="G5", expected_pages=expected_pages
                )
            },
        )

        g4 = self.basic_report()
        g4["coverage_scope"] = "full_course"
        self.assertIn(
            "accessibility_claim_scope_mismatch",
            {
                issue.code
                for issue in validate_accessibility_report(
                    g4, expected_gate="G4", expected_pages=g4["pages"]
                )
            },
        )

    def test_wcag_claim_requires_every_a_aa_criterion_and_both_check_methods(self):
        report = self.wcag_report()
        expected_pages = report["pages"]
        self.assertEqual(
            validate_accessibility_report(
                report, expected_gate="G5", expected_pages=expected_pages
            ),
            [],
        )

        missing = copy.deepcopy(report)
        missing["applicable_criteria"].pop()
        self.assertIn(
            "accessibility_criteria_incomplete",
            {
                issue.code
                for issue in validate_accessibility_report(
                    missing, expected_gate="G5", expected_pages=expected_pages
                )
            },
        )

        no_manual = copy.deepcopy(report)
        no_manual["manual_checks"] = []
        self.assertIn(
            "accessibility_manual_checks_incomplete",
            {
                issue.code
                for issue in validate_accessibility_report(
                    no_manual, expected_gate="G5", expected_pages=expected_pages
                )
            },
        )

        untested = copy.deepcopy(report)
        untested["manual_checks"][0]["status"] = "NOT_TESTED"
        self.assertIn(
            "accessibility_criterion_untested",
            {
                issue.code
                for issue in validate_accessibility_report(
                    untested, expected_gate="G5", expected_pages=expected_pages
                )
            },
        )

        not_automatable_only = copy.deepcopy(report)
        criterion_id = not_automatable_only["automated_checks"][0]["criterion_id"]
        page_id = not_automatable_only["automated_checks"][0]["page_id"]
        not_automatable_only["automated_checks"][0]["status"] = "NOT_AUTOMATABLE"
        not_automatable_only["manual_checks"] = [
            item
            for item in not_automatable_only["manual_checks"]
            if not (item["criterion_id"] == criterion_id and item["page_id"] == page_id)
        ]
        self.assertIn(
            "accessibility_criterion_untested",
            {
                issue.code
                for issue in validate_accessibility_report(
                    not_automatable_only,
                    expected_gate="G5",
                    expected_pages=expected_pages,
                )
            },
        )

    def test_wcag_requires_cartesian_page_criterion_coverage_and_unique_check_ids(self):
        report = self.wcag_report()
        page_id = report["pages"][1]["id"]
        criterion_id = next(iter(WCAG_22_AA_CRITERIA))
        report["automated_checks"] = [
            item for item in report["automated_checks"]
            if not (item["page_id"] == page_id and item["criterion_id"] == criterion_id)
        ]
        report["manual_checks"] = [
            item for item in report["manual_checks"]
            if not (item["page_id"] == page_id and item["criterion_id"] == criterion_id)
        ]
        self.assertIn(
            "accessibility_criterion_untested",
            {issue.code for issue in validate_accessibility_report(
                report, expected_gate="G5", expected_pages=report["pages"]
            )},
        )

        duplicate = self.wcag_report()
        duplicate["manual_checks"][0]["check_id"] = duplicate["automated_checks"][0]["check_id"]
        self.assertIn(
            "accessibility_duplicate_check_id",
            {issue.code for issue in validate_accessibility_report(
                duplicate, expected_gate="G5", expected_pages=duplicate["pages"]
            )},
        )

    def test_high_or_serious_unresolved_finding_blocks(self):
        report = self.wcag_report()
        report["findings"] = [
            {
                "finding_id": "finding-focus-loss",
                "page_ids": ["unit-1"],
                "criterion_ids": ["2.4.3"],
                "severity": "SERIOUS",
                "status": "OPEN",
                "summary": "Focus is lost after closing the dialog.",
                "resolution": "Pending remediation.",
            }
        ]
        self.assertIn(
            "accessibility_unresolved_blocker",
            {
                issue.code
                for issue in validate_accessibility_report(
                    report, expected_gate="G5", expected_pages=report["pages"]
                )
            },
        )

    def test_report_pass_label_is_rejected_and_cannot_hide_findings(self):
        report = self.wcag_report()
        report["status"] = "PASS"
        report["findings"] = [
            {
                "finding_id": "finding-obscured-focus",
                "page_ids": ["unit-1"],
                "criterion_ids": ["2.4.11"],
                "severity": "HIGH",
                "status": "OPEN",
                "summary": "The sticky header fully obscures keyboard focus.",
                "resolution": "Pending remediation.",
            }
        ]
        codes = {
            issue.code
            for issue in validate_accessibility_report(
                report, expected_gate="G5", expected_pages=report["pages"]
            )
        }
        self.assertIn("schema_additional_property", codes)
        self.assertIn("accessibility_unresolved_blocker", codes)

    def test_report_binding_matches_consumed_id_path_hash_and_claim(self):
        report = self.basic_report()
        payload = json.dumps(
            report, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
        digest = hashlib.sha256(payload).hexdigest()
        reference = {
            "id": report["report_id"],
            "gate": "G4",
            "kind": "accessibility_report",
            "path": "evidence/accessibility-g4.json",
            "sha256": digest,
        }
        declared = {
            "evidence_id": reference["id"],
            "path": reference["path"],
            "sha256": digest,
            "claim_scope": "basic_accessibility_smoke",
        }
        self.assertEqual(
            validate_accessibility_binding(declared, reference, report), []
        )
        for field, value in (
            ("evidence_id", "wrong-id"),
            ("path", "wrong/path.json"),
            ("sha256", "0" * 64),
            ("claim_scope", "wcag_2_2_aa"),
        ):
            with self.subTest(field=field):
                changed = dict(declared)
                changed[field] = value
                self.assertIn(
                    "accessibility_report_binding_mismatch",
                    {
                        issue.code
                        for issue in validate_accessibility_binding(
                            changed, reference, report
                        )
                    },
                )


if __name__ == "__main__":
    unittest.main()
