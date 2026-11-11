"""將H3確認候選套入原頁殼層，僅產生隔離預覽，沒有發布入口。"""
import copy
from collections import Counter
import json
import os
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from bs4 import BeautifulSoup, Tag
from markdown_it import MarkdownIt

from src.course_improvement_loop import artifact, digest, read_json, require, save
from src.course_loop_stages import check_inputs, load_stage, stage_status
from src.course_handout_component_overlay import build_component_preview


def require_preserved_controls(source_path, preview):
    """動態表單容器在JS執行前也必須存在，不能只保留script。"""
    original = BeautifulSoup(Path(source_path).read_text(encoding="utf-8"), "html.parser")
    def signatures(soup):
        return Counter((n.name, tuple((k, str(n.get(k, ""))) for k in
                       ("id", "name", "type", "data-gen36-form", "data-action")))
                       for n in soup.select("[data-gen36-form],form,input,textarea,select,button"))
    missing = signatures(original) - signatures(preview)
    require(not missing, "套用遺失原操作元件或動態表單容器；請明確映射並保留原DOM")


def rebase_url(url, origin, destination):
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or not parts.path:
        return url
    target = Path(unquote(parts.path))
    if not target.is_absolute():
        target = origin / target
    relative = os.path.relpath(target.resolve(), destination)
    return urlunsplit(("", "", quote(relative, safe="/"), parts.query, parts.fragment))


def normalized(text):
    return " ".join(text.split())


def preflight_candidate(source_path, candidate_path, output_path=None):
    """H3前檢查HTML候選的基本相容性；不產製預覽，也不確認內容。"""
    source_path = Path(source_path).resolve(strict=True)
    candidate_path = Path(candidate_path).resolve(strict=True)
    require(source_path.suffix.lower() in (".html", ".htm"), "來源必須是HTML講義")
    source_soup = BeautifulSoup(source_path.read_text(encoding="utf-8"), "html.parser")
    candidate_text = candidate_path.read_text(encoding="utf-8")
    rendered = BeautifulSoup(MarkdownIt("commonmark", {"html": True}).enable("table").render(candidate_text),
                            "html.parser")
    nodes = list(rendered.find_all(recursive=False))
    findings = []

    source_titles = source_soup.select("h1")
    candidate_title = normalized(nodes[0].get_text()) if nodes and nodes[0].name == "h1" else None
    source_title = normalized(source_titles[0].get_text()) if len(source_titles) == 1 else None
    if source_title is None:
        findings.append({"severity": "blocker", "code": "source_h1_not_unique",
                         "message": "原頁沒有唯一H1，需先確認標題對應。"})
    if candidate_title is None:
        findings.append({"severity": "blocker", "code": "candidate_h1_missing",
                         "message": "候選第一個區塊必須是H1。"})
    elif source_title is not None and candidate_title != source_title:
        findings.append({"severity": "blocker", "code": "h1_mismatch",
                         "message": "候選H1與原頁不同；若要套用至此講義，先對齊標題再進行H3。"})

    bodies = source_soup.select(".lesson-body")
    if len(bodies) != 1:
        findings.append({"severity": "blocker", "code": "lesson_body_not_unique",
                         "message": "原頁沒有唯一.lesson-body，無法沿用現有套用器。"})
    allowed = {"h1", "h2", "p", "pre", "ol", "ul", "table", "h3", "h4",
               "blockquote", "details", "hr"}
    unsupported = [node.name for node in nodes if node.name not in allowed]
    if unsupported:
        findings.append({"severity": "blocker", "code": "unsupported_candidate_blocks",
                         "message": "候選含目前套用器不支援的區塊：" + ", ".join(unsupported)})

    section_count = len(bodies[0].select(".lesson-section")) if len(bodies) == 1 else None
    candidate_section_count = sum(node.name == "h2" for node in nodes)
    if section_count is not None and section_count != candidate_section_count:
        findings.append({"severity": "review", "code": "section_count_differs",
                         "message": "候選H2數與原頁區段數不同，需由映射明確處理分合。"})

    component_selectors = {
        "pre": "pre", "tables": "table", "images": "img", "buttons": "button",
        "forms": "form", "inputs": "input,textarea,select",
        "cards": ".card,.step,.callout", "dynamic_hosts": "[data-gen36-form]",
    }
    protected = ({key: len(bodies[0].select(selector)) for key, selector in component_selectors.items()}
                 if len(bodies) == 1 else {})
    if any(protected.values()):
        findings.append({"severity": "review", "code": "existing_components_need_mapping",
                         "message": "原頁含需保留或逐一對應的圖卡、操作元件或素材；H3後產製預覽前仍須完成元件映射。"})

    blockers = [item for item in findings if item["severity"] == "blocker"]
    result = {
        "schema_version": "handout-preflight-1",
        "status": "blocked" if blockers else "passed",
        "source": artifact(source_path),
        "candidate": artifact(candidate_path),
        "source_h1": source_title,
        "candidate_h1": candidate_title,
        "source_section_count": section_count,
        "candidate_h2_count": candidate_section_count,
        "protected_component_counts": protected,
        "findings": findings,
        "layout_mapping_required": True,
        "preview_created": False,
        "h3_confirmed": False,
    }
    if output_path is not None:
        output_path = Path(output_path).resolve()
        require(not output_path.exists(), "預檢報告已存在；不覆寫既有紀錄")
        require(output_path not in (source_path, candidate_path), "預檢報告不可覆寫輸入檔")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result["report"] = str(output_path)
        with output_path.open("x", encoding="utf-8") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    return result


