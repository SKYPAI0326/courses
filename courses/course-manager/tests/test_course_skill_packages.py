import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = PROJECT_ROOT / "skill-packages" / "course-run"
ROUTING_PATH = PACKAGE_ROOT / "references" / "gate-routing.json"


class CourseSkillPackageTests(unittest.TestCase):
    def setUp(self):
        self.routing = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))

    def test_all_skill_package_references_exist(self):
        required_package_files = (
            PACKAGE_ROOT / "SKILL.md",
            PACKAGE_ROOT / "agents" / "openai.yaml",
            PACKAGE_ROOT / "references" / "course-contract-routing.md",
            ROUTING_PATH,
        )
        referenced_files = tuple(
            (PACKAGE_ROOT / relative_path).resolve()
            for relative_path in self.routing["support_files"]
        )

        for path in required_package_files + referenced_files:
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"missing referenced file: {path}")

    def test_gate_routing_has_exact_g0_through_g6_order(self):
        self.assertEqual(
            [gate["id"] for gate in self.routing["gates"]],
            [f"G{index}" for index in range(7)],
        )
        for index, gate in enumerate(self.routing["gates"]):
            self.assertEqual(
                gate["prerequisite_gates"],
                [f"G{prior}" for prior in range(index)],
            )

    def test_gate_routing_requires_user_approval_for_every_gate(self):
        self.assertEqual(self.routing["approval_authority"]["role"], "course-run")
        self.assertTrue(
            self.routing["approval_authority"]["requires_explicit_user_approval"]
        )
        self.assertTrue(
            all(gate["user_approval_required"] for gate in self.routing["gates"])
        )

    def test_gate_routing_gives_children_submit_but_not_approve_authority(self):
        child_authority = self.routing["child_authority"]

        self.assertTrue(child_authority["can_submit"])
        self.assertFalse(child_authority["can_approve"])
        self.assertEqual(
            {gate["submission_authority"] for gate in self.routing["gates"]},
            {"producer"},
        )
        self.assertEqual(
            {gate["approval_authority"] for gate in self.routing["gates"]},
            {"course-run"},
        )

    def test_gate_routing_routes_missing_required_evidence_to_blocked(self):
        policy = self.routing["missing_required_evidence"]

        self.assertEqual(policy["gate_status"], "BLOCKED")
        self.assertTrue(policy["preserve_failure_evidence"])
        self.assertTrue(
            all(
                gate["missing_required_evidence_status"] == "BLOCKED"
                for gate in self.routing["gates"]
            )
        )

    def test_gate_routing_separates_lifecycle_from_evidence_maturity(self):
        lifecycle = set(self.routing["gate_lifecycle_states"])
        maturity = set(self.routing["evidence_maturity_states"])

        self.assertEqual(
            lifecycle, {"DRAFT", "REVIEW", "APPROVED", "BLOCKED", "STALE"}
        )
        self.assertEqual(
            maturity,
            {
                "MACHINE_CHECKED",
                "LEARNER_READ",
                "PLATFORM_VERIFIED",
                "HUMAN_READY",
            },
        )
        self.assertTrue(lifecycle.isdisjoint(maturity))
        self.assertEqual(self.routing["gate_status_path"], "gates.<gate_id>.status")
        self.assertEqual(
            self.routing["evidence_maturity_path"],
            "gates.<gate_id>.evidence[].maturity",
        )


if __name__ == "__main__":
    unittest.main()
