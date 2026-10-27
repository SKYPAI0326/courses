"""Pure catalog constants and stable file identity helpers."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


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