def build_confirmed_preview(confirmation_path, mapping_path, output):
    """接收獨立H3，不更改追加候選所屬的歷史控制器。"""
    confirmation_path, mapping_path, output = map(lambda p: Path(p).resolve(),
                                                 (confirmation_path, mapping_path, output))
    require(not output.exists(), "預覽目錄已存在；保留既有版本，不覆寫")
    receipt = read_json(confirmation_path)
    require(receipt.get("schema_version") == "handout-confirmation-1"
            and receipt.get("status") == "confirmed" and receipt.get("actor"), "缺少獨立H3確認")
    for key in ("source", "candidate", "feedback"):
        require(digest(receipt[key]["path"]) == receipt[key]["sha256"], f"H3的{key}版本已變")
    require(Path(receipt["feedback"]["path"]).read_text().strip(), "H3缺少使用者原話")
    source, candidate = receipt["source"], receipt["candidate"]
    require(not Path(source["path"]).is_relative_to(output), "預覽不能包含正式來源")
    plan = read_json(mapping_path)
    require(plan.get("task_scope") == "content-change" and plan.get("reason"), "須明列套用範圍")
    soup = BeautifulSoup(Path(source["path"]).read_text(), "html.parser")
    require(len(soup.select(".lesson-body")) == 1, "須有唯一lesson-body")
    link_attributes = {rebase_url(a["href"], Path(source["path"]).parent, Path("/")):
                       {k: copy.deepcopy(a[k]) for k in ("target", "rel", "download") if a.has_attr(k)}
                       for a in soup.select("a[href]")}
    extended = plan.get("extended_blocks") is True
    rendered = BeautifulSoup(MarkdownIt("commonmark", {"html": extended}).enable("table").render(
        Path(candidate["path"]).read_text()), "html.parser")
    nodes = list(rendered.find_all(recursive=False))
    require(nodes and nodes[0].name == "h1", "候選缺少標題")
    require(normalized(nodes[0].get_text()) == normalized(soup.h1.get_text()), "頁首標題不同")
    allowed = {"h1", "h2", "p", "pre", "ol", "ul", "table"}
    if extended:
        allowed.update(("h3", "h4", "blockquote", "details", "hr"))
        require(not rendered.select("script,style,iframe,form,input,button"), "候選含未授權操作或程式")
    require(all(n.name in allowed for n in nodes),
            "候選包含未支援區塊")
    if plan.get("layout_strategy") == "preserve-existing-components":
        return build_component_preview(confirmation_path, mapping_path, output, receipt,
                                       source, candidate, plan, soup, nodes,
                                       link_attributes, require_preserved_controls)
    groups = {"intro": []}
    heading = "intro"
    for i, node in enumerate(nodes[1:]):
        node["data-candidate-block"] = str(i)
        if node.name == "h2":
            heading = node.get_text()
            require(heading not in groups, "重複候選標題")
            groups[heading] = []
        groups[heading].append(node)
    if plan.get("intro_groups"):
        intro = groups.pop("intro")
        allocated = []
        split = {}
        for key, indices in plan["intro_groups"].items():
            require(key not in groups and isinstance(indices, list), "頁首映射識別碼重複或格式錯誤")
            require(all(isinstance(i, int) and 0 <= i < len(intro) for i in indices), "頁首區塊索引無效")
            split[key] = [intro[i] for i in indices]
            allocated.extend(indices)
        require(allocated == list(range(len(intro))), "頁首映射須依序完整涵蓋每個區塊，不可遺漏或重複")
        groups = {**split, **groups}
    require(list(plan["groups"]) == list(groups), "映射須完整且依候選順序")
    targets = []
    for key, spec in plan["groups"].items():
        matches = soup.select(spec["selector"])
        require(len(matches) == 1, f"映射非唯一：{key}")
        targets.append(matches[0])
    require(len({id(n) for n in targets}) == len(targets), "映射重複目標")
    require(not any(a in b.parents or b in a.parents for a in targets for b in targets if a is not b),
            "映射目標不可互相包含")
    pres = list(soup.select(".lesson-body pre"))
    if plan.get("preserve_prompt_controls"):
        pres += [n for n in soup.select(".lesson-body [data-policy-prompt]") if n not in pres]
    preserved = {}
    for selector in plan.get("preserve_dom", []):
        matches = soup.select(selector)
        require(len(matches) == 1 and matches[0].find_parent(class_="lesson-body"), "保留元件須唯一且在正文內")
        owner = next((i for i, target in enumerate(targets) if target in matches[0].parents), None)
        require(owner is not None, "保留元件缺少區段映射")
        preserved.setdefault(owner, []).append(copy.deepcopy(matches[0]))
    controls = {n.get("id"): [copy.deepcopy(row) for row in soup.select(".policy-copy-row")
                              if row.select_one(f'[data-policy-copy="{n.get("id")}"]')]
                for n in pres if n.get("id")}
    prompt_parents = [n.parent for n in pres]
    used, blocks = [], []
    for group_index, ((key, children), target) in enumerate(zip(groups.items(), targets)):
        spec = plan["groups"][key]
        mode = spec["mode"]
        if spec.get("id"):
            require(not target.get("id") or target["id"] == spec["id"], "不可更改原錨點")
            target["id"] = spec["id"]
        if mode == "section":
            require("lesson-section" in target.get("class", []) and target.find_parent(class_="lesson-body"),
                    "區段須在lesson-body內")
            for old in list(target.contents):
                if not (isinstance(old, Tag) and "section-eyebrow" in old.get("class", [])):
                    old.extract()
        else:
            require(mode in ("intro", "outcomes", "agenda"), "未知映射模式")
            if children:
                target.clear()
        for node in children:
            label = spec.get("markdown_label")
            if label and node.name == "p" and node.get_text().startswith("**" + label + "**"):
                # 只將明列的頁首粗體標記轉為HTML；不更動候選檔或標籤後文字。
                require(len(node.contents) == 1 and isinstance(node.contents[0], str), "頁首粗體標記不是單一文字節點")
                tail = node.get_text()[len(label) + 4:]
                node.clear()
                strong = soup.new_tag("strong"); strong.string = label
                node.append(strong); node.append(tail)
            tag, index, text = node.name, node["data-candidate-block"], node.get_text()
            if plan.get("preserve_prompt_controls") and tag == "p" and any(
                    old.get_text().strip() == text.strip() for old in pres):
                # 候選把原pre寫成普通段落時，仍使用原提示詞節點與控制項。
                tag = "pre"
            if mode == "intro":
                require(tag == "p", "導言僅支援段落")
                container = target
                for item in list(node.contents):
                    container.append(item.extract())
                container["data-candidate-block"] = index
            elif mode == "outcomes":
                require(tag in ("h2", "p") or (extended and tag in ("ul", "ol")), "完成物映射不支援此區塊")
                if tag in ("ul", "ol"):
                    node["class"] = ["handout-list"]
                    target.append(node)
                    blocks.append({"index": int(index), "tag": tag, "text": text})
                    continue
                container = soup.new_tag("strong" if tag == "h2" else "span")
                container["data-candidate-block"] = index
                for item in list(node.contents): container.append(item.extract())
                target.append(container)
            else:
                container = node
                if tag == "h2":
                    node["class"] = ["section-heading"] if mode == "section" else ["agenda-heading"]
                elif tag == "p" and mode == "section": node["class"] = ["body-text"]
                elif tag in ("ol", "ul"):
                    node["class"] = ["handout-list"]
                    if mode == "agenda":
                        for li in node.find_all("li", recursive=False): li["class"] = ["agenda-topic"]
                elif tag == "pre":
                    matches = [j for j, old in enumerate(pres) if j not in used
                               and old.get_text().strip() == text.strip()]
                    require(len(matches) == 1, "提示詞無唯一原節點對應")
                    j = matches[0]; used.append(j)
                    parent = prompt_parents[j]
                    if plan.get("preserve_prompt_controls"):
                        # 逐一保留提示詞葉節點與其複製控制，避免複製含另一段提示詞的整個父層。
                        leaf = copy.deepcopy(pres[j])
                        leaf["data-candidate-block"] = index
                        if parent is target:
                            container = soup.new_tag("div", attrs={"class": ["handout-prompt-group"]})
                        else:
                            container = soup.new_tag(parent.name, attrs=copy.deepcopy(parent.attrs))
                        container.append(leaf)
                        for row in controls.get(pres[j].get("id"), []): container.append(row)
                        if "tool-body" in parent.get("class", []):
                            wrap = soup.new_tag(parent.parent.name, attrs=copy.deepcopy(parent.parent.attrs))
                            head = parent.parent.select_one(":scope > .tool-head")
                            if head: wrap.append(copy.deepcopy(head))
                            wrap.append(container); container = wrap
                    else:
                        # 舊映射保留原有處理，不改變歷史預覽行為。
                        container = copy.deepcopy(parent if "prompt" in " ".join(parent.get("class", [])) else pres[j])
                        (container if container.name == "pre" else container.find("pre"))["data-candidate-block"] = index
                if tag == "table":
                    wrap = soup.new_tag("div", attrs={"class": ["handout-table-scroll"],
                                                      "tabindex": "0", "role": "region", "aria-label": "可左右捲動的表格"})
                    wrap.append(container); target.append(wrap)
                else: target.append(container)
            blocks.append({"index": int(index), "tag": tag, "text": text})
        for node in preserved.get(group_index, []): target.append(node)
    require(len(used) == len(pres), "原提示詞有遺漏")
    for block in blocks:
        n = soup.select_one(f'[data-candidate-block="{block["index"]}"]')
        require(n is not None and normalized(n.get_text()) == normalized(block["text"]), "候選文字映射不符")
    for n in soup.find_all(True):
        if n.name == "a" and n.has_attr("href"):
            key = rebase_url(n["href"], Path(source["path"]).parent, Path("/"))
            for attr, value in link_attributes.get(key, {}).items(): n[attr] = value
        for attr in ("href", "src"):
            if n.has_attr(attr): n[attr] = rebase_url(n[attr], Path(source["path"]).parent, output)
    style = soup.new_tag("style", attrs={"id": "handout-preview-content"})
    style.string = ('.handout-list{padding-left:1.5em;line-height:1.8}.outcomes>span{margin-left:.4em}'
                    '.agenda-heading{font-size:inherit;margin:0 0 .5em}.handout-table-scroll{max-width:100%;overflow-x:auto;margin:1.5em 0}'
                    '.handout-table-scroll table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:.9rem}'
                    '.handout-table-scroll th,.handout-table-scroll td{border:1px solid var(--c-border,#ddd);padding:.75em;text-align:left;vertical-align:top;overflow-wrap:anywhere}'
                    '.handout-table-scroll th{background:var(--c-surface,#f5f5f5)}'
                    '.lesson-section[id]{scroll-margin-top:90px}')
    soup.head.append(style)
    ids = [n["id"] for n in soup.select("[id]")]
    require(len(ids) == len(set(ids)), "預覽有重複id")
    require_preserved_controls(source["path"], soup)
    output.mkdir(parents=True)
    (output / "original.html").write_bytes(Path(source["path"]).read_bytes())
    (output / "candidate.md").write_bytes(Path(candidate["path"]).read_bytes())
    preview = output / "preview.html"; preview.write_text(str(soup))
    manifest = {"schema_version": "handout-preview-2", "status": "pending_browser_checks",
                "task_scope": "content-change", "source": source, "candidate": candidate,
                "confirmation": artifact(confirmation_path), "feedback": receipt["feedback"],
                "h3": receipt, "mapping": artifact(mapping_path), "preview": artifact(preview),
                "blocks": blocks, "protected_pre_count": len(used), "formal_overwrite": False, "published": False}
    save(output / "manifest.json", manifest)
    return manifest


