"""Meaningful material, fidelity, storage, link and actual export checks for this batch."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,re,sys,importlib.util
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent;B=R/'_backup/2026-10-08-pre-ch3-ch4'
parse=lambda p:BeautifulSoup(p.read_text(),'html.parser')
norm=lambda t:re.sub(r'\s+','',t)
report={'checked_units':[],'local_links':0,'formal_atoms':0,'exact_materials':0,'old_fields_preserved':{},'required_fields':{},'legacy_code_and_tables_preserved':0,'human_and_platform':'PENDING'}
for u in ['CH3-1','CH4-1']:
 page=parse(R/(u+'.html'));old=parse(B/(u+'.html'));formal=parse(E/(u+'-rendered.html'));work=page.find(id='workplace-practice')
 body=page.select('.lesson-body');assert len(body)==1;assert all(s.find_parent(class_='lesson-body')==body[0] for s in page.select('.lesson-section'))
 for atom in formal.select('p,h2,h3,h4,li,pre,table'):
  assert norm(atom.get_text()) in norm(work.get_text()),(u,atom.get_text()[:80]);report['formal_atoms']+=1
 for pre in formal.select('pre'):assert pre.get_text() in [p.get_text() for p in work.select('pre')]
 # All original complete demonstration prompts and numerical tables survive as optional references.
 for atom in old.select('#lesson-demo pre,#lesson-demo table,#lesson-practice pre,#lesson-practice table'):
  t=atom.get_text().replace('共同素材','自選素材').replace('unit4-lifestyle-application-card.md','unit4-decision-card.md')
  assert norm(t) in norm(page.get_text()),(u,'lost legacy example',t[:70]);report['legacy_code_and_tables_preserved']+=1
 fields={x['data-field'] for x in page.select('[data-field]')};assert fields=={x['data-field'] for x in old.select('[data-field]')}
 form=page.select_one('[data-workbench-form]');assert form['data-workbench-key']==old.select_one('[data-workbench-form]')['data-workbench-key']
 assert form.select_one('[data-workbench-status]');assert form.select_one('[data-workbench-progress-label]')
 report['old_fields_preserved'][u]=len(fields);report['required_fields'][u]=len(form.select('[data-required="true"]'))
 for button in work.select('[data-gamma-copy]'):
  pre=work.find(id=button['data-gamma-copy']);d=button.find_parent('details');a=d.select_one('a[download]');assert a
  assert pre.get_text()==(R/a['href']).read_text(),(u,pre.get('id'),'payload changed')
  assert button.parent.select_one('[data-copy-status]');report['exact_materials']+=1
 # No changed gate script/style or gate UI markup.
 script=lambda s:next(x.get_text() for x in s.select('script') if 'aibeginner_auth' in x.get_text())
 assert script(page)==script(old)
 for ident in ['_gate','_gs']:assert str(page.find(id=ident))==str(old.find(id=ident))
 assert len(page.select('h1'))==1
 report['checked_units'].append(u)
for file in ['CH3-1.html','CH4-1.html','index.html','module1.html']:
 p=R/file;s=parse(p)
 for x in s.select('[href],[src]'):
  v=x.get('href',x.get('src',''))
  if not v or v.startswith(('http:','https:','mailto:','data:','javascript:')):continue
  name,_,anchor=v.partition('#');dest=(p.parent/name).resolve() if name else p
  assert dest.exists(),(file,v)
  if anchor and dest.suffix=='.html':assert parse(dest).find(id=anchor),(file,v)
  report['local_links']+=1
for name,sha in json.loads((B/'protected.json').read_text()).items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==sha,name
# Independent recomputation of case decision feasibility, by supplied variables not expected strings only.
a=json.loads((R/'assets/workplace/decisions/truth-map.json').read_text())
z=a['case-a']
for key in ['A','B']:
 row=z[key];assert row['sessions']*row['capacity']==z['people'];assert row['sessions']*(row['teaching']+row['setup'])==row['total_minutes']
assert z['A']['total_minutes']<=z['initial_limit_minutes'];assert z['A']['total_minutes']>z['changed_limit_minutes'];assert z['B']['total_minutes']<=z['changed_limit_minutes']
z=a['case-b'];assert all(z[k]['document_weekly']<=z['initial_doc_limit'] and z[k]['user_weekly']<=z['user_limit'] for k in ['A','B'])
assert z['A']['document_weekly']<=z['changed_doc_limit']<z['B']['document_weekly'];assert z['B']['validation_in_document_weekly']==10
# Cross-source truth map binds the decisive propositions to actual provided source paragraphs.
t=json.loads((R/'assets/workplace/documents/truth-map.json').read_text());assert t['case-a']['approved_capacity']==18 and t['case-a']['meeting_capacity']==20
D=R/'assets/workplace/documents'
for name,phrases in {'case-a/02-notice.txt':['18人','3個工作天','取代','只適用R教室'],'case-a/03-meeting.txt':['20人','沒有附新版核准公告','不得宣稱20人已核准'],'case-b/02-notice.txt':['1個工作天','未變更結案期限'],'case-b/03-meeting.txt':['首次回覆尚未寄出','回覆日期未提供','詢問期限']}.items():
 text=(D/name).read_text();assert all(p in text for p in phrases),(name,phrases)
# Browser exact copies and actual downloaded exports, not a generated substitute.
copies=json.loads((E/'browser-copy.json').read_text());assert len(copies)==18 and all(x['exact'] for x in copies)
fixtures=json.loads((E/'browser-fixtures.json').read_text());trim=lambda x:re.sub(r'匯出時間：[^\n]*','',x).strip()
for u in ['CH3','CH4']:
 a=(E/(u+'-export.md')).read_text();b=(E/(u+'-export-after-reload.md')).read_text();assert trim(a)==trim(b)
 assert all(v.strip() in a for v in fixtures[u+'-1'].values());assert '**姓名或代號**' in a
 assert '（未填）' in a,'Optional fields should not be compulsory'
 assert '**check1**' not in a,'Checkboxes must keep human readable export labels'
view=json.loads((E/'browser-viewport.json').read_text());assert len(view)==4 and all(not x['horizontalOverflow'] for x in view)
positions=json.loads((E/'browser-desktop-positions.json').read_text());assert len(positions)==8 and all(x['stickyTop']==0 and x['contentWidth']<=1120 for x in positions)
report.update(result='PASS',browser_exact_copies=len(copies),actual_export_reload_equal=True,protected_files_unchanged=True,decision_case_numeric_recompute=True)
(E/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
# Build only scoped course search records. Never overwrite the root mixed index.
sys.path.insert(0,str(R.parents[1]/'docs'))
spec=importlib.util.spec_from_file_location('course_search',R.parents[1]/'docs/build-search-index.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
entries=[]
for p in sorted(R.glob('*.html')):
 if m.should_ignore(p):continue
 title,desc=m.extract(p);entries.append({'url':p.relative_to(R.parents[1]).as_posix(),'title':title,'desc':desc,'course':'ai-beginner-practical','course_label':m.COURSE_LABEL['ai-beginner-practical'],'type':m.classify(p)})
(E/'search-index-course-entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
