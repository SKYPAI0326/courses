"""v0.10 狀態控制器；只登記已有成果，不執行模型、教材修改或網路操作。"""
from __future__ import annotations

import copy
import fcntl
import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path


class LoopError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise LoopError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise LoopError(f"無法讀取 JSON：{path}：{exc}") from exc


def artifact(path):
    path = Path(path).resolve(strict=True)
    return {"path": str(path), "sha256": digest(path)}


def validate_unit(unit):
    require(isinstance(unit, dict), "章節須為物件")
    for key in ("id", "purpose", "historical_rules", "assessment_basis"):
        require(isinstance(unit.get(key), str) and unit[key].strip(), f"缺少 {key}")
    require(unit.get("candidate_limit") == 2, "本版固定兩版上限，不接受重置額度")
    refs = unit.get("artifacts", {})
    require(isinstance(refs, dict) and refs, "缺少證據與來源")
    for ref in refs.values():
        require(isinstance(ref, dict) and set(ref) == {"path", "sha256"}, "檔案參照格式錯誤")
        require(isinstance(ref["path"], str) and Path(ref["path"]).is_absolute(), "檔案路徑須為絕對路徑")
        require(isinstance(ref["sha256"], str) and len(ref["sha256"]) == 64, "缺少檔案版本")
    require(unit.get("source") in refs and unit["assessment_basis"] in refs, "來源或評估依據不存在")
    candidates = unit.get("candidates")
    require(isinstance(candidates, list) and len(candidates) <= 2, "候選用量超過上限")
    require(len(set(candidates)) == len(candidates) and all(c in refs for c in candidates), "候選參照重複或不存在")
    current = candidates[-1] if candidates else unit["source"]
    require(unit.get("assessed_version") == current, "評估未綁定目前版本")
    for collection in ("problems", "questions"):
        rows = unit.get(collection)
        require(isinstance(rows, list), f"缺少 {collection}")
        ids = [r.get("id") for r in rows]
        require(all(isinstance(i, str) and i for i in ids) and len(set(ids)) == len(ids), "問題識別碼不合法")
        for row in rows:
            require(isinstance(row.get("description"), str) and row["description"], "缺少問題描述")
            require(row.get("basis") in refs, "問題必須有紀錄依據")
            require(type(row.get("open")) is bool, "問題狀態須為布林值")
            require(type(row.get("core" if collection == "problems" else "required")) is bool, "缺少核心／必要性判斷")
    problems = {p["id"]: p for p in unit["problems"]}
    questions = {q["id"]: q for q in unit["questions"]}
    grades = unit.get("grades", {})
    require(set(grades) == {"A", "B", "C"}, "須分別記 A／B／C")
    for grade in grades.values():
        require(grade.get("level") in ("L0", "L1", "L2", "L3", "pending"), "不合法等級")
        ps, qs = grade.get("problems", []), grade.get("questions", [])
        require(all(p in problems and problems[p]["open"] for p in ps), "等級引用無效 P")
        require(all(q in questions and questions[q]["open"] and questions[q]["required"] for q in qs), "等級引用無效 Q")
        if grade["level"] == "pending":
            require(bool(qs), "待判定必須對應必要 Q")
        else:
            require(not qs, "必要 Q 未解，不得給確定等級")
        if grade.get("cap") is not None:
            require(grade["level"] == "pending" and grade["cap"] == "L1", "封頂只用於待判定且已知最高 L1")
            require(any(problems[p]["core"] for p in ps), "封頂必須有已知核心 P，未實測不算 P")
        if grade["level"] in ("L0", "L1", "L2"):
            require(bool(ps), "低等級必須有已確認 P")
        if grade["level"] == "L3":
            require(not ps, "未解 P 不能直接判 L3")
    human = unit.get("human", {})
    require(human.get("decision") in (None, "H1", "H2"), "人工決策類型不合法")
    require(human.get("h3") in ("pending", "confirmed", "not_required"), "缺少 H3 狀態")
    if human["h3"] == "confirmed":
        require(human.get("version") == current and human.get("basis") in refs, "H3認可必須綁定版本及回饋")
    failures = unit.get("failures", {})
    require(isinstance(failures, dict) and all(k in problems and type(n) is int and n >= 0 for k, n in failures.items()), "失敗紀錄不合法")
    attempts = unit.get("attempts")
    require(isinstance(attempts, list) and all(isinstance(a, dict) and a.get("problem") in problems and isinstance(a.get("method"), str) for a in attempts), "缺少修法歷史")
    require(isinstance(unit.get("restrictions"), list) and all(isinstance(r, str) and r for r in unit["restrictions"]), "限制須為文字清單")
    require(type(unit.get("regression")) is bool, "缺少退步判斷")
    plan = unit.get("next_fix")
    if plan is not None:
        require(plan.get("problem") in problems and problems[plan["problem"]]["open"], "修法須對應未解 P")
        require(isinstance(plan.get("method"), str) and plan["method"].strip(), "缺少具體修法")
        require(plan.get("basis") in refs, "修法缺少依據")
        if failures.get(plan["problem"], 0):
            require(not any(a["problem"] == plan["problem"] and a["method"] == plan["method"] for a in attempts), "補救不可重複已失敗修法")


