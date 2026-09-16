#!/usr/bin/env python3
"""Find recurring AI-style contrast phrases in learner-facing course copy.

This is a review gate, not a grammar judge.  It reports phrases that need a
human rewrite so the sentence states the situation, action, and result
directly.  Use --strict in CI or before course release.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("contrast-not-but", re.compile(r"不是[^。；\n]{0,100}而是")),
    ("contrast-not-rather", re.compile(r"不在於[^。；\n]{0,100}而在於")),
    ("contrast-only-but", re.compile(r"不只是[^。；\n]{0,100}(?:也|還)")),
)
DEFAULT_EXTENSIONS = {".md", ".html", ".htm"}
# Internal design notes may quote the prohibited pattern while documenting the
# rule itself.  The default scan targets learner-facing copy and lesson plans;
# pass those internal files explicitly when reviewing them by hand.
DEFAULT_EXCLUDES = {".git", "_validation", "_backup", "_design", "_review", "_gates.md", "node_modules"}


def iter_files(paths: list[Path], extensions: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file():
            if path.suffix.lower() in extensions:
                files.append(path)
            continue
        if not path.exists():
            continue
        for candidate in path.rglob("*"):
            if not candidate.is_file() or candidate.suffix.lower() not in extensions:
                continue
            if any(part in DEFAULT_EXCLUDES for part in candidate.parts):
                continue
            files.append(candidate)
    return sorted(set(files))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--strict", action="store_true", help="exit 1 when a pattern is found")
    args = parser.parse_args()

    findings = 0
    for path in iter_files(args.paths, DEFAULT_EXTENSIONS):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, 1):
            for label, pattern in PATTERNS:
                for match in pattern.finditer(line):
                    excerpt = match.group(0).strip()
                    print(f"{label}\t{path}:{line_number}\t{excerpt}")
                    findings += 1
    print(f"Copy pattern audit: {findings} finding(s)")
    return 1 if args.strict and findings else 0


if __name__ == "__main__":
    sys.exit(main())
