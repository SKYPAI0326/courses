#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import stat
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


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def _governed_rollback_script(
    installer_path: Path,
    packages_root: Path,
    skills_root: Path,
    operations_root: Path,
) -> str:
    values = {
        "installer": json.dumps(str(installer_path)),
        "packages": json.dumps(str(packages_root)),
        "skills": json.dumps(str(skills_root)),
        "operations": json.dumps(str(operations_root)),
    }
    return f"""#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

operation_dir = Path(__file__).absolute().parent
command = [
    sys.executable,
    {values['installer']},
    "--rollback-operation",
    str(operation_dir),
    "--packages-root",
    {values['packages']},
    "--skills-root",
    {values['skills']},
    "--operations-root",
    {values['operations']},
]
raise SystemExit(subprocess.call(command))
"""


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


def _authority_path(operations_root: Path, operation_id: str) -> Path:
    return operations_root / ".authority" / f"{operation_id}.json"


def _install_container_path(
    skills_root: Path, operation_id: str, package_name: str
) -> Path:
    return skills_root / f".course-skill-install-{operation_id}-{package_name}"


def _recovery_container_path(
    skills_root: Path, operation_id: str, package_name: str
) -> Path:
    return skills_root / f".course-skill-recover-{operation_id}-{package_name}"


def _fd_matches_path(path: Path, descriptor: int) -> bool:
    try:
        path_state = os.stat(path, follow_symlinks=False)
    except OSError:
        return False
    descriptor_state = os.fstat(descriptor)
    return (
        stat.S_ISDIR(path_state.st_mode)
        and path_state.st_dev == descriptor_state.st_dev
        and path_state.st_ino == descriptor_state.st_ino
    )


def _fd_matches_child(parent_descriptor: int, name: str, descriptor: int) -> bool:
    try:
        path_state = os.stat(name, dir_fd=parent_descriptor, follow_symlinks=False)
    except OSError:
        return False
    descriptor_state = os.fstat(descriptor)
    return (
        stat.S_ISDIR(path_state.st_mode)
        and path_state.st_dev == descriptor_state.st_dev
        and path_state.st_ino == descriptor_state.st_ino
    )


def _open_authority_directory(
    operations_root: Path, *, create: bool
) -> tuple[int, int]:
    """Open the authority directory without following its path components."""

    operations_root = Path(operations_root)
    root_descriptor: int | None = None
    authority_descriptor: int | None = None
    try:
        if create:
            operations_root.mkdir(parents=True, exist_ok=True)
            _safe_root_argument(operations_root, "operations root")
        root_descriptor = os.open(
            operations_root,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
        )
        if not _fd_matches_path(operations_root, root_descriptor):
            raise InstallError("operations root changed while opening authority")
        if create:
            try:
                os.mkdir(".authority", mode=0o700, dir_fd=root_descriptor)
                os.fsync(root_descriptor)
            except FileExistsError:
                pass
        authority_state = os.stat(
            ".authority", dir_fd=root_descriptor, follow_symlinks=False
        )
        if not stat.S_ISDIR(authority_state.st_mode):
            raise InstallError(
                "operation authority path must be a non-symlink directory"
            )
        authority_descriptor = os.open(
            ".authority",
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
            dir_fd=root_descriptor,
        )
        if not _fd_matches_child(
            root_descriptor, ".authority", authority_descriptor
        ):
            raise InstallError("operation authority directory changed while opening")
        return root_descriptor, authority_descriptor
    except InstallError:
        if authority_descriptor is not None:
            os.close(authority_descriptor)
        if root_descriptor is not None:
            os.close(root_descriptor)
        raise
    except OSError as error:
        if authority_descriptor is not None:
            os.close(authority_descriptor)
        if root_descriptor is not None:
            os.close(root_descriptor)
        raise InstallError(
            f"cannot open independent operation authority: {error}"
        ) from error


def _authority_binding_is_current(
    operations_root: Path, root_descriptor: int, authority_descriptor: int
) -> bool:
    return _fd_matches_path(operations_root, root_descriptor) and _fd_matches_child(
        root_descriptor, ".authority", authority_descriptor
    )


def _prepare_authority_directory(operations_root: Path) -> None:
    root_descriptor, authority_descriptor = _open_authority_directory(
        operations_root, create=True
    )
    os.close(authority_descriptor)
    os.close(root_descriptor)


