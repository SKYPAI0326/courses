#!/usr/bin/env python3
"""verify-hours.py — gen-ai-140h 三方時數一致性檢查
比對：(A) HTML data-duration / (B) _outlines/gen-ai-140h.md / (C) courses/gen-ai-140h/_講師指引/part{1-5}.md

使用：
  python3 docs/verify-hours.py            # 全檢查
  python3 docs/verify-hours.py --json     # JSON 輸出
"""
import re, json, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
COURSE = ROOT / 'courses' / 'gen-ai-140h'
OUTLINE = ROOT / '_outlines' / 'gen-ai-140h.md'
GUIDE_DIR = COURSE / '_講師指引'

UNIT_RE = re.compile(r'(CH|PRAC)\d+-\d+', re.IGNORECASE)


def get_html_durations():
    """從 HTML 抽出 {unit: classroom_h} dict"""
    out = {}
    for n in '12345':
        part_dir = COURSE / f'part{n}'
        if not part_dir.exists():
            continue
        for html in part_dir.glob('*.html'):
            process_html(html, out)
    return out


def process_html(path, out):
    name = path.stem  # CH1-1
    if not UNIT_RE.fullmatch(name):
        return
    text = path.read_text(encoding='utf-8')
    m = re.search(r'data-duration="([0-9.]+)h"', text)
    if m:
        out[name.upper()] = float(m.group(1))


def get_outline_durations():
    """從大綱 markdown 抽出 {unit: classroom_h} dict"""
    out = {}
    if not OUTLINE.exists():
        return out
    text = OUTLINE.read_text(encoding='utf-8')
    # 形如：- CH1-1：... *(課堂 2h / 自學 1h)*
    pat = re.compile(r'-\s+((?:CH|PRAC)\d+-\d+)[:：][^*\n]*\*\(課堂\s*([0-9.]+)h')
    for m in pat.finditer(text):
        out[m.group(1).upper()] = float(m.group(2))
    return out


def get_guide_durations():
    """從講師指引 markdown 抽出 {unit: classroom_h} dict（依 140h 欄位）"""
    out = {}
    for md in sorted(GUIDE_DIR.glob('part*.md')):
        if not md.exists():
            continue
        text = md.read_text(encoding='utf-8')
        # 形如：| CH1-1 | 2h | ...
        pat = re.compile(r'\|\s*((?:CH|PRAC)\d+-\d+)\s*\|\s*([0-9.]+)h\s*\|')
        for m in pat.finditer(text):
            out[m.group(1).upper()] = float(m.group(2))
    return out


def main():
    json_mode = '--json' in sys.argv
    html = get_html_durations()
    outline = get_outline_durations()
    guide = get_guide_durations()

    all_units = sorted(set(html.keys()) | set(outline.keys()) | set(guide.keys()))
    diffs = []
    for u in all_units:
        h = html.get(u)
        o = outline.get(u)
        g = guide.get(u)
        rec = {'unit': u, 'html': h, 'outline': o, 'guide': g}
        if h is not None:
            if o is not None and o != h:
                rec['issue'] = f'outline {o}h ≠ html {h}h'
                diffs.append(rec)
            elif g is not None and g != h:
                rec['issue'] = f'guide {g}h ≠ html {h}h'
                diffs.append(rec)
            elif o is None and g is None:
                rec['issue'] = 'html only (outline/guide missing)'
                diffs.append(rec)
        else:
            rec['issue'] = 'no html record'
            diffs.append(rec)

    if json_mode:
        print(json.dumps({'total': len(all_units), 'diffs': diffs},
                         ensure_ascii=False, indent=2))
    else:
        print(f'掃描單元：{len(all_units)}')
        print(f'三方一致：{len(all_units) - len(diffs)}')
        print(f'有差異：{len(diffs)}')
        if diffs:
            print('\n--- 差異清單 ---')
            for d in diffs:
                print(f'  {d["unit"]:10s} html={d.get("html","-")} '
                      f'outline={d.get("outline","-")} '
                      f'guide={d.get("guide","-")}  ← {d["issue"]}')

    return 1 if diffs else 0


if __name__ == '__main__':
    sys.exit(main())
