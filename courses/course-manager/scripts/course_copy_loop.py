#!/usr/bin/env python3
"""建立文案專用隔離run；後續沿用course_loop.py，不自動啟動模型。"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.course_copy_profile import copy_spec, copy_course_spec
from src.course_improvement_loop import LoopError, require
from src.course_loop_runtime import prepare


def main():
    p = argparse.ArgumentParser(description=__doc__)
    scope = p.add_mutually_exclusive_group(required=True)
    scope.add_argument("--source", type=Path)
    scope.add_argument("--course-manifest", type=Path, help="已列齊授權章節及呼叫總額的JSON清單")
    p.add_argument("--unit")
    p.add_argument("--title")
    p.add_argument("--purpose")
    p.add_argument("--run", type=Path, required=True)
    p.add_argument("--material", type=Path, action="append", default=[])
    p.add_argument("--keep", action="append", default=[], help="額外必須逐字保留的文字，可重複指定")
    a = p.parse_args()
    try:
        if a.course_manifest:
            require(not any((a.unit, a.title, a.purpose, a.material, a.keep)), "整課參數請寫入清單，不混用單章參數")
            spec = copy_course_spec(a.course_manifest)
        else:
            require(all((a.unit, a.title, a.purpose)), "單章須指定unit、title及purpose")
            spec = copy_spec(a.source, a.unit, a.title, a.purpose, a.material, a.keep)
        result = prepare(spec, a.run)
    except (LoopError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
