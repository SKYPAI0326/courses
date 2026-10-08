from pathlib import Path
from bs4 import BeautifulSoup,Tag,Comment
from html.parser import HTMLParser
import html,json,re,copy
root=Path.cwd()
def soup(x):return BeautifulSoup(x,'html.parser')

def fragment(x):return list(soup(x).contents)

def settext(e,t):e.clear();e.append(t)

def add(e,x):
 for n in fragment(x):e.append(n)

class Spans(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=False);self.text=text;self.nodes=[];self.stack=[];self.starts=[0]
  for l in text.splitlines(True):self.starts.append(self.starts[-1]+len(l))
  self.feed(text)
 def pos(self):
  l,c=self.getpos();return self.starts[l-1]+c
 def handle_starttag(self,t,a):
  n={'tag':t,'start':self.pos(),'end':None};self.nodes.append(n)
  if t in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:n['end']=self.pos()+len(self.get_starttag_text())
  else:self.stack.append(n)
 def handle_endtag(self,t):
  assert self.stack and self.stack[-1]['tag']==t,(t,self.stack[-1]['tag'] if self.stack else None)
  n=self.stack.pop();n['end']=self.text.index('>',self.pos())+1
 def handle_startendtag(self,t,a):
  self.nodes.append({'tag':t,'start':self.pos(),'end':self.pos()+len(self.get_starttag_text())})

def edit_existing(name,fn):
 p=root/name;text=p.read_text();s=soup(text);sp=Spans(text);tags=s.find_all(True);assert len(tags)==len(sp.nodes),(name,len(tags),len(sp.nodes))
 ranges={id(t):n for t,n in zip(tags,sp.nodes)}
 for t,n in zip(tags,sp.nodes):assert t.name==n['tag']
 changes=[]
 def replace(target,new):
  n=ranges[id(target)];changes.append((n['start'],n['end'],str(new)))
 fn(s,replace)
 changes.sort()
 for a,b in zip(changes,changes[1:]):assert a[1]<=b[0],(name,a[:2],b[:2])
 for a,b,v in reversed(changes):text=text[:a]+v+text[b:]
 p.write_text(text)
