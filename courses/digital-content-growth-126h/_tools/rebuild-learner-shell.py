#!/usr/bin/env python3
"""Rebuild the learner-facing shell for digital-content-growth-126h.

The script deliberately keeps the teaching body from each existing lesson.
It replaces only the page chrome, navigation, production-status leakage, and
course/module landing structures.
"""

from __future__ import annotations

import re
import subprocess
from datetime import date
from html import escape
from pathlib import Path

from bs4 import BeautifulSoup


COURSE_DIR = Path(__file__).resolve().parents[1]
REPAIR_DIR = COURSE_DIR / "_repair" / "2026-09-16"
BACKUP_HTML_DIR = COURSE_DIR / "_backup" / "2026-09-16-pre-repair" / "html"
COURSE_TITLE = "數位內容與成長行銷人才培訓"
INSTITUTION = "弄一下工作室"
COURSE_URL = "https://skypai0326.github.io/courses/courses/digital-content-growth-126h"
OG_IMAGE = "https://skypai0326.github.io/courses/素材/og-default.png"
TODAY = date.today().isoformat()
TEMPLATE_DIR = COURSE_DIR / "assets" / "templates"
DATASET_DIR = COURSE_DIR / "assets" / "datasets"


PARTS = [
    {
        "number": 1,
        "title": "創業企劃與能力方向・前段",
        "hours": "4h",
        "purpose": "把專長或點子整理成共同 Brief，建立後續五科共用的任務框架。",
        "output": "共同服務／品牌 Brief",
        "units": [
            ("CH1-1", "從專長／點子到應用情境", "把專長或點子改寫成可用於求職、企業專案、自由工作或個人品牌的應用情境。", "1h"),
            ("CH1-2", "問題、受眾與需求", "把模糊想法改寫成目標對象與可觀察問題。", "1h"),
            ("CH1-3", "服務價值與共同任務框架", "建立價值主張、溝通目標與後續科目共用的內容任務。", "1h"),
            ("PRAC1", "建立個人服務／微型品牌 Brief", "完成後續五科共用的主題、受眾、價值與工作簡報。", "1h"),
        ],
    },
    {
        "number": 2,
        "title": "攝影與影片編修",
        "hours": "30h",
        "purpose": "從影像任務、腳本、素材來源與視覺資產，完成一組可行銷內容。",
        "output": "短影音、平面資產、來源紀錄與行銷判斷說明",
        "units": [
            ("CH2-1", "影像在行銷中的角色", "區分品牌認知、受眾理解、信任建立與行動促成的影像任務。", "3h"),
            ("CH2-2", "受眾、訊息與內容定位", "將服務 Brief 轉成影像主題、訊息層級與內容角度。", "3h"),
            ("CH2-3", "腳本、分鏡與平台格式", "依受眾與使用情境設計開頭、敘事、CTA 與版本需求。", "4h"),
            ("CH2-4", "素材取得", "比較自行拍攝、有授權素材與 AI 生成三種路徑，完成來源與風險紀錄。", "4h"),
            ("CH2-5", "Affinity 視覺資產製作", "使用向量、影像與排版工具建立品牌與社群所需的視覺資產。", "4h"),
            ("CH2-6", "剪輯判斷", "依訊息、節奏、字幕、聲音與 CTA 做取捨，不追求特效堆疊。", "4h"),
            ("CH2-7", "Windows 本機剪輯與輸出", "使用課前驗證的免費工具完成匯入、時間軸、字幕、音訊與輸出。", "4h"),
            ("PRAC2", "完成一組可行銷內容", "交付短影音、平面素材、來源紀錄與行銷判斷說明。", "4h"),
        ],
    },
    {
        "number": 3,
        "title": "社群媒體經營",
        "hours": "30h",
        "purpose": "選擇平台角色，建立內容支柱、月曆、互動規則與成效紀錄。",
        "output": "平台策略、內容月曆、內容樣稿、互動規則與成效紀錄表",
        "units": [
            ("CH3-1", "平台角色與選擇", "區分 Instagram、Facebook、Threads 與 LINE 在觸及、互動、承接與回訪的功能。", "3h"),
            ("CH3-2", "受眾、定位與內容支柱", "建立社群主題、內容支柱與可持續的表達方式。", "4h"),
            ("CH3-3", "內容改編與跨平台分發", "將 PRAC2 素材改寫成不同平台的貼文、短影音與互動內容。", "4h"),
            ("CH3-4", "內容月曆與發布流程", "規劃頻率、節奏、素材狀態、CTA 與協作紀錄。", "4h"),
            ("CH3-5", "互動、私訊與風險處理", "建立留言、私訊、負評與敏感情境的回應原則。", "4h"),
            ("CH3-6", "自然觸及與社群成效", "讀取基本指標，區分曝光、互動、導流與轉換訊號。", "4h"),
            ("CH3-7", "LINE 延伸：名單承接與回訪", "設計從社群觸及到名單承接與後續溝通的簡單路徑。", "3h"),
            ("PRAC3", "完成社群經營方案", "交付平台策略、內容月曆、內容樣稿、互動規則與成效紀錄表。", "4h"),
        ],
    },
    {
        "number": 4,
        "title": "SEO 與網站行為追蹤",
        "hours": "24h",
        "purpose": "從搜尋意圖走到 LocalWP、GA4、GTM 與 GSC 資料支持的行銷決策。",
        "output": "SEO、GA4、GTM 證據整合與優化行動",
        "units": [
            ("CH4-1", "搜尋生態與搜尋意圖", "連結服務 Brief、受眾問題與 SEO／內容機會。", "3h"),
            ("CH4-2", "關鍵字與內容規劃", "依搜尋意圖建立關鍵字群組、頁面目的與內容優先序。", "3h"),
            ("CH4-3", "頁面與技術基本檢查", "在 LocalWP 網站檢查標題、階層、連結、索引與基本技術問題。", "3h"),
            ("CH4-4", "GA4 資料模型與 Demo Account", "區分使用者、工作階段、事件、參數與轉換，建立閱讀地圖。", "3h"),
            ("CH4-5", "GA4 報表與探索分析", "從流量來源、行為與路徑資料提出內容或渠道假設。", "3h"),
            ("CH4-6", "GTM 概念與基礎佈建", "在 LocalWP 示範網站設定標籤、觸發條件與變數。", "3h"),
            ("CH4-7", "事件驗證與轉換判讀", "使用 DebugView 或等價驗證路徑，將事件連到行銷決策。", "3h"),
            ("PRAC4", "GSC 資料包與追蹤決策", "判讀教師提供的 GSC 資料，整合 SEO、GA4 與 GTM 證據提出優化行動。", "3h"),
        ],
    },
    {
        "number": 5,
        "title": "國際數位廣告投放實務",
        "hours": "30h",
        "purpose": "從市場與受眾選擇、渠道配置、素材與預算，完成兩輪資料決策的投放企劃。",
        "output": "一平台深度投放包、另一平台轉譯版本、兩輪決策紀錄與優化報告",
        "units": [
            ("CH5-1", "國際市場與受眾選擇", "依服務條件、需求、語言、文化與可觸及性選擇市場。", "3h"),
            ("CH5-2", "自然流量與付費流量", "建立漏斗、渠道角色、目標與預算配置的判斷框架。", "3h"),
            ("CH5-3", "Google Ads 企劃", "設計搜尋意圖、關鍵字、廣告文案、落地頁與測試假設。", "4h"),
            ("CH5-4", "Meta Ads 企劃", "設計受眾、素材變體、版位、訊息與再行銷情境。", "4h"),
            ("CH5-5", "LINE Ads 延伸與渠道比較", "比較名單承接、訊息與廣告渠道的配合方式。", "2h"),
            ("CH5-6", "預算與情境模擬", "使用模擬表比較市場、渠道、素材與預算的不同結果。", "4h"),
            ("CH5-7", "兩輪資料決策實驗", "讀取 Round 1／Round 2 資料，判斷暫停、加碼或修改。", "4h"),
            ("PRAC5", "完成國際廣告投放包", "交付一個平台的深度投放包、另一平台的轉譯版本、兩輪決策紀錄、預算與優化報告。", "6h"),
        ],
    },
    {
        "number": 6,
        "title": "創業企劃與能力整合・後段",
        "hours": "8h",
        "purpose": "把前五個 Part 的成果收斂成一致的主張、能力證據、提案與 30 天行動表。",
        "output": "整合企劃書、提案簡報與 30 天行動表",
        "units": [
            ("CH6-1", "整合受眾、問題與價值", "將前面各科成果收斂成一致的服務／品牌主張。", "2h"),
            ("CH6-2", "方案、商業模式與交付", "依選定應用情境整理服務內容、專案交付方式與基本條件。", "2h"),
            ("CH6-3", "作品呈現與 30 天行動方案", "把內容、社群、SEO、追蹤與廣告成果整理成可展示的能力證據。", "2h"),
            ("PRAC6", "完成整合企劃與提案", "依選定應用情境完成企劃書、簡報與 30 天行動表。", "2h"),
        ],
    },
]


