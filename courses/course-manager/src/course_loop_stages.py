"""對話內AI的單章任務收送；不呼叫模型、不允許AI直接寫控制狀態。"""
import copy
import hashlib
import json
import re
from pathlib import Path

from src.course_improvement_loop import artifact, decide, digest, locked, read_json, require, save, validate_unit
from src.course_loop_review import (assignment, checks_for_current, enabled, require_approval,
                                   reviewer_inputs, target, validate_execution, validate_policy, validate_resolutions)
from src.course_copy_readability import READABILITY_INSTRUCTIONS, validate_readability


INSTRUCTIONS = {
    "assess": "讀取允許材料，固定本章用途；依v0.7/v0.10評估A/B/C，區分P與Q。交原文證據及修正交接（修法、保留內容、驗證方法）。未知不可當缺失；不產候選稿。",
    "rewrite": "依已接收的交接修正指定問題，保留事實、案例、操作與閱讀優點；交可連續閱讀的完整Markdown候選及改動說明。不改正式稿，不自評通過，不發明素材。",
    "compare": "比對原稿、候選與交接；逐項列原文、改善及未解P/Q，檢查閱讀退步，交A/B/C及必要下一修法。這是作者自查，不代填人工H3。未測不等於失敗。",
    "review": "使用新上下文，直接核對原稿、候選、用途與交接及必要檢查證據；無需改寫也須檢查局部缺口。辨認漏查及新增退步，逐項列原文依據。失敗檢查對應未解P，待補證對應必要Q；不能沿用作者自評或代填H3。",
}

COPY_INSTRUCTIONS = {
    "assess": "先把原稿當作學員會從頭讀到尾的文章，逐段指出讀者已理解什麼、接下來被要求理解或操作什麼，以及正文如何交代兩者關係。不可用章節標題、任務順序或評估者已知背景替正文補脈絡。若主要段落仍是任務與限制的堆疊，依v0.7判B並登記整篇閱讀缺口；交接須說明如何用既有事實發展解釋，不只補轉場句。另核對A/C、P/Q及保留事實，不產候選。",
    "rewrite": "依交接重建完整講義的閱讀推進，讓學員從正文理解問題、材料意義、示範中的判斷，以及下一步為何成立。保留必要操作清單，但不可只在清單前後加承接句、代碼解釋或摘要；主要段落要有依既有事實展開的解釋。保留原案例、數值、提示詞、操作與有用說明，不發明素材或示範；交完整Markdown候選及改動說明，不自評通過。",
    "compare": "先不依作者改寫意圖，從頭連讀候選，逐個主要區段引用相鄰正文，說明讀者實際能理解什麼、仍須自行拼出什麼。再比對原稿、交接與保留內容。局部P已解不等於整篇可讀；若正文仍主要靠任務、限制與檢查指令推進，新增未解B問題並依v0.7判級，不給B L3。既有P/Q以原id與description回交，只改open；這是作者自查，不代填H3。",
    "review": "使用新上下文，先以指定學員身分從頭連讀候選，不以既有P/Q、標題或作者自評補正文。逐個主要區段引用相鄰正文，說明讀者已理解什麼、下一段要求什麼、文本提供了哪個具體理由；若主要段落仍只是任務與限制堆疊，記新的未解B問題並依v0.7判級，不給B L3。完成整篇判斷後再核對原稿、保留事實、既有P/Q與必要檢查；不得代填H3。",
}

COPY_V04_INSTRUCTIONS = {
    "assess": "把原稿當作學員會連讀的講義，先找主要教學段落。若正文主要交辦任務、限制與交付，指出連續原文、讀者缺少的案例理解及既有材料能支持的改寫；不要只修轉場。保留事實與操作，另依v0.7核對A/C、P/Q，不產候選。",
    "rewrite": "依交接直接重寫主要交辦段落本身：用原稿與必要來源已有的案例事實說清楚材料支持什麼判斷、為何採取下一步，再保留既有操作讓學員實作。交完整Markdown候選，保留原案例、數值、提示詞、操作順序、限制、交付與有用說明。只在清單前後補引言、轉場或摘要不算改寫；缺足夠事實就回交，不虛構。",
    "compare": "先只連讀候選正文，引用主要承載教學的完整連續段落，尤其是要求學員操作、判斷與交付的段落；說明讀者在操作前實際能理解的案例、理由與判準，不能挑後段一句解釋替整段交辦背書。若主要正文仍由任務與限制推進，記未解B問題且不給B L3。再核對原稿、交接、保留內容與退步；既有P/Q用原id回交，不代填H3。",
    "review": "用新上下文先只連讀候選正文，引用主要承載教學的完整連續段落，尤其是要求學員操作、判斷與交付的段落；說明讀者在操作前實際能理解的案例、理由與判準，不能挑後段一句解釋替整段交辦背書。若主要正文仍由任務與限制推進，記未解B問題且不給B L3。完成候選本身的閱讀判斷後，再核對原稿、來源、既有P/Q及必要檢查，不代填H3。",
}


