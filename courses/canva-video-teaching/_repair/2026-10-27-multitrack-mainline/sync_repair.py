from pathlib import Path
from urllib.parse import unquote
import copy
import hashlib
import json
import os
import re
import zipfile

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from PIL import Image
import xml.etree.ElementTree as ET
import yaml

HERE = Path(__file__).resolve()
COURSE = HERE.parents[2]
REPO = COURSE.parent.parent
SLUG = "canva-video-teaching"
MD = MarkdownIt("commonmark", {"html": True, "breaks": True}).enable("table")

LESSON_IDS = [f"CH{m}-{n}" for m in (1, 2) for n in range(1, 7)]
RESOURCE_NAMES = [
    "Canva功能與技巧",
    "時間軸與字幕實作",
    "開始前準備",
    "案例與腳本",
    "學生製作任務",
    "三頁起始檔",
    "舊專案相容處理",
    "配音與聲音製作",
    "操作與檔案技術卡",
    "技巧與修復卡",
]


def unit_source(unit_id):
    return REPO / "_lessons" / SLUG / f"{unit_id}.md"


def unit_page(unit_id):
    return COURSE / f"ch{unit_id[2]}" / f"{unit_id}.html"


def resource_source(name):
    return COURSE / "resources" / f"{name}.md"


def resource_page(name):
    return COURSE / "resources" / f"{name}.html"


ALL_MAP = {}
for unit_id in LESSON_IDS:
    ALL_MAP[str(unit_source(unit_id).resolve())] = unit_page(unit_id)
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


def learner_text(source):
    raw = source.read_text()
    return raw.split("<!-- learner-content:start -->", 1)[1].split("<!-- learner-content:end -->", 1)[0].strip()


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


def sync_page(source, page, text):
    soup = BeautifulSoup(page.read_text(), "html.parser")
    if source.parent == COURSE / "resources":
        title = source.read_text().splitlines()[0].lstrip("# ")
        soup.title.string = title + "｜Canva 教學短片製作"
        soup.select_one(".lesson-title").string = title
    body = render_body(text, source, page)
    soup.select_one(".lesson-body").replace_with(body)
    update_toc(soup, body)
    footer = soup.select_one(".footer-meta")
    if footer:
        footer["data-platform-version"] = "Canva Web / Record Voiceover 授課帳號實測 2026-10-27；課內匯出證據 2026-10-11"
        footer["data-built-at"] = "2026-10-27"
        footer.string = "Canva 網頁版 · 2026 年 10 月"
    page.write_text(str(soup))


def create_resource_shell(name, objective):
    page = resource_page(name)
    source = resource_source(name)
    soup = BeautifulSoup(resource_page("Canva功能與技巧").read_text(), "html.parser")
    title = source.read_text().splitlines()[0].lstrip("# ")
    soup.title.string = title + "｜Canva 教學短片製作"
    description = soup.find("meta", attrs={"name": "description"})
    if description:
        description["content"] = objective
    soup.select_one(".lesson-title").string = title
    soup.select_one(".outcome-item").string = objective
    body = render_body(source.read_text(), source, page)
    soup.select_one(".lesson-body").replace_with(body)
    update_toc(soup, body)
    footer = soup.select_one(".footer-meta")
    footer["data-platform-version"] = "Canva Web / Record Voiceover 授課帳號實測 2026-10-27"
    footer["data-built-at"] = "2026-10-27"
    footer.string = "Canva 網頁版 · 2026 年 10 月"
    page.write_text(str(soup))


for unit_id in LESSON_IDS:
    sync_page(unit_source(unit_id), unit_page(unit_id), learner_text(unit_source(unit_id)))

create_resource_shell("舊專案相容處理", "辨識舊頁面式 Canva 專案，完成必要維護後回到本課多軌主線。")
for name in RESOURCE_NAMES:
    sync_page(resource_source(name), resource_page(name), resource_source(name).read_text())

