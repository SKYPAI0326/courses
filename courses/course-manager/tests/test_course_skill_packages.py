import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = PROJECT_ROOT / "skill-packages" / "course-run"
ROUTING_PATH = PACKAGE_ROOT / "references" / "gate-routing.json"
RESEARCHER_ROOT = PROJECT_ROOT / "skill-packages" / "course-researcher"
RESEARCH_POLICY_PATH = RESEARCHER_ROOT / "references" / "research-policy.json"
PM_ROOT = PROJECT_ROOT / "skill-packages" / "course-pm"
ARCHITECTURE_POLICY_PATH = PM_ROOT / "references" / "architecture-policy.json"


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

    def test_support_files_are_resolvable_from_standalone_installed_package(self):
        for relative_path in self.routing["support_files"]:
            with self.subTest(relative_path=relative_path):
                self.assertNotIn("..", Path(relative_path).parts)
                self.assertTrue((PACKAGE_ROOT / relative_path).is_file())

    def test_project_runtime_dependencies_are_explicit_and_resolvable(self):
        runtime = self.routing["project_runtime"]

        self.assertEqual(runtime["working_directory"], "courses/course-manager")
        for relative_path in runtime["required_paths"]:
            with self.subTest(relative_path=relative_path):
                self.assertNotIn("..", Path(relative_path).parts)
                self.assertTrue((PROJECT_ROOT / relative_path).is_file())

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

    def test_gate_routing_separates_automatic_pass_from_external_approval(self):
        self.assertEqual(self.routing["gate_pass_authority"]["role"], "course-run")
        self.assertTrue(self.routing["gate_pass_authority"]["requires_validated_evidence"])
        self.assertFalse(
            self.routing["gate_pass_authority"]["requires_explicit_user_approval"]
        )
        self.assertTrue(
            self.routing["external_action_authority"]["requires_explicit_user_approval"]
        )
        self.assertTrue(
            all(not gate["user_approval_required"] for gate in self.routing["gates"])
        )

    def test_gate_routing_gives_children_evidence_but_not_pass_authority(self):
        child_authority = self.routing["child_authority"]

        self.assertTrue(child_authority["can_return_evidence"])
        self.assertFalse(child_authority["can_pass_gate"])
        self.assertEqual(
            {gate["evidence_authority"] for gate in self.routing["gates"]},
            {"producer"},
        )
        self.assertEqual(
            {gate["pass_authority"] for gate in self.routing["gates"]},
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
            lifecycle,
            {"NOT_STARTED", "IN_PROGRESS", "PASS", "FAIL", "BLOCKED", "STALE"},
        )
        self.assertEqual(
            maturity,
            {
                "STATIC_VALIDATED",
                "EXECUTION_VALIDATED",
                "INDEPENDENT_AI_VERIFIED",
                "HUMAN_VERIFIED",
            },
        )
        self.assertTrue(lifecycle.isdisjoint(maturity))
        self.assertEqual(self.routing["gate_status_path"], "gates.<gate_id>.status")
        self.assertEqual(
            self.routing["evidence_maturity_path"],
            "gates.<gate_id>.evidence[].maturity",
        )

    def load_research_policy(self):
        return json.loads(RESEARCH_POLICY_PATH.read_text(encoding="utf-8"))

    def load_architecture_policy(self):
        return json.loads(ARCHITECTURE_POLICY_PATH.read_text(encoding="utf-8"))

    def test_researcher_requires_external_current_sources(self):
        policy = self.load_research_policy()

        self.assertTrue(policy["external_sources"]["required"])
        self.assertTrue(policy["external_sources"]["authoritative_current_required"])
        self.assertTrue(policy["external_sources"]["technical_primary_sources_required"])
        self.assertEqual(
            set(policy["external_sources"]["required_fields"]),
            {"id", "title", "url", "source_type", "retrieved_at", "version", "context"},
        )

    def test_researcher_requires_hands_on_for_high_tool_dependency(self):
        policy = self.load_research_policy()

        self.assertEqual(policy["hands_on"]["trigger"], {"tool_dependency": "high"})
        self.assertTrue(policy["hands_on"]["required"])
        self.assertEqual(
            set(policy["hands_on"]["required_fields"]),
            {
                "id",
                "executed",
                "environment",
                "input",
                "result",
                "failure_notes",
                "limitations",
            },
        )
        self.assertEqual(policy["hands_on"]["missing_status"], "BLOCKED")

    def test_researcher_records_conflicts_unknowns_and_non_conclusions(self):
        policy = self.load_research_policy()

        self.assertEqual(
            set(policy["preserve_even_when_empty"]),
            {"conflicts", "unknowns", "non_conclusions"},
        )
        self.assertTrue(policy["failed_hands_on_is_evidence"])

    def test_researcher_does_not_use_source_count_as_pass_condition(self):
        policy = self.load_research_policy()

        self.assertIsNone(policy["completion"]["minimum_source_count"])
        self.assertEqual(
            policy["completion"]["criterion"],
            "course_decisions_supported_by_traceable_evidence",
        )

    def test_pm_does_not_repeat_g0_interview(self):
        policy = self.load_architecture_policy()

        self.assertFalse(policy["ownership"]["repeat_g0_interview"])
        self.assertFalse(policy["ownership"]["choose_theme"])

    def test_pm_requires_g0_and_g1_pass(self):
        policy = self.load_architecture_policy()

        self.assertEqual(
            policy["required_gate_status"], {"G0": "PASS", "G1": "PASS"}
        )
        self.assertEqual(
            policy["inputs"], ["G0_requirements", "G1_research", "adaptation"]
        )

    def test_pm_outputs_one_reasoned_main_blueprint(self):
        policy = self.load_architecture_policy()

        self.assertEqual(policy["main_blueprint_count"], 1)
        self.assertEqual(
            set(policy["required_outputs"]),
            {
                "outcomes",
                "assessment",
                "capability_progression",
                "units",
                "dependencies",
                "duration_fit",
                "material_risks",
                "evidence_citations",
            },
        )

    def test_pm_uses_adaptation_not_fixed_course_type_template(self):
        policy = self.load_architecture_policy()

        self.assertFalse(policy["fixed_course_type_template"])
        self.assertEqual(
            set(policy["adaptation_dimensions"]),
            {
                "learner_gap",
                "task_nature",
                "tool_dependency",
                "volatility",
                "failure_risk",
                "evidence_type",
            },
        )


if __name__ == "__main__":
    unittest.main()
