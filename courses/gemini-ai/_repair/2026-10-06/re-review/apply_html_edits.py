"""Apply guarded parser-context course page edits for the 2026-10-06 review."""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import html, json, os, re

ROOT=Path(__file__).resolve().parents[3]
META=json.loads((ROOT/'_source/lesson-map.json').read_text())
ROUTE=list(META)
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Boundary(HTMLParser):
    def __init__(self,source,tag):
        super().__init__(convert_charrefs=False); self.source=source; self.tag=tag; self.depth=0; self.end=None
        self.lines=[0]
        for line in source.splitlines(keepends=True): self.lines.append(self.lines[-1]+len(line))
    def handle_starttag(self,tag,attrs):
        if tag==self.tag: self.depth+=1
    def handle_endtag(self,tag):
        if tag==self.tag:
            self.depth-=1
            if self.depth==0 and self.end is None:
                line,col=self.getpos(); i=self.lines[line-1]+col; self.end=self.source.index('>',i)+1

def span(raw,node):
    start=sum(len(x) for x in raw.splitlines(keepends=True)[:node.sourceline-1])+node.sourcepos
    tail=raw[start:]
    if node.name in VOID: return start,start+tail.index('>')+1
    parser=Boundary(tail,node.name); parser.feed(tail); assert parser.end is not None,node.name
    return start,start+parser.end

def replace_node(raw,node,make):
    a,b=span(raw,node); return raw[:a]+make(raw[a:b],node)+raw[b:]

def replace(raw,selector,make):
    soup=BeautifulSoup(raw,'html.parser'); nodes=soup.select(selector)
    assert len(nodes)==1,(selector,len(nodes))
    return replace_node(raw,nodes[0],make)

def inner(raw,selector,text):
    return replace(raw,selector,lambda old,node:old[:old.index('>')+1]+text+old[old.rfind('</'):])

def attrs(raw,selector,changes):
    def make(old,node):
        for k,v in changes.items(): node[k]=v
        values=[]
        for k,v in sorted(node.attrs.items(),key=lambda kv:kv[0]=='content'):
            if v is True: values.append(k); continue
            if isinstance(v,list): v=' '.join(v)
            values.append(k+'="'+html.escape(str(v),quote=True)+'"')
        return '<'+node.name+' '+' '.join(values)+'>'+old[old.index('>')+1:]
    return replace(raw,selector,make)

def after(raw,selector,addition):
    return replace(raw,selector,lambda old,node:old+addition)

def map_rows():
    text=(ROOT/'_source/CURRICULUM-MAP.md').read_text()
    block=text.split('## 全部 40 單元：用途、先修與交付',1)[1].split('## 已識別的內容銜接與待修缺口',1)[0]
    rows={}
    for line in block.splitlines():
        if not line.startswith('| [`'): continue
        cells=line.split('|')
        path_match=re.search(r'`(part[1-6]/[^`]+\.html)`',cells[1])
        if not path_match: continue
        role_match=re.match(r'\s*(核心|延伸|參考)：',cells[2])
        assert role_match,(path_match.group(1),cells[2])
        rows[path_match.group(1)]={'role':role_match.group(1),'guidance':cells[3].strip()}
    assert set(rows)=={p.relative_to(ROOT).as_posix() for p in ROOT.glob('part*/*.html')},'curriculum map must map all 40 lessons'
    return rows

