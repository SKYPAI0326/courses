from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
ns={'__file__':str(ROOT/'_tools/apply-repair.py')}
exec((ROOT/'_tools/apply-repair.py').read_text().split('for file in sorted(')[0],ns)
replace=ns['replace'];span=ns['span'];inner=ns['inner']
def script_patch(raw,marker,fn):
    s=BeautifulSoup(raw,'html.parser');nodes=[n for n in s.select('script') if marker in n.get_text()];assert len(nodes)==1
    n=nodes[0];a,b=span(raw,n);return raw[:a]+fn(raw[a:b])+raw[b:]
def once(s,a,b):assert s.count(a)==1,(a,s.count(a));return s.replace(a,b,1)
def paragraph(raw,selector,marker,text):
    nodes=[n for n in BeautifulSoup(raw,'html.parser').select(selector) if marker in n.get_text()];assert len(nodes)==1,(marker,len(nodes))
    n=nodes[0];a,b=span(raw,n);old=raw[a:b];return raw[:a]+old[:old.index('>')+1]+text+old[old.rfind('</'):]+raw[b:]

p=ROOT/'part2/PRAC2-2.html';raw=p.read_text()
raw=replace(raw,'#tz-list',lambda old,node:'<label class="body-text">台北起始日期<input class="tz-name-input" type="date" id="meeting-date" value="2026-10-06"></label><label class="body-text">會議長度（分鐘）<input class="tz-name-input" type="number" id="meeting-duration" min="1" max="480" step="1" value="60"></label>'+old)
def tzscript(s):
    a=s.index('const TZ_LIST =');b=s.index('let rowId',a)
    s=s[:a]+'''const TZ_LIST = [
{name:'台北',zone:'Asia/Taipei'},{name:'東京',zone:'Asia/Tokyo'},{name:'新加坡',zone:'Asia/Singapore'},
{name:'首爾',zone:'Asia/Seoul'},{name:'上海',zone:'Asia/Shanghai'},{name:'香港',zone:'Asia/Hong_Kong'},
{name:'雪梨',zone:'Australia/Sydney'},{name:'倫敦',zone:'Europe/London'},{name:'巴黎',zone:'Europe/Paris'},
{name:'紐約',zone:'America/New_York'},{name:'洛杉磯',zone:'America/Los_Angeles'},{name:'芝加哥',zone:'America/Chicago'}];
function tzEscape(v){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
''' + s[b:]
    s=once(s,'${t.name} (UTC${t.offset >= 0 ? \'+\' : \'\'}${t.offset})','${t.name} (${t.zone})')
    a=s.index('function calcTimezone()');b=s.index('function copyInstructions()',a)
    s=s[:a]+'''function zonedParts(date,zone){const parts=new Intl.DateTimeFormat('en-GB',{timeZone:zone,year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(date);return Object.fromEntries(parts.map(p=>[p.type,p.value]))}
function intervalInWork(start,end,zone){const a=zonedParts(start,zone),b=zonedParts(end,zone);const same=a.year===b.year&&a.month===b.month&&a.day===b.day;return same&&Number(a.hour)*60+Number(a.minute)>=540&&Number(b.hour)*60+Number(b.minute)<=1080}
function calcTimezone(){
 const rows=[...document.querySelectorAll('[id^="tzrow-"]')];
 const date=document.getElementById('meeting-date').value,duration=Number(document.getElementById('meeting-duration').value);
 if(rows.length<2||!date||!Number.isInteger(duration)||duration<1||duration>480){alert('請選日期、至少兩城市及1–480整數分鐘');return}
 const selected=rows.map(row=>{const id=row.id.replace('tzrow-',''),idx=Number(document.getElementById('tzsel-'+id).value);return {...TZ_LIST[idx],label:document.getElementById('tzlabel-'+id).value.trim()||TZ_LIST[idx].name}});
 let html='<p>依各地 09:00–18:00 工作時間篩選，尚未取得出席者實際確認。</p><div class="table-scroll"><table class="time-table"><thead><tr><th>台北起始</th>'+selected.map(t=>'<th>'+tzEscape(t.label)+'<br>'+t.zone+'</th>').join('')+'</tr></thead><tbody>';let feasible=0;
 for(let h=0;h<24;h++){const start=new Date(date+'T'+String(h).padStart(2,'0')+':00:00+08:00'),end=new Date(start.getTime()+duration*60000);const ok=selected.every(t=>intervalInWork(start,end,t.zone));if(ok)feasible++;html+='<tr><td>'+String(h).padStart(2,'0')+':00</td>'+selected.map(t=>{const a=zonedParts(start,t.zone),b=zonedParts(end,t.zone);return '<td class="'+(ok?'time-cell-ok':'time-cell-bad')+'">'+a.month+'/'+a.day+' '+a.hour+':'+a.minute+'–'+b.hour+':'+b.minute+'</td>'}).join('')+'</tr>'}
 html+='</tbody></table></div><p>'+(feasible?'找到 '+feasible+' 個整點候選；請再向出席者確認。':'沒有符合所有城市完整工作區間的整點候選；改日期、長度或時段再查。')+'</p>';document.getElementById('time-table-wrap').innerHTML=html;document.getElementById('time-grid').style.display='block';
}
''' +s[b:];return s
raw=script_patch(raw,'const TZ_LIST',tzscript)
raw=paragraph(raw,'.tz-legend span','所有人皆可開會','全區間符合工作時間，出席仍待確認')
raw=inner(raw,'#instruction-box','製作單檔跨時區候選時段工具：選台北日期、會議長度、城市與 IANA 時區，使用 Intl.DateTimeFormat 依選定日期處理夏令時間。完整起訖區間須落在各地 09:00–18:00，跨日期或超出時間不列可用；沒有候選要明示。顯示当地日期與起訖時間，標明這只是工作時間候選，未取得出席者確認。不要使用固定 UTC 偏移，也不要把起始時間合格當作全區間合格。'.replace('当地','當地'))
p.write_text(raw)

