#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
import hashlib, json, zipfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).parent
BACKUP = ROOT/'_backup/2026-10-09-instructor-pre'
PAGES = [f'chapters/CH{i}.html' for i in range(1,6)] + ['part4/SUPP4-3.html', 'part2/BUDGET-2.html', 'index.html', 'playground/index.html']
errors = []; page_results = []

def check(ok, msg):
    if not ok: errors.append(msg)

for rel in PAGES:
    path = ROOT/rel; doc = BeautifulSoup(path.read_text(), 'html.parser'); before = BeautifulSoup((BACKUP/rel).read_text(), 'html.parser')
    for tag in ('style', 'script'):
        check([x.get_text() for x in doc.select(tag)] == [x.get_text() for x in before.select(tag)], f'{rel}: changed {tag}')
    for selector in ('.lesson-nav', '.topbar', '#_gate', '#course-gate', '#gate-overlay'):
        check([str(x) for x in doc.select(selector)] == [str(x) for x in before.select(selector)], f'{rel}: changed {selector}')
    ids = [x['id'] for x in doc.select('[id]')]
    check(len(ids) == len(set(ids)), f'{rel}: duplicate ids')
    copy_results = []
    for btn in doc.select('[data-policy-copy]'):
        ident = btn['data-policy-copy']; target = doc.find(id=ident)
        check(target is not None and target.name == 'pre', f'{rel}: missing copy pre {ident}')
        check(doc.find(id=ident+'-policy-status') is not None, f'{rel}: missing copy status {ident}')
        copy_results.append(ident)
    for a in doc.select('a[href]'):
        parsed = urlparse(a['href'])
        if parsed.scheme or parsed.netloc: continue
        target = (path.parent/unquote(parsed.path)).resolve() if parsed.path else path
        check(target.exists(), f'{rel}: missing link {a["href"]}')
        if target.exists() and parsed.fragment and target.suffix == '.html':
            linked = doc if target == path else BeautifulSoup(target.read_text(), 'html.parser')
            check(linked.find(id=unquote(parsed.fragment)) is not None, f'{rel}: missing anchor {a["href"]}')
    page_results.append({'page':rel, 'copy_targets':copy_results, 'styles_scripts_navigation_preserved':True})

# Core version chain and the operation path remain explicit.
def body(n):
    return BeautifulSoup((ROOT/f'chapters/CH{n}.html').read_text(), 'html.parser').select_one('.lesson-body')
check('若 v1 一開始就全部正確' in body(3).get_text(), 'CH3: no already-correct path')
check('繼續用 v1' not in body(4).get_text(), 'CH4: old rollback persists')
check('先在 v2 還原' not in body(5).get_text(), 'CH5: wrong version persists')
check('schedule-A-v3.json' in body(5).get_text() and 'schedule-B-v3.json' in body(5).get_text(), 'CH5: new backup names missing')
check(body(1).find(id='prompt-snake-style') is None, 'CH1: extension not relocated')
supp = BeautifulSoup((ROOT/'part4/SUPP4-3.html').read_text(), 'html.parser')
for ident in ['prompt-snake-style','prompt-snake-features','prompt-snake-polish']:
    original = BeautifulSoup((BACKUP/'chapters/CH1.html').read_text(), 'html.parser').find(id=ident)
    check(supp.find(id=ident).get_text() == original.get_text(), f'moved complete prompt altered: {ident}')
for ident in ['prompt-revision-example-case','prompt-calculation-case','prompt-multi-condition-case']:
    case = body(2).find(id=ident).get_text()
    check(not any(x in case for x in ['核對答案','預期：','應同時','應顯示','挑戰完成','估算合計26000']), f'answer in initial case copy: {ident}')
check(not body(2).find(id='write-own').find_parent('details'), 'CH2: writing task hidden')
check(body(2).find(id='ch2-section-4').find_parent('details') is not None, 'CH2: alternate snake example not optional')
check(body(2).find(id='ch2-section-7').find_parent('details') is not None, 'CH2: alternate claim example not optional')

