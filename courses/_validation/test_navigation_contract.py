#!/usr/bin/env python3
"""Contract checks for learner-facing course navigation.

This is intentionally a small standard-library checker so the same rules can
run before and after the batch repair without changing course content.
"""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote
import re
import sys


REPO = Path(__file__).resolve().parents[2]
COURSES = REPO / "courses"
SITE_INDEX = REPO / "index.html"
EXCLUDED_PARTS = {part for part in ()}


def official_html(course_root: Path):
    for path in sorted(course_root.rglob("*.html")):
        relative = path.relative_to(course_root)
        if any(part.startswith("_") for part in relative.parts):
            continue
        if "assets" in relative.parts:
            continue
        yield path


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
                "attrs": attributes,
                "line": self.getpos()[0],
                "parts": [],
                "in_nav": any(
                    class_name in {"lesson-nav", "nav-footer", "module-nav", "nav-return"}
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


def resolve(page: Path, href: str) -> Path | None:
    clean = unquote((href or "").split("#", 1)[0].split("?", 1)[0])
    if not clean or clean.startswith(("/", "//")):
        return None
    if re.match(r"^[a-z][a-z0-9+.-]*:", clean, re.I):
        return None
    return (page.parent / clean).resolve()


def explicit_back(anchors: list[dict]) -> dict | None:
    return next(
        (
            anchor
            for anchor in anchors
            if {"back-link", "breadcrumb"} & anchor["classes"]
        ),
        None,
    )


def logo(anchors: list[dict]) -> dict | None:
    return next((anchor for anchor in anchors if "logo" in anchor["classes"]), None)


def course_roots() -> list[Path]:
    return sorted(path.parent for path in COURSES.glob("*/index.html"))


def is_module_page(path: Path) -> bool:
    return bool(re.fullmatch(r"module\d+\.html", path.name))


def is_unit_page(path: Path) -> bool:
    return path.name != "index.html" and not is_module_page(path)


def role(anchor: dict) -> str:
    data_role = anchor["attrs"].get("data-nav-role")
    if data_role in {"prev", "next"}:
        return data_role
    if data_role == "return":
        return "return"
    text = anchor.get("text", "")
    if any(word in text for word in ("上一單元", "上一節", "上一堂", "上一頁", "上一課")):
        return "prev"
    if any(word in text for word in ("下一單元", "下一節", "下一堂", "下一頁", "下一課")):
        return "next"
    return "unknown"


def scan() -> dict:
    result = {
        "courses": len(course_roots()),
        "pages": 0,
        "broken_local_refs": [],
        "broken_logos": [],
        "non_site_logos": [],
        "oversized_nav": [],
        "unlabelled_two_button_nav": [],
        "return_in_sequence": [],
        "ambiguous_back": [],
        "missing_back": [],
    }
    for course_root in course_roots():
        for page in official_html(course_root):
            result["pages"] += 1
            anchors = parse(page)
            relative_name = f"{course_root.name}/{page.relative_to(course_root)}"
            page_logo = logo(anchors)
            if page_logo:
                target = resolve(page, page_logo["href"])
                if target is None or not target.exists():
                    result["broken_logos"].append((relative_name, page_logo["line"], page_logo["href"]))
                elif target != SITE_INDEX:
                    result["non_site_logos"].append((relative_name, page_logo["line"], page_logo["href"]))
            if is_unit_page(page):
                back = explicit_back(anchors)
                if back is None:
                    result["missing_back"].append((relative_name, 1, ""))
                else:
                    target = resolve(page, back["href"])
                    if target is None or not target.exists():
                        result["broken_local_refs"].append((relative_name, back["line"], back["href"]))
                    elif target.name not in {"index.html"} and not is_module_page(target):
                        result["ambiguous_back"].append((relative_name, back["line"], back["href"]))
                nav_links = [anchor for anchor in anchors if anchor["in_nav"] and anchor["href"]]
                nav = [anchor for anchor in nav_links if role(anchor) in {"prev", "next"}]
                for anchor in nav:
                    target = resolve(page, anchor["href"])
                    is_overview_target = target is not None and (
                        target.name == "index.html" or is_module_page(target)
                    )
                    if is_overview_target and re.search(
                        r"返回|回到|回課程|課程(?:總覽|首頁|目錄)|首頁|目錄",
                        anchor["text"],
                    ):
                        result["return_in_sequence"].append(
                            (relative_name, anchor["line"], anchor["text"])
                        )
                if len(nav) > 2:
                    result["oversized_nav"].append((relative_name, nav[0]["line"], len(nav)))
                elif len(nav) == 2 and [role(anchor) for anchor in nav] != ["prev", "next"]:
                    result["unlabelled_two_button_nav"].append(
                        (relative_name, nav[0]["line"], [anchor["text"] for anchor in nav])
                    )
                for anchor in nav_links:
                    target = resolve(page, anchor["href"])
                    if target is not None and not target.exists():
                        result["broken_local_refs"].append((relative_name, anchor["line"], anchor["href"]))
    return result


def main() -> int:
    result = scan()
    print(
        f"courses={result['courses']} pages={result['pages']} "
        f"broken_logos={len(result['broken_logos'])} "
        f"non_site_logos={len(result['non_site_logos'])} "
        f"oversized_nav={len(result['oversized_nav'])} "
        f"unlabelled_two_button_nav={len(result['unlabelled_two_button_nav'])} "
        f"return_in_sequence={len(result['return_in_sequence'])} "
        f"ambiguous_back={len(result['ambiguous_back'])} "
        f"missing_back={len(result['missing_back'])} "
        f"broken_local_refs={len(result['broken_local_refs'])}"
    )
    report_only = {
        key: value
        for key, value in result.items()
        if key in {"oversized_nav", "ambiguous_back", "missing_back"} and value
    }
    for key, values in report_only.items():
        print(f"[WARN:{key}] {len(values)}")
        for value in values[:20]:
            print("  ", value)

    hard_failures = {
        key: value
        for key, value in result.items()
        if key in {"broken_logos", "unlabelled_two_button_nav", "return_in_sequence", "broken_local_refs"}
        and value
    }
    for key, values in hard_failures.items():
        print(f"[{key}] {len(values)}")
        for value in values[:20]:
            print("  ", value)
    if hard_failures:
        print("FAIL: navigation contract is not satisfied")
        return 1
    print("PASS: navigation contract is satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