COPY_V05_INSTRUCTIONS = {
    phase: instruction + "以學員能否理解為優先：製作端用語要還原成具體的人、材料、行為與結果；保留代碼但先交代它代表的資料。條列能幫助操作就保留，不把清單硬併成長句。缺背景不等於一定缺事實，先找現有來源能否解釋；確實無據才回交。"
    for phase, instruction in COPY_V04_INSTRUCTIONS.items()
}

COPY_V06_INSTRUCTIONS = {phase: instruction + READABILITY_INSTRUCTIONS
                         for phase, instruction in COPY_V05_INSTRUCTIONS.items()}


def validate_copy_reading_decision(task, response):
    """核對引文與判斷的一致性；不宣稱程式能判定自然語言品質。"""
    decision = response.get("reading_decision")
    require(isinstance(decision, dict) and set(decision) == {"verdict", "explanation", "passages"},
            "文案比較／覆核缺少reading_decision閱讀依據")
    require(decision["verdict"] in ("supported", "gap"), "文案閱讀判斷不合法")
    require(isinstance(decision["explanation"], str) and decision["explanation"].strip(), "須說明整篇閱讀判斷")
    rows = decision["passages"]
    require(isinstance(rows, list) and rows, "須引用主要教學段落，不能只交分數")
    candidate = Path(task["target"]["path"]).read_text(encoding="utf-8")
    b = response["evaluation"]["grades"]["B"]
    open_b = {p["id"] for p in response["evaluation"]["problems"] if p["open"]} & set(b["problems"])
    gaps = []
    for row in rows:
        require(isinstance(row, dict) and set(row) == {"quote", "reader_understanding", "remaining_gap", "problem_id"},
                "閱讀段落欄位不完整")
        require(isinstance(row["quote"], str) and len(row["quote"].strip()) >= 8 and row["quote"] in candidate,
                "閱讀引文須逐字出自目前候選")
        require(isinstance(row["reader_understanding"], str) and row["reader_understanding"].strip(),
                "須說明學員能理解的具體內容")
        require(isinstance(row["remaining_gap"], str), "閱讀缺口須為文字，沒有則留空")
        if row["remaining_gap"].strip():
            require(row["problem_id"] in open_b, "閱讀缺口須對應仍open的B問題")
            gaps.append(row)
        else:
            require(row["problem_id"] is None, "無閱讀缺口時problem_id須為null")
    require((decision["verdict"] == "gap") == bool(gaps), "整篇判斷與閱讀缺口矛盾")
    if gaps:
        require(b["level"] != "L3", "已記錄閱讀缺口，不得給B L3")


def validate_copy_reading_audit(task, response):
    """每個主要區段都要有可在候選正文定位的閱讀證據。"""
    candidate = Path(task["target"]["path"]).read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^##[ \t]+(.+?)[ \t]*$", candidate))
    blocks = [(match.group(1), candidate[match.end():matches[i + 1].start() if i + 1 < len(matches) else None])
              for i, match in enumerate(matches)] or [("全文", candidate)]
    audit = response.get("reading_audit")
    require(isinstance(audit, dict) and set(audit) == {"sections", "overall"}, "文案比較／覆核缺少整篇閱讀紀錄")
    sections = audit["sections"]
    require(isinstance(sections, list) and len(sections) == len(blocks), "文案閱讀紀錄須逐一覆蓋主要區段")
    for row, (heading, body) in zip(sections, blocks):
        require(isinstance(row, dict) and set(row) == {"heading", "quote", "reader_understanding", "continuity", "verdict"},
                "文案閱讀紀錄欄位不完整")
        require(row["heading"] == heading, "文案閱讀紀錄區段順序與候選不符")
        require(isinstance(row["quote"], str) and len(row["quote"].strip()) >= 8 and row["quote"] in body,
                "文案閱讀引文須逐字出自對應區段正文")
        require(all(isinstance(row[k], str) and row[k].strip() for k in ("reader_understanding", "continuity")),
                "文案閱讀紀錄須說明讀者理解及段落關係")
        require(row["verdict"] in ("supported", "gap"), "文案閱讀判斷不合法")
    require(audit["overall"] in ("supported", "gap"), "文案整篇閱讀判斷不合法")
    require((audit["overall"] == "gap") == any(row["verdict"] == "gap" for row in sections),
            "整篇閱讀判斷與區段紀錄矛盾")
    if audit["overall"] == "gap":
        b = response["evaluation"]["grades"]["B"]
        require(b["level"] != "L3" and b["problems"], "已記錄閱讀缺口，不得給B L3或省略未解P")


