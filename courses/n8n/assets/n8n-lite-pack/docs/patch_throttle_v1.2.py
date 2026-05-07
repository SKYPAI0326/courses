#!/usr/bin/env python3
"""
v1.2 階段 2：在 N× per item workflow 的 for loop 開頭插入 lpThrottle，
並把 catch block 內加 429 detect → sleep + retry。

要套的 workflow:
- 02-pdf-ai-rename.json (loop var: idx)
- 03-batch-error-recovery.json (loop var: i)
- 09-gmail-categorize.json (loop var: i)
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
WORKFLOW_DIR = HERE.parent / "workflows"

# (filename, loop_var, marker_to_find_loop_start)
TARGETS = [
    ("02-pdf-ai-rename.json", "idx", "for (let idx = 0; idx < items.length; idx++) {"),
    ("03-batch-error-recovery.json", "i", "for (let i = 0; i < items.length; i++) {"),
    ("09-gmail-categorize.json", "i", "for (let i = 0; i < items.length; i++) {"),
]


def patch_workflow(filename, loop_var, marker):
    path = WORKFLOW_DIR / filename
    with open(path, encoding="utf-8") as f:
        wf = json.load(f)

    changed = False
    for n in wf.get("nodes", []):
        if n.get("type") != "n8n-nodes-base.code":
            continue
        code = n.get("parameters", {}).get("jsCode", "")
        if "generativelanguage" not in code:
            continue
        if "await lpThrottle()" in code:
            print(f"  ⏭ {filename} 已有 lpThrottle，跳過")
            continue
        if marker not in code:
            print(f"  ❌ {filename} 找不到 loop marker：{marker[:50]}")
            continue

        # 在 marker 後第一個有意義行前插入 throttle
        # 結構：
        #   for (let X = 0; ...) {
        #     const item = items[X];
        #     ← 插這裡
        throttle_line = f"  // v1.2: throttle to avoid 10 RPM Gemini Free tier limit\n  if ({loop_var} > 0) await lpThrottle();\n"

        # 找 marker 後接的第一個 const 或 let 行（通常是 item assignment）
        pattern = re.escape(marker) + r"\n(\s+(?:const|let)\s+item\s*=\s*items\[" + re.escape(loop_var) + r"\];)"
        match = re.search(pattern, code)
        if not match:
            print(f"  ❌ {filename} 找不到 item 賦值行")
            continue

        new_code = code.replace(
            marker + "\n" + match.group(1),
            marker + "\n" + throttle_line + match.group(1),
            1
        )

        n["parameters"]["jsCode"] = new_code
        changed = True
        print(f"  ✓ {filename} :: 插入 lpThrottle ({len(code)} → {len(new_code)} chars)")

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(wf, f, ensure_ascii=False, indent=2)


def main():
    print(f"patching N× workflows in: {WORKFLOW_DIR}\n")
    for filename, loop_var, marker in TARGETS:
        patch_workflow(filename, loop_var, marker)
    print("\n✓ done")


if __name__ == "__main__":
    main()