def decide(unit):
    validate_unit(unit)
    changed = [key for key, ref in unit["artifacts"].items()
               if not Path(ref["path"]).is_file() or digest(ref["path"]) != ref["sha256"]]
    limits = list(unit["restrictions"])
    used = len(unit["candidates"])
    if used >= 2:
        limits.append("候選版本已用滿2／2，不可新增內容版本")
    if unit["human"]["h3"] == "pending":
        limits.append("H3尚未確認")
    repeat = any(n >= 2 for n in unit["failures"].values())
    qs = [q["id"] for q in unit["questions"] if q["open"] and q["required"]]
    ps = [p["id"] for p in unit["problems"] if p["open"]]
    if changed:
        status, reason = "waiting_human", "H1：來源／證據版本改變，需辨認差異"
        limits.append("變動檔案：" + ", ".join(changed))
    elif unit["human"]["decision"] or repeat:
        status, reason = "waiting_human", (unit["human"]["decision"] or "H2") + "：需人工決策"
    elif qs:
        status, reason = "waiting_evidence", "必要證據未齊：" + ", ".join(qs)
    elif not ps and not unit["regression"] and all(g["level"] == "L3" for g in unit["grades"].values()):
        status = "waiting_human" if unit["human"]["h3"] == "pending" else "complete"
        reason = "H3：等待閱讀確認" if status == "waiting_human" else "本章已無必要缺口；不再改稿"
    elif used >= 2 or unit["restrictions"]:
        status, reason = "limited_stop", "仍有未解問題，但額度或授權限制禁止續修"
    elif unit["regression"] and not unit["next_fix"]:
        status, reason = "waiting_human", "H2：退步尚無可分離且有依據的修法"
    elif ps and unit["next_fix"]:
        status, reason = "ready_for_revision", "已有未解 P、具體修法與額度；僅可登記外部已產出的候選"
    else:
        status, reason = "waiting_human", "H2：判斷或修法不足，不能以低等級自動改寫"
    return {"id": unit["id"], "status": status, "reason": reason,
            "candidate_usage": f"{used}/2", "constraints": limits,
            "can_register_candidate": status == "ready_for_revision",
            "auto_rewrite": False, "can_execute_course_operations": False}


