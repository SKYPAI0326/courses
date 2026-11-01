"""模組總覽頁同步（一次性）：單元卡標題與完成物、M9 卡片順序、「AI 接口」改成「模組作業」。

用法（在 courses/digital-marketing-70h 下）：python3 _review/2026-11-01/update-module-pages.py
資料來源：_lessons/digital-marketing-70h/lesson-meta.json（標題、完成物、順序）與 outline-draft.md（模組作業）。
只處理有 unit-card 的總覽頁；module1 沒有卡片，另行人工修改。
"""
import json, re
from html import escape
from pathlib import Path

root = Path(__file__).resolve().parents[2]
meta = json.loads((root.parents[1] / '_lessons' / root.name / 'lesson-meta.json').read_text())
draft = (Path(__file__).with_name('outline-draft.md')).read_text()
work = {}
for code, body in re.findall(r'\n### (M\d+) [^\n]+\n([\s\S]*?)(?=\n### M\d+ |\n---\n)', draft):
    a = re.search(r'\*\*模組作業：([^*]+)\*\*\n((?:- [^\n]+\n)+)', body)
    if a:
        work[code] = (a.group(1), [l[2:] for l in a.group(2).splitlines()])

for n in range(1, 11):
    code, f = f'M{n}', root / f'module{n}.html'
    text = f.read_text()
    pages = [p for p in meta['pages'] if p['module'] == code]
    cards = {p['file']: (f'      <a href="{p["file"]}" class="unit-card">\n        <div class="unit-num">{p["num"]}</div>\n'
                         f'        <div class="unit-name">{escape(p["short"])}</div>\n        <div class="unit-desc">完成物：{escape(p["artifact"])}</div>\n      </a>') for p in pages}
    found = re.findall(r'<a href="([^"]+)" class="unit-card">', text)
    if not found:
        continue
    # 卡片依 meta 順序重排：把第一張到最後一張之間整段換掉（縮排各頁不同，保留第一張前的縮排）
    s = text.index(f'<a href="{found[0]}" class="unit-card">') - 6
    e = text.index('</a>', text.index(f'<a href="{found[-1]}" class="unit-card">')) + 4
    s = text.rindex('\n', 0, s + 6) + 1
    # module2 卡片分散在四個子區塊，整段替換會吃掉子區塊標題，改由人工逐張處理
    if set(found) == set(cards) and code != 'M2':
        text = text[:s] + '\n'.join(cards[p['file']] for p in pages) + text[e:]
    if code in work:
        name, lines = work[code]
        text = re.sub(r'<div class="meta-item">AI 接口：<strong>[^<]*</strong></div>', f'<div class="meta-item">模組作業：<strong>{escape(name)}</strong></div>', text)
        items = '\n'.join(f'      <li>{escape(l)}</li>' for l in lines)
        block = (f'<div class="lesson-section">\n  <div class="section-eyebrow">模組作業</div>\n  <h2 class="section-heading">分組作業：<em>{escape(name)}</em></h2>\n'
                 f'  <div class="ai-interface">\n    <div class="ai-label">各組用自己的主題產品完成，上台分享</div>\n    <ul class="ai-list">\n{items}\n    </ul>\n  </div>\n</div>')
        text = re.sub(r'<div class="lesson-section">\s*<div class="section-eyebrow">AI 接口[^<]*</div>[\s\S]*?</ul>\s*</div>\s*</div>', block.replace('\\', r'\\'), text, count=1)
    f.write_text(text)
    print(code, 'cards', len(found), 'assignment', code in work)
