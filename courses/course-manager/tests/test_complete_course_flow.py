import csv
import json
import runpy
import shutil
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
from src.course_gate import replay_passed_gate


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

    def test_proof_builder_rebuilds_deterministically_with_external_fixture_authority(self):
        from tests.proof_authority_fixture import rebuild_proof

        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first"
            rebuild_proof(first)

            first_files = {
                path.relative_to(first): path.read_bytes()
                for path in first.rglob("*")
                if path.is_file()
            }
            shutil.rmtree(first)
            rebuild_proof(first)
            rebuilt_files = {
                path.relative_to(first): path.read_bytes()
                for path in first.rglob("*")
                if path.is_file()
            }
            self.assertEqual(first_files, rebuilt_files)

    def test_rebuilt_proof_replays_all_gates_and_remains_unpublished(self):
        from tests.proof_authority_fixture import rebuild_proof

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "proof"
            rebuild_proof(root)
            contract = json.loads(
                (root / "_design/campaign-performance-brief/course-contract.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(validate_contract(contract), [])
            self.assertEqual(
                [contract["gates"][f"G{i}"]["status"] for i in range(7)],
                ["PASS"] * 7,
            )
            self.assertEqual(
                {
                    item.get("maturity")
                    for item in contract["evidence_index"]
                    if item.get("kind") == "independent_course_trial"
                },
                {"INDEPENDENT_AI_VERIFIED"},
            )
            self.assertEqual(
                contract["external_actions"][0]["status"],
                "PUBLISH_APPROVAL_REQUIRED",
            )
            self.assertIsNone(contract["external_actions"][0]["authorization"])
            validation = json.loads(
                (root / "evidence/proof-validation.json").read_text(encoding="utf-8")
            )
            self.assertEqual(validation["human_validation"], "PENDING_HUMAN")
            self.assertEqual(validation["external_publication"], "NOT_EXECUTED")
            for gate_id in (f"G{i}" for i in range(7)):
                with self.subTest(gate_id=gate_id):
                    self.assertEqual(replay_passed_gate(contract, gate_id, root), "PASS")

            for reference in contract["evidence_index"]:
                evidence_path = root / reference["path"]
                self.assertTrue(evidence_path.is_file(), reference["id"])
                self.assertEqual(
                    __import__("hashlib").sha256(evidence_path.read_bytes()).hexdigest(),
                    reference["sha256"],
                    reference["id"],
                )

    def test_rebuilt_proof_rejects_answer_reuse_and_incomplete_coverage(self):
        from tests.proof_authority_fixture import rebuild_proof

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "proof"
            rebuild_proof(root)
            requirements = json.loads((root / "evidence/g0-requirements.json").read_text())
            blueprint = json.loads((root / "evidence/blueprint.json").read_text())
            trial = json.loads((root / "trials/g5-full-course.json").read_text())
            held_out = next(
                item for item in trial["evidence_bindings"]
                if item["role"] == "held-out-output"
            )
            answer = next(
                item for item in trial["evidence_bindings"]
                if item["role"] == "answer-key-output"
            )
            answer["sha256"] = held_out["sha256"]
            issues = validate_trial_record(
                trial,
                {"schema_version": 1, "authors": ["course-author-ai"], "validators": ["course-validator"]},
                "full_course",
                requirements=requirements,
                requirements_sha256=__import__("hashlib").sha256(
                    (root / "evidence/g0-requirements.json").read_bytes()
                ).hexdigest(),
                blueprint=blueprint,
                runner_authority_id="test-proof-runner-authority",
            )
            self.assertIn("transfer_hash_reused", {issue.code for issue in issues})

            lessons = [
                json.loads((root / f"evidence/lesson-unit-{index}.json").read_text())
                for index in range(1, 4)
            ]
            production_bundle = json.loads(
                (root / "evidence/production-record.json").read_text()
            )
            production = production_bundle["record"]
            production["learning_coverage"].pop()
            coverage_issues = validate_learning_coverage(
                requirements, blueprint, lessons, production
            )
            self.assertIn(
                "uncovered_capability", {issue.code for issue in coverage_issues}
            )

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

    def test_checked_in_snapshot_matches_task8_rebuild(self):
        from tests.proof_authority_fixture import rebuild_proof

        with tempfile.TemporaryDirectory() as temporary:
            rebuilt = Path(temporary) / "rebuilt"
            rebuild_proof(rebuilt)
            for rebuilt_path in rebuilt.rglob("*"):
                if not rebuilt_path.is_file():
                    continue
                relative = rebuilt_path.relative_to(rebuilt)
                checked_in = PROOF_ROOT / relative
                self.assertTrue(checked_in.is_file(), relative.as_posix())
                self.assertEqual(
                    checked_in.read_bytes(), rebuilt_path.read_bytes(), relative.as_posix()
                )

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
        self.assertEqual(release_proposal["status"], "PUBLISH_APPROVAL_REQUIRED")
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
