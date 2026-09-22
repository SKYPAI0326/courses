#!/usr/bin/env python3
"""Run deterministic validation over generated AI review logs."""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


TOOLS_ROOT = Path(__file__).resolve().parent
VALIDATOR_PATH = TOOLS_ROOT / "validate-ai-review-output.py"


def load_validator():
    if not VALIDATOR_PATH.is_file():
        raise AssertionError(f"missing validator: {VALIDATOR_PATH}")
    spec = importlib.util.spec_from_file_location("ai_review_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot import AI review validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("stage1", "stage2"), required=True)
    args = parser.parse_args()
    validator = load_validator()
    root = TOOLS_ROOT.parent / "_validation" / "ai-simulated" / args.stage
    if not root.is_dir():
        raise AssertionError(f"missing review output directory: {root}")
    paths = sorted(root.glob("CH*.json"))
    if not paths:
        raise AssertionError(f"no {args.stage} JSON logs found in {root}")
    errors: list[str] = []
    for path in paths:
        errors.extend(f"{path.name}: {error}" for error in validator.validate_log(path, args.stage))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"{args.stage} output checks passed: {len(paths)} logs")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"AI review output check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
