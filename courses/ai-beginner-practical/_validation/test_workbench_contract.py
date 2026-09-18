#!/usr/bin/env python3
"""Contract test for the CH1-1 learner-facing web workbench."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "CH1-1.html"


def require(text: str, needle: str, label: str) -> None:
    assert needle in text, f"{label} missing: {needle}"


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")

    for needle in (
        'href="#practice-workbench"',
        'id="practice-workbench"',
        'id="unit1-workbench"',
        'data-field="name"',
        'data-field="date"',
        'data-action="save"',
        'data-action="export"',
        'data-action="print"',
        'data-action="reset"',
        "localStorage",
        "unit1-practice-sheet-complete.md",
        "window.print()",
        "複製提示詞",
    ):
        require(text, needle, "CH1-1 workbench")

    for question in range(1, 6):
        require(text, f'id="wb-prompt-q{question}"', f"CH1-1 question {question}")
        require(text, f'data-field="q{question}Response"', f"CH1-1 question {question}")

    for field in (
        "revisionTarget",
        "revisionProblem",
        "revisionOriginal",
        "revisionInstruction",
        "revisionResponse",
        "revisionKept",
        "personalFuzzy",
        "personalSituation",
        "personalTask",
        "personalData",
        "personalConditions",
        "personalFormat",
        "personalPrompt",
        "personalChange",
        "personalInstruction",
        "personalBetter",
    ):
        require(text, f'data-field="{field}"', f"CH1-1 {field}")

    for check in range(1, 7):
        require(text, f'data-field="check{check}"', f"CH1-1 completion check {check}")

    assert 'href="assets/worksheets/unit1-practice-sheet.md"' in text, "offline worksheet must remain available"
    assert "全選複製到自己的純文字／Markdown 編輯器" not in text, "old copy-out workflow must not be the main path"
    print("workbench contract: PASS")


if __name__ == "__main__":
    main()
