#!/usr/bin/env python3
"""Build the course entry only, preserving lessons, materials, gate and bookmarked reference groups."""
from pathlib import Path
from bs4 import BeautifulSoup,NavigableString
import html,json,importlib.util
ROOT=Path(__file__).resolve().parents[1]
STYLE='''.hero-actions{display:flex;gap:12px;flex-wrap:wrap;margin:8px 0}.entry-start,.entry-outline{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:12px 20px;border:1px solid var(--c-border);border-radius:var(--radius);font-size:.92rem;line-height:1.6;text-decoration:none}.entry-start{background:var(--c-main);border-color:var(--c-main);color:var(--c-card)}.entry-outline{background:var(--c-card);color:var(--c-text)}.hero .hero-desc{max-width:40em}.course-entry h2{font-size:1.5rem;line-height:1.5;margin:0 0 14px}.course-entry p{font-size:.94rem;line-height:1.85}.entry-section-intro{max-width:46em;margin-bottom:24px}.chapter-grid{list-style:none;padding:0;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}.chapter-grid>li{min-width:0}.chapter-link{height:100%;display:flex;flex-direction:column;padding:24px;border:1px solid var(--c-border);border-radius:var(--radius);background:var(--c-card);color:var(--c-text);text-decoration:none}.chapter-label{font-size:.78rem;line-height:1.7;color:var(--c-main);margin-bottom:12px}.chapter-link h3{font-size:1.12rem;line-height:1.65;margin:0 0 12px}.chapter-link p{margin:0 0 20px}.chapter-open{font-size:.82rem;line-height:1.7;margin-top:auto;color:var(--c-main);padding-top:14px;border-top:1px solid var(--c-border)}.chapter-open>span{float:right}.chapter-link:hover,.entry-outline:hover,.resource-link:hover{border-color:var(--c-main)}.entry-start:hover{opacity:.9}.entry-resources{margin-top:44px}.resource-link{display:block;background:var(--c-card);color:var(--c-text);text-decoration:none;border:1px solid var(--c-border);border-radius:var(--radius);padding:28px}.resource-kicker{font-size:.78rem;line-height:1.7;color:var(--c-muted);display:block;margin-bottom:10px}.resource-link p{max-width:48em;margin:0 0 20px}.resource-action{display:block;font-size:.88rem;line-height:1.7;color:var(--c-main)}.resource-action>span{float:right}.entry-reference{margin-top:20px;border:1px solid var(--c-border);border-radius:var(--radius);background:var(--c-card)}.entry-reference>summary{padding:22px 28px;cursor:pointer;font-size:1rem;font-weight:600;line-height:1.7}.reference-caption{font-size:.85rem;font-weight:400;color:var(--c-muted);margin-left:12px}.reference-content{padding:0 28px 28px}.reference-content>p{margin:0 0 20px}.reference-group{margin-top:24px}.reference-group h3{font-size:1.02rem;line-height:1.6;margin:0 0 10px}.supplement-list{padding-left:22px;line-height:2}.supplement-list a,.entry-materials a{color:var(--c-text);text-decoration:underline;text-underline-offset:4px}.entry-materials{margin-top:24px;color:var(--c-muted)}.entry-start:focus-visible,.entry-outline:focus-visible,.chapter-link:focus-visible,.resource-link:focus-visible,summary:focus-visible,.supplement-list a:focus-visible{outline:3px solid var(--c-main);outline-offset:4px}.course-entry [id]{scroll-margin-top:80px}@media(max-width:600px){.chapter-grid{grid-template-columns:minmax(0,1fr)}.chapter-link{padding:22px}.hero-actions{flex-direction:column;align-items:stretch}.resource-link{padding:24px}.entry-reference>summary{padding:20px 24px}.reference-caption{display:block;margin-left:20px}.reference-content{padding:0 24px 24px}.course-entry h2{font-size:1.3rem}.entry-resources{margin-top:32px}}'''
DISCLOSURE="""(function(){const panel=document.getElementById('supplements');function revealReference(){let id;try{id=decodeURIComponent(location.hash.slice(1))}catch(e){return}const target=document.getElementById(id);if(target&&(target===panel||panel.contains(target))){panel.open=true;requestAnimationFrame(()=>target.scrollIntoView({block:'start'}))}}window.addEventListener('hashchange',revealReference);revealReference()})()"""

