#!/usr/bin/env python3
"""Scan learner-facing course copy for recurring template signals.

The scanner separates BLOCK patterns (rewrite before release) from REVIEW
patterns (a human checks context, evidence, and sentence rhythm).  It is not
an authorship detector or a grammar judge.  Use ``--strict`` to fail only on
BLOCK findings; REVIEW findings remain visible for the cold-read gate.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RiskPattern:
    code: str
    severity: str
    expression: re.Pattern[str]


RISK_PATTERNS: tuple[RiskPattern, ...] = (
    # These patterns repeatedly force an abstract contrast onto the reader.
    RiskPattern("contrast-not-but", "BLOCK", re.compile(r"不是[^。；\n]{0,100}而是")),
    RiskPattern("contrast-not-rather", "BLOCK", re.compile(r"不在於[^。；\n]{0,100}而在於")),
    RiskPattern("contrast-only-but", "BLOCK", re.compile(r"不只是[^。；\n]{0,100}(?:而是|也|還)")),
    # The following signals require context.  A product label, an explicit
    # constraint, or nearby evidence may make the wording valid.
    RiskPattern("transition-filler", "REVIEW", re.compile(r"值得注意的是|需要(?:特別)?強調的是|接下來我們將|總而言之|綜合來看")),
    RiskPattern("mechanical-order", "REVIEW", re.compile(r"首先|其次|最後")),
    RiskPattern("rhetorical-question", "REVIEW", re.compile(r"你是否曾經想過|那麼問題來了|你可能會問")),
    RiskPattern("hedging", "REVIEW", re.compile(r"可能可以|或許能夠|不妨考慮看看|在某些情況下可能有助於")),
    RiskPattern("vague-authority", "REVIEW", re.compile(r"研究顯示|專家認為|業界普遍認為|大家都知道")),
    RiskPattern("unsupported-emphasis", "REVIEW", re.compile(r"毫無疑問|絕對關鍵|必然能夠|大幅提升|全面改善")),
    RiskPattern("fake-personalization", "REVIEW", re.compile(r"最適合你的方式取決於|你可以依照自身需求彈性調整|每個人的情況都不一樣")),
    RiskPattern("abstract-promise", "REVIEW", re.compile(r"賦能|創造價值|提升影響力|促進轉型|實現突破|建立閉環")),
    RiskPattern("corporate-jargon", "REVIEW", re.compile(r"整合資源|協同合作|推動落地|打造完整生態系|建立可持續|建立可擴展|可複製的機制")),
    RiskPattern("promotional-adjective", "REVIEW", re.compile(r"全面|深度|完整|無縫|強大|高效|卓越|革命性")),
    RiskPattern("service-response", "REVIEW", re.compile(r"這是一個很好的問題|你指出的非常重要|很高興你提出|希望這些資訊對你有所幫助")),
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
    parser.add_argument("--strict", action="store_true", help="exit 1 when a BLOCK pattern is found")
    args = parser.parse_args()

    findings = 0
    blockers = 0
    reviews = 0
    for path in iter_files(args.paths, DEFAULT_EXTENSIONS):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(lines, 1):
            for risk in RISK_PATTERNS:
                for match in risk.expression.finditer(line):
                    excerpt = match.group(0).strip()
                    print(f"{risk.severity}\t{risk.code}\t{path}:{line_number}\t{excerpt}")
                    findings += 1
                    if risk.severity == "BLOCK":
                        blockers += 1
                    else:
                        reviews += 1
    print(f"Copy pattern audit: {findings} finding(s) ({blockers} BLOCK, {reviews} REVIEW)")
    return 1 if args.strict and blockers else 0


if __name__ == "__main__":
    sys.exit(main())
