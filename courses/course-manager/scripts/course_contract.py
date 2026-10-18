#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.course_contract import (  # noqa: E402
    ContractStateError,
    assert_external_action_authorized,
    begin_gate,
    block_gate,
    fail_gate,
    load_contract,
    migrate_contract_v1,
    migrate_contract_v2,
    new_contract,
    propose_external_action,
    record_change,
    render_gate_summary,
    save_contract_atomic,
    validate_contract,
)
from src.transactions import (  # noqa: E402
    TransactionCommittedDurabilityError,
    TransactionError,
    authorize_external_action_atomic,
    bind_external_approval_authority_atomic,
    mutate_contract_atomic,
    resolve_gate_blocker_atomic,
)


def _contract_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--contract", required=True, type=Path)


def _gate_arguments(parser: argparse.ArgumentParser) -> None:
    _contract_argument(parser)
    parser.add_argument("--gate", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--at", required=True)


def _expected_revision_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--expected-revision", type=int)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the course design contract")
    commands = parser.add_subparsers(dest="command", required=True)

    command = commands.add_parser("init", help="create a v3 contract")
    command.add_argument("--root", required=True, type=Path)
    command.add_argument("--slug", required=True)
    command.add_argument("--title", required=True)
    command.add_argument("--created-by", required=True)
    command.add_argument("--at", required=True)

    command = commands.add_parser(
        "enroll-approval-authority",
        help=(
            "operator governance step: bind one external approval public key "
            "before any Gate work"
        ),
        description=(
            "Enroll the verification-only approval trust root. This is an "
            "explicit operator governance step and is never performed "
            "automatically by a course producer."
        ),
    )
    _contract_argument(command)
    command.add_argument("--authority-id", required=True)
    command.add_argument("--public-key", required=True, type=Path)
    _expected_revision_argument(command)

    for name in ("validate", "status"):
        _contract_argument(commands.add_parser(name))

    command = commands.add_parser("begin")
    _gate_arguments(command)
    _expected_revision_argument(command)

    command = commands.add_parser("fail")
    _gate_arguments(command)
    command.add_argument("--issue", action="append", required=True)
    _expected_revision_argument(command)

    command = commands.add_parser("block")
    _gate_arguments(command)
    command.add_argument("--reason", required=True)
    _expected_revision_argument(command)

    command = commands.add_parser("resolve-blocker")
    _gate_arguments(command)
    command.add_argument("--workspace-root", required=True, type=Path)
    command.add_argument("--blocker-id", required=True)
    command.add_argument("--resolution", required=True)
    command.add_argument("--evidence-id", action="append", required=True)
    _expected_revision_argument(command)

    command = commands.add_parser("change")
    _gate_arguments(command)
    command.add_argument("--reason", required=True)
    command.add_argument("--semantic", action="store_true")
    _expected_revision_argument(command)

    command = commands.add_parser("propose-action")
    _contract_argument(command)
    command.add_argument("--action-id", required=True)
    command.add_argument("--kind", required=True)
    command.add_argument("--manifest-path", required=True)
    command.add_argument("--manifest-sha256", required=True)
    command.add_argument("--actor", required=True)
    command.add_argument("--at", required=True)
    _expected_revision_argument(command)

    command = commands.add_parser("authorize-action")
    _contract_argument(command)
    command.add_argument("--action-id", required=True)
    command.add_argument("--receipt", required=True, type=Path)
    command.add_argument("--at", required=True)
    _expected_revision_argument(command)

    command = commands.add_parser("check-action")
    _contract_argument(command)
    command.add_argument("--action-id", required=True)
    command.add_argument("--manifest-sha256", required=True)

    command = commands.add_parser("migrate")
    _contract_argument(command)
    command.add_argument("--workspace-root", type=Path)
    command.add_argument("--actor", required=True)
    command.add_argument("--at", required=True)
    _expected_revision_argument(command)

    # Old automation receives a deliberate migration error rather than a silent
    # reinterpretation of gate approval as external publishing authorization.
    command = commands.add_parser("approve", help=argparse.SUPPRESS)
    _contract_argument(command)
    return parser


def _print_issues(contract: dict) -> int:
    issues = validate_contract(contract)
    for issue in issues:
        print(f"{issue.code} {issue.path}: {issue.message}")
    return 1 if issues else 0


def _mutate(
    path: Path, operation, *, expected_revision: int | None = None
) -> dict:
    return mutate_contract_atomic(
        path, operation, expected_revision=expected_revision
    )


