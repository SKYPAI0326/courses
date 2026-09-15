#!/usr/bin/env python3
"""Regression tests for the Lite Pack compose patch embedded in the wizards."""
from __future__ import annotations

import os
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / "assets/n8n-lite-pack.zip"
MAC_PAGE = ROOT / "lessons/m0-install-mac.html"
WIN_PAGE = ROOT / "lessons/m0-install-win.html"
LAUNCH_PAGE = ROOT / "lessons/m1-1-launch.html"

REQUIRED = {
    "N8N_RESTRICT_FILE_ACCESS_TO": "/files/shared",
    "N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES": "true",
    "N8N_BLOCK_ENV_ACCESS_IN_NODE": "false",
    "GEMINI_API_KEY": "${GEMINI_API_KEY:-}",
}

FIXTURE = """services:
  postgres:
    image: postgres:16
    environment:
      - GEMINI_API_KEY=wrong-service-value
  n8n:
    image: n8nio/n8n:2.37.7
    restart: unless-stopped
    environment:
      # Existing comments are valid YAML and must not break patching.
      - DB_TYPE=postgresdb

      # Another comment and blank line before the missing settings.
    volumes:
      - ./shared:/files/shared
"""


def mac_python_block() -> str:
    with zipfile.ZipFile(PACKAGE) as archive:
        source = archive.read("n8n-lite-pack/setup-wizard.command").decode("utf-8")
    marker = "COMPOSE_PATCHED=$(python3 - <<'PY'\n"
    body = source.split(marker, 1)[1].split("\nPY\n", 1)[0]
    return body


def run_mac_patch(compose: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["COMPOSE"] = str(compose)
    return subprocess.run(
        ["python3", "-"],
        input=mac_python_block(),
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )


def parsed_env(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^\s*-\s*([A-Z0-9_]+)=(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2)
    return values


def test_mac_patch_accepts_comments_and_blank_lines() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        compose = Path(tmp) / "n8n-compose.yml"
        compose.write_text(FIXTURE, encoding="utf-8")
        result = run_mac_patch(compose)
        assert result.returncode == 0, result.stderr
        assert result.stdout.startswith("PATCHED:"), result.stdout
        values = parsed_env(compose.read_text(encoding="utf-8"))
        assert {key: values[key] for key in REQUIRED} == REQUIRED


def test_windows_wizard_uses_same_current_contract_and_no_brittle_block_regex() -> None:
    with zipfile.ZipFile(PACKAGE) as archive:
        source = archive.read("n8n-lite-pack/setup-wizard.ps1").decode("utf-8-sig")
    assert "N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=true" in source
    assert "n8n-compose.yml" in source
    assert "$EnvironmentContent -notmatch $pat" in source
    assert "(?:      - [^\\r\\n]+\\r?\\n)+" not in source


def test_download_links_use_current_cache_busters() -> None:
    for page in (MAC_PAGE, WIN_PAGE):
        source = page.read_text(encoding="utf-8")
        assert "n8n-starter-kit.zip?v=1.1.0" in source
        assert "n8n-lite-pack.zip?v=1.3.6" in source
    assert "n8n-starter-kit.zip?v=1.1.0" in LAUNCH_PAGE.read_text(encoding="utf-8")


if __name__ == "__main__":
    test_mac_patch_accepts_comments_and_blank_lines()
    test_windows_wizard_uses_same_current_contract_and_no_brittle_block_regex()
    test_download_links_use_current_cache_busters()
    print("PASS")
