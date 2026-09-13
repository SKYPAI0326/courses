#!/usr/bin/env python3
"""Static cross-asset contract check for the n8n Lite Pack.

This checker deliberately does not claim platform execution.  It verifies that
the 14 workflow JSON files parse, records their trigger/response contracts,
flags webhook fan-out with lastNode, and finds stale high-risk claims in the
overview and lesson pages.
"""
from __future__ import annotations

import html
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "assets" / "n8n-lite-pack.zip"
STARTER_DIR = ROOT / "assets" / "n8n-starter-kit"
STARTER_ZIP = ROOT / "assets" / "n8n-starter-kit.zip"
LOCAL_LITE_DIR = Path.home() / "Downloads" / "n8n-lite-pack"
LESSONS = ROOT / "lessons"
OVERVIEW = LESSONS / "m0-workflow-tour.html"
SLUGS = {
    "01": "webhook", "02": "pdf-rename", "03": "batch", "04": "daily",
    "05": "telegram", "06": "webhook-ai", "07": "tunnel",
    "08": "expression", "09": "gmail", "10": "folder-organize",
    "11": "csv-clean", "12": "knowledge-rag", "13": "daily-ops",
    "14": "api-monitor",
}


def executable(nodes: list[dict]) -> list[dict]:
    return [n for n in nodes if n.get("type") != "n8n-nodes-base.stickyNote"]


def fanout_sources(data: dict) -> list[str]:
    result = []
    for source, value in (data.get("connections") or {}).items():
        total = sum(len(branch) for branch in value.get("main", []) if isinstance(branch, list))
        if total > 1:
            result.append(f"{source}({total})")
    return result


def reachable_fanout_from_webhook(data: dict, webhook_names: list[str]) -> bool:
    """Return whether a fan-out is reachable from one of the webhook routes."""
    connections = data.get("connections") or {}
    seen: set[str] = set()
    stack = list(webhook_names)
    while stack:
        source = stack.pop()
        if source in seen:
            continue
        seen.add(source)
        branches = (connections.get(source) or {}).get("main", [])
        destinations = [dest for branch in branches if isinstance(branch, list) for dest in branch]
        if len(destinations) > 1:
            return True
        stack.extend(dest.get("node") for dest in destinations if dest.get("node"))
    return False


def plain(path: Path) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", path.read_text(errors="ignore"))).split())


