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
    }
}

# ── 注入的 @media print CSS（紙本友善）───────────────────────────
PRINT_CSS = """
<style>
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
@media print {
  html, body { background:#fff !important; }
  body { font-size:11pt; line-height:1.72; }
  .topbar, .progress-strip, .section-dots,
  .back-link, .lesson-nav, .footer, .copy-btn,
  .copy-row, script { display:none !important; }
  .lesson-hero { padding:24px 0 20px !important; max-width:none !important; }
  .lesson-body { padding:0 !important; max-width:none !important; }
  .lesson-title { font-size:22pt !important; page-break-after:avoid; }
  .section-heading { font-size:14pt !important; page-break-after:avoid; }
  .lesson-section { page-break-inside:auto; margin-bottom:32px !important; }
  .callout, .code-block, pre, .scenario-grid, .tool-grid,
  .compare-grid, .compare-card, details, .prac-sample,
  .material-block, .output-fold, .qa-item {
    page-break-inside:avoid;
  }
  details { margin:14px 0 !important; }
  details > summary { cursor:default !important; }
  a { color:#333 !important; text-decoration:none !important; }
  .code-block, pre { background:#f2f0ea !important; color:#222 !important;
    border:1px solid #d0ccc2 !important; font-size:9.5pt !important; }
  input[type="radio"], input[type="checkbox"] { display:none !important; }
  .quiz-opt::before { content:"○ "; color:#888; margin-right:4px; }
  .quiz-item { page-break-inside:avoid; margin:14px 0; }
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

    # 5) 移除 copy-btn（.copy-btn / .copy-row）
    for sel in [".copy-btn", ".copy-row"]:
        for el in soup.select(sel):
            el.decompose()

    # 6) 移除 quiz radio input（label 保留）
    for el in soup.select('input[type="radio"]'):
        el.decompose()
    for el in soup.select('input[type="checkbox"]'):
        el.decompose()

    # 7) 注入 @media print CSS（放在 </head> 前）
    head = soup.find("head")
    if head:
        head.append(BeautifulSoup(PRINT_CSS, "html.parser"))

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
</style>
</head>
<body>
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
