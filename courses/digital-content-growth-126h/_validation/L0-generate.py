#!/usr/bin/env python3
"""Generate the course-specific truth table used by release validation."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


COURSE_DIR = Path(__file__).resolve().parents[1]
VALIDATION_DIR = COURSE_DIR / "_validation"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_truth(path: Path) -> dict[str, object]:
    rows = read_csv(path)
    headers = list(rows[0]) if rows else []
    status_values = sorted({row.get("source_status", "") for row in rows})
    return {
        "path": str(path.relative_to(COURSE_DIR)),
        "rows": len(rows),
        "headers": headers,
        "source_status_values": status_values,
        "all_rows_marked_synthetic": bool(rows) and status_values == ["synthetic"],
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    markdown_assets = sorted((COURSE_DIR / "assets" / "templates").glob("*.md"))
    html_assets = sorted((COURSE_DIR / "assets" / "templates").glob("*.html"))
    missing_html = [p.name for p in markdown_assets if not p.with_suffix(".html").exists()]
    learner_pages = sorted(COURSE_DIR.glob("*.html"))
    unit_pages = sorted(COURSE_DIR.glob("CH*.html")) + sorted(COURSE_DIR.glob("PRAC*.html"))

    datasets = {
        path.stem: csv_truth(path)
        for path in sorted((COURSE_DIR / "assets" / "datasets").glob("*.csv"))
    }

    truth = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "course": "digital-content-growth-126h",
        "pages": {
            "learner_html": len(learner_pages),
            "unit_html": len(unit_pages),
            "unit_ids": [p.stem for p in unit_pages],
        },
        "assets": {
            "markdown_templates": len(markdown_assets),
            "html_templates": len(html_assets),
            "markdown_without_html": missing_html,
            "learner_asset_format": "html-first",
        },
        "datasets": datasets,
        "source_hashes": {
            "outline": sha256(COURSE_DIR.parent.parent / "_outlines" / "digital-content-growth-126h.md"),
        },
    }

    output = VALIDATION_DIR / "L0-truth-table.json"
    output.write_text(json.dumps(truth, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("═══ L0 Truth Table ═══")
    print(f"unit pages: {truth['pages']['unit_html']}")
    print(f"learner pages: {truth['pages']['learner_html']}")
    print(f"markdown/html asset pairs missing: {len(missing_html)}")
    for name, info in datasets.items():
        print(f"{name}: rows={info['rows']} synthetic={info['all_rows_marked_synthetic']}")
    print(f"✓ wrote {output}")


if __name__ == "__main__":
    main()
