#!/usr/bin/env python3
"""build-all.py — 課程網頁總建置器

在 git push 前跑：
  1. lint-page.py --all --baseline --no-warn       （BLOCKER 擋）
  2. build-search-index.py                          （重建搜尋索引）
  3. build-sitemap.py                               （重建 sitemap）

任一步失敗就離開非 0。供 pre-push hook 呼叫。

使用：
  python3 docs/build-all.py                 # 全跑
  python3 docs/build-all.py --lint-only     # 只跑 lint
  python3 docs/build-all.py --skip-lint     # 跳過 lint（緊急時）

Exit code：
  0 = 全通過
  1 = 任一步失敗
  2 = 使用錯誤
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEPS = [
    ("lint",   ["python3", "docs/lint-page.py", "--all", "--baseline", "--no-warn"]),
    ("search", ["python3", "docs/build-search-index.py"]),
    ("sitemap", ["python3", "docs/build-sitemap.py"]),
]


def run_step(name: str, cmd: list) -> int:
    print(f"\n▶ [{name}] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"✖ [{name}] 失敗 (exit {result.returncode})")
    return result.returncode


def main():
    ap = argparse.ArgumentParser(description="課程網頁總建置器（lint + search + sitemap）")
    ap.add_argument("--lint-only", action="store_true", help="只跑 lint")
    ap.add_argument("--skip-lint", action="store_true", help="跳過 lint（緊急用）")
    args = ap.parse_args()

    if args.lint_only and args.skip_lint:
        print("✖ --lint-only 與 --skip-lint 互斥", file=sys.stderr)
        sys.exit(2)

    steps = STEPS
    if args.lint_only:
        steps = [s for s in STEPS if s[0] == "lint"]
    if args.skip_lint:
        steps = [s for s in STEPS if s[0] != "lint"]

    for name, cmd in steps:
        rc = run_step(name, cmd)
        if rc != 0:
            print(f"\n═══ 失敗：{name} 步驟 exit {rc}")
            sys.exit(1)

    print("\n═══ ✅ 全部通過")
    sys.exit(0)


if __name__ == "__main__":
    main()
