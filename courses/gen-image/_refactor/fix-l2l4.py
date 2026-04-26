#!/usr/bin/env python3
"""L2/L4 → 線稿/完稿 batch replacement for gen-image course HTML pages.

依 _outlines/gen-image.style-guide.md 第 22 行硬規：
  L0-L4 wireframe 五級 → 線稿 / 完稿（二分）

保護不變動：
  - 圖檔名 L[024][_-]xxx.png
  - placeholder 命名 L[024]_編號{XX}
  - L0_xxx.png / L2_01.png 等

替換順序：
  1. 完整詞「L2 視覺化線稿」「L4 完稿」「L2 線稿」→ 線稿 / 完稿
  2. L2-A / L2-B（CH3-2 情境題範例代號）→ 線稿 A / 線稿 B
  3. 裸 L2 / L4 → 線稿 / 完稿
  4. 收尾去重複「線稿 線稿」「完稿 完稿」

Usage:
  python3 _refactor/fix-l2l4.py courses/gen-image/CH3-1.html
  python3 _refactor/fix-l2l4.py courses/gen-image/*.html
"""
import re
import sys
from pathlib import Path

REPLACEMENTS = [
    (re.compile(r'L2\s*視覺化線稿'), '線稿'),
    (re.compile(r'L4\s*完稿'), '完稿'),
    (re.compile(r'L2\s*線稿'), '線稿'),
    (re.compile(r'L0\s*結構\s*JSON'), '結構 JSON'),
    (re.compile(r'L2-A(?![A-Za-z0-9_])'), '線稿 A'),
    (re.compile(r'L2-B(?![A-Za-z0-9_])'), '線稿 B'),
    (re.compile(r'L2(?![A-Za-z0-9_\-])'), '線稿'),
    (re.compile(r'L4(?![A-Za-z0-9_\-])'), '完稿'),
]

PROTECT_PATTERNS = [
    re.compile(r'L[024][_\-][\w\-]*\.(?:png|jpg|jpeg|svg|webp)'),
    re.compile(r'L[024]_編號\{[^}]+\}'),
    re.compile(r'L[024]_\d+\.png'),
]

def process(text):
    protected = {}
    counter = [0]

    def protect(m):
        key = f"\x00PROTECT{counter[0]}\x00"
        protected[key] = m.group(0)
        counter[0] += 1
        return key

    for pat in PROTECT_PATTERNS:
        text = pat.sub(protect, text)

    for pat, repl in REPLACEMENTS:
        text = pat.sub(repl, text)

    text = re.sub(r'(線稿)\s*(?=線稿)', '', text)
    text = re.sub(r'(完稿)\s*(?=完稿)', '', text)

    # 清掉「中文字 + 空白 + 線稿/完稿」與「線稿/完稿 + 空白 + 中文字」殘留間距
    cjk = r'[一-鿿]'
    text = re.sub(rf'({cjk})\s+(線稿|完稿)', r'\1\2', text)
    text = re.sub(rf'(線稿|完稿)\s+({cjk})', r'\1\2', text)

    for key, original in protected.items():
        text = text.replace(key, original)

    return text


if __name__ == '__main__':
    files = sys.argv[1:]
    if not files:
        print("Usage: fix-l2l4.py <file.html> [...]")
        sys.exit(1)

    for fp in files:
        path = Path(fp)
        original = path.read_text(encoding='utf-8')
        modified = process(original)
        if original != modified:
            path.write_text(modified, encoding='utf-8')
            l2_b = len(re.findall(r'L2', original))
            l2_a = len(re.findall(r'L2', modified))
            l4_b = len(re.findall(r'L4', original))
            l4_a = len(re.findall(r'L4', modified))
            print(f"{path.name}: L2 {l2_b}→{l2_a}  L4 {l4_b}→{l4_a}")
        else:
            print(f"{path.name}: (no change)")
