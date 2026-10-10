from pathlib import Path
from playwright.sync_api import sync_playwright
import json
B=Path(__file__).resolve().parents[2];O=B/'_repair/2026-10-11-followthrough';shots=O/'screenshots';shots.mkdir(exist_ok=True);base='http://127.0.0.1:9877/courses/gen-ai-36h/';rels=['part2/CH2-3.html','part5/CH5-1.html','part5/CH5-2.html','part5/CH5-4.html','assets/part5-rebuild-guide.html','assets/part5-stage-handoff.html','assets/START-HERE.html'];results=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True);context=browser.new_context(viewport={'width':1440,'height':1000});context.add_init_script("sessionStorage.setItem('gen36_auth','1');");page=context.new_page()
 for width in [1440,390,430]:
  page.set_viewport_size({'width':width,'height':1000})
  for rel in rels:
   page.goto(base+rel,wait_until='load');page.evaluate('localStorage.clear()');page.reload(wait_until='load');page.wait_for_timeout(100)
   dimensions=page.evaluate('({width:innerWidth,scrollWidth:document.documentElement.scrollWidth})');assert dimensions['scrollWidth']<=width+1,(rel,width,dimensions);results.append({'page':rel,'width':width,**dimensions})
   if rel in ['part5/CH5-2.html','assets/part5-rebuild-guide.html','assets/part5-stage-handoff.html'] and width in [1440,390]:
    page.screenshot(path=str(shots/f'{Path(rel).stem}-{width}-top.png'))
    if rel=='part5/CH5-2.html' and width==1440:
     for ratio,name in [(0.3,'modified'),(0.6,'middle'),(1,'bottom')]:
      page.evaluate('(r)=>scrollTo({top:(document.documentElement.scrollHeight-innerHeight)*r,behavior:"instant"})',ratio);page.screenshot(path=str(shots/f'CH5-2-1440-{name}.png'))
    if rel=='assets/part5-rebuild-guide.html':
     page.locator('#review-filter').scroll_into_view_if_needed();page.screenshot(path=str(shots/f'filter-{width}.png'))
     table=page.locator('table').first;pattern=table.locator('tr').nth(3).locator('td').nth(2).inner_text();assert pattern==r'^[^@\s]+@[^@\s]+\.[^@\s]+$',repr(pattern)
     assert table.locator('tr').nth(6).locator('td').nth(2).inner_text()=='^(inquiry|complaint|partnership|other)$'
     if width==390:
      wrapper=table.locator('..');assert wrapper.evaluate('(el)=>el.scrollWidth>el.clientWidth');wrapper.evaluate('(el)=>el.scrollLeft=el.scrollWidth');assert wrapper.evaluate('(el)=>el.scrollLeft>0');page.screenshot(path=str(shots/'filter-390-scrolled.png'))
 page.set_viewport_size({'width':1440,'height':1000});page.goto(base+'part5/CH5-2.html')
 for anchor in ['s1-to-s2','review-filter']:
  with context.expect_page() as pop:page.locator('.lesson-body a[href$="#'+anchor+'"]').click()
  popup=pop.value;popup.wait_for_load_state('load');assert popup.url.endswith('#'+anchor);assert popup.locator('#'+anchor).count()==1;assert popup.evaluate('scrollY')>0;assert page.url.endswith('CH5-2.html');popup.close()
 nav=page.locator('a.nav-btn').last;destination=nav.get_attribute('href');nav.click();assert destination.split('/')[-1] in page.url
 page.goto(base+'part5/CH5-2.html');page.evaluate('scrollTo({top:1400,behavior:"instant"})');page.wait_for_function("localStorage.getItem('progress:'+location.pathname)==='1400'");page.reload(wait_until='load');page.wait_for_function('Math.abs(scrollY-1400)<10');browser.close()
(O/'browser-results.json').write_text(json.dumps({'actor':'tool-run','engine':'Chromium headless','viewport_checks':results,'functional':['two deep links open new tabs at expected anchors; original stays on lesson','course navigation same tab','persisted scroll restore','regex displayed exactly, mobile table horizontally scrollable'],'platform':'Make NOT_RUN'},ensure_ascii=False,indent=2)+'\n');print('PASS 21 viewport checks, anchor popups, nav/scroll and regex copy text.')
