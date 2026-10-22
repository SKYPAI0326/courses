#!/usr/bin/env python3
"""Rebuild only the portable artifacts directly affected by the lesson edits."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt


COURSE_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = COURSE_DIR.parents[1]
SOURCE_DIR = REPO_ROOT / "_lessons/canva-video-teaching"
DOWNLOADS = COURSE_DIR / "downloads"
MD = MarkdownIt("commonmark", {"html": True, "breaks": True}).enable("table")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def learner_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    return raw.split("<!-- learner-content:start -->", 1)[1].split(
        "<!-- learner-content:end -->", 1
    )[0].strip()


def unit_id(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("unit_id:"):
            return line.split(":", 1)[1].strip()
    raise ValueError(f"missing unit_id: {path}")


def update_search_index() -> None:
    index_path = COURSE_DIR / "search-index.json"
    records = json.loads(index_path.read_text(encoding="utf-8"))
    by_id = {record["id"]: record for record in records}
    for name in ("CH2-1.md", "CH2-3.md"):
        source = SOURCE_DIR / name
        record = by_id[unit_id(source)]
        record["text"] = BeautifulSoup(MD.render(learner_text(source)), "html.parser").get_text(
            " ", strip=True
        )
    index_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def update_portable_text() -> None:
    parts = [
        "Canva 完整操作步驟\n\n依 CH1-1 至 CH2-6 接續製作；EXT1 為課後延伸。"
        "案例文字在「校園案例與腳本.txt」，參考影片在影音練習包。"
    ]
    sources = sorted(path for path in SOURCE_DIR.glob("*.md") if path.name != "INDEX.md")
    for source in sources:
        fragment = BeautifulSoup(MD.render(learner_text(source)), "html.parser")
        for link in fragment.find_all("a"):
            url = link.get("href", "")
            if url.startswith("https:"):
                link.append(f"（{url}）")
        parts.append(f"{unit_id(source)}\n{fragment.get_text(chr(10), strip=True)}")
    (DOWNLOADS / "Canva完整操作步驟.txt").write_text("\n\n".join(parts), encoding="utf-8")


def rebuild_text_pack() -> None:
    target = DOWNLOADS / "canva-text-pack.zip"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(DOWNLOADS.iterdir(), key=lambda item: item.name):
            if path.suffix in (".txt", ".csv", ".srt"):
                archive.write(path, path.name)


def rebuild_offline_bundle() -> None:
    target = DOWNLOADS / "canva-handouts-offline.zip"
    files = [
        COURSE_DIR / "index.html",
        COURSE_DIR / "module1.html",
        COURSE_DIR / "module2.html",
        COURSE_DIR / "EXT1.html",
        COURSE_DIR / "search-index.json",
        *sorted((COURSE_DIR / "ch1").glob("*.html")),
        *sorted((COURSE_DIR / "ch2").glob("*.html")),
        *sorted((COURSE_DIR / "resources").glob("*.html")),
        *sorted(path for path in (COURSE_DIR / "assets").rglob("*") if path.is_file()),
        *sorted(
            path
            for path in DOWNLOADS.iterdir()
            if path.is_file()
            and path.name not in {target.name, "canva-media-pack.zip"}
        ),
    ]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, str(path.relative_to(COURSE_DIR)))
        archive.writestr(
            "開啟講義.txt",
            "解壓縮完整資料夾後開啟 index.html。請保留 assets、resources、ch1、ch2 及 "
            "downloads 資料夾。Canva 操作與外部網站需要網路；參考影片與文字材料可離線閱讀。",
        )


def update_inventory() -> None:
    inventory_path = COURSE_DIR / "_validation/continuity-artifact-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory["active_html"] = len(list(COURSE_DIR.rglob("*.html")))
    inventory["body_pages"] = sum(
        "lesson-body" in path.read_text(encoding="utf-8") for path in COURSE_DIR.rglob("*.html")
    )
    inventory["resource_markdown"] = len(list((COURSE_DIR / "resources").glob("*.md")))
    inventory["download_files"] = len(list(DOWNLOADS.iterdir()))
    for record in inventory["archives"]:
        path = REPO_ROOT / record["path"]
        with zipfile.ZipFile(path) as archive:
            record["sha256"] = sha256(path)
            record["entries"] = len(archive.infolist())
            record["members"] = archive.namelist()
    inventory_path.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    update_search_index()
    update_portable_text()
    rebuild_text_pack()
    rebuild_offline_bundle()
    update_inventory()
    print("rebuilt search index, portable text, text pack, offline bundle, and archive inventory")


if __name__ == "__main__":
    main()
