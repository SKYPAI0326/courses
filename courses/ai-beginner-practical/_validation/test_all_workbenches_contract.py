#!/usr/bin/env python3
"""Static contract test for the learner-facing workbenches in CH2–CH4."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(text: str, needle: str, label: str) -> None:
    assert needle in text, f"{label} missing: {needle}"


def check_common(text: str, label: str, anchor: str, filename: str) -> None:
    for needle in (
        f'href="#{anchor}"',
        f'id="{anchor}"',
        'data-workbench-form',
        'data-action="save"',
        'data-action="export"',
        'data-action="print"',
        'data-action="reset"',
        'assets/learner-workbench.css',
        'assets/learner-workbench.js',
        filename,
        'localStorage',
    ):
        require(text, needle, label)


def check_fields(text: str, fields: tuple[str, ...], label: str) -> None:
    for field in fields:
        require(text, f'data-field="{field}"', label)


def main() -> None:
    ch2 = (ROOT / "CH2-1.html").read_text(encoding="utf-8")
    check_common(ch2, "CH2-1 communication workbench", "communication-workbench", "unit2-communication-pack-complete.md")
    check_fields(
        ch2,
        (
            "emailScenario", "emailPrompt", "emailFirst", "messageScenario", "messagePrompt", "messageFirst",
            "introData", "introSocial", "introDating", "introInterview", "revisionInstruction", "revisionSecond",
        ),
        "CH2-1 communication workbench",
    )

    ch3 = (ROOT / "CH3-1.html").read_text(encoding="utf-8")
    check_common(ch3, "CH3-1 NotebookLM companion log", "notebooklm-log", "unit3-notebooklm-reading-pack-complete.md")
    check_fields(
        ch3,
        (
            "notebook", "sourceNews", "sourceNotice", "sourceBook", "sourceStatus", "sourceCheck1",
            "newsPrompt", "newsOne", "news200", "news350", "newsCitations", "noticeImpact", "noticeDeadline",
            "noticeNext", "bookPoints", "bookActions", "check6",
        ),
        "CH3-1 NotebookLM companion log",
    )
    require(ch3, "不會自動讀取 NotebookLM", "CH3-1 boundary")
    require(ch3, "notebooklm.google.com", "CH3-1 platform")

    ch4 = (ROOT / "CH4-1.html").read_text(encoding="utf-8")
    check_common(ch4, "CH4-1 lifestyle workbench", "lifestyle-workbench", "unit4-lifestyle-application-card.md")
    check_fields(
        ch4,
        (
            "card", "goal", "time", "budget", "preferences", "limits", "original", "background", "task",
            "constraints", "format", "fullPrompt", "firstAnswer", "conditionCheck", "revisionInstruction",
            "revisedAnswer", "comparison", "next", "check1",
        ),
        "CH4-1 lifestyle workbench",
    )

    for name, text in (("CH2-1", ch2), ("CH3-1", ch3), ("CH4-1", ch4)):
        assert "全選複製到自己的文字／Markdown 編輯器" not in text, f"{name} still presents copy-out as main path"
        assert "複製到自己的文字筆記並另存為" not in text, f"{name} still presents text-note setup as main path"

    print("all workbenches contract: PASS")


if __name__ == "__main__":
    main()
