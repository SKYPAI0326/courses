#!/usr/bin/env python3
"""Learner-facing entry smoke test for the UI/UX course.

This catches two failures that ordinary link scans miss:
1. a learner page points to an internal production document;
2. a core start material appears after the first requested action.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "part2/CH6-prototype-task-test.html",
    "part2/CH7-figma-handoff-export.html",
    "part3/CH8-web-git-deploy.html",
}
INTERNAL_MARKERS = ("_design/", "_backup/", "_repair/")


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.href: str | None = None
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.href = dict(attrs).get("href")
            self.text = []

    def handle_data(self, data: str) -> None:
        if self.href is not None:
            self.text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.href:
            self.links.append((self.href, " ".join("".join(self.text).split())))
            self.href = None


def learner_pages() -> list[str]:
    index = (ROOT / "index.html").read_text()
    seen: list[str] = []
    for href in re.findall(r'href="([^"]+\.html)"', index):
        if href.startswith("part") and href not in seen:
            seen.append(href)
    return seen


def main() -> int:
    failures: list[str] = []
    pages = learner_pages()
    if len(pages) != 16:
        failures.append(f"expected 16 learner pages, found {len(pages)}")

    for rel in pages:
        page = ROOT / rel
        source = page.read_text()
        parser = LinkParser()
        parser.feed(source)

        for href, label in parser.links:
            parsed = urlparse(href)
            if parsed.scheme or href.startswith("#"):
                continue
            if any(marker in href for marker in INTERNAL_MARKERS) or href.endswith(".md"):
                failures.append(f"{rel}: internal learner link {label!r} -> {href}")

            target = (page.parent / parsed.path).resolve()
            if parsed.path and not target.exists():
                failures.append(f"{rel}: missing target {href}")

        if rel in REQUIRED:
            action = re.search(r"<th>第一步</th><td", source)
            if action is None:
                failures.append(f"{rel}: missing first-action marker")
            else:
                before_action = source[: action.start()]
                material = re.search(r'href="(?:\.\./)?(?:assets|web-starter)/', before_action)
                if material is None:
                    failures.append(f"{rel}: no start material link before first action")

    if failures:
        print("LEARNER_ENTRY_SMOKE: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"LEARNER_ENTRY_SMOKE: PASS ({len(pages)} learner pages; required first-use checks: {len(REQUIRED)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
