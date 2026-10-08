#!/usr/bin/env python3
"""Render already reviewed source bodies into the existing V4 course shell."""
from pathlib import Path
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
from bs4.dammit import EntitySubstitution
from copy import deepcopy
import importlib.util, json, hashlib, html, argparse
spec=importlib.util.spec_from_file_location('chapters',Path(__file__).with_name('build-five-chapters.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
SITE,BEFORE,OUT=m.SITE,m.BEFORE,m.OUT
theme_spec=importlib.util.spec_from_file_location('coldtone_styles',Path(__file__).with_name('coldtone_styles.py'));theme=importlib.util.module_from_spec(theme_spec);theme_spec.loader.exec_module(theme)

GROUPS=[
('prompt','提示詞設計與比較','第二章之後，整理需求、比較輸出及建立模板。',['part1/PRAC1-1.html','part1/PRAC1-2.html','part1/PRAC1-3.html']),
('forms','計算、排班與表單','第三章之後，將不同輸入與規則做成可查核工具。',['part2/BUDGET-1.html','part2/BUDGET-2.html','part2/CH2-2.html','part5/PRAC5-6.html','part5/PRAC5-7.html','part5/PRAC5-11.html']),
('visual','介面、圖表與資訊呈現','以工作判斷選呈現方式；修改後仍核對資料與原功能。',['part2/CH2-3.html','part2/PRAC2-3.html','part3/CH3-1.html','part3/CH3-2.html','part3/CH3-3.html','part3/PRAC3-1.html','part3/PRAC3-2.html','part3/PRAC3-3.html','part5/PRAC5-4.html','part5/PRAC5-8.html']),
('work','行政、行銷與會議工作','第三章之後按職務選案例；模型語意判斷另有平台需求。',['part5/PRAC5-1.html','part5/PRAC5-2.html','part5/PRAC5-3.html','part5/PRAC5-5.html','part5/PRAC5-9.html','part5/PRAC5-10.html','part5/PRAC5-12.html','part6/CH6-1.html','part6/PRAC6-1.html']),
('reuse','改造、保存與提示詞管理','第四、第五章之後，依成果類型擴充與重用。',['part4/CH4-2.html','part4/CH4-3.html','part4/PRAC4-2.html','part4/SUPP4-1.html','part4/SUPP4-3.html']),
('sharing','分享與外部部署參考','第五章之後，需要分享或部署時再核對環境與條件。',['part4/PRAC4-1.html','part6/CH6-2.html','part6/CH6-3.html'])]
GOALS=[
('用白話請AI做遊戲，存檔、開啟，再修改一次。','留下能重開的snake-v1、v2，說明配色前後的差異。'),
('從一份示例學會補齊需求，再寫自己的提示詞。','留下自己寫的工具需求；當次資料與核對答案分開。'),
('做出排班工具，換兩組資料並測錯誤輸入。','留下測過的schedule-v2、兩組備份、班表與測試紀錄。'),
('替排班工具加一項可調規則，重查新舊功能。','留下測過的schedule-v3；保留v2，記錄修改前後的測試。'),
('課堂整理排班交付包；課後再做資料清理工具。','課內：v3及A／B還原與使用說明。課後：CSV清理工具的兩組資料、結果與交付包。')]

class MetaOrder(HTMLFormatter):
    def attributes(self,tag):
        priority={'meta':['name','property'],'link':['rel']}.get(tag.name,[])
        return [(k,tag.attrs[k]) for k in priority if k in tag.attrs]+[(k,v) for k,v in tag.attrs.items() if k not in priority]
def serialize(doc):
    text=doc.decode(formatter=MetaOrder(entity_substitution=EntitySubstitution.substitute_xml))
    canonical=doc.select_one('link[rel=canonical]')
    prefix='/courses/gemini-ai/'
    if canonical and prefix in canonical.get('href',''):
        page=canonical['href'].split(prefix,1)[1].split('#',1)[0].split('?',1)[0]
        text=theme.apply_html(text,page,m.ROOT)
    return text

def body_text(path):
    text=path.read_text();return text.split('<!-- learner-content:start -->',1)[1].split('<!-- learner-content:end -->',1)[0].strip()
def nav(prev,next_,prev_title,next_title):
    return BeautifulSoup(f'''<a class="nav-btn nav-prev" data-nav-role="prev" href="{prev}"><div><div class="nav-btn-label">{('返回目錄' if 'index' in prev else '上一章')}</div><div class="nav-btn-title">{prev_title}</div></div></a><a class="nav-btn nav-next next" data-nav-role="next" href="{next_}"><div><div class="nav-btn-label">{('返回目錄' if 'index' in next_ else '下一章')}</div><div class="nav-btn-title">{next_title}</div></div></a>''','html.parser')
def meta(doc,file,title,desc):
    doc.title.string=title+'｜Gemini AI 實戰課'
    for sel in ['meta[name="description"]','meta[property="og:description"]','meta[name="twitter:description"]']:
        tag=doc.select_one(sel)
        if tag:tag['content']=desc
    for sel in ['meta[property="og:title"]','meta[name="twitter:title"]']:
        tag=doc.select_one(sel)
        if tag:tag['content']=title+'｜Gemini AI 實戰課'
    url='https://skypai0326.github.io/courses/courses/gemini-ai/'+file
    for tag in doc.select('link[rel="canonical"]'):tag['href']=url
    for tag in doc.select('meta[property="og:url"]'):tag['content']=url
def fidelity(source,doc):
    src=BeautifulSoup(body_text(source),'html.parser')
    expected=src.select_one('.lesson-body') or src
    assert expected.get_text(' ',strip=True)==doc.select_one('.lesson-body').get_text(' ',strip=True),source
    assert [(x.get('id'),x.get_text()) for x in src.select('pre')]==[(x.get('id'),x.get_text()) for x in doc.select('.lesson-body pre')],source
    assert [(x.get('id'),x.get_text()) for x in src.select('[data-policy-prompt]')]==[(x.get('id'),x.get_text()) for x in doc.select('.lesson-body [data-policy-prompt]')],source
    assert [(x.get('href'),x.get_text()) for x in src.select('a[href]')]==[(x.get('href'),x.get_text()) for x in doc.select('.lesson-body a[href]')],source

def main():
    review=m.ROOT/'_source/CONTENT-REVIEW.md'
    assert review.exists(),'先完成內容審閱紀錄'
    OUT.mkdir(parents=True,exist_ok=True)
    (SITE/'chapters').mkdir(exist_ok=True)
    records=[]
    for n,title in enumerate(m.TITLES,1):
        source=SITE/f'_source/chapters/CH{n}.md'
        doc=BeautifulSoup((BEFORE/m.OLD[0]).read_text(),'html.parser');body=doc.select_one('.lesson-body');body.clear()
        for node in list(BeautifulSoup(body_text(source),'html.parser').contents):body.append(node)
        hero=doc.select_one('.lesson-hero');hero.select_one('.hero-part').string='核心課程';hero.select_one('.hero-num').string=f'第 {n} 章'
        hero.select_one('h1').string=title;hero.select_one('.lesson-tagline').string=GOALS[n-1][0]
        outcomes=hero.select_one('.outcomes');outcomes.clear();outcomes.append(BeautifulSoup('<div class="outcomes-label">本章成果</div><div class="outcome-item">'+GOALS[n-1][1].replace('两组','兩組')+'</div>','html.parser'))
        top=doc.select_one('.topbar-tag')
        if top:top.string=f'第 {n} 章'
        footer=doc.select_one('.footer-note')
        if footer:footer.string=f'Gemini AI 實戰課 · 第 {n} 章／共 5 章'
        oldnav=doc.select_one('.lesson-nav');oldnav.clear();oldnav.extend(list(nav('../index.html' if n==1 else f'CH{n-1}.html','../index.html' if n==5 else f'CH{n+1}.html','Gemini AI 課程目錄' if n==1 else m.TITLES[n-2],'補充教材與成果回顧' if n==5 else m.TITLES[n]).contents))
        meta(doc,f'chapters/CH{n}.html',f'第{n}章 {title}',GOALS[n-1][0]);doc.html['data-built-at']='2026-10-08'
        fidelity(source,doc);page=SITE/f'chapters/CH{n}.html';page.write_text(serialize(doc))
        fidelity(source,BeautifulSoup(page.read_text(),'html.parser'))
        records.append({'source':str(source.relative_to(SITE)),'page':str(page.relative_to(SITE)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'fidelity':'PASS'})
    groups={file:(key,title) for key,title,desc,files in GROUPS for file in files}
    rows=json.loads((m.ROOT/'_source/page-inventory.json').read_text());titles={row['path']:row['title'] for row in rows}
    for file,(key,group) in groups.items():
        source=SITE/'_source/supplements'/(file.replace('/','-').removesuffix('.html')+'.md')
        doc=BeautifulSoup((BEFORE/file).read_text(),'html.parser');body=doc.select_one('.lesson-body');new=BeautifulSoup(body_text(source),'html.parser').select_one('.lesson-body');body.replace_with(new)
        hero=doc.select_one('.lesson-hero')
        if hero:
            for tag in hero.select('.hero-part'):tag.string='補充教材 · '+group
            for tag in hero.select('.hero-num'):tag.string='依用途選讀'
            hero['data-learning-role']='reference' if key=='sharing' else 'extension'
            if file=='part4/SUPP4-3.html':hero.select_one('h1').string=titles[file]
        for tag in doc.select('.topbar-tag'):tag.string='補充教材'
        footer=doc.select_one('.footer-note')
        if footer:footer.string='Gemini AI 實戰課 · 補充教材 · '+group
        # Each supplement returns to its own topic group; sequential case pairs stay inside supplements.
        n=doc.select_one('.lesson-nav');n.clear();n.extend(list(nav('../index.html#supplement-'+key,'../index.html#supplement-'+key,group,group).contents))
        for label in n.select('.nav-btn-label'):label.string='返回補充目錄'
        meta(doc,file,titles[file],doc.select_one('meta[name="description"]')['content']);doc.html['data-built-at']='2026-10-08'
        fidelity(source,doc);(SITE/file).write_text(serialize(doc));records.append({'source':str(source.relative_to(SITE)),'page':file,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'fidelity':'PASS'})
    index=BeautifulSoup((BEFORE/'index.html').read_text(),'html.parser');main=index.select_one('main');main.clear()
    markup='''<section id="core-course" class="core-route"><h2>五章核心：完成一個可重用的工作工具</h2><p class="body-text">先體驗生成與修改，再學會寫需求。第三至第五章持續完成同一個排班工具，從初版走到可交付版本。操作與練習都放在章內，請按順序閱讀。</p><p class="body-text">成果自檢 <span id="core-progress-count">0 / 5</span>。勾選前核對完成物；紀錄只保存在目前瀏覽器，不代表講師評分。</p><div class="core-progress-track"><div id="core-progress-fill"></div></div><ol class="core-route-list">'''
    for n,title in enumerate(m.TITLES,1):
        markup+=f'<li><a href="chapters/CH{n}.html"><strong>第{n}章 · {title}</strong></a><p class="body-text">{GOALS[n-1][0]}</p><label><input type="checkbox" data-core-complete="CH{n}"> {GOALS[n-1][1]}</label></li>'
    markup+='''</ol><p class="body-text">需要素材時，可<a href="assets/materials/materials.zip" download>下載素材包</a>，或在各章第一次使用的位置取得個別檔案。六小時為規劃時數，不含休息，尚待真人試教。</p></section><section id="supplements"><h2>按工作需求選用補充教材</h2><p class="body-text">核心完成後，依自己的用途選一份教材。先看先備與材料，再閱讀完整示例、操作和核對結果。補充教材各自返回本目錄，保留自己的閱讀與成果紀錄。</p>'''
    for key,title,desc,files in GROUPS:
        markup+=f'<section id="supplement-{key}"><h3>{title}</h3><p class="body-text">{desc}</p><ul class="supplement-list">'
        for file in files:markup+=f'<li><a href="{file}">{html.escape(titles[file])}</a></li>'
        markup+='</ul></section>'
    markup+='</section>';main.append(BeautifulSoup(markup,'html.parser'))
    hero=index.select_one('.hero')
    for tag in hero.select('h1'):tag.string='用白話設計、修改與交付工作工具'
    for tag in hero.select('p'):tag.string='從第一個生成體驗開始，逐章完成可重用的工作成果，再按需求選讀補充教材。'
    for a in hero.select('a[href]'):
        if a['href'].startswith(('#','part')):a['href']='#core-course'
    for stat,number,label in zip(hero.select('.stat'),['5','36','6h'],['核心章節','補充教材','規劃時數']):
        stat.select_one('.stat-num').string=number;stat.select_one('.stat-lbl').string=label
    meta(index,'index.html','用白話設計、修改與交付工作工具','五章核心依序建立生成、需求設計、工作工具、修改查核及保存交付能力，另有36份補充教材。')
    # Replace obsolete route counts in learner-visible closing copy.
    closing=index.select_one('.next-step')
    if closing:closing.decompose()
    for script in index.select('script'):
        if 'gemini-ai-core-evidence-v3' in script.get_text():script.string=script.get_text().replace('gemini-ai-core-evidence-v3','gemini-ai-five-chapters-v1')
    extra=index.new_tag('style');extra.string='.core-route-list{padding-left:24px}.core-route-list li{padding:20px 0;border-bottom:1px solid var(--c-border)}.core-route-list a,.supplement-list a{color:var(--c-text);text-decoration:underline;text-underline-offset:4px}.core-route-list label{display:block;font-size:.88rem;line-height:1.8}.core-route-list input{margin-right:8px}#supplements{margin-top:56px}#supplements>section{margin:32px 0}.supplement-list{padding-left:24px;line-height:2.1}.core-progress-track{height:3px;background:var(--c-border);margin:12px 0 24px}#core-progress-fill{height:100%;background:var(--c-text);width:0%}section[id]{scroll-margin-top:76px}';index.head.append(extra)
    (SITE/'index.html').write_text(serialize(index))
    # Old bookmarks become explicit aliases, not an eighth or ninth core station.
    for old,target in m.MAP.items():
        doc=BeautifulSoup((BEFORE/old).read_text(),'html.parser');redirect=doc.new_tag('script');redirect.string=f"location.replace('../{target}'+location.hash);";doc.head.insert(0,redirect)
        doc.select_one('.back-link')['href']='../'+target
        (SITE/old).write_text(serialize(doc))
    (SITE/'_source/lesson-map.json').write_text(json.dumps({f'chapters/CH{n}.html':{'title':title,'chapter':n,'role':'core','prev':'index.html' if n==1 else f'chapters/CH{n-1}.html','next':'index.html' if n==5 else f'chapters/CH{n+1}.html','source':f'_source/chapters/CH{n}.md'} for n,title in enumerate(m.TITLES,1)},ensure_ascii=False,indent=2))
    (OUT/'fidelity.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    if (SITE/'_source/playground/catalog.json').exists():
        pg_spec=importlib.util.spec_from_file_location('playground',Path(__file__).with_name('build-playground.py'));pg=importlib.util.module_from_spec(pg_spec);pg_spec.loader.exec_module(pg);pg.build(SITE,__import__(__name__))
    print('正式正文與HTML保真核對完成；47講義與2入口，7舊網址保留轉向。' if (SITE/'_source/playground/catalog.json').exists() else '5核心、36補充及首頁轉製完成；41份正文保真一致。')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site',type=Path,default=m.ROOT,help='課程目錄；預設從主目錄正式來源轉製')
    args=parser.parse_args()
    SITE=args.site.resolve()
    assert SITE==m.ROOT or SITE==m.SITE, '只允許本課主目錄或既有檢閱版'
    main()
