"""Read-only proposal builders for new courses, moves, and merges."""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .catalog import SCHEMA_VERSION, file_sha256, relative_posix
from .discover import SUPPORT_NAMES, TEXT_SUFFIXES, classify_item, scan_workspace
from .inspect import inspect_path


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def _resolve_inside(root: Path, value: str) -> Path:
    root = root.absolute()
    candidate = (root / value).absolute()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError(f"path escapes workspace: {value}") from error
    try:
        candidate.resolve(strict=False).relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"path resolves outside workspace: {value}") from error
    if any(part in {".git", ".worktrees"} for part in candidate.relative_to(root).parts):
        raise ValueError(f"managed path is not allowed: {value}")
    return candidate


def _files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(
        candidate
        for candidate in path.rglob("*")
        if candidate.is_file()
        and not candidate.is_symlink()
        and not any(part in {".git", ".worktrees"} for part in candidate.relative_to(path).parts)
    )


def _file_manifest(root: Path, path: Path) -> list[dict[str, Any]]:
    return [
        {
            "path": relative_posix(file, root),
            "bytes": file.stat().st_size,
            "sha256": file_sha256(file),
        }
        for file in _files(path)
    ]


def _formal_html_count(catalog: dict[str, Any]) -> int:
    return sum(item.get("learner_html_count", 0) for item in catalog.get("items", []))


def _base_proposal(proposal_type: str, catalog: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "proposal_id": f"{proposal_type}-{uuid.uuid4().hex[:12]}",
        "proposal_type": proposal_type,
        "created_at": _now(),
        "root": ".",
        "sources": [],
        "destination": None,
        "baseline": {
            "git": catalog.get("git", {}),
            "formal_html_count": _formal_html_count(catalog),
        },
        "evidence": {},
        "decisions_required": [],
        "risk": {"level": "review", "reasons": []},
        "status": "proposed",
    }


def _item_by_path(catalog: dict[str, Any], path: str) -> dict[str, Any] | None:
    return next((item for item in catalog.get("items", []) if item.get("path") == path), None)


def build_new_course_proposal(root: Path, query: str) -> dict[str, Any]:
    root = root.absolute()
    catalog = scan_workspace(root)
    proposal = _base_proposal("new-course", catalog)
    original_tokens = [token for token in re.findall(r"[\w-]+", query) if token]
    tokens = [token.casefold() for token in original_tokens]
    candidates = []
    for item in catalog["items"]:
        if item["kind"] in {"support", "management"}:
            continue
        fields = [
            item.get("name", ""),
            item.get("path", ""),
            item.get("classification_reason", ""),
            *item.get("search_terms", []),
        ]
        matched = [original for original, token in zip(original_tokens, tokens) if any(token in field.casefold() for field in fields)]
        if not matched:
            continue
        evidence = [f"query token: {token}" for token in dict.fromkeys(matched)]
        evidence.append(f"kind: {item['kind']}")
        candidates.append(
            {
                "path": item["path"],
                "kind": item["kind"],
                "score": len(set(value.casefold() for value in matched)),
                "evidence": evidence,
                "fingerprint": item["fingerprint"],
            }
        )
    candidates.sort(key=lambda candidate: (-candidate["score"], candidate["path"].casefold()))
    proposal["candidates"] = candidates[:5]
    proposal["evidence"] = {
        "query": query,
        "candidate_count": len(proposal["candidates"]),
        "catalog_scanned_at": catalog["scanned_at"],
    }
    proposal["decisions_required"] = ["create-new", "reuse-source", "move", "merge", "defer"]
    proposal["risk"] = {
        "level": "review",
        "reasons": ["similarity is evidence only; it does not authorize reuse or merge"],
    }
    return proposal


def _reference_replacements(root: Path, source: Path, destination: Path) -> list[dict[str, Any]]:
    source_rel = relative_posix(source, root)
    destination_rel = relative_posix(destination, root)
    source_files = _files(source)
    old_targets = {
        f"{source_rel}/{file.relative_to(source).as_posix()}":
        f"{destination_rel}/{file.relative_to(source).as_posix()}"
        for file in source_files
    }
    old_targets[source_rel] = destination_rel
    replacements = []
    for file in _files(root):
        if any(part in {".git", ".worktrees", "course-manager"} for part in file.relative_to(root).parts):
            continue
        if file.suffix.lower() not in TEXT_SUFFIXES:
            continue
        data = file.read_bytes()
        if b"\x00" in data:
            continue
        text = data.decode("utf-8", errors="replace")
        for old, new in sorted(old_targets.items()):
            token = re.compile(rf"(?<![\w\-/]){re.escape(old)}(?![\w\-/])")
            if not token.search(text):
                continue
            replacements.append(
                {
                    "file": relative_posix(file, root),
                    "old": old,
                    "new": new,
                    "sha256_before": file_sha256(file),
                }
            )
    return replacements


def _destination_collisions(root: Path, source: Path, destination: Path) -> list[dict[str, Any]]:
    if not destination.exists():
        return []
    if destination.is_file():
        return [{"path": relative_posix(destination, root), "status": "conflict"}]
    source_files = {file.relative_to(source).as_posix(): file for file in _files(source)}
    collisions = []
    for relative, source_file in source_files.items():
        target_file = destination / relative
        if not target_file.exists():
            continue
        status = "identical" if file_sha256(source_file) == file_sha256(target_file) else "conflict"
        collisions.append(
            {
                "path": f"{relative_posix(destination, root)}/{relative}",
                "status": status,
                "source_sha256": file_sha256(source_file),
                "destination_sha256": file_sha256(target_file),
            }
        )
    return collisions


