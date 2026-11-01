"""角色與版本綁定的覆核；檢查結果不取代教材語意或操作實測。"""
import copy
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from src.course_improvement_loop import artifact, locked, read_json, require, save


ROLE_FOR_PHASE = {"assess": "assessor", "rewrite": "writer", "compare": "writer", "review": "reviewer"}


def enabled(s):
    return s["schema_version"] == "stages-2"


def validate_policy(policy):
    require(isinstance(policy, dict) and set(policy) == {"roles", "checks"}, "覆核設定須包含roles與checks")
    roles = policy["roles"]
    require(isinstance(roles, dict) and set(roles) == {"assessor", "writer", "reviewer"}, "須指定三種角色")
    require(all(isinstance(v, str) and v.strip() for v in roles.values()), "每個角色須指定模型")
    require(roles["writer"] not in (roles["assessor"], roles["reviewer"]), "評估與覆核不得使用改寫模型")
    checks = policy["checks"]
    require(isinstance(checks, list) and checks, "須明列本章必要檢查，不能空白放行")
    ids = []
    for c in checks:
        require(isinstance(c.get("id"), str) and c["id"], "檢查缺少id")
        require(c.get("kind") in ("local_links", "required_text", "external"), "不支援的檢查類型")
        require(isinstance(c.get("description"), str) and c["description"].strip(), "須說明檢查用途")
        if c["kind"] == "required_text":
            require(isinstance(c.get("texts"), list) and c["texts"]
                    and all(isinstance(t, str) and t for t in c["texts"]), "須列必要保留文字")
        ids.append(c["id"])
    require(len(ids) == len(set(ids)), "檢查id重複")


def assignment(s):
    role = ROLE_FOR_PHASE[s["phase"]]
    return {"role": role, "model": s["config"]["review_policy"]["roles"][role],
            "fresh_context_required": role == "reviewer"}


def validate_execution(s, execution):
    a = assignment(s)
    require(isinstance(execution, dict) and set(execution) == {"role", "model", "context_id"},
            "須由執行端登記role/model/context_id")
    require(execution["role"] == a["role"] and execution["model"] == a["model"], "回交角色或模型與派送不符")
    require(isinstance(execution["context_id"], str) and execution["context_id"].strip(), "缺少執行上下文識別碼")
    if a["fresh_context_required"]:
        used = [r["execution"]["context_id"] for r in s["receipts"].values()]
        require(execution["context_id"] not in used, "覆核須使用未用過的新上下文")


def target(s):
    return s["candidates"][-1] if s["candidates"] else s["config"]["source"]


def checks_for_current(s):
    key = s.get("latest_checks")
    require(key in s["artifacts"], "缺少本版本檢查證據")
    data = read_json(s["artifacts"][key]["path"])
    require(data["target"] == s["artifacts"][target(s)], "檢查證據不是目前版本")
    require([r["id"] for r in data["checks"]] == [c["id"] for c in s["config"]["review_policy"]["checks"]],
            "必要檢查不完整")
    return data


def require_approval(s):
    gate = s.get("review_gate")
    require(gate and gate["target"] == s["artifacts"][target(s)]
            and gate["checks"] == s.get("latest_checks"), "目前版本尚未覆核放行")
    require(all(c["status"] == "pass" for c in checks_for_current(s)["checks"]), "必要檢查尚未通過")


def validate_resolutions(s, response):
    rows = checks_for_current(s)["checks"]
    resolutions = response["check_resolutions"]
    require(isinstance(resolutions, dict) and set(resolutions) == {r["id"] for r in rows if r["status"] != "pass"},
            "失敗或未實測的必要檢查須逐項回交P/Q，不得忽略")
    ev = response["evaluation"]
    for r in rows:
        if r["status"] == "pass":
            continue
        collection = ev["problems"] if r["status"] == "fail" else ev["questions"]
        require(any(p["id"] == resolutions[r["id"]] and p["open"]
                    and (r["status"] == "fail" or p["required"]) for p in collection),
                "檢查失敗須對應未解P，待補證須對應必要Q")


def reviewer_inputs(s):
    # 不提供作者的報告與自評等級，避免直接照抄作者的放行結論。
    refs = {k: copy.deepcopy(v) for k, v in s["artifacts"].items()
            if not k.endswith(":report") and (s["candidates"] or not k.endswith(":handoff"))}
    issues = {c: [{k: v for k, v in p.items() if k != "basis"} for p in s["unit"][c]]
              for c in ("problems", "questions")}
    return refs, issues


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []
        self.text_parts = []

    def handle_data(self, data):
        self.text_parts.append(data)

    def handle_starttag(self, tag, attrs):
        self.targets.extend(value for key, value in attrs if key in ("href", "src") and value)