def build(site,renderer):
    source=json.loads((site/'_source/course-entry.json').read_text());catalog=json.loads((site/'_source/playground/catalog.json').read_text());doc=BeautifulSoup((site/'index.html').read_text(),'html.parser');hero=doc.select_one('.hero');main=doc.select_one('main');assert hero and main
    esc=html.escape
    reference_count=len(catalog['references'])
    hero.select_one('h1').string=source['title'];hero.select_one('.hero-desc').string=source['intro']
    for node in hero.select('.hero-stats,.hero-actions'):node.decompose()
    hero.append(BeautifulSoup('<nav class="hero-actions" aria-label="開始課程"><a class="entry-start" href="chapters/CH1.html">從第1章開始 <span aria-hidden="true"> →</span></a><a class="entry-outline" href="#core-course">查看五章內容</a></nav>','html.parser'))
    markup=f'<section id="core-course" aria-labelledby="core-title"><h2 id="core-title">依序完成五章</h2><p class="entry-section-intro">{esc(source["route_intro"])}</p><ol class="chapter-grid">'
    for c in source['chapters']:
        markup+=f'<li><a class="chapter-link" href="{esc(c["href"])}"><span class="chapter-label">第{c["chapter"]}章 · 核心課程</span><h3>{esc(c["title"])}</h3><p>{esc(c["goal"])}</p><span class="chapter-open">閱讀本章 <span aria-hidden="true">→</span></span></a></li>'
    markup+='</ol></section>'
    markup+=f'<section class="entry-resources" aria-labelledby="resources-title"><h2 id="resources-title">完成核心後，按工作需要選用</h2><a id="playground-entry" class="resource-link" href="playground/index.html"><span class="resource-kicker">選用 · 29個工具案例</span><h3>案例遊樂園</h3><p>{esc(source["playground_intro"])}</p><span class="resource-action">選一個工作案例 <span aria-hidden="true">→</span></span></a><details id="supplements" class="entry-reference"><summary>延伸參考 <span class="reference-caption">{reference_count}份教材 · 需要時展開</span></summary><div class="reference-content"><p>{esc(source["reference_intro"])}</p>'
    for key,title,desc,files in renderer.GROUPS:
        refs=[r for r in catalog['references'] if r['group']==key]
        if not refs:continue
        markup+=f'<section class="reference-group" id="supplement-{key}"><h3>{esc(title)}</h3><ul class="supplement-list">'
        markup+=''.join(f'<li><a href="{esc(r["page"])}">{esc(r["title"])}</a></li>' for r in refs);markup+='</ul></section>'
    markup+='</div></details><p class="entry-materials">跟做資料可在各章首次使用處取得，也可<a href="assets/materials/materials.zip" download>下載核心素材包</a>。</p></section>'
    main.clear();main['class']=['section','course-entry'];main.append(BeautifulSoup(markup,'html.parser'))
    for sc in doc.select('script'):
        if 'core-progress-count' in sc.get_text() or sc.get('id')=='entry-reference-navigation':sc.decompose()
    for st in doc.select('head style'):
        if st.get_text().startswith(('.core-route-list{','#playground-entry{')) or st.get('id')=='course-entry-layout':st.decompose()
    st=doc.new_tag('style',id='course-entry-layout');st.string=STYLE;doc.head.append(st)
    sc=doc.new_tag('script',id='entry-reference-navigation');sc.string=DISCLOSURE;doc.body.append(sc)
    renderer.meta(doc,'index.html',source['title'],f'五章核心依序學會用白話製作、修改與交付工作工具；另有29個工具案例與{reference_count}份選用參考。')
    for parent in [doc.head,doc.body,hero]:
        for node in list(parent.contents):
            if isinstance(node,NavigableString) and not node.strip():node.extract()
    (site/'index.html').write_text(renderer.serialize(doc))

if __name__=='__main__':
    spec=importlib.util.spec_from_file_location('course_renderer',ROOT/'_tools/render-five-chapters.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer);build(ROOT,renderer)
    print('僅更新課程入口：開始入口、五章卡片、遊樂園與折疊參考。')
