#!/usr/bin/env python3
"""Validate AI simulation logs against learner contexts and current hashes."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


TOOLS_ROOT = Path(__file__).resolve().parent
COURSE_ROOT = TOOLS_ROOT.parent
PROJECT_ROOT = COURSE_ROOT.parents[1]
CONTEXT_ROOT = COURSE_ROOT / "_validation" / "ai-simulated" / "context"
ALLOWED_VERDICTS = {"PASS", "FAIL", "PENDING"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
STAGE_PROMPTS = {
    "stage1": "simulated-learner-v1",
    "stage2": "adversarial-review-v1",
}
STAGE1_LAYERS = ("entry", "completion", "understanding", "transfer")
STAGE2_LAYERS = {"content", "fidelity", "platform", "sequence"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict)):
        return bool(value)
    return value is not None


def context_for(unit_id: str) -> dict[str, Any]:
    path = CONTEXT_ROOT / f"{unit_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"missing context for {unit_id}: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def expected_artifacts(unit_ids: list[str]) -> dict[str, str]:
    expected: dict[str, str] = {}
    for unit_id in unit_ids:
        context = context_for(unit_id)
        expected[context["page"]] = context["page_sha256"]
        for asset in context.get("assets", []):
            expected[asset["path"]] = asset["sha256"]
    return expected


def validate_artifacts(log: dict[str, Any], unit_ids: list[str], errors: list[str]) -> None:
    artifacts = log.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifacts must be a non-empty list")
        return
    actual: dict[str, str] = {}
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict) or not artifact.get("path") or not artifact.get("sha256"):
            errors.append(f"artifacts[{index}] must contain path and sha256")
            continue
        path = str(artifact["path"])
        if path in actual:
            errors.append(f"duplicate artifact path: {path}")
        actual[path] = str(artifact["sha256"])
        file_path = PROJECT_ROOT / path
        if not file_path.is_file():
            errors.append(f"artifact file missing: {path}")
        elif sha256(file_path) != artifact["sha256"]:
            errors.append(f"stale artifact hash: {path}")
    try:
        expected = expected_artifacts(unit_ids)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
        return
    if set(actual) != set(expected):
        errors.append(
            "artifact paths do not match context: "
            f"missing={sorted(set(expected) - set(actual))}, extra={sorted(set(actual) - set(expected))}"
        )
    for path, expected_hash in expected.items():
        if path in actual and actual[path] != expected_hash:
            errors.append(f"context hash mismatch: {path}")


def validate_finding(finding: Any, location: str, errors: list[str]) -> None:
    if not isinstance(finding, dict):
        errors.append(f"{location} must be an object")
        return
    verdict = finding.get("verdict")
    if verdict not in ALLOWED_VERDICTS:
        errors.append(f"{location}.verdict must be PASS, FAIL or PENDING")
    confidence = finding.get("confidence")
    if confidence not in ALLOWED_CONFIDENCE:
        errors.append(f"{location}.confidence must be high, medium or low")
    citations = finding.get("citations")
    if not isinstance(citations, list) or (verdict == "PASS" and not citations):
        errors.append(f"{location}.citations must be a non-empty list for PASS")
    if verdict in {"FAIL", "PENDING"} and not nonempty(finding.get("observations")):
        errors.append(f"{location}.observations is required for FAIL/PENDING")
    for field in ("observations", "risk", "repair_direction"):
        if not nonempty(finding.get(field)):
            errors.append(f"{location}.{field} is required")


def validate_common(log: dict[str, Any], stage: str, errors: list[str]) -> list[str]:
    if log.get("stage") != stage:
        errors.append(f"stage must be {stage}")
    if log.get("actor") != "independent-ai":
        errors.append("actor must be independent-ai")
    if log.get("simulated_not_human") is not True:
        errors.append("simulated_not_human must be true")
    if log.get("prompt_revision") != STAGE_PROMPTS[stage]:
        errors.append(f"prompt_revision must be {STAGE_PROMPTS[stage]}")
    if not nonempty(log.get("model")):
        errors.append("model is required")
    if not nonempty(log.get("input_context")):
        errors.append("input_context is required")
    if not nonempty(log.get("limitations")):
        errors.append("limitations is required")
    unit_ids: list[str]
    if stage == "stage1":
        unit_id = log.get("unit_id")
        if not isinstance(unit_id, str) or not unit_id:
            errors.append("unit_id is required")
            unit_ids = []
        else:
            unit_ids = [unit_id]
    else:
        raw = log.get("unit_ids")
        if not isinstance(raw, list) or not raw or not all(isinstance(x, str) for x in raw):
            errors.append("unit_ids must be a non-empty list of strings")
            unit_ids = []
        else:
            unit_ids = sorted(set(raw))
    for unit_id in unit_ids:
        if not (CONTEXT_ROOT / f"{unit_id}.json").is_file():
            errors.append(f"unknown unit context: {unit_id}")
    if unit_ids:
        validate_artifacts(log, unit_ids, errors)
    return unit_ids


def validate_log(path: Path, stage: str) -> list[str]:
    errors: list[str] = []
    try:
        log = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read JSON: {exc}"]
    if not isinstance(log, dict):
        return ["log root must be an object"]
    unit_ids = validate_common(log, stage, errors)
    if stage == "stage1":
        for layer in STAGE1_LAYERS:
            if layer not in log:
                errors.append(f"missing stage1 layer: {layer}")
            else:
                validate_finding(log[layer], layer, errors)
        if not isinstance(log.get("issues"), list):
            errors.append("issues must be a list")
    else:
        if not isinstance(log.get("challenge_findings"), list) or not log["challenge_findings"]:
            errors.append("challenge_findings must be a non-empty list")
        else:
            for index, finding in enumerate(log["challenge_findings"]):
                if not isinstance(finding, dict):
                    errors.append(f"challenge_findings[{index}] must be an object")
                    continue
                layer = finding.get("layer")
                if layer not in STAGE2_LAYERS:
                    errors.append(f"challenge_findings[{index}].layer is invalid")
                validate_finding(finding, f"challenge_findings[{index}]", errors)
        if log.get("verdict") not in ALLOWED_VERDICTS:
            errors.append("stage2 verdict must be PASS, FAIL or PENDING")
        if not isinstance(log.get("conflicts_with_stage1"), bool):
            errors.append("conflicts_with_stage1 must be boolean")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("stage1", "stage2"), required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=Path)
    group.add_argument("--dir", type=Path)
    args = parser.parse_args()
    paths = [args.file] if args.file else sorted(args.dir.glob("CH*.json"))
    if not paths:
        print("no JSON logs found", file=sys.stderr)
        return 1
    all_errors: list[str] = []
    for path in paths:
        errors = validate_log(path, args.stage)
        all_errors.extend(f"{path}: {error}" for error in errors)
    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        return 1
    print(f"validated {len(paths)} {args.stage} AI review log(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
