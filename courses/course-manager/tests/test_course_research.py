import copy
import hashlib
import tempfile
import unittest

from src.course_contract import _commit_gate_pass, begin_gate, new_contract
from src.course_research import (
    research_ready,
    route_research_to_gate,
    validate_research_record,
)


class CourseResearchValidationTests(unittest.TestCase):
    def valid_record(self):
        return {
            "schema_version": 1,
            "research_questions": [
                {
                    "id": "question-1",
                    "question": "目標工具能否完成代表性交付物？",
                    "decision_use": "決定是否安排完整實作與備援路徑",
                }
            ],
            "sources": [
                {
                    "id": "source-1",
                    "title": "官方產品說明",
                    "url": "https://example.com/official",
                    "source_type": "official",
                    "retrieved_at": "2026-10-18",
                    "version": "2026-10",
                    "context": "個人標準方案、繁體中文介面",
                }
            ],
            "claims": [
                {
                    "id": "claim-1",
                    "statement": "代表性任務可在標準方案完成。",
                    "source_ids": ["source-1"],
                    "confidence": "high",
                }
            ],
            "conflicts": [],
            "unknowns": [],
            "representative_task": {
                "description": "由真實商品資料產出一份活動企劃",
                "deliverable": "可供主管審核的活動企劃",
                "success_criteria": ["內容可追溯到來源資料", "包含受眾與渠道理由"],
            },
            "hands_on_record": None,
            "design_implications": [
                {
                    "id": "implication-1",
                    "decision": "G3 安排一次完整企劃實作。",
                    "rationale": "學員必須能完成真實交付物。",
                    "evidence_refs": ["claim-1"],
                }
            ],
            "maintenance": {"review_due": None, "owner": None},
        }

    def high_tool_hands_on(self, status="SUCCEEDED"):
        return {
            "id": "hands-on-1",
            "executed": True,
            "environment": {
                "tool": "Example AI",
                "plan": "standard",
                "version": "2026-10",
                "locale": "zh-TW",
            },
            "input": "一份去識別化商品資料",
            "result": {
                "status": status,
                "deliverable_path": "evidence/representative-output.md",
            },
            "failure_notes": [] if status == "SUCCEEDED" else ["匯出時服務回傳錯誤"],
            "limitations": ["免費方案每日額度有限"],
        }

    def test_claim_requires_source_date_context_and_design_implication(self):
        mutations = {
            "missing source": lambda record: record["claims"][0].update(source_ids=[]),
            "missing date": lambda record: record["sources"][0].update(retrieved_at=""),
            "missing context": lambda record: record["sources"][0].update(context=""),
            "missing implication": lambda record: record.update(design_implications=[]),
        }

        for label, mutate in mutations.items():
            with self.subTest(label=label):
                record = self.valid_record()
                mutate(record)
                self.assertTrue(validate_research_record(record, {}))

    def test_no_fixed_source_count_when_decisions_are_supported(self):
        record = self.valid_record()

        issues = validate_research_record(record, {})

        self.assertEqual(issues, [])
        self.assertTrue(research_ready(record, {}))
        self.assertEqual(len(record["sources"]), 1)

    def test_conflicting_sources_and_unknowns_are_preserved(self):
        record = self.valid_record()
        record["conflicts"] = [
            {
                "id": "conflict-1",
                "claim_ids": ["claim-1"],
                "description": "官方說明與目前介面標示的額度不同。",
                "handling": "課堂採實測值並標記複查日期。",
            }
        ]
        record["unknowns"] = [
            {
                "id": "unknown-1",
                "question": "企業帳號是否有不同額度？",
                "impact": "只影響延伸說明，不影響核心練習。",
                "blocking": False,
            }
        ]
        before = copy.deepcopy(record)

        issues = validate_research_record(record, {})

        self.assertEqual(issues, [])
        self.assertEqual(record, before)
        self.assertTrue(research_ready(record, {}))

    def test_high_tool_dependency_requires_hands_on_execution(self):
        adaptation = {"tool_dependency": "high"}
        for hands_on in (None, {"id": "hands-on-1", "executed": False}):
            with self.subTest(hands_on=hands_on):
                record = self.valid_record()
                record["hands_on_record"] = hands_on

                codes = {
                    issue.code for issue in validate_research_record(record, adaptation)
                }

                self.assertIn("hands_on_required", codes)
                self.assertFalse(research_ready(record, adaptation))

    def test_high_volatility_requires_review_due_and_owner(self):
        adaptation = {"volatility": "high"}
        cases = (
            ({"review_due": None, "owner": "課程維護者"}, "review_due_required"),
            ({"review_due": "2027-01-15", "owner": None}, "review_owner_required"),
            ({"review_due": "15/01/2027", "owner": "課程維護者"}, "invalid_review_due"),
        )
        for maintenance, expected_code in cases:
            with self.subTest(maintenance=maintenance):
                record = self.valid_record()
                record["maintenance"] = maintenance
                codes = {
                    issue.code for issue in validate_research_record(record, adaptation)
                }
                self.assertIn(expected_code, codes)

    def test_hands_on_failure_can_be_valid_evidence_but_blocks_readiness(self):
        record = self.valid_record()
        record["hands_on_record"] = self.high_tool_hands_on(status="FAILED")
        record["design_implications"][0]["evidence_refs"] = ["hands-on-1"]
        adaptation = {"tool_dependency": "high"}

        issues = validate_research_record(record, adaptation)
        codes = {issue.code for issue in issues}

        self.assertNotIn("hands_on_required", codes)
        self.assertNotIn("missing_hands_on_field", codes)
        self.assertIn("hands_on_failed", codes)
        self.assertFalse(research_ready(record, adaptation))

    def test_research_implication_must_reference_claim_or_hands_on_record(self):
        record = self.valid_record()
        record["design_implications"][0]["evidence_refs"] = ["source-1"]

        issues = validate_research_record(record, {})

        self.assertIn("unknown_implication_evidence", {issue.code for issue in issues})
        self.assertFalse(research_ready(record, {}))

    def test_representative_task_requires_description_deliverable_and_criteria(self):
        cases = (
            None,
            {"description": "", "deliverable": "成果", "success_criteria": ["可驗收"]},
            {"description": "任務", "deliverable": "", "success_criteria": ["可驗收"]},
            {"description": "任務", "deliverable": "成果", "success_criteria": []},
        )

        for representative_task in cases:
            with self.subTest(representative_task=representative_task):
                record = self.valid_record()
                record["representative_task"] = representative_task
                codes = {issue.code for issue in validate_research_record(record, {})}
                self.assertIn("invalid_representative_task", codes)
                self.assertFalse(research_ready(record, {}))

    def test_source_retrieved_at_must_be_iso_date(self):
        record = self.valid_record()
        record["sources"][0]["retrieved_at"] = "not-a-date"

        codes = {issue.code for issue in validate_research_record(record, {})}

        self.assertIn("invalid_source_date", codes)
        self.assertFalse(research_ready(record, {}))

    def test_stable_ids_must_be_unique(self):
        record = self.valid_record()
        duplicate = copy.deepcopy(record["claims"][0])
        duplicate["statement"] = "另一項主張。"
        record["claims"].append(duplicate)

        codes = {issue.code for issue in validate_research_record(record, {})}

        self.assertIn("duplicate_id", codes)
        self.assertFalse(research_ready(record, {}))

    def test_conflict_claim_references_must_exist(self):
        record = self.valid_record()
        record["conflicts"] = [
            {
                "id": "conflict-1",
                "claim_ids": ["missing-claim"],
                "description": "來源不一致。",
                "handling": "暫緩決策。",
            }
        ]

        codes = {issue.code for issue in validate_research_record(record, {})}

        self.assertIn("unknown_conflict_claim", codes)
        self.assertFalse(research_ready(record, {}))

    def test_research_routes_valid_evidence_directly_to_g1_pass(self):
        contract = new_contract(
            "practical-ai",
            "實用生成式 AI",
            "課程團隊",
            "2026-10-18T12:00:00+08:00",
        )
        begin_gate(contract, "G0", "course-run", "2026-10-18T12:10:00+08:00")
        contract["evidence_index"].append(
            {
                "id": "g0-requirements",
                "gate": "G0",
                "kind": "requirements_record",
                "path": "evidence/g0-requirements.json",
                "sha256": hashlib.sha256(b"g0-requirements").hexdigest(),
            }
        )
        _commit_gate_pass(
            contract,
            "G0",
            ["g0-requirements"],
            "requirements-validator",
            "course-run",
            "2026-10-18T12:15:00+08:00",
        )
        begin_gate(contract, "G1", "course-run", "2026-10-18T12:20:00+08:00")

        with tempfile.TemporaryDirectory() as temporary:
            status = route_research_to_gate(
                contract,
                self.valid_record(),
                {},
                "evidence/g1-research.json",
                "a" * 64,
                "course-researcher",
                "2026-10-18T12:30:00+08:00",
                workspace_root=temporary,
            )

        self.assertEqual(status, "PASS")
        self.assertEqual(contract["gates"]["G1"]["status"], "PASS")
        self.assertTrue(
            any(item.get("id") == "g1-research" for item in contract["evidence_index"])
        )


if __name__ == "__main__":
    unittest.main()
