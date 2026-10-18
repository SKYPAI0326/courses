#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PACKAGE_NAMES = ("course-run", "course-researcher", "course-pm")


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
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _copy_verified(source: Path, destination: Path, expected_hash: str) -> None:
    shutil.copytree(source, destination, symlinks=True)
    actual_hash = tree_hash(destination)
    if actual_hash != expected_hash:
        raise InstallError(
            f"copy verification failed for {source}: expected {expected_hash}, got {actual_hash}"
        )


def _new_operation_dir(operations_root: Path) -> Path:
    operations_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    return Path(tempfile.mkdtemp(prefix=f"{stamp}-", dir=operations_root))


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

containers = []
try:
    for record in records:
        target = Path(record["target"])
        container = Path(tempfile.mkdtemp(
            prefix=f".course-skill-rollback-{record['name']}-", dir=target.parent
        ))
        installed = container / "installed"
        os.replace(target, installed)
        if record["before_exists"]:
            restored = container / "restored"
            copy_verified(operation_dir / record["backup"], restored, record["before_hash"])
            os.replace(restored, target)
        containers.append((container, installed, record))
except Exception:
    for container, installed, record in reversed(containers):
        target = Path(record["target"])
        if target.exists():
            shutil.rmtree(target)
        if installed.exists():
            os.replace(installed, target)
        shutil.rmtree(container, ignore_errors=True)
    raise
else:
    for container, _installed, _record in containers:
        shutil.rmtree(container)

manifest["status"] = "ROLLED_BACK"
manifest["rolled_back_at"] = datetime.now(timezone.utc).isoformat()
write_manifest(manifest_path, manifest)
print(f"rolled back: {operation_dir}")
"""


def _remove_verified_directory(path: Path, expected_hash: str) -> None:
    if tree_hash(path) != expected_hash:
        raise InstallError(f"refusing to remove changed installed skill: {path}")
    shutil.rmtree(path)


def install(
    packages_root: Path,
    skills_root: Path,
    operations_root: Path,
    apply: bool,
) -> InstallResult:
    packages_root = Path(packages_root).resolve()
    skills_root = Path(skills_root).resolve()
    operations_root = Path(operations_root).resolve()
    actions: list[InstallAction] = []

    for name in PACKAGE_NAMES:
        source = packages_root / name
        if not source.is_dir():
            raise InstallError(f"missing validated package: {source}")
        target = skills_root / name
        before_hash = tree_hash(target) if target.is_dir() else None
        after_hash = tree_hash(source)
        actions.append(
            InstallAction(
                name=name,
                action="UPDATE" if before_hash is not None else "ADD",
                source=source,
                target=target,
                before_hash=before_hash,
                after_hash=after_hash,
            )
        )

    if not apply:
        return InstallResult(False, None, tuple(actions))

    skills_root.mkdir(parents=True, exist_ok=True)
    operation_dir = _new_operation_dir(operations_root)
    backups_dir = operation_dir / "backups"
    backups_dir.mkdir()
    package_records: list[dict[str, Any]] = []

    try:
        for action in actions:
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
                }
            )

        manifest = {
            "schema_version": 1,
            "status": "PREPARED",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "installer_path": str(Path(__file__).resolve()),
            "packages": package_records,
        }
        _write_json_atomic(operation_dir / "manifest.json", manifest)
        (operation_dir / "rollback.py").write_text(
            _rollback_script(), encoding="utf-8"
        )

        swap_containers: list[tuple[Path, Path | None, InstallAction]] = []
        try:
            for action in actions:
                container = Path(
                    tempfile.mkdtemp(
                        prefix=f".course-skill-{action.name}-", dir=skills_root
                    )
                )
                staged = container / "staged"
                _copy_verified(action.source, staged, action.after_hash)
                previous: Path | None = None
                if action.target.exists():
                    previous = container / "previous"
                    os.replace(action.target, previous)
                os.replace(staged, action.target)
                if tree_hash(action.target) != action.after_hash:
                    raise InstallError(f"installed hash mismatch: {action.target}")
                swap_containers.append((container, previous, action))
        except Exception:
            for container, previous, action in reversed(swap_containers):
                if action.target.exists():
                    _remove_verified_directory(action.target, action.after_hash)
                if previous is not None and previous.exists():
                    os.replace(previous, action.target)
                shutil.rmtree(container, ignore_errors=True)
            raise
        else:
            for container, _previous, _action in swap_containers:
                shutil.rmtree(container)

        manifest["status"] = "APPLIED"
        manifest["applied_at"] = datetime.now(timezone.utc).isoformat()
        _write_json_atomic(operation_dir / "manifest.json", manifest)
        return InstallResult(True, operation_dir, tuple(actions))
    except Exception:
        if (operation_dir / "manifest.json").exists():
            manifest = json.loads(
                (operation_dir / "manifest.json").read_text(encoding="utf-8")
            )
            manifest["status"] = "FAILED"
            _write_json_atomic(operation_dir / "manifest.json", manifest)
        raise


def rollback_install(operation_dir: Path) -> None:
    operation_dir = Path(operation_dir).resolve()
    manifest_path = operation_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
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

    swap_containers: list[tuple[Path, Path | None, dict[str, Any]]] = []
    try:
        for record in records:
            target = Path(record["target"])
            container = Path(
                tempfile.mkdtemp(
                    prefix=f".course-skill-rollback-{record['name']}-",
                    dir=target.parent,
                )
            )
            previous = container / "installed"
            os.replace(target, previous)
            if record["before_exists"]:
                staged = container / "restored"
                backup = operation_dir / record["backup"]
                _copy_verified(backup, staged, record["before_hash"])
                os.replace(staged, target)
            swap_containers.append((container, previous, record))
    except Exception:
        for container, previous, record in reversed(swap_containers):
            target = Path(record["target"])
            if target.exists():
                shutil.rmtree(target)
            if previous is not None and previous.exists():
                os.replace(previous, target)
            shutil.rmtree(container, ignore_errors=True)
        raise
    else:
        for container, _previous, _record in swap_containers:
            shutil.rmtree(container)

    manifest["status"] = "ROLLED_BACK"
    manifest["rolled_back_at"] = datetime.now(timezone.utc).isoformat()
    _write_json_atomic(manifest_path, manifest)


def build_parser() -> argparse.ArgumentParser:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Install the course skill foundation")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="report changes only")
    mode.add_argument("--apply", action="store_true", help="apply with backup and rollback")
    parser.add_argument("--packages-root", type=Path, default=project_root / "skill-packages")
    parser.add_argument("--skills-root", type=Path, default=Path.home() / ".agents" / "skills")
    parser.add_argument(
        "--operations-root",
        type=Path,
        default=project_root / "operations" / "course-skill-foundation",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = install(
            args.packages_root,
            args.skills_root,
            args.operations_root,
            apply=args.apply,
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
