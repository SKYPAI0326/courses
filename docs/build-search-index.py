#!/usr/bin/env python3
"""
build-search-index.py — 弄一下工作室課程站內搜尋索引產生器
-----------------------------------------------------------
掃描 courses/**/*.html，抽出 <title> 與 meta description，輸出 search-index.json。
前端 search.html 用純 JS 做字元級子字串過濾（CJK 友善，不依賴 Lunr/Fuse）。

使用：
  cd "課程專用網頁"
  python3 docs/build-search-index.py

輸出：
  search-index.json（站根目錄）
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COURSES_DIR = ROOT / "courses"
OUT = ROOT / "search-index.json"

# 課程 slug → 顯示名稱（從 COURSES.md 同步；若新課程記得補這張表）
COURSE_LABEL = {
    "ai-workshop": "AI 實務全攻略",
    "ccs-foundations": "CCS 基礎",
    "digital-marketing-70h": "數位行銷 70h",
    "gemini-ai": "Gemini AI",
    "gen-ai-140h": "生成式 AI 140h",
    "gen-ai-36h": "生成式 AI 36h",
    "gtm": "Google Tag Manager",
    "n8n": "n8n 自動化",
    "ntub-seo-ga4": "SEO × GA4",
    "office-ai": "Office AI",
    "prompt-basic": "AI 交辦方法（6h）",
}

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
DESC_RE = re.compile(
    r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
    re.IGNORECASE | re.DOTALL,
)


def classify(path: Path) -> str:
    """依檔名判斷頁型。"""
    name = path.name.lower()
    if name == "index.html":
        return "index" if path.parent != ROOT else "root"
    if name.startswith("module"):
        return "module"
    if name.startswith("prac"):
        return "prac"
    if name.startswith("ch") or re.match(r"^m\d", name):
        return "lesson"
    return "page"


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def extract(path: Path):
    html = read_text(path)
    if not html:
        return None
    title = ""
    desc = ""
    m = TITLE_RE.search(html)
    if m:
        title = re.sub(r"\s+", " ", m.group(1)).strip()
    m = DESC_RE.search(html)
    if m:
        desc = re.sub(r"\s+", " ", m.group(1)).strip()
    return title, desc


def main():
    entries = []
    # 根 index.html
    root_index = ROOT / "index.html"
    if root_index.exists():
        ex = extract(root_index)
        if ex:
            t, d = ex
            entries.append({
                "url": "index.html",
                "title": t or "弄一下工作室",
                "desc": d,
                "course": "",
                "course_label": "站內首頁",
                "type": "root",
            })

    for course_dir in sorted(COURSES_DIR.iterdir()):
        if not course_dir.is_dir():
            continue
        slug = course_dir.name
        label = COURSE_LABEL.get(slug, slug)
        for html in sorted(course_dir.rglob("*.html")):
            rel = html.relative_to(ROOT).as_posix()
            ex = extract(html)
            if not ex:
                continue
            t, d = ex
            entries.append({
                "url": rel,
                "title": t,
                "desc": d,
                "course": slug,
                "course_label": label,
                "type": classify(html),
            })

    OUT.write_text(
        json.dumps(entries, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"✓ 已寫入 {OUT.relative_to(ROOT)}（{len(entries)} 筆）")


if __name__ == "__main__":
    main()