def _parse_issues(values: list[str]) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    for value in values:
        try:
            item = json.loads(value)
        except json.JSONDecodeError:
            item = {"message": value}
        if not isinstance(item, dict):
            raise ContractStateError("each --issue must be a JSON object or text")
        issues.append(item)
    return issues


def _initialize(args: argparse.Namespace) -> Path:
    contract = new_contract(args.slug, args.title, args.created_by, args.at)
    root = args.root.resolve(strict=False)
    design_root = args.root / "_design"
    course_root = design_root / args.slug
    if design_root.is_symlink() or course_root.is_symlink():
        raise ContractStateError("contract directory must not be a symbolic link")
    path = course_root / "course-contract.json"
    if not path.resolve(strict=False).is_relative_to(root):
        raise ContractStateError(f"contract path escapes requested root: {path}")
    if path.exists():
        raise ContractStateError(f"contract already exists: {path}")
    save_contract_atomic(path, contract)
    return path


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "approve":
            raise ContractStateError(
                "approve is unavailable in contract v3; run migrate, then use the "
                "validated Gate workflow or authorize-action as appropriate"
            )
        if args.command == "init":
            print(_initialize(args))
            return 0
        if args.command == "validate":
            return _print_issues(load_contract(args.contract))
        if args.command == "status":
            contract = load_contract(args.contract)
            if _print_issues(contract):
                return 1
            print(render_gate_summary(contract))
            return 0
        if args.command == "enroll-approval-authority":
            public_key = json.loads(args.public_key.read_text(encoding="utf-8"))
            if not isinstance(public_key, dict):
                raise ContractStateError("approval public key must be a JSON object")
            bind_external_approval_authority_atomic(
                args.contract,
                args.authority_id,
                public_key,
                expected_revision=args.expected_revision,
            )
            print(args.contract)
            return 0
        if args.command == "check-action":
            assert_external_action_authorized(
                load_contract(args.contract), args.action_id, args.manifest_sha256
            )
            print(args.contract)
            return 0
        if args.command == "migrate":
            workspace_root = args.workspace_root or args.contract.parent

            def migrate(contract):
                if contract.get("schema_version") == 1:
                    migrated = migrate_contract_v1(
                        contract,
                        args.actor,
                        args.at,
                        workspace_root=workspace_root,
                    )
                elif contract.get("schema_version") == 2:
                    migrated = migrate_contract_v2(
                        contract, workspace_root, args.actor, args.at
                    )
                else:
                    raise ContractStateError(
                        "migrate requires schema_version 1 or 2"
                    )
                contract.clear()
                contract.update(migrated)

            _mutate(
                args.contract,
                migrate,
                expected_revision=args.expected_revision,
            )
            print(args.contract)
            return 0

        if args.command == "resolve-blocker":
            resolve_gate_blocker_atomic(
                args.contract,
                args.gate,
                args.blocker_id,
                args.resolution,
                args.evidence_id,
                args.actor,
                args.at,
                workspace_root=args.workspace_root,
                expected_revision=args.expected_revision,
            )
            print(args.contract)
            return 0

        if args.command == "authorize-action":
            receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
            authorize_external_action_atomic(
                args.contract,
                args.action_id,
                receipt,
                args.at,
                expected_revision=args.expected_revision,
            )
            print(args.contract)
            return 0

        operations = {
            "begin": lambda contract: begin_gate(contract, args.gate, args.actor, args.at),
            "fail": lambda contract: fail_gate(
                contract, args.gate, _parse_issues(args.issue), args.actor, args.at
            ),
            "block": lambda contract: block_gate(
                contract, args.gate, args.reason, args.actor, args.at
            ),
            "change": lambda contract: record_change(
                contract, args.gate, args.reason, args.actor, args.at, args.semantic
            ),
            "propose-action": lambda contract: propose_external_action(
                contract,
                args.action_id,
                args.kind,
                args.manifest_path,
                args.manifest_sha256,
                args.actor,
                args.at,
            ),
        }
        _mutate(
            args.contract,
            operations[args.command],
            expected_revision=args.expected_revision,
        )
        print(args.contract)
        return 0
    except TransactionCommittedDurabilityError as error:
        print(
            f"error: revision {error.revision} was already committed at {error.path}; "
            "directory durability is uncertain. Do not retry automatically.",
            file=sys.stderr,
        )
        return 3
    except (
        ContractStateError,
        TransactionError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
