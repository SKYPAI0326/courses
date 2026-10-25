#!/usr/bin/env python3
from pathlib import Path
import re
import sys

from bs4 import BeautifulSoup


COURSE_ROOT = Path(__file__).resolve().parents[1]
ASSET_CSS = "assets/prompt-copy.css"
ASSET_JS = "assets/prompt-copy.js"
DIRECT_SELECTORS = (
    ".prompt-template",
    ".ai-prompt",
    ".wf-prompt",
    ".ub-prompt",
    ".uc-prompt",
)
PASTE_LABEL = re.compile(r"貼(?:進|入|到)")


def eligible_targets(soup):
    targets = []
    seen = set()

    def add(node):
        if node is None or node.find_parent(class_="lesson-body") is None:
            return
        identity = id(node)
        if identity not in seen:
            seen.add(identity)
            targets.append(node)

    for selector in DIRECT_SELECTORS:
        for node in soup.select(selector):
            add(node)

    for node in soup.select(".dialog-box"):
        label = node.select_one(":scope > .dialog-label")
        if label and PASTE_LABEL.search(label.get_text(" ", strip=True)):
            add(node)

    for node in soup.select(".prompt-block"):
        if "不好的修改指令" not in node.get_text(" ", strip=True):
            add(node)

    return targets


def main():
    failures = []
    page_count = 0
    target_count = 0

    for page in sorted(COURSE_ROOT.glob("*.html")):
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        targets = eligible_targets(soup)
        if not targets:
            continue

        page_count += 1
        target_count += len(targets)
        if soup.find("link", href=ASSET_CSS) is None:
            failures.append(f"{page.name}: missing {ASSET_CSS}")
        if soup.find("script", src=ASSET_JS) is None:
            failures.append(f"{page.name}: missing {ASSET_JS}")
        for index, target in enumerate(targets, start=1):
            if not target.has_attr("data-copy-prompt"):
                classes = ".".join(target.get("class", [])) or target.name
                failures.append(
                    f"{page.name}: eligible target {index} ({classes}) missing data-copy-prompt"
                )

    if not (COURSE_ROOT / ASSET_CSS).is_file():
        failures.append(f"missing shared asset: {ASSET_CSS}")
    if not (COURSE_ROOT / ASSET_JS).is_file():
        failures.append(f"missing shared asset: {ASSET_JS}")

    print(f"prompt-copy inventory: pages={page_count} targets={target_count}")
    if failures:
        for failure in failures[:80]:
            print(f"FAIL {failure}")
        if len(failures) > 80:
            print(f"... {len(failures) - 80} more failures")
        return 1

    print("PASS all eligible learner prompts have copy controls")
    return 0


if __name__ == "__main__":
    sys.exit(main())
