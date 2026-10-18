#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.course_orchestrator import (  # noqa: E402
    OrchestrationError,
    complete_gate,
    resume_course,
)
from src.runtime import (  # noqa: E402
    RuntimeConfigurationError,
    doctor,
    resolve_runtime_paths,
    source_root_from_module,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Resume or complete one governed course Gate transaction"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="read-only runtime readiness report")

    for name in ("resume", "complete"):
        command = commands.add_parser(name)
        command.add_argument("--contract", type=Path, required=True)
        command.add_argument("--actor", required=True)
        command.add_argument("--at", required=True)
        command.add_argument("--expected-revision", type=int)
        if name == "complete":
            command.add_argument("--gate", required=True)
            command.add_argument("--evidence-id", action="append", required=True)
    return parser


def _runtime_paths():
    paths = resolve_runtime_paths()
    actual = source_root_from_module()
    if paths.design_system_root != actual:
        raise RuntimeConfigurationError(
            "COURSE_DESIGN_SYSTEM_ROOT does not match the executing runtime"
        )
    return paths


def _contract_within_web_root(contract: Path, web_root: Path) -> Path:
    path = contract.absolute()
    try:
        relative = path.relative_to(web_root)
    except ValueError as error:
        raise RuntimeConfigurationError(
            "course contract must be inside COURSE_WEB_ROOT"
        ) from error
    current = web_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise RuntimeConfigurationError(
                f"course contract path must not contain a symbolic link: {current}"
            )
    return path


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        report = doctor()
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if report["status"] == "READY" else 2
    try:
        paths = _runtime_paths()
        contract = _contract_within_web_root(args.contract, paths.course_web_root)
        if args.command == "resume":
            envelope = resume_course(
                contract,
                paths.course_web_root,
                paths.state_root,
                actor=args.actor,
                at=args.at,
                expected_revision=args.expected_revision,
            )
        else:
            envelope = complete_gate(
                contract,
                paths.course_web_root,
                paths.state_root,
                args.gate,
                args.evidence_id,
                actor=args.actor,
                at=args.at,
                expected_revision=args.expected_revision,
            )
    except (RuntimeConfigurationError, OrchestrationError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
