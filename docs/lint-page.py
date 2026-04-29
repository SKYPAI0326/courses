#!/usr/bin/env python3
"""
lint-page.py — 弄一下工作室課程頁面合規性檢查器（單一真相源）
-----------------------------------------------------------
對單一 HTML 或整個 courses/ 目錄執行規則檢查。
本腳本是**唯一**的規則實作；所有 skill / agent / CLAUDE.md 應引用此檔，不再重述規則。

使用：
  python3 docs/lint-page.py <file.html>           # 單頁
  python3 docs/lint-page.py courses/<slug>/       # 單課
  python3 docs/lint-page.py --all                 # 全站
  python3 docs/lint-page.py --changed             # git diff 變動過的頁（pre-commit hook 用）
  python3 docs/lint-page.py --summary             # 只印分類統計

Exit code：
  0 = 無 BLOCKER（ERROR/WARN 可存在）
  1 = 有 BLOCKER
  2 = 使用錯誤

嚴重度設計：
  BLOCKER = 結構性錯誤或視覺災難，不可放行（box-shadow / 禁用組件 / 自創變數）
  ERROR   = 標準功能缺失，應補（skip-link / main#main / SEO meta）
  WARN    = 改善建議（metadata / 「您」用詞 / 字型非 8 階）
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = ROOT / "docs" / ".lint-baseline.json"
BASELINE_V3_PATH = ROOT / "docs" / ".lint-baseline-v3.json"

# v3 規則 ID 集合（供 --v3-soft 降級用）
V3_RULE_IDS = {
    "B-v3-1", "B-v3-2", "B-v3-3",
    "E-v3-1", "E-v3-2", "E-v3-3",
    "W-v3-1", "W-v3-2", "W-v3-3", "W-v3-4",
}

# WARN 分桶（2026-04-26 Round 3c 加）— 訊息 keyword 對應到問題類別
# 用於 --by-bucket 模式，幫助 1000+ WARN 變成可執行清單
BUCKETS = {
    "migration-debt": [
        r"非 V4.*字型",        # 397 條 — v3→v4 字型尺度漂移
        r"--c-main 在 CSS 中出現",  # 嚴格派遷移後在單元頁的副作用
        r"Step N",             # 舊文案未本土化
        r"『您』",              # 文案規範漂移
    ],
    "structural": [
        r"lesson-section 僅",  # < 5 個 section
        r"callout 有",         # > 4 個 callout
        r"big-quote 有",        # > 1 個 big-quote
    ],
    "metadata": [
        r"缺 footer metadata",  # 341 + 13 條 — data-built-at / data-platform-version
        r"缺.*twitter",         # twitter card meta
    ],
    "a11y": [
        r"aria-hidden",         # 47 條 — 箭頭未標 aria-hidden
        r"focus-visible",       # focus ring
    ],
    "motion": [
        r":hover 同時變化",     # W-v3-4：hover 屬性 > 2
    ],
    "v3-misc": [
        r"\[W-v3-1\]", r"\[W-v3-3\]",  # v3 其他規則
    ],
}


def bucket_of(msg: str) -> str:
    """把 WARN 訊息分桶。fallback 為 'other'。"""
    for bucket, patterns in BUCKETS.items():
        for p in patterns:
            if re.search(p, msg):
                return bucket
    return "other"

# ── 規則定義 ──────────────────────────────────────────────

# 判斷頁型：有不同嚴格度
def classify(path: Path) -> str:
    """回傳 'root' / 'course-index' / 'lesson' / 'module' / 'search' / 'other'。"""
    rel = path.relative_to(ROOT).as_posix() if path.is_absolute() else str(path)
    name = path.name.lower()
    if rel == "index.html":
        return "root"
    if name == "search.html":
        return "search"
    if rel.startswith("courses/") and name == "index.html":
        return "course-index"
    if name.startswith("module"):
        return "module"
    if name.startswith("ch") or name.startswith("prac") or re.match(r"^m\d", name):
        return "lesson"
    return "other"


# 讀檔（忽略編碼錯誤）
def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


# ── BLOCKER 規則 ──────────────────────────────────────────

def check_box_shadow(html: str) -> list:
    """禁用 box-shadow（2026-04-16 清理後禁回流）。允許 #_gate 內用。"""
    issues = []
    # 先剝除 gate 區塊（有 #_gs / #_gate）
    without_gate = re.sub(r'<style id="_gs">.*?</style>', '', html, flags=re.DOTALL)
    without_gate = re.sub(r'<div id="_gate".*?</div>\s*<script>.*?</script>', '', without_gate, flags=re.DOTALL)
    if re.search(r'\bbox-shadow\s*:', without_gate):
        issues.append(("BLOCKER", "發現 box-shadow（2026-04-16 後禁用，gate 區塊除外）"))
    return issues


def check_custom_color_vars(html: str) -> list:
    issues = []
    # --c-a6 已登記於 design-tokens.md（2026-04-24 gen-image 奶茶棕）；允許 a1-a6
    matches = re.findall(r'--c-a([7-9]|\d{2,})\b', html)
    if matches:
        issues.append(("BLOCKER", f"自創 --c-a{matches[0]}+ 變數（禁止，只允許 a1-a6）"))
    return issues


def check_banned_components(html: str) -> list:
    """Pilot A 舊組件禁用。"""
    banned = ["concepts-strip", "case-block", "assets-box", "quiz-block", "hands-on-box"]
    issues = []
    for cls in banned:
        if re.search(rf'class="[^"]*\b{cls}\b', html):
            issues.append(("BLOCKER", f'使用舊組件 class="{cls}"（2026-04-15 Pilot A 後廢除）'))
    return issues


