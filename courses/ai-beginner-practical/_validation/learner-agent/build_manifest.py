#!/usr/bin/env python3
"""Build a bounded evidence manifest for an independent learner-agent run."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


PAGE_NAMES = (
    "index.html",
    "module1.html",
    "CH1-1.html",
    "CH2-1.html",
    "CH3-1.html",
    "CH4-1.html",
)
FORBIDDEN_ROOTS = ("_validation", "_repair", "_backup", "_review", "_tools")
FORBIDDEN_PATHS = (
    "COURSE-OUTLINE.md",
    "COURSE-BLUEPRINT.md",
    "COVERAGE-LEDGER.md",
    "_gates.md",
    "_plan.md",
    "STYLE-GUIDE.md",
)


class PageParser(HTMLParser):
    """Extract visible learner text and local links without executing page code."""

    SKIP_TAGS = {"script", "style", "template", "noscript"}
    VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__()
        self.text_parts: list[str] = []
        self.local_links: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        if self._skip_depth:
            if tag in self.VOID_TAGS:
                return
            self._skip_depth += 1
            return
        if tag in self.SKIP_TAGS or attrs_map.get("id") == "_gate":
            self._skip_depth = 1
            return
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.local_links.append(value)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if not self._skip_depth:
            for key, value in attrs:
                if key in {"href", "src"} and value:
                    self.local_links.append(value)

    def handle_endtag(self, tag: str) -> None:
        if self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            self.text_parts.append(data)

    @property
    def visible_text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.text_parts)).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_local_link(page: Path, link: str, root: Path) -> Path | None:
    parsed = urlparse(unquote(link))
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    candidate = (page.parent / parsed.path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def build_manifest(root: Path) -> dict[str, object]:
    pages: list[dict[str, object]] = []
    asset_paths: set[Path] = set()
    for page_name in PAGE_NAMES:
        page = root / page_name
        if not page.is_file():
            raise FileNotFoundError(f"missing learner page: {page_name}")
        raw = page.read_bytes()
        parser = PageParser()
        parser.feed(raw.decode("utf-8"))
        for link in parser.local_links:
            target = resolve_local_link(page, link, root)
            if target and target.is_file() and target.suffix.lower() not in {".html", ".css", ".js"}:
                asset_paths.add(target)
        pages.append(
            {
                "path": page_name,
                "html_sha256": hashlib.sha256(raw).hexdigest(),
                "visible_text_sha256": hashlib.sha256(parser.visible_text.encode("utf-8")).hexdigest(),
                "visible_text": parser.visible_text,
            }
        )

    assets = []
    for asset in sorted(asset_paths):
        assets.append(
            {
                "path": asset.relative_to(root).as_posix(),
                "sha256": sha256(asset),
            }
        )
    return {
        "course": root.name,
        "evidence_mode": "learner-facing-pages",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_rule": "Read only the listed learner pages and linked learner assets; do not read internal validation or authoring files.",
        "pages": pages,
        "learner_assets": assets,
        "forbidden_roots": list(FORBIDDEN_ROOTS),
        "forbidden_paths": list(FORBIDDEN_PATHS),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--course-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = build_manifest(args.course_root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output.resolve()}")
    print(f"Pages: {len(payload['pages'])}; learner assets: {len(payload['learner_assets'])}")


if __name__ == "__main__":
    main()
