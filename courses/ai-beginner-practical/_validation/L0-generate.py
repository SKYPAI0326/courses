#!/usr/bin/env python3
"""Generate objective teaching anchors for the frozen CH4 comparison material."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path


COURSE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = COURSE_DIR / "assets" / "datasets" / "unit4-air-conditioner-comparison.md"
OUTPUT_PATH = COURSE_DIR / "_validation" / "L0-truth-table.json"
TEXT_OUTPUT_PATH = COURSE_DIR / "_validation" / "L0-air-conditioner-truth.txt"


def parse_table(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    table_lines = [line for line in lines if line.strip().startswith("|")]
    if len(table_lines) < 3:
        raise ValueError(f"No complete Markdown table found in {path}")

    def cells(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    headers = cells(table_lines[0])
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        values = cells(line)
        if len(values) != len(headers):
            raise ValueError(f"Table row has {len(values)} cells; expected {len(headers)}")
        rows.append(dict(zip(headers, values)))
    return headers, rows


def nt_dollars(value: str) -> int:
    match = re.search(r"\d[\d,]*", value)
    if not match:
        raise ValueError(f"No numeric price found in {value!r}")
    return int(match.group(0).replace(",", ""))


def number(value: str) -> float:
    match = re.search(r"\d+(?:\.\d+)?", value)
    if not match:
        raise ValueError(f"No numeric value found in {value!r}")
    return float(match.group(0))


def full_unit_years(value: str) -> int:
    match = re.search(r"全機\s*(\d+)\s*年", value)
    if not match:
        raise ValueError(f"No full-unit warranty found in {value!r}")
    return int(match.group(1))


def build_truth() -> dict:
    table_headers, table_rows = parse_table(DATASET_PATH)
    products = table_headers[1:]
    headers = ["欄位"] + [row["欄位"] for row in table_rows]
    rows = [
        {
            "欄位": product,
            **{row["欄位"]: row[product] for row in table_rows},
        }
        for product in products
    ]
    if products != ["清風 A12", "節能 B12"]:
        raise ValueError(f"Unexpected product order: {products}")

    prices = {row["欄位"]: nt_dollars(row["練習價格"]) for row in rows}
    efficiency = {row["欄位"]: number(row["能源效率"]) for row in rows}
    noise = {row["欄位"]: number(row["噪音"]) for row in rows}
    warranty = {row["欄位"]: full_unit_years(row["保固"]) for row in rows}
    missing_fields = [
        header for header in headers[1:] if all(row[header] == "未提供" for row in rows)
    ]
    room_conditions = {row["建議房間條件（素材提供）"] for row in rows}

    dataset = {
        "source_path": str(DATASET_PATH.relative_to(COURSE_DIR)),
        "source_sha256": hashlib.sha256(DATASET_PATH.read_bytes()).hexdigest(),
        "row_count": len(rows),
        "products": products,
        "prices_ntd": prices,
        "price_difference_ntd": abs(prices[products[1]] - prices[products[0]]),
        "energy_efficiency_cspf": efficiency,
        "energy_efficiency_winner": max(efficiency, key=efficiency.get),
        "noise_db": noise,
        "quietest_winner": min(noise, key=noise.get),
        "full_unit_warranty_years": warranty,
        "full_unit_warranty_winner": max(warranty, key=warranty.get),
        "shared_room_condition": next(iter(room_conditions)) if len(room_conditions) == 1 else None,
        "missing_fields": missing_fields,
        "manual_confirmation_questions": [
            "實際安裝尺寸與室內外機位置是否符合？",
            "安裝費、搬運費與其他施工費是多少？",
            "當期價格、促銷與保固條件是否仍有效？",
        ],
        "answer_boundary": "不得直接宣布哪一台一定比較好",
    }
    return {
        "generated_at": date.today().isoformat(),
        "datasets": {"unit4-air-conditioner-comparison": dataset},
    }


def write_outputs(payload: dict) -> None:
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    dataset = payload["datasets"]["unit4-air-conditioner-comparison"]
    lines = [
        "L0 Truth Table｜CH4 冷氣比較共同素材",
        f"來源：{dataset['source_path']}",
        f"來源 SHA-256：{dataset['source_sha256']}",
        f"產品列數：{dataset['row_count']}",
        f"價格：{dataset['prices_ntd']}",
        f"價格差：NT$ {dataset['price_difference_ntd']:,}",
        f"能源效率較高：{dataset['energy_efficiency_winner']}",
        f"室內噪音較低：{dataset['quietest_winner']}",
        f"全機保固較長：{dataset['full_unit_warranty_winner']}",
        f"共同房間條件：{dataset['shared_room_condition']}",
        f"資料未提供欄位：{'、'.join(dataset['missing_fields'])}",
        "人工確認問題：",
    ]
    lines.extend(f"{index}. {question}" for index, question in enumerate(dataset["manual_confirmation_questions"], 1))
    lines.append(f"回答界線：{dataset['answer_boundary']}")
    TEXT_OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    truth = build_truth()
    write_outputs(truth)
    print(json.dumps(truth["datasets"]["unit4-air-conditioner-comparison"], ensure_ascii=False, indent=2))
    print(f"\nWrote {OUTPUT_PATH}")
    print(f"Wrote {TEXT_OUTPUT_PATH}")