def check_gradient(html: str) -> list:
    if re.search(r'\blinear-gradient\s*\(|\bradial-gradient\s*\(', html):
        return [("BLOCKER", "使用 gradient（禁用）")]
    return []


def check_grid_autofit(html: str) -> list:
    if re.search(r'repeat\s*\(\s*auto-fit', html):
        return [("BLOCKER", "使用 grid-template-columns: repeat(auto-fit, ...)（會產 3+1 孤兒，禁用）")]
    return []


def check_border_radius_max(html: str) -> list:
    """圓角上限 8px（design-tokens §1）。
    豁免：≥50px（pill/circle 刻意形狀）、50%（圓）。
    真正要抓的是 9–49px 的中間區間（card/button 超標）。
    """
    issues = []
    matches = re.findall(r'border-radius\s*:\s*([^;{}"\']+)', html)
    offenders = set()
    for val in matches:
        cleaned = re.sub(r'(var|calc)\s*\([^)]*\)', '', val)
        for num in re.findall(r'(\d+(?:\.\d+)?)\s*px', cleaned):
            try:
                v = float(num)
                if 8 < v < 50:
                    offenders.add(num + "px")
            except ValueError:
                pass
    if offenders:
        issues.append(
            ("BLOCKER", f"border-radius 超過 8px 上限：{', '.join(sorted(offenders))}")
        )
    return issues


# ── ERROR 規則 ────────────────────────────────────────────

def check_skip_link(html: str) -> list:
    if 'class="skip-link"' not in html and "class='skip-link'" not in html:
        return [("ERROR", "缺 skip-link `<a href=\"#main\" class=\"skip-link\">`")]
    return []


def check_main_wrapper(html: str) -> list:
    if not re.search(r'id=["\']main["\']', html):
        return [("ERROR", "缺 `<main id=\"main\">` 或 `<section id=\"main\">` wrapper")]
    return []


def check_seo_meta(html: str) -> list:
    issues = []
    required = {
        'description': r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']+["\']',
        'og:title': r'<meta\s+property=["\']og:title["\']',
        'og:description': r'<meta\s+property=["\']og:description["\']',
        'og:url': r'<meta\s+property=["\']og:url["\']',
        'og:image': r'<meta\s+property=["\']og:image["\']',
        'canonical': r'<link\s+rel=["\']canonical["\']',
    }
    for key, pattern in required.items():
        if not re.search(pattern, html, re.IGNORECASE):
            issues.append(("ERROR", f"缺 SEO meta: {key}"))
    return issues


def check_twitter_meta(html: str) -> list:
    issues = []
    required = ['twitter:card', 'twitter:title', 'twitter:description']
    for key in required:
        if f'name="{key}"' not in html and f"name='{key}'" not in html:
            issues.append(("WARN", f"缺 Twitter meta: {key}"))
    return issues


# ── WARN 規則 ─────────────────────────────────────────────

def check_platform_metadata(html: str) -> list:
    if 'data-platform-version' not in html:
        return [("WARN", "缺 footer metadata `data-platform-version`（course-refresh 依賴）")]
    if 'data-built-at' not in html:
        return [("WARN", "缺 footer metadata `data-built-at`")]
    return []


def check_focus_visible(html: str) -> list:
    if ':focus-visible' not in html:
        return [("WARN", "缺 `:focus-visible` CSS 規則（鍵盤 a11y）")]
    return []


def check_you_form(html: str) -> list:
    """檢查『您』——僅在 body 內容判斷，避免誤抓 comment。"""
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if not body_match:
        return []
    body = body_match.group(1)
    # 移除 HTML comment
    body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)
    if '您' in body:
        count = body.count('您')
        return [("WARN", f"內文含『您』{count} 處（Style Guide: 用『你』）")]
    return []


def check_step_n(html: str) -> list:
    """檢查『Step N』——允許『STEP BY STEP』英文 eyebrow。"""
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if not body_match:
        return []
    body = body_match.group(1)
    # 容許 STEP BY STEP
    body_cleaned = re.sub(r'STEP BY STEP', '', body)
    matches = re.findall(r'\bStep\s+\d+', body_cleaned)
    if matches:
        return [("WARN", f"含『Step N』{len(matches)} 處（應用『步驟 N』）")]
    return []


def check_aria_hidden_arrow(html: str) -> list:
    """裝飾性箭頭 span / i 應包 aria-hidden。

    2026-04-26 Round 7 修正：原 line-based 規則會誤判內文符號（例如 cycle-bridge
    內「→ 下一循環」、step-tip 內「→ 解法」等內文視覺符號、不是裝飾元素、
    不該標 aria-hidden）。改成只抓「裝飾性 span / i 元素」內的箭頭、放過內文。

    判準：
    - 抓 `<span ...>箭頭文字</span>` 形式的元素
    - 該 span 屬性無 aria-hidden 才報
    - 內文段落 / 列表 / blockquote 等內出現的裝飾箭頭符號不抓
    """
    # 只抓「純箭頭 span」（內容只有箭頭 + 空白），不抓含內文的 span
    # 範例：抓 <span>←</span> 但放過 <span>→ 變體 B 上下對調...</span>
    pattern = r'<span\b[^>]*>\s*[←→]\s*</span>'
    offenders = 0
    for m in re.finditer(pattern, html):
        if 'aria-hidden' not in m.group(0):
            offenders += 1
    if offenders > 0:
        return [("WARN", f"{offenders} 處裝飾性箭頭 span 無 aria-hidden（a11y）")]
    return []


