#!/usr/bin/env python3
"""Build the focused #06/#12 local-UI repair ZIP from the current Lite Pack."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


N8N_DIR = Path(__file__).resolve().parents[1]
ASSETS = N8N_DIR / "assets"
SOURCE_ZIP = ASSETS / "n8n-lite-pack.zip"
PACKAGE = ASSETS / "n8n-lite-pack-ui-fix"
MERGER_SOURCE = N8N_DIR / "_tools" / "lite-pack-ui-fix" / "merge-workflow.cjs"
OUTPUT_ZIP = ASSETS / "n8n-lite-pack-ui-fix.zip"

WORKFLOWS = {
    "n8n-lite-pack/workflows/06-webhook-gemini-file.json": {
        "filename": "06-webhook-gemini-file.json",
        "workflow_id": "lite-pack-06-webhook-gemini-file",
        "node_id": "code-html-ui-06",
        "node_name": "Code: 組 HTML (ai-ui)",
        "local_path": "/webhook/ai-ui",
    },
    "n8n-lite-pack/workflows/12-knowledge-rag.json": {
        "filename": "12-knowledge-rag.json",
        "workflow_id": "lite-pack-12-knowledge-rag",
        "node_id": "code-html-ui",
        "node_name": "Code: 組 HTML (kb-ui)",
        "local_path": "/webhook/kb-ui",
    },
}


def validate_workflow(raw: bytes, spec: dict[str, str]) -> None:
    workflow = json.loads(raw)
    if workflow.get("id") != spec["workflow_id"]:
        raise SystemExit(f"Unexpected workflow ID for {spec['filename']}")
    matches = [node for node in workflow.get("nodes", []) if node.get("id") == spec["node_id"]]
    if len(matches) != 1:
        raise SystemExit(f"Expected exactly one target UI node in {spec['filename']}")
    node = matches[0]
    if node.get("name") != spec["node_name"] or node.get("type") != "n8n-nodes-base.code":
        raise SystemExit(f"Target UI node identity changed in {spec['filename']}")
    code = node.get("parameters", {}).get("jsCode", "")
    if not isinstance(code, str) or not code.strip() or spec["local_path"] not in code:
        raise SystemExit(f"Target UI code is missing or lacks {spec['local_path']}")


def zip_info(name: str, executable: bool = False) -> ZipInfo:
    info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = ZIP_DEFLATED
    info.external_attr = (stat.S_IFREG | (0o755 if executable else 0o644)) << 16
    return info


def main() -> None:
    if not SOURCE_ZIP.is_file():
        raise SystemExit(f"Missing source Lite Pack ZIP: {SOURCE_ZIP}")
    if not MERGER_SOURCE.is_file():
        raise SystemExit(f"Missing merger source: {MERGER_SOURCE}")
    shutil.copy2(MERGER_SOURCE, PACKAGE / "merge-workflow.cjs")
    workflow_dir = PACKAGE / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)

    with ZipFile(SOURCE_ZIP) as source:
        names = set(source.namelist())
        for member, spec in WORKFLOWS.items():
            if member not in names:
                raise SystemExit(f"Missing source workflow: {member}")
            raw = source.read(member)
            validate_workflow(raw, spec)
            (workflow_dir / spec["filename"]).write_bytes(raw)

    package_files = [
        PACKAGE / "README.md",
        PACKAGE / "apply-fix.command",
        PACKAGE / "apply-fix.bat",
        PACKAGE / "apply-fix.ps1",
        PACKAGE / "merge-workflow.cjs",
        workflow_dir / "06-webhook-gemini-file.json",
        workflow_dir / "12-knowledge-rag.json",
    ]
    missing = [str(file) for file in package_files if not file.is_file()]
    if missing:
        raise SystemExit("Missing package source file(s): " + ", ".join(missing))

    fd, temp_name = tempfile.mkstemp(prefix="n8n-lite-pack-ui-fix-", suffix=".zip", dir=ASSETS)
    os.close(fd)
    temp_path = Path(temp_name)
    try:
        with ZipFile(temp_path, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for directory in ("n8n-lite-pack-ui-fix/", "n8n-lite-pack-ui-fix/workflows/"):
                info = ZipInfo(directory, date_time=(2026, 1, 1, 0, 0, 0))
                info.external_attr = (stat.S_IFDIR | 0o755) << 16
                archive.writestr(info, b"")
            for file in package_files:
                relative = file.relative_to(PACKAGE).as_posix()
                target = f"n8n-lite-pack-ui-fix/{relative}"
                executable = file.name == "apply-fix.command"
                archive.writestr(zip_info(target, executable), file.read_bytes())
        temp_path.replace(OUTPUT_ZIP)
    finally:
        temp_path.unlink(missing_ok=True)

    digest = hashlib.sha256(OUTPUT_ZIP.read_bytes()).hexdigest()
    print(f"Built {OUTPUT_ZIP}")
    print(f"Size: {OUTPUT_ZIP.stat().st_size} bytes")
    print(f"SHA-256: {digest}")


if __name__ == "__main__":
    main()
