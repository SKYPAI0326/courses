from pathlib import Path
from html import escape
import json
root=Path(__file__).resolve().parents[1];meta=json.loads((root/'_repair/2026-10-09/lesson-meta.json').read_text());scope={'__file__':str(root/'_tools/render-lessons.py')};exec((root/'_tools/render-lessons.py').read_text().split('a=argparse.ArgumentParser();')[0],scope);Anchors=scope['Anchors']
for p in [root/'index.html',*root.glob('part*/*.html')]:
 text=p.read_text();parser=Anchors(text);edits=[]
 for n in parser.nodes:
  cls=n['attrs'].get('class','').split()
  if 'prac-title' in cls or 'nav-btn-title' in cls:
   a=n['parent']
   while a and 'href' not in a['attrs']:a=a['parent']
   if a:
    unit=Path(a['attrs']['href']).stem
    if unit in meta:edits.append((n['inner'],n['close'],escape(meta[unit]['title'])))
  if 'prac-badge' in cls:edits.append((n['inner'],n['close'],'獨立練習'))
  if n['tag']=='script' and not n['attrs'].get('src') and 'function copyLink()' in text[n['inner']:n['close']]:edits.append((n['start'],n['end'],''))
  if n['tag']=='footer' and 'data-platform-version' in n['attrs']:
   attrs=n['attrs'].copy();attrs['data-platform-version']='2026-10-content-repair';attrs['data-built-at']='2026-10-09';edits.append((n['start'],n['inner'],'<footer '+' '.join(f'{k}="{escape(v,quote=True)}"' for k,v in attrs.items())+'>'))
 for start,end,new in sorted(edits,reverse=True):text=text[:start]+new+text[end:]
 p.write_text(text)
for p in (root/'_repair/2026-10-09/lesson-plans').glob('*.md'):
 s=p.read_text();s=s.replace('course_type: 操作型','course_type: skill-operation').replace('course_type: 條件變化練習','course_type: skill-operation').replace('course_type: 整合練習','course_type: integration-capstone');p.write_text(s)
print('Synced practice/navigation labels and content revision metadata; removed template share script')
