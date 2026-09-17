#!/usr/bin/env python3
"""Audit learner-facing course substance and build evidence for persona review."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.links: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key == "href" and value:
                self.links.append(value)

    @property
    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()


def digest(value: str | bytes) -> str:
    raw = value if isinstance(value, bytes) else value.encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def audit_page(course_dir: Path, path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    source = raw.decode("utf-8", errors="replace")
    parser = VisibleTextParser()
    parser.feed(source)
    text = parser.text
    lower = text.lower()
    ordered_step_items = sum(
        len(re.findall(r"<li\b", block, re.I))
        for block in re.findall(r"<ol\b[^>]*>(.*?)</ol>", source, re.I | re.S)
    )
    table_step_rows = len(re.findall(r"<td>\s*(?:[1-9]|1[0-2])\s*</td>", source, re.I))
    explicit_step_markers = len(re.findall(r"步驟\s*[0-9一二三四五六七八九十]", text))
    asset_links = [link for link in parser.links if link.startswith("assets/templates/")]
    missing_assets = []
    for link in asset_links:
        target = (path.parent / link.split("#", 1)[0]).resolve()
        if not target.exists():
            missing_assets.append(link)

    checks = {
        "title": bool(re.search(r"<title>[^<]+</title>", source, re.I)),
        "h1": bool(re.search(r"<h1\b", source, re.I)),
        "orientation": "起始材料" in text and any(marker in text for marker in ("情境", "現在在哪裡", "上一堂", "本堂", "這堂")),
        "completion_artifact": any(marker in text for marker in ("完成物", "完成品", "完成後你會留下", "要留下什麼", "成果")),
        "concept_or_explanation": "概念" in text or "判斷" in text,
        "worked_operation": any(marker in text for marker in ("操作示範", "示範", "跟著做", "學員跟做", "同步演練", "動手", "產物整理", "完整示範", "提案架構", "分組製作", "口頭演練", "個人製作")),
        "observable_verification": any(marker in text for marker in ("檢核", "驗收", "自我檢查", "Checkpoint", "通過條件")),
        "pitfalls": any(marker in text for marker in ("常見錯誤", "沒看到時", "失敗時", "卡住時", "回修", "修復")),
        "recovery": any(marker in text for marker in ("修復", "卡住", "回修", "停止", "重跑", "回到", "備援")),
        "transfer_or_handoff": any(marker in text for marker in ("交接", "交給", "下一個使用位置", "變化題", "Solo", "下游")),
        "action_steps": max(explicit_step_markers, ordered_step_items, table_step_rows) >= 5,
        "no_raw_markdown_asset_href": not any(link.endswith(".md") for link in asset_links),
        "no_production_notes": not any(marker in raw.decode("utf-8", errors="replace") for marker in ("講師授課筆記", "Verification Asset Spec", "_lessons/", "BLOCK：待建立")),
    }
    hard_keys = ("title", "h1", "orientation", "completion_artifact", "concept_or_explanation", "worked_operation", "observable_verification", "pitfalls", "action_steps", "no_raw_markdown_asset_href", "no_production_notes")
    hard_failures = [key for key in hard_keys if not checks[key]]
    warnings = [key for key in checks if key not in hard_keys and not checks[key]]
    return {
        "path": str(path.relative_to(course_dir)),
        "html_sha256": digest(raw),
        "visible_text_sha256": digest(text),
        "visible_text_chars": len(text),
        "asset_links": len(asset_links),
        "missing_assets": missing_assets,
        "checks": checks,
        "hard_failures": hard_failures,
        "warnings": warnings,
        "status": "BLOCK" if hard_failures or missing_assets else ("REVIEW" if warnings else "READY_FOR_HUMAN"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--build-evidence-manifest", action="store_true")
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    course_dir = project_root / "courses" / args.slug
    validation_dir = course_dir / "_validation"
    excluded_dirs = {"_backup", "_repair", "_validation", "assets", "web-starter"}
    pages = sorted(
        path
        for pattern in ("CH*.html", "PRAC*.html")
        for path in course_dir.rglob(pattern)
        if not any(part in excluded_dirs for part in path.relative_to(course_dir).parts[:-1])
    )
    records = [audit_page(course_dir, path) for path in pages]
    summary = {
        "pages": len(records),
        "block": sum(record["status"] == "BLOCK" for record in records),
        "review": sum(record["status"] == "REVIEW" for record in records),
        "ready_for_human": sum(record["status"] == "READY_FOR_HUMAN" for record in records),
        "missing_assets": sum(bool(record["missing_assets"]) for record in records),
    }
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "course": args.slug,
        "summary": summary,
        "pages": records,
    }
    validation_dir.mkdir(parents=True, exist_ok=True)
    if args.build_evidence_manifest:
        output = validation_dir / "L5-evidence-manifest.json"
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {output}")
    print(json.dumps(summary, ensure_ascii=False))
    for record in records:
        if record["status"] != "READY_FOR_HUMAN":
            print(f"{record['status']}: {record['path']} hard={record['hard_failures']} warn={record['warnings']}")
    return 1 if summary["block"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
