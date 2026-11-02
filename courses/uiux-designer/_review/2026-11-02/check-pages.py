"""改寫稿硬規則檢查（PM 用，只看規格書第 6 節與第 5 節可機器判斷的部分）。

用法：在 courses/uiux-designer/ 下執行 python3 _review/2026-11-02/check-pages.py _review/2026-11-02/round1
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES = {
    '堂號或代碼': r'第\s?\d{1,2}\s?堂|前堂|(?<![A-Za-z/ ])T0\d(?![0-9])|(?<![A-Za-z])S\d{2}(?![0-9])|TASK-0|SCROLL-0|MOTION-0|EMPTY-TEST|(?<![A-Za-z0-9/])[AB][1-8](?![0-9A-Za-z])',
    '同伴他人': r'同學|同伴|他人|別人|受測者|分組|小組|組員|講師',
    '稽核語': r'假裝|待補|PENDING|不能宣稱|不能據此|真人試跑|機器\s?PASS|證據',
    'AI': r'(?<![A-Za-z])AI(?![A-Za-z])|Figma Make|人工智慧',
    '舊介面名': r'Layout grid|Layout guides／|Present(?!ation)|Reset overrides|Create instance|Destination.{0,4}None|New design file|Vertical scrolling|Export frames to PDF|Dev Mode.{0,6}(開|點選)',
    '你是開頭': r'^你是',
}
CAVEAT = re.compile(r'不要|不能|不是|不算|不可|別把|不必|不需')


def check(f):
    md = f.read_text(encoding='utf-8')
    body = re.split(r'^## 自我檢查', md, flags=re.M)[0]
    probs = []
    head = body.split('\n## ', 1)[0].strip().splitlines()
    head = [l for l in head if l.strip()]
    if len(head) != 3 or not head[0].startswith('# ') or not head[1].startswith('副標') or not head[2].startswith('本堂完成物'):
        probs.append(f'開頭三行格式不符：{len(head)} 行')
    secs = re.split(r'^## ', body, flags=re.M)[1:]
    names = [s.partition('\n')[0].strip() for s in secs]
    if not any(n.startswith('換你做') for n in names): probs.append('缺「換你做」小節')
    if names[-1:] != ['本堂查證來源']: probs.append('最後一節不是本堂查證來源')
    nodetail = re.sub(r'<details>.*?</details>', '', body)
    for k, pat in RULES.items():
        hits = re.findall(pat, re.sub(r'`[^`]*`|\([^)]*\.(?:html|csv|svg|png|psd|json|zip)\)', '', nodetail), flags=re.M)
        if hits: probs.append(f'{k}：{len(hits)} 處 {sorted(set(hits))[:6]}')
    for s in secs:
        h, _, b = s.partition('\n')
        b2 = re.sub(r'<details>.*?</details>|^\|.*$', '', b, flags=re.M)
        n = len(CAVEAT.findall(b2))
        if n > 1: probs.append(f'限制語 {n} 句：{h.strip()}')
    for sent in re.split(r'[。；\n]', re.sub(r'^\|.*$|<details>.*?</details>|`[^`]*`|```.*?```', '', nodetail, flags=re.M | re.S)):
        nums = re.findall(r'(?<![A-Za-z0-9])\d{2,4}(?![0-9])', sent)
        if len(nums) > 3: probs.append(f'一句 {len(nums)} 個數值：{sent.strip()[:40]}')
    for link in re.findall(r'\]\((\.\./[^)#]+)', body):
        if not (ROOT / 'part1' / link).resolve().exists(): probs.append(f'連結不存在：{link}')
    chars = len(re.sub(r'\s', '', re.sub(r'<[^>]+>|[#|*`-]', '', body)))
    return chars, probs


for f in sorted(Path(sys.argv[1]).glob('*.md')):
    chars, probs = check(f)
    print(f'== {f.stem}  {chars} 字  {"OK" if not probs else len(probs)}')
    for p in probs: print('  -', p)
