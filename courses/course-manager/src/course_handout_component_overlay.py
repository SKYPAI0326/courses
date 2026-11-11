"""Apply an approved Markdown rewrite inside an existing handout component layout."""
import copy
import os
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from bs4 import BeautifulSoup, NavigableString, Tag

from src.course_improvement_loop import artifact, digest, require, save


def normalized(text):
    return " ".join(text.split())


def local_target_key(url, base):
    parts = urlsplit(str(url))
    if parts.scheme or parts.netloc:
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path,
                           parts.query, parts.fragment))
    if not parts.path:
        return urlunsplit(("", "", "", parts.query, parts.fragment))
    target = Path(unquote(parts.path))
    if not target.is_absolute():
        target = base / target
    return urlunsplit(("", "", str(target.resolve()), parts.query, parts.fragment))


def rebase_url(url, origin, destination):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or not parts.path:
        return url
    target = Path(unquote(parts.path))
    if not target.is_absolute():
        target = origin / target
    relative = os.path.relpath(target.resolve(), destination)
    return urlunsplit(("", "", quote(relative, safe="/"), parts.query, parts.fragment))


def copy_contents(target, source):
    target.clear()
    for child in source.contents:
        target.append(copy.deepcopy(child))


def set_text(target, value):
    target.clear()
    target.append(str(value))


def mark(target, index, item=None):
    current = target.get("data-candidate-blocks", "").split()
    value = str(index)
    if value not in current:
        current.append(value)
    target["data-candidate-blocks"] = " ".join(current)
    if item is not None:
        items = target.get("data-candidate-items", "").split()
        item_value = f"{index}:{item}"
        if item_value not in items:
            items.append(item_value)
        target["data-candidate-items"] = " ".join(items)


def href_attrs(source_soup, source_path):
    result = {}
    for anchor in source_soup.select("a[href]"):
        key = local_target_key(anchor["href"], source_path.parent)
        result.setdefault(key, {})
        for attr in ("target", "rel", "download"):
            if anchor.has_attr(attr):
                result[key][attr] = copy.deepcopy(anchor[attr])
    return result


def parse_card_item(item):
    title_node = item.find("strong", recursive=False)
    require(title_node is not None, "圖卡候選項目缺少標題")
    title = normalized(title_node.get_text(" ", strip=True))
    match = re.fullmatch(r"(.+?)（([^（）]+)）", title)
    require(match is not None, f"圖卡標題須明列名稱與原標籤：{title}")
    name, tag = match.group(1).strip(), f"（{match.group(2).strip()}）"

    summary_nodes = []
    passed_title = False
    first_break = False
    for child in item.contents:
        if child is title_node:
            passed_title = True
            continue
        if not passed_title:
            continue
        if isinstance(child, Tag) and child.name == "br":
            if first_break:
                break
            first_break = True
            continue
        if isinstance(child, Tag) and child.name == "a":
            break
        if first_break:
            summary_nodes.append(copy.deepcopy(child))
    summary = normalized(" ".join(
        node.get_text(" ", strip=True) if isinstance(node, Tag) else str(node)
        for node in summary_nodes
    ))
    require(summary, f"圖卡缺少說明：{name}")
    links = item.select("a[href]")
    require(links, f"圖卡缺少素材連結：{name}")
    return name, tag, summary_nodes, links


