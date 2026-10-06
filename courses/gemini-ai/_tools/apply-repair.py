"""Contextual source edits selected by parsed DOM; keep untouched source bytes."""
from pathlib import Path
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import json,html,os
ROOT=Path(__file__).resolve().parents[1]
META=json.loads((ROOT/'_source/lesson-map.json').read_text());ROUTE=list(META)
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Boundary(HTMLParser):
    def __init__(self,source,tag):
        super().__init__(convert_charrefs=False);self.source=source;self.tag=tag;self.depth=0;self.end=None
        self.lines=[0]
        for line in source.splitlines(keepends=True):self.lines.append(self.lines[-1]+len(line))
    def handle_starttag(self,tag,attrs):
        if tag==self.tag:self.depth+=1
    def handle_endtag(self,tag):
        if tag==self.tag:
            self.depth-=1
            if self.depth==0 and self.end is None:
                line,col=self.getpos();i=self.lines[line-1]+col;self.end=self.source.index('>',i)+1
def span(raw,node):
    start=sum(len(x) for x in raw.splitlines(keepends=True)[:node.sourceline-1])+node.sourcepos
    tail=raw[start:]
    if node.name in VOID:return start,start+tail.index('>')+1
    parser=Boundary(tail,node.name);parser.feed(tail);assert parser.end is not None,node.name
    return start,start+parser.end
def replace(raw,selector,make,index=None):
    soup=BeautifulSoup(raw,'html.parser');nodes=soup.select(selector)
    if index is None:assert len(nodes)==1,(selector,len(nodes));node=nodes[0]
    else:node=nodes[index]
    a,b=span(raw,node);return raw[:a]+make(raw[a:b],node)+raw[b:]
def inner(raw,selector,text):
    return replace(raw,selector,lambda old,node:old[:old.index('>')+1]+text+old[old.rfind('</'):])
def attrs(raw,selector,changes):
    def make(old,node):
        for k,v in changes.items():node[k]=v
        # Serialize only the selected opening tag; keep original inner source.
        values=[]
        for k,v in sorted(node.attrs.items(),key=lambda kv:kv[0]=='content'):
            if isinstance(v,list):v=' '.join(v)
            values.append(k+'="'+html.escape(str(v),quote=True)+'"')
        opening='<'+node.name+' '+ ' '.join(values)+'>'
        return opening+old[old.index('>')+1:]
    return replace(raw,selector,make)
CSS='''.lesson-section{scroll-margin-top:90px}.lesson-body pre{max-width:100%;overflow-wrap:anywhere;white-space:pre-wrap}.lesson-body details{border-top:1px solid var(--c-border);padding:16px 0;margin:20px 0}.lesson-body summary{cursor:pointer;font-weight:600}.lesson-body li{margin-bottom:12px}.lesson-body a{overflow-wrap:anywhere}.lesson-body table{max-width:100%}.lesson-body .core-route{font-size:.85rem;color:var(--c-muted);margin-bottom:28px}.lesson-title{overflow-wrap:anywhere}.core-table-scroll{max-width:100%;overflow:auto}'''
COPYJS='''document.querySelectorAll('[data-copy]').forEach(btn=>btn.addEventListener('click',async()=>{const id=btn.dataset.copy;const text=document.getElementById(id).textContent;const status=document.querySelector('[data-copy-status="'+id+'"]');try{await navigator.clipboard.writeText(text);status.textContent='已複製，請貼到對應的生成輸入框。'}catch(e){status.textContent='無法自動複製；請選取下方完整指令，按 Ctrl+C／Cmd+C。'}}));'''
def extra_style(raw):
    return replace(raw,'head > style',lambda old,node:old[:-8]+CSS+'</style>',0)