p=ROOT/'part5/PRAC5-11.html';raw=p.read_text()
raw=paragraph(raw,'.body-text','每位成員可以獨立','每位成員標記自己每一時段的忙碌程度；未填保持「未確認」。整體視圖以任何忙碌優先，再處理未知，只有全員明確空閒才顯示空閒。資料只保存在目前瀏覽器。')
raw=paragraph(raw,'.callout-body','點擊格子可循環','點擊循環：未確認→空閒→稍忙→忙碌→非常忙→未確認。新增成員或清空資料都回未確認；不可把沒填當作空閒。')
raw=paragraph(raw,'.callout-body','整體熱度是','整體視圖只能讀取。任一成員忙碌便不列全員空閒；沒有人忙碌但有人未填，顯示未確認。全員填空閒才可作候選，仍需確認會議長度與實際出席。')
raw=replace(raw,'.heat-legend',lambda old,node:old[:-6]+'<span>未確認：尚未填資料</span></div>')
raw=inner(raw,'#instruction-box','製作單檔團隊可用性表。成員與時段資料只存目前瀏覽器。空白狀態為未確認；點擊在未確認、空閒、稍忙、忙碌、非常忙間循環。整體取任一忙碌的最大值；沒人忙但有人未知則未確認；只有全員明確空閒才列候選，不取平均。顯示文字提示，不只顏色。清空回未知，新增成員也未知；不宣稱取得日曆權限或全員已確認出席。')
def heatscript(s):
    a=s.index('function getOverallValue(');b=s.index('function renderTable()',a)
    s=s[:a]+'''function memberValue(m,d,h){const v=(data[m]||{})[`${d}-${h}`];return Number.isInteger(v)&&v>=0&&v<=3?v:4}
function getOverallValue(d,h){const values=members.map(m=>memberValue(m,d,h));const busy=values.filter(v=>v>0&&v<4);if(busy.length)return Math.max(...busy);return values.includes(4)?4:0}
''' +s[b:]
    s=once(s,"((data[currentMember]||{})[`${d}-${h}`]||0)","memberValue(currentMember,d,h)")
    s=once(s,"['空閒','稍忙','忙碌','非常忙'][val]","['空閒','稍忙','忙碌','非常忙','未確認'][val]")
    s=once(s,'data[currentMember][key] = ((data[currentMember][key]||0) + 1) % 4;','data[currentMember][key] = (memberValue(currentMember,d,h) + 1) % 5;')
    return s
raw=script_patch(raw,'function getOverallValue',heatscript)
raw=replace(raw,'head > style',lambda old,node:old[:-8]+'.heat-4{background:#edeae3;border:1px dashed #7a766d}'+'</style>',0)
p.write_text(raw)

