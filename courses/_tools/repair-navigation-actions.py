#!/usr/bin/env python3
"""Move return actions out of the previous/next slots without changing prose."""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from html import escape, unescape
from pathlib import Path


_NAV_SPEC = importlib.util.spec_from_file_location(
    "normalize_navigation", Path(__file__).with_name("normalize-navigation.py")
)
assert _NAV_SPEC is not None and _NAV_SPEC.loader is not None
nav = importlib.util.module_from_spec(_NAV_SPEC)
sys.modules[_NAV_SPEC.name] = nav
_NAV_SPEC.loader.exec_module(nav)


ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "_backup" / "2026-09-21-pre-navigation"

RETURN_WORDS = re.compile(
    r"返回|回到|回課程|課程(?:總覽|首頁|目錄)|首頁|目錄|Module\s*\d+\s*總覽|Part\s*\d+\s*總覽",
    flags=re.I,
)

NAVIGATION_STYLE = """<style id="navigation-action-fix">
.nav-return{max-width:var(--content-w,780px);margin:0 auto;padding:0 48px 16px;display:flex;justify-content:center}
.nav-return{align-items:center;gap:10px;flex-wrap:wrap}
.nav-return-note{font-size:.82rem;color:var(--c-muted,#7a766d);line-height:1.7}
.nav-return-link{font-size:.82rem!important;color:var(--c-muted,#7a766d)!important;background:transparent!important;border-color:var(--c-border,#d8d4cb)!important}
.nav-return-link:hover{color:var(--c-main,#6f624f)!important;background:var(--c-surface,#edeae3)!important;border-color:var(--c-main,#6f624f)!important}
.nav-disabled{color:var(--c-faint,#bcb8ae)!important;background:transparent!important;border-color:var(--c-border-soft,#e8e4da)!important;cursor:not-allowed;opacity:.8}
.nav-disabled:hover{color:var(--c-faint,#bcb8ae)!important;background:transparent!important;border-color:var(--c-border-soft,#e8e4da)!important}
@media(max-width:768px){.nav-return{padding-left:20px;padding-right:20px}}
@media(max-width:600px){.nav-return{padding-left:24px;padding-right:24px}}
</style>"""

NAVIGATION_STYLE_EXTRA = """.nav-return{align-items:center;gap:10px;flex-wrap:wrap}
.nav-return-note{font-size:.82rem;color:var(--c-muted,#7a766d);line-height:1.7}
"""


def visible_text(anchor: str) -> str:
    return " ".join(unescape(re.sub(r"<[^>]+>", "", anchor)).split())


RETURN_MARKER = re.compile(
    r"(?:"
    r"返回\s*(?:課程(?:總覽|目錄|首頁|單元)|Module\s*\d+(?:\s*總覽)?|Part\s*\d+\s*總覽|總覽|總結)|"
    r"回到\s*(?:起點)?(?:課程(?:總覽|目錄|首頁)|總覽)|"
    r"回課程(?:總覽|目錄|首頁)|回首頁|"
    r"課程(?:總覽|目錄)|返回總覽|回到總覽"
    r")",
    flags=re.I,
)


def render_text(text: str) -> str:
    """Escape visible text while keeping arrows decorative for screen readers."""
    pieces: list[str] = []
    cursor = 0
    for match in re.finditer(r"[←→]", text):
        pieces.append(escape(text[cursor : match.start()]))
        pieces.append(f'<span aria-hidden="true">{match.group(0)}</span>')
        cursor = match.end()
    pieces.append(escape(text[cursor:]))
    return "".join(pieces)


def split_return_text(text: str) -> tuple[str, str, str] | None:
    """Return prefix, actionable return text, and suffix for composite labels."""
    match = RETURN_MARKER.search(text)
    if not match:
        return None
    action_start = match.start()
    action_end = match.end()
    trailing_arrow = re.match(r"\s*→", text[action_end:])
    if trailing_arrow:
        action_end += trailing_arrow.end()

    prefix_candidate = text[:action_start]
    suffix = text[action_end:]
    has_completion_prefix = bool(re.search(r"完成|完課|課程完結", prefix_candidate))
    if not has_completion_prefix and not suffix:
        return None

    # Keep a preceding arrow with the return action, e.g. "完成 Part 3 →返回".
    arrow = max(prefix_candidate.rfind("→"), prefix_candidate.rfind("←"))
    if arrow >= 0 and not prefix_candidate[arrow + 1 :].strip():
        action_start = arrow

    prefix = text[:action_start]
    action = text[action_start:action_end]
    return prefix, action, suffix


