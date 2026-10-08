"""Protect exact raw <pre> payloads before Markdown rendering using parser spans."""
from html.parser import HTMLParser
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];E=Path(__file__).parent
class PreSpans(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=False);self.text=text;self.starts=[0];self.ranges=[];self.active=None
  for line in text.splitlines(True):self.starts.append(self.starts[-1]+len(line))
  self.feed(text);assert self.active is None
 def pos(self):
  l,c=self.getpos();return self.starts[l-1]+c
 def handle_starttag(self,tag,attrs):
  if tag=='pre':assert self.active is None;self.active=self.pos()
 def handle_endtag(self,tag):
  if tag=='pre':
   assert self.active is not None;self.ranges.append((self.active,self.text.index('>',self.pos())+1));self.active=None
for unit in ['CH3-1','CH4-1']:
 src=(R/(unit+'-LESSON-PLAN.md')).read_text().split('<!-- learner-content:start -->')[1].split('<!-- learner-content:end -->')[0]
 parser=PreSpans(src);payloads={}
 for i,(a,b) in enumerate(parser.ranges):payloads[str(i)]=src[a:b]
 for i,(a,b) in reversed(list(enumerate(parser.ranges))):src=src[:a]+f'<div data-raw-token="{i}"></div>'+src[b:]
 (E/(unit+'-render-input.md')).write_text(src);(E/(unit+'-raw-payloads.json')).write_text(json.dumps(payloads,ensure_ascii=False,indent=2)+'\n')
