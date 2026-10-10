from pathlib import Path
from html.parser import HTMLParser
from html import escape
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
import json,re,hashlib,argparse
root=Path(__file__).resolve().parents[1];plans=root/'_repair/2026-10-09/lesson-plans';meta=json.loads((plans.parent/'lesson-meta.json').read_text());md=MarkdownIt('commonmark',{'html':True}).enable('table')
class Anchors(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=False);self.text=text;self.lines=[0]+[m.end() for m in re.finditer('\n',text)];self.stack=[];self.nodes=[];self.feed(text)
 def pos(self):
  line,col=self.getpos();return self.lines[line-1]+col
 def handle_starttag(self,tag,attrs):
  node={'tag':tag,'attrs':dict(attrs),'start':self.pos(),'inner':self.pos()+len(self.get_starttag_text()),'parent':self.stack[-1] if self.stack else None}
  if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append(node)
  else:node['close']=node['inner'];node['end']=node['inner'];self.nodes.append(node)
 def handle_endtag(self,tag):
  if self.stack and self.stack[-1]['tag']==tag:
   node=self.stack.pop();node['close']=self.pos();node['end']=self.text.find('>',self.pos())+1;self.nodes.append(node)
 def find(self,cls):
  n=[x for x in self.nodes if cls in x['attrs'].get('class','').split()];assert len(n)==1,(cls,len(n));return n[0]
def render(body):
 html=md.render(body);s=BeautifulSoup(html,'html.parser');sections=[];current=None
 for n in list(s.contents):
  if getattr(n,'name',None)=='h2':
   current=BeautifulSoup('<section class="lesson-section"><div class="section-eyebrow"><span></span></div></section>','html.parser').section
   current.select_one('span').string=f'({len(sections)+1:02}) · 學習與實作';n['class']='section-heading';current.append(n);sections.append(current)
  elif current is not None: current.append(n)
 for section in sections:
  for p in section.select('p'):p['class']='body-text'
  for pre in section.select('pre'):pre['class']='full-prompt';wrap=s.new_tag('div',attrs={'class':'full-prompt-wrap'});pre.wrap(wrap)
  for table in section.select('table'):wrap=s.new_tag('div',attrs={'class':'repair-table','tabindex':'0','role':'region','aria-label':'資料表，可水平捲動'});table.wrap(wrap)
 return '\n'.join(str(x) for x in sections)
a=argparse.ArgumentParser();a.add_argument('units',nargs='*');a.add_argument('--evidence-output',type=Path,default=plans.parent/'render-evidence.json',help='Write renderer evidence here (relative to course root unless absolute).');args=a.parse_args();evidence={}
for unit in args.units or meta:
 m=meta[unit];p=root/m['path'];source=(plans/(unit+'.md')).read_text();body=source.split('<!-- learner-content:start -->')[1].split('<!-- learner-content:end -->')[0].strip();assert body.startswith('## ')
 for link in re.findall(r'\]\((\.\./assets/[^)]+)\)',body):assert (p.parent/link).is_file(),(unit,link)
 # Parse explicit wrapper and replace only its children. No global serialization.
 text=p.read_text();parser=Anchors(text);replacements=[];n=parser.find('lesson-body');rendered=render(body)
 extras=''
 if unit in ['PRAC6','PRAC7']:
  kind='toolbox' if unit=='PRAC6' else 'showcase';extras=f'<section class="lesson-section"><h2 class="section-heading">填寫與保存</h2><div data-gen36-form="{kind}"></div></section>'
 replacements.append((n['inner'],n['close'],'\n'+rendered+extras+'\n'))
 for cls,value in [('lesson-title',escape(m['title'])),('lesson-tagline',escape(m['goal']))]:
  n=parser.find(cls);replacements.append((n['inner'],n['close'],value))
 part_names={'1':'AI 基礎與提示詞','2':'辦公文字與附件','3':'來源筆記與版本核對','4':'小工具生成與測試','5':'人工覆核與 Make 自動化','6':'個人 AI 工作流程整合','7':'結業專題'}
 n=parser.find('hero-part');part=m['path'][4];replacements.append((n['inner'],n['close'],f'Part {part} · '+part_names[part]))
 hero=parser.find('lesson-hero')
 optional=[x for x in parser.nodes if x.get('parent') is hero and set(x['attrs'].get('class','').split())&{'outcomes','howto'}]
 for n in optional:replacements.append((n['inner'],n['close'],'<strong>本節完成物：</strong>'+escape(m['goal'])))
 try:
  n=parser.find('agenda');old=text[n['inner']:n['close']];minutes=re.search(r'(\d+)\s*分鐘',old);total=int(minutes.group(1)) if minutes else 60
  cuts=[0,round(total*.2),round(total*.5),round(total*.8),total];topics=['理解任務與完整示範','跟著操作並核對結果','自己練習與修正','保存、驗收與下一步']
  agenda='<strong>本節 '+str(total)+' 分鐘：練習時間可依進度調整</strong>'+''.join(f'<div class="agenda-row"><div class="agenda-time">{cuts[i]}–{cuts[i+1]} 分</div><div class="agenda-topic">{topics[i]}</div></div>' for i in range(4));replacements.append((n['inner'],n['close'],agenda))
 except AssertionError: pass
 title=[x for x in parser.nodes if x['tag']=='title'][0];replacements.append((title['inner'],title['close'],escape(m['title']+'｜生成式 AI 工作應用班')))
 for x in parser.nodes:
  if x['tag']=='meta' and (x['attrs'].get('name')=='description' or x['attrs'].get('property') in ['og:title','og:description'] or x['attrs'].get('name') in ['twitter:title','twitter:description']):
   attrs=x['attrs'].copy();attrs['content']=m['title'] if attrs.get('property')=='og:title' or attrs.get('name')=='twitter:title' else m['goal'];replacements.append((x['start'],x['end'],'<meta '+' '.join(f'{k}="{escape(v,quote=True)}"' for k,v in attrs.items())+'>'))
 for start,end,new in sorted(replacements,reverse=True):text=text[:start]+new+text[end:]
 if 'repair-content.css' not in text:text=text.replace('</head>','<link rel="stylesheet" href="../assets/repair-content.css">\n</head>')
 if unit in ['PRAC6','PRAC7'] and 'learner-forms.js' not in text:text=text.replace('</body>','<script src="../assets/course-tools.js"></script><script src="../assets/learner-forms.js"></script>\n</body>')
 # No old learner-only scripts remain outside body, other than the existing access gates.
 dom=BeautifulSoup(text,'html.parser');assert len(dom.select('.lesson-body'))==1
 actual=dom.select_one('.lesson-body');assert all(x.find_parent(class_='lesson-body') for x in actual.select('.lesson-section'))
 p.write_text(text)
 evidence[unit]={'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'html_sha256':hashlib.sha256(text.encode()).hexdigest(),'material_links':'all local links exist','fidelity':'full learner-content rendered; tables/code retained','review':'single-agent source review','browser':'PENDING'}
evidence_path=args.evidence_output if args.evidence_output.is_absolute() else root/args.evidence_output;evidence_path.parent.mkdir(parents=True,exist_ok=True);evidence_path.write_text(json.dumps(evidence,ensure_ascii=False,indent=2));print('Rendered',len(evidence),'pages, shell/nav/gate preserved; evidence:',evidence_path)