def check_lesson_section_count(html: str) -> list:
    """單元頁 lesson-section 應 ≥ 5 個（design-tokens §3 骨幹元件）。"""
    count = len(re.findall(r'class="[^"]*\blesson-section\b', html))
    if count < 5:
        return [("WARN", f"lesson-section 僅 {count} 個（應 ≥ 5 個）")]
    return []


def check_big_quote_cap(html: str) -> list:
    """big-quote 每頁最多 1 個。"""
    count = len(re.findall(r'class="[^"]*\bbig-quote\b', html))
    if count > 1:
        return [("WARN", f"big-quote 有 {count} 個（每頁最多 1 個）")]
    return []


def check_callout_cap(html: str) -> list:
    """callout 每頁最多 4 個（design-tokens §3 使用限制）。"""
    count = len(re.findall(r'class="[^"]*\bcallout\b(?!\s*-)', html))
    if count > 4:
        return [("WARN", f"callout 有 {count} 個（每頁最多 4 個）")]
    return []


def check_font_size_tier(html: str) -> list:
    """檢測非 V4 15 階字型值。
    真相源：_規範/design-tokens.md §2 字型尺寸階（V4 標準）。
    改一處 = 改兩處（tokens + 此白名單）。
    """
    # V4 標準 14 階 + 1 舊相容（1.2rem）。兩種寫法（.9rem / 0.9rem）都允許。
    allowed = {
        # 標題組
        "2rem",
        "1.45rem",
        "1.2rem",    # 舊相容 (.big-quote)
        "1.1rem",
        "1.05rem",
        # 內文組
        ".95rem", "0.95rem",
        ".92rem", "0.92rem",
        ".9rem", "0.9rem",
        ".88rem", "0.88rem",
        # 說明組
        ".85rem", "0.85rem",
        ".82rem", "0.82rem",
        ".8rem", "0.8rem",
        # 註解組
        ".75rem", "0.75rem",
        ".72rem", "0.72rem",
        ".7rem", "0.7rem",
    }
    # 淘汰清單（明確報 WARN 給升級訊號）：.78 / .76 / .73 / .68 / 1rem
    # 不加入 allowed，lint 會報它們。
    # 抓所有 font-size: Xrem
    matches = re.findall(r'font-size\s*:\s*([\d.]+rem)', html)
    bad = [m for m in matches if m not in allowed]
    if bad:
        unique = sorted(set(bad))
        if len(unique) > 3:
            return [("WARN", f"非 V4 15 階字型值（tokens §2 外）：{', '.join(unique[:3])} 等 {len(unique)} 個")]
        return [("WARN", f"非 V4 15 階字型值（tokens §2 外）：{', '.join(unique)}")]
    return []


# ── v3 規則（2026-04-19 追加，additive 不取代既有）──────────
# 訊息前綴 [B-v3-N]/[E-v3-N]/[W-v3-N] 供 --v3-soft 過濾用

def check_v3_lesson_title_br(html: str) -> list:
    """B-v3-1: lesson-title 內禁 <br>（除非 white-space:pre-line）"""
    m = re.search(r'<h1[^>]*class="[^"]*\blesson-title\b[^"]*"[^>]*>(.*?)</h1>', html, re.S)
    if m and re.search(r'<br\s*/?>', m.group(1)):
        if 'white-space:pre-line' not in html and 'white-space: pre-line' not in html:
            return [("BLOCKER", "[B-v3-1] lesson-title 禁 <br>，改 max-width:Nch 軟斷")]
    return []


def check_v3_section_eyebrow_format(html: str) -> list:
    """B-v3-2: section-eyebrow 禁英文 Section NN"""
    issues = []
    for m in re.finditer(
        r'<div[^>]*class="[^"]*\bsection-eyebrow\b[^"]*"[^>]*>(.*?)</div>', html, re.S
    ):
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if re.match(r'^\s*SECTION\s+\d+', text, re.IGNORECASE):
            issues.append(
                ("BLOCKER", "[B-v3-2] section-eyebrow 禁英文『Section NN』，改 `(NN)` 或「第 N 節」")
            )
            break
    return issues


def check_v3_callout_variants(html: str) -> list:
    """B-v3-3: callout 禁自創色系變體（warn/danger/error/success 等）"""
    allowed = {"info", "tip", "key"}
    issues = []
    for m in re.finditer(r'class="[^"]*\bcallout\s+([a-z][\w-]*)\b', html):
        variant = m.group(1)
        if variant not in allowed and variant != "callout":
            issues.append(
                ("BLOCKER", f"[B-v3-3] callout 自創變體 `.callout.{variant}`（只允 info/tip/key）")
            )
            break
    return issues


def check_v3_prefers_reduced_motion(html: str) -> list:
    """E-v3-1: 含 .reveal 或 IntersectionObserver 時須有 prefers-reduced-motion"""
    needs = ('class="reveal"' in html or "class='reveal'" in html
             or 'IntersectionObserver' in html or 'class="reveal ' in html)
    if needs and 'prefers-reduced-motion' not in html:
        return [("ERROR", "[E-v3-1] 頁面含動畫但缺 @media (prefers-reduced-motion:reduce)")]
    return []


def check_v3_progressbar_aria(html: str) -> list:
    """E-v3-2: .progress-strip 須有 role=progressbar"""
    if re.search(r'class="[^"]*\bprogress-strip\b', html):
        # 檢查同一元素或附近有 role=progressbar
        if not re.search(r'role=["\']progressbar["\']', html):
            return [("ERROR", "[E-v3-2] .progress-strip 缺 role=\"progressbar\" + aria-* 屬性")]
    return []


