#!/usr/bin/env python3
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
            handle.write("\n")
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
