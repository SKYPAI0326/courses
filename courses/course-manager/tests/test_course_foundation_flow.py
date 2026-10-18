import copy
import json
import unittest
from pathlib import Path

from src.course_contract import (
    ContractStateError,
    approve_gate,
    new_contract,
    record_change,
    render_gate_summary,
    submit_gate,
)
from src.course_research import route_research_to_gate


FIXTURES = Path(__file__).resolve().parent / "fixtures"
ADAPTATION = {
    "learner_gap": "high",
    "task_nature": "operation",
    "tool_dependency": "high",
    "volatility": "high",
    "failure_risk": "medium",
    "evidence_type": "artifact_and_operation",
}


class CourseFoundationFlowTests(unittest.TestCase):
    def load_json(self, relative_path):
        return json.loads((FIXTURES / relative_path).read_text(encoding="utf-8"))

    def approved_g0(self):
        return self.load_json("course-contracts/g0-approved.json")

    def valid_research(self):
        return self.load_json("course-research/valid-high-tool.json")

    def route_valid_research(self, contract):
        return route_research_to_gate(
            contract,
            self.valid_research(),
            ADAPTATION,
            "evidence/g1-research.json",
            "a" * 64,
            "course-researcher",
            "2026-10-18T15:00:00+08:00",
        )

    def test_g0_must_be_approved_before_research_submission(self):
        contract = new_contract(
            "fictional-sheets",
            "虛構試算表實作課",
            "課程團隊",
            "2026-10-18T12:00:00+08:00",
        )

        with self.assertRaises(ContractStateError):
            self.route_valid_research(contract)

        self.assertEqual(contract["gates"]["G1"]["status"], "DRAFT")

    def test_valid_high_tool_research_can_reach_g1_review(self):
        contract = self.approved_g0()

        status = self.route_valid_research(contract)

        self.assertEqual(status, "REVIEW")
        self.assertEqual(contract["gates"]["G1"]["status"], "REVIEW")
        self.assertEqual(contract["G1_research"]["record_path"], "evidence/g1-research.json")
        self.assertEqual(contract["G1_research"]["sha256"], "a" * 64)
        self.assertEqual(contract["adaptation"], ADAPTATION)
        self.assertTrue(
            any(
                item.get("kind") == "research_record"
                for item in contract["gates"]["G1"]["evidence"]
            )
        )

    def test_missing_hands_on_keeps_g1_blocked(self):
        contract = self.approved_g0()
        blocked = self.load_json("course-research/blocked-no-hands-on.json")

        status = route_research_to_gate(
            contract,
            blocked,
            ADAPTATION,
            "evidence/g1-blocked.json",
            "b" * 64,
            "course-researcher",
            "2026-10-18T15:00:00+08:00",
        )

        self.assertEqual(status, "BLOCKED")
        self.assertEqual(contract["gates"]["G1"]["status"], "BLOCKED")
        self.assertTrue(
            any(
                risk.get("blocking") is True
                and "hands_on_required" in risk.get("reason", "")
                for risk in contract["gates"]["G1"]["risks"]
            )
        )

    def test_g1_approval_allows_g2_submission(self):
        contract = self.approved_g0()
        self.route_valid_research(contract)
        approve_gate(
            contract,
            "G1",
            "使用者",
            "2026-10-18T15:10:00+08:00",
            "核准研究證據與適配決策",
        )

        submit_gate(
            contract,
            "G2",
            "course-pm",
            "2026-10-18T16:00:00+08:00",
        )

        self.assertEqual(contract["gates"]["G2"]["status"], "REVIEW")

    def test_g0_semantic_change_stales_g1_and_g2(self):
        contract = self.approved_g0()
        self.route_valid_research(contract)
        approve_gate(
            contract,
            "G1",
            "使用者",
            "2026-10-18T15:10:00+08:00",
            "核准研究",
        )
        submit_gate(contract, "G2", "course-pm", "2026-10-18T16:00:00+08:00")
        approve_gate(
            contract,
            "G2",
            "使用者",
            "2026-10-18T16:10:00+08:00",
            "核准藍圖",
        )

        invalidated = record_change(
            contract,
            "G0",
            "學員改為完全沒有試算表經驗",
            "course-run",
            "2026-10-19T09:00:00+08:00",
            semantic=True,
        )

        self.assertEqual(invalidated, ["G0", "G1", "G2", "G3", "G4", "G5", "G6"])
        self.assertEqual(contract["gates"]["G0"]["status"], "DRAFT")
        self.assertEqual(contract["gates"]["G1"]["status"], "STALE")
        self.assertEqual(contract["gates"]["G2"]["status"], "STALE")

    def test_human_summary_preserves_full_requirement_text(self):
        contract = self.approved_g0()
        prose = contract["G0_requirements"]["learner_context"]
        before = copy.deepcopy(contract)

        summary = render_gate_summary(contract)

        self.assertEqual(contract, before)
        self.assertEqual(contract["G0_requirements"]["learner_context"], prose)
        self.assertNotIn(prose, summary)
        self.assertIn("$.G1_research", summary)


if __name__ == "__main__":
    unittest.main()