def check_v3_aria_hidden_icons(html: str) -> list:
    """E-v3-3: .callout-icon / .flow-node 須 aria-hidden"""
    issues = []
    for cls in ("callout-icon", "flow-node"):
        for m in re.finditer(rf'<div[^>]*class="[^"]*(?<![\w-]){cls}(?![\w-])[^"]*"[^>]*>', html):
            if 'aria-hidden' not in m.group(0):
                issues.append(
                    ("ERROR", f"[E-v3-3] .{cls} 缺 aria-hidden=\"true\"（裝飾性圖示 a11y）")
                )
                break
    return issues


def check_v3_hardcoded_max_width(html: str) -> list:
    """W-v3-1: lesson-tagline / hero-desc 使用 px max-width（建議 ch/em 或移除）"""
    issues = []
    for cls in ("lesson-tagline", "hero-desc"):
        pattern = rf'\.{cls}\s*\{{[^}}]*max-width\s*:\s*\d+px'
        if re.search(pattern, html):
            issues.append(
                ("WARN", f"[W-v3-1] .{cls} 寫死 px max-width（建議改 ch/em 或移除）")
            )
    return issues


def _check_v3_main_color_count_impl(html: str, threshold: int, context_label: str) -> list:
    """W-v3-2 共用實作；threshold 為 --c-main 在 CSS 中出現次數上限。"""
    style_match = re.search(r'<style[^>]*>(.*?)</style>', html, re.S)
    if not style_match:
        return []
    style = style_match.group(1)
    count = len(re.findall(r'var\s*\(\s*--c-main\s*\)', style))
    if count > threshold:
        return [("WARN", f"[W-v3-2] --c-main 在 CSS 中出現 {count} 次（{context_label} 建議 ≤ {threshold}）")]
    return []


def check_v3_main_color_count(html: str) -> list:
    """W-v3-2 lesson/module 版（≤ 16）— 異常偵測警戒線。

    2026-04-26 Round 7 修正：原 ≤ 4 上限是給「克制主義」old 設計、針對 hero
    內 4 個固定位置（左邊線 / tag / progress / section-eyebrow）。但 v4 課程
    系統實際使用 nav-btn / topbar-tag / outcomes border / step-block hover
    等多處用 main color、自然會 5-15 次。對 v4 課程而言 ≤4 是錯規則。

    新上限 ≤ 16：覆蓋 v4 課程實際範圍（gen-image lesson 5-11 次、PRAC 6-7
    次、module 15-16 次都在範圍內）。仍保留「異常偵測」概念：超過 16
    才報、提示可能有設計失控。
    """
    return _check_v3_main_color_count_impl(html, threshold=16, context_label="lesson v3")


def check_v3_main_color_count_index(html: str) -> list:
    """W-v3-2 root/course-index 版（放寬 ≤ 30）— 2026-04-26 Round 3b 後加。
    總覽頁的 hero/section/module/topbar 等組件依嚴格派必然 > 4 處 var(--c-main)，
    視為「異常偵測警戒線」而非容忍上限。30 不是 cap、是 nag threshold：
    14 個 index.html 實測中 13 個 ≤ 30，唯一超出的 gen-ai-140h（33 處）會繼續觸發 WARN
    提示為 migration debt，不擋放行（仍是 WARN 不是 ERROR）。
    """
    return _check_v3_main_color_count_impl(html, threshold=30, context_label="index v3")


def check_v3_section_heading_em_color(html: str) -> list:
    """W-v3-3: .section-heading em 變色為非 --c-text/inherit/currentColor"""
    m = re.search(
        r'\.section-heading\s+em\s*\{[^}]*color\s*:\s*([^;}]+)',
        html,
    )
    if m:
        val = m.group(1).strip()
        allowed = ('--c-text', 'inherit', 'currentColor', 'currentcolor')
        if not any(a in val for a in allowed):
            return [("WARN", f"[W-v3-3] .section-heading em 變色 `{val}`（建議用 --c-text / inherit）")]
    return []


def check_v3_hover_complexity(html: str) -> list:
    """W-v3-4: :hover 區塊內 property 數 > 2（近似指標）"""
    issues = []
    count_offenders = 0
    for m in re.finditer(r'([\w.#:\-,>\s]+):hover\s*\{([^}]+)\}', html):
        body = m.group(2)
        # 計算分號分隔的 property 數
        props = [p.strip() for p in body.split(';') if ':' in p and p.strip()]
        # 過濾 transition / cursor（非視覺反饋）
        visual_props = [p for p in props if not re.match(
            r'(transition|cursor|will-change)\b', p.strip()
        )]
        if len(visual_props) > 2:
            count_offenders += 1
    if count_offenders:
        return [("WARN", f"[W-v3-4] {count_offenders} 處 :hover 同時變化 > 2 屬性（v3 建議 ≤ 2）")]
    return []


# ── gen-ai-140h-specific 規則（2026-04-27 Phase 1 互動性改造）───────
# 對應 `courses/gen-ai-140h/_報告/2026-04-27-互動性審核.md` v2 §9.7.1 + §10
# 規則 scope 嚴格篩 'gen-ai-140h' 路徑；其他課程不套。
# 全部 level 設為 WARN，避免擋既有頁面（pre-commit 不擋 WARN）。
# 三條規則簽名為 (path, html) — 與通用規則 (html) 不同；在 lint_file
# 內 dispatch 時會依 callable 簽名選傳參方式。

GEN140_FREE_PRAC = {
    "PRAC5-5", "PRAC5-6", "PRAC5-7", "PRAC5-8",
    "PRAC5-9", "PRAC5-10", "PRAC5-11", "PRAC5-12",
}


def _is_gen140(path: Path) -> bool:
    return "gen-ai-140h" in str(path)


def _is_free_prac(path: Path) -> bool:
    """Part 5 自由演練 PRAC5-5~12（時數/作品集規則豁免）。"""
    stem = path.stem  # 不含 .html
    return stem in GEN140_FREE_PRAC