def load_stage(path):
    s = read_json(path)
    require(s.get("schema_version") in ("stages-1", "stages-2"), "不是階段狀態檔")
    require(s.get("phase") in (*INSTRUCTIONS, "checks", "stopped"), "階段不合法")
    if enabled(s):
        validate_policy(s["config"]["review_policy"])
    else:
        require(s["phase"] not in ("checks", "review"), "舊狀態不能直接進入新版覆核")
    require(len(s["candidates"]) <= 2, "候選用量超限")
    return s


def check_inputs(s):
    for key, ref in s["artifacts"].items():
        require(Path(ref["path"]).is_file() and digest(ref["path"]) == ref["sha256"], f"來源或成果已變更：{key}；停止，不自動重綁")


def create_stage(config, path):
    path = Path(path).resolve()
    with locked(path):
        require(not path.exists(), "試驗狀態已存在，請resume")
        output = Path(config["output_root"]).resolve()
        require(output.is_dir() and output == path.parent, "狀態須位於既有隔離輸出目錄")
        refs = config["artifacts"]
        require(config["source"] in refs, "缺少原稿")
        if "review_policy" in config:
            validate_policy(config["review_policy"])
        s = {"schema_version": "stages-2" if "review_policy" in config else "stages-1", "revision": 0, "config": copy.deepcopy(config),
             "phase": "assess", "artifacts": copy.deepcopy(refs), "candidates": [],
             "unit": None, "task": None, "receipts": {}, "history": [], "attempts": []}
        check_inputs(s)
        save(path, s)
    return stage_status(path)


def stage_status(path):
    s = load_stage(path)
    check_inputs(s)
    decision = decide(s["unit"]) if s["phase"] == "stopped" else None
    if enabled(s):
        if decision and (decision["status"] == "complete" or decision["reason"].startswith("H3")):
            require_approval(s)
        elif s["phase"] in ("checks", "review"):
            decision = {"status": "waiting_checks" if s["phase"] == "checks" else "waiting_review",
                        "can_register_candidate": False, "reason": "本版本尚未完成必要檢查與覆核，不得結案"}
    return {"revision": s["revision"], "phase": s["phase"], "candidate_usage": f"{len(s['candidates'])}/2",
            "pending_task": s["task"], "decision": decision, "execution": "conversation_ai",
            "can_execute_course_operations": False}


def confirm_h3(path, feedback, candidate_sha256, expected_revision, actor):
    """登記已有的人工閱讀認可；此入口不供AI任務response代填。"""
    require(isinstance(actor, str) and actor.strip(), "須記錄人工回饋者")
    with locked(path):
        s = load_stage(path)
        check_inputs(s)
        require(s["phase"] == "stopped" and s["task"] is None and s["unit"] is not None,
                "須先完成比較並停止，才能接收H3")
        require(bool(s["candidates"]), "沒有可確認的候選")
        current = s["candidates"][-1]
        if enabled(s):
            require_approval(s)
        require(s["artifacts"][current]["sha256"] == candidate_sha256, "人工回饋版本與目前候選不符")
        ref = artifact(feedback)
        root = Path(s["config"]["output_root"]).resolve()
        require(Path(ref["path"]).is_relative_to(root) and Path(ref["path"]).stat().st_size > 0,
                "回饋須為隔離目錄內的非空紀錄")
        signature = {"candidate": current, "sha256": candidate_sha256, "feedback": ref, "actor": actor}
        existing = s.get("h3_receipt")
        if existing:
            require(existing["confirmation"] == signature, "已確認H3；不同回饋須另行處理，不可覆寫")
            return {**existing, "duplicate": True}
        require(s["revision"] == expected_revision, "revision已變，請重新讀取狀態")
        require(s["unit"]["human"]["h3"] == "pending", "目前沒有待確認的H3")
        protected = {r["path"] for r in s["artifacts"].values()} | {str(Path(path).resolve())}
        require(ref["path"] not in protected, "人工回饋必須另存，不得沿用教材或覆寫來源")
        key = f"human-h3-{s['revision'] + 1}"
        s["artifacts"][key] = ref
        s["unit"]["artifacts"][key] = copy.deepcopy(ref)
        s["unit"]["human"].update(h3="confirmed", version=current, basis=key)
        validate_unit(s["unit"])
        decision = decide(s["unit"])
        s["revision"] += 1
        receipt = {"confirmation": signature, "revision": s["revision"],
                   "status": decision["status"], "candidate_usage": len(s["candidates"])}
        s["h3_receipt"] = receipt
        s["history"].append({"event": "human_h3_confirmed", "receipt": receipt})
        save(path, s)
        return {**receipt, "duplicate": False}


