#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.course_contract import (  # noqa: E402
    ContractStateError,
    approve_gate,
    block_gate,
    load_contract,
    new_contract,
    record_change,
    render_gate_summary,
    save_contract_atomic,
    submit_gate,
    validate_contract,
)


def _contract_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", required=True, type=Path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the course design contract")
    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init", help="create a new course contract")
    init_parser.add_argument("--root", required=True, type=Path)
    init_parser.add_argument("--slug", required=True)
    init_parser.add_argument("--title", required=True)
    init_parser.add_argument("--created-by", required=True)
    init_parser.add_argument("--at", required=True)

    validate_parser = commands.add_parser("validate", help="validate a contract")
    _contract_argument(validate_parser)

    status_parser = commands.add_parser("status", help="show current gate status")
    _contract_argument(status_parser)

    submit_parser = commands.add_parser("submit", help="submit a gate for review")
    _contract_argument(submit_parser)
    submit_parser.add_argument("--gate", required=True)
    submit_parser.add_argument("--actor", required=True)
    submit_parser.add_argument("--at", required=True)

    approve_parser = commands.add_parser("approve", help="record explicit user approval")
    _contract_argument(approve_parser)
    approve_parser.add_argument("--gate", required=True)
    approve_parser.add_argument("--approved-by", required=True)
    approve_parser.add_argument("--at", required=True)
    approve_parser.add_argument("--note", required=True)

    block_parser = commands.add_parser("block", help="block a gate")
    _contract_argument(block_parser)
    block_parser.add_argument("--gate", required=True)
    block_parser.add_argument("--reason", required=True)
    block_parser.add_argument("--actor", required=True)
    block_parser.add_argument("--at", required=True)

    change_parser = commands.add_parser("change", help="record a course change")
    _contract_argument(change_parser)
    change_parser.add_argument("--gate", required=True)
    change_parser.add_argument("--reason", required=True)
    change_parser.add_argument("--actor", required=True)
    change_parser.add_argument("--at", required=True)
    change_parser.add_argument("--semantic", action="store_true")

    return parser


def _print_issues(contract) -> int:
    issues = validate_contract(contract)
    for issue in issues:
        print(f"{issue.code} {issue.path}: {issue.message}")
    return 1 if issues else 0


def _load_mutate_validate_save(path: Path, operation) -> None:
    contract = load_contract(path)
    operation(contract)
    issues = validate_contract(contract)
    if issues:
        joined = "; ".join(f"{issue.path}: {issue.message}" for issue in issues)
        raise ContractStateError(f"mutation produced an invalid contract: {joined}")
    save_contract_atomic(path, contract)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            contract = new_contract(args.slug, args.title, args.created_by, args.at)
            path = args.root / "_design" / args.slug / "course-contract.json"
            if path.exists():
                raise ContractStateError(f"contract already exists: {path}")
            save_contract_atomic(path, contract)
            print(path)
            return 0

        if args.command == "validate":
            return _print_issues(load_contract(args.contract))

        if args.command == "status":
            contract = load_contract(args.contract)
            if _print_issues(contract):
                return 1
            print(render_gate_summary(contract))
            return 0

        if args.command == "submit":
            _load_mutate_validate_save(
                args.contract,
                lambda contract: submit_gate(
                    contract, args.gate, args.actor, args.at
                ),
            )
        elif args.command == "approve":
            _load_mutate_validate_save(
                args.contract,
                lambda contract: approve_gate(
                    contract,
                    args.gate,
                    args.approved_by,
                    args.at,
                    args.note,
                ),
            )
        elif args.command == "block":
            _load_mutate_validate_save(
                args.contract,
                lambda contract: block_gate(
                    contract, args.gate, args.reason, args.actor, args.at
                ),
            )
        elif args.command == "change":
            _load_mutate_validate_save(
                args.contract,
                lambda contract: record_change(
                    contract,
                    args.gate,
                    args.reason,
                    args.actor,
                    args.at,
                    args.semantic,
                ),
            )
        print(args.contract)
        return 0
    except (ContractStateError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
