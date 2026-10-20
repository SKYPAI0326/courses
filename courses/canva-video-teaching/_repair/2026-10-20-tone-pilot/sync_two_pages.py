#!/usr/bin/env python3
"""Replace selected learner bodies from a renderer output."""

from pathlib import Path
import sys

from bs4 import BeautifulSoup


COURSE_DIR = Path(__file__).resolve().parents[2]
ALLOWED_PAGES = {
    *(Path(f"ch1/CH1-{number}.html") for number in range(1, 7)),
    *(Path(f"ch2/CH2-{number}.html") for number in range(1, 7)),
    Path("EXT1.html"),
}
BODY_MARKER = '<div class="lesson-body">'
NAV_MARKER = '<div class="nav-footer">'


def split_shell(text: str) -> tuple[str, str, str]:
    assert text.count(BODY_MARKER) == 1, "expected one lesson-body marker"
    assert text.count(NAV_MARKER) == 1, "expected one nav-footer marker"
    prefix, rest = text.split(BODY_MARKER, 1)
    body_inner, suffix = rest.split(NAV_MARKER, 1)
    return prefix, BODY_MARKER + body_inner, NAV_MARKER + suffix


def preserve_existing_attributes(old_body, new_body) -> None:
    old_links = {}
    for link in old_body.find_all("a", href=True):
        old_links.setdefault(link["href"], dict(link.attrs))

    for link in new_body.find_all("a", href=True):
        assert link["href"] in old_links, f"unexpected link: {link['href']}"
        link.attrs = dict(old_links[link["href"]])

    old_images = {}
    for image in old_body.find_all("img", src=True):
        old_images.setdefault(image["src"].split("?", 1)[0], dict(image.attrs))

    for image in new_body.find_all("img", src=True):
        key = image["src"].split("?", 1)[0]
        assert key in old_images, f"unexpected image: {key}"
        image.attrs = dict(old_images[key])


def mark_action_lists(new_body) -> None:
    for section in new_body.select(".lesson-section"):
        lists = [node for node in section.find_all(["ol", "ul"], recursive=False) if "step-list" in node.get("class", [])]
        for action_list in lists:
            action_list["class"] = [*action_list.get("class", []), "action-steps"]
        if lists:
            headings_before = lists[0].find_all_previous("h3", limit=1)
            if not headings_before or headings_before[0].find_parent(class_="lesson-section") is not section:
                lists[0]["data-action-label"] = "操作步驟"


def sync_page(render_root: Path, relative_page: Path) -> None:
    target = COURSE_DIR / relative_page
    rendered = render_root / relative_page
    current_text = target.read_text(encoding="utf-8")
    rendered_text = rendered.read_text(encoding="utf-8")

    current_soup = BeautifulSoup(current_text, "html.parser")
    rendered_soup = BeautifulSoup(rendered_text, "html.parser")
    old_body = current_soup.select_one(".lesson-body")
    new_body = rendered_soup.select_one(".lesson-body")
    assert old_body is not None and new_body is not None
    assert len(old_body.select(".lesson-section")) == len(new_body.select(".lesson-section"))

    preserve_existing_attributes(old_body, new_body)
    mark_action_lists(new_body)
    old_prefix, _, old_suffix = split_shell(current_text)
    if '<body class="action-layout-pilot">' not in old_prefix:
        assert old_prefix.count("<body>") == 1
        old_prefix = old_prefix.replace("<body>", '<body class="action-layout-pilot">', 1)
    new_body_html = str(new_body)
    assert new_body_html.startswith(BODY_MARKER)
    updated = old_prefix + new_body_html + old_suffix

    updated_soup = BeautifulSoup(updated, "html.parser")
    assert len(updated_soup.select(".lesson-body")) == 1
    assert all(section.find_parent(class_="lesson-body") for section in updated_soup.select(".lesson-section"))
    assert updated_soup.select_one("#_gate") is not None, "access gate must remain"
    target.write_text(updated, encoding="utf-8")
    print(f"synced {relative_page}")


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit("usage: sync_two_pages.py RENDERED_COURSE_DIR PAGE [PAGE ...]")
    render_root = Path(sys.argv[1]).resolve()
    pages = [Path(value) for value in sys.argv[2:]]
    unexpected = [str(page) for page in pages if page not in ALLOWED_PAGES]
    assert not unexpected, f"unsupported page(s): {', '.join(unexpected)}"
    for page in pages:
        sync_page(render_root, page)


if __name__ == "__main__":
    main()
