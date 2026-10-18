from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Mapping

try:
    import fcntl
except ImportError:  # pragma: no cover - exercised by platform policy tests
    fcntl = None


SHA256_LENGTH = 64


class RepairTransactionError(ValueError):
    pass


@dataclass(frozen=True)
class RepairRoute:
    owner_gate: str
    requires_new_course: bool
    revalidation_scope: tuple[str, ...]


def classify_repair_finding(
    code: str, policy: Mapping[str, Any]
) -> RepairRoute:
    if not isinstance(code, str) or not code.strip():
        raise ValueError("repair finding code must contain text")
    new_course = policy.get("new_course_triggers")
    if isinstance(new_course, Mapping) and code in new_course:
        item = new_course[code]
        if not isinstance(item, Mapping):
            raise ValueError(f"invalid new-course route for {code}")
        scope = item.get("revalidation_scope")
        if not isinstance(scope, list) or not all(isinstance(value, str) for value in scope):
            raise ValueError(f"invalid revalidation scope for {code}")
        if item.get("owner_gate") != "G0":
            raise ValueError(f"new-course reframe must start at G0: {code}")
        return RepairRoute("G0", True, tuple(scope))

    routes = policy.get("finding_routes")
    if not isinstance(routes, Mapping) or code not in routes:
        raise ValueError(f"unclassified repair finding: {code}")
    item = routes[code]
    if not isinstance(item, Mapping):
        raise ValueError(f"invalid repair route for {code}")
    owner_gate = item.get("owner_gate")
    scope = item.get("revalidation_scope")
    if owner_gate not in {f"G{index}" for index in range(7)}:
        raise ValueError(f"repair route requires one valid owner Gate: {code}")
    if not isinstance(scope, list) or not scope or not all(
        isinstance(value, str) and value.strip() for value in scope
    ):
        raise ValueError(f"invalid revalidation scope for {code}")
    return RepairRoute(owner_gate, False, tuple(scope))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RepairTransactionError(f"cannot read {label}: {error}") from error
    if not isinstance(value, dict):
        raise RepairTransactionError(f"{label} must be a JSON object")
    return value


def _valid_digest(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == SHA256_LENGTH
        and all(character in "0123456789abcdef" for character in value)
    )


