import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.course_contract import approve_gate, new_contract, save_contract_atomic, submit_gate


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI = PROJECT_ROOT / "scripts" / "course_contract.py"


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

    def test_init_writes_design_contract_at_expected_path(self):
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
        self.assertTrue(expected.is_file())
        contract = json.loads(expected.read_text(encoding="utf-8"))
        self.assertEqual(contract["identity"]["title"], "實用生成式 AI")
        self.assertIn(str(expected), result.stdout)

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
        submit_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")
        path = self.write_contract(contract)

        result = self.run_cli("status", "--contract", path)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Current gate: G0", result.stdout)
        self.assertIn("State: REVIEW", result.stdout)
        self.assertIn("Deliverables", result.stdout)
        self.assertIn("evidence/g0-requirements.md", result.stdout)
        self.assertIn("Evidence", result.stdout)
        self.assertIn("evidence/g0-interview.md", result.stdout)
        self.assertIn("Blockers", result.stdout)
        self.assertIn("時數未確認", result.stdout)
        self.assertIn("Open questions", result.stdout)
        self.assertIn("是否提供共用帳號？", result.stdout)
        self.assertIn("Next action: resolve blocking risks before approval", result.stdout)

    def test_approve_requires_explicit_approval_note(self):
        contract = new_contract(
            "practical-ai", "實用生成式 AI", "課程團隊", "2026-10-18T12:00:00+08:00"
        )
        submit_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")
        path = self.write_contract(contract)

        result = self.run_cli(
            "approve",
            "--contract",
            path,
            "--gate",
            "G0",
            "--approved-by",
            "使用者",
            "--at",
            "2026-10-18T13:05:00+08:00",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--note", result.stderr)
        unchanged = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(unchanged["gates"]["G0"]["status"], "REVIEW")

    def test_change_semantic_flag_controls_invalidation(self):
        contract = new_contract(
            "practical-ai", "實用生成式 AI", "課程團隊", "2026-10-18T12:00:00+08:00"
        )
        for gate_id in ("G0", "G1", "G2"):
            submit_gate(contract, gate_id, "child", "2026-10-18T13:00:00+08:00")
            approve_gate(
                contract,
                gate_id,
                "使用者",
                "2026-10-18T13:05:00+08:00",
                f"核准 {gate_id}",
            )
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
        self.assertEqual(after_nonsemantic["gates"]["G1"]["status"], "APPROVED")
        self.assertEqual(after_nonsemantic["gates"]["G2"]["status"], "APPROVED")

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
        self.assertEqual(after_semantic["gates"]["G0"]["status"], "APPROVED")
        self.assertEqual(after_semantic["gates"]["G1"]["status"], "DRAFT")
        self.assertTrue(
            all(
                after_semantic["gates"][gate_id]["status"] == "STALE"
                for gate_id in ("G2", "G3", "G4", "G5", "G6")
            )
        )

    def test_validate_returns_nonzero_for_invalid_contract(self):
        path = self.root / "invalid.json"
        path.write_text(
            json.dumps({"schema_version": 1, "gates": {}}, ensure_ascii=False),
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
            "submit",
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