def replace_anchor_content(anchor: str, text: str) -> str:
    tag = opening_tag(anchor)
    tag = nav.add_class(tag, "nav-return-link")
    tag = nav.set_attribute(tag, "data-nav-role", "return")
    tag = nav.set_attribute(tag, "aria-label", text.replace("←", "").replace("→", "").strip())
    return tag + render_text(text) + "</a>"


def split_return_block(block: str) -> tuple[str, bool]:
    anchor_match = re.search(r"<a\b[^>]*>.*?</a>", block, flags=re.I | re.S)
    if not anchor_match or "nav-return-note" in block:
        return block, False
    anchor = anchor_match.group(0)
    split = split_return_text(visible_text(anchor))
    if split is None:
        return block, False
    prefix, action, suffix = split
    children: list[str] = []
    if prefix:
        children.append(f'<span class="nav-return-note">{render_text(prefix)}</span>')
    children.append(replace_anchor_content(anchor, action))
    if suffix:
        children.append(f'<span class="nav-return-note">{render_text(suffix)}</span>')
    # Keep the original text sequence exact. The flex gap in `.nav-return`
    # supplies visual separation without inserting a new text-space node.
    replacement = (
        anchor_match.string[: anchor_match.start()]
        + "".join(children)
        + anchor_match.string[anchor_match.end() :]
    )
    return replacement, True


def compact_split_return_block(block: str) -> tuple[str, bool]:
    """Remove inter-child whitespace introduced by an earlier split pass."""
    if "nav-return-note" not in block:
        return block, False
    compacted = re.sub(
        r"</(?:a|span)>\s+(?=<(?:a\b|span\s+class=[\"']nav-return-note\b))",
        lambda match: match.group(0).split(">", 1)[0] + ">",
        block,
        flags=re.I,
    )
    return compacted, compacted != block


def refresh_split_return_blocks(html: str, original: str) -> tuple[str, int]:
    """Rebuild split blocks from the original anchor to recover exact spacing."""
    originals = original_nav_anchors_from_html(original)
    count = 0
    result = html
    for open_start, _, _, close_end in reversed(nav._nav_container_spans(html)):
        opening = html[open_start : html.find(">", open_start) + 1]
        if not re.search(r"\bclass\s*=\s*[\"'][^\"']*\bnav-return\b", opening, re.I):
            continue
        block = result[open_start:close_end]
        if "nav-return-note" not in block:
            continue
        current_text = re.sub(r"\s+", "", visible_text(block))
        candidates = [
            anchor
            for anchor in originals
            if re.sub(r"\s+", "", visible_text(anchor)) == current_text
        ]
        if not candidates:
            continue
        anchor_match = re.search(r"<a\b[^>]*>.*?</a>", block, flags=re.I | re.S)
        if not anchor_match:
            continue
        opening_match = re.match(r"<[a-z][^>]*>", block, flags=re.I | re.S)
        closing_match = re.search(r"</([a-z][\w:-]*)>\s*$", block, flags=re.I | re.S)
        if not opening_match or not closing_match:
            continue
        synthetic = (
            block[: opening_match.end()]
            + candidates[0]
            + f"</{closing_match.group(1)}>"
        )
        replacement, changed = split_return_block(synthetic)
        if changed:
            count += 1
            result = result[:open_start] + replacement + result[close_end:]
    return result, count


def split_return_actions(html: str) -> tuple[str, int]:
    count = 0
    result = html
    for open_start, open_end, close_start, close_end in reversed(nav._nav_container_spans(html)):
        opening = html[open_start:open_end]
        if not re.search(r"\bclass\s*=\s*[\"'][^\"']*\bnav-return\b", opening, flags=re.I):
            continue
        block = result[open_start:close_end]
        replacement, changed = split_return_block(block)
        compacted, compacted_changed = compact_split_return_block(replacement)
        replacement = compacted
        changed = changed or compacted_changed
        if changed:
            count += 1
            result = result[:open_start] + replacement + result[close_end:]
    return result, count