def nav(raw,file):
    i=ROUTE.index(file);links=[]
    for target,label,cls in [(ROUTE[i-1] if i else 'index.html','上一站','nav-prev'),(ROUTE[i+1] if i+1<len(ROUTE) else 'index.html','下一站' if i+1<len(ROUTE) else '完成自檢，返回目錄','nav-next next')]:
        rel=os.path.relpath(target,Path(file).parent)
        title=META[target]['title'] if target in META else '課程成果清單'
        links.append(f'<a class="nav-btn {cls}" data-nav-role="{"next" if "next" in cls else "prev"}" href="{rel}"><div><div class="nav-btn-label">{label}</div><div class="nav-btn-title">{title}</div></div></a>')
    return inner(raw,'.lesson-nav','\n'+''.join(links)+'\n')

OPTIONAL={
'part1/PRAC1-1.html':'支援需求整理；直接使用組合台填一次需求，再回主案例，不必自建組合台。',
'part1/PRAC1-2.html':'支援需求缺口查核；關鍵字分數不能當作工具品質，請用一筆已知答案測生成結果。',
'part1/PRAC1-3.html':'支援會議欄位規格；在 AI 交辦前確認任務、原文與待確認欄，不把模板當提取成果。',
'part2/CH2-2.html':'延伸排班與規則轉換；選一項冲突或無解情境核對，不必在完成預算前另建工具。',
'part2/CH2-3.html':'延伸介面調整；在已完成工具上選一種風格，重跑原測試，確認功能沒有改變。',
'part2/PRAC2-2.html':'延伸跨時區排會；選日期及會議長度，確認完整區間都在工作時間。此簡版只使用預設工作時段，沒有取得真實出席確認。',
'part2/PRAC2-3.html':'支援既有工具的色彩；在實際表單與錯誤狀態中核對辨識度，不另做必修配色產品。',
'part3/CH3-1.html':'延伸圖表形式；先從 KPI 的數字與方向出發，選能支持判讀的圖，不要求學 SVG 座標。',
'part3/CH3-2.html':'延伸專案流程；用節點與前置關係找一個流程阻塞，與日期時程的判斷分開。',
'part3/CH3-3.html':'延伸漏斗分析；核對每層的母數與轉換率，再寫一項需要調查的流失點。',
'part3/PRAC3-1.html':'延伸訓練前後比較；每個分數寫出行為證據與下一項行動，不用漂亮形狀替代判斷。',
'part3/PRAC3-2.html':'延伸活動時程；新增負責人與前置任務，檢查一項延期影響，而不只換圖表樣式。',
'part4/CH4-2.html':'支援指令保存；直接整理本課生成與修復指令，附輸入、答案與版本，不必另建 Prompt 管理器。',
'part4/CH4-3.html':'延伸限時挑戰方法；時間由講師調節，以需求變更、測試與交付證據驗收。必修終點在獨立改造站。',
'part4/PRAC4-1.html':'支援成果查核；用這份清單驗收已完成工具，不要求再生成一個清單工具才能完課。',
'part4/PRAC4-2.html':'延伸指令資料庫；學員需知道資料保存與還原，不以 CRUD 程式術語作學習目標。',
'part5/PRAC5-1.html':'延伸郵件草稿；提供目的、對象、時間與所需行動，寄出前核對。此工具是固定模板，沒有執行語意模型。',
'part5/PRAC5-2.html':'延伸關鍵字篩選；本頁只找特定字句，不能分辨取消或提議。需要語意交辦時，回必修 AI 交辦並核對原文。',
'part5/PRAC5-3.html':'延伸廣告連結；核對既有參數、片段與重複 UTM，產出可追蹤連結。',
'part5/PRAC5-4.html':'延伸公告預覽；核對時間、地點、對象與報名方式。預覽是近似示意，不保證平台實際呈現相同。',
'part5/PRAC5-5.html':'延伸進度判讀；每個紅燈補阻礙、負責人與下一步，顏色本身不是處理進度。',
'part5/PRAC5-6.html':'延伸選項比較；先定義評分證據與權重，由人做決策，不把總分當自動錄用結論。',
'part5/PRAC5-7.html':'延伸會議暖身；用抽籤分配發言順序，確認名單沒有重複，毋須升級為主專案。',
'part5/PRAC5-8.html':'延伸成果報告；把已核對的預算或 KPI 資料貼入 Markdown，補摘要、問題與決策，列印成 PDF；不需理解 DOM 或解析程式。',
'part5/PRAC5-9.html':'延伸活動準備度；倒數旁應記未完成項與責任人，時間歸零不代表任務完成。',
'part5/PRAC5-10.html':'延伸文字規則掃描；未命中只表示未命中本次關鍵字規則，不保證內容安全或合規。',
'part5/PRAC5-11.html':'延伸團隊可用性；未知保持未確認，任一人忙碌都不能宣稱全員可用。',
'part5/PRAC5-12.html':'獨立改造選項：行政案件期限追蹤。先增加責任人、期限與下一步，再測逾期、近期、未知、備份與還原。',
'part6/CH6-2.html':'延伸分享與公開發布；先完成 A/B 語意測試，再按目前官方說明確認權限與可能費用，發布不是必修完課條件。',
'part6/CH6-3.html':'延伸 GitHub 與其他部署；只在成果可用且需要公開服務時進入。舊版平台與費率流程須依當時官方文件重查。'}

