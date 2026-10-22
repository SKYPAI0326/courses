#!/usr/bin/env python3
"""Machine-verifiable acceptance checks for the accepted Deep Review findings."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


COURSE_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = COURSE_DIR.parents[1]
SOURCE_DIR = REPO_ROOT / "_lessons/canva-video-teaching"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def check(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> None:
    failures: list[str] = []
    ch21 = (SOURCE_DIR / "CH2-1.md").read_text(encoding="utf-8")
    ch23 = (SOURCE_DIR / "CH2-3.md").read_text(encoding="utf-8")

    check("footage-v1.mp4" in ch21, "B-03 CH2-1 lacks a direct fallback video", failures)
    check("平面備援" in ch21, "B-03 CH2-1 does not label the flattened fallback", failures)
    check(
        "不能分層修改原有文字與背景" in ch21,
        "B-03 CH2-1 omits the flattened fallback limitation",
        failures,
    )
    check(
        "播放第 10 秒閱讀與第 16 秒自習" not in ch23,
        "A-002 CH2-3 still hard-codes the 36-second scene starts",
        failures,
    )
    for marker in ("36 秒版", "38 秒版", "較短版本", "實際片段起點"):
        check(marker in ch23, f"A-002 CH2-3 missing branch marker: {marker}", failures)
    check(
        "既有頁面加入音訊後確認覆蓋全片" not in ch23,
        "A-002 CH2-3 still promises that a 36-second track covers every branch",
        failures,
    )

    for page, markers in {
        "ch2/CH2-1.html": ("footage-v1.mp4", "平面備援", "不能分層修改原有文字與背景"),
        "ch2/CH2-3.html": ("36 秒版", "38 秒版", "較短版本", "實際片段起點"),
    }.items():
        text = (COURSE_DIR / page).read_text(encoding="utf-8")
        check('class="action-layout-pilot"' in text, f"HTML action layout missing: {page}", failures)
        check("action-steps" in text, f"HTML action steps missing: {page}", failures)
        for marker in markers:
            check(marker in text, f"source/HTML sync missing {marker}: {page}", failures)

    evidence_path = COURSE_DIR / "_validation/evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    ext1 = next(unit for unit in evidence["units"] if unit["id"] == "EXT1")
    check(ext1.get("platform_required") is True, "A-003 EXT1 must require platform evidence", failures)
    check("2026-10-22" in evidence.get("scope_note", ""), "A-001 scope note is stale", failures)
    check(
        evidence["outline"]["sha256"] == sha256(REPO_ROOT / evidence["outline"]["path"]),
        "A-001 outline snapshot is stale",
        failures,
    )
    fresh_layers = {
        record.get("layer")
        for record in evidence.get("records", [])
        if "2026-10-22" in record.get("tested_at", "")
    }
    check(
        {"content", "fidelity", "technical", "platform", "sequence"} <= fresh_layers,
        "A-001 evidence lacks a fresh five-layer status set",
        failures,
    )

    portable_text = (COURSE_DIR / "downloads/Canva完整操作步驟.txt").read_text(encoding="utf-8")
    check("平面備援" in portable_text, "portable text is stale for CH2-1", failures)
    check("38 秒版" in portable_text, "portable text is stale for CH2-3", failures)

    text_pack = COURSE_DIR / "downloads/canva-text-pack.zip"
    with zipfile.ZipFile(text_pack) as archive:
        packed_text = archive.read("Canva完整操作步驟.txt").decode("utf-8")
        check(packed_text == portable_text, "text pack contains a stale portable handout", failures)

    offline = COURSE_DIR / "downloads/canva-handouts-offline.zip"
    expected_files = [
        COURSE_DIR / "index.html",
        COURSE_DIR / "module1.html",
        COURSE_DIR / "module2.html",
        COURSE_DIR / "EXT1.html",
        COURSE_DIR / "search-index.json",
        *sorted((COURSE_DIR / "ch1").glob("*.html")),
        *sorted((COURSE_DIR / "ch2").glob("*.html")),
        *sorted((COURSE_DIR / "resources").glob("*.html")),
        COURSE_DIR / "assets/handout.css",
        COURSE_DIR / "assets/handout.js",
    ]
    with zipfile.ZipFile(offline) as archive:
        member_names = set(archive.namelist())
        check(
            all(not name.startswith("/") and ".." not in Path(name).parts for name in member_names),
            "B-02 offline ZIP contains an unsafe member path",
            failures,
        )
        for path in expected_files:
            member = str(path.relative_to(COURSE_DIR))
            check(member in member_names, f"B-02 offline ZIP missing {member}", failures)
            if member in member_names:
                check(
                    sha256_bytes(archive.read(member)) == sha256(path),
                    f"B-02 offline ZIP stale member: {member}",
                    failures,
                )

    inventory_path = COURSE_DIR / "_validation/continuity-artifact-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    for record in inventory["archives"]:
        archive_path = REPO_ROOT / record["path"]
        check(record["sha256"] == sha256(archive_path), f"inventory stale: {record['path']}", failures)
        with zipfile.ZipFile(archive_path) as archive:
            check(record["entries"] == len(archive.infolist()), f"inventory count stale: {record['path']}", failures)

    gates = (COURSE_DIR / "_gates.md").read_text(encoding="utf-8")
    check("2026-10-22" in gates, "B-04 Gate date is stale", failures)
    check("未提交、推送、公開發布" not in gates, "B-04 Gate still contains stale Git status", failures)
    check("MACHINE_READY_PENDING_HUMAN" in gates, "B-04 Gate omits current validator status", failures)

    if failures:
        print(f"FAIL: {len(failures)} acceptance checks")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("PASS: all Deep Review machine-verifiable acceptance checks")


if __name__ == "__main__":
    main()
