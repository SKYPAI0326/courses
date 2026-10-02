import tempfile
import unittest
from pathlib import Path

from src.catalog import catalog_is_stale, find_items
from src.discover import scan_workspace
from src.inspect import extract_references, inspect_path, read_text_excerpt


class InspectTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self._write(
            "formal-course/CH1-1.html",
            '<html><head><title>SQL Server Keys</title></head>'
            '<body><a href="../assets/shared.css">CSS</a></body></html>',
        )
        self._write("assets/shared.css", "body { color: black; }\n")
        self._write("notes/research.md", "See formal-course/CH1-1.html before class.\n")
        (self.root / "archive.pdf").write_bytes(b"%PDF\x00\x01binary")

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_catalog_reports_stale_when_item_fingerprint_changes(self):
        catalog = scan_workspace(self.root)
        self._write("formal-course/CH1-1.html", "changed")

        stale, reasons = catalog_is_stale(self.root, catalog)

        self.assertTrue(stale)
        self.assertTrue(any("formal-course" in reason for reason in reasons))

    def test_find_matches_name_path_kind_and_search_terms(self):
        catalog = scan_workspace(self.root)

        matches = find_items(catalog, "SQL Server")

        self.assertEqual([item["path"] for item in matches], ["formal-course"])

    def test_inspect_returns_bounded_text_for_markdown_and_html(self):
        result = inspect_path(self.root, "formal-course")

        self.assertEqual(result["path"], "formal-course")
        self.assertIn("formal-course/CH1-1.html", result["tree"])
        summary = next(item for item in result["file_summaries"] if item["path"].endswith("CH1-1.html"))
        self.assertIn("SQL Server Keys", summary["text"])
        self.assertFalse(summary["truncated"])

    def test_deep_inspection_has_larger_text_limit(self):
        self._write("formal-course/long.md", "x" * 2500)

        shallow = inspect_path(self.root, "formal-course", deep=False)
        deep = inspect_path(self.root, "formal-course", deep=True)
        shallow_text = next(item["text"] for item in shallow["file_summaries"] if item["path"].endswith("long.md"))
        deep_text = next(item["text"] for item in deep["file_summaries"] if item["path"].endswith("long.md"))

        self.assertEqual(len(shallow_text), 2000)
        self.assertEqual(len(deep_text), 2500)

    def test_reference_extraction_separates_incoming_and_outgoing_paths(self):
        references = extract_references(self.root, self.root / "formal-course")

        self.assertTrue(any(ref["target"] == "../assets/shared.css" for ref in references["outgoing"]))
        self.assertTrue(any(ref["source"] == "notes/research.md" for ref in references["incoming"]))

    def test_binary_files_are_summarized_without_decoding_as_text(self):
        result = inspect_path(self.root, ".")
        summary = next(item for item in result["file_summaries"] if item["path"] == "archive.pdf")

        self.assertEqual(summary["file_type"], "binary")
        self.assertIsNone(summary["text"])

    def test_read_text_excerpt_is_bounded(self):
        path = self.root / "notes" / "long.md"
        path.write_text("a" * 2500, encoding="utf-8")

        self.assertEqual(len(read_text_excerpt(path)), 2000)
        self.assertEqual(len(read_text_excerpt(path, deep=True)), 2500)


if __name__ == "__main__":
    unittest.main()
