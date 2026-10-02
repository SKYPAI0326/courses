"""Bounded content inspection and path reference extraction."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .catalog import file_sha256, relative_posix
from .discover import TEXT_SUFFIXES, classify_item


REFERENCE_PATTERN = re.compile(
    r"(?<![\w])(?:\.\.?/)?(?:[\w.-]+/)*[\w.-]+\.(?:html?|css|js|md|markdown|pdf|docx|json|csv|tsv)(?:#[\w.-]+)?"
)
TEXT_LIMIT = 2_000
DEEP_TEXT_LIMIT = 20_000


def _files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(candidate for candidate in path.rglob("*") if candidate.is_file() and not candidate.is_symlink())


def _is_binary(path: Path, data: bytes | None = None) -> bool:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return True
    if data is None:
        data = path.read_bytes()[:4096]
    return b"\x00" in data


def read_text_excerpt(path: Path, deep: bool = False) -> str:
    limit = DEEP_TEXT_LIMIT if deep else TEXT_LIMIT
    data = path.read_bytes()
    if _is_binary(path, data):
        return ""
    return data.decode("utf-8", errors="replace")[:limit]


class _HtmlReferenceParser(HTMLParser):
    def __init__(self, source: str):
        super().__init__()
        self.source = source
        self.references: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for attribute, value in attrs:
            if attribute in {"href", "src", "poster"} and value:
                self.references.append({"source": self.source, "attribute": attribute, "target": value})


def _text_references(source: str, text: str) -> list[dict[str, str]]:
    return [{"source": source, "attribute": "text", "target": value} for value in REFERENCE_PATTERN.findall(text)]


def _outgoing_for_file(root: Path, path: Path) -> list[dict[str, str]]:
    relative = relative_posix(path, root)
    data = path.read_bytes()
    if _is_binary(path, data):
        return []
    text = data.decode("utf-8", errors="replace")
    references: list[dict[str, str]] = []
    if path.suffix.lower() in {".html", ".htm"}:
        parser = _HtmlReferenceParser(relative)
        parser.feed(text)
        references.extend(parser.references)
    references.extend(_text_references(relative, text))
    unique = {}
    for reference in references:
        key = (reference["source"], reference["attribute"], reference["target"])
        unique[key] = reference
    return list(unique.values())


def extract_references(root: Path, scope: Path) -> dict[str, list[dict[str, str]]]:
    root = root.absolute()
    scope = scope.absolute()
    scope_files = _files(scope)
    outgoing = []
    for path in scope_files:
        outgoing.extend(_outgoing_for_file(root, path))

    scope_targets = {
        relative_posix(path, root)
        for path in scope_files
        if not _is_binary(path)
    }
    incoming = []
    for path in _files(root):
        if path in scope_files or _is_binary(path):
            continue
        text = path.read_bytes().decode("utf-8", errors="replace")
        source = relative_posix(path, root)
        for target in sorted(scope_targets):
            if target in text:
                incoming.append({"source": source, "attribute": "text", "target": target})

    return {"outgoing": outgoing, "incoming": incoming, "unknown": []}


def _file_summary(root: Path, path: Path, deep: bool) -> dict[str, Any]:
    data = path.read_bytes()
    binary = _is_binary(path, data)
    text = None
    truncated = False
    if not binary:
        limit = DEEP_TEXT_LIMIT if deep else TEXT_LIMIT
        decoded = data.decode("utf-8", errors="replace")
        text = decoded[:limit]
        truncated = len(decoded) > limit
    return {
        "path": relative_posix(path, root),
        "bytes": len(data),
        "sha256": file_sha256(path),
        "file_type": "binary" if binary else "text",
        "text": text,
        "truncated": truncated,
    }


def inspect_path(root: Path, relative_path: str, deep: bool = False) -> dict[str, Any]:
    root = root.absolute()
    target = (root / relative_path).absolute()
    target.relative_to(root)
    if not target.exists():
        raise FileNotFoundError(relative_path)
    files = _files(target)
    if target == root:
        classification = {
            "kind": "workspace",
            "status": "active",
            "risk": {"move": "blocked", "merge": "requires-review", "reasons": ["workspace root"]},
            "classification_reason": "workspace root",
        }
    else:
        classification = classify_item(root, target)
    return {
        "path": relative_posix(target, root),
        "kind": classification["kind"],
        "status": classification["status"],
        "tree": [relative_posix(path, root) for path in files],
        "file_summaries": [_file_summary(root, path, deep) for path in files],
        "content_signals": classification.get("search_terms", []),
        "references": extract_references(root, target),
        "risk": classification["risk"],
        "classification_reason": classification["classification_reason"],
    }