def apply_tool_grid(soup, grid, candidate_list, source_path):
    cards = grid.select(".tool-card")
    items = candidate_list.find_all("li", recursive=False)
    require(len(cards) == len(items), "候選圖卡數與原圖卡數不同，不能保留原圖卡版型")
    for item_index, (card, item) in enumerate(zip(cards, items), 1):
        name, tag, summary_nodes, links = parse_card_item(item)
        name_target = card.select_one(".tool-name")
        tag_target = card.select_one(".tool-tag")
        summary_target = card.select_one(".tool-summary")
        require(name_target and tag_target and summary_target, "原圖卡缺少名稱、標籤或說明槽位")
        set_text(name_target, name)
        set_text(tag_target, tag)
        summary_target.clear()
        for node in summary_nodes:
            summary_target.append(node)

        for link in links:
            key = local_target_key(link["href"], source_path.parent)
            matches = [a for a in card.select("a[href]")
                       if local_target_key(a["href"], source_path.parent) == key]
            require(matches, f"候選圖卡連結不在原圖卡素材內：{link.get_text(' ', strip=True)}")
            text_target = next((a for a in card.select(".tool-list-item a[href]")
                                if local_target_key(a["href"], source_path.parent) == key), None)
            if text_target is None:
                list_target = card.select_one(".tool-list")
                if list_target is None:
                    list_target = soup.new_tag("div", attrs={"class": ["tool-list"]})
                    card.append(list_target)
                row = soup.new_tag("div", attrs={"class": ["tool-list-item"]})
                arrow = soup.new_tag("span", attrs={"class": ["tool-check"]})
                arrow.string = "→"
                text_target = soup.new_tag("a", attrs={"href": matches[0]["href"]})
                for attr in ("target", "rel", "download"):
                    if matches[0].has_attr(attr):
                        text_target[attr] = copy.deepcopy(matches[0][attr])
                row.append(arrow)
                row.append(text_target)
                list_target.append(row)
            set_text(text_target, normalized(link.get_text(" ", strip=True)))
        mark(card, candidate_list["data-candidate-block"], item_index)
    mark(grid, candidate_list["data-candidate-block"])


def step_parts(item):
    title = item.find("strong", recursive=False)
    require(title is not None, "步驟候選項目缺少粗體動作標題")
    heading = normalized(title.get_text(" ", strip=True))
    rest = []
    passed = False
    first_content = True
    separator = ""
    for child in item.contents:
        if child is title:
            passed = True
            continue
        if not passed:
            continue
        if first_content and isinstance(child, Tag) and child.name == "br":
            first_content = False
            continue
        if first_content and isinstance(child, NavigableString):
            value = str(child)
            match = re.match(r"^\s*([：:])\s*", value)
            if match:
                separator = match.group(1)
                value = value[match.end():]
                if value:
                    rest.append(NavigableString(value))
                first_content = False
                continue
        if isinstance(child, NavigableString) and first_content and not str(child).strip():
            continue
        first_content = False
        rest.append(copy.deepcopy(child))
    require(rest, f"步驟缺少說明：{heading}")
    return heading + separator, rest


def apply_steps(soup, wrapper, candidate_list):
    source_steps = wrapper.select(".step-block")
    items = candidate_list.find_all("li", recursive=False)
    require(len(source_steps) == len(items), "候選步驟數與原步驟卡數不同")
    for item_index, (step, item) in enumerate(zip(source_steps, items), 1):
        content = step.select_one(".step-content")
        heading_target = content.select_one(".step-heading") if content else None
        body_target = content.select_one(".step-body") if content else None
        circle = step.select_one(".step-circle")
        require(content and heading_target and body_target and circle, "原步驟卡缺少必要槽位")
        heading, body_nodes = step_parts(item)
        set_text(heading_target, heading)
        body_target.clear()
        paragraph = soup.new_tag("p")
        for node in body_nodes:
            paragraph.append(node)
        body_target.append(paragraph)
        set_text(circle, item_index)
        mark(step, candidate_list["data-candidate-block"], item_index)
    mark(wrapper, candidate_list["data-candidate-block"])


