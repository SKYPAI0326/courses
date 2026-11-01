"""可操作的整課執行入口；準備與啟動分離，模型結果經既有控制器接收。"""
import copy
import fcntl
import json
import re
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from src.course_improvement_loop import LoopError, artifact, digest, read_json, require, save
from src.course_improvement_queue import (authorize_dispatch, confirm_integration, dispatch,
                                          initialize_queue, load_queue, queue_status)
from src.course_loop_executor import build_prompt, collect_result, execute_codex, response_schema
from src.course_copy_reports import apply_report_patch, hydrate_reading, merge_issue_updates
from src.course_loop_review import run_checks, validate_policy
from src.course_loop_stages import (check_inputs, confirm_h3, create_stage, load_stage,
                                    next_task, receive, stage_status, supplement_evidence)


def write_once(path, text):
    path = Path(path)
    if path.exists():
        require(path.read_text(encoding="utf-8") == text, f"既有成果不同，不覆寫：{path}")
    else:
        with path.open("x", encoding="utf-8") as stream:
            stream.write(text)


@contextmanager
def run_lock(root):
    # 不讓兩個work等待鎖後悄悄接著消耗另一批額度。
    with (Path(root) / "runner.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise LoopError("此run已有執行者，請先查status") from exc
        yield


def load_run(root):
    root = Path(root).resolve()
    s = read_json(root / "run.json")
    require(s.get("schema_version") == "course-run-1", "不是可執行的課程run；不能接管舊試作")
    require(digest(root / "spec.json") == s["spec_sha256"], "課程範圍設定變更，停止，不自動重綁")
    return s


def prepare(spec, root):
    root = Path(root).resolve()
    require(not root.exists(), "run目錄已存在，請status／work接續，不重新初始化")
    require(isinstance(spec.get("id"), str) and re.fullmatch(r"[A-Za-z0-9_-]+", spec["id"]), "課程id只接受英數、底線與連字號")
    limits = spec["limits"]
    for k, low, high in (("max_model_calls", 1, 1000), ("timeout_seconds", 10, 900), ("max_input_chars", 1000, 2000000)):
        require(type(limits.get(k)) is int and low <= limits[k] <= high, f"缺少或不合法的{ k }")
    require(limits.get("reasoning_effort") in ("low", "medium"), "須明確設定low或medium")
    require(isinstance(spec.get("rules"), list) and spec["rules"], "須提供現行判級／文案／流程規範")
    rule_refs = {f"rule-{i}": artifact(p) for i, p in enumerate(spec["rules"])}
    units, configs = [], {}
    seen = set()
    for u in spec["units"]:
        require(re.fullmatch(r"[A-Za-z0-9_-]+", u["id"]) and u["id"] not in seen, "章節id不合法或重複")
        require(u["title"].strip() and u["purpose"].strip(), "須指定章節標題與用途")
        profile = u.get("profile")
        require(profile in (None, "copy-v0.3", "copy-v0.4", "copy-v0.5", "copy-v0.6"), "不支援的單章流程設定")
        policy = {"roles": copy.deepcopy(spec["roles"]), "checks": copy.deepcopy(u["checks"])}
        validate_policy(policy)
        refs = {"source": artifact(u["source"]), **rule_refs,
                **{f"material-{i}": artifact(p) for i, p in enumerate(u.get("materials", []))}}
        for ref in refs.values():
            require(not Path(ref["path"]).is_relative_to(root), "輸入不能位於尚未建立的run內")
            try:
                Path(ref["path"]).read_text(encoding="utf-8")
            except UnicodeError as exc:
                raise LoopError("本版模型輸入須為UTF-8文字；二進位材料請提供摘錄或external檢查") from exc
        for dep in u["dependencies"]:
            require(dep["unit"] in seen, "相依須指向前章")
        seen.add(u["id"])
        directory = root / "units" / u["id"]
        configs[u["id"]] = {"id": u["id"], "purpose": u["purpose"], "source": "source", "artifacts": refs,
                             "output_root": str(directory), "review_policy": policy, "restrictions": []}
        if profile:
            configs[u["id"]]["profile"] = profile
        if u.get("citation_contract"):
            require(profile == "copy-v0.6" and u["citation_contract"] == "locations-v1", "不支援的引文契約")
            configs[u["id"]]["citation_contract"] = u["citation_contract"]
        units.append({"id": u["id"], "title": u["title"], "purpose": u["purpose"], "source": refs["source"],
                      "stage_state": str(directory / "state.json"), "dependencies": copy.deepcopy(u["dependencies"]),
                      "review_policy": policy})
    require(units, "課程清單不能空白")
    root.mkdir(parents=True)
    save(root / "spec.json", spec)
    for uid, config in configs.items():
        directory = root / "units" / uid
        directory.mkdir(parents=True)
        save(directory / "config.json", config)
        # 快照供比較；模型以綁定來源為準，來源改變即停，不悄悄採用新稿。
        write_once(directory / ("original" + Path(config["artifacts"]["source"]["path"]).suffix),
                   Path(config["artifacts"]["source"]["path"]).read_text(encoding="utf-8"))
    manifest = {"id": spec["id"], "dispatch_enabled": False, "units": units}
    initialize_queue(manifest, root / "queue.json")
    save(root / "run.json", {"schema_version": "course-run-1", "spec_sha256": digest(root / "spec.json"),
                            "model_calls": 0, "jobs": {}, "last_error": None})
    return status(root)


def activate(root, actor, note):
    root = Path(root).resolve()
    with run_lock(root):
        load_run(root)
        q = load_queue(root / "queue.json")
        authorize_dispatch(root / "queue.json", q["revision"], actor, note)
    return status(root)


def unit_path(root, uid):
    units = load_queue(Path(root) / "queue.json")["manifest"]["units"]
    require(any(u["id"] == uid for u in units), "章節不在本run範圍")
    return Path(next(u["stage_state"] for u in units if u["id"] == uid))


def status(root):
    root = Path(root).resolve()
    runtime = load_run(root)
    result = queue_status(root / "queue.json")
    for row in result["units"]:
        path = unit_path(root, row["id"])
        if path.exists():
            s = load_stage(path)
            row["candidate"] = s["artifacts"][s["candidates"][-1]] if s["candidates"] else None
            row["human"] = s["unit"]["human"] if s["unit"] else None
            row["questions"] = s["unit"]["questions"] if s["unit"] else []
            row["reports"] = [ref["path"] for k, ref in s["artifacts"].items() if k.endswith(":report")]
    result.update(model_calls=runtime["model_calls"], model_call_limit=read_json(root / "spec.json")["limits"]["max_model_calls"],
                  last_error=runtime["last_error"], execution="codex-exec; foreground only")
    return result


def initialize_child(root, ticket):
    path = Path(ticket["stage_state"])
    if not path.exists():
        config = read_json(path.parent / "config.json")
        for uid, ref in ticket["upstream_versions"].items():
            config["artifacts"][f"upstream-{uid}"] = ref
        create_stage(config, path)
    return path


def accept_job(root, runtime, job):
    directory = Path(job["directory"])
    task = read_json(directory / "task.json")
    provider = read_json(directory / "provider-result.json")
    require(provider["model"] == task["assignment"]["model"] and provider["fresh_process"] is True,
            "執行模型或新程序紀錄不符")
    answer = read_json(directory / "answer.json")
    if job.get("report_repair", {}).get("mode") == "locations-v1":
        answer = apply_report_patch(task, read_json(job["report_repair"]["original_answer"]), answer)
        write_once(directory / "assembled-answer.json", json.dumps(answer, ensure_ascii=False, indent=2))
    elif task.get("citation_contract") == "locations-v1":
        answer = hydrate_reading(task, answer)
        answer["evaluation"] = merge_issue_updates(task["current_evaluation"], answer["evaluation"])
        write_once(directory / "assembled-answer.json", json.dumps(answer, ensure_ascii=False, indent=2))
    if job.get("report_repair"):
        require(digest(job["report_repair"]["original_answer"]) == job["report_repair"]["original_answer_sha256"],
                "原拒收報告已變動，不接收更正")
        original = read_json(job["report_repair"]["original_answer"])
        if task.get("citation_contract") == "locations-v1":
            original["evaluation"] = merge_issue_updates(task["current_evaluation"], original["evaluation"])
        validate_report_repair(original, answer)
    require(isinstance(answer, dict) and isinstance(answer.get("documents"), dict), "模型回交不是documents物件")
    roles = {"report", "handoff"} if task["phase"] == "assess" else ({"report", "candidate"} if task["phase"] == "rewrite" else {"report"})
    expected = {"documents"} | ({"evaluation"} if task["phase"] != "rewrite" else set()) | ({"check_resolutions"} if task["phase"] == "review" else set())
    if task.get("profile") == "copy-v0.3" and task["phase"] in ("compare", "review"):
        expected.add("reading_audit")
    if task.get("profile") in ("copy-v0.5", "copy-v0.6") and task["phase"] in ("compare", "review"):
        expected.add("reading_decision")
    require(set(answer) == expected and set(answer["documents"]) == roles, "模型回交欄位不符合階段")
    outputs = {}
    for role, content in answer["documents"].items():
        require(isinstance(content, str) and content.strip(), "模型交付空白文件")
        dest = directory / f"{role}.md"
        write_once(dest, content)
        outputs[role] = str(dest)
    response = {"task_id": task["id"], "outputs": outputs}
    for key in ("evaluation", "check_resolutions", "reading_audit", "reading_decision"):
        if key in answer:
            response[key] = answer[key]
    execution = {"role": task["assignment"]["role"], "model": provider["model"], "context_id": provider["context_id"]}
    write_once(directory / "response.json", json.dumps(response, ensure_ascii=False, indent=2))
    if task.get("profile") in ("copy-v0.3", "copy-v0.4", "copy-v0.5", "copy-v0.6") and task["phase"] in ("compare", "review"):
        prior = task["current_evaluation"]
        identity_changes = []
        for collection in ("problems", "questions"):
            registered = {row["id"]: row["description"] for row in prior[collection]}
            for row in response["evaluation"][collection]:
                if row["id"] in registered and row["description"] != registered[row["id"]]:
                    identity_changes.append({"collection": collection, "id": row["id"],
                                             "returned_description": row["description"],
                                             "registered_description": registered[row["id"]]})
                    row["description"] = registered[row["id"]]
        if identity_changes:
            write_once(directory / "identity-normalization.json", json.dumps({
                "rule": "registered-problem-description-is-controller-owned",
                "changes": identity_changes,
                "effect": "保留原回交與報告，控制器沿用既有問題描述；open、core、required與判級不改"
            }, ensure_ascii=False, indent=2))
    # 相容舊schema的冗餘表示；不變更等級、問題或文件，原始回交永久保留。
    normalized = []
    for principle, grade in response.get("evaluation", {}).get("grades", {}).items():
        if grade.get("level") == "L1" and grade.get("cap") == "L1":
            grade["cap"] = None
            normalized.append(principle)
    if normalized:
        write_once(directory / "normalization.json", json.dumps({
            "rule": "definite-L1-redundant-cap", "principles": normalized,
            "effect": "僅移除與已判定L1相同的冗餘cap；等級與問題不變"
        }, ensure_ascii=False, indent=2))
    write_once(directory / "controller-response.json", json.dumps(response, ensure_ascii=False, indent=2))
    receipt = receive(job["state"], response, execution)
    save(directory / "receipt.json", receipt)
    job["status"] = "accepted"
    runtime["last_error"] = None
    save(Path(root) / "run.json", runtime)


def work(root, max_tasks=1, transport=execute_codex):
    root = Path(root).resolve()
    require(type(max_tasks) is int and 1 <= max_tasks <= 100, "每次工作須介於1至100個模型任務")
    with run_lock(root):
        runtime = load_run(root)
        limits = read_json(root / "spec.json")["limits"]
        require(load_queue(root / "queue.json")["manifest"]["dispatch_enabled"], "本run尚未start，不執行模型")
        try:
            # 已完成模型輸出但接收中斷時，先回交快取，不重呼模型或重複計版。
            for job in runtime["jobs"].values():
                if job["status"] != "accepted":
                    require((Path(job["directory"]) / "provider-result.json").exists(),
                            "前次模型任務沒有完成證據；停止，不自動重送，請先recover；明確失敗才可retry")
                    accept_job(root, runtime, job)
            for _ in range(max_tasks):
                ticket = dispatch(root / "queue.json")["ticket"]
                if ticket is None:
                    break
                path = initialize_child(root, ticket)
                s = load_stage(path)
                if s["phase"] == "checks":
                    evidence_path = path.parent / "check-evidence.json"
                    run_checks(path, s["revision"], read_json(evidence_path) if evidence_path.exists() else None)
                task = next_task(path)
                if task.get("stopped"):
                    continue
                require(runtime["model_calls"] < limits["max_model_calls"], "本run模型呼叫額度已用完；不自動增加")
                require(task["id"] not in runtime["jobs"], "工作已有執行紀錄，不能重新計版或重送")
                directory = path.parent / "jobs" / task["id"]
                directory.mkdir(parents=True)
                write_once(directory / "task.json", json.dumps(task, ensure_ascii=False, indent=2))
                write_once(directory / "prompt.txt", build_prompt(task, limits["max_input_chars"]))
                save(directory / "schema.json", response_schema(task))
                job = {"state": str(path), "directory": str(directory), "status": "running", "attempts": 1}
                runtime["jobs"][task["id"]] = job
                runtime["model_calls"] += 1
                save(root / "run.json", runtime)
                try:
                    provider = transport(directory, task["assignment"]["model"], limits["timeout_seconds"], limits["reasoning_effort"])
                    save(directory / "provider-result.json", provider)
                    job["status"] = "returned"
                    save(root / "run.json", runtime)
                    accept_job(root, runtime, job)
                except Exception:
                    job["status"] = "failed"
                    raise
        except (LoopError, OSError, ValueError, KeyError, TypeError) as exc:
            runtime["last_error"] = str(exc)
            save(root / "run.json", runtime)
    return status(root)


def retry(root, uid, reason, transport=execute_codex):
    """只允許已失敗、沒有候選輸出的任務補救一次；未知執行狀態不重送。"""
    root = Path(root).resolve()
    with run_lock(root):
        runtime = load_run(root)
        path = unit_path(root, uid)
        task = next_task(path)
        require("id" in task and task["id"] in runtime["jobs"], "沒有可補救的執行紀錄")
        job = runtime["jobs"][task["id"]]
        old = Path(job["directory"])
        require(job["status"] == "failed" and job["attempts"] == 1 and reason.strip(), "僅允許失敗任務一次明確補救")
        require(not (old / "provider-result.json").exists(), "已有完整模型結果，請work接收快取，不重新生成")
        require(not (old / "answer.json").exists(), "已有模型輸出，須先人工辨認，不另生成候選規避計版")
        limits = read_json(root / "spec.json")["limits"]
        require(runtime["model_calls"] < limits["max_model_calls"], "模型額度已用完")
        directory = old.parent / (old.name + "-retry")
        directory.mkdir()
        for name in ("task.json", "prompt.txt", "schema.json"):
            write_once(directory / name, (old / name).read_text())
        job.update(directory=str(directory), status="running", attempts=2, retry_reason=reason, previous_directory=str(old))
        runtime["model_calls"] += 1
        save(root / "run.json", runtime)
        try:
            provider = transport(directory, task["assignment"]["model"], limits["timeout_seconds"], limits["reasoning_effort"])
            save(directory / "provider-result.json", provider)
            accept_job(root, runtime, job)
        except (LoopError, OSError, ValueError, KeyError, TypeError) as exc:
            job["status"] = "failed"
            runtime["last_error"] = str(exc)
            save(root / "run.json", runtime)
    return status(root)


def validate_report_repair(original, corrected):
    """只准更正引文與已關閉項目的引用，不准把判斷改成通過。"""
    expected = copy.deepcopy(original["evaluation"])
    for principle in expected["grades"].values():
        for refs, collection in (("problems", "problems"), ("questions", "questions")):
            closed = {row["id"] for row in expected[collection] if not row["open"]}
            principle[refs] = [key for key in principle[refs] if key not in closed]
    require(corrected.get("evaluation") == expected, "報告更正不得改變原判級、問題狀態、修法或新增判斷")
    before = copy.deepcopy(original.get("reading_decision"))
    after = copy.deepcopy(corrected.get("reading_decision"))
    for decision in (before, after):
        require(isinstance(decision, dict) and isinstance(decision.get("passages"), list), "缺少原閱讀判斷")
        for row in decision["passages"]:
            row.pop("quote", None)
            row.pop("support_quotes", None)
            row.pop("quote_ref", None)
            row.pop("support_refs", None)
    require(before == after, "報告更正只能修引文，不得改變原閱讀結論")


def repair_report(root, uid, reason, actor, transport=execute_codex):
    """明確授權後，一次更正被拒收的比較報告；沿用原任務及總額。"""
    root = Path(root).resolve()
    with run_lock(root):
        runtime = load_run(root)
        path = unit_path(root, uid)
        task = next_task(path)
        require(task.get("phase") == "compare" and task.get("profile") == "copy-v0.6", "僅支援v0.6作者比較報告更正")
        job = runtime["jobs"].get(task["id"])
        require(job and job["status"] == "failed" and job["attempts"] == 1 and reason.strip() and actor.strip(),
                "須明確授權且每份失敗比較報告只更正一次")
        old = Path(job["directory"])
        require((old / "provider-result.json").is_file() and (old / "answer.json").is_file(), "須有完整原始回交")
        require(runtime["last_error"] and any(text in runtime["last_error"] for text in
                ("重述依據須逐字", "閱讀引文須逐字", "等級引用無效 P", "等級引用無效 Q", "引文段落不存在", "引文範圍越界")), "不是可更正的引文或引用拒收")
        limits = read_json(root / "spec.json")["limits"]
        require(runtime["model_calls"] < limits["max_model_calls"], "模型額度已用完")
        directory = old.parent / (old.name + "-report-repair")
        directory.mkdir()
        task = copy.deepcopy(task)
        task["allowed_inputs"]["rejected-report"] = artifact(old / "answer.json")
        task["report_patch"] = True
        task["instructions"] += ("\n本次只交replacements局部更正，不重交報告或evaluation，不重新評估或改稿。"
            "以原始rejected-report的passages零起算索引指定passage，quote_ref與support_refs選當前正文位置。"
            "只修有問題的引文。其餘資料由控制器原樣保存，不能輸出評級、P/Q、候選或新示範。")
        write_once(directory / "task.json", json.dumps(task, ensure_ascii=False, indent=2))
        write_once(directory / "prompt.txt", build_prompt(task, limits["max_input_chars"]))
        save(directory / "schema.json", response_schema(task))
        job.update(directory=str(directory), status="running", attempts=2,
                   report_repair={"mode": "locations-v1", "original_directory": str(old), "original_answer": str(old / "answer.json"),
                                  "original_answer_sha256": digest(old / "answer.json"), "reason": reason, "actor": actor})
        runtime["model_calls"] += 1
        save(root / "run.json", runtime)
        try:
            provider = transport(directory, task["assignment"]["model"], limits["timeout_seconds"], limits["reasoning_effort"])
            save(directory / "provider-result.json", provider)
            accept_job(root, runtime, job)
        except (LoopError, OSError, ValueError, KeyError, TypeError) as exc:
            job["status"] = "failed"
            runtime["last_error"] = str(exc)
            save(root / "run.json", runtime)
    return status(root)


def recover(root, uid):
    root = Path(root).resolve()
    with run_lock(root):
        runtime = load_run(root)
        path = unit_path(root, uid)
        jobs = [j for j in runtime["jobs"].values() if j["state"] == str(path) and j["status"] != "accepted"]
        require(len(jobs) == 1, "沒有單一待恢復的模型任務")
        job = jobs[0]
        directory = Path(job["directory"])
        task = read_json(directory / "task.json")
        collect_result(directory, task["assignment"]["model"])
        accept_job(root, runtime, job)
    return status(root)


def human_confirmation(root, uid, feedback, sha256, revision, actor):
    root = Path(root).resolve()
    with run_lock(root):
        load_run(root)
        path = unit_path(root, uid)
        require(Path(feedback).is_file(), "缺少使用者原話紀錄")
        text = Path(feedback).read_text(encoding="utf-8")
        dest = path.parent / f"human-feedback-{revision}.md"
        write_once(dest, text)
        result = confirm_h3(path, dest, sha256, revision, actor)
    return result


def supply_check(root, uid, check_id, result, report, sha256):
    root = Path(root).resolve()
    with run_lock(root):
        load_run(root)
        path = unit_path(root, uid)
        s = load_stage(path)
        check_inputs(s)
        spec = s["config"]["review_policy"]["checks"]
        require(any(c["id"] == check_id and c["kind"] == "external" for c in spec), "不是本章指定的外部檢查")
        require(result in ("pass", "fail", "pending"), "不合法檢查狀態")
        current = s["artifacts"][s["candidates"][-1] if s["candidates"] else s["config"]["source"]]
        require(current["sha256"] == sha256, "實測結果不是目前版本")
        require(s["phase"] == "checks" or (s["phase"] == "stopped" and stage_status(path)["decision"]["status"] == "waiting_evidence"),
                "僅在checks或必要補證停止時接收")
        text = Path(report).read_text(encoding="utf-8")
        require(text.strip(), "實測報告不可空白")
        key = f"evidence-{uuid4().hex}"
        dest = path.parent / f"{key}.md"
        write_once(dest, text)
        if s["phase"] == "stopped":
            supplement_evidence(path, {key: str(dest)}, s["revision"])
        mapping_path = path.parent / "check-evidence.json"
        mapping = read_json(mapping_path) if mapping_path.exists() else {}
        mapping[check_id] = {"target": current, "status": result, "report": str(dest)}
        save(mapping_path, mapping)
    return status(root)


def finish(root, evidence, revision, actor):
    root = Path(root).resolve()
    with run_lock(root):
        load_run(root)
        dest = root / f"integration-{revision}.md"
        write_once(dest, Path(evidence).read_text(encoding="utf-8"))
        return confirm_integration(root / "queue.json", dest, revision, actor)


def report(root):
    root = Path(root).resolve()
    data = status(root)
    rows = ["# 課程改善進度", "", f"狀態：{data['course_status']}；派送：{data['dispatch_enabled']}。",
            f"模型呼叫：{data['model_calls']}／{data['model_call_limit']}。", ""]
    if data["last_error"]:
        rows += ["執行停止原因：" + data["last_error"], ""]
    for u in data["units"]:
        rows += [f"## {u['id']} {u['status']}", "", f"候選用量：{u['candidate_usage']}；階段：{u.get('stage_phase', '未開始')}。"]
        if u.get("candidate"):
            rows += [f"[目前完整候選](<{u['candidate']['path']}>)", f"版本：`{u['candidate']['sha256']}`；revision：{u['child_revision']}。"]
        rows += [f"[報告{i + 1}](<{p}>)" for i, p in enumerate(u.get("reports", []))]
        rows += ["待補證：" + q["description"] for q in u.get("questions", []) if q["open"] and q["required"]]
        rows += u["blockers"] + [""]
    rows += ["完成不包含正式講義覆蓋或發布；人工閱讀確認僅適用指定候選。", ""]
    (root / "REPORT.md").write_text("\n".join(rows), encoding="utf-8")
    return {"report": str(root / "REPORT.md"), "status": data}
