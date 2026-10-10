from pathlib import Path
from bs4 import BeautifulSoup
import json
ns={};exec(Path('_tools/repair-2026-10-11-plain-language.py').read_text().split('phase=sys.argv')[0].replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = Path.cwd()'),ns)
p=Path('CH2-1.html');data=p.read_text();s=BeautifulSoup(data,'html.parser');spans=ns['Spans'](data);edits=[];log=[]
for node in s.select('.lesson-body .callout-body'):
 t=node.get_text(' ',strip=True)
 if t.startswith(('停下來檢查：','下一個任務：')):
  wrapper=node.parent;assert wrapper.get('class')==['callout','tip'];assert not wrapper.select('a,pre,input,textarea,select,script,style');a,b=spans.spans[(wrapper.sourceline,wrapper.sourcepos)];edits.append((a,b));log.append({'before':data[a:b],'after':'','reason':'完成檢查與前往Gamma已在步驟8，移除緊接的同義提醒'})
assert len(edits)==2
for a,b in reversed(edits):data=data[:a]+data[b:]
p.write_text(data);plan=Path('CH2-1-LESSON-PLAN.md');source=plan.read_text();start='<!-- learner-content:start -->';end='<!-- learner-content:end -->';a=source.index(start);b=source.index(end);title=source[a:b].splitlines()[1];body=BeautifulSoup(data,'html.parser').select_one('.lesson-body').decode_contents();plan.write_text(source[:a]+start+'\n'+title+'\n\n'+body+'\n'+source[b:]);out=Path('_repair/2026-10-11-plain-language');(out/'CH2-1.html.after.txt').write_text(BeautifulSoup(data,'html.parser').get_text(' ',strip=True));(out/'CH2-1.html.callout-edits.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
