#!/usr/bin/env python3
"""Regression contract for the simulated-learner repair batch."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LESSONS = ("CH1-1.html", "CH2-1.html", "CH3-1.html", "CH4-1.html")
LLM_STARTER = "assets/fallback/text-llm-minimum-start.md"


def require(text: str, needle: str, label: str) -> None:
    assert needle in text, f"{label} missing: {needle}"


def main() -> None:
    assert (ROOT / LLM_STARTER).exists(), "generic LLM starter asset missing"
    starter = (ROOT / LLM_STARTER).read_text(encoding="utf-8")
    for needle in ("任一可合法使用的文字型 LLM", "自學者", "取得路徑"):
        require(starter, needle, "generic LLM starter")

    for name in ("index.html", "module1.html", *LESSONS):
        text = (ROOT / name).read_text(encoding="utf-8")
        require(text, "課程提供者", name)

    for name in ("CH1-1.html", "CH2-1.html", "CH4-1.html"):
        text = (ROOT / name).read_text(encoding="utf-8")
        require(text, "environment-contract", name)
        require(text, LLM_STARTER, name)

    ch3 = (ROOT / "CH3-1.html").read_text(encoding="utf-8")
    require(ch3, "environment-contract", "CH3-1.html")
    require(ch3, "NotebookLM 實機準備", "CH3-1.html")

    ch1 = (ROOT / "CH1-1.html").read_text(encoding="utf-8")
    require(ch1, "修訂後完整輸出", "CH1-1.html")
    require(ch1, "只改變呈現格式", "CH1-1.html")

    ch2 = (ROOT / "CH2-1.html").read_text(encoding="utf-8")
    require(ch2, "完整訊息示範", "CH2-1.html")
    require(ch2, "三版自我介紹示範", "CH2-1.html")
    require(ch2, "LINE／短訊息", "CH2-1.html")

    ch4 = (ROOT / "CH4-1.html").read_text(encoding="utf-8")
    require(ch4, "完整冷氣比較表", "CH4-1.html")
    require(ch4, "完整四天修正版", "CH4-1.html")
    require(ch4, "module1.html#course-capstone", "CH4-1.html")

    fallback = (ROOT / "assets/fallback/unit3-notebooklm-text-fallback.md").read_text(encoding="utf-8")
    require(fallback, "約 300–350 字", "unit3 fallback")
    assert "約 500 字" not in fallback, "unit3 fallback keeps conflicting 500-word requirement"

    capstone = (ROOT / "assets/worksheets/course-capstone-handoff.md").read_text(encoding="utf-8")
    for needle in ("CH1-1 完成物", "CH2-1 完成物", "CH3-1 完成物", "CH4-1 完成物", "回修位置", "工具不可用"):
        require(capstone, needle, "course capstone")

    print("cold-follow contract: PASS")


if __name__ == "__main__":
    main()
