import contextlib
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.course_contract import begin_gate, new_contract, save_contract_atomic
from src.course_evidence import materialize_json_evidence
from tests.gate_test_support import _commit_gate_pass


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI = PROJECT_ROOT / "scripts" / "course_contract.py"
FIXTURES = PROJECT_ROOT / "tests" / "fixtures"


class CourseContractCliTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(CLI), *map(str, arguments)],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_contract(self, contract):
        path = self.root / "_design" / contract["identity"]["slug"] / "course-contract.json"
        save_contract_atomic(path, contract)
        return path

    def add_evidence(self, contract, gate_id, evidence_id):
        contract["evidence_index"].append(
            {
                "id": evidence_id,
                "gate": gate_id,
                "kind": "test_record",
                "path": f"evidence/{evidence_id}.json",
                "sha256": hashlib.sha256(evidence_id.encode("utf-8")).hexdigest(),
            }
        )

    def pass_gate(self, contract, gate_id):
        begin_gate(contract, gate_id, "course-run", "2026-10-18T13:00:00+08:00")
        evidence_id = f"{gate_id.lower()}-evidence"
        self.add_evidence(contract, gate_id, evidence_id)
        _commit_gate_pass(
            contract,
            gate_id,
            [evidence_id],
            f"{gate_id.lower()}-validator",
            "course-run",
            "2026-10-18T13:05:00+08:00",
        )

    def test_init_writes_v3_contract_at_expected_path(self):
        result = self.run_cli(
            "init",
            "--root",
            self.root,
            "--slug",
            "practical-ai",
            "--title",
            "實用生成式 AI",
            "--created-by",
            "課程團隊",
            "--at",
            "2026-10-18T12:00:00+08:00",
        )

        expected = self.root / "_design" / "practical-ai" / "course-contract.json"
        self.assertEqual(result.returncode, 0, result.stderr)
        contract = json.loads(expected.read_text(encoding="utf-8"))
        self.assertEqual(contract["schema_version"], 3)
        self.assertEqual(contract["revision"], 0)
        self.assertEqual(contract["gates"]["G0"]["status"], "NOT_STARTED")

    def test_init_rejects_design_directory_symlink_escape(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.root / "_design").symlink_to(outside, target_is_directory=True)

        result = self.run_cli(
            "init",
            "--root",
            self.root,
            "--slug",
            "practical-ai",
            "--title",
            "實用生成式 AI",
            "--created-by",
            "課程團隊",
            "--at",
            "2026-10-18T12:00:00+08:00",
        )

        self.assertEqual(result.returncode, 2)
        self.assertFalse((outside / "practical-ai" / "course-contract.json").exists())

    def test_init_rejects_slug_directory_symlink_escape(self):
        design = self.root / "_design"
        outside = self.root / "outside"
        design.mkdir()
        outside.mkdir()
        (design / "practical-ai").symlink_to(outside, target_is_directory=True)

        result = self.run_cli(
            "init",
            "--root",
            self.root,
            "--slug",
            "practical-ai",
            "--title",
            "實用生成式 AI",
            "--created-by",
            "課程團隊",
            "--at",
            "2026-10-18T12:00:00+08:00",
        )

        self.assertEqual(result.returncode, 2)
        self.assertFalse((outside / "course-contract.json").exists())

    def test_status_reports_gate_state_evidence_risks_and_next_action(self):
        contract = new_contract(
            "practical-ai", "實用生成式 AI", "課程團隊", "2026-10-18T12:00:00+08:00"
        )
        begin_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")
        gate = contract["gates"]["G0"]
        gate["deliverables"] = [
            {"id": "requirements-brief", "path": "evidence/g0-requirements.md"}
        ]
        gate["evidence"] = [{"id": "interview", "path": "evidence/g0-interview.md"}]
        gate["risks"] = [
            {
                "id": "risk-1",
                "blocking": True,
                "resolved": False,
                "description": "時數未確認",
            }
        ]
        gate["open_questions"] = [{"id": "q1", "text": "是否提供共用帳號？"}]
        path = self.write_contract(contract)

        result = self.run_cli("status", "--contract", path)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Current gate: G0", result.stdout)
        self.assertIn("State: IN_PROGRESS", result.stdout)
        self.assertIn("evidence/g0-requirements.md", result.stdout)
        self.assertIn("時數未確認", result.stdout)
        self.assertIn("是否提供共用帳號？", result.stdout)
        self.assertIn("Next action: resolve blocking risks", result.stdout)
        self.assertNotIn("approval", result.stdout.lower())

    def test_raw_pass_command_is_not_exposed(self):
        contract = new_contract(
            "practical-ai", "實用生成式 AI", "課程團隊", "2026-10-18T12:00:00+08:00"
        )
        self.add_evidence(contract, "G0", "g0-evidence")
        path = self.write_contract(contract)

        passed = self.run_cli(
            "pass",
            "--contract",
            path,
            "--gate",
            "G0",
            "--evidence-id",
            "g0-evidence",
            "--validator-id",
            "requirements-validator",
            "--actor",
            "course-run",
            "--at",
            "2026-10-18T13:05:00+08:00",
        )
        after = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(passed.returncode, 2)
        self.assertIn("invalid choice", passed.stderr)
        self.assertEqual(after["gates"]["G0"]["status"], "NOT_STARTED")

    def test_approve_command_directs_v1_operator_to_migrate(self):
        contract = new_contract(
            "practical-ai", "實用生成式 AI", "課程團隊", "2026-10-18T12:00:00+08:00"
        )
        path = self.write_contract(contract)

        result = self.run_cli("approve", "--contract", path)

        self.assertEqual(result.returncode, 2)
        self.assertIn("migrate", result.stderr)
        self.assertEqual(json.loads(path.read_text(encoding="utf-8")), contract)

    def test_change_semantic_flag_controls_invalidation(self):
        contract = new_contract(
            "practical-ai", "實用生成式 AI", "課程團隊", "2026-10-18T12:00:00+08:00"
        )
        for gate_id in ("G0", "G1", "G2"):
            self.pass_gate(contract, gate_id)
        path = self.write_contract(contract)

        nonsemantic = self.run_cli(
            "change",
            "--contract",
            path,
            "--gate",
            "G1",
            "--reason",
            "修正錯字",
            "--actor",
            "編輯",
            "--at",
            "2026-10-19T09:00:00+08:00",
        )
        after_nonsemantic = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(nonsemantic.returncode, 0, nonsemantic.stderr)
        self.assertEqual(after_nonsemantic["revision"], 1)
        self.assertEqual(after_nonsemantic["gates"]["G1"]["status"], "PASS")
        self.assertEqual(after_nonsemantic["gates"]["G2"]["status"], "PASS")

        semantic = self.run_cli(
            "change",
            "--contract",
            path,
            "--gate",
            "G1",
            "--reason",
            "代表工具改版",
            "--actor",
            "course-run",
            "--at",
            "2026-10-19T10:00:00+08:00",
            "--semantic",
        )
        after_semantic = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(semantic.returncode, 0, semantic.stderr)
        self.assertEqual(after_semantic["revision"], 2)
        self.assertEqual(after_semantic["gates"]["G0"]["status"], "PASS")
        self.assertEqual(after_semantic["gates"]["G1"]["status"], "IN_PROGRESS")
        self.assertTrue(
            all(
                after_semantic["gates"][gate_id]["status"] == "STALE"
                for gate_id in ("G2", "G3", "G4", "G5", "G6")
            )
        )

    def test_block_and_resolve_blocker_are_transactional_and_do_not_auto_pass(self):
        contract = new_contract(
            "practical-ai", "實用生成式 AI", "課程團隊", "2026-10-18T12:00:00+08:00"
        )
        path = self.write_contract(contract)

        blocked = self.run_cli(
            "block",
            "--contract",
            path,
            "--gate",
            "G0",
            "--reason",
            "缺少學員使用情境",
            "--actor",
            "course-run",
            "--at",
            "2026-10-18T13:05:00+08:00",
        )
        after_block = json.loads(path.read_text(encoding="utf-8"))
        blocker_id = after_block["gates"]["G0"]["risks"][-1]["id"]
        reference = materialize_json_evidence(
            self.root,
            evidence_id="g0-blocker-resolution",
            gate_id="G0",
            kind="blocker_resolution",
            relative_path="evidence/g0-blocker-resolution.json",
            value={"learner_context": "已確認"},
        )
        after_block["evidence_index"].append(reference)
        save_contract_atomic(path, after_block)

        resolved = self.run_cli(
            "resolve-blocker",
            "--contract",
            path,
            "--workspace-root",
            self.root,
            "--gate",
            "G0",
            "--blocker-id",
            blocker_id,
            "--resolution",
            "已取得學員使用情境",
            "--evidence-id",
            reference["id"],
            "--actor",
            "course-run",
            "--at",
            "2026-10-18T13:10:00+08:00",
            "--expected-revision",
            1,
        )
        after_resolution = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(blocked.returncode, 0, blocked.stderr)
        self.assertEqual(after_block["revision"], 1)
        self.assertEqual(resolved.returncode, 0, resolved.stderr)
        self.assertEqual(after_resolution["revision"], 2)
        self.assertEqual(after_resolution["gates"]["G0"]["status"], "BLOCKED")
        self.assertEqual(
            after_resolution["gates"]["G0"]["evidence"][-1]["blocker_id"],
            blocker_id,
        )

        restarted = self.run_cli(
            "begin",
            "--contract",
            path,
            "--gate",
            "G0",
            "--actor",
            "course-run",
            "--at",
            "2026-10-18T13:20:00+08:00",
            "--expected-revision",
            2,
        )
        after_restart = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(restarted.returncode, 0, restarted.stderr)
        self.assertEqual(after_restart["revision"], 3)
        self.assertEqual(after_restart["gates"]["G0"]["status"], "IN_PROGRESS")

    def test_stale_expected_revision_is_rejected_without_write(self):
        contract = new_contract(
            "practical-ai", "實用生成式 AI", "課程團隊", "2026-10-18T12:00:00+08:00"
        )
        path = self.write_contract(contract)
        first = self.run_cli(
            "change",
            "--contract",
            path,
            "--gate",
            "G0",
            "--reason",
            "first",
            "--actor",
            "test",
            "--at",
            "2026-10-18T13:00:00+08:00",
            "--expected-revision",
            0,
        )
        before_stale = path.read_bytes()

        stale = self.run_cli(
            "change",
            "--contract",
            path,
            "--gate",
            "G0",
            "--reason",
            "stale",
            "--actor",
            "test",
            "--at",
            "2026-10-18T13:01:00+08:00",
            "--expected-revision",
            0,
        )

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(stale.returncode, 2)
        self.assertIn("revision conflict", stale.stderr)
        self.assertEqual(path.read_bytes(), before_stale)

    def test_committed_durability_error_is_not_retried_and_is_explicit(self):
        import src.transactions as transactions

        spec = importlib.util.spec_from_file_location("course_contract_cli", CLI)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
        contract = new_contract(
            "practical-ai",
            "實用生成式 AI",
            "課程團隊",
            "2026-10-18T12:00:00+08:00",
        )
        contract["revision"] = 1
        path = self.root / "course-contract.json"
        error = transactions.TransactionCommittedDurabilityError(
            path,
            contract,
            OSError("directory fsync failed"),
        )
        stderr = io.StringIO()

        with mock.patch.object(cli, "_mutate", side_effect=error) as mutate:
            with contextlib.redirect_stderr(stderr):
                result = cli.main(
                    [
                        "change",
                        "--contract",
                        str(path),
                        "--gate",
                        "G0",
                        "--reason",
                        "change",
                        "--actor",
                        "test",
                        "--at",
                        "2026-10-18T13:00:00+08:00",
                    ]
                )

        self.assertEqual(result, 3)
        self.assertEqual(mutate.call_count, 1)
        self.assertIn("already committed", stderr.getvalue())
        self.assertIn("durability is uncertain", stderr.getvalue())
        self.assertIn("revision 1", stderr.getvalue())
        self.assertIn(str(path), stderr.getvalue())

    def test_external_action_commands_require_exact_authorized_hash(self):
        contract = new_contract(
            "practical-ai", "實用生成式 AI", "課程團隊", "2026-10-18T12:00:00+08:00"
        )
        for gate_id in ("G0", "G1", "G2", "G3", "G4", "G5", "G6"):
            self.pass_gate(contract, gate_id)
        path = self.write_contract(contract)

        proposed = self.run_cli(
            "propose-action",
            "--contract",
            path,
            "--action-id",
            "publish-1",
            "--kind",
            "publish-course",
            "--manifest-path",
            "evidence/release.json",
            "--manifest-sha256",
            "a" * 64,
            "--actor",
            "course-ops",
            "--at",
            "2026-10-18T18:00:00+08:00",
        )
        authorized = self.run_cli(
            "authorize-action",
            "--contract",
            path,
            "--action-id",
            "publish-1",
            "--approved-by",
            "使用者",
            "--at",
            "2026-10-18T18:05:00+08:00",
            "--note",
            "核准發布",
        )
        checked = self.run_cli(
            "check-action",
            "--contract",
            path,
            "--action-id",
            "publish-1",
            "--manifest-sha256",
            "a" * 64,
        )
        rejected = self.run_cli(
            "check-action",
            "--contract",
            path,
            "--action-id",
            "publish-1",
            "--manifest-sha256",
            "b" * 64,
        )

        self.assertEqual(proposed.returncode, 0, proposed.stderr)
        self.assertEqual(authorized.returncode, 0, authorized.stderr)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(rejected.returncode, 2)

    def test_migrate_command_upgrades_v1_to_v3(self):
        path = self.root / "legacy.json"
        source = FIXTURES / "course-contracts" / "v1-approved-through-g2.json"
        path.write_bytes(source.read_bytes())

        result = self.run_cli(
            "migrate",
            "--contract",
            path,
            "--actor",
            "course-run",
            "--at",
            "2026-10-18T19:00:00+08:00",
        )
        migrated = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(migrated["schema_version"], 3)
        self.assertEqual(migrated["gates"]["G0"]["status"], "STALE")

    def test_migrate_command_upgrades_v2_to_v3_with_workspace_evidence(self):
        evidence = self.root / "evidence" / "g0.json"
        evidence.parent.mkdir()
        evidence.write_bytes(b"g0")
        contract = new_contract(
            "practical-ai",
            "實用生成式 AI",
            "course-run",
            "2026-10-18T12:00:00+08:00",
        )
        begin_gate(contract, "G0", "course-run", "2026-10-18T12:05:00+08:00")
        contract["evidence_index"].append(
            {
                "id": "g0-evidence",
                "gate": "G0",
                "kind": "requirements_record",
                "path": "evidence/g0.json",
                "sha256": hashlib.sha256(b"g0").hexdigest(),
            }
        )
        _commit_gate_pass(
            contract,
            "G0",
            ["g0-evidence"],
            "requirements-validator",
            "course-run",
            "2026-10-18T12:10:00+08:00",
        )
        contract["schema_version"] = 2
        del contract["revision"]
        contract.pop("evidence_archive", None)
        path = self.write_contract(contract)

        result = self.run_cli(
            "migrate",
            "--contract",
            path,
            "--workspace-root",
            self.root,
            "--actor",
            "course-run",
            "--at",
            "2026-10-18T19:00:00+08:00",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        migrated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(migrated["schema_version"], 3)
        self.assertEqual(migrated["gates"]["G0"]["status"], "PASS")

    def test_validate_returns_nonzero_for_invalid_contract(self):
        path = self.root / "invalid.json"
        path.write_text(
            json.dumps({"schema_version": 2, "gates": {}}, ensure_ascii=False),
            encoding="utf-8",
        )

        result = self.run_cli("validate", "--contract", path)

        self.assertEqual(result.returncode, 1)
        self.assertIn("$.identity", result.stdout)
        self.assertIn("$.gates.G0", result.stdout)

    def test_mutation_rejects_invalid_loaded_contract_before_change(self):
        contract = new_contract(
            "practical-ai", "實用生成式 AI", "課程團隊", "2026-10-18T12:00:00+08:00"
        )
        contract["changes"] = "not-a-list"
        path = self.root / "invalid-contract.json"
        before = json.dumps(contract, ensure_ascii=False, indent=2) + "\n"
        path.write_text(before, encoding="utf-8")

        result = self.run_cli(
            "begin",
            "--contract",
            path,
            "--gate",
            "G0",
            "--actor",
            "course-run",
            "--at",
            "2026-10-18T13:00:00+08:00",
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(path.read_text(encoding="utf-8"), before)

    def test_status_does_not_mutate_or_summarize_away_original_prose(self):
        prose = (
            "這門課給第一次負責行銷企劃的同仁。學員要能從真實商品資料完成一份"
            "可交付給主管審核的活動方案，並保留選擇受眾與渠道的完整理由。"
        )
        contract = new_contract(
            "marketing-practice", "行銷企劃實作", "課程團隊", "2026-10-18T12:00:00+08:00"
        )
        contract["G0_requirements"]["learner_context"] = prose
        path = self.write_contract(contract)
        before = path.read_bytes()

        result = self.run_cli("status", "--contract", path)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(path.read_bytes(), before)
        loaded = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(loaded["G0_requirements"]["learner_context"], prose)
        self.assertNotIn(prose, result.stdout)
        self.assertIn("$.G0_requirements", result.stdout)


if __name__ == "__main__":
    unittest.main()
