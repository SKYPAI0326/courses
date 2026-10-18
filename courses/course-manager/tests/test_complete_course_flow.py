import csv
import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.course_contract import validate_contract
from src.course_architecture import validate_course_blueprint, validate_learning_coverage
from src.course_content import validate_lesson_record
from src.course_requirements import validate_requirements_record
from src.course_validation import evidence_maturity, validate_trial_record
from src.course_accessibility import validate_accessibility_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROOF_ROOT = PROJECT_ROOT / "proofs/campaign-performance-brief"
PROOF_BUILDER = runpy.run_path(str(PROOF_ROOT / "build_proof.py"))


class CompleteCourseFlowTests(unittest.TestCase):
    def load_json(self, relative):
        return json.loads((PROOF_ROOT / relative).read_text(encoding="utf-8"))

    def test_proof_builder_emits_canonical_g0_and_g2_records(self):
        requirements = PROOF_BUILDER["requirements_record"]()
        blueprint = PROOF_BUILDER["blueprint_record"](requirements)

        self.assertEqual(validate_requirements_record(requirements), [])
        self.assertEqual(
            validate_course_blueprint(blueprint, requirements, known_g1_evidence_ids={"g1-research"}),
            [],
        )

    def test_proof_builder_fails_preflight_before_writing_without_authority(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "proof-output"
            completed = subprocess.run(
                [sys.executable, str(PROOF_ROOT / "build_proof.py"), "--output-root", str(output)],
                text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("PRECONDITION FAILED", completed.stderr + completed.stdout)
            self.assertFalse(output.exists())

    def test_proof_builder_preserves_child_capability_coverage_through_g5(self):
        requirements = PROOF_BUILDER["requirements_record"]()
        blueprint = PROOF_BUILDER["blueprint_record"](requirements)
        lessons = [
            PROOF_BUILDER["lesson_record"](unit_id, "a" * 64)
            for unit_id in ("unit-1", "unit-2", "unit-3")
        ]
        production = {
            "learning_coverage": PROOF_BUILDER["production_learning_coverage"](blueprint),
            "final_artifact": {
                "acceptance": [
                    {"criterion_id": item["id"]}
                    for item in requirements["acceptance_criteria"]
                ]
            },
            "full_course_trial": {"actions": [
                {"id": row["trial_evidence_id"], "sequence": index, "result": "PASS"}
                for index, row in enumerate(
                    PROOF_BUILDER["production_learning_coverage"](blueprint), start=1
                )
            ]},
        }

        for lesson in lessons:
            self.assertEqual(validate_lesson_record(lesson, blueprint), [])
        self.assertEqual(
            validate_learning_coverage(
                requirements, blueprint, lessons, production
            ),
            [],
        )

    def test_proof_builder_emits_canonical_trial_and_basic_accessibility_factories(self):
        requirements = PROOF_BUILDER["requirements_record"]()
        blueprint = PROOF_BUILDER["blueprint_record"](requirements)
        trial = PROOF_BUILDER["trial_record"](
            requirements,
            blueprint,
            scope="representative_unit",
            representative_unit_id="unit-3",
            runner_authority_id="test-independent-lab",
        )
        self.assertEqual(
            validate_trial_record(
                trial,
                ["course-author-ai"],
                "representative_unit",
                requirements=requirements,
                requirements_sha256=trial["requirements_sha256"],
                blueprint=blueprint,
                representative_unit_id="unit-3",
                runner_authority_id="test-independent-lab",
            ),
            [],
        )
        self.assertEqual(evidence_maturity(trial), "INDEPENDENT_AI_VERIFIED")

        pages = [{"id": "unit-3", "path": "course/unit-3.html"}]
        report = PROOF_BUILDER["accessibility_report"]("G4", pages)
        self.assertEqual(
            validate_accessibility_report(
                report, expected_gate="G4", expected_pages=pages
            ),
            [],
        )

    def test_legacy_snapshot_is_fail_closed_until_task8_rebuild(self):
        contract = self.load_json(
            "_design/campaign-performance-brief/course-contract.json"
        )
        self.assertIn(
            "invalid_pass_evidence_binding",
            {issue.code for issue in validate_contract(contract)},
        )
        self.assertEqual(
            [contract["gates"][f"G{i}"]["status"] for i in range(7)],
            ["PASS"] * 7,
        )
        indexed = {item["id"] for item in contract["evidence_index"]}
        for gate_id in (f"G{i}" for i in range(7)):
            pass_events = [
                event
                for event in contract["gates"][gate_id]["evidence"]
                if event.get("kind") == "gate_validation"
                and event.get("outcome") == "PASS"
            ]
            self.assertTrue(pass_events, gate_id)
            self.assertTrue(
                set(pass_events[-1]["evidence_ids"]).issubset(indexed), gate_id
            )

        pilot_trial = self.load_json("trials/g4-representative-unit.json")
        full_trial = self.load_json("trials/g5-full-course.json")
        self.assertIn(
            "schema_required",
            {
                issue.code
                for issue in validate_trial_record(
                    pilot_trial, ["course-author-ai"], "representative_unit"
                )
            },
        )
        self.assertIn(
            "schema_required",
            {
                issue.code
                for issue in validate_trial_record(
                    full_trial, ["course-author-ai"], "full_course"
                )
            },
        )
        self.assertNotEqual(
            pilot_trial["isolated_context_id"], full_trial["isolated_context_id"]
        )
        self.assertNotEqual(evidence_maturity(pilot_trial), "INDEPENDENT_AI_VERIFIED")
        self.assertNotEqual(evidence_maturity(full_trial), "INDEPENDENT_AI_VERIFIED")

        with (PROOF_ROOT / "course/assets/campaign-data.csv").open(
            encoding="utf-8"
        ) as handle:
            rows = list(csv.DictReader(handle))
        expected = {}
        for row in rows:
            impressions = int(row["impressions"])
            clicks = int(row["clicks"])
            cost = float(row["cost_twd"])
            conversions = int(row["conversions"])
            value = float(row["conversion_value_twd"])
            expected[row["campaign"]] = {
                "ctr": clicks / impressions * 100,
                "cvr": conversions / clicks * 100,
                "cpc": cost / clicks,
                "cpa": cost / conversions,
                "roas": value / cost,
            }
        artifact = (
            PROOF_ROOT / "trials/full-course-output/campaign-performance-brief.md"
        ).read_text(encoding="utf-8")
        self.assertIn("# 行銷活動成效摘要", artifact)
        self.assertIn("## 數據摘要", artifact)
        self.assertIn("## 判讀", artifact)
        self.assertIn("## 建議", artifact)
        self.assertIn("Prospecting Social", artifact)
        self.assertRegex(artifact, r"CPA[^\n]*NT\$1,000")
        self.assertRegex(artifact, r"ROAS[^\n]*2\.00")
        self.assertAlmostEqual(expected["Prospecting Social"]["cpa"], 1000.0)
        self.assertAlmostEqual(expected["Prospecting Social"]["roas"], 2.0)

        release_proposal = self.load_json("evidence/release-proposal.json")
        self.assertEqual(release_proposal["status"], "PENDING_AUTHORIZATION")
        self.assertIsNone(release_proposal["result"])
        release_actions = [
            action
            for action in contract["external_actions"]
            if action["kind"] == "course-release"
        ]
        self.assertEqual(len(release_actions), 1)
        self.assertEqual(
            release_actions[0]["status"], "PUBLISH_APPROVAL_REQUIRED"
        )
        self.assertIsNone(release_actions[0]["authorization"])
        self.assertEqual(
            release_actions[0]["manifest_sha256"],
            release_proposal["manifest_sha256"],
        )

    def test_learner_pages_meet_the_new_course_html_contract(self):
        required_head_markers = (
            '<meta name="description"',
            '<meta property="og:title"',
            '<meta property="og:description"',
            '<meta property="og:url"',
            '<meta property="og:image"',
            '<meta name="twitter:card"',
            '<meta name="twitter:title"',
            '<meta name="twitter:description"',
            '<meta name="twitter:image"',
            '<link rel="canonical"',
        )
        for filename in ("index.html", "unit-1.html", "unit-2.html", "unit-3.html"):
            page = (PROOF_ROOT / "course" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertIn(
                    '<a href="#main" class="skip-link">跳至主要內容</a>', page
                )
                self.assertIn('<main id="main"', page)
                self.assertIn('data-learner-content-root="true"', page)
                for marker in required_head_markers:
                    self.assertIn(marker, page)

        styles = (PROOF_ROOT / "course/styles.css").read_text(encoding="utf-8")
        self.assertIn(".skip-link", styles)
        self.assertIn(":focus-visible", styles)


if __name__ == "__main__":
    unittest.main()
