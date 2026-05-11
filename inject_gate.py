#!/usr/bin/env python3
"""
inject_gate.py — 為所有課程 HTML 檔案注入密碼關卡
執行：python3 inject_gate.py
"""

import os
import re
from pathlib import Path

BASE = Path(__file__).parent / "courses"

# 各課程設定：(sessionStorage Key, SHA-256 hash)
COURSES = {
    "ai-workshop":     ("aiws_auth",    "09c81d07e25432c504712a3cf843802ff8ab41735f5cdb2be9ee311e06e8783f"),
    "ccs-foundations": ("ccs_auth",     "f195a697efb749102d1eee6c7071180ece0bba71b6df57eb92fe857fc61cb4d8"),
    "gemini-ai":       ("gemini_auth",  "af4216b537dbe50ab6bce3a5f75201f51894267495ac777423d8f18d11318db8"),
    "gen-ai-140h":     ("gen140_auth",  "34810b0ecfa2dab0a29120fc3ff1f867aec23bc5f23a184b8c6c3c7d3a550400"),
    "gtm":             ("gtm_auth",     "5142d1f99cbf6f9db528ce5aee5fab62c299fafabfeef9e5e0fa9a1dbff5f151"),
    "n8n":             ("n8n_auth",     "825e2dce35d14124f94b648f6ab2ab60c9db1d8f393c2b61722fe02412b9a199"),
    "ntub-seo-ga4":    ("ntub_auth",    "1c0d96ab18b0574bb4e6c04b2c4baff23637a70205a6b651ccdd6f2c9b638c81"),
    "office-ai":       ("officeai_auth","6ab0aa487f1730f54a645b5ac78f9118d45255eed7e62414cbc37108a848e5e4"),
    "digital-marketing-70h": ("digimkt_auth", "6d9278e29c0d1ab888cfabe6a73a06f54c124fb0a4bb3dfccd7720d3e80d9eb7"),
    "gen-ai-36h":      ("gen36_auth",   "2eeb336fddc0ac7aa5ce7ff9aa2b3a51db0f7ad83fd07d4e7d877dfc1d2b9089"),
    "prompt-basic":    ("pbasic_auth",  "f9be9b95884b731054cc95fa9e6fd80b5407004a08a203effc20a9d28212a555"),
    "simple-ai":       ("simpleai_auth","a47706648c17a64cac8b79fee80c1041ac453db7375062f88945af8721a3d86b"),
    "ipas-ai-beginner":("ipas_auth",    "17daf42d25e66eac9653114c7c170836e5dad10e22f8e95ffa29f6afdfd24b9f"),
    "line-stickers":   ("linestickers_auth", "0d9099fca21f914a1d4ad2b6dc42dd3e26e1cc9dc10996c235a9e3d8b6e36ab2"),
    "career-pivot-mid":("careerpivot_auth", "b4bacdf1af0913ed18ec5123a52d6678b473f880f3769dfb4060ef9378fa28ba"),
}

GATE_TEMPLATE = '''\
<style id="_gs">
#_gate{{position:fixed;inset:0;z-index:9999;background:#f5f3ee;display:flex;align-items:center;justify-content:center;font-family:'Noto Sans TC',sans-serif}}
#_gate-box{{width:100%;max-width:340px;padding:48px 36px;background:#fff;border:1px solid #d8d4cb;border-radius:6px;text-align:center}}
#_gate-title{{font-family:'Noto Serif TC',serif;font-size:1.35rem;font-weight:700;color:#2c2b28;margin-bottom:8px}}
#_gate-sub{{font-size:.8rem;color:#8c8880;margin-bottom:28px;line-height:1.7}}
#_gate-input{{width:100%;padding:10px 14px;border:1px solid #d8d4cb;border-radius:6px;font-size:.95rem;font-family:inherit;background:#f5f3ee;color:#2c2b28;outline:none;text-align:center;letter-spacing:.15em;box-sizing:border-box}}
#_gate-input:focus{{border-color:#6b7fa3;background:#fff}}
#_gate-btn{{margin-top:12px;width:100%;padding:11px;background:#6b7fa3;color:#fff;border:none;border-radius:6px;font-size:.85rem;font-family:inherit;cursor:pointer;transition:background .2s}}
#_gate-btn:hover{{background:#5c6f91}}
#_gate-err{{font-size:.76rem;color:#b5703a;margin-top:10px;min-height:16px}}
</style>
<div id="_gate">
  <div id="_gate-box">
    <div id="_gate-title">弄一下工作室</div>
    <div id="_gate-sub">課程專屬講義<br>請輸入課程密碼</div>
    <input id="_gate-input" type="password" placeholder="••••••••" autocomplete="off">
    <button id="_gate-btn" onclick="_gc()">進入課程</button>
    <div id="_gate-err"></div>
  </div>
</div>
<script>
(function(){{const K='{key}',H='{hash}';if(sessionStorage.getItem(K)==='1'){{var g=document.getElementById('_gate');if(g)g.style.display='none';return}}async function _gc(){{var v=document.getElementById('_gate-input').value,buf=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(v)),hex=Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('');if(hex===H){{sessionStorage.setItem(K,'1');document.getElementById('_gate').style.display='none'}}else{{document.getElementById('_gate-err').textContent='密碼錯誤，請再試一次'}}}}window._gc=_gc;document.getElementById('_gate-input').addEventListener('keydown',function(e){{if(e.key==='Enter')_gc()}})}})()</script>
'''

