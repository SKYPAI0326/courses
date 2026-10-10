"""Source/link checks, not a substitute for a learner or platform trial."""
from pathlib import Path
from bs4 import BeautifulSoup
import json, hashlib, urllib.parse

root=Path(__file__).resolve().parents[1]
backup=root/'_backup/2026-10-11-pre-step-by-step'
out=root/'_validation/step-by-step-2026-10-11'
out.mkdir(parents=True,exist_ok=True)
pages=['index.html','module1.html','CH1-1.html','CH2-1.html','CH3-1.html','CH4-1.html','PRAC2-1.html','assets/templates/unit2-communication-scenarios.html']
report={};broken=[]
margin='\n.lesson-page .step-block[id],.lesson-page .lesson-section[id],.lesson-page .learner-workbench[id]{scroll-margin-top:144px;}\n'
gamma_margin='\n@media(max-width:760px){.lesson-page .step-block[id],.lesson-page .lesson-section[id],.lesson-page .learner-workbench[id]{scroll-margin-top:192px;}}\n'
gamma_steps='\n.lesson-page .step-block{padding:18px 0;border-bottom:1px solid var(--c-border);}.lesson-page .step-circle{display:none;}.lesson-page .step-heading{font-weight:700;line-height:1.6;margin-bottom:8px;}\n'
for name in pages:
    p=root/name;s=BeautifulSoup(p.read_text(),'html.parser');old=BeautifulSoup((backup/name).read_text(),'html.parser')
    for link in s.select('a[href]'):
        u=urllib.parse.urlsplit(link['href'])
        if u.scheme or (not u.path and not u.fragment):continue
        dest=(p.parent/urllib.parse.unquote(u.path)).resolve() if u.path else p
        if not dest.exists():broken.append([name,link['href']]);continue
        if u.fragment and dest.suffix=='.html':
            other=s if dest==p else BeautifulSoup(dest.read_text(),'html.parser')
            if not other.find(id=urllib.parse.unquote(u.fragment)):broken.append([name,link['href'],'anchor'])
    fields=lambda soup:[(e.get('id'),e.get('data-field'),e.get('data-required')) for e in soup.select('[data-field]')]
    assert fields(s)==fields(old),(name,'saved fields changed')
    assert [str(e) for e in old.select('script:not([src])')]==[str(e) for e in s.select('script:not([src])')],name
    old_scripts=[e['src'] for e in old.select('script[src]')]
    expected=old_scripts+(['assets/gamma-practice.js'] if name=='CH2-1.html' else [])
    assert sorted(e['src'] for e in s.select('script[src]'))==sorted(expected),name
    assert [str(e) for e in old.select('style')]==[str(e).replace(margin,'').replace(gamma_margin,'').replace(gamma_steps,'') for e in s.select('style')],name
    for el in s.select('[data-gamma-copy]'):assert s.find(id=el['data-gamma-copy']),(name,'copy target')
    for pre in old.select('pre[id]'):
        if pre.get('id') in ['ch2-email-prompt','ch2-message-prompt']:continue
        new=s.find(id=pre['id'])
        assert new is not None and new.get_text()==pre.get_text(),(name,pre['id'],'original material changed')
    lesson=root/name.replace('.html','-LESSON-PLAN.md')
    if lesson.exists():
        source=lesson.read_text().split('<!-- learner-content:start -->')[1].split('<!-- learner-content:end -->')[0]
        content=source[source.index('\n\n')+2:]
        assert BeautifulSoup(content,'html.parser').get_text(' ',strip=True)==s.select_one('.lesson-body').get_text(' ',strip=True),(name,'lesson fidelity')
    report[name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'savedFieldKeysUnchanged':True,'inlineScriptsUnchanged':True,'cssOnlyPlannedRulesChanged':True,'originalMaterialsPreserved':True,'lessonSynchronized':lesson.exists()}
for case in 'abc':
    source=(root/f'assets/workplace/tasks/case-{case}.txt').read_text().strip()
    ready=(root/f'assets/workplace/tasks/ready-{case}.txt').read_text()
    assert source in ready and '[貼上' not in ready
    s=BeautifulSoup((root/'CH1-1.html').read_text(),'html.parser')
    assert s.find(id='ready-'+case).get_text()==ready.strip()
s=BeautifulSoup((root/'CH2-1.html').read_text(),'html.parser')
for file,sid in [('email-client','ch2-ready-client'),('email-manager','ch2-ready-manager'),('message','ch2-ready-message')]:
    assert s.find(id=sid).get_text()==(root/f'assets/workplace/communication/{file}.txt').read_text().strip()
assert '工作台步驟 4、6、7' not in s.get_text()
assert '從步驟 8 重跑' not in s.get_text()
assert not broken,broken
(out/'source-checks.json').write_text(json.dumps({'kind':'author-self-check','pages':report,'brokenLocalLinks':broken,'readyPromptsHaveFullOriginal':True},ensure_ascii=False,indent=2))
print('8頁連結／錨點完整；原案例保留；5份教案正文保真；欄位鍵未變；6份新提示詞檔案與頁面一致。')
