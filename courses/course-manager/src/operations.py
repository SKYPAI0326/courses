"""Approved, scoped file operations with manifests and rollback support."""

from __future__ import annotations

import base64
import hashlib
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from .catalog import SCHEMA_VERSION, file_sha256, relative_posix


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


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


def _fingerprint(root: Path, path: Path) -> dict[str, Any]:
    entries = []
    digest = hashlib.sha256()
    for file in _files(path):
        relative = relative_posix(file, root)
        checksum = file_sha256(file)
        entries.append({"path": relative, "sha256": checksum, "bytes": file.stat().st_size})
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(checksum.encode("ascii"))
        digest.update(b"\n")
    return {"file_count": len(entries), "content_hash": f"sha256:{digest.hexdigest()}", "files": entries}


def _file_manifest(root: Path, path: Path) -> list[dict[str, Any]]:
    return [
        {"path": relative_posix(file, root), "bytes": file.stat().st_size, "sha256": file_sha256(file)}
        for file in _files(path)
    ]


def _inside(root: Path, relative: str) -> Path:
    root = root.absolute()
    candidate = (root / relative).absolute()
    try:
        candidate.relative_to(root)
        candidate.resolve(strict=False).relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"path escapes workspace: {relative}") from error
    return candidate


def _manager_root(root: Path) -> Path:
    return root / "course-manager"


def _manifest_path(root: Path, operation_id: str) -> Path:
    return _manager_root(root) / "operations" / "manifests" / f"{operation_id}.json"


def _log_path(root: Path) -> Path:
    return _manager_root(root) / "operations" / "logs.jsonl"


def load_approval(path: Path) -> dict[str, Any]:
    approval = _load_json(path)
    if approval.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("approval schema_version must be 1")
    if approval.get("approved") is not True:
        raise ValueError("approval must set approved to true")
    if not approval.get("proposal_id"):
        raise ValueError("approval proposal_id is required")
    try:
        datetime.fromisoformat(approval.get("approved_at", ""))
    except ValueError as error:
        raise ValueError("approval approved_at must be ISO-8601") from error
    return approval


def create_manifest(root: Path, proposal: dict[str, Any]) -> dict[str, Any]:
    root = root.absolute()
    operation_id = f"operation-{uuid.uuid4().hex[:12]}"
    source_rel = proposal["sources"][0]
    destination_rel = proposal["destination"]
    source = _inside(root, source_rel)
    destination = _inside(root, destination_rel)
    return {
        "schema_version": SCHEMA_VERSION,
        "operation_id": operation_id,
        "proposal_id": proposal["proposal_id"],
        "created_at": datetime.now().astimezone().isoformat(),
        "source_fingerprint": proposal.get("source_fingerprint"),
        "before": {
            "source": source_rel,
            "destination": destination_rel,
            "source_files": _file_manifest(root, source),
            "destination_exists": destination.exists(),
            "destination_files": _file_manifest(root, destination) if destination.exists() else [],
        },
        "after": {"destination_files": []},
        "path_replacements": proposal.get("path_replacements", []),
        "applied_replacements": [],
        "rollback_steps": proposal.get("rollback_order", []),
        "completed_steps": [],
        "verification_status": "PENDING",
    }


def _replacement_before_path(root: Path, source_rel: str, record: dict[str, Any]) -> Path:
    path = _inside(root, record["file"])
    if record["file"] == source_rel or record["file"].startswith(source_rel + "/"):
        return path
    return path


def _replacement_after_path(root: Path, source_rel: str, destination_rel: str, record: dict[str, Any]) -> Path:
    record_path = record["file"]
    if record_path == source_rel:
        return _inside(root, destination_rel)
    prefix = source_rel + "/"
    if record_path.startswith(prefix):
        return _inside(root, destination_rel + record_path[len(source_rel):])
    return _inside(root, record_path)


def _validate_proposal(root: Path, proposal: dict[str, Any]) -> tuple[Path, Path]:
    if proposal.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("proposal schema_version must be 1")
    if proposal.get("proposal_type") != "move":
        raise ValueError("only move proposals can be applied")
    if proposal.get("status") == "blocked":
        raise ValueError("proposal is blocked")
    if len(proposal.get("sources", [])) != 1 or not proposal.get("destination"):
        raise ValueError("move proposal must contain one source and one destination")
    source = _inside(root, proposal["sources"][0])
    destination = _inside(root, proposal["destination"])
    if not source.exists():
        raise ValueError("source no longer exists")
    current = _fingerprint(root, source)
    expected = proposal.get("source_fingerprint", {})
    if current.get("content_hash") != expected.get("content_hash") or current.get("file_count") != expected.get("file_count"):
        raise ValueError("source fingerprint changed")
    collisions = proposal.get("evidence", {}).get("destination_collisions", [])
    if collisions:
        raise ValueError("destination collision requires an explicit resolution")
    if destination.exists():
        raise ValueError("destination already exists")
    for record in proposal.get("path_replacements", []):
        path = _replacement_before_path(root, proposal["sources"][0], record)
        if not path.exists() or not path.is_file():
            raise ValueError(f"replacement file no longer exists: {record['file']}")
        if file_sha256(path) != record.get("sha256_before"):
            raise ValueError(f"replacement file changed: {record['file']}")
        data = path.read_bytes()
        if b"\x00" in data or record["old"].encode("utf-8") not in data:
            raise ValueError(f"replacement is not applicable: {record['file']}")
    return source, destination


