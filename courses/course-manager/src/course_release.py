from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Mapping

from src.course_contract import (
    ContractStateError,
    assert_external_action_authorized,
    load_contract,
    validate_contract,
)
from src.transactions import (
    TransactionError,
    begin_external_action_execution_atomic,
    finish_external_action_execution_atomic,
)

try:
    import fcntl
except ImportError:  # pragma: no cover - fail closed on unsupported hosts
    fcntl = None  # type: ignore[assignment]


SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
PLATFORM_PATTERN = re.compile(r'data-platform-version=["\']([^"\']+)["\']')
BUILT_AT_PATTERN = re.compile(r'data-built-at=["\'](\d{4}-\d{2}-\d{2})["\']')
REQUIRED_CHECKS = {
    "technical",
    "links",
    "registration",
    "access",
    "rollback",
    "maintenance",
}


@dataclass(frozen=True)
class ReleaseIssue:
    code: str
    path: str
    message: str


class ReleaseAuthorizationError(ValueError):
    pass


class ReleaseCommittedDurabilityError(OSError):
    """A rename committed but its containing directory fsync was uncertain."""

    committed = True


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _issue(issues: list[ReleaseIssue], code: str, path: str, message: str) -> None:
    issues.append(ReleaseIssue(code, path, message))


def _canonical_hash(value: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_path(root: Path, relative: str, *, must_exist: bool = False) -> Path:
    if not _text(relative):
        raise ValueError("path must contain text")
    posix = PurePosixPath(relative)
    windows = PureWindowsPath(relative)
    if (
        posix.is_absolute()
        or windows.is_absolute()
        or bool(windows.drive)
        or "\\" in relative
        or ".." in posix.parts
        or ".." in windows.parts
        or posix == PurePosixPath(".")
    ):
        raise ValueError(f"path must be a safe POSIX relative path: {relative}")
    rel = Path(*posix.parts)
    root_resolved = root.resolve()
    candidate = (root_resolved / rel).resolve(strict=False)
    try:
        candidate.relative_to(root_resolved)
    except ValueError as error:
        raise ValueError(f"path escapes release root: {relative}") from error
    if must_exist and not candidate.is_file():
        raise ValueError(f"required file does not exist: {relative}")
    return candidate


def validate_release_record(record: Mapping[str, Any]) -> list[ReleaseIssue]:
    issues: list[ReleaseIssue] = []
    if record.get("schema_version") != 1:
        _issue(
            issues,
            "unsupported_release_schema",
            "$.schema_version",
            "release record schema_version must be 1",
        )
    if not _text(record.get("course_id")):
        _issue(issues, "release_identity_missing", "$.course_id", "course id is required")
    if record.get("g5_status") != "PASS":
        _issue(
            issues,
            "g5_pass_required",
            "$.g5_status",
            "G6 readiness requires G5 PASS",
        )
    if record.get("g6_state") != "READY_TO_PUBLISH":
        _issue(
            issues,
            "invalid_g6_state",
            "$.g6_state",
            "G6 state must be READY_TO_PUBLISH before external authorization",
        )
    if record.get("published") is not False:
        _issue(
            issues,
            "g6_cannot_claim_published",
            "$.published",
            "G6 PASS means ready to publish, not already published",
        )

    checks = record.get("checks")
    seen: set[str] = set()
    if not isinstance(checks, list):
        _issue(issues, "release_checks_missing", "$.checks", "release checks must be a list")
    else:
        for index, check in enumerate(checks):
            path = f"$.checks[{index}]"
            if not isinstance(check, Mapping):
                _issue(issues, "release_checks_missing", path, "release check must be an object")
                continue
            check_id = check.get("id")
            evidence = check.get("evidence")
            if not _text(check_id) or check_id in seen:
                _issue(issues, "release_checks_missing", f"{path}.id", "check id is missing or duplicated")
            else:
                seen.add(check_id)
            if check.get("result") != "PASS":
                _issue(issues, "release_check_failed", f"{path}.result", "every release check must pass")
            if (
                not isinstance(evidence, Mapping)
                or not _text(evidence.get("path"))
                or not SHA256_PATTERN.fullmatch(str(evidence.get("sha256", "")))
            ):
                _issue(
                    issues,
                    "release_checks_missing",
                    f"{path}.evidence",
                    "release check requires a path and lowercase SHA-256",
                )
        if seen != REQUIRED_CHECKS:
            _issue(
                issues,
                "release_checks_missing",
                "$.checks",
                "release checks must cover technical, links, registration, access, rollback, and maintenance",
            )

    changes = record.get("changes")
    targets: set[str] = set()
    if not isinstance(changes, list) or not changes:
        _issue(issues, "release_targets_missing", "$.changes", "release must declare target changes")
    else:
        for index, change in enumerate(changes):
            path = f"$.changes[{index}]"
            if not isinstance(change, Mapping):
                _issue(issues, "release_targets_missing", path, "release change must be an object")
                continue
            source = change.get("source_path")
            target = change.get("target_path")
            if not _text(source) or not _text(target):
                _issue(
                    issues,
                    "release_targets_missing",
                    path,
                    "release change requires source_path and target_path",
                )
            elif target in targets:
                _issue(
                    issues,
                    "release_target_duplicate",
                    f"{path}.target_path",
                    f"duplicate release target: {target}",
                )
            else:
                targets.add(target)

    maintenance = record.get("maintenance")
    if not isinstance(maintenance, Mapping):
        _issue(
            issues,
            "maintenance_plan_missing",
            "$.maintenance",
            "release requires a maintenance plan",
        )
    else:
        for field in ("owner", "cadence", "next_review"):
            if not _text(maintenance.get(field)):
                _issue(
                    issues,
                    "maintenance_plan_missing",
                    f"$.maintenance.{field}",
                    f"maintenance {field} is required",
                )
        sources = maintenance.get("freshness_sources")
        if not isinstance(sources, list) or not sources or not all(_text(item) for item in sources):
            _issue(
                issues,
                "maintenance_plan_missing",
                "$.maintenance.freshness_sources",
                "maintenance requires at least one freshness source",
            )
    return issues


def build_release_proposal(
    course_root: Path, record: Mapping[str, Any]
) -> dict[str, Any]:
    issues = validate_release_record(record)
    if issues:
        summary = "; ".join(f"{issue.path}: {issue.message}" for issue in issues)
        raise ValueError(f"invalid release record: {summary}")
    root = course_root.resolve()
    if not root.is_dir():
        raise ValueError(f"course root does not exist: {course_root}")
    record_hash = _canonical_hash(record)
    release_id = f"release-{record['course_id']}-{record_hash[:12]}"
    backup_directory = f".release-backups/{release_id}"
    targets: list[dict[str, Any]] = []
    rollback_targets: list[dict[str, Any]] = []
    seen: set[str] = set()
    for change in record["changes"]:
        source_relative = change["source_path"]
        target_relative = change["target_path"]
        if target_relative in seen:
            raise ValueError(f"duplicate release target: {target_relative}")
        seen.add(target_relative)
        source = _safe_path(root, source_relative, must_exist=True)
        target = _safe_path(root, target_relative)
        if not target.parent.is_dir():
            raise ValueError(f"release target parent does not exist: {target_relative}")
        before_hash = _file_sha256(target) if target.is_file() else None
        after_hash = _file_sha256(source)
        backup_path = f"{backup_directory}/{target_relative}"
        targets.append(
            {
                "source_path": source_relative,
                "target_path": target_relative,
                "before_sha256": before_hash,
                "after_sha256": after_hash,
                "backup_path": backup_path,
            }
        )
        rollback_targets.append(
            {
                "target_path": target_relative,
                "existed_before": before_hash is not None,
                "before_sha256": before_hash,
                "backup_path": backup_path if before_hash is not None else None,
            }
        )
    manifest = {
        "schema_version": 1,
        "course_id": record["course_id"],
        "course_root": str(root),
        "release_record_sha256": record_hash,
        "targets": targets,
        "backup": {
            "directory": backup_directory,
            "required": True,
            "verify_sha256": True,
        },
        "rollback": {
            "strategy": "restore_verified_backups_and_remove_new_targets",
            "targets": rollback_targets,
        },
    }
    manifest_hash = _canonical_hash(manifest)
    return {
        "schema_version": 1,
        "revision": 0,
        "action_id": f"course-release-{manifest_hash[:16]}",
        "status": "PUBLISH_APPROVAL_REQUIRED",
        "manifest": manifest,
        "manifest_sha256": manifest_hash,
        "journal": {"phase": "PENDING", "targets": [], "updated_at": None},
        "result": None,
    }


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        try:
            _fsync_directory(path.parent)
        except OSError as error:
            raise ReleaseCommittedDurabilityError(
                f"proposal replace committed at {path}, but directory fsync failed"
            ) from error
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _atomic_replace_from_source(source: Path, target: Path) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".release", dir=target.parent)
    temp_path = Path(temp_name)
    try:
        with source.open("rb") as source_handle, os.fdopen(fd, "wb") as temp_handle:
            shutil.copyfileobj(source_handle, temp_handle)
            temp_handle.flush()
            os.fsync(temp_handle.fileno())
        os.replace(temp_path, target)
        try:
            _fsync_directory(target.parent)
        except OSError as error:
            raise ReleaseCommittedDurabilityError(
                f"target replace committed at {target}, but directory fsync failed"
            ) from error
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _crash_checkpoint(phase: str, target_index: int) -> None:
    """Test seam: production performs no action; subprocess tests replace it."""


