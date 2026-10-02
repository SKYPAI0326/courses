#!/usr/bin/env python3
"""Course Manager command-line entry point."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence


COMMANDS = (
    "scan",
    "find",
    "inspect",
    "propose-new",
    "propose-move",
    "propose-merge",
    "verify",
    "apply",
    "rollback",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="course-manager",
        description="Scan and manage course project folders with guarded operations.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Workspace root; defaults to the parent of course-manager.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan the workspace.")
    scan.add_argument("--write", action="store_true", help="Write the catalog and report.")

    find = subparsers.add_parser("find", help="Find catalog entries.")
    find.add_argument("query")
    find.add_argument("--kind", default=None)
    find.add_argument("--stale-ok", action="store_true")

    inspect = subparsers.add_parser("inspect", help="Inspect one project folder.")
    inspect.add_argument("path")
    inspect.add_argument("--deep", action="store_true")

    new_course = subparsers.add_parser("propose-new", help="Propose a new course project.")
    new_course.add_argument("topic_or_path")

    move = subparsers.add_parser("propose-move", help="Propose a guarded move.")
    move.add_argument("source")
    move.add_argument("destination")

    merge = subparsers.add_parser("propose-merge", help="Propose a guarded merge.")
    merge.add_argument("source")
    merge.add_argument("target")

    verify = subparsers.add_parser("verify", help="Verify the workspace or a manifest.")
    verify.add_argument("--baseline", default=None)
    verify.add_argument("--write", action="store_true", help="Write a verification report.")

    apply = subparsers.add_parser("apply", help="Apply an approved proposal.")
    apply.add_argument("proposal")
    apply.add_argument("--approval", required=True)

    rollback = subparsers.add_parser("rollback", help="Rollback an approved manifest.")
    rollback.add_argument("manifest")
    rollback.add_argument("--approval", required=True)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    namespace = build_parser().parse_args(argv)
    if namespace.command == "scan":
        return _handle_scan(namespace)
    if namespace.command == "find":
        return _handle_find(namespace)
    if namespace.command == "inspect":
        return _handle_inspect(namespace)
    if namespace.command == "propose-new":
        return _handle_propose_new(namespace)
    if namespace.command == "propose-move":
        return _handle_propose_move(namespace)
    if namespace.command == "propose-merge":
        return _handle_propose_merge(namespace)
    print("command handler is not implemented yet", flush=True)
    return 2


def _workspace_root(namespace: argparse.Namespace) -> Path:
    return (namespace.root or Path(__file__).resolve().parent.parent).absolute()


def _manager_root(root: Path) -> Path:
    return root / "course-manager"


def _scan_report(catalog: dict) -> str:
    counts: dict[str, int] = {}
    for item in catalog["items"]:
        counts[item["kind"]] = counts.get(item["kind"], 0) + 1
    lines = [
        "# Course Manager Scan Report",
        "",
        f"Scanned at: {catalog['scanned_at']}",
        f"Items: {len(catalog['items'])}",
        "",
        "## Counts",
        "",
    ]
    lines.extend(f"- {kind}: {counts[kind]}" for kind in sorted(counts))
    lines.extend(["", "## Needs Review or Blocked", ""])
    flagged = [
        item
        for item in catalog["items"]
        if item["status"] in {"needs-review", "blocked"} or item["risk"]["move"] == "blocked"
    ]
    lines.extend(f"- {item['path']}: {item['kind']} — {item['classification_reason']}" for item in flagged)
    if not flagged:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def _handle_scan(namespace: argparse.Namespace) -> int:
    from src.catalog import write_catalog
    from src.discover import scan_workspace

    root = _workspace_root(namespace)
    catalog = scan_workspace(root)
    counts: dict[str, int] = {}
    for item in catalog["items"]:
        counts[item["kind"]] = counts.get(item["kind"], 0) + 1
    print(json.dumps({"items": len(catalog["items"]), "counts": counts}, ensure_ascii=False, indent=2))
    if namespace.write:
        manager_root = _manager_root(root)
        catalog_path = manager_root / "registry" / "catalog.json"
        write_catalog(catalog_path, catalog)
        report_dir = manager_root / "reports" / "scans"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"scan-{catalog['scanned_at'].replace(':', '').replace('+', '-')}.md"
        report_path.write_text(_scan_report(catalog), encoding="utf-8")
        print(f"WROTE {catalog_path}")
        print(f"WROTE {report_path}")
    else:
        print(json.dumps(catalog, ensure_ascii=False, indent=2))
    return 0


def _handle_find(namespace: argparse.Namespace) -> int:
    from src.catalog import catalog_is_stale, find_items, load_catalog

    root = _workspace_root(namespace)
    catalog_path = _manager_root(root) / "registry" / "catalog.json"
    if not catalog_path.exists():
        print(f"CATALOG_MISSING: {catalog_path}")
        return 2
    catalog = load_catalog(catalog_path)
    stale, reasons = catalog_is_stale(root, catalog)
    if stale:
        print("CATALOG_STALE: " + "; ".join(reasons))
    matches = find_items(catalog, namespace.query, namespace.kind)
    print(json.dumps(matches, ensure_ascii=False, indent=2))
    return 0 if matches else 1


def _handle_inspect(namespace: argparse.Namespace) -> int:
    from src.inspect import inspect_path

    root = _workspace_root(namespace)
    try:
        result = inspect_path(root, namespace.path, deep=namespace.deep)
    except (FileNotFoundError, ValueError) as error:
        print(f"INSPECT_ERROR: {error}")
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def _write_proposal(root: Path, proposal: dict, category: str) -> int:
    from src.proposals import write_proposal

    path = _manager_root(root) / "proposals" / category / f"{proposal['proposal_id']}.json"
    write_proposal(path, proposal)
    print(json.dumps({"status": proposal["status"], "proposal": str(path)}, ensure_ascii=False, indent=2))
    return 0


def _handle_propose_new(namespace: argparse.Namespace) -> int:
    from src.proposals import build_new_course_proposal

    root = _workspace_root(namespace)
    try:
        proposal = build_new_course_proposal(root, namespace.topic_or_path)
    except (FileNotFoundError, ValueError) as error:
        print(f"PROPOSAL_ERROR: {error}")
        return 2
    return _write_proposal(root, proposal, "new-courses")


def _handle_propose_move(namespace: argparse.Namespace) -> int:
    from src.proposals import build_move_proposal

    root = _workspace_root(namespace)
    try:
        proposal = build_move_proposal(root, namespace.source, namespace.destination)
    except (FileNotFoundError, ValueError) as error:
        print(f"PROPOSAL_ERROR: {error}")
        return 2
    return _write_proposal(root, proposal, "moves")


def _handle_propose_merge(namespace: argparse.Namespace) -> int:
    from src.proposals import build_merge_proposal

    root = _workspace_root(namespace)
    try:
        proposal = build_merge_proposal(root, namespace.source, namespace.target)
    except (FileNotFoundError, ValueError) as error:
        print(f"PROPOSAL_ERROR: {error}")
        return 2
    return _write_proposal(root, proposal, "merges")


if __name__ == "__main__":
    raise SystemExit(main())