UNIT_MAP = {unit[0]: (part, unit) for part in PARTS for unit in part["units"]}
ALL_UNITS = [unit[0] for part in PARTS for unit in part["units"]]


def esc(value: str) -> str:
    return escape(value, quote=True)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def arrow(value: str) -> str:
    return f'<span aria-hidden="true">{value}</span>'


def meta_head(title: str, description: str, url: str) -> str:
    return f'''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{INSTITUTION}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="canonical" href="{esc(url)}">
<style>:focus-visible {{ outline: 2px solid #2f3b32; outline-offset: 3px; }}</style>
<link rel="stylesheet" href="assets/course-shell.css">'''


def topbar(tag: str, logo_href: str = "index.html") -> str:
    return f'''<a href="#main" class="skip-link">跳至主要內容</a>
<header class="topbar">
  <a class="logo" href="{logo_href}">{INSTITUTION}</a>
  <div class="topbar-divider"></div>
  <span class="topbar-sub">{COURSE_TITLE}</span>
  <span class="spacer"></span>
  <span class="topbar-tag">{esc(tag)}</span>
</header>'''


def footer(platform: str = "Windows 教室；課程提供模板、示範資料與備援路徑") -> str:
    return f'''<footer class="footer" data-platform-version="{esc(platform)}" data-built-at="{TODAY}">
  <span class="footer-logo">{INSTITUTION}</span>
  <span>｜</span>
  <span>{COURSE_TITLE}</span>
</footer>'''