def inject(html_path: Path, key: str, hash_val: str) -> bool:
    """Canonical replace：偵測舊 gate 整段移除（含 style + div + script），重新注入正版。

    舊邏輯「看到 id=\"_gate\" 就 skip」會讓 placeholder / 舊版 / 雙重 gate 殘留——
    course-web-builder skill 的 placeholder bug、過去版本不同步的 dual-style 都是這樣堆積的。

    新邏輯：
      1. 移除頁內所有 <style id=\"_gs\">...</style>（可能 0..N 個）
      2. 移除頁內所有 <div id=\"_gate\">...</div>（可能 0..N 個）
      3. 移除頁內所有含 'crypto.subtle.digest' 且涉及 gate 的 <script>...</script>
      4. 在 <body> 後注入單一 canonical GATE_TEMPLATE
    """
    content = html_path.read_text(encoding="utf-8")
    original = content

    # 1. 移除舊 style block
    content = re.sub(r'<style id="_gs">[\s\S]*?</style>\s*', '', content)
    # 2. 移除舊 gate div（包含 nested div—— 用 _gate-err 當鎖點，後接 2 個閉合 </div>）
    content = re.sub(
        r'<div id="_gate">[\s\S]*?<div id="_gate-err"></div>\s*</div>\s*</div>\s*',
        '',
        content,
    )
    # 3. 移除舊 gate script（特徵：crypto.subtle.digest + sessionStorage 操作）
    content = re.sub(
        r'<script>\s*\(function\(\)\{[^<]*?crypto\.subtle\.digest[^<]*?\}\)\(\)\s*</script>\s*',
        '',
        content,
    )

    # 4. 注入正版
    gate = GATE_TEMPLATE.format(key=key, hash=hash_val)
    new_content, count = re.subn(
        r'(<body[^>]*>)',
        r'\1\n' + gate,
        content,
        count=1,
        flags=re.IGNORECASE,
    )

    if count == 0:
        print(f"  [SKIP] 找不到 <body>：{html_path.name}")
        return False

    if new_content == original:
        # 已經是 canonical，沒實際變更
        return False

    html_path.write_text(new_content, encoding="utf-8")
    return True


def main():
    total_injected = 0
    total_skipped = 0
    total_missing = 0

    for course_name, (key, hash_val) in COURSES.items():
        course_dir = BASE / course_name
        if not course_dir.exists():
            print(f"[WARN] 課程目錄不存在：{course_dir}")
            total_missing += 1
            continue

        html_files = list(course_dir.rglob("*.html"))
        injected = skipped = 0

        for f in sorted(html_files):
            result = inject(f, key, hash_val)
            if result:
                injected += 1
            else:
                skipped += 1

        print(f"[{course_name}] 注入 {injected} 個，跳過 {skipped} 個（共 {len(html_files)} 個）")
        total_injected += injected
        total_skipped += skipped

    print(f"\n完成：注入 {total_injected}，跳過 {total_skipped}，課程目錄缺失 {total_missing}")


if __name__ == "__main__":
    main()
