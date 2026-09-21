#!/usr/bin/env python3
"""Normalize deterministic learner navigation without rewriting lesson prose."""

from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
import argparse
import re
import sys


REPO = Path(__file__).resolve().parents[2]
COURSES = REPO / "courses"
SITE_INDEX = REPO / "index.html"


class AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, set[str]]] = []
        self.anchor: dict | None = None
        self.anchors: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        if tag == "a":
            self.anchor = {
                "href": attributes.get("href", ""),
                "classes": classes,
                "line": self.getpos()[0],
                "parts": [],
                "in_nav": any(
                    class_name in {"lesson-nav", "nav-footer"}
                    for _, stack_classes in self.stack
                    for class_name in stack_classes
                ),
            }
        self.stack.append((tag, classes))

    def handle_data(self, data: str) -> None:
        if self.anchor is not None:
            self.anchor["parts"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.anchor is not None:
            self.anchor["text"] = " ".join("".join(self.anchor["parts"]).split())
            self.anchors.append(self.anchor)
            self.anchor = None
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                self.stack = self.stack[:index]
                break


def parse(path: Path) -> list[dict]:
    parser = AnchorParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser.anchors


def official_html(course_root: Path) -> list[Path]:
    paths = []
    for path in course_root.rglob("*.html"):
        relative = path.relative_to(course_root)
        if any(part.startswith("_") for part in relative.parts) or "assets" in relative.parts:
            continue
        paths.append(path)
    return sorted(paths)


def resolve(page: Path, href: str) -> Path | None:
    clean = unquote((href or "").split("#", 1)[0].split("?", 1)[0])
    if not clean or clean.startswith(("/", "//")):
        return None
    if re.match(r"^[a-z][a-z0-9+.-]*:", clean, re.I):
        return None
    return (page.parent / clean).resolve()


def is_module_page(path: Path) -> bool:
    return bool(re.fullmatch(r"module\d+\.html", path.name))


def is_unit_page(path: Path) -> bool:
    return path.name != "index.html" and not is_module_page(path)


def anchor_tag_with_class(html: str, class_name: str) -> tuple[int, int, str] | None:
    for match in re.finditer(r"<a\b[^>]*>", html, flags=re.I | re.S):
        tag = match.group(0)
        class_match = re.search(
            r"\bclass\s*=\s*([\"'])(.*?)\1", tag, flags=re.I | re.S
        )
        if class_match and class_name in class_match.group(2).split():
            return match.start(), match.end(), tag
    return None


def back_tag(html: str) -> tuple[int, int, str] | None:
    for match in re.finditer(r"<a\b[^>]*>", html, flags=re.I | re.S):
        tag = match.group(0)
        class_match = re.search(
            r"\bclass\s*=\s*([\"'])(.*?)\1", tag, flags=re.I | re.S
        )
        if not class_match:
            continue
        classes = set(class_match.group(2).split())
        if {"back-link", "breadcrumb"} & classes:
            return match.start(), match.end(), tag
    return None


def replace_href(tag: str, href: str) -> str:
    pattern = r"(\bhref\s*=\s*)([\"']).*?\2"
    if re.search(pattern, tag, flags=re.I | re.S):
        return re.sub(pattern, lambda m: f'{m.group(1)}{m.group(2)}{href}{m.group(2)}', tag, count=1, flags=re.I | re.S)
    return tag[:-1] + f' href="{href}">'


def set_attribute(tag: str, name: str, value: str) -> str:
    pattern = rf"(?<![\w-])(\b{name}\s*=\s*)([\"']).*?\2"
    if re.search(pattern, tag, flags=re.I | re.S):
        return re.sub(pattern, lambda m: f'{m.group(1)}{m.group(2)}{value}{m.group(2)}', tag, count=1, flags=re.I | re.S)
    return tag[:-1] + f' {name}="{value}">'


def add_class(tag: str, class_name: str) -> str:
    pattern = r"(\bclass\s*=\s*)([\"'])(.*?)\2"
    match = re.search(pattern, tag, flags=re.I | re.S)
    if not match:
        return tag[:-1] + f' class="{class_name}">'
    classes = match.group(3).split()
    if class_name not in classes:
        classes.append(class_name)
    replacement = f"{match.group(1)}{match.group(2)}{' '.join(classes)}{match.group(2)}"
    return tag[: match.start()] + replacement + tag[match.end() :]


def remove_attribute(tag: str, name: str) -> str:
    return re.sub(rf"\s+(?<![\w-])\b{name}\s*=\s*([\"']).*?\1", "", tag, count=1, flags=re.I | re.S)


def update_nav_anchor(anchor: str, nav_role: str, disabled: bool = False) -> str:
    anchor = add_class(anchor, "nav-prev" if nav_role == "prev" else "nav-next")
    anchor = set_attribute(anchor, "aria-label", "上一單元" if nav_role == "prev" else "下一單元")
    anchor = set_attribute(anchor, "data-nav-role", nav_role)
    if disabled:
        anchor = remove_attribute(anchor, "href")
        anchor = add_class(anchor, "nav-disabled")
        anchor = set_attribute(anchor, "aria-disabled", "true")
        anchor = set_attribute(anchor, "tabindex", "-1")
        anchor = set_attribute(anchor, "data-nav-state", "disabled")
    return anchor


def group_key(name: str) -> str | None:
    match = re.match(r"(CH|PRAC|WS)(\d+)", name, flags=re.I)
    if match:
        return f"CH{match.group(2)}"
    match = re.match(r"(m\d+)", name, flags=re.I)
    if match:
        return match.group(1).lower()
    return None


def lesson_like(name: str) -> bool:
    stem = Path(name).stem.lower()
    if re.search(r"(tour|overview|guide|hub|home|summary)", stem):
        return False
    return bool(
        re.match(r"(?:ch|prac|ws)\d", stem, flags=re.I)
        or re.match(r"m\d", stem, flags=re.I)
        or re.match(r"post-llm-\d", stem, flags=re.I)
    )


def href_from_tag(tag: str) -> str:
    match = re.search(r"\bhref\s*=\s*([\"'])(.*?)\1", tag, flags=re.I | re.S)
    return match.group(2) if match else ""


def overview_for(
    page: Path,
    course_root: Path,
    current_target: Path | None,
    group_modules: dict[str, set[Path]],
    modules: list[Path],
) -> Path | None:
    if current_target and current_target.exists() and not lesson_like(current_target.name):
        return None
    group = group_key(page.name)
    candidates = sorted(group_modules.get(group or "", set()))
    if len(candidates) == 1:
        return candidates[0]
    if len(modules) == 1:
        return modules[0]
    return course_root / "index.html"


def rel_href(page: Path, target: Path) -> str:
    return Path(__import__("os").path.relpath(target, page.parent)).as_posix()


TAG_TOKEN_RE = re.compile(
    r"<(?P<closing>/)?(?P<tag>div|nav)\b"
    r"(?P<attrs>(?:[^>\"']|\"[^\"]*\"|'[^']*')*)>",
    flags=re.I | re.S,
)


def _nav_container_spans(html: str) -> list[tuple[int, int, int, int]]:
    """Return outermost target container spans with balanced div/nav tags."""
    stack: list[tuple[str, int, int, bool]] = []
    spans: list[tuple[int, int, int, int]] = []

    for token in TAG_TOKEN_RE.finditer(html):
        tag = token.group("tag").lower()
        if token.group("closing"):
            opening_index = next(
                (index for index in range(len(stack) - 1, -1, -1) if stack[index][0] == tag),
                None,
            )
            if opening_index is None:
                continue
            opening_tag, start, open_end, is_target = stack.pop(opening_index)
            if is_target:
                spans.append((start, open_end, token.start(), token.end()))
            continue

        classes = set(re.findall(r"(?:^|\s)class\s*=\s*([\"'])(.*?)\1", token.group("attrs"), flags=re.I | re.S))
        class_text = " ".join(value for _, value in classes)
        is_target = bool(re.search(r"(?:^|\s)(?:nav-footer|lesson-nav|nav-return)(?:\s|$)", class_text, flags=re.I))
        stack.append((tag, token.start(), token.end(), is_target))

    outermost: list[tuple[int, int, int, int]] = []
    for span in sorted(spans, key=lambda item: (item[0], -item[3])):
        if any(
            existing[0] <= span[0] and span[3] <= existing[3]
            for existing in outermost
        ):
            continue
        outermost.append(span)
    return outermost


def should_disable_nav_anchor(page: Path | None, anchor: str, nav_role: str) -> bool:
    if page is None:
        return False
    href = href_from_tag(anchor)
    target = resolve(page, href)
    if not href or target is None or not target.exists():
        return True
    # A valid overview link is a return action, not a missing sequence link.
    # The repair pass moves it to its own active return slot instead of
    # leaving a visible action label without an href.
    return False


def nav_container_rewrite(html: str, page: Path | None = None) -> tuple[str, int, int]:
    changes = 0
    ambiguous = 0

    def rewrite_body(body: str) -> str | None:
        nonlocal ambiguous
        anchors = list(re.finditer(r"<a\b[^>]*>.*?</a>", body, flags=re.I | re.S))
        if len(anchors) < 2:
            ambiguous += 1
            return None
        first = anchors[0].group(0)
        last = anchors[-1].group(0)
        middle = [item.group(0) for item in anchors[1:-1]]
        first_text = unescape(re.sub(r"<[^>]+>", " ", first))
        last_text = unescape(re.sub(r"<[^>]+>", " ", last))
        first_left = len(anchors) == 2 or "←" in first or "上一" in first_text or "上一" in body[: anchors[0].start() + 80]
        last_right = len(anchors) == 2 or "→" in last or "下一" in last_text or "下一" in body[max(0, anchors[-1].start() - 80) :]
        if not first_left or not last_right:
            ambiguous += 1
            return None
        updated_first = re.sub(
            r"<a\b[^>]*>",
            lambda m: update_nav_anchor(m.group(0), "prev", should_disable_nav_anchor(page, first, "prev")),
            first,
            count=1,
            flags=re.I | re.S,
        )
        updated_last = re.sub(
            r"<a\b[^>]*>",
            lambda m: update_nav_anchor(m.group(0), "next", should_disable_nav_anchor(page, last, "next")),
            last,
            count=1,
            flags=re.I | re.S,
        )
        if len(anchors) > 2:
            # Only discard middle links that are clearly return/overview controls.
            middle_text = " ".join(re.sub(r"<[^>]+>", " ", item) for item in middle)
            if not re.search(r"返回|回|首頁|總覽|Part|Module|課程", middle_text, flags=re.I):
                ambiguous += 1
                return None
        replacements = {0: updated_first, len(anchors) - 1: updated_last}
        if len(anchors) > 2:
            replacements.update({index: "" for index in range(1, len(anchors) - 1)})

        pieces: list[str] = []
        cursor = 0
        for index, anchor in enumerate(anchors):
            pieces.append(body[cursor : anchor.start()])
            pieces.append(replacements.get(index, anchor.group(0)))
            cursor = anchor.end()
        pieces.append(body[cursor:])
        return re.sub(r"[ \t]+(?=\r?$)", "", "".join(pieces), flags=re.M)

    result = html
    for open_start, open_end, close_start, close_end in reversed(_nav_container_spans(html)):
        body = result[open_end:close_start]
        new_body = rewrite_body(body)
        if new_body is None:
            continue
        changes += 1
        result = result[:open_end] + new_body + result[close_start:]

    return result, changes, ambiguous


def apply_page(page: Path, course_root: Path, pages: list[Path], apply: bool) -> tuple[str, list[str]]:
    original = page.read_text(encoding="utf-8", errors="replace")
    updated = original
    reasons: list[str] = []

    canonical_logo = rel_href(page, SITE_INDEX)
    logo_match = anchor_tag_with_class(updated, "logo")
    if logo_match and href_from_tag(logo_match[2]) != canonical_logo:
        updated = updated[: logo_match[0]] + replace_href(logo_match[2], canonical_logo) + updated[logo_match[1] :]
        reasons.append(f"logo->{canonical_logo}")

    if is_unit_page(page):
        back_match = back_tag(updated)
        if back_match:
            current_target = resolve(page, href_from_tag(back_match[2]))
            modules = [path for path in pages if is_module_page(path)]
            group_modules: dict[str, set[Path]] = {}
            for candidate in pages:
                if not is_unit_page(candidate):
                    continue
                candidate_back = back_tag(candidate.read_text(encoding="utf-8", errors="replace"))
                if not candidate_back:
                    continue
                candidate_target = resolve(candidate, href_from_tag(candidate_back[2]))
                if candidate_target and candidate_target.exists() and is_module_page(candidate_target):
                    key = group_key(candidate.name)
                    if key:
                        group_modules.setdefault(key, set()).add(candidate_target)
            desired = overview_for(page, course_root, current_target, group_modules, modules)
            if desired is not None:
                desired_href = rel_href(page, desired)
                if href_from_tag(back_match[2]) != desired_href:
                    updated = updated[: back_match[0]] + replace_href(back_match[2], desired_href) + updated[back_match[1] :]
                    reasons.append(f"back->{desired_href}")

    if is_unit_page(page):
        updated, nav_changes, nav_ambiguous = nav_container_rewrite(updated, page)
        if nav_changes:
            reasons.append(f"footer-nav={nav_changes}")
        if nav_ambiguous:
            reasons.append(f"footer-ambiguous={nav_ambiguous}")

    if apply and updated != original:
        page.write_text(updated, encoding="utf-8")
    return updated, reasons


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.dry_run == args.apply:
        parser.error("choose exactly one of --dry-run or --apply")

    changed = 0
    ambiguous = 0
    for course_index in sorted(COURSES.glob("*/index.html")):
        course_root = course_index.parent
        pages = official_html(course_root)
        for page in pages:
            before = page.read_bytes()
            updated, reasons = apply_page(page, course_root, pages, args.apply)
            if updated.encode("utf-8") != before:
                changed += 1
                print(f"{course_root.name}/{page.relative_to(course_root)}: {', '.join(reasons)}")
            ambiguous += sum(1 for reason in reasons if reason.startswith("footer-ambiguous"))
    mode = "dry-run" if args.dry_run else "apply"
    print(f"mode={mode} changed_pages={changed} ambiguous_nav_containers={ambiguous}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
