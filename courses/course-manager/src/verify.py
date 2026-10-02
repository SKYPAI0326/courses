"""Workspace and operation-manifest verification."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from .catalog import file_sha256, relative_posix
from .discover import SUPPORT_NAMES, scan_workspace


SNAPSHOT_PARTS = {"_backup", "_repair", "_validation", ".worktrees", "output", "tmp"}
SUPPORT_PARTS = SUPPORT_NAMES | {"_archive", "_legacy", "_local"}
SNAPSHOT_WARNING_PARTS = SNAPSHOT_PARTS - {".worktrees"}


def _html_files(path: Path) -> list[Path]:
    return sorted(
        candidate
        for candidate in path.rglob("*")
        if candidate.is_file()
        and not candidate.is_symlink()
        and candidate.suffix.lower() in {".html", ".htm"}
        and not any(part in SUPPORT_PARTS or part in SNAPSHOT_PARTS for part in candidate.relative_to(path).parts)
    )


def iter_formal_html(root: Path, catalog: dict[str, Any] | None = None) -> list[Path]:
    root = root.absolute()
    if catalog is None:
        catalog = scan_workspace(root)
    formal: list[Path] = []
    for item in catalog.get("items", []):
        if item.get("kind") != "course-html":
            continue
        path = root / item["path"]
        if path.exists():
            formal.extend(_html_files(path))
    if formal:
        return sorted(set(formal))

    excluded = SUPPORT_NAMES | {"course-manager", "no-web-handouts"}
    for child in sorted(root.iterdir(), key=lambda value: value.name.casefold()):
        if not child.is_dir() or child.name in excluded or child.name.startswith("."):
            continue
        formal.extend(_html_files(child))
    return sorted(set(formal))


class _LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for attribute, value in attrs:
            if attribute in {"href", "src", "poster"} and value is not None:
                self.links.append((attribute, value))


def _is_external(raw: str) -> bool:
    if not raw or raw.startswith("#"):
        return True
    parsed = urlsplit(raw)
    return bool(parsed.scheme or parsed.netloc or parsed.path == "")


def check_local_links(root: Path, html_paths: list[Path]) -> list[dict[str, Any]]:
    root = root.absolute()
    missing: list[dict[str, Any]] = []
    for html_path in sorted(html_paths):
        parser = _LinkParser()
        parser.feed(html_path.read_text(encoding="utf-8", errors="replace"))
        for attribute, raw in parser.links:
            if _is_external(raw):
                continue
            target_value = unquote(urlsplit(raw).path)
            target = (html_path.parent / target_value).absolute()
            try:
                target.resolve(strict=False).relative_to(root.resolve())
            except ValueError:
                missing.append(
                    {
                        "file": relative_posix(html_path, root),
                        "attribute": attribute,
                        "raw": raw,
                        "resolved": str(target),
                        "reason": "outside workspace",
                    }
                )
                continue
            if not target.exists():
                missing.append(
                    {
                        "file": relative_posix(html_path, root),
                        "attribute": attribute,
                        "raw": raw,
                        "resolved": relative_posix(target, root),
                        "reason": "missing target",
                    }
                )
    return missing


def _snapshot_html(root: Path) -> list[Path]:
    return sorted(
        candidate
        for candidate in root.rglob("*")
        if candidate.is_file()
        and not candidate.is_symlink()
        and candidate.suffix.lower() in {".html", ".htm"}
        and any(part in SNAPSHOT_WARNING_PARTS for part in candidate.relative_to(root).parts)
    )


def _formal_fingerprints(root: Path, html_paths: list[Path]) -> dict[str, str]:
    return {relative_posix(path, root): file_sha256(path) for path in html_paths}


def _baseline_html_count(baseline: dict[str, Any] | None) -> int | None:
    if not baseline:
        return None
    if "formal_html_count" in baseline:
        return baseline["formal_html_count"]
    if "baseline" in baseline and isinstance(baseline["baseline"], dict):
        value = baseline["baseline"].get("formal_html_count")
        if value is not None:
            return value
    return None


def verify_workspace(root: Path, baseline: dict[str, Any] | None = None) -> dict[str, Any]:
    root = root.absolute()
    catalog = scan_workspace(root)
    formal_html = iter_formal_html(root, catalog)
    local_links = check_local_links(root, formal_html)
    backup_links = check_local_links(root, _snapshot_html(root))
    unexpected: list[str] = []
    expected_count = _baseline_html_count(baseline)
    if expected_count is not None and expected_count != len(formal_html):
        unexpected.append(f"formal HTML count changed: expected {expected_count}, actual {len(formal_html)}")
    messages = []
    if local_links:
        messages.append(f"{len(local_links)} formal HTML local links are missing or outside the workspace")
    if backup_links:
        messages.append(f"{len(backup_links)} backup/snapshot local links need review")
    if unexpected:
        messages.extend(unexpected)
    if local_links or unexpected:
        status = "BLOCK"
    elif backup_links:
        status = "WARN"
    else:
        status = "PASS"
    return {
        "status": status,
        "counts": {
            "formal_html": len(formal_html),
            "local_links": len(local_links),
            "backup_warnings": len(backup_links),
        },
        "formal_html": [relative_posix(path, root) for path in formal_html],
        "local_links": local_links,
        "fingerprints": _formal_fingerprints(root, formal_html),
        "unexpected_changes": unexpected,
        "messages": messages,
    }


def _manifest_files(root: Path, path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    paths = [path] if path.is_file() else sorted(candidate for candidate in path.rglob("*") if candidate.is_file())
    return [
        {"path": relative_posix(file, root), "bytes": file.stat().st_size, "sha256": file_sha256(file)}
        for file in paths
    ]


def verify_manifest(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    root = root.absolute()
    unexpected: list[str] = []
    destination = root / manifest.get("before", {}).get("destination", "")
    expected = manifest.get("after", {}).get("destination_files", [])
    actual = _manifest_files(root, destination)
    if actual != expected:
        expected_by_path = {row.get("path"): row for row in expected}
        actual_by_path = {row.get("path"): row for row in actual}
        for path in sorted(set(expected_by_path) | set(actual_by_path)):
            if expected_by_path.get(path) != actual_by_path.get(path):
                unexpected.append(f"manifest destination changed: {path}")
    if manifest.get("verification_status") == "APPLIED":
        source = root / manifest.get("before", {}).get("source", "")
        if source.exists():
            unexpected.append(f"source still exists after apply: {manifest['before']['source']}")
    status = "BLOCK" if unexpected else "PASS"
    return {"status": status, "unexpected_changes": unexpected, "destination_files": actual}
