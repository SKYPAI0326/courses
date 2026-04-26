#!/usr/bin/env python3
"""
build-print-pdf.py — 課程網頁 → 紙本改版 PDF 批次產生器
-------------------------------------------------------
針對 gen-ai-140h 等長課程，依 Part 分組，每 Part 產出一份 PDF：
  - 移除密碼關卡、topbar、progress、lesson-nav、back-link、scripts
  - 所有 <details> 加 open 屬性（紙本常駐展開）
  - 移除 quiz radio（<input type="radio">）
  - 移除 copy-btn 元素
  - 注入 @media print CSS（頁邊、字級、避免斷行）

流程：
  for each Part:
    產生封面 HTML → Chrome headless → cover.pdf
    for each unit (CH / PRAC):
      clean HTML → temp → Chrome headless → unit.pdf
    pdfunite cover.pdf unit*.pdf → _pdf/part{N}.pdf

使用：
  python3 docs/build-print-pdf.py gen-ai-140h          # 產 7 份 Part PDF
  python3 docs/build-print-pdf.py gen-ai-140h --part 1 # 只產 part1

依賴：Google Chrome（/Applications/...）、pdfunite（brew install poppler）、bs4
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from bs4 import BeautifulSoup  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ── 課程 slug 對應中文名 + Part 標題（需要時擴充）────────────────
COURSE_META = {
    "gen-ai-140h": {
        "name": "生成式 AI 職訓實務應用班（140h）",
        "institution": "弄一下工作室",
        "parts": {
            1: "Part 1｜解鎖 AI 工作模式",
            2: "Part 2｜建立文字與知識產能",
            3: "Part 3｜把資料變成流程",
            4: "Part 4｜零代碼工具工坊",
            5: "Part 5｜前端與部署實戰",
            6: "Part 6｜AI 應用開發進階",
            7: "Part 7｜專題衝刺與成果發表",
        },
    },
    "office-ai": {
        "name": "辦公室 AI 工具實務應用",
        "institution": "弄一下工作室",
        "parts": {
            1: "Part 1｜認識 AI 並開口問 AI",
            2: "Part 2｜文書加速三件事",
            3: "Part 3｜會議與協作升級",
            4: "Part 4｜打造我的 AI 工作流",
            5: "Part 5｜行銷文案 AI 實戰",
        },
    },
}

# ── 注入的 @media print CSS（紙本友善）───────────────────────────
# 關鍵：原站頁面用 .reveal (opacity:0) + JS 加 .in 觸發淡入動畫；
# 我們砍了所有 <script>，必須用 CSS 強制顯示，否則 PDF 只印得到 hero。
PRINT_CSS = """
<style id="print-override">
/* 強制顯示所有淡入動畫元素（放在 @media print 外，確保任何情境都生效） */
.reveal, .section-rule, [class*="reveal"] {
  opacity: 1 !important;
  transform: none !important;
  transition: none !important;
  animation: none !important;
  visibility: visible !important;
}
/* 浮水印：螢幕預覽時隱藏，只印 PDF 時顯示 */
.print-watermark { display: none; }
@page { size: A4; margin: 20mm 18mm 18mm 18mm; }
@media print {
  /* 所有元素都印背景色（Chrome headless 預設 exact 但有些 UA 會略過） */
  *, *::before, *::after {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  html, body { background:#fff !important; }
  body { font-size:11pt !important; line-height:1.75 !important;
    orphans:3; widows:3; }

  /* 移除站點導覽、互動元件 */
  .topbar, .progress-strip, .section-dots,
  .back-link, .lesson-nav, .footer, .copy-btn,
  .copy-row, script { display:none !important; }

  /* 主版面滿版（左右 margin 改靠 @page 留白；所有內層 wrapper 清零） */
  .lesson-hero, .prac-hero {
    padding:0 0 14px !important; max-width:none !important;
    margin:0 !important;
  }
  .lesson-body, .tool-wrap {
    padding:0 !important; max-width:none !important; margin:0 !important;
  }
  .hero-eyebrow, .hero-meta, .prac-tagline, .lesson-tagline {
    margin:0 0 6px !important; max-width:none !important;
  }
  .prac-title { font-size:22pt !important; line-height:1.35 !important;
    margin:4px 0 10px !important; page-break-after:avoid; }
  .lesson-title { font-size:22pt !important; line-height:1.35 !important;
    margin:4px 0 10px !important; page-break-after:avoid; }
  .section-heading { font-size:15pt !important; line-height:1.4 !important;
    page-break-after:avoid; margin:14px 0 14px !important; }
  .section-eyebrow { page-break-after:avoid; margin-top:10px !important; }
  .lesson-section { margin-bottom:26px !important;
    opacity:1 !important; transform:none !important; page-break-inside:auto; }

  /* 段落控制：允許分頁，但避免標題孤立於頁尾 */
  p { orphans:3; widows:3; margin:0 0 10px !important; }
  h2, h3, h4 { page-break-after:avoid; }

  /* 只對小型區塊 avoid-break（避免大區塊被整個推到下頁造成大量留白） */
  .callout, .big-quote, .quiz-item,
  .outcome-item, .scenario-card, .tool-card, .compare-card {
    page-break-inside:avoid;
  }

  /* details / prac-sample：允許內部分頁，不要硬撐 */
  details, .prac-sample, .compare-grid, .scenario-grid, .tool-grid,
  .material-block, .output-fold, .qa-item {
    page-break-inside:auto !important;
  }
  details { margin:14px 0 !important; }
  details > summary { cursor:default !important; list-style:none !important; }
  details > summary::-webkit-details-marker { display:none !important; }
  details > summary::marker { content:'' !important; }

  /* 連結色去除（紙本無法點，藍色反而礙眼） */
  a { color:#2c2b28 !important; text-decoration:none !important; }

  /* 通用程式區塊（code-block、pre） */
  .code-block, pre {
    background:#f2f0ea !important; color:#1a1a1a !important;
    border:1px solid #d0ccc2 !important;
    font-size:10pt !important; line-height:1.65 !important;
    padding:12px 14px !important; page-break-inside:auto !important;
  }

  /* prac-sample 內部字級 & 紙本友善改色 */
  .ps-head, summary.ps-head { padding-right:0 !important; }
  summary.ps-head::after { display:none !important; }
  .ps-eyebrow { font-size:.78rem !important; }
  .ps-hint { font-size:10pt !important; line-height:1.7 !important; }
  .ps-label { font-size:10pt !important; margin-bottom:6px !important; }
  .ps-label-tag { font-size:9pt !important; }
  .ps-material {
    font-size:10.5pt !important; line-height:1.8 !important;
    background:#f6f3ec !important; padding:12px 14px !important;
    page-break-inside:auto !important;
  }
  /* 深底 Prompt → 淺底黑字（省墨、清楚） */
  .ps-prompt {
    background:#f4f1ea !important; color:#1a1a1a !important;
    border:1px solid #d8d4cb !important;
    font-size:10pt !important; line-height:1.75 !important;
    padding:12px 14px !important;
    font-family:ui-monospace,'SF Mono',Menlo,monospace !important;
    page-break-inside:auto !important;
  }
  .ps-expect {
    font-size:10pt !important; line-height:1.75 !important;
    padding:12px 14px !important;
    page-break-inside:auto !important;
  }
  .ps-block { margin-bottom:12px !important; page-break-inside:auto !important; }
  .prac-sample { padding:16px 18px !important; page-break-inside:auto !important; }

  /* Mini Practice 步驟 */
  .mini-prac { page-break-inside:auto !important; }
  .mini-prac-step { page-break-inside:avoid; margin:8px 0 !important; }

  /* Quiz radio 隱藏、option 用紙本圓圈字元代替 */
  input[type="radio"], input[type="checkbox"] { display:none !important; }
  .quiz-opt { display:flex !important; align-items:baseline !important;
    gap:8px !important; padding:4px 0 !important; }
  .quiz-opt::before { content:"○"; color:#666; flex-shrink:0; }
  .quiz-item { page-break-inside:avoid; margin:12px 0 !important; }

  /* ─── 紙本講義：office-ai 互動元件轉靜態 ─── */

  /* 保險隱藏網頁專屬 UI（DOM 已 decompose，CSS 再補一刀） */
  .tab-btn, .mode-btn, .tab-row, .mode-row,
  .drill-reveal-btn, .btn-drill-copy,
  .prompt-copy, .step-example-copy,
  .action-row, .toast,
  button, select {
    display: none !important;
  }

  /* 強制展開預設隱藏的內容（tool-panel / reveal / result） */
  .tool-panel, .drill-reveal-content, .result-area, .result-box {
    display: block !important;
    opacity: 1 !important;
    visibility: visible !important;
    max-height: none !important;
    overflow: visible !important;
  }

  /* tool-panel 每個面板的視覺分隔（配 .print-panel-label 小標） */
  .tool-panel {
    margin: 0 0 10px !important;
    padding: 0 !important;
    page-break-inside: auto !important;
  }
  .print-panel-label {
    font-family: 'Shippori Mincho', serif !important;
    font-size: 12pt !important; font-weight: 700 !important;
    color: #2c2b28 !important;
    margin: 12px 0 6px !important;
    padding: 4px 10px !important;
    border-left: 3px solid #b5703a !important;
    background: #f6f3ec !important;
    page-break-after: avoid !important;
  }
  /* 工具卡：紙本用輕框、小 padding */
  .tool-card {
    padding: 10px 12px !important;
    border: 1px solid #d8d4cb !important;
    background: #fff !important;
    margin: 0 0 8px !important;
    border-radius: 0 !important;
  }
  .field-group { gap: 6px !important; margin-bottom: 4px !important;
    display: block !important; }
  .field-item { gap: 2px !important; margin-bottom: 6px !important;
    display: block !important; page-break-inside: avoid; }

  /* 填空：textarea / input 轉為紙本手寫區 */
  textarea, input[type="text"], input[type="number"],
  input[type="email"], input[type="tel"] {
    background: #fff !important;
    color: #2c2b28 !important;
    border: 1px solid #c2bdb0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    outline: none !important;
    font-size: 10.5pt !important;
    font-family: 'Noto Sans TC', sans-serif !important;
    width: 100% !important;
    display: block !important;
    resize: none !important;
    margin: 4px 0 10px !important;
  }
  /* 單行輸入：低調底線 */
  input[type="text"], input[type="number"],
  input[type="email"], input[type="tel"] {
    border: none !important;
    border-bottom: 1px solid #7a766d !important;
    padding: 4px 6px !important;
    min-height: 1.6em !important;
  }
  /* 多行輸入：橫格線引導手寫（高度依 rows 屬性，不再 min-height 強撐） */
  textarea {
    min-height: 2.6em !important;
    padding: 4px 8px !important;
    line-height: 1.7em !important;
    margin: 2px 0 4px !important;
    background-image: repeating-linear-gradient(
      to bottom, #fff 0, #fff 1.7em,
      #e0dcd2 1.7em, #e0dcd2 calc(1.7em + 1px)
    ) !important;
  }
  /* placeholder 作為紙本「範例提示」保留為淺灰斜體 */
  textarea::placeholder, input::placeholder {
    color: #a7a29a !important; opacity: 1 !important;
    font-style: italic !important;
  }
  .field-label {
    font-size: 10pt !important;
    font-weight: 500 !important;
    color: #5a564f !important;
    margin: 8px 0 4px !important;
    display: block !important;
  }
  .field-item { margin-bottom: 14px !important; page-break-inside: avoid; }

  /* select 已轉 ul；保險套樣式 */
  .print-select-options {
    list-style: none !important;
    padding: 0 !important;
    margin: 6px 0 12px !important;
  }
  .print-select-options li {
    padding: 3px 0 !important;
    font-size: 10.5pt !important;
    line-height: 1.65 !important;
  }

  /* .result-area / .result-box 已在 clean_html() decompose，這裡保險隱藏殘餘 */
  .result-area, .result-box, .result-text, .result-label, .result-empty {
    display: none !important;
  }

  /* checkbox-item（PRAC3 用）：以 ☐ 符號代替拔掉的 input */
  .checkbox-item {
    display: flex !important; align-items: baseline !important;
    gap: 8px !important; padding: 4px 0 !important;
  }
  .checkbox-item::before {
    content: "☐"; color: #5a564f; flex-shrink: 0;
  }

  /* discuss-section（小組討論，靜態內容） */
  .discuss-section {
    border: 1px solid #d0ccc2 !important;
    background: #f9f7f1 !important;
    padding: 12px 14px !important;
    page-break-inside: auto !important;
    margin: 14px 0 10px !important;
    max-width: none !important;
  }
  .discuss-title { margin-bottom: 8px !important; font-size: 11pt !important; }
  .discuss-label { margin-bottom: 4px !important; }
  .discuss-list { gap: 4px !important; }
  .discuss-item {
    padding: 4px 6px !important;
    background: transparent !important;
    border-left: 2px solid #d0ccc2 !important;
    gap: 8px !important;
  }

  /* lesson-section 間距再收一點（原 26px → 18px） */
  .lesson-section { margin-bottom: 18px !important; }

  /* 圖示（svg/img）若太大縮排 */
  img, svg { max-width:100% !important; height:auto !important; }

  /* 每頁浮水印：position:fixed 元素在 Chrome headless 印 PDF 時會自動重複於每一頁 */
  .print-watermark {
    display: block !important;
    position: fixed !important;
    top: 50% !important; left: 50% !important;
    transform: translate(-50%, -50%) rotate(-30deg) !important;
    font-family: 'Shippori Mincho', serif !important;
    font-size: 64pt !important;
    font-weight: 700 !important;
    color: rgba(44, 43, 40, 0.06) !important;
    letter-spacing: 0.15em !important;
    white-space: nowrap !important;
    pointer-events: none !important;
    z-index: 9999 !important;
    user-select: none !important;
  }
}
.print-page-break { page-break-before:always; }
</style>
"""

# ── 自然排序（PRAC5-1, 2, ..., 10, 11, 12 而非字典序）────────────
def natural_key(s: str):
    return [int(t) if t.isdigit() else t.lower()
            for t in re.split(r'(\d+)', s)]


def clean_html(src: Path, dst: Path) -> None:
    """讀取 src HTML，套紙本改版清理，寫到 dst。"""
    html = src.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")

    # 1) 移除 #_gate 區塊（整個 div + 相關 style/script）
    for el in soup.select("#_gate"):
        el.decompose()

    # 2) 移除全部 <script>
    for el in soup.find_all("script"):
        el.decompose()

    # 3) 移除 topbar / progress-strip / section-dots / back-link /
    #    lesson-nav / footer（紙本不需要）
    for sel in [".topbar", ".progress-strip", ".section-dots",
                ".back-link", ".lesson-nav", ".footer"]:
        for el in soup.select(sel):
            el.decompose()

    # 4) 展開所有 <details>（加 open 屬性）
    for el in soup.find_all("details"):
        el["open"] = ""

    # 5) 移除所有網頁專屬的按鈕列、互動列、以及「AI 生成結果」空框
    #    （紙本不需要「貼入 Gemini 看結果」的空白區——學員真的要看結果是在 AI 上）
    for sel in [
        ".copy-btn", ".copy-row",
        ".btn-drill-copy", ".prompt-copy", ".step-example-copy",
        ".btn-drill-gemini", ".btn-drill-chatgpt", ".btn-drill-copilot",
        ".drill-reveal-btn",
        ".action-row", ".drill-action-row",
        ".template-btn", ".tmpl-btn",
        ".toast",
        ".result-area", ".result-box",
    ]:
        for el in soup.select(sel):
            el.decompose()

    # 5b) 保險：清除所有 class 帶 btn- 前綴的 <a> 連結（紙本不能點）
    for el in soup.find_all("a"):
        classes = el.get("class") or []
        if any(c.startswith("btn-") for c in classes):
            el.decompose()

    # 6) 先抓 tab-btn / mode-btn 與 tool-panel 的對應（靠 onclick 的 switchTab('name', ...)）
    tab_panel_labels: dict[str, str] = {}
    for btn in soup.select(".tab-btn, .mode-btn"):
        onclick = btn.get("onclick", "")
        m = re.search(r"switch(?:Tab|Mode)\(['\"]([^'\"]+)['\"]", onclick)
        if m:
            tab_panel_labels[f"panel-{m.group(1)}"] = btn.get_text(strip=True)

    # 7) 在每個 tool-panel 前插入 panel 標題 h4（取代原本的 tab 切換按鈕）
    for panel in soup.select(".tool-panel"):
        pid = panel.get("id", "")
        label = tab_panel_labels.get(pid)
        if label:
            h4 = soup.new_tag("h4", attrs={"class": "print-panel-label"})
            h4.string = label
            panel.insert_before(h4)

    # 8) 移除 tab/mode 按鈕列（label 已轉為 h4 小標）
    for sel in [".tab-row", ".mode-row", ".tab-btn", ".mode-btn"]:
        for el in soup.select(sel):
            el.decompose()

    # 9) 移除殘留的所有 <button>（lesson-nav / gate / copy 等皆已處理，此為總掃）
    for el in soup.find_all("button"):
        el.decompose()

    # 10) 清除互動屬性（onclick / contenteditable / data-toggle 等）
    for el in soup.find_all(True):
        for attr in (
            "onclick", "onchange", "oninput",
            "onkeyup", "onkeydown", "onsubmit",
            "onfocus", "onblur",
            "contenteditable", "data-toggle", "data-action",
        ):
            if el.has_attr(attr):
                del el[attr]

    # 11) 解除預設隱藏的內容區塊（移除 style 中的 display:none 與 hidden 屬性）
    SHOW_CLASSES = {
        "drill-reveal-content", "result-area",
        "tool-panel", "result-box",
    }
    for el in soup.find_all(True):
        if set(el.get("class") or []) & SHOW_CLASSES:
            if el.has_attr("style"):
                el["style"] = re.sub(
                    r"display\s*:\s*none\s*;?", "", el["style"]
                )
            if el.has_attr("hidden"):
                del el["hidden"]

    # 12) <select> 轉為「☐ 選項」勾選清單
    for sel_el in soup.find_all("select"):
        ul = soup.new_tag("ul", attrs={"class": "print-select-options"})
        for opt in sel_el.find_all("option"):
            text = opt.get_text(strip=True)
            if not text or text.startswith("請選擇") or text.startswith("--"):
                continue
            li = soup.new_tag("li")
            li.string = f"☐ {text}"
            ul.append(li)
        if ul.contents:
            sel_el.replace_with(ul)
        else:
            sel_el.decompose()

    # 13) radio / checkbox：拔掉 input（label 保留；CSS 會替 quiz-opt/checkbox-item 補 ☐/○）
    for el in soup.select('input[type="radio"]'):
        el.decompose()
    for el in soup.select('input[type="checkbox"]'):
        el.decompose()

    # 14) 注入 @media print CSS（放在 </head> 前）
    head = soup.find("head")
    if head:
        head.append(BeautifulSoup(PRINT_CSS, "html.parser"))

    # 15) 注入浮水印 DOM（body 最前端，Chrome headless 印 PDF 時 fixed 元素會每頁重複）
    body = soup.find("body")
    if body:
        watermark = soup.new_tag("div", attrs={"class": "print-watermark"})
        watermark.string = "弄一下工作室版權所有"
        body.insert(0, watermark)

    dst.write_text(str(soup), encoding="utf-8")


def build_cover_html(course: str, part_num: int, units: list[Path]) -> str:
    """產生一個 Part 的封面 + 目錄 HTML。"""
    meta = COURSE_META[course]
    title = meta["parts"][part_num]
    unit_rows = []
    for u in units:
        name = u.stem
        unit_rows.append(f'<li><span class="num">{name}</span></li>')
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;700&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
@page {{ size:A4; margin:0; }}
body {{ margin:0; font-family:'Noto Sans TC',sans-serif; color:#2c2b28; background:#fff; }}
.cover {{ height:100vh; padding:48mm 24mm; display:flex; flex-direction:column;
  justify-content:space-between; }}
.cover-top {{ }}
.cover-institution {{ font-size:10pt; letter-spacing:.2em; color:#7a766d; }}
.cover-course {{ font-family:'Shippori Mincho',serif; font-weight:700; font-size:20pt;
  margin-top:18pt; letter-spacing:-.01em; }}
.cover-mid {{ margin-top:60mm; }}
.cover-label {{ font-size:10pt; letter-spacing:.3em; color:#7a766d; margin-bottom:8pt; }}
.cover-part {{ font-family:'Shippori Mincho',serif; font-weight:700; font-size:36pt;
  line-height:1.3; letter-spacing:-.01em; }}
.cover-bottom {{ font-size:9pt; color:#7a766d; border-top:1px solid #d8d4cb;
  padding-top:10pt; display:flex; justify-content:space-between; }}
.toc {{ page-break-before:always; padding:24mm; }}
.toc h2 {{ font-family:'Shippori Mincho',serif; font-size:16pt; font-weight:700;
  letter-spacing:.05em; margin-bottom:22pt; border-bottom:1px solid #2c2b28;
  padding-bottom:10pt; }}
.toc ol {{ list-style:none; padding:0; }}
.toc li {{ font-size:12pt; padding:8pt 0; border-bottom:1px dotted #d8d4cb;
  display:flex; justify-content:space-between; }}
.toc li .num {{ font-family:'Shippori Mincho',serif; letter-spacing:.05em; }}
.print-watermark {{
  position: fixed; top: 50%; left: 50%;
  transform: translate(-50%, -50%) rotate(-30deg);
  font-family: 'Shippori Mincho', serif; font-weight: 700;
  font-size: 64pt; color: rgba(44, 43, 40, 0.06);
  letter-spacing: 0.15em; white-space: nowrap;
  pointer-events: none; z-index: 9999; user-select: none;
}}
</style>
</head>
<body>
<div class="print-watermark">弄一下工作室版權所有</div>
<section class="cover">
  <div class="cover-top">
    <div class="cover-institution">{meta["institution"]}</div>
    <div class="cover-course">{meta["name"]}</div>
  </div>
  <div class="cover-mid">
    <div class="cover-label">PART {part_num}</div>
    <div class="cover-part">{title.split('｜')[1] if '｜' in title else title}</div>
  </div>
  <div class="cover-bottom">
    <span>紙本改版手冊</span>
    <span>共 {len(units)} 單元</span>
  </div>
</section>
<section class="toc">
  <h2>本 Part 單元目錄</h2>
  <ol>{"".join(unit_rows)}</ol>
</section>
</body>
</html>
"""


def html_to_pdf(html: Path, pdf: Path) -> bool:
    """Chrome headless 印 PDF。"""
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf}",
        "--virtual-time-budget=8000",
        "--run-all-compositor-stages-before-draw",
        f"file://{html.resolve()}",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if pdf.exists() and pdf.stat().st_size > 0:
        return True
    print(f"  ✗ print 失敗: {html.name}")
    if r.stderr:
        print(f"    {r.stderr[:200]}")
    return False


def merge_pdfs(pdfs: list[Path], out: Path) -> bool:
    cmd = ["pdfunite", *[str(p) for p in pdfs], str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode == 0


def collect_part_units(course_dir: Path, part_num: int) -> list[Path]:
    """收集指定 Part 的 CH + PRAC 頁，先 CH 後 PRAC，數字自然排序。"""
    part_dir = course_dir / f"part{part_num}"
    if not part_dir.exists():
        return []
    all_html = list(part_dir.glob("*.html"))
    ch = sorted([h for h in all_html if h.stem.startswith("CH")],
                key=lambda p: natural_key(p.stem))
    prac = sorted([h for h in all_html if h.stem.startswith("PRAC")],
                  key=lambda p: natural_key(p.stem))
    return ch + prac


def build_part_pdf(course: str, course_dir: Path, part_num: int,
                   out_dir: Path, keep_temp: bool = False) -> Path | None:
    units = collect_part_units(course_dir, part_num)
    if not units:
        print(f"  (part{part_num} 無單元，略過)")
        return None

    print(f"▶ Part {part_num}：{len(units)} 單元")

    tmp = Path(tempfile.mkdtemp(prefix=f"print-{course}-p{part_num}-"))
    try:
        pdfs: list[Path] = []

        # 封面
        cover_html = tmp / "00-cover.html"
        cover_html.write_text(build_cover_html(course, part_num, units),
                              encoding="utf-8")
        cover_pdf = tmp / "00-cover.pdf"
        if html_to_pdf(cover_html, cover_pdf):
            pdfs.append(cover_pdf)
            print(f"  ✓ cover")

        # 各單元
        for i, src in enumerate(units, 1):
            cleaned = tmp / f"{i:02d}-{src.stem}.html"
            pdf = tmp / f"{i:02d}-{src.stem}.pdf"
            clean_html(src, cleaned)
            if html_to_pdf(cleaned, pdf):
                pdfs.append(pdf)
                print(f"  ✓ {src.stem}")

        # 合併
        out = out_dir / f"part{part_num}.pdf"
        out_dir.mkdir(parents=True, exist_ok=True)
        if merge_pdfs(pdfs, out):
            size_mb = out.stat().st_size / 1024 / 1024
            print(f"  ✓ 合併 → {out.relative_to(ROOT)} ({size_mb:.1f} MB)")
            return out
        else:
            print(f"  ✗ 合併失敗")
            return None
    finally:
        if not keep_temp:
            shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("course", help="課程 slug，如 gen-ai-140h")
    ap.add_argument("--part", type=int,
                    help="只產指定 Part（預設全部）")
    ap.add_argument("--keep-temp", action="store_true",
                    help="保留暫存 HTML/PDF 供除錯")
    args = ap.parse_args()

    if args.course not in COURSE_META:
        print(f"✗ 未知課程 {args.course}，需先在 COURSE_META 註冊")
        sys.exit(1)

    course_dir = ROOT / "courses" / args.course
    if not course_dir.exists():
        print(f"✗ {course_dir} 不存在")
        sys.exit(1)

    if not Path(CHROME).exists():
        print(f"✗ Chrome 不存在：{CHROME}")
        sys.exit(1)

    if not shutil.which("pdfunite"):
        print("✗ 需要 pdfunite（brew install poppler）")
        sys.exit(1)

    out_dir = course_dir / "_pdf"
    parts = [args.part] if args.part else sorted(COURSE_META[args.course]["parts"].keys())

    built = []
    for pn in parts:
        result = build_part_pdf(args.course, course_dir, pn, out_dir, args.keep_temp)
        if result:
            built.append(result)

    print()
    print(f"═══ 完成 {len(built)} 份 PDF ═══")
    for p in built:
        size_mb = p.stat().st_size / 1024 / 1024
        print(f"  {p.relative_to(ROOT)}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
