"""Shared, repository-relative scope for bulk course HTML operations.

Underscore *directories* are internal except public _assets. Filenames such
as _unlock.html are not internal. This is scan policy, not an access control.
"""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDED = {"node_modules", "tmp", "output"}


def clean_git_environment(extra=None):
    """Return an environment safe for a separate ``git -C`` invocation."""
    env = os.environ.copy()
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        env.pop(name, None)
    if extra:
        env.update(extra)
    return env


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
    """Yield bulk-scan HTML, honoring gitignore when ``root`` is a checkout.

    Tracked files and non-ignored untracked files remain visible so new course
    pages are checked before their first commit. Ignored build artifacts and
    conflict copies stay out of lint, search, sitemap, and gate bulk scans.
    Outside a Git checkout (for example unit-test fixtures), fall back to the
    filesystem traversal used previously.
    """
    root = Path(root).resolve()
    start = Path(start)
    if not start.is_absolute():
        start = root / start
    if start.is_symlink() or not is_public_html(start / "scope-probe.html", root):
        return

    try:
        pathspec = start.resolve().relative_to(root).as_posix() or "."
        output = subprocess.check_output(
            ["git", "-C", str(root), "ls-files", "--cached", "--others",
             "--exclude-standard", "-z", "--", pathspec],
            stderr=subprocess.DEVNULL,
            env=clean_git_environment(),
        )
    except (OSError, subprocess.CalledProcessError, ValueError):
        output = None

    if output is not None:
        for raw in sorted(part for part in output.split(b"\0") if part):
            path = root / os.fsdecode(raw)
            if not path.is_symlink() and path.is_file() and is_public_html(path, root):
                yield path
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
