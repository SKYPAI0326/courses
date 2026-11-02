"""產生 v8 下載包：離線講義包與文字包。同樣的輸入每次產出逐位元相同的 ZIP。

用法（在 repo 根目錄）：
python3 courses/canva-video-teaching/_tools/build-packs.py          # 重建兩個 ZIP
python3 courses/canva-video-teaching/_tools/build-packs.py --check  # 只檢查離線包內的本地連結

離線包：v8 頁面＋頁面引用到的所有本地檔；首頁連到兩個 ZIP 的連結在包內改成線上網址。
文字包：9 個單元的學員正文、4 份資源頁與示範講稿，轉成純文字。
"""
from pathlib import Path
from urllib.parse import unquote
import io
import re
import sys
import zipfile

from bs4 import BeautifulSoup

COURSE = Path(__file__).resolve().parents[1]
REPO = COURSE.parents[1]
SITE = "https://skypai0326.github.io/courses/courses/canva-video-teaching/"
UNITS = ["CH1-1", "CH1-2", "CH1-3", "CH1-4", "CH1-5", "CH2-1", "CH2-2", "CH3-1", "CH3-2"]
RESOURCES = ["卡住時", "老師流程卡", "學生版流程卡", "收件檢查表"]
PAGES = ["index.html", "module1.html", "module2.html", "module3.html", "EXT1.html"] + \
    [f"ch{u[2]}/{u}.html" for u in UNITS] + [f"resources/{n}.html" for n in RESOURCES]
OFFLINE, TEXT = "downloads/canva-handouts-offline.zip", "downloads/canva-text-pack.zip"
ROOT = "Canva影片快速上手/"
STAMP = (2026, 11, 2, 0, 0, 0)
STORED = (".mp4", ".zip", ".png", ".jpg", ".pptx")


def local_refs(page):
    soup = BeautifulSoup((COURSE / page).read_text(), "html.parser")
    for el in soup.find_all(["a", "img", "source", "video", "link", "script"]):
        for attr in ("href", "src", "poster"):
            url = el.get(attr)
            if url and not url.startswith(("http:", "https:", "#", "mailto:", "data:")):
                yield (COURSE / page).parent / unquote(url.split("#")[0].split("?")[0])


def add(zf, name, data):
    info = zipfile.ZipInfo(ROOT + name, STAMP)
    info.compress_type = zipfile.ZIP_STORED if name.endswith(STORED) else zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, data)


def offline_files():
    files = set(PAGES)
    for page in PAGES:
        for target in local_refs(page):
            rel = target.resolve().relative_to(COURSE.resolve()).as_posix()
            if rel not in (OFFLINE, TEXT):
                files.add(rel)
    return sorted(files)


def build_offline():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for rel in offline_files():
            data = (COURSE / rel).read_bytes()
            if rel == "index.html":  # 包內連到下載包的連結改成線上網址
                text = data.decode()
                for pack in (OFFLINE, TEXT):
                    text = text.replace(f'href="{pack}"', f'href="{SITE}{pack}"')
                data = text.encode()
            add(zf, rel, data)
    (COURSE / OFFLINE).write_bytes(buf.getvalue())


def learner_text(unit):
    raw = (REPO / "_lessons/canva-video-teaching" / f"{unit}.md").read_text()
    return raw.split("<!-- learner-content:start -->", 1)[1].split("<!-- learner-content:end -->", 1)[0].strip()


def plain(md):
    md = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"（圖：\1）", md)
    md = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"\*\*([^*]+)\*\*", r"\1", md)
    return md.strip() + "\n"


def build_text():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for i, unit in enumerate(UNITS, 1):
            text = learner_text(unit)
            title = text.splitlines()[0].lstrip("# ").strip()
            add(zf, f"{i:02d}_{title.replace('：', '_').replace('，', '_')}.txt", plain(text).encode())
        for name in RESOURCES:
            add(zf, f"資源_{name}.txt", plain((COURSE / "resources" / f"{name}.md").read_text()).encode())
        add(zf, "示範講稿_校園午餐垃圾觀察.txt", (COURSE / "downloads/示範講稿_校園午餐垃圾觀察.txt").read_bytes())
    (COURSE / TEXT).write_bytes(buf.getvalue())


def check_offline():
    with zipfile.ZipFile(COURSE / OFFLINE) as zf:
        names = {n[len(ROOT):] for n in zf.namelist()}
        missing = []
        for page in [n for n in names if n.endswith(".html")]:
            soup = BeautifulSoup(zf.read(ROOT + page).decode(), "html.parser")
            for el in soup.find_all(["a", "img", "source", "video", "link", "script"]):
                for attr in ("href", "src", "poster"):
                    url = el.get(attr)
                    if url and not url.startswith(("http:", "https:", "#", "mailto:", "data:")):
                        target = (Path(page).parent / unquote(url.split("#")[0].split("?")[0])).as_posix()
                        target = re.sub(r"(^|/)\./", r"\1", target)
                        while "/../" in "/" + target:
                            target = re.sub(r"(^|/)[^/]+/\.\./", r"\1", target, count=1)
                        if target not in names:
                            missing.append(f"{page} → {url}")
    print(f"離線包 {len(names)} 個檔案，失效連結 {len(missing)} 筆")
    for m in missing:
        print("  ", m)
    return not missing


if __name__ == "__main__":
    if "--check" not in sys.argv:
        build_offline()
        build_text()
    sys.exit(0 if check_offline() else 1)
