"""合併 gen-image 課程所有 HTML，產出單一 Word 講義（v2 排版優化版）。

v2 改動：
- 章節分頁：每個單元 H1 前加上 page-break-before:always，Word 開新頁
- 清掉所有 inline style 與 class（網頁殘留樣式不適合 Word，會反而亂版）
- details 標題改用真正的 H3（pandoc 才會套 Heading 3 樣式 → 自動進目錄）
- 圖片限寬 600px（避免吃掉整頁）
- 移除 figure/figcaption 多餘空白
- 用 reference docx（ref.docx）統一中文字型與行距
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
REFACTOR = ROOT / "_refactor"
OUT_HTML = REFACTOR / "講義-合併.html"
OUT_DOCX = ROOT / "講義-商業用圖片生成.docx"
REF_DOCX = REFACTOR / "ref.docx"
IMG_CACHE = REFACTOR / "img_compressed"  # 壓縮後圖片暫存區
IMG_MAX_WIDTH = 1600  # 圖片最大寬度（px）— Word 列印 A4 約 1600 即足夠
IMG_JPEG_QUALITY = 80

PAGES: list[tuple[str, str]] = [
    ("index.html",   "課程封面"),
    ("CH1-1.html",   "CH 1.1 你不是設計師、你是 AI 的需求方"),
    ("CH1-2.html",   "CH 1.2 三段工作流地圖 + 平台選擇"),
    ("CH2-1.html",   "CH 2.1 商業廣告的 8 種用途版型"),
    ("CH2-2.html",   "CH 2.2 從 brief 到完稿的 prompt 結構"),
    ("PRAC2.html",   "PRAC 2 多主題生圖演練"),
    ("CH3-1.html",   "CH 3.1 線稿反推"),
    ("CH3-2.html",   "CH 3.2 從線稿讀出結構語言"),
    ("PRAC3.html",   "PRAC 3 線稿反推演練"),
    ("CH4-1.html",   "CH 4.1 同線稿 × 跨產業套用"),
    ("CH4-2.html",   "CH 4.2 同線稿 × 多變體"),
    ("CH4-3.html",   "CH 4.3 同款品牌、3 張系列也像同個牌子"),
    ("PRAC4.html",   "PRAC 4 品牌系列演練"),
    ("CH5-1.html",   "CH 5.1 從 brief 到品牌系列整合實戰"),
]

STRIP_SELECTORS = [
    "header.topbar", ".topbar",
    "footer.footer", ".footer",
    ".skip-link",
    "nav.lesson-nav", ".lesson-nav",
    ".back-link", ".prev-next",
    ".password-gate", "#password-gate",
    "script", "noscript", "style", "link", "meta",
]

# 保留的 HTML 屬性（其餘全清，避免 inline style 污染 Word）
KEEP_ATTRS = {"href", "src", "alt", "open", "colspan", "rowspan", "scope", "width"}
KEEP_CLASSES = {"page-break"}  # Lua filter 要靠這個 class 認分頁標記


def strip_decorative_attrs(soup: BeautifulSoup) -> None:
    """清掉所有 inline style/id/data-* 等網頁專用屬性。class 只保留白名單。"""
    for tag in soup.find_all(True):
        for attr in list(tag.attrs.keys()):
            if attr in KEEP_ATTRS:
                continue
            if attr == "class":
                kept_classes = [c for c in tag.attrs.get("class", []) if c in KEEP_CLASSES]
                if kept_classes:
                    tag["class"] = kept_classes
                else:
                    del tag.attrs[attr]
                continue
            del tag.attrs[attr]


def details_to_h3(soup: BeautifulSoup, body: Tag) -> None:
    """details/summary → h3 標題 + 內容區塊（變成正規 Word Heading 3，自動進目錄）"""
    for det in body.find_all("details"):
        summary = det.find("summary")
        h3 = soup.new_tag("h3")
        if summary:
            h3.string = summary.get_text(strip=True)
            summary.decompose()
        else:
            h3.string = "展開內容"
        # 把 details 變成正常段落容器
        wrapper = soup.new_tag("div")
        wrapper.append(h3)
        for child in list(det.children):
            if isinstance(child, Tag):
                wrapper.append(child.extract())
            elif isinstance(child, NavigableString) and str(child).strip():
                wrapper.append(NavigableString(str(child)))
        det.replace_with(wrapper)


# ── 語義化轉換：把 HTML 視覺裝飾改成 Word 看得懂的語義 tag ──
CALLOUT_LABELS = {
    "key":  "【重點】",
    "tip":  "【提示】",
    "info": "【說明】",
    "warn": "【注意】",
    "ok":   "【可以】",
    "ng":   "【不可】",
}


def transform_callouts(soup: BeautifulSoup, body: Tag) -> None:
    """.callout.{key,tip,info,...} → <blockquote><strong>【類型】</strong> ...</blockquote>"""
    for el in body.select(".callout"):
        classes = el.get("class", []) or []
        kind = next((c for c in classes if c in CALLOUT_LABELS), None)
        label = CALLOUT_LABELS.get(kind, "【提示】")

        bq = soup.new_tag("blockquote")
        prefix = soup.new_tag("strong")
        prefix.string = f"{label} "
        bq.append(prefix)

        body_el = el.select_one(".callout-body") or el
        # 拿掉 callout-icon
        for icon in body_el.select(".callout-icon"):
            icon.decompose()
        for child in list(body_el.children):
            if isinstance(child, Tag):
                bq.append(child.extract())
            elif isinstance(child, NavigableString) and str(child).strip():
                bq.append(NavigableString(str(child)))
        el.replace_with(bq)


def transform_asides(soup: BeautifulSoup, body: Tag) -> None:
    """.aside-tip / .step-tip / .today-deliverables-note → blockquote（如果還不是的話）"""
    for sel, label in [
        (".aside-tip", "【補充】"),
        (".step-tip", "【步驟提示】"),
        (".today-deliverables-note", "【今日交付】"),
    ]:
        for el in body.select(sel):
            # 已經是 blockquote 就只加 prefix
            if el.name == "blockquote":
                # 第一個 child 之前插 strong 標籤
                first_strong = el.find("strong")
                # 若已經有 <strong> 開頭，不重複加 label
                already = first_strong and first_strong.get_text(strip=True).startswith(label[1:-1])
                if not already:
                    pref = soup.new_tag("strong")
                    pref.string = f"{label} "
                    el.insert(0, pref)
                continue
            bq = soup.new_tag("blockquote")
            pref = soup.new_tag("strong")
            pref.string = f"{label} "
            bq.append(pref)
            for child in list(el.children):
                if isinstance(child, Tag):
                    bq.append(child.extract())
                elif isinstance(child, NavigableString) and str(child).strip():
                    bq.append(NavigableString(str(child)))
            el.replace_with(bq)


def transform_quotes_and_prompts(soup: BeautifulSoup, body: Tag) -> None:
    """type-quote → blockquote；code-block / pre 維持 <pre>（Word 會用等寬字）"""
    for el in body.select(".type-quote"):
        bq = soup.new_tag("blockquote")
        em = soup.new_tag("em")
        em.string = el.get_text(strip=True)
        bq.append(em)
        el.replace_with(bq)
    # pre 已是 pre，無需轉換；但確保 .code-block 變 pre
    for el in body.find_all("pre"):
        # 移除所有屬性，保留為純 pre（Word 套 Code Block 樣式）
        attrs_to_keep = {}
        el.attrs = attrs_to_keep


def transform_card_titles(soup: BeautifulSoup, body: Tag) -> None:
    """tool-card / type-card 內的小標 → 變 H4，提供層次"""
    for sel in [".tool-card-title", ".type-card-title", ".version-title"]:
        for el in body.select(sel):
            h = soup.new_tag("h4")
            h.string = el.get_text(strip=True)
            el.replace_with(h)


def remove_decorative_dividers(soup: BeautifulSoup, body: Tag) -> None:
    """純裝飾的 divider（type-divider 等）刪除，避免 Word 出現一堆細線。"""
    for sel in [".type-divider", ".section-divider", ".part-line"]:
        for el in body.select(sel):
            el.decompose()


def compress_image(src_path: Path) -> Path:
    """把單張圖縮到 IMG_MAX_WIDTH，存到快取目錄，回傳新路徑。"""
    IMG_CACHE.mkdir(exist_ok=True)
    out = IMG_CACHE / src_path.name
    if out.exists() and out.stat().st_mtime >= src_path.stat().st_mtime:
        return out
    with Image.open(src_path) as im:
        im = im.convert("RGB") if im.mode in ("RGBA", "P") else im
        if im.width > IMG_MAX_WIDTH:
            ratio = IMG_MAX_WIDTH / im.width
            im = im.resize((IMG_MAX_WIDTH, int(im.height * ratio)), Image.LANCZOS)
        # 一律存成 JPEG（Word 對 JPEG 內建壓縮較友善）
        out_jpg = out.with_suffix(".jpg")
        im.save(out_jpg, "JPEG", quality=IMG_JPEG_QUALITY, optimize=True)
        return out_jpg


def normalize_images(soup: BeautifulSoup, body: Tag) -> None:
    """圖片：壓縮 + 改絕對路徑 + 限寬"""
    for img in body.find_all("img"):
        src = img.get("src", "")
        if src.startswith("img/"):
            src_path = ROOT / src
            if src_path.exists():
                compressed = compress_image(src_path)
                img["src"] = str(compressed.resolve())
            else:
                img["src"] = str(src_path.resolve())
        img["width"] = "600"


def clean_page(html_path: Path, page_title: str, is_first: bool) -> str:
    raw = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    body = soup.body or soup

    for sel in STRIP_SELECTORS:
        for el in body.select(sel):
            el.decompose()

    # 語義化（必須在 strip_decorative_attrs 之前，因為要靠 class 識別）
    transform_callouts(soup, body)
    transform_asides(soup, body)
    transform_quotes_and_prompts(soup, body)
    transform_card_titles(soup, body)
    remove_decorative_dividers(soup, body)

    details_to_h3(soup, body)
    normalize_images(soup, body)
    strip_decorative_attrs(soup)

    # 章節分頁：除了第一頁，先放一個 <hr>（Lua filter 會轉成 Word 分頁）
    page_h1 = soup.new_tag("h1")
    page_h1.string = page_title

    main = body.find("main") or body
    fragment = BeautifulSoup("<div></div>", "html.parser")
    section = fragment.div
    if not is_first:
        # Lua filter 會把 class="page-break" 的 div 轉成 Word 分頁
        pb = soup.new_tag("div")
        pb["class"] = "page-break"
        section.append(pb)
    section.append(page_h1)
    for child in list(main.children):
        if isinstance(child, Tag) and child.name in ("script", "style"):
            continue
        if isinstance(child, Tag):
            section.append(child.extract())
        elif isinstance(child, NavigableString) and str(child).strip():
            section.append(NavigableString(str(child)))

    # 把 H1 之外的網頁標題降一級（避免目錄出現多個 H1）
    # body 內原本若有 H1（hero-title），降為 H2
    for inner_h1 in section.find_all("h1"):
        if inner_h1 is page_h1:
            continue
        inner_h1.name = "h2"

    return str(fragment)


def build_combined() -> Path:
    parts = []
    for i, (fname, title) in enumerate(PAGES):
        path = ROOT / fname
        if not path.exists():
            print(f"⚠️ 缺檔：{fname}", file=sys.stderr)
            continue
        print(f"  · {fname} → {title}")
        parts.append(clean_page(path, title, is_first=(i == 0)))

    combined = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head><meta charset="UTF-8"><title>商業用圖片生成｜講義</title></head>
<body>
<h1>商業用圖片生成</h1>
<p>弄一下工作室 · 課程講義（Word 合併版）</p>
<p>本檔由 14 個課程頁面合併產生，每個單元自成一頁。</p>
{''.join(parts)}
</body>
</html>
"""
    OUT_HTML.write_text(combined, encoding="utf-8")
    return OUT_HTML


