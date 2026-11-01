"""整課順序與相依控制；只派單章工作票，不呼叫AI或修改教材。"""
import copy
from pathlib import Path

from src.course_improvement_loop import LoopError, artifact, digest, locked, read_json, require, save
from src.course_loop_stages import load_stage, stage_status
from src.course_loop_review import validate_policy


def load_queue(path):
    s = read_json(path)
    require(s.get("schema_version") == "queue-1", "不是整課佇列狀態")
    return s


def unit_policy(manifest, unit):
    return unit.get("review_policy", manifest.get("review_policy"))


def authorize_dispatch(path, expected_revision, actor, note):
    """保存指定範圍的啟動紀錄，不初始化或重置既有佇列。"""
    require(isinstance(actor, str) and actor.strip() and isinstance(note, str) and note.strip(), "缺少啟動者與授權範圍")
    with locked(path):
        s = load_queue(path)
        require(s["revision"] == expected_revision, "revision已變，請重讀")
        require(not s["manifest"]["dispatch_enabled"], "佇列已啟動，不重複登記")
        s["manifest"]["dispatch_enabled"] = True
        s["revision"] += 1
        s["history"].append({"event": "dispatch_authorized", "actor": actor, "note": note})
        save(path, s)
    return queue_status(path)


def initialize_queue(manifest, path):
    path = Path(path).resolve()
    with locked(path):
        require(not path.exists(), "佇列已存在，不可初始化重置歷史")
        require(type(manifest.get("dispatch_enabled")) is bool, "須明確設定派送授權")
        if "review_policy" in manifest:
            validate_policy(manifest["review_policy"])
        units = manifest["units"]
        require(bool(units), "課程清單不能為空")
        seen, sources, child_paths = set(), set(), set()
        for u in units:
            if unit_policy(manifest, u) is not None:
                validate_policy(unit_policy(manifest, u))
            require(u["id"] not in seen, "章節識別碼重複")
            require(bool(u["purpose"].strip()), "缺少章節用途")
            ref = u["source"]
            require(artifact(ref["path"]) == ref, "章節來源版本不符")
            require(ref["path"] not in sources, "同一來源不能重複計為兩章")
            child = Path(u["stage_state"]).resolve()
            require(child.is_relative_to(path.parent) and child != path and child not in child_paths,
                    "單章狀態須在整課隔離目錄內且不能重複")
            require(not child.exists(), "新佇列不自動借用既有試作狀態")
            deps = u["dependencies"]
            require(len({d["unit"] for d in deps}) == len(deps), "相依重複")
            for dep in deps:
                require(dep["unit"] in seen and bool(dep["reason"].strip()), "相依必須指向前章並說明原因")
                require(type(dep.get("allow_h3_provisional")) is bool, "須明確設定是否允許H3暫定參照")
            seen.add(u["id"])
            sources.add(ref["path"])
            child_paths.add(child)
        s = {"schema_version": "queue-1", "revision": 0, "manifest": copy.deepcopy(manifest),
             "active": None, "bindings": {}, "history": [], "integration_review": None}
        save(path, s)
    return queue_status(path)


def inspect(s):
    rows = []
    by_id = {}
    for u in s["manifest"]["units"]:
        row = {"id": u["id"], "title": u["title"], "status": "pending", "candidate_usage": "0/2",
               "version": None, "blockers": [], "provisional": False}
        source = u["source"]
        if not Path(source["path"]).is_file() or digest(source["path"]) != source["sha256"]:
            row.update(status="waiting_human", blockers=["H1：正式來源版本改變；不得沿用舊佇列判斷"])
        elif Path(u["stage_state"]).exists():
            try:
                child = load_stage(u["stage_state"])
                require(child["config"]["id"] == u["id"], "單章身分與佇列不符")
                require(child["config"]["purpose"] == u["purpose"], "單章用途與佇列不符")
                if unit_policy(s["manifest"], u) is not None:
                    require(child["schema_version"] == "stages-2" and child["config"].get("review_policy") == unit_policy(s["manifest"], u),
                            "單章未採用佇列指定的角色與覆核設定")
                require(child["config"]["artifacts"][child["config"]["source"]] == source, "單章來源與佇列不符")
                result = stage_status(u["stage_state"])
                row["candidate_usage"] = result["candidate_usage"]
                current = child["candidates"][-1] if child["candidates"] else child["config"]["source"]
                row["version"] = child["artifacts"][current]
                row["child_revision"] = result["revision"]
                row["stage_phase"] = result["phase"]
                if result["phase"] != "stopped":
                    row["status"] = "in_progress"
                else:
                    decision = result["decision"]
                    row["status"] = decision["status"]
                    row["reason"] = decision["reason"]
                    row["constraints"] = decision["constraints"]
                    row["h3_only"] = (decision["status"] == "waiting_human" and decision["reason"].startswith("H3："))
            except (LoopError, OSError, KeyError, TypeError) as exc:
                row.update(status="waiting_human", blockers=[f"H1：單章紀錄需確認：{exc}"])
        bound = s["bindings"].get(u["id"], {})
        for dep in u["dependencies"]:
            upstream = by_id[dep["unit"]]
            usable = upstream["status"] == "complete"
            provisional = (dep["allow_h3_provisional"] and upstream.get("h3_only", False)
                           and upstream["status"] == "waiting_human" and not upstream["blockers"])
            if not usable and not provisional:
                row["blockers"].append(f"等待{dep['unit']}：{dep['reason']}（{upstream['status']}）")
            elif dep["unit"] in bound and bound[dep["unit"]] != upstream["version"]:
                row["blockers"].append(f"H1：{dep['unit']}參照版本已變；需確認受影響範圍，不自動重綁")
            if provisional:
                row["provisional"] = True
        if row["blockers"] and row["status"] != "waiting_human":
            row["underlying_status"] = row["status"]
            row["status"] = "dependency_blocked"
        rows.append(row)
        by_id[u["id"]] = row
    return rows


