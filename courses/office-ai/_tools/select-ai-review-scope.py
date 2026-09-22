#!/usr/bin/env python3
"""Select the second-stage adversarial review scope from stage-1 findings."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_SEQUENCE = {"CH1-1", "CH1-2", "CH1-3"}
DEFAULT_PLATFORM_UNITS = {"CH1-2", "CH5-1"}
DEFAULT_FLAGSHIP_UNITS = {"CH2-3", "CH3-1", "CH3-2"}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flagship_units(outline_path: Path) -> set[str]:
    if not outline_path.is_file():
        return set(DEFAULT_FLAGSHIP_UNITS)
    text = outline_path.read_text(encoding="utf-8", errors="ignore")
    found = set(re.findall(r"-\s*(CH\d-\d).*?\(flagship", text, flags=re.IGNORECASE))
    return found or set(DEFAULT_FLAGSHIP_UNITS)


def select_adversarial_scope(
    stage1_dir: Path,
    outline_path: Path,
    required_platform_units: set[str],
    sequence_units: set[str] | None = None,
) -> dict[str, Any]:
    sequence_units = sequence_units or set(DEFAULT_SEQUENCE)
    platform_units = set(required_platform_units) or set(DEFAULT_PLATFORM_UNITS)
    flagship = flagship_units(outline_path)
    reasons: dict[str, list[str]] = {}
    hashes: dict[str, str] = {}
    for path in sorted(stage1_dir.glob("CH*.json")):
        log = json.loads(path.read_text(encoding="utf-8"))
        unit_id = log["unit_id"]
        hashes[unit_id] = file_sha256(path)
        unit_reasons: list[str] = []
        if unit_id in platform_units:
            unit_reasons.append("platform")
        if unit_id in flagship:
            unit_reasons.append("flagship")
        if unit_id in sequence_units:
            unit_reasons.append("sequence")
        if any(
            isinstance(log.get(layer), dict) and log[layer].get("confidence") == "low"
            for layer in ("entry", "completion", "understanding", "transfer")
        ):
            unit_reasons.append("low-confidence")
        if log.get("completion", {}).get("verdict") != "PASS":
            unit_reasons.append("completion-not-pass")
        if any(issue.get("severity") in {"BLOCKER", "MAJOR"} for issue in log.get("issues", []) if isinstance(issue, dict)):
            unit_reasons.append("blocker-or-major")
        if unit_reasons:
            reasons[unit_id] = sorted(set(unit_reasons))
    return {
        "schema_version": 1,
        "stage": "stage2",
        "prompt_revision": "adversarial-review-v1",
        "unit_ids": sorted(reasons),
        "reasons": reasons,
        "source_stage1_hashes": hashes,
        "required_platform_units": sorted(platform_units),
        "sequence_units": sorted(sequence_units),
        "flagship_units": sorted(flagship),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage1-dir", type=Path, required=True)
    parser.add_argument("--outline", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--platform-unit", action="append", default=[])
    args = parser.parse_args()
    scope = select_adversarial_scope(args.stage1_dir, args.outline, set(args.platform_unit) or DEFAULT_PLATFORM_UNITS)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(scope, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"selected adversarial scope: {len(scope['unit_ids'])} units")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