def check_gen140_duration(path: Path, html: str) -> list:
    """gen140-duration（B-4，§9.1）：gen-ai-140h CH/PRAC 頁面 hero-meta 缺時數標示。
    自由演練 PRAC5-5~12 跳過（時數彈性）。

    實作說明：hero-meta 內含 nested <div>（如 .hero-divider-v），所以不用嚴格
    `(.*?)</div>` 配對；改抓 hero-meta 起點往後 800 字節內含「小時/H/hour」即視為合格。
    """
    if not _is_gen140(path):
        return []
    name = path.name
    if not (name.startswith("CH") or name.startswith("PRAC")):
        return []
    if _is_free_prac(path):
        return []
    # 找 hero-meta 起點
    start = re.search(r'<div[^>]*class="[^"]*\bhero-meta\b[^"]*"[^>]*>', html)
    if not start:
        return [("WARN", f"{path.name}: hero-meta 缺時數標示（B-4）")]
    # 取起點後 800 字（hero-meta 區塊長度上限約 300，留餘裕）
    chunk = html[start.start(): start.start() + 800]
    has_duration = (
        'data-duration' in chunk
        or '小時' in chunk
        or re.search(r'\bhours?\b', chunk, re.IGNORECASE)
        or re.search(r'\b\d+\s*[Hh]\b', chunk)
    )
    if not has_duration:
        return [("WARN", f"{path.name}: hero-meta 缺時數標示（B-4）")]
    return []


def check_gen140_portfolio(path: Path, html: str) -> list:
    """gen140-portfolio（E-2，§3）：gen-ai-140h PRAC 頁缺 .artifact-save 元件。
    自由演練 PRAC5-5~12 跳過。"""
    if not _is_gen140(path):
        return []
    if not path.name.startswith("PRAC"):
        return []
    if _is_free_prac(path):
        return []
    if 'artifact-save' not in html:
        return [("WARN", f"{path.name}: PRAC 頁缺 .artifact-save 元件（E-2）")]
    return []


def check_gen140_iv_script(path: Path, html: str) -> list:
    """gen140-iv-script（§3 共用資產）：gen-ai-140h 頁面缺 interactivity-v1.js script 引用。
    例外：index.html（landing）、my-portfolio.html（已內含 logic）。"""
    if not _is_gen140(path):
        return []
    if path.name in ("index.html", "my-portfolio.html"):
        return []
    if 'interactivity-v1.js' not in html:
        return [("WARN", f"{path.name}: 缺 interactivity-v1.js script 引用")]
    return []


def check_gen140_density(path: Path, html: str) -> list:
    """gen140-interactivity-density（§10.2 Codex 補）：gen-ai-140h 主課頁面互動密度過低。

    加權公式（每實例分數）：
      debug-loop=5；real-task-rewrite/evidence-submit/sp-builder/mini-deliverable=4；
      artifact-save/instructor-check/ai-recycler/case-rubric/result-compare/gallery-walk=3；
      inline-reflection/peer-handoff=2；lone checkbox=1。

    期望門檻：
      - PRAC 主課：score ≥ 8 × duration_h
      - CH 主課：  score ≥ 5 × duration_h
      - 自由演練 PRAC5-5~12 / 入口頁不檢查
    不達標觸發 WARN（不擋）。
    """
    if not _is_gen140(path):
        return []
    if _is_free_prac(path):
        return []
    name = path.name
    # 入口/儀表頁不檢查
    if name in {"index.html", "my-portfolio.html", "my-progress.html",
                "pre-test.html", "ENV-SETUP.html"}:
        return []
    # 只看 CH/PRAC 主課
    if not (name.startswith("CH") or name.startswith("PRAC")):
        return []
    # 抽 data-duration（無則由 gen140-duration 規則處理，這裡跳過）
    m = re.search(r'data-duration="([0-9.]+)h"', html)
    if not m:
        return []
    try:
        duration = float(m.group(1))
    except ValueError:
        return []
    if duration <= 0:
        return []
    # 加權元件 score
    weights = {
        'inline-reflection': 2,
        'artifact-save': 3,
        'peer-handoff': 2,
        'instructor-check': 3,
        'real-task-rewrite': 4,
        'ai-recycler': 3,
        'evidence-submit': 4,
        'debug-loop': 5,
        'case-rubric': 3,
        'result-compare': 3,
        'gallery-walk': 3,
        'sp-builder': 4,
        'mini-deliverable': 4,
    }
    score = 0
    for cls, w in weights.items():
        # 比對 class="..." 中含目標 class 的實例（允許多 class 共存）
        count = len(re.findall(
            r'class="[^"]*\b' + re.escape(cls) + r'\b[^"]*"', html))
        score += count * w
    is_prac = name.startswith("PRAC")
    per_h = 8 if is_prac else 5
    expected = duration * per_h
    if score < expected:
        kind = "PRAC" if is_prac else "CH"
        return [("WARN",
                 f"{path.name}: 互動密度 score={score} < 期望 {expected:.0f}"
                 f"（標 {duration}h，{kind} 期望每 h ≥ {per_h}）")]
    return []


def check_gen140_track(path: Path, html: str) -> list:
    """gen140-track-value（§10.2 Codex 補）：data-track 屬性值合法性。

    合法值（5 個）：
      - 140h-core / 140h-skip / 180h-extra（§10.2 框架本次新增）
      - basic / advanced（Phase 3.3 DualPath 既有）
    其餘值觸發 WARN（不擋）。
    """
    if not _is_gen140(path):
        return []
    valid = {'140h-core', '140h-skip', '180h-extra', 'basic', 'advanced'}
    issues = []
    for v in re.findall(r'data-track="([^"]*)"', html):
        if v not in valid:
            issues.append((
                "WARN",
                f"{path.name}: data-track=\"{v}\" 不合法（合法：{sorted(valid)}）"
            ))
    return issues


