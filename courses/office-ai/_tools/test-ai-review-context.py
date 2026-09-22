#!/usr/bin/env python3
"""Deterministic checks for the learner-only AI review context bundle."""
from __future__ import annotations

import json
import sys
from pathlib import Path


COURSE_ROOT = Path(__file__).resolve().parents[1]
CONTEXT_ROOT = COURSE_ROOT / "_validation" / "ai-simulated" / "context"
MANIFEST = CONTEXT_ROOT / "manifest.json"
EXPECTED_UNITS = {
    "CH1-1", "CH1-2", "CH1-3", "CH1-4",
    "CH2-1", "CH2-2", "CH2-3",
    "CH3-1", "CH3-2", "CH3-3",
    "CH4-1", "CH4-2", "CH4-3",
    "CH5-1", "CH5-2", "CH5-3",
    "CH6-1", "CH6-2", "CH6-3",
}
FORBIDDEN_MARKERS = (
    "_review",
    "_validation",
    "_lessons",
    "author-self-check",
    "validator",
    "learner-content:start",
    "learner-content:end",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    if not MANIFEST.is_file():
        fail(f"missing context manifest: {MANIFEST}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1:
        fail("context manifest schema_version must be 1")
    units = manifest.get("units")
    if not isinstance(units, list) or {u.get("unit_id") for u in units} != EXPECTED_UNITS:
        fail("context manifest must contain exactly the 19 office-ai units")
    for unit in units:
        unit_id = unit["unit_id"]
        path = CONTEXT_ROOT / f"{unit_id}.json"
        if not path.is_file():
            fail(f"missing context file: {path}")
        context = json.loads(path.read_text(encoding="utf-8"))
        if context.get("schema_version") != 1:
            fail(f"{unit_id}: invalid schema_version")
        if context.get("unit_id") != unit_id:
            fail(f"{unit_id}: context unit_id mismatch")
        if not context.get("page_sha256") or len(context["page_sha256"]) != 64:
            fail(f"{unit_id}: missing page SHA-256")
        if not context.get("visible_sections"):
            fail(f"{unit_id}: visible_sections is empty")
        serialized = path.read_text(encoding="utf-8")
        for marker in FORBIDDEN_MARKERS:
            if marker in serialized:
                fail(f"{unit_id}: forbidden internal marker present: {marker}")
        for asset in context.get("assets", []):
            if not asset.get("path") or not asset.get("sha256"):
                fail(f"{unit_id}: asset lacks path or hash")
    print(f"context checks passed: {len(units)} units")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError) as exc:
        print(f"context check failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
