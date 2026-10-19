#!/usr/bin/env python3
"""Build and verify WebP previews while retaining clickable originals."""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PAGES = 29
EXPECTED_OCCURRENCES = 79
EXPECTED_PNG_ORIGINALS = 61
MAX_PREVIEW_BYTES = 15 * 1024 * 1024
VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
SRC_RE = re.compile(r"(\bsrc\s*=\s*)([\"'])(.*?)\2", re.IGNORECASE | re.DOTALL)


@dataclass(frozen=True)
class AuditResult:
    page_count: int
    image_occurrences: int
    unique_png_originals: int
    unique_webp_previews: int
    original_bytes: int
    preview_bytes: int
    errors: tuple[str, ...]


@dataclass(frozen=True)
class _Element:
    tag: str
    start: int
    end: int
    attrs: tuple[tuple[str, str | None], ...]


def _line_offsets(text: str) -> list[int]:
    offsets = [0]
    for match in re.finditer("\n", text):
        offsets.append(match.end())
    return offsets


def _absolute_offset(offsets: list[int], position: tuple[int, int]) -> int:
    line, column = position
    return offsets[line - 1] + column


def _local_suffix(value: str) -> str:
    if value.startswith(("http://", "https://", "data:")):
        return ""
    return Path(urlsplit(value).path).suffix.lower()


def _replace_suffix(value: str, suffix: str) -> str:
    parts = urlsplit(value)
    path = str(Path(parts.path).with_suffix(suffix))
    return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))


def _format_anchor(original: str, alt: str, attrs: tuple[tuple[str, str | None], ...]) -> str:
    controlled = {"href", "target", "rel", "aria-label", "download"}
    preserved = [(name, value) for name, value in attrs if name.lower() not in controlled]
    label = f"{alt or '圖片'}｜開啟原圖（新分頁）"
    output = [
        f'href="{html.escape(original, quote=True)}"',
        'target="_blank"',
        'rel="noopener"',
        f'aria-label="{html.escape(label, quote=True)}"',
    ]
    for name, value in preserved:
        output.append(name if value is None else f'{name}="{html.escape(value, quote=True)}"')
    return "<a " + " ".join(output) + ">"


class _TransformParser(HTMLParser):
    def __init__(self, text: str) -> None:
        super().__init__(convert_charrefs=False)
        self.text = text
        self.offsets = _line_offsets(text)
        self.stack: list[_Element] = []
        self.operations: list[tuple[int, int, str]] = []
        self.used_anchors: set[int] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        raw = self.get_starttag_text()
        start = _absolute_offset(self.offsets, self.getpos())
        end = start + len(raw)
        element = _Element(tag.lower(), start, end, tuple(attrs))

        if tag.lower() == "img":
            self._handle_image(element, raw)

        if tag.lower() not in VOID_TAGS:
            self.stack.append(element)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index].tag == lowered:
                del self.stack[index:]
                return

    def _handle_image(self, image: _Element, raw: str) -> None:
        attrs = dict(image.attrs)
        src = attrs.get("src")
        if not src or _local_suffix(src) not in {".png", ".webp", ".svg"}:
            return

        anchor = next((item for item in reversed(self.stack) if item.tag == "a"), None)
        if anchor is not None and (not self.stack or self.stack[-1] is not anchor):
            raise ValueError("image is inside a non-direct image link")
        if anchor is not None and anchor.start in self.used_anchors:
            raise ValueError("multiple images share one direct image link")

        anchor_attrs = anchor.attrs if anchor else ()
        anchor_dict = dict(anchor_attrs)
        suffix = _local_suffix(src)
        if suffix == ".svg":
            original = src
            preview = src
        elif suffix == ".png":
            original = src
            preview = _replace_suffix(src, ".webp")
        else:
            href = anchor_dict.get("href", "")
            original = href if _local_suffix(href) == ".png" else _replace_suffix(src, ".png")
            preview = src

        alt = attrs.get("alt") or ""
        anchor_tag = _format_anchor(original, alt, anchor_attrs)
        changed_image = SRC_RE.sub(
            lambda match: match.group(1) + match.group(2) + preview + match.group(2),
            raw,
            count=1,
        )
        self.operations.append((image.start, image.end, changed_image))

        if anchor is None:
            self.operations.append((image.start, image.start, anchor_tag))
            self.operations.append((image.end, image.end, "</a>"))
        else:
            self.used_anchors.add(anchor.start)
            self.operations.append((anchor.start, anchor.end, anchor_tag))


def transform_html(text: str) -> str:
    parser = _TransformParser(text)
    parser.feed(text)
    transformed = text
    for start, end, replacement in sorted(
        parser.operations,
        key=lambda operation: (operation[0], operation[1]),
        reverse=True,
    ):
        transformed = transformed[:start] + replacement + transformed[end:]
    return transformed


