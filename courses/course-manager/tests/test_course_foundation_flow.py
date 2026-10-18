import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.course_contract import (
    ContractStateError,
    begin_gate,
    new_contract,
    record_change,
    render_gate_summary,
)
from tests.gate_test_support import _commit_gate_pass
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
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.workspace_root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def load_json(self, relative_path):
        return json.loads((FIXTURES / relative_path).read_text(encoding="utf-8"))

    def passed_g0(self):
        legacy = self.load_json("course-contracts/g0-approved.json")
        contract = new_contract(
            legacy["identity"]["slug"],
            legacy["identity"]["title"],
            legacy["governance"]["created_by"],
            legacy["governance"]["created_at"],
        )
        contract["G0_requirements"] = copy.deepcopy(legacy["G0_requirements"])
        begin_gate(
            contract,
            "G0",
            "course-run",
            "2026-10-18T13:50:00+08:00",
        )
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
            "2026-10-18T14:00:00+08:00",
        )
        return contract

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
            workspace_root=self.workspace_root,
        )

    def test_g0_must_pass_before_research_routing(self):
        contract = new_contract(
            "fictional-sheets",
            "虛構試算表實作課",
            "課程團隊",
            "2026-10-18T12:00:00+08:00",
        )

        with self.assertRaises(ContractStateError):
            self.route_valid_research(contract)

        self.assertEqual(contract["gates"]["G1"]["status"], "NOT_STARTED")

    def test_research_routes_valid_evidence_directly_to_g1_pass(self):
        contract = self.passed_g0()
        begin_gate(contract, "G1", "course-run", "2026-10-18T14:30:00+08:00")

        status = self.route_valid_research(contract)

        self.assertEqual(status, "PASS")
        self.assertEqual(contract["gates"]["G1"]["status"], "PASS")
        self.assertEqual(contract["G1_research"]["record_path"], "evidence/g1-research.json")
        self.assertEqual(
            contract["G1_research"]["sha256"],
            next(
                item["sha256"]
                for item in contract["evidence_index"]
                if item.get("id") == "g1-research"
            ),
        )
        self.assertEqual(contract["adaptation"], ADAPTATION)
        self.assertTrue(
            any(item.get("id") == "g1-research" for item in contract["evidence_index"])
        )

    def test_missing_hands_on_keeps_g1_blocked(self):
        contract = self.passed_g0()
        begin_gate(contract, "G1", "course-run", "2026-10-18T14:30:00+08:00")
        blocked = self.load_json("course-research/blocked-no-hands-on.json")

        status = route_research_to_gate(
            contract,
            blocked,
            ADAPTATION,
            "evidence/g1-blocked.json",
            "b" * 64,
            "course-researcher",
            "2026-10-18T15:00:00+08:00",
            workspace_root=self.workspace_root,
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

    def test_g1_pass_allows_g2_begin(self):
        contract = self.passed_g0()
        begin_gate(contract, "G1", "course-run", "2026-10-18T14:30:00+08:00")
        self.route_valid_research(contract)

        begin_gate(contract, "G2", "course-run", "2026-10-18T16:00:00+08:00")

        self.assertEqual(contract["gates"]["G2"]["status"], "IN_PROGRESS")

    def test_g0_semantic_change_stales_g1_and_g2(self):
        contract = self.passed_g0()
        begin_gate(contract, "G1", "course-run", "2026-10-18T14:30:00+08:00")
        self.route_valid_research(contract)
        begin_gate(contract, "G2", "course-run", "2026-10-18T16:00:00+08:00")
        contract["evidence_index"].append(
            {
                "id": "g2-blueprint",
                "gate": "G2",
                "kind": "course_blueprint",
                "path": "evidence/g2-blueprint.md",
                "sha256": hashlib.sha256(b"g2-blueprint").hexdigest(),
            }
        )
        _commit_gate_pass(
            contract,
            "G2",
            ["g2-blueprint"],
            "course-blueprint-validator",
            "course-run",
            "2026-10-18T16:10:00+08:00",
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
        self.assertEqual(contract["gates"]["G0"]["status"], "IN_PROGRESS")
        self.assertEqual(contract["gates"]["G1"]["status"], "STALE")
        self.assertEqual(contract["gates"]["G2"]["status"], "STALE")

    def test_human_summary_preserves_full_requirement_text(self):
        contract = self.passed_g0()
        prose = contract["G0_requirements"]["learner_context"]
        before = copy.deepcopy(contract)

        summary = render_gate_summary(contract)

        self.assertEqual(contract, before)
        self.assertEqual(contract["G0_requirements"]["learner_context"], prose)
        self.assertNotIn(prose, summary)
        self.assertIn("$.G1_research", summary)


if __name__ == "__main__":
    unittest.main()