for file in sorted([str(p.relative_to(ROOT)) for p in ROOT.glob('part*/*.html')]):
    path=ROOT/file;raw=path.read_text();s=BeautifulSoup(raw,'html.parser');body=s.select_one('.lesson-body')
    assert body and len(s.select('.lesson-body'))==1
    assert not body.select('#core-route-banner'), 'Do not apply twice'
    if file in META:
        d=META[file];i=ROUTE.index(file)
        fragment=(ROOT/'_source/fragments'/d['fragment']).read_text()
        def modify(old,node):
            opening=old[:old.index('>')+1];inside=old[old.index('>')+1:old.rfind('</')]
            return opening+f'<p class="core-route" id="core-route-banner">必修 {i+1}／{len(ROUTE)} · <a href="../index.html#required-route">路線與成果自檢</a> · 本頁上方為正式步驟，下方保留原有延伸。</p>'+fragment+'<details id="legacy-reference"><summary>原有章節延伸（需要時展開；操作與驗收依上方正文）</summary>'+inside+'</details>'+old[old.rfind('</'):]
        raw=replace(raw,'.lesson-body',modify)
        raw=inner(raw,'.lesson-hero .lesson-title',html.escape(d['title']))
        raw=inner(raw,'.lesson-tagline',html.escape(d['tagline']))
        raw=inner(raw,'.outcomes','<div class="outcomes-label">本次成果</div>'+''.join('<div class="outcome-item"><div class="outcome-dot"></div><span>'+html.escape(x)+'</span></div>' for x in d['outcomes']))
        raw=inner(raw,'title',html.escape(d['title']+'｜Gemini AI 實戰課'))
        for selector in ['meta[name="description"]','meta[property="og:description"]','meta[name="twitter:description"]']:
            if BeautifulSoup(raw,'html.parser').select_one(selector):raw=attrs(raw,selector,{'content':d['tagline']})
        for selector in ['meta[property="og:title"]','meta[name="twitter:title"]']:
            if BeautifulSoup(raw,'html.parser').select_one(selector):raw=attrs(raw,selector,{'content':d['title']+'｜Gemini AI 實戰課'})
        raw=nav(raw,file)
        raw=replace(raw,'body',lambda old,node:old[:-7]+'<script>'+COPYJS+'</script>\n</body>')
        # Dots represent required content only, not collapsed legacy sections.
        for n in BeautifulSoup(raw,'html.parser').select('script'):
            if "const sections = Array.from(document.querySelectorAll('.lesson-section'))" in n.get_text():
                a,b=span(raw,n);raw=raw[:a]+raw[a:b].replace("querySelectorAll('.lesson-section')","querySelectorAll('.lesson-body > .lesson-section')")+raw[b:];break
    else:
        text=OPTIONAL[file].replace('冲','衝')
        addition=f'<section class="lesson-section" id="core-route-banner"><h2 class="section-heading">選修用途與學員判斷</h2><p class="body-text">{text}</p><p class="body-text">前段單檔生成沿用 AI Studio 對話；原有 Canvas 操作屬延伸替代路徑，不是本課必修切換。<a href="../index.html#required-route">返回必修路線與成果自檢</a>。完整原文與生成指令保留於下方。</p></section>'
        if file=='part5/PRAC5-12.html':
            addition+='<section class="lesson-section" id="case-upgrade"><h2 class="section-heading">行政案件：期限與備份改造</h2><p class="body-text">下載 <a href="../assets/materials/cases.csv" download>案件資料 CSV</a> 與 <a href="../assets/materials/prompt-cases.txt" download>完整改造指令</a>，加入責任人、期限、阻礙與下一步。原有 Kanban 可作起點，這些期限與匯入功能需要依指令生成，不能假定原示範已具備。</p><p class="body-text">截至日設 2026-10-06：A01 近期、A02 期限待確認、A03 逾期、A04 完成。A03 改完成後逾期數減一；重複匯入 A01 不得增生第二案。備份 JSON、重開並還原，核對責任人與日期。資料僅在此瀏覽器保存，不代表多人同步或關閉後通知。</p></section>'
        if file in ['part6/CH6-2.html','part6/CH6-3.html']:
            addition+='<p class="body-text"><a href="https://ai.google.dev/gemini-api/docs/aistudio-build-mode" target="_blank" rel="noopener">先查官方 Build 分享與部署說明</a>；本課不保證公開服務全程免費。</p>'
            # body-text stays inside body, immediately after the identified section.
        def modify(old,node):
            a=old.index('>')+1;b=old.rfind('</')
            return old[:a]+addition+'<details id="legacy-reference"><summary>開啟此選修的完整操作與示範</summary>'+old[a:b]+'</details>'+old[b:]
        raw=replace(raw,'.lesson-body',modify)
        raw=attrs(raw,'.lesson-hero',{'data-learning-role':'optional'})
    raw=extra_style(raw)
    path.write_text(raw)

