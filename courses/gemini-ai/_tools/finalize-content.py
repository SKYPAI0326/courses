from pathlib import Path
import json,zipfile
ROOT=Path(__file__).resolve().parents[1]
ns={'__file__':str(ROOT/'_tools/apply-repair.py')}
exec((ROOT/'_tools/apply-repair.py').read_text().split('for file in sorted(')[0],ns)
extra='<p class="body-text">預設改造需求：增加「餘額低於核定預算 10%」提醒，讓承辦人提早處理費用風險。先自行寫追加指令；此規則不在原基本版。核定 25,000 時，餘額 3,700 不提醒；再把講師實支改成 11,200，應為實支 23,000、差異 2,400、餘額 2,000，顯示低餘額提醒。原有超支、缺值與匯出功能須保留。</p>'
f=ROOT/'_source/fragments/part4-PRAC4-3.fragment'
for file,selector in [(f,'#core-1'),(ROOT/'part4/PRAC4-3.html','.lesson-body > #core-1')]:
    raw=file.read_text()
    if '預設改造需求：' not in raw:
        raw=ns['replace'](raw,selector,lambda old,node:old[:old.rfind('</section>')]+extra+old[old.rfind('</section>'):])
        file.write_text(raw)
a=ROOT/'assets/materials/reference-answers.json';d=json.loads(a.read_text())
d['solo_low_budget_alert']={'approved':25000,'threshold':2500,'initial_remaining':3700,'initial_alert':False,'changed_lecturer_actual':11200,'actual':23000,'difference':2400,'remaining':2000,'alert':True}
a.write_text(json.dumps(d,ensure_ascii=False,indent=2))
for file in [*sorted((ROOT/'_source/fragments').glob('*.fragment')),*sorted(ROOT.glob('part*/*.html'))]:
    raw=file.read_text();s=ns['BeautifulSoup'](raw,'html.parser')
    nodes=[n for n in s.select('a[target="_blank"][href]') if '../assets/tools/' in n['href'] and not n.find_parent(id='legacy-reference')]
    for node in nodes[::-1]:
        a,b=ns['span'](raw,node);download=f' · <a href="{node["href"]}" download>下載 HTML 參考檔</a>'
        if not raw[b:].startswith(download):raw=raw[:b]+download+raw[b:]
    file.write_text(raw)
for f in (ROOT/'_source/fragments').glob('*.fragment'):
    text=f.read_text()
    if '<!-- learner-content:start -->' not in text:
        f.write_text('<!-- learner-content:start -->\n'+text+'<!-- learner-content:end -->\n')
p=ROOT/'index.html';s=p.read_text();p.write_text('\n'.join(x.rstrip() for x in s.splitlines())+'\n')
M=ROOT/'assets/materials'
with zipfile.ZipFile(M/'materials.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(M.iterdir()):
        if p.suffix!='.zip':z.write(p,p.name)
print('補足独立需求變更、參考品實際下載與來源界線。'.replace('独','獨'))