def apply_table(target, candidate_table):
    source_rows = target.find_all("tr")
    candidate_rows = candidate_table.find_all("tr")
    require(len(source_rows) == len(candidate_rows), "候選表格列數與原表不同")
    for source_row, candidate_row in zip(source_rows, candidate_rows):
        source_cells = source_row.find_all(["th", "td"], recursive=False)
        candidate_cells = candidate_row.find_all(["th", "td"], recursive=False)
        require(len(source_cells) == len(candidate_cells), "候選表格欄數與原表不同")
        for source_cell, candidate_cell in zip(source_cells, candidate_cells):
            require(source_cell.name == candidate_cell.name, "候選表格表頭／資料格語意與原表不同")
            copy_contents(source_cell, candidate_cell)
    mark(target, candidate_table["data-candidate-block"])


def quote_contents(block, marker):
    paragraphs = block.find_all("p", recursive=False)
    require(len(paragraphs) == 1, "引言候選須為單段，避免遺失段落關係")
    children = list(paragraphs[0].contents)
    first_index = next((i for i, child in enumerate(children)
                        if isinstance(child, Tag) or str(child).strip()), None)
    if marker is not None:
        require(first_index is not None and isinstance(children[first_index], Tag)
                and children[first_index].name == "strong"
                and normalized(children[first_index].get_text(" ", strip=True)) == normalized(marker),
                "候選引言標記與原圖示／標籤不同")
        children = children[first_index + 1:]
        if children and isinstance(children[0], Tag) and children[0].name == "br":
            children = children[1:]
    return [copy.deepcopy(child) for child in children]


def apply_quote(section, selector, block):
    matches = section.select(selector)
    require(len(matches) == 1, f"引言映射非唯一：{selector}")
    target = matches[0]
    if "intro-band" in target.get("class", []):
        label = target.select_one(".intro-label")
        body = target.select_one(".intro-text")
        require(label and body, "原任務引言缺少文字槽位")
        contents = quote_contents(block, label.get_text(" ", strip=True))
        body.clear()
        for child in contents:
            body.append(child)
        mapped_target = target
    elif "big-quote" in target.get("class", []):
        paragraphs = block.find_all("p", recursive=False)
        require(len(paragraphs) == 1, "結尾引言須為單段")
        copy_contents(target, paragraphs[0])
        mapped_target = target
    else:
        icon = target.select_one(".callout-icon")
        body = target.select_one(".callout-body")
        require(icon and body, "原callout缺少圖示或正文槽位")
        contents = quote_contents(block, icon.get_text(" ", strip=True))
        body.clear()
        for child in contents:
            body.append(child)
        mapped_target = target
    require(normalized(mapped_target.get_text(" ", strip=True)) == normalized(block.get_text(" ", strip=True)),
            "引言文字映射與候選不符")
    mark(mapped_target, block["data-candidate-block"])


def component_counts(soup, selectors):
    return {selector: len(soup.select(selector)) for selector in selectors}


