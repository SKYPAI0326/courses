#!/usr/bin/env python3
"""Validate course HTML structure, ids, CSS blocks, and optional text snapshots.

This is a deterministic static gate. It does not replace browser smoke testing;
the caller must still check representative pages at the required viewports.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

CONTENT_CLASSES = {"lesson-section", "body-text", "step-list", "prac-box"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
OFFICE_AI_REGRESSION_TARGETS = (
    "ch1/CH1-1.html",
    "ch1/CH1-2.html",
    "ch6/CH6-2.html",
    "ch6/CH6-3.html",
)


class Node:
    def __init__(self, tag: str, attrs, parent: "Node | None", ordinal: int):
        self.tag = tag
        self.attrs = dict(attrs)
        self.parent = parent
        self.ordinal = ordinal
        self.children: list[Node] = []

    @property
    def classes(self) -> set[str]:
        return set(self.attrs.get("class", "").split())


class Tree(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.root = Node("#document", [], None, -1)
        self.stack = [self.root]
        self.nodes: list[Node] = []
        self.style_text: list[str] = []
        self._in_style = False
        self._style_chunks: list[str] = []
        self.errors: list[str] = []
        self.ordinal = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        node = Node(tag, attrs, self.stack[-1], self.ordinal)
        self.ordinal += 1
        self.stack[-1].children.append(node)
        self.nodes.append(node)
        if tag == "style":
            self._in_style = True
            self._style_chunks = []
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag.lower(), attrs, self.stack[-1], self.ordinal)
        self.ordinal += 1
        self.stack[-1].children.append(node)
        self.nodes.append(node)

    def handle_data(self, data):
        if self._in_style:
            self._style_chunks.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                if i != len(self.stack) - 1:
                    inner = ", ".join(f"<{node.tag}>" for node in self.stack[i + 1:])
                    self.errors.append(f"misnested closing tag </{tag}> before {inner}")
                if tag == "style":
                    self.style_text.append("".join(self._style_chunks))
                    self._in_style = False
                    self._style_chunks = []
                self.stack = self.stack[:i]
                return
        self.errors.append(f"unmatched closing tag </{tag}>")

    def close(self):
        super().close()
        if self._in_style and self._style_chunks:
            self.style_text.append("".join(self._style_chunks))
        for node in self.stack[1:]:
            self.errors.append(f"unclosed <{node.tag}>")


def has_ancestor(node: Node, class_name: str) -> bool:
    parent = node.parent
    while parent and parent.tag != "#document":
        if class_name in parent.classes:
            return True
        parent = parent.parent
    return False


def css_brace_errors(css: str) -> list[str]:
    """Check CSS brace balance while ignoring comments and quoted strings."""
    errors: list[str] = []
    depth = 0
    quote: str | None = None
    escaped = False
    i = 0
    while i < len(css):
        ch = css[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            i += 1
            continue
        if css.startswith("/*", i):
            end = css.find("*/", i + 2)
            if end < 0:
                errors.append("unclosed CSS comment")
                break
            i = end + 2
            continue
        if ch in "'\"":
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                errors.append("unmatched CSS closing brace")
                depth = 0
        i += 1
    if quote:
        errors.append("unclosed CSS string")
    if depth:
        errors.append(f"unclosed CSS block(s): {depth}")
    media_probe = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    if "@media" in media_probe and "{" not in media_probe:
        errors.append("@media query has no opening block")
    return errors


def load_text_checker():
    path = Path(__file__).with_name("check_content_unchanged.py")
    spec = importlib.util.spec_from_file_location("course_content_checker", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate(path: Path, expected_body_count: int | None = 1, before: Path | None = None) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    parser = Tree()
    parser.feed(text)
    parser.close()
    errors = list(parser.errors)

    bodies = [n for n in parser.nodes if "lesson-body" in n.classes]
    heroes = [n for n in parser.nodes if "lesson-hero" in n.classes]
    sections = [n for n in parser.nodes if "lesson-section" in n.classes]
    navs = [n for n in parser.nodes if "lesson-nav" in n.classes]
    content_nodes = [n for n in parser.nodes if n.classes & CONTENT_CLASSES]

    if content_nodes and not bodies:
        errors.append("content classes present but missing .lesson-body")
    if expected_body_count is not None and content_nodes and len(bodies) != expected_body_count:
        errors.append(f"expected {expected_body_count} .lesson-body element(s), found {len(bodies)}")
    if heroes and bodies and min(n.ordinal for n in bodies) < min(n.ordinal for n in heroes):
        errors.append(".lesson-body appears before .lesson-hero")
    for node in content_nodes:
        if not has_ancestor(node, "lesson-body"):
            errors.append(f"content class outside .lesson-body: {sorted(node.classes & CONTENT_CLASSES)}")
    if sections and not has_ancestor(sections[0], "lesson-body"):
        errors.append("first .lesson-section is outside .lesson-body")
    if navs and bodies and min(n.ordinal for n in navs) < max(n.ordinal for n in bodies):
        errors.append(".lesson-nav appears before or inside .lesson-body")

    ids = [n.attrs.get("id") for n in parser.nodes if n.attrs.get("id")]
    for value, count in Counter(ids).items():
        if count > 1:
            errors.append(f"duplicate id: {value} ({count} occurrences)")
    for css in parser.style_text:
        errors.extend(css_brace_errors(css))
    if before is not None:
        checker = load_text_checker()
        if checker is None or checker.main(str(before), str(path)) != 0:
            errors.append("visible text or href changed from --before snapshot")
    return not errors, errors


def collect_files(files: list[Path], batch: Path | None) -> list[Path]:
    found = list(files)
    if batch:
        found.extend(sorted(
            path for path in batch.rglob("*.html")
            if not any(part.startswith("_") for part in path.relative_to(batch).parts[:-1])
        ))
    # preserve order while de-duplicating
    return list(dict.fromkeys(p for p in found if p.is_file()))


def count_sections(path: Path) -> int:
    parser = Tree()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return sum("lesson-section" in node.classes for node in parser.nodes)


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--batch", type=Path, help="recursively scan a course directory")
    parser.add_argument("--office-ai-regression", type=Path, help="run the four fixed office-ai wrapper regression targets")
    parser.add_argument("--before", type=Path, help="before HTML for visible-text/href diff (single file)")
    parser.add_argument("--before-dir", type=Path, help="before course directory; paths are matched relative to --batch")
    parser.add_argument("--expected-body-count", type=int, default=1)
    args = parser.parse_args(argv)
    if args.office_ai_regression is not None and (args.files or args.batch):
        parser.error("--office-ai-regression cannot be combined with FILE or --batch")
    regression = args.office_ai_regression is not None
    if regression:
        paths = [args.office_ai_regression / relative for relative in OFFICE_AI_REGRESSION_TARGETS]
    else:
        paths = collect_files(args.files, args.batch)
    if not paths:
        parser.error("provide FILE.html or --batch DIRECTORY")
    if args.before is not None and len(paths) != 1:
        parser.error("--before is supported for one target file at a time")
    if args.before is not None and args.before_dir is not None:
        parser.error("use either --before or --before-dir, not both")
    if args.before_dir is not None and not (args.batch is not None or regression):
        parser.error("--before-dir requires --batch")

    blocked = 0
    for path in paths:
        if not path.is_file():
            blocked += 1
            print(f"HTML STRUCTURE BLOCK: {path}")
            print("- regression target is missing")
            continue
        before = args.before
        if args.before_dir is not None:
            relative = path.relative_to(args.batch or args.office_ai_regression)
            before = args.before_dir / relative
            if not before.is_file():
                ok, errors = False, [f"missing before snapshot: {before}"]
            else:
                ok, errors = validate(path, args.expected_body_count, before)
        else:
            ok, errors = validate(path, args.expected_body_count, before)
        if regression and count_sections(path) < 1:
            ok = False
            errors = list(errors) + ["office-ai regression requires lesson_section_count >= 1"]
        if ok:
            note = "lesson-body checked" if any("lesson-body" in n for n in []) else "static structure checked"
            print(f"HTML structure OK: {path} ({note}; browser smoke still required)")
        else:
            blocked += 1
            print(f"HTML STRUCTURE BLOCK: {path}")
            for error in errors:
                print(f"- {error}")
    print(f"summary: checked={len(paths)} blocked={blocked}")
    return 1 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(cli())
