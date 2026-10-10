const fs=require('fs'),path=require('path');
const {pathToFileURL}=require('url');
const {chromium}=require('/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=process.cwd(),out=path.join(root,'_validation/review-findings-2026-10-11');
const result={kind:'author-self-check',pages:[],copy:[],screenshots:[],errors:[]};
const assert=(ok,msg)=>{if(!ok)throw Error(msg)};
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try{
  const ctx=await browser.newContext();
  await ctx.addInitScript(()=>{localStorage.clear();localStorage.setItem('aibeginner_auth','1');window.__copied='';Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async t=>{window.__copied=t}}})});
  for(const name of ['CH2-1','CH4-1']){
   const page=await ctx.newPage();page.on('pageerror',e=>result.errors.push({name,error:e.message}));
   await page.goto(pathToFileURL(path.join(root,name+'.html')).href);
   for(const width of [1440,390,430]){
    await page.setViewportSize({width,height:900});
    const selector=name==='CH2-1'?'h3.step-heading':'#own-case-revision';
    if(name==='CH4-1'){
     await page.locator('#own-case-revision').evaluate(e=>{e.open=true;e.querySelector('details').open=true});
    }
    for(const [position,target] of [['top',null],['changed',name==='CH2-1'?'text=先看：同一讀者的語氣調整':'#prompt-change-own'],['middle',name==='CH2-1'?'#ch2-step-6':'#ch4-step-8'],['bottom','.nav-footer']]){
     if(width!==1440&&position!=='changed')continue;
     if(target){await page.locator(target).first().evaluate(e=>{for(let p=e.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;e.scrollIntoView({block:'center',behavior:'instant'})})}
     else await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));
     const sizes=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth}));
     assert(sizes.scroll<=width+1,name+' horizontal overflow '+width);
     const file=name+'-'+width+'-'+position+'.png';await page.screenshot({path:path.join(out,file)});result.screenshots.push(file);
    }
    const step=name==='CH2-1'?'#ch2-step-6':'#ch4-step-5';
    await page.locator(step).evaluate(e=>e.scrollIntoView({block:'start',behavior:'instant'}));
    const bounds=await page.evaluate(sel=>({top:document.querySelector(sel).getBoundingClientRect().top,bars:Math.max(0,...Array.from(document.querySelectorAll('.topbar,.lesson-quicknav,.progress-strip')).filter(e=>['fixed','sticky'].includes(getComputedStyle(e).position)).map(e=>e.getBoundingClientRect().bottom))}),step);
    assert(bounds.top>=bounds.bars-1,name+' header covers anchor '+width);
    result.pages.push({name,width,noOverflow:true,stepClearOfHeader:true});
   }
   if(name==='CH4-1'){
    await page.locator('#own-case-revision').evaluate(e=>e.open=true);
    await page.locator('[data-gamma-copy="prompt-change-own"]').click();
    const copied=await page.evaluate(()=>window.__copied);
    const expected=fs.readFileSync(path.join(root,'assets/workplace/decisions/prompts/change-own.txt'),'utf8').trim();
    assert(copied===expected,'copied prompt mismatch');
    result.copy.push({id:'prompt-change-own',complete:true});
   }
   await page.close();
  }
  assert(result.errors.length===0,'page errors');
 }finally{fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify(result,null,2));await browser.close()}
 console.log(JSON.stringify({viewportChecks:result.pages.length,screenshots:result.screenshots.length,copyChecks:result.copy.length,errors:result.errors.length}));
})().catch(e=>{console.error(e);process.exit(1)});
