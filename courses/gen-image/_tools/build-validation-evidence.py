#!/usr/bin/env python3
"""Build version-bound validation evidence for the repaired gen-image course."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "courses" / "gen-image"
VALIDATION = COURSE / "_validation"

UNIT_TYPES = {
    "CH1-1": "concept",
    "CH1-2": "skill-operation",
    "CH2-1": "concept",
    "CH2-2": "skill-operation",
    "PRAC2": "skill-operation",
    "CH3-1": "skill-operation",
    "CH3-2": "concept",
    "PRAC3": "skill-operation",
    "CH4-1": "skill-operation",
    "CH4-2": "skill-operation",
    "CH4-3": "skill-operation",
    "PRAC4": "skill-operation",
    "CH5-1": "integration-capstone",
}

PLATFORM_REQUIRED = {
    "CH1-2", "CH2-2", "PRAC2", "CH3-1", "PRAC3",
    "CH4-1", "CH4-2", "CH4-3", "PRAC4", "CH5-1",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def snap(paths: set[Path]) -> list[dict[str, str]]:
    return [
        {"path": rel(path), "sha256": sha(path)}
        for path in sorted(paths, key=lambda item: rel(item))
    ]


def local_page_files(page: Path) -> set[Path]:
    files: set[Path] = set()
    text = page.read_text(encoding="utf-8")
    for value in re.findall(r'(?:href|src)=["\']([^"\'#]+)', text):
        if value.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "data:")):
            continue
        target = (page.parent / value).resolve()
        if target.is_file() and target.is_relative_to(ROOT):
            files.add(target)
    return files


def main() -> None:
    VALIDATION.mkdir(parents=True, exist_ok=True)
    unit_ids = list(UNIT_TYPES)
    units = []
    sources: set[Path] = set()
    full_artifacts: set[Path] = set()
    for unit_id, course_type in UNIT_TYPES.items():
        source = ROOT / "_lessons" / "gen-image" / f"{unit_id}.md"
        page = COURSE / f"{unit_id}.html"
        sources.add(source)
        full_artifacts.update({source, page})
        full_artifacts.update(local_page_files(page))
        required = unit_id in PLATFORM_REQUIRED
        units.append({
            "id": unit_id,
            "course_type": course_type,
            "source": rel(source),
            "page": rel(page),
            "assets": [],
            "platform_required": required,
            "platform_reason": "" if required else "本單元可用課程內素材完成概念判讀，不要求登入外部平台。",
        })

    content_log = VALIDATION / "deep-review-repair-self-check.md"
    fidelity_log = VALIDATION / "fidelity-review.md"
    technical_log = VALIDATION / "machine-checks.md"
    for log in (content_log, fidelity_log, technical_log):
        if not log.is_file() or not log.read_text(encoding="utf-8").strip():
            raise SystemExit(f"missing evidence log: {log}")

    technical_artifacts = full_artifacts | {
        COURSE / "_repair/2026-10-17-image-refresh/IMAGE-MANIFEST.tsv",
        COURSE / "_repair/2026-10-17-image-refresh/ASSET-PROVENANCE.tsv",
        COURSE / "_repair/2026-10-17-image-refresh/IMAGE-PROMPT-SET.md",
        COURSE / "_tools/verify-image-refresh.py",
        COURSE / "_tools/test-deep-review-repair.py",
        COURSE / "_tools/test-learner-record-browser.py",
    }

    records = [
        {
            "layer": "content",
            "unit_ids": unit_ids,
            "actor": "author-self-check",
            "verdict": "PASS",
            "notes": "Deep Review 修補後由作者逐項重查 8 個已接受問題；這是作者自審，不冒充獨立複審或真人跟做。",
            "log": {"path": rel(content_log), "sha256": sha(content_log)},
            "artifacts": snap(sources),
        },
        {
            "layer": "fidelity",
            "unit_ids": unit_ids,
            "actor": "author-self-check",
            "verdict": "PASS",
            "notes": "逐單元對照正式來源、HTML 與頁面引用素材，確認核心教學與安全閘門沒有在轉製時遺漏。",
            "log": {"path": rel(fidelity_log), "sha256": sha(fidelity_log)},
            "artifacts": snap(full_artifacts),
        },
        {
            "layer": "technical",
            "unit_ids": unit_ids,
            "actor": "tool-run",
            "verdict": "PASS",
            "notes": "正式頁結構、變更頁 lint／內容掃描、連結可達性、素材清冊、scoped diff 與三種視窗瀏覽器驗收均無本輪阻擋錯誤。",
            "log": {"path": rel(technical_log), "sha256": sha(technical_log)},
            "artifacts": snap(technical_artifacts),
        },
    ]

    outline = ROOT / "_outlines" / "gen-image.md"
    evidence = {
        "schema_version": 1,
        "outline": {"path": rel(outline), "sha256": sha(outline)},
        "scope_note": "本輪覆蓋大綱的 13 個核心單元；CH6 情境卡與附錄做趨勢/規範修補與 smoke test，但不列為正式技能單元。",
        "units": units,
        "records": records,
    }
    (VALIDATION / "evidence.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
