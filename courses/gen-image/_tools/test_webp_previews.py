#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
import importlib.util
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from webp_previews import audit_course, transform_html


class TransformHtmlTests(unittest.TestCase):
    def test_wraps_unlinked_png_and_uses_webp_preview(self) -> None:
        source = '<figure><img src="assets/example.png" alt="Example" loading="lazy"></figure>'

        transformed = transform_html(source)

        self.assertEqual(
            transformed,
            '<figure><a href="assets/example.png" target="_blank" rel="noopener" '
            'aria-label="Example｜開啟原圖（新分頁）"><img src="assets/example.webp" '
            'alt="Example" loading="lazy"></a></figure>',
        )

    def test_updates_existing_download_anchor_without_nesting(self) -> None:
        source = (
            '<a href="img/sample.png" download><img src="img/sample.png" '
            'alt="Sample" loading="eager"></a>'
        )

        transformed = transform_html(source)

        self.assertEqual(transformed.count("<a "), 1)
        self.assertNotIn("download", transformed)
        self.assertEqual(
            transformed,
            '<a href="img/sample.png" target="_blank" rel="noopener" '
            'aria-label="Sample｜開啟原圖（新分頁）"><img src="img/sample.webp" '
            'alt="Sample" loading="eager"></a>',
        )

    def test_wraps_svg_without_changing_its_display_source(self) -> None:
        source = '<img src="assets/diagram.svg" alt="Diagram" loading="lazy">'

        transformed = transform_html(source)

        self.assertEqual(
            transformed,
            '<a href="assets/diagram.svg" target="_blank" rel="noopener" '
            'aria-label="Diagram｜開啟原圖（新分頁）"><img src="assets/diagram.svg" '
            'alt="Diagram" loading="lazy"></a>',
        )

    def test_preserves_protected_image_attributes_verbatim(self) -> None:
        source = (
            '<img class="hero" src="photo.png" alt="Detailed image" loading="lazy" '
            'style="width:100%;height:auto" width="1254" height="1254">'
        )

        transformed = transform_html(source)

        self.assertIn(
            '<img class="hero" src="photo.webp" alt="Detailed image" loading="lazy" '
            'style="width:100%;height:auto" width="1254" height="1254">',
            transformed,
        )

    def test_rejects_image_nested_inside_non_direct_link(self) -> None:
        source = '<a href="lesson.html"><span><img src="photo.png" alt="Photo"></span></a>'

        with self.assertRaisesRegex(ValueError, "non-direct image link"):
            transform_html(source)


class AuditCourseTests(unittest.TestCase):
    def test_counts_reused_png_once_and_checks_real_preview(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            assets = root / "assets"
            assets.mkdir()
            original = assets / "shared.png"
            real_png = (
                Path(__file__).resolve().parents[1]
                / "assets/course-visuals/2026-10/v01-a-hero-2026-10.png"
            )
            original.write_bytes(real_png.read_bytes())
            preview = assets / "shared.webp"
            subprocess.run(
                ["cwebp", "-quiet", "-q", "90", str(original), "-o", str(preview)],
                check=True,
            )
            markup = (
                '<a href="assets/shared.png" target="_blank" rel="noopener" '
                'aria-label="Shared｜開啟原圖（新分頁）"><img src="assets/shared.webp" '
                'alt="Shared" loading="lazy"></a>'
            )
            (root / "one.html").write_text(markup, encoding="utf-8")
            (root / "two.html").write_text(markup, encoding="utf-8")

            result = audit_course(root)

            self.assertEqual(result.page_count, 2)
            self.assertEqual(result.image_occurrences, 2)
            self.assertEqual(result.unique_png_originals, 1)
            self.assertEqual(result.unique_webp_previews, 1)
            self.assertEqual(result.errors, ())


class HistoricalVerifierTests(unittest.TestCase):
    def test_collects_webp_display_and_png_original_link(self) -> None:
        verifier_path = Path(__file__).with_name("verify-image-refresh.py")
        spec = importlib.util.spec_from_file_location("verify_image_refresh", verifier_path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        markup = (
            '<a href="assets/course-visuals/2026-10/example.png" target="_blank" '
            'rel="noopener"><img src="assets/course-visuals/2026-10/example.webp" '
            'alt="Example"></a>'
        )

        references = module.collect_local_references(markup)

        self.assertEqual(
            references,
            (
                "assets/course-visuals/2026-10/example.webp",
                "assets/course-visuals/2026-10/example.png",
            ),
        )


if __name__ == "__main__":
    unittest.main()