# Overview: required route first, preserve the old catalog as a branch.
file='index.html';path=ROOT/file;raw=path.read_text()
raw=inner(raw,'.hero-desc','從零開始，用預算、KPI 與 AI 會議交辦完成工作成果。每案練習核對、修正、保存與交付；其他工具依工作需要選修。')
for i,(value,label) in enumerate([('10','必修站點'),('3','工作主案例'),('6h','參考時數')]):
    raw=inner(raw,f'.hero-stats .stat:nth-of-type({i+1}) .stat-num',value)
    raw=inner(raw,f'.hero-stats .stat:nth-of-type({i+1}) .stat-lbl',label)
raw=inner(raw,'.prog-label','必修成果自檢')
raw=inner(raw,'.prog-pct','0 / 10')
raw=attrs(raw,'.prog-pct',{'id':'core-progress-count'})
raw=attrs(raw,'.prog-fill',{'id':'core-progress-fill'})
route='<section id="required-route"><h2 class="section-title">必修路線：完成工作成果</h2><p class="body-text">依序走 10 站。勾選前核對該站的完成證據；捲動閱讀不會自動完課。勾選只保存在本機瀏覽器，不是講師評分。原有 40 頁全部保留在下方章節資料庫。</p><ol class="core-route-list">'
evidence=['看過計時器並完成帳號與資料夾準備','需求單包含一項變更與驗收方式','自製計時器已測正常／例外並重開','手算估算、差異與核定餘額','自製預算工具通過查核、修復與匯出','KPI 方向與缺值已測，月報可更新','已判斷 A 的有效交辦與排除項','AI 應用已實測 A/B，核對並保存結果','工具／資料／指令／報告已保存並重開','獨立改造、再測與完整交付完成']
for i,(file,d) in enumerate(META.items()):
    route+=f'<li><a href="{file}">{i+1}. {d["title"]}</a><label><input type="checkbox" data-core-complete="{file}"> {evidence[i]}</label></li>'