def next_task(path):
    with locked(path):
        s = load_stage(path)
        check_inputs(s)
        if s["phase"] == "stopped":
            return {"stopped": True, "decision": stage_status(path)["decision"]}
        if s["phase"] == "checks":
            return {"stopped": False, "waiting_checks": True, "revision": s["revision"],
                    "command": "run-checks", "target": s["artifacts"][target(s)]}
        if s["task"] is not None:
            return copy.deepcopy(s["task"])
        if s["phase"] == "rewrite":
            require(decide(s["unit"])["can_register_candidate"] and len(s["candidates"]) < 2, "目前不得派送改寫")
        task_id = f"{s['config']['id']}-{s['revision'] + 1}-{s['phase']}"
        profile = s["config"].get("profile")
        task = {"id": task_id, "phase": s["phase"], "purpose": s["config"]["purpose"],
                "instructions": (COPY_V06_INSTRUCTIONS[s["phase"]] if profile == "copy-v0.6"
                                 else COPY_V05_INSTRUCTIONS[s["phase"]] if profile == "copy-v0.5"
                                 else COPY_V04_INSTRUCTIONS[s["phase"]] if profile == "copy-v0.4"
                                 else COPY_INSTRUCTIONS[s["phase"]] if profile == "copy-v0.3"
                                 else INSTRUCTIONS[s["phase"]]),
                "allowed_inputs": copy.deepcopy(s["artifacts"]),
                "output_root": s["config"]["output_root"], "current_evaluation": s["unit"],
                "candidate_usage": len(s["candidates"]), "candidate_limit": 2}
        if profile:
            task["profile"] = profile
        if enabled(s):
            task["assignment"] = assignment(s)
            task["target"] = copy.deepcopy(s["artifacts"][target(s)])
            if s["phase"] == "review":
                checks_for_current(s)
                task["allowed_inputs"], task["current_evaluation"] = reviewer_inputs(s)
                task["checks"] = s["latest_checks"]
        s["task"] = task
        s["revision"] += 1
        s["history"].append({"event": "dispatch", "task_id": task_id, "phase": s["phase"]})
        save(path, s)
        return task


def supplement_evidence(path, evidence, expected_revision):
    """只重開必要證據待確認的評估；不重置候選、不自動改稿。"""
    with locked(path):
        s = load_stage(path)
        check_inputs(s)
        require(s["revision"] == expected_revision, "revision已變，請重新讀取")
        require(s["phase"] == "stopped" and s["task"] is None and s["unit"] is not None,
                "目前不是可補證的停止狀態")
        require(decide(s["unit"])["status"] == "waiting_evidence", "目前不在等待必要補證")
        require(not s["unit"]["restrictions"], "使用者限制仍在；不得自行解除後補證")
        require(isinstance(evidence, dict) and bool(evidence), "須提供新證據路徑對照")
        root = Path(s["config"]["output_root"]).resolve()
        protected = {r["path"] for r in s["artifacts"].values()} | {str(Path(path).resolve())}
        added = {}
        for key, filename in evidence.items():
            require(isinstance(key, str) and key and key not in s["artifacts"], "證據識別碼須為新值")
            ref = artifact(filename)
            require(Path(ref["path"]).is_relative_to(root) and ref["path"] not in protected
                    and Path(ref["path"]).stat().st_size > 0, "證據須另存於隔離目錄，不可沿用狀態或舊輸入")
            added[key] = ref
            protected.add(ref["path"])
        s["artifacts"].update(added)
        s["phase"] = "compare" if s["candidates"] else "assess"
        s["evidence_recheck"] = True
        if enabled(s):
            s["review_gate"] = None
        s["revision"] += 1
        s["history"].append({"event": "evidence_added", "artifacts": added, "candidate_usage": len(s["candidates"])})
        save(path, s)
    return stage_status(path)


