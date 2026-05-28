#!/usr/bin/env python3
"""
inject_reveal_fallback.py — 在有 .reveal{opacity:0} 規則的 HTML 注入 IntersectionObserver fallback

問題：IntersectionObserver 在某些 timing（page load + scroll restore + viewport 邊界判斷）
會漏掉首屏 reveal 元素，造成元素永遠 opacity:0 看起來像「大塊空白」。
2026-05-28 在 gen-ai-140h/part5/CH5-1 首次觸發。

修補：在 </body> 前注入獨立 fallback script，1.5s 後強制把所有 .reveal:not(.in) 補上 .in。
不影響 IntersectionObserver 動畫，只在它 miss 時兜底。
"""
import re
import sys
from pathlib import Path

MARKER = "<!-- reveal-fallback v1 -->"
FALLBACK = (
    f"{MARKER}\n"
    "<script>setTimeout(function(){"
    "document.querySelectorAll('.reveal:not(.in),.section-rule:not(.in)')"
    ".forEach(function(el){el.classList.add('in')})"
    "},1500);</script>\n"
)

PATTERN_HAS_REVEAL_CSS = re.compile(r"^\.reveal\{opacity:0", re.MULTILINE)
PATTERN_BODY_END = re.compile(r"(\s*</body>)", re.IGNORECASE)


def inject(path: Path) -> str:
    """Returns 'skip'/'inject'/'already'."""
    content = path.read_text(encoding="utf-8")
    if not PATTERN_HAS_REVEAL_CSS.search(content):
        return "skip"
    if MARKER in content:
        return "already"
    new, n = PATTERN_BODY_END.subn(f"\n{FALLBACK}\\1", content, count=1)
    if n == 0:
        return "skip"
    path.write_text(new, encoding="utf-8")
    return "inject"


def main():
    if len(sys.argv) < 2:
        print("用法：python3 inject_reveal_fallback.py <目錄或檔案>")
        sys.exit(1)
    target = Path(sys.argv[1])
    if target.is_file():
        files = [target]
    else:
        files = sorted(target.rglob("*.html"))
    counts = {"inject": 0, "already": 0, "skip": 0}
    for f in files:
        r = inject(f)
        counts[r] += 1
        if r == "inject":
            print(f"  [INJECT] {f.relative_to(target if target.is_dir() else target.parent)}")
    print(f"\n完成：注入 {counts['inject']}、已存在 {counts['already']}、略過 {counts['skip']}（共 {len(files)} 檔）")


if __name__ == "__main__":
    main()