p=ROOT/'part5/PRAC5-3.html';raw=p.read_text()
def utmscript(s):
    a=s.index("  let url = base +");b=s.index("  document.getElementById('utm-url')",a)
    return s[:a]+'''  let parsed;
  try{parsed=new URL(base);if(!['https:','http:'].includes(parsed.protocol))throw Error('protocol')}catch(e){alert('請輸入完整 http／https 網址');return}
  parsed.searchParams.set('utm_source',source);parsed.searchParams.set('utm_campaign',campaign);
  if(medium)parsed.searchParams.set('utm_medium',medium);else parsed.searchParams.delete('utm_medium');
  if(content)parsed.searchParams.set('utm_content',content);else parsed.searchParams.delete('utm_content');
  const url=parsed.toString();
''' +s[b:]
raw=script_patch(raw,'function generateUTM()',utmscript)
raw=replace(raw,'#instruction-box',lambda old,node:old[:old.rfind('</')]+ '\n網址以 URL 與 searchParams 處理，保留原有參數與片段；set 更新同名 UTM，避免重複，選填欄空白應移除旧值。'+old[old.rfind('</'):])
p.write_text(raw.replace('移除旧值','移除舊值'))

# Old interactive KPI remains accessible; it must also handle direction/unknown.
p=ROOT/'part3/PRAC3-3.html';raw=p.read_text()
def kpiscript(s):
    s=once(s,"unit=''", "unit='', direction='higher'")
    s=once(s,'    <button class="kpi-remove"', '<select class="kpi-input" id="kdir-${id}" aria-label="指標方向"><option value="higher" ${direction===\'higher\'?\'selected\':\'\'}>越大越好</option><option value="lower" ${direction===\'lower\'?\'selected\':\'\'}>越小越好</option></select>\n    <button class="kpi-remove"')
    s=once(s,"  const kpis = [];","  const readNumber=id=>{const v=document.getElementById(id)?.value;const n=Number(v);return v!==''&&Number.isFinite(n)&&n>=0?n:null};\n  const kpis = [];")
    s=once(s,"parseFloat(document.getElementById('ktarget-' + id)?.value) || 0","readNumber('ktarget-'+id)")
    s=once(s,"parseFloat(document.getElementById('kactual-' + id)?.value) || 0","readNumber('kactual-'+id)")
    s=once(s,"unit: document.getElementById('kunit-' + id)?.value.trim() || ''","direction:document.getElementById('kdir-'+id).value,\n      unit: document.getElementById('kunit-' + id)?.value.trim() || ''")
    a=s.index('    const rate =');b=s.index('    return `<div class="kpi-card">',a)
    s=s[:a]+'''    const known=k.actual!==null&&k.target!==null;
    const ok=known&&(k.direction==='lower'?k.actual<=k.target:k.actual>=k.target);
    const rate=known&&k.target>0?k.actual/k.target*100:null;
    const pct=rate===null?0:Math.min(100,rate);
    const color=ok?'var(--c-a3)':'var(--c-a2)',badge=known?(ok?'已達標':'未達標'):'待確認',barColor=ok?'#5a7a5a':'#c9963a',badgeClass=ok?'badge-ok':'badge-warn';
''' +s[b:]
    s=once(s,'${k.actual.toLocaleString()}','${k.actual===null?\'待確認\':k.actual.toLocaleString()}')
    s=once(s,'${k.target.toLocaleString()}','${k.target===null?\'待確認\':k.target.toLocaleString()}')
    s=once(s,'${rate.toFixed(1)}%','${rate===null?\'不計比值\':rate.toFixed(1)+\'%\'}（${k.direction===\'lower\'?\'越小越好\':\'越大越好\'}）')
    return s
raw=script_patch(raw,'function renderDashboard()',kpiscript)
raw=replace(raw,'head > style',lambda old,node:old[:-8]+'.kpi-input-row{grid-template-columns:2fr 1fr 1fr 1fr 1.5fr auto}.kpi-input{min-width:0}@media(max-width:768px){.kpi-input-row{grid-template-columns:1fr 1fr}.kpi-input-row>*{max-width:100%}}'+'</style>',0)
raw=replace(raw,'#instruction-box',lambda old,node:old[:old.rfind('</')]+ '\n增加每個指標的方向：越大越好 actual>=target；越小越好 actual<=target。缺值不可當零，顯示待確認；零目標不計比值，但依方向判達標。圖條只是相對值，不以百分比統一判所有方向。'+old[old.rfind('</'):])
p.write_text(raw)
print('已修正時區／全區間、熱點未知／最大忙碌、UTM 結構與原 KPI 方向。')
