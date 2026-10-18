#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


PACKAGE_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PACKAGE_ROLES = frozenset({"core", "compatibility", "optional"})
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class InstallError(RuntimeError):
    pass


@dataclass(frozen=True)
class InstallAction:
    name: str
    action: str
    source: Path
    target: Path
    before_hash: str | None
    after_hash: str


@dataclass(frozen=True)
class InstallResult:
    applied: bool
    operation_dir: Path | None
    actions: tuple[InstallAction, ...]


def _load_manifest_records(path: Path) -> tuple[dict[str, str], ...]:
    path = Path(path)
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise InstallError(f"cannot read package manifest {path}: {error}") from error
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise InstallError("package manifest must be a schema_version 1 object")
    packages = manifest.get("packages")
    if not isinstance(packages, list) or not packages:
        raise InstallError("package manifest requires a non-empty packages list")

    records: list[dict[str, str]] = []
    seen: set[str] = set()
    required = {"name", "role", "entrypoint", "baseline_hash"}
    for index, item in enumerate(packages):
        if not isinstance(item, dict) or set(item) != required:
            raise InstallError(
                f"manifest package {index} must contain exactly {sorted(required)}"
            )
        name = item.get("name")
        role = item.get("role")
        entrypoint = item.get("entrypoint")
        baseline_hash = item.get("baseline_hash")
        if not isinstance(name, str) or not PACKAGE_NAME_PATTERN.fullmatch(name):
            raise InstallError(f"invalid package name at manifest index {index}")
        if name in seen:
            raise InstallError(f"duplicate package in manifest: {name}")
        if role not in PACKAGE_ROLES:
            raise InstallError(f"invalid package role for {name}: {role!r}")
        if entrypoint != "SKILL.md":
            raise InstallError(f"unsupported package entrypoint for {name}: {entrypoint!r}")
        if not isinstance(baseline_hash, str) or not SHA256_PATTERN.fullmatch(
            baseline_hash
        ):
            raise InstallError(f"invalid baseline hash for package: {name}")
        seen.add(name)
        records.append(
            {
                "name": name,
                "role": role,
                "entrypoint": entrypoint,
                "baseline_hash": baseline_hash,
            }
        )
    return tuple(records)


def load_package_manifest(path: Path) -> tuple[str, ...]:
    return tuple(record["name"] for record in _load_manifest_records(path))


def _safe_root_argument(
    path: Path,
    label: str,
    *,
    allow_absent: bool = False,
) -> Path:
    expanded = Path(path).expanduser()
    if not expanded.is_absolute():
        raise InstallError(f"{label} must be an absolute path")
    candidate = Path(os.path.abspath(expanded))
    current = Path(candidate.anchor)
    for part in candidate.parts[1:]:
        current = current / part
        if current.is_symlink():
            if current.parent == Path(candidate.anchor):
                continue
            raise InstallError(
                f"unsupported symbolic-link component in {label}: {current}"
            )
    if candidate.exists() and not candidate.is_dir():
        raise InstallError(f"{label} must be a directory: {candidate}")
    if not allow_absent and not candidate.is_dir():
        raise InstallError(f"{label} directory does not exist: {candidate}")
    return candidate


def _paths_overlap(left: Path, right: Path) -> bool:
    left = left.resolve(strict=False)
    right = right.resolve(strict=False)
    try:
        left.relative_to(right)
        return True
    except ValueError:
        pass
    try:
        right.relative_to(left)
        return True
    except ValueError:
        return False


