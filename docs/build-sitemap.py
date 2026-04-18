#!/usr/bin/env python3
"""
build-sitemap.py — 弄一下工作室課程站地圖產生器
-----------------------------------------------------------
掃描 courses/**/*.html + 站根首頁，產出 sitemap.xml。
每次新增/修改頁面後必須重跑；或由 course-ops sitemap 子命令呼叫。

使用：
  cd "課程專用網頁"
  python3 docs/build-sitemap.py

輸出：
  sitemap.xml（站根目錄）
"""
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COURSES_DIR = ROOT / "courses"
OUT = ROOT / "sitemap.xml"
BASE_URL = "https://skypai0326.github.io/courses"

# 頁型 → 優先度對照（GitHub Pages 搜尋權重參考）
PRIORITY = {
    "root": "1.0",       # 站首頁
    "index": "0.9",      # 課程首頁
    "module": "0.8",     # 模組總覽
    "lesson": "0.7",     # 單元頁（CH/m）
    "prac": "0.7",       # 練習頁
    "page": "0.5",       # 其他
}

# 忽略的路徑（_backup/ 之類）
IGNORE_PARTS = {"_backup", "_pilots", ".git", "node_modules"}


def classify(path: Path) -> str:
    name = path.name.lower()
    if name == "index.html":
        return "root" if path.parent == ROOT else "index"
    if name.startswith("module"):
        return "module"
    if name.startswith("prac"):
        return "prac"
    if name.startswith("ch") or re.match(r"^m\d", name):
        return "lesson"
    return "page"


def file_lastmod(path: Path) -> str:
    """取檔案 mtime 轉 YYYY-MM-DD。"""
    import os
    ts = os.path.getmtime(path)
    return date.fromtimestamp(ts).isoformat()


def should_ignore(path: Path) -> bool:
    return any(part.startswith("_backup") or part in IGNORE_PARTS for part in path.parts)


def collect_pages():
    """回傳 [(relative_url, lastmod, priority), ...]。"""
    entries = []

    # 站根首頁
    root_index = ROOT / "index.html"
    if root_index.exists():
        entries.append(("", file_lastmod(root_index), PRIORITY["root"]))

    # 課程頁面（遞迴掃）
    if COURSES_DIR.exists():
        for html in sorted(COURSES_DIR.rglob("*.html")):
            if should_ignore(html):
                continue
            rel = html.relative_to(ROOT).as_posix()
            kind = classify(html)
            entries.append((rel, file_lastmod(html), PRIORITY.get(kind, "0.5")))

    return entries


def build_xml(entries):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel, lastmod, priority in entries:
        loc = f"{BASE_URL}/{rel}" if rel else f"{BASE_URL}/"
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    entries = collect_pages()
    xml = build_xml(entries)
    OUT.write_text(xml, encoding="utf-8")
    print(f"✓ 已寫入 sitemap.xml（{len(entries)} 筆 URL）")


if __name__ == "__main__":
    main()
