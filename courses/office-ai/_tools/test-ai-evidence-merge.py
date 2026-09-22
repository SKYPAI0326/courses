#!/usr/bin/env python3
"""Tests AI evidence construction, replacement and safety boundaries."""
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
from pathlib import Path


TOOLS = Path(__file__).resolve().parent
MERGER_PATH = TOOLS / "merge-ai-review-evidence.py"
COURSE_ROOT = TOOLS.parent
EVIDENCE = COURSE_ROOT / "_validation" / "evidence.json"
BASE_EVIDENCE = COURSE_ROOT / "_validation" / "evidence.pre-ai-simulated-2026-09-22.json"
CONTEXT_MANIFEST = COURSE_ROOT / "_validation" / "ai-simulated" / "context" / "manifest.json"


def load_merger():
    if not MERGER_PATH.is_file():
        raise AssertionError(f"missing evidence merger: {MERGER_PATH}")
    spec = importlib.util.spec_from_file_location("ai_evidence_merger", MERGER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot import evidence merger")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    merger = load_merger()
    evidence_path = BASE_EVIDENCE if BASE_EVIDENCE.is_file() else EVIDENCE
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    records = merger.build_records(
        COURSE_ROOT / "_validation" / "ai-simulated" / "stage1",
        COURSE_ROOT / "_validation" / "ai-simulated" / "stage2",
        CONTEXT_MANIFEST,
    )
    if not records or not all(r.get("actor") == "independent-ai" for r in records):
        raise AssertionError("build_records must return independent-ai records only")
    merged = merger.merge_records(copy.deepcopy(evidence), records)
    if len(merged["records"]) != len(evidence["records"]) + len(records):
        raise AssertionError("merge must preserve existing records and append new AI records")
    if merged["records"][: len(evidence["records"])] != evidence["records"]:
        raise AssertionError("existing evidence records changed during merge")
    try:
        merger.merge_records(copy.deepcopy(evidence), [{"actor": "human", "layer": "entry", "unit_ids": ["CH1-1"]}])
    except ValueError:
        pass
    else:
        raise AssertionError("human records must be rejected by AI merger")
    base = copy.deepcopy(records[0])
    base["verdict"] = "PENDING"
    later = copy.deepcopy(base)
    later["verdict"] = "PASS"
    replacement = merger.merge_records(copy.deepcopy(evidence), [base, later])
    matches = [r for r in replacement["records"] if r.get("layer") == base["layer"] and r.get("unit_ids") == base["unit_ids"] and r.get("actor") == "independent-ai"]
    if len(matches) != 1 or matches[0]["verdict"] != "PASS":
        raise AssertionError("later AI record must replace earlier same-key record")
    stale = copy.deepcopy(records[0])
    stale["artifacts"][0]["sha256"] = "0" * 64
    try:
        merger.merge_records(copy.deepcopy(evidence), [stale])
    except ValueError:
        pass
    else:
        raise AssertionError("stale hashes must be rejected by AI merger")
    print(f"evidence merge checks passed: {len(records)} AI records")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, json.JSONDecodeError) as exc:
        print(f"evidence merge check failed: {exc}")
        raise SystemExit(1)