class _AuditParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.stack: list[tuple[str, dict[str, str | None]]] = []
        self.images: list[tuple[dict[str, str | None], dict[str, str | None] | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lowered = tag.lower()
        attributes = dict(attrs)
        if lowered == "img":
            anchor = next((item[1] for item in reversed(self.stack) if item[0] == "a"), None)
            direct = self.stack[-1][1] if self.stack and self.stack[-1][0] == "a" else None
            self.images.append((attributes, direct if direct is anchor else None))
        if lowered not in VOID_TAGS:
            self.stack.append((lowered, attributes))

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == lowered:
                del self.stack[index:]
                return


def _dimensions(path: Path) -> tuple[int, int]:
    process = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    width = re.search(r"pixelWidth:\s*(\d+)", process.stdout)
    height = re.search(r"pixelHeight:\s*(\d+)", process.stdout)
    if not width or not height:
        raise ValueError(f"could not read dimensions: {path}")
    return int(width.group(1)), int(height.group(1))


def audit_course(root: Path) -> AuditResult:
    root = root.resolve()
    pages_with_images = 0
    occurrences = 0
    originals: set[Path] = set()
    previews: set[Path] = set()
    errors: list[str] = []

    for page in sorted(root.glob("*.html")):
        parser = _AuditParser()
        parser.feed(page.read_text(encoding="utf-8"))
        if parser.images:
            pages_with_images += 1
        for image, anchor in parser.images:
            occurrences += 1
            src = image.get("src") or ""
            suffix = _local_suffix(src)
            if suffix not in {".webp", ".svg"}:
                errors.append(f"non-preview display source: {page.name} -> {src}")
            if anchor is None:
                errors.append(f"image lacks direct original link: {page.name} -> {src}")
                continue
            href = anchor.get("href") or ""
            if anchor.get("target") != "_blank":
                errors.append(f"image link lacks target=_blank: {page.name} -> {src}")
            if "noopener" not in (anchor.get("rel") or "").split():
                errors.append(f"image link lacks noopener: {page.name} -> {src}")
            if "download" in anchor:
                errors.append(f"image link still downloads: {page.name} -> {src}")
            expected_label = f"{image.get('alt') or '圖片'}｜開啟原圖（新分頁）"
            if anchor.get("aria-label") != expected_label:
                errors.append(f"image link label mismatch: {page.name} -> {src}")

            display = (page.parent / urlsplit(src).path).resolve()
            original = (page.parent / urlsplit(href).path).resolve()
            if not display.is_file():
                errors.append(f"missing display image: {page.name} -> {src}")
            if not original.is_file():
                errors.append(f"missing original image: {page.name} -> {href}")

            if suffix == ".webp":
                if _local_suffix(href) != ".png":
                    errors.append(f"WebP does not link to PNG: {page.name} -> {href}")
                previews.add(display)
                originals.add(original)
            elif suffix == ".svg" and href != src:
                errors.append(f"SVG original target changed: {page.name} -> {href}")

    for preview in sorted(previews):
        original = preview.with_suffix(".png")
        if not original.is_file() or not preview.is_file():
            continue
        if preview.stat().st_size >= original.stat().st_size:
            errors.append(f"preview is not smaller: {preview.relative_to(root)}")
        try:
            if _dimensions(preview) != _dimensions(original):
                errors.append(f"preview dimensions changed: {preview.relative_to(root)}")
        except (OSError, subprocess.CalledProcessError, ValueError) as exc:
            errors.append(f"dimension check failed: {preview.relative_to(root)}: {exc}")

    original_bytes = sum(path.stat().st_size for path in originals if path.is_file())
    preview_bytes = sum(path.stat().st_size for path in previews if path.is_file())
    return AuditResult(
        page_count=pages_with_images,
        image_occurrences=occurrences,
        unique_png_originals=len(originals),
        unique_webp_previews=len(previews),
        original_bytes=original_bytes,
        preview_bytes=preview_bytes,
        errors=tuple(errors),
    )


def _png_originals(root: Path) -> set[Path]:
    originals: set[Path] = set()
    for page in sorted(root.glob("*.html")):
        parser = _AuditParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for image, anchor in parser.images:
            src = image.get("src") or ""
            if _local_suffix(src) == ".png":
                originals.add((page.parent / urlsplit(src).path).resolve())
            elif _local_suffix(src) == ".webp" and anchor:
                href = anchor.get("href") or ""
                if _local_suffix(href) == ".png":
                    originals.add((page.parent / urlsplit(href).path).resolve())
    return originals


def write_previews(root: Path) -> None:
    originals = _png_originals(root)
    for original in sorted(originals):
        preview = original.with_suffix(".webp")
        subprocess.run(
            ["cwebp", "-quiet", "-mt", "-q", "90", str(original), "-o", str(preview)],
            check=True,
        )
    for page in sorted(root.glob("*.html")):
        source = page.read_text(encoding="utf-8")
        transformed = transform_html(source)
        if transformed != source:
            page.write_text(transformed, encoding="utf-8")


def _print_result(result: AuditResult) -> None:
    reduction = 0.0 if not result.original_bytes else 100 * (1 - result.preview_bytes / result.original_bytes)
    print(
        "WEBP PREVIEW VERIFY: "
        f"pages={result.page_count} occurrences={result.image_occurrences} "
        f"png={result.unique_png_originals} webp={result.unique_webp_previews} "
        f"original={result.original_bytes / 1048576:.2f}MiB "
        f"preview={result.preview_bytes / 1048576:.2f}MiB reduction={reduction:.1f}%"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.write:
        write_previews(ROOT)

    result = audit_course(ROOT)
    errors = list(result.errors)
    if result.page_count != EXPECTED_PAGES:
        errors.append(f"expected {EXPECTED_PAGES} image pages; found {result.page_count}")
    if result.image_occurrences != EXPECTED_OCCURRENCES:
        errors.append(f"expected {EXPECTED_OCCURRENCES} image occurrences; found {result.image_occurrences}")
    if result.unique_png_originals != EXPECTED_PNG_ORIGINALS:
        errors.append(f"expected {EXPECTED_PNG_ORIGINALS} PNG originals; found {result.unique_png_originals}")
    if result.unique_webp_previews != EXPECTED_PNG_ORIGINALS:
        errors.append(f"expected {EXPECTED_PNG_ORIGINALS} WebP previews; found {result.unique_webp_previews}")
    if result.preview_bytes > MAX_PREVIEW_BYTES:
        errors.append(f"preview payload exceeds 15 MiB: {result.preview_bytes / 1048576:.2f} MiB")

    _print_result(result)
    if errors:
        print("WEBP PREVIEW VERIFY: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("WEBP PREVIEW VERIFY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
