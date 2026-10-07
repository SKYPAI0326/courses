from pathlib import Path
import unittest

from bs4 import BeautifulSoup, Comment, Tag


COURSE_ROOT = Path(__file__).resolve().parents[4]
PAGES = {
    "CH1-1": {
        "html": "part1/CH1-1.html",
        "fragment": "_source/fragments/part1-CH1-1.fragment",
        "required": ["只交付一份完整 HTML", "CSS 寫在同一檔案", "原生 JavaScript", "API"],
    },
    "CH1-2": {
        "html": "part1/CH1-2.html",
        "fragment": "_source/fragments/part1-CH1-2.fragment",
        "required": ["<!DOCTYPE html>", "</html>", "重複按開始", "驗收", "1500 秒", "301 秒", "300 秒", "390 像素", "離線"],
    },
    "CH1-3": {
        "html": "part1/CH1-3.html",
        "fragment": "_source/fragments/part1-CH1-3.fragment",
        "required": ["<!DOCTYPE html>", "</html>", "外部函式庫", "不需網路", "1500 秒", "301 秒", "300 秒", "390 像素", "離線"],
    },
}


def normalized_text(node):
    return " ".join(node.get_text(" ", strip=True).split())


class ChapterOneHandoutTests(unittest.TestCase):
    def setUp(self):
        self.pages = {}
        for name, spec in PAGES.items():
            html = BeautifulSoup((COURSE_ROOT / spec["html"]).read_text(), "html.parser")
            fragment = BeautifulSoup((COURSE_ROOT / spec["fragment"]).read_text(), "html.parser")
            self.pages[name] = (html, fragment, spec)

    def test_visible_chapter_content_matches_its_official_fragment(self):
        for name, (page, fragment, _spec) in self.pages.items():
            with self.subTest(chapter=name):
                body = page.select_one(".lesson-body")
                comments = [node for node in body.find_all(string=lambda s: isinstance(s, Comment))]
                start = next((node for node in comments if node.strip() == "learner-content:start"), None)
                end = next((node for node in comments if node.strip() == "learner-content:end"), None)
                self.assertIsNotNone(start, "missing learner-content:start")
                self.assertIsNotNone(end, "missing learner-content:end")
                self.assertIs(start.parent, body)
                self.assertIs(end.parent, body)
                visible_nodes = []
                node = start.next_sibling
                while node is not None and node is not end:
                    visible_nodes.append(node)
                    node = node.next_sibling
                self.assertIs(node, end, "learner-content markers are out of order")
                page_text = " ".join(normalized_text(item) for item in visible_nodes if isinstance(item, Tag))
                self.assertEqual(page_text, normalized_text(fragment))

    def test_prompts_retain_complete_file_constraints_and_render_boundaries(self):
        for name, (page, _fragment, spec) in self.pages.items():
            with self.subTest(chapter=name):
                prompts = page.select(".lesson-body .prompt-box, .lesson-body .result-box")
                self.assertTrue(prompts, "missing visible prompt")
                prompt_text = "\n".join(prompt.get_text("\n", strip=True) for prompt in prompts)
                for required in spec["required"]:
                    self.assertIn(required, prompt_text)

    def test_specification_prompt_is_the_same_in_ch1_2_ch1_3_and_material_asset(self):
        chapter2 = self.pages["CH1-2"][0].select_one(".lesson-body .prompt-box")
        chapter3 = self.pages["CH1-3"][0].select_one(".lesson-body #prompt-timer")
        self.assertIsNotNone(chapter2)
        self.assertIsNotNone(chapter3)
        expected = normalized_text(chapter2)
        self.assertEqual(normalized_text(chapter3), expected)
        asset = (COURSE_ROOT / "assets/materials/prompt-timer.txt").read_text()
        self.assertEqual(" ".join(asset.split()), expected)
        from zipfile import ZipFile
        with ZipFile(COURSE_ROOT / "assets/materials/materials.zip") as archive:
            packaged = archive.read("prompt-timer.txt").decode()
        self.assertEqual(" ".join(packaged.split()), expected)

    def test_chapter1_1_produces_the_promised_work_requirement_record(self):
        page = self.pages["CH1-1"][0]
        record = page.select_one(".lesson-body #core-1 .requirements-record")
        self.assertIsNotNone(record, "add the promised note template to the learner page")
        for label in ["使用者與工作情境", "目前問題", "必要輸入", "預期結果", "驗收證據"]:
            self.assertIn(label, normalized_text(record))

    def test_chapter1_1_observes_topic_change_before_countdown_reaches_zero(self):
        page = self.pages["CH1-1"][0]
        steps = [normalized_text(item) for item in page.select(".lesson-body #core-1 ol li")]
        topic_step = next(i for i, step in enumerate(steps) if "修改會議主題" in step)
        zero_step = next(i for i, step in enumerate(steps) if "倒數到零" in step)
        self.assertLess(topic_step, zero_step, "a stopped timer cannot demonstrate topic edits during countdown")

    def test_chapter1_2_requires_a_learner_written_requirement_before_the_model_answer(self):
        page = self.pages["CH1-2"][0]
        exercise = page.select_one(".lesson-body #core-1 .spec-writing-exercise")
        prompt = page.select_one(".lesson-body #core-2 .prompt-box")
        self.assertIsNotNone(exercise, "include an actual writing task, not only analysis of a completed prompt")
        self.assertIsNotNone(prompt)
        self.assertLess(exercise.sourceline or 0, prompt.sourceline or 0)
        text = normalized_text(exercise)
        self.assertIn("自己的需求", text)
        self.assertIn("對應的驗收", text)
        self.assertIn("先完成再往下對照", text)
        exception_check = normalized_text(page.select_one(".lesson-body #core-1 tr:nth-of-type(5)"))
        self.assertIn("逐一輸入空白、0、-1、1.5 並按「開始」", exception_check)
        self.assertIn("設為 10 秒、按「重設」和「開始」", exception_check)

    def test_chapter1_3_tests_prompt_boundaries_and_uses_one_versioned_save_path(self):
        page = self.pages["CH1-3"][0]
        body = normalized_text(page.select_one(".lesson-body"))
        for expected in ["1500 秒", "25:00", "未命名會議", "300 秒", "301 秒", "手機畫面", "離線"]:
            self.assertIn(expected, body)
        self.assertIn("meeting-timer-v1.html", body)
        self.assertIn("meeting-timer-v2.html", body)
        self.assertIn("檔名輸入 meeting-timer-v1.html", body)
        self.assertNotIn("檔名輸入 meeting-timer.html", body)
        self.assertIn("離線未驗證", body)
        self.assertIn("音訊驗收未通過", body)
        boundary_row = next(
            normalized_text(row)
            for row in page.select(".lesson-body #core-3 tbody tr")
            if "301 秒" in normalized_text(row)
        )
        self.assertIn("301", boundary_row)
        self.assertIn("300", boundary_row)
        self.assertLess(boundary_row.index("301"), boundary_row.index("重設"))
        self.assertLess(boundary_row.index("重設"), boundary_row.index("300"))
        prompt = normalized_text(page.select_one(".lesson-body #prompt-timer"))
        self.assertIn("將秒數設為 301 秒，按「重設」再按「開始」", prompt)
        self.assertIn("將秒數改為 300 秒，再按「重設」和「開始」", prompt)
        self.assertIn("將秒數設為 1 秒，按「重設」和「開始」測歸零", prompt)
        self.assertIn("空白、0、-1、1.5 各自輸入後按「開始」都不可啟動", prompt)
        self.assertIn("畫面或計時規則", body)
        self.assertIn("不要要求 AI 改程式", body)
        self.assertIn("按重設再按開始重測", body)
        audio_row = next(
            normalized_text(row)
            for row in page.select(".lesson-body #core-3 tbody tr")
            if "測歸零" in normalized_text(row)
        )
        self.assertIn("1，按「重設」再按「開始」", audio_row)
        self.assertIn("按「重設」和「開始」重測", audio_row)
        exception_row = next(
            normalized_text(row)
            for row in page.select(".lesson-body #core-3 tbody tr")
            if "空白、0、-1、1.5" in normalized_text(row)
        )
        self.assertIn("按「開始」", exception_row)
        self.assertIn("按「重設」再按「開始」", exception_row)

    def test_chapter_pages_do_not_require_duplicate_downloads(self):
        for name, (page, _fragment, _spec) in self.pages.items():
            with self.subTest(chapter=name):
                body = page.select_one(".lesson-body")
                self.assertFalse(body.select("a[download]"), "learner material should be readable in the page")
                self.assertFalse(body.select("details#legacy-reference"), "old handout must not be hidden or duplicated")


if __name__ == "__main__":
    unittest.main()
