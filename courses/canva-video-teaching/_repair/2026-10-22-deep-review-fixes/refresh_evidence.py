#!/usr/bin/env python3
"""Append current, honestly scoped evidence records for the Deep Review repair."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


STAGE = Path(__file__).resolve().parent
COURSE_DIR = STAGE.parents[1]
REPO_ROOT = COURSE_DIR.parents[1]
EVIDENCE_PATH = COURSE_DIR / "_validation/evidence.json"
TESTED_AT = "2026-10-22T19:20:00+08:00"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def log_record(path: Path) -> dict[str, str]:
    return {"path": relative(path), "sha256": sha256(path)}


def main() -> None:
    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    outline_path = REPO_ROOT / evidence["outline"]["path"]
    evidence["outline"]["sha256"] = sha256(outline_path)
    evidence["scope_note"] = (
        "13單元（CH1-1至CH2-6與EXT1）、12資源、28學員頁、四下載包；"
        "2026-10-22 Deep Review修正。內容、來源保真與機器檢查使用現行雜湊；"
        "CH2-1平面備援匯入、38秒完整平台路徑、EXT1、真人冷讀與連續跟做仍PENDING；未重新公開發布。"
    )

    ext1 = next(unit for unit in evidence["units"] if unit["id"] == "EXT1")
    ext1["platform_required"] = True
    ext1.pop("platform_reason", None)

    paths = {evidence["outline"]["path"]}
    for unit in evidence["units"]:
        paths.update([unit["source"], unit["page"], *unit.get("assets", [])])
    missing = [path for path in sorted(paths) if not (REPO_ROOT / path).is_file()]
    if missing:
        raise SystemExit(f"missing artifact paths: {missing}")
    artifacts = [
        {"path": path, "sha256": sha256(REPO_ROOT / path)} for path in sorted(paths)
    ]
    unit_ids = [unit["id"] for unit in evidence["units"]]

    content_log = STAGE / "CONTENT-SELF-CHECK.md"
    fidelity_log = STAGE / "FIDELITY-SELF-CHECK.md"
    technical_log = STAGE / "static-output.txt"
    common = {"unit_ids": unit_ids, "tested_at": TESTED_AT}
    records = [
        {
            "layer": "content",
            "actor": "author-self-check",
            "verdict": "PASS",
            **common,
            "notes": (
                "Deep Review六項裁決已逐項處理；CH2-1新增平面備援，CH2-3依實際起點分流。"
                "平台時間與真人可用性未由此紀錄宣稱。"
            ),
            "log": log_record(content_log),
            "artifacts": artifacts,
        },
        {
            "layer": "fidelity",
            "actor": "author-self-check",
            "verdict": "PASS",
            **common,
            "notes": "作者核對正式來源、學員頁、搜尋索引與可攜文字；平台行為不在此結論內。",
            "log": log_record(fidelity_log),
            "artifacts": artifacts,
        },
        {
            "layer": "fidelity",
            "actor": "tool-run",
            "verdict": "PASS",
            **common,
            "notes": "25個單元與資源頁的來源文字及表格比對無缺漏，676個本地連結可解析。",
            "log": log_record(technical_log),
            "artifacts": artifacts,
        },
        {
            "layer": "technical",
            "actor": "tool-run",
            "verdict": "PASS",
            **common,
            "notes": (
                "28頁lint、25頁結構、substance、本地連結、四ZIP CRC與36秒備援媒體長度通過；"
                "未包含Canva平台操作。"
            ),
            "log": log_record(technical_log),
            "artifacts": artifacts,
        },
        {
            "layer": "platform",
            "actor": "author-self-check",
            "verdict": "PENDING",
            **common,
            "notes": "歷史部分Canva證據保留；本輪CH2-1平面備援、38秒全流程與EXT1未做平台重跑。",
        },
        {
            "layer": "platform",
            "actor": "tool-run",
            "verdict": "PENDING",
            **common,
            "notes": "本輪只有本地靜態與媒體檢查，沒有可替代Canva或WhisperDesktop實作的工具證據。",
        },
        {
            "layer": "sequence",
            "actor": "author-self-check",
            "verdict": "PENDING",
            **common,
            "notes": "內容分支已對齊；真人冷讀、連續跟做、計時與轉用尚未執行。",
        },
    ]
    evidence["records"] = [
        record for record in evidence["records"] if record.get("tested_at") != TESTED_AT
    ]
    evidence["records"].extend(records)
    evidence["last_repair"] = {
        "date": "2026-10-22",
        "version": "deep-review-fixes",
        "content": "AUTHOR_CHECK_PASS",
        "fidelity": "AUTHOR_AND_TOOL_PASS",
        "technical": "TOOL_PASS",
        "platform": "PENDING",
        "human": "PENDING",
        "report": relative(STAGE / "REPAIR-REPORT.md"),
    }
    EVIDENCE_PATH.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"evidence refreshed: {len(unit_ids)} units, {len(artifacts)} artifacts, {len(records)} records")


if __name__ == "__main__":
    main()