def part_url(number: int) -> str:
    return f"module{number}.html"


def unit_url(code: str) -> str:
    return f"{code}.html"


def template_code_from_href(href: str) -> str | None:
    match = re.fullmatch(r"assets/templates/([^/]+)\.md", href or "")
    return match.group(1) if match else None


def template_actions(code: str) -> str:
    return (
        f'<span class="asset-actions">'
        f'<a class="asset-action" href="assets/templates/{esc(code)}.html" '
        f'target="_blank" rel="noopener">開啟閱讀版（新分頁）</a>'
        f'<a class="asset-action secondary" href="assets/templates/{esc(code)}.md" '
        f'download="{esc(code)}-模板.md">下載原始模板（UTF-8）</a>'
        f'</span>'
    )


def enhance_asset_links(main: BeautifulSoup, document: BeautifulSoup) -> None:
    """讓學員先進入閱讀版，並保留同一份原始檔的單檔下載。"""
    for link in list(main.find_all("a", href=True)):
        href = link.get("href", "")
        code = template_code_from_href(href)
        if code:
            if link.find_parent(class_="asset-actions"):
                continue
            wrapper = document.new_tag("span", attrs={"class": "asset-actions"})
            link["href"] = f"assets/templates/{code}.html"
            link["target"] = "_blank"
            link["rel"] = ["noopener"]
            link["class"] = ["asset-action"]
            link.clear()
            link.append("開啟閱讀版（新分頁）")
            download = document.new_tag(
                "a",
                href=href,
                download=f"{code}-模板.md",
                attrs={"class": "asset-action secondary"},
            )
            download.append("下載原始模板（UTF-8）")
            link.replace_with(wrapper)
            wrapper.append(link)
            wrapper.append(download)
        elif href.startswith("assets/") and href.lower().endswith(".csv"):
            link["download"] = Path(href).name
            classes = link.get("class", [])
            link["class"] = [*classes, "asset-download"]


