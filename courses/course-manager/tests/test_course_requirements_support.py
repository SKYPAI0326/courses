import copy
import unittest

from src.course_requirements_support import validate_requirements_support_record


class RequirementsSupportTests(unittest.TestCase):
    def valid_record(self):
        return {
            "schema_version": 1,
            "support_id": "g0-fallback-support",
            "requirements_id": "campaign-brief-requirements",
            "unknown_id": "unknown-export",
            "fallback_id": "fallback-markdown-export",
            "acceptance_criterion_ids": ["criterion-decision-brief"],
            "alternative_path": {
                "description": "改交付 Markdown，沿用同一組主管驗收規準。",
                "steps": ["開啟課程範本，填入指標與建議後另存 Markdown。"],
                "expected_result": "Markdown 包含與 PDF 相同的指標表、判讀與後續測試。",
            },
            "verification": {
                "executed": True,
                "verifier_id": "course-validator",
                "verified_at": "2026-10-18T09:01:30+08:00",
                "environment": "LibreOffice 24.2、繁體中文介面、macOS 測試帳號。",
                "method": "依替代步驟由空白範本完成一次 Markdown 匯出並逐項核對。",
                "observed_result": "匯出的 Markdown 可開啟，且全部驗收欄位都有可觀察結果。",
            },
            "preserved_acceptance_ids": ["criterion-decision-brief"],
            "artifacts": [
                {"evidence_id": "g0-fallback-artifact", "sha256": "a" * 64}
            ],
        }

    def test_closed_support_requires_replayed_artifact_chain(self):
        record = self.valid_record()
        self.assertEqual(
            validate_requirements_support_record(
                record, {"g0-fallback-artifact": "a" * 64}
            ),
            [],
        )
        for mutation in ("empty", "self-pass", "missing-artifact", "wrong-hash", "partial-acceptance"):
            with self.subTest(mutation=mutation):
                candidate = copy.deepcopy(record)
                known = {"g0-fallback-artifact": "a" * 64}
                if mutation == "empty":
                    candidate = {}
                elif mutation == "self-pass":
                    candidate["validation"] = {"status": "PASS"}
                    candidate["artifacts"] = []
                elif mutation == "missing-artifact":
                    known = {}
                elif mutation == "wrong-hash":
                    known["g0-fallback-artifact"] = "b" * 64
                else:
                    candidate["preserved_acceptance_ids"] = []
                self.assertTrue(validate_requirements_support_record(candidate, known))