def build_move_proposal(root: Path, source: str, destination: str) -> dict[str, Any]:
    root = root.absolute()
    source_path = _resolve_inside(root, source)
    destination_path = _resolve_inside(root, destination)
    if not source_path.exists():
        raise FileNotFoundError(source)
    if destination_path == source_path or source_path in destination_path.parents:
        raise ValueError("destination cannot be the source or inside the source")

    catalog = scan_workspace(root)
    source_rel = relative_posix(source_path, root)
    item = _item_by_path(catalog, source_rel) or classify_item(root, source_path)
    inspection = inspect_path(root, source_rel)
    replacements = _reference_replacements(root, source_path, destination_path)
    collisions = _destination_collisions(root, source_path, destination_path)
    reasons: list[str] = []
    decisions: list[str] = []
    if item["kind"] == "course-html":
        reasons.append("contains learner-facing HTML")
        decisions.append("formal HTML impact")
    if item["kind"] in {"support", "management"} or source_path.name in SUPPORT_NAMES:
        reasons.append("source is a support or management directory")
        decisions.append("support path handling")
    if replacements:
        reasons.append("path references require explicit replacements")
        decisions.append("approve reference updates")
    if collisions:
        reasons.append("destination has file collisions")
        decisions.append("resolve destination collisions")
    elif destination_path.exists():
        reasons.append("destination already exists")
        decisions.append("choose an empty destination path")

    proposal = _base_proposal("move", catalog)
    proposal.update(
        {
            "sources": [source_rel],
            "destination": relative_posix(destination_path, root),
            "source_fingerprint": item["fingerprint"],
            "source_kind": item["kind"],
            "source_manifest": _file_manifest(root, source_path),
            "path_replacements": replacements,
            "rollback_order": [
                f"restore {relative_posix(destination_path, root)} to {source_rel}",
                "restore approved path replacements from manifest backup",
            ],
            "evidence": {
                "classification": inspection,
                "incoming_references": inspection["references"]["incoming"],
                "outgoing_references": inspection["references"]["outgoing"],
                "destination_collisions": collisions,
                "formal_html_count": _formal_html_count(catalog),
            },
        }
    )
    proposal["decisions_required"] = decisions
    proposal["risk"] = {
        "level": "blocked" if reasons else "review",
        "reasons": reasons or ["no blocking evidence found; explicit approval is still required"],
    }
    proposal["status"] = "blocked" if reasons else "proposed"
    return proposal


def build_merge_proposal(root: Path, source: str, target: str) -> dict[str, Any]:
    root = root.absolute()
    source_path = _resolve_inside(root, source)
    target_path = _resolve_inside(root, target)
    if not source_path.exists():
        raise FileNotFoundError(source)
    if not target_path.exists():
        raise FileNotFoundError(target)
    if not target_path.is_dir() or not source_path.is_dir():
        raise ValueError("merge source and target must be directories")

    catalog = scan_workspace(root)
    source_rel = relative_posix(source_path, root)
    target_rel = relative_posix(target_path, root)
    source_item = _item_by_path(catalog, source_rel) or classify_item(root, source_path)
    target_item = _item_by_path(catalog, target_rel) or classify_item(root, target_path)
    source_files = {file.relative_to(source_path).as_posix(): file for file in _files(source_path)}
    target_files = {file.relative_to(target_path).as_posix(): file for file in _files(target_path)}
    matrix = []
    for relative in sorted(set(source_files) | set(target_files)):
        source_file = source_files.get(relative)
        target_file = target_files.get(relative)
        if source_file and target_file:
            source_hash = file_sha256(source_file)
            target_hash = file_sha256(target_file)
            status = "identical" if source_hash == target_hash else "conflict"
        elif source_file:
            source_hash = file_sha256(source_file)
            target_hash = None
            status = "new"
        else:
            source_hash = None
            target_hash = file_sha256(target_file)
            status = "source-only"
        matrix.append(
            {
                "path": relative,
                "status": status,
                "source_sha256": source_hash,
                "target_sha256": target_hash,
            }
        )

    reasons = []
    decisions = []
    if any(row["status"] == "conflict" for row in matrix):
        reasons.append("same relative paths contain different content")
        decisions.append("resolve conflicting files")
    for label, item in (("source", source_item), ("target", target_item)):
        if item["kind"] == "course-html":
            reasons.append(f"{label} contains learner-facing HTML")
            decisions.append(f"review {label} HTML impact")
        if item["kind"] in {"support", "management"}:
            reasons.append(f"{label} is a support or management directory")
            decisions.append(f"review {label} support path")

    proposal = _base_proposal("merge", catalog)
    proposal.update(
        {
            "sources": [source_rel],
            "destination": target_rel,
            "target": target_rel,
            "source_fingerprint": source_item["fingerprint"],
            "target_fingerprint": target_item["fingerprint"],
            "file_matrix": matrix,
            "evidence": {
                "source_kind": source_item["kind"],
                "target_kind": target_item["kind"],
                "source_file_count": len(source_files),
                "target_file_count": len(target_files),
            },
        }
    )
    proposal["decisions_required"] = decisions
    proposal["risk"] = {
        "level": "blocked" if reasons else "review",
        "reasons": reasons or ["file matrix has no conflicts; explicit approval is still required"],
    }
    proposal["status"] = "blocked" if reasons else "proposed"
    return proposal


def write_proposal(path: Path, proposal: dict[str, Any]) -> None:
    if proposal.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("proposal schema_version must be 1")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(proposal, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)
