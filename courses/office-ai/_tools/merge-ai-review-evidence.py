#!/usr/bin/env python3
"""Merge independent-ai review logs into evidence.json and build triage."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any


TOOLS_ROOT = Path(__file__).resolve().parent
COURSE_ROOT = TOOLS_ROOT.parent
PROJECT_ROOT = COURSE_ROOT.parents[1]
VALIDATION_ROOT = COURSE_ROOT / "_validation"
AI_ROOT = VALIDATION_ROOT / "ai-simulated"
EVIDENCE_PATH = VALIDATION_ROOT / "evidence.json"
TRIAGE_PATH = AI_ROOT / "AI-TRIAGE-REPORT.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative_project(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


def load_contexts(context_manifest: Path) -> dict[str, dict[str, Any]]:
    manifest = json.loads(context_manifest.read_text(encoding="utf-8"))
    result: dict[str, dict[str, Any]] = {}
    context_root = context_manifest.parent
    for unit in manifest.get("units", []):
        path = context_root / f"{unit['unit_id']}.json"
        result[unit["unit_id"]] = json.loads(path.read_text(encoding="utf-8"))
    return result


def load_evidence_units() -> dict[str, dict[str, Any]]:
    data = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    return {unit["id"]: unit for unit in data.get("units", [])}


def artifact_bundle(unit_ids: list[str], contexts: dict[str, dict[str, Any]], units: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    paths: dict[str, str] = {}
    for unit_id in unit_ids:
        if unit_id not in contexts or unit_id not in units:
            raise ValueError(f"unknown unit in AI review: {unit_id}")
        source = units[unit_id]["source"]
        source_path = PROJECT_ROOT / source
        if not source_path.is_file():
            raise ValueError(f"formal source missing: {source}")
        paths[source] = sha256(source_path)
        context = contexts[unit_id]
        paths[context["page"]] = context["page_sha256"]
        for asset in context.get("assets", []):
            paths[asset["path"]] = asset["sha256"]
    return [{"path": path, "sha256": value} for path, value in sorted(paths.items())]


def validate_record_artifacts(record: dict[str, Any]) -> None:
    artifacts = record.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("AI record artifacts must be a non-empty list")
    for artifact in artifacts:
        path = PROJECT_ROOT / artifact["path"]
        if not path.is_file():
            raise ValueError(f"AI record artifact missing: {artifact['path']}")
        if sha256(path) != artifact["sha256"]:
            raise ValueError(f"AI record artifact stale: {artifact['path']}")


def log_path(path: Path) -> str:
    return relative_project(path)


def base_record(layer: str, unit_ids: list[str], verdict: str, log: dict[str, Any], path: Path, artifacts: list[dict[str, str]], finding: dict[str, Any], stage: str) -> dict[str, Any]:
    return {
        "layer": layer,
        "unit_ids": unit_ids,
        "actor": "independent-ai",
        "verdict": verdict,
        "notes": finding.get("observations", "") + " 風險：" + finding.get("risk", "") + " 修復方向：" + finding.get("repair_direction", ""),
        "log": {"path": log_path(path), "sha256": sha256(path)},
        "artifacts": artifacts,
        "method": {
            "stage": stage,
            "model": log.get("model"),
            "prompt_revision": log.get("prompt_revision"),
            "input_context": log.get("input_context"),
        },
        "simulated_not_human": True,
        "limitations": log.get("limitations", []),
        "confidence": finding.get("confidence"),
        "citations": finding.get("citations", []),
    }


def build_records(stage1_dir: Path, stage2_dir: Path, context_manifest: Path) -> list[dict[str, Any]]:
    contexts = load_contexts(context_manifest)
    units = load_evidence_units()
    records: list[dict[str, Any]] = []
    for path in sorted(stage1_dir.glob("CH*.json")):
        log = json.loads(path.read_text(encoding="utf-8"))
        unit_ids = [log["unit_id"]]
        artifacts = artifact_bundle(unit_ids, contexts, units)
        for layer in ("entry", "completion", "understanding", "transfer"):
            records.append(base_record(layer, unit_ids, log[layer]["verdict"], log, path, artifacts, log[layer], "stage1"))
    for path in sorted(stage2_dir.glob("CH*.json")):
        log = json.loads(path.read_text(encoding="utf-8"))
        unit_ids = sorted(set(log["unit_ids"]))
        artifacts = artifact_bundle(unit_ids, contexts, units)
        for finding in log.get("challenge_findings", []):
            records.append(base_record(finding["layer"], unit_ids, finding["verdict"], log, path, artifacts, finding, "stage2"))
    for record in records:
        validate_record_artifacts(record)
    return records


def record_key(record: dict[str, Any]) -> tuple[str, tuple[str, ...], str]:
    return record.get("layer", ""), tuple(sorted(record.get("unit_ids", []))), record.get("actor", "")


def merge_records(evidence: dict[str, Any], new_records: list[dict[str, Any]]) -> dict[str, Any]:
    result = copy.deepcopy(evidence)
    existing = result.setdefault("records", [])
    for record in new_records:
        if record.get("actor") != "independent-ai" or record.get("simulated_not_human") is not True:
            raise ValueError("AI merger accepts only independent-ai records with simulated_not_human=true")
        validate_record_artifacts(record)
    latest: dict[tuple[str, tuple[str, ...], str], dict[str, Any]] = {}
    for record in new_records:
        latest[record_key(record)] = record
    new_keys = set(latest)
    existing[:] = [record for record in existing if record_key(record) not in new_keys]
    for record in latest.values():
        existing.append(copy.deepcopy(record))
    return result


def triage_priority(verdict: str, confidence: str | None, severity: str | None = None) -> int:
    if severity == "BLOCKER" or verdict == "FAIL":
        return 0
    if severity == "MAJOR":
        return 1
    if verdict == "PENDING":
        return 2
    if confidence == "low":
        return 3
    return 4


def build_triage(records: list[dict[str, Any]], stage1_dir: Path, stage2_dir: Path) -> str:
    findings: list[dict[str, Any]] = []
    for path in sorted(stage1_dir.glob("CH*.json")):
        log = json.loads(path.read_text(encoding="utf-8"))
        for layer in ("entry", "completion", "understanding", "transfer"):
            finding = log[layer]
            findings.append({"unit_ids": [log["unit_id"]], "layer": layer, "stage": "stage1", **finding})
        for issue in log.get("issues", []):
            # PASS/PENDING layer findings already carry the issue details. Keep
            # only explicit blocker/major issue records to avoid duplicate triage.
            if issue.get("severity") not in {"BLOCKER", "MAJOR", "FAIL"}:
                continue
            findings.append({"unit_ids": [log["unit_id"]], "layer": issue.get("layer", "unknown"), "stage": "stage1-issue", "verdict": "FAIL", "confidence": "low", "citations": [], "observations": issue.get("summary", ""), "risk": issue.get("summary", ""), "repair_direction": issue.get("human_action", "")})
    for path in sorted(stage2_dir.glob("CH*.json")):
        log = json.loads(path.read_text(encoding="utf-8"))
        for finding in log.get("challenge_findings", []):
            findings.append({"unit_ids": log["unit_ids"], "stage": "stage2", **finding})
    findings.sort(key=lambda item: (triage_priority(item.get("verdict", ""), item.get("confidence"), item.get("severity")), item.get("unit_ids", []), item.get("layer", "")))
    lines = [
        "# AI Triage Report: office-ai",
        "",
        f"- generated_at: `{date.today().isoformat()}`",
        "- actor: `independent-ai`",
        "- simulated_not_human: `true`",
        "- purpose: 排序使用者最後要真人檢測的項目；不代表真人通過。",
        "",
        "## Priority findings",
        "",
    ]
    for index, finding in enumerate(findings, 1):
        verdict = finding.get("verdict", "PENDING")
        confidence = finding.get("confidence", "unknown")
        units = ", ".join(finding.get("unit_ids", []))
        lines.extend([
            f"### {index}. {units} · {finding.get('layer', 'unknown')} · {verdict} · confidence={confidence}",
            f"- stage: `{finding.get('stage')}`",
            f"- citations: {', '.join(finding.get('citations', [])) or '未提供'}",
            f"- observation: {finding.get('observations', '')}",
            f"- risk: {finding.get('risk', '')}",
            f"- repair / human action: {finding.get('repair_direction', '')}",
            "",
        ])
    lines.extend([
        "## Reading rule",
        "",
        "先處理 FAIL／BLOCKER／MAJOR，再處理 PENDING、平台、sequence 與低信心項目；PASS 只代表目前 AI 模擬找不到確定性缺口。真人結果仍須另建 `human` evidence。",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("course", choices=["office-ai"])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    stage1 = AI_ROOT / "stage1"
    stage2 = AI_ROOT / "stage2"
    context_manifest = AI_ROOT / "context" / "manifest.json"
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    records = build_records(stage1, stage2, context_manifest)
    triage = build_triage(records, stage1, stage2)
    if args.dry_run:
        print(json.dumps({"new_ai_records": len(records), "triage_lines": len(triage.splitlines()), "dry_run": True}, ensure_ascii=False))
        return 0
    backup = VALIDATION_ROOT / "evidence.pre-ai-simulated-2026-09-22.json"
    if not backup.exists():
        backup.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    merged = merge_records(evidence, records)
    tmp = EVIDENCE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(EVIDENCE_PATH)
    TRIAGE_PATH.write_text(triage, encoding="utf-8")
    print(json.dumps({"new_ai_records": len(records), "total_records": len(merged["records"]), "triage": str(TRIAGE_PATH)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
