#!/usr/bin/env python3
"""Verify lesson text outside navigation containers is unchanged."""

from __future__ import annotations

import importlib.util
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "_backup/2026-09-21-pre-navigation"
TOOLS = ROOT / "_tools"
SPEC = importlib.util.spec_from_file_location("normalize_navigation", TOOLS / "normalize-navigation.py")
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool, bool]] = []
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        in_nav = any(item[1] for item in self.stack)
        is_nav = tag in {"div", "nav"} and bool(classes & {"nav-footer", "lesson-nav", "nav-return"})
        hidden = tag in {"script", "style"} or any(item[2] for item in self.stack)
        self.stack.append((tag, in_nav or is_nav, hidden))

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if not any(item[1] for item in self.stack) and not any(item[2] for item in self.stack):
            self.parts.append(data)


def visible_text(path: Path) -> str:
    parser = VisibleTextParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return " ".join("".join(parser.parts).split())


def main() -> int:
    checked = 0
    failures: list[str] = []
    for course_index in sorted(ROOT.glob("*/index.html")):
        course_root = course_index.parent
        for page in MODULE.official_html(course_root):
            relative = page.relative_to(ROOT)
            before = BACKUP / relative
            if not before.exists():
                failures.append(f"missing backup: {relative}")
                continue
            checked += 1
            if visible_text(before) != visible_text(page):
                failures.append(str(relative))

    print(f"checked_pages={checked} text_outside_navigation_differences={len(failures)}")
    for failure in failures[:20]:
        print(f"  {failure}")
    if failures:
        print("FAIL: learner text outside navigation changed")
        return 1
    print("PASS: learner text outside navigation is preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
