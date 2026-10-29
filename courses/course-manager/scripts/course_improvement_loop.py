#!/usr/bin/env python3
"""管理課程改善紀錄與對話AI階段收送；不直接呼叫模型或操作教材。"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.course_improvement_loop import LoopError, checkpoint, initialize, read_json, report, require
from src.course_loop_stages import confirm_h3, create_stage, next_task, receive, recheck_comparison, stage_status, supplement_evidence
from src.course_loop_review import run_checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    checks = sub.add_parser("run-checks")
    checks.add_argument("--state", type=Path, required=True)
    checks.add_argument("--expected-revision", type=int, required=True)
    checks.add_argument("--evidence-map", type=Path)
    recheck = sub.add_parser("recheck-comparison")
    recheck.add_argument("--state", type=Path, required=True)
    recheck.add_argument("--evidence", type=Path, required=True)
    recheck.add_argument("--expected-revision", type=int, required=True)
    supplement = sub.add_parser("supplement-evidence")
    supplement.add_argument("--state", type=Path, required=True)
    supplement.add_argument("--evidence", type=Path, required=True)
    supplement.add_argument("--expected-revision", type=int, required=True)
    h3 = sub.add_parser("confirm-h3")
    h3.add_argument("--state", type=Path, required=True)
    h3.add_argument("--feedback", type=Path, required=True)
    h3.add_argument("--candidate-sha256", required=True)
    h3.add_argument("--expected-revision", type=int, required=True)
    h3.add_argument("--actor", required=True)
    for name in ("stage-init", "next", "accept"):
        p = sub.add_parser(name)
        p.add_argument("--state", type=Path, required=True)
        if name == "stage-init":
            p.add_argument("--config", type=Path, required=True)
        if name == "accept":
            p.add_argument("--response", type=Path, required=True)
            p.add_argument("--role")
            p.add_argument("--model")
            p.add_argument("--context-id")
    for name in ("init", "status", "resume", "checkpoint"):
        p = sub.add_parser(name)
        p.add_argument("--state", type=Path, required=True)
        if name == "init":
            p.add_argument("--manifest", type=Path, required=True)
        if name == "checkpoint":
            p.add_argument("--unit", type=Path, required=True)
            p.add_argument("--expected-revision", type=int, required=True)
            p.add_argument("--actor", required=True)
            p.add_argument("--note", required=True)
    args = parser.parse_args()
    try:
        if args.command == "run-checks":
            result = run_checks(args.state, args.expected_revision, read_json(args.evidence_map) if args.evidence_map else None)
        elif args.command == "recheck-comparison":
            result = recheck_comparison(args.state, args.evidence, args.expected_revision)
        elif args.command == "supplement-evidence":
            result = supplement_evidence(args.state, read_json(args.evidence), args.expected_revision)
        elif args.command == "confirm-h3":
            result = confirm_h3(args.state, args.feedback, args.candidate_sha256, args.expected_revision, args.actor)
        elif args.command == "stage-init":
            config = read_json(args.config)
            require("review_policy" in config, "新試驗須指定review_policy；舊試驗請resume，不重新初始化")
            result = create_stage(config, args.state)
        elif args.command == "next":
            result = next_task(args.state)
        elif args.command == "accept":
            execution = {"role": args.role, "model": args.model, "context_id": args.context_id} if any((args.role, args.model, args.context_id)) else None
            result = receive(args.state, read_json(args.response), execution)
        elif args.command == "init":
            result = initialize(read_json(args.manifest), args.state)
        elif args.command == "checkpoint":
            result = checkpoint(args.state, read_json(args.unit), args.expected_revision, args.actor, args.note)
        else:
            result = stage_status(args.state) if read_json(args.state).get("schema_version") in ("stages-1", "stages-2") else report(args.state)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (LoopError, OSError, KeyError, TypeError) as exc:
        print(f"控制程式拒絕執行：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