route+='</ol><p class="body-text"><a href="assets/materials/materials.zip" download>下載完整素材包 ZIP</a> · <a href="assets/materials/README.md">材料用途與對應單元</a>。下載受限時，各站也有逐檔連結與可閱讀答案。6 小時是安排假設，講師應保留核對、修復與獨立操作時間。</p></section>'
def overview(old,node):
    a=old.index('>')+1;b=old.rfind('</');inside=old[a:b]
    # Extract exact progress node from this main context, then keep old catalog.
    s=BeautifulSoup(inside,'html.parser');prog=s.select_one('.progress-bar-wrap');x,y=span(inside,prog)
    progress=inside[x:y];catalog=inside[:x]+inside[y:]
    return old[:a]+progress+route+'<details id="optional-catalog"><summary>章節資料庫：必修參照與選修延伸</summary>'+catalog+'</details>'+old[b:]
raw=replace(raw,'main.section',overview)
for n in BeautifulSoup(raw,'html.parser').select('#optional-catalog .part-count'):
    a,b=span(raw,n);raw=raw[:a]+raw[a:b].replace(n.get_text(),'含延伸')+raw[b:]
for f,d in META.items():
    s=BeautifulSoup(raw,'html.parser');a=s.select_one(f'#optional-catalog a[href="{f}"]')
    if a:
        for cls in ['.lesson-title','.prac-title']:
            if a.select_one(cls):raw=inner(raw,f'#optional-catalog a[href="{f}"] {cls}',html.escape(d['title'])+' · 必修')
# The legacy deployment promise is replaced in its identified paragraph.
s=BeautifulSoup(raw,'html.parser')
for n in s.select('#optional-catalog p'):
    if '全程走免費路線' in n.get_text():
        a,b=span(raw,n);raw=raw[:a]+str(n).replace(n.get_text(),'AI 交辦生成與查核在必修；分享、公開發布與其他部署為延伸，使用前確認平台權限、額度與費用。')+raw[b:];break
for sel in ['#optional-catalog a[href="part6/CH6-2.html"] .lesson-title']:
    raw=inner(raw,sel,'選修：分享與公開發布（先確認權限與費用）')
INDEXCSS='''.core-route-list{padding-left:24px;margin:24px 0}.core-route-list li{padding:12px 0;border-bottom:1px solid var(--c-border)}.core-route-list a{color:var(--c-text);font-weight:600}.core-route-list label{display:block;font-size:.85rem;color:var(--c-muted);margin-top:8px}.core-route-list input{margin-right:8px}#optional-catalog{margin-top:40px}#optional-catalog>summary{cursor:pointer;font-weight:600;margin-bottom:24px}#required-route{scroll-margin-top:90px}#required-route p{font-size:.9rem;line-height:1.9;overflow-wrap:anywhere}'''
raw=replace(raw,'head > style',lambda old,node:old[:-8]+INDEXCSS+'</style>',0)
INDEXJS='''const coreKey='gemini-ai-core-evidence-v1';let completed={};try{completed=JSON.parse(localStorage.getItem(coreKey))||{}}catch(e){}const boxes=[...document.querySelectorAll('[data-core-complete]')];function refreshCore(){const n=boxes.filter(b=>b.checked).length;document.getElementById('core-progress-count').textContent=n+' / '+boxes.length;document.getElementById('core-progress-fill').style.width=n/boxes.length*100+'%'}boxes.forEach(b=>{b.checked=completed[b.dataset.coreComplete]===true;b.addEventListener('change',()=>{completed[b.dataset.coreComplete]=b.checked;try{localStorage.setItem(coreKey,JSON.stringify(completed))}catch(e){}refreshCore()})});refreshCore();'''
raw=replace(raw,'body',lambda old,node:old[:-7]+'<script>'+INDEXJS+'</script>\n</body>')
path.write_text(raw)
print('已修補 40 個學習頁與總覽，原正文保留，必修導航 10 站。')
