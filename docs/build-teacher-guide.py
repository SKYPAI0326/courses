#!/usr/bin/env python3
"""build-teacher-guide.py — 從教案產出「講師手冊」HTML（講師授課用，不對學員公開）。

一教案 → 兩產物的講師端：
  - 學員拿：courses/{slug}/*.html（純學員視角，部署、密碼後）
  - 講師拿：_teacher/{slug}.html（本腳本產出，授課調度全在這）

來源：_lessons/{slug}/*.md 的 frontmatter（unit_id/title/duration/learning_objective）
      + 「## 講師授課筆記（不進講義）」整段。

輸出：_teacher/{slug}.html

⚠️ _teacher/ 不在 courses/ 底下，不屬學員課程站、不進 sitemap/search-index。
   它仍在 repo 內（GitHub Pages 技術上可由 URL 取得但無連結）。需要更強隔離時
   可另設講師密碼 gate（本腳本不處理）。

用法：python3 docs/build-teacher-guide.py {slug}
      python3 docs/build-teacher-guide.py --all
"""
import re
import sys
import html
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LESSONS = BASE / "_lessons"
OUT_DIR = BASE / "_teacher"
NOTE_HEADER = "## 講師授課筆記（不進講義）"


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, _, v = line.partition(":")
                fm[k.strip()] = v.strip()
    return fm


def extract_teacher_notes(text: str) -> str:
    """取真正的 NOTE_HEADER 區段（行首錨定，避免命中設計註解裡的參照字串）
    到下一個行首 '## ' 或檔尾。"""
    m = re.search(r"^## 講師授課筆記（不進講義）[ \t]*$", text, re.MULTILINE)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.MULTILINE)
    body = rest[: nxt.start()] if nxt else rest
    return body.strip()


def unit_sort_key(unit_id: str):
    """CH a-b → (a, b)；PRAC n → (n, 99)（排在該章之後）。"""
    m = re.match(r"CH(\d+)-(\d+)", unit_id)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    m = re.match(r"PRAC(\d+)", unit_id)
    if m:
        return (int(m.group(1)), 99)
    return (999, 999)


def md_to_html(md: str) -> str:
    """極簡 markdown → HTML：**粗體**、`碼`、- 清單、> 引言、空行分段。"""
    md = html.escape(md)
    md = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", md)
    md = re.sub(r"`(.+?)`", r"<code>\1</code>", md)
    out, in_ul = [], False
    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{line[2:]}</li>")
            continue
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if not line.strip():
            continue
        if line.startswith("> "):
            out.append(f'<p class="quote">{line[2:]}</p>')
        else:
            out.append(f"<p>{line}</p>")
    if in_ul:
        out.append("</ul>")
    return "\n".join(out)


def build(slug: str) -> Path:
    lesson_dir = LESSONS / slug
    if not lesson_dir.is_dir():
        raise SystemExit(f"找不到教案目錄：{lesson_dir}")
    units = []
    for md_path in lesson_dir.glob("*.md"):
        text = md_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        uid = fm.get("unit_id", md_path.stem)
        units.append({
            "uid": uid,
            "title": fm.get("title", ""),
            "duration": fm.get("duration", ""),
            "objective": fm.get("learning_objective", ""),
            "notes": extract_teacher_notes(text),
        })
    units.sort(key=lambda u: unit_sort_key(u["uid"]))

    course_name = slug
    outline = BASE / "_outlines" / f"{slug}.md"
    if outline.exists():
        ofm = parse_frontmatter(outline.read_text(encoding="utf-8"))
        course_name = ofm.get("name", slug)

    cards = []
    for u in units:
        notes_html = md_to_html(u["notes"]) if u["notes"] else \
            '<p class="missing">（本單元教案尚未分離「講師授課筆記」——授課調度可能還混在教學流程，需回頭整理）</p>'
        cards.append(f"""
  <section class="unit">
    <div class="unit-head">
      <span class="uid">{html.escape(u['uid'])}</span>
      <span class="utitle">{html.escape(u['title'])}</span>
      <span class="udur">{html.escape(u['duration'])}</span>
    </div>
    <div class="obj"><strong>學習目標：</strong>{html.escape(u['objective'])}</div>
    <div class="notes">{notes_html}</div>
  </section>""")

    doc = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>{html.escape(course_name)} · 講師手冊（不對學員公開）</title>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{{--c-bg:#f5f3ee;--c-card:#fff;--c-border:#d8d4cb;--c-text:#2c2b28;--c-muted:#7a766d;--c-main:#b5703a}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Noto Sans TC',sans-serif;background:var(--c-bg);color:var(--c-text);line-height:1.8;padding:40px 20px}}
.wrap{{max-width:780px;margin:0 auto}}
.banner{{background:#fbeee2;border:1px solid var(--c-main);border-radius:4px;padding:14px 18px;font-size:.85rem;color:#8a4a1a;margin-bottom:28px}}
h1{{font-family:'Shippori Mincho',serif;font-size:1.6rem;margin-bottom:6px}}
.sub{{font-size:.85rem;color:var(--c-muted);margin-bottom:32px}}
.unit{{background:var(--c-card);border:1px solid var(--c-border);border-left:3px solid var(--c-main);border-radius:4px;padding:20px 24px;margin-bottom:18px}}
.unit-head{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:8px}}
.uid{{font-size:.72rem;color:var(--c-main);font-weight:700;letter-spacing:.05em}}
.utitle{{font-family:'Shippori Mincho',serif;font-size:1.1rem;font-weight:700;flex:1}}
.udur{{font-size:.75rem;color:var(--c-muted)}}
.obj{{font-size:.82rem;color:var(--c-muted);margin-bottom:14px;padding-bottom:12px;border-bottom:1px dashed var(--c-border)}}
.notes p{{font-size:.9rem;margin:8px 0}}
.notes ul{{margin:8px 0 8px 22px}}
.notes li{{font-size:.9rem;margin:4px 0}}
.notes .quote{{border-left:2px solid var(--c-main);padding-left:12px;color:var(--c-muted);font-style:italic}}
.notes code{{background:#efece5;padding:1px 5px;border-radius:3px;font-size:.85em}}
.missing{{color:#b5703a;font-size:.85rem}}
.foot{{font-size:.75rem;color:var(--c-muted);margin-top:32px;text-align:center}}
</style>
</head>
<body>
<div class="wrap">
  <div class="banner">⚠️ <strong>講師授課用，不對學員公開。</strong>請勿放入學員密碼後的課程網站（courses/）。本檔含 demo 腳本、時間分配、現場備案、收束話術。</div>
  <h1>{html.escape(course_name)}</h1>
  <div class="sub">講師手冊 · 共 {len(units)} 單元 · 由 _lessons/{html.escape(slug)}/ 的「講師授課筆記」自動彙編</div>
{''.join(cards)}
  <div class="foot">弄一下工作室 · 講師手冊 · 重跑 build-teacher-guide.py 即更新</div>
</div>
</body>
</html>"""

    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / f"{slug}.html"
    out_path.write_text(doc, encoding="utf-8")
    return out_path


def main():
    args = sys.argv[1:]
    if not args:
        raise SystemExit("用法：python3 docs/build-teacher-guide.py {slug} | --all")
    slugs = [d.name for d in LESSONS.iterdir() if d.is_dir()] if args[0] == "--all" else [args[0]]
    for slug in slugs:
        p = build(slug)
        print(f"✓ 講師手冊：{p.relative_to(BASE)}")


if __name__ == "__main__":
    main()
