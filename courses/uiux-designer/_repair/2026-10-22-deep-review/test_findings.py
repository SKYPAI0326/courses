from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


COURSE = Path(__file__).resolve().parents[2]
PROJECT = COURSE.parents[1]


class DeepReviewRepairTests(unittest.TestCase):
    def read_course(self, relative: str) -> str:
        return (COURSE / relative).read_text(encoding="utf-8")

    def test_current_validation_state_is_blocked(self) -> None:
        report = self.read_course("_validation/FINAL-REPORT.md")
        result = json.loads(self.read_course("_validation/validation-result.json"))
        self.assertIn("狀態：BLOCKED", report)
        self.assertIn("有效證據：0 筆", report)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["valid_record_count"], 0)

    def test_gate_header_records_current_block(self) -> None:
        gates = self.read_course("_gates.md")
        self.assertRegex(gates, r"\*\*目前狀態\*\*：`BLOCKED`")
        self.assertIn("## 2026-10-22：Deep Review 修復", gates)

    def test_b6_overview_lists_all_eight_tasks(self) -> None:
        index = self.read_course("index.html")
        row = re.search(r"<tr><td[^>]*>第 14 堂.*?</tr>", index, re.S)
        self.assertIsNotNone(row)
        self.assertIn("T01–T08", row.group(0))
        self.assertNotIn("T01–T07", row.group(0))

    def test_vscode_has_official_entry_and_success_check(self) -> None:
        course_start = self.read_course("assets/COURSE-START.html")
        lesson = (PROJECT / "_lessons/uiux-designer/B8-web-git-deploy.md").read_text(encoding="utf-8")
        page = self.read_course("part3/CH8-web-git-deploy.html")
        official = "https://code.visualstudio.com/Download"
        for text in (course_start, lesson, page):
            self.assertIn(official, text)
            self.assertIn("Welcome", text)
            self.assertIn("Open Folder", text)


if __name__ == "__main__":
    unittest.main()
