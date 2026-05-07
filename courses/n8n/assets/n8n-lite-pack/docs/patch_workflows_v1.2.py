#!/usr/bin/env python3
"""
Lite Pack v1.2 workflow patcher

- inject LP helper（throttle / retry / size guard）到所有用 Gemini 的 Code node 開頭
- 把 const GEMINI_API_KEY = '__GEMINI_API_KEY__'; 那段移除（helper 內已有）
- 標 v1.2 註解
- N× per item workflow（#02 / #03 / #09）額外加 throttle 提示

跑法：python3 patch_workflows_v1.2.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
WORKFLOW_DIR = HERE.parent / "workflows"
HELPER = (HERE / "lp-helper-template.js").read_text(encoding="utf-8").strip()

# 哪些 workflow 是 N× per item（需 throttle）
THROTTLE_WORKFLOWS = {"02-pdf-ai-rename.json", "03-batch-error-recovery.json", "09-gmail-categorize.json"}

# #10 / #11 已有自己的設計，不動
SKIP_WORKFLOWS = {"10-folder-organize.json", "11-csv-clean-score.json"}


def patch_jscode(filename: str, code: str) -> str:
    """patch a single Code node jsCode."""
    if "generativelanguage" not in code:
        return code  # 不是 LLM workflow，跳過

    if "const LP = {" in code:
        return code  # 已 patched，避免重複

    # 1. 移除舊的 GEMINI_API_KEY 宣告（含註解）
    code = re.sub(
        r"//[^\n]*__GEMINI_API_KEY__[^\n]*\n",
        "",
        code,
    )
    code = re.sub(
        r"const GEMINI_API_KEY = '__GEMINI_API_KEY__';\s*\n",
        "",
        code,
    )

    # 2. 取代 httpRequest call to Gemini → lpCall
    # 找 await this.helpers.httpRequest({...generativelanguage...}) 整段
    # 簡單策略：用 marker 標出，接下來用人工或更細的 patch
    # 這裡先做 inject helper 在開頭
    is_throttle = filename in THROTTLE_WORKFLOWS
    throttle_hint = ""
    if is_throttle:
        throttle_hint = (
            "// ⚠ 本 workflow 每筆 input 都打 1 次 LLM API。\n"
            "// 若處理 > 10 筆 → 在 loop 內加 `if (i > 0) await lpThrottle();`\n"
            "// 否則撞 Free tier 10 RPM 上限會 429。\n\n"
        )

    header = f"// Lite Pack v1.2 · LLM helper（共用骨架，下面業務邏輯維持原樣）\n{throttle_hint}{HELPER}\n\n// ════════════════════════════════════════════════════════════\n// 業務邏輯（這裡開始是這個 workflow 特有的）\n// ════════════════════════════════════════════════════════════\n"

    return header + code.lstrip()


def patch_workflow(path: Path) -> bool:
    """patch a single workflow JSON file."""
    if path.name in SKIP_WORKFLOWS:
        print(f"  ⏭ {path.name} 已有自己的設計，跳過")
        return False

    with open(path, encoding="utf-8") as f:
        wf = json.load(f)

    changed = False
    for n in wf.get("nodes", []):
        if n.get("type") != "n8n-nodes-base.code":
            continue
        code = n.get("parameters", {}).get("jsCode", "")
        if not code:
            continue
        new_code = patch_jscode(path.name, code)
        if new_code != code:
            n["parameters"]["jsCode"] = new_code
            changed = True
            print(f"  ✓ {path.name} :: {n.get('name', '?')[:40]} ({len(code)} → {len(new_code)} chars)")

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(wf, f, ensure_ascii=False, indent=2)
    return changed


def main():
    if not WORKFLOW_DIR.exists():
        print(f"❌ workflows dir not found: {WORKFLOW_DIR}")
        sys.exit(1)

    print(f"patching workflows in: {WORKFLOW_DIR}\n")
    total = patched = 0
    for path in sorted(WORKFLOW_DIR.glob("*.json")):
        total += 1
        if patch_workflow(path):
            patched += 1

    print(f"\n✓ {patched}/{total} workflow patched")


if __name__ == "__main__":
    main()
