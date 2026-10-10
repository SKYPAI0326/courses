from pathlib import Path
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from urllib.parse import unquote,urlsplit
import json,subprocess,re,hashlib,collections
site=Path(__file__).resolve().parents[4];b=site/'courses/gen-ai-36h';out=b/'_repair/2026-10-11';meta=json.loads((b/'_repair/2026-10-09/lesson-meta.json').read_text());md=MarkdownIt('commonmark',{'html':True}).enable('table');norm=lambda s:re.sub(r'\s+','',s);results={};logs=[]
ids=list(meta)
for i in range(0,len(ids),3):
 batch=ids[i:i+3]
 r=subprocess.run(['python3',str(b/'_tools/render-lessons.py'),*batch,'--evidence-output',str(out/f'render-{i//3+1:02}.json')],capture_output=True,text=True);assert r.returncode==0,r.stdout+r.stderr
 for u in batch:
  p=b/meta[u]['path'];doc=BeautifulSoup(p.read_text(),'html.parser');body=doc.select_one('.lesson-body');old=BeautifulSoup((b/'_backup/2026-10-11-pre-repair/files'/meta[u]['path']).read_text(),'html.parser')
  src=b/f'_repair/2026-10-09/lesson-plans/{u}.md';text=src.read_text().split('<!-- learner-content:start -->')[1].split('<!-- learner-content:end -->')[0];atoms=BeautifulSoup(md.render(text),'html.parser').select('h2,p,pre,table,li');missing=[a.get_text()[:100] for a in atoms if norm(a.get_text()) not in norm(body.get_text())];assert not missing,(u,missing)
  auth=lambda dom:[s.get_text() for s in dom.select('script') if 'gen36_auth' in s.get_text()]
  nav=lambda dom:[a.get('href') for a in dom.select('a.nav-btn')]
  assert auth(doc)==auth(old) and nav(doc)==nav(old),u
  for a in body.select('a[href^="../assets/"]'):assert a.get('target')=='_blank' and 'noopener' in a.get('rel',[]),(u,str(a))
  for a in doc.select('[href],[src]'):
   url=a.get('href',a.get('src'));parts=urlsplit(url)
   if not parts.scheme and parts.path:assert (p.parent/unquote(parts.path)).exists(),(u,url)
  for cmd in [['python3','docs/lint-page.py',str(p.relative_to(site)),'--summary'],['python3','/Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py',str(p)]]:
   r=subprocess.run(cmd,cwd=site,capture_output=True,text=True);logs.append(' '.join(cmd)+'\n'+r.stdout+r.stderr);assert r.returncode==0,(u,r.stdout,r.stderr)
  results[u]={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'page_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_atoms':len(atoms),'missing':0,'nav_auth':'unchanged','asset_links':'new tab, existing targets','structure':'PASS','lint':'no blockers','browser':'pending'}
(out/'static-checks.log').write_text('\n'.join(logs));(out/'fidelity.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
# Check all asset guide/portal links and IDs.
for p in (b/'assets').rglob('*.html'):
 doc=BeautifulSoup(p.read_text(),'html.parser');allids=[n['id'] for n in doc.select('[id]')];assert len(allids)==len(set(allids)),p
 for a in doc.select('a[href],script[src],link[href]'):
  value=a.get('href',a.get('src'));parts=urlsplit(value)
  if not parts.scheme and parts.path:assert (p.parent/unquote(parts.path)).exists(),(p,value)
# Cross-page duplicate paragraphs: review, do not conflate with model performance.
paras=collections.defaultdict(list)
for u,m in meta.items():
 doc=BeautifulSoup((b/m['path']).read_text(),'html.parser')
 for p in doc.select('.lesson-body p'):
  t=p.get_text(' ',strip=True)
  if len(t)>45:paras[t].append(u)
shared={t:us for t,us in paras.items() if len(set(us))>2}
(out/'shared-copy.json').write_text(json.dumps(shared,ensure_ascii=False,indent=2)+'\n')
print('PASS 28 pages: atom fidelity, local links, new tabs, nav/auth, lint and structure. Shared paragraphs >2 pages:',len(shared))
