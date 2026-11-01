"""把驗收通過的改寫稿寫進正式正文 _lessons/canva-video-teaching/。

用法（在 repo 根目錄）：
python3 courses/canva-video-teaching/_review/2026-11-01/apply-round.py <改寫稿資料夾> CH1-1 CH1-2 ...
寫完再跑 `python3 courses/canva-video-teaching/_tools/render-lessons.py <units>` 轉製 HTML。
"""
import re, sys
from pathlib import Path

repo = Path(__file__).resolve().parents[4]
lessons = repo / '_lessons/canva-video-teaching'
MINUTES = {'CH2-2': 30, 'CH2-3': 30}  # 新大綱調整的時數
src, units = Path(sys.argv[1]), sys.argv[2:]

for u in units:
    text = re.split(r'\n## 自我檢查', (src / f'{u}.md').read_text())[0].strip()
    lines = [l.strip() for l in text[:text.index('\n## ')].splitlines() if l.strip()]
    title = lines[0].lstrip('# ').strip()
    subtitle = lines[1]
    artifact = re.sub(r'^本節完成物：', '', next(l for l in lines if l.startswith('本節完成物'))).strip()

    p = lessons / f'{u}.md'
    raw = p.read_text()
    fm = re.match(r'---\n([\s\S]*?)\n---\n', raw).group(1)
    fm = re.sub(r'(?m)^title: .*$', f'title: {title}', fm)
    fm = re.sub(r'(?m)^learning_objective: .*$', f'learning_objective: "{artifact}"', fm)
    if 'subtitle:' not in fm:
        fm = re.sub(r'(?m)^(learning_objective: .*)$', rf'\1\nsubtitle: "{subtitle}"', fm)
    else:
        fm = re.sub(r'(?m)^subtitle: .*$', f'subtitle: "{subtitle}"', fm)
    if u in MINUTES:
        fm = re.sub(r'(?m)^duration_minutes: .*$', f'duration_minutes: {MINUTES[u]}', fm)
    fm = re.sub(r'(?m)^platform_version: .*$', 'platform_version: "2026-11-01 依 Canva 說明中心繁中版與定價頁改寫；新功能待授課帳號實跑"', fm)
    fm = re.sub(r'(?m)^revision: .*$', 'revision: 2026-11-01', fm)
    fm = re.sub(r'(?m)^status: .*$', 'status: REWRITE_2026-11-01', fm)

    before = raw[raw.index('\n---\n', 4) + 5:raw.index('<!-- learner-content:start -->')]
    after = raw[raw.index('<!-- learner-content:end -->') + len('<!-- learner-content:end -->'):].rstrip('\n')
    note = ('\n\n### 2026-11-01 改寫紀錄（不進講義）\n\n'
            '依 `courses/canva-video-teaching/_review/2026-11-01/改寫規格書.md` 重寫：補足 Canva 影音功能、每頁一條成功路徑、前後頁承接。'
            '上方講師筆記的配時與平台說明以改寫前內容為準，現行配時見正式大綱。驗收：PM 腳本檢查與事實抽查；新功能尚未在授課帳號實跑。\n')
    if '2026-11-01 改寫紀錄' not in after:
        after += note
    p.write_text(f'---\n{fm}\n---\n{before}<!-- learner-content:start -->\n{text}\n\n<!-- learner-content:end -->{after}')
    print(u, '→', title)
