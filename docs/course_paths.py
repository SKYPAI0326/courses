"""Shared, repository-relative scope for bulk course HTML operations.

Underscore *directories* are internal except public _assets. Filenames such
as _unlock.html are not internal. This is scan policy, not an access control.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED = {"node_modules", "tmp", "output"}


def internal_directory(name):
    return (name.startswith(".") or name in EXCLUDED
            or (name.startswith("_") and name != "_assets"))


def is_public_html(path, root=ROOT):
    path, root = Path(path), Path(root).resolve()
    if not path.is_absolute():
        path = root / path
    try:
        relative = path.resolve().relative_to(root)
        lexical = path.relative_to(root)
    except ValueError:
        return False
    return (path.suffix.lower() == ".html"
            and not any(internal_directory(p) for p in relative.parts[:-1])
            and not any(internal_directory(p) for p in lexical.parts[:-1])
            and not path.name.startswith("."))


def iter_public_html(start, root=ROOT):
    """Prune internal trees before descent; never follow directory symlinks."""
    root = Path(root).resolve()
    start = Path(start)
    if not start.is_absolute():
        start = root / start
    if start.is_symlink() or not is_public_html(start / "scope-probe.html", root):
        return
    for directory, dirs, files in os.walk(start, followlinks=False):
        dirs[:] = sorted(d for d in dirs if not internal_directory(d)
                         and not (Path(directory) / d).is_symlink())
        for name in sorted(files):
            path = Path(directory) / name
            if is_public_html(path, root):
                yield path


def is_explicit_lint_target(path, root=ROOT):
    """Allow explicitly named internal templates, but never a foreign checkout."""
    root = Path(root).resolve()
    path = Path(path)
    if not path.is_absolute():
        path = root / path
    try:
        relative = path.resolve().relative_to(root)
        lexical = path.relative_to(root)
    except ValueError:
        return False
    return (path.suffix.lower() == ".html"
            and not any(p.startswith(".") or p in EXCLUDED
                        for p in (*relative.parts[:-1], *lexical.parts[:-1])))