def _read_operation_authority(
    operations_root: Path, operation_id: str
) -> tuple[bytes, os.stat_result]:
    root_descriptor, authority_descriptor = _open_authority_directory(
        operations_root, create=False
    )
    receipt_descriptor: int | None = None
    try:
        receipt_descriptor = os.open(
            f"{operation_id}.json",
            os.O_RDONLY | os.O_NOFOLLOW,
            dir_fd=authority_descriptor,
        )
        receipt_state = os.fstat(receipt_descriptor)
        if not stat.S_ISREG(receipt_state.st_mode):
            raise InstallError("operation authority receipt must be a regular file")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(receipt_descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        if not _authority_binding_is_current(
            operations_root, root_descriptor, authority_descriptor
        ):
            raise InstallError("operation authority directory changed while reading")
        return b"".join(chunks), receipt_state
    except InstallError:
        raise
    except OSError as error:
        raise InstallError(
            "independent operation authority is unavailable: "
            f"{_authority_path(operations_root, operation_id)}: {error}"
        ) from error
    finally:
        if receipt_descriptor is not None:
            os.close(receipt_descriptor)
        os.close(authority_descriptor)
        os.close(root_descriptor)


def _write_operation_authority(
    operation_dir: Path,
    packages_root: Path,
    skills_root: Path,
    operations_root: Path,
    actions: Sequence[InstallAction],
    allowed_updates: set[str],
) -> str:
    authority_path = _authority_path(operations_root, operation_dir.name)
    authority = {
        "schema_version": 1,
        "operation_id": operation_dir.name,
        "operation_dir": str(operation_dir),
        "packages_root": str(packages_root),
        "package_manifest_sha256": _file_sha256(packages_root / "manifest.json"),
        "skills_root": str(skills_root),
        "operations_root": str(operations_root),
        "allowed_updates": sorted(allowed_updates),
        "packages": [
            {
                "name": action.name,
                "action": action.action,
                "target": str(skills_root / action.name),
                "before_exists": action.before_hash is not None,
                "before_hash": action.before_hash,
                "after_hash": action.after_hash,
                "backup": (
                    f"backups/{action.name}"
                    if action.before_hash is not None
                    else None
                ),
                "install_container": str(
                    _install_container_path(
                        skills_root, operation_dir.name, action.name
                    )
                ),
                "recovery_container": str(
                    _recovery_container_path(
                        skills_root, operation_dir.name, action.name
                    )
                ),
            }
            for action in actions
        ],
    }
    serialized = (
        json.dumps(authority, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")
    root_descriptor, authority_descriptor = _open_authority_directory(
        operations_root, create=True
    )
    temporary_name = (
        f".{operation_dir.name}.{secrets.token_hex(12)}.authority.tmp"
    )
    temporary_descriptor: int | None = None
    temporary_exists = False
    try:
        try:
            os.stat(
                f"{operation_dir.name}.json",
                dir_fd=authority_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            pass
        else:
            raise InstallError(f"operation authority already exists: {authority_path}")
        temporary_descriptor = os.open(
            temporary_name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=authority_descriptor,
        )
        temporary_exists = True
        offset = 0
        while offset < len(serialized):
            offset += os.write(temporary_descriptor, serialized[offset:])
        os.fchmod(temporary_descriptor, 0o444)
        os.fsync(temporary_descriptor)
        os.close(temporary_descriptor)
        temporary_descriptor = None
        if not _authority_binding_is_current(
            operations_root, root_descriptor, authority_descriptor
        ):
            raise InstallError("operation authority directory changed before receipt write")
        os.rename(
            temporary_name,
            f"{operation_dir.name}.json",
            src_dir_fd=authority_descriptor,
            dst_dir_fd=authority_descriptor,
        )
        temporary_exists = False
        os.fsync(authority_descriptor)
        if not _authority_binding_is_current(
            operations_root, root_descriptor, authority_descriptor
        ):
            raise InstallError("operation authority directory changed during receipt write")
    except InstallError:
        raise
    except OSError as error:
        raise InstallError(f"cannot write operation authority: {error}") from error
    finally:
        if temporary_descriptor is not None:
            os.close(temporary_descriptor)
        if temporary_exists:
            try:
                os.unlink(temporary_name, dir_fd=authority_descriptor)
            except FileNotFoundError:
                pass
        os.close(authority_descriptor)
        os.close(root_descriptor)
    return hashlib.sha256(serialized).hexdigest()


def _load_recovery_context(
    operation_dir: Path,
    *,
    packages_root: Path,
    skills_root: Path,
    operations_root: Path,
) -> tuple[Path, dict[str, Any], dict[str, dict[str, Any]]]:
    packages_root = _safe_root_argument(packages_root, "packages root")
    skills_root = _safe_root_argument(skills_root, "skills root", allow_absent=True)
    operations_root = _safe_root_argument(operations_root, "operations root")
    _validate_install_root_topology(packages_root, skills_root, operations_root)
    operation_dir = _safe_root_argument(operation_dir, "operation directory")
    if operation_dir.parent != operations_root:
        raise InstallError("operation directory is outside the authorized operations root")

    manifest_path, manifest = _load_operation_manifest(operation_dir)
    operation_id = operation_dir.name
    if manifest.get("operation_id") != operation_id:
        raise InstallError("operation manifest identity does not match its directory")
    authority_path = _authority_path(operations_root, operation_id)
    authority_bytes, authority_state = _read_operation_authority(
        operations_root, operation_id
    )
    if authority_state.st_mode & 0o222:
        raise InstallError(f"independent operation authority is writable: {authority_path}")
    if manifest.get("authority_sha256") != hashlib.sha256(authority_bytes).hexdigest():
        raise InstallError("operation manifest does not match independent authority")
    try:
        authority = json.loads(authority_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise InstallError(f"cannot read operation authority {authority_path}: {error}") from error
    expected_authority_fields = {
        "schema_version": 1,
        "operation_id": operation_id,
        "operation_dir": str(operation_dir),
        "packages_root": str(packages_root),
        "package_manifest_sha256": _file_sha256(packages_root / "manifest.json"),
        "skills_root": str(skills_root),
        "operations_root": str(operations_root),
    }
    for field, expected in expected_authority_fields.items():
        if authority.get(field) != expected:
            raise InstallError(f"operation authority has invalid {field}")
    if authority.get("allowed_updates") != manifest.get("allowed_updates"):
        raise InstallError("operation update authorization differs from authority")

    package_manifest = {
        record["name"]: record for record in _load_manifest_records(packages_root / "manifest.json")
    }
    authority_records = authority.get("packages")
    manifest_records = manifest.get("packages")
    if not isinstance(authority_records, list) or not authority_records:
        raise InstallError("operation authority has no package records")
    if not isinstance(manifest_records, list) or len(manifest_records) != len(
        authority_records
    ):
        raise InstallError("operation package records differ from authority")
    trusted_fields = (
        "name",
        "action",
        "target",
        "before_exists",
        "before_hash",
        "after_hash",
        "backup",
    )
    container_required_phases = {
        "CONTAINER_CREATE_INTENT",
        "STAGING",
        "PREVIOUS_MOVE_INTENT",
        "PREVIOUS_MOVED",
        "TARGET_REPLACE_INTENT",
        "TARGET_REPLACED",
        "VERIFIED",
        "RECOVERY_CREATE_INTENT",
        "RECOVERY_INTENT",
        "TARGET_QUARANTINE_INTENT",
        "TARGET_QUARANTINED",
        "RESTORE_INTENT",
        "RESTORED_STAGED",
        "TARGET_RESTORE_INTENT",
        "TARGET_RESTORED",
        "CLEANUP_INTENT",
        "RECOVERY_CONTAINER_CLEANED",
        "INSTALL_CONTAINER_CLEANUP_INTENT",
    }
    recovery_required_phases = {
        "RECOVERY_CREATE_INTENT",
        "RECOVERY_INTENT",
        "TARGET_QUARANTINE_INTENT",
        "TARGET_QUARANTINED",
        "RESTORE_INTENT",
        "RESTORED_STAGED",
        "TARGET_RESTORE_INTENT",
        "TARGET_RESTORED",
        "CLEANUP_INTENT",
        "ROLLBACK_CONTAINER_CREATE_INTENT",
        "ROLLBACK_CONTAINER_READY",
        "ROLLBACK_TARGET_MOVE_INTENT",
        "ROLLBACK_TARGET_MOVED",
        "ROLLBACK_RESTORE_STAGE_INTENT",
        "ROLLBACK_RESTORED_STAGED",
        "ROLLBACK_TARGET_RESTORE_INTENT",
        "ROLLBACK_TARGET_RESTORED",
        "ROLLBACK_CLEANUP_INTENT",
        "ROLLBACK_ABORT_CONTAINER_CREATE_INTENT",
        "ROLLBACK_ABORT_CONTAINER_READY",
        "ROLLBACK_ABORT_STAGE_AFTER_INTENT",
        "ROLLBACK_ABORT_AFTER_STAGED",
        "ROLLBACK_ABORT_BEFORE_MOVE_INTENT",
        "ROLLBACK_ABORT_BEFORE_MOVED",
        "ROLLBACK_ABORT_TARGET_RESTORE_INTENT",
        "ROLLBACK_ABORT_TARGET_RESTORED",
        "ROLLBACK_ABORT_CLEANUP_INTENT",
    }
    trusted: dict[str, dict[str, Any]] = {}
    for authority_record, manifest_record in zip(authority_records, manifest_records):
        if not isinstance(authority_record, dict) or not isinstance(manifest_record, dict):
            raise InstallError("operation package record must be an object")
        name = authority_record.get("name")
        if not isinstance(name, str) or name in trusted or name not in package_manifest:
            raise InstallError("operation authority package set is invalid")
        if authority_record.get("target") != str(skills_root / name):
            raise InstallError(f"operation authority target is invalid: {name}")
        if authority_record.get("after_hash") != package_manifest[name]["baseline_hash"]:
            raise InstallError(f"operation authority baseline is invalid: {name}")
        if authority_record.get("action") not in {"ADD", "UPDATE"}:
            raise InstallError(f"operation authority action is invalid: {name}")
        before_exists = authority_record.get("before_exists")
        before_hash = authority_record.get("before_hash")
        expected_backup = f"backups/{name}" if before_exists is True else None
        if authority_record.get("backup") != expected_backup:
            raise InstallError(f"operation authority backup is invalid: {name}")
        if before_exists is True:
            if not isinstance(before_hash, str) or not SHA256_PATTERN.fullmatch(before_hash):
                raise InstallError(f"operation authority before hash is invalid: {name}")
        elif before_exists is not False or before_hash is not None:
            raise InstallError(f"operation authority before state is invalid: {name}")
        expected_install_container = str(
            _install_container_path(skills_root, operation_id, name)
        )
        expected_recovery_container = str(
            _recovery_container_path(skills_root, operation_id, name)
        )
        if authority_record.get("install_container") != expected_install_container:
            raise InstallError(f"operation authority install container is invalid: {name}")
        if authority_record.get("recovery_container") != expected_recovery_container:
            raise InstallError(f"operation authority recovery container is invalid: {name}")
        if any(
            manifest_record.get(field) != authority_record.get(field)
            for field in trusted_fields
        ):
            raise InstallError(f"operation manifest record differs from authority: {name}")
        phase = manifest_record.get("phase")
        if not isinstance(phase, str):
            raise InstallError(f"operation recovery phase is invalid: {name}")
        for field, expected in (
            ("container", expected_install_container),
            ("recovery_container", expected_recovery_container),
        ):
            value = manifest_record.get(field)
            if value is None:
                continue
            if value != expected:
                raise InstallError(
                    f"operation {field} differs from authority: {name}"
                )
        if (
            phase in container_required_phases
            and manifest_record.get("container") != expected_install_container
        ):
            raise InstallError(f"operation container identity is missing: {name}")
        if (
            phase in recovery_required_phases
            and manifest_record.get("recovery_container")
            != expected_recovery_container
        ):
            raise InstallError(f"operation recovery identity is missing: {name}")
        if (
            phase
            in {
                "RECOVERY_CONTAINER_CLEANED",
                "INSTALL_CONTAINER_CLEANUP_INTENT",
                "RECOVERED",
                "ROLLBACK_CONTAINER_CLEANED",
                "ROLLED_BACK",
            }
            and manifest_record.get("recovery_container") is not None
        ):
            raise InstallError(f"cleaned recovery container remains recorded: {name}")
        if phase == "RECOVERED" and manifest_record.get("container") is not None:
            raise InstallError(f"cleaned install container remains recorded: {name}")
        trusted[name] = authority_record
    return manifest_path, manifest, trusted


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
    authority: dict[str, Any],
) -> None:
    name = authority["name"]
    before_exists = authority["before_exists"]
    before_hash = authority["before_hash"]
    after_hash = authority["after_hash"]
    target = Path(authority["target"])
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
        backup = operation_dir / authority["backup"]
        if backup.parent != operation_dir / "backups":
            raise InstallError(f"backup path escapes operation directory: {name}")
        if _verified_tree_hash(backup, f"backup {name}") != before_hash:
            raise InstallError(f"verified backup differs from before hash: {name}")

    recovery_value = record.get("recovery_container")
    recovery = (
        Path(authority["recovery_container"])
        if isinstance(recovery_value, str)
        else None
    )
    if recovery is None and not (
        (before_exists and current_hash == before_hash)
        or (not before_exists and current_hash is None)
    ):
        recovery = Path(authority["recovery_container"])
        record["recovery_container"] = str(recovery)
        record["phase"] = "RECOVERY_CREATE_INTENT"
        _write_json_atomic(manifest_path, manifest)
        recovery.mkdir()
        _fsync_directory(target.parent)
        record["phase"] = "RECOVERY_INTENT"
        _write_json_atomic(manifest_path, manifest)

    phase = record.get("phase")
    if recovery is not None and phase == "RECOVERY_CREATE_INTENT":
        if recovery.exists():
            if not recovery.is_dir() or any(recovery.iterdir()):
                raise InstallError(f"recovery container create state is invalid: {name}")
        else:
            recovery.mkdir()
            _fsync_directory(target.parent)
        record["phase"] = "RECOVERY_INTENT"
        _write_json_atomic(manifest_path, manifest)

    target_is_before = (before_exists and current_hash == before_hash) or (
        not before_exists and current_hash is None
    )
    phase = record.get("phase")
    if recovery is not None and phase == "CLEANUP_INTENT" and target_is_before:
        if recovery.exists():
            shutil.rmtree(recovery)
            _fsync_directory(recovery.parent)
        record["recovery_container"] = None
        record["phase"] = "RECOVERY_CONTAINER_CLEANED"
        _write_json_atomic(manifest_path, manifest)
        recovery = None

    quarantined = recovery / "quarantined" if recovery is not None else None
    restored = recovery / "restored" if recovery is not None else None
    quarantine_hash: str | None = None
    if quarantined is not None and (quarantined.exists() or quarantined.is_symlink()):
        quarantine_hash = _verified_tree_hash(quarantined, f"quarantine {name}")
        if quarantine_hash != after_hash:
            raise InstallError(f"recovery quarantine differs from installed hash: {name}")
    restored_hash: str | None = None
    if restored is not None and (restored.exists() or restored.is_symlink()):
        restored_hash = _verified_tree_hash(restored, f"restored staging {name}")
        if restored_hash != before_hash:
            raise InstallError(f"recovery staging differs from before hash: {name}")

    phase = record.get("phase")
    if (
        phase in {
            "TARGET_QUARANTINED",
            "RESTORE_INTENT",
            "RESTORED_STAGED",
            "TARGET_RESTORE_INTENT",
        }
        and not target_is_before
        and quarantine_hash is None
    ):
        raise InstallError(f"recovery quarantine is missing: {name}")

    if recovery is not None and current_hash == after_hash and quarantine_hash is None:
        record["phase"] = "TARGET_QUARANTINE_INTENT"
        _write_json_atomic(manifest_path, manifest)
        _durable_replace(target, quarantined)
        current_hash = None
        quarantine_hash = after_hash
        record["phase"] = "TARGET_QUARANTINED"
        _write_json_atomic(manifest_path, manifest)

    if before_exists and current_hash != before_hash:
        assert backup is not None and before_hash is not None
        if restored_hash is None:
            _copy_verified(backup, restored, before_hash)
            record["phase"] = "RESTORE_INTENT"
            _write_json_atomic(manifest_path, manifest)
            restored_hash = before_hash
        record["phase"] = "TARGET_RESTORE_INTENT"
        _write_json_atomic(manifest_path, manifest)
        if not target.exists() and restored is not None and restored.exists():
            _durable_replace(restored, target)
        current_hash = _verified_tree_hash(target, f"restored target {name}")
        if current_hash != before_hash:
            raise InstallError(f"restored target differs from before hash: {name}")
        record["phase"] = "TARGET_RESTORED"
        _write_json_atomic(manifest_path, manifest)

    target_is_before = (before_exists and current_hash == before_hash) or (
        not before_exists and current_hash is None
    )
    if not target_is_before:
        raise InstallError(f"recovery did not restore the authorized before state: {name}")

    if recovery is not None and recovery.exists():
        record["phase"] = "CLEANUP_INTENT"
        _write_json_atomic(manifest_path, manifest)
        shutil.rmtree(recovery)
        _fsync_directory(recovery.parent)
        record["recovery_container"] = None
        record["phase"] = "RECOVERY_CONTAINER_CLEANED"
        _write_json_atomic(manifest_path, manifest)

    container_value = record.get("container")
    if isinstance(container_value, str):
        container = Path(authority["install_container"])
        if container.exists():
            record["phase"] = "INSTALL_CONTAINER_CLEANUP_INTENT"
            _write_json_atomic(manifest_path, manifest)
            shutil.rmtree(container)
            _fsync_directory(container.parent)
        record["container"] = None
    record["phase"] = "RECOVERED"
    _write_json_atomic(manifest_path, manifest)


def recover_install(
    operation_dir: Path,
    *,
    packages_root: Path,
    skills_root: Path,
    operations_root: Path,
    final_status: str = "RECOVERED",
) -> None:
    """Roll an interrupted PREPARED/EXECUTING install back to its before state."""

    if final_status not in {"RECOVERED", "FAILED"}:
        raise ValueError("recovery final status must be RECOVERED or FAILED")
    operation_dir = _safe_root_argument(operation_dir, "operation directory")
    manifest_path, manifest, authority = _load_recovery_context(
        operation_dir,
        packages_root=packages_root,
        skills_root=skills_root,
        operations_root=operations_root,
    )
    status = manifest.get("status")
    if status in {"RECOVERED", "FAILED"}:
        if any(record.get("phase") != "RECOVERED" for record in manifest["packages"]):
            raise InstallError("completed recovery contains unfinished package state")
        for record in manifest["packages"]:
            trusted = authority[record["name"]]
            target = Path(trusted["target"])
            if trusted["before_exists"]:
                if _verified_tree_hash(target, f"recovered target {record['name']}") != trusted["before_hash"]:
                    raise InstallError("completed recovery target differs from authority")
            elif target.exists() or target.is_symlink():
                raise InstallError("completed recovery unexpectedly retains added target")
        return
    if status not in {"PREPARED", "EXECUTING"}:
        raise InstallError(
            f"recovery requires PREPARED or EXECUTING manifest, got {status!r}"
        )
    for record in reversed(manifest["packages"]):
        if not isinstance(record, dict):
            raise InstallError("operation package record must be an object")
        _recover_package_record(
            operation_dir,
            manifest_path,
            manifest,
            record,
            authority[record["name"]],
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
        status = manifest.get("status")
        if status in {"PREPARED", "EXECUTING"}:
            raise InstallError(
                "unfinished install must be recovered before a new apply: "
                f"{manifest_path.parent}"
            )
        if status in {"ROLLING_BACK", "ROLLBACK_ABORTING"}:
            raise InstallError(
                "unfinished rollback must be resumed before a new apply: "
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
    _prepare_authority_directory(operations_root)
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

        authority_sha256 = _write_operation_authority(
            operation_dir,
            packages_root,
            skills_root,
            operations_root,
            mutable_actions,
            allowed_updates,
        )
        manifest = {
            "schema_version": 2,
            "operation_id": operation_dir.name,
            "authority_sha256": authority_sha256,
            "status": "PREPARED",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "installer_path": str(Path(__file__).resolve()),
            "allowed_updates": sorted(allowed_updates),
            "packages": package_records,
        }
        manifest_path = operation_dir / "manifest.json"
        _write_json_atomic(manifest_path, manifest)
        _write_text_durable(
            operation_dir / "rollback.py",
            _governed_rollback_script(
                Path(__file__).resolve(),
                packages_root,
                skills_root,
                operations_root,
            ),
            executable=True,
        )

        package_record_by_name = {
            record["name"]: record for record in package_records
        }
        for action in mutable_actions:
            record = package_record_by_name[action.name]
            container = _install_container_path(
                skills_root, operation_dir.name, action.name
            )
            record["container"] = str(container)
            record["phase"] = "CONTAINER_CREATE_INTENT"
            _write_json_atomic(manifest_path, manifest)
            try:
                container.mkdir()
            except OSError as error:
                raise InstallError(
                    f"cannot create authorized install container {container}: {error}"
                ) from error
            _fsync_directory(skills_root)
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
                authority_container = _install_container_path(
                    skills_root, operation_dir.name, record["name"]
                )
                if Path(container_value) != authority_container:
                    raise InstallError(
                        f"install container differs from authority: {record['name']}"
                    )
                shutil.rmtree(authority_container, ignore_errors=True)
                record["container"] = None
        _write_json_atomic(manifest_path, manifest)
        return InstallResult(True, operation_dir, tuple(actions))
    except Exception as original_error:
        recovery_error: Exception | None = None
        manifest_path = operation_dir / "manifest.json"
        if manifest_path.exists():
            try:
                interrupted = json.loads(manifest_path.read_text(encoding="utf-8"))
                if interrupted.get("status") in {"PREPARED", "EXECUTING"}:
                    recover_install(
                        operation_dir,
                        packages_root=packages_root,
                        skills_root=skills_root,
                        operations_root=operations_root,
                        final_status="FAILED",
                    )
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


ROLLBACK_RECORD_PHASES = frozenset(
    {
        "APPLIED",
        "ROLLBACK_CONTAINER_CREATE_INTENT",
        "ROLLBACK_CONTAINER_READY",
        "ROLLBACK_TARGET_MOVE_INTENT",
        "ROLLBACK_TARGET_MOVED",
        "ROLLBACK_RESTORE_STAGE_INTENT",
        "ROLLBACK_RESTORED_STAGED",
        "ROLLBACK_TARGET_RESTORE_INTENT",
        "ROLLBACK_TARGET_RESTORED",
        "ROLLBACK_CLEANUP_INTENT",
        "ROLLBACK_CONTAINER_CLEANED",
        "ROLLED_BACK",
    }
)


def _rollback_tree_hash_if_present(path: Path, label: str) -> str | None:
    if not path.exists() and not path.is_symlink():
        return None
    return _verified_tree_hash(path, label)


def _rollback_record_state(
    operation_dir: Path,
    record: dict[str, Any],
    authority: dict[str, Any],
) -> dict[str, Any]:
    name = authority["name"]
    phase = record.get("phase")
    if phase not in ROLLBACK_RECORD_PHASES:
        raise InstallError(f"rollback phase is invalid: {name}: {phase!r}")

    before_exists = authority["before_exists"]
    before_hash = authority["before_hash"]
    after_hash = authority["after_hash"]
    target = Path(authority["target"])
    recovery = Path(authority["recovery_container"])
    recovery_value = record.get("recovery_container")
    if phase == "APPLIED":
        if recovery_value is not None:
            raise InstallError(f"applied rollback container must be absent: {name}")
    elif phase in {"ROLLBACK_CONTAINER_CLEANED", "ROLLED_BACK"}:
        if recovery_value is not None:
            raise InstallError(f"cleaned rollback container remains recorded: {name}")
    elif recovery_value != str(recovery):
        raise InstallError(f"rollback container identity is missing: {name}")

    target_hash = _rollback_tree_hash_if_present(target, f"rollback target {name}")
    if target_hash not in {None, before_hash, after_hash}:
        raise InstallError(f"rollback target has unauthorized content: {name}")

    container_exists = recovery.exists() or recovery.is_symlink()
    installed_hash: str | None = None
    restored_hash: str | None = None
    if container_exists:
        if recovery.is_symlink() or not recovery.is_dir():
            raise InstallError(f"rollback container must be a non-symlink directory: {name}")
        children = {child.name for child in recovery.iterdir()}
        if not children.issubset({"installed", "restored"}):
            raise InstallError(f"rollback container has unauthorized content: {name}")
        installed_hash = _rollback_tree_hash_if_present(
            recovery / "installed", f"rollback installed quarantine {name}"
        )
        restored_hash = _rollback_tree_hash_if_present(
            recovery / "restored", f"rollback restored staging {name}"
        )
        if installed_hash not in {None, after_hash}:
            raise InstallError(f"rollback installed quarantine differs from authority: {name}")
        if restored_hash not in {None, before_hash}:
            raise InstallError(f"rollback restored staging differs from authority: {name}")

    if before_exists:
        backup = operation_dir / authority["backup"]
        if backup.parent != operation_dir / "backups":
            raise InstallError(f"backup path escapes operation directory: {name}")
        if _verified_tree_hash(backup, f"rollback backup {name}") != before_hash:
            raise InstallError(f"verified backup differs from before hash: {name}")

    state = {
        "name": name,
        "phase": phase,
        "before_exists": before_exists,
        "before_hash": before_hash,
        "after_hash": after_hash,
        "target": target,
        "target_hash": target_hash,
        "recovery": recovery,
        "container_exists": container_exists,
        "installed_hash": installed_hash,
        "restored_hash": restored_hash,
    }
    target_is_before = (before_exists and target_hash == before_hash) or (
        not before_exists and target_hash is None
    )

    valid = False
    if phase == "APPLIED":
        valid = target_hash == after_hash and not container_exists
    elif phase == "ROLLBACK_CONTAINER_CREATE_INTENT":
        valid = (
            target_hash == after_hash
            and (not container_exists or (installed_hash is None and restored_hash is None))
        )
    elif phase == "ROLLBACK_CONTAINER_READY":
        valid = (
            target_hash == after_hash
            and container_exists
            and installed_hash is None
            and restored_hash is None
        )
    elif phase == "ROLLBACK_TARGET_MOVE_INTENT":
        valid = container_exists and restored_hash is None and (
            (target_hash == after_hash and installed_hash is None)
            or (target_hash is None and installed_hash == after_hash)
        )
    elif phase == "ROLLBACK_TARGET_MOVED":
        valid = (
            container_exists
            and target_hash is None
            and installed_hash == after_hash
            and restored_hash is None
        )
    elif phase == "ROLLBACK_RESTORE_STAGE_INTENT":
        valid = (
            before_exists
            and container_exists
            and target_hash is None
            and installed_hash == after_hash
            and restored_hash in {None, before_hash}
        )
    elif phase == "ROLLBACK_RESTORED_STAGED":
        valid = (
            before_exists
            and container_exists
            and target_hash is None
            and installed_hash == after_hash
            and restored_hash == before_hash
        )
    elif phase == "ROLLBACK_TARGET_RESTORE_INTENT":
        valid = before_exists and container_exists and installed_hash == after_hash and (
            (target_hash is None and restored_hash == before_hash)
            or (target_hash == before_hash and restored_hash is None)
        )
    elif phase == "ROLLBACK_TARGET_RESTORED":
        valid = (
            target_is_before
            and container_exists
            and installed_hash == after_hash
            and restored_hash is None
        )
    elif phase == "ROLLBACK_CLEANUP_INTENT":
        valid = target_is_before and (
            not container_exists
            or (installed_hash == after_hash and restored_hash is None)
        )
    elif phase in {"ROLLBACK_CONTAINER_CLEANED", "ROLLED_BACK"}:
        valid = target_is_before and not container_exists

    if not valid:
        raise InstallError(f"rollback intermediate state is inconsistent: {name}: {phase}")
    return state


def _write_rollback_record_phase(
    manifest_path: Path,
    manifest: dict[str, Any],
    record: dict[str, Any],
    phase: str,
) -> None:
    record["phase"] = phase
    _write_json_atomic(manifest_path, manifest)


def _rollback_package_record(
    operation_dir: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    record: dict[str, Any],
    authority: dict[str, Any],
) -> None:
    state = _rollback_record_state(operation_dir, record, authority)
    phase = state["phase"]
    target: Path = state["target"]
    recovery: Path = state["recovery"]
    name = state["name"]

    if phase == "APPLIED":
        record["recovery_container"] = str(recovery)
        _write_rollback_record_phase(
            manifest_path, manifest, record, "ROLLBACK_CONTAINER_CREATE_INTENT"
        )
        phase = "ROLLBACK_CONTAINER_CREATE_INTENT"

    if phase == "ROLLBACK_CONTAINER_CREATE_INTENT":
        if not recovery.exists():
            try:
                recovery.mkdir()
            except OSError as error:
                raise InstallError(
                    f"cannot create authorized rollback container {recovery}: {error}"
                ) from error
            _fsync_directory(recovery.parent)
        _write_rollback_record_phase(
            manifest_path, manifest, record, "ROLLBACK_CONTAINER_READY"
        )
        phase = "ROLLBACK_CONTAINER_READY"

    if phase == "ROLLBACK_CONTAINER_READY":
        _write_rollback_record_phase(
            manifest_path, manifest, record, "ROLLBACK_TARGET_MOVE_INTENT"
        )
        phase = "ROLLBACK_TARGET_MOVE_INTENT"

    if phase == "ROLLBACK_TARGET_MOVE_INTENT":
        state = _rollback_record_state(operation_dir, record, authority)
        installed = recovery / "installed"
        if state["target_hash"] == state["after_hash"]:
            _durable_replace(target, installed)
        _write_rollback_record_phase(
            manifest_path, manifest, record, "ROLLBACK_TARGET_MOVED"
        )
        phase = "ROLLBACK_TARGET_MOVED"

    if phase == "ROLLBACK_TARGET_MOVED":
        if state["before_exists"]:
            _write_rollback_record_phase(
                manifest_path, manifest, record, "ROLLBACK_RESTORE_STAGE_INTENT"
            )
            phase = "ROLLBACK_RESTORE_STAGE_INTENT"
        else:
            _write_rollback_record_phase(
                manifest_path, manifest, record, "ROLLBACK_TARGET_RESTORED"
            )
            phase = "ROLLBACK_TARGET_RESTORED"

    if phase == "ROLLBACK_RESTORE_STAGE_INTENT":
        state = _rollback_record_state(operation_dir, record, authority)
        if state["restored_hash"] is None:
            _copy_verified(
                operation_dir / authority["backup"],
                recovery / "restored",
                authority["before_hash"],
            )
        _write_rollback_record_phase(
            manifest_path, manifest, record, "ROLLBACK_RESTORED_STAGED"
        )
        phase = "ROLLBACK_RESTORED_STAGED"

    if phase == "ROLLBACK_RESTORED_STAGED":
        _write_rollback_record_phase(
            manifest_path, manifest, record, "ROLLBACK_TARGET_RESTORE_INTENT"
        )
        phase = "ROLLBACK_TARGET_RESTORE_INTENT"

    if phase == "ROLLBACK_TARGET_RESTORE_INTENT":
        state = _rollback_record_state(operation_dir, record, authority)
        restored = recovery / "restored"
        if state["target_hash"] is None:
            _durable_replace(restored, target)
        _write_rollback_record_phase(
            manifest_path, manifest, record, "ROLLBACK_TARGET_RESTORED"
        )
        phase = "ROLLBACK_TARGET_RESTORED"

    if phase == "ROLLBACK_TARGET_RESTORED":
        _rollback_record_state(operation_dir, record, authority)
        _write_rollback_record_phase(
            manifest_path, manifest, record, "ROLLBACK_CLEANUP_INTENT"
        )
        phase = "ROLLBACK_CLEANUP_INTENT"

    if phase == "ROLLBACK_CLEANUP_INTENT":
        state = _rollback_record_state(operation_dir, record, authority)
        if state["container_exists"]:
            shutil.rmtree(recovery)
            _fsync_directory(recovery.parent)
        record["recovery_container"] = None
        _write_rollback_record_phase(
            manifest_path, manifest, record, "ROLLBACK_CONTAINER_CLEANED"
        )
        phase = "ROLLBACK_CONTAINER_CLEANED"

    if phase == "ROLLBACK_CONTAINER_CLEANED":
        _rollback_record_state(operation_dir, record, authority)
        _write_rollback_record_phase(manifest_path, manifest, record, "ROLLED_BACK")

    _rollback_record_state(operation_dir, record, authority)


def _rollback_abort_state(
    record: dict[str, Any], authority: dict[str, Any]
) -> dict[str, Any]:
    name = authority["name"]
    target = Path(authority["target"])
    recovery = Path(authority["recovery_container"])
    target_hash = _rollback_tree_hash_if_present(target, f"rollback abort target {name}")
    if target_hash not in {
        None,
        authority["before_hash"],
        authority["after_hash"],
    }:
        raise InstallError(f"rollback abort target has unauthorized content: {name}")
    container_exists = recovery.exists() or recovery.is_symlink()
    hashes: dict[str, str | None] = {
        "installed": None,
        "restored": None,
        "aborted_before": None,
    }
    if container_exists:
        if recovery.is_symlink() or not recovery.is_dir():
            raise InstallError(f"rollback abort container is unsafe: {name}")
        children = {child.name for child in recovery.iterdir()}
        if not children.issubset(hashes):
            raise InstallError(f"rollback abort container has unauthorized content: {name}")
        for child in hashes:
            hashes[child] = _rollback_tree_hash_if_present(
                recovery / child, f"rollback abort {child} {name}"
            )
        if hashes["installed"] not in {None, authority["after_hash"]}:
            raise InstallError(f"rollback abort installed tree differs from authority: {name}")
        for child in ("restored", "aborted_before"):
            if hashes[child] not in {None, authority["before_hash"]}:
                raise InstallError(f"rollback abort before tree differs from authority: {name}")
    return {
        "name": name,
        "target": target,
        "target_hash": target_hash,
        "recovery": recovery,
        "container_exists": container_exists,
        **hashes,
    }


def _abort_rollback_to_applied(
    manifest_path: Path,
    manifest: dict[str, Any],
    authority: dict[str, dict[str, Any]],
    packages_root: Path,
) -> None:
    for record in manifest["packages"]:
        trusted = authority[record["name"]]
        source = packages_root / trusted["name"]
        _validate_package_tree(source, trusted["name"])
        if tree_hash(source) != trusted["after_hash"]:
            raise InstallError(
                f"rollback abort source differs from authority: {trusted['name']}"
            )
        _rollback_abort_state(record, trusted)

    manifest["status"] = "ROLLBACK_ABORTING"
    manifest["rollback_phase"] = "ROLLBACK_ABORTING"
    _write_json_atomic(manifest_path, manifest)

    for record in reversed(manifest["packages"]):
        trusted = authority[record["name"]]
        state = _rollback_abort_state(record, trusted)
        target: Path = state["target"]
        recovery: Path = state["recovery"]
        if state["target_hash"] != trusted["after_hash"]:
            if not state["container_exists"]:
                record["recovery_container"] = str(recovery)
                _write_rollback_record_phase(
                    manifest_path,
                    manifest,
                    record,
                    "ROLLBACK_ABORT_CONTAINER_CREATE_INTENT",
                )
                recovery.mkdir()
                _fsync_directory(recovery.parent)
                _write_rollback_record_phase(
                    manifest_path,
                    manifest,
                    record,
                    "ROLLBACK_ABORT_CONTAINER_READY",
                )
            elif record.get("recovery_container") is None:
                record["recovery_container"] = str(recovery)
                _write_rollback_record_phase(
                    manifest_path,
                    manifest,
                    record,
                    "ROLLBACK_ABORT_CONTAINER_READY",
                )
            state = _rollback_abort_state(record, trusted)
            installed = recovery / "installed"
            if state["installed"] is None:
                _write_rollback_record_phase(
                    manifest_path,
                    manifest,
                    record,
                    "ROLLBACK_ABORT_STAGE_AFTER_INTENT",
                )
                _copy_verified(
                    packages_root / trusted["name"],
                    installed,
                    trusted["after_hash"],
                )
                _write_rollback_record_phase(
                    manifest_path,
                    manifest,
                    record,
                    "ROLLBACK_ABORT_AFTER_STAGED",
                )
            state = _rollback_abort_state(record, trusted)
            if (
                trusted["before_exists"]
                and state["target_hash"] == trusted["before_hash"]
            ):
                _write_rollback_record_phase(
                    manifest_path,
                    manifest,
                    record,
                    "ROLLBACK_ABORT_BEFORE_MOVE_INTENT",
                )
                _durable_replace(target, recovery / "aborted_before")
                _write_rollback_record_phase(
                    manifest_path,
                    manifest,
                    record,
                    "ROLLBACK_ABORT_BEFORE_MOVED",
                )
            _write_rollback_record_phase(
                manifest_path,
                manifest,
                record,
                "ROLLBACK_ABORT_TARGET_RESTORE_INTENT",
            )
            _durable_replace(installed, target)
            _write_rollback_record_phase(
                manifest_path,
                manifest,
                record,
                "ROLLBACK_ABORT_TARGET_RESTORED",
            )

        if _rollback_tree_hash_if_present(
            target, f"rollback abort restored target {trusted['name']}"
        ) != trusted["after_hash"]:
            raise InstallError(
                f"rollback abort did not restore installed state: {trusted['name']}"
            )
        if recovery.exists():
            _write_rollback_record_phase(
                manifest_path,
                manifest,
                record,
                "ROLLBACK_ABORT_CLEANUP_INTENT",
            )
            shutil.rmtree(recovery)
            _fsync_directory(recovery.parent)
        record["recovery_container"] = None
        _write_rollback_record_phase(manifest_path, manifest, record, "APPLIED")

    manifest["status"] = "APPLIED"
    manifest.pop("rollback_phase", None)
    manifest.pop("rolled_back_at", None)
    _write_json_atomic(manifest_path, manifest)


def rollback_install(
    operation_dir: Path,
    *,
    packages_root: Path,
    skills_root: Path,
    operations_root: Path,
) -> None:
    operation_dir = _safe_root_argument(
        Path(operation_dir), "operation directory"
    )
    manifest_path, manifest, authority = _load_recovery_context(
        operation_dir,
        packages_root=packages_root,
        skills_root=skills_root,
        operations_root=operations_root,
    )
    if manifest.get("status") in {"PREPARED", "EXECUTING"}:
        recover_install(
            operation_dir,
            packages_root=packages_root,
            skills_root=skills_root,
            operations_root=operations_root,
        )
        return
    if manifest.get("status") == "ROLLED_BACK":
        if manifest.get("rollback_phase") != "ROLLED_BACK":
            raise InstallError("rolled-back operation has incomplete final journal state")
        for record in manifest["packages"]:
            state = _rollback_record_state(
                operation_dir, record, authority[record["name"]]
            )
            if state["phase"] != "ROLLED_BACK":
                raise InstallError(
                    f"completed rollback has unfinished package state: {record['name']}"
                )
        return
    if manifest.get("status") == "ROLLBACK_ABORTING":
        _abort_rollback_to_applied(
            manifest_path, manifest, authority, Path(packages_root)
        )
        return
    if manifest.get("status") not in {"APPLIED", "ROLLING_BACK"}:
        raise InstallError(
            "rollback requires APPLIED or ROLLING_BACK manifest, "
            f"got {manifest.get('status')!r}"
        )

    records = manifest.get("packages", [])
    for record in records:
        _rollback_record_state(
            operation_dir, record, authority[record["name"]]
        )

    if manifest["status"] == "APPLIED":
        manifest["status"] = "ROLLING_BACK"
        manifest["rollback_phase"] = "ROLLBACK_EXECUTING"
        _write_json_atomic(manifest_path, manifest)
    elif manifest.get("rollback_phase") not in {
        "ROLLBACK_EXECUTING",
        "ROLLBACK_COMPLETE_INTENT",
    }:
        raise InstallError("rolling-back operation has invalid final journal state")

    try:
        for record in records:
            _rollback_package_record(
                operation_dir,
                manifest_path,
                manifest,
                record,
                authority[record["name"]],
            )

        for record in records:
            state = _rollback_record_state(
                operation_dir, record, authority[record["name"]]
            )
            if state["phase"] != "ROLLED_BACK":
                raise InstallError(f"rollback package is incomplete: {record['name']}")
        manifest["rollback_phase"] = "ROLLBACK_COMPLETE_INTENT"
        _write_json_atomic(manifest_path, manifest)
        manifest["status"] = "ROLLED_BACK"
        manifest["rollback_phase"] = "ROLLED_BACK"
        manifest["rolled_back_at"] = datetime.now(timezone.utc).isoformat()
        _write_json_atomic(manifest_path, manifest)
    except Exception as original_error:
        try:
            _abort_rollback_to_applied(
                manifest_path, manifest, authority, Path(packages_root)
            )
        except Exception as recovery_error:  # pragma: no cover - catastrophic
            raise recovery_error from original_error
        raise


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
    mode.add_argument(
        "--rollback-operation",
        type=Path,
        help="roll an APPLIED operation back using independent root authority",
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
        configured_state = os.environ.get("COURSE_DESIGN_STATE_ROOT")
        operations_root = args.operations_root
        if operations_root is None and configured_state:
            operations_root = (
                Path(configured_state) / "operations" / "course-skill-foundation"
            )
        if args.recover_operation is not None or args.rollback_operation is not None:
            if operations_root is None:
                raise InstallError(
                    "COURSE_DESIGN_STATE_ROOT or --operations-root is required "
                    "for recovery/rollback"
                )
            operation = args.recover_operation or args.rollback_operation
            if args.recover_operation is not None:
                recover_install(
                    operation,
                    packages_root=args.packages_root,
                    skills_root=skills_root,
                    operations_root=operations_root,
                )
                print(f"RECOVERED {operation}")
            else:
                rollback_install(
                    operation,
                    packages_root=args.packages_root,
                    skills_root=skills_root,
                    operations_root=operations_root,
                )
                print(f"ROLLED_BACK {operation}")
            return 0
        if args.verify_installed:
            verified = verify_installed_packages(
                args.packages_root,
                skills_root,
                args.package_names,
            )
            for name, package_hash in verified.items():
                print(f"VERIFIED {name}: {package_hash}")
            return 0
        if operations_root is None:
            if args.apply and not configured_state:
                raise InstallError(
                    "COURSE_DESIGN_STATE_ROOT or --operations-root is required for apply"
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
