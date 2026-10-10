const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require('/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.resolve(__dirname, '..');
const out = path.join(root, '_validation/step-by-step-2026-10-11');
fs.mkdirSync(out, {recursive:true});
const names = ['index','module1','CH1-1','CH2-1','CH3-1','CH4-1','PRAC2-1'];
const resume=process.argv[2];
const selected=resume?names.slice(names.indexOf(resume)):names;
const previous=resume?JSON.parse(fs.readFileSync(path.join(out,'browser-results.json'),'utf8')):null;
const results = previous||{kind:'author-self-check', viewports:[], workbench:[], copy:[], screenshots:[], errors:[]};
if(resume){
 for(const key of ['viewports','workbench','copy','errors'])results[key]=results[key].filter(x=>!selected.includes(x.name));
 results.screenshots=results.screenshots.filter(x=>!selected.some(name=>x.startsWith(name+'-')));
}
const targets={'CH1-1':'#ch1-step-4','CH2-1':'#ch2-step-6','CH3-1':'#ch3-step-5','CH4-1':'#ch4-step-3','PRAC2-1':'#gamma-outline-1'};
function check(ok, why){if(!ok)throw new Error(why);}
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try {
  const ctx=await browser.newContext({acceptDownloads:true});
  await ctx.addInitScript(()=>{
    localStorage.setItem('aibeginner_auth','1');
    window.__copied='';
    Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>{window.__copied=text;}}});
  });
  for(const name of selected){
   const page=await ctx.newPage();
   page.on('pageerror',e=>results.errors.push({name,error:e.message}));
   await page.goto(pathToFileURL(path.join(root,name+'.html')).href);
   await page.evaluate(()=>{for(const key of Object.keys(localStorage)){if(key!=='aibeginner_auth')localStorage.removeItem(key)} });
   await page.reload();
   for(const width of [1440,390,430]){
    await page.setViewportSize({width,height:900});
    await page.evaluate(()=>window.scrollTo(0,0));
    const top=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,body:document.body.scrollWidth}));
    check(top.scroll<=width+1,name+' top overflow '+width);
    let anchor=null;
    if(targets[name]){
     await page.locator(targets[name]).evaluate(e=>{let p=e.parentElement;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement} e.scrollIntoView({behavior:'instant',block:'start'});});
     anchor=await page.evaluate(sel=>{const e=document.querySelector(sel),r=e.getBoundingClientRect(),bars=Array.from(document.querySelectorAll('.topbar,.lesson-quicknav,.progress-strip')).filter(b=>['sticky','fixed'].includes(getComputedStyle(b).position));return {top:r.top,barBottom:Math.max(0,...bars.map(b=>b.getBoundingClientRect().bottom)),scroll:document.documentElement.scrollWidth};},targets[name]);
     check(anchor.scroll<=width+1,name+' step overflow '+width);
     check(anchor.top>=anchor.barBottom-1,name+' anchor hidden by header '+width);
     results.viewports.push({name,width,top,anchor});
    }else results.viewports.push({name,width,top});
    if((name==='CH2-1') || (width===390 && targets[name])){
      const file=name+'-'+width+'-steps.png';await page.screenshot({path:path.join(out,file)});results.screenshots.push(file);
    }
   }
   if(name==='CH2-1'){
    await page.setViewportSize({width:1440,height:900});
    for(const [position,sel] of [['top',null],['workbench','#communication-workbench'],['bottom','#lesson-quiz']]){
      if(sel)await page.locator(sel).evaluate(e=>{let p=e.parentElement;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}e.scrollIntoView({behavior:'instant',block:'start'})});else await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));
      const file=name+'-1440-'+position+'.png';await page.screenshot({path:path.join(out,file)});results.screenshots.push(file);
    }
   }
   if(name.startsWith('CH')){
    const form=page.locator('form').filter({has:page.locator('[data-field]')}).first();
    await form.evaluate(e=>{let p=e.parentElement;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}});
    const values=await form.locator('[data-required="true"]').evaluateAll(es=>es.map(e=>({field:e.dataset.field,type:e.type,id:e.id})));
    for(const v of values){
      const field=form.locator('[data-field="'+v.field+'"]');
      await field.evaluate(e=>{let p=e.parentElement;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}});
      if(v.type==='checkbox')await field.check();else if(v.type==='select-one')await field.selectOption({label:'一項限制條件'});else await field.fill(name+'：'+v.field+'：自查保存內容');
    }
    await form.locator('[data-action="save"]').click();
    await page.reload();
    const restored=await page.locator('[data-required="true"]').evaluateAll(es=>es.every(e=>e.type==='checkbox'?e.checked:e.type==='select-one'?e.value==='一項限制條件':e.value.includes('自查保存內容')));
    check(restored,name+' restore failed');
    await form.evaluate(e=>{let p=e.parentElement;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}});
    const downloadPromise=page.waitForEvent('download');await form.locator('[data-action="export"]').click();const download=await downloadPromise;
    const dest=path.join(out,download.suggestedFilename());await download.saveAs(dest);
    const content=fs.readFileSync(dest,'utf8');for(const v of values.filter(v=>v.type!=='checkbox'))check(content.includes(v.type==='select-one'?'一項限制條件':name+'：'+v.field+'：自查保存內容'),name+' export missing '+v.field);
    results.workbench.push({name,requiredFields:values.length,restore:restored,filename:download.suggestedFilename(),contentVerified:true});
   }
   if(name==='CH1-1'||name==='CH2-1'){
    const id=name==='CH1-1'?'ready-a':'ch2-ready-message';
    await page.locator('#'+id).evaluate(e=>{let p=e.parentElement;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}});
    await page.locator('[data-gamma-copy="'+id+'"]').click();
    const text=await page.locator('#'+id).textContent();check(await page.evaluate(()=>window.__copied)===text,name+' copied text differs');results.copy.push({name,id,complete:true});
   }
   if(name==='PRAC2-1'){
    for(const kind of ['企劃.txt','10頁大綱.md','Gamma貼入文字.txt']){
      await page.locator('#gamma-save-content').fill('第一段：'+kind+'\n最後一段：完整保存');await page.locator('#gamma-save-kind').selectOption(kind);
      const event=page.waitForEvent('download');await page.locator('#gamma-save-download').click();const download=await event;const dest=path.join(out,download.suggestedFilename());await download.saveAs(dest);
      check(fs.readFileSync(dest,'utf8').includes('最後一段：完整保存'),'Gamma download missing tail');results.copy.push({name,filename:download.suggestedFilename(),complete:true});
    }
   }
   await page.close();
  }
  check(!results.errors.length,'page errors');
 } finally {
  fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify(results,null,2));await browser.close();
 }
 console.log(JSON.stringify({viewports:results.viewports.length,workbench:results.workbench.length,copy:results.copy.length,errors:results.errors.length,screenshots:results.screenshots.length}));
})().catch(e=>{console.error(e);process.exit(1)});