for filename in ("index.html", "module1.html", "module2.html"):
    page = COURSE / filename
    soup = BeautifulSoup(page.read_text(), "html.parser")
    footer = soup.select_one(".footer-note")
    if footer:
        footer["data-built-at"] = "2026-10-27"
        footer["data-platform-version"] = "Canva Web / 官方文件 2026-10-27"
    if filename == "index.html":
        description = soup.select_one(".hero-desc")
        description.string = "用新建多軌時間軸完成固定 36 秒教學短片；第一場做畫面版 v1，第二場複製為 v2，再加入旁白、配樂與字幕。"
        for stat in soup.select(".stat"):
            label = stat.select_one(".stat-lbl")
            number = stat.select_one(".stat-num")
            if label and number and "成品秒數" in label.get_text():
                number.string = "36"
        intro = soup.select_one(".intro-text")
        if intro:
            intro.string = "兩場沿用同一支 36 秒作品：先安排四個主片段、上層圖文與時間，再建立 v2 加入旁白、配樂與字幕。每場 150 分鐘，包含 10 分鐘休息。"
        existing = soup.find("a", href="resources/舊專案相容處理.html")
        if not existing:
            cards = [card for card in soup.select(".lesson-card") if card.get("href", "").startswith("resources/")]
            if cards:
                card = copy.copy(cards[-1])
                card["href"] = "resources/舊專案相容處理.html"
                card["data-search"] = "舊專案相容處理 頁面式 Canva 舊設計"
                card.select_one(".lesson-num").string = "R13"
                card.select_one(".lesson-title").string = "舊專案相容處理"
                card.select_one(".lesson-meta").string = "只有舊設計仍顯示頁面縮圖時使用；新作品回到多軌主線。"
                cards[-1].insert_after(card)
        resource_cards = {
            "resources/三頁起始檔.html": ("從四片段底稿恢復 36 秒主作品", "在新建多軌影片恢復四片段文字、實拍與時間，再接回第二場。"),
            "resources/時間軸與字幕實作.html": ("在 Canva 選對物件、剪好聲音並完成字幕", "在同一支 36 秒 v2 分割旁白停頓、校訂字幕並下載檢查。"),
        }
        for href, (title, description) in resource_cards.items():
            card = soup.find("a", href=href)
            if card:
                card.select_one(".lesson-title").string = title
                card.select_one(".lesson-meta").string = description
                card["data-search"] = title + " " + description
    if filename == "module2.html":
        soup.select_one(".hero-desc").string = "開啟 36 秒 v1 建立 v2，在同一支作品錄製旁白、分割停頓、調整配樂，校訂字幕並交付。"
    page.write_text(str(soup))


def plain(markdown):
    return BeautifulSoup(MD.render(markdown), "html.parser").get_text("\n", strip=True)


downloads = COURSE / "downloads"
(downloads / "Canva功能與技巧.txt").write_text(plain(resource_source("Canva功能與技巧").read_text()))
(downloads / "時間軸與字幕實作.txt").write_text(plain(resource_source("時間軸與字幕實作").read_text()))
(downloads / "校園案例與腳本.txt").write_text(plain(resource_source("案例與腳本").read_text()))
(downloads / "學生製作任務.txt").write_text(plain(resource_source("學生製作任務").read_text()))
(downloads / "三頁起始檔操作.txt").write_text(plain(resource_source("三頁起始檔").read_text()))
(downloads / "舊專案相容處理.txt").write_text(plain(resource_source("舊專案相容處理").read_text()))
(downloads / "配音與聲音製作.txt").write_text(plain(resource_source("配音與聲音製作").read_text()))
(downloads / "操作與檔案技術卡.txt").write_text(plain(resource_source("操作與檔案技術卡").read_text()))
(downloads / "技巧與修復卡.txt").write_text(plain(resource_source("技巧與修復卡").read_text()))
(downloads / "作品檢查.txt").write_text(
    "□ 全片固定 36 秒，橫式 16:9\n"
    "□ 主軌依序是位置 0 秒、閱讀 10 秒、自習 16 秒、提問 22 秒\n"
    "□ 實拍影片可見動作，與例句和錄音一致\n"
    "□ 可指出裁短、裁切、圖層與文字起訖的操作結果\n"
    "□ 動畫及轉場不妨礙閱讀，套用後總長仍是 36 秒\n"
    "□ 旁白分割處沒有爆音、截字或長空白，配樂不蓋過講解\n"
    "□ 字幕已逐句回聽，繁體字、標點與時間正確\n"
    "□ 字幕沒有遮住例句、人物與圖形\n"
    "□ MP4 下載檔可完整播放，結束於 36 秒\n"
    "□ 已保存可修改的 v1、v2、時間表與素材來源\n"
    "□ 課後轉用版已更換新題材，素材、文字、旁白、字幕與提問一致\n"
    "□ 課後轉用版已附 MP4、可編輯網址與修改說明，沒有殘留舊題材內容\n"
)

