from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,re
R=Path.cwd();E=R/'_validation/field-repairs-2026-10-08';B=R/'_backup/2026-10-08-pre-field-repairs';baseline=json.loads((B/'manifest.json').read_text());report={'pages':{},'protected':{}}
for f,sha in baseline['protected'].items():
 assert hashlib.sha256((R/f).read_bytes()).hexdigest()==sha,f;report['protected'][f]='unchanged'
for i in [1,3,4]:
 f=f'CH{i}-1.html';s=BeautifulSoup((R/f).read_text(),'html.parser');old=BeautifulSoup((B/f).read_text(),'html.parser');target=s.select_one('#workplace-practice');assert target.find_parent(class_='lesson-body') is s.select_one('.lesson-body')
 assert len(s.select('.lesson-body'))==1
 assert [dict(x.attrs) for x in s.select('[data-field]')]==baseline['pages'][f]['fields'],f+' fields'
 for css,v in baseline['pages'][f]['shell'].items():
  actual=str(s.select_one(css))
  if i==1 and css=='.page-hero':
   syntax=json.loads((E/'title-syntax-fix.json').read_text());v=v.replace(syntax['before'],syntax['after'])
  assert actual==v,(f,css)
 # Compare all non-content portions after masking the allowed changed subtree and two explicit acceptance paragraphs.
 for soup in [s,old]:
  if i==1:
   h=soup.select_one('h1.lesson-title');assert h.get_text(' ',strip=True)=='第一次用 LLM 完成工作任務';h.replace_with('__SAME_TITLE_WORDS__')
  soup.select_one('#workplace-practice').replace_with('__TARGET__')
  if i in [3,4]:soup.select_one('#lesson-check > p.body-text').replace_with('__ALLOWED_CHECK_COPY__')
 # Verify exact original bytes outside explicitly allowed parser-grounded spans; void br changes BeautifulSoup serialization state.
 ns={};exec((R/'_validation/ch3-ch4-2026-10-08/parser_edit.py').read_text(),ns)
 def masked_bytes(path):
  raw=path.read_text();tree=BeautifulSoup(raw,'html.parser');spans=ns['Spans'](raw);tags=tree.find_all(True);assert len(tags)==len(spans.nodes)
  ranges={id(x):y for x,y in zip(tags,spans.nodes)}
  targets=[tree.select_one('#workplace-practice')]
  if i==1:targets.append(tree.select_one('h1.lesson-title'))
  if i in [3,4]:targets.append(tree.select_one('#lesson-check > p.body-text'))
  for x in sorted(targets,key=lambda x:ranges[id(x)]['start'],reverse=True):
   span=ranges[id(x)];raw=raw[:span['start']]+'__ALLOWED_'+x.name+'__'+raw[span['end']:]
  return raw
 assert masked_bytes(R/f)==masked_bytes(B/f),f+' unexpected outside-target byte edits' 
 s=BeautifulSoup((R/f).read_text(),'html.parser');target=s.select_one('#workplace-practice')
 src=(R/f'CH{i}-1-LESSON-PLAN.md').read_text().split('<!-- learner-content:start -->')[1].split('<!-- learner-content:end -->')[0]
 formal=BeautifulSoup((E/f'CH{i}-1-rendered.html').read_text(),'html.parser')
 def atom(x):return re.sub(r'\s+','',x.get_text())
 a=[atom(x) for x in formal.select('p,h2,h3,h4,li,pre,table')];p=[atom(x) for x in target.select('p,h2,h3,h4,li,pre,table')];assert a==p,(f,'atoms differ')
 materials=[]
 for details in target.select('details'):
  link=details.select_one('a[download]');pre=details.select_one('pre');btn=details.select_one('[data-gamma-copy]')
  if not(link and pre and btn):continue
  path=R/link['href'];assert path.is_file(),str(path)
  assert pre.get_text().rstrip()==path.read_text().rstrip(),(f,link['href'],'payload')
  assert btn['data-gamma-copy']==pre['id'];assert btn.parent.select_one('[data-copy-status]') is not None
  materials.append({'id':pre['id'],'path':link['href'],'button':btn.get_text()})
 links=[]
 for x in s.select('[href],[src]'):
  v=x.get('href',x.get('src',''))
  if not v or v.startswith(('http','mailto:','tel:','data:','javascript:','//')):continue
  path,_,anchor=v.partition('#');dest=R/path if path else R/f
  assert dest.exists(),(f,v)
  if anchor and (not path or dest.suffix=='.html'):assert BeautifulSoup(dest.read_text(),'html.parser').find(id=anchor),(f,v)
  links.append(v)
 ids=[x['id'] for x in s.select('[id]')];assert len(ids)==len(set(ids)),f+' duplicate id'
 # Historical lesson appendix remains byte identical.
 lesson=f'CH{i}-1-LESSON-PLAN.md';marker='<!-- learner-content:end -->'
 assert (R/lesson).read_text().split(marker,1)[1]==(B/lesson).read_text().split(marker,1)[1]
 report['pages'][f]={'atoms':len(a),'exact_payloads':materials,'fields':len(s.select('[data-field]')),'required':len(s.select('[data-required=true]')),'links':len(links),'shell_and_optional_content':'unchanged'}
report['calculations']={'A_original':[2*(90+30),3*(60+15)],'A_changed_over_margin':[240-228,228-225],'B_changed_doc_A_B':[20<=25,30<=25],'B_user_A_B':[25<=30,15<=30],'B_four_week':[20*4,25*4,30*4,15*4]}
report['result']='PASS';report['human_and_new_platform_prompts']='PENDING'
(E/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({f:{k:v for k,v in x.items() if k!='exact_payloads'} for f,x in report['pages'].items()},ensure_ascii=False,indent=2));print('PASS; exact payloads:',sum(len(x['exact_payloads']) for x in report['pages'].values()))
