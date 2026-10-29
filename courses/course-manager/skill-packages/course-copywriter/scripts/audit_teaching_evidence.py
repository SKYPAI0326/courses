#!/usr/bin/env python3
"""Check learner copy for objective, artifact, and branch evidence gaps.

The checker is intentionally explicit: callers provide the fields, artifacts,
and branch terms that define the current lesson's learning contract.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


def plain_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<!--.*?-->", "\n", raw, flags=re.S)
    raw = re.sub(r"<(script|style)\b.*?</\1\s*>", "\n", raw, flags=re.I | re.S)
    raw = re.sub(r"<[^>]+>", "\n", raw)
    return html.unescape(raw)


def section(text: str, starts: tuple[str, ...], ends: tuple[str, ...]) -> str:
    start = min((text.find(marker) for marker in starts if text.find(marker) >= 0), default=0)
    tail = text[start:]
    end_positions = [tail.find(marker) for marker in ends if tail.find(marker) >= 0]
    return tail[: min(end_positions)] if end_positions else tail


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--field", action="append", default=[])
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--branch", action="append", default=[])
    parser.add_argument("--canonical-field", action="append", default=[], help="欄位必須在示範區形成完整產物規格")
    parser.add_argument("--failure-response", type=int, default=0, help="示範區至少要有幾個含失敗處理動詞的模組列")
    parser.add_argument("--terminal", action="append", default=[], help="必須出現在分流或驗證中的終態／回路詞")
    parser.add_argument("--contract-note", action="append", default=[], help="來源替換必須明示的契約說明詞")
    args = parser.parse_args()
    if not args.path.is_file():
        parser.error(f"file not found: {args.path}")

    text = plain_text(args.path)
    demo = section(text, ("操作示範", "示範：", "Demo"), ("動手", "跟著做", "Hands-on", "Solo"))
    verify = section(text, ("檢核", "驗證", "完成驗證", "Verification"), ("試跑包", "下一節預告"))
    findings: list[str] = []

    for field in args.field:
        if field not in text:
            findings.append(f"BLOCKER E1: 核心欄位『{field}』完全未出現")
        elif field not in demo:
            findings.append(f"BLOCKER E2: 核心欄位『{field}』未在示範區出現完整證據")
        if field not in verify:
            findings.append(f"MAJOR E3: 核心欄位『{field}』未在驗證區被明確驗收")

    for artifact in args.artifact:
        count = len(re.findall(re.escape(artifact), text))
        if count < 2:
            findings.append(f"MAJOR E4: 產物『{artifact}』只出現 {count} 次，未形成可追蹤規格")

    if args.artifact and re.search(r"一(?:張|份)\s*(?:工作流地圖|地圖|版本|產物|完成物)", text) and len(args.artifact) > 1:
        findings.append("MINOR E5: 文字同時出現單一產物描述與多版本產物，請統一交付數量")

    if args.canonical_field:
        missing = [field for field in args.canonical_field if field not in demo]
        if missing:
            findings.append(f"BLOCKER E9: 完整示範缺少 canonical 欄位：{'、'.join(missing)}")
        elif not _has_canonical_header(args.path, args.canonical_field, demo):
            findings.append("BLOCKER E10: 示範區雖提到所有欄位，但沒有同一份完整 canonical 產物表")

    if args.failure_response:
        response_segments = re.findall(r"[^\n。；]+(?:負責人|流程負責人|人工負責人)[^\n。；]*(?:停止|重試|記錄|標記)[^\n。；]*", demo)
        if len(response_segments) < args.failure_response:
            findings.append(f"MAJOR E11: 示範區只有 {len(response_segments)} 個模組列具體寫出負責人與停止／記錄／重試，要求 {args.failure_response} 個")

    for terminal in args.terminal:
        if terminal not in text:
            findings.append(f"MAJOR E12: 分流終態／回路『{terminal}』未出現")

    for note in args.contract_note:
        if note not in text:
            findings.append(f"MAJOR E13: 來源替換契約未明示『{note}』")

    for branch in args.branch:
        if branch not in text:
            findings.append(f"MAJOR E6: 分流欄位『{branch}』未出現")
            continue
        has_states = re.search(r"true", text, re.I) and re.search(r"false", text, re.I)
        has_exit = re.search(r"人工確認|負責人|佇列|出口|停在|交給|停止|下一步", text)
        if not has_states:
            findings.append(f"MAJOR E7: 分流『{branch}』沒有同時說明 true／false 狀態")
        if not has_exit:
            findings.append(f"MAJOR E8: 分流『{branch}』沒有去向、負責人或停止狀態")

    print(f"Teaching evidence audit: {args.path}")
    for finding in findings:
        print(finding)
    print(f"Summary: {len(findings)} finding(s)")
    return 1 if any(item.startswith(("BLOCKER", "MAJOR")) for item in findings) else 0


def _has_canonical_header(path: Path, fields: list[str], demo: str) -> bool:
    """Require one artifact header, not merely scattered field mentions."""
    if path.suffix.lower() in {".html", ".htm"}:
        raw = path.read_text(encoding="utf-8")
        raw_demo = section(raw, ("操作示範", "示範：", "Demo"), ("動手", "跟著做", "Hands-on", "Solo"))
        headers = re.findall(r"<th\b[^>]*>(.*?)</th>", raw_demo, flags=re.I | re.S)
        clean = [html.unescape(re.sub(r"<[^>]+>", "", h)).strip() for h in headers]
        return all(any(field == header or field in header for header in clean) for field in fields)
    for line in demo.splitlines():
        if line.lstrip().startswith("|") and all(field in line for field in fields):
            return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())
