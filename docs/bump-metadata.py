#!/usr/bin/env python3
"""bump-metadata.py — 批次升級 HTML footer metadata（data-built-at / data-platform-version）

場景：course-refresh 產出 Refresh Report 後，對已通過人工審閱的頁面批次更新 built-at（重新計時），
或在平台實際升版後批次更新 platform-version。

使用：
  python3 docs/bump-metadata.py courses/<slug>/                       # 整課升 built-at 為今天
  python3 docs/bump-metadata.py courses/<slug>/CH1-1.html              # 單頁
  python3 docs/bump-metadata.py courses/<slug>/ --platform-version "n8n v1.62"  # 同時升平台版
  python3 docs/bump-metadata.py courses/<slug>/ --dry-run              # 只印變更、不寫檔

規則：
  - 只改既有 metadata 欄位的值，不新增欄位（新增請去改 lesson-template.html）
  - 缺 metadata 的頁會 WARN，不當失敗
  - 預設 --built-at 為今天

Exit code：
  0 = 成功（即使 0 檔變更）
  1 = 有 I/O 或寫入錯誤
  2 = 使用錯誤
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def update_file(path: Path, new_version: str | None, new_built_at: str, dry_run: bool):
    """回傳 (changed: bool, messages: list[str])"""
    try:
        html = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return False, [f"❌ 讀檔失敗：{e}"]

    changes = []
    new_html = html

    m = re.search(r'data-built-at="([^"]*)"', new_html)
    if m:
        old = m.group(1)
        if old != new_built_at:
            new_html = re.sub(
                r'data-built-at="[^"]*"', f'data-built-at="{new_built_at}"', new_html
            )
            changes.append(f"built-at: {old} → {new_built_at}")
    else:
        changes.append("⚠ 無 data-built-at 欄位（跳過；到 lesson-template.html 加）")

    if new_version is not None:
        m = re.search(r'data-platform-version="([^"]*)"', new_html)
        if m:
            old = m.group(1)
            if old != new_version:
                new_html = re.sub(
                    r'data-platform-version="[^"]*"',
                    f'data-platform-version="{new_version}"',
                    new_html,
                )
                changes.append(f"platform-version: {old} → {new_version}")
        else:
            changes.append("⚠ 無 data-platform-version 欄位（跳過）")

    actually_changed = new_html != html
    if actually_changed and not dry_run:
        try:
            path.write_text(new_html, encoding="utf-8")
        except OSError as e:
            return False, [f"❌ 寫檔失敗：{e}"]

    return actually_changed, changes


def collect(paths):
    files = []
    for p in paths:
        path = Path(p)
        if not path.is_absolute():
            path = ROOT / p
        if path.is_dir():
            files.extend(path.rglob("*.html"))
        elif path.is_file():
            files.append(path)
        else:
            print(f"⚠ 路徑不存在：{p}", file=sys.stderr)
    return [
        f for f in files
        if not any(part.startswith("_backup") for part in f.parts)
        and ".git" not in f.parts
        and "node_modules" not in f.parts
    ]


def main():
    ap = argparse.ArgumentParser(
        description="批次升級 HTML footer metadata（built-at / platform-version）"
    )
    ap.add_argument("paths", nargs="+", help="檔案或目錄路徑")
    ap.add_argument(
        "--platform-version",
        help="新的 platform version 值（例 'n8n v1.62'）；不給則只升 built-at",
    )
    ap.add_argument(
        "--built-at",
        default=date.today().isoformat(),
        help="新的 built-at（YYYY-MM-DD，預設今天）",
    )
    ap.add_argument("--dry-run", action="store_true", help="只印變更、不寫檔")
    args = ap.parse_args()

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", args.built_at):
        print(f"❌ --built-at 格式錯誤，需 YYYY-MM-DD：{args.built_at}", file=sys.stderr)
        sys.exit(2)

    files = collect(args.paths)
    if not files:
        print("無目標 HTML")
        sys.exit(0)

    changed = 0
    warned = 0
    io_errors = 0
    for f in sorted(files):
        updated, msgs = update_file(f, args.platform_version, args.built_at, args.dry_run)
        if msgs:
            rel = f.relative_to(ROOT).as_posix() if f.is_absolute() else str(f)
            print(f"\n📄 {rel}")
            for m in msgs:
                print(f"  · {m}")
                if m.startswith("❌"):
                    io_errors += 1
                elif m.startswith("⚠"):
                    warned += 1
            if updated:
                changed += 1

    verb = "將變動" if args.dry_run else "已變動"
    print("\n═══ 摘要 ═══")
    print(f"掃描：{len(files)} 檔")
    print(f"{verb}：{changed} 檔")
    if warned:
        print(f"WARN：{warned} 條（缺 metadata 欄位）")
    if io_errors:
        print(f"❌ I/O 錯誤：{io_errors} 條")
    if args.dry_run:
        print("（--dry-run 未寫檔，要實際執行把此旗標拿掉）")

    sys.exit(1 if io_errors else 0)


if __name__ == "__main__":
    main()
