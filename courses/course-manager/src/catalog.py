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
