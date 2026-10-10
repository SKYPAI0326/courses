#!/usr/bin/env python3
"""Build accepted playground from canonical sources without adding a sixth core chapter."""
from pathlib import Path
from bs4 import BeautifulSoup
import html,json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]

def build(site,renderer):
    catalog=json.loads((site/'_source/playground/catalog.json').read_text());cases=catalog['cases']
    titles={r['path']:r['title'] for r in json.loads((ROOT/'_source/page-inventory.json').read_text())}
    used={c['page'] for c in cases}
    refs=[{'page':f,'title':titles[f],'group':key,'group_title':title} for key,title,desc,files in renderer.GROUPS for f in files if f not in used]
    catalog['references']=refs
    (site/'_source/playground/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2))
    (site/'playground').mkdir(exist_ok=True)
    records=[]
    shell=(site/'chapters/CH1.html').read_text()
    for c in cases:
        file=c['page'];source=site/c['source'];isnew=c['id'].startswith('PG')
        if isnew:
            doc=BeautifulSoup(shell,'html.parser');body=doc.select_one('.lesson-body');body.clear()
            fragment=BeautifulSoup(renderer.body_text(source),'html.parser')
            for node in list(fragment.contents):body.append(node)
            hero=doc.select_one('.lesson-hero');hero.select_one('h1').string=c['title'];hero.select_one('.lesson-tagline').string=c['goal']
            hero.select_one('.outcomes').clear();hero.select_one('.outcomes').append(BeautifulSoup('<div class="outcomes-label">完成物</div><div class="outcome-item">可重用工具、A／B測試與資料／結果檔。</div>','html.parser'))
        else:doc=BeautifulSoup((site/file).read_text(),'html.parser')
        hero=doc.select_one('.lesson-hero');hero.select_one('.hero-part').string='案例遊樂園 · '+c['category'];hero.select_one('.hero-num').string=c['id']+' · 選用案例';hero['data-learning-role']='playground'
        doc.select_one('.topbar-tag').string='案例遊樂園'
        doc.select_one('.back-link')['href']='../playground/index.html'
        doc.select_one('.footer-note').string='Gemini AI 實戰課 · 案例遊樂園 · '+c['title']
        n=doc.select_one('.lesson-nav');n.clear();n.extend(list(renderer.nav('../playground/index.html','../playground/index.html','選另一個工具案例','回案例遊樂園').contents))
        for label in n.select('.nav-btn-label'):label.string='返回案例遊樂園'
        renderer.meta(doc,file,c['title'],c['goal']);doc.html['data-built-at']='2026-10-08'
        renderer.fidelity(source,doc);serialized=renderer.serialize(doc);renderer.fidelity(source,BeautifulSoup(serialized,'html.parser'))
        (site/file).write_text(serialized)
        records.append({'source':c['source'],'page':file,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'html_sha256':hashlib.sha256((site/file).read_bytes()).hexdigest(),'fidelity':'PASS'})
    # Keep the course index's shell, gate, typography and progress script.
    index=BeautifulSoup((site/'index.html').read_text(),'html.parser');supp=index.select_one('#supplements');supp.clear()
    supp.append(BeautifulSoup(f'<h2>延伸參考：方法、保存與部署</h2><p>以下{len(refs)}份參考教材協助比較需求、改造介面、保存及分享；需要製作工作工具時，從案例遊樂園選案例。</p>','html.parser'))
    for key,title,desc,files in renderer.GROUPS:
        group=[r for r in refs if r['group']==key]
        if not group:continue
        links=''.join(f'<li><a href="{r["page"]}">{html.escape(r["title"])}</a></li>' for r in group)
        supp.append(BeautifulSoup(f'<section id="supplement-{key}"><h3>{title}</h3><ul class="supplement-list">{links}</ul></section>','html.parser'))
    entry=BeautifulSoup('<section id="playground-entry"><h2>案例遊樂園：將五章的方法用到不同工作</h2><p>完成核心之後，依工作需求選案例；每例有背景、完整示範、可重用提示詞、獨立案例資料及核對方法。先挑一種與排班不同的處理方式，再用另一組資料測試。</p><p><a href="playground/index.html">進入29個工具案例</a> · 資料整理、計算規則、需求文字、圖表呈現、工作協作。</p><p>遊樂園是獨立選用區，不增加核心章節，也不要求按案例編號依序完成。</p></section>','html.parser')
    supp.insert_before(entry)
    hero=index.select_one('.hero')
    for tag in hero.select('p'):tag.string='五章完成需求、生成、查核、修改與交付；再到案例遊樂園，用同一套方法製作不同工作工具。'
    for stat,number,label in zip(hero.select('.stat'),['5','29',str(len(refs))],['核心章節','工具案例','延伸參考']):stat.select_one('.stat-num').string=number;stat.select_one('.stat-lbl').string=label
    renderer.meta(index,'index.html','用白話設計、修改與交付工作工具',f'五章核心、29個工具案例與{len(refs)}份延伸參考；提示詞描述可重用結構，案例資料分開附加。')
    sty=index.new_tag('style');sty.string='#playground-entry{margin:48px 0;padding:28px 0;border-top:1px solid var(--c-border);border-bottom:1px solid var(--c-border)}#playground-entry p{line-height:1.9;margin:16px 0}#playground-entry a{color:var(--c-text);text-decoration:underline}';index.head.append(sty)
    (site/'index.html').write_text(renderer.serialize(index))
    build_landing(site,renderer,cases,index)
    # Apply the canonical course entry last; keep the playground's own shell.
    import importlib.util
    entry_spec=importlib.util.spec_from_file_location('course_entry',ROOT/'_tools/build-course-entry.py');entry=importlib.util.module_from_spec(entry_spec);entry_spec.loader.exec_module(entry);entry.build(site,renderer)
    # Complete prompt/case package includes original core materials for cross-links.
    zippath=site/'assets/playground/playground-materials.zip'
    with zipfile.ZipFile(zippath,'w',zipfile.ZIP_DEFLATED) as z:
        for folder in [site/'assets/playground',site/'assets/materials']:
            for p in sorted(folder.rglob('*')):
                if p.is_file() and p.suffix!='.zip':z.write(p,p.relative_to(site))
        z.writestr('README.txt','依案例代碼找到prompt.txt與cases.txt；提示詞描述工具結構，案例資料另附。新PG案例含作者參考工具。材料是測試資料，非學員通過證據。\n')
    (site/'_repair/2026-10-08/playground-build').mkdir(parents=True,exist_ok=True)
    (site/'_repair/2026-10-08/playground-build/fidelity.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    print(f'遊樂園29例、獨立入口、{len(refs)}份延伸參考、素材包已轉製')


def build_landing(site,renderer,cases,index):
    """Generate only the card-based playground entry; lesson sources and assets are untouched."""
    existing=site/'playground/index.html'
    reuse_shell=existing.exists()
    pg=BeautifulSoup(existing.read_text() if reuse_shell else renderer.serialize(index),'html.parser');main=pg.select_one('main');main.clear()
    for st in pg.select('#playground-card-layout'):st.decompose()
    categories=list(dict.fromkeys(c['category'] for c in cases))
    groups={group:'case-group-'+str(i+1) for i,group in enumerate(categories)}
    summaries={'需求與文字':'提示詞、通知與報告','計算與規則':'金額、門檻與日期','圖表與呈現':'圖表、配色與流程','工作與協作':'專案、人員與排程','資料整理':'清理、排序與分類'}
    intro="""<section id="choose-case"><h2>先選一個工作問題，再選工具的處理方式</h2><p>當你已能寫需求、產生完整HTML、核對結果並保存交付包，就可以換一種工作試試。從下方分類進入，再選一個與工作需求相近的案例。</p><p>第一次先選入門案例，讀背景與示範，再複製結構提示詞。案例資料另外提供；產生空白工具後才填資料，用A／B及例外核對，最後依第五章保存。作者參考品用來理解畫面反應，自己的生成成果仍需實測。</p><p><a href="../index.html#core-course">回五章核心</a> · <a href="../index.html#supplements">延伸參考</a> · <a href="../assets/playground/playground-materials.zip" download>下載29例提示詞與案例素材包</a></p><nav class="category-grid" aria-label="按工作用途選案例">"""
    for i,group in enumerate(categories):
        count=sum(c['category']==group for c in cases)
        intro+=f'<a class="category-link category-{i+1}" href="#{groups[group]}"><span class="category-label">{group}</span><span class="category-summary">{summaries[group]}</span><span class="category-count">{count} 個案例 <span aria-hidden="true">↓</span></span></a>'
    intro+='</nav></section>';main.append(BeautifulSoup(intro,'html.parser'))
    for i,group in enumerate(categories):
        members=[c for c in cases if c['category']==group]
        block=BeautifulSoup(f'<section class="case-group category-{i+1}" id="{groups[group]}" data-group="{group}" aria-labelledby="{groups[group]}-title"><div class="case-group-heading"><h2 id="{groups[group]}-title">{group}</h2><span>{len(members)} 個案例</span><a href="#choose-case" class="back-to-categories">回分類 <span aria-hidden="true">↑</span></a></div><ul class="case-list"></ul></section>','html.parser')
        for c in members:
            href='../'+c['page'];block.ul.append(BeautifulSoup(f'<li data-case="{c["id"]}" data-category="{group}" data-level="{c["difficulty"]}"><a class="case-link" href="{href}"><div class="case-link-top"><span class="case-level">{c["difficulty"]}</span><span class="case-start">第{c["after_chapter"]}章後</span><span class="case-arrow" aria-hidden="true">↗</span></div><h3>{html.escape(c["title"])}</h3><p class="case-goal">{html.escape(c["goal"])}</p><span class="case-open">查看示範與提示詞 <span aria-hidden="true">→</span></span></a></li>','html.parser'))
        main.append(block)
    for sc in pg.select('script'):
        if 'core-progress-count' in sc.get_text():sc.decompose()
    pg.select_one('.hero h1').string='案例遊樂園'
    for p in pg.select('.hero p'):p.string='把白話需求做成可重用工具，體驗不同工作中的資料整理、計算、呈現與協作。'
    for a in pg.select('.hero a[href]'):a['href']='#choose-case'
    if not reuse_shell:
        for a in pg.select('a[href]'):
            if a['href'].startswith('../../'):a['href']='../'+a['href']
        for a in pg.select('.topbar a[href]'):
            if a.get('href')=='index.html':a['href']='../index.html'
    renderer.meta(pg,'playground/index.html','案例遊樂園','29個可重用工作工具案例，完整提示詞、兩組案例資料、例外與核對方法。')
    style=pg.new_tag('style');style['id']='playground-card-layout';style.string='.category-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin:28px 0 8px}.category-link{display:flex;flex-direction:column;gap:10px;padding:20px 16px;border:1px solid var(--c-border);border-top-width:3px;border-radius:var(--radius);background:var(--c-card);color:var(--c-text);text-decoration:none;min-width:0}.category-label{font-size:1.05rem;font-weight:600;line-height:1.5}.category-summary{font-size:.82rem;line-height:1.65;color:var(--c-muted)}.category-count{font-size:.78rem;margin-top:auto}.category-count>span{float:right}.category-1.category-link{border-top-color:var(--c-a1)}.category-2.category-link{border-top-color:var(--c-a2)}.category-3.category-link{border-top-color:var(--c-a3)}.category-4.category-link{border-top-color:var(--c-a4)}.category-5.category-link{border-top-color:var(--c-a5)}.case-group{margin:56px 0;scroll-margin-top:80px}.case-group-heading{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin:0 0 18px}.case-group-heading h2{margin:0}.case-group-heading>span{font-size:.85rem;color:var(--c-muted)}.back-to-categories{margin-left:auto;color:var(--c-muted);font-size:.82rem;text-decoration:underline;text-underline-offset:4px}.case-list{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;padding:0;list-style:none}.case-list li{min-width:0}.case-link{display:flex;flex-direction:column;height:100%;padding:24px;border:1px solid var(--c-border);border-radius:var(--radius);background:var(--c-card);color:var(--c-text);text-decoration:none;min-width:0}.case-link-top{display:flex;gap:10px;align-items:center;font-size:.78rem;line-height:1.5;margin-bottom:18px;color:var(--c-muted)}.case-level{padding:3px 8px;border:1px solid var(--c-border);border-radius:var(--radius-sm);color:var(--c-text)}.case-arrow{margin-left:auto;font-size:1.2rem;color:var(--c-main)}.case-link h3{font-size:1.12rem;line-height:1.55;font-weight:600;margin:0 0 12px}.case-link .case-goal{font-size:.94rem;line-height:1.75;margin:0 0 24px}.case-open{margin-top:auto;padding-top:16px;border-top:1px solid var(--c-border);font-size:.82rem;color:var(--c-main)}.case-open>span{float:right}.case-link:hover,.category-link:hover{border-color:var(--c-main);background:var(--c-bg)}.case-link:focus-visible,.category-link:focus-visible,.back-to-categories:focus-visible{outline:3px solid var(--c-main);outline-offset:4px}#choose-case{scroll-margin-top:80px}#choose-case>p{line-height:1.9;margin:12px 0}#choose-case>p a{color:var(--c-text);text-decoration:underline;text-underline-offset:4px}@media(max-width:900px){.category-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:600px){.category-grid,.case-list{grid-template-columns:minmax(0,1fr)}.category-link{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px 12px;padding:18px 20px}.category-label{grid-column:1}.category-summary{grid-column:1}.category-count{grid-column:2;grid-row:1/3;align-self:center;margin:0}.category-count>span{float:none;margin-left:10px}.case-link{padding:22px}.case-group{margin:40px 0}}';pg.head.append(style)
    (site/'playground/index.html').write_text(renderer.serialize(pg))

if __name__=='__main__':
    import argparse,importlib.util
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--landing-only',action='store_true',required=True);parser.parse_args()
    spec=importlib.util.spec_from_file_location('course_renderer',ROOT/'_tools/render-five-chapters.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
    cases=json.loads((ROOT/'_source/playground/catalog.json').read_text())['cases']
    build_landing(ROOT,renderer,cases,BeautifulSoup((ROOT/'index.html').read_text(),'html.parser'))
    print('僅更新遊樂園入口：5分類方塊、29案例卡片。')
