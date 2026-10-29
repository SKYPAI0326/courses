"""文案專用設定；沿用既有控制器，不建立第二套狀態機。"""
import re
import json
from html.parser import HTMLParser
from pathlib import Path

from src.course_improvement_loop import require


def copy_course_spec(manifest_path):
    """將明確列齊的授權章節接入既有整課佇列；共用呼叫總額。"""
    path = Path(manifest_path).resolve()
    manifest = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(manifest.get("units"), list) and manifest["units"], "整課文案清單須列出章節")
    budget = manifest.get("max_model_calls")
    require(type(budget) is int and 1 <= budget <= 1000, "整課須明列已核准的max_model_calls總額")
    def resolve(p):
        return (path.parent / p).resolve()
    spec = None
    units = []
    for unit in manifest["units"]:
        part = copy_spec(resolve(unit["source"]), unit["id"], unit["title"], unit["purpose"],
                         [resolve(p) for p in unit.get("materials", [])], unit.get("keep", []))
        spec = spec or part
        units.extend(part["units"])
    spec.update(id=manifest["id"], units=units)
    spec["limits"]["max_model_calls"] = budget
    return spec


class PreBlocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = False
        self.parts = []
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            self.active, self.parts = True, []

    def handle_data(self, data):
        if self.active:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "pre" and self.active:
            self.blocks.append("".join(self.parts).strip())
            self.active = False


def copy_spec(source, unit_id, title, purpose, materials=(), keep=()):
    source = Path(source).resolve()
    require(source.suffix.lower() in (".html", ".htm", ".md"), "文案入口只接受HTML或Markdown")
    text = source.read_text(encoding="utf-8")
    if source.suffix.lower() in (".html", ".htm"):
        parser = PreBlocks()
        parser.feed(text)
        protected = parser.blocks
    else:
        protected = [m.group(2).strip() for m in re.finditer(
            r"^(`{3,}|~{3,})[^\n]*\n(.*?)^\1[ \t]*$", text, re.M | re.S)]
    protected = list(dict.fromkeys(x for x in [*protected, *keep] if x.strip()))
    root = Path(__file__).resolve().parents[1]
    base = root / "operations/course-content-scoring"
    checks = [{"id": "links", "kind": "local_links", "description": "候選的本機引用路徑存在；語意與連結目標另由覆核比對"}]
    if protected:
        checks.append({"id": "protected-text", "kind": "required_text",
                       "description": "原稿程式／提示詞區塊及指定文字逐字保留，不以潤稿改動操作內容",
                       "texts": protected})
    return {
        "id": f"copy-{unit_id}",
        "roles": {"assessor": "gpt-6.1-sol", "writer": "gpt-6-luna", "reviewer": "gpt-6.1-sol"},
        "rules": [str(base / name) for name in (
            "三原則判斷等級與修正交接-v0.7.md", "單章課程改善流程-v0.10.md", "講義文案撰寫基準-v0.3.md")]
            + [str(root / "docs/course-copy-profile-v0.6.md")],
        "limits": {"max_model_calls": 8, "timeout_seconds": 180,
                   "max_input_chars": 200000, "reasoning_effort": "low"},
        "units": [{"id": unit_id, "title": title,
                   "profile": "copy-v0.6",
                   "citation_contract": "locations-v1",
                   "purpose": "文案迭代：" + purpose + "。僅修閱讀脈絡，保留教學事實；不是整章技術驗收。",
                   "source": str(source), "materials": [str(Path(p).resolve()) for p in materials],
                   "dependencies": [], "checks": checks}]
    }
