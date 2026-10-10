from pathlib import Path
import json
from playwright.sync_api import sync_playwright
b=Path(__file__).resolve().parents[2];out=b/'_repair/2026-10-11';shots=out/'screenshots';shots.mkdir(exist_ok=True)
meta=json.loads((b/'_repair/2026-10-09/lesson-meta.json').read_text());origin='http://127.0.0.1:9877';prefix=origin+'/courses/gen-ai-36h/';results=[];issues=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True)
 context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1,accept_downloads=True)
 context.add_init_script("sessionStorage.setItem('gen36_auth','1');")
 page=context.new_page();page.goto(origin);page.evaluate('localStorage.clear()')
 for width in [1440,390,430]:
  page.set_viewport_size({'width':width,'height':1000})
  for u,m in meta.items():
   page.evaluate('localStorage.clear()');page.goto(prefix+m['path'],wait_until='domcontentloaded');page.wait_for_timeout(80)
   metrics=page.evaluate('''()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,bodyWidth:document.querySelector('.lesson-body').getBoundingClientRect().width,top:scrollY,sections:document.querySelectorAll('.lesson-body .lesson-section').length})''')
   if metrics['scroll']>width+1:issues.append([u,width,'horizontal overflow',metrics])
   if metrics['top']>5:issues.append([u,width,'first entry scrolled',metrics])
   results.append({'unit':u,'viewport':width,**metrics})
   if u in ['CH2-1','CH5-3','PRAC7']:
    page.screenshot(path=str(shots/f'{u}-{width}-top.png'))
    if width==1440:
     for pos,name in [(0.3,'modified'),(0.55,'middle'),(1,'bottom')]:
      page.evaluate('(ratio)=>scrollTo({top:(document.documentElement.scrollHeight-innerHeight)*ratio,behavior:"instant"})',pos);page.wait_for_timeout(80);page.screenshot(path=str(shots/f'{u}-{width}-{name}.png'))
 # UI link opens in new page; navigation stays same tab.
 page.goto(prefix+'part2/CH2-1.html');page.evaluate('scrollTo(0,0)')
 with context.expect_page() as pop:page.locator('.lesson-body a[href*="START-HERE.html"]').first.click()
 popup=pop.value;popup.wait_for_load_state('domcontentloaded');assert 'START-HERE.html' in popup.url;assert 'CH2-1.html' in page.url;popup.close()
 nav=page.locator('a.nav-btn').last;destination=nav.get_attribute('href');nav.click();assert destination.split('/')[-1] in page.url
 # Persisted mid-page scroll and fresh top state.
 page.goto(prefix+'part2/CH2-1.html');page.evaluate('scrollTo({top:1400,behavior:"instant"})');page.wait_for_function("localStorage.getItem('progress:'+location.pathname)==='1400'");page.reload(wait_until='load');page.wait_for_function('Math.abs(scrollY-1400)<10')
 page.evaluate("localStorage.removeItem('progress:'+location.pathname)");page.goto('about:blank');page.goto(prefix+'part2/CH2-1.html');page.wait_for_timeout(100);assert page.evaluate('scrollY')<5
 # Reference chart actually reads fixture and outputs regional counts plus corrected version.
 page.goto(prefix+'assets/reference-chart.html');page.locator('#file').set_input_files(str(b/'assets/sales-raw-transactions.csv'));page.wait_for_function("document.querySelector('#status').textContent.includes('6,950')")
 table=page.locator('#table').inner_text();assert '有效筆數' in table
 assert 'North\t4\t1800' in table and 'South\t2\t1450' in table,table
 rows=(b/'assets/sales-raw-transactions.csv').read_text().replace('TX-006,,','TX-006,2026-04-06,');page.locator('#file').set_input_files({'name':'sales-corrected.csv','mimeType':'text/csv','buffer':rows.encode()});page.wait_for_function("document.querySelector('#status').textContent.includes('7,550')");assert 'South\t3\t2050' in page.locator('#table').inner_text()
 page.locator('#file').set_input_files(str(b/'assets/sales-24-months.csv'));page.wait_for_function("document.querySelector('#status').textContent.includes('4,165,200')")
 # Real form labels, persistence, export/import and invalid import preservation.
 for unit,kind in [('PRAC6','toolbox'),('PRAC7','showcase')]:
  part='part6' if unit=='PRAC6' else 'part7';page.goto(prefix+part+'/'+unit+'.html');page.evaluate('localStorage.clear()');page.reload()
  if kind=='toolbox':page.get_by_role('button',name='新增工具卡',exact=True).click()
  labels=page.locator('.gen36-editor label');sample={}
  for i in range(labels.count()):
   label=labels.nth(i);field=label.locator('input,textarea');name=label.inner_text();value='https://example.com/result' if '網址' in name else '測試 '+name+' <核對> & 原始來源';sample[name]=value;field.fill(value)
  page.reload();assert page.locator('.gen36-editor input').first.input_value().startswith('測試 名稱')
  with page.expect_download() as d:page.get_by_role('button',name='匯出JSON備份',exact=True).click()
  file=out/(kind+'-browser-backup.json');d.value.save_as(str(file));data=json.loads(file.read_text());assert data['kind']==kind
  page.locator('.gen36-editor input').first.fill('暫改')
  page.locator('input[type=file]').set_input_files(str(file));page.wait_for_timeout(120);assert page.locator('.gen36-editor input').first.input_value().startswith('測試 名稱')
  page.locator('input[type=file]').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{bad'});page.wait_for_timeout(120);assert '匯入失敗' in page.locator('.gen36-status').inner_text();assert page.locator('.gen36-editor input').first.input_value().startswith('測試 名稱')
  if kind=='showcase':
   with page.expect_download() as d:page.get_by_role('button',name='匯出個人HTML',exact=True).click()
   export=out/'showcase-browser-export.html';d.value.save_as(str(export));html=export.read_text();assert '&lt;核對&gt;' in html
   extra=context.new_page();extra.goto(export.as_uri());assert '測試 名稱' in extra.locator('body').inner_text();extra.close()
 # New readable guides at mobile size.
 for rel in ['assets/html-file-workflow.html','assets/part5-stage-handoff.html','assets/part6-filled-workflow.html','assets/capstone/branch-guide.html']:
  page.set_viewport_size({'width':390,'height':1000});page.goto(prefix+rel);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),rel
 page.close();browser.close()
(out/'browser-results.json').write_text(json.dumps({'actor':'tool-run','engine':'Chromium headless','checks':results,'issues':issues,'functional':['asset opens new tab; course navigation same tab','first entry and persisted scroll reload','raw/corrected/monthly CSV chart values and regional counts','PRAC6/7 actual fields, saved reload, JSON roundtrip, invalid JSON preservation','PRAC7 escaped HTML export reopened','four readable guides 390px']},ensure_ascii=False,indent=2))
assert not issues,issues
print('PASS browser: 84 lesson viewport checks, new-tab/navigation/scroll, chart and form workflows.')
