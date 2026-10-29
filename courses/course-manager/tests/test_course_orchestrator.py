import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

try:
    from src import course_orchestrator
except ImportError:
    course_orchestrator = None

from src.course_contract import (
    begin_gate,
    block_gate,
    load_contract,
    new_contract,
    resolve_gate_blocker,
    save_contract_atomic,
)
from src.course_evidence import materialize_json_evidence
from tests.test_course_requirements import CourseRequirementsTests


class CourseOrchestratorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.workspace = self.root / "course-workspace"
        self.state = self.root / "state"
        self.workspace.mkdir()
        self.state.mkdir()
        self.contract_path = self.workspace / "_design" / "demo" / "course-contract.json"
        self.contract_path.parent.mkdir(parents=True)

    def tearDown(self):
        self.temporary.cleanup()

    def require_orchestrator(self):
        self.assertIsNotNone(
            course_orchestrator,
            "src.course_orchestrator must execute resumable Gate dispatch",
        )
        return course_orchestrator

    def save_new_contract(self):
        contract = new_contract(
            "demo", "Portable Demo", "course-run", "2026-10-18T09:00:00+08:00"
        )
        save_contract_atomic(self.contract_path, contract)
        return contract

    def save_in_progress_g0(self, *, valid=True):
        contract = self.save_new_contract()
        begin_gate(contract, "G0", "course-run", "2026-10-18T09:01:00+08:00")
        record = CourseRequirementsTests().valid_record()
        if not valid:
            record["final_artifact"]["observable_result"] = "了解概念"
        contract["G0_requirements"] = copy.deepcopy(record)
        reference = materialize_json_evidence(
            self.workspace,
            evidence_id="g0-demo-requirements",
            gate_id="G0",
            kind="requirements_record",
            relative_path="evidence/g0-requirements.json",
            value=record,
        )
        contract["evidence_index"].append(reference)
        save_contract_atomic(self.contract_path, contract)
        return reference

    def test_resume_starts_first_gate_once_and_reuses_dispatch_envelope(self):
        module = self.require_orchestrator()
        self.save_new_contract()

        first = module.resume_course(
            self.contract_path,
            self.workspace,
            self.state,
            actor="course-run",
            at="2026-10-18T09:01:00+08:00",
        )
        revision = load_contract(self.contract_path)["revision"]
        second = module.resume_course(
            self.contract_path,
            self.workspace,
            self.state,
            actor="course-run",
            at="2026-10-18T09:01:00+08:00",
        )

        self.assertEqual(first, second)
        self.assertEqual(first["action"], "DISPATCH_GATE")
        self.assertEqual(first["gate_id"], "G0")
        self.assertEqual(first["producer"], "course-run")
        self.assertEqual(load_contract(self.contract_path)["revision"], revision)
        self.assertTrue((self.state / "dispatch" / f"{first['id']}.json").is_file())

    def test_resume_wraps_transaction_revision_conflict(self):
        module = self.require_orchestrator()
        self.save_new_contract()

        with self.assertRaisesRegex(module.OrchestrationError, "revision conflict"):
            module.resume_course(
                self.contract_path,
                self.workspace,
                self.state,
                actor="course-run",
                at="2026-10-18T09:01:00+08:00",
                expected_revision=9,
            )

    def test_in_progress_resume_rejects_an_unlocked_stale_snapshot(self):
        module = self.require_orchestrator()
        contract = self.save_new_contract()
        begin_gate(contract, "G0", "course-run", "2026-10-18T09:01:00+08:00")
        save_contract_atomic(self.contract_path, contract)
        stale = load_contract(self.contract_path)

        from src.transactions import mutate_contract_atomic

        mutate_contract_atomic(
            self.contract_path,
            lambda value: block_gate(
                value,
                "G0",
                "concurrent evidence loss",
                "review-race",
                "2026-10-18T09:02:00+08:00",
            ),
            expected_revision=0,
        )

        with mock.patch.object(module, "load_contract", return_value=stale):
            with self.assertRaisesRegex(module.OrchestrationError, "revision conflict"):
                module.resume_course(
                    self.contract_path,
                    self.workspace,
                    self.state,
                    actor="course-run",
                    at="2026-10-18T09:03:00+08:00",
                    expected_revision=0,
                )

        self.assertFalse((self.state / "dispatch").exists())

    def test_complete_calls_central_validator_and_begins_next_gate_atomically(self):
        module = self.require_orchestrator()
        reference = self.save_in_progress_g0()

        envelope = module.complete_gate(
            self.contract_path,
            self.workspace,
            self.state,
            "G0",
            [reference["id"]],
            actor="course-run",
            at="2026-10-18T09:02:00+08:00",
        )
        contract = load_contract(self.contract_path)

        self.assertEqual(contract["gates"]["G0"]["status"], "PASS")
        self.assertEqual(
            contract["gates"]["G0"]["evidence"][-1]["validator_id"],
            "course-requirements-validator",
        )
        self.assertEqual(contract["gates"]["G1"]["status"], "IN_PROGRESS")
        self.assertEqual(envelope["gate_id"], "G1")
        self.assertEqual(envelope["action"], "DISPATCH_GATE")

    def test_repeated_complete_is_idempotent_and_does_not_add_a_revision(self):
        module = self.require_orchestrator()
        reference = self.save_in_progress_g0()
        first = module.complete_gate(
            self.contract_path, self.workspace, self.state, "G0", [reference["id"]],
            actor="course-run", at="2026-10-18T09:02:00+08:00",
        )
        revision = load_contract(self.contract_path)["revision"]
        second = module.complete_gate(
            self.contract_path, self.workspace, self.state, "G0", [reference["id"]],
            actor="course-run", at="2026-10-18T09:02:00+08:00",
        )

        self.assertEqual(first, second)
        self.assertEqual(load_contract(self.contract_path)["revision"], revision)

    def test_pass_replay_uses_locked_current_snapshot_after_concurrent_change(self):
        module = self.require_orchestrator()
        reference = self.save_in_progress_g0()
        module.complete_gate(
            self.contract_path,
            self.workspace,
            self.state,
            "G0",
            [reference["id"]],
            actor="course-run",
            at="2026-10-18T09:02:00+08:00",
        )
        stale = load_contract(self.contract_path)
        for path in (self.state / "dispatch").glob("*.json"):
            path.unlink()

        from src.transactions import mutate_contract_atomic

        mutate_contract_atomic(
            self.contract_path,
            lambda value: block_gate(
                value,
                "G1",
                "concurrent evidence loss",
                "review-race",
                "2026-10-18T09:03:00+08:00",
            ),
            expected_revision=1,
        )

        with mock.patch.object(module, "load_contract", return_value=stale):
            envelope = module.complete_gate(
                self.contract_path,
                self.workspace,
                self.state,
                "G0",
                [reference["id"]],
                actor="course-run",
                at="2026-10-18T09:04:00+08:00",
            )

        self.assertEqual(envelope["contract_revision"], 2)
        self.assertEqual(envelope["gate_id"], "G1")
        self.assertEqual(envelope["gate_status"], "BLOCKED")
        self.assertEqual(envelope["action"], "PAUSE")

    def test_pass_replay_preserves_expected_revision_cas(self):
        module = self.require_orchestrator()
        reference = self.save_in_progress_g0()
        module.complete_gate(
            self.contract_path,
            self.workspace,
            self.state,
            "G0",
            [reference["id"]],
            actor="course-run",
            at="2026-10-18T09:02:00+08:00",
        )

        from src.transactions import mutate_contract_atomic

        mutate_contract_atomic(
            self.contract_path,
            lambda value: block_gate(
                value,
                "G1",
                "concurrent evidence loss",
                "review-race",
                "2026-10-18T09:03:00+08:00",
            ),
            expected_revision=1,
        )
        isolated_state = self.root / "isolated-state"

        with self.assertRaisesRegex(module.OrchestrationError, "revision conflict"):
            module.complete_gate(
                self.contract_path,
                self.workspace,
                isolated_state,
                "G0",
                [reference["id"]],
                actor="course-run",
                at="2026-10-18T09:04:00+08:00",
                expected_revision=1,
            )

        self.assertFalse((isolated_state / "dispatch").exists())

    def test_insufficient_evidence_pauses_with_blocked_envelope(self):
        module = self.require_orchestrator()
        reference = self.save_in_progress_g0(valid=False)

        envelope = module.complete_gate(
            self.contract_path, self.workspace, self.state, "G0", [reference["id"]],
            actor="course-run", at="2026-10-18T09:02:00+08:00",
        )

        self.assertEqual(envelope["action"], "PAUSE")
        self.assertEqual(envelope["reason"], "EVIDENCE_INSUFFICIENT")
        self.assertTrue(envelope["requires_user_input"])
        self.assertEqual(load_contract(self.contract_path)["gates"]["G0"]["status"], "BLOCKED")

    def test_resume_restarts_a_blocked_gate_after_its_blocker_is_resolved(self):
        module = self.require_orchestrator()
        contract = self.save_new_contract()
        begin_gate(contract, "G0", "course-run", "2026-10-18T09:01:00+08:00")
        block_gate(
            contract,
            "G0",
            "缺少學員情境",
            "course-run",
            "2026-10-18T09:02:00+08:00",
        )
        blocker = contract["gates"]["G0"]["risks"][-1]
        reference = materialize_json_evidence(
            self.workspace,
            evidence_id="g0-resolution",
            gate_id="G0",
            kind="blocker_resolution",
            relative_path="evidence/g0-resolution.json",
            value={"learner_context": "已確認"},
        )
        contract["evidence_index"].append(reference)
        resolve_gate_blocker(
            contract,
            "G0",
            blocker["id"],
            "已取得學員情境",
            [reference["id"]],
            "course-run",
            "2026-10-18T09:03:00+08:00",
            workspace_root=self.workspace,
        )
        save_contract_atomic(self.contract_path, contract)

        envelope = module.resume_course(
            self.contract_path,
            self.workspace,
            self.state,
            actor="course-run",
            at="2026-10-18T09:04:00+08:00",
        )

        self.assertEqual(envelope["action"], "DISPATCH_GATE")
        self.assertEqual(envelope["gate_status"], "IN_PROGRESS")

    def test_repair_fix_fails_closed_without_full_transaction_proof(self):
        module = self.require_orchestrator()
        with self.assertRaises(module.OrchestrationError):
            module.validate_repair_fix_authority(
                {
                    "approved_plan_sha256": "a" * 64,
                    "before_hashes": {"lesson.html": "b" * 64},
                    "backup_manifest_sha256": "c" * 64,
                }
            )

    def test_course_run_cli_works_from_arbitrary_cwd_with_explicit_roots(self):
        self.save_new_contract()
        project_root = Path(__file__).resolve().parents[1]
        unrelated = self.root / "outside-clone-cwd"
        unrelated.mkdir()
        skills = self.root / "skills"
        skills.mkdir()
        environment = {
            **os.environ,
            "HOME": str(self.root / "clean-home"),
            "COURSE_DESIGN_SYSTEM_ROOT": str(project_root),
            "COURSE_WEB_ROOT": str(self.workspace),
            "SKILLS_ROOT": str(skills),
            "COURSE_DESIGN_STATE_ROOT": str(self.state),
        }

        process = subprocess.run(
            [
                sys.executable,
                str(project_root / "scripts/course_run.py"),
                "resume",
                "--contract",
                str(self.contract_path),
                "--actor",
                "course-run",
                "--at",
                "2026-10-18T09:01:00+08:00",
            ],
            cwd=unrelated,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout)["action"], "DISPATCH_GATE")

    def test_course_run_cli_rejects_contract_symlink_escape(self):
        outside = self.root / "outside-contract.json"
        contract = new_contract(
            "outside", "Outside", "course-run", "2026-10-18T09:00:00+08:00"
        )
        begin_gate(contract, "G0", "course-run", "2026-10-18T09:01:00+08:00")
        save_contract_atomic(outside, contract)
        linked = self.workspace / "linked-contract.json"
        linked.symlink_to(outside)
        project_root = Path(__file__).resolve().parents[1]
        skills = self.root / "skills"
        skills.mkdir()
        environment = {
            **os.environ,
            "COURSE_DESIGN_SYSTEM_ROOT": str(project_root),
            "COURSE_WEB_ROOT": str(self.workspace),
            "SKILLS_ROOT": str(skills),
            "COURSE_DESIGN_STATE_ROOT": str(self.state),
        }

        process = subprocess.run(
            [
                sys.executable,
                str(project_root / "scripts/course_run.py"),
                "resume",
                "--contract",
                str(linked),
                "--actor",
                "course-run",
                "--at",
                "2026-10-18T09:02:00+08:00",
            ],
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(process.returncode, 2)
        self.assertIn("symbolic link", process.stderr)
        self.assertFalse((self.state / "dispatch").exists())


if __name__ == "__main__":
    unittest.main()
