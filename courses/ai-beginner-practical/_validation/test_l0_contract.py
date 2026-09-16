#!/usr/bin/env python3
"""L0 contract test for the frozen CH4 air-conditioner teaching dataset."""

import json
import subprocess
import sys
from pathlib import Path


COURSE_DIR = Path(__file__).resolve().parents[1]
GENERATOR = COURSE_DIR / "_validation" / "L0-generate.py"
TRUTH = COURSE_DIR / "_validation" / "L0-truth-table.json"


def main() -> int:
    if not GENERATOR.exists():
        raise AssertionError("L0-generate.py must exist before the truth table can be trusted")

    subprocess.run([sys.executable, str(GENERATOR)], cwd=COURSE_DIR, check=True)
    payload = json.loads(TRUTH.read_text(encoding="utf-8"))
    dataset = payload["datasets"]["unit4-air-conditioner-comparison"]

    assert dataset["row_count"] == 2
    assert dataset["price_difference_ntd"] == 5000
    assert dataset["energy_efficiency_winner"] == "節能 B12"
    assert dataset["quietest_winner"] == "清風 A12"
    assert dataset["full_unit_warranty_winner"] == "節能 B12"
    assert dataset["shared_room_condition"] == "約 4–6 坪"
    assert dataset["missing_fields"] == ["尺寸", "安裝費", "當期促銷"]
    assert len(dataset["manual_confirmation_questions"]) == 3
    assert dataset["answer_boundary"] == "不得直接宣布哪一台一定比較好"
    print("L0 contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
