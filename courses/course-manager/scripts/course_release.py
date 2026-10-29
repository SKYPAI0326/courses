#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.course_release import (  # noqa: E402
    apply_release_proposal,
    build_release_proposal,
    recover_release_proposal,
    save_release_proposal,
    scan_course_freshness,
    validate_release_record,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and apply governed course releases")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--record", type=Path, required=True)

    propose_parser = subparsers.add_parser("propose")
    propose_parser.add_argument("--root", type=Path, required=True)
    propose_parser.add_argument("--record", type=Path, required=True)
    propose_parser.add_argument("--output", type=Path, required=True)

    apply_parser = subparsers.add_parser("apply")
    apply_parser.add_argument("--proposal", type=Path, required=True)
    apply_parser.add_argument("--contract", type=Path, required=True)

    recover_parser = subparsers.add_parser("recover")
    recover_parser.add_argument("--proposal", type=Path, required=True)
    recover_parser.add_argument("--contract", type=Path, required=True)

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("--root", type=Path, required=True)
    scan_parser.add_argument("--as-of", required=True)

    args = parser.parse_args()
    if args.command == "validate":
        record = json.loads(args.record.read_text(encoding="utf-8"))
        issues = validate_release_record(record)
        print(json.dumps([issue.__dict__ for issue in issues], ensure_ascii=False, indent=2))
        return 1 if issues else 0
    if args.command == "propose":
        record = json.loads(args.record.read_text(encoding="utf-8"))
        proposal = build_release_proposal(args.root, record)
        save_release_proposal(args.output, proposal)
        return 0
    if args.command == "apply":
        apply_release_proposal(args.proposal, args.contract)
        return 0
    if args.command == "recover":
        recover_release_proposal(args.proposal, args.contract)
        return 0
    report = scan_course_freshness(args.root, args.as_of)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
