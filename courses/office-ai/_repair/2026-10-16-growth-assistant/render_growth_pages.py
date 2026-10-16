#!/usr/bin/env python3
"""Render the three approved learner-content sources into existing course shells."""

from __future__ import annotations

import html
import re
from pathlib import Path

from markdown_it import MarkdownIt


COURSE = Path(__file__).resolve().parents[2]
BASE = COURSE.parents[1]
MD = MarkdownIt("commonmark", {"html": False, "linkify": False, "typographer": False}).enable("table")

PROSE_CSS = r"""
/* growth-assistant learner content — source-rendered 2026-10-16 */
.prose .lesson-section{margin-bottom:64px}
.prose .section-heading code,.prose h3 code{font-family:'Courier New',monospace;font-size:.88em;background:var(--c-surface);padding:.1em .35em;border-radius:3px}
.prose h3{font-family:'Shippori Mincho',serif;font-size:1.1rem;line-height:1.55;margin:30px 0 12px;color:var(--c-text)}
.prose p{font-size:.92rem;line-height:1.95;margin:0 0 18px;color:var(--c-text)}
.prose ul,.prose ol{margin:0 0 22px;padding-left:1.55rem;font-size:.92rem;line-height:1.9}
.prose li{margin:7px 0;padding-left:.2rem}
.prose blockquote{margin:20px 0;padding:16px 20px;background:var(--c-surface);border-left:3px solid var(--c-a2);color:var(--c-text)}
.prose blockquote p:last-child{margin-bottom:0}
.prose pre{position:relative;max-width:100%;overflow:auto;margin:20px 0 24px;padding:18px 20px;background:#fff;border:1px solid var(--c-border);border-left:3px solid var(--c-a2);border-radius:var(--radius);white-space:pre-wrap;overflow-wrap:anywhere}
.prose pre code{font-family:'Courier New',monospace;font-size:.8rem;line-height:1.75;color:var(--c-text)}
.prose p code,.prose li code,.prose td code{font-family:'Courier New',monospace;font-size:.85em;background:var(--c-surface);padding:.12em .35em;border-radius:3px}
.prose table{display:table;width:100%;border-collapse:collapse;margin:20px 0 28px;background:#fff;font-size:.85rem;line-height:1.65}
.prose th,.prose td{border:1px solid var(--c-border);padding:11px 13px;vertical-align:top;text-align:left}
.prose th{background:var(--c-surface);font-weight:700}
.prose a{color:var(--c-a2);text-decoration-thickness:1px;text-underline-offset:3px;overflow-wrap:anywhere}
.prose a:hover{color:var(--c-a1)}
.prose strong{font-weight:700}
.prose hr{border:0;border-top:1px solid var(--c-border);margin:48px 0}
@media(max-width:768px){.prose table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}.prose th,.prose td{min-width:150px}.prose pre{padding:15px 16px}}
""".strip()

PAGES = {
    "CH1-2": {
        "source": BASE / "_lessons/office-ai/CH1-2.md",
        "target": COURSE / "ch1/CH1-2.html",
        "number": "1.2",
        "chapter": "章節一 AI 與我的日常工作",
    },
    "CH6-1": {
        "source": BASE / "_lessons/office-ai/CH6-1.md",
        "target": COURSE / "ch6/CH6-1.html",
        "number": "6.1",
        "chapter": "章節六 建立可持續成長的 AI 助理",
    },
    "CH6-3": {
        "source": BASE / "_lessons/office-ai/CH6-3.md",
        "target": COURSE / "ch6/CH6-3.html",
        "number": "6.3",
        "chapter": "章節六 建立可持續成長的 AI 助理",
    },
}


def extract(source: str) -> tuple[str, str, list[str], str]:
    match = re.search(r"<!-- learner-content:start -->\s*(.*?)\s*<!-- learner-content:end -->", source, re.S)
    if not match:
        raise ValueError("learner-content markers not found")
    lines = match.group(1).strip().splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError("learner content must start with H1")
    title = lines[0][2:].strip()
    outcomes_i = lines.index("## 本節完成後，你能做到什麼")
    next_h2 = next(i for i in range(outcomes_i + 1, len(lines)) if lines[i].startswith("## "))
    intro = " ".join(line.strip() for line in lines[1:outcomes_i] if line.strip())
    outcomes = [line[2:].strip() for line in lines[outcomes_i + 1:next_h2] if line.startswith("- ")]
    body = "\n".join(lines[next_h2:]).strip()
    if len(outcomes) < 3:
        raise ValueError("at least three outcomes required")
    return title, intro, outcomes, body


