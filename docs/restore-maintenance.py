#!/usr/bin/env python3
"""Restore archived files by manifest; dry-run unless --apply is supplied."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def restore(root, manifest_path, apply=False):
    root = Path(root).resolve()
    data = json.loads(Path(manifest_path).read_text())
    archive = (root / data["archive_root_relative_to_repo"]).resolve()
    pending = []
    # Validate the entire batch before copying anything.
    for entry in data["archived"]:
        target = root / entry["path"]
        source = archive / entry["archive_path"]
        if not target.resolve().is_relative_to(root) or not source.resolve().is_relative_to(archive):
            raise ValueError("Path escapes expected root")
        if not source.is_file() or digest(source) != entry["sha256"]:
            raise ValueError(f"Archive missing or changed: {source}")
        if target.exists() or target.is_symlink():
            if target.is_symlink() or not target.is_file() or digest(target) != entry["sha256"]:
                raise ValueError(f"Refuse to overwrite different content: {target}")
        else:
            pending.append((source, target, entry["sha256"]))
    if apply:
        for source, target, expected in pending:
            target.parent.mkdir(parents=True, exist_ok=True)
            # Exclusive creation protects changes made after preflight, too.
            with target.open("xb") as output, source.open("rb") as input_file:
                shutil.copyfileobj(input_file, output)
            shutil.copystat(source, target)
            if digest(target) != expected:
                raise ValueError(f"Restored checksum mismatch: {target}")
    return len(pending)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    count = restore(Path(__file__).resolve().parent.parent, args.manifest, args.apply)
    print(f"{'Restored' if args.apply else 'Dry run; would restore'} {count} files")
