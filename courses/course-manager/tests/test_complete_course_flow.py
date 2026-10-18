import csv
import json
import runpy
import unittest
from pathlib import Path

from src.course_contract import validate_contract
from src.course_architecture import validate_course_blueprint, validate_learning_coverage
from src.course_content import validate_lesson_record
from src.course_requirements import validate_requirements_record
from src.course_validation import evidence_maturity, validate_trial_record


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
        self.assertEqual(validate_course_blueprint(blueprint, requirements), [])

    def test_proof_builder_preserves_child_capability_coverage_through_g5(self):
        requirements = PROOF_BUILDER["requirements_record"]()
        blueprint = PROOF_BUILDER["blueprint_record"](requirements)
        lessons = [
            PROOF_BUILDER["lesson_record"](unit_id, "a" * 64)
            for unit_id in ("unit-1", "unit-2", "unit-3")
        ]
        production = {
            "learning_coverage": PROOF_BUILDER["production_learning_coverage"](
                blueprint
            )
        }

        for lesson in lessons:
            self.assertEqual(validate_lesson_record(lesson, blueprint), [])
        self.assertEqual(
            validate_learning_coverage(
                requirements, blueprint, lessons, production
            ),
            [],
        )

    def test_new_course_reaches_g6_ready_without_external_publish(self):
        contract = self.load_json(
            "_design/campaign-performance-brief/course-contract.json"
        )
        self.assertEqual(validate_contract(contract), [])
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
        self.assertEqual(
            validate_trial_record(pilot_trial, ["course-author-ai"], "representative_unit"),
            [],
        )
        self.assertEqual(
            validate_trial_record(full_trial, ["course-author-ai"], "full_course"),
            [],
        )
        self.assertNotEqual(
            pilot_trial["isolated_context_id"], full_trial["isolated_context_id"]
        )
        self.assertEqual(evidence_maturity(pilot_trial), "INDEPENDENT_AI_VERIFIED")
        self.assertEqual(evidence_maturity(full_trial), "INDEPENDENT_AI_VERIFIED")

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
