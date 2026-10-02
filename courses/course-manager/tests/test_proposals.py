import json
import tempfile
import unittest
from pathlib import Path

from src.proposals import (
    build_merge_proposal,
    build_move_proposal,
    build_new_course_proposal,
    write_proposal,
)


class ProposalTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "no-handout-project").mkdir()
        (self.root / "no-handout-project" / "README.md").write_text(
            "# SQL Server automation course\n", encoding="utf-8"
        )
        (self.root / "move-source").mkdir()
        (self.root / "move-source" / "README.md").write_text(
            "# Reusable SQL lab\n", encoding="utf-8"
        )
        (self.root / "consumer.md").write_text(
            "See move-source/README.md before class.\n", encoding="utf-8"
        )
        (self.root / "formal-course").mkdir()
        (self.root / "formal-course" / "index.html").write_text(
            "<html><title>Formal course</title></html>\n", encoding="utf-8"
        )
        (self.root / "assets").mkdir()
        (self.root / "assets" / "shared.css").write_text("body {}\n", encoding="utf-8")
        (self.root / "_tools").mkdir()
        (self.root / "_tools" / "tool.sh").write_text("echo tool\n", encoding="utf-8")
        (self.root / "merge-source").mkdir()
        (self.root / "merge-target").mkdir()
        (self.root / "merge-source" / "same.txt").write_text("same\n", encoding="utf-8")
        (self.root / "merge-target" / "same.txt").write_text("same\n", encoding="utf-8")
        (self.root / "merge-source" / "conflict.txt").write_text("source\n", encoding="utf-8")
        (self.root / "merge-target" / "conflict.txt").write_text("target\n", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_new_course_proposal_lists_similar_candidates_and_evidence(self):
        proposal = build_new_course_proposal(self.root, "SQL Server")

        self.assertEqual(proposal["proposal_type"], "new-course")
        self.assertTrue(proposal["candidates"])
        self.assertEqual(proposal["candidates"][0]["path"], "no-handout-project")
        self.assertIn("SQL", " ".join(proposal["candidates"][0]["evidence"]))
        self.assertIn("create-new", proposal["decisions_required"])

    def test_move_proposal_blocks_formal_html_and_support(self):
        formal = build_move_proposal(self.root, "formal-course", "archive/formal-course")
        support = build_move_proposal(self.root, "_tools", "archive/_tools")

        self.assertEqual(formal["status"], "blocked")
        self.assertTrue(any("HTML" in reason for reason in formal["risk"]["reasons"]))
        self.assertEqual(support["status"], "blocked")
        self.assertTrue(any("support" in reason.lower() for reason in support["risk"]["reasons"]))

    def test_move_proposal_records_exact_reference_replacements(self):
        proposal = build_move_proposal(self.root, "move-source", "archive/move-source")

        self.assertEqual(proposal["path_replacements"][0]["file"], "consumer.md")
        self.assertEqual(proposal["path_replacements"][0]["old"], "move-source/README.md")
        self.assertEqual(
            proposal["path_replacements"][0]["new"], "archive/move-source/README.md"
        )
        self.assertTrue(proposal["path_replacements"][0]["sha256_before"])
        self.assertEqual(proposal["status"], "blocked")

    def test_merge_marks_identical_and_conflicting_files(self):
        proposal = build_merge_proposal(self.root, "merge-source", "merge-target")
        matrix = {row["path"]: row["status"] for row in proposal["file_matrix"]}

        self.assertEqual(matrix["same.txt"], "identical")
        self.assertEqual(matrix["conflict.txt"], "conflict")
        self.assertEqual(proposal["status"], "blocked")

    def test_write_proposal_creates_json_only_at_requested_path(self):
        proposal = build_new_course_proposal(self.root, "SQL Server")
        path = self.root / "course-manager" / "proposals" / "new.json"

        write_proposal(path, proposal)

        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["schema_version"], 1)


if __name__ == "__main__":
    unittest.main()
