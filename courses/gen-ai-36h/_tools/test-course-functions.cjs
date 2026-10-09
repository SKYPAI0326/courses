const assert=require('node:assert/strict');
const t=require('../assets/course-tools.js');
for(const [months,total,count] of [[3,94500,1],[6,189000,2],[12,378000,4]]){
 const q=t.quote({fee:30000,months,discount:0,payment:'quarter',tax:true});
 assert.equal(q.total,total);assert.equal(q.installments.length,count);assert.equal(q.installments.reduce((a,b)=>a+b,0),total);
}
const q=t.quote({fee:30000,months:12,discount:15,payment:'year',tax:true});assert.equal(q.net,296820);assert.equal(q.total,311661);assert.equal(q.discountPercent,17.55);
for(const x of [{fee:30000,months:3,discount:0,payment:'year'}, {fee:-1,months:12,discount:0,payment:'month'}, {fee:30000,months:'',discount:0,payment:'month'},{fee:30000,months:12,discount:31,payment:'month'},{fee:'',months:12,discount:0,payment:'month'}])assert.throws(()=>t.quote(x));
const tail=t.quote({fee:30000,months:12,discount:17.3,payment:'quarter',tax:true});assert.equal(tail.installments.reduce((a,b)=>a+b,0),tail.total);
const rows=Array.from({length:24},(_,i)=>({month:`${2024+Math.floor((i+4)/12)}-${String((i+4)%12+1).padStart(2,'0')}`,revenue:100+i*10,orders:10}));
assert.equal(t.stats(rows).total,5160);assert.equal(t.stats(rows).yoy.length,12);assert.equal(t.stats(rows.slice(12)).yoy[0].percent,null);assert.throws(()=>t.stats([...rows,rows[0]]));assert.throws(()=>t.stats([{month:'bad',revenue:1,orders:1}]));
const good={submitted_at:'2026-10-09T09:00',name:'測試',email:'test@example.com',subject:'問價',message:'詢問方案',category:'inquiry',summary:'詢問方案',next_action:'準備草稿',review_status:'已覆核'};
assert.equal(t.route(good,[]).route,'業務');assert.equal(t.route(good,[t.key(good)]).status,'duplicate');assert.equal(t.route({...good,review_status:'待覆核'},[]).status,'blocked');assert.equal(t.route({...good,category:'unknown'},[]).status,'blocked');
const cards=[{name:'摘要',when:'週報',input:'五行',output:'三點',check:'日期',recovery:'補資料',location:'本機'}];
const json=t.exportData('toolbox',cards);assert.deepEqual(t.importData(json,'toolbox').data,cards);assert.throws(()=>t.importData('{broken','toolbox'));assert.throws(()=>t.importData(json,'showcase'));assert.throws(()=>t.importData(JSON.stringify({version:2,kind:'toolbox',data:cards}),'toolbox'));
const storage={setItem(){throw Error('quota')},getItem(){return null}};assert.equal(t.save(storage,'test',json).ok,false);
const html=t.showcase({name:'<script>alert(1)</script>',task:'測試 & 說明',user:'同事',input:'資料',output:'文件',check:'已核對',recovery:'重讀',status:'尚未量測',url:'javascript:alert(1)',tools:'Claude'});
assert(!html.includes('<script>'));assert(html.includes('&lt;script&gt;'));assert(!html.includes('href="javascript:'));assert(!html.includes('localStorage'));assert(!html.includes('gateHash'));
assert.equal(t.safeUrl('https://example.com/demo'),'https://example.com/demo');assert.equal(t.safeUrl('data:text/html,x'),'');assert.equal(t.safeUrl('file:///private/x'),'');
console.log('PASS: quote boundaries, totals/YoY, routing/dedup, JSON validation, storage failure, escaped export.');