ROWS=map_rows()
CORE_BRIDGES={
'part1/CH1-1.html':'從工作需求開始；準備需求單與測試起點。',
'part1/CH1-2.html':'沿用計時器需求，補輸入、規則、例外、輸出與驗收。',
'part1/CH1-3.html':'把可核對規格交給模型，生成、保存、測試並重開。',
'part2/CH2-1.html':'先手算四筆活動資料，為後續工具留下已知答案。',
'part2/PRAC2-1.html':'接續手算基準，生成預算工具並用同一批資料驗算。',
'part3/PRAC3-3.html':'從固定計算進到資料方向與缺值判斷；下一站開始讀懂會議原文。',
'part6/CH6-1.html':'沿用已知答案方法，但這次要辨識提議、取消和未知。',
'part6/PRAC6-1.html':'在 Build 預覽實測 A/B，核對原文並修復語意錯誤。',
'part4/CH4-1.html':'把已驗收工具、資料、完整指令、報告及驗收證據放進同一交付包。',
'part4/PRAC4-3.html':'從預算、KPI、會議案例擇一增加新規則，回歸測試後獨立交付。'}
NEAREST_CORE={
'part1/PRAC1-1.html':'part1/CH1-2.html','part1/PRAC1-2.html':'part1/CH1-2.html','part1/PRAC1-3.html':'part1/CH1-2.html',
'part2/CH2-2.html':'part2/CH2-1.html','part2/CH2-3.html':'part2/PRAC2-1.html','part2/PRAC2-2.html':'part2/CH2-1.html','part2/PRAC2-3.html':'part2/PRAC2-1.html',
'part3/CH3-1.html':'part3/PRAC3-3.html','part3/CH3-2.html':'part3/PRAC3-3.html','part3/CH3-3.html':'part3/PRAC3-3.html','part3/PRAC3-1.html':'part3/PRAC3-3.html','part3/PRAC3-2.html':'part3/PRAC3-3.html',
'part4/CH4-2.html':'part4/CH4-1.html','part4/CH4-3.html':'part4/PRAC4-3.html','part4/PRAC4-1.html':'part4/CH4-1.html','part4/PRAC4-2.html':'part4/CH4-1.html',
'part5/PRAC5-1.html':'part4/PRAC4-3.html','part5/PRAC5-2.html':'part6/CH6-1.html','part5/PRAC5-3.html':'part4/PRAC4-3.html','part5/PRAC5-4.html':'part4/PRAC4-3.html','part5/PRAC5-5.html':'part4/PRAC4-3.html','part5/PRAC5-6.html':'part4/PRAC4-3.html','part5/PRAC5-7.html':'part4/PRAC4-3.html','part5/PRAC5-8.html':'part4/PRAC4-3.html','part5/PRAC5-9.html':'part4/PRAC4-3.html','part5/PRAC5-10.html':'part4/PRAC4-3.html','part5/PRAC5-11.html':'part4/PRAC4-3.html','part5/PRAC5-12.html':'part4/PRAC4-3.html',
'part6/CH6-2.html':'part6/PRAC6-1.html','part6/CH6-3.html':'part6/PRAC6-1.html'}
assert set(NEAREST_CORE)==set(ROWS)-set(META)

def route_banner(file,i):
    prev=ROUTE[i-1] if i else None; nxt=ROUTE[i+1] if i+1<len(ROUTE) else None
    pieces=[f'必修第 {i+1}／{len(ROUTE)} 站']
    if prev: pieces.append('前站 <a href="'+html.escape(os.path.relpath(prev,Path(file).parent),quote=True)+'">'+html.escape(META[prev]['title'])+'</a>')
    pieces.append(html.escape(CORE_BRIDGES[file]))
    if file=='part3/PRAC3-3.html': pieces.append('下一站 <a href="../part6/CH6-1.html">開始會議語意判斷</a>，不必先做完所有圖表練習。')
    elif file=='part6/PRAC6-1.html': pieces.append('下一站 <a href="../part4/CH4-1.html">保存並重新使用成果</a>；Publish 不屬於必修驗收。')
    elif nxt: pieces.append('下一站 <a href="'+html.escape(os.path.relpath(nxt,Path(file).parent),quote=True)+'">'+html.escape(META[nxt]['title'])+'</a>。')
    else: pieces.append('<a href="../index.html#required-route">返回成果自檢</a>。')
    pieces.append('<a href="../index.html#required-route">查看十站完成證據</a>。')
    return '<p class="core-route" id="core-route-banner">'+' · '.join(pieces)+'</p>'

def extension_banner(file):
    item=ROWS[file]; target=NEAREST_CORE[file]
    role_text={'延伸':'有工作需求時再做的延伸實作','參考':'部署／平台參考，使用前先核對當前官方說明'}[item['role']]
    guidance=item['guidance'].replace('`','')
    assert guidance.strip(),f'empty learner-facing role guidance: {file}'
    bridge=f'<a href="{html.escape(os.path.relpath(target,Path(file).parent),quote=True)}">{html.escape(META[target]["title"])}</a>'
    official=''
    if file in ('part6/CH6-2.html','part6/CH6-3.html'):
        official=' <a href="https://ai.google.dev/gemini-api/docs/aistudio-build-mode" target="_blank" rel="noopener">Google AI Studio Build 官方說明</a>；<a href="https://ai.google.dev/gemini-api/docs/aistudio-deploying" target="_blank" rel="noopener">官方部署與資格說明</a>。'
    return ('<section class="lesson-section optional-route" id="core-route-banner" data-learning-role="'+item['role']+'">'
        '<h2 class="section-heading">'+role_text+'</h2>'
        '<p class="body-text">'+html.escape(guidance)+'</p>'
        '<p class="body-text">本頁可以跳過；需要此工作案例時，先具備 '+bridge+' 的能力。原始示範、完整提示詞與操作內容均保留在下方並預設展開。'+official+' '
        '<a href="../index.html#required-route">返回必修路線</a>。</p></section>')

