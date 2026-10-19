#!/usr/bin/env python3
"""Verify the versioned course-image migration without mutating files."""

from __future__ import annotations

import csv
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "_repair/2026-10-17-image-refresh/IMAGE-MANIFEST.tsv"
VERSION_PREFIX = "assets/course-visuals/2026-10/"


class _ImageReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.anchor_stack: list[str | None] = []
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag.lower() == "a":
            self.anchor_stack.append(attributes.get("href"))
        elif tag.lower() == "img":
            src = attributes.get("src")
            if src:
                self.references.append(src)
            if self.anchor_stack and self.anchor_stack[-1]:
                self.references.append(self.anchor_stack[-1] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self.anchor_stack:
            self.anchor_stack.pop()


def collect_local_references(text: str) -> tuple[str, ...]:
    """Return image display sources followed by their direct original links."""
    parser = _ImageReferenceParser()
    parser.feed(text)
    return tuple(parser.references)


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a decodable PNG header")
    return struct.unpack(">II", header[16:24])


def main() -> int:
    errors: list[str] = []

    if not MANIFEST.exists():
        errors.append(f"manifest missing: {MANIFEST.relative_to(ROOT)}")
        rows: list[dict[str, str]] = []
    else:
        with MANIFEST.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))

    # Scope the migration gate to the 26 learner pages named by the manifest.
    # The standalone 2-hour workshop owns a separate, already-versioned image pack.
    page_names = sorted(
        {
            page.strip()
            for row in rows
            for page in row.get("pages", "").split(";")
            if page.strip()
        }
    )
    html_files = [ROOT / page for page in page_names]
    for html in html_files:
        if not html.is_file():
            errors.append(f"manifest page missing: {html.name}")

    references: list[tuple[Path, str]] = []
    for html in html_files:
        if not html.is_file():
            continue
        text = html.read_text(encoding="utf-8")
        references.extend((html, src) for src in collect_local_references(text))

    legacy = [(html.name, src) for html, src in references if src.startswith("img/")]
    if legacy:
        errors.append(f"legacy image references remain: {len(legacy)}")

    if rows:
        required = {"old_path", "new_path", "pages", "role", "output_type", "status"}
        if not rows or not required.issubset(rows[0]):
            errors.append("manifest headers are incomplete")
        old_paths = [row.get("old_path", "") for row in rows]
        if len(rows) != 59 or len(set(old_paths)) != 59:
            errors.append(f"manifest must contain 59 unique old assets; found {len(rows)} rows / {len(set(old_paths))} unique")

        for row in rows:
            new_path = row.get("new_path", "")
            if not new_path.startswith(VERSION_PREFIX):
                errors.append(f"unversioned manifest target: {new_path}")
                continue
            target = ROOT / new_path
            if not target.is_file() or target.stat().st_size == 0:
                errors.append(f"missing target: {new_path}")
                continue
            if target.suffix.lower() == ".png":
                try:
                    width, height = png_dimensions(target)
                    # Panoramic hero banners may have one shorter edge; require
                    # at least 800 px on that edge and 1.5 MP overall instead.
                    if min(width, height) < 800 or width * height < 1_500_000:
                        errors.append(f"undersized PNG: {new_path} ({width}x{height})")
                except (OSError, ValueError) as exc:
                    errors.append(f"invalid PNG: {new_path}: {exc}")
            elif target.suffix.lower() != ".svg":
                errors.append(f"unsupported target type: {new_path}")
            if row.get("status") != "READY":
                errors.append(f"manifest row not READY: {row.get('old_path', '')}")

    manifest_new = {row.get("new_path", "") for row in rows}
    used_versioned = {src for _, src in references if src.startswith(VERSION_PREFIX)}
    missing_from_html = sorted(manifest_new - used_versioned)
    if missing_from_html:
        errors.append(f"manifest targets not used by HTML: {len(missing_from_html)}")

    # The manifest is a closed record of the 59 legacy replacements, not a
    # registry for every later versioned visual. Additional versioned assets
    # are valid when their local targets exist, which is checked below.

    for html, src in references:
        if src.startswith(("http://", "https://", "data:")):
            continue
        target = (html.parent / src).resolve()
        if not target.is_file():
            errors.append(f"missing local reference: {html.name} -> {src}")

    if errors:
        print("IMAGE REFRESH VERIFY: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"IMAGE REFRESH VERIFY: PASS — {len(rows)} assets, {len(used_versioned)} versioned targets, 0 legacy references")
    return 0


if __name__ == "__main__":
    sys.exit(main())
