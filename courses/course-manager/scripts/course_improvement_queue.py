#!/usr/bin/env python3
"""整課佇列入口；派工作票而非執行AI。"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.course_improvement_loop import LoopError, read_json
from src.course_improvement_queue import confirm_integration, dispatch, initialize_queue, queue_status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "status", "resume", "dispatch", "confirm-integration"):
        p = sub.add_parser(name)
        p.add_argument("--state", type=Path, required=True)
        if name == "init":
            p.add_argument("--manifest", type=Path, required=True)
        if name == "confirm-integration":
            p.add_argument("--evidence", type=Path, required=True)
            p.add_argument("--expected-revision", type=int, required=True)
            p.add_argument("--actor", required=True)
    args = parser.parse_args()
    try:
        if args.command == "init":
            result = initialize_queue(read_json(args.manifest), args.state)
        elif args.command == "dispatch":
            result = dispatch(args.state)
        elif args.command == "confirm-integration":
            result = confirm_integration(args.state, args.evidence, args.expected_revision, args.actor)
        else:
            result = queue_status(args.state)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (LoopError, OSError, KeyError, TypeError, ValueError) as exc:
        print(f"佇列拒絕執行：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