def _repository_root(path: Path) -> Path | None:
    for candidate in (path, *path.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def _validate_install_root_topology(
    packages_root: Path,
    skills_root: Path,
    operations_root: Path | None,
) -> None:
    roots = {
        "packages root": packages_root,
        "skills root": skills_root,
    }
    if operations_root is not None:
        roots["operations root"] = operations_root
    items = tuple(roots.items())
    for index, (left_name, left) in enumerate(items):
        for right_name, right in items[index + 1 :]:
            if _paths_overlap(left, right):
                raise InstallError(
                    f"installer roots overlap: {left_name}={left} and "
                    f"{right_name}={right}"
                )
    repository = _repository_root(packages_root)
    if (
        operations_root is not None
        and repository is not None
        and _paths_overlap(repository, operations_root)
    ):
        raise InstallError(
            f"operations root must be outside the source repository: {repository}"
        )


def _validate_package_tree(root: Path, name: str) -> None:
    if root.is_symlink() or not root.is_dir():
        raise InstallError(f"missing validated package: {root}")
    for path in root.rglob("*"):
        if path.is_symlink():
            raise InstallError(
                f"package {name} contains an unsupported symbolic link: {path}"
            )


def tree_hash(root: Path) -> str:
    root = Path(root)
    if not root.is_dir():
        raise InstallError(f"skill directory does not exist: {root}")
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            digest.update(b"L\\0")
            digest.update(relative.encode("utf-8"))
            digest.update(b"\\0")
            digest.update(os.readlink(path).encode("utf-8"))
        elif path.is_dir():
            digest.update(b"D\\0")
            digest.update(relative.encode("utf-8"))
            digest.update(b"\\0")
        elif path.is_file():
            digest.update(b"F\\0")
            digest.update(relative.encode("utf-8"))
            digest.update(b"\\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
        _fsync_directory(path.parent)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _write_text_durable(path: Path, value: str, *, executable: bool = False) -> None:
    path.write_text(value, encoding="utf-8")
    if executable:
        path.chmod(0o755)
    with path.open("rb") as handle:
        os.fsync(handle.fileno())
    _fsync_directory(path.parent)


def _durable_replace(source: Path, destination: Path) -> None:
    source_parent = source.parent
    destination_parent = destination.parent
    os.replace(source, destination)
    _fsync_directory(destination_parent)
    if source_parent != destination_parent:
        _fsync_directory(source_parent)


def _copy_verified(source: Path, destination: Path, expected_hash: str) -> None:
    shutil.copytree(source, destination, symlinks=True)
    actual_hash = tree_hash(destination)
    if actual_hash != expected_hash:
        raise InstallError(
            f"copy verification failed for {source}: expected {expected_hash}, got {actual_hash}"
        )
    for path in sorted(destination.rglob("*")):
        if path.is_file() and not path.is_symlink():
            with path.open("rb") as handle:
                os.fsync(handle.fileno())
    directories = [
        path for path in destination.rglob("*") if path.is_dir() and not path.is_symlink()
    ]
    for directory in sorted(directories, key=lambda item: len(item.parts), reverse=True):
        _fsync_directory(directory)
    _fsync_directory(destination)
    _fsync_directory(destination.parent)


def _new_operation_dir(operations_root: Path) -> Path:
    operations_root.mkdir(parents=True, exist_ok=True)
    _fsync_directory(operations_root.parent)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    operation_dir = Path(tempfile.mkdtemp(prefix=f"{stamp}-", dir=operations_root))
    _fsync_directory(operations_root)
    return operation_dir


def _rollback_script() -> str:
    return """#!/usr/bin/env python3
import hashlib
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


class RollbackError(RuntimeError):
    pass


def tree_hash(root):
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            digest.update(b"L\\\\0")
            digest.update(relative.encode("utf-8"))
            digest.update(b"\\\\0")
            digest.update(os.readlink(path).encode("utf-8"))
        elif path.is_dir():
            digest.update(b"D\\\\0")
            digest.update(relative.encode("utf-8"))
            digest.update(b"\\\\0")
        elif path.is_file():
            digest.update(b"F\\\\0")
            digest.update(relative.encode("utf-8"))
            digest.update(b"\\\\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def copy_verified(source, destination, expected_hash):
    shutil.copytree(source, destination, symlinks=True)
    if tree_hash(destination) != expected_hash:
        raise RollbackError(f"backup copy verification failed: {source}")


def write_manifest(path, value):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False
        ) as handle:
            temporary = Path(handle.name)
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


operation_dir = Path(__file__).resolve().parent
manifest_path = operation_dir / "manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
if manifest.get("status") != "APPLIED":
    raise SystemExit(f"rollback requires APPLIED manifest, got {manifest.get('status')!r}")

records = manifest.get("packages", [])
for record in records:
    target = Path(record["target"])
    if not target.is_dir() or tree_hash(target) != record["after_hash"]:
        raise SystemExit(f"installed skill changed or is missing: {record['name']}")
    if record["before_exists"]:
        backup = operation_dir / record["backup"]
        if not backup.is_dir() or tree_hash(backup) != record["before_hash"]:
            raise SystemExit(f"verified backup is unavailable: {record['name']}")

states = []
try:
    for record in records:
        target = Path(record["target"])
        container = Path(tempfile.mkdtemp(
            prefix=f".course-skill-rollback-{record['name']}-", dir=target.parent
        ))
        installed = container / "installed"
        state = {
            "container": container,
            "installed": installed,
            "record": record,
            "installed_moved": False,
            "restored_target": False,
        }
        states.append(state)
        os.replace(target, installed)
        state["installed_moved"] = True
        if record["before_exists"]:
            restored = container / "restored"
            copy_verified(operation_dir / record["backup"], restored, record["before_hash"])
            os.replace(restored, target)
            state["restored_target"] = True

    manifest["status"] = "ROLLED_BACK"
    manifest["rolled_back_at"] = datetime.now(timezone.utc).isoformat()
    write_manifest(manifest_path, manifest)
except Exception:
    for state in reversed(states):
        container = state["container"]
        installed = state["installed"]
        record = state["record"]
        target = Path(record["target"])
        if state["restored_target"] and target.exists():
            shutil.rmtree(target)
        if state["installed_moved"] and installed.exists():
            os.replace(installed, target)
        shutil.rmtree(container, ignore_errors=True)
    raise
else:
    for state in states:
        shutil.rmtree(state["container"], ignore_errors=True)
print(f"rolled back: {operation_dir}")
"""


def _remove_directory_if_present(path: Path) -> None:
    if path.is_symlink():
        path.unlink()
    elif path.exists():
        if not path.is_dir():
            raise InstallError(f"refusing to remove non-directory transaction target: {path}")
        shutil.rmtree(path)


def _recover_rollback_states(states: list[dict[str, Any]]) -> None:
    recovery_errors: list[str] = []
    for state in reversed(states):
        record: dict[str, Any] = state["record"]
        target = Path(record["target"])
        container: Path = state["container"]
        installed: Path = state["installed"]
        try:
            if state["restored_target"]:
                _remove_directory_if_present(target)
            if state["installed_moved"] and installed.exists():
                os.replace(installed, target)
        except Exception as error:  # pragma: no cover - catastrophic recovery failure
            recovery_errors.append(f"{record['name']}: {error}")
        finally:
            shutil.rmtree(container, ignore_errors=True)
    if recovery_errors:
        raise InstallError("rollback recovery failed: " + "; ".join(recovery_errors))


def _load_operation_manifest(operation_dir: Path) -> tuple[Path, dict[str, Any]]:
    safe_operation = _safe_root_argument(operation_dir, "operation directory")
    manifest_path = safe_operation / "manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise InstallError(f"operation manifest must be a regular file: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise InstallError(f"cannot read operation manifest {manifest_path}: {error}") from error
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 2:
        raise InstallError("crash recovery requires a schema_version 2 operation manifest")
    records = manifest.get("packages")
    if not isinstance(records, list) or not records:
        raise InstallError("operation manifest has no recoverable package records")
    return manifest_path, manifest


def _record_target(record: dict[str, Any]) -> Path:
    target_value = record.get("target")
    if not isinstance(target_value, str):
        raise InstallError("operation record target is invalid")
    return _safe_root_argument(
        Path(target_value),
        f"operation target for {record.get('name', '<unknown>')}",
        allow_absent=True,
    )


def _verified_tree_hash(path: Path, label: str) -> str:
    if path.is_symlink() or not path.is_dir():
        raise InstallError(f"{label} must be a non-symlink directory")
    _validate_package_tree(path, label)
    return tree_hash(path)


def _recover_package_record(
    operation_dir: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    record: dict[str, Any],
) -> None:
    name = record.get("name")
    if not isinstance(name, str) or not PACKAGE_NAME_PATTERN.fullmatch(name):
        raise InstallError("operation record package name is invalid")
    before_exists = record.get("before_exists")
    before_hash = record.get("before_hash")
    after_hash = record.get("after_hash")
    if not isinstance(before_exists, bool) or not isinstance(after_hash, str):
        raise InstallError(f"operation record hashes are invalid: {name}")
    if not SHA256_PATTERN.fullmatch(after_hash):
        raise InstallError(f"operation after hash is invalid: {name}")
    if before_exists and (
        not isinstance(before_hash, str) or not SHA256_PATTERN.fullmatch(before_hash)
    ):
        raise InstallError(f"operation before hash is invalid: {name}")
    if not before_exists and before_hash is not None:
        raise InstallError(f"unexpected before hash for added package: {name}")

    target = _record_target(record)
    current_hash: str | None = None
    if target.exists() or target.is_symlink():
        current_hash = _verified_tree_hash(target, f"installed target {name}")
        allowed = {after_hash}
        if before_exists:
            allowed.add(before_hash)
        if current_hash not in allowed:
            raise InstallError(
                f"refusing recovery because target changed after crash: {name}"
            )

    backup: Path | None = None
    if before_exists:
        backup_value = record.get("backup")
        if not isinstance(backup_value, str):
            raise InstallError(f"verified backup path is missing: {name}")
        backup = operation_dir / backup_value
        if backup.parent != operation_dir / "backups":
            raise InstallError(f"backup path escapes operation directory: {name}")
        if _verified_tree_hash(backup, f"backup {name}") != before_hash:
            raise InstallError(f"verified backup differs from before hash: {name}")

    if (before_exists and current_hash == before_hash) or (
        not before_exists and current_hash is None
    ):
        record["phase"] = "RECOVERED"
        _write_json_atomic(manifest_path, manifest)
    else:
        recovery = Path(
            tempfile.mkdtemp(prefix=f".course-skill-recover-{name}-", dir=target.parent)
        )
        record["recovery_container"] = str(recovery)
        record["phase"] = "RECOVERY_INTENT"
        _write_json_atomic(manifest_path, manifest)
        quarantined = recovery / "quarantined"
        if current_hash is not None:
            _durable_replace(target, quarantined)
            record["phase"] = "TARGET_QUARANTINED"
            _write_json_atomic(manifest_path, manifest)
        if before_exists:
            assert backup is not None and before_hash is not None
            restored = recovery / "restored"
            _copy_verified(backup, restored, before_hash)
            record["phase"] = "RESTORE_INTENT"
            _write_json_atomic(manifest_path, manifest)
            _durable_replace(restored, target)
        record["phase"] = "RECOVERED"
        _write_json_atomic(manifest_path, manifest)
        shutil.rmtree(recovery, ignore_errors=True)

    container_value = record.get("container")
    if isinstance(container_value, str):
        container = Path(container_value)
        if container.parent == target.parent and container.name.startswith(
            f".course-skill-{name}-"
        ):
            shutil.rmtree(container, ignore_errors=True)


def recover_install(
    operation_dir: Path,
    *,
    final_status: str = "RECOVERED",
) -> None:
    """Roll an interrupted PREPARED/EXECUTING install back to its before state."""

    if final_status not in {"RECOVERED", "FAILED"}:
        raise ValueError("recovery final status must be RECOVERED or FAILED")
    operation_dir = _safe_root_argument(operation_dir, "operation directory")
    manifest_path, manifest = _load_operation_manifest(operation_dir)
    status = manifest.get("status")
    if status not in {"PREPARED", "EXECUTING"}:
        raise InstallError(
            f"recovery requires PREPARED or EXECUTING manifest, got {status!r}"
        )
    for record in reversed(manifest["packages"]):
        if not isinstance(record, dict):
            raise InstallError("operation package record must be an object")
        _recover_package_record(
            operation_dir, manifest_path, manifest, record
        )
    manifest["status"] = final_status
    manifest["recovered_at"] = datetime.now(timezone.utc).isoformat()
    _write_json_atomic(manifest_path, manifest)


def _reject_unfinished_operations(operations_root: Path) -> None:
    if not operations_root.exists():
        return
    for manifest_path in sorted(operations_root.glob("*/manifest.json")):
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise InstallError(
                f"cannot inspect prior operation manifest {manifest_path}: {error}"
            ) from error
        if manifest.get("status") in {"PREPARED", "EXECUTING"}:
            raise InstallError(
                "unfinished install must be recovered before a new apply: "
                f"{manifest_path.parent}"
            )


def install(
    packages_root: Path,
    skills_root: Path,
    operations_root: Path | None,
    apply: bool,
    package_names: Sequence[str] | None = None,
    allow_updates: Sequence[str] = (),
) -> InstallResult:
    packages_root = _safe_root_argument(Path(packages_root), "packages root")
    skills_root = _safe_root_argument(
        Path(skills_root), "skills root", allow_absent=True
    )
    operations_root = (
        _safe_root_argument(
            Path(operations_root), "operations root", allow_absent=True
        )
        if operations_root is not None
        else None
    )
    _validate_install_root_topology(packages_root, skills_root, operations_root)
    records = _load_manifest_records(packages_root / "manifest.json")
    manifest_names = tuple(record["name"] for record in records)
    record_by_name = {record["name"]: record for record in records}
    selected_names = tuple(package_names) if package_names is not None else manifest_names
    if not selected_names:
        raise InstallError("at least one package must be selected")
    if len(selected_names) != len(set(selected_names)):
        raise InstallError("selected package names must not repeat")
    unknown_names = sorted(set(selected_names) - set(manifest_names))
    if unknown_names:
        raise InstallError(
            f"selected packages are absent from manifest: {', '.join(unknown_names)}"
        )
    allowed_updates = set(allow_updates)
    unknown_allowances = sorted(allowed_updates - set(selected_names))
    if unknown_allowances:
        raise InstallError(
            "update allowances must name selected manifest packages: "
            + ", ".join(unknown_allowances)
        )
    actions: list[InstallAction] = []

    for name in selected_names:
        source = packages_root / name
        _validate_package_tree(source, name)
        entrypoint = source / record_by_name[name]["entrypoint"]
        if entrypoint.is_symlink() or not entrypoint.is_file():
            raise InstallError(f"missing package entrypoint: {entrypoint}")
        target = skills_root / name
        if target.is_symlink():
            raise InstallError(f"unsupported symbolic-link skill target: {target}")
        if target.exists() and not target.is_dir():
            raise InstallError(f"skill target must be a directory or absent: {target}")
        if target.is_dir():
            _validate_package_tree(target, name)
        before_hash = tree_hash(target) if target.is_dir() else None
        after_hash = tree_hash(source)
        if after_hash != record_by_name[name]["baseline_hash"]:
            raise InstallError(
                f"package source differs from manifest baseline: {name}"
            )
        if before_hash is None:
            action_type = "ADD"
        elif before_hash == after_hash:
            action_type = "UNCHANGED"
        else:
            action_type = "UPDATE"
        actions.append(
            InstallAction(
                name=name,
                action=action_type,
                source=source,
                target=target,
                before_hash=before_hash,
                after_hash=after_hash,
            )
        )

    if not apply:
        return InstallResult(False, None, tuple(actions))

    if operations_root is None:
        raise InstallError("an external operations root is required for apply")

    unauthorized_updates = [
        action.name
        for action in actions
        if action.action == "UPDATE" and action.name not in allowed_updates
    ]
    if unauthorized_updates:
        raise InstallError(
            "installed packages differ from the versioned baseline; rerun with "
            "explicit update allowance for: " + ", ".join(unauthorized_updates)
        )

    mutable_actions = [action for action in actions if action.action != "UNCHANGED"]
    if not mutable_actions:
        return InstallResult(False, None, tuple(actions))

    _reject_unfinished_operations(operations_root)
    skills_root.mkdir(parents=True, exist_ok=True)
    operation_dir = _new_operation_dir(operations_root)
    backups_dir = operation_dir / "backups"
    backups_dir.mkdir()
    _fsync_directory(operation_dir)
    package_records: list[dict[str, Any]] = []

    try:
        for action in mutable_actions:
            backup_path: Path | None = None
            if action.before_hash is not None:
                backup_path = backups_dir / action.name
                _copy_verified(action.target, backup_path, action.before_hash)
            package_records.append(
                {
                    "name": action.name,
                    "action": action.action,
                    "source": str(action.source),
                    "target": str(action.target),
                    "before_exists": action.before_hash is not None,
                    "before_hash": action.before_hash,
                    "after_hash": action.after_hash,
                    "backup": (
                        backup_path.relative_to(operation_dir).as_posix()
                        if backup_path is not None
                        else None
                    ),
                    "phase": "PREPARED",
                    "container": None,
                    "recovery_container": None,
                }
            )

        manifest = {
            "schema_version": 2,
            "status": "PREPARED",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "installer_path": str(Path(__file__).resolve()),
            "allowed_updates": sorted(allowed_updates),
            "packages": package_records,
        }
        manifest_path = operation_dir / "manifest.json"
        _write_json_atomic(manifest_path, manifest)
        _write_text_durable(
            operation_dir / "rollback.py", _rollback_script(), executable=True
        )

        package_record_by_name = {
            record["name"]: record for record in package_records
        }
        for action in mutable_actions:
            record = package_record_by_name[action.name]
            container = Path(
                tempfile.mkdtemp(
                    prefix=f".course-skill-{action.name}-", dir=skills_root
                )
            )
            record["container"] = str(container)
            record["phase"] = "STAGING"
            _write_json_atomic(manifest_path, manifest)
            staged = container / "staged"
            _copy_verified(action.source, staged, action.after_hash)
            manifest["status"] = "EXECUTING"
            record["phase"] = "PREVIOUS_MOVE_INTENT"
            _write_json_atomic(manifest_path, manifest)
            if action.target.exists():
                previous = container / "previous"
                _durable_replace(action.target, previous)
                record["phase"] = "PREVIOUS_MOVED"
                _write_json_atomic(manifest_path, manifest)
            record["phase"] = "TARGET_REPLACE_INTENT"
            _write_json_atomic(manifest_path, manifest)
            _durable_replace(staged, action.target)
            record["phase"] = "TARGET_REPLACED"
            _write_json_atomic(manifest_path, manifest)
            if tree_hash(action.target) != action.after_hash:
                raise InstallError(f"installed hash mismatch: {action.target}")
            record["phase"] = "VERIFIED"
            _write_json_atomic(manifest_path, manifest)

        manifest["status"] = "APPLIED"
        manifest["applied_at"] = datetime.now(timezone.utc).isoformat()
        for record in package_records:
            record["phase"] = "APPLIED"
        _write_json_atomic(manifest_path, manifest)
        for record in package_records:
            container_value = record.get("container")
            if isinstance(container_value, str):
                shutil.rmtree(Path(container_value), ignore_errors=True)
        return InstallResult(True, operation_dir, tuple(actions))
    except Exception as original_error:
        recovery_error: Exception | None = None
        manifest_path = operation_dir / "manifest.json"
        if manifest_path.exists():
            try:
                interrupted = json.loads(manifest_path.read_text(encoding="utf-8"))
                if interrupted.get("status") in {"PREPARED", "EXECUTING"}:
                    recover_install(operation_dir, final_status="FAILED")
            except Exception as error:  # pragma: no cover - catastrophic and re-raised
                recovery_error = error
        if recovery_error is not None:
            raise recovery_error from original_error
        raise


def verify_source_packages(
    packages_root: Path,
    package_names: Sequence[str] | None = None,
) -> dict[str, str]:
    packages_root = _safe_root_argument(Path(packages_root), "packages root")
    records = _load_manifest_records(packages_root / "manifest.json")
    record_by_name = {record["name"]: record for record in records}
    selected = tuple(package_names) if package_names is not None else tuple(record_by_name)
    if not selected or len(selected) != len(set(selected)):
        raise InstallError("source verification requires unique manifest package names")
    unknown = sorted(set(selected) - set(record_by_name))
    if unknown:
        raise InstallError(
            "source verification packages are absent from manifest: "
            + ", ".join(unknown)
        )
    verified: dict[str, str] = {}
    for name in selected:
        source = packages_root / name
        _validate_package_tree(source, name)
        expected = record_by_name[name]["baseline_hash"]
        actual = tree_hash(source)
        if actual != expected:
            raise InstallError(f"package source differs from manifest baseline: {name}")
        verified[name] = actual
    return verified


def verify_installed_packages(
    packages_root: Path,
    skills_root: Path,
    package_names: Sequence[str] | None = None,
) -> dict[str, str]:
    packages_root = _safe_root_argument(Path(packages_root), "packages root")
    skills_root = _safe_root_argument(Path(skills_root), "skills root")
    records = _load_manifest_records(packages_root / "manifest.json")
    record_by_name = {record["name"]: record for record in records}
    selected = tuple(package_names) if package_names is not None else tuple(record_by_name)
    if not selected or len(selected) != len(set(selected)):
        raise InstallError("verification requires unique manifest package names")
    unknown = sorted(set(selected) - set(record_by_name))
    if unknown:
        raise InstallError(
            "verification packages are absent from manifest: " + ", ".join(unknown)
        )
    verified: dict[str, str] = {}
    for name in selected:
        target = skills_root / name
        expected = record_by_name[name]["baseline_hash"]
        if target.is_symlink() or not target.is_dir():
            raise InstallError(f"installed skill is missing: {name}")
        _validate_package_tree(target, name)
        actual = tree_hash(target)
        if actual != expected:
            raise InstallError(
                f"installed skill differs from manifest baseline: {name}"
            )
        verified[name] = actual
    return verified


def rollback_install(operation_dir: Path) -> None:
    operation_dir = _safe_root_argument(
        Path(operation_dir), "operation directory"
    )
    manifest_path = operation_dir / "manifest.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise InstallError(f"operation manifest must be a regular file: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") in {"PREPARED", "EXECUTING"}:
        recover_install(operation_dir)
        return
    if manifest.get("status") != "APPLIED":
        raise InstallError(
            f"rollback requires APPLIED manifest, got {manifest.get('status')!r}"
        )

    records = manifest.get("packages", [])
    for record in records:
        target = Path(record["target"])
        if not target.is_dir():
            raise InstallError(f"installed target is missing: {target}")
        current_hash = tree_hash(target)
        if current_hash != record["after_hash"]:
            raise InstallError(
                f"installed skill changed after install: {record['name']}"
            )
        if record["before_exists"]:
            backup = operation_dir / record["backup"]
            if not backup.is_dir() or tree_hash(backup) != record["before_hash"]:
                raise InstallError(f"verified backup is unavailable: {record['name']}")

    swap_states: list[dict[str, Any]] = []
    try:
        for record in records:
            target = Path(record["target"])
            container = Path(
                tempfile.mkdtemp(
                    prefix=f".course-skill-rollback-{record['name']}-",
                    dir=target.parent,
                )
            )
            installed = container / "installed"
            state: dict[str, Any] = {
                "container": container,
                "installed": installed,
                "record": record,
                "installed_moved": False,
                "restored_target": False,
            }
            swap_states.append(state)
            os.replace(target, installed)
            state["installed_moved"] = True
            if record["before_exists"]:
                staged = container / "restored"
                backup = operation_dir / record["backup"]
                _copy_verified(backup, staged, record["before_hash"])
                os.replace(staged, target)
                state["restored_target"] = True

        manifest["status"] = "ROLLED_BACK"
        manifest["rolled_back_at"] = datetime.now(timezone.utc).isoformat()
        _write_json_atomic(manifest_path, manifest)
    except Exception as original_error:
        try:
            _recover_rollback_states(swap_states)
        except Exception as recovery_error:  # pragma: no cover - catastrophic
            raise recovery_error from original_error
        raise
    else:
        for state in swap_states:
            shutil.rmtree(state["container"], ignore_errors=True)


def build_parser() -> argparse.ArgumentParser:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Install the course skill foundation")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="report changes only")
    mode.add_argument("--apply", action="store_true", help="apply with backup and rollback")
    mode.add_argument(
        "--verify-source",
        action="store_true",
        help="verify versioned package sources against the manifest",
    )
    mode.add_argument(
        "--verify-installed",
        action="store_true",
        help="verify installed trees against manifest hashes",
    )
    mode.add_argument(
        "--recover-operation",
        type=Path,
        help="roll a PREPARED/EXECUTING operation back before retrying apply",
    )
    parser.add_argument("--packages-root", type=Path, default=project_root / "skill-packages")
    parser.add_argument("--skills-root", type=Path)
    parser.add_argument(
        "--package",
        action="append",
        dest="package_names",
        help="install only this manifest package; repeat to select more",
    )
    parser.add_argument(
        "--allow-update",
        action="append",
        default=[],
        help="explicitly allow replacement of this changed installed package",
    )
    parser.add_argument(
        "--operations-root",
        type=Path,
        default=None,
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.recover_operation is not None:
            recover_install(args.recover_operation)
            print(f"RECOVERED {args.recover_operation}")
            return 0
        if args.verify_source:
            verified = verify_source_packages(
                args.packages_root,
                args.package_names,
            )
            for name, package_hash in verified.items():
                print(f"SOURCE_VERIFIED {name}: {package_hash}")
            return 0
        skills_root = args.skills_root
        if skills_root is None:
            configured_skills = os.environ.get("SKILLS_ROOT")
            if not configured_skills:
                raise InstallError("SKILLS_ROOT or --skills-root is required")
            skills_root = Path(configured_skills)
        if args.verify_installed:
            verified = verify_installed_packages(
                args.packages_root,
                skills_root,
                args.package_names,
            )
            for name, package_hash in verified.items():
                print(f"VERIFIED {name}: {package_hash}")
            return 0
        operations_root = args.operations_root
        if operations_root is None:
            configured_state = os.environ.get("COURSE_DESIGN_STATE_ROOT")
            if args.apply and not configured_state:
                raise InstallError(
                    "COURSE_DESIGN_STATE_ROOT or --operations-root is required for apply"
                )
            operations_root = (
                Path(configured_state) / "operations" / "course-skill-foundation"
                if configured_state
                else None
            )
        result = install(
            args.packages_root,
            skills_root,
            operations_root,
            apply=args.apply,
            package_names=args.package_names,
            allow_updates=args.allow_update,
        )
    except (InstallError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    for action in result.actions:
        print(f"{action.action} {action.name}: {action.target}")
    if result.operation_dir is not None:
        print(f"operation: {result.operation_dir}")
    else:
        print("dry-run: no files changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