def ensure_reference_docx() -> Path | None:
    """產生（或重用）reference docx，套用中文友善字型與行距。"""
    if REF_DOCX.exists():
        return REF_DOCX
    # 用 pandoc --print-default-data-file 拿預設 reference.docx 當底
    try:
        proc = subprocess.run(
            ["pandoc", "-o", str(REF_DOCX), "--print-default-data-file", "reference.docx"],
            check=True, capture_output=True,
        )
        # 上面那個寫法不會輸出檔案，改用：
        REF_DOCX.unlink(missing_ok=True)
        with open(REF_DOCX, "wb") as f:
            data = subprocess.run(
                ["pandoc", "--print-default-data-file", "reference.docx"],
                check=True, capture_output=True,
            ).stdout
            f.write(data)
        return REF_DOCX
    except subprocess.CalledProcessError:
        return None


def to_docx(html_path: Path) -> Path:
    lua_filter = REFACTOR / "page_break.lua"
    cmd = [
        "pandoc",
        str(html_path),
        "-o", str(OUT_DOCX),
        "--from", "html+raw_html+native_divs+native_spans",
        "--to", "docx",
        "--resource-path", str(ROOT),
        "--toc",
        "--toc-depth=2",
        "--standalone",
    ]
    if lua_filter.exists():
        cmd += ["--lua-filter", str(lua_filter)]
    ref = ensure_reference_docx()
    if ref and ref.exists() and ref.stat().st_size > 0:
        cmd += ["--reference-doc", str(ref)]
    print("執行：", " ".join(cmd))
    subprocess.run(cmd, check=True)
    return OUT_DOCX


if __name__ == "__main__":
    print("== 合併 HTML ==")
    html = build_combined()
    print(f"  → {html}")
    print("== 轉 Word ==")
    docx = to_docx(html)
    print(f"  → {docx}")
    print(f"\n✅ 完成：{docx}")
