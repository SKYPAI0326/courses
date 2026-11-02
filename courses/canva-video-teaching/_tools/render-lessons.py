"""把 _lessons/canva-video-teaching/ 的學員正文轉成單元頁 HTML，保留既有外殼。

用法（在 repo 根目錄）：
python3 courses/canva-video-teaching/_tools/render-lessons.py CH1-1 CH1-2 ...
python3 courses/canva-video-teaching/_tools/render-lessons.py --out <資料夾> CH1-2   # 試轉到複本，不動正式檔

正文轉製沿用 _repair/2026-10-27-multitrack-mainline/sync_repair.py 的 render_body。
learner-content 段開頭的「# 標題／副標／本節完成物」三行轉成頁首；其餘開場段併進第一節。
同步更新頁首標題、meta、時數、總覽與場次頁卡片、課程搜尋索引中該頁的條目；不重建下載包。
"""
from pathlib import Path
from urllib.parse import unquote
import hashlib
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from bs4.dammit import EntitySubstitution
from bs4.formatter import HTMLFormatter
from markdown_it import MarkdownIt
from PIL import Image
import yaml

COURSE = Path(__file__).resolve().parents[1]
REPO = COURSE.parent.parent
SLUG = "canva-video-teaching"
MD = MarkdownIt("commonmark", {"html": True, "breaks": True}).enable("table")
LESSON_IDS = [f"CH1-{n}" for n in range(1, 6)] + ["CH2-1", "CH2-2", "CH3-1", "CH3-2"]  # v8（2026-11-02）
COURSE_NAME = "Canva 影片快速上手"


class KeepOrder(HTMLFormatter):
    def attributes(self, tag):  # 保留原屬性順序，lint 的 SEO meta 檢查依 name／property 在前判斷
        return tag.attrs.items()


def html(soup):
    return soup.decode(formatter=KeepOrder(entity_substitution=EntitySubstitution.substitute_xml))


def unit_source(unit_id):
    return REPO / "_lessons" / SLUG / f"{unit_id}.md"


def unit_page(unit_id):
    return COURSE / f"ch{unit_id[2]}" / f"{unit_id}.html"


ALL_MAP = {str(unit_source(u).resolve()): unit_page(u) for u in LESSON_IDS}
for path in (COURSE / "resources").glob("*.md"):
    ALL_MAP[str(path.resolve())] = path.with_suffix(".html")


def rel(target, page):
    return os.path.relpath(target, page.parent).replace(os.sep, "/")


def linkfix(url, source, page):
    if url.startswith(("http:", "https:", "mailto:", "data:", "#")):
        return url
    path, sep, anchor = url.partition("#")
    target = (source.parent / unquote(path)).resolve()
    output = ALL_MAP.get(str(target), target)
    return rel(output, page) + ((sep + anchor) if sep else "")


def is_parallel_reference(url):
    clean = url.split("#", 1)[0].split("?", 1)[0].lower()
    return url.startswith(("http:", "https:")) or clean.endswith((".html", ".mp4", ".wav", ".pdf"))


def render_body(text, source, page):
    frag = BeautifulSoup(MD.render(text), "html.parser")
    heading = frag.find("h1")
    if heading:
        heading.decompose()
    for element in frag.find_all(["a", "img", "video", "source"]):
        for attribute in ("href", "src", "poster"):
            if element.get(attribute):
                element[attribute] = linkfix(element[attribute], source, page)
                if element.name in ("img", "source") and attribute == "src" and not element[attribute].startswith(("http:", "https:", "data:")):
                    asset = (page.parent / element[attribute]).resolve()
                    if asset.is_file():
                        element[attribute] += "?v=" + hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
        if element.name == "a" and is_parallel_reference(element.get("href", "")):
            element["target"] = "_blank"
            element["rel"] = "noopener noreferrer"
            element["title"] = "另開新分頁"
            label = element.get_text(" ", strip=True)
            if label:
                element["aria-label"] = label + "（另開新分頁）"
    for paragraph in frag.find_all("p"):
        paragraph["class"] = ["body-text"]
    for table in frag.find_all("table"):
        table["class"] = ["lesson-table"]
        wrapper = frag.new_tag("div", attrs={"class": "table-scroll", "tabindex": "0", "aria-label": "表格，可向左右捲動"})
        table.wrap(wrapper)
    for listing in frag.find_all(["ul", "ol"]):
        listing["class"] = ["step-list"]
    for block in frag.find_all("pre"):
        block["class"] = ["code-block"]
    for subheading in frag.find_all("h3"):
        subheading["class"] = ["subheading"]
    for image in frag.find_all("img"):
        image_path = (page.parent / unquote(image.get("src", "").split("?", 1)[0])).resolve()
        if image_path.is_file():
            if image_path.suffix.lower() == ".svg":
                box = ET.fromstring(image_path.read_text()).get("viewBox", "").split()
                if len(box) == 4:
                    image["width"], image["height"] = str(round(float(box[2]))), str(round(float(box[3])))
            else:
                with Image.open(image_path) as dimensions:
                    image["width"], image["height"] = str(dimensions.width), str(dimensions.height)
        image["loading"] = "lazy"
        parent = image.parent
        if parent.name == "p" and len(parent.find_all(recursive=False)) == 1:
            parent.name = "figure"
            parent["class"] = ["lesson-figure"]
            caption = frag.new_tag("figcaption")
            caption.string = image.get("alt", "")
            parent.append(caption)
    body = frag.new_tag("div", attrs={"class": "lesson-body"})
    current = None
    count = 0
    for element in list(frag.contents):
        if isinstance(element, str) and not element.strip():
            continue
        if current is None or getattr(element, "name", None) == "h2":
            count += 1
            current = frag.new_tag("section", attrs={"class": "lesson-section", "id": f"section-{count}"})
            eyebrow = frag.new_tag("div", attrs={"class": "section-eyebrow"})
            eyebrow.string = f"({count:02})"
            current.append(eyebrow)
            body.append(current)
            if getattr(element, "name", None) != "h2":
                generated = frag.new_tag("h2", attrs={"class": "section-heading"})
                generated.string = "準備開始"
                current.append(generated)
        if getattr(element, "name", None) == "h2":
            element["class"] = ["section-heading"]
        current.append(element.extract())
    return body


