#!/usr/bin/env python3
r"""check-integrity.py — 課程系統跨檔一致性檢查

偵測「三處 slug 不一致」與「outline / 課程資料夾 / index.html 缺漏」。

三處 slug 來源：
  A. courses/ 底下的資料夾
  B. COURSES.md 的現有課程表（| `{slug}/` |）
  C. inject_gate.py 的 COURSES dict keys

規則：
  1. A ∩ B ∩ C 應一致；差集 = ERROR
  2. A 中每個 slug 都該有 courses/<slug>/index.html = WARN if missing
  3. A 中每個 slug 都該有 _outlines/<slug>.md = WARN if missing
  4. _outlines/ 中每個非底線前綴的 .md 都該對應 A 的某個 slug = WARN

使用：
  python3 docs/check-integrity.py            # 人類可讀報告
  python3 docs/check-integrity.py --strict   # 任一 WARN/ERROR 都 exit 1

Exit：0 = 全通過；1 = 有 ERROR（或 --strict 下有 WARN）
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def slugs_from_courses_dir() -> set:
    d = ROOT / "courses"
    if not d.exists():
        return set()
    return {p.name for p in d.iterdir() if p.is_dir() and not p.name.startswith(".")}


COMMON_WORDS = {"courses", "slug"}  # 散文中提到的代稱，不算


def slugs_from_courses_md() -> set:
    md = ROOT / "COURSES.md"
    if not md.exists():
        return set()
    text = md.read_text(encoding="utf-8", errors="ignore")
    found = set()
    # 只吃表格 row：以 `|` 開頭、首欄是 backtick-slug/
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        m = re.search(r'`([a-z0-9][a-z0-9\-]*)/`', line)
        if m and m.group(1) not in COMMON_WORDS:
            found.add(m.group(1))
    return found


def slugs_from_inject_gate() -> set:
    py = ROOT / "inject_gate.py"
    if not py.exists():
        return set()
    text = py.read_text(encoding="utf-8", errors="ignore")
    # 抓 COURSES dict 內 "slug":
    m = re.search(r'COURSES\s*=\s*\{(.*?)\n\}', text, re.DOTALL)
    if not m:
        return set()
    return set(re.findall(r'"([a-z0-9][a-z0-9\-]*)"\s*:', m.group(1)))


def outlines_present() -> set:
    d = ROOT / "_outlines"
    if not d.exists():
        return set()
    # 只吃單層 stem（無 `.` 中綴，例如略過 `prompt-basic.style-guide.md`）
    return {p.stem for p in d.glob("*.md")
            if not p.stem.startswith("_") and "." not in p.stem}


def report(problems: list) -> int:
    errors = sum(1 for level, _ in problems if level == "ERROR")
    warns = sum(1 for level, _ in problems if level == "WARN")

    for level, msg in problems:
        icon = "❌" if level == "ERROR" else "⚠"
        print(f"  {icon} [{level}] {msg}")
    print(f"\n═══ 摘要 ═══")
    print(f"ERROR：{errors} · WARN：{warns}")
    return errors, warns


def main():
    ap = argparse.ArgumentParser(description="課程系統跨檔一致性檢查")
    ap.add_argument("--strict", action="store_true", help="有 WARN 也 exit 1")
    args = ap.parse_args()

    dir_slugs = slugs_from_courses_dir()
    md_slugs = slugs_from_courses_md()
    gate_slugs = slugs_from_inject_gate()
    outline_slugs = outlines_present()

    print(f"📁 courses/                {len(dir_slugs)} 個")
    print(f"📄 COURSES.md               {len(md_slugs)} 個")
    print(f"🔐 inject_gate.py COURSES   {len(gate_slugs)} 個")
    print(f"📋 _outlines/               {len(outline_slugs)} 個\n")

    problems = []

    # 1. 三處交集檢查
    # courses/ 有、COURSES.md 沒 → ERROR
    for s in sorted(dir_slugs - md_slugs):
        problems.append(("ERROR", f"courses/{s}/ 存在但未登錄於 COURSES.md"))
    # courses/ 有、inject_gate.py 沒 → ERROR
    for s in sorted(dir_slugs - gate_slugs):
        problems.append(("ERROR", f"courses/{s}/ 存在但未登錄於 inject_gate.py COURSES"))
    # inject_gate.py 有、courses/ 沒 → ERROR
    for s in sorted(gate_slugs - dir_slugs):
        problems.append(("ERROR", f"inject_gate.py 登錄了 {s} 但 courses/{s}/ 不存在"))
    # COURSES.md 有、courses/ 沒 → WARN（可能是預留位置）
    for s in sorted(md_slugs - dir_slugs):
        problems.append(("WARN", f"COURSES.md 有 {s} 但 courses/{s}/ 不存在（預留位置？）"))

    # 2. index.html 存在
    for s in sorted(dir_slugs):
        idx = ROOT / "courses" / s / "index.html"
        if not idx.exists():
            problems.append(("WARN", f"courses/{s}/index.html 不存在"))

    # 3. outline 存在
    for s in sorted(dir_slugs):
        ol = ROOT / "_outlines" / f"{s}.md"
        if not ol.exists():
            problems.append(("WARN", f"_outlines/{s}.md 不存在"))

    # 4. outline 對應資料夾
    for s in sorted(outline_slugs - dir_slugs):
        problems.append(("WARN", f"_outlines/{s}.md 存在但 courses/{s}/ 不存在"))

    if not problems:
        print("✅ 全部一致")
        sys.exit(0)

    errors, warns = report(problems)

    if errors or (args.strict and warns):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