def recheck_comparison(path, evidence, expected_revision):
    """H3前發現新缺口時重開比較；保留原判斷與用量，不直接放行改稿。"""
    with locked(path):
        s = load_stage(path)
        check_inputs(s)
        require(s["revision"] == expected_revision, "revision已變，請重新讀取")
        require(s["phase"] == "stopped" and s["task"] is None and s["candidates"]
                and s["unit"] is not None, "須為已有候選的停止狀態")
        decision = decide(s["unit"])
        require(decision["status"] == "waiting_human" and decision["reason"].startswith("H3")
                and s["unit"]["human"]["h3"] == "pending", "僅限尚未確認的H3比較補查")
        require(not s["unit"]["restrictions"], "使用者限制仍在，不得自行重開")
        ref = artifact(evidence)
        root = Path(s["config"]["output_root"]).resolve()
        protected = {r["path"] for r in s["artifacts"].values()} | {str(Path(path).resolve())}
        require(Path(ref["path"]).is_relative_to(root) and ref["path"] not in protected
                and Path(ref["path"]).stat().st_size > 0, "補查須有隔離目錄內的新證據檔")
        key = f"comparison-recheck-{s['revision'] + 1}"
        s["artifacts"][key] = ref
        s["phase"] = "compare"
        s["evidence_recheck"] = True
        if enabled(s):
            s["review_gate"] = None
        s["revision"] += 1
        s["history"].append({"event": "comparison_reopened", "evidence": key,
                             "candidate_usage": len(s["candidates"])})
        save(path, s)
    return stage_status(path)


