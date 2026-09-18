#!/usr/bin/env python3
"""Regression checks for the post-dedup learning identities of CH3 and CH4."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(text: str, needle: str, label: str) -> None:
    assert needle in text, f"{label} missing: {needle}"


def main() -> None:
    ch3 = (ROOT / "CH3-1.html").read_text(encoding="utf-8")
    for needle in (
        "來源地圖",
        "主張與證據狀態台帳",
        "U3-CLAIM",
        "支持／部分支持／來源未提及",
        "U3-COMPARE",
        "跨來源比較",
        "書籍三層筆記",
    ):
        require(ch3, needle, "CH3 post-dedup identity")
    assert "沿用查證規格，只替換來源與完成物" not in ch3
    assert "新聞三段式摘要與引用" not in ch3

    ch4 = (ROOT / "CH4-1.html").read_text(encoding="utf-8")
    for needle in (
        "選擇標準與優先順序",
        "U4-FRAME",
        "U4-TRADEOFF",
        "U4-MISSING",
        "U4-BOUNDARY",
        "缺資料",
        "方案取捨",
        "生活決策卡",
    ):
        require(ch4, needle, "CH4 post-dedup identity")
    assert "五個欄位，讓範本變成自己的任務" not in ch4
    assert "個人生活應用工作台" not in ch4

    for plan, terms in {
        "CH3-1-LESSON-PLAN.md": ("主張／引用／證據狀態台帳", "U3-COMPARE", "跨來源"),
        "CH4-1-LESSON-PLAN.md": ("選擇標準", "取捨矩陣", "U4-MISSING"),
    }.items():
        text = (ROOT / plan).read_text(encoding="utf-8")
        for term in terms:
            require(text, term, plan)

    print("post-dedup learning contract: PASS")


if __name__ == "__main__":
    main()
