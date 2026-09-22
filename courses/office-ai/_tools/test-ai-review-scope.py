#!/usr/bin/env python3
"""Checks deterministic adversarial-scope selection."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


TOOLS = Path(__file__).resolve().parent
SCOPE_PATH = TOOLS / "select-ai-review-scope.py"


def load_scope():
    if not SCOPE_PATH.is_file():
        raise AssertionError(f"missing scope selector: {SCOPE_PATH}")
    spec = importlib.util.spec_from_file_location("ai_review_scope", SCOPE_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot import scope selector")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture(unit_id: str, confidence: str = "high", issue: bool = False) -> dict:
    return {
        "unit_id": unit_id,
        "stage": "stage1",
        "actor": "independent-ai",
        "simulated_not_human": True,
        "prompt_revision": "simulated-learner-v1",
        "completion": {"verdict": "FAIL" if issue else "PASS", "confidence": confidence},
        "entry": {"verdict": "PASS", "confidence": confidence},
        "understanding": {"verdict": "PASS", "confidence": confidence},
        "transfer": {"verdict": "PASS", "confidence": confidence},
        "issues": [{"severity": "MAJOR"}] if issue else [],
    }


def main() -> int:
    selector = load_scope()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        (root / "CH1-1.json").write_text(json.dumps(fixture("CH1-1")), encoding="utf-8")
        (root / "CH1-2.json").write_text(json.dumps(fixture("CH1-2", confidence="high")), encoding="utf-8")
        (root / "CH4-1.json").write_text(json.dumps(fixture("CH4-1", confidence="low")), encoding="utf-8")
        scope = selector.select_adversarial_scope(root, Path("/tmp/no-outline.md"), {"CH1-2"}, sequence_units={"CH1-1"})
    selected = set(scope["unit_ids"])
    if not {"CH1-1", "CH1-2", "CH4-1"}.issubset(selected):
        raise AssertionError(f"scope missed required units: {selected}")
    if "platform" not in scope["reasons"]["CH1-2"]:
        raise AssertionError("platform reason missing")
    if "low-confidence" not in scope["reasons"]["CH4-1"]:
        raise AssertionError("low-confidence reason missing")
    print("adversarial scope checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
