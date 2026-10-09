from pathlib import Path
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from urllib.parse import urlsplit,unquote
import json,csv,hashlib,re,subprocess
root=Path(__file__).resolve().parents[1];backup=root/'_backup/2026-10-09-pre-repair';meta=json.loads((root/'_repair/2026-10-09/lesson-meta.json').read_text());md=MarkdownIt('commonmark',{'html':True}).enable('table');results={};errors=[]
for unit,m in meta.items():
 p=root/m['path'];s=BeautifulSoup(p.read_text(),'html.parser');old=BeautifulSoup((backup/'site/courses/gen-ai-36h'/m['path']).read_text(),'html.parser');source=(root/'_repair/2026-10-09/lesson-plans'/(unit+'.md')).read_text();body=source.split('<!-- learner-content:start -->')[1].split('<!-- learner-content:end -->')[0].strip();original=BeautifulSoup(md.render(body),'html.parser')
 visible=lambda x:re.sub(r'\s+','',x.get_text())
 # Every source paragraph, table and code block is preserved; extra form is allowed.
 for n in original.select('p,pre,table,li'):
  if visible(n) not in visible(s.select_one('.lesson-body')):errors.append((unit,'fidelity',visible(n)[:50]))
 for attr in ['href','src']:
  for n in s.select(f'[{attr}]'):
   value=n[attr];parts=urlsplit(value)
   if not parts.scheme and parts.path:
    target=(p.parent/unquote(parts.path)).resolve()
    if not target.exists():errors.append((unit,'missing link',value))
 # Keep original auth gate script text; exclude old non-auth share/copy handlers.
 auth=lambda dom:[(n.string or '') for n in dom.select('script') if 'gen36_auth' in (n.string or '')]
 assert auth(s)==auth(old),(unit,'auth changed')
 links=lambda dom:[n.get('href') for n in dom.select('a.nav-btn')]
 assert links(s) and links(s)==links(old),(unit,'nav routes changed')
 results[unit]={'characters':len(visible(s.select_one('.lesson-body'))),'sections':len(s.select('.lesson-body .lesson-section')),'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'html_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fidelity':'all paragraphs/tables/code retained','auth':'original scripts identical','browser':'PENDING'}
index=BeautifulSoup((root/'index.html').read_text(),'html.parser');cards=index.select('.lesson-card,.prac-card');assert len(cards)==28
for n in cards:
 unit=Path(n['href']).stem;assert n.select_one('.lesson-title,.prac-title').get_text()==meta[unit]['title'],unit
rows=list(csv.DictReader((root/'assets/sales-24-months.csv').open()));assert len(rows)==24 and len(set(r['month'] for r in rows))==24
node='/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
for p in root.glob('assets/*.js'):
 subprocess.run([node,'--check',str(p)],check=True,capture_output=True)
assert not errors,errors
(root/'_repair/2026-10-09/fidelity-and-links.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('PASS: 28 source-to-HTML fidelity, local links, original auth/nav, index titles, 24 month fixture, JS syntax.')
