"""PM 自動檢查：改寫稿是否守住規格書的硬規則。

用法（在 courses/gen-ai-36h 下）：
python3 _review/2026-11-01/check-pages.py _review/2026-11-01/part34/round1 CH3-1 CH3-2 PRAC3
只檢查學員正文（「## 自我檢查」之前）。結果只是篩選，需要判斷的再人工看。
"""
import re, sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
CODE = re.compile(open(Path(__file__).with_name('measure.py')).read().split("CODE = re.compile(r'")[1].split("')\n")[0])
FORBIDDEN = re.compile(r'\b(?:[A-Z]{1,4}\d{2}[ab]?|SRC-\w+|MSG-\d+|CN-\d+|REG-\d+|MTG-\d+|UP-\d+|NOT_RUN|PENDING|CH\d-\d)\b')
CAVEAT = re.compile(r'不能|不要|不可|不代表|仍(?:須|要|需)')
PEER = re.compile(r'同伴|同學|旁邊的人|分組|互相')

src, units = Path(sys.argv[1]), sys.argv[2:]
for u in units:
    text = (src / f'{u}.md').read_text()
    body = re.split(r'\n## 自我檢查', text)[0]
    issues = []
    n = len(re.sub(r'\s', '', body)) or 1
    head = body[:body.index('\n## ')] if '\n## ' in body else body
    extra = [l for l in head.splitlines()[1:] if l.strip() and not l.startswith('本節完成物')][1:]
    if extra:
        issues.append(f'第一個小節前有正文 {len(extra)} 行')
    prose = re.sub(r'```[\s\S]*?```', '', body)
    prose_nolink = re.sub(r'\]\([^)]*\)', ']', prose)
    if f := sorted(set(FORBIDDEN.findall(prose_nolink))):
        issues.append(f'代碼：{f}')
    if p := re.findall(r'```[^\n]*\n((?:你是|請扮演|扮演一位)[^\n]{0,15})', body):
        issues.append(f'提示詞開頭：{p}')
    if p := re.findall(r'.{0,8}Part \d.{0,8}', prose):
        issues.append(f'Part 編號引用：{p[:3]}')
    if p := PEER.findall(prose):
        issues.append(f'同伴互動字樣 {len(p)} 處')
    secs = re.split(r'\n(?=## )', prose)[1:]
    over = [i + 1 for i, s in enumerate(secs) if len([x for x in re.split(r'[。！？\n]', s) if CAVEAT.search(x)]) > 1]
    if over:
        issues.append(f'限制語超過一句的小節：{over}')
    missing = [l for l in re.findall(r'\]\((\.\./assets/[^)#\s]+)', body) if not (root / l.replace('../', '', 1)).exists()]
    if missing:
        issues.append(f'連結不存在：{missing}')
    dens = round(len(CODE.findall(body)) / n * 1000, 1)
    print(f'{u}: 識別碼 {dens}/千字；' + ('；'.join(issues) if issues else '無硬規則問題'))