def pandoc_html(source: Path) -> str:
    try:
        result = subprocess.run(
            ["pandoc", "--from=gfm", "--to=html5", "--wrap=none", str(source)],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return f'<pre class="asset-source-fallback">{esc(source.read_text(encoding="utf-8"))}</pre>'


def ensure_utf8_bom(path: Path) -> None:
    raw = path.read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        path.write_bytes(b"\xef\xbb\xbf" + raw)


def build_asset_pages() -> None:
    """產生可讀 HTML，並讓文字資產在 Windows 下載後仍保留 UTF-8 標記。"""
    for source in sorted(TEMPLATE_DIR.glob("*.md")):
        ensure_utf8_bom(source)
        code = source.stem
        title_line = next(
            (line[2:].strip() for line in source.read_text(encoding="utf-8-sig").splitlines() if line.startswith("# ")),
            f"{code} 模板",
        )
        body = pandoc_html(source)
        body_soup = BeautifulSoup(body, "html.parser")
        first_h1 = body_soup.find("h1")
        if first_h1:
            first_h1.decompose()
        body = str(body_soup).strip()
        canonical = f"{COURSE_URL}/assets/templates/{code}.html"
        html = f'''<!doctype html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title_line)}｜模板閱讀版｜{COURSE_TITLE}</title>
<meta name="description" content="{esc(title_line)}的學員模板閱讀版，可直接閱讀或下載 UTF-8 原始模板。">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{INSTITUTION}">
<meta property="og:title" content="{esc(title_line)}｜模板閱讀版">
<meta property="og:description" content="{esc(title_line)}的學員模板閱讀版，可直接閱讀或下載 UTF-8 原始模板。">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title_line)}｜模板閱讀版">
<meta name="twitter:description" content="{esc(title_line)}的學員模板閱讀版，可直接閱讀或下載 UTF-8 原始模板。">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="canonical" href="{esc(canonical)}">
<style>:focus-visible {{ outline: 2px solid #2f3b32; outline-offset: 3px; }}</style>
<link rel="stylesheet" href="../course-shell.css">
</head>
<body class="asset-page">
{topbar(f"{code} · 模板閱讀版", "../../index.html")}
<header class="asset-hero">
  <a class="breadcrumb" href="../../{code}.html"><span aria-hidden="true">←</span> 返回 {code} 講義</a>
  <div class="hero-eyebrow">學員資產 · LEARNER ASSET</div>
  <h1 class="asset-title">{esc(title_line)}</h1>
  <p class="asset-lead">這是本單元的可讀模板。你可以先在本頁查看欄位，再下載 UTF-8 原始檔自行編輯；原始講義仍保留在上一頁。</p>
  <div class="asset-toolbar">
    <a class="asset-action" href="../../{code}.html">返回 {code} 講義</a>
    <a class="asset-action secondary" href="{code}.md" download="{esc(code)}-模板.md">下載原始模板（UTF-8）</a>
  </div>
</header>
<main class="asset-main" id="main">
  <article class="asset-document">
{body}
  </article>
</main>
{footer("學員模板閱讀版")}
</body>
</html>
'''
        source.with_suffix(".html").write_text(html, encoding="utf-8")

    for dataset in sorted(DATASET_DIR.glob("*.csv")):
        ensure_utf8_bom(dataset)


def render_index() -> str:
    parts_html = []
    for part in PARTS:
        parts_html.append(f'''<a class="part-card" href="{part_url(part["number"])}">
  <span class="part-label">PART {part["number"]} · {part["hours"]}</span>
  <h2>{esc(part["title"])}</h2>
  <p>{esc(part["purpose"])}</p>
  <span class="part-output"><strong>本 Part 主要產物：</strong>{esc(part["output"])}</span>
</a>''')
    description = "從共同 Brief 出發，串起內容、社群、SEO／追蹤、廣告與整合提案。"
    return f'''<!doctype html>
<html lang="zh-TW">
<head>
{meta_head(f"{COURSE_TITLE}｜{INSTITUTION}", description, f"{COURSE_URL}/index.html")}
</head>
<body class="course-page">
{topbar("126h · 整合課程", "../../index.html")}
<header class="course-hero">
  <div class="hero-eyebrow">{INSTITUTION} · INTEGRATED PROGRAM</div>
  <h1 class="hero-title">{COURSE_TITLE}</h1>
  <p class="hero-desc">把專長或點子轉成可被看見、可被推廣、可被驗證的方案。你會沿著同一條能力主線，依自己的應用情境完成可展示的工作成果。</p>
  <hr class="hero-rule">
</header>
<main class="course-main" id="main">
  <section class="intro-panel">
    <h2>你會沿著一條能力主線前進</h2>
    <p>問題與需求 → 服務／品牌方向 → 影像與平面內容 → 社群經營 → SEO／GA4／GTM → 國際廣告 → 整合企劃與提案。求職作品集、企業專案、自由工作與個人品牌都可以使用這條主線。</p>
  </section>
  <div class="capability-chain"><strong>讀法：</strong>先從 Part 1 建立共同主題，再依序使用前一個 Part 的產物。每個 Part 都有自己的導覽頁與完成物，單元頁會說明起始材料、操作與驗證。</div>
  <div class="section-label">六個 Part</div>
  <div class="part-grid">{''.join(parts_html)}</div>
  <nav class="module-nav"><a class="nav-btn primary" href="module1.html">從 Part 1 開始 {arrow('→')}</a><a class="nav-btn" href="../../index.html">{arrow('←')} 所有課程</a></nav>
</main>
{footer()}
</body>
</html>
'''


def render_module(part: dict) -> str:
    n = part["number"]
    previous = f'<a class="nav-btn" href="module{n - 1}.html">{arrow("←")} Part {n - 1}</a>' if n > 1 else f'<a class="nav-btn" href="index.html">{arrow("←")} 課程總覽</a>'
    following = f'<a class="nav-btn primary" href="module{n + 1}.html">Part {n + 1} {arrow("→")}</a>' if n < len(PARTS) else f'<a class="nav-btn primary" href="index.html">回課程總覽 {arrow("→")}</a>'
    units_html = []
    for code, title, purpose, hours in part["units"]:
        kind = "prac" if code.startswith("PRAC") else ""
        badge = " · 整合實作" if kind else ""
        units_html.append(f'''<a class="unit-link {kind}" href="{unit_url(code)}">
  <span class="unit-code">{code}{badge}</span>
  <span><span class="unit-title">{esc(title)}</span><span class="unit-purpose">{esc(purpose)}</span></span>
  <span class="unit-hours">{hours} <span class="unit-arrow" aria-hidden="true">→</span></span>
</a>''')
    description = part["purpose"]
    return f'''<!doctype html>
<html lang="zh-TW">
<head>
{meta_head(f"Part {n}｜{part["title"]}", description, f"{COURSE_URL}/module{n}.html")}
</head>
<body class="module-page">
{topbar(f"PART {n} · {part["hours"]}")}
<header class="module-hero">
  <a class="breadcrumb" href="index.html">{arrow('←')} 課程總覽</a>
  <div class="hero-eyebrow">PART {n} · {part["hours"]}</div>
  <h1 class="module-title">{esc(part["title"])}</h1>
  <p class="module-lead">{esc(description)}</p>
</header>
<main class="module-main" id="main">
  <section class="module-summary">
    <div class="summary-item"><strong>{part["hours"]}</strong><span>本 Part 時數</span></div>
    <div class="summary-item"><strong>{len(part["units"])} 個單元</strong><span>包含 CH 與整合實作</span></div>
    <div class="summary-item"><strong>完成一組成果</strong><span>{esc(part["output"])}</span></div>
  </section>
  <section class="orientation-panel">
    <h2>進入本 Part 前，你要知道的事</h2>
    <p>本頁列出學習順序。每個單元會先說明任務與起始材料，再進入概念、示範、練習與驗證。完成本 Part 後，把這組產物交給下一個 Part 使用。</p>
  </section>
  <div class="section-label">單元順序</div>
  <div class="unit-list">{''.join(units_html)}</div>
  <nav class="module-nav">{previous}{following}</nav>
</main>
{footer()}
</body>
</html>
'''


def extract_artifact(text: str) -> str:
    patterns = [
        r"(?:本節完成物|完成物|交付物)\s*[：:]\s*([^。\n]{2,180})",
        r"(?:留下|取得)\s+([`「][^`」]{2,120}[`」])",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = clean_text(match.group(1)).strip("。；; ")
            if value and "依本頁" not in value:
                return value
    return "依本頁完成驗證段落保存版本化產物"


def extract_platform(soup: BeautifulSoup) -> str:
    meta = soup.find(attrs={"data-platform-version": True})
    if meta:
        return meta.get("data-platform-version", "")
    return "Windows 教室；課程提供模板、示範資料與備援路徑"


def learnerize_asset_language(html: str) -> str:
    """把製作端資產狀態改寫成學員可採取的行動提示。"""
    replacements = [
        ("課前確認：正式案例卡與上游參考品尚未全部可尋址。", "使用備援：先使用本頁模板與示例建立本機版本，正式案例取得後再替換。"),
        ("課前確認：教師社群資料包與資料字典尚未全部可尋址。", "使用備援：先使用本頁模板與去識別示例，正式資料取得後再替換。"),
        ("課前確認：LINE 情境卡與參考序列尚未全部可尋址。", "使用備援：先使用本頁模板、虛構測試狀態與紙面序列，不需要 LINE 帳號或真實名單。"),
        ("課前確認：", "使用前先確認："),
        ("依課前檢查", "依本頁的資產與備援說明"),
        ("課前需提供", "若課堂尚未提供"),
        ("教師需補交", "若尚未取得"),
        ("教師仍需提供去識別情境，否則用本頁案例做角色演練並標記模擬。", "若課堂尚未提供去識別情境，先用本頁案例做角色演練並標記模擬。"),
        ("教師仍需提供三平台改編包、發布流程示例與 LINE 情境列，否則使用本頁示例並標記待補。", "若課堂尚未提供三平台改編包、發布流程示例與 LINE 情境列，先使用本頁示例並標記待補。"),
        ("仍需課前由課堂提供", "若課堂尚未提供"),
        ("需要教師課前提供", "若課堂尚未提供"),
        ("尚未全部可尋址", "目前未納入本頁資產"),
        ("否則保留模擬與待補狀態", "先以模擬版本完成，並標記仍待補的部分"),
        ("待課前確認", "待補證據"),
    ]
    for source, target in replacements:
        html = html.replace(source, target)
    return html


def extract_internal_notes(path: Path) -> list[str]:
    if not path.exists():
        return []
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    notes = []
    for section in soup.find_all("section"):
        heading = section.find("h2")
        if heading and "講師授課筆記" in heading.get_text(" ", strip=True):
            notes.append(f"## {path.stem}\n\n{clean_text(section.get_text(' ', strip=True))}\n")
    return notes


def render_lesson(path: Path, internal_notes: list[str]) -> str:
    raw = path.read_text(encoding="utf-8")
    old = BeautifulSoup(raw, "html.parser")
    code = path.stem
    part, unit = UNIT_MAP[code]
    title = clean_text(old.find("h1", class_="lesson-title").get_text(" ", strip=True))
    tagline_node = old.find(class_="lesson-tagline")
    tagline = clean_text(tagline_node.get_text(" ", strip=True) if tagline_node else "")
    description = clean_text((old.find("meta", attrs={"name": "description"}) or {}).get("content", "")) or tagline
    main = old.find("main", id="main")
    platform = extract_platform(old)
    outcomes = old.find_all(class_="outcome-item")
    if main is None:
        raise RuntimeError(f"missing main#main: {path}")

    for section in list(main.find_all("section")):
        heading = section.find("h2")
        if heading and "講師授課筆記" in heading.get_text(" ", strip=True):
            internal_notes.append(f"## {code}\n\n{clean_text(section.get_text(' ', strip=True))}\n")
            section.decompose()
    for nav in list(main.find_all(class_="nav-footer")):
        nav.decompose()
    for orientation in list(main.find_all(class_="lesson-orientation")):
        orientation.decompose()
    for hero in list(main.find_all(class_="page-hero")):
        hero.decompose()
    # 老頁面的少數章節把頁面標題再次放進教學正文；新外殼已提供唯一的 h1，
    # 這些殘留標題會造成目錄與閱讀層級錯亂，因此只移除正文中的額外 h1。
    for extra_h1 in list(main.find_all("h1")):
        extra_h1.decompose()
    for style in list(old.find_all("style")):
        style.decompose()
    enhance_asset_links(main, old)

    body_text = clean_text(main.get_text(" ", strip=True))
    artifact = extract_artifact(body_text)
    asset_link = main.find("a", href=re.compile(r"^assets/"))
    if asset_link:
        asset_code = Path(asset_link.get("href", "")).stem
        if asset_link.get("href", "").startswith("assets/templates/"):
            asset_html = f'使用 {template_actions(asset_code)} 開始；頁面內會說明它的用途與備援。'
        else:
            asset_html = f'使用 <a href="{esc(asset_link.get("href"))}" download>{clean_text(asset_link.get_text(" ", strip=True)) or "本單元起始資產"}</a> 開始；頁面內會說明它的用途與備援。'
    else:
        asset_html = "從本頁情境與任務段落提供的示例開始；若需要外部工具，依單元內的限制與備援路徑完成同一項判斷。"

    idx = ALL_UNITS.index(code)
    previous_code = ALL_UNITS[idx - 1] if idx > 0 else None
    next_code = ALL_UNITS[idx + 1] if idx + 1 < len(ALL_UNITS) else None
    previous_href = unit_url(previous_code) if previous_code else part_url(part["number"])
    previous_label = previous_code or f"Part {part["number"]}"
    next_href = unit_url(next_code) if next_code else (part_url(part["number"] + 1) if part["number"] < len(PARTS) else "index.html")
    next_label = next_code or (f"Part {part["number"] + 1}" if part["number"] < len(PARTS) else "課程總覽")
    outcomes_html = "".join(f'<div class="outcome-item">{clean_text(item.get_text(" ", strip=True))}</div>' for item in outcomes[:4])
    if not outcomes_html:
        outcomes_html = f'<div class="outcome-item">{esc(unit[2])}</div>'

    content_html = learnerize_asset_language(
        "".join(str(child) for child in main.contents if getattr(child, "name", None) not in {"script"})
    ).strip()
    part_tag = f"PART {part["number"]} · {part["title"]}"
    unit_title = f"({code}) {title}｜{COURSE_TITLE}"
    url = f"{COURSE_URL}/{code}.html"
    return f'''<!doctype html>
<html lang="zh-TW">
<head>
{meta_head(unit_title, description, url)}
</head>
<body class="lesson-page">
{topbar(part_tag)}
<header class="page-hero">
  <a class="breadcrumb" href="{part_url(part["number"])}">{arrow('←')} 返回 Part {part["number"]}</a>
  <div class="hero-eyebrow">{code} · {unit[3]}</div>
  <h1 class="lesson-title">{esc(title)}</h1>
  <p class="lesson-tagline">{esc(tagline or unit[2])}</p>
  <div class="outcomes"><div class="outcomes-label">本單元完成後</div>{outcomes_html}</div>
</header>
<main class="lesson-main" id="main">
  <section class="lesson-orientation">
    <div class="section-eyebrow">學習導覽</div>
    <h2>這一頁要完成什麼</h2>
    <p class="orientation-lead">{esc(unit[2])} 完成後，你會留下可交接的成果，並把它交給 {esc(next_label)} 使用。</p>
    <div class="orientation-grid">
      <div class="orientation-item"><strong>起始材料</strong><span>{asset_html}</span></div>
      <div class="orientation-item"><strong>完成物</strong><span>{esc(artifact)}</span></div>
      <div class="orientation-item"><strong>閱讀順序</strong><span>情境與任務 → 概念／案例 → 操作或練習 → 驗證 → 下一個使用位置。</span></div>
    </div>
  </section>
{content_html}
  <nav class="nav-footer">
    <a class="nav-btn" href="{previous_href}">{arrow('←')} {esc(previous_label)}</a>
    <a class="nav-btn" href="{part_url(part["number"])}">回 Part {part["number"]}</a>
    <a class="nav-btn primary" href="{next_href}">{esc(next_label)} {arrow('→')}</a>
  </nav>
</main>
{footer(platform)}
</body>
</html>
'''


def main() -> None:
    internal_notes: list[str] = []
    for code in ALL_UNITS:
        internal_notes.extend(extract_internal_notes(BACKUP_HTML_DIR / f"{code}.html"))
    if not internal_notes:
        for code in ALL_UNITS:
            internal_notes.extend(extract_internal_notes(COURSE_DIR / f"{code}.html"))
    (COURSE_DIR / "index.html").write_text(render_index(), encoding="utf-8")
    for part in PARTS:
        (COURSE_DIR / f"module{part['number']}.html").write_text(render_module(part), encoding="utf-8")
    for code in ALL_UNITS:
        render_path = COURSE_DIR / f"{code}.html"
        render_path.write_text(render_lesson(render_path, []), encoding="utf-8")
    build_asset_pages()

    internal_dir = REPAIR_DIR / "internal-notes"
    internal_dir.mkdir(parents=True, exist_ok=True)
    (internal_dir / "EXTRACTED-TEACHER-NOTES.md").write_text(
        "# Extracted teacher notes\n\n" + "\n".join(internal_notes), encoding="utf-8"
    )
    print(f"rebuilt {len(PARTS) + len(ALL_UNITS) + 1} learner pages")
    print(f"archived {len(internal_notes)} internal sections")


if __name__ == "__main__":
    main()
