#!/usr/bin/env python3

import json
import os
import re
import sys
import unicodedata
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text))


def page_for_source(reader: PdfReader, source: str) -> int:
    target = normalized(source)
    for index, page in enumerate(reader.pages):
        if target in normalized(page.extract_text() or ""):
            return index
    return 0


def is_footer_only(page) -> bool:
    text = unicodedata.normalize("NFKC", page.extract_text() or "")
    return "來源：" not in text and len(normalized(text)) < 55


def clean_document(pdf_path: Path, title: str, source: str) -> None:
    reader = PdfReader(str(pdf_path))
    kept = [index for index, page in enumerate(reader.pages) if not is_footer_only(page)]
    old_to_new = {old: new for new, old in enumerate(kept)}
    writer = PdfWriter()
    for index in kept:
        writer.add_page(reader.pages[index])
    source_page = page_for_source(reader, source)
    writer.add_outline_item(title, old_to_new.get(source_page, 0))
    writer.add_metadata({
        "/Title": f"行政 AI 虛擬助理實戰｜{title}｜學員版",
        "/Author": "弄一下工作室",
        "/Subject": "可列印、可搜尋、NotebookLM Ready 學員講義",
        "/Keywords": "行政 AI, Gemini, NotebookLM, 學員講義",
    })
    temp = pdf_path.with_suffix(".postprocess.pdf")
    with temp.open("wb") as handle:
        writer.write(handle)
    os.replace(temp, pdf_path)


def merge_full(pdf_path: Path, cover_pdf: str, chapter_items: list[dict], appendix_pdf: str) -> None:
    writer = PdfWriter()
    cover = PdfReader(cover_pdf)
    writer.append(cover, import_outline=False)
    writer.add_outline_item("封面", 0)
    offset = len(cover.pages)
    for item in chapter_items:
        reader = PdfReader(item["path"])
        writer.append(reader, import_outline=False)
        writer.add_outline_item(f"CH{item['chapter']}｜{item['title']}", offset)
        offset += len(reader.pages)
    appendix = PdfReader(appendix_pdf)
    writer.append(appendix, import_outline=False)
    writer.add_outline_item("課程資產庫附錄", offset)
    writer.add_metadata({
        "/Title": "行政 AI 虛擬助理實戰｜全課合併版｜學員版",
        "/Author": "弄一下工作室",
        "/Subject": "6 章完整內容、章末答案與課程資產庫；可列印、可搜尋、NotebookLM Ready",
        "/Keywords": "行政 AI, Gemini, NotebookLM, 虛擬助理, 學員講義",
    })
    with pdf_path.open("wb") as handle:
        writer.write(handle)


def main() -> None:
    mode = sys.argv[1]
    if mode == "document":
        clean_document(Path(sys.argv[2]), sys.argv[3], sys.argv[4])
    elif mode == "full":
        merge_full(Path(sys.argv[2]), sys.argv[3], json.loads(sys.argv[4]), sys.argv[5])
    else:
        raise SystemExit(f"未知模式：{mode}")


if __name__ == "__main__":
    main()

