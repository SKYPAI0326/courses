#!/usr/bin/env python3
"""ACP-AE learner handout contract checks."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]

LESSONS = [
    "CH1-1", "CH1-2", "CH1-3", "CH1-4", "CH1-5", "PRAC1",
    "CH2-1", "CH3-1", "CH3-2", "CH3-3",
]
HTML_FILES = [
    ROOT / "index.html", ROOT / "module1.html", ROOT / "module2.html", ROOT / "module3.html",
    *(ROOT / "part1" / f"{name}.html" for name in LESSONS[:6]),
    ROOT / "part2" / "CH2-1.html",
    *(ROOT / "part3" / f"{name}.html" for name in LESSONS[7:]),
]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []

    lesson_root = REPO / "_lessons" / "acp-ae"
    for name in LESSONS:
        path = lesson_root / f"{name}.md"
        require(path.is_file(), f"missing formal lesson: {path}", failures)
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            require("<!-- learner-content:start -->" in text, f"missing learner-content start: {path}", failures)
            require("<!-- learner-content:end -->" in text, f"missing learner-content end: {path}", failures)
            for anchor in ("第一個動作", "成功訊號", "完成檢查", "修復"):
                require(anchor in text, f"missing {anchor}: {path}", failures)

    for path in HTML_FILES:
        require(path.is_file(), f"missing HTML: {path}", failures)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        require('<main id="main"' in text, f"missing main#main: {path}", failures)
        require('class="lesson-body"' in text or path.name.startswith("module") or path.name == "index.html", f"missing lesson-body: {path}", failures)
        require('<meta name="description"' in text, f"missing description: {path}", failures)
        require('rel="canonical"' in text, f"missing canonical: {path}", failures)
        require('data-platform-version=' in text, f"missing platform metadata: {path}", failures)
        require('data-built-at="2026-10-16"' in text, f"missing build date: {path}", failures)
        unresolved = re.search(r"\{\{\s*[A-Za-z_][^{}]*\}\}|\b(?:TODO|TBD)\b", text)
        require(unresolved is None, f"unresolved placeholder: {path}", failures)
        require("您" not in text, f"formal second-person violation: {path}", failures)
        require("講師示範" not in text, f"audience firewall violation: {path}", failures)

        parser = LinkParser()
        parser.feed(text)
        for href in parser.links:
            if href.startswith(("http://", "https://", "mailto:", "#", "javascript:")):
                continue
            target = (path.parent / href.split("#", 1)[0].split("?", 1)[0]).resolve()
            require(target.exists(), f"broken link: {path} -> {href}", failures)

    task_pages = [ROOT / "part3" / f"CH3-{n}.html" for n in (1, 2, 3)]
    task_card_count = sum(
        path.read_text(encoding="utf-8").count('data-question-card="')
        for path in task_pages if path.is_file()
    )
    require(task_card_count == 40, f"operation cards: expected 40, got {task_card_count}", failures)

    concept_path = ROOT / "part2" / "CH2-1.html"
    concept_count = concept_path.read_text(encoding="utf-8").count('data-concept-question="') if concept_path.is_file() else 0
    require(concept_count == 13, f"concept questions: expected 13, got {concept_count}", failures)

    representative_count = sum(
        len(re.findall(r'data-practice="representative"', path.read_text(encoding="utf-8")))
        for path in task_pages if path.is_file()
    )
    require(representative_count == 9, f"representative practices: expected 9, got {representative_count}", failures)

    for rel in (
        "assets/downloads/acp-ae-task-cards.md",
        "assets/downloads/acp-ae-evidence-checklist.md",
        "assets/handout.css",
        "assets/handout.js",
    ):
        require((ROOT / rel).is_file(), f"missing shared asset: {rel}", failures)

    if failures:
        print("ACP-AE handout validation failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print(f"ACP-AE handout validation passed: {len(LESSONS)} lessons, {len(HTML_FILES)} HTML files, 40 operation cards, 13 concept questions, 9 representative practices.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
