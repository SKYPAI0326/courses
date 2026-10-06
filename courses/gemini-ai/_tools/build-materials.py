"""Build inspectable teaching materials and offline reference tools; no AI calls."""
from pathlib import Path
import csv,json,html

ROOT=Path(__file__).resolve().parents[1]
M=ROOT/'assets/materials';T=ROOT/'assets/tools'
M.mkdir(parents=True,exist_ok=True);T.mkdir(parents=True,exist_ok=True)

def csvfile(name,fields,rows):
    with (M/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(fields);w.writerows(rows)

budget=[['講師',4,2500,10500,'增加交通費'],['場地',1,8000,8500,'延長使用'],['餐點',40,150,6500,'增加配送'],['印刷',40,50,2300,'加印']]
csvfile('budget-normal.csv',['item','quantity','unit_price','actual','note'],budget)
csvfile('budget-invalid.csv',['item','quantity','unit_price','actual','note'],[['餐點','',150,6500,'數量待確認'],['場地',1,-8000,8500,'不可接受負單價']])
csvfile('budget-transfer.csv',['item','quantity','unit_price','actual','note'],[['講師',3,3000,9500,'含交通'],['場地',1,5000,5000,''],['餐點',30,180,5600,'含配送'],['印刷',30,40,1200,'']])
kpis=[['受理件數','件','higher',100,120,90,'2026-09','案件台帳'],['處理時間','天','lower',3,5,4,'2026-09','結案台帳'],['錯誤率','%','lower',2,1,1.5,'2026-09','複核紀錄']]
csvfile('kpi-normal.csv',['metric','unit','direction','target','actual','previous','period','source'],kpis)
csvfile('kpi-exceptions.csv',['metric','unit','direction','target','actual','previous','period','source'],[['新增服務','件','higher',10,12,0,'2026-09','試辦台帳'],['回覆時間','天','lower',2,'',3,'2026-09','資料未到'],['錯誤率','%','lower',0,0,1,'2026-09','複核紀錄']])
meeting_a='''活動籌備會議逐字稿 A（虛構資料）
會議日期：2026/10/06
主持人：今天確認場地、餐點與邀請安排。只記錄今天確定要做的交辦。
林：我負責在 2026/10/09 前確認場地。
陳：餐點我來詢價，期限還沒定。
王：下次可考慮直播，今天先不決定。
主持人：取消原訂明天寄出邀請的安排。
林：了解，我完成場地確認後會回報。
主持人：下次會議再確認餐點期限，今天先到這裡。
'''
meeting_b='''行政協調會議逐字稿 B（虛構資料）
會議日期：2026/10/07
主持人：上次的兩項工作今天更新，請以最後的明確決議為準。
林：場地已確認，這項完成了。
陳：我會在 2026/10/12 前完成餐點詢價。
王：或許可以做問卷，但我沒有承諾接這項。
主持人：新增「整理報名名單」，負責人與期限下次再確認。
林：海報原本由我負責，先暫定 2026/10/10 交付。
主持人：海報改由王負責，期限延到 2026/10/13，請以這次調整為準。
王：好，我接下海報。
主持人：邀請寄送仍維持取消，不要列成新的待辦。
'''
(M/'meeting-a.txt').write_text(meeting_a);(M/'meeting-b.txt').write_text(meeting_b)
answers={
 'budget':{'approved':30000,'estimated':26000,'actual':27800,'difference':1800,'remaining':2200,'together_quantity45_estimated':26750,'together_difference':1050,'together_remaining':2200,'transfer_approved':25000,'transfer_estimated':20600,'transfer_actual':21300,'transfer_difference':700,'transfer_remaining':3700},
 'kpi':[{'metric':r[0],'status':s,'change':c} for r,s,c in zip(kpis,['已達標','未達標','已達標'],[33.333333,25,-33.333333])],
 'meeting_a':[
  {'task':'確認場地','owner':'林','due_date':'2026-10-09','status':'待辦','source_text':'林：我負責在 2026/10/09 前確認場地。','uncertain_reason':'','confirmed':False},
  {'task':'餐點詢價','owner':'陳','due_date':None,'status':'待辦','source_text':'陳：餐點我來詢價，期限還沒定。','uncertain_reason':'期限未定','confirmed':False}],
 'meeting_b':[
  {'task':'餐點詢價','owner':'陳','due_date':'2026-10-12','status':'待辦','source_text':'陳：我會在 2026/10/12 前完成餐點詢價。','uncertain_reason':'','confirmed':False},
  {'task':'整理報名名單','owner':None,'due_date':None,'status':'待辦','source_text':'主持人：新增「整理報名名單」，負責人與期限下次再確認。','uncertain_reason':'負責人與期限未定','confirmed':False},
  {'task':'海報','owner':'王','due_date':'2026-10-13','status':'待辦','source_text':'主持人：海報改由王負責，期限延到 2026/10/13，請以這次調整為準。\n王：好，我接下海報。','uncertain_reason':'','confirmed':False}],
 'meeting_b_excluded':['場地：已完成，可列歷史；不列有效待辦','問卷：僅提議','邀請寄送：已取消'],
 'meeting_b_superseded':['海報：林／2026-10-10 是已被更新的舊值']}
(M/'reference-answers.json').write_text(json.dumps(answers,ensure_ascii=False,indent=2))
(M/'requirements-template.txt').write_text('工作情境／使用者：\n輸入資料與來源：\n處理規則：\n缺值與例外：\n輸出與保存位置：\n正常測試輸入／預期答案：\n例外測試输入／預期處理：\n需求變更／預期差異：\n'.replace('输入','輸入'))
csvfile('acceptance-template.csv',['case','input_file','expected','observed','pass_or_pending','repair_prompt','retest_result'],[['預算','budget-normal.csv','估算26000；實支27800；差異1800；餘額2200','','待測','',''],['KPI','kpi-normal.csv','件數達標；時間未達標；錯誤率達標','','待測','',''],['AI交辦','meeting-a.txt','兩項有效待辦；陳期限待確認','','待測','',''],['保存','自製工具','關閉重開、改資料再輸出','','待測','','']])
(M/'README.md').write_text('''# 學員素材包

全部為虛構教學資料。CSV 為 UTF-8（含 BOM），可用試算表開啟，也可在參考工具貼上匯入；逐字稿 TXT 為完整輸入。answers JSON 是答案，請先預判再展開核對。

預算：budget-normal.csv 配核定 30000；budget-invalid.csv 查防呆；budget-transfer.csv 配核定 25000 作獨立遷移。
KPI：kpi-normal.csv 查方向；kpi-exceptions.csv 查零基期與缺值。
交辦：meeting-a.txt 同步練習；meeting-b.txt 新資料驗證。
requirements-template.txt 填需求；acceptance-template.csv 記錄實際結果與修复。

參考工具位於 ../tools/。它們是完成品與故障備援，不是學員生成成果。AI 交辦參考頁只顯示人工核對的固定答案，沒有呼叫模型。
'''.replace('修复','修復'))

STYLE='''*{box-sizing:border-box}body{margin:0;background:#f5f3ee;color:#2c2b28;font-family:system-ui,"Noto Sans TC",sans-serif;line-height:1.8}main{max-width:1000px;margin:auto;padding:24px}h1{font-size:1.5rem}h2{font-size:1.15rem}label{display:block}input,select,textarea,button{font:inherit;padding:8px;border:1px solid #d8d4cb;border-radius:4px;max-width:100%}input,select,textarea{width:100%;background:#fff;color:#2c2b28}button{cursor:pointer;background:#fff;margin:4px}button:disabled{opacity:.5;cursor:default}a{color:#5a7a5a}table{width:100%;border-collapse:collapse;min-width:620px}td,th{padding:8px;border-bottom:1px solid #d8d4cb;text-align:left}th{font-weight:600}td input{min-width:65px}.scroll{overflow:auto;max-width:100%}.note{color:#6e6b66}.error{color:#a05030;white-space:pre-wrap}.summary{padding:16px;background:#fff;margin:16px 0;white-space:pre-wrap}textarea{min-height:100px}.actions{display:flex;gap:8px;flex-wrap:wrap}pre{white-space:pre-wrap;overflow-wrap:anywhere}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid #2c2b28;outline-offset:2px}@media(max-width:500px){main{padding:16px}h1{font-size:1.3rem}}@media print{.actions,.import-box,button,.note{display:none}main{max-width:none;padding:0}input,select{border:0;padding:0}.scroll{overflow:visible}table{min-width:0;font-size:10pt}h1{font-size:16pt}}'''
COMMON='''const $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function download(name,text,type='text/plain'){const url=URL.createObjectURL(new Blob([text],{type}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
function csvText(rows){return '\\ufeff'+rows.map(row=>row.map(v=>'"'+String(v??'').replace(/"/g,'""')+'"').join(',')).join('\\r\\n')}
function safeCell(v){const t=String(v??'');return /^[=+@-]/.test(t)?"'"+t:t}
function parseCSV(text){let rows=[],row=[],cell='',quoted=false;text=text.replace(/^\\ufeff/,'');for(let i=0;i<text.length;i++){const c=text[i];if(c==='"'){if(quoted&&text[i+1]==='"'){cell+='"';i++}else if(!quoted&&cell!=='')throw Error('引號格式錯誤');else quoted=!quoted}else if(c===','&&!quoted){row.push(cell);cell=''}else if((c==='\\n'||c==='\\r')&&!quoted){if(c==='\\r'&&text[i+1]==='\\n')i++;row.push(cell);if(row.some(x=>x!==''))rows.push(row);row=[];cell=''}else cell+=c}if(quoted)throw Error('引號未結束');row.push(cell);if(row.some(x=>x!==''))rows.push(row);return rows}
function number(v){if(v===null||v===undefined||String(v).trim()==='')return null;const n=Number(v);return Number.isFinite(n)&&n>=0?n:null}
function money(v){const n=number(v);return n!==null&&Math.abs(n*100-Math.round(n*100))<0.00001?n:null}
function announce(t){$('error').textContent=t}
'''
def page(name,title,body,js=''):
    text=f'<!DOCTYPE html>\n<html lang="zh-Hant"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{title}：離線參考成品與查核素材"><title>{title}｜課程參考工具</title><style>{STYLE}</style></head><body><a href="#main">跳至主要內容</a><main id="main"><h1>{title}</h1>{body}</main><script>{COMMON}\n{js}</script></body></html>'
    (T/name).write_text(text)

page('budget-reference.html','活動預算與核銷差異表', '''<p class="note">離線參考成品。資料保存在這個瀏覽器；交付前下載備份，換電腦請還原 JSON。所有費用已包含必要費用。</p>
<label>核定預算（元）<input id="approved" type="number" min="0" step="0.01" value="30000"></label>
<div class="scroll"><table><thead><tr><th>項目</th><th>數量</th><th>單價</th><th>實支</th><th>備註</th><th>操作</th></tr></thead><tbody id="rows"></tbody></table></div>
<div class="actions"><button id="add">新增項目</button><button id="reset">載入標準資料</button><button id="export">下載明細 CSV</button><button id="print">列印／另存 PDF</button><button id="backup">備份 JSON</button><label>還原 JSON<input id="restore" type="file" accept=".json"></label></div>
<p id="error" class="error" role="status"></p><div id="summary" class="summary" aria-live="polite"></div>
<details class="import-box"><summary>貼上素材 CSV 匯入（取代目前明細，核定預算另填）</summary><textarea id="csv" aria-label="預算 CSV"></textarea><button id="import">匯入 CSV</button></details>''', '''
const key='gemini-budget-reference-v1';const defaults='''+json.dumps(budget,ensure_ascii=False)+''';let rows=structuredClone(defaults);
function validate(items,approved){const errors=[];if(money(approved)===null)errors.push('核定預算須是非負金額，最多兩位小數');if(!items.length)errors.push('至少需要一項明細');items.forEach((r,i)=>{if(!Array.isArray(r)||r.length!==5){errors.push('明細欄位錯誤');return}if(!String(r[0]).trim())errors.push(`第 ${i+1} 列缺項目`);if(number(r[1])===null||!Number.isInteger(number(r[1])))errors.push(`第 ${i+1} 列數量须為非負整數`);if(money(r[2])===null||money(r[3])===null)errors.push(`第 ${i+1} 列單價／實支缺值或不是有效非負金額`)});return errors}
function calculate(items,approved){const estimated=items.reduce((n,r)=>n+Math.round(Number(r[1])*Number(r[2])*100),0)/100;const actual=items.reduce((n,r)=>n+Math.round(Number(r[3])*100),0)/100;return {estimated,actual,difference:Math.round((actual-estimated)*100)/100,remaining:Math.round((Number(approved)-actual)*100)/100}}
function render(){ $('rows').innerHTML=rows.map((r,i)=>`<tr>${r.map((v,j)=>`<td><input aria-label="第${i+1}列${['項目','數量','單價','實支','備註'][j]}" data-row="${i}" data-col="${j}" value="${esc(v)}" ${j>0&&j<4?'type="number" min="0" step="'+(j===1?'1':'0.01')+'"':''}></td>`).join('')}<td><button data-remove="${i}">刪除</button></td></tr>`).join('');update() }
function update(){const errors=validate(rows,$('approved').value);announce(errors.join('；'));$('export').disabled=$('print').disabled=errors.length>0;if(errors.length){$('summary').textContent='資料未完整：請修正後重新核對，不顯示舊總額。';return}const r=calculate(rows,$('approved').value);$('summary').textContent=`估算合計：${r.estimated.toFixed(2)} 元\\n實支合計：${r.actual.toFixed(2)} 元\\n較估算差異：${r.difference.toFixed(2)} 元\\n核定預算餘額：${r.remaining.toFixed(2)} 元${r.remaining<0?'（超支）':''}`;try{localStorage.setItem(key,JSON.stringify({approved:$('approved').value,rows}))}catch(e){announce('瀏覽器無法保存，請下載 JSON 備份')}}
$('rows').addEventListener('input',e=>{if(e.target.dataset.row!==undefined){rows[+e.target.dataset.row][+e.target.dataset.col]=e.target.value;update()}});
$('rows').addEventListener('click',e=>{if(e.target.dataset.remove!==undefined){rows.splice(+e.target.dataset.remove,1);render()}});
$('approved').oninput=update;$('add').onclick=()=>{rows.push(['',1,0,0,'']);render()};$('reset').onclick=()=>{rows=structuredClone(defaults);$('approved').value=30000;render()};
$('export').onclick=()=>{if(validate(rows,$('approved').value).length)return;const r=calculate(rows,$('approved').value);download('budget-report.csv',csvText([['項目','數量','單價','估算','實支','備註'],...rows.map(x=>[safeCell(x[0]),x[1],x[2],Number(x[1])*Number(x[2]),x[3],safeCell(x[4])]),['估算合計',r.estimated],['實支合計',r.actual],['較估算差異',r.difference],['核定預算',$('approved').value],['預算餘額',r.remaining]]),'text/csv;charset=utf-8')};
$('print').onclick=()=>{if(!validate(rows,$('approved').value).length)window.print()};$('backup').onclick=()=>download('budget-backup.json',JSON.stringify({approved:$('approved').value,rows},null,2),'application/json');
$('restore').onchange=async e=>{try{const d=JSON.parse(await e.target.files[0].text());const errors=validate(d.rows,d.approved);if(errors.length)throw Error(errors.join('；'));rows=d.rows;$('approved').value=d.approved;render()}catch(e){announce('還原失敗，保留目前資料：'+e.message)}};
$('import').onclick=()=>{try{const d=parseCSV($('csv').value);if(d.shift().join(',')!=='item,quantity,unit_price,actual,note')throw Error('欄位須為 item,quantity,unit_price,actual,note');const errors=validate(d,$('approved').value);if(errors.length)throw Error(errors.join('；'));rows=d;render()}catch(e){announce('匯入失敗，保留目前資料：'+e.message)}};
try{const d=JSON.parse(localStorage.getItem(key));if(d&&!validate(d.rows,d.approved).length){rows=d.rows;$('approved').value=d.approved}}catch(e){}render();
'''.replace('须','須'))

page('kpi-reference.html','部門 KPI 月報', '''<p class="note">離線參考成品。目標方向決定達標；上期變化只說明數字，不推論原因。更新前請保存來源。資料存在本機瀏覽器，可下載 JSON 備份。</p>
<div class="scroll"><table><thead><tr><th>指標</th><th>單位</th><th>方向</th><th>目標</th><th>實際</th><th>上期</th><th>期間</th><th>來源</th></tr></thead><tbody id="rows"></tbody></table></div>
<div class="actions"><button id="reset">載入標準資料</button><button id="add">新增指標</button><button id="export">下載月報 CSV</button><button id="print">列印／另存 PDF</button><button id="backup">備份 JSON</button><label>還原 JSON<input id="restore" type="file" accept=".json"></label></div><p id="error" class="error" role="status"></p><div id="summary" class="summary" aria-live="polite"></div>
<details class="import-box"><summary>貼上素材 CSV 匯入（取代目前指標）</summary><textarea id="csv" aria-label="KPI CSV"></textarea><button id="import">匯入 CSV</button></details>''', '''
const key='gemini-kpi-reference-v1';const defaults='''+json.dumps(kpis,ensure_ascii=False)+''';let rows=structuredClone(defaults);
function result(r){const target=number(r[3]),actual=number(r[4]),previous=number(r[5]);if(!['higher','lower'].includes(r[2]))return {status:'方向錯誤',change:null};const status=target===null||actual===null?'待確認':(r[2]==='higher'?actual>=target:actual<=target)?'已達標':'未達標';return {status,change:actual===null||previous===null||previous===0?null:(actual-previous)/previous*100}}
function valid(items){return Array.isArray(items)&&items.length>0&&items.every(r=>Array.isArray(r)&&r.length===8&&['higher','lower'].includes(r[2]))}
function render(){$('rows').innerHTML=rows.map((r,i)=>`<tr>${r.map((v,j)=>'<td>'+(j===2?`<select aria-label="第${i+1}列方向" data-row="${i}" data-col="2"><option value="higher" ${v==='higher'?'selected':''}>越大越好</option><option value="lower" ${v==='lower'?'selected':''}>越小越好</option></select>`:`<input aria-label="第${i+1}列${['指標','單位','方向','目標','實際','上期','期間','來源'][j]}" data-row="${i}" data-col="${j}" value="${esc(v)}" ${j>=3&&j<=5?'type="number" min="0" step="any"':''}>`)+'</td>').join('')}</tr>`).join('');update()}
function update(){const missing=rows.some(r=>!r[0]||!r[1]||!r[6]||!r[7]);announce(missing?'請補指標、單位、期間與來源；缺數值須在交付時註明待確認。':'');$('export').disabled=$('print').disabled=missing;$('summary').innerHTML=rows.map(r=>{const a=result(r),t=number(r[3]),v=number(r[4]);const ratio=t!==null&&t>0&&v!==null?Math.min(100,v/t*100):0;return `<section><h2>${esc(r[0])}：${a.status}</h2><p>${esc(r[6])}；來源：${esc(r[7])}。目標 ${esc(r[3])}／實際 ${esc(r[4])} ${esc(r[1])}；${r[2]==='higher'?'越大越好':'越小越好'}。</p><progress max="100" value="${ratio}" aria-label="${esc(r[0])}實際相對目標；非達標分數"></progress><p>較上期變化：${a.change===null?'不可計算（缺值或基期為零）':a.change.toFixed(1)+'%'}；圖條只呈現相對數值，達標以方向與目標判定。</p></section>`}).join('');try{localStorage.setItem(key,JSON.stringify(rows))}catch(e){announce('本機保存失敗，請下載備份')}}
$('rows').addEventListener('input',e=>{if(e.target.dataset.row!==undefined){rows[+e.target.dataset.row][+e.target.dataset.col]=e.target.value;update()}});$('reset').onclick=()=>{rows=structuredClone(defaults);render()};$('add').onclick=()=>{rows.push(['','件','higher','','','','2026-09','']);render()};
$('export').onclick=()=>{if($('export').disabled)return;download('kpi-monthly-report.csv',csvText([['指標','單位','方向','目標','實際','上期','期間','來源','狀態','較上期變化'],...rows.map(r=>[...r.map(safeCell),result(r).status,result(r).change===null?'不可計算':result(r).change.toFixed(1)+'%'])]),'text/csv;charset=utf-8')};$('print').onclick=()=>{if(!$('print').disabled)window.print()};
$('import').onclick=()=>{try{const d=parseCSV($('csv').value);if(d.shift().join(',')!=='metric,unit,direction,target,actual,previous,period,source'||!valid(d))throw Error('欄位或方向錯誤');if(d.some(r=>r.slice(3,6).some(v=>v!==''&&number(v)===null)))throw Error('數值不可為負或文字');rows=d;render()}catch(e){announce('匯入失敗，保留目前資料：'+e.message)}};
$('backup').onclick=()=>download('kpi-backup.json',JSON.stringify(rows,null,2),'application/json');$('restore').onchange=async e=>{try{const d=JSON.parse(await e.target.files[0].text());if(!valid(d)||d.some(r=>r.slice(3,6).some(v=>v!==''&&number(v)===null)))throw Error('JSON 格式或數值錯誤');rows=d;render()}catch(e){announce('還原失敗，保留目前資料：'+e.message)}};
try{const d=JSON.parse(localStorage.getItem(key));if(valid(d))rows=d}catch(e){}render();
''')

page('timer-reference.html','會議倒數計時器', '''<p class="note">暖身參考品。生成後應能在本機使用，不需要呼叫 AI。</p><label>會議主題<input id="topic" value="活動籌備"></label><label>秒數<input id="seconds" type="number" min="1" step="1" value="10"></label><div id="display" class="summary" role="status">10</div><div class="actions"><button id="start">開始</button><button id="pause">暫停</button><button id="reset">重設</button></div><p id="error" class="error" role="status"></p>''','''let left=10,tick=null;function paint(){$('display').textContent=$('topic').value+'：'+left+' 秒'+(left===0?'（時間到）':'')}function stop(){clearInterval(tick);tick=null}$('start').onclick=()=>{const n=number($('seconds').value);if(n===null||n<1||!Number.isInteger(n)){announce('請輸入正整數秒數');return}announce('');if(tick)return;if(left===0)left=n;tick=setInterval(()=>{left--;paint();if(left===0)stop()},1000)};$('pause').onclick=stop;$('reset').onclick=()=>{stop();const n=number($('seconds').value);if(n===null||n<1||!Number.isInteger(n)){announce('請輸入正整數秒數');return}left=n;announce('');paint()};$('seconds').oninput=()=>{stop();const n=number($('seconds').value);if(n!==null&&Number.isInteger(n)&&n>0){left=n;paint()}else announce('請輸入正整數秒數')};$('topic').oninput=paint;paint();''')

meeting_body='<p class="note">人工核對的固定答案，沒有呼叫 AI，也不能處理新的逐字稿。用於比較你的生成結果；學員需先讀原文、預判，再核對。</p>'
for name,txt in [('a',meeting_a),('b',meeting_b)]:
    meeting_body+=f'<h2>逐字稿 {name.upper()}</h2><pre>{html.escape(txt)}</pre><div class="scroll"><table><thead><tr><th>任務</th><th>負責人</th><th>期限</th><th>待確認</th><th>原文</th></tr></thead><tbody>'
    for r in answers['meeting_'+name]:meeting_body+='<tr>'+''.join(f'<td>{html.escape(str(r.get(k) or ("無" if k=="uncertain_reason" else "待確認")))}</td>' for k in ['task','owner','due_date','uncertain_reason','source_text'])+'</tr>'
    meeting_body+='</tbody></table></div>'
meeting_body+='<p>B 排除：場地已完成、問卷僅提議、邀請已取消。海報以王／2026-10-13 為準。所有有效交辦在人工核對前均未確認。</p>'
page('meeting-reference.html','會議交辦欄位答案',meeting_body)
print('素材與四個離線參考品已建立。')