portable = ["Canva 完整操作步驟\n\n依 CH1-1 至 CH2-6 接續製作固定 36 秒作品；EXT1 為課後延伸。"]
for unit_id in LESSON_IDS:
    portable.append(unit_id + "\n" + plain(learner_text(unit_source(unit_id))))
(downloads / "Canva完整操作步驟.txt").write_text("\n\n".join(portable))

search_path = COURSE / "search-index.json"
search = json.loads(search_path.read_text())
records = {item["id"]: item for item in search}
for unit_id in LESSON_IDS:
    records[unit_id]["text"] = plain(learner_text(unit_source(unit_id))).replace("\n", " ")
for name in RESOURCE_NAMES:
    records[name] = {
        "id": name,
        "title": resource_source(name).read_text().splitlines()[0].lstrip("# "),
        "url": f"resources/{name}.html",
        "text": plain(resource_source(name).read_text()).replace("\n", " "),
    }
search_path.write_text(json.dumps(list(records.values()), ensure_ascii=False, indent=2))

with zipfile.ZipFile(downloads / "canva-text-pack.zip", "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(downloads.iterdir()):
        if path.suffix in (".txt", ".csv", ".srt"):
            archive.write(path, path.name)

offline = downloads / "canva-handouts-offline.zip"
with zipfile.ZipFile(offline, "w", zipfile.ZIP_DEFLATED) as archive:
    inputs = [COURSE / "index.html", COURSE / "module1.html", COURSE / "module2.html", COURSE / "EXT1.html", search_path]
    inputs += list((COURSE / "ch1").glob("*.html")) + list((COURSE / "ch2").glob("*.html"))
    portable_downloads = [
        path for path in downloads.iterdir()
        if path.suffix.lower() != ".zip" or path.name == "canva-text-pack.zip"
    ]
    inputs += list((COURSE / "resources").glob("*.html")) + list((COURSE / "assets").rglob("*")) + portable_downloads
    for path in inputs:
        if path.is_file() and path != offline:
            archive.write(path, str(path.relative_to(COURSE)))
    archive.writestr("開啟講義.txt", "解壓縮完整資料夾後開啟 index.html。Canva 操作與外部網站需要網路；課內文字、圖片與參考影片可離線閱讀。")

inventory_path = COURSE / "_validation" / "continuity-artifact-inventory.json"
inventory = json.loads(inventory_path.read_text())
inventory["active_html"] = len(list(COURSE.rglob("*.html")))
inventory["body_pages"] = sum(1 for path in COURSE.rglob("*.html") if BeautifulSoup(path.read_text(), "html.parser").select_one(".lesson-body"))
inventory["resource_markdown"] = len(list((COURSE / "resources").glob("*.md")))
inventory["download_files"] = len([path for path in downloads.iterdir() if path.is_file()])
for archive_info in inventory.get("archives", []):
    archive_path = REPO / archive_info["path"]
    if archive_path.is_file():
        archive_info["sha256"] = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        with zipfile.ZipFile(archive_path) as archive:
            archive_info["entries"] = len(archive.namelist())
            archive_info["members"] = archive.namelist()
inventory_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2))

print(json.dumps({"lessons": len(LESSON_IDS), "resources": len(RESOURCE_NAMES), "new_resource": str(resource_page("舊專案相容處理").relative_to(COURSE))}, ensure_ascii=False))