def check_gen140_widget_after_nav(path: Path, html: str) -> list:
    """gen140-widget-after-nav（PR-4 結構債防護）：7 個內容 widget class 不應出現在
    nav-footer / lesson-nav 之後（即跑出 .lesson-body / .prac-body / <main> wrapper 外）。

    Phase 3.1 同源錯誤：widget 被誤放在 body wrapper 結束之後、layout shell 之間。
    PR #36 (Codex audit 8537bb8f) 修補後加此規則防 regression。

    注意：用 nav-footer 位置作 heuristic，不偵測所有可能的位置錯誤，但 cover Phase 3.1
    同源 pattern（widget 在 nav 之後 = body 已過早結束）。
    """
    if not _is_gen140(path):
        return []

    widget_classes = ['instructor-check', 'artifact-save', 'real-task-rewrite',
                      'evidence-submit', 'debug-loop', 'mini-deliverable', 'result-compare']

    # 找最早的 nav-footer 或 lesson-nav（layout shell 起始）
    nav_match = re.search(r'<(?:div|nav)[^>]*class="(?:nav-footer|lesson-nav)"', html)
    if not nav_match:
        return []

    nav_pos = nav_match.start()
    after_nav = html[nav_pos:]

    issues = []
    for cls in widget_classes:
        widget_pattern = r'<div[^>]*class="(?:[^"]*\s)?' + re.escape(cls) + r'(?:\s[^"]*)?"'
        if re.search(widget_pattern, after_nav):
            issues.append((
                "WARN",
                f"{path.name}: widget '.{cls}' 出現在 nav-footer/lesson-nav 之後 — "
                f"應放在 .lesson-body / .prac-body / <main> 內（PR-4 結構債防護）"
            ))

    return issues


GEN140_RULES = [
    check_gen140_duration,
    check_gen140_portfolio,
    check_gen140_iv_script,
    check_gen140_density,
    check_gen140_track,
    check_gen140_widget_after_nav,
]


# ── 規則套用 ──────────────────────────────────────────────

# 頁型 → 應套用的規則集
# V3 規則共用集（不含 W-v3-2，因為 W-v3-2 依頁型 dispatch 嚴格/放寬版本）
V3_RULES_COMMON = [
    check_v3_lesson_title_br, check_v3_section_eyebrow_format, check_v3_callout_variants,
    check_v3_prefers_reduced_motion, check_v3_progressbar_aria, check_v3_aria_hidden_icons,
    check_v3_hardcoded_max_width,
    check_v3_section_heading_em_color, check_v3_hover_complexity,
]
# V3_RULES：legacy alias（外部可能引用），non-dispatch source。
# 真正的 dispatch 在下方 RULES_BY_TYPE，會依頁型選 strict 或 relaxed 版的 W-v3-2。
# 修 lint 規則時請動 V3_RULES_COMMON / RULES_BY_TYPE，不要改本變數。
V3_RULES = V3_RULES_COMMON + [check_v3_main_color_count]

RULES_BY_TYPE = {
    "lesson": [
        # BLOCKER
        check_box_shadow, check_custom_color_vars, check_banned_components,
        check_gradient, check_grid_autofit, check_border_radius_max,
        # ERROR
        check_skip_link, check_main_wrapper, check_seo_meta,
        # WARN
        check_twitter_meta, check_platform_metadata, check_focus_visible,
        check_you_form, check_step_n, check_aria_hidden_arrow, check_font_size_tier,
        check_lesson_section_count, check_big_quote_cap, check_callout_cap,
        # v3（追加，不取代）— W-v3-2 用嚴格版（≤ 4）
        *V3_RULES_COMMON, check_v3_main_color_count,
    ],
    "prac": None,  # legacy；classify() 已把 prac* 直接歸 lesson，此分支實際不會被命中
    "module": [
        check_box_shadow, check_custom_color_vars, check_banned_components,
        check_gradient, check_grid_autofit, check_border_radius_max,
        check_skip_link, check_main_wrapper, check_seo_meta,
        check_twitter_meta, check_focus_visible,
        *V3_RULES_COMMON, check_v3_main_color_count,  # 嚴格版
    ],
    "course-index": [
        check_box_shadow, check_custom_color_vars, check_gradient,
        check_border_radius_max,
        check_skip_link, check_main_wrapper, check_seo_meta,
        check_twitter_meta, check_focus_visible,
        *V3_RULES_COMMON, check_v3_main_color_count_index,  # 放寬版（≤ 30）
    ],
    "root": [
        check_box_shadow, check_custom_color_vars, check_gradient,
        check_border_radius_max,
        check_skip_link, check_main_wrapper, check_seo_meta, check_twitter_meta,
        *V3_RULES_COMMON, check_v3_main_color_count_index,  # 放寬版（≤ 30）
    ],
    "search": [
        check_box_shadow, check_custom_color_vars, check_gradient,
        check_border_radius_max,
        check_skip_link, check_main_wrapper,
    ],
    "other": [
        check_box_shadow, check_custom_color_vars, check_gradient,
        check_border_radius_max,
    ],
}


