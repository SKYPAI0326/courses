#!/usr/bin/env python3
"""Build review handouts from the frozen learner-content blocks."""

from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).resolve()
COURSE_DIR = SCRIPT.parents[1]
ACP_ROOT = SCRIPT.parents[2]
PROJECT_ROOT = SCRIPT.parents[4]
LESSON_DIR = PROJECT_ROOT / "_lessons" / "ai-short-video-editing"
OUTPUT_DIR = COURSE_DIR / "_review-handouts"
REFERENCE = OUTPUT_DIR / "CH0-3.html"

UNITS = ["CH0-1", "CH0-2", "CH0-3", "CH0-4", "CH1-1", "CH1-2", "CH1-3", "CH1-4"]


def frontmatter(source: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", source, re.S)
    if not match:
        raise ValueError("missing frontmatter")
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def learner_markdown(source: str) -> str:
    match = re.search(
        r"<!-- learner-content:start -->\s*(.*?)\s*<!-- learner-content:end -->",
        source,
        re.S,
    )
    if not match:
        raise ValueError("missing learner-content markers")
    return match.group(1)


def pandoc(markdown: str) -> str:
    result = subprocess.run(
        ["pandoc", "--from", "gfm", "--to", "html5"],
        input=markdown,
        text=True,
        capture_output=True,
        check=True,
    )
    body = result.stdout
    body = re.sub(r"\A<h1[^>]*>.*?</h1>\s*", "", body, count=1, flags=re.S)
    body = body.replace("<table>", '<div class="table-scroll" role="region" tabindex="0"><table class="lesson-table">')
    body = body.replace("</table>", "</table></div>")
    body = re.sub(r"<blockquote>\s*", '<div class="callout"><div class="callout-icon" aria-hidden="true">i</div><div class="callout-body">', body)
    body = re.sub(r"\s*</blockquote>", "</div></div>", body)

    def asset_link(match: re.Match[str]) -> str:
        path = html.unescape(match.group(1))
        target = ACP_ROOT / path
        if not target.exists():
            return match.group(0)
        label = html.escape(path)
        return f'<a href="../../{label}"><code>{label}</code></a>'

    body = re.sub(r"<code>(assets/[^<]+)</code>", asset_link, body)
    return body


def media_preview(unit: str) -> str:
    if unit == "CH0-1":
        return """
      <figure class="media-preview">
        <img src="../../assets/ai-short-video-editing/premiere-foundation-starter/media/still-01-lighthouse.png" alt="基礎練習素材中的海邊燈塔畫面">
        <figcaption>固定素材預覽：課堂會從這張來源畫面對應到原始媒體、Project item、source clip、sequence 與 timeline clip。</figcaption>
      </figure>"""
    if unit == "CH1-1":
        return """
      <figure class="media-preview">
        <video controls preload="metadata" src="../../assets/ai-short-video-editing/ai-demo/ai-short-video-demo-01.mp4"></video>
        <figcaption>120 秒固定中文口播原片；轉錄與字幕抽查都使用同一版本。</figcaption>
      </figure>"""
    if unit == "CH1-3":
        return """
      <figure class="media-preview portrait">
        <video controls preload="metadata" src="../../assets/ai-short-video-editing/ai-demo/ai-mini-cut-reference.mp4"></video>
        <figcaption>25.1 秒直式參考片。比對規格與可理解性，不要求逐格複製。</figcaption>
      </figure>"""
    return ""


def build(unit: str, css: str) -> None:
    source_path = LESSON_DIR / f"{unit}.md"
    source = source_path.read_text(encoding="utf-8")
    meta = frontmatter(source)
    body = pandoc(learner_markdown(source))
    index = UNITS.index(unit)
    previous = UNITS[index - 1] if index else None
    following = UNITS[index + 1] if index + 1 < len(UNITS) else None
    prev_link = (
        f'<a href="{previous}.html" class="nav-btn"><span aria-hidden="true">←</span> {previous}</a>'
        if previous
        else '<a href="index.html" class="nav-btn"><span aria-hidden="true">←</span> 內容檢核入口</a>'
    )
    next_link = (
        f'<a href="{following}.html" class="nav-btn primary">{following} <span aria-hidden="true">→</span></a>'
        if following
        else '<a href="index.html" class="nav-btn primary">回到內容檢核入口 <span aria-hidden="true">→</span></a>'
    )
    title = meta["title"]
    objective = meta["learning_objective"]
    duration = meta["duration"]
    platform = meta.get("platform_version", "")
    preview = media_preview(unit).strip()
    canonical = f"https://skypai0326.github.io/courses/courses/acp-pr/ai-short-video-editing/_review-handouts/{unit}.html"
    extra_css = """
.lesson-body .lesson-section>h2{font-family:'Shippori Mincho',serif;font-size:1.45rem;line-height:1.4;margin:42px 0 16px}
.lesson-body .lesson-section>h2:first-of-type{margin-top:12px}
.lesson-body .lesson-section>h3{font-family:'Shippori Mincho',serif;font-size:1.08rem;line-height:1.5;margin:28px 0 10px}
.lesson-body p{font-size:.92rem;line-height:1.9;margin-bottom:16px}
.lesson-body ul,.lesson-body ol{font-size:.92rem;line-height:1.9;margin:0 0 20px 1.4rem;padding-left:.5rem}
.lesson-body li{margin-bottom:6px}
.lesson-body code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.84em;background:var(--c-surface);padding:.08em .35em;border-radius:3px;overflow-wrap:anywhere}
.lesson-body a{color:#426c72;text-underline-offset:3px}
.media-preview{margin:28px 0;background:var(--c-card);border:1px solid var(--c-border);border-radius:var(--radius);overflow:hidden}
.media-preview img,.media-preview video{display:block;width:100%;height:auto;background:#111}
.media-preview.portrait video{max-height:640px;object-fit:contain}
.media-preview figcaption{font-size:.82rem;color:var(--c-muted);padding:12px 16px;line-height:1.7}
@media(max-width:600px){.lesson-body .lesson-section>h2{font-size:1.3rem}.lesson-body .lesson-section>h3{font-size:1.02rem}}
"""
    document = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(unit)} {html.escape(title)}｜ACP Premiere 證照基礎與 AI 輔助剪輯</title>
