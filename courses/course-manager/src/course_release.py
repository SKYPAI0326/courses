from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from src.course_contract import (
    ContractStateError,
    assert_external_action_authorized,
    load_contract,
)


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
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"path escapes release root: {relative}")
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
        "action_id": f"course-release-{manifest_hash[:16]}",
        "status": "PENDING_AUTHORIZATION",
        "manifest": manifest,
        "manifest_sha256": manifest_hash,
        "result": None,
    }


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
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
    finally:
        if temp_path.exists():
            temp_path.unlink()


def apply_release_proposal(proposal_path: Path, contract_path: Path) -> None:
    proposal = json.loads(proposal_path.read_text(encoding="utf-8"))
    if proposal.get("status") != "PENDING_AUTHORIZATION":
        raise ReleaseAuthorizationError("release authorization is missing or already consumed")
    manifest = proposal.get("manifest")
    if not isinstance(manifest, Mapping):
        raise ReleaseAuthorizationError("release proposal manifest is missing")
    manifest_hash = _canonical_hash(manifest)
    if proposal.get("manifest_sha256") != manifest_hash:
        raise ReleaseAuthorizationError("release proposal changed after its hash was created")
    contract = load_contract(contract_path)
    try:
        assert_external_action_authorized(
            contract, proposal.get("action_id", ""), manifest_hash
        )
    except ContractStateError as error:
        raise ReleaseAuthorizationError(str(error)) from error

    root = Path(manifest.get("course_root", ""))
    if not root.is_absolute() or not root.is_dir():
        raise ReleaseAuthorizationError("authorized release root is invalid")
    targets = manifest.get("targets")
    if not isinstance(targets, list) or not targets:
        raise ReleaseAuthorizationError("authorized release has no targets")
    resolved: list[tuple[Mapping[str, Any], Path, Path, Path]] = []
    seen: set[Path] = set()
    for index, item in enumerate(targets):
        if not isinstance(item, Mapping):
            raise ReleaseAuthorizationError(f"target {index} is invalid")
        try:
            source = _safe_path(root, item.get("source_path", ""), must_exist=True)
            target = _safe_path(root, item.get("target_path", ""))
            backup = _safe_path(root, item.get("backup_path", ""))
        except ValueError as error:
            raise ReleaseAuthorizationError(str(error)) from error
        if target in seen or not target.parent.is_dir():
            raise ReleaseAuthorizationError(f"duplicate or invalid target: {target}")
        seen.add(target)
        before = _file_sha256(target) if target.is_file() else None
        if before != item.get("before_sha256"):
            raise ReleaseAuthorizationError(
                f"target changed after authorization: {item.get('target_path')}"
            )
        if _file_sha256(source) != item.get("after_sha256"):
            raise ReleaseAuthorizationError(
                f"release source changed after authorization: {item.get('source_path')}"
            )
        resolved.append((item, source, target, backup))

    applying = dict(proposal)
    applying["status"] = "APPLYING_AUTHORIZATION_CONSUMED"
    applying["result"] = {
        "outcome": "IN_PROGRESS",
        "modified_targets": [],
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    _atomic_write_json(proposal_path, applying)

    applied: list[str] = []
    try:
        for item, _source, target, backup in resolved:
            if item.get("before_sha256") is not None:
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, backup)
                if _file_sha256(backup) != item["before_sha256"]:
                    raise OSError(f"backup verification failed: {item['target_path']}")
        for item, source, target, _backup in resolved:
            _atomic_replace_from_source(source, target)
            if _file_sha256(target) != item["after_sha256"]:
                raise OSError(f"release verification failed: {item['target_path']}")
            applied.append(item["target_path"])
    except Exception:
        for item, _source, target, backup in reversed(resolved):
            if item.get("before_sha256") is None:
                if target.exists():
                    target.unlink()
            elif backup.is_file():
                _atomic_replace_from_source(backup, target)
        applying["status"] = "FAILED_AUTHORIZATION_CONSUMED"
        applying["result"] = {
            "outcome": "FAIL_ROLLED_BACK",
            "modified_targets": applied,
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }
        _atomic_write_json(proposal_path, applying)
        raise

    applying["status"] = "APPLIED"
    applying["result"] = {
        "outcome": "PASS",
        "modified_targets": applied,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "authorization_consumed": True,
    }
    _atomic_write_json(proposal_path, applying)


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
