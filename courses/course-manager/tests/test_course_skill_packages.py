import json
import subprocess
import sys
import unittest
from pathlib import Path

from scripts.install_course_skill_foundation import tree_hash


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = PROJECT_ROOT / "skill-packages" / "course-run"
ROUTING_PATH = PACKAGE_ROOT / "references" / "gate-routing.json"
RESEARCHER_ROOT = PROJECT_ROOT / "skill-packages" / "course-researcher"
RESEARCH_POLICY_PATH = RESEARCHER_ROOT / "references" / "research-policy.json"
PM_ROOT = PROJECT_ROOT / "skill-packages" / "course-pm"
ARCHITECTURE_POLICY_PATH = PM_ROOT / "references" / "architecture-policy.json"
MANIFEST_PATH = PROJECT_ROOT / "skill-packages" / "manifest.json"
EXPECTED_MANIFEST_PACKAGES = {
    "course-run",
    "course-researcher",
    "course-pm",
    "course-designer",
    "build-course-page",
    "course-validator",
    "course-ops",
    "course-refresh",
    "course-repair",
    "course-html-contract",
    "course-copywriter",
    "course-reviewer",
    "course-register",
    "course-handout-designer",
    "course-typography-fixer",
    "course-pdf",
}
QUICK_VALIDATE = Path(
    "/Users/paichenwei/.codex/skills/.system/skill-creator/scripts/quick_validate.py"
)


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

    def test_manifest_lists_each_core_compatibility_and_optional_package_once(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        packages = manifest["packages"]
        names = [item["name"] for item in packages]

        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), EXPECTED_MANIFEST_PACKAGES)
        self.assertEqual(
            {item["role"] for item in packages},
            {"core", "compatibility", "optional"},
        )
        self.assertTrue(all(item["entrypoint"] == "SKILL.md" for item in packages))

    def test_every_manifest_package_is_self_contained_and_skill_valid(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        for item in manifest["packages"]:
            package = PROJECT_ROOT / "skill-packages" / item["name"]
            with self.subTest(package=item["name"]):
                self.assertTrue((package / item["entrypoint"]).is_file())
                self.assertEqual(item["baseline_hash"], tree_hash(package))
                result = subprocess.run(
                    [sys.executable, str(QUICK_VALIDATE), str(package)],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

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

    def test_course_run_auto_dispatches_passed_gate_without_user_approval(self):
        policy = self.routing["automatic_dispatch"]

        self.assertTrue(policy["enabled"])
        self.assertEqual(policy["trigger"], "validated_gate_pass")
        self.assertEqual(policy["action"], "begin_next_gate")
        self.assertFalse(policy["requires_user_approval"])

    def test_course_run_asks_only_for_configured_decision_triggers(self):
        triggers = self.routing["user_decision_triggers"]

        self.assertEqual(
            set(triggers),
            {
                "design_changing_missing_information",
                "material_judgment",
                "paid_service",
                "credentials_or_rights",
                "external_mutation",
            },
        )
        self.assertTrue(all(item["ask_user"] for item in triggers.values()))
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
                "stable_criteria",
                "child_capability_coverage",
                "assessment",
                "capability_progression",
                "units",
                "dependencies",
                "acyclic_unit_graph",
                "duration_fit",
                "break_buffer_policy",
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

    def test_g3_authoring_roles_have_one_canonical_content_contract(self):
        designer = (PROJECT_ROOT / "skill-packages/course-designer/SKILL.md").read_text(
            encoding="utf-8"
        )
        copywriter = (
            PROJECT_ROOT / "skill-packages/course-copywriter/SKILL.md"
        ).read_text(encoding="utf-8")
        handout = (
            PROJECT_ROOT / "skill-packages/course-handout-designer/SKILL.md"
        ).read_text(encoding="utf-8")
        validator = (
            PROJECT_ROOT / "skill-packages/course-validator/SKILL.md"
        ).read_text(encoding="utf-8")
        contract = (
            PROJECT_ROOT
            / "skill-packages/course-designer/references/learner-content-contract.json"
        )

        self.assertTrue(contract.is_file())
        self.assertIn("G3 內容主責", designer)
        self.assertIn("診斷編輯", copywriter)
        self.assertIn("方法庫", handout)
        self.assertIn("不得替作者發明", validator)

    def test_g4_g5_skills_name_trial_transfer_accessibility_and_human_boundaries(self):
        run_routing = (
            PROJECT_ROOT
            / "skill-packages/course-run/references/course-contract-routing.md"
        ).read_text(encoding="utf-8")
        validator = (
            PROJECT_ROOT / "skill-packages/course-validator/SKILL.md"
        ).read_text(encoding="utf-8")
        builder = (
            PROJECT_ROOT / "skill-packages/build-course-page/SKILL.md"
        ).read_text(encoding="utf-8")

        for text in (run_routing, validator):
            self.assertIn("course-accessibility-report.schema.json", text)
            self.assertIn("basic_accessibility_smoke", text)
            self.assertIn("wcag_2_2_aa", text)
            self.assertIn("PENDING_HUMAN", text)
            self.assertIn("changed_conditions", text)
        self.assertIn("course-accessibility-report.schema.json", builder)
        self.assertIn("basic_accessibility_smoke", builder)

    def test_g4_chooses_course_specific_visuals_with_common_invariants(self):
        visual_path = (
            PROJECT_ROOT
            / "skill-packages/build-course-page/references/course-visual-decision.json"
        )
        visual = json.loads(visual_path.read_text(encoding="utf-8"))
        builder = (
            PROJECT_ROOT / "skill-packages/build-course-page/SKILL.md"
        ).read_text(encoding="utf-8")
        html_contract = (
            PROJECT_ROOT / "skill-packages/course-html-contract/SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertEqual(
            set(visual["inputs"]),
            {"topic", "learner", "task", "content_density", "primary_devices"},
        )
        self.assertIn("不是新課的版型規格", builder)
        self.assertIn("不必複製 `.lesson-body`", html_contract)
        self.assertIn("mobile_tablet_desktop_core_path", visual["common_invariants"])


if __name__ == "__main__":
    unittest.main()