def _require_release_platform() -> None:
    if (
        os.name != "posix"
        or fcntl is None
        or not hasattr(os, "O_NOFOLLOW")
        or not hasattr(os, "O_DIRECTORY")
    ):
        raise ReleaseAuthorizationError(
            "release transactions require POSIX flock, O_NOFOLLOW, and O_DIRECTORY"
        )


@contextmanager
def _release_root_lock(root: Path, timeout: float = 10.0):
    _require_release_platform()
    lock_path = root / ".course-release.lock"
    descriptor = os.open(
        lock_path,
        os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW,
        0o600,
    )
    if not stat.S_ISREG(os.fstat(descriptor).st_mode):
        os.close(descriptor)
        raise ReleaseAuthorizationError("release lock path is not a regular file")
    deadline = time.monotonic() + timeout
    try:
        while True:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError as error:
                if time.monotonic() >= deadline:
                    raise ReleaseAuthorizationError(
                        "timed out waiting for release-root lock"
                    ) from error
                time.sleep(0.01)
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


def _load_proposal(path: Path) -> dict[str, Any]:
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as error:
        raise ReleaseAuthorizationError(
            "proposal path must be a regular non-symlink file"
        ) from error
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ReleaseAuthorizationError(
                "proposal path must be a regular non-symlink file"
            )
        with os.fdopen(os.dup(descriptor), "r", encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        raise ReleaseAuthorizationError(f"release proposal is unreadable: {error}") from error
    finally:
        os.close(descriptor)
    if not isinstance(value, dict):
        raise ReleaseAuthorizationError("release proposal root must be an object")
    required = {
        "schema_version", "revision", "action_id", "status", "manifest",
        "manifest_sha256", "journal", "result",
    }
    if set(value) != required or value.get("schema_version") != 1:
        raise ReleaseAuthorizationError("release proposal has missing or unknown fields")
    revision = value.get("revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 0:
        raise ReleaseAuthorizationError("release proposal revision is invalid")
    if value.get("status") not in {
        "PUBLISH_APPROVAL_REQUIRED", "AUTHORIZED", "EXECUTING", "CONSUMED", "FAILED"
    }:
        raise ReleaseAuthorizationError("release proposal lifecycle state is invalid")
    return value


def _proposal_relative_path(root: Path, proposal_path: Path, *, label: str) -> Path:
    """Return the lexical path below root while rejecting in-root symlinks.

    macOS may expose a real root below ``/private`` through a system ``/var``
    symlink. Find the lexical ancestor that resolves to the governed root, then
    reject symlinks at that boundary or anywhere below it.
    """

    absolute = proposal_path.absolute()
    boundary = next(
        (ancestor for ancestor in absolute.parents if ancestor.resolve() == root),
        None,
    )
    if boundary is None:
        raise ReleaseAuthorizationError(f"{label} escapes release root")
    if boundary.is_symlink():
        raise ReleaseAuthorizationError(f"{label} must not contain symbolic links")
    relative = absolute.relative_to(boundary)
    current = boundary
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ReleaseAuthorizationError(f"{label} must not contain symbolic links")
    return relative


def _proposal_root(proposal: Mapping[str, Any], proposal_path: Path) -> Path:
    manifest = proposal.get("manifest")
    if not isinstance(manifest, Mapping):
        raise ReleaseAuthorizationError("release proposal manifest is missing")
    manifest_hash = _canonical_hash(manifest)
    if proposal.get("manifest_sha256") != manifest_hash:
        raise ReleaseAuthorizationError("release proposal changed after its hash was created")
    root = Path(manifest.get("course_root", ""))
    if not root.is_absolute() or not root.is_dir() or root.is_symlink():
        raise ReleaseAuthorizationError("authorized release root is invalid")
    root = root.resolve()
    _proposal_relative_path(root, proposal_path, label="proposal path")
    return root


def _write_proposal(
    path: Path, proposal: Mapping[str, Any], *, expected_revision: int
) -> dict[str, Any]:
    current = _load_proposal(path)
    if current.get("revision") != expected_revision:
        raise ReleaseAuthorizationError(
            f"proposal revision conflict: expected {expected_revision}, found {current.get('revision')}"
        )
    updated = dict(proposal)
    updated["revision"] = expected_revision + 1
    _atomic_write_json(path, updated)
    return updated


def _set_proposal_state(
    path: Path,
    proposal: Mapping[str, Any],
    status: str,
    *,
    result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    updated = dict(proposal)
    updated["status"] = status
    if result is not None:
        updated["result"] = dict(result)
    return _write_proposal(
        path, updated, expected_revision=int(proposal["revision"])
    )


def _resolve_targets(
    root: Path,
    manifest: Mapping[str, Any],
    *,
    require_before_state: bool = True,
    require_source_state: bool = True,
) -> list[tuple[Mapping[str, Any], Path, Path, Path]]:
    targets = manifest.get("targets")
    if not isinstance(targets, list) or not targets:
        raise ReleaseAuthorizationError("authorized release has no targets")
    resolved: list[tuple[Mapping[str, Any], Path, Path, Path]] = []
    seen: set[Path] = set()
    for index, item in enumerate(targets):
        if not isinstance(item, Mapping):
            raise ReleaseAuthorizationError(f"target {index} is invalid")
        try:
            source = _safe_path(
                root,
                item.get("source_path", ""),
                must_exist=require_source_state,
            )
            target = _safe_path(root, item.get("target_path", ""))
            backup = _safe_path(root, item.get("backup_path", ""))
        except ValueError as error:
            raise ReleaseAuthorizationError(str(error)) from error
        if target in seen or not target.parent.is_dir():
            raise ReleaseAuthorizationError(f"duplicate or invalid target: {target}")
        seen.add(target)
        before = _file_sha256(target) if target.is_file() else None
        if require_before_state and before != item.get("before_sha256"):
            raise ReleaseAuthorizationError(
                f"target changed after authorization: {item.get('target_path')}"
            )
        if require_source_state and _file_sha256(source) != item.get("after_sha256"):
            raise ReleaseAuthorizationError(
                f"release source changed after authorization: {item.get('source_path')}"
            )
        resolved.append((item, source, target, backup))
    return resolved


def _copy_backup(
    root: Path, source: Path, backup: Path, expected_hash: str
) -> None:
    backup.parent.mkdir(parents=True, exist_ok=True)
    current = backup.parent
    while True:
        _fsync_directory(current)
        if current == root:
            break
        current = current.parent
    _atomic_replace_from_source(source, backup)
    if _file_sha256(backup) != expected_hash:
        raise OSError(f"backup verification failed: {backup}")


def _journal_target(item: Mapping[str, Any], phase: str) -> dict[str, Any]:
    return {
        "target_path": item["target_path"],
        "before_sha256": item.get("before_sha256"),
        "after_sha256": item["after_sha256"],
        "backup_path": item.get("backup_path"),
        "phase": phase,
    }


def _update_journal(
    proposal_path: Path,
    proposal: Mapping[str, Any],
    target_entry: Mapping[str, Any],
) -> dict[str, Any]:
    updated = dict(proposal)
    journal = dict(updated.get("journal", {}))
    entries = list(journal.get("targets", []))
    entries = [
        entry for entry in entries
        if not isinstance(entry, Mapping)
        or entry.get("target_path") != target_entry.get("target_path")
    ]
    entries.append(dict(target_entry))
    journal["phase"] = "EXECUTING"
    journal["targets"] = entries
    journal["updated_at"] = datetime.now(timezone.utc).isoformat()
    updated["journal"] = journal
    return _write_proposal(
        proposal_path, updated, expected_revision=int(proposal["revision"])
    )


def _verify_replace_cas(
    proposal_path: Path,
    expected_proposal: Mapping[str, Any],
    item: Mapping[str, Any],
    source: Path,
    target: Path,
) -> None:
    current = _load_proposal(proposal_path)
    expected_manifest = expected_proposal.get("manifest")
    if (
        current.get("revision") != expected_proposal.get("revision")
        or current.get("action_id") != expected_proposal.get("action_id")
        or current.get("manifest_sha256") != expected_proposal.get("manifest_sha256")
        or current.get("manifest") != expected_manifest
        or not isinstance(expected_manifest, Mapping)
        or _canonical_hash(current.get("manifest", {}))
        != expected_proposal.get("manifest_sha256")
    ):
        raise ReleaseAuthorizationError(
            "release proposal manifest/revision CAS failed before target replace"
        )
    before = _file_sha256(target) if target.is_file() else None
    if before != item.get("before_sha256"):
        raise ReleaseAuthorizationError(
            f"target changed immediately before replace: {item['target_path']}"
        )
    if _file_sha256(source) != item.get("after_sha256"):
        raise ReleaseAuthorizationError(
            f"release source changed immediately before replace: {item['source_path']}"
        )


def _rollback_targets(
    resolved: list[tuple[Mapping[str, Any], Path, Path, Path]]
) -> None:
    for item, _source, target, backup in reversed(resolved):
        current = _file_sha256(target) if target.is_file() else None
        before = item.get("before_sha256")
        after = item.get("after_sha256")
        if current == before:
            continue
        if current != after:
            raise ReleaseAuthorizationError(
                f"cannot recover target with unexpected content: {item['target_path']}"
            )
        if before is None:
            target.unlink()
            _fsync_directory(target.parent)
        else:
            if not backup.is_file() or _file_sha256(backup) != before:
                raise ReleaseAuthorizationError(
                    f"verified rollback backup is missing: {item['target_path']}"
                )
            _atomic_replace_from_source(backup, target)
            if _file_sha256(target) != before:
                raise ReleaseAuthorizationError(
                    f"rollback verification failed: {item['target_path']}"
                )


def _validated_recovery_progress(
    proposal: Mapping[str, Any],
    resolved: list[tuple[Mapping[str, Any], Path, Path, Path]],
) -> list[str]:
    """Validate journal/target agreement before any recovery mutation."""

    journal = proposal.get("journal")
    if not isinstance(journal, Mapping):
        raise ReleaseAuthorizationError("release recovery journal is missing")
    phase = journal.get("phase")
    entries = journal.get("targets")
    if phase not in {"PENDING", "EXECUTING"} or not isinstance(entries, list):
        raise ReleaseAuthorizationError("release recovery journal is invalid")
    manifest_by_target = {
        item["target_path"]: item for item, _source, _target, _backup in resolved
    }
    journal_by_target: dict[str, Mapping[str, Any]] = {}
    expected_fields = {
        "target_path", "before_sha256", "after_sha256", "backup_path", "phase"
    }
    for entry in entries:
        if not isinstance(entry, Mapping) or set(entry) != expected_fields:
            raise ReleaseAuthorizationError("release recovery journal entry is invalid")
        target_path = entry.get("target_path")
        item = manifest_by_target.get(target_path)
        if item is None or target_path in journal_by_target:
            raise ReleaseAuthorizationError(
                "release recovery journal target is unknown or duplicated"
            )
        if (
            entry.get("before_sha256") != item.get("before_sha256")
            or entry.get("after_sha256") != item.get("after_sha256")
            or entry.get("backup_path") != item.get("backup_path")
            or entry.get("phase")
            not in {"BACKUP_READY", "BEFORE_REPLACE", "AFTER_REPLACE"}
        ):
            raise ReleaseAuthorizationError(
                "release recovery journal does not match the authorized manifest"
            )
        journal_by_target[str(target_path)] = entry

    modified: list[str] = []
    for item, _source, target, backup in resolved:
        before = item.get("before_sha256")
        after = item.get("after_sha256")
        current = _file_sha256(target) if target.is_file() else None
        entry = journal_by_target.get(str(item["target_path"]))
        if current == before:
            continue
        if current != after:
            raise ReleaseAuthorizationError(
                f"release recovery target has unexpected content: {item['target_path']}"
            )
        if (
            phase != "EXECUTING"
            or entry is None
            or entry.get("phase") not in {"BEFORE_REPLACE", "AFTER_REPLACE"}
        ):
            raise ReleaseAuthorizationError(
                f"release recovery journal cannot prove target replacement: {item['target_path']}"
            )
        if before is not None and (
            not backup.is_file() or _file_sha256(backup) != before
        ):
            raise ReleaseAuthorizationError(
                f"release recovery backup is missing or invalid: {item['target_path']}"
            )
        modified.append(str(item["target_path"]))
    if phase == "PENDING" and entries:
        raise ReleaseAuthorizationError(
            "pending release recovery journal cannot contain target progress"
        )
    return modified


def _contract_action(contract: Mapping[str, Any], action_id: str) -> Mapping[str, Any]:
    matches = [
        item for item in contract.get("external_actions", [])
        if isinstance(item, Mapping) and item.get("id") == action_id
    ]
    if len(matches) != 1:
        raise ReleaseAuthorizationError("release action is missing from contract")
    return matches[0]


def _finish_contract_action(
    contract_path: Path,
    contract: Mapping[str, Any],
    action_id: str,
    status: str,
    modified: list[str],
    error: str | None = None,
) -> dict[str, Any]:
    try:
        return finish_external_action_execution_atomic(
            contract_path,
            action_id,
            status,
            modified,
            datetime.now(timezone.utc).isoformat(),
            error,
            expected_revision=int(contract["revision"]),
        )
    except (ContractStateError, TransactionError) as failure:
        raise ReleaseAuthorizationError(str(failure)) from failure


def _recover_locked(
    proposal_path: Path,
    contract_path: Path,
    proposal: dict[str, Any],
    root: Path,
) -> None:
    manifest = proposal["manifest"]
    resolved = _resolve_targets(
        root,
        manifest,
        require_before_state=False,
        require_source_state=False,
    )
    contract = load_contract(contract_path)
    contract_issues = validate_contract(contract)
    if contract_issues:
        summary = "; ".join(
            f"{issue.path}: {issue.message}" for issue in contract_issues
        )
        raise ReleaseAuthorizationError(
            f"release recovery contract is invalid: {summary}"
        )
    action = _contract_action(contract, proposal["action_id"])
    action_status = action.get("status")
    if action.get("manifest_sha256") != proposal.get("manifest_sha256"):
        raise ReleaseAuthorizationError(
            "contract action and release proposal identity do not match"
        )
    execution = action.get("execution")
    if action_status in {"EXECUTING", "FAILED", "CONSUMED"} and (
        not isinstance(execution, Mapping)
        or isinstance(execution.get("proposal_revision"), bool)
        or not isinstance(execution.get("proposal_revision"), int)
        or proposal.get("revision", -1) < execution["proposal_revision"]
    ):
        raise ReleaseAuthorizationError(
            "contract action and proposal execution revision do not match"
        )
    if action_status == "CONSUMED":
        if any(
            (not target.is_file() or _file_sha256(target) != item.get("after_sha256"))
            for item, _s, target, _b in resolved
        ):
            raise ReleaseAuthorizationError("consumed release targets do not match manifest")
        if proposal.get("status") != "CONSUMED":
            _set_proposal_state(
                proposal_path,
                proposal,
                "CONSUMED",
                result={
                    "outcome": "PASS",
                    "modified_targets": [item["target_path"] for item, *_ in resolved],
                    "finished_at": datetime.now(timezone.utc).isoformat(),
                    "authorization_consumed": True,
                },
            )
        return
    if action_status not in {"EXECUTING", "FAILED"}:
        raise ReleaseAuthorizationError(
            f"release recovery requires EXECUTING/FAILED action, found {action_status!r}"
        )
    modified = _validated_recovery_progress(proposal, resolved)
    _rollback_targets(resolved)
    if action_status == "EXECUTING":
        contract = _finish_contract_action(
            contract_path, contract, proposal["action_id"], "FAILED", modified,
            "interrupted release recovered by deterministic rollback",
        )
    if (
        action_status == "FAILED"
        and proposal.get("status") == "FAILED"
        and isinstance(proposal.get("result"), Mapping)
        and proposal["result"].get("outcome") == "FAIL_ROLLED_BACK"
    ):
        return
    _set_proposal_state(
        proposal_path,
        proposal,
        "FAILED",
        result={
            "outcome": "FAIL_ROLLED_BACK",
            "modified_targets": modified,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "authorization_consumed": True,
        },
    )


def recover_release_proposal(proposal_path: Path, contract_path: Path) -> None:
    proposal_path = Path(proposal_path).absolute()
    proposal = _load_proposal(proposal_path)
    root = _proposal_root(proposal, proposal_path)
    with _release_root_lock(root):
        proposal = _load_proposal(proposal_path)
        _recover_locked(proposal_path, Path(contract_path), proposal, root)


def save_release_proposal(proposal_path: Path, proposal: Mapping[str, Any]) -> None:
    """Create a proposal once under the same release-root lock used by apply."""

    path = Path(proposal_path).absolute()
    manifest = proposal.get("manifest")
    if not isinstance(manifest, Mapping):
        raise ReleaseAuthorizationError("release proposal manifest is missing")
    raw_root = Path(str(manifest.get("course_root", "")))
    if not raw_root.is_absolute() or not raw_root.is_dir() or raw_root.is_symlink():
        raise ReleaseAuthorizationError("release proposal root is invalid")
    root = raw_root.resolve()
    _proposal_relative_path(root, path, label="proposal output")
    if not path.parent.is_dir():
        raise ReleaseAuthorizationError("proposal output parent does not exist")
    if proposal.get("revision") != 0 or proposal.get("status") != "PUBLISH_APPROVAL_REQUIRED":
        raise ReleaseAuthorizationError("new proposal must start at revision 0 awaiting approval")
    if proposal.get("manifest_sha256") != _canonical_hash(manifest):
        raise ReleaseAuthorizationError("new proposal manifest hash is invalid")
    with _release_root_lock(root):
        if path.exists() or path.is_symlink():
            raise ReleaseAuthorizationError("proposal output already exists")
        _atomic_write_json(path, proposal)


def apply_release_proposal(proposal_path: Path, contract_path: Path) -> None:
    proposal_path = Path(proposal_path).absolute()
    contract_path = Path(contract_path)
    proposal = _load_proposal(proposal_path)
    root = _proposal_root(proposal, proposal_path)
    with _release_root_lock(root):
        proposal = _load_proposal(proposal_path)
        root = _proposal_root(proposal, proposal_path)
        if proposal.get("status") not in {"PUBLISH_APPROVAL_REQUIRED", "AUTHORIZED"}:
            raise ReleaseAuthorizationError(
                "release authorization is missing or already consumed"
            )
        manifest = proposal["manifest"]
        manifest_hash = proposal["manifest_sha256"]
        contract = load_contract(contract_path)
        try:
            assert_external_action_authorized(
                contract, proposal.get("action_id", ""), manifest_hash
            )
        except ContractStateError as error:
            raise ReleaseAuthorizationError(str(error)) from error
        resolved = _resolve_targets(root, manifest)
        if proposal["status"] == "PUBLISH_APPROVAL_REQUIRED":
            proposal = _set_proposal_state(proposal_path, proposal, "AUTHORIZED")
        started_at = datetime.now(timezone.utc).isoformat()
        try:
            executing_contract = begin_external_action_execution_atomic(
                contract_path,
                proposal["action_id"],
                manifest_hash,
                int(proposal["revision"]),
                started_at,
                expected_revision=int(contract["revision"]),
            )
        except (ContractStateError, TransactionError) as error:
            raise ReleaseAuthorizationError(str(error)) from error
        executing = dict(proposal)
        executing["journal"] = {
            "phase": "EXECUTING",
            "targets": [],
            "updated_at": started_at,
        }
        proposal = _set_proposal_state(
            proposal_path,
            executing,
            "EXECUTING",
            result={
                "outcome": "IN_PROGRESS",
                "modified_targets": [],
                "started_at": started_at,
            },
        )

        modified: list[str] = []
        try:
            for item, _source, target, backup in resolved:
                if item.get("before_sha256") is not None:
                    if _file_sha256(target) != item["before_sha256"]:
                        raise ReleaseAuthorizationError(
                            f"target changed before backup: {item['target_path']}"
                        )
                    _copy_backup(root, target, backup, item["before_sha256"])
                proposal = _update_journal(
                    proposal_path, proposal, _journal_target(item, "BACKUP_READY")
                )
            for index, (item, source, target, _backup) in enumerate(resolved):
                before = _file_sha256(target) if target.is_file() else None
                if before != item.get("before_sha256"):
                    raise ReleaseAuthorizationError(
                        f"target changed after authorization: {item['target_path']}"
                    )
                if _file_sha256(source) != item.get("after_sha256"):
                    raise ReleaseAuthorizationError(
                        f"release source changed after authorization: {item['source_path']}"
                    )
                proposal = _update_journal(
                    proposal_path, proposal, _journal_target(item, "BEFORE_REPLACE")
                )
                _crash_checkpoint("before_replace", index)
                _verify_replace_cas(
                    proposal_path, proposal, item, source, target
                )
                _atomic_replace_from_source(source, target)
                if _file_sha256(target) != item["after_sha256"]:
                    raise OSError(f"release verification failed: {item['target_path']}")
                proposal = _update_journal(
                    proposal_path, proposal, _journal_target(item, "AFTER_REPLACE")
                )
                modified.append(item["target_path"])
                _crash_checkpoint("after_replace", index)
        except BaseException as error:
            if isinstance(error, (KeyboardInterrupt, SystemExit)):
                raise
            try:
                _rollback_targets(resolved)
                _finish_contract_action(
                    contract_path,
                    executing_contract,
                    proposal["action_id"],
                    "FAILED",
                    modified,
                    str(error),
                )
                _set_proposal_state(
                    proposal_path,
                    proposal,
                    "FAILED",
                    result={
                        "outcome": "FAIL_ROLLED_BACK",
                        "modified_targets": modified,
                        "finished_at": datetime.now(timezone.utc).isoformat(),
                        "authorization_consumed": True,
                    },
                )
            except Exception:
                # Leave EXECUTING journal intact. A later recovery can safely
                # inspect hashes and finish rollback without reviving authority.
                raise
            raise

        _finish_contract_action(
            contract_path,
            executing_contract,
            proposal["action_id"],
            "CONSUMED",
            modified,
        )
        _set_proposal_state(
            proposal_path,
            proposal,
            "CONSUMED",
            result={
                "outcome": "PASS",
                "modified_targets": modified,
                "finished_at": datetime.now(timezone.utc).isoformat(),
                "authorization_consumed": True,
            },
        )


def scan_course_freshness(course_root: Path, as_of: str) -> dict[str, Any]:
    root = course_root.resolve()
    if not root.is_dir():
        raise ValueError(f"course root does not exist: {course_root}")
    try:
        current_date = date.fromisoformat(as_of)
    except ValueError as error:
        raise ValueError("as_of must use YYYY-MM-DD") from error
    items: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.html")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        platform_match = PLATFORM_PATTERN.search(text)
        built_match = BUILT_AT_PATTERN.search(text)
        relative = path.relative_to(root).as_posix()
        if not platform_match or not built_match:
            items.append(
                {
                    "path": relative,
                    "platform_version": platform_match.group(1) if platform_match else None,
                    "built_at": built_match.group(1) if built_match else None,
                    "age_days": None,
                    "severity": "UNKNOWN",
                    "affected_gate": "G6",
                    "recommended_action": "補齊可追溯來源後重新掃描；任何修改需另行授權。",
                }
            )
            continue
        try:
            built_date = date.fromisoformat(built_match.group(1))
        except ValueError:
            age_days = None
        else:
            age_days = (current_date - built_date).days
        if age_days is None or age_days < 0:
            severity, gate, action = (
                "UNKNOWN",
                "G6",
                "查明日期與版本來源後重新掃描。",
            )
        elif age_days <= 90:
            severity, gate, action = ("OK", None, "維持現況，依排程再次掃描。")
        elif age_days <= 180:
            severity, gate, action = (
                "REVIEW",
                "G1",
                "查閱官方版本資料並實際核對代表操作，不直接改課。",
            )
        else:
            severity, gate, action = (
                "STALE",
                "G1",
                "重新驗證平台行為；確認漂移後再由 course-repair 提案修正。",
            )
        items.append(
            {
                "path": relative,
                "platform_version": platform_match.group(1),
                "built_at": built_match.group(1),
                "age_days": age_days,
                "severity": severity,
                "affected_gate": gate,
                "recommended_action": action,
            }
        )
    counts: dict[str, int] = {}
    for item in items:
        counts[item["severity"]] = counts.get(item["severity"], 0) + 1
    return {
        "schema_version": 1,
        "course_root": str(root),
        "as_of": as_of,
        "read_only": True,
        "counts": counts,
        "items": items,
    }
