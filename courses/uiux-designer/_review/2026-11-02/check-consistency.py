"""跨堂一致性檢查（PM 用）：起始材料與講義名稱、已淘汰名稱、資料筆數、A1 色票對比。

用法：在 courses/uiux-designer/ 下執行 python3 _review/2026-11-02/check-consistency.py _review/2026-11-02/round8
有問題時 exit 1。
"""
import csv, html, importlib.util, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('r', ROOT / '_tools/repair_render_reference.py')
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
UNITS = {u[0].split('-')[0]: u[0] for u in R.UNITS}
NAME = re.compile(r'(?:Screen|Button|Row|List|Login|Detail|Dialog|Toast|Nav|Top Bar|Field|Icon|Tags|Header|Sheet|Menu|Radio Group|Checkbox|Toggle|Select|Components|Flow|IA|Case|Note|Hotspot) / [A-Za-z0-9]+(?: [A-Za-z0-9]+)*')
RETIRED = ['Screen / Completed', 'Login / Content', 'Button / View Completed', 'Button / Base', 'List Long']
# 講義中名稱以外允許出現在起始材料的（素材本身的檔名、示意圖層）
ALLOW = {'Components / Booking'}


def body(f):
    return re.split(r'^## 自我檢查', f.read_text(encoding='utf-8'), flags=re.M)[0]


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def main(rd):
    rd = Path(rd); probs = []
    lessons = {k: body(rd / f'{k}.md') for k in UNITS if (rd / f'{k}.md').exists()}
    alltext = ''.join(lessons.values())
    order = sorted(lessons, key=lambda k: (k[0], int(k[1])))
    # 1. 起始材料出現的物件名稱，必須在該堂或之前的講義出現過
    for i, k in enumerate(order):
        f = ROOT / 'assets' / UNITS[k] / 'START-HERE.html'
        if not f.exists():
            continue
        txt = html.unescape(re.sub(r'<[^>]+>', ' ', f.read_text(encoding='utf-8')))
        seen = ''.join(lessons[x] for x in order[:i + 1])
        for n in sorted(set(NAME.findall(txt))):
            if n not in seen and n not in ALLOW and not re.fullmatch(r'Row / T\d\d', n):
                probs.append(f'起始材料 {k}：`{n}` 不在本堂或之前的講義')
    # 2. 已淘汰名稱
    for n in RETIRED:
        for k, b in lessons.items():
            if n in b:
                probs.append(f'講義 {k}：仍用已淘汰名稱 `{n}`')
        for f in (ROOT / 'assets').glob('*/START-HERE.html'):
            if n in f.read_text(encoding='utf-8'):
                probs.append(f'{f.relative_to(ROOT)}：仍用已淘汰名稱 `{n}`')
    # 3. 主線任務資料筆數
    rows = list(csv.reader((ROOT / 'assets/shared/TASK-DATA.csv').open(encoding='utf-8-sig')))[1:]
    for k, b in lessons.items():
        for m in re.finditer(r'.{0,8}(?<![前第])三筆任務.{0,8}', b):
            probs.append(f'講義 {k}：「{m.group(0)}」，TASK-DATA 有 {len(rows)} 筆')
    for m in re.finditer(r'Row / T(\d\d)', alltext):
        if int(m[1]) > len(rows):
            probs.append(f'講義引用 Row / T{m[1]}，TASK-DATA 只有 {len(rows)} 筆')
    # 4. A1 色票對比（依講義自訂門檻）
    a1 = lessons.get('A1', '')
    var = {m[1]: m[2].upper() for m in re.finditer(r'\| `([A-Za-z ]+)` \| `#([0-9A-Fa-f]{6})`', a1)}
    pairs = [('Card', 'Primary', 4.5), ('Card', 'Primary Hover', 4.5), ('Card', 'Primary Pressed', 4.5),
             ('Text', 'Surface', 4.5), ('Muted', 'Surface', 4.5), ('Text', 'Primary Soft', 4.5),
             ('Disabled Text', 'Disabled', 4.5), ('Error', 'Card', 4.5), ('Success', 'Card', 4.5), ('Warning', 'Card', 4.5),
             ('Control Border', 'Card', 3), ('Control Border', 'Surface', 3), ('Focus Ring', 'Card', 3)]
    for a, b_, need in pairs:
        if a in var and b_ in var:
            r = ratio(var[a], var[b_])
            if r < need:
                probs.append(f'A1 對比：{a} / {b_} = {r:.2f}，低於 {need}')
        else:
            probs.append(f'A1 規格表找不到變數 {a} 或 {b_}')
    # 5. 起始材料 A1 色表與講義一致
    s = (ROOT / 'assets/A1-visual-foundations/START-HERE.html').read_text(encoding='utf-8')
    for name, hx in var.items():
        if f'#{hx}' not in s.upper():
            probs.append(f'A1 起始材料色表缺 {name} #{hx}')
    for p in probs:
        print('-', p)
    print(f'{len(probs)} 個問題')
    return 1 if probs else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
