#!/usr/bin/env python3
"""Ensure the four units keep distinct learning outputs after de-duplication."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(text: str, needle: str, label: str) -> None:
    assert needle in text, f"{label} missing: {needle}"


def main() -> None:
    ch1 = (ROOT / "CH1-1.html").read_text(encoding="utf-8")
    require(ch1, "U1-GAP", "CH1 gap comparison")
    require(ch1, 'data-field="personalNeed"', "CH1 personal task card")
    require(ch1, "個人任務卡", "CH1 personal task card")
    for old in ("personalFuzzy", "personalChange", "personalInstruction", "personalBetter", "U1-REVISE"):
        assert old not in ch1, f"CH1 still contains retired workflow key: {old}"

    ch2 = (ROOT / "CH2-1.html").read_text(encoding="utf-8")
    require(ch2, "U2-AUDIENCE", "CH2 reader conversion")
    require(ch2, "讀者轉換", "CH2 reader conversion")
    require(ch2, "原讀者、新讀者", "CH2 comparison evidence")
    assert "U2-ITERATE" not in ch2, "CH2 still uses retired generic iteration stage"

    ch3 = (ROOT / "CH3-1.html").read_text(encoding="utf-8")
    for needle in ("newsTwo", "newsThree", "主張與證據狀態台帳", "步驟 1", "跨來源比較"):
        require(ch3, needle, "CH3 evidence workflow")
    for old in ("news200", "news350", "新聞三段式摘要"):
        assert old not in ch3, f"CH3 still contains retired summary workflow: {old}"

    ch4 = (ROOT / "CH4-1.html").read_text(encoding="utf-8")
    for needle in ("條件敏感性", "方案取捨", "缺資料", "U4-TRADEOFF"):
        require(ch4, needle, "CH4 decision workflow")

    assets = (ROOT / "assets/worksheets/course-capstone-handoff.md").read_text(encoding="utf-8")
    for needle in ("缺口或取捨的判讀", "方案比較、取捨、缺資料與下一步", "人工確認位置"):
        require(assets, needle, "capstone handoff")

    pdf_tool = (ROOT / "_tools/build-pdfs.js").read_text(encoding="utf-8")
    for needle in ("缺條件比較", "主張台帳", "方案取捨"):
        require(pdf_tool, needle, "PDF source")

    print("full course repartition contract: PASS")


if __name__ == "__main__":
    main()
