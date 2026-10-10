from pathlib import Path
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from urllib.parse import urlsplit,unquote
import json,re,subprocess,hashlib,csv
R=Path(__file__).resolve().parents[4];B=R/'courses/gen-ai-36h';O=B/'_repair/2026-10-11-followthrough';md=MarkdownIt('commonmark',{'html':True}).enable('table');norm=lambda s:re.sub(r'\s+','',s);meta=json.loads((B/'_repair/2026-10-09/lesson-meta.json').read_text());changed=['CH2-3','CH5-1','CH5-2','CH5-4'];logs=[];results={}
for uid,m in meta.items():
 p=B/m['path'];doc=BeautifulSoup(p.read_text(),'html.parser');body=doc.select_one('.lesson-body');src=B/f'_repair/2026-10-09/lesson-plans/{uid}.md'
 assert src.read_bytes()==(R/f'_lessons/gen-ai-36h/{uid}.md').read_bytes()
 atoms=BeautifulSoup(md.render(src.read_text().split('<!-- learner-content:start -->')[1].split('<!-- learner-content:end -->')[0]),'html.parser').select('h2,p,pre,table,li')
 assert all(norm(a.get_text()) in norm(body.get_text()) for a in atoms),uid
 for a in body.select('a[href^="../assets/"]'):assert a.get('target')=='_blank' and 'noopener' in a.get('rel',[])
 if uid in changed:
  old=BeautifulSoup((B/'_backup/2026-10-11-followthrough-pre-repair/files'/m['path']).read_text(),'html.parser')
  assert [s.get_text() for s in doc.select('script') if 'gen36_auth' in s.get_text()]==[s.get_text() for s in old.select('script') if 'gen36_auth' in s.get_text()]
  assert [a.get('href') for a in doc.select('a.nav-btn')]==[a.get('href') for a in old.select('a.nav-btn')]
 for cmd in [['python3','docs/lint-page.py',str(p.relative_to(R)),'--summary'],['python3','/Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py',str(p)]]:
  r=subprocess.run(cmd,cwd=R,capture_output=True,text=True);logs.append(' '.join(cmd)+'\n'+r.stdout+r.stderr);assert r.returncode==0,(uid,r.stdout,r.stderr)
 results[uid]={'atoms':len(atoms),'fidelity':'PASS','lint':'PASS','structure':'PASS','changed':uid in changed}
# All lesson/asset local targets and fragments, not just counts.
paths=[B/m['path'] for m in meta.values()]+list((B/'assets').rglob('*.html'));linkcount=0
for p in paths:
 doc=BeautifulSoup(p.read_text(),'html.parser');ids=[x['id'] for x in doc.select('[id]')];assert len(ids)==len(set(ids)),p
 for a in doc.select('[href],[src]'):
  u=urlsplit(a.get('href',a.get('src')))
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  assert target.exists(),(p,str(a))
  if u.fragment and target.suffix=='.html':assert BeautifulSoup(target.read_text(),'html.parser').find(id=unquote(u.fragment)),(p,str(a))
  linkcount+=1
for name in ['part5-stage-handoff','part5-rebuild-guide','START-HERE']:
 doc=BeautifulSoup((B/f'assets/{name}.html').read_text(),'html.parser');source=BeautifulSoup(md.render((B/f'assets/{name}.md').read_text()),'html.parser')
 assert all(norm(a.get_text()) in norm(doc.article.get_text()) for a in source.select('h1,h2,h3,p,pre,table,li')),name
# Extract actual rendered operands, test valid fixtures and missing-field/invalid values.
doc=BeautifulSoup((B/'assets/part5-rebuild-guide.html').read_text(),'html.parser');rows=[x.select('td') for x in doc.select('table')[0].select('tr')[1:]];rules={c[0].get_text():[c[1].get_text(),c[2].get_text()] for c in rows};assert len(rules)==9
fields=list(rules);evaluate=lambda row:all((row.get(k,'')==v if op=='Text: Equal to' else re.search(v,row.get(k,'')) is not None) for k,(op,v) in rules.items())
cases=list(csv.DictReader((B/'assets/part5-test-inputs.csv').open()));tests=[]
for case in cases:
 expected=case['test_case'] not in ['T05a','T05b'];assert evaluate(case)==expected;tests.append([case['test_case'],expected])
for field in fields:
 case=cases[0].copy();case[field]='';assert not evaluate(case);tests.append(['empty '+field,False])
for field,value in [('category','INQUIRY'),('category','inquiry '),('category','inquiry|other'),('email','a@example'),('email','a b@example.com'),('email','no-at'),('review_status','待覆核')]:
 case=cases[0].copy();case[field]=value;assert not evaluate(case);tests.append([field+'='+value,False])
# Exact matches for Blueprint operators, route predicates and source-key expression; serialization checked separately.
bpfile=B/'assets/reference-make-blueprint.json';bp=json.loads(bpfile.read_text());flow=bp['flow'];assert [m['module'] for m in flow]==['google-sheets:watchRows','google-sheets:makeAPICall','builtin:BasicRouter']
conditions=flow[1]['filter']['conditions'];assert len(conditions)==1
for c in conditions[0]:
 field=fields[int(re.search(r'`(\d+)`',c['a']).group(1))]
 if field in ['category','review_status'] and c['b']=='.+':
  assert c['o']=='text:pattern';continue
 assert c['o']==('text:equal' if rules[field][0]=='Text: Equal to' else 'text:pattern')
 if field=='email':continue
 assert c['b']==rules[field][1] or (field in ['category','review_status'] and c['b']=='.+')
dedup=flow[2]['filter']['conditions'][0][0];assert dedup['o']=='array:notcontain' and dedup['a']=='{{flatten(4.body.values)}}';assert dedup['b'] in doc.get_text()
routevalues=[r['flow'][0]['filter']['conditions'][0][0]['b'] for r in flow[2]['routes']];assert set(routevalues)==set(['inquiry','complaint','partnership','other'])
old=subprocess.check_output(['git','show','HEAD:'+str(bpfile.relative_to(R))],cwd=R);assert old==bpfile.read_bytes()
emailraw=next(c['b'] for c in conditions[0] if c['a']=='{{1.`2`}}');emailui=rules['email'][1]
notes={'blueprint_unchanged':True,'non_email_conditions_and_dedup':'exact match, redundant non-empty category/status implied','email_ui':emailui,'email_blueprint_decoded_json':emailraw,'email_import_runtime':'NOT_RUN: JSON pattern has extra escaping; do not infer imported runtime equivalence from a Python regex test','platform':'NOT_RUN','ui_rule_tests':tests}
logs.append('PASS all 28 pages: fidelity/structure/lint; '+str(linkcount)+' local links/fragments; 3 guide atom fidelity; '+str(len(tests))+' UI rule cases; Blueprint non-email conditions/routes/key exact; email import escaping NOT_RUN.')
(O/'static-checks.log').write_text('\n'.join(logs));(O/'fidelity.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');(O/'make-rule-checks.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n');print(logs[-1])
