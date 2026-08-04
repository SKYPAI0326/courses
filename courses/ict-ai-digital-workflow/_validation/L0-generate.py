#!/usr/bin/env python3
import csv
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def amount(value):
    cleaned = re.sub(r"[^0-9.-]", "", value)
    return int(float(cleaned))


def summarize(relative_path):
    path = ROOT / relative_path
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    values = [amount(row["金額"]) for row in rows]
    pending = [
        row["項目"] for row in rows
        if row.get("狀態") == "待確認"
        or ("報價來源" in row and (not row.get("報價來源") or not row.get("報價日期")))
    ]
    formatted = [row["項目"] for row in rows if row["金額"].strip() != str(amount(row["金額"]))]
    result = {
        "path": str(relative_path),
        "total_rows": len(rows),
        "clean_total": sum(values),
        "max_item": rows[values.index(max(values))]["項目"],
        "max_amount": max(values),
        "pending_count": len(pending),
        "pending_items": pending,
        "formatted_amount_items": formatted,
    }
    if relative_path == Path("assets/CH5/cost-data.csv"):
        confirmed = [
            amount(row["金額"]) for row in rows
            if row.get("報價來源") and row.get("報價日期")
        ]
        result["confirmed_subtotal"] = sum(confirmed)
        result["budget_limit"] = 18000
        result["over_budget_amount"] = sum(values) - 18000
    return result


truth = {
    "generated_at": date.today().isoformat(),
    "datasets": {
        "ch3_budget": summarize(Path("assets/CH3/budget-raw.csv")),
        "ch5_capstone_cost": summarize(Path("assets/CH5/cost-data.csv")),
    },
    "content_anchors": {
        "unsupported_claims_in_fixed_ai_output": ["現場銷售提升 30%", "10 月第 3 個週末"],
        "source_b_status": "待確認或排除",
    },
}

output = ROOT / "_validation/L0-truth-table.json"
output.write_text(json.dumps(truth, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

for name, dataset in truth["datasets"].items():
    print(f"{name}: rows={dataset['total_rows']} total={dataset['clean_total']} pending={dataset['pending_count']}")
print(f"written: {output}")