def receive(path, response, execution=None):
    """結果及receipt同筆原子提交；完全相同重送為唯讀，異內容重送拒絕。"""
    fingerprint = hashlib.sha256(json.dumps(response, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    with locked(path):
        s = load_stage(path)
        check_inputs(s)
        task_id = response["task_id"]
        if task_id in s["receipts"]:
            require(s["receipts"][task_id]["fingerprint"] == fingerprint, "同任務重送內容不同")
            if enabled(s):
                require(s["receipts"][task_id]["execution"] == execution, "重送執行身分不同")
            return {**s["receipts"][task_id], "duplicate": True}
        task = s["task"]
        require(task is not None and task["id"] == task_id, "任務不存在或已過期")
        phase = s["phase"]
        if enabled(s):
            validate_execution(s, execution)
        expected = {"report", "handoff"} if phase == "assess" else ({"candidate", "report"} if phase == "rewrite" else {"report"})
        require(set(response["outputs"]) == expected, "回交檔案不符合階段契約")
        root = Path(s["config"]["output_root"]).resolve()
        protected = {Path(r["path"]).resolve() for r in s["artifacts"].values()} | {Path(path).resolve()}
        keys = {}
        for role, output_path in response["outputs"].items():
            p = Path(output_path).resolve(strict=True)
            require(p.is_file() and p.is_relative_to(root) and p not in protected, "成果須為隔離目錄內的新檔，不得覆寫來源或狀態")
            require(p.stat().st_size > 0, "不可接收空成果")
            protected.add(p)
            key = f"{task_id}:{role}"
            s["artifacts"][key] = artifact(p)
            keys[role] = key
        if phase == "rewrite":
            require(set(response) == {"task_id", "outputs"}, "改寫階段不能回填評級或人工認可")
            require(decide(s["unit"])["can_register_candidate"] and len(s["candidates"]) < 2, "停止規則禁止新增候選")
            s["candidates"].append(keys["candidate"])
            plan = s["unit"]["next_fix"]
            s["attempts"].append({"problem": plan["problem"], "method": plan["method"]})
            s["phase"] = "compare"
            if enabled(s):
                s["review_gate"] = None
        else:
            fields = {"task_id", "outputs", "evaluation"}
            if task.get("profile") == "copy-v0.3" and phase in ("compare", "review"):
                fields.add("reading_audit")
                validate_copy_reading_audit(task, response)
            if task.get("profile") == "copy-v0.5" and phase in ("compare", "review"):
                fields.add("reading_decision")
                validate_copy_reading_decision(task, response)
            if task.get("profile") == "copy-v0.6" and phase in ("compare", "review"):
                fields.add("reading_decision")
                validate_copy_reading_decision(task, validate_readability(task, response))
            if phase == "review":
                fields.add("check_resolutions")
                validate_resolutions(s, response)
            require(set(response) == fields, "評估階段欄位不符")
            ev = copy.deepcopy(response["evaluation"])
            require(set(ev) == {"problems", "questions", "grades", "regression", "next_fix"}, "AI不可變更用途、限制、額度或H3")
            # 所有判斷綁定這次回交報告；AI不得自行指定舊證據來結案。
            for rows in (ev["problems"], ev["questions"]):
                for row in rows:
                    row["basis"] = keys["report"]
            if ev["next_fix"]:
                ev["next_fix"]["basis"] = keys.get("handoff", keys["report"])
            previous = s["unit"]
            failures = copy.deepcopy(previous["failures"]) if previous else {}
            if previous:
                for collection in ("problems", "questions"):
                    new_rows = {r["id"]: r for r in ev[collection]}
                    for old in previous[collection]:
                        require(old["id"] in new_rows, "比較不能刪除P/Q歷史")
                        for field in ("description", "core" if collection == "problems" else "required"):
                            require(new_rows[old["id"]][field] == old[field], "不能改問題身分或降低必要性")
                count_failure = (not enabled(s) or (phase == "review" and s["candidates"]
                                 and target(s) not in s.get("failure_counted_versions", [])))
                if not s.get("evidence_recheck") and count_failure:
                    attempted_problem = s["attempts"][-1]["problem"]
                    if next(p for p in ev["problems"] if p["id"] == attempted_problem)["open"]:
                        failures[attempted_problem] = failures.get(attempted_problem, 0) + 1
            unit = {"id": s["config"]["id"], "purpose": s["config"]["purpose"],
                    "historical_rules": "v0.10；單章對話AI隔離試驗", "candidate_limit": 2,
                    "source": s["config"]["source"], "artifacts": copy.deepcopy(s["artifacts"]),
                    "candidates": list(s["candidates"]), "assessment_basis": keys["report"],
                    "assessed_version": s["candidates"][-1] if s["candidates"] else s["config"]["source"],
                    "human": {"decision": None, "h3": "pending" if s["candidates"] else "not_required"},
                    "failures": failures, "attempts": list(s["attempts"]),
                    "restrictions": list(s["config"].get("restrictions", [])), **ev}
            if s.get("evidence_recheck") and previous:
                unit["human"] = copy.deepcopy(previous["human"])
            validate_unit(unit)
            s["unit"] = unit
            decision = decide(unit)
            s["phase"] = "rewrite" if decision["can_register_candidate"] else "stopped"
            if enabled(s):
                s["review_gate"] = None
                if phase == "compare" or (phase == "assess" and decision["status"] == "complete"):
                    s["phase"] = "checks"
                elif phase == "review":
                    if s["candidates"]:
                        s.setdefault("failure_counted_versions", []).append(target(s))
                    if decision["status"] == "complete" or decision["reason"].startswith("H3"):
                        require(all(c["status"] == "pass" for c in checks_for_current(s)["checks"]),
                                "必要檢查未通過，不得覆核放行")
                        s["review_gate"] = {"target": copy.deepcopy(s["artifacts"][target(s)]),
                                            "checks": s["latest_checks"], "report": keys["report"],
                                            "execution": copy.deepcopy(execution)}
        s["revision"] += 1
        receipt = {"task_id": task_id, "fingerprint": fingerprint, "revision": s["revision"],
                   "phase": s["phase"], "candidate_usage": len(s["candidates"])}
        if enabled(s):
            receipt["execution"] = copy.deepcopy(execution)
        s["receipts"][task_id] = receipt
        s["history"].append({"event": "accept", "receipt": receipt, "evaluation": copy.deepcopy(s["unit"]) if phase != "rewrite" else None})
        s["task"] = None
        s["evidence_recheck"] = False
        save(path, s)
        return {**receipt, "duplicate": False}
