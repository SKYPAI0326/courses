"""Read-only workspace discovery and evidence-based folder classification."""

from __future__ import annotations

import hashlib
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .catalog import SCHEMA_VERSION, file_sha256, relative_posix


SUPPORT_NAMES = {
    ".git",
    ".worktrees",
    "_backup",
    "_deliverables",
    "_repair",
    "_skill-audit",
    "_tools",
    "_validation",
    "assets",
    "docs",
    "output",
    "tmp",
}
SUPPORT_PARTS = SUPPORT_NAMES | {".pytest_cache"}
TEXT_SUFFIXES = {".html", ".htm", ".md", ".markdown", ".txt", ".json", ".js", ".css", ".py", ".sh"}
ASSET_SUFFIXES = {".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".csv", ".tsv", ".json"}
LESSON_PATTERN = re.compile(r"^(?:CH|PRAC|WS|module|m\d|lesson)", re.IGNORECASE)
HEADING_PATTERN = re.compile(r"(?:<title[^>]*>(.*?)</title>|<h[1-3][^>]*>(.*?)</h[1-3]>|^#{1,3}\s+(.+)$)", re.IGNORECASE | re.MULTILINE | re.DOTALL)


def _regular_files(path: Path) -> list[Path]:
    files: list[Path] = []
    for candidate in path.rglob("*"):
        if any(part in {".git", ".worktrees"} for part in candidate.relative_to(path).parts):
            continue
        if candidate.is_symlink():
            continue
        if candidate.is_file():
            files.append(candidate)
    return sorted(files)


def _is_snapshot_path(path: Path, item_root: Path) -> bool:
    relative_parts = path.relative_to(item_root).parts
    return any(part in {"_backup", "_repair", "_validation", ".worktrees", "output", "tmp"} for part in relative_parts)


def _read_search_terms(files: Iterable[Path]) -> list[str]:
    terms: set[str] = set()
    for path in files:
        terms.add(path.stem)
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")[:8000]
        except OSError:
            continue
        for match in HEADING_PATTERN.finditer(text):
            value = next((group for group in match.groups() if group), "")
            value = re.sub(r"\s+", " ", value).strip()
            if value:
                terms.add(value[:160])
    return sorted(terms, key=lambda value: value.casefold())


def _fingerprint(root: Path, files: list[Path]) -> dict[str, Any]:
    entries = []
    digest = hashlib.sha256()
    for path in files:
        relative = relative_posix(path, root)
        checksum = file_sha256(path)
        size = path.stat().st_size
        entries.append({"path": relative, "sha256": checksum, "bytes": size})
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(checksum.encode("ascii"))
        digest.update(b"\n")
    return {"file_count": len(entries), "content_hash": f"sha256:{digest.hexdigest()}", "files": entries}


def _signals(item_root: Path, files: list[Path], learner_html: list[Path]) -> dict[str, Any]:
    names = [path.name for path in files]
    stems = [path.stem for path in files]
    lesson_files = [path for path in files if LESSON_PATTERN.match(path.name)]
    source_files = [
        path
        for path in files
        if path.suffix.lower() in {".docx", ".pdf"}
        or "_plan" in path.name.lower()
        or "_gates" in path.name.lower()
        or "outline" in path.name.lower()
        or "lesson-plan" in path.name.lower()
        or "blueprint" in path.name.lower()
        or path.name.upper().startswith("COURSE-")
    ]
    asset_files = [path for path in files if path.suffix.lower() in ASSET_SUFFIXES]
    return {
        "has_index": any(path.name.lower() == "index.html" for path in learner_html),
        "lesson_signal_count": len(lesson_files),
        "source_signal_count": len(source_files),
        "asset_signal_count": len(asset_files),
        "has_backup": any(part == "_backup" for path in files for part in path.relative_to(item_root).parts),
        "has_restore_script": any("restore" in path.name.lower() and path.suffix.lower() in {".sh", ".py"} for path in files),
        "has_outline": any("outline" in name.lower() for name in names + stems),
        "has_ag": any(path.name == "AGENTS.md" for path in files),
    }


def workspace_git_state(root: Path) -> dict[str, Any]:
    try:
        branch = subprocess.run(
            ["git", "-C", str(root), "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return {"available": False, "branch": None, "status": [], "status_sha256": None}
    return {
        "available": True,
        "branch": branch or None,
        "status": status.splitlines(),
        "status_sha256": hashlib.sha256(status.encode("utf-8")).hexdigest(),
    }


def iter_managed_items(root: Path) -> list[Path]:
    return sorted(
        (
            child
            for child in root.iterdir()
            if child.is_dir()
            and not child.is_symlink()
            and child.name not in {".git", ".worktrees"}
        ),
        key=lambda path: path.name.casefold(),
    )


def classify_item(root: Path, path: Path) -> dict[str, Any]:
    files = _regular_files(path)
    support_root = path.name in SUPPORT_NAMES or path.name.startswith(".") or path.name.startswith("_")
    learner_html = [] if support_root else [
        file
        for file in files
        if file.suffix.lower() in {".html", ".htm"} and not _is_snapshot_path(file, path)
    ]
    html_files = [file for file in files if file.suffix.lower() in {".html", ".htm"}]
    signals = _signals(path, files, learner_html)

    if path.name == "course-manager":
        kind = "management"
        status = "active"
        move_risk = "blocked"
        reason = "management control plane"
    elif path.name in SUPPORT_NAMES or path.name.startswith(".") or path.name.startswith("_"):
        kind = "support"
        status = "active"
        move_risk = "blocked"
        reason = "shared, backup, validation, or management support directory"
    elif learner_html:
        kind = "course-html"
        status = "active"
        move_risk = "blocked-by-default"
        reason = "contains learner-facing HTML and course page signals"
    elif signals["source_signal_count"] > 0:
        kind = "source-only"
        status = "needs-review"
        move_risk = "requires-proposal"
        reason = "contains course source or planning files but no learner-facing HTML"
    elif files:
        kind = "no-handout-project"
        status = "candidate"
        move_risk = "requires-proposal"
        reason = "independent files without learner-facing HTML or course source signals"
    else:
        kind = "unknown"
        status = "needs-review"
        move_risk = "blocked"
        reason = "empty directory has insufficient evidence"

    return {
        "id": relative_posix(path, root),
        "name": path.name,
        "path": relative_posix(path, root),
        "kind": kind,
        "status": status,
        "html_count": len(html_files),
        "learner_html_count": len(learner_html),
        "signals": signals,
        "search_terms": _read_search_terms(files),
        "classification_reason": reason,
        "risk": {"move": move_risk, "merge": "requires-review", "reasons": [reason]},
        "references": {"outgoing": [], "incoming": [], "unknown": []},
        "fingerprint": _fingerprint(root, files),
        "last_verified_at": None,
    }


def scan_workspace(root: Path) -> dict[str, Any]:
    root = root.absolute()
    items = [classify_item(root, path) for path in iter_managed_items(root)]
    return {
        "schema_version": SCHEMA_VERSION,
        "root": ".",
        "scanned_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "git": workspace_git_state(root),
        "items": items,
    }
