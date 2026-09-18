#!/usr/bin/env python3
"""Contract test for course navigation and first-action discoverability."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LESSONS = ("CH1-1.html", "CH2-1.html", "CH3-1.html", "CH4-1.html")
ANCHORS = ("lesson-start", "lesson-demo", "lesson-practice", "lesson-check", "lesson-assets", "lesson-quiz")


def assert_all(text: str, needles: tuple[str, ...], label: str) -> None:
    missing = [needle for needle in needles if needle not in text]
    assert not missing, f"{label} missing: {', '.join(missing)}"


def main() -> None:
    css = (ROOT / "assets/layout-redesign.css").read_text(encoding="utf-8")
    assert_all(
        css,
        (".lesson-quicknav", ".lesson-start", ".module-quicknav", ".module-start", ".hero-actions", "overflow-x: auto"),
        "shared layout hooks",
    )
    for name in LESSONS:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert 'class="lesson-quicknav"' in text, f"{name} needs a page quick navigation"
        assert 'class="lesson-start"' in text, f"{name} needs a first-action card"
        assert 'class="body-text completion-line"' in text, f"{name} needs a visible core completion line"
        assert_all(text, tuple(f'id="{anchor}"' for anchor in ANCHORS), name)
        assert_all(text, tuple(f'href="#{anchor}"' for anchor in ANCHORS), f"{name} quicknav targets")

    ch1 = (ROOT / "CH1-1.html").read_text(encoding="utf-8")
    assert 'href="#practice-workbench"' in ch1, "CH1-1 first action needs to open the embedded workbench"
    assert 'data-action="export"' in ch1, "CH1-1 workbench needs an export action"
    assert 'data-action="print"' in ch1, "CH1-1 workbench needs a print action"

    for name, anchor in (("CH2-1.html", "communication-workbench"), ("CH3-1.html", "notebooklm-log"), ("CH4-1.html", "lifestyle-workbench")):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert f'href="#{anchor}"' in text, f"{name} first action needs to open its workbench"
        assert 'data-action="export"' in text, f"{name} workbench needs an export action"
        assert 'data-action="print"' in text, f"{name} workbench needs a print action"

    module = (ROOT / "module1.html").read_text(encoding="utf-8")
    assert 'class="module-quicknav"' in module
    assert 'class="module-start"' in module
    assert module.count('class="completion-line"') >= 3, "module needs visible completion lines"
    assert_all(module, tuple(f'id="{anchor}"' for anchor in ("ch1-1", "ch2-1", "ch3-1", "ch4-1", "course-capstone")), "module anchors")

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'class="hero-actions"' in index, "index needs an explicit starting CTA"
    assert 'href="CH1-1.html"' in index
    print("UI/practicality contract: PASS")


if __name__ == "__main__":
    main()
