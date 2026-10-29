#!/usr/bin/env python3
"""課程改善統一入口：prepare/start/work/status/report及人工與補證接續。"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.course_improvement_loop import LoopError, read_json
from src.course_loop_executor import doctor
from src.course_loop_runtime import (activate, finish, human_confirmation, prepare, report,
                                     recover, retry, status, supply_check, work)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("doctor")
    for name in ("prepare", "start", "work", "status", "report", "retry", "recover", "confirm-h3", "supply-check", "finish"):
        p = subs.add_parser(name)
        p.add_argument("--run", type=Path, required=True)
        if name == "prepare":
            p.add_argument("--spec", type=Path, required=True)
        if name in ("start", "confirm-h3", "finish"):
            p.add_argument("--actor", required=True)
        if name == "start":
            p.add_argument("--note", required=True)
        if name == "work":
            p.add_argument("--max-tasks", type=int, default=1)
        if name in ("retry", "recover", "confirm-h3", "supply-check"):
            p.add_argument("--unit", required=True)
        if name == "retry":
            p.add_argument("--reason", required=True)
        if name == "confirm-h3":
            p.add_argument("--feedback", type=Path, required=True)
        if name in ("confirm-h3", "supply-check"):
            p.add_argument("--candidate-sha256", required=True, help="supply-check可填目前原稿版本的雜湊")
        if name in ("confirm-h3", "finish"):
            p.add_argument("--expected-revision", type=int, required=True)
        if name == "supply-check":
            p.add_argument("--check", required=True)
            p.add_argument("--result", choices=["pass", "fail", "pending"], required=True)
        if name in ("supply-check", "finish"):
            p.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "doctor":
            result = doctor()
        elif args.command == "prepare":
            result = prepare(read_json(args.spec), args.run)
        elif args.command == "start":
            result = activate(args.run, args.actor, args.note)
        elif args.command == "work":
            result = work(args.run, args.max_tasks)
        elif args.command == "status":
            result = status(args.run)
        elif args.command == "report":
            result = report(args.run)
        elif args.command == "retry":
            result = retry(args.run, args.unit, args.reason)
        elif args.command == "recover":
            result = recover(args.run, args.unit)
        elif args.command == "confirm-h3":
            result = human_confirmation(args.run, args.unit, args.feedback, args.candidate_sha256, args.expected_revision, args.actor)
        elif args.command == "supply-check":
            result = supply_check(args.run, args.unit, args.check, args.result, args.evidence, args.candidate_sha256)
        else:
            result = finish(args.run, args.evidence, args.expected_revision, args.actor)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if result.get("last_error") else 0
    except (LoopError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"課程loop停止：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