def queue_status(path):
    s = load_queue(path)
    rows = inspect(s)
    all_done = all(r["status"] == "complete" for r in rows)
    versions = {r["id"]: r["version"] for r in rows}
    review = s["integration_review"]
    reviewed = bool(review and review["versions"] == versions
                    and Path(review["evidence"]["path"]).is_file()
                    and digest(review["evidence"]["path"]) == review["evidence"]["sha256"])
    status = "complete" if all_done and reviewed else ("waiting_integration_review" if all_done else "incomplete")
    return {"revision": s["revision"], "course_status": status,
            "dispatch_enabled": s["manifest"]["dispatch_enabled"], "active": s["active"],
            "units": rows, "auto_rewrite": False}


def dispatch(path):
    """派工作票；不建立單章state、不執行next、不呼叫AI。"""
    with locked(path):
        s = load_queue(path)
        require(s["manifest"]["dispatch_enabled"], "本佇列只建清單，尚未授權派送")
        rows = inspect(s)
        by_id = {r["id"]: r for r in rows}
        active = s["active"]
        if active:
            row = by_id[active["unit"]]
            if row["status"] in ("pending", "in_progress", "ready_for_revision") and not row["blockers"]:
                return {"ticket": active, "reused": True}
            s["history"].append({"event": "park", "ticket": active, "status": row["status"]})
            s["active"] = None
        chosen = next((r for r in rows if r["status"] in ("pending", "in_progress", "ready_for_revision") and not r["blockers"]), None)
        if chosen:
            u = next(u for u in s["manifest"]["units"] if u["id"] == chosen["id"])
            binding = {d["unit"]: by_id[d["unit"]]["version"] for d in u["dependencies"]}
            s["bindings"][u["id"]] = binding
            ticket = {"id": f"{s['manifest']['id']}-{s['revision'] + 1}-{u['id']}", "unit": u["id"],
                      "action": "resume_single_unit" if Path(u["stage_state"]).exists() else "start_single_unit",
                      "stage_state": u["stage_state"], "source": u["source"], "purpose": u["purpose"],
                      "upstream_versions": binding, "provisional": chosen["provisional"]}
            if unit_policy(s["manifest"], u) is not None:
                ticket["review_policy"] = copy.deepcopy(unit_policy(s["manifest"], u))
            s["active"] = ticket
            s["history"].append({"event": "dispatch", "ticket": ticket})
        if active != s["active"] or chosen:
            s["revision"] += 1
            save(path, s)
        return {"ticket": s["active"], "reused": False, "blocked": [r for r in rows if r["blockers"]]}


def confirm_integration(path, evidence, expected_revision, actor):
    """登記跨章銜接檢查，不代替單章H3或自行宣布操作通過。"""
    require(bool(actor.strip()), "須記錄確認者")
    with locked(path):
        s = load_queue(path)
        require(s["revision"] == expected_revision, "revision已變，請重讀")
        rows = inspect(s)
        require(all(r["status"] == "complete" for r in rows), "尚有未完成或相依阻塞章節")
        ref = artifact(evidence)
        require(Path(ref["path"]).is_relative_to(Path(path).resolve().parent) and Path(ref["path"]).stat().st_size > 0,
                "銜接證據須另存在隔離目錄")
        require(ref["path"] != str(Path(path).resolve()), "狀態檔不能作為銜接證據")
        s["integration_review"] = {"versions": {r["id"]: r["version"] for r in rows}, "evidence": ref, "actor": actor}
        s["active"] = None
        s["revision"] += 1
        s["history"].append({"event": "integration_confirmed", "review": s["integration_review"]})
        save(path, s)
    return queue_status(path)