def local_links(filename):
    p = Path(filename)
    content = p.read_text(encoding="utf-8")
    parser = Links()
    parser.feed(content)
    links = list(parser.targets)
    if p.suffix.lower() not in (".html", ".htm"):
        # 排除程式碼示例；支援一般行內連結及參照式連結的定義。
        prose = re.sub(r"```.*?```|`[^`]*`", "", content, flags=re.S)
        links += re.findall(r"\]\(\s*(<[^>]+>|[^\s)]+)", prose)
        links += re.findall(r"(?m)^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)", prose)
    checked, skipped = [], []
    for raw in links:
        url = raw.strip("<>")
        parts = urlsplit(url)
        if parts.scheme not in ("", "file") or parts.netloc or not parts.path:
            skipped.append(url)
            continue
        dest = Path(unquote(parts.path))
        if not dest.is_absolute():
            dest = p.parent / dest
        checked.append({"target": str(dest.resolve()), "exists": dest.exists()})
    return {"status": "pass" if all(r["exists"] for r in checked) else "fail",
            "observations": checked, "not_checked": skipped,
            "scope": "僅本機路徑存在性；不驗證遠端、頁內錨點、權限或實作效果"}


def missing_required_text(filename, texts):
    p = Path(filename)
    raw = p.read_text(encoding="utf-8")
    decoded = raw
    if p.suffix.lower() in (".html", ".htm"):
        parser = Links()
        parser.feed(raw)
        decoded = "".join(parser.text_parts)
    return [t for t in texts if t not in raw and t not in decoded]


def run_checks(path, expected_revision, evidence=None):
    from src.course_loop_stages import check_inputs, load_stage, stage_status
    with locked(path):
        s = load_stage(path)
        check_inputs(s)
        require(enabled(s) and s["phase"] == "checks" and s["task"] is None, "目前不在必要檢查階段")
        require(s["revision"] == expected_revision, "revision已變，請重新讀取")
        specs = s["config"]["review_policy"]["checks"]
        evidence = evidence or {}
        require(isinstance(evidence, dict) and set(evidence) <= {c["id"] for c in specs if c["kind"] == "external"},
                "外部證據只能對應已指定的檢查")
        root = Path(s["config"]["output_root"]).resolve()
        current = s["artifacts"][target(s)]
        protected = {r["path"] for r in s["artifacts"].values()} | {str(Path(path).resolve())}
        results = []
        for c in specs:
            if c["kind"] == "local_links":
                result = local_links(current["path"])
            elif c["kind"] == "required_text":
                missing = missing_required_text(current["path"], c["texts"])
                result = {"status": "fail" if missing else "pass", "missing": missing,
                          "scope": "指定文字保留，不證明語意與數值推論正確"}
            else:
                item = evidence.get(c["id"])
                result = {"status": "pending", "reason": "尚未提供本版本實測紀錄"}
                if item:
                    require(item.get("target") == current and item.get("status") in ("pass", "fail", "pending"),
                            "外部證據須綁定目前版本並明列狀態")
                    ref = artifact(item["report"])
                    supplemented = any(ref in event.get("artifacts", {}).values() for event in s["history"]
                                       if event["event"] == "evidence_added")
                    require(Path(ref["path"]).is_relative_to(root) and (ref["path"] not in protected or supplemented)
                            and Path(ref["path"]).stat().st_size > 0, "實測紀錄須另存隔離目錄")
                    key = f"external-check-{s['revision'] + 1}-{c['id']}"
                    s["artifacts"][key] = ref
                    protected.add(ref["path"])
                    result = {"status": item["status"], "evidence": ref,
                              "scope": "外部執行者提供紀錄；控制器不驗證內容真實性"}
            results.append({"id": c["id"], "kind": c["kind"], "description": c["description"], **result})
        key = f"checks-{s['revision'] + 1}"
        report = root / f"{key}.json"
        data = {"target": current, "checks": results}
        # 若上次寫完報告但狀態尚未提交就中斷，只接受相同報告後接續。
        if report.exists():
            require(read_json(report) == data and str(report) not in protected, "檢查報告已存在且不能覆寫")
        else:
            save(report, data)
        s["artifacts"][key] = artifact(report)
        s["latest_checks"] = key
        s["review_gate"] = None
        s["phase"] = "review"
        s["revision"] += 1
        s["history"].append({"event": "checks_recorded", "evidence": key, "target": current})
        save(path, s)
    return stage_status(path)