# Render only the approved ten fragments; preserve all other bytes inside each learner page.
for i,file in enumerate(ROUTE):
    path=ROOT/file; raw=path.read_text(); fragment=(ROOT/'_source/fragments'/META[file]['fragment']).read_text().rstrip('\n')
    fragment=fragment.replace('<!-- learner-content:start -->','').replace('<!-- learner-content:end -->','').strip()
    soup=BeautifulSoup(raw,'html.parser')
    core=soup.select('.lesson-body > .lesson-section#core-1'); legacy=soup.select('.lesson-body > #legacy-reference')
    assert len(core)==1 and len(legacy)==1,file
    a,_=span(raw,core[0]); b,_=span(raw,legacy[0]); assert a<b,file
    raw=raw[:a]+fragment+'\n'+raw[b:]
    banners=BeautifulSoup(raw,'html.parser').select('#core-route-banner')
    assert len(banners)>=1 and banners[0].find_parent(class_='lesson-body'),file
    raw=replace_node(raw,banners[0],lambda old,node:route_banner(file,i))
    assert len(BeautifulSoup(raw,'html.parser').select('#core-route-banner'))==1,file
    raw=attrs(raw,'.lesson-hero',{'data-learning-role':'core'})
    legacy=BeautifulSoup(raw,'html.parser').select('#legacy-reference')
    assert len(legacy)==1,file
    raw=attrs(raw,'#legacy-reference',{'open':True})
    raw=inner(raw,'#legacy-reference > summary','原始完整課程內容、案例與提示詞（保留）')
    path.write_text(raw)

# Add a learner-facing role note to each extension/reference page and expose the full original lesson.
for file,item in ROWS.items():
    if file in META: continue
    path=ROOT/file; raw=path.read_text()
    soup=BeautifulSoup(raw,'html.parser')
    assert len(soup.select('.lesson-body'))==1 and len(soup.select('#legacy-reference'))==1,file
    existing=soup.select('#core-route-banner')
    banner=extension_banner(file)
    if existing:
        assert len(existing)==1,file
        raw=replace(raw,'#core-route-banner',lambda old,node:banner)
    else:
        raw=replace(raw,'#legacy-reference',lambda old,node:banner+old)
    role={'延伸':'extension','參考':'reference'}[item['role']]
    raw=attrs(raw,'.lesson-hero',{'data-learning-role':role})
    raw=attrs(raw,'#legacy-reference',{'open':True})
    raw=inner(raw,'#legacy-reference > summary','原始完整單元內容、案例與提示詞（保留）')
    path.write_text(raw)

# Update the catalog to show all 40 lesson roles at first load.
path=ROOT/'index.html'; raw=path.read_text()
raw=attrs(raw,'#optional-catalog',{'open':True})
raw=inner(raw,'#optional-catalog > summary','完整課程章節（40 個單元；依核心、延伸與參考分流）')
raw=after(raw,'#optional-catalog > summary','<p class="catalog-route-note">十站必修只是一條依能力排列的工作實作路徑；下列章節保留全課 40 頁，未列必修者依工作需要選讀。詳細的學習用途、先修能力和內容限制見各單元開頭說明。</p>')
for file,item in ROWS.items():
    selector='#optional-catalog a[href="'+file+'"]'
    soup=BeautifulSoup(raw,'html.parser'); anchor=soup.select(selector); assert len(anchor)==1,(file,len(anchor))
    badge='<span class="course-role-badge">'+html.escape(item['role'])+'</span>'
    role={'核心':'core','延伸':'extension','參考':'reference'}[item['role']]
    raw=attrs(raw,selector,{'data-learning-role':role})
    title_selector=selector+' .lesson-title'
    if BeautifulSoup(raw,'html.parser').select_one(title_selector):
        title=BeautifulSoup(raw,'html.parser').select_one(title_selector).get_text(' ',strip=True)
        title=re.sub(r'\s*·\s*(必修|核心|延伸|參考)\s*$','',title).strip()
        raw=inner(raw,title_selector,html.escape(title)+' '+badge)
    else:
        def add_badge(old,node):
            assert old.count('</a>')==1,file
            return old[:old.rfind('</a>')]+badge+old[old.rfind('</a>'):]
        raw=replace(raw,selector,add_badge)
path.write_text(raw)
print(f'Updated index and {len(ROWS)} lesson pages; rendered {len(ROUTE)} approved fragments.')
