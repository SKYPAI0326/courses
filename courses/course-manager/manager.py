#!/usr/bin/env python3
"""Course Manager command-line entry point."""

from __future__ import annotations

import argparse
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
    del namespace
    print("command handler is not implemented yet", flush=True)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
