#!/usr/bin/env python3
"""Refresh only office-ai records in the shared site search index."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


COURSE = Path(__file__).resolve().parents[2]
BASE = COURSE.parents[1]
DOCS = BASE / "docs"
INDEX = BASE / "search-index.json"
BASELINE = COURSE / "_backup/2026-10-16-pre-growth-assistant/project/search-index.json"

sys.path.insert(0, str(DOCS))
spec = importlib.util.spec_from_file_location("build_search_index", DOCS / "build-search-index.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)

generated_path = COURSE / "_repair/2026-10-16-growth-assistant/evidence/generated-search-index.json"
module.OUT = generated_path
module.main()
generated = json.loads(generated_path.read_text(encoding="utf-8"))

current = json.loads(BASELINE.read_text(encoding="utf-8"))
new_office = [entry for entry in generated if entry.get("course") == "office-ai"]
old_indices = [i for i, entry in enumerate(current) if entry.get("course") == "office-ai"]
if not old_indices:
    raise SystemExit("office-ai has no baseline search-index insertion point")
insert_at = old_indices[0]
others = [entry for entry in current if entry.get("course") != "office-ai"]
updated = others[:insert_at] + new_office + others[insert_at:]

if [entry for entry in updated if entry.get("course") != "office-ai"] != others:
    raise SystemExit("non-office-ai entries changed")

INDEX.write_text(json.dumps(updated, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
report = {
    "old_office_ai_count": len(old_indices),
    "new_office_ai_count": len(new_office),
    "non_office_ai_count": len(others),
    "changed_urls": [
        entry["url"]
        for entry in new_office
        if entry not in [old for old in current if old.get("course") == "office-ai"]
    ],
}
(COURSE / "_repair/2026-10-16-growth-assistant/evidence/search-index-sync.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(report, ensure_ascii=False, indent=2))
