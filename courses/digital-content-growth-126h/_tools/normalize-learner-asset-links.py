#!/usr/bin/env python3
"""Make learner-facing asset links readable without exposing raw Markdown."""

from __future__ import annotations

import re
from pathlib import Path


COURSE_DIR = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(
    r'<a class="asset-action secondary" href="assets/templates/(?P<name>[^"]+)\.md" '
    r'download="[^"]*">下載原始模板（UTF-8）</a>'
)
ASSET_NOTE = (
    '<p class="asset-note">學員請使用 HTML 閱讀版或 HTML 工作版；可直接複製到 Word、'
    '記事本或其他可編輯工具另存。Markdown 原始檔保留給課程製作者，不列入學員操作。</p>'
)


def normalize_page(path: Path) -> tuple[str, int, bool]:
    original = path.read_text(encoding="utf-8")

    def replace_link(match: re.Match[str]) -> str:
        name = match.group("name")
        html_target = COURSE_DIR / "assets" / "templates" / f"{name}.html"
        if not html_target.exists():
            raise FileNotFoundError(f"Missing learner HTML asset for {name}.md: {html_target}")
        return (
            f'<a class="asset-action secondary" href="assets/templates/{name}.html" '
            f'download="{name}.html">下載 HTML 工作版</a>'
        )

    updated, count = LINK_RE.subn(replace_link, original)
    note_added = False
    if count and 'class="asset-note"' not in updated:
        marker = '<div class="asset-bundle">'
        if marker not in updated:
            raise ValueError(f"Asset bundle marker missing: {path}")
        updated = updated.replace(marker, marker + ASSET_NOTE, 1)
        note_added = True

    return updated, count, note_added


def main() -> None:
    total_links = 0
    changed_pages = 0
    for path in sorted(COURSE_DIR.glob("*.html")):
        updated, count, note_added = normalize_page(path)
        if count or note_added:
            path.write_text(updated, encoding="utf-8")
            changed_pages += 1
            total_links += count

    print(f"changed learner pages: {changed_pages}")
    print(f"normalized Markdown links: {total_links}")


if __name__ == "__main__":
    main()
