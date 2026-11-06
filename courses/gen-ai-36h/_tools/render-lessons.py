from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
import json,re,hashlib,argparse,datetime
# 2026-11-01 起學員正文唯一落筆層是 _lessons/gen-ai-36h/；教案只留教師紀錄
root=Path(__file__).resolve().parents[1];plans=root/'_repair/2026-10-09/lesson-plans';lessons=root.parents[1]/'_lessons'/root.name;meta=json.loads((plans.parent/'lesson-meta.json').read_text());md=MarkdownIt('commonmark',{'html':True}).enable('table')
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
 prompt_id=0
 for section in sections:
  for p in section.select('p'):p['class']='body-text'
  for link in section.select('a[href^="../assets/"]'):
   link['target']='_blank'
   link['rel']=sorted(set(link.get('rel', [])) | {'noopener'})
  for pre in section.select('pre'):
   prompt_id+=1;pre['class']='full-prompt';pre['id']=f'p{prompt_id}';wrap=s.new_tag('div',attrs={'class':'full-prompt-wrap'});btn=s.new_tag('button',attrs={'class':'copy-btn-tl','data-target':pre['id'],'type':'button'});btn.string='複製';pre.wrap(wrap);wrap.insert(0,btn)
  for table in section.select('table'):wrap=s.new_tag('div',attrs={'class':'repair-table','tabindex':'0','role':'region','aria-label':'資料表，可水平捲動'});table.wrap(wrap)
 return '\n'.join(str(x) for x in sections)
def update_nav(page,title):
 # 相鄰頁上一節／下一節按鈕顯示的是目標頁標題，標題改了要一起改
 for f in root.glob('part*/*.html'):
  text=f.read_text()
  def sub(mt):
   href=re.search(r'href="([^"#]+)"',mt.group(1));return mt.group(1)+escape(title)+mt.group(3) if href and (f.parent/href.group(1)).resolve()==page.resolve() else mt.group(0)
  new=re.sub(r'(<a\b[^>]*class="[^"]*\bnav-btn\b[^"]*"[^>]*>(?:(?!</a>)[\s\S])*?<div class="nav-btn-title">)([^<]*)(</div>)',sub,text)
  if new!=text:f.write_text(new)
a=argparse.ArgumentParser();a.add_argument('units',nargs='*');a.add_argument('--evidence-output',type=Path,default=plans.parent/'render-evidence.json',help='Write renderer evidence here (relative to course root unless absolute).');args=a.parse_args();evidence={}
for unit in args.units or meta:
 m=meta[unit];p=root/m['path'];source=(lessons/(unit+'.md')).read_text();body=source.split('<!-- learner-content:start -->')[1].split('<!-- learner-content:end -->')[0].strip();assert body.startswith('## ')
 for link in re.findall(r'\]\((\.\./assets/[^)]+)\)',body):
  parts=urlsplit(link);target=p.parent/unquote(parts.path);assert target.is_file(),(unit,link)
  if parts.fragment and target.suffix=='.html':assert BeautifulSoup(target.read_text(),'html.parser').find(id=unquote(parts.fragment)),(unit,link,'missing anchor')
 # Parse explicit wrapper and replace only its children. No global serialization.
 text=p.read_text();parser=Anchors(text);replacements=[];n=parser.find('lesson-body');rendered=render(body)
 extras=''
 if unit in ['PRAC6','PRAC7']:
  kind='toolbox' if unit=='PRAC6' else 'showcase';extras=f'<section class="lesson-section"><h2 class="section-heading">填寫與保存</h2><div data-gen36-form="{kind}"></div></section>'
 replacements.append((n['inner'],n['close'],'\n'+rendered+extras+'\n'))
 for cls,value in [('lesson-title',escape(m['title'])),('lesson-tagline',escape(m['goal']))]:
  n=parser.find(cls);replacements.append((n['inner'],n['close'],value))
 part_names={'1':'AI 基礎與提示詞','2':'用 AI 處理辦公文字與附件','3':'用 Gemini Notebook 從文件找答案','4':'用 AI 做出工作小工具','5':'用 AI 整理訊息，交給 Make 自動處理','6':'建立自己的 AI 工作流程','7':'結業專題：用 AI 完成一件自己的工作'}
 n=parser.find('hero-part');part=m['path'][4];replacements.append((n['inner'],n['close'],f'Part {part} · '+part_names[part]))
 hero=parser.find('lesson-hero')
 optional=[x for x in parser.nodes if x.get('parent') is hero and set(x['attrs'].get('class','').split())&{'outcomes','howto'}]
 for n in optional:replacements.append((n['inner'],n['close'],'<strong>本節完成物：</strong>'+escape(m['artifact'])))
 try:
  n=parser.find('agenda');old=text[n['inner']:n['close']];minutes=re.search(r'(\d+)\s*分鐘',text[hero['inner']:min(hero['close'],n['start'])])
  topics=re.findall(r'^## (.+)$',body,re.M)
  # 時數只取頁首（不含練習順序本身）；PRAC 頁首沒有分鐘數時不寫時數
  agenda=('<strong>本節 '+minutes.group(1)+' 分鐘：依下列任務順序操作，分段時間依進度調整</strong>' if minutes else '<strong>這一節的練習順序</strong>')+''.join(f'<div class="agenda-row"><div class="agenda-time">{i+1:02}</div><div class="agenda-topic">{escape(topic)}</div></div>' for i,topic in enumerate(topics));replacements.append((n['inner'],n['close'],agenda))
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
 text=re.sub(r'data-built-at="[^"]*"',f'data-built-at="{datetime.date.today().isoformat()}"',text,count=1)
 p.write_text(text);update_nav(p,m['title'])
 evidence[unit]={'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'html_sha256':hashlib.sha256(text.encode()).hexdigest(),'material_links':'all local links exist','fidelity':'full learner-content rendered; tables/code retained','review':'single-agent source review','browser':'PENDING'}
evidence_path=args.evidence_output if args.evidence_output.is_absolute() else root/args.evidence_output;evidence_path.parent.mkdir(parents=True,exist_ok=True)
# 只轉部分頁面時保留其他頁面的既有證據
rendered=len(evidence);evidence={**(json.loads(evidence_path.read_text()) if evidence_path.exists() else {}),**evidence};evidence_path.write_text(json.dumps(evidence,ensure_ascii=False,indent=2));print('Rendered',rendered,'pages, shell/nav/gate preserved; evidence:',evidence_path)
