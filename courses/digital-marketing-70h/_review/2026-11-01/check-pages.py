"""PM 自動檢查：改寫稿是否守住 `改寫規格書-共通.md` 的硬規則（沿用 gen-ai-36h 版，改成本課規則）。

用法（在 courses/digital-marketing-70h 下）：
python3 _review/2026-11-01/check-pages.py _review/2026-11-01/round1 [m3-2 m3-4 …]
不給單元就檢查資料夾內全部 md。只檢查學員正文（「## 自我檢查」之前）。結果只是篩選，需要判斷的再人工看。
"""
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
meta = {p['unit']: p for p in json.loads((root.parents[1] / '_lessons' / root.name / 'lesson-meta.json').read_text())['pages']}
last = {}
for p in meta.values():
    last[p['module']] = p['unit']  # 依 meta 順序，模組最後一頁
MCODE = re.compile(r'(?<![A-Za-z0-9])(?:M\d{1,2}[A-D]?(?:-\d)?|\d{1,2}[A-D]?-\d|Module \d+|Part \d)(?![A-Za-z0-9.])')
FILE = re.compile(r'(?<![/\w])[\w-]+\.(?:md|csv|json)\b')
STATUS = re.compile(r'\b(?:[A-Z]{3,}(?: [A-Z]{3,})+|PENDING|PASS|VERIFIED|NOT_RUN)\b')
IDS = re.compile(r'\b(?:WEB|INT|REV|SOCIAL|BRIEF|SEARCH|MEASURE|AD|LIST|EMAIL|LINE)-\d{2}\b')
CAVEAT = re.compile(r'不能|不要|不可|不得|仍(?:須|要|需)')
PEER = re.compile(r'互評|互相評|互打分|投票|評分表|同儕回饋|旁邊的人|鄰座|交換')
AIWORD = re.compile(r'AI|ChatGPT|Claude|Gemini|提示詞')
SUBS = ['個人準備', '小組討論', '上台分享', '回饋', '放進企劃書']

src = Path(sys.argv[1])
units = sys.argv[2:] or sorted(p.stem for p in src.glob('*.md'))
for u in units:
    text = (src / f'{u}.md').read_text()
    body = re.split(r'\n## 自我檢查', text)[0]
    m, issues = meta[u], []
    lines = [l for l in body.split('\n## ', 1)[0].splitlines() if l.strip()]
    if len(lines) != 3:
        issues.append(f'第一個小節前有 {len(lines)} 行（應為 3）')
    if lines and lines[0].removeprefix('# ').strip() != m['title']:
        issues.append(f'標題不符：{lines[0][:30]}')
    if not any(l == '本節完成物：' + m['artifact'] for l in lines):
        issues.append('完成物不符')
    prose = re.sub(r'```[\s\S]*?```', '', body)
    plain = re.sub(r'\]\([^)]*\)', ']', prose)
    for name, pat in [('模組／單元碼', MCODE), ('檔名', FILE), ('英文狀態碼', STATUS), ('證據 ID', IDS)]:
        if f := sorted(set(pat.findall(plain))):
            issues.append(f'{name}：{f[:6]}')
    if p := re.findall(r'```[^\n]*\n((?:你是|請|幫我|扮演)[^\n]{0,12})', body):
        issues.append(f'提示詞開頭：{p}')
    secs = re.split(r'\n(?=## )', prose)[1:]
    over = [s.split('\n')[0][3:15] for s in secs if len([x for x in re.split(r'[。！？\n]', s) if CAVEAT.search(x)]) > 1]
    if over:
        issues.append(f'限制語超過一句的小節 {len(over)}：{over[:3]}')
    if p := PEER.findall(prose):
        issues.append(f'互評／交換字樣：{sorted(set(p))}')
    ai_secs = [s for s in secs if s.startswith('## 用 AI 加速')]
    if m['module'] == 'M1' and AIWORD.search(plain):
        issues.append('消費者心理模組出現 AI')
    if m['module'] not in ('M1', 'M2') and len(ai_secs) > 1:
        issues.append(f'「用 AI 加速」小節 {len(ai_secs)} 個')
    assign = [s for s in secs if s.startswith('## 模組作業')]
    if u == last[m['module']]:
        if len(assign) != 1:
            issues.append('模組最後一頁缺模組作業')
        elif miss := [x for x in SUBS if f'### {x}' not in assign[0]]:
            issues.append(f'作業缺子標題：{miss}')
    elif assign:
        issues.append('非模組最後一頁出現模組作業')
    links = re.findall(r'\]\(([^)#\s]+)', body)
    if miss := [l for l in links if not l.startswith('http') and not (root / l).exists()]:
        issues.append(f'連結不存在：{miss}')
    n = len(re.sub(r'\s', '', body))
    if not 1800 <= n <= 4200:
        issues.append(f'字數 {n}')
    print(f'{u}: {n} 字、{len(secs)} 節；' + ('；'.join(issues) if issues else '無硬規則問題'))