def ensure_navigation_style(html: str) -> tuple[str, bool]:
    if not re.search(r"\bnav-return\b|\bnav-disabled\b", html):
        return html, False
    style_pattern = re.compile(
        r"(<style\b[^>]*\bid\s*=\s*[\"']navigation-action-fix[\"'][^>]*>)(.*?)(</style>)",
        flags=re.I | re.S,
    )
    match = style_pattern.search(html)
    if match:
        if ".nav-return-note" in match.group(2):
            return html, False
        updated = match.group(1) + match.group(2) + NAVIGATION_STYLE_EXTRA + match.group(3)
        return html[: match.start()] + updated + html[match.end() :], True
    head = re.search(r"</head>", html, flags=re.I)
    if not head:
        return html, False
    return html[: head.start()] + NAVIGATION_STYLE + "\n" + html[head.start() :], True


def opening_tag(anchor: str) -> str:
    match = re.match(r"<a\b[^>]*>", anchor, flags=re.I | re.S)
    if not match:
        raise ValueError(f"not an anchor: {anchor[:80]}")
    return match.group(0)


def replace_closing_tag(anchor: str, tag: str) -> str:
    return re.sub(r"</a>\s*$", f"</{tag}>", anchor, count=1, flags=re.I)


def remove_class(tag: str, class_name: str) -> str:
    match = re.search(r"(\bclass\s*=\s*)([\"'])(.*?)\2", tag, flags=re.I | re.S)
    if not match:
        return tag
    classes = [item for item in match.group(3).split() if item != class_name]
    if classes:
        replacement = f"{match.group(1)}{match.group(2)}{' '.join(classes)}{match.group(2)}"
        return tag[: match.start()] + replacement + tag[match.end() :]
    return re.sub(r"\s+class\s*=\s*([\"']).*?\1", "", tag, count=1, flags=re.I | re.S)


def make_return_anchor(anchor: str, href: str) -> str:
    original_tag = opening_tag(anchor)
    tag = original_tag
    for class_name in ("nav-prev", "nav-next", "nav-disabled", "primary"):
        tag = remove_class(tag, class_name)
    tag = nav.add_class(tag, "nav-return-link")
    tag = nav.replace_href(tag, href)
    tag = nav.set_attribute(tag, "data-nav-role", "return")
    tag = nav.set_attribute(tag, "aria-label", visible_text(anchor).replace("←", "").replace("→", "").strip())
    for attribute in ("aria-disabled", "tabindex", "data-nav-state"):
        tag = nav.remove_attribute(tag, attribute)
    return tag + anchor[len(original_tag) :]


def make_edge_status(anchor: str) -> str:
    tag = opening_tag(anchor)
    tag = nav.remove_attribute(tag, "href")
    tag = re.sub(r"^<a\b", "<span", tag, count=1, flags=re.I)
    tag = nav.set_attribute(tag, "role", "status")
    tag = nav.set_attribute(tag, "aria-disabled", "true")
    tag = nav.remove_attribute(tag, "tabindex")
    return replace_closing_tag(tag + anchor[len(opening_tag(anchor)) :], "span")


def original_nav_anchors_from_html(html: str) -> list[str]:
    anchors: list[str] = []
    for open_start, open_end, close_start, _ in nav._nav_container_spans(html):
        body = html[open_end:close_start]
        anchors.extend(match.group(0) for match in re.finditer(r"<a\b[^>]*>.*?</a>", body, flags=re.I | re.S))
    return anchors


def original_nav_anchors(path: Path) -> list[str]:
    return original_nav_anchors_from_html(path.read_text(encoding="utf-8", errors="replace"))


def original_for(current_anchor: str, originals: list[str]) -> str | None:
    text = visible_text(current_anchor)
    matches = [item for item in originals if visible_text(item) == text]
    return matches[0] if len(matches) == 1 else None


def clean_nav_whitespace(html: str) -> str:
    result = html
    for open_start, open_end, close_start, close_end in reversed(nav._nav_container_spans(html)):
        body = result[open_end:close_start]
        cleaned = re.sub(r"[ \t]+(?=\r?$)", "", body, flags=re.M)
        if cleaned != body:
            result = result[:open_end] + cleaned + result[close_start:]
    return result