def append_operation_log(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def apply_proposal(root: Path, proposal_path: Path, approval_path: Path) -> dict[str, Any]:
    root = root.absolute()
    try:
        proposal = _load_json(proposal_path)
        approval = load_approval(approval_path)
        if approval["proposal_id"] != proposal.get("proposal_id"):
            raise ValueError("approval does not match proposal")
        source, destination = _validate_proposal(root, proposal)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        return {"status": "REFUSED", "reason": str(error)}

    manifest = create_manifest(root, proposal)
    manifest_path = _manifest_path(root, manifest["operation_id"])
    _write_json(manifest_path, manifest)
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))
        manifest["completed_steps"].append({"action": "move", "source": proposal["sources"][0], "destination": proposal["destination"]})
        for record in proposal.get("path_replacements", []):
            before_path = _replacement_before_path(root, proposal["sources"][0], record)
            after_path = _replacement_after_path(root, proposal["sources"][0], proposal["destination"], record)
            path = after_path if after_path.exists() else before_path
            before_data = path.read_bytes()
            if file_sha256(path) != record["sha256_before"]:
                raise ValueError(f"replacement file changed during apply: {record['file']}")
            old = record["old"].encode("utf-8")
            new = record["new"].encode("utf-8")
            if old not in before_data:
                raise ValueError(f"replacement is not applicable after move: {record['file']}")
            after_data = before_data.replace(old, new)
            temporary = path.with_name(f".{path.name}.course-manager.tmp")
            temporary.write_bytes(after_data)
            temporary.replace(path)
            manifest["applied_replacements"].append(
                {
                    "file_before": record["file"],
                    "file_after": relative_posix(path, root),
                    "old": record["old"],
                    "new": record["new"],
                    "before_b64": base64.b64encode(before_data).decode("ascii"),
                    "sha256_after": file_sha256(path),
                }
            )
            manifest["completed_steps"].append({"action": "replace", "file": relative_posix(path, root)})
        manifest["after"] = {"destination_files": _file_manifest(root, destination)}
        manifest["verification_status"] = "APPLIED"
        _write_json(manifest_path, manifest)
        append_operation_log(
            _log_path(root),
            {"operation_id": manifest["operation_id"], "proposal_id": manifest["proposal_id"], "status": "APPLIED"},
        )
        return {"status": "APPLIED", "operation_id": manifest["operation_id"], "manifest": str(manifest_path)}
    except Exception as error:
        manifest["after"] = {"destination_files": _file_manifest(root, destination) if destination.exists() else []}
        manifest["verification_status"] = "PARTIAL"
        manifest["error"] = str(error)
        _write_json(manifest_path, manifest)
        append_operation_log(
            _log_path(root),
            {"operation_id": manifest["operation_id"], "proposal_id": manifest["proposal_id"], "status": "PARTIAL", "error": str(error)},
        )
        return {"status": "PARTIAL", "operation_id": manifest["operation_id"], "manifest": str(manifest_path), "reason": str(error)}


def rollback_manifest(root: Path, manifest_path: Path, approval_path: Path) -> dict[str, Any]:
    root = root.absolute()
    try:
        manifest = _load_json(manifest_path)
        approval = load_approval(approval_path)
        if approval["proposal_id"] != manifest.get("proposal_id"):
            raise ValueError("approval does not match manifest")
        if manifest.get("verification_status") not in {"APPLIED", "PARTIAL"}:
            raise ValueError("manifest is not rollback-ready")
        source = _inside(root, manifest["before"]["source"])
        destination = _inside(root, manifest["before"]["destination"])
        if not destination.exists():
            raise ValueError("destination no longer exists")
        if source.exists():
            raise ValueError("source path already exists")
        expected_after = manifest.get("after", {}).get("destination_files", [])
        if _file_manifest(root, destination) != expected_after:
            raise ValueError("destination changed after apply")
        for replacement in manifest.get("applied_replacements", []):
            path = _inside(root, replacement["file_after"])
            if not path.exists() or file_sha256(path) != replacement["sha256_after"]:
                raise ValueError(f"replacement file changed after apply: {replacement['file_after']}")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        return {"status": "REFUSED", "reason": str(error)}

    try:
        source.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(destination), str(source))
        for replacement in manifest.get("applied_replacements", []):
            path = _inside(root, replacement["file_before"])
            before_data = base64.b64decode(replacement["before_b64"])
            temporary = path.with_name(f".{path.name}.course-manager.tmp")
            temporary.write_bytes(before_data)
            temporary.replace(path)
        manifest["verification_status"] = "ROLLED_BACK"
        manifest["rollback_completed_at"] = datetime.now().astimezone().isoformat()
        _write_json(manifest_path, manifest)
        append_operation_log(
            _log_path(root),
            {"operation_id": manifest["operation_id"], "proposal_id": manifest["proposal_id"], "status": "ROLLED_BACK"},
        )
        return {"status": "ROLLED_BACK", "operation_id": manifest["operation_id"], "manifest": str(manifest_path)}
    except Exception as error:
        manifest["verification_status"] = "PARTIAL"
        manifest["rollback_error"] = str(error)
        _write_json(manifest_path, manifest)
        append_operation_log(
            _log_path(root),
            {"operation_id": manifest["operation_id"], "proposal_id": manifest["proposal_id"], "status": "PARTIAL", "error": str(error)},
        )
        return {"status": "PARTIAL", "operation_id": manifest["operation_id"], "manifest": str(manifest_path), "reason": str(error)}
