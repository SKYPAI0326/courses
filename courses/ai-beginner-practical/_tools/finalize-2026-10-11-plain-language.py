from pathlib import Path
from bs4 import BeautifulSoup
import json
root=Path.cwd()
ns={}
exec((root/'_tools/repair-2026-10-11-plain-language.py').read_text().split("phase=sys.argv")[0].replace("ROOT = Path(__file__).resolve().parents[1]","ROOT = Path.cwd()"),ns)
Page=ns['Page'];Spans=ns['Spans']
class Current(Page):
 def __init__(self,name):
  self.name=name;self.source=(root/name).read_text();self.soup=BeautifulSoup(self.source,'html.parser');self.body=self.soup.select_one('.lesson-body');self.spans=Spans(self.source);self.edits=[]
pages={}
for name in ['CH1-1.html','CH3-1.html','PRAC2-1.html']:
 p=Current(name)
 if name=='CH1-1.html':
  p.label('選做：五欄拆解與其他舊紀錄','課後選做：五欄拆解與生活練習')
  p.label('選做：原五題與錯誤表檢查','課後選做：五個生活對話與錯誤檢查')
 if name in ['CH1-1.html','CH3-1.html']:
  step=p.node('#'+('ch1' if name.startswith('CH1') else 'ch3')+'-step-1')
  wrapper=step.parent.find_previous_sibling()
  assert wrapper.name=='div' and wrapper.select_one('table')
  raw=p.raw(wrapper).replace('<table>','<table class="lesson-table">',1)
  p.replace(wrapper,raw+'<p class="table-scroll-note">手機可左右滑動表格，查看所選案例的其他欄位。</p>','新增案例表沿用既有樣式與手機提示')
 if name=='PRAC2-1.html':
  n=p.node('#gamma-source-1 .step-body p','選 A 報表改善')
  p.inner(n,'選 A 報表改善、B 文件交接，或自己的企劃。展開所選企劃，按「複製全文」，保留標題到 P10；自備企劃保留全文。','自備企劃不用P編號')
 data=p.render();after=BeautifulSoup(data,'html.parser')
 assert [a.get('href') for a in p.soup.select('a[href]')]==[a.get('href') for a in after.select('a[href]')]
 for sel in ['pre','script','style','[data-field]']:
  assert [str(n) for n in p.soup.select(sel)]==[str(n) for n in after.select(sel)]
 pages[name]=(p,data)
for name,(p,data) in pages.items():
 target=root/name.replace('.html','-LESSON-PLAN.md');source=target.read_text();start='<!-- learner-content:start -->';end='<!-- learner-content:end -->';a=source.index(start);b=source.index(end);title=source[a:b].splitlines()[1];body=BeautifulSoup(data,'html.parser').select_one('.lesson-body').decode_contents()
 target.write_text(source[:a]+start+'\n'+title+'\n\n'+body+'\n'+source[b:]);(root/name).write_text(data)
 out=root/'_repair/2026-10-11-plain-language'
 (out/(name+'.after.txt')).write_text(BeautifulSoup(data,'html.parser').get_text(' ',strip=True))
 (out/(name+'.follow-up-edits.json')).write_text(json.dumps([{'reason':why,'before':p.source[a:b],'after':new} for a,b,new,why in p.edits],ensure_ascii=False,indent=2))
 print(name,len(p.edits),'final refinements')