def repair_page_html(current: str, original: str, page: Path) -> tuple[str, int, int]:
    original_anchors = [
        match.group(0)
        for open_start, open_end, close_start, _ in nav._nav_container_spans(original)
        for match in re.finditer(r"<a\b[^>]*>.*?</a>", original[open_end:close_start], flags=re.I | re.S)
    ]
    changed = 0
    unresolved = 0
    return_blocks: list[str] = []
    result = current

    for open_start, open_end, close_start, close_end in reversed(nav._nav_container_spans(current)):
        container = result[open_start:close_end]
        body_start = open_end - open_start
        body_end = close_start - open_start
        body = container[body_start:body_end]
        anchors = list(re.finditer(r"<a\b[^>]*>.*?</a>", body, flags=re.I | re.S))
        disabled = [
            match
            for match in anchors
            if re.search(r"\bdata-nav-state\s*=\s*[\"']disabled[\"']", match.group(0), flags=re.I)
        ]
        if not disabled:
            continue

        replacements: dict[int, str] = {}
        moved: list[str] = []
        for match in disabled:
            current_anchor = match.group(0)
            original_anchor = original_for(current_anchor, original_anchors)
            original_href = nav.href_from_tag(original_anchor) if original_anchor else ""
            target = nav.resolve(page, original_href)
            if original_anchor and original_href and target is not None and target.exists():
                moved.append(make_return_anchor(current_anchor, original_href))
                replacements[match.start()] = ""
                changed += 1
            elif original_anchor:
                replacements[match.start()] = make_edge_status(current_anchor)
                changed += 1
            else:
                unresolved += 1

        if not replacements:
            continue
        pieces: list[str] = []
        cursor = 0
        for match in anchors:
            pieces.append(body[cursor:match.start()])
            pieces.append(replacements.get(match.start(), match.group(0)))
            cursor = match.end()
        pieces.append(body[cursor:])
        new_body = "".join(pieces)

        # A return-only footer has no previous/next controls after the move.
        has_sequence_control = bool(re.search(r"data-nav-role\s*=\s*[\"'](?:prev|next)[\"']", new_body, flags=re.I))
        new_container = container[:body_start] + new_body + container[body_end:]
        if not has_sequence_control:
            new_container = ""
        block = "".join(
            f'<div class="nav-return" role="navigation" aria-label="返回課程導覽">\n  {item}\n</div>\n'
            for item in moved
        )
        replacement = block + new_container
        result = result[:open_start] + replacement + result[close_end:]

    result, refresh_count = refresh_split_return_blocks(result, original)
    changed += refresh_count
    result, split_count = split_return_actions(result)
    changed += split_count
    result, style_changed = ensure_navigation_style(result)
    if style_changed:
        changed += 1
    if changed and not re.search(r"id\s*=\s*[\"']navigation-action-fix[\"']", result, flags=re.I):
        unresolved += 1
    result = clean_nav_whitespace(result)
    return result, changed, unresolved


def repair_page(page: Path, apply: bool) -> tuple[bool, int, int]:
    relative = page.relative_to(ROOT)
    original_path = BACKUP / relative
    if not original_path.exists():
        return False, 0, 1
    current = page.read_text(encoding="utf-8", errors="replace")
    original = original_path.read_text(encoding="utf-8", errors="replace")
    updated, changed, unresolved = repair_page_html(current, original, page)
    if apply and updated != current:
        page.write_text(updated, encoding="utf-8")
    return updated != current, changed, unresolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.dry_run == args.apply:
        parser.error("choose exactly one of --dry-run or --apply")

    changed_pages = 0
    moved_actions = 0
    unresolved = 0
    for course_index in sorted(ROOT.glob("*/index.html")):
        for page in nav.official_html(course_index.parent):
            changed, moved, unresolved_page = repair_page(page, args.apply)
            if changed:
                changed_pages += 1
                print(f"{page.relative_to(ROOT)}: moved_or_repaired={moved}")
            moved_actions += moved
            unresolved += unresolved_page

    mode = "dry-run" if args.dry_run else "apply"
    print(f"mode={mode} changed_pages={changed_pages} moved_or_repaired={moved_actions} unresolved={unresolved}")
    return 1 if unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
