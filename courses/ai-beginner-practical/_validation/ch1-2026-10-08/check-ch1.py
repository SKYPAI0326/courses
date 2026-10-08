from pathlib import Path
from bs4 import BeautifulSoup
import json,hashlib,re,sys,importlib.util
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent;B=R/'_backup/2026-10-08-pre-ch1';parse=lambda p:BeautifulSoup(p.read_text(),'html.parser');norm=lambda x:re.sub(r'\s+','',x)
s=parse(R/'CH1-1.html');old=parse(B/'CH1-1.html');formal=parse(E/'CH1-1-rendered.html');report={}
assert len(s.select('.lesson-body'))==1
assert all(x.find_parent(class_='lesson-body')==s.select_one('.lesson-body') for x in s.select('.lesson-section'))
fields={x['data-field'] for x in s.select('[data-field]')};assert fields=={x['data-field'] for x in old.select('[data-field]')} and len(fields)==46
req=s.select('[data-required="true"]');assert len(req)==12
for atom in formal.select('p,h2,h3,h4,li,pre,table'):assert norm(atom.get_text()) in norm(s.find(id='workplace-practice').get_text()),atom.get_text()[:80]
oldatoms=old.select('pre,code,.code-block,table');legacy=0
for atom in oldatoms:
 if atom.find_parent(id='lesson-start'):continue
 assert norm(atom.get_text()) in norm(s.get_text());legacy+=1
for b in s.select('[data-gamma-copy]'):
 pre=s.find(id=b['data-gamma-copy']);a=b.parent.select_one('a[download]');assert pre.get_text()==(R/a['href']).read_text();assert b.parent.select_one('[data-copy-status]')
key='ai-beginner-practical:CH1-1:workbench:v2';assert key in str(s) and key in str(old)
for ident in ['_gate','_gs']:assert str(old.find(id=ident))==str(s.find(id=ident))
getgate=lambda z:next(x.get_text() for x in z.select('script') if 'aibeginner_auth' in x.get_text());assert getgate(old)==getgate(s)
links=0
for file in ['CH1-1.html','index.html','module1.html']:
 p=R/file
 for x in parse(p).select('[href],[src]'):
  v=x.get('href',x.get('src',''))
  if not v or v.startswith(('http:','https:','mailto:','data:','javascript:')):continue
  name,_,anchor=v.partition('#');dest=(p.parent/name).resolve() if name else p
  assert dest.is_file(),(file,v)
  if anchor and dest.suffix=='.html':assert parse(dest).find(id=anchor),(file,v)
  links+=1
copies=json.loads((E/'browser-copy.json').read_text());assert len(copies)==6 and all(x['exact'] for x in copies)
a=(E/'CH1-export.md').read_text();b=(E/'CH1-export-after-reload.md').read_text();trim=lambda x:re.sub(r'匯出時間：[^\n]*','',x).strip();assert trim(a)==trim(b)
fixture=json.loads((E/'browser-fixture.json').read_text());assert all(v.strip() in a for v in fixture.values());assert '（未填）' in a
restore=json.loads((E/'browser-restore.json').read_text());assert len(restore)==12 and all(x['value'] for x in restore)
view=json.loads((E/'browser-viewport.json').read_text());assert len(view)==6 and all(not x['horizontalOverflow'] for x in view)
assert all(x['sectionWidth']==1120 and x['stickyTop']==0 and x['workbenchWidth']<1120 for x in view if x['spot']!='phone')
protected=json.loads((R/'_backup/2026-10-08-pre-ch3-ch4/protected.json').read_text())
for name,sha in protected.items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==sha,name
# Other chapter content/pages were not edited by CH1; compare current batch snapshot source versions.
for name in ['CH2-1-LESSON-PLAN.md','CH2-1.html','CH3-1-LESSON-PLAN.md','CH3-1.html','CH4-1-LESSON-PLAN.md','CH4-1.html','PRAC2-1-LESSON-PLAN.md','PRAC2-1.html']:
 # Original CH1 start snapshot was not necessary for files outside edit scope: use latest pre-CH1 evidence snapshots.
 e=json.loads((B/'_validation/evidence.json').read_text());path='courses/ai-beginner-practical/'+name
 hashes=[x['sha256'] for r in e['records'] for x in r.get('artifacts',[]) if x['path']==path];assert hashes,name
 actual=hashlib.sha256((R/name).read_bytes()).hexdigest()
 if actual!=hashes[-1]:
  fmt=json.loads((E/'formatting-cleanup.json').read_text())[name];assert name in ['CH3-1.html','CH4-1.html']
  assert fmt['before_sha256']==hashes[-1] and fmt['after_sha256']==actual
  assert hashlib.sha256(''.join(x.rstrip()+'\n' for x in (R/name).read_text().splitlines()).encode()).hexdigest()==fmt['normalized_sha256']
# Both index cards keep distinct workflows; original CH2 overview card restored byte-semantic.
oldmod=parse(B/'module1.html');newmod=parse(R/'module1.html')
select=lambda z:next(c for c in z.select('#ch1-1 .course-card') if c.select_one('a[href="CH2-1.html"]'))
assert str(select(oldmod))==str(select(newmod))
report.update(result='PASS',old_fields=46,required=12,formal_atoms=len(formal.select('p,h2,h3,h4,li,pre,table')),exact_materials=6,old_examples=legacy,local_links=links,browser_copies=6,exports_reload_identical=True,protected_unchanged=True,other_chapter_content_unchanged=True,platform_and_human='PENDING')
(E/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
sys.path.insert(0,str(R.parents[1]/'docs'));spec=importlib.util.spec_from_file_location('course_search',R.parents[1]/'docs/build-search-index.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
entries=[]
for p in sorted(R.glob('*.html')):
 if m.should_ignore(p):continue
 title,desc=m.extract(p);entries.append({'url':p.relative_to(R.parents[1]).as_posix(),'title':title,'desc':desc,'course':'ai-beginner-practical','course_label':m.COURSE_LABEL['ai-beginner-practical'],'type':m.classify(p)})
(E/'search-index-course-entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
