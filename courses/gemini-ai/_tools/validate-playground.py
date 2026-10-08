#!/usr/bin/env python3
"""Static validation for canonical core, playground and references; excludes historical snapshots."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import subprocess,json,hashlib,zipfile,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_repair/2026-10-08/playground-build';catalog=json.loads((ROOT/'_source/playground/catalog.json').read_text());lessons=[f'chapters/CH{i}.html' for i in range(1,6)]+[c['page'] for c in catalog['cases']]+[r['page'] for r in catalog['references']];pages=['index.html','playground/index.html']+lessons
errors=[];copies=0;prompts=0
for file in pages:
    p=ROOT/file;s=BeautifulSoup(p.read_text(),'html.parser');ids=[x['id'] for x in s.select('[id]')]
    if len(ids)!=len(set(ids)):errors.append((file,'duplicate id'))
    if file in lessons:
        body=s.select_one('.lesson-body');assert body
        if any(not x.find_parent(class_='lesson-body') for x in s.select('.lesson-section,.body-text,.step-list')):errors.append((file,'content outside lesson-body'))
        positions=[p.read_text().find(x) for x in ['class="lesson-hero"','class="lesson-body"','class="lesson-nav"']]
        if positions!=sorted(positions):errors.append((file,'wrapper order'))
        for button in s.select('[data-policy-copy]'):
            copies+=1
            if not s.find(id=button['data-policy-copy']):errors.append((file,'copy target missing'))
        for prompt in s.select('[data-policy-prompt]'):
            prompts+=1
            if not s.select_one('[data-policy-copy="'+prompt['id']+'"]'):errors.append((file,'prompt lacks copy'))
    for a in s.select('a[href],img[src],script[src],link[href]'):
        href=a.get('href',a.get('src'));url=urlsplit(href)
        if url.scheme or href.startswith('//'):continue
        target=(p.parent/unquote(url.path)).resolve() if url.path else p
        if target.is_dir():target=target/'index.html'
        if not target.exists():errors.append((file,'missing link',href));continue
        if url.fragment and target.suffix=='.html':
            targetdoc=s if target==p else BeautifulSoup(target.read_text(),'html.parser')
            if not targetdoc.find(id=unquote(url.fragment)):errors.append((file,'missing anchor',href))
# Exact prompt download match and case material existence for all library entries.
for c in catalog['cases']:
    s=BeautifulSoup((ROOT/c['page']).read_text(),'html.parser');ps=s.select('[data-policy-prompt]')
    for i,pr in enumerate(ps,1):
        f=ROOT/'assets/playground'/c['id']/('prompt.txt' if i==1 else f'prompt-{i}.txt')
        if not f.exists() or f.read_text()!=pr.get_text():errors.append((c['id'],'TXT prompt drift',str(f)))
    for name in ['cases.txt','answers.md']:
        if not (ROOT/'assets/playground'/c['id']/name).exists():errors.append((c['id'],'material missing',name))
with zipfile.ZipFile(ROOT/'assets/playground/playground-materials.zip') as z:
    for p in (ROOT/'assets/playground').rglob('*'):
        if p.is_file() and p.suffix!='.zip' and z.read(str(p.relative_to(ROOT)))!=p.read_bytes():errors.append(('zip drift',str(p)))
lint=subprocess.run(['python3',str(ROOT.parents[1]/'docs/lint-page.py'),*[str(ROOT/f) for f in pages],'--summary','--by-bucket'],text=True,capture_output=True)
(OUT/'lint.txt').write_text(lint.stdout+lint.stderr)
structure=subprocess.run(['python3','/Users/paichenwei/.agents/skills/course-html-contract/scripts/validate_html_structure.py',*[str(ROOT/f) for f in lessons]],text=True,capture_output=True)
(OUT/'structure.txt').write_text(structure.stdout+structure.stderr)
result={'pages':len(pages),'lessons':len(lessons),'cases':len(catalog['cases']),'references':len(catalog['references']),'copies':copies,'prompt_areas':prompts,'link_and_material_errors':errors,'lint_exit':lint.returncode,'structure_exit':structure.returncode,'platform_generation':'PENDING','human_follow_along':'PENDING'}
(OUT/'static-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));(OUT/'pages.json').write_text(json.dumps(pages,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2));print(lint.stdout)
sys.exit(bool(errors or lint.returncode or structure.returncode))
