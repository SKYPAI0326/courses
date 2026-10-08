#!/usr/bin/env python3
"""Source/DOM/runtime verification only; this does not claim browser layout validation."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,hashlib,subprocess,tempfile,shutil,importlib.util
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'_repair/2026-10-08/course-entry'
node='/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
source=json.loads((ROOT/'_source/course-entry.json').read_text());s=BeautifulSoup((ROOT/'index.html').read_text(),'html.parser');catalog=json.loads((ROOT/'_source/playground/catalog.json').read_text())
assert s.select_one('.entry-start')['href']=='chapters/CH1.html'
assert [x['href'] for x in s.select('.chapter-link')]==[c['href'] for c in source['chapters']]
assert [x.get_text(' ',strip=True) for x in s.select('.chapter-link h3')]==[c['title'] for c in source['chapters']]
assert [x.get_text(' ',strip=True) for x in s.select('.chapter-link p')]==[c['goal'] for c in source['chapters']]
assert s.select_one('#playground-entry')['href']=='playground/index.html'
assert not s.select('[data-core-complete],#core-progress-count,.body-text,.lesson-section,.hero-stats')
assert not s.select_one('#supplements').has_attr('open')
assert [(x['href'],x.get_text(' ',strip=True)) for x in s.select('.supplement-list a')]==[(r['page'],r['title']) for r in catalog['references']]
assert all(s.find(id='supplement-'+r['group']) for r in catalog['references'])
before=BeautifulSoup((OUT/'before/index.html').read_text(),'html.parser')
assert s.select_one('head style').get_text()==before.select_one('head style').get_text(),'Base design stylesheet changed'
for selector in ['#_gate','#_gs','.topbar','.footer']:
 assert str(s.select_one(selector))==str(before.select_one(selector)),selector
assert any('gemini_auth' in x.get_text() for x in s.select('script'))
# Exercise only the isolated reference-navigation function, without opening a browser/page.
script=s.select_one('#entry-reference-navigation').get_text()
vmtest=r"""const vm=require('vm'),assert=require('assert');const code=JSON.parse(require('fs').readFileSync(0,'utf8'));let handler,seen=[];const panel={open:false,contains:x=>x.reference===true,scrollIntoView:o=>seen.push('panel')};const target={reference:true,scrollIntoView:o=>seen.push('target')};const env={location:{hash:''},document:{getElementById:id=>id==='supplements'?panel:id==='supplement-sharing'?target:id==='core-course'?{}:null},window:{addEventListener:(name,fn)=>{assert.equal(name,'hashchange');handler=fn}},requestAnimationFrame:fn=>fn(),decodeURIComponent};vm.runInNewContext(code,env);assert.equal(panel.open,false);env.location.hash='#supplement-sharing';handler();assert.equal(panel.open,true);assert.deepEqual(seen,['target']);panel.open=false;env.location.hash='#core-course';handler();assert.equal(panel.open,false);env.location.hash='#supplements';handler();assert.equal(panel.open,true);panel.open=false;env.location.hash='#%FF';handler();assert.equal(panel.open,false);env.location.hash='#supplement-sharing';vm.runInNewContext(code,env);assert.equal(panel.open,true);console.log('PASS reference hash changes, direct bookmark and malformed hash')"""
subprocess.run([node,'-e',vmtest],input=json.dumps(script),text=True,check=True)
for modname,filename in [('renderer','render-five-chapters.py'),('entry','build-course-entry.py'),('pg','build-playground.py')]:
 spec=importlib.util.spec_from_file_location(modname,ROOT/'_tools'/filename);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);globals()[modname]=mod
with tempfile.TemporaryDirectory() as tmp:
 site=Path(tmp)
 for f in ['index.html','playground/index.html','_source/course-entry.json','_source/playground/catalog.json']:
  p=site/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/f,p)
 entry.build(site,renderer);assert (site/'index.html').read_bytes()==(ROOT/'index.html').read_bytes()
 pg.build_landing(site,renderer,catalog['cases'],s)
 oldpg=BeautifulSoup((ROOT/'playground/index.html').read_text(),'html.parser');newpg=BeautifulSoup((site/'playground/index.html').read_text(),'html.parser')
 assert oldpg.select_one('main').get_text(' ',strip=True)==newpg.select_one('main').get_text(' ',strip=True)
 assert [(a.get('href'),a.get_text(' ',strip=True)) for a in oldpg.select('a')]==[(a.get('href'),a.get_text(' ',strip=True)) for a in newpg.select('a')]
 assert [st.get_text() for st in oldpg.select('style')]==[st.get_text() for st in newpg.select('style')]
 assert str(oldpg.select_one('.hero'))==str(newpg.select_one('.hero'))
 # Full-build hook is part of the generation path, after the playground has its own shell.
 code=(ROOT/'_tools/build-playground.py').read_text();assert code.index('build_landing(site,renderer,cases,index)')<code.index('entry.build(site,renderer)')
prior=json.loads((OUT/'before/_validation/L5-evidence-manifest.json').read_text());changed=[r['path'] for r in prior['pages'] if hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()!=r['html_sha256']];assert changed==['index.html'],changed
result={'source_and_links':'PASS','reference_anchor_runtime':'PASS (isolated Node VM, no browser)','reproducible_entry_build':'PASS','playground_rebuild_content_links_styles':'PASS','changed_public_pages':changed,'other_48_page_hashes':'unchanged','gate_topbar_footer':'unchanged','old_browser_evidence':'superseded for homepage','browser_layout':'PENDING: file URL inspection blocked by browser security policy'}
(OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