def lint_file(path: Path) -> list:
    """回傳該檔的 [(severity, msg), ...]。"""
    kind = classify(path)
    rules = RULES_BY_TYPE.get(kind, RULES_BY_TYPE["other"])
    if rules is None:
        rules = RULES_BY_TYPE["lesson"]
    html = read(path)
    issues = []
    for rule in rules:
        try:
            issues.extend(rule(html))
        except Exception as e:
            issues.append(("WARN", f"規則 {rule.__name__} 執行失敗: {e}"))
    # gen-ai-140h-specific 規則（path-aware；自帶 scope 篩，不套其他課程）
    for rule in GEN140_RULES:
        try:
            issues.extend(rule(path, html))
        except Exception as e:
            issues.append(("WARN", f"規則 {rule.__name__} 執行失敗: {e}"))
    return issues


# ── Baseline（允許舊違規 grandfather）──────────────────────

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix() if path.is_absolute() else str(path)


def _is_v3_msg(msg: str) -> bool:
    """判斷一條 issue 訊息是否為 v3 規則（訊息以 [B-v3-N]/[E-v3-N]/[W-v3-N] 開頭）"""
    return bool(re.match(r'^\[([BEW]-v3-\d+)\]', msg))


def load_baseline() -> dict:
    """回傳 {relpath: [{"severity": str, "msg": str}, ...]}"""
    if not BASELINE_PATH.exists():
        return {}
    try:
        return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_baseline(data: dict):
    BASELINE_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def filter_against_baseline(relpath: str, issues: list, baseline: dict) -> tuple:
    """回傳 (shown_issues, grandfathered_count)。完全相符 (severity, msg) 的違規會被壓掉。"""
    known = baseline.get(relpath, [])
    known_set = {(k["severity"], k["msg"]) for k in known}
    shown = []
    grandfathered = 0
    for sev, msg in issues:
        if (sev, msg) in known_set:
            grandfathered += 1
        else:
            shown.append((sev, msg))
    return shown, grandfathered


def build_baseline_snapshot(files: list) -> dict:
    """掃所有檔，回傳完整 baseline dict。"""
    snapshot = {}
    for f in files:
        issues = lint_file(f)
        if issues:
            snapshot[rel(f)] = [{"severity": s, "msg": m} for s, m in issues]
    return snapshot


def audit_baseline(files: list, baseline: dict) -> list:
    """找出 baseline 內已不存在的條目（違規已被修復，應該從 baseline 移除）。"""
    stale = []
    current = build_baseline_snapshot(files)
    for relpath, items in baseline.items():
        current_items = current.get(relpath, [])
        current_set = {(c["severity"], c["msg"]) for c in current_items}
        for item in items:
            if (item["severity"], item["msg"]) not in current_set:
                stale.append((relpath, item["severity"], item["msg"]))
    return stale


# ── CLI ──────────────────────────────────────────────────

def collect_files(args) -> list:
    files = []
    if args.all:
        for p in ROOT.rglob("*.html"):
            rel = p.relative_to(ROOT).as_posix()
            if any(part.startswith("_backup") or part.startswith("_pilots") for part in p.parts):
                continue
            if "node_modules" in p.parts or ".git" in p.parts:
                continue
            files.append(p)
    elif args.changed:
        try:
            out = subprocess.check_output(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                cwd=ROOT, text=True
            )
            for line in out.splitlines():
                if line.endswith(".html"):
                    f = ROOT / line
                    if f.exists():
                        files.append(f)
        except subprocess.CalledProcessError:
            pass
    elif args.paths:
        for pat in args.paths:
            p = Path(pat)
            if not p.is_absolute():
                p = ROOT / p
            if p.is_dir():
                files.extend(p.rglob("*.html"))
            elif p.is_file():
                files.append(p)
    return [f for f in files if not any(part.startswith("_backup") for part in f.parts)]


