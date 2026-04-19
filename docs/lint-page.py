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
    matches = re.findall(r'--c-a([6-9]|\d{2,})\b', html)
    if matches:
        issues.append(("BLOCKER", f"自創 --c-a{matches[0]}+ 變數（禁止，只允許 a1-a5）"))
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
    """箭頭 ← / → 應包 aria-hidden。"""
    issues = []
    # 找文字中的箭頭但未在 aria-hidden span 內
    pattern = r'[←→](?![^<]*aria-hidden)'
    # 簡化檢查：若箭頭出現但沒 aria-hidden="true" 在同行附近
    lines = html.split('\n')
    offenders = 0
    for line in lines:
        if re.search(r'[←→]', line) and 'aria-hidden' not in line:
            offenders += 1
    if offenders > 0:
        return [("WARN", f"{offenders} 行含箭頭但無 aria-hidden（a11y）")]
    return issues


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
    """檢測非 8 階字型值。"""
    allowed = {"2rem", "1.45rem", "1.2rem", "1.1rem", "1.05rem",
               ".92rem", "0.92rem", ".85rem", "0.85rem", ".7rem", "0.7rem",
               # 實務常見不標準但暫容許的
               ".8rem", "0.8rem", ".9rem", "0.9rem", "1rem",
               ".75rem", "0.75rem", ".78rem", "0.78rem", ".76rem", "0.76rem",
               ".68rem", "0.68rem", ".73rem", "0.73rem"}
    # 抓所有 font-size: Xrem
    matches = re.findall(r'font-size\s*:\s*([\d.]+rem)', html)
    bad = [m for m in matches if m not in allowed]
    if bad:
        unique = sorted(set(bad))
        if len(unique) > 3:
            return [("WARN", f"非標準 font-size 階（8 階外）：{', '.join(unique[:3])} 等 {len(unique)} 個")]
        return [("WARN", f"非標準 font-size 階（8 階外）：{', '.join(unique)}")]
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


def check_v3_main_color_count(html: str) -> list:
    """W-v3-2: --c-main 出現次數 > 4 → WARN（僅計 CSS 內引用）"""
    style_match = re.search(r'<style[^>]*>(.*?)</style>', html, re.S)
    if not style_match:
        return []
    style = style_match.group(1)
    count = len(re.findall(r'var\s*\(\s*--c-main\s*\)', style))
    if count > 4:
        return [("WARN", f"[W-v3-2] --c-main 在 CSS 中出現 {count} 次（v3 建議 ≤ 4）")]
    return []


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


# ── 規則套用 ──────────────────────────────────────────────

# 頁型 → 應套用的規則集
V3_RULES = [
    check_v3_lesson_title_br, check_v3_section_eyebrow_format, check_v3_callout_variants,
    check_v3_prefers_reduced_motion, check_v3_progressbar_aria, check_v3_aria_hidden_icons,
    check_v3_hardcoded_max_width, check_v3_main_color_count,
    check_v3_section_heading_em_color, check_v3_hover_complexity,
]

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
        # v3（追加，不取代）
        *V3_RULES,
    ],
    "prac": None,  # 同 lesson
    "module": [
        check_box_shadow, check_custom_color_vars, check_banned_components,
        check_gradient, check_grid_autofit, check_border_radius_max,
        check_skip_link, check_main_wrapper, check_seo_meta,
        check_twitter_meta, check_focus_visible,
        *V3_RULES,
    ],
    "course-index": [
        check_box_shadow, check_custom_color_vars, check_gradient,
        check_border_radius_max,
        check_skip_link, check_main_wrapper, check_seo_meta,
        check_twitter_meta, check_focus_visible,
        *V3_RULES,
    ],
    "root": [
        check_box_shadow, check_custom_color_vars, check_gradient,
        check_border_radius_max,
        check_skip_link, check_main_wrapper, check_seo_meta, check_twitter_meta,
        *V3_RULES,
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
            if any(part.startswith("_backup") for part in p.parts):
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

    if total_blocker > 0:
        print("\n❌ 有 BLOCKER，不可放行。")
        sys.exit(1)
    print("\n✅ 無 BLOCKER。")
    sys.exit(0)


if __name__ == "__main__":
    main()