def build_preview(state_path, mapping_path, output):
    state_path, mapping_path, output = map(lambda p: Path(p).resolve(), (state_path, mapping_path, output))
    require(not output.exists(), "預覽目錄已存在；保留既有版本，不覆寫")
    s = load_stage(state_path)
    check_inputs(s)
    require(stage_status(state_path)["decision"] is not None, "候選尚未停止待確認")
    require(s.get("h3_receipt") and s["unit"]["human"]["h3"] == "confirmed", "須先取得候選H3確認")
    require(stage_status(state_path)["decision"]["status"] == "complete", "本章仍有未解問題，不得套用")
    candidate = s["artifacts"][s["candidates"][-1]]
    require(s["h3_receipt"]["confirmation"]["sha256"] == candidate["sha256"], "H3不是目前候選")
    source = s["artifacts"][s["config"]["source"]]
    require(Path(source["path"]).suffix.lower() in (".html", ".htm"), "第一版須有原HTML版型")
    require(not Path(source["path"]).is_relative_to(output), "預覽不能包含正式來源位置")
    plan = read_json(mapping_path)
    require(plan.get("task_scope") == "content-change" and plan.get("reason", "").strip(), "須列明內容套用範圍與原因")
    soup = BeautifulSoup(Path(source["path"]).read_text(), "html.parser")
    roots = soup.select(".lesson-body")
    require(len(roots) == 1, "第一版僅支援唯一lesson-body原版型")
    body = roots[0]
    old_ids = [n.get("id") for n in body.select(".lesson-section")]
    markdown = Path(candidate["path"]).read_text()
    rendered = BeautifulSoup(MarkdownIt("commonmark", {"html": False}).render(markdown), "html.parser")
    nodes = [n for n in rendered.contents if isinstance(n, Tag)]
    require(nodes and nodes[0].name == "h1", "候選須有章節標題")
    require(soup.select_one("h1") is not None and normalized(nodes[0].get_text()) == normalized(soup.select_one("h1").get_text()), "候選標題與原頁不同，需先明確處理頁首對應")
    require(all(n.name in ("p", "h2", "pre") for n in nodes[1:]), "候選有尚未支援的區塊；先明確擴充映射，不丟棄內容")
    headings = [n.get_text() for n in nodes if n.name == "h2"]
    require(list(plan["sections"]) == headings, "區段映射須逐項對應候選標題順序")
    ids = [plan["intro_id"], *plan["sections"].values()]
    require(all(isinstance(i, str) and i for i in ids) and len(set(ids)) == len(ids), "區段id不得空白或重複")
    require(set(old_ids) <= set(ids), "須保留原區段錨點；不能默默移除")
    source_pres = list(body.select("pre"))
    grid_indices = plan.get("grid_pre_indices", [])
    require(all(type(i) is int and 0 <= i < len(source_pres) for i in grid_indices), "表格保護索引不符原稿pre")
    used = []
    blocks = []
    new_body = soup.new_tag(body.name, attrs=copy.deepcopy(body.attrs))

    def section(sid):
        original = body.find(id=sid)
        attrs = copy.deepcopy(original.attrs) if original and "lesson-section" in original.get("class", []) else {"id": sid, "class": ["lesson-section"]}
        node = soup.new_tag("section", attrs=attrs)
        new_body.append(node)
        return node

    current = section(plan["intro_id"])
    for index, node in enumerate(nodes[1:]):
        if node.name == "h2":
            current = section(plan["sections"][node.get_text()])
            node["class"] = ["section-heading"]
        elif node.name == "p":
            node["class"] = ["body-text"]
        elif node.name == "pre":
            text = node.get_text().rstrip("\n")
            matches = [i for i, old in enumerate(source_pres) if old.get_text().strip() == text.strip() and i not in used]
            require(len(matches) == 1, "候選程式／提示詞無唯一原節點對應；停止避免改掉互動或內容")
            i = matches[0]; used.append(i)
            old = source_pres[i]
            pre = copy.deepcopy(old)
            if i in grid_indices:
                pre["data-preserve-grid"] = "true"
            pre["data-candidate-block"] = str(index)
            wrapper = soup.new_tag("div", attrs={"class": ["prompt-wrap"]})
            wrapper.append(pre)
            button = body.find("button", attrs={"data-policy-copy": old.get("id")}) if old.get("id") else None
            if button:
                row = button.find_parent(class_="policy-copy-row")
                require(row is not None, "複製按鈕缺少原控制容器")
                wrapper.append(copy.deepcopy(row))
            current.append(wrapper)
            blocks.append({"index": index, "tag": "pre", "text": text, "id": old.get("id")})
            continue
        node["data-candidate-block"] = str(index)
        for anchor in node.select("a[href]"):
            parts = urlsplit(anchor["href"])
            if not parts.scheme and Path(unquote(parts.path)).is_absolute():
                anchor["href"] = rebase_url(anchor["href"], Path(source["path"]).parent, output)
            else:
                anchor["href"] = rebase_url(anchor["href"], Path(candidate["path"]).parent, output)
        blocks.append({"index": index, "tag": node.name, "text": node.get_text()})
        current.append(node)
    require(len(used) == len(source_pres), "原稿程式／提示詞有遺漏，停止套用")
    # 只重算非正文的本機相對位置，目的地不變；CSS、JS與殼層節點仍沿用。
    for node in soup.find_all(True):
        if node is body or body in node.parents:
            continue
        for attr in ("href", "src"):
            if node.has_attr(attr):
                node[attr] = rebase_url(node[attr], Path(source["path"]).parent, output)
    body.replace_with(new_body)
    if grid_indices:
        style = soup.new_tag("style", attrs={"id": "handout-preview-grid"})
        style.string = '.lesson-body pre[data-preserve-grid="true"]{white-space:pre;overflow-x:auto;max-width:100%;}'
        soup.head.append(style)
    ids_all = [n["id"] for n in soup.select("[id]")]
    require(len(ids_all) == len(set(ids_all)), "套用造成重複id")
    for block in blocks:
        node = soup.select_one(f'[data-candidate-block="{block["index"]}"]')
        require(node is not None and normalized(node.get_text()) == normalized(block["text"]), "候選文字對應失敗")
    require_preserved_controls(source["path"], soup)
    output.mkdir(parents=True)
    (output / "original.html").write_bytes(Path(source["path"]).read_bytes())
    (output / "candidate.md").write_bytes(Path(candidate["path"]).read_bytes())
    preview = output / "preview.html"
    preview.write_text(str(soup), encoding="utf-8")
    manifest = {"schema_version": "handout-preview-1", "status": "pending_browser_checks",
                "task_scope": "content-change", "source": source, "candidate": candidate,
                "stage_state": artifact(state_path), "h3": s["h3_receipt"], "mapping": artifact(mapping_path),
                "preview": artifact(preview), "blocks": blocks, "original_section_ids": old_ids,
                "preview_section_ids": ids, "protected_pre_count": len(used),
                "formal_overwrite": False, "published": False}
    save(output / "manifest.json", manifest)
    return manifest


def record_checks(output, report_path):
    """接收執行者的實際檢查紀錄；不將預覽認可當作發布授權。"""
    output = Path(output).resolve()
    manifest = read_json(output / "manifest.json")
    keys = ("confirmation", "feedback") if "confirmation" in manifest else ("stage_state",)
    for key in ("source", "candidate", *keys, "mapping", "preview"):
        ref = manifest[key]
        require(digest(ref["path"]) == ref["sha256"], f"{key}版本已變，不能沿用檢查")
    report = read_json(report_path)
    require(report["preview_sha256"] == manifest["preview"]["sha256"], "檢查不是目前預覽")
    require(report.get("status") == "pass" and report.get("content") is True and report.get("interaction") is True,
            "內容或互動尚未通過")
    rows = report.get("viewports", [])
    require({r["width"] for r in rows} >= {390, 820, 1440} and all(r.get("overflow") is False for r in rows),
            "必要尺寸未檢查或仍有整頁溢出")
    screenshots = report.get("screenshots", [])
    require(screenshots and all(digest(r["path"]) == r["sha256"] for r in screenshots), "缺少可追溯的畫面證據")
    manifest.update(status="preview_ready_for_review", verification=artifact(report_path))
    save(output / "manifest.json", manifest)
    return manifest
