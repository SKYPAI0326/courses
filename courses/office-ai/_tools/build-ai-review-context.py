#!/usr/bin/env python3
"""Build learner-only JSON context bundles for the office-ai AI review."""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
from datetime import date
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup


PROJECT_ROOT = Path(__file__).resolve().parents[3]
COURSES_ROOT = PROJECT_ROOT / "courses"
COURSE_ROOT = COURSES_ROOT / "office-ai"
CONTEXT_ROOT = COURSE_ROOT / "_validation" / "ai-simulated" / "context"
CONCEPT_UNITS = {"CH1-1", "CH1-2", "CH6-2", "CH6-3"}
TEXT_ASSET_SUFFIXES = {".txt", ".md", ".csv", ".tsv", ".json"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative_to_project(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


def unit_id_for(page: Path) -> str:
    return page.stem


def page_title(soup: BeautifulSoup, fallback: str) -> str:
    heading = soup.select_one("h1.lesson-title, h1")
    if heading:
        return heading.get_text(" ", strip=True)
    title = soup.find("title")
    return title.get_text(" ", strip=True) if title else fallback


def clean_visible_element(element: Any) -> str:
    clone = BeautifulSoup(str(element), "html.parser")
    for tag in clone.select("script, style, nav, footer, #_gate, [aria-hidden='true']"):
        tag.decompose()
    for comment in clone.find_all(string=lambda value: getattr(value, "strip", lambda: "")().startswith("<!--")):
        comment.extract()
    return clone.get_text(" ", strip=True)


def visible_sections(soup: BeautifulSoup) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    seen: set[str] = set()
    for element in soup.select(".lesson-hero, .lesson-section"):
        text = clean_visible_element(element)
        if not text or text in seen:
            continue
        seen.add(text)
        heading = element.find(["h1", "h2", "h3", "h4"])
        sections.append({
            "heading": heading.get_text(" ", strip=True) if heading else "",
            "text": text,
        })
    if not sections:
        body = soup.body or soup
        text = clean_visible_element(body)
        if text:
            sections.append({"heading": "", "text": text})
    return sections


def asset_paths(page: Path) -> list[Path]:
    soup = BeautifulSoup(page.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    result: list[Path] = []
    seen: set[Path] = set()
    for element in soup.find_all(["a", "img", "source"]):
        attribute = "href" if element.name == "a" else "src"
        href = element.get(attribute)
        if not href or href.startswith(("#", "http://", "https://", "mailto:", "javascript:")):
            continue
        href = href.split("#", 1)[0].split("?", 1)[0]
        if "/assets/" not in href and not href.startswith("../assets/"):
            continue
        candidate = (page.parent / href).resolve()
        if candidate.is_file() and candidate not in seen:
            seen.add(candidate)
            result.append(candidate)
    return sorted(result)


def asset_entry(path: Path) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "path": relative_to_project(path),
        "sha256": sha256(path),
        "size": path.stat().st_size,
        "media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
    }
    if path.suffix.lower() in TEXT_ASSET_SUFFIXES and path.stat().st_size <= 100_000:
        entry["text_content"] = path.read_text(encoding="utf-8", errors="replace")
    return entry


def course_title() -> str:
    outline = PROJECT_ROOT / "_outlines" / "office-ai.md"
    if outline.is_file():
        match = re.search(r"^name:\s*(.+?)\s*$", outline.read_text(encoding="utf-8"), re.MULTILINE)
        if match:
            return match.group(1).strip().strip('"')
    return "辦公室 AI 工具實務應用"


def build_context(page_path: Path, course_root: Path = COURSE_ROOT, project_root: Path = PROJECT_ROOT) -> dict[str, Any]:
    unit_id = unit_id_for(page_path)
    soup = BeautifulSoup(page_path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    return {
        "schema_version": 1,
        "course": "office-ai",
        "course_title": course_title(),
        "unit_id": unit_id,
        "title": page_title(soup, unit_id),
        "course_type": "concept" if unit_id in CONCEPT_UNITS else "skill-operation",
        "page": relative_to_project(page_path),
        "page_sha256": sha256(page_path),
        "visible_sections": visible_sections(soup),
        "assets": [asset_entry(path) for path in asset_paths(page_path)],
        "input_boundary": "learner-facing visible page plus the page's directly referenced local assets",
        "generated_at": date.today().isoformat(),
    }


def build_manifest(course_root: Path = COURSE_ROOT, project_root: Path = PROJECT_ROOT) -> dict[str, Any]:
    page_paths = sorted(course_root.glob("ch*/CH*.html"))
    contexts = [build_context(path, course_root, project_root) for path in page_paths]
    return {
        "schema_version": 1,
        "course": "office-ai",
        "generated_at": date.today().isoformat(),
        "input_boundary": "learner-facing visible page plus directly referenced local assets",
        "units": [
            {
                "unit_id": context["unit_id"],
                "title": context["title"],
                "course_type": context["course_type"],
                "context_path": f"courses/office-ai/_validation/ai-simulated/context/{context['unit_id']}.json",
                "page": context["page"],
                "page_sha256": context["page_sha256"],
                "asset_count": len(context["assets"]),
            }
            for context in contexts
        ],
    }, contexts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("course", choices=["office-ai"])
    args = parser.parse_args()
    del args
    CONTEXT_ROOT.mkdir(parents=True, exist_ok=True)
    manifest, contexts = build_manifest()
    for context in contexts:
        path = CONTEXT_ROOT / f"{context['unit_id']}.json"
        path.write_text(json.dumps(context, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (CONTEXT_ROOT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"built learner-only contexts: {len(contexts)} units")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
