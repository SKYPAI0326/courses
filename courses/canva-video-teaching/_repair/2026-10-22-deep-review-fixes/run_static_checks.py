#!/usr/bin/env python3
"""Run current HTML, link, source-fidelity, ZIP, and media checks without publishing."""

from __future__ import annotations

import json
import re
import subprocess
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt


STAGE = Path(__file__).resolve().parent
COURSE_DIR = STAGE.parents[1]
REPO_ROOT = COURSE_DIR.parents[1]
MD = MarkdownIt("commonmark", {"html": True, "breaks": True}).enable("table")


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value)


def main() -> None:
    pages = [
        COURSE_DIR / "index.html",
        COURSE_DIR / "module1.html",
        COURSE_DIR / "module2.html",
        COURSE_DIR / "EXT1.html",
        *sorted((COURSE_DIR / "ch1").glob("*.html")),
        *sorted((COURSE_DIR / "ch2").glob("*.html")),
        *sorted((COURSE_DIR / "resources").glob("*.html")),
    ]
    issues: list[object] = []
    fidelity = []
    link_count = 0

    for page in pages:
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        for element in soup.find_all(["a", "img", "source", "script", "link"]):
            url = element.get("href") or element.get("src")
            parsed = urlsplit(url or "")
            if not url or parsed.scheme or parsed.netloc:
                continue
            target = (page.parent / unquote(parsed.path)).resolve() if parsed.path else page
            link_count += 1
            if not target.is_file():
                issues.append([str(page.relative_to(COURSE_DIR)), url, "missing file"])
            elif parsed.fragment and target.suffix == ".html":
                target_soup = BeautifulSoup(target.read_text(encoding="utf-8"), "html.parser")
                if target_soup.find(id=unquote(parsed.fragment)) is None:
                    issues.append([str(page.relative_to(COURSE_DIR)), url, "missing anchor"])

        if page.name.startswith(("CH", "EXT")):
            source = REPO_ROOT / "_lessons/canva-video-teaching" / page.with_suffix(".md").name
            raw = source.read_text(encoding="utf-8")
            text = raw.split("<!-- learner-content:start -->", 1)[1].split(
                "<!-- learner-content:end -->", 1
            )[0]
        elif page.parent.name == "resources":
            source = page.with_suffix(".md")
            text = source.read_text(encoding="utf-8")
        else:
            continue

        rendered = BeautifulSoup(MD.render(text), "html.parser")
        heading = rendered.find("h1")
        if heading:
            heading.decompose()
        body = soup.select_one(".lesson-body")
        if body is None:
            issues.append([str(page.relative_to(COURSE_DIR)), "missing lesson-body"])
            continue
        actual = normalize(body.get_text())
        missing = []
        for element in rendered.find_all(["p", "h2", "h3", "li", "pre", "td", "th", "blockquote"]):
            value = normalize(element.get_text())
            if value and value not in actual:
                missing.append(value)
        table_rows = lambda dom: [
            [normalize(cell.get_text()) for cell in table.find_all(["th", "td"])]
            for table in dom.find_all("table")
        ]
        tables_equal = table_rows(rendered) == table_rows(body)
        fidelity.append(
            {
                "page": str(page.relative_to(COURSE_DIR)),
                "source": str(source.relative_to(REPO_ROOT)),
                "text_missing": missing,
                "tables_equal": tables_equal,
            }
        )
        if missing or not tables_equal:
            issues.append([str(page.relative_to(COURSE_DIR)), "source fidelity"])

    lint = subprocess.run(
        [
            "python3",
            str(REPO_ROOT / "docs/lint-page.py"),
            *[str(page) for page in pages],
            "--summary",
        ],
        capture_output=True,
        text=True,
    )
    content_pages = [
        page for page in pages if page.name not in {"index.html", "module1.html", "module2.html"}
    ]
    structure = subprocess.run(
        [
            "python3",
            "/Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py",
            *[str(page) for page in content_pages],
        ],
        capture_output=True,
        text=True,
    )
    substance = subprocess.run(
        ["python3", str(REPO_ROOT / "docs/audit-course-substance.py"), "canva-video-teaching"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    zip_results = []
    for path in sorted((COURSE_DIR / "downloads").glob("*.zip")):
        with zipfile.ZipFile(path) as archive:
            zip_results.append(
                {"name": path.name, "entries": len(archive.infolist()), "invalid": archive.testzip()}
            )

    media = COURSE_DIR / "assets/media/footage-v1.mp4"
    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(media),
        ],
        capture_output=True,
        text=True,
    )
    duration = float(probe.stdout.strip()) if probe.returncode == 0 else None
    if duration is None or not 35.5 <= duration <= 36.5:
        issues.append([str(media.relative_to(COURSE_DIR)), "expected approximately 36 seconds", duration])

    result = {
        "pages": len(pages),
        "content_pages": len(content_pages),
        "local_links": link_count,
        "issues": issues,
        "fidelity": fidelity,
        "lint_exit": lint.returncode,
        "structure_exit": structure.returncode,
        "substance_exit": substance.returncode,
        "zips": zip_results,
        "fallback_video_duration_seconds": duration,
    }
    (STAGE / "static-results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    output = "\n".join(
            [
                "COMMAND: lint-page.py --summary",
                lint.stdout,
                lint.stderr,
                "COMMAND: validate-course-structure.py",
                structure.stdout,
                structure.stderr,
                "COMMAND: audit-course-substance.py canva-video-teaching",
                substance.stdout,
                substance.stderr,
                "COMMAND: ffprobe assets/media/footage-v1.mp4",
                probe.stdout,
                probe.stderr,
            ]
        ).rstrip() + "\n"
    (STAGE / "static-output.txt").write_text(output, encoding="utf-8")
    summary = {key: value for key, value in result.items() if key != "fidelity"}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    failed = bool(
        issues
        or lint.returncode
        or structure.returncode
        or substance.returncode
        or any(record["invalid"] for record in zip_results)
    )
    raise SystemExit(failed)


if __name__ == "__main__":
    main()
