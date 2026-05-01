#!/usr/bin/env python3
"""批次跑 11 個 imagegen（A2-A6 + C1-C6）"""
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gen_ch6_cards import CARDS

BRIDGE = "/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/ai-orchestration/codex_bridge.py"
IMG_DIR = Path("/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/gen-image/img")

# 對應每張卡片的尺寸
SIZES = {
    "A2": "1024x1024",   # campaign-kv 1:1 anchor
    "A3": "1024x1280",   # brand-poster 直立
    "A4": "1024x1280",   # editorial-cover 直立
    "A5": "1792x1024",   # brand-identity-board 橫式 grid
    "A6": "1792x1024",   # bilingual-layout 橫式
    "C1": "1024x1280",   # bento-grid 直立
    "C2": "1024x1280",   # comparison 直立
    "C3": "1024x1280",   # step-by-step 直立
    "C4": "1024x1280",   # founder-portrait 直立
    "C5": "1024x1024",   # sticker-set 1:1 grid
    "C6": "1024x1280",   # lookbook-grid 直立
}

def main():
    for c in CARDS:
        cid = c["id"]
        if cid == "A1":
            print(f"[skip] {cid} 已生 v51")
            continue
        size = SIZES.get(cid, "1024x1024")
        out = str(IMG_DIR / c["image_path"])
        print(f"\n═══ {cid} imagegen 開始 ({size}) ═══")
        try:
            result = subprocess.run(
                ["python3", BRIDGE,
                 "--task", "imagegen",
                 "--prompt", c["prompt_full"],
                 "--out", out,
                 "--size", size,
                 "--reset-quota", "--yes"],
                capture_output=True, text=True, timeout=300
            )
            # 取 last 3 lines of stdout/stderr
            output = (result.stdout + result.stderr).strip().split("\n")
            for line in output[-5:]:
                print(line)
            if result.returncode == 0:
                print(f"✓ {cid} 完成")
            else:
                print(f"✗ {cid} 失敗 (returncode={result.returncode})")
        except subprocess.TimeoutExpired:
            print(f"✗ {cid} 逾時（>5min）")
        except Exception as e:
            print(f"✗ {cid} 例外: {e}")

    print("\n═══ 全部完成 ═══")


if __name__ == "__main__":
    main()
