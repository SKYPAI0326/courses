from pathlib import Path
from bs4 import BeautifulSoup
import json
ns={};exec(Path('_tools/repair-2026-10-11-plain-language.py').read_text().split('phase=sys.argv')[0].replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = Path.cwd()'),ns)
changes={'原示範（選做）':'課後示範','原練習（選做）':'課後練習','原問答（選做）':'課後問答','選做轉移':'課後換讀者'}
log=[]
for name in ['CH2-1.html','CH3-1.html','CH4-1.html']:
 p=Path(name);data=p.read_text();s=BeautifulSoup(data,'html.parser');spans=ns['Spans'](data);edits=[]
 for n in s.select('.lesson-quicknav a'):
  old=n.get_text(' ',strip=True)
  if old in changes:
   a,b=spans.spans[(n.sourceline,n.sourcepos)];raw=data[a:b];new=raw[:raw.index('>')+1]+changes[old]+raw[raw.rfind('</'):];edits.append((a,b,new));log.append({'file':name,'before':old,'after':changes[old],'href':n['href']})
 for a,b,new in reversed(edits):data=data[:a]+new+data[b:]
 p.write_text(data)
 out=Path('_repair/2026-10-11-plain-language');(out/(name+'.after.txt')).write_text(BeautifulSoup(data,'html.parser').get_text(' ',strip=True))
Path('_repair/2026-10-11-plain-language/navigation-edits.json').write_text(json.dumps(log,ensure_ascii=False,indent=2));print(len(log),'navigation labels clarified')
