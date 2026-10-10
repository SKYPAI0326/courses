"""Scoped, reversible content repair. --prepare backs up; --apply writes proposals."""
from pathlib import Path
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import argparse, hashlib, importlib.util, json, re, shutil

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parents[1]
REPORT = ROOT / '_repair/2026-10-11'
BACKUP = ROOT / '_backup/2026-10-11-pre-repair'
UNITS = {
 'A1-visual-foundations': 'part1/CH1-visual-foundations.html',
 'A4-component-instance': 'part1/CH4-component-instance.html',
 'A5-variants-properties': 'part1/CH5-variants-properties.html',
 'B1-wireframe-prototype-entry': 'part2/CH1-wireframe-prototype-entry.html',
 'B2-trigger-navigation-action': 'part2/CH2-trigger-navigation-action.html',
 'B3-transition-motion-purpose': 'part2/CH3-transition-motion-purpose.html',
 'B6-prototype-task-test': 'part2/CH6-prototype-task-test.html',
 'B7-figma-handoff-export': 'part2/CH7-figma-handoff-export.html',
}
spec = importlib.util.spec_from_file_location('render_reference', ROOT / '_tools/repair_render_reference.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
proposals = {}
changes = []

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def propose(path, text):
    path = path.resolve()
    if not path.exists() or path.read_text() != text: proposals[path] = text
def replace(text, old, new):
    assert text.count(old) == 1, ('ambiguous source', old[:100], text.count(old))
    changes.append({'before': old, 'after': new})
    return text.replace(old, new, 1)
def line_replace(text, prefix, new):
    lines = [x for x in text.splitlines() if x.startswith(prefix)]
    assert len(lines) == 1, (prefix, len(lines))
    return replace(text, lines[0], new)

CRITERIA = [
 ('內容與視覺', 'V1', '規則表列出標題、內文、按鈕、錯誤的字型／字級／行高／色碼，畫面使用值與表一致。'),
 ('內容與視覺', 'V2', '360×800下S02與S10長備註完整可讀，沒有截字或與相鄰內容重疊。'),
 ('內容與視覺', 'V3', '待確認、已確認與錯誤都含明確文字，灰階或遮住色塊仍能辨認狀態。'),
 ('內容與視覺', 'V4', '主要動作與一般內文有對比紀錄；依第01堂門檻，大字至少3:1、一般文字至少4.5:1。'),
 ('元件與版面', 'C1', '在測試副本改Button主元件圓角，兩個Instance同步；還原後Label覆寫仍保留。'),
 ('元件與版面', 'C2', '四種Hierarchy／State組合皆唯一且可選，Default與Disabled有文字或外觀區別。'),
 ('元件與版面', 'C3', 'Row用Auto Layout；長備註下高度隨內容增加，文字與動作不重疊。'),
 ('元件與版面', 'C4', '在測試副本新增再移除一列，後續列與容器重新排列；還原12筆資料。'),
 ('任務流程', 'F1', '從Login起點按主要Button可進活動報名List，沒有跳錯Frame。'),
 ('任務流程', 'F2', '從List選定一筆報名後，Detail的id、姓名與備註都對應SIGNUP-DATA.csv該筆。'),
 ('任務流程', 'F3', 'Detail能開確認Dialog，說明是「將此報名標記為已確認」。'),
 ('任務流程', 'F4', 'Dialog取消只關閉彈窗，仍在同一筆Detail且資料狀態未變。'),
 ('任務流程', 'F5', '確認後能看見該筆已確認狀態與成功結果，沒有改到另一筆資料。'),
 ('滾動與回饋', 'S1', '360×800預覽可捲到S12，最後一列與動作完整可見。'),
 ('滾動與回饋', 'S2', '清單中段與底部，Header／Nav／FAB仍固定，且不遮住資料或可點動作。'),
 ('滾動與回饋', 'S3', '成功回饋含可辨认的結果文字，與已確認清單一致；返回不會丟失該筆已確認狀態。'),
 ('測試與交付', 'E1', '主線T01–T08均有實際觀察；整合作品另附選定id、360×800與逐步預期／實際紀錄。'),
 ('測試與交付', 'E2', '保留一個真實或刻意植入故障的畫面／設定、定位與修復前後證據。'),
 ('測試與交付', 'E3', '修復後从Login重跑整段任務，取消、確認、長清單皆有回歸結果。'),
 ('測試與交付', 'E4', '保存的.fig或自己的設計檔能重開，TASK-01預覽起點正確，測試JSON可載入；附兩項設計取捨理由。'),
]
# Keep wording Traditional Chinese even in generated checklists.
CRITERIA = [(c,i,t.replace('辨认','辨認').replace('後从','後從')) for c,i,t in CRITERIA]

class Ranges(HTMLParser):
    """Find original byte-character ranges through parsed tag context, preserving shell."""
    VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text=text; self.lines=[0]; self.stack=[]; self.ranges=[]
        for m in re.finditer('\n',text): self.lines.append(m.end())
        self.feed(text)
    def charpos(self):
        l,c=self.getpos(); return self.lines[l-1]+c
    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append((tag,dict(attrs),self.charpos(),self.charpos()+len(self.get_starttag_text())))
    def handle_startendtag(self,tag,attrs): pass
    def handle_endtag(self,tag):
        assert self.stack and self.stack[-1][0]==tag, ('misnested input',tag)
        t,a,start,inner=self.stack.pop(); endstart=self.charpos(); end=self.text.index('>',endstart)+1
        self.ranges.append((t,a,start,inner,endstart,end))

def dom_inner(text, selector, inner, ancestor='.lesson-body'):
    soup=BeautifulSoup(text,'html.parser'); nodes=soup.select(selector)
    assert len(nodes)==1, (selector,len(nodes))
    node=nodes[0]
    if ancestor: assert node.find_parent(class_=ancestor[1:]) is not None
    # Match the parsed start position of this exact selected node.
    offsets=Ranges(text)
    start=offsets.lines[node.sourceline-1]+node.sourcepos
    rows=[r for r in offsets.ranges if r[2]==start]
    assert len(rows)==1
    _,_,_,begin,end,_=rows[0]
    fragment=BeautifulSoup(inner,'html.parser')
    node.clear()
    for child in list(fragment.contents): node.append(child)
    if ancestor:
        for n in node.select('.lesson-section,.body-text,.step-list,.prac-box'):
            assert n.find_parent(class_='lesson-body') is not None
    result=text[:begin]+inner+text[end:]
    assert len(BeautifulSoup(result,'html.parser').select(selector))==1
    return result

def formal(md): return md.split('<!-- learner-content:start -->',1)[1].split('<!-- learner-content:end -->',1)[0]
def sections(md):
    chunks=re.split(r'^## (.+)\n',formal(md),flags=re.M)
    return {chunks[i]:chunks[i+1].strip() for i in range(1,len(chunks),2)}
def sync_page(oldmd,newmd,path):
    text=path.read_text(); old=sections(oldmd); new=sections(newmd)
    assert old.keys()==new.keys()
    for heading,content in new.items():
        if old[heading]==content: continue
        soup=BeautifulSoup(text,'html.parser'); body=soup.select_one('.lesson-body')
        matches=[s for s in body.select('.lesson-section') if s.find('h2').get_text()==heading]
        assert len(matches)==1, heading
        section=matches[0]; h2=section.find('h2')
        rendered=renderer.render(content).replace('../../courses/uiux-designer/','../')
        text=dom_inner(text, '#'+section['id'], str(h2)+'\n'+rendered+'\n')
    # The only duplicated outcome changed is the B1 hero; sync its same fact.
    oldout='線框真的呈現資訊與動作位置，至少記錄一次閱讀反饋。'
    newout='線框呈現資訊與動作位置，並留下本人走讀紀錄；他人閱讀反饋另記實際結果或待補。'
    if oldout in formal(oldmd) and newout in formal(newmd):
        soup=BeautifulSoup(text,'html.parser')
        n=[n for n in soup.select('.hero .outcome-item') if n.get_text()==oldout]
        assert len(n)==1
        index=soup.select('.hero .outcome-item').index(n[0])+1
        text=dom_inner(text,f'.hero .outcome-item:nth-of-type({index+1})',newout,ancestor='.hero')
    return text

def build():
    for unit,page in UNITS.items():
        path=BASE/'_lessons/uiux-designer'/f'{unit}.md'; old=path.read_text(); md=old
        if unit.startswith('A1-'):
            md=line_replace(md,'講師先把', '自己選取標題「登入工作室」，在右側Text設定字級24、行高32px、字重700；接著選內文設成16／24／400，輔助文字設成14／22／400。數字順序都是字級／行高／字重。逐一點回三個文字層，核對右側值與文字規則表一致，再看手機Frame內的長句是否完整。字型沒有700或400時選最接近的可用粗細並記錄差異；字重清單沒有Medium時也用實際可取得的粗細。右側Line height若是Auto或百分比，改成明確px值。建立文字樣式的入口通常在Text樣式圖示；若找不到，先以規則表完成設定，樣式的儲存不影響本堂核心結果。課堂示範也依此路徑，獨讀時可直接完成。')
        elif unit.startswith('A4-'):
            md=line_replace(md,'4. 用同一來源', '4. 用同一來源多插入一個Instance，改Label為「取消」。自己記下「來源控制：Padding、圓角；此Instance覆寫：Label」，再在主元件暫改圓角，確認原按鈕與取消按鈕同步、兩者Label各自保留，還原圓角並保存前後值。有同學時可請他依紀錄核對。此時取消還是同樣外觀，主次樣式下一堂處理。')
        elif unit.startswith('A5-'):
            md=line_replace(md,'講師故意把', '先複製整個Button元件集到空白區，命名Button / Variant Repair，不改正式來源。在副本把Secondary／Default那個Variant的Hierarchy改成Primary、State維持Default，讓兩個Variant都成為Primary／Default。把副本的四組屬性逐列寫入組合表：此時Primary／Default重複、Secondary／Default缺失。將剛才改動的那個Variant恢復Secondary／Default，核對四列各出現一次，再回正式Instance確認仍可選四種組合。保留副本修復前後紀錄；若只有顏色不同但屬性值重複，仍然不算通過。課堂可由講師植入同一故障，獨讀時自己依此操作。')
        elif unit.startswith('B1-'):
            md=line_replace(md,'3. 把任務卡', '3. 把任務卡放在兩張線框旁，畫箭頭表示Login→List。自己依任務卡走讀：从Login的帳號／密碼欄找到「登入」，沿箭頭到List，再找第一筆T01標題與詳情動作。記錄「起點→動作標籤→下一張畫面→T01位置」，缺一步就補標籤或調整位置。有同學時可先請他只看線框做同樣走讀，保留他的實際路徑，不口頭補充。'.replace('从','從'))
            md=line_replace(md,'**中間結果：**', '**中間結果：**本人走讀紀錄能逐一對到線框上的登入欄位、登入動作與T01位置，缺漏已修正，這時才進到精緻介面。有同學的閱讀結果另記；沒有同學時標「他人反饋待補」，本人核對不能證明新使用者已理解。線框上的箭頭只是設計說明，還不是Prototype連線。')
            md=line_replace(md,'將使用者換成', '將使用者換成「第一次使用的工讀生」，目標改為找到T02的期限。做一張Detail線框，並在現有T01詳情旁建立 `Screen / Detail T02`：標題、期限、說明都改為T02。自己從Login線框沿任務路徑定位T02，再在Detail線框找到期限，將找到的位置與第07堂資料表核對。記錄走讀路徑與核對結果；若發現缺標籤、走錯筆或期限不符，保留修改前後，沒有發現問題就照實記「未發現缺漏」。有同學時另外記錄他只看線框的實際路徑與誤解。最後確認原TASK-01入口沒有被這個測試分支覆蓋。')
            md=replace(md,'線框真的呈現資訊與動作位置，至少記錄一次閱讀反饋。','線框呈現資訊與動作位置，並留下本人走讀紀錄；他人閱讀反饋另記實際結果或待補。')
        elif unit.startswith('B2-'):
            md=line_replace(md,'從List Empty增加', '從List Empty增加「檢視示範任務」Button，連回Screen / List；再建立Detail T03，依第07堂資料表填入T03標題與期限，獨立接上T03及返回。自己在Preview選List Empty為測試起點，依「檢視示範任務→T03→返回」實際點選，核對期限是星期五17:00、返回Screen / List。若停留原畫面，回Interactions核對所選Button或Row的Destination；若顯示T01資料，改到自己的Detail T03並重跑。有同學時可請他同路徑無提示操作，分開記錄本人與同學結果。交出新增的三條連線、一次故障修復及實際Preview結果，測完把主線起點還原Login。')
        elif unit.startswith('B3-'):
            md=line_replace(md,'讓Check位置從', '讓Check位置從x300移到x260，同時用Opacity0→100；保留一份同內容的Instant版本。自己在Preview依相同起點各播放一次，記錄動畫版是否從右側移入並淡入、Instant是否直接出現，以及兩版的完成文字與最終位置是否一致。依能否看清狀態變化與設定Duration說明你的選擇，不把200ms引數當成人的實際等待感。有同學時另記他對理解與等待的回饋，未邀請就標待補。交出前後值表、兩版比較、正確配對結果、故意改名失敗與修復，以及主線兩種轉場理由。')
        elif unit.startswith('B6-'):
            md=line_replace(md,'講師故意把', '先保存目前作品的.fig副本，再在測試副本選Row / T01，把Destination暫改None，從List Long執行測試表的T02。自己觀察點選後是否仍停在List，截取Preview與Interactions設定，再把Destination恢復Screen / Detail並重跑。若介面不允許選None，可暫時移除該條互動，記「互動不存在」，修復時依第10堂重新建立Navigate to → Screen / Detail。下表示範None故障的完整紀錄；請另填自己的實際結果，不把示範值當作已完成證據。課堂也可由講師做同一示範。')
            md=line_replace(md,'6. 下載檢查表', '6. 下載檢查表JSON，另存截圖，自己重新載入JSON，只照紀錄找到同一個層名、故障設定與修復後的目的地，再從Login重跑。若紀錄不足以定位，就補上Frame／層名、動作及修改前後值。有另一位同學時可請他只讀紀錄核對，另記他的結果；沒有同學時標「本人重現／他人核對待補」。記錄要能重現，不能只有全部勾選。')
            oldtable=md.split('| 評分項目 |',1)[1].split('\n\n',1)[0]
            rows=['| 評分項目 | 可觀察判準（每項5分） | 滿分 |','|---|---|---|']
            for category in dict.fromkeys(c for c,_,_ in CRITERIA):
                items=[(i,t) for c,i,t in CRITERIA if c==category]
                rows.append('| '+category+' | '+'；'.join(i+'：'+t for i,t in items)+' | '+str(len(items)*5)+' |')
            md=replace(md,'| 評分項目 |'+oldtable,'\n'.join(rows))
            md=replace(md,'\n| 評分項目 |', '\n計分時開啟[整合作品逐項評分表（可保存／下載）](../../courses/uiux-designer/assets/B6-prototype-task-test/reference/CAPSTONE-SCORE.html)。下表20項各5分，符合整項且附實際證據才得5分，不符合得0分，不給部分分；未執行先記0分與原因，補測後才重算。勾選通過項目數乘5就是總分。本人自測可核對功能，真人理解另列待補。\n\n| 評分項目 |')
            md=line_replace(md,'達80分且', '達80分且沒有阻斷任務才算通過；有阻斷就回該操作單元修復再測。無效連線、無法看最後一筆、取消離開錯誤畫面、確認後沒有結果都屬阻斷或必要功能缺失，不能用其他項目高分抵消。未執行這些必要路徑時標「待補測」，不能因其他項目達80分就宣告通過；其餘未得分項目仍列入修復清單。請說明兩項取捨（例如長按鈕改垂直、用Instant降低動態負擔），不是只複製樣式。')
            md=line_replace(md,'由同學選一筆', '選一筆不同於原T01的任務；有同學時由他選取並執行，獨讀時自行選T02或T03並記「本人自測」。先從該筆Detail直接開始測返回，再依整合作品的新情境做360版本，減少講義提示，自行選擇版面與回饋。交出一次無提示或明記提示的紀錄、至少一個修復前後比較、完整回歸及逐項評分表；沒有受測者時另留他人測試待辦。刻意植入的故障要標明，不虛構使用者誤解。')
        elif unit.startswith('B7-'):
            md=line_replace(md,'Photoshop桌面版需', '第一次使用前先開啟[Photoshop桌面版準備與啟動](../../courses/uiux-designer/assets/shared/PHOTOSHOP-START.html)：已有授權者依Adobe官方入口安裝並開啟；使用教室工作站者須取得實際地點／時段、登入方式與儲存位置，再確認能開啟512×512的三層PSD。沒有軟體仍可檢查PNG尺寸與透明效果，但那不等於完成PSD重開／修改／匯出；在完成檢查表記「Photoshop操作待補」及所缺條件，可先整理Figma輸出，取得可用工作站後回本堂補做。不要把一張扁平PNG改副檔名為.psd來交作業。')
            md=line_replace(md,'**驗收方法：**', '**驗收方法：**獨讀時先關閉作品編輯分頁與檔案，只照交付資料夾內自己的README重新找到.fig、Prototype連結、PSD及PNG。依清單重開.fig或分享設計、Preview與PSD，核對起點Login、PSD三層，以及PNG的512×512與透明角落。把exports/dialog-confirm.png暫移到交付資料夾外的missing-test資料夾，再只照清單確認它缺少；記缺檔位置，放回後重查。有同學時可請他依同一清單操作，另記結果；自己核對記「本人重開」，不能當成接手者已驗收。若Photoshop不可用，PSD項仍待補。這個練習測試交付是否真的可用，不是把資料夾截圖當成通過。第16堂網站會使用本堂badge與同一套視覺規則。')
            md=line_replace(md,'將badge的Background', '將badge的Background顯示，先匯出錯誤白底PNG；再隱藏與重新透明匯出，留下兩版比較。將Dialog文字加長並重新匯出，更新清單的實際高度，不沿用舊值。關閉已開檔案後，自己只照README找到Prototype、PSD與徽章，核對實際檔名／路徑及新版Dialog高度，將找不到或數值不符的項目修正後再重開。有同學時另記他的閱讀與重開結果，沒有同學就標「他人交付驗收待補」，不杜撰誤解。Photoshop未可用時，白底／透明匯出練習與PSD核對保留待補。')
        md=replace(md,'revision: 2026-10-09','revision: 2026-10-11')
        propose(path,md); propose(ROOT/page,sync_page(old,md,ROOT/page))

    bp=ROOT/'_design/COURSE-BLUEPRINT.md'
    propose(bp,replace(bp.read_text(),'T01–T07都有實際觀察','T01–T08都有實際觀察'))
    env=ROOT/'_design/ENVIRONMENT-CONTRACT.md'
    propose(env,replace(env.read_text(),'status-badge.psd、PNG參考、PSD-README','PHOTOSHOP-START.html的自有授權啟動／教室準備條件、status-badge.psd、PNG參考、PSD-README')+'\n2026-10-11起點補充：[Photoshop桌面版準備與啟動](../assets/shared/PHOTOSHOP-START.html)。教室地點／時段、登入方式與儲存位置須由主辦提供；目前未提供，不能宣稱教室路徑可用。自有授權安裝路徑已依官方文件補齊，桌面實測仍待補。\n')
    p=ROOT/'assets/B1-wireframe-prototype-entry/reference/EXPECTED-CHECK.html'
    soup=BeautifulSoup(p.read_text(),'html.parser')
    tr=[tr for tr in soup.select('table.records tbody tr') if tr.find('td').get_text()=='線框真的呈現資訊與動作位置，至少記錄一次閱讀反饋。']
    assert len(tr)==1
    n=soup.select('table.records tbody tr').index(tr[0])+1
    propose(p,dom_inner(p.read_text(),f'table.records tbody tr:nth-child({n}) td:first-child','線框呈現資訊與動作位置，並留下本人走讀紀錄；他人閱讀反饋另記實際結果或待補。',ancestor=None))
    p=ROOT/'assets/COURSE-START.html'
    propose(p,dom_inner(p.read_text(),'main table tr:nth-child(3) td:nth-child(2)','依<a href="shared/PHOTOSHOP-START.html">Photoshop桌面版準備與啟動</a>取得授權軟體／教室使用資訊，確認本課三層PSD能開',ancestor=None))
    p=ROOT/'assets/B7-figma-handoff-export/START-HERE.html'
    text=p.read_text(); soup=BeautifulSoup(text,'html.parser')
    intro=soup.select('main > p')[2]
    idx=soup.select('main > p').index(intro)+1
    # nth-of-type counts only p tags in main, preserving every other original node.
    text=dom_inner(text,f'main > p:nth-of-type({idx})',str(intro.decode_contents())+' 第15堂先讀<a href="../shared/PHOTOSHOP-START.html">Photoshop桌面版準備與啟動</a>；下載<a href="../shared/status-badge.psd">512×512三層PSD</a>、<a href="../shared/status-badge.png">透明PNG參考</a>與<a href="../shared/PSD-README.html">圖層說明</a>。沒有可用軟體就先記待補條件。',ancestor=None)
    propose(p,text)
    p=ROOT/'assets/B7-figma-handoff-export/START-HERE.md'
    propose(p,p.read_text()+'\nPhotoshop操作前讀[準備與啟動](../shared/PHOTOSHOP-START.html)，取得[分層PSD](../shared/status-badge.psd)與[圖層說明](../shared/PSD-README.html)。教室使用資訊尚未提供時標待補，不推定有可用工作站。\n')
    p=ROOT/'assets/B7-figma-handoff-export/reference/HANDOFF-CHECK.html'
    text=p.read_text(); soup=BeautifulSoup(text,'html.parser'); intro=soup.select('main > p')[0]
    propose(p,dom_inner(text,'main > p:first-of-type',intro.decode_contents()+' 獨讀時依README關閉再重開實際檔案，記「本人重開」；同學驗收另列結果或待補。Photoshop未可用時在PSD項寫缺少的工作站／權限，不能勾選完成。',ancestor=None))
    p=ROOT/'assets/B7-figma-handoff-export/reference/HANDOFF-CHECK.md'
    propose(p,p.read_text()+'\n独讀可依README自行關閉再重開檔案，記「本人重開」；他人驗收另記結果或待補。Photoshop不可用時，PSD與透明匯出保留待補。\n'.replace('独','獨'))
    p=ROOT/'assets/B6-prototype-task-test/reference/TASK-TEST-FORM.html'
    text=p.read_text(); soup=BeautifulSoup(text,'html.parser'); lab=soup.select_one('textarea[name="decision"]').parent
    text=dom_inner(text,'main > label:last-of-type',lab.decode_contents()+'<br><a href="CAPSTONE-SCORE.html">開啟整合作品20項評分表</a>：每項符合且附證據5分，未符合或未測0分；80分且必要路徑已測、無阻斷才通過。',ancestor=None)
    propose(p,text)
    p=ROOT/'assets/B6-prototype-task-test/reference/TASK-TEST-FORM.md'
    propose(p,p.read_text()+'\n完成T01–T08後，使用[整合作品逐項評分表](CAPSTONE-SCORE.html)保存20項得分與證據；未測必要路徑不能宣告通過。\n')
    make_score_form(); make_photoshop_start()

def make_score_form():
    template=BeautifulSoup((ROOT/'assets/B6-prototype-task-test/reference/TASK-TEST-FORM.html').read_text(),'html.parser')
    toolbar=str(template.select_one('.toolbar'))
    title='整合作品逐項評分表'
    head='<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'｜UI/UX課程</title><meta name="description" content="活動報名確認整合作品：20項可觀察判準、得分與證據保存。"><link rel="stylesheet" href="../../asset-start.css">'+str(template.style)
    rows=[]
    for c,i,t in CRITERIA:
        rows.append('<tr><td><strong>'+i+'／'+c+'</strong><p>'+t+'</p></td><td><label>實際結果／設定／證據檔名<textarea name="'+i+'-evidence"></textarea></label><label><input type="checkbox" name="'+i+'-pass">符合整項且附證據（5分）</label><p>未符合或未執行不勾選（0分），並寫原因。</p></td></tr>')
    body='<main data-record-key="B6-capstone-score-2026-10-11"><a href="../../../part2/CH6-prototype-task-test.html#section-6">返回整合作品講義</a><h1>'+title+'</h1><p>作品情境：活動報名確認，12筆SIGNUP-DATA.csv、360×800。每項只得5或0分，不給部分分。先操作、寫證據，再勾選；勾選數乘5＝總分。80分且必要路徑已測、沒有阻斷才通過。本人功能自測與他人理解分開記錄。</p>'+toolbar+'<label>姓名<input name="learner"></label><label>日期<input type="date" name="date"></label><label>作品檔名／連結<input name="artifact"></label><label>受測者／本人自測<input name="tester"></label><label>選定報名id<input name="signup-id"></label><div class="table-wrap"><table class="records"><thead><tr><th>可觀察判準（每項5分）</th><th>實際證據與得分</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div><h2>計分與判定</h2><label>通過項目數（0–20）<input type="number" min="0" max="20" name="passed-count"></label><label>總分＝項目數×5（0–100）<input type="number" min="0" max="100" step="5" name="total"></label><label>必要路徑實際結果：登入、正確Detail、取消、確認結果、S12與固定元素<textarea name="required-routes"></textarea></label><label>未測／阻斷／未得分項目與回修位置<textarea name="remaining"></textarea></label><label>判定與理由：通過／需修復／待補測<input name="verdict"></label><p>必要路徑未測填「待補測」；有阻斷或總分不足80填「需修復」。其餘未得分項目即使總分達80仍保留修復待辦。真人理解未驗證另記待補，不由本表推定。</p><label>兩項設計取捨與理由<textarea name="decision"></textarea></label><p>下載JSON後與第14堂測試截圖放進交付包tests/。同一瀏覽器可保存；換電腦先下載JSON。</p></main><script src="../../record-form.js"></script>'
    propose(ROOT/'assets/B6-prototype-task-test/reference/CAPSTONE-SCORE.html','<!doctype html><html lang="zh-TW"><head>'+head+'</head><body>'+body+'</body></html>\n')

def make_photoshop_start():
    content='''<!doctype html><html lang="zh-TW"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Photoshop桌面版準備與啟動｜UI/UX課程</title><meta name="description" content="第15堂的授權軟體入口、教室工作站準備條件與三層PSD啟動檢查。"><link rel="stylesheet" href="../asset-start.css"><style>main{max-width:800px;margin:auto;padding:32px 24px}li{margin:12px 0}code,a{overflow-wrap:anywhere}img{max-width:100%}</style></head><body><main><a href="../../part2/CH7-figma-handoff-export.html#section-2">返回第15堂材料起點</a><h1>Photoshop桌面版準備與啟動</h1><p>第15堂要親自開啟、修改與儲存分層PSD，再匯出透明PNG。先選自己的已授權電腦或已確認的教室工作站，完成下列啟動檢查後再進講義操作。</p><h2>使用自己的授權電腦</h2><ol><li>確認你已有可使用Photoshop桌面版的Adobe授權；學校／公司帳號使用所配發的帳號與存取權。到<a href="https://www.adobe.com/home">Adobe Home</a>登入，進Apps找到Photoshop桌面版，依<a href="https://helpx.adobe.com/download-install/apps/download-install-apps/creative-cloud-apps/download-creative-cloud-apps.html">Adobe官方安裝步驟</a>選Download並完成安裝。若只見購買／試用、沒有可用權限，先記「授權待補」並確認已有的配發資格。</li><li>已有Creative Cloud桌面程式時，開啟Apps，找到Photoshop選Install；安裝後選Open，或從電腦的應用程式開Photoshop。只有網頁版入口時，回官方文件選桌面程式。Creative Cloud程式尚未安裝可依<a href="https://helpx.adobe.com/download-install/apps/download-install-apps/creative-cloud-apps/download-creative-cloud-desktop-app-from-web.html">官方下載說明</a>取得安裝檔。</li><li>遇到安裝失敗、系統不支援或要求管理員權限時，記錄錯誤與缺少條件，使用原授權單位的支援管道確認。可改用已確認的教室工作站；尚未確認就保留「Photoshop操作待補」。</li></ol><h2>使用教室工作站</h2><p>本教材尚未取得教室的實際使用資訊。開課前主辦須提供下列資料；學員把它記到自己的第15堂檢查表。缺任一必要條件時，教室路徑仍待確認。</p><ul><li>實際地點、可使用日期／時段，以及預約方式或是否免預約。</li><li>工作站編號或識別方式、登入流程；授權由誰提供，Photoshop桌面版是否已安裝可啟動。紀錄登入流程，不把密碼寫進交付包。</li><li>能下載本課PSD並儲存／帶走成果的位置與方式，例如個人資料夾；先確認使用者有寫入權限。</li></ul><h2>開始前的啟動檢查</h2><ol><li>下載本課<a href="status-badge.psd" download>status-badge.psd</a>到自己的可寫入資料夾，開Photoshop桌面版，選File → Open開啟該檔。</li><li>核對畫布512×512、RGB，Layers中有Background、Card、Check三個獨立圖層。依<a href="PSD-README.html">圖層說明</a>核對；只有一張扁平圖片時，確認開的是.psd而非參考.png。</li><li>切换Background可見性，確認能看見白底或透明棋盤格；再切換Check，勾號消失時Card仍保留。完成後恢復Check可見、Background隱藏。</li><li>在第15堂檢查表記使用裝置、Photoshop版本、PSD下載位置與啟動結果；能開檔且可寫入成果資料夾，再回講義「Photoshop儲存分層與透明PNG」繼續。啟動成功尚不代表完成儲存／重開／匯出。</li></ol><h2>暫時沒有可用軟體</h2><p>可先整理Figma規格、.fig與畫面輸出，並閱讀<a href="status-badge.png">透明PNG參考</a>；在PSD項記「Photoshop操作待補」、缺少的授權／工作站／權限與回修位置。取得環境後重開本頁，完成啟動檢查與第15堂全部Photoshop步驟。PNG參考不能證明已完成PSD操作。</p><p>安裝入口依Adobe官方文件於2026-10-11查證；教室使用資訊與實際桌面操作仍須留下真實結果。</p></main></body></html>'''.replace('切换','切換')
    propose(ROOT/'assets/shared/PHOTOSHOP-START.html',content+'\n')

def prepare():
    REPORT.mkdir(parents=True,exist_ok=True)
    assert not BACKUP.exists(), 'backup already exists; never overwrite'
    existing=[p for p in proposals if p.exists()]
    # Include evidence metadata before its stale-record invalidation.
    existing += [ROOT/'_validation/evidence.json',ROOT/'_validation/validation-result.json']
    manifest={'date':'2026-10-11','base':str(BASE),'files':[], 'new_files':[str(p.relative_to(BASE)) for p in proposals if not p.exists()]}
    for p in existing:
        rel=p.relative_to(BASE); dest=BACKUP/'site'/rel; dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,dest)
        assert digest(p)==digest(dest)
        manifest['files'].append({'path':str(rel),'sha256':digest(p)})
    (BACKUP/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    (REPORT/'proposed-changes.json').write_text(json.dumps([{'path':str(p.relative_to(BASE)),'content':t} for p,t in proposals.items()],ensure_ascii=False,indent=2)+'\n')
    (REPORT/'text-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
    # Hashes and visible-text snapshots are captured before edits.
    snaps={}
    for _,page in UNITS.items():
        s=BeautifulSoup((ROOT/page).read_text(),'html.parser')
        snaps[page]={'text':s.select_one('.lesson-body').get_text('\n',strip=True),'sections':[(n['id'],n.find('h2').get_text()) for n in s.select('.lesson-body .lesson-section')], 'shell_sha256':hashlib.sha256(str(s.head).encode()).hexdigest()}
    (REPORT/'before-snapshot.json').write_text(json.dumps(snaps,ensure_ascii=False,indent=2)+'\n')
    restore='''#!/bin/bash
set -euo pipefail
course_dir="$(cd "$(dirname "$0")/.." && pwd)"
python3 - "$course_dir" <<'PY'
from pathlib import Path
import hashlib,json,shutil,sys
root=Path(sys.argv[1]); base=root.parents[1]; backup=root/'_backup/2026-10-11-pre-repair'
m=json.loads((backup/'manifest.json').read_text())
for row in m['files']:
 p=backup/'site'/row['path']; assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
for row in m['files']:
 dst=base/row['path']; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(backup/'site'/row['path'],dst)
print('已還原',len(m['files']),'個修復前檔案；新增檔保留，清單見manifest.json。')
PY
'''
    (ROOT/'_tools/restore-2026-10-11-pre-repair.sh').write_text(restore)
    plan='''# Repair Plan：獨立閱讀與跟做

task_scope: content-change
授權：使用者「執行修正」，限前輪審查發現的獨讀路徑、Photoshop起點、B6計分及T08一致性。
範圍：A1、A4、A5、B1、B2、B3、B6、B7教案及對應HTML；相關起始材料、檢查表、Blueprint、Environment Contract；受影響的舊證據失效標記。
文字完整變更清單：text-changes.json；各目標完整修訂案：proposed-changes.json。
不刪除或合併活動；修改原段落使獨讀可执行。課程順序、section id、外層DOM、CSS、導覽與既有表單欄位不變。B6原評分表改為同五類、同權重100分的20個5分判準，新增評分表與Photoshop入口，連結在首次使用前提供。

## 修復清單
1. BLOCKER：正式正文依賴講師／同學。修教案來源，補可自行走讀、植入／修復故障、重開核對的方法；保留同儕活動並分開真實證據與待補。
2. BLOCKER：Photoshop工作站無取得路徑。新增自有授權官方安裝入口與啟動檢查；教室實際資訊未提供就維持待確認，不虛構教室。無軟體不通過PSD操作。
3. MAJOR：B6評分無逐項標準。每項5或0分且附證據，未測記0與待補；必要路徑未測或有阻斷不得通過。同步可保存表單。
4. MINOR：Blueprint的T01–T07改T01–T08；正文與現有測試表已列T08，予以保留。

## 執行順序與驗收
scan → plan → 雜湊備份／還原脚本 → 來源 → 明確DOM錨點同步 → 表單／材料 → 結構、lint、全文與連結核對、git diff、代表頁browser smoke → 報告。
備份含既有未提交修改；不動其他課程，未授權commit／push。既有證據hash失效須标記待重驗；靜態通過不宣告真人或平台已完成。
search-index僅索引title/meta，本輪正式頁title/meta不變；新增材料由講義連結取得，索引是否納入按公開路徑規則核對，必要時僅同步本課條目。
'''.replace('可执行','可執行').replace('脚本','腳本').replace('标記','標記')
    (REPORT/'REPAIR-PLAN.md').write_text(plan)
    scan='''# Scan：獨立閱讀與跟做

依前輪16堂正式正文審查，修復集中8堂；原學習主線視覺→版面→元件→內容→流程→回饋→測試→交付→網站保留。責任層是教案內容與環境入口，HTML同源同步，非改通用契約或新增測驗題。

## Activity Identity Audit
| 單元 | Demo材料／方法／支援 | Together新增認知工作／產物 | Solo新條件／獨立判準 | 重複判定 |
|---|---|---|---|---|
| A1 | Login文字、完整字型數值示範 | 自選三種文字角色核對規則表、長句可讀 | 更換Primary與長句、對比紀錄 | 角色與限制不同，保留 |
| A4 | Button來源與Instance同步 | 取消Label覆寫、辨認來源控制與局部差異 | 長Label、来源同步與破壞修復 | 新增覆寫／診斷，保留 |
| A5 | 四組Variant軸 | 屬性去重、缺失組合診斷，測試副本 | 改狀態、重複修復與可選驗證 | 複本故障給明確起點；不新增重跑活動 |
| B1 | 低細節線框、畫面責任 | 元件對映、唯一命名與入口 | 初次工讀生／T02期限、本人走讀核對 | 資訊規劃與起點不同，保留 |
| B2 | Login至Detail基本连線 | 正確熱區／目的地／返回與故障定位 | Empty→T03→返回、三條新連線 | 分支與資料不同，保留 |
| B3 | 同名配對與轉場引數 | 根據用途判斷方向及配對 | Check位移＋透明／Instant比較、改名故障 | 新引數與比較，保留 |
| B6 | None故障的完整紀錄 | 真實失敗排序、定位、修復與全回歸 | 報名12筆、360、證據計分 | 測試與新情境遷移不同，保留 |
| B7 | Design規格、各格式用途 | 三層PSD／透明PNG、可重開交付包 | 錯誤白底修復、Dialog加長與清單更新 | 格式判斷與交付一致性不同，保留 |

素材、產物、操作、決策、認知工作與支援程度見上表及各課來源內部活動表；本輪只解除活動對現場人的必然依賴，仍保留真人理解／接手驗收待辦。

## Shared Copy Audit
16堂都共用「先開起始材料／完成檢查表」入口段，屬必要素材导航；保留可點的本堂路徑。未新增跨頁結尾口號或同一工作流套標題；本人自測標記只出現在會誤認真人證據的活動。既有想一想與答案保留，不新增固定數量問題。

## Assets／Environment
B6 TASK-TEST-FORM已有T01–T08，缺的是精確計分；新增CAPSTONE-SCORE。B7 PSD／PNG／圖層說明均存在，缺的是软件取得／啟動；新增PHOTOSHOP-START並同步入口。教室資訊與桌面實跑仍待補。
'''.replace('来源','來源').replace('连線','連線').replace('导航','導覽').replace('软件','軟體')
    (REPORT/'SCAN.md').write_text(scan)
    print('Prepared',len(existing),'backups;',len(proposals),'proposals')

def apply():
    m=json.loads((BACKUP/'manifest.json').read_text())
    for row in m['files']:
        assert digest(BASE/row['path'])==row['sha256'], ('changed since backup',row['path'])
    saved=json.loads((REPORT/'proposed-changes.json').read_text())
    for item in saved:
        p=BASE/item['path']; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(item['content'])
    changed={i['path'] for i in saved}
    p=ROOT/'_validation/evidence.json'; ev=json.loads(p.read_text()); invalid=0
    for rec in ev['records']:
        if any(a.get('path') in changed for a in rec.get('artifacts',[])):
            rec['previous_verdict']=rec['verdict']; rec['verdict']='PENDING'
            rec['invalidated_at']='2026-10-11'; rec['invalidation_reason']='獨讀修復改變來源／頁面／材料hash，歷史紀錄保留；本輪範圍驗證見_repair/2026-10-11。'
            invalid+=1
    ev['latest_scoped_repair']='courses/uiux-designer/_repair/2026-10-11/REPAIR-REPORT.md'
    # Register additional dependencies without inventing platform evidence.
    for u in ev['units']:
        extra=[]
        if u['id']=='B6':extra=['courses/uiux-designer/assets/B6-prototype-task-test/reference/CAPSTONE-SCORE.html']
        if u['id']=='B7':extra=['courses/uiux-designer/assets/shared/PHOTOSHOP-START.html']
        u['assets']+= [a for a in extra if a not in u['assets']]
    p.write_text(json.dumps(ev,ensure_ascii=False,indent=2)+'\n')
    p=ROOT/'_validation/validation-result.json'; vr=json.loads(p.read_text())
    vr['previous_status']=vr['status'];vr['status']='PENDING_REVALIDATION'
    vr['invalidated_at']='2026-10-11';vr['latest_scoped_repair']=ev['latest_scoped_repair']
    vr['invalidation_reason']='本輪改變內容與材料；歷史機器驗證結論不代表目前版本。平台與真人待補清單保留。'
    p.write_text(json.dumps(vr,ensure_ascii=False,indent=2)+'\n')
    print('Applied',len(saved),'files; invalidated',invalid,'historical records')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true');parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    if args.prepare:build();prepare()
    elif args.apply:apply()
    else:parser.error('choose --prepare or --apply')