def overview_card_text(overview_html: str, href: str) -> str:
    """Return visible text for one workflow card, keeping flags scoped to that card."""
    match = re.search(
        rf'<a\s+href="{re.escape(href)}"[^>]*>(.*?)</a>',
        overview_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return ""
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", match.group(1))).split())


def starter_archive_drift() -> list[str]:
    """Compare downloadable Starter Kit archive with its source directory."""
    drift = []
    if not STARTER_ZIP.exists():
        return ["Starter Kit archive missing"]
    with zipfile.ZipFile(STARTER_ZIP) as archive:
        names = set(archive.namelist())
        for source in sorted(path for path in STARTER_DIR.iterdir() if path.is_file()):
            archive_name = f"n8n-starter-kit/{source.name}"
            if archive_name not in names:
                drift.append(f"{source.name}: missing from archive")
            elif archive.read(archive_name) != source.read_bytes():
                drift.append(f"{source.name}: archive differs from source")
    return drift


def local_lite_drift() -> list[str]:
    """If present, compare the learner's extracted Lite Pack with repo ZIP."""
    if not LOCAL_LITE_DIR.exists():
        return []
    drift = []
    with zipfile.ZipFile(ZIP) as archive:
        archive_workflows = {
            Path(name).name: name
            for name in archive.namelist()
            if name.startswith("n8n-lite-pack/workflows/")
            and re.search(r"/\d{2}-.*\.json$", name)
        }
        local_files = {
            path.name: path
            for path in LOCAL_LITE_DIR.glob("workflows/[0-9][0-9]-*.json")
        }
        for missing in sorted(set(archive_workflows) - set(local_files)):
            drift.append(f"{missing}: missing from local extraction")
        for extra in sorted(set(local_files) - set(archive_workflows)):
            drift.append(f"{extra}: unexpected local workflow")
        for filename, local in sorted(local_files.items()):
            archive_name = archive_workflows.get(filename)
            if archive_name and archive.read(archive_name) != local.read_bytes():
                drift.append(f"{local.name}: local extracted file differs")
    return drift


def main() -> int:
    failures = []
    print("# Lite Pack contract check")
    print(f"source: {ZIP}")
    print("\n| # | JSON nodes | webhook contract | fan-out | model | page flags |")
    print("|---|---:|---|---|---|---|")
    with zipfile.ZipFile(ZIP) as archive:
        workflow_names = sorted(
            name for name in archive.namelist()
            if name.startswith("n8n-lite-pack/workflows/") and re.search(r"/\d{2}-.*\.json$", name)
        )
        if len(workflow_names) != 14:
            failures.append(f"expected 14 workflow JSON, found {len(workflow_names)}")
        for name in workflow_names:
            try:
                data = json.loads(archive.read(name))
            except Exception as exc:  # pragma: no cover - diagnostic path
                failures.append(f"{name}: JSON parse failed: {exc}")
                continue
            match = re.search(r"/(\d{2})-", name)
            ident = match.group(1) if match else "??"
            nodes = executable(data.get("nodes", []))
            hooks = []
            webhook_names = []
            models = set()
            for node in nodes:
                params = node.get("parameters") or {}
                if node.get("type") == "n8n-nodes-base.webhook":
                    webhook_names.append(node.get("name", ""))
                    hooks.append(
                        f"{params.get('httpMethod')} {params.get('path')} {params.get('responseMode')}"
                    )
                models.update(re.findall(r"gemini-[0-9.]+-[a-z]+", json.dumps(node, ensure_ascii=False)))
            risky = []
            if hooks and any("lastNode" in hook for hook in hooks) and reachable_fanout_from_webhook(data, webhook_names):
                risky.append("WEBHOOK+FANOUT+LASTNODE")
                failures.append(f"#{ident}: webhook fan-out uses lastNode")
            lesson = LESSONS / f"m0-workflow-{ident}-{SLUGS.get(ident, 'unknown')}.html"
            text = plain(lesson) if lesson.exists() else ""
            flags = []
            for pattern, label in (
                (r"GET\s*\+\s*POST", "GET+POST"),
                (r"Gemini 2\.5|gemini-2\.5", "Gemini2.5"),
                (r"Lite Pack v0\.9|n8n latest", "old-footer"),
                (r"3 秒|24 小時", "old-tunnel-claim"),
            ):
                if re.search(pattern, text, re.I):
                    flags.append(label)
            print(
                f"| {ident} | {len(nodes)} | {', '.join(hooks) or '-'} | "
                f"{', '.join(fanout_sources(data)) or '-'} | {', '.join(sorted(models)) or '-'} | "
                f"{', '.join(flags) or '-'} |"
            )
    overview_html = OVERVIEW.read_text(errors="ignore")
    overview = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", overview_html)).split())
    overview_flags = []
    for pattern, label in (
        (r"8 個 workflow", "overview-count-8"),
        (r"Gemini 2\.5", "overview-gemini2.5"),
    ):
        if re.search(pattern, overview, re.I):
            overview_flags.append(label)
    card01 = overview_card_text(overview_html, "m0-workflow-01-webhook.html")
    if re.search(r"外部 POST", card01, re.I):
        overview_flags.append("overview-01-post")
    card07 = overview_card_text(overview_html, "m0-workflow-07-tunnel.html")
    if re.search(r"都能 POST", card07, re.I):
        overview_flags.append("overview-07-post")
    print("\nOverview flags:", ", ".join(overview_flags) or "none")
    if overview_flags:
        failures.extend(f"overview: {flag}" for flag in overview_flags)
    drift = starter_archive_drift()
    print("Starter Kit archive:", "MATCH" if not drift else f"DRIFT ({len(drift)} files)")
    if drift:
        for item in drift:
            print("- starter-kit:", item)
        failures.extend(f"starter-kit archive: {item}" for item in drift)
    local_drift = local_lite_drift()
    if LOCAL_LITE_DIR.exists():
        print("Local Downloads Lite Pack:", "MATCH" if not local_drift else f"DRIFT ({len(local_drift)} files)")
        if local_drift:
            for item in local_drift:
                print("- local-lite:", item)
            failures.extend(f"local lite-pack: {item}" for item in local_drift)
    print("Result:", "FAIL" if failures else "PASS")
    if failures:
        print("Failures:")
        for failure in failures:
            print("-", failure)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