def _relative_path(value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value.strip() or "\\" in value:
        raise RepairTransactionError(f"{label} must be a safe relative POSIX path")
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    if (
        posix.is_absolute()
        or windows.is_absolute()
        or windows.drive
        or posix == PurePosixPath(".")
        or ".." in posix.parts
        or ".." in windows.parts
    ):
        raise RepairTransactionError(f"{label} must be a safe relative POSIX path")
    return Path(*posix.parts)


def _safe_file(root: Path, relative: Path, label: str) -> Path:
    root = root.resolve(strict=True)
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise RepairTransactionError(f"{label} must not contain a symbolic link")
    try:
        current.resolve(strict=True).relative_to(root)
    except (OSError, ValueError) as error:
        raise RepairTransactionError(f"{label} is missing or escapes its root") from error
    if not current.is_file():
        raise RepairTransactionError(f"{label} must be a regular file")
    return current


def _absolute_regular_file(value: Any, label: str) -> Path:
    if not isinstance(value, str):
        raise RepairTransactionError(f"{label} must be an absolute file path")
    path = Path(value)
    if not path.is_absolute():
        raise RepairTransactionError(f"{label} must be an absolute file path")
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise RepairTransactionError(f"{label} must be a regular file") from error
    for parent in (resolved, *resolved.parents):
        if parent.is_symlink():
            raise RepairTransactionError(f"{label} must not contain a symbolic link")
        if parent == parent.parent:
            break
    if not resolved.is_file():
        raise RepairTransactionError(f"{label} must be a regular file")
    return resolved


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    encoded = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(descriptor)
    os.replace(temporary, path)
    _fsync_directory(path.parent)


def _copy_replace(source: Path, target: Path, stage: Path) -> None:
    if stage.exists() or stage.is_symlink():
        raise RepairTransactionError(f"repair staging path already exists: {stage}")
    with source.open("rb") as input_handle:
        descriptor = os.open(stage, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(descriptor, "wb", closefd=False) as output_handle:
                shutil.copyfileobj(input_handle, output_handle)
                output_handle.flush()
                os.fsync(output_handle.fileno())
        finally:
            os.close(descriptor)
    os.replace(stage, target)
    _fsync_directory(target.parent)


def _crash_checkpoint(phase: str) -> None:
    if os.environ.get("COURSE_REPAIR_CRASH_AT") == phase:
        os._exit(94)


@contextmanager
def _operation_lock(state_root: Path):
    if os.name != "posix" or fcntl is None:
        raise RepairTransactionError("repair transactions require POSIX file locking")
    lock_path = state_root / ".course-repair.lock"
    descriptor = os.open(lock_path, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _preflight_proof(
    proof_path: Path, course_root: Path, state_root: Path
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if os.name != "posix" or fcntl is None:
        raise RepairTransactionError("repair transactions require POSIX file locking")
    proof_path = proof_path.resolve(strict=True)
    course_root = course_root.resolve(strict=True)
    state_root = state_root.resolve(strict=True)
    if course_root == state_root or course_root in state_root.parents or state_root in course_root.parents:
        raise RepairTransactionError("course and repair state roots must not overlap")
    proof = _load_json(proof_path, "repair proof")
    if proof.get("schema_version") != 1:
        raise RepairTransactionError("repair proof schema_version must be 1")
    operation_id = proof.get("operation_id")
    if (
        not isinstance(operation_id, str)
        or not operation_id
        or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for character in operation_id)
    ):
        raise RepairTransactionError("repair proof operation_id is invalid")

    plan = proof.get("approved_plan")
    manifest_ref = proof.get("backup_manifest")
    if not isinstance(plan, Mapping) or not isinstance(manifest_ref, Mapping):
        raise RepairTransactionError("repair proof requires approved_plan and backup_manifest")
    plan_path = _safe_file(
        course_root, _relative_path(plan.get("path"), "approved plan path"), "approved plan"
    )
    manifest_path = _safe_file(
        course_root,
        _relative_path(manifest_ref.get("path"), "backup manifest path"),
        "backup manifest",
    )
    for label, path, expected in (
        ("approved plan", plan_path, plan.get("sha256")),
        ("backup manifest", manifest_path, manifest_ref.get("sha256")),
    ):
        if not _valid_digest(expected) or _sha256(path) != expected:
            raise RepairTransactionError(f"{label} SHA-256 does not match")
    manifest = _load_json(manifest_path, "backup manifest")
    targets = manifest.get("targets")
    before_hashes = proof.get("before_hashes")
    mutations = proof.get("mutations")
    restore = proof.get("isolated_restore_proof")
    if not isinstance(targets, list) or not targets:
        raise RepairTransactionError("backup manifest targets must be a non-empty list")
    if not isinstance(before_hashes, Mapping) or not before_hashes:
        raise RepairTransactionError("repair proof requires before_hashes")
    if not isinstance(mutations, list) or not mutations:
        raise RepairTransactionError("repair proof requires mutations")
    if not isinstance(restore, Mapping) or restore.get("verified") is not True:
        raise RepairTransactionError("repair proof requires verified isolated restore proof")
    if restore.get("restored_hashes") != before_hashes:
        raise RepairTransactionError("isolated restore proof hashes do not match before_hashes")
    isolation_value = restore.get("isolation_root")
    if not isinstance(isolation_value, str) or not Path(isolation_value).is_absolute():
        raise RepairTransactionError("isolated restore proof requires an absolute isolation_root")
    isolation_root = Path(isolation_value).resolve(strict=True)
    if isolation_root == course_root or isolation_root in course_root.parents or course_root in isolation_root.parents:
        raise RepairTransactionError("isolated restore proof must be outside the course root")

    manifest_by_path: dict[str, Mapping[str, Any]] = {}
    for item in targets:
        if not isinstance(item, Mapping):
            raise RepairTransactionError("backup manifest target is invalid")
        relative = _relative_path(item.get("path"), "repair target path")
        key = relative.as_posix()
        if key in manifest_by_path:
            raise RepairTransactionError("backup manifest target paths must be unique")
        before = item.get("before_sha256")
        backup_digest = item.get("backup_sha256")
        if not _valid_digest(before) or not _valid_digest(backup_digest) or before != backup_digest:
            raise RepairTransactionError("backup manifest hashes are invalid")
        target = _safe_file(course_root, relative, f"repair target {key}")
        backup_relative = _relative_path(item.get("backup_path"), "backup path")
        backup = _safe_file(course_root, backup_relative, f"repair backup {key}")
        isolated = _safe_file(isolation_root, relative, f"isolated restored target {key}")
        if before_hashes.get(key) != before:
            raise RepairTransactionError("before_hashes do not exactly match backup manifest")
        if _sha256(target) != before or _sha256(backup) != backup_digest or _sha256(isolated) != before:
            raise RepairTransactionError("target, backup or isolated restore SHA-256 mismatch")
        manifest_by_path[key] = item
    if set(before_hashes) != set(manifest_by_path):
        raise RepairTransactionError("before_hashes must cover every and only repair target")

    mutation_by_path: dict[str, Mapping[str, Any]] = {}
    records: list[dict[str, Any]] = []
    for item in mutations:
        if not isinstance(item, Mapping):
            raise RepairTransactionError("repair mutation is invalid")
        relative = _relative_path(item.get("path"), "repair mutation path")
        key = relative.as_posix()
        if key in mutation_by_path or key not in manifest_by_path:
            raise RepairTransactionError("repair mutations must exactly and uniquely match targets")
        replacement = _absolute_regular_file(item.get("replacement_path"), "replacement path")
        replacement_hash = item.get("replacement_sha256")
        if not _valid_digest(replacement_hash) or _sha256(replacement) != replacement_hash:
            raise RepairTransactionError("replacement SHA-256 does not match")
        manifest_item = manifest_by_path[key]
        target = course_root / relative
        backup = course_root / _relative_path(manifest_item["backup_path"], "backup path")
        stage = target.with_name(f".{target.name}.{operation_id}.repair-stage")
        records.append(
            {
                "path": key,
                "target": str(target),
                "before_sha256": manifest_item["before_sha256"],
                "backup": str(backup),
                "replacement": str(replacement),
                "replacement_sha256": replacement_hash,
                "stage": str(stage),
                "phase": "PREPARED",
            }
        )
        mutation_by_path[key] = item
    if set(mutation_by_path) != set(manifest_by_path):
        raise RepairTransactionError("repair mutations must cover every backup manifest target")
    return proof, records


def _write_operation(path: Path, operation: dict[str, Any]) -> None:
    _atomic_json(path, operation)


def _restore_records(
    operation_path: Path, operation: dict[str, Any], course_root: Path
) -> dict[str, Any]:
    records = operation.get("journal")
    if not isinstance(records, list) or not records:
        raise RepairTransactionError("repair operation journal is invalid")
    operation["status"] = "ROLLING_BACK"
    _write_operation(operation_path, operation)
    for record in reversed(records):
        if not isinstance(record, dict):
            raise RepairTransactionError("repair operation journal record is invalid")
        relative = _relative_path(record.get("path"), "operation target path")
        target = course_root / relative
        if str(target) != record.get("target"):
            raise RepairTransactionError("repair operation target authority mismatch")
        backup = Path(str(record.get("backup")))
        if not backup.is_file() or _sha256(backup) != record.get("before_sha256"):
            raise RepairTransactionError("repair recovery backup is missing or inconsistent")
        if target.is_symlink() or not target.is_file():
            raise RepairTransactionError("repair recovery target is missing or unsafe")
        current_hash = _sha256(target)
        if current_hash == record.get("before_sha256"):
            record["phase"] = "ROLLED_BACK"
            _write_operation(operation_path, operation)
            continue
        if current_hash != record.get("replacement_sha256"):
            raise RepairTransactionError("repair recovery target has an unauthorized hash")
        record["phase"] = "ROLLBACK_INTENT"
        _write_operation(operation_path, operation)
        _crash_checkpoint("ROLLBACK_INTENT")
        stage = Path(record["stage"])
        if stage.exists() or stage.is_symlink():
            if stage.is_file() and _sha256(stage) == record.get("before_sha256"):
                os.replace(stage, target)
                _fsync_directory(target.parent)
            else:
                raise RepairTransactionError("repair recovery staging path is inconsistent")
        else:
            _copy_replace(backup, target, stage)
        _crash_checkpoint("TARGET_RESTORED")
        if _sha256(target) != record.get("before_sha256"):
            raise RepairTransactionError("repair recovery failed to restore target")
        record["phase"] = "ROLLED_BACK"
        _write_operation(operation_path, operation)
    operation["status"] = "ROLLED_BACK"
    _write_operation(operation_path, operation)
    return operation


def apply_repair_transaction(
    proof_path: Path | str, course_root: Path | str, state_root: Path | str
) -> dict[str, Any]:
    proof_path = Path(proof_path)
    course_root = Path(course_root)
    state_root = Path(state_root)
    proof, records = _preflight_proof(proof_path, course_root, state_root)
    operation_id = str(proof["operation_id"])
    operations = state_root / "repair-operations"
    operation_path = operations / f"{operation_id}.json"
    if operation_path.exists() or operation_path.is_symlink():
        raise RepairTransactionError("repair operation already exists; recover or inspect it")
    with _operation_lock(state_root):
        # Close the preflight-to-journal race before the first operation write.
        proof, records = _preflight_proof(proof_path, course_root, state_root)
        operations.mkdir(mode=0o700, parents=False, exist_ok=True)
        operation = {
            "schema_version": 1,
            "operation_id": operation_id,
            "status": "PREPARED",
            "course_root": str(course_root.resolve(strict=True)),
            "proof_path": str(proof_path.resolve(strict=True)),
            "proof_sha256": _sha256(proof_path),
            "approved_plan_sha256": proof["approved_plan"]["sha256"],
            "backup_manifest_sha256": proof["backup_manifest"]["sha256"],
            "journal": records,
        }
        _write_operation(operation_path, operation)
        try:
            operation["status"] = "EXECUTING"
            _write_operation(operation_path, operation)
            for record in operation["journal"]:
                target = Path(record["target"])
                if _sha256(target) != record["before_sha256"]:
                    raise RepairTransactionError("repair target changed after preflight")
                record["phase"] = "TARGET_REPLACE_INTENT"
                _write_operation(operation_path, operation)
                _crash_checkpoint("TARGET_REPLACE_INTENT")
                _copy_replace(Path(record["replacement"]), target, Path(record["stage"]))
                _crash_checkpoint("TARGET_REPLACED")
                if _sha256(target) != record["replacement_sha256"]:
                    raise RepairTransactionError("repair target replacement hash mismatch")
                record["phase"] = "APPLIED"
                _write_operation(operation_path, operation)
            operation["status"] = "FINALIZE_INTENT"
            _write_operation(operation_path, operation)
            _crash_checkpoint("FINALIZE_INTENT")
            operation["status"] = "APPLIED"
            _write_operation(operation_path, operation)
            return operation
        except BaseException:
            _restore_records(operation_path, operation, course_root.resolve(strict=True))
            raise


def recover_repair_transaction(
    operation_path: Path | str, course_root: Path | str
) -> dict[str, Any]:
    operation_path = Path(operation_path).resolve(strict=True)
    course_root = Path(course_root).resolve(strict=True)
    operation = _load_json(operation_path, "repair operation")
    if operation.get("course_root") != str(course_root):
        raise RepairTransactionError("repair operation course root does not match")
    status = operation.get("status")
    if status == "ROLLED_BACK":
        return operation
    if status == "APPLIED":
        raise RepairTransactionError("an applied repair requires an explicit rollback command")
    return _restore_records(operation_path, operation, course_root)
