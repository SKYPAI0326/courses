#!/usr/bin/env python3
"""Find high-risk continuity breaks in course Markdown or learner HTML.

This is a warning-oriented heuristic. It cannot judge prose quality; every
warning still needs a human decision.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+)" )
LIST_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
LABEL_RE = re.compile(r"^\s*[^。！？：:]{1,28}[：:]\s*$")
CAUSAL_RE = re.compile(r"因此|所以|這代表|完成後|回到|因為|才能|接著|換句話說|也就是")


def visible_lines(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".html", ".htm"}:
        raw = re.sub(r"<!--.*?-->", "\n", raw, flags=re.S)
        raw = re.sub(r"<(script|style)\b.*?</\1\s*>", "\n", raw, flags=re.I | re.S)
        # Flow diagrams are deliberate worked artifacts; surrounding prose is
        # what needs a continuity check, not the diagram's visual arrows.
        raw = re.sub(r"<pre\b.*?</pre\s*>", "\n", raw, flags=re.I | re.S)
        raw = re.sub(r"</?(?:h[1-6]|p|div|section|article|li|tr|pre|blockquote|br)\b[^>]*>", "\n", raw, flags=re.I)
        raw = re.sub(r"<[^>]+>", " ", raw)
        raw = html.unescape(raw)
    return [line.rstrip() for line in raw.splitlines()]


def next_content(lines: list[str], index: int) -> tuple[int | None, str]:
    for pos in range(index + 1, len(lines)):
        stripped = lines[pos].strip()
        if stripped:
            return pos, stripped
    return None, ""


def audit(path: Path) -> list[tuple[str, int, str]]:
    lines = visible_lines(path)
    warnings: list[tuple[str, int, str]] = []

    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()
            pos, following = next_content(lines, index)
            structured_heading = re.match(r"(?:步驟|Checkpoint|檢核|完成前|正例|錯例|反例|原始|不需|若使用|概念|講師|常見錯誤|試跑包|動手練習|商業情境)", heading_text, re.I)
            if level <= 3 and not structured_heading and pos is not None and (LIST_RE.match(following) or TABLE_RE.match(following) or following.startswith("```")):
                warnings.append(("C1", pos + 1, "標題後直接進入清單、表格或程式碼，缺少目的／情境句"))

        arrow_count = len(re.findall(r"[→➜>]", stripped))
        prose_punctuation = re.search(r"[。！？；，：:「」\"|]", stripped)
        if arrow_count >= 2 and not prose_punctuation and len(stripped) <= 100:
            warnings.append(("C2", index + 1, "出現工具或步驟箭頭鏈，請補上資料、理由與結果"))

    label_run = 0
    label_start = 0
    for index, line in enumerate(lines):
        if LABEL_RE.match(line) and not line.strip().startswith("http"):
            if label_run == 0:
                label_start = index
            label_run += 1
            if label_run == 3:
                warnings.append(("C3", label_start + 1, "連續三個以上標籤式片語，可能形成表單堆疊"))
        else:
            label_run = 0

    cue_count = sum(1 for line in lines if re.search(r"接下來|最後", line))
    causal_count = sum(1 for line in lines if CAUSAL_RE.search(line))
    if cue_count >= 6 and cue_count > causal_count * 2:
        warnings.append(("C4", 1, "時間提示多於因果承接，請確認段落不是只靠『接下來／最後』串接"))

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    if not args.path.is_file():
        parser.error(f"file not found: {args.path}")

    warnings = audit(args.path)
    print(f"Copy continuity audit: {args.path}")
    for code, line, message in warnings:
        print(f"WARN {code} line {line}: {message}")
    print(f"Summary: {len(warnings)} warning(s); human review required")
    return 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
