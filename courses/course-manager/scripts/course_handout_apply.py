#!/usr/bin/env python3
"""講義套用：從H3確認候選與明確區段映射建立隔離HTML預覽。"""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.course_handout_apply import (build_preview, build_confirmed_preview,
                                      preflight_candidate, record_checks)
from src.course_improvement_loop import LoopError


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--state", type=Path)
    p.add_argument("--confirmation", type=Path, help="追加候選的獨立H3確認；保留舊state不改")
    p.add_argument("--mapping", type=Path)
    p.add_argument("--preflight", action="store_true", help="H3前唯讀檢查候選與原HTML的基本相容性")
    p.add_argument("--source", type=Path, help="--preflight使用的原HTML")
    p.add_argument("--candidate", type=Path, help="--preflight使用的Markdown候選")
    p.add_argument("--checks", type=Path, help="登記本預覽的實際檢查JSON；不重新產製")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    try:
        if args.preflight:
            if args.state or args.confirmation or args.mapping or args.checks or not args.source or not args.candidate:
                p.error("預檢須指定source與candidate，且不可混用state、confirmation、mapping或checks")
            result = preflight_candidate(args.source, args.candidate, args.output)
            print(json.dumps({k: result.get(k) for k in ("status", "report", "findings", "preview_created", "h3_confirmed")},
                             ensure_ascii=False, indent=2))
            return 1 if result["status"] == "blocked" else 0
        if args.source or args.candidate:
            p.error("source與candidate只用於--preflight")
        if args.checks:
            if args.state or args.confirmation or args.mapping:
                p.error("登記檢查時不帶state或mapping")
            result = record_checks(args.output, args.checks)
        else:
            if bool(args.state) == bool(args.confirmation) or not args.mapping:
                p.error("產製預覽須指定state或confirmation其中一項，以及mapping")
            result = (build_confirmed_preview(args.confirmation, args.mapping, args.output)
                      if args.confirmation else build_preview(args.state, args.mapping, args.output))
        print(json.dumps({k: result[k] for k in ("status", "preview", "protected_pre_count")}, ensure_ascii=False, indent=2))
    except (LoopError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
