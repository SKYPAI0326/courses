const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..'),out=path.join(root,'_repair/2026-10-11-plain-language/rendered');fs.mkdirSync(out,{recursive:true});
const targets={'CH1-1':'#ch1-step-1','CH2-1':'#ch2-step-6','CH3-1':'#ch3-step-1','CH4-1':'#ch4-step-8','PRAC2-1':'#gamma-outline-1'};
(async()=>{const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});const result=[];
try{const ctx=await browser.newContext();await ctx.addInitScript(()=>localStorage.setItem('aibeginner_auth','1'));
for(const [name,sel] of Object.entries(targets)){
 const page=await ctx.newPage();await page.setViewportSize({width:1440,height:1000});await page.goto(pathToFileURL(path.join(root,name+'.html')).href);
 for(const [position,target] of [['top',null],['middle',sel],['workbench',name==='PRAC2-1'?'#gamma-save-content':'form'],['bottom','footer']]){
  if(target)await page.locator(target).first().evaluate(e=>{let p=e.parentElement;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}e.scrollIntoView({behavior:'instant',block:'start'})});else await page.evaluate(()=>window.scrollTo(0,0));
  const file=name+'-1440-'+position+'.png';await page.screenshot({path:path.join(out,file)});result.push({name,width:1440,position,file,...await page.evaluate(()=>({pageWidth:document.documentElement.scrollWidth,viewport:innerWidth}))});
 }
 for(const width of [390,430]){
  await page.setViewportSize({width,height:1000});await page.locator(sel).evaluate(e=>{let p=e.parentElement;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}const table=e.parentElement.previousElementSibling;if((e.id==='ch1-step-1'||e.id==='ch3-step-1')&&table) table.previousElementSibling.scrollIntoView({behavior:'instant',block:'start'});else e.scrollIntoView({behavior:'instant',block:'start'})});
  const file=name+'-'+width+'-middle.png';await page.screenshot({path:path.join(out,file)});result.push({name,width,position:'middle',file,...await page.evaluate(()=>({pageWidth:document.documentElement.scrollWidth,viewport:innerWidth}))});
 }
 await page.close();
}
}finally{fs.writeFileSync(path.join(out,'screenshots.json'),JSON.stringify(result,null,2));await browser.close();}
console.log(JSON.stringify({screenshots:result.length,overflow:result.filter(r=>r.pageWidth>r.viewport)}));})().catch(e=>{console.error(e);process.exit(1)});
