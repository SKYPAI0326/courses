"""Catalog persistence and stable file identity helpers."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1


def relative_posix(path: Path, root: Path) -> str:
    """Return a stable POSIX path without resolving symlink targets."""

    root_abs = Path(os.path.abspath(root))
    path_abs = Path(os.path.abspath(path))
    return path_abs.relative_to(root_abs).as_posix() or "."


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_catalog(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        catalog = json.load(stream)
    if catalog.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported catalog schema: {catalog.get('schema_version')!r}")
    return catalog


def write_catalog(path: Path, catalog: dict[str, Any]) -> None:
    if catalog.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("catalog schema_version must be 1")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def current_workspace_state(root: Path) -> dict[str, Any]:
    from .discover import scan_workspace

    catalog = scan_workspace(root)
    relevant_status = [
        line for line in catalog["git"].get("status", []) if "course-manager/" not in line
    ]
    relevant_git = dict(catalog["git"])
    relevant_git["status"] = relevant_status
    if relevant_git.get("available"):
        status_text = "\n".join(relevant_status)
        if relevant_status:
            status_text += "\n"
        relevant_git["status_sha256"] = hashlib.sha256(status_text.encode("utf-8")).hexdigest()
    return {
        "git": relevant_git,
        "items": {
            item["path"]: item["fingerprint"]["content_hash"]
            for item in catalog["items"]
            if item.get("kind") != "management"
        },
    }


def catalog_is_stale(root: Path, catalog: dict[str, Any]) -> tuple[bool, list[str]]:
    current = current_workspace_state(root)
    reasons: list[str] = []
    stored_git = dict(catalog.get("git", {}))
    stored_status = [line for line in stored_git.get("status", []) if "course-manager/" not in line]
    if stored_git.get("available"):
        stored_text = "\n".join(stored_status)
        if stored_status:
            stored_text += "\n"
        stored_git["status_sha256"] = hashlib.sha256(stored_text.encode("utf-8")).hexdigest()
    current_git = current.get("git", {})
    if stored_git.get("status_sha256") != current_git.get("status_sha256"):
        reasons.append("git status changed")

    stored_items = {
        item["path"]: item.get("fingerprint", {}).get("content_hash")
        for item in catalog.get("items", [])
        if item.get("kind") != "management"
    }
    current_items = current["items"]
    for path in sorted(set(stored_items) | set(current_items)):
        if path not in stored_items:
            reasons.append(f"new item: {path}")
        elif path not in current_items:
            reasons.append(f"removed item: {path}")
        elif stored_items[path] != current_items[path]:
            reasons.append(f"item fingerprint changed: {path}")
    return bool(reasons), reasons


def find_items(catalog: dict[str, Any], query: str, kind: str | None = None) -> list[dict[str, Any]]:
    needle = query.casefold().strip()
    matches = []
    for item in catalog.get("items", []):
        if kind and item.get("kind") != kind:
            continue
        searchable = [
            item.get("name", ""),
            item.get("path", ""),
            item.get("kind", ""),
            item.get("classification_reason", ""),
            *item.get("search_terms", []),
        ]
        if any(needle in value.casefold() for value in searchable if isinstance(value, str)):
            matches.append(item)
    return sorted(matches, key=lambda item: item["path"].casefold())
