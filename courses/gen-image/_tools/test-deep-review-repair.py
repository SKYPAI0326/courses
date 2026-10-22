#!/usr/bin/env python3
"""Regression checks for the 2026-10-22 Deep Review repair."""

from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "courses" / "gen-image"
LESSONS = ROOT / "_lessons" / "gen-image"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def main_pages() -> set[Path]:
    pages = {COURSE / "index.html"}
    pages.update(COURSE.glob("module[1-6].html"))
    pages.update(COURSE.glob("CH*.html"))
    pages.update(COURSE.glob("PRAC*.html"))
    return {page.resolve() for page in pages}


def reachable_pages(pages: set[Path]) -> set[Path]:
    seen: set[Path] = set()
    pending = [(COURSE / "index.html").resolve()]
    while pending:
        page = pending.pop()
        if page in seen or page not in pages:
            continue
        seen.add(page)
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for href in parser.hrefs:
            if href.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = (page.parent / href.split("#", 1)[0]).resolve()
            if target in pages and target not in seen:
                pending.append(target)
    return seen


def check_evidence_hashes(errors: list[str]) -> None:
    evidence_path = COURSE / "_validation" / "evidence.json"
    if not evidence_path.is_file():
        errors.append("missing _validation/evidence.json")
        return
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    for record in evidence.get("records", []):
        for artifact in record.get("artifacts", []):
            path = ROOT / artifact["path"]
            if not path.is_file() or sha(path) != artifact["sha256"]:
                errors.append(f"stale evidence artifact: {artifact['path']}")

    result_path = COURSE / "_validation" / "validation-result.json"
    if not result_path.is_file():
        errors.append("missing _validation/validation-result.json")
        return
    result = json.loads(result_path.read_text(encoding="utf-8"))
    for page in result.get("pages", []):
        path = COURSE / page["path"]
        if not path.is_file() or sha(path) != page["html_sha256"]:
            errors.append(f"stale validation page: {page['path']}")


def main() -> int:
    errors: list[str] = []

    pages = main_pages()
    if len(pages) != 41:
        errors.append(f"expected 41 main pages, found {len(pages)}")
    reachable = reachable_pages(pages)
    if reachable != pages:
        missing = ", ".join(sorted(path.name for path in pages - reachable))
        errors.append(f"unreachable main pages: {missing}")

    fragment_links = []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        fragment_links.extend(
            f"{page.name}:{href}"
            for href in re.findall(r'href=["\']([^"\']+\.md#[^"\']+)["\']', text)
        )
    if fragment_links:
        errors.append(f"markdown fragment links remain: {len(fragment_links)}")

    source = (LESSONS / "CH5-1.md").read_text(encoding="utf-8")
    page = (COURSE / "CH5-1.html").read_text(encoding="utf-8")
    for required in ("3 張系列完稿", "L2 線稿", "局部修改", "release gate"):
        if required not in source or required not in page:
            errors.append(f"capstone contract missing in source or HTML: {required}")
    if "瀨戶內慢旅" in source or "島嶼慢旅（虛構品牌）" not in source:
        errors.append("CH5-1 source still diverges from the fictional travel case in HTML")

    workbook = (COURSE / "assets" / "downloads" / "offline-candidate-workbook.md").read_text(encoding="utf-8")
    for required in ("## PRAC4", "v16-brand-spring-2026-10.png", "v17-brand-summer-2026-10.png", "v18-brand-winter-2026-10.png"):
        if required not in workbook:
            errors.append(f"offline PRAC4 contract missing: {required}")

    record_script = COURSE / "assets" / "learner-record.js"
    if not record_script.is_file():
        errors.append("missing assets/learner-record.js")
    for name in ("PRAC2.html", "PRAC3.html", "PRAC4.html", "CH5-1.html"):
        text = (COURSE / name).read_text(encoding="utf-8")
        for required in ("assets/learner-record.js", "data-record-copy", "data-record-download"):
            if required not in text:
                errors.append(f"{name} missing learner record control: {required}")

    image_manifest = (COURSE / "_repair" / "2026-10-17-image-refresh" / "IMAGE-MANIFEST.tsv").read_text(encoding="utf-8")
    provenance = (COURSE / "_repair" / "2026-10-17-image-refresh" / "ASSET-PROVENANCE.tsv").read_text(encoding="utf-8")
    prompts = (COURSE / "_repair" / "2026-10-17-image-refresh" / "IMAGE-PROMPT-SET.md").read_text(encoding="utf-8")
    for label, text in (("manifest", image_manifest), ("provenance", provenance), ("prompt set", prompts)):
        if "v64-four-step-loop-2026-10.svg" not in text:
            errors.append(f"v64 missing from {label}")
    if "v63-three-stage-workflow-2026-10.svg" not in provenance:
        errors.append("v63 unused-candidate status missing from provenance")

    check_evidence_hashes(errors)

    if errors:
        print(f"DEEP REVIEW REPAIR CHECK: FAIL ({len(errors)} issues)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("DEEP REVIEW REPAIR CHECK: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