@contextmanager
def locked(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix(path.suffix + ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def save(path, state):
    """一次原子替換快照與內嵌歷史；中斷前後均為完整JSON。"""
    path = Path(path)
    fd, name = tempfile.mkstemp(prefix=".loop-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(state, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def load(path):
    state = read_json(path)
    require(state.get("schema_version") == 1 and state.get("controller_rules") == "v0.10", "不支援的狀態版本")
    require(type(state.get("revision")) is int and state["revision"] >= 0, "狀態revision不合法")
    require(isinstance(state.get("units"), list) and state["units"], "沒有章節")
    ids = [u["id"] for u in state["units"]]
    require(len(set(ids)) == len(ids), "章節重複")
    for unit in state["units"]:
        validate_unit(unit)
    require(len(state.get("history", [])) == state["revision"] + 1, "歷史與revision不一致")
    return state


def initialize(manifest, path):
    with locked(path):
        require(not Path(path).exists(), "狀態已存在；請resume，不可重新初始化重置用量")
        units = manifest.get("units", [])
        require(bool(units) and len({u["id"] for u in units}) == len(units), "缺少章節或章節重複")
        for unit in units:
            validate_unit(unit)
            require(not any(not Path(r["path"]).is_file() or digest(r["path"]) != r["sha256"] for r in unit["artifacts"].values()), "匯入來源版本不符")
        state = {"schema_version": 1, "controller_rules": "v0.10", "revision": 0,
                 "units": copy.deepcopy(units), "history": [{"revision": 0, "action": "import_existing_records", "units": copy.deepcopy(units)}]}
        save(path, state)
    return report(path)


def report(path):
    state = load(path)
    return {"revision": state["revision"], "controller_rules": "v0.10",
            "mode": "records_only", "units": [decide(u) for u in state["units"]]}


def checkpoint(path, proposal, expected_revision, actor, note):
    require(bool(actor.strip()) and bool(note.strip()), "更新須記執行者與依據說明")
    with locked(path):
        state = load(path)
        require(state["revision"] == expected_revision, "revision已變；請重新讀取，禁止覆蓋新進度")
        matches = [u for u in state["units"] if u["id"] == proposal.get("id")]
        require(len(matches) == 1, "只能更新已登記章節")
        old = matches[0]
        validate_unit(proposal)
        require(not any(not Path(r["path"]).is_file() or digest(r["path"]) != r["sha256"] for r in old["artifacts"].values()), "舊來源已改變；本版不自動遷移")
        for key in ("id", "purpose", "historical_rules", "source", "candidate_limit", "restrictions"):
            require(proposal[key] == old[key], f"不得透過checkpoint改變{key}；需另行確認工作邊界")
        require(all(proposal["artifacts"].get(k) == v for k, v in old["artifacts"].items()), "不可移除或覆寫既有來源／證據")
        before, after = old["candidates"], proposal["candidates"]
        require(after[:len(before)] == before and len(after) in (len(before), len(before) + 1), "不可重置候選歷史或跳增版本")
        for key, count in old["failures"].items():
            require(proposal["failures"].get(key, -1) >= count, "不能重置同一失敗紀錄")
        require(proposal["attempts"][:len(old["attempts"])] == old["attempts"], "不能刪除修法歷史")
        if old["human"]["h3"] != "not_required":
            require(proposal["human"]["h3"] != "not_required", "不能取消既有H3要求")
        if proposal["grades"] != old["grades"]:
            require(proposal["assessment_basis"] != old["assessment_basis"], "改變評級須附新評估依據")
        for collection in ("problems", "questions"):
            new = {r["id"]: r for r in proposal[collection]}
            for row in old[collection]:
                require(row["id"] in new, "問題歷史不得刪除；請記錄解決狀態")
                for key in ("description", "core" if collection == "problems" else "required"):
                    require(new[row["id"]][key] == row[key], "不能降低既有問題必要性或替換問題身分")
                if row["open"] and not new[row["id"]]["open"]:
                    require(new[row["id"]]["basis"] != row["basis"], "解決P／Q須提供新證據參照")
        if len(after) > len(before):
            require(decide(old)["can_register_candidate"], "目前狀態禁止新增候選")
            require(proposal["human"]["h3"] != "confirmed", "新候選不得繼承舊H3認可")
            require(proposal["assessment_basis"] != old["assessment_basis"], "新候選需新的評估紀錄")
            require(proposal["attempts"] == old["attempts"] + [{"problem": old["next_fix"]["problem"], "method": old["next_fix"]["method"]}], "新候選須登記本次修法")
        require(not any(not Path(r["path"]).is_file() or digest(r["path"]) != r["sha256"] for r in proposal["artifacts"].values()), "新證據版本不符")
        state["units"][state["units"].index(old)] = copy.deepcopy(proposal)
        state["revision"] += 1
        state["history"].append({"revision": state["revision"], "action": "checkpoint",
                                 "actor": actor, "note": note, "unit": copy.deepcopy(proposal)})
        save(path, state)
    return report(path)
