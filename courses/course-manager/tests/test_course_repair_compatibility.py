import json
import unittest
from pathlib import Path

from src.course_repair import RepairRoute, classify_repair_finding


PROJECT_ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = (
    PROJECT_ROOT
    / "skill-packages/course-repair/references/new-system-routing.json"
)


class CourseRepairCompatibilityTests(unittest.TestCase):
    def policy(self):
        return json.loads(POLICY_PATH.read_text(encoding="utf-8"))

    def test_repair_keeps_existing_course_entry_separate_from_new_course_flow(self):
        policy = self.policy()

        self.assertEqual(policy["entrypoint"], "existing_course_repair")
        self.assertFalse(policy["inherits_new_course_gate_history"])
        self.assertEqual(
            policy["workflow"], ["scan", "plan", "backup", "fix", "verify"]
        )

    def test_repair_requires_backup_before_first_mutation(self):
        policy = self.policy()

        self.assertTrue(policy["mutation_guard"]["backup_required"])
        self.assertTrue(policy["mutation_guard"]["restore_proof_required"])
        self.assertEqual(policy["mutation_guard"]["first_mutating_stage"], "fix")
        self.assertLess(
            policy["workflow"].index("backup"), policy["workflow"].index("fix")
        )

    def test_finding_routes_to_single_responsible_gate(self):
        policy = self.policy()
        expected = {
            "source_mismatch": "G1",
            "sequence_overload": "G2",
            "explanation_gap": "G3",
            "interface_block": "G4",
            "full_course_integration": "G5",
            "deployment_failure": "G6",
        }

        for code, gate_id in expected.items():
            with self.subTest(code=code):
                route = classify_repair_finding(code, policy)
                self.assertIsInstance(route, RepairRoute)
                self.assertEqual(route.owner_gate, gate_id)
                self.assertFalse(route.requires_new_course)
                self.assertEqual(len({route.owner_gate}), 1)

    def test_learner_outcome_or_whole_architecture_reframe_starts_new_contract(self):
        policy = self.policy()

        for code in (
            "learner_reframe",
            "outcome_reframe",
            "whole_course_architecture_reframe",
        ):
            with self.subTest(code=code):
                route = classify_repair_finding(code, policy)
                self.assertEqual(route.owner_gate, "G0")
                self.assertTrue(route.requires_new_course)
                self.assertEqual(route.revalidation_scope, tuple(f"G{i}" for i in range(7)))

    def test_repair_reuses_validator_without_claiming_new_course_gate_history(self):
        policy = self.policy()

        validator = policy["validator_reuse"]
        self.assertEqual(validator["skill"], "course-validator")
        self.assertTrue(validator["reuse_evidence_formats"])
        self.assertFalse(validator["create_new_course_gate_history"])
        route = classify_repair_finding("explanation_gap", policy)
        self.assertEqual(
            route.revalidation_scope,
            ("content", "fidelity", "independent_trial"),
        )


if __name__ == "__main__":
    unittest.main()
