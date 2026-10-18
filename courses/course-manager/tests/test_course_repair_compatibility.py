import json
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.course_repair import (
    RepairRoute,
    RepairTransactionError,
    apply_repair_transaction,
    classify_repair_finding,
    recover_repair_transaction,
)


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

    @staticmethod
    def digest(path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    def repair_fixture(self, root):
        root = Path(root)
        course = root / "existing-course"
        state = root / "state"
        course.mkdir()
        state.mkdir()
        target = course / "lesson.html"
        target.write_text("before\n", encoding="utf-8")
        plan = course / "_repair/2026-10-19/REPAIR-PLAN.md"
        plan.parent.mkdir(parents=True)
        plan.write_text("approved repair plan\n", encoding="utf-8")
        backup = course / "_backup/2026-10-19-pre-repair/lesson.html"
        backup.parent.mkdir(parents=True)
        backup.write_bytes(target.read_bytes())
        replacement = state / "staged-lesson.html"
        replacement.write_text("after\n", encoding="utf-8")
        isolated = root / "isolated-restore"
        isolated.mkdir()
        (isolated / "lesson.html").write_bytes(backup.read_bytes())
        manifest = course / "_backup/2026-10-19-pre-repair/manifest.json"
        manifest_value = {
            "schema_version": 1,
            "course_id": "existing-course",
            "targets": [
                {
                    "path": "lesson.html",
                    "before_sha256": self.digest(target),
                    "backup_path": "_backup/2026-10-19-pre-repair/lesson.html",
                    "backup_sha256": self.digest(backup),
                }
            ],
        }
        manifest.write_text(
            json.dumps(manifest_value, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        proof = state / "repair-proof.json"
        proof_value = {
            "schema_version": 1,
            "operation_id": "repair-existing-course-20261019",
            "approved_plan": {
                "path": "_repair/2026-10-19/REPAIR-PLAN.md",
                "sha256": self.digest(plan),
            },
            "backup_manifest": {
                "path": "_backup/2026-10-19-pre-repair/manifest.json",
                "sha256": self.digest(manifest),
            },
            "before_hashes": {"lesson.html": self.digest(target)},
            "isolated_restore_proof": {
                "verified": True,
                "restored_hashes": {"lesson.html": self.digest(target)},
                "isolation_root": str(isolated),
            },
            "mutations": [
                {
                    "path": "lesson.html",
                    "replacement_path": str(replacement),
                    "replacement_sha256": self.digest(replacement),
                }
            ],
        }
        proof.write_text(
            json.dumps(proof_value, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        return course, state, target, proof

    def test_repair_transaction_replays_every_proof_before_first_write(self):
        with tempfile.TemporaryDirectory() as temporary:
            course, state, target, proof = self.repair_fixture(temporary)
            proof_value = json.loads(proof.read_text(encoding="utf-8"))
            proof_value["before_hashes"]["lesson.html"] = "0" * 64
            proof.write_text(json.dumps(proof_value), encoding="utf-8")

            with self.assertRaises(RepairTransactionError):
                apply_repair_transaction(proof, course, state)

            self.assertEqual(target.read_text(encoding="utf-8"), "before\n")
            self.assertFalse((state / "repair-operations").exists())

    def test_repair_transaction_applies_with_durable_journal(self):
        with tempfile.TemporaryDirectory() as temporary:
            course, state, target, proof = self.repair_fixture(temporary)

            operation = apply_repair_transaction(proof, course, state)

            self.assertEqual(target.read_text(encoding="utf-8"), "after\n")
            self.assertEqual(operation["status"], "APPLIED")
            self.assertEqual(operation["journal"][0]["phase"], "APPLIED")
            persisted = json.loads(
                (state / "repair-operations/repair-existing-course-20261019.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(persisted, operation)

    def test_repair_transaction_recovers_after_each_mutation_boundary(self):
        checkpoints = ("TARGET_REPLACE_INTENT", "TARGET_REPLACED", "FINALIZE_INTENT")
        for checkpoint in checkpoints:
            with self.subTest(checkpoint=checkpoint), tempfile.TemporaryDirectory() as temporary:
                course, state, target, proof = self.repair_fixture(temporary)
                script = (
                    "from pathlib import Path; "
                    "from src.course_repair import apply_repair_transaction; "
                    f"apply_repair_transaction(Path({str(proof)!r}), Path({str(course)!r}), "
                    f"Path({str(state)!r}))"
                )
                env = os.environ.copy()
                env["COURSE_REPAIR_CRASH_AT"] = checkpoint
                completed = subprocess.run(
                    [sys.executable, "-c", script],
                    cwd=PROJECT_ROOT,
                    env=env,
                    check=False,
                )
                self.assertEqual(completed.returncode, 94)

                operation_path = state / "repair-operations/repair-existing-course-20261019.json"
                recovered = recover_repair_transaction(operation_path, course)
                self.assertEqual(recovered["status"], "ROLLED_BACK")
                self.assertEqual(target.read_text(encoding="utf-8"), "before\n")
                self.assertEqual(
                    recover_repair_transaction(operation_path, course)["status"],
                    "ROLLED_BACK",
                )

    def test_course_run_cli_dispatches_existing_course_repair_transaction(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            course, state, target, proof = self.repair_fixture(root)
            web_root = root / "managed-courses"
            web_root.mkdir()
            relocated = web_root / course.name
            course.rename(relocated)
            proof_value = json.loads(proof.read_text(encoding="utf-8"))
            for field in ("approved_plan", "backup_manifest"):
                proof_value[field]["sha256"] = self.digest(
                    relocated / proof_value[field]["path"]
                )
            proof.write_text(json.dumps(proof_value), encoding="utf-8")
            skills = root / "skills"
            skills.mkdir()
            environment = {
                **os.environ,
                "COURSE_DESIGN_SYSTEM_ROOT": str(PROJECT_ROOT),
                "COURSE_WEB_ROOT": str(web_root),
                "SKILLS_ROOT": str(skills),
                "COURSE_DESIGN_STATE_ROOT": str(state),
            }

            completed = subprocess.run(
                [
                    sys.executable,
                    str(PROJECT_ROOT / "scripts/course_run.py"),
                    "repair-fix",
                    "--course-root",
                    str(relocated),
                    "--proof",
                    str(proof),
                ],
                env=environment,
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(completed.stdout)["status"], "APPLIED")
            self.assertEqual((relocated / "lesson.html").read_text(), "after\n")


if __name__ == "__main__":
    unittest.main()