def sections(body_md: str) -> str:
    body_md = body_md.replace("../../courses/office-ai/", "../")
    # CommonMark treats a closing emphasis marker immediately followed by a
    # CJK character as non-flanking. A separating space preserves the intended
    # bold label without changing the wording.
    body_md = re.sub(r"\*\*([^*\n]+?)\*\*(?=\S)", r"**\1** ", body_md)
    rendered = MD.render(body_md)
    parts = re.split(r"(?=<h2>)", rendered)
    chunks: list[str] = []
    section_no = 0
    for part in parts:
        if not part.strip():
            continue
        if not part.startswith("<h2>"):
            raise ValueError("body contains content before first H2")
        part = part.replace("<h2>", '<h2 class="section-heading">', 1)
        chunks.append(
            '    <div class="lesson-section">\n'
            f'      <div class="section-eyebrow">({section_no:02d})</div>\n'
            + "      " + part.replace("\n", "\n      ").rstrip()
            + "\n    </div>"
        )
        section_no += 1
    return "\n".join(chunks)


def set_meta(page: str, prop: str, value: str, *, property_attr: bool = False) -> str:
    attr = "property" if property_attr else "name"
    pattern = rf'(<meta {attr}="{re.escape(prop)}" content=")[^"]*(">)'
    return re.sub(pattern, lambda m: m.group(1) + html.escape(value, quote=True) + m.group(2), page, count=1)


def render_page(config: dict[str, object]) -> None:
    source = Path(config["source"]).read_text(encoding="utf-8")
    target = Path(config["target"])
    page = target.read_text(encoding="utf-8")
    title, intro, outcomes, body_md = extract(source)
    number = str(config["number"])
    chapter = str(config["chapter"])
    page_title = f"{number} {title}｜辦公室 AI 工具實務應用"
    description = re.sub(r"[`*_]", "", intro)

    page = re.sub(r"<title>.*?</title>", f"<title>{html.escape(page_title)}</title>", page, count=1)
    page = set_meta(page, "description", description)
    page = set_meta(page, "og:title", page_title, property_attr=True)
    page = set_meta(page, "og:description", description, property_attr=True)
    page = set_meta(page, "twitter:title", page_title)
    page = set_meta(page, "twitter:description", description)

    if PROSE_CSS not in page:
        page = page.replace("</style>", PROSE_CSS + "\n</style>", 1)

    outcome_html = "\n".join(
        f'      <div class="outcome-item"><div class="outcome-dot"></div><span>{MD.renderInline(item)}</span></div>'
        for item in outcomes
    )
    hero_body = f"""

  <div class="lesson-hero" id="main">
    <a class="back-link" href="../index.html"><span aria-hidden="true">←</span> 回到課程總覽</a>
    <div class="hero-meta">
      <span class="hero-part">{html.escape(chapter)}</span>
      <div class="hero-divider-v"></div>
      <span class="hero-num">單元 {html.escape(number)}</span>
    </div>
    <h1 class="lesson-title">{MD.renderInline(title)}</h1>
    <p class="lesson-tagline">{MD.renderInline(intro)}</p>
    <div class="outcomes">
      <div class="outcomes-label">學完這節，你會</div>
{outcome_html}
    </div>
  </div>

  <div class="lesson-body prose">
{sections(body_md)}
  </div>

"""
    page, count = re.subn(
        r'\s*<div class="lesson-hero" id="main">.*?\s*(?=<div class="(?:nav-return|lesson-nav)")',
        hero_body,
        page,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise ValueError(f"unable to replace learner body in {target}")
    page = re.sub(r'data-platform-version="[^"]*" data-built-at="[^"]*"', 'data-platform-version="gemini-web-2026-10-16" data-built-at="2026-10-16"', page, count=1)
    page = "\n".join(line.rstrip() for line in page.splitlines()) + "\n"
    target.write_text(page, encoding="utf-8")


for page_config in PAGES.values():
    render_page(page_config)

print("Rendered:", ", ".join(PAGES))
