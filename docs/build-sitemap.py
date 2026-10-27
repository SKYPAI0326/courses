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
import subprocess
from datetime import date
from pathlib import Path
from course_paths import clean_git_environment, is_public_html, iter_public_html

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

_GIT_LASTMOD_BY_PATH = None

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


def git_lastmod_by_path() -> dict:
    """Return the newest commit date for each published source path."""
    global _GIT_LASTMOD_BY_PATH
    if _GIT_LASTMOD_BY_PATH is not None:
        return _GIT_LASTMOD_BY_PATH

    dates = {}
    try:
        result = subprocess.run(
            ["git", "-c", "core.quotepath=false", "log", "--no-renames",
             "--format=@@DATE@@%cs", "--name-only", "--", "index.html", "courses"],
            cwd=ROOT, capture_output=True, text=True, check=True,
            env=clean_git_environment(),
        )
        current_date = None
        for line in result.stdout.splitlines():
            if line.startswith("@@DATE@@"):
                current_date = line.removeprefix("@@DATE@@")
            elif line and current_date and line not in dates:
                dates[line] = current_date
    except (OSError, subprocess.CalledProcessError):
        pass

    _GIT_LASTMOD_BY_PATH = dates
    return dates


def file_lastmod(path: Path) -> str:
    """Use the Git commit date; fall back to mtime for a new untracked page."""
    import os
    try:
        relative = path.resolve().relative_to(ROOT.resolve()).as_posix()
        committed = git_lastmod_by_path().get(relative)
        if committed:
            return committed
    except ValueError:
        pass
    ts = os.path.getmtime(path)
    return date.fromtimestamp(ts).isoformat()


def should_ignore(path: Path) -> bool:
    return not is_public_html(path, ROOT)


def is_gated(path: Path) -> bool:
    """偵測頁面是否有密碼關卡（#_gate）。密碼頁 Google 不會也不該收錄，排除出 sitemap。"""
    try:
        return 'id="_gate"' in path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False


def collect_pages():
    """回傳 [(relative_url, lastmod, priority), ...]。"""
    entries = []

    # 站根首頁
    root_index = ROOT / "index.html"
    if root_index.exists():
        entries.append(("", file_lastmod(root_index), PRIORITY["root"]))

    # 課程頁面（遞迴掃）
    if COURSES_DIR.exists():
        for html in sorted(iter_public_html(COURSES_DIR, ROOT)):
            if should_ignore(html):
                continue
            if is_gated(html):
                continue
            # The Pages project base is `/courses`; keep the repository's
            # `courses/` directory in the suffix so links resolve to the files.
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
