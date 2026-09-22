#!/usr/bin/env python3
"""Checks for the versioned LLM simulation prompt contracts."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "_validation" / "ai-simulated"
PROMPTS = ROOT / "prompts"
REQUIRED_SHARED = (
    "30 秒入口六題",
    "第一個動作",
    "可觀察結果",
    "完成物",
    "失敗時的回復",
    "simulated_not_human",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    learner = PROMPTS / "simulated-learner-v1.md"
    adversarial = PROMPTS / "adversarial-review-v1.md"
    schema = PROMPTS / "output-schema-v1.json"
    for path in (learner, adversarial, schema):
        if not path.is_file():
            fail(f"missing prompt contract: {path}")
    learner_text = learner.read_text(encoding="utf-8")
    adversarial_text = adversarial.read_text(encoding="utf-8")
    for marker in REQUIRED_SHARED:
        if marker not in learner_text or marker not in adversarial_text:
            fail(f"shared requirement missing from both prompts: {marker}")
    for marker in ("只能引用 learner-facing", "不可讀作者", "PASS", "PENDING"):
        if marker not in learner_text:
            fail(f"learner prompt missing boundary or verdict rule: {marker}")
    for marker in ("挑戰", "衝突", "BLOCKER", "MAJOR", "不得自行改檔"):
        if marker not in adversarial_text:
            fail(f"adversarial prompt missing challenge rule: {marker}")
    data = json.loads(schema.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        fail("output schema must use schema_version 1")
    if data.get("stage1", {}).get("required") is None:
        fail("output schema must define stage1 required fields")
    if data.get("stage2", {}).get("required") is None:
        fail("output schema must define stage2 required fields")
    print("prompt contract checks passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError) as exc:
        print(f"prompt contract check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
