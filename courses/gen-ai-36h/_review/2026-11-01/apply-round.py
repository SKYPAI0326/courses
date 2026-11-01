"""把驗收通過的改寫稿寫進正式講義：_lessons、教案指向、lesson-meta、首頁卡片標題。

用法（在 courses/gen-ai-36h 下）：
python3 _review/2026-11-01/apply-round.py _review/2026-11-01/part34/round1 "規格書路徑" CH3-1 CH3-2 PRAC3
寫完再跑 `python3 _tools/render-lessons.py <units>` 轉製 HTML。
"""
import re, sys, json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
lessons = root.parents[1] / '_lessons' / root.name
src, spec, units = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
meta_p = root / '_repair/2026-10-09/lesson-meta.json'
meta = json.loads(meta_p.read_text())
index_p = root / 'index.html'
index = index_p.read_text()

for u in units:
    text = re.split(r'\n## 自我檢查', (src / f'{u}.md').read_text())[0]
    title = re.search(r'^# (.+)$', text, re.M).group(1).strip()
    first = text.index('\n## ')
    lines = [l.strip() for l in text[:first].splitlines() if l.strip()]
    subtitle = lines[1]
    artifact = re.sub(r'^本節完成物：', '', next(l for l in lines if l.startswith('本節完成物'))).rstrip('。')
    body = text[first + 1:].strip()
    intro = [l for l in lines[2:] if not l.startswith('本節完成物')]
    if intro:  # 轉製程式只轉小節內容，開場段併進第一節
        h, rest = body.split('\n', 1)
        body = h + '\n\n' + '\n\n'.join(intro) + '\n\n' + rest.lstrip()

    p = lessons / f'{u}.md'
    fm = re.match(r'---\n([\s\S]*?)\n---\n', p.read_text()).group(1)
    fm = re.sub(r'(?m)^title: .*$', f'title: {title}', fm)
    fm = re.sub(r'(?m)^learning_objective: .*$', f'learning_objective: {subtitle}', fm)
    fm = re.sub(r'(?m)^platform_version: .*$', 'platform_version: 2026-11-01 依改寫規格書重寫；介面待帳號實跑', fm)
    teacher = (f'## 教師與版本紀錄（不轉製學員正文）\n'
               f'- 2026-11-01 依 `{spec}` 重寫：學員指揮 AI 完成工作，核對交給 AI，學員只抽看 AI 標出的 3 處以內。\n'
               f'- 驗收：PM 自動檢查與事實抽查（精簡流程）。平台實跑與真人試讀尚未進行。\n')
    p.write_text(f'---\n{fm}\n---\n\n# {title}\n\n<!-- learner-content:start -->\n{body}\n<!-- learner-content:end -->\n\n{teacher}')

    lp = root / f'_repair/2026-10-09/lesson-plans/{u}.md'
    t = lp.read_text()
    if '學員正文已移至' not in t:
        s, e = t.index('<!-- learner-content:start -->'), t.index('<!-- learner-content:end -->')
        t = t[:s] + f'<!-- learner-content:start -->\n學員正文已移至 `_lessons/gen-ai-36h/{u}.md`（2026-11-01 起），本檔只保留教師與版本紀錄。\n' + t[e:]
        t = t.rstrip('\n') + f'\n- 2026-11-01：上面描述的做法已過期，現行做法見 `_lessons/gen-ai-36h/{u}.md` 的教師紀錄。\n'
        lp.write_text(t)

    old_title = meta[u]['title']
    for cls in ('lesson-title', 'prac-title'):
        index = index.replace(f'<div class="{cls}">{old_title}</div>', f'<div class="{cls}">{title}</div>')
    meta[u].update(title=title, goal=subtitle, artifact=artifact)
    print(u, '→', title)

meta_p.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
index_p.write_text(index)