def build_component_preview(confirmation_path, mapping_path, output, receipt, source,
                           candidate, plan, soup, nodes, link_attributes,
                           require_preserved_controls):
    """Preserve original course components and apply candidate text into their slots."""
    require(plan.get("layout_strategy") == "preserve-existing-components",
            "缺少保留原元件版型策略")
    require(plan.get("extended_blocks") is True, "此映射須啟用擴充Markdown區塊")
    source_path = Path(source["path"]).resolve()
    candidate_path = Path(candidate["path"]).resolve()
    origin = source_path.parent
    require(len(nodes) > 1 and nodes[0].name == "h1", "候選缺少唯一頁面H1")
    require(normalized(nodes[0].get_text()) == normalized(soup.h1.get_text()), "候選標題與原頁不同")
    allowed = {"h1", "h2", "h3", "p", "pre", "ol", "ul", "table", "blockquote", "hr"}
    require(all(n.name in allowed for n in nodes), "候選含未支援區塊")
    candidate_blocks = nodes[1:]
    for index, node in enumerate(candidate_blocks):
        node["data-candidate-block"] = str(index)
    mapped = set()
    records = []

    def record(node, target, mode, mapped_text=None):
        if node.name == "h1":
            records.append({"index": -1, "tag": node.name,
                            "text": normalized(node.get_text(" ", strip=True)),
                            "target": target, "mode": mode,
                            "mapped_text": mapped_text})
            return
        index = int(node["data-candidate-block"])
        require(index not in mapped, f"候選區塊重複映射：{index}")
        mapped.add(index)
        records.append({"index": index, "tag": node.name,
                        "text": normalized(node.get_text(" ", strip=True)),
                        "target": target, "mode": mode,
                        "mapped_text": mapped_text})

    intro, groups, current = [], [], None
    for node in candidate_blocks:
        if node.name == "h2":
            if current is not None:
                groups.append(current)
            current = [node]
        elif current is None:
            intro.append(node)
        else:
            current.append(node)
    if current is not None:
        groups.append(current)
    require(len(groups) == plan.get("expected_section_count"), "候選區段數與映射不符")
    require(intro and intro[-1].name == "hr", "頁首候選缺少與原頁殼層對應的分隔")
    intro_boundary = intro.pop()
    require([n.name for n in intro] == ["p", "p", "h3", "ul"], "頁首區塊順序與原頁Hero不符")

    hero = soup.select_one(".page-hero")
    body = soup.select_one(".lesson-body")
    back = hero.select_one(".back-link") if hero else None
    tagline = hero.select_one(".lesson-tagline") if hero else None
    outcome_label = hero.select_one(".outcomes-label") if hero else None
    outcomes = hero.select_one(".outcomes") if hero else None
    require(hero and body and back and tagline and outcome_label and outcomes,
            "原頁缺少可承接候選頁首的Hero元件")
    require(normalized(intro[0].get_text(" ", strip=True)) == normalized(tagline.get_text(" ", strip=True)),
            "候選導言與原Hero文案不同")
    candidate_back = intro[1].select("a[href]")
    require(len(candidate_back) == 1 and normalized(candidate_back[0].get_text(" ", strip=True))
            == normalized(back.get_text(" ", strip=True)), "候選返回連結標籤與原Hero不同")
    require(local_target_key(candidate_back[0]["href"], candidate_path.parent)
            == local_target_key(back["href"], origin), "候選返回連結目的地與原Hero不同")
    require(normalized(intro[2].get_text(" ", strip=True)) == normalized(outcome_label.get_text(" ", strip=True)),
            "候選學習成果標籤與原Hero不同")
    candidate_outcomes = [normalized(x.get_text(" ", strip=True)) for x in intro[3].find_all("li", recursive=False)]
    source_outcomes = [normalized(x.get_text(" ", strip=True)) for x in outcomes.select(".outcome-item")]
    require(candidate_outcomes == source_outcomes, "候選學習成果與原Hero不同")
    mark(tagline, intro[0]["data-candidate-block"])
    mark(back, intro[1]["data-candidate-block"])
    mark(outcome_label, intro[2]["data-candidate-block"])
    mark(outcomes, intro[3]["data-candidate-block"])
    mark(body, intro_boundary["data-candidate-block"])
    record(nodes[0], "h1", "source-title-equal")
    for node, target, mode in zip(intro, [".lesson-tagline", ".back-link", ".outcomes-label", ".outcomes"],
                                  ["shell-copy-equal", "shell-link-equal", "shell-label-equal", "shell-list-equal"]):
        record(node, target, mode)
    record(intro_boundary, ".page-hero > .lesson-body boundary", "existing-shell-spacing")

    last_group = groups[-1]
    tail_split = next((i for i, node in enumerate(last_group)
                       if node.name == "hr" and len(last_group) - i - 1 == 2
                       and all(x.name == "p" for x in last_group[i + 1:])), None)
    require(tail_split is not None, "候選頁尾未能明確映射到原頁nav/footer")
    tail_separator = last_group[tail_split]
    tail = last_group[tail_split + 1:]
    groups[-1] = last_group[:tail_split]
    require([n.name for n in tail] == ["p", "p"], "候選頁尾區塊格式不符原頁殼層")
    nav = soup.select_one(".nav-footer")
    footer = soup.select_one("footer")
    require(nav and footer, "原頁缺少導覽或頁尾殼層")
    candidate_nav_links = tail[0].select("a[href]")
    source_nav_links = nav.select("a[href]")
    require(len(candidate_nav_links) == len(source_nav_links) == 2,
            "候選頁尾導覽連結數與原殼層不同")
    require([normalized(a.get_text(" ", strip=True)) for a in candidate_nav_links]
            == [normalized(a.get_text(" ", strip=True)) for a in source_nav_links],
            "候選頁尾導覽標籤與原殼層不同")
    require(local_target_key(candidate_nav_links[0]["href"], candidate_path.parent)
            == local_target_key(source_nav_links[0]["href"], origin),
            "候選課程首頁連結目的地與原殼層不同")
    candidate_footer_parts = [normalized(part) for part in tail[1].get_text(" ", strip=True).split("｜")]
    source_footer_parts = [normalized(footer.select_one(selector).get_text(" ", strip=True))
                           for selector in (".footer-logo", ".footer-note", ".footer-meta")]
    require(candidate_footer_parts == source_footer_parts,
            "候選頁尾文字分段與原頁footer元件不同")
    mark(nav, tail[0]["data-candidate-block"])
    mark(footer, tail[1]["data-candidate-block"])
    mark(nav, tail_separator["data-candidate-block"])
    record(tail_separator, ".lesson-body > .nav-footer boundary", "existing-shell-spacing")
    record(tail[0], ".nav-footer", "shell-navigation-equal")
    record(tail[1], "footer", "shell-footer-equal",
           normalized(" ｜ ".join(source_footer_parts)))

    rules = plan.get("sections")
    sections = soup.select(".lesson-body > .lesson-section")
    require(isinstance(rules, list) and len(rules) == len(groups) == len(sections),
            "原頁區段數與映射清單不符")
    section_rules = soup.select("main hr.section-rule")
    require(len(section_rules) == len(sections) - 1, "原頁區段分隔數不符")
    candidate_pres = 0
    for section_index, (group, section, rule) in enumerate(zip(groups, sections, rules), 1):
        require(group and group[0].name == "h2", f"第{section_index}節候選標題缺漏")
        require(len(group) > 1 and group[-1].name == "hr" if section_index < len(sections) else True,
                f"第{section_index}節分隔映射缺漏")
        separator = group.pop() if section_index < len(sections) else None
        if section_index == len(sections):
            require(not any(n.name == "hr" for n in group), "最後一節含未對應的水平線")
        target_matches = soup.select(rule.get("selector", ""))
        require(len(target_matches) == 1 and target_matches[0] is section,
                f"第{section_index}節selector未唯一對應原區段")
        eyebrow = section.find(class_="section-eyebrow", recursive=False)
        heading_target = section.find("h2", class_="section-heading", recursive=False)
        require(eyebrow and heading_target, f"第{section_index}節缺少原eyebrow或H2")
        prefix = normalized(eyebrow.get_text(" ", strip=True))
        candidate_heading = normalized(group[0].get_text(" ", strip=True))
        require(candidate_heading.startswith(prefix), f"第{section_index}節標題前綴與原eyebrow不同")
        title = candidate_heading[len(prefix):].strip()
        require(title, f"第{section_index}節缺少標題文字")
        set_text(heading_target, title)
        mark(heading_target, group[0]["data-candidate-block"])
        record(group[0], rule["selector"] + " > h2.section-heading + eyebrow", "split-existing-eyebrow",
               normalized(prefix + " " + title))

        content = group[1:]
        require(all(n.name in {"p", "h3", "pre", "ol", "ul", "table", "blockquote"} for n in content),
                f"第{section_index}節有未支援內容區塊")
        quote_targets = list(rule.get("blockquote_targets", []))
        quote_index = 0
        body_targets = section.find_all("p", class_="body-text", recursive=False)
        body_cursor = 0
        direct_h3 = section.find_all("h3", recursive=False)
        h3_cursor = 0
        for position, block in enumerate(content):
            tag = block.name
            block_id = block["data-candidate-block"]
            if tag == "p":
                if body_cursor < len(body_targets):
                    target = body_targets[body_cursor]
                elif body_targets:
                    target = copy.deepcopy(body_targets[-1])
                    target.clear()
                    body_targets[-1].insert_after(target)
                    body_targets.append(target)
                else:
                    target = soup.new_tag("p", attrs={"class": ["body-text"]})
                    anchor = section.select_one(".table-scroll")
                    if anchor is None:
                        anchor = section.select_one(".callout")
                    if anchor is None:
                        section.append(target)
                    else:
                        anchor.insert_before(target)
                    body_targets.append(target)
                copy_contents(target, block)
                mark(target, block_id)
                record(block, rule["selector"] + " > p.body-text", "replace-or-add-copy")
                body_cursor += 1
            elif tag == "h3":
                if h3_cursor < len(direct_h3):
                    target = direct_h3[h3_cursor]
                    h3_cursor += 1
                    require("step-heading" in target.get("class", []), "原H3沒有相容的既有標籤")
                else:
                    target = soup.new_tag("h3", attrs={"class": ["step-heading"]})
                    following = content[position + 1:]
                    next_block = next((x for x in following if x.name in ("ol", "table", "p")), None)
                    if next_block is not None and next_block.name == "ol":
                        anchor = section.select_one(".steps-wrap")
                    else:
                        anchor = section.select_one(".table-scroll")
                    require(anchor is not None, "新增候選H3缺少原版型插入位置")
                    anchor.insert_before(target)
                copy_contents(target, block)
                mark(target, block_id)
                record(block, rule["selector"] + " > h3.step-heading", "existing-or-inline-subheading")
            elif tag == "blockquote":
                require(quote_index < len(quote_targets), f"第{section_index}節引言映射不足")
                selector = quote_targets[quote_index]
                apply_quote(section, selector, block)
                record(block, rule["selector"] + " " + selector, "update-existing-callout-or-quote")
                quote_index += 1
            elif tag == "ul":
                grid = section.select(".tool-grid")
                require(len(grid) == 1, f"第{section_index}節候選清單沒有唯一原圖卡區")
                apply_tool_grid(soup, grid[0], block, source_path)
                record(block, rule["selector"] + " .tool-grid", "update-card-copy-preserve-images")
            elif tag == "ol":
                wrappers = section.select(".steps-wrap")
                require(len(wrappers) == 1, f"第{section_index}節候選步驟沒有唯一原步驟區")
                apply_steps(soup, wrappers[0], block)
                record(block, rule["selector"] + " .steps-wrap", "update-step-copy-preserve-wrapper")
            elif tag == "table":
                tables = section.select(".table-scroll table")
                require(len(tables) == 1, f"第{section_index}節候選表格沒有唯一原表格")
                apply_table(tables[0], block)
                record(block, rule["selector"] + " .table-scroll table", "update-cells-preserve-table")
            elif tag == "pre":
                candidate_pres += 1
                text = block.get_text().strip()
                matches = [pre for pre in section.select("pre") if pre.get_text().strip() == text]
                require(len(matches) == 1, f"第{section_index}節提示詞無唯一原節點對應")
                mark(matches[0], block_id)
                record(block, rule["selector"] + " pre", "preserve-exact-prompt")
        require(quote_index == len(quote_targets), f"第{section_index}節原callout映射未完整使用")
        require(body_cursor >= len(section.find_all("p", class_="body-text", recursive=False)),
                f"第{section_index}節原body-text有未映射內容")
        require(h3_cursor == len(direct_h3), f"第{section_index}節原H3有未映射內容")
        if separator is not None:
            mark(section_rules[section_index - 1], separator["data-candidate-block"])
            record(separator, f"main hr.section-rule[{section_index}]", "preserve-existing-section-rule")

    require(candidate_pres == len(soup.select(".lesson-body pre")), "候選提示詞數與原提示詞數不同")
    require(mapped == set(range(len(candidate_blocks))), "部分候選區塊未映射或重複映射")
    required_links = []
    for node in candidate_blocks:
        for anchor in node.select("a[href]"):
            key = local_target_key(anchor["href"], candidate_path.parent)
            if urlsplit(anchor["href"]).scheme or urlsplit(anchor["href"]).netloc:
                continue
            if not urlsplit(anchor["href"]).path and urlsplit(anchor["href"]).fragment:
                continue
            required_links.append(key)
    source_links = {local_target_key(a["href"], origin) for a in BeautifulSoup(
        Path(source["path"]).read_text(encoding="utf-8"), "html.parser").select("a[href]")}
    require(set(required_links) <= source_links, "候選新增原稿沒有的連結目的地")

    components = [".lesson-body", ".lesson-section", ".section-eyebrow", ".section-rule",
                  ".tool-grid", ".tool-card", ".steps-wrap", ".step-block", ".callout",
                  ".table-scroll", ".lesson-table", ".nav-footer", ".page-hero", "img", "pre"]
    before_counts = component_counts(BeautifulSoup(Path(source["path"]).read_text(encoding="utf-8"), "html.parser"), components)
    require(plan.get("preserved_component_counts") == before_counts,
            "映射宣告的原版型元件數與來源實際數量不同")
    after_counts = component_counts(soup, components)
    require(after_counts == before_counts, "預覽變更了原版型、圖卡、提示詞或圖片元件數量")

    for node in soup.find_all(True):
        if node.name == "a" and node.has_attr("href"):
            key = rebase_url(node["href"], origin, Path("/"))
            for attr, value in link_attributes.get(key, {}).items():
                node[attr] = copy.deepcopy(value)
        for attr in ("href", "src"):
            if node.has_attr(attr):
                node[attr] = rebase_url(node[attr], origin, output)
    ids = [node["id"] for node in soup.select("[id]")]
    require(len(ids) == len(set(ids)), "預覽有重複id")
    require_preserved_controls(source_path, soup)

    for node in soup.select("a[href],img[src],source[src]"):
        attr = "href" if node.name == "a" else "src"
        url = node[attr]
        parts = urlsplit(url)
        if parts.scheme or parts.netloc:
            continue
        if not parts.path:
            if parts.fragment:
                require(soup.find(id=unquote(parts.fragment)) is not None,
                        f"預覽錨點不存在：{parts.fragment}")
            continue
        target = Path(unquote(parts.path))
        if not target.is_absolute():
            target = output / target
        require(target.resolve().exists(), f"預覽本機連結不存在：{url}")

    output.mkdir(parents=True)
    (output / "original.html").write_bytes(source_path.read_bytes())
    (output / "candidate.md").write_bytes(candidate_path.read_bytes())
    (output / "mapping.json").write_bytes(Path(mapping_path).read_bytes())
    preview = output / "preview.html"
    preview.write_text(str(soup), encoding="utf-8")
    manifest = {
        "schema_version": "handout-preview-components-1",
        "status": "pending_browser_checks",
        "task_scope": "content-change",
        "layout_strategy": "preserve-existing-components",
        "source": source,
        "candidate": candidate,
        "confirmation": artifact(confirmation_path),
        "feedback": receipt["feedback"],
        "h3": receipt,
        "mapping": artifact(mapping_path),
        "preview": artifact(preview),
        "blocks": records,
        "preserved_component_counts": before_counts,
        "image_count_preserved": before_counts["img"],
        "protected_pre_count": candidate_pres,
        "formal_overwrite": False,
        "published": False,
    }
    save(output / "manifest.json", manifest)
    return manifest
