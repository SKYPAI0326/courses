#!/usr/bin/env python3
"""Refresh evidence records invalidated by the growth-assistant content change."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


COURSE = Path(__file__).resolve().parents[2]
BASE = COURSE.parents[1]
EVIDENCE = COURSE / "_validation/evidence.json"
CORE_CHANGED = {"CH1-2", "CH6-1", "CH6-3"}
SHELL_CHANGED = {"CH1-1", "CH1-3", "CH5-3", "CH6-2"}


def full_path(relative: str) -> Path:
    return BASE / relative


def digest(relative: str) -> str:
    return hashlib.sha256(full_path(relative).read_bytes()).hexdigest()


def artifact(relative: str) -> dict[str, str]:
    return {"path": relative, "sha256": digest(relative)}


data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
data["outline"] = {"path": "_outlines/office-ai.md", "sha256": digest("_outlines/office-ai.md")}
data["scope_note"] = "本輪更新 CH1-2、CH6-1、CH6-3 的成長型知識助理主線，並同步四個相鄰頁的章節／導覽標題；版本不符的舊紀錄已退出現行證據。"

unit_updates = {
    "CH1-2": {
        "course_type": "concept",
        "assets": ["courses/office-ai/assets/datasets/meeting-transcript-sample.txt"],
        "platform_required": True,
        "platform_reason": "本頁要求 Gemini Notebook 指定來源、引用與回查；付費帳號僅驗證入口，完整任務及免費帳號仍待實跑。",
    },
    "CH6-1": {
        "course_type": "skill-operation",
        "assets": [
            "courses/office-ai/assets/skills/ta-core.md",
            "courses/office-ai/assets/skills/ta-work.md",
            "courses/office-ai/assets/datasets/week-tasks-sample.txt",
            "courses/office-ai/assets/datasets/meeting-transcript-sample.txt",
        ],
        "platform_required": True,
        "platform_reason": "本頁要求 Gemini Skills、Gemini Notebook 連接器、唯讀列本與受控回寫；入口已驗證，完整八項與免費帳號仍待實跑。",
    },
    "CH6-3": {
        "course_type": "integration-capstone",
        "assets": [
            "courses/office-ai/assets/skills/ta-core.md",
            "courses/office-ai/assets/skills/ta-learning.md",
            "courses/office-ai/assets/after-class-guide.md",
            "courses/office-ai/assets/datasets/prompts-all.txt",
        ],
        "platform_required": True,
        "platform_reason": "本頁要求講義回查、引導式解惑、受控沉澱與 30 天成長；入口已驗證，完整八項與免費帳號仍待實跑。",
    },
}
for unit in data["units"]:
    if unit["id"] in unit_updates:
        unit.update(unit_updates[unit["id"]])

# Core-content changes invalidate every record that touches those units. Shell
# title changes invalidate only records that bind the changed page bytes; source-
# only content reviews remain valid. Removed independent simulations are not
# relabeled as current.
shell_pages = {
    "courses/office-ai/ch1/CH1-1.html",
    "courses/office-ai/ch1/CH1-3.html",
    "courses/office-ai/ch5/CH5-3.html",
    "courses/office-ai/ch6/CH6-2.html",
}


def invalidated(record: dict) -> bool:
    record_units = set(record.get("unit_ids", []))
    if not CORE_CHANGED.isdisjoint(record_units):
        return True
    if SHELL_CHANGED.isdisjoint(record_units):
        return False
    artifact_paths = {item.get("path") for item in record.get("artifacts", []) if isinstance(item, dict)}
    return bool(shell_pages & artifact_paths)


data["records"] = [record for record in data["records"] if not invalidated(record)]

assets = {unit: unit_updates[unit]["assets"] for unit in CORE_CHANGED}
pages = {"CH1-2": "courses/office-ai/ch1/CH1-2.html", "CH6-1": "courses/office-ai/ch6/CH6-1.html", "CH6-3": "courses/office-ai/ch6/CH6-3.html"}
sources = {unit: f"_lessons/office-ai/{unit}.md" for unit in CORE_CHANGED}

for unit in ("CH1-2", "CH6-1", "CH6-3"):
    content_log = f"courses/office-ai/_review/{unit}-content.md"
    fidelity_log = f"courses/office-ai/_review/{unit}-fidelity.md"
    data["records"].append(
        {
            "layer": "content",
            "unit_ids": [unit],
            "actor": "author-self-check",
            "verdict": "PASS",
            "notes": "作者依 course contract 核對入口、完整示範、學員操作、修復路徑、完成線與可移植條件；真人與獨立審查仍待驗。",
            "log": artifact(content_log),
            "artifacts": [artifact(sources[unit]), *[artifact(path) for path in assets[unit]]],
        }
    )
    data["records"].append(
        {
            "layer": "fidelity",
            "unit_ids": [unit],
            "actor": "author-self-check",
            "verdict": "PASS",
            "notes": "正式 learner-content 已完整渲染到現行 HTML；僅把重複的成果標題轉為 hero 標籤，正文、Prompt、表格與資產連結保留。",
            "log": artifact(fidelity_log),
            "artifacts": [artifact(sources[unit]), artifact(pages[unit]), *[artifact(path) for path in assets[unit]]],
        }
    )

platform_log = "courses/office-ai/_review/platform-growth-assistant-2026-10-16.md"
data["records"].append(
    {
        "layer": "platform",
        "unit_ids": ["CH1-2", "CH6-1", "CH6-3"],
        "actor": "human",
        "verdict": "PENDING",
        "notes": "指定付費帳號已確認三份 Skill、Gemini Notebook 連接器與唯讀列出 15 本筆記本；完整任務、回寫及免費帳號 50 筆路徑仍待實跑。",
        "log": artifact(platform_log),
        "artifacts": [artifact(sources[unit]) for unit in ("CH1-2", "CH6-1", "CH6-3")] + [artifact(pages[unit]) for unit in ("CH1-2", "CH6-1", "CH6-3")],
    }
)

technical_log = "courses/office-ai/_review/technical-growth-assistant-2026-10-16.md"
if full_path(technical_log).exists():
    all_units = [unit["id"] for unit in data["units"]]
    technical_paths = []
    for unit in data["units"]:
        technical_paths.extend([unit["source"], unit["page"], *unit.get("assets", [])])
    technical_paths = list(dict.fromkeys(technical_paths))
    data["records"].append(
        {
            "layer": "technical",
            "unit_ids": all_units,
            "actor": "tool-run",
            "verdict": "PASS",
            "notes": "全課 19 頁通過 lint blocker/error、HTML structure 與正式頁本地連結檢查；本輪三個內容頁另通過 substance 與 1440/390/430 browser smoke。",
            "log": artifact(technical_log),
            "artifacts": [artifact(path) for path in technical_paths],
        }
    )

navigation_log = "courses/office-ai/_review/navigation-title-sync-2026-10-16.md"
if full_path(navigation_log).exists():
    shell_units = [unit for unit in data["units"] if unit["id"] in SHELL_CHANGED]
    shell_artifacts = []
    for unit in shell_units:
        shell_artifacts.extend([unit["source"], unit["page"], *unit.get("assets", [])])
    shell_artifacts = list(dict.fromkeys(shell_artifacts))
    data["records"].append(
        {
            "layer": "fidelity",
            "unit_ids": [unit["id"] for unit in shell_units],
            "actor": "author-self-check",
            "verdict": "PASS",
            "notes": "與備份逐檔比較後，只同步相鄰單元名稱與章節標籤；教學正文、Prompt、資產、gate、script 及連結目的地未變。",
            "log": artifact(navigation_log),
            "artifacts": [artifact(path) for path in shell_artifacts],
        }
    )

EVIDENCE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Updated {EVIDENCE}; records={len(data['records'])}")
