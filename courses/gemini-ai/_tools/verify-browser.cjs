const {chromium}=require('/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..'),out=path.join(root,'_repair/2026-10-06/evidence');fs.mkdirSync(out,{recursive:true});
const meta=JSON.parse(fs.readFileSync(path.join(root,'_source/lesson-map.json'),'utf8')),route=Object.keys(meta),records=[],errors=[];
const base='http://127.0.0.1:31876/';
async function check(name,fn){await fn();records.push({name,status:'PASS'});console.log('PASS',name)}
(async()=>{
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
await context.route('https://**/*',r=>r.abort());
await context.addInitScript(()=>{sessionStorage.setItem('gemini_auth','1')});
const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
const go=async file=>{await page.goto(base+file,{waitUntil:'domcontentloaded'});await page.waitForTimeout(80)};
await check('10站必修实际导航闭环',async()=>{
 await go(route[0]);
 for(let i=0;i<route.length;i++){
  assert(page.url().includes(route[i]));assert((await page.locator('#core-route-banner').innerText()).includes(`${i+1}／10`));
  const next=page.locator('.lesson-nav [data-nav-role="next"]');await next.click();
 }
 assert(page.url().endsWith('index.html'));
});
await check('成果勾选持久化而非阅读自动完课',async()=>{
 await page.locator('[data-core-complete]').first().check();await page.reload();assert.equal(await page.locator('#core-progress-count').innerText(),'1 / 10');
 await page.locator('[data-core-complete]').first().uncheck();
});
await check('预算正常、变更、超支、空值修复与持久化',async()=>{
 await go('assets/tools/budget-reference.html');await page.locator('#reset').click();
 let s=await page.locator('#summary').innerText();for(const n of ['26000.00','27800.00','1800.00','2200.00'])assert(s.includes(n));
 await page.locator('input[data-row="2"][data-col="1"]').fill('45');assert((await page.locator('#summary').innerText()).includes('26750.00'));
 await page.locator('#approved').fill('27000');assert((await page.locator('#summary').innerText()).includes('-800.00'));
 await page.locator('input[data-row="2"][data-col="1"]').fill('');assert(await page.locator('#export').isDisabled());assert(!(await page.locator('#summary').innerText()).includes('27800'));
 await page.locator('input[data-row="2"][data-col="1"]').fill('45');assert(!(await page.locator('#export').isDisabled()));await page.reload();assert.equal(await page.locator('input[data-row="2"][data-col="1"]').inputValue(),'45');
});
await check('预算CSV/JSON导出、非法导入保留、还原与独立迁移',async()=>{
 await page.locator('#approved').fill('30000');let pending=page.waitForEvent('download');await page.locator('#export').click();let d=await pending;await d.saveAs(path.join(out,d.suggestedFilename()));
 const csv=fs.readFileSync(path.join(out,d.suggestedFilename()),'utf8');assert(csv.includes('26750'));assert(csv.includes('2200'));
 pending=page.waitForEvent('download');await page.locator('#backup').click();d=await pending;await d.saveAs(path.join(out,d.suggestedFilename()));
 const saved=JSON.parse(fs.readFileSync(path.join(out,d.suggestedFilename()),'utf8'));assert.equal(saved.rows[2][1],'45');
 await page.locator('#restore').setInputFiles({name:'invalid.json',mimeType:'application/json',buffer:Buffer.from('{"approved":30000,"rows":[]}')});await page.waitForFunction(()=>document.getElementById('error').textContent.includes('還原失敗'));assert.equal(await page.locator('input[data-row="2"][data-col="1"]').inputValue(),'45');
 await page.locator('#restore').setInputFiles(path.join(out,'budget-backup.json'));await page.waitForFunction(()=>document.getElementById('error').textContent==='');assert.equal(await page.locator('input[data-row="2"][data-col="1"]').inputValue(),'45');
 await page.locator('details').evaluate(e=>e.open=true);await page.locator('#csv').fill(fs.readFileSync(path.join(root,'assets/materials/budget-invalid.csv'),'utf8'));await page.locator('#import').click();assert((await page.locator('#error').innerText()).includes('匯入失敗'));assert.equal(await page.locator('input[data-row="2"][data-col="1"]').inputValue(),'45');
 await page.locator('#approved').fill('25000');await page.locator('#csv').fill(fs.readFileSync(path.join(root,'assets/materials/budget-transfer.csv'),'utf8'));await page.locator('#import').click();const s=await page.locator('#summary').innerText();for(const n of ['20600.00','21300.00','700.00','3700.00'])assert(s.includes(n));
 await page.pdf({path:path.join(out,'budget-print.pdf'),format:'A4',printBackground:true});
});
await check('KPI方向、变更、零基期、缺值与零目标',async()=>{
 await go('assets/tools/kpi-reference.html');await page.locator('#reset').click();let statuses=await page.locator('#summary h2').allTextContents();assert.deepEqual(statuses,['受理件數：已達標','處理時間：未達標','錯誤率：已達標']);
 await page.locator('input[data-row="1"][data-col="4"]').fill('2');assert((await page.locator('#summary').innerText()).includes('-50.0%'));await page.reload();assert.equal(await page.locator('input[data-row="1"][data-col="4"]').inputValue(),'2');
 await page.locator('details').evaluate(e=>e.open=true);await page.locator('#csv').fill(fs.readFileSync(path.join(root,'assets/materials/kpi-exceptions.csv'),'utf8'));await page.locator('#import').click();statuses=await page.locator('#summary h2').allTextContents();assert.deepEqual(statuses,['新增服務：已達標','回覆時間：待確認','錯誤率：已達標']);assert((await page.locator('#summary').innerText()).includes('不可計算'));
 let pending=page.waitForEvent('download');await page.locator('#export').click();let d=await pending;await d.saveAs(path.join(out,d.suggestedFilename()));assert(fs.readFileSync(path.join(out,d.suggestedFilename()),'utf8').includes('待確認'));
 pending=page.waitForEvent('download');await page.locator('#backup').click();d=await pending;await d.saveAs(path.join(out,d.suggestedFilename()));
 await page.locator('#restore').setInputFiles(path.join(out,'kpi-backup.json'));await page.waitForFunction(()=>document.getElementById('error').textContent==='');assert((await page.locator('#summary').innerText()).includes('回覆時間：待確認'));
 await page.pdf({path:path.join(out,'kpi-print.pdf'),format:'A4',printBackground:true});
});
await check('计时器暂停、重复开始、重设、归零',async()=>{
 await go('assets/tools/timer-reference.html');await page.locator('#seconds').fill('3');await page.locator('#start').click();await page.locator('#start').click();await page.waitForTimeout(1100);await page.locator('#pause').click();const s=await page.locator('#display').innerText();assert(s.includes('2 秒'));await page.waitForTimeout(1100);assert.equal(await page.locator('#display').innerText(),s);await page.locator('#reset').click();assert((await page.locator('#display').innerText()).includes('3 秒'));
 await page.locator('#seconds').fill('1');await page.locator('#start').click();await page.waitForTimeout(1200);assert((await page.locator('#display').innerText()).includes('時間到'));
});
await check('时区夏令时间与完整会议区间',async()=>{
 await go('part2/PRAC2-2.html');await page.locator('#legacy-reference').evaluate(e=>e.open=true);
 const dates=await page.evaluate(()=>{const winter=new Date('2026-01-15T09:00:00+08:00'),summer=new Date('2026-07-15T09:00:00+08:00');return [zonedParts(winter,'America/New_York').hour,zonedParts(summer,'America/New_York').hour,intervalInWork(new Date('2026-10-06T17:00:00+08:00'),new Date('2026-10-06T18:30:00+08:00'),'Asia/Taipei')]});assert.deepEqual(dates,['20','21',false]);
 await page.locator('#meeting-duration').fill('90');await page.locator('[onclick="calcTimezone()"]').click();assert((await page.locator('#time-table-wrap').innerText()).includes('尚未取得出席者實際確認'));
});
await check('热点未知不等于空闲，单人忙碌不被平均隐藏',async()=>{
 await go('part5/PRAC5-11.html');const r=await page.evaluate(()=>{members=['甲','乙','丙','丁'];data={'甲':{'週一-09:00':1},'乙':{'週一-09:00':0},'丙':{'週一-09:00':0},'丁':{'週一-09:00':0}};const busy=getOverallValue('週一','09:00');data['甲']={};const unknown=getOverallValue('週一','09:00');data['甲']={'週一-09:00':0};return [busy,unknown,getOverallValue('週一','09:00')]});assert.deepEqual(r,[1,4,0]);
});
await check('UTM保留查询与片段，更新重复参数',async()=>{
 await go('part5/PRAC5-3.html');await page.locator('#legacy-reference').evaluate(e=>e.open=true);await page.locator('#u-base').fill('https://example.com/a?keep=1&utm_source=old&utm_source=old2#section');await page.locator('#u-source').fill('電子郵件');await page.locator('#u-campaign').fill('活動 A');await page.locator('[onclick="generateUTM()"]').click();const u=new URL(await page.locator('#utm-url').innerText());assert.equal(u.hash,'#section');assert.equal(u.searchParams.get('keep'),'1');assert.equal(u.searchParams.getAll('utm_source').length,1);assert.equal(u.searchParams.get('utm_source'),'電子郵件');
});
await check('原KPI示范也处理方向与未知',async()=>{
 await go('part3/PRAC3-3.html');await page.locator('#legacy-reference').evaluate(e=>e.open=true);await page.locator('#ktarget-1').fill('3');await page.locator('#kactual-1').fill('5');await page.locator('#kdir-1').selectOption('lower');await page.evaluate(()=>renderDashboard());assert((await page.locator('#dashboard-grid .kpi-card').first().innerText()).includes('未達標'));await page.locator('#kactual-1').fill('');await page.evaluate(()=>renderDashboard());assert((await page.locator('#dashboard-grid .kpi-card').first().innerText()).includes('待確認'));
});
const visual=[];const reps=['index.html','part2/PRAC2-1.html','part3/PRAC3-3.html','part6/PRAC6-1.html','assets/tools/budget-reference.html','assets/tools/kpi-reference.html'];
await check('桌面1440与手机390/430的页面宽度、导航与可见范围',async()=>{
 for(const width of [1440,390,430]){
  await page.setViewportSize({width,height:900});
  for(const file of [...new Set([...route,...reps,'part2/PRAC2-2.html','part5/PRAC5-11.html'])]){
   await go(file);await page.evaluate(()=>{Object.keys(localStorage).filter(k=>k.startsWith('progress:')).forEach(k=>localStorage.removeItem(k));window.scrollTo(0,0)});
   const m=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,bodyCount:document.querySelectorAll('.lesson-body').length}));assert(m.scroll<=m.width+1,`${file} ${width}px overflow ${m.scroll}`);
   const pos=width===1440&&reps.includes(file)?['top','modified','middle','bottom']:['top'];
   for(const at of pos){
    await page.evaluate(at=>{const body=document.querySelector('.lesson-body');if(at==='modified'&&body)body.scrollIntoView();else window.scrollTo(0,at==='bottom'?document.documentElement.scrollHeight:at==='middle'?document.documentElement.scrollHeight/2:0)},at);await page.waitForTimeout(200);
    visual.push({file,width,position:at,...m});
    if(reps.includes(file)){const name=file.replaceAll('/','-').replace('.html','')+`-${width}-${at}.png`;await page.screenshot({path:path.join(out,name)});}
   }
   if(file!=='index.html'&&file.startsWith('part')){await page.locator('.lesson-nav').scrollIntoViewIfNeeded();assert(await page.locator('.lesson-nav a').first().isVisible())}
  }
 }
});
assert.deepEqual(errors,[],'browser pageerror');
fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify({executor:'author self-test via Playwright / Chrome',records,visual,pageerrors:errors,platform_generation:'PENDING',human_follow_along:'PENDING'},null,2));
await browser.close();console.log(`Completed ${records.length} checks, ${visual.length} viewport/position observations.`);
})().catch(e=>{fs.writeFileSync(path.join(out,'browser-failure.txt'),e.stack);console.error(e);process.exit(1)});
