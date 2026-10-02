import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.operations import apply_proposal, rollback_manifest
from src.proposals import build_move_proposal, write_proposal


class OperationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "clean-source").mkdir()
        (self.root / "clean-source" / "README.md").write_text("clean source\n", encoding="utf-8")
        (self.root / "referenced-source").mkdir()
        (self.root / "referenced-source" / "README.md").write_text("referenced source\n", encoding="utf-8")
        (self.root / "consumer.md").write_text(
            "Read referenced-source/README.md.\n", encoding="utf-8"
        )
        (self.root / "changed-source").mkdir()
        (self.root / "changed-source" / "README.md").write_text("before\n", encoding="utf-8")
        (self.root / "collision-source").mkdir()
        (self.root / "collision-source" / "README.md").write_text("source\n", encoding="utf-8")
        (self.root / "collision-destination").mkdir()
        (self.root / "collision-destination" / "README.md").write_text("target\n", encoding="utf-8")
        (self.root / "archive").mkdir()
        (self.root / "course-manager").mkdir()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _proposal(self, source: str, destination: str):
        proposal = build_move_proposal(self.root, source, destination)
        path = self.root / "course-manager" / "proposal.json"
        write_proposal(path, proposal)
        return path, proposal

    def _approval(self, path: Path, proposal_id: str, approved: bool = True):
        path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "proposal_id": proposal_id,
                    "approved": approved,
                    "approved_at": "2026-10-02T15:00:00+08:00",
                }
            ),
            encoding="utf-8",
        )

    def test_apply_requires_matching_approved_proposal(self):
        proposal_path, proposal = self._proposal("clean-source", "archive/clean-source")
        approval_path = self.root / "approval.json"
        self._approval(approval_path, proposal["proposal_id"], approved=False)

        result = apply_proposal(self.root, proposal_path, approval_path)

        self.assertEqual(result["status"], "REFUSED")
        self.assertTrue((self.root / "clean-source").exists())

    def test_apply_refuses_when_source_fingerprint_changed(self):
        proposal_path, proposal = self._proposal("changed-source", "archive/changed-source")
        (self.root / "changed-source" / "README.md").write_text("changed\n", encoding="utf-8")
        approval_path = self.root / "approval.json"
        self._approval(approval_path, proposal["proposal_id"])

        result = apply_proposal(self.root, proposal_path, approval_path)

        self.assertEqual(result["status"], "REFUSED")
        self.assertTrue((self.root / "changed-source").exists())
        self.assertFalse((self.root / "archive" / "changed-source").exists())

    def test_apply_moves_only_listed_paths_and_does_not_stage_git(self):
        proposal_path, proposal = self._proposal("clean-source", "archive/clean-source")
        approval_path = self.root / "approval.json"
        self._approval(approval_path, proposal["proposal_id"])

        result = apply_proposal(self.root, proposal_path, approval_path)

        self.assertEqual(result["status"], "APPLIED")
        self.assertFalse((self.root / "clean-source").exists())
        self.assertEqual(
            (self.root / "archive" / "clean-source" / "README.md").read_text(encoding="utf-8"),
            "clean source\n",
        )
        self.assertFalse((self.root / ".git" / "index").exists())

    def test_apply_refuses_destination_collision(self):
        proposal_path, proposal = self._proposal("collision-source", "collision-destination")
        approval_path = self.root / "approval.json"
        self._approval(approval_path, proposal["proposal_id"])

        result = apply_proposal(self.root, proposal_path, approval_path)

        self.assertEqual(result["status"], "REFUSED")
        self.assertTrue((self.root / "collision-source").exists())

    def test_rollback_restores_source_and_removes_destination(self):
        proposal_path, proposal = self._proposal("clean-source", "archive/clean-source")
        approval_path = self.root / "approval.json"
        self._approval(approval_path, proposal["proposal_id"])
        applied = apply_proposal(self.root, proposal_path, approval_path)

        rolled_back = rollback_manifest(self.root, Path(applied["manifest"]), approval_path)

        self.assertEqual(rolled_back["status"], "ROLLED_BACK")
        self.assertTrue((self.root / "clean-source" / "README.md").exists())
        self.assertFalse((self.root / "archive" / "clean-source").exists())

    def test_apply_and_rollback_use_approved_reference_replacements(self):
        proposal_path, proposal = self._proposal("referenced-source", "archive/referenced-source")
        proposal["status"] = "proposed"
        write_proposal(proposal_path, proposal)
        approval_path = self.root / "approval.json"
        self._approval(approval_path, proposal["proposal_id"])

        applied = apply_proposal(self.root, proposal_path, approval_path)

        self.assertEqual(applied["status"], "APPLIED")
        self.assertIn("archive/referenced-source/README.md", (self.root / "consumer.md").read_text(encoding="utf-8"))
        rollback = rollback_manifest(self.root, Path(applied["manifest"]), approval_path)

        self.assertEqual(rollback["status"], "ROLLED_BACK")
        self.assertIn("referenced-source/README.md", (self.root / "consumer.md").read_text(encoding="utf-8"))

    def test_partial_failure_is_recorded(self):
        proposal_path, proposal = self._proposal("clean-source", "archive/clean-source")
        approval_path = self.root / "approval.json"
        self._approval(approval_path, proposal["proposal_id"])
        real_move = shutil.move

        def move_then_fail(source, destination):
            result = real_move(source, destination)
            raise RuntimeError("simulated post-move failure")

        with patch("src.operations.shutil.move", side_effect=move_then_fail):
            result = apply_proposal(self.root, proposal_path, approval_path)

        self.assertEqual(result["status"], "PARTIAL")
        manifest = json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
        self.assertEqual(manifest["verification_status"], "PARTIAL")


if __name__ == "__main__":
    unittest.main()