budgetcase = (ROOT/'assets/materials/prompt-budget-case.txt').read_text().strip()
check(budgetcase == body(2).find(id='prompt-calculation-case').get_text(), 'budget case TXT differs from CH2')
check(budgetcase == BeautifulSoup((ROOT/'part2/BUDGET-2.html').read_text(), 'html.parser').find(id='prompt-budget-case').get_text(), 'budget case TXT differs from E02')
for name,n,ident in [('prompt-snake.txt',1,'prompt-snake'),('prompt-snake-case.txt',1,'prompt-snake-case'),('prompt-snake-revision.txt',1,'prompt-snake-revision'),('prompt-own-requirement.txt',2,'prompt-own-requirement'),('prompt-schedule.txt',3,'prompt-schedule'),('prompt-schedule-repair.txt',3,'prompt-schedule-repair'),('prompt-solo-schedule.txt',4,'prompt-solo-schedule'),('prompt-schedule-rule-repair.txt',4,'prompt-schedule-repair'),('prompt-budget-warning.txt',4,'prompt-budget-warning')]:
    check((ROOT/'assets/materials'/name).read_text().strip() == body(n).find(id=ident).get_text(), f'prompt TXT mismatch {name}')

with zipfile.ZipFile(ROOT/'assets/materials/materials.zip') as z:
    expected = {p.name:p for p in (ROOT/'assets/materials').iterdir() if p.is_file() and p.suffix != '.zip'}
    check(set(z.namelist()) == set(expected), 'materials ZIP entries mismatch')
    for name,p in expected.items(): check(z.read(name) == p.read_bytes(), f'materials ZIP content differs: {name}')
with zipfile.ZipFile(ROOT/'assets/playground/playground-materials.zip') as z:
    expected = {str(p.relative_to(ROOT)):p for folder in [ROOT/'assets/playground', ROOT/'assets/materials'] for p in folder.rglob('*') if p.is_file() and p.suffix != '.zip'}
    check(set(z.namelist()) == set(expected)|{'README.txt'}, 'playground ZIP entries mismatch')
    for name,p in expected.items(): check(z.read(name) == p.read_bytes(), f'playground ZIP content differs: {name}')

# Full catalog relationships and all initial case/answer material remain intact.
catalog = json.loads((ROOT/'_source/playground/catalog.json').read_text())
check(len(catalog['cases']) == 29 and len(catalog['references']) == 13, 'course framework count changed')
for case in catalog['cases']:
    check((ROOT/case['page']).exists() and (ROOT/case['source']).exists(), f'catalog missing {case["id"]}')
    parsed = BeautifulSoup((ROOT/case['page']).read_text(), 'html.parser')
    for i,pre in enumerate(parsed.select('[data-policy-prompt]'),1):
        name = 'prompt.txt' if i == 1 else f'prompt-{i}.txt'
        check((ROOT/'assets/playground'/case['id']/name).read_text().strip() == pre.get_text().strip(), f'playground prompt mismatch {case["id"]}/{name}')
    for name in ['cases.txt','answers.md']: check((ROOT/'assets/playground'/case['id']/name).exists(), f'playground missing {case["id"]}/{name}')
manual = json.loads((ROOT/'_repair/2026-10-08/playground-build/manual-content-review.json').read_text())
check(manual['cases']['E02']['source_sha256'] == hashlib.sha256((ROOT/'_source/supplements/part2-BUDGET-2.md').read_bytes()).hexdigest(), 'E02 review fingerprint stale')
result = {'status':'PASS' if not errors else 'FAIL', 'pages':page_results, 'all_playground_cases_checked':29, 'references_preserved':13, 'errors':errors, 'platform_generation':'PENDING', 'human_follow_along':'PENDING'}
(OUT/'static-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print(json.dumps({'status':result['status'],'affected_pages':len(PAGES),'cases_checked':29,'errors':errors}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