def update_toc(soup, body):
    toc = soup.select_one(".section-toc ol")
    if not toc:
        return
    toc.clear()
    for section in body.select(".lesson-section"):
        item = soup.new_tag("li")
        link = soup.new_tag("a", href="#" + section["id"])
        link.string = section.h2.get_text(" ", strip=True)
        item.append(link)
        toc.append(item)


def parse(unit_id):
    raw = unit_source(unit_id).read_text()
    meta = yaml.safe_load(raw.split("---", 2)[1])
    text = raw.split("<!-- learner-content:start -->", 1)[1].split("<!-- learner-content:end -->", 1)[0].strip()
    first = text.find("\n## ")
    head, rest = (text[:first], text[first + 1:]) if first >= 0 else (text, "")
    lines = [line.strip() for line in head.splitlines() if line.strip()]
    title, subtitle = meta["title"], meta.get("learning_objective", "")
    artifact = subtitle
    if lines and lines[0].startswith("# "):
        title = lines.pop(0)[2:].strip()
    done = [line for line in lines if line.startswith("本節完成物：")]
    if done:  # 新格式：標題、副標、本節完成物三行
        artifact = done[0].split("：", 1)[1].strip()
        subtitle = lines[0] if not lines[0].startswith("本節完成物：") else subtitle
        lines = [line for line in lines if line not in (subtitle, done[0])]
    intro = lines
    body = rest
    if intro and rest:  # 開場段併進第一節
        h, tail = rest.split("\n", 1)
        body = h + "\n\n" + "\n\n".join(intro) + "\n\n" + tail.lstrip()
    elif intro:
        body = "\n\n".join(intro)
    return title, subtitle, artifact, int(meta.get("duration_minutes", 0)), body


def set_meta(soup, attr, key, value):
    tag = soup.find("meta", attrs={attr: key})
    if tag:
        tag["content"] = value


def render(unit_id, out_dir=None):
    title, subtitle, artifact, minutes, body_md = parse(unit_id)
    page = unit_page(unit_id)
    target = (out_dir / page.name) if out_dir else page
    soup = BeautifulSoup(page.read_text(), "html.parser")
    body = render_body(body_md, unit_source(unit_id), page)
    soup.select_one(".lesson-body").replace_with(body)
    update_toc(soup, body)
    soup.title.string = f"{title}｜{COURSE_NAME}"
    soup.select_one(".lesson-title").string = title
    soup.select_one(".outcome-item").string = artifact
    eyebrow = soup.select_one(".hero-eyebrow")
    if eyebrow and minutes:
        eyebrow.string = f"{unit_id} · {minutes} 分鐘"
    for attr, key, value in (("name", "description", subtitle), ("property", "og:description", subtitle), ("name", "twitter:description", subtitle),
                             ("property", "og:title", f"{unit_id} {title}｜{COURSE_NAME}"), ("name", "twitter:title", f"{unit_id} {title}｜{COURSE_NAME}")):
        set_meta(soup, attr, key, value)
    target.write_text(html(soup))
    return title, subtitle, minutes, body_md


def update_cards(results, out_dir=None):
    for filename in ("index.html", "module1.html", "module2.html", "module3.html"):
        page = COURSE / filename
        soup = BeautifulSoup(page.read_text(), "html.parser")
        changed = False
        for unit_id, (title, subtitle, minutes, _) in results.items():
            for card in soup.select(f'a.lesson-card[href$="{unit_id}.html"]'):
                card.select_one(".lesson-title").string = title
                card.select_one(".lesson-meta").string = f"{minutes} 分鐘 · {subtitle}"
                card["data-search"] = f"{title} {minutes} 分鐘 · {subtitle}"
                changed = True
        if changed:
            ((out_dir / filename) if out_dir else page).write_text(html(soup))


def update_search(results, out_dir=None):
    path = COURSE / "search-index.json"
    records = json.loads(path.read_text())
    for item in records:
        if item["id"] in results:
            title, _, _, body_md = results[item["id"]]
            item["title"] = title
            item["text"] = BeautifulSoup(MD.render(body_md), "html.parser").get_text(" ", strip=True)
    ((out_dir / path.name) if out_dir else path).write_text(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    args = sys.argv[1:]
    out_dir = None
    if args[:1] == ["--out"]:
        out_dir = Path(args[1])
        out_dir.mkdir(parents=True, exist_ok=True)
        args = args[2:]
    results = {u: render(u, out_dir) for u in args}
    update_cards(results, out_dir)
    update_search(results, out_dir)
    for u, (title, *_rest) in results.items():
        print(u, "→", title)
