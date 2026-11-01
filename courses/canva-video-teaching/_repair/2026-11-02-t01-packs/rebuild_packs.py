#!/usr/bin/env python3
"""T-01: carry the 2026-11-01 CH1-5 / CH2-6 fixes (91371ef0) into the download packs.

Replaces only the CH1-5 and CH2-6 sections of Canva完整操作步驟.txt, then rewrites
canva-text-pack.zip and canva-handouts-offline.zip with their existing member lists
and order, reading each member from disk. Run with --check to only report.
Restore: git checkout main -- courses/canva-video-teaching/downloads courses/canva-video-teaching/_validation/continuity-artifact-inventory.json
"""

import hashlib
import json
import sys
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

COURSE = Path(__file__).resolve().parents[2]
REPO = COURSE.parents[1]
LESSONS = REPO / "_lessons/canva-video-teaching"
DOWNLOADS = COURSE / "downloads"
STEPS = DOWNLOADS / "Canva完整操作步驟.txt"
UNITS = ("CH1-5", "CH2-6")
MD = MarkdownIt("commonmark", {"html": True, "breaks": True}).enable("table")


def plain(unit):
    raw = (LESSONS / f"{unit}.md").read_text(encoding="utf-8")
    body = raw.split("<!-- learner-content:start -->", 1)[1].split("<!-- learner-content:end -->", 1)[0].strip()
    return BeautifulSoup(MD.render(body), "html.parser").get_text("\n", strip=True)


def sections(text):
    return text.split("\n\n")


def rebuild_steps(check):
    parts = sections(STEPS.read_text(encoding="utf-8"))
    heads = [p.split("\n", 1)[0] for p in parts]
    # Format check: every unchanged unit must already equal plain(md); otherwise this builder is wrong.
    for i, head in enumerate(heads):
        if (LESSONS / f"{head}.md").is_file() and head not in UNITS:
            status = "same" if parts[i] == f"{head}\n{plain(head)}" else "DIFFERENT"
            print(f"format {head}: {status}")
    for unit in UNITS:
        i = heads.index(unit)
        new = f"{unit}\n{plain(unit)}"
        print(f"{unit}: {'unchanged' if parts[i] == new else 'replaced'}")
        parts[i] = new
    if not check:
        STEPS.write_text("\n\n".join(parts), encoding="utf-8")


def rezip(target, base):
    with zipfile.ZipFile(target) as old:
        entries = [(info.filename, old.read(info) if not (base / info.filename).is_file() else None) for info in old.infolist()]
    tmp = target.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as new:
        for name, inline in entries:
            if inline is None:
                new.write(base / name, name)
            else:
                new.writestr(name, inline)
                print(f"{target.name}: kept inline member {name}")
    tmp.replace(target)


def update_inventory():
    path = COURSE / "_validation/continuity-artifact-inventory.json"
    inventory = json.loads(path.read_text(encoding="utf-8"))
    for record in inventory.get("archives", []):
        archive_path = REPO / record["path"]
        record["sha256"] = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        with zipfile.ZipFile(archive_path) as archive:
            record["entries"] = len(archive.namelist())
            record["members"] = archive.namelist()
    path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    check = "--check" in sys.argv
    rebuild_steps(check)
    if not check:
        rezip(DOWNLOADS / "canva-text-pack.zip", DOWNLOADS)
        rezip(DOWNLOADS / "canva-handouts-offline.zip", COURSE)
        update_inventory()
        print("rebuilt steps text, text pack, offline bundle, and archive inventory")
