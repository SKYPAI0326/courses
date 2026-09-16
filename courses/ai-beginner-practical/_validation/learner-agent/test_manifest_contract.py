#!/usr/bin/env python3
"""Contract test for the learner-agent evidence manifest builder."""

from pathlib import Path
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(__file__).with_name("build_manifest.py")
OUTPUT = Path(__file__).with_name("evidence-manifest.json")


def main() -> None:
    assert SCRIPT.exists(), "build_manifest.py must exist before L5 can use page evidence"
    subprocess.run(
        [sys.executable, str(SCRIPT), "--course-root", str(ROOT), "--output", str(OUTPUT)],
        check=True,
    )
    payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
    assert payload["course"] == "ai-beginner-practical"
    assert payload["evidence_mode"] == "learner-facing-pages"
    assert payload["pages"]
    assert {page["path"] for page in payload["pages"]} == {
        "index.html",
        "module1.html",
        "CH1-1.html",
        "CH2-1.html",
        "CH3-1.html",
        "CH4-1.html",
    }
    for page in payload["pages"]:
        assert page["html_sha256"]
        assert page["visible_text_sha256"]
        assert page["visible_text"]
        assert page["path"] not in payload["forbidden_paths"]
    assert "_validation" in payload["forbidden_roots"]
    assert any(asset["path"].endswith(".md") for asset in payload["learner_assets"])
    print("learner-agent evidence manifest: PASS")


if __name__ == "__main__":
    main()
