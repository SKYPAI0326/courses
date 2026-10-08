"""Verify source fidelity, retained practice, links and actual browser export evidence."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,re,sys,importlib.util
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent;B=R/'_backup/2026-10-07-pre-gamma-integration'
parse=lambda p:BeautifulSoup(p.read_text(),'html.parser')
norm=lambda t:re.sub(r'\s+','',t.replace('\\n','\n'))
gamma=parse(R/'PRAC2-1.html');ch2=parse(R/'CH2-1.html');old=parse(B/'CH2-1.html')
# Compare every rendered formal-source atom, including exact prompts and complete tables.
assert hashlib.sha256((R/'PRAC2-1-LESSON-PLAN.md').read_bytes()).hexdigest()==(E/'render-source-sha256.txt').read_text().strip()
source=parse(E/'rendered-formal-source.txt');text=norm(gamma.select_one('.lesson-body').get_text())
atoms=source.select('p,h2,h3,pre,table');assert all(norm(x.get_text()) in text for x in atoms)
source_pre=[x.get_text().strip() for x in source.select('pre')]
page_pre=[x.get_text().strip() for x in gamma.select('pre')]
assert all(x in page_pre for x in source_pre)
for key,name in {'proposal-a':'case-a/proposal.md','proposal-b':'case-b/proposal.md','prompt-outline':'prompts/outline.txt','prompt-gamma-text':'prompts/gamma-text.txt','prompt-gamma-generate':'prompts/gamma-generate.txt','quick-check':'checks/quick-check.md'}.items():
 assert gamma.select_one('#'+key).get_text()==(R/'assets/workplace/gamma'/name).read_text()
# All old storage fields survive; only required status changes.
old_fields={x['data-field'] for x in old.select('[data-field]')};new_fields={x['data-field'] for x in ch2.select('[data-field]')}
assert old_fields==new_fields
assert ch2.select_one('[data-workbench-form]')['data-workbench-key']==old.select_one('[data-workbench-form]')['data-workbench-key']
req={x['data-field'] for x in ch2.select('[data-required="true"]')}
assert req=={'emailScenario','emailPrompt','emailFirst','emailCheck','emailRevision','messageScenario','messagePrompt','messageFirst','messageCheck','check1','check2','check3','check5'}
assert ch2.select_one('[data-workbench-form] [data-workbench-status]')
assert ch2.select_one('[data-workbench-form] [data-workbench-progress-label]')
for x in old.select('#lesson-demo pre'):
 assert norm(x.get_text()) in norm(ch2.select_one('#lesson-demo').get_text()),'Lost complete demonstration input/output'
old_steps=old.select('#lesson-demo .step-block')
for i in [6,7]:
 original=norm(old_steps[i].get_text());assert any(norm(d.get_text()).find(original)>=0 for d in ch2.select('#lesson-demo details'))
for selector in ['.scenario-grid','.steps-wrap','.completion-line']:
 assert norm(old.select_one('#lesson-practice').select_one(selector).get_text()) in norm(ch2.select_one('#lesson-practice details').get_text())
links=0
for name in ['PRAC2-1.html','CH2-1.html','index.html','module1.html']:
 p=R/name;s=parse(p)
 for e in s.select('[href],[src]'):
  v=e.get('href',e.get('src',''))
  if not v or v.startswith(('http:','https:','mailto:','data:','javascript:')):continue
  path,_,anchor=v.partition('#');dest=(p.parent/path).resolve() if path else p
  assert dest.exists(),(name,v)
  if anchor and dest.suffix=='.html':assert parse(dest).find(id=anchor),(name,v)
  links+=1
# Course gate exact script/css; no changed authentication credential.
def gate_script(s):return next(x.get_text() for x in s.select('script') if 'aibeginner_auth' in x.get_text())
assert gate_script(gamma)==gate_script(old)
for row in json.loads((R/'_validation/gamma-2026-10-07/preexisting-files.json').read_text()).items():
 name,digest=row;assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
copy=json.loads((E/'browser-copy.json').read_text());assert len(copy)==6 and all(x['exact'] for x in copy)
for name in ['browser-viewport.json','browser-ch2-viewport.json']:
 rows=json.loads((E/name).read_text());assert [x['width'] for x in rows]==[390,430];assert all(not x['horizontalOverflow'] for x in rows)
w=json.loads((E/'browser-workbench.json').read_text());export=(E/'workbench-export.md').read_text();after=(E/'workbench-export-after-reload.md').read_text()
assert all(v in export for v in w['fixture'].values())
trim=lambda x:re.sub(r'匯出時間：.*','',x).strip()
assert trim(export)==trim(after);assert '（13/13）' in w['progress']
assert '選做：三版自我介紹' in export and '（未填）' in export
report={'result':'PASS','scope':'source fidelity, retained practice, local links, exact copied materials, browser functional export and reload','formal_source_atoms':len(atoms),'exact_code_blocks':len(source_pre),'local_links':links,'old_fields_preserved':len(old_fields),'required_text_fields_and_checks':len(req),'exact_copies':6,'actual_export_reload_equal':True,'protected_user_files_unchanged':True,'human_follow_along':'PENDING'}
(E/'integration-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
# Scoped search entries from existing generator; root mixed worktree stays unchanged.
sys.path.insert(0,str(R.parents[1]/'docs'))
spec=importlib.util.spec_from_file_location('course_search',R.parents[1]/'docs/build-search-index.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
entries=[]
for p in sorted(R.glob('*.html')):
 if m.should_ignore(p):continue
 title,desc=m.extract(p);entries.append({'url':p.relative_to(R.parents[1]).as_posix(),'title':title,'desc':desc,'course':'ai-beginner-practical','course_label':m.COURSE_LABEL['ai-beginner-practical'],'type':m.classify(p)})
(E/'search-index-course-entries.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
assert any(x['url'].endswith('/PRAC2-1.html') for x in entries)
(E/'OPS.md').write_text('搜尋索引：本課'+str(len(entries))+'筆scoped entries已產生，未覆寫根search-index.json；發布時以course欄替換本課紀錄，保留其他專案變更。\nSitemap：新頁含相同#_gate，依既有build-sitemap規則排除，沒有新增公開URL。\n核心PDF已存在並驗證，但根.gitignore忽略*.pdf；將來提交／發布需精準納入兩份成品PDF，不修改全域忽略規則。\n')