<meta name="description" content="{html.escape(objective)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="弄一下工作室">
<meta property="og:title" content="{html.escape(unit)} {html.escape(title)}｜ACP Premiere 證照基礎與 AI 輔助剪輯">
<meta property="og:description" content="{html.escape(objective)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://skypai0326.github.io/courses/素材/og-default.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canonical}">
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>{css}{extra_css}</style>
</head>
<body>
<a href="#main" class="skip-link">跳至主要內容</a>
<header class="topbar">
  <a href="index.html" class="logo">弄一下工作室</a>
  <div class="topbar-divider"></div>
  <span class="topbar-sub">ACP Premiere 證照基礎與 AI 輔助剪輯</span>
  <div class="spacer"></div>
  <span class="topbar-tag">內容與素材檢核稿</span>
</header>
<div class="progress-strip" role="progressbar" aria-label="閱讀進度" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="progress-fill" id="prog"></div></div>
<main id="main">
  <div class="page-hero">
    <a href="index.html" class="back-link"><span aria-hidden="true">←</span> 返回內容檢核入口</a>
    <div class="hero-eyebrow">{html.escape(unit)} · {html.escape(duration)}</div>
    <h1 class="lesson-title">{html.escape(title)}</h1>
    <p class="lesson-tagline">{html.escape(objective)}</p>
    <div class="outcomes"><div class="outcomes-label">本單元完成證據</div><div class="outcome-item">依正文完成指定檔案、狀態或判斷，並用可觀察結果驗收。</div></div>
  </div>
  <div class="lesson-body" data-learner-content-root="true">
    <section class="lesson-section">
      <div class="callout"><div class="callout-icon" aria-hidden="true">!</div><div class="callout-body"><strong>目前狀態</strong>固定素材與練習檔已建立；Windows Premiere Pro 2024 路徑與零基礎真人跟做仍待驗證。本頁可用於內容與素材檢核，不代表已可直接授課。</div></div>
{preview}
      {body}
    </section>
  </div>
  <nav class="nav-footer" aria-label="單元導覽">{prev_link}{next_link}</nav>
</main>
<footer class="footer">
  <span class="footer-logo">弄一下工作室</span><div class="footer-div"></div>
  <span class="footer-note">內容與素材檢核型講義</span><div class="footer-div"></div>
  <span class="footer-meta" data-platform-version="{html.escape(platform)}" data-built-at="2026-10-24">{html.escape(platform)} · 2026-10-24</span>
</footer>
<script>
const fill=document.getElementById('prog');const strip=document.querySelector('.progress-strip');
function updateProgress(){{const h=document.documentElement;const max=h.scrollHeight-h.clientHeight;const pct=max>0?(h.scrollTop/max)*100:100;fill.style.width=pct+'%';strip.setAttribute('aria-valuenow',String(Math.round(pct)));}}
window.addEventListener('scroll',updateProgress,{{passive:true}});window.addEventListener('load',updateProgress);
</script>
</body>
</html>
"""
    (OUTPUT_DIR / f"{unit}.html").write_text(document, encoding="utf-8")


def main() -> None:
    reference = REFERENCE.read_text(encoding="utf-8")
    css_match = re.search(r"<style>(.*?)</style>", reference, re.S)
    if not css_match:
        raise SystemExit("reference CSS not found")
    css = css_match.group(1)
    for unit in UNITS:
        if unit != "CH0-3":
            build(unit, css)
    print("Built review handouts:", ", ".join(unit for unit in UNITS if unit != "CH0-3"))


if __name__ == "__main__":
    main()
