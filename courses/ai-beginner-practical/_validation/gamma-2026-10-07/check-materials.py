"""Check actual Gamma lesson inputs, references, provenance and numeric baselines."""
from collections import Counter, defaultdict
from decimal import Decimal
import csv
import hashlib
import json
from pathlib import Path
import re

COURSE = Path(__file__).resolve().parents[2]
PACK = COURSE / "assets/workplace/gamma"
EVIDENCE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(name):
    with (PACK / "case-a/data" / name).open(encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def total(rows, field):
    return sum((Decimal(row[field]) for row in rows), Decimal(0))


files = sorted([*PACK.rglob("*.md"), *PACK.rglob("*.txt")])
files.append(COURSE / "PRAC2-1-LESSON-PLAN.md")
links_checked = 0
for path in files:
    text = path.read_text()
    for link in re.findall(r"\]\(([^)]+)\)", text):
        if link.startswith(("http:", "https:", "#")):
            continue
        assert (path.parent / link.split("#")[0]).exists(), (path, link)
        links_checked += 1

for case in ("case-a", "case-b"):
    proposal = (PACK / case / "proposal.md").read_text()
    assert re.findall(r"^## (P\d{2}) ", proposal, re.M) == [f"P{i:02}" for i in range(1, 11)]
    slides = (PACK / case / "gamma-text.txt").read_text()
    assert re.findall(r"^第(\d+)頁：", slides, re.M) == [str(i) for i in range(1, 11)]
    assert len(re.split(r"^---\s*$", slides, flags=re.M)) == 10
    reference = (PACK / case / "outline-reference.md").read_text()
    assert len(re.findall(r"^\| \d+ \|", reference, re.M)) == 10

sales = read_rows("sales-raw.csv")
expense = read_rows("expense-raw.csv")
assert len(sales) == 50 and total(sales, "金額(萬)") == Decimal("7705.6")
assert len(expense) == 200 and total(expense, "金額") == Decimal("3138430")
monthly = defaultdict(Decimal)
for row in sales:
    monthly[row["日期"][:7]] += Decimal(row["金額(萬)"])
assert list(sorted(monthly.values())) == [Decimal("1280.4"), Decimal("2991.0"), Decimal("3434.2")]
keys = lambda row: (row["申請人"], row["日期"], row["項目"], Decimal(row["金額"]))
counts = Counter(keys(row) for row in expense)
flagged = [row for row in expense if counts[keys(row)] > 1 or Decimal(row["金額"]) < 10]
assert {row["編號"] for row in flagged} == {"E0010", "E0130", "E0188"}
assert total(flagged, "金額") == Decimal("9601")

provenance = json.loads((COURSE / "_sources/2026-10-07-practical-expansion/provenance.json").read_text())
for item in provenance["files"]:
    assert sha(COURSE / item["snapshot"]) == item["sha256"], item
preexisting = json.loads((EVIDENCE / "preexisting-files.json").read_text())
for name, checksum in preexisting.items():
    assert sha(COURSE / name) == checksum, name

actual_inputs = {}
for case in ("case-a", "case-b"):
    sent = EVIDENCE / f"{case}-prompt-sent.txt"
    if sent.exists():
        expected = (PACK / "prompts/outline.txt").read_text() + "\n" + (PACK / case / "proposal.md").read_text()
        actual = sent.read_text()
        correction = "none"
        if case == "case-a" and "未解問题" in actual:
            # Preserve the actual input. The only post-run source change was this typo.
            assert actual.count("未解問题") == 1
            actual = actual.replace("未解問题", "未解問題")
            correction = "one documented typo: 未解問题 -> 未解問題; actual input preserved"
        assert re.sub(r"\s", "", actual) == re.sub(r"\s", "", expected), case
        actual_inputs[case] = {"match": "full source and common prompt match ignoring whitespace", "post_run_correction": correction}

report = {
    "scope": "PRAC2-1 source, actual materials and independent numeric check; no HTML or learner test",
    "result": "PASS",
    "local_links_checked": links_checked,
    "cases": 2,
    "sections_per_proposal": 10,
    "reference_pages_per_case": 10,
    "reference_slide_blocks_per_case": 10,
    "sales_rows": len(sales),
    "sales_total_wan": str(total(sales, "金額(萬)")),
    "sales_monthly_wan": {key: str(value) for key, value in sorted(monthly.items())},
    "expense_rows": len(expense),
    "expense_total_yuan": str(total(expense, "金額")),
    "review_ids": [row["編號"] for row in flagged],
    "review_total_yuan": str(total(flagged, "金額")),
    "snapshots_verified": len(provenance["files"]),
    "preexisting_changes_preserved": list(preexisting),
    "actual_full_inputs": actual_inputs,
    "source_sha256": sha(COURSE / "PRAC2-1-LESSON-PLAN.md"),
    "assets": {str(path.relative_to(COURSE)): sha(path) for path in files if path != COURSE / "PRAC2-1-LESSON-PLAN.md"},
}
(EVIDENCE / "material-checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({key: value for key, value in report.items() if key != "assets"}, ensure_ascii=False, indent=2))