def main():
    ap = argparse.ArgumentParser(description="課程頁面合規檢查")
    ap.add_argument("paths", nargs="*", help="檔案或目錄路徑")
    ap.add_argument("--all", action="store_true", help="掃全站")
    ap.add_argument("--changed", action="store_true", help="只掃 git staged 的 HTML（pre-commit 用）")
    ap.add_argument("--summary", action="store_true", help="只印統計摘要")
    ap.add_argument("--by-bucket", action="store_true",
                    help="WARN 依類別分桶統計（migration-debt / structural / metadata / a11y / motion / v3-misc / other）")
    ap.add_argument("--no-warn", action="store_true", help="不顯示 WARN 級別")
    ap.add_argument("--baseline", action="store_true",
                    help="套用 baseline（舊違規忽略、新違規照舊 BLOCKER）")
    ap.add_argument("--write-baseline", action="store_true",
                    help="把當前所有違規寫入 baseline（慎用，視同承認技術債）")
    ap.add_argument("--audit-baseline", action="store_true",
                    help="列出 baseline 中已被修復、可移除的條目")
    ap.add_argument("--v3-soft", action="store_true",
                    help="v3 規則降級：B-v3-* → WARN、E-v3-* → WARN（舊課 migration 寬容模式）")
    ap.add_argument("--v3-baseline", action="store_true",
                    help="套用 .lint-baseline-v3.json（過渡期允許特定頁免責）")
    ap.add_argument("--write-v3-baseline", action="store_true",
                    help="把當前 v3 違規寫入 .lint-baseline-v3.json")
    args = ap.parse_args()

    # --write-baseline / --audit-baseline / --write-v3-baseline 強制對全站操作
    if args.write_baseline or args.audit_baseline or args.write_v3_baseline:
        args.all = True

    if not (args.all or args.changed or args.paths):
        ap.print_help()
        sys.exit(2)

    files = collect_files(args)
    if not files:
        print("無符合條件的 HTML 檔案")
        sys.exit(0)

    # --write-baseline 分支：建檔、存檔、離開
    if args.write_baseline:
        snapshot = build_baseline_snapshot(files)
        save_baseline(snapshot)
        total = sum(len(v) for v in snapshot.values())
        print(f"✅ 已寫入 baseline：{BASELINE_PATH.relative_to(ROOT)}")
        print(f"   · {len(snapshot)} 檔、{total} 條違規")
        print(f"\n下次跑 `--baseline` 這些條目會被壓掉，只顯示新增違規。")
        sys.exit(0)

    # --audit-baseline 分支：列 stale、離開
    if args.audit_baseline:
        baseline = load_baseline()
        if not baseline:
            print("⚠ baseline 不存在，無需稽核")
            sys.exit(0)
        stale = audit_baseline(files, baseline)
        if not stale:
            print("✅ baseline 無過期條目（全部仍觸發）")
            sys.exit(0)
        print(f"📋 baseline 有 {len(stale)} 條已修復、建議移除：\n")
        by_file: dict = {}
        for relpath, sev, msg in stale:
            by_file.setdefault(relpath, []).append((sev, msg))
        for relpath in sorted(by_file):
            print(f"📄 {relpath}")
            for sev, msg in by_file[relpath]:
                print(f"  · [{sev}] {msg}")
        print(f"\n建議：`python3 docs/lint-page.py --write-baseline` 重建（會順手清掉過期條目）")
        sys.exit(0)

    baseline = load_baseline() if args.baseline else {}
    v3_baseline = {}
    if args.v3_baseline and BASELINE_V3_PATH.exists():
        try:
            v3_baseline = json.loads(BASELINE_V3_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            v3_baseline = {}

    # --write-v3-baseline：蒐集目前所有 v3 違規寫入
    if args.write_v3_baseline:
        snapshot = {}
        for f in sorted(files):
            issues = lint_file(f)
            v3_issues = [(s, m) for s, m in issues if _is_v3_msg(m)]
            if v3_issues:
                snapshot[rel(f)] = [{"severity": s, "msg": m} for s, m in v3_issues]
        BASELINE_V3_PATH.write_text(
            json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        total = sum(len(v) for v in snapshot.values())
        print(f"✅ 已寫入 v3 baseline：{BASELINE_V3_PATH.relative_to(ROOT)}")
        print(f"   · {len(snapshot)} 檔、{total} 條 v3 違規")
        sys.exit(0)

    total_blocker = total_error = total_warn = 0
    total_grandfathered = 0
    files_with_blocker = []
    details = []
    bucket_counts = {}  # bucket → count（--by-bucket 用）
    bucket_files = {}   # bucket → set of relpath（--by-bucket 用）

    for f in sorted(files):
        issues = lint_file(f)
        if args.baseline:
            relpath = f.relative_to(ROOT).as_posix() if f.is_absolute() else str(f)
            issues, g = filter_against_baseline(relpath, issues, baseline)
            total_grandfathered += g
        # v3-baseline 過濾（僅壓 v3 違規）
        if args.v3_baseline and v3_baseline:
            relpath = f.relative_to(ROOT).as_posix() if f.is_absolute() else str(f)
            issues, g = filter_against_baseline(relpath, issues, v3_baseline)
            total_grandfathered += g
        # v3-soft 降級：把 v3 的 BLOCKER/ERROR 降為 WARN
        if args.v3_soft:
            issues = [
                ("WARN", m) if _is_v3_msg(m) and s in ("BLOCKER", "ERROR") else (s, m)
                for s, m in issues
            ]
        b = sum(1 for s, _ in issues if s == "BLOCKER")
        e = sum(1 for s, _ in issues if s == "ERROR")
        w = sum(1 for s, _ in issues if s == "WARN")
        total_blocker += b
        total_error += e
        total_warn += w
        if b > 0:
            files_with_blocker.append(f)
        # --by-bucket 累積
        if args.by_bucket:
            relpath = f.relative_to(ROOT).as_posix() if f.is_absolute() else str(f)
            for sev, msg in issues:
                if sev == "WARN":
                    bk = bucket_of(msg)
                    bucket_counts[bk] = bucket_counts.get(bk, 0) + 1
                    bucket_files.setdefault(bk, set()).add(relpath)
        if issues and not args.summary:
            relpath = f.relative_to(ROOT).as_posix() if f.is_absolute() else str(f)
            details.append((relpath, issues))

    if not args.summary:
        for relpath, issues in details:
            visible = [i for i in issues if not (args.no_warn and i[0] == "WARN")]
            if not visible:
                continue
            print(f"\n📄 {relpath}")
            for sev, msg in visible:
                icon = {"BLOCKER": "❌", "ERROR": "⚠️", "WARN": "·"}[sev]
                print(f"  {icon} [{sev}] {msg}")

    print(f"\n═══ 摘要 ═══")
    print(f"掃描：{len(files)} 頁")
    print(f"BLOCKER：{total_blocker} 條（{len(files_with_blocker)} 檔）")
    print(f"ERROR：  {total_error} 條")
    if not args.no_warn:
        print(f"WARN：   {total_warn} 條")
    if args.baseline and total_grandfathered:
        print(f"baseline 壓掉：{total_grandfathered} 條（舊違規、先留）")

    if args.by_bucket and bucket_counts:
        print(f"\n═══ WARN 分桶 ═══")
        for bk, c in sorted(bucket_counts.items(), key=lambda x: -x[1]):
            n_files = len(bucket_files.get(bk, set()))
            print(f"  {bk:<18} {c:>5} 條 · 跨 {n_files} 檔")

    if total_blocker > 0:
        print("\n❌ 有 BLOCKER，不可放行。")
        sys.exit(1)
    print("\n✅ 無 BLOCKER。")
    sys.exit(0)


if __name__ == "__main__":
    main()
