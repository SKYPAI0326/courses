#!/usr/bin/env python3
"""Regression tests for active return actions and explicit edge states."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "_tools"
for path in (TOOLS,):
    sys.path.insert(0, str(path))

SPEC = importlib.util.spec_from_file_location(
    "repair_navigation_actions", TOOLS / "repair-navigation-actions.py"
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_return_action_is_moved_and_restored() -> None:
    current = (
        '<html><head></head><body><main>'
        '<div class="nav-footer">'
        '<a href="CH5.html" class="nav-btn nav-prev" data-nav-role="prev">← 上一單元</a>'
        '<a class="nav-btn primary nav-next nav-disabled" data-nav-role="next" '
        'aria-disabled="true" tabindex="-1" data-nav-state="disabled">'
        '返回課程總覽 <span aria-hidden="true">→</span></a>'
        '</div></main></body></html>'
    )
    original = (
        '<html><head></head><body><main>'
        '<div class="nav-footer">'
        '<a href="CH5.html" class="nav-btn nav-prev">← 上一單元</a>'
        '<a href="index.html" class="nav-btn primary nav-next">'
        '返回課程總覽 <span aria-hidden="true">→</span></a>'
        '</div></main></body></html>'
    )
    page = ROOT / "admin-ai-assistant" / "CH6.html"
    result, changed, unresolved = MODULE.repair_page_html(current, original, page)

    assert changed >= 1
    assert unresolved == 0
    assert 'data-nav-role="return"' in result
    assert 'href="index.html"' in result
    assert 'data-nav-state="disabled"' not in result
    assert result.count('data-nav-role="prev"') == 1
    assert result.count('data-nav-role="return"') == 1
    assert '返回課程總覽' in result


def test_edge_state_is_not_an_anchor() -> None:
    current = (
        '<html><head></head><body><main><div class="nav-footer">'
        '<a class="nav-btn nav-prev nav-disabled" data-nav-role="prev" '
        'aria-disabled="true" tabindex="-1" data-nav-state="disabled">'
        '← 本單元是第一個</a>'
        '<a href="CH1-2.html" class="nav-btn primary nav-next" data-nav-role="next">下一單元 →</a>'
        '</div></main></body></html>'
    )
    original = (
        '<html><head></head><body><main><div class="nav-footer">'
        '<a href="#" class="nav-btn nav-prev">← 本單元是第一個</a>'
        '<a href="CH1-2.html" class="nav-btn primary nav-next">下一單元 →</a>'
        '</div></main></body></html>'
    )
    page = ROOT / "gen-image" / "CH1-1.html"
    result, changed, unresolved = MODULE.repair_page_html(current, original, page)

    assert changed >= 1
    assert unresolved == 0
    assert 'data-nav-state="disabled"' in result
    assert '<span class="nav-btn nav-prev nav-disabled"' in result
    assert '<a class="nav-btn nav-prev nav-disabled"' not in result


def test_composite_return_text_is_split_without_text_loss() -> None:
    current = (
        '<html><head></head><body><main>'
        '<div class="nav-return" role="navigation" aria-label="返回課程導覽">'
        '<a class="nav-btn nav-return-link" aria-label="完成 Part 3 返回課程總覽" '
        'data-nav-role="return" href="index.html">完成 Part 3 →返回課程總覽</a>'
        '</div></main></body></html>'
    )
    original = current
    page = ROOT / "gen-ai-36h" / "part3" / "PRAC3.html"
    result, changed, unresolved = MODULE.repair_page_html(current, original, page)

    assert changed >= 1
    assert unresolved == 0
    assert 'class="nav-return-note">完成 Part 3 ' in result
    assert 'data-nav-role="return"' in result
    assert 'aria-hidden="true">→</span>返回課程總覽' in result
    assert '完成 Part 3' in result


if __name__ == "__main__":
    test_return_action_is_moved_and_restored()
    test_edge_state_is_not_an_anchor()
    test_composite_return_text_is_split_without_text_loss()
    print("PASS: navigation action repair preserves return text and edge semantics")
