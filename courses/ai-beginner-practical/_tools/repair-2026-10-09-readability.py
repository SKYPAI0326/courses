#!/usr/bin/env python3
"""Apply the approved readability repair using DOM anchors and source spans."""
from pathlib import Path
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import hashlib, html, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / '_backup/2026-10-09-pre-readability'
OUT = ROOT / '_repair/2026-10-09-readability'
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Spans(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source, self.stack, self.spans = source, [], {}
        self.lines = [0]
        for m in re.finditer('\n', source): self.lines.append(m.end())
        self.feed(source)
    def source_offset(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col
    def handle_starttag(self, tag, attrs):
        pos, start = self.getpos(), self.source_offset()
        if tag in VOID: self.spans[pos] = (start, start+len(self.get_starttag_text()))
        else: self.stack.append((tag, pos, start))
    def handle_startendtag(self, tag, attrs):
        start = self.source_offset()
        self.spans[self.getpos()] = (start, start+len(self.get_starttag_text()))
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            name, pos, start = self.stack[i]
            if name == tag:
                end = self.source.index('>', self.source_offset()) + 1
                self.spans[pos] = (start, end)
                del self.stack[i:]
                return

class Page:
    def __init__(self, name):
        self.name = name
        self.source = (BACKUP/name).read_text()
        self.parser = Spans(self.source)
        self.soup = BeautifulSoup(self.source, 'html.parser')
        self.body = self.soup.select_one('.lesson-body')
        self.edits = []
    def node(self, selector, prefix=None):
        found = self.soup.select(selector)
        if prefix is not None: found = [n for n in found if n.get_text(' ',strip=True).startswith(prefix)]
        assert len(found)==1, (self.name,selector,prefix,len(found))
        return found[0]
    def raw(self, node):
        a,b=self.parser.spans[(node.sourceline,node.sourcepos)]
        return self.source[a:b]
    def replace(self, node, new, reason):
        assert node is self.body or node.find_parent(class_='lesson-body') is self.body or node.find_parent(class_='page-hero') is not None or node.name=='script', (self.name,node.name,reason)
        a,b=self.parser.spans[(node.sourceline,node.sourcepos)]
        self.edits.append((a,b,new,reason))
    def inner(self,node,new,reason):
        raw=self.raw(node)
        self.replace(node,raw[:raw.index('>')+1]+new+raw[raw.rfind('</'):],reason)
    def p(self,prefix,new,selector='.lesson-body p'):
        self.inner(self.node(selector,prefix),new,'改寫：'+prefix[:35])
    def text(self,selector,new,prefix=None):
        self.inner(self.node(selector,prefix),html.escape(new),'改寫標籤')
    def insert_after(self,node,new,reason):
        a,b=self.parser.spans[(node.sourceline,node.sourcepos)]
        for i,(start,end,changed,old_reason) in enumerate(self.edits):
            if (start,end)==(a,b):
                self.edits[i]=(a,b,changed+'\n'+new,old_reason+'；'+reason)
                return
        self.replace(node,self.raw(node)+'\n'+new,reason)
    def render(self):
        edits=sorted(self.edits)
        for left,right in zip(edits,edits[1:]):assert left[1]<=right[0],('overlap',self.name,left[3],right[3])
        result=self.source
        for a,b,new,reason in reversed(edits):result=result[:a]+new+result[b:]
        return result

def link(href,label):
    return f'<a href="{href}" target="_blank" rel="noopener">{label}</a>'
def paragraph(text): return '<p class="body-text">'+text+'</p>'
pages={f:Page(f) for f in ['index.html','module1.html','CH1-1.html','CH2-1.html','CH3-1.html','CH4-1.html','PRAC2-1.html']}

# Shared labels: keep the original fields, keys and scripts.
for name in ['CH3-1.html','CH4-1.html']:
    p=pages[name]
    p.text('.learner-workbench-note','把提示詞、第一版與修訂結果貼回這裡。按「儲存到本機」後重新整理，確認內容還在；完成後匯出。選做欄位可留空。')
    for n in p.body.select('p'):
        if n.get_text(' ',strip=True).startswith('完成上方自己的一份成品即可。以下舊例'):
            p.inner(n,'完成本章作品後，可依需要查看下方範例。請自行核對，不需要其他學員的檔案。','清除選做區殘句')
    titles={'lesson-concept':'課後參考：'+('來源、引用與閱讀筆記' if name.startswith('CH3') else '生活方案與比較方法'),
            'lesson-demo':'課後示範：'+('新聞、公告與書籍筆記' if name.startswith('CH3') else '旅遊與購物方案'),
            'lesson-practice':'課後練習：'+('用其他文章查核引用' if name.startswith('CH3') else '用自己的生活需求比較方案'),
            'lesson-assets':'課後素材與離線備援','lesson-quiz':'課後自我檢查'}
    for sid,title in titles.items():
        matches=p.body.select(f'#{sid} > details > summary')
        if matches:p.inner(matches[0],title,'按用途命名選做入口')
    for n in p.body.select('section:not([id]) > details > summary'):
        if n.get_text().startswith('選做工具箱'):p.inner(n,'課後查閱：常見問題與修正方法','按用途命名選做入口')
    p.text('#lesson-check h2','完成後，重開檔案做最後檢查')
    p.p('自己只看完成物，回答：','只看匯出檔，回答「交給誰、依據在哪裡、還缺什麼、下一步由誰做」。答不出時，回自己的資料與修訂步驟補齊。',selector='#lesson-check p')

p=pages['CH1-1.html']
p.text('.lesson-tagline','3 小時｜選一個工作任務，完成一份可使用的短文。')
p.text('.lesson-start-copy','選一份材料，看過短示範後起稿。把自己的回答貼回工作台，完成後下載保存。')
p.text('.lesson-start-link','選材料與看示範 →')
p.p('這些句子文法正確','信寫得順，卻多了原資料沒有的日期、折扣與交期。寄出前要逐句核對，避免讓客戶把猜測當成承諾。')
p.p('所以，隨意問 LLM','本課會用四種工作練習：寫短文、改成適合不同讀者的文字、查文件依據，以及比較方案。每次都要知道哪些內容有資料支持、哪些仍待確認。')
p.p('教育提醒、服務回覆','今天選一個與自己工作接近的任務，寫出第一版，找出一個需要修正的地方，再保存新版。每人獨立完成一案。',selector='#lesson-start p')
p.p('第一步到下方展開','先看下方設備通知示範，再選自己的材料。<a href="#workplace-practice">看示範與選材料 →</a>　<a href="#practice-workbench">貼回工作台 →</a>',selector='#lesson-start p')
p.p('180分鐘：','本章安排 3 小時。下方生活題供課後選做。',selector='#lesson-start p')
p.p('先選一個與你單位','可選教育行政課前提醒、服務窗口回覆或業務週摘要。已有獲准使用的原文，也可改用自己的資料；先寫清楚給誰看、希望他做什麼。')
p.p('本章要交一份可使用','最後帶走一份短文，並保留原提示詞、第一版、修正指令與新版。這些直接存在同一個工作台。')
p.text('#workplace-practice h3','先確認能送出一句話',prefix='開始前')
p.p('準備能輸入','先開啟課前與講師確認可用的文字對話工具。送出「請用一句話說明你能協助哪些文字工作」，複製回答並貼入自己的筆記。看到回答、貼得回來，就可以開始。尚未準備工具時，先依'+link('assets/fallback/text-llm-minimum-start.md','工具啟動卡')+'操作；本頁工作台負責保存，不會產生 AI 回答。')
p.p('若沒有工具','無法登入或送出時，先請講師協助確認入口。暫時可用作者範例練習找出新增的事實，記下「平台待重跑」；工具可用後再送出自己的提示詞。無法暫存時，立即匯出或用'+link('assets/worksheets/unit1-practice-sheet.md','離線工作表')+'保存。')
p.p('CH1先練','現在只處理一份原文與一份短文。下一章再練不同讀者的寫法。')
p.text('#workplace-practice h3','先看：一則設備通知怎麼修',prefix='看一個獨立示範')
p.p('這是作者示範','這是作者編寫的示範。你接著用自己的材料起稿；若有多種錯誤，先修最影響使用的一種。每次回答可能略有不同，記下你改了什麼指令、哪一句變好了。')
p.text('#workplace-practice h3','短文有沒有新增事實、超過長度？',prefix='自己驗字數')
p.p('A正文上限150','教育提醒最多150字，服務回覆最多100字。選取交付的正文，以文字工具檢查「不含空白的字元數」；標點、數字與英文也算，另列的待確認不算。若工具不能計數，可看下方分行示範。不要只相信模型報的字數。')
p.p('2026-10-08實跑A','修短時也要重新核對原文。例如「已安排訪談」不能直接改成「尚未進行」；原文沒有說完成狀態，就寫「完成狀態待確認」。原句已正確時可保留，記下核對依據。')
for prefix,new in [
('U1-START／','1. 看示範、選一案。確認這份短文給誰看，希望對方做什麼。'),
('U1-ASK／','2. 起稿。展開所選材料，複製起稿提示詞，替換方括號並貼入完整原文後送出。把完整提示詞與第一版貼回工作台。'),
('U1-DIAG／','3. 找一個問題。比較原文與回答，寫「原文是……，回答是……，可能造成……」。先查看自己案例的日期、狀態或件數，不必檢查其他案例。'),
('U1-GAP／','4. 修一次。只補一項條件，其他資料與格式不變。保存新版，指出改了哪句及其原文依據。第一版已正確時，確認一項重要條件，照實記錄無差異。'),
('U1-SAVE／','5. 保存。將待確認事項、確認者與下一步留在工作台。按「儲存」，重新整理確認內容仍在，再匯出並從下載資料夾重開。'),
('165–180分鐘：','6. 回看成果。只看匯出檔，說出原任務、修改理由及下一步。需要協助時，把卡住的句子指出來。')]:
    p.inner(p.node('#workplace-practice li',prefix),new,'簡化個人操作步驟')
p.text('#workplace-practice h3','把回答貼回同一個工作台',prefix='工作台怎麼')
p.p('主線用八個欄位','起稿後貼回第一版，修正後貼回新版；在旁邊簡短寫問題、修改理由與待確認。作品以「新版完整短文」為準。其他選做欄位可留空。')
p.p('必做八個文字欄','展開後，把自己的提示詞與前後版貼回對應欄位。填完不等於內容正確，請依頁尾清單核對。',selector='#lesson-practice p')
p.p('確認原prompt','檢查：原文與提示詞完整；第一版、新版與一次修正都在；重要日期、狀態及數字符合原文；待確認事項有確認者與下一步。',selector='#lesson-check p')
p.p('按工作台儲存','按「儲存」後重新整理，再按「匯出 Markdown」。到下載資料夾打開 <code>unit1-practice-sheet-complete.md</code>，確認前後版都在。<a href="#practice-workbench">回工作台保存</a>',selector='#lesson-check p')
for sid,title in {'lesson-concept':'課後參考：語言模型與搜尋的差別','lesson-example-bank':'課後素材：五個生活對話題','lesson-demo':'課後示範：資訊不足時怎麼追問','lesson-error-clinic':'課後練習：判斷回答錯在哪裡','lesson-assets':'離線工作表與備援範例','lesson-quiz':'課後自我檢查'}.items():
    p.text(f'#{sid} > details > summary',title)
for n in p.body.select('section:not([id]) > details > summary'):
    if n.get_text().startswith('選做：原概念'):p.inner(n,'課後查閱：常見問題與處理方法','按用途命名選做入口')
for n in p.soup.select('.outcome-item'):
    if '變因' in n.get_text():p.inner(n,'能只改一項條件，核對回答的變化。','簡化學習成果用語')

p=pages['CH2-1.html']
p.text('#lesson-start h2','先寫自己的文字，再做十頁提案')
p.p('CH1 的任務定義','先看 Email 前後版，再用自己的情境寫一封 Email、一則短訊息，並為 Email 改一次讀者。文字保存後，接著用完整企劃做 Gamma 簡報。每人獨立選題與操作。')
table=p.node('#lesson-start table')
p.replace(table,'<table><thead><tr><th>開始前</th><th>你要做的事</th></tr></thead><tbody><tr><td>作品</td><td>自己的 Email、短訊息與 Email 改寫版；接著完成十頁 Gamma 提案。</td></tr><tr><td>材料</td><td>可用的文字對話工具、下方工作台，以及'+link('assets/templates/unit2-communication-scenarios.html','情境素材頁')+'。</td></tr><tr><td>第一步</td><td>看下方完整 Email 示範，找出給誰看、要對方做什麼；再選自己的情境。</td></tr></tbody></table>','將八列任務契約收斂為三個開始資訊')
p.p('情境素材庫保留','自我介紹、額外轉換與其他情境供課後選做。先完成自己的文字，再進入簡報。')
p.p('三小時完成線：','本章 3 小時：前半完成文字，後半製作 Gamma 提案。工具暫時不可用時，先保存已有內容，註明還缺哪一步。')
p.p('提示詞是你交給','提示詞就是交給 AI 的工作說明。把事情、要做的成品、不能改的條件與成品格式寫清楚，AI 才有資料可用。')
p.p('阿凱讀完後覺得','林小姐曾和工作室合作過一次，阿凱希望口吻更自然。他保留價格、交期與追問，只改讀者關係：')
p.p('這個錯例看起來流暢','錯例新增了開始日期、折扣、保證，還把7個工作天改成5天。先指出哪句沒有依據，補上「未提供的內容標為待補」試一次；若仍有錯，就依原文手動修正，保留模型版與人工修改後的成品。')
p.text('#lesson-demo h3','再看：短訊息如何交代事情與下一步',prefix='兩個轉移案例')
p.p('Email 的方法要能','短訊息通常只要2–4句：先講事情，再讓對方知道下一步。以下示範保留已知事實，沒有編造婉拒理由。')
# Move optional examples into the existing optional section, keeping their markup.
optional=[]
for n in p.body.select('#lesson-demo details'):
    if any(x in n.find('summary').get_text() for x in ['自我介紹','步驟10','原完整兩份']):
        optional.append(p.raw(n));p.replace(n,'','將選做活動集中課後區')
for n in p.body.select('#lesson-demo .scenario-row'):
    title=n.select_one('.scenario-task')
    if title and title.get_text().startswith('選做：三版'):
        optional.append(p.raw(n));p.replace(n,'','將選做判斷集中課後區')
wraps=p.body.select('#lesson-demo > .steps-wrap')
first=[n for n in wraps if len(n.select('.step-block'))==3 and 'U2-START' in n.get_text()]
assert len(first)==1
p.replace(first[0],'','合併再次閱讀示範的三個框至現有示範檢查')
practice=p.node('#lesson-practice')
raw=p.raw(practice);a=raw.index('>')+1;b=raw.rfind('</section>')
p.replace(practice,raw[:a]+'<details class="workbench-disclosure"><summary>課後選做：自我介紹、額外改寫與轉換練習</summary>'+raw[a:b]+''.join(optional)+'</details>'+raw[b:],'將課後活動集中於既有區塊')
for n in p.body.select('#lesson-demo .step-block'):
    head=n.select_one('.step-heading');body=n.select_one('.step-body');circle=n.select_one('.step-circle')
    if not head or not body:continue
    t=head.get_text(' ',strip=True)
    if t.startswith('Together · 從五種'):
        new='1. 選自己的 Email 情境';number='1';content='<p>從素材頁選一種情境，填背景、任務、限制與格式。替換方括號，寫清楚收件者和希望他做的事。</p><p>資料沒有的日期、金額與承諾，寫「待補」。不知道怎麼填時，先用素材中的示範值。</p>'
    elif t.startswith('Together · 送出 Email'):
        new='2. 送出 Email，保存第一版';number='2';content='<p>把完整提示詞送到自己的對話工具。收到回答後，將提示詞與第一版貼回上方工作台。</p><p>核對日期、金額、交期與承諾是否符合背景。格式不符就補格式再試一次；事實仍有錯時，依原文手動修正並說明。</p>'
    elif '核心 LINE／短訊息' in t:
        new='3. 寫一則短訊息';number='3';content='<p>從婉拒、催促、道歉、報平安或解釋誤會選一種，說清收件者關係與希望對方做的事。格式指定2–4句，直接給訊息。</p><p>送出後貼回提示詞與第一版。只看訊息，對方應能知道事情和下一步；若仍像長信，補「先講重點，不要寒暄段落」再試一次。</p>'
    elif 'U2-AUDIENCE' in t and t.startswith('必做'):
        new='4. 為 Email 改一次讀者';number='4';content='<p>回原 Email 對話，說明新讀者、他要知道什麼，以及必須保留的事實。送出後將指令和修正版貼入 Email 對應欄位。</p><p>比較兩版：口吻與重點是否適合新讀者？日期、金額和行動是否保留？簡短記下改了哪裡。若事實被刪，補上必須保留的資訊，仍不符時手動修正。</p>'
    elif 'U2-SAVE' in t:
        new='5. 保存文字，接著做簡報';number='5';content='<p>完成頁尾文字檢查，按「匯出 Markdown」，到下載資料夾開啟 <code>unit2-communication-pack-complete.md</code>，確認 Email、短訊息與改寫版都在。</p><p>接著開啟 <a href="PRAC2-1.html" target="_blank" rel="noopener">Gamma 十頁提案演練</a>。選做欄位可留空。</p>'
    else:continue
    p.inner(head,new,'簡化必做步驟標題');p.inner(circle,number,'連續編號必做操作');p.inner(body,content,'將重複固定欄位整理成動作與檢查')
p.p('備援路徑：','<strong>工具暫時不能用：</strong>先用完整示範核對事實，保存已寫的提示詞並記下未完成步驟。工具恢復後，接著完成自己的 Email、讀者轉換與短訊息。')
p.p('若瀏覽器不能暫存','瀏覽器不能暫存時，立即匯出或列印；也可使用素材頁的離線文字。找不到工具的輸入或複製功能時，先請講師協助，保留目前紀錄。')
p.p('不要只在最後的成品','先找出錯誤句子，再比對背景資料。補上缺少的限制後試一次；仍有錯時依原文人工修正。兩個版本都保留，記下你改了什麼。')
p.p('跨階段錯誤要回到','例如回答多了一個日期：先回背景查原文，補「沒有提供的日期標待補」試一次；若仍新增日期，手動刪除或改成待補。保留原回答與人工修正版，檢查其餘事實後再使用。')
q=p.node('#lesson-quiz .quiz-item','Q2')
p.inner(q,'<div class="quiz-q">Q2：Email 出現背景沒有的「下週一交付」。補限制再試一次後，仍有這句。你會怎麼完成？</div><div class="quiz-opts"><label class="quiz-opt"><input type="radio" name="q2"><span>A. 保留，因為寫得很肯定</span></label><label class="quiz-opt"><input type="radio" name="q2"><span>B. 不核對原文，一直重問</span></label><label class="quiz-opt"><input type="radio" name="q2"><span>C. 依原文刪除或改成待補，保留模型版與人工修正版，再核對其他事實</span></label><label class="quiz-opt"><input type="radio" name="q2"><span>D. 換成另一個自己猜的日期</span></label></div><details class="quiz-ans"><summary>顯示答案</summary><div>正確答案：C。提示詞修正後仍要核對。你可以依原文完成可用的人工修正版，並保留修改理由。</div></details>','必答題改為必做Email，加入人工收尾判斷')
for n in p.body.select('.callout-body'):
    t=n.get_text(' ',strip=True)
    if 'Checkpoint U2-CHECK-2' in t:p.inner(n,'<strong>Email 檢查：</strong>工作台應有自己的提示詞與第一版，且主旨、正文、署名完整。若有未提供的日期或承諾，回背景補限制試一次，仍錯就依原文人工修正。','簡化Email檢查')
    elif '示範停站' in t:p.inner(n,'<strong>看懂示範了嗎？</strong>指出改了哪個讀者、哪一句口吻，以及保持不變的價格與交期；接著用自己的情境操作。','合併示範閱讀檢查')
# Only remove the two invalid closing tags from their explicitly located scenario nodes.
for n in p.body.select('.scenario-pick'):
    raw=p.raw(n)
    if '</br>' in raw:
        # The optional introduction has been moved as raw markup; normalize its copied payload too.
        if any(a<=p.parser.spans[(n.sourceline,n.sourcepos)][0]<b for a,b,_,_ in p.edits):continue
        p.replace(n,raw.replace('</br>',''),'修正無效br關閉標籤')
# The moved optional source is normalized before insertion, not by a global HTML replacement.
p.edits=[(a,b,new.replace('</br>','') if reason=='將課後活動集中於既有區塊' else new,reason) for a,b,new,reason in p.edits]

p=pages['CH3-1.html']
p.p('從下方工作演練','選同一案例的三份文件，做成 FAQ、交接摘要或待辦清單其中一種。每人使用自己的帳號與材料完成。',selector='#lesson-start p')
p.p('先取得完整來源／資料','<a href="#workplace-practice">選材料，開始加入來源 →</a>　<a href="#lesson-check">完成檢查 →</a>',selector='#lesson-start p')
p.p('每人獨立選一組','可選教育行政、服務交接，或自己同一件工作中的三份文件。下方新聞、公告與書籍素材供課後選做。')
setup='<ol><li>展開下方所選案例的第一份文件，按「複製全文」。</li><li>開啟筆記本工具，登入自己的帳號，建立一個新筆記本。</li><li>在來源區選「新增來源」，選擇貼上文字的方式，把剛才的全文貼入。</li><li>將來源命名為材料標題，例如「DA1排課規範」。完成加入後，點開它，確認第一段與原文一致。</li><li>用相同方法加入該案例的第二、三份文件。來源列表應有三個名稱，三份都能讀到原文。</li></ol>'
p.p('先展開下方A或B','先選下方一組文件，再'+link('https://notebooklm.google.com/','開啟 NotebookLM／Gemini Notebook')+'。加入第一份來源的方法如下：'+setup+paragraph('若來源為空或名稱重複，先回本頁重新複製完整文字，分開加入。尚未能登入或建立筆記本時，請講師協助；三份可讀後才開始提問。'))
# Replace the preceding paragraph with valid block siblings rather than putting ol inside p.
p.edits[-1]=(p.edits[-1][0],p.edits[-1][1],paragraph('先選下方一組文件，再'+link('https://notebooklm.google.com/','開啟 NotebookLM／Gemini Notebook')+'。先練習加入第一份來源：')+setup+paragraph('來源列表應有三個可辨認的名稱，三份都能讀到原文。來源為空時回本頁重複製，尚未能登入時請講師協助；確認三份可讀再提問。'),'補來源加入的完整操作橋接')
p.text('#workplace-practice h3','先練一次：回答有沒有原文支持？',prefix='引用支持')
p.p('來源是加入筆記本','來源就是你加入的原文；引用是回答旁邊可點回原文的標記。要核對的「主張」，就是回答中一句可以查證的話。例如原文寫「1工作天首次回覆」，只能證明回覆期限，不能寫成「1工作天結案」。')
p.p('先看文件狀態','文件較新不一定能改規定。先看是否正式核准、適用哪個期間與對象。排課案的會議只是建議20人，沒有核准容量變更，不能直接取代公告的18人。')
p.p('主張核對時','選三句重要回答，點旁邊引用，確認原文是否支持。可標「支持」「只支持部分」「沒寫」「文件互相矛盾」。自己的推論放建議區並標明，不能寫成已核准規定。')
demo=p.node('#workplace-practice p','主張核對時')
small=paragraph('<strong>看一筆核對：</strong>回答說「R教室可收20人」。點該句旁的引用，來源會議記錄寫「建議調至20人」，公告仍寫18人。這筆應記「20人尚未核准；先依公告18人，請教務確認容量變更」。')+paragraph('把這次看到的資料直接貼入「實際引用回查」：自己的筆記本網址、點到的引用標記、來源名稱、支持句，以及上述判斷。引用數字依你當次畫面填，不能抄示範代號。再以同樣方法核對另外兩句。')
p.insert_after(demo,small,'先示範一筆引用核對，再作自己的三筆')
for prefix,new in [
('U3-SOURCE：','1. 加入三份來源。照上方方法操作，將筆記本網址與三個來源名稱留在工作台。讀不到時重新加入完整文字。'),
('U3-CLAIM：','2. 產生一份成品。選 FAQ、交接或待辦提示詞之一送出。把實際提示詞與第一版貼回工作台；應有選定格式及重要句子的引用。'),
('U3-CITE：','3. 核對三句。點各句旁的引用，讀原文。將筆記本網址、來源名、引用標記、原文短摘與支持判斷貼回「實際引用回查」。匯出檔可能沒有可點引用，所以也要保留網址和原句。'),
('U3-COMPARE：','4. 留下尚不能回答的事。排課案核對容量18／20人及R教室3天／一般5天；服務案分清首次回覆與結案，以及已登記但尚未回覆。只查自己的一案，把差異、待確認和詢問角色留在成品。'),
('U3-REPAIR：','5. 修一次。送修訂提示詞，保存修正版與理由。仍有錯就依原文手動修正並標明。第一版已正確時，記下核對依據，不必故意製造錯誤。'),
('U3-SAVE：','6. 保存。匯出工作台，在下載資料夾重開，確認三筆回查、第一版、修訂成品及未解問題都在。找不到檔案先查下載位置；不能暫存時立即匯出或列印。')]:p.inner(p.node('#workplace-practice li',prefix),new,'簡化來源查核操作')
p.p('下方展示實跑錯句','注意兩種狀態：「原文沒寫結案」表示不知道是否結案；「原文寫首次回覆尚未寄出」表示已知還沒寄出。請評估也不等於正在評估。下方範例示範如何回查和修句。')
p.p('你仍只提交','先送一次修訂，再逐句核對；殘留錯誤可依原文人工修正。模型版與人工版都保留。首版已正確時，記「無差異」與依據即可。')
p.p('成品中有同一情境','作品要讓接手者知道依據和下一步。完成後依頁尾清單核對，再下載保存。')
p.p('自己隔開提示詞','下次改用自己單位的規範、公告與會議記錄，先確認它們在說同一件事。課程的模擬規定只用於練習。')
p.p('NotebookLM不可用時','<strong>現在無法使用：</strong>下載所選三份原文，用'+link('assets/workplace/documents/fallback.md','工作文件離線備援')+'人工核對，成品註明「平台待重跑」。'+paragraph('<strong>工具恢復後：</strong>加入原來三份來源，送已保存提示詞，點實際引用核對後再匯出。短來源可能引用整份文件，仍要找出支持句。操作名稱不同時查閱'+link('https://support.google.com/gemininotebook/answer/16215270?hl=zh-Hant','官方新增來源說明')+'。'))
# Split this multi-topic paragraph at its DOM span into valid sibling paragraphs.
a,b,new,reason=p.edits[-1];p.edits[-1]=(a,b,new.replace('<p class="body-text"><strong>工具恢復後：','</p><p class="body-text"><strong>工具恢復後：').replace('</p></p>','</p>'),'拆開無法使用與恢復操作')

p=pages['CH4-1.html']
p.p('先到下方工作演練','選補訓或行政交接一案，完成一頁建議。每人獨立使用自己的資料與帳號操作。',selector='#lesson-start p')
p.p('先取得完整來源／資料','<a href="#workplace-practice">選一個決策案例 →</a>　<a href="#lesson-check">完成檢查 →</a>',selector='#lesson-start p')
p.text('.lesson-start-copy','選一個案例，讀完整資料，比較兩方案。再改一項限制，保存前後建議。')
p.p('每人獨立選A','選補訓、行政交接，或自己已有兩方案資料的需求。若沿用前章成果，只取已核對的背景與限制；沒有資料的工時標為估計。生活題供課後選做。')
p.p('先展開所選完整brief','展開你選的案例，讀限制與兩方案數字。複製完整資料，貼在「兩方案比較」提示詞下方，再送到自己的對話工具。回答應比較兩個方案；資料沒有的數字標待確認。')
p.p('複製下方提示詞，後接','下方提示詞先做第一輪比較。接上所選案例的完整文字，包含限制、優先順序與待確認；不要只貼表格。保存這份完整提示詞與第一版。')
for prefix,new in [
('U4-FRAME：','1. 選一案起稿。貼上完整資料與比較提示詞。回答應列出兩方案、不能超過的限制及三項優先標準。'),
('U4-TRADEOFF：','2. 看比較。先核對算式，再看三項標準、推薦方案及要放棄什麼。只說「效率較高」時，要求用原資料說明。'),
('U4-MISSING：','3. 驗算自己的案例。補訓案檢查座位、授課加準備時間；交接案分開檢查兩位窗口的每週時間、一次設定與10分鐘人工查核。缺資料直接留在建議中。'),
('U4-CHANGE：','4. 只改一項限制。補訓案把講師上限240改成228分鐘；交接案只把文件窗口30改成25分鐘／週，使用窗口仍30。其他條件不變。若回答偷偷改人數或刪查核，修一次，仍錯就依原文人工整理。'),
('U4-DECIDE：','5. 寫修訂建議。指出新限制改到哪個算式、要選哪個方案、代價與仍待確認的事。兩者都不合格時，寫「目前無可行方案」，指出要請主管調整什麼。'),
('U4-SAVE：','6. 保存。把完整提示詞、第一版、改條件指令及修訂版貼回工作台，匯出後從下載資料夾重開。確認算式、限制與下一步仍在。不能暫存時立即匯出或列印。')]:p.inner(p.node('#workplace-practice li',prefix),new,'簡化方案比較操作')
p.text('[data-gamma-copy-status]','展開所選案例即可複製完整資料或提示詞。')
p.p('第一輪先依原限制','先按原限制比較，再按新限制重新判斷。補訓案是240改228分鐘；交接案只有文件窗口30改25分鐘／週。主管要看的結果貼到「修訂決策卡」，前後版仍留在工作台。')
p.p('若正文過長','把修訂建議放入下方一頁模板，開啟文件工具的列印預覽。確認正文一頁、字能讀、算式與待確認都在。過長時先用精簡提示整理一次，再檢查；未看預覽就標「一頁草稿」。不另做手動逐字計數作業。')
p.p('2026-10-08授課帳號','模型拒答、文字破損或精簡後仍太長時，保留原回答，依已核對資料手動填一頁模板，標明「人工整理」。不必反覆送出同一個失敗指令。')
p.p('人工恢復時','人工整理只驗算自己的一案：補訓案兩場集中班需240分鐘，超新上限12分鐘；三場小班需225分鐘，尚餘3分鐘。交接案文件窗口的人工方式需20分鐘／週，工具方式需30分鐘／週，後者超新上限5分鐘；使用窗口25／15分鐘均未超30。保留10分鐘人工查核，不能刪掉來湊額度。算式不清楚時請講師協助。')
p.p('A原上限240分鐘時','補訓案原上限240分鐘時，可先選兩場集中班；改228後，應改三場小班，並確認上課安排。交接案原額度下可先選工具方式；文件窗口改25分鐘後，應改人工方式。以下參考供你完成後核對計算與理由，不當成自己的模型輸出。')
p.p('一份可交付建議至少','一頁建議要讓主管看出選擇理由與成立條件。完成後依頁尾清單核對；填寫進度不表示算式正確或已核准。')
p.p('自己只看成品，說出','帶回單位使用時，換成真實需求和兩方案資料，確認工時是估計或實測、設定是否核准，再提出建議。')
p.p('工具不可用或精簡拒答','工具不能用時，先用'+link('assets/workplace/decisions/fallback.md','決策離線備援')+'計算並填一頁模板，標「模型待重跑」。恢復後送原資料與兩輪提示詞，保存真回答。想練自己的單位需求，可用'+link('assets/worksheets/course-capstone-handoff.md','課後短交接')+'，沿用已完成資料。')
p.p('同一需求至少兩方案','檢查：兩方案與三項標準都有比較；限制有算式；只改一項條件後重新判斷；取捨、待確認與下一步都在；正文已預覽為一頁；匯出檔能重開。人工整理或模型待重跑請如實標記。',selector='#lesson-check p')
for n in p.body.select('details > summary'):
    if n.get_text().startswith('A完整補訓'):p.inner(n,'補訓案：兩場集中班與三場小班','以案例名稱代替單獨字母')
    elif n.get_text().startswith('B完整行政'):p.inner(n,'交接案：人工方式與工具方式','以案例名稱代替單獨字母')

p=pages['PRAC2-1.html']
p.text('.lesson-tagline','CH2 後半演練｜從完整企劃做出自己的十頁工作提案。')
p.p('開始前，確認你的 LLM','開始前，確認文字對話工具能送出與複製回答，Gamma 能登入與建立內容。收到回答後用下方文字存檔區下載，檔案會放到瀏覽器的下載資料夾。')
anchor=p.node('#gamma-source p','開始前，確認你的 LLM')
save='''<div class="prac-box" id="gamma-save"><h3>文字存檔區：貼上、下載、重開</h3><p class="body-text">複製企劃或模型回答的全文，貼入下方。選擇檔案用途，按「下載文字檔」。到下載資料夾開啟剛下載的檔案，確認全文還在。這裡不會產生 AI 回答，也不會自動保存貼入文字，離開前先下載。</p><div class="wb-field"><label for="gamma-save-kind">我要保存的檔案</label><select id="gamma-save-kind"><option value="企劃.txt">來源企劃</option><option value="10頁大綱.md" selected>十頁大綱</option><option value="Gamma貼入文字.txt">Gamma 貼入文字</option></select></div><div class="wb-field"><label for="gamma-save-content">貼入全文</label><textarea id="gamma-save-content" rows="10" placeholder="貼上完整文字後再下載"></textarea></div><button class="nav-btn" id="gamma-save-download" type="button">下載文字檔</button><p class="body-text" id="gamma-save-status" role="status" aria-live="polite"></p></div>'''
save=save.replace('id="gamma-save-content" rows=','id="gamma-save-content" style="width:100%;max-width:100%;box-sizing:border-box;padding:12px;font:inherit" rows=')
p.insert_after(anchor,save,'補一個純文字下載區，示範保存而不增加學員作業')
p.p('開啟 outline.txt','開啟'+link('assets/workplace/gamma/prompts/outline.txt','十頁大綱提示詞')+'，複製全文，接上所選企劃全文後一次送出。課程案例使用P01–P10；自帶企劃沒有編號時，使用原文小標題與短摘對照，不能補造編號。',selector='#gamma-outline p')
p.p('等待回答後，保存為','收到回答後，複製全文到<a href="#gamma-save">文字存檔區</a>，選「十頁大綱」並下載。在下載資料夾打開 <code>10頁大綱.md</code>，確認第1至10頁都在。每頁應有標題、主旨、要點、版面建議與來源；核對清單留在檔案中，不算第11頁。')
p.p('逐頁看它引用的 P','逐頁回到來源查看數字、期間、角色與狀態。選報表案時查第4／5頁基準；選交接案時查六題、四週與兩位窗口的預計安排。自己的企劃用小標題與原句核對。只檢查自己選的一案。')
p.p('保存結果為自己的','收到十段文字後，複製全文到<a href="#gamma-save">文字存檔區</a>，選「Gamma 貼入文字」並下載。重開 <code>Gamma貼入文字.txt</code>，確認有十個頁面區塊，中間九行 <code>---</code>。來源與製作說明留在大綱，不貼成投影片。')
p.p('實際試跑的大綱曾','每頁整理成2–4個要點；要點太多時合併同一意思，不能刪掉會影響核准的條件。文字仍密時，可在 Gamma 分行或改表格，匯出後再看是否可讀。')
p.p('在訊息輸入框貼入','若首頁有訊息輸入框，貼上生成指令，再接自己的十段文字並送出。這個對話式生成入口可能叫 Agent；看到十張大綱後先核對，再生成。若它改了事實，回覆要求保留原文字與條件。')
p.p('選擇貼上文字，貼入','若介面提供「使用經典生成器」，選貼上文字，接自己的十段內容。指定簡報、十張卡片與繁體中文，文字處理選 Preserve／保留。若轉進訊息介面，就用上一條路徑；只做自己畫面提供的一條。')
p.p('你若使用完整模擬案例','下次用自己的工作企劃時，先改讀者、希望核准的事與資料。例如從「請主管核准試行」改成「交給窗口執行」，簡報中的請求、方法與下一步也要跟著調整。')
# Generate exact revised source payloads and then synchronize their inline copies.
assets={}
f='assets/workplace/gamma/prompts/outline.txt';s=(BACKUP/f).read_text();s=s.replace('來源對應：引用企劃P01至P10章節編號，必要時列多個。','來源對應：課程案例引用企劃P01至P10章節編號；自帶企劃沒有這些編號時，使用原文小標題並附支持短句。沒有標題時直接摘錄支持句，不捏造編號。必要時列多個來源位置。');assets[f]=s
f='assets/workplace/gamma/checks/quick-check.md';s=(BACKUP/f).read_text().replace('每頁可回到所選企劃 P01–P10；','每頁可回到所選企劃的 P01–P10，或自帶企劃的小標題／支持原句；');assets[f]=s
for f in ['assets/workplace/decisions/prompts/compare.txt','assets/workplace/decisions/prompts/change.txt','assets/workplace/decisions/prompts/one-page.txt']:
    s=(BACKUP/f).read_text()
    s=s.replace('字數由本人核對，列印是否一頁另用預覽驗。','450漢字只作精簡參考，不要求學員人工逐字計數；用列印預覽確認正文一頁且可讀。')
    s=s.replace('列印頁數由本人另驗。','用列印預覽確認正文一頁且可讀。')
    s=s.replace('字數需由我自行核對，列印一頁需用預覽驗。','450漢字只作精簡參考，不要求學員人工逐字計數；以列印預覽確認正文一頁且可讀。')
    s=s.replace('A原上限240分鐘；B文件／使用原上限各30分鐘／週','補訓案原上限240分鐘；交接案文件／使用原上限各30分鐘／週')
    s=s.replace('本輪A只改講師上限228分鐘；B只改文件窗口25分鐘／週','本輪補訓案只改講師上限228分鐘；交接案只改文件窗口25分鐘／週')
    s+='\n請以案例和方案的完整名稱稱呼：補訓案用「兩場集中班／三場小班」，交接案用「人工方式／工具方式」，不單獨用A或B。\n'
    assets[f]=s
for name, mappings in [('PRAC2-1.html',{'outline-prompt':'assets/workplace/gamma/prompts/outline.txt','quick-check':'assets/workplace/gamma/checks/quick-check.md'}),('CH4-1.html',{'prompt-compare':'assets/workplace/decisions/prompts/compare.txt','prompt-change':'assets/workplace/decisions/prompts/change.txt','prompt-one-page':'assets/workplace/decisions/prompts/one-page.txt'})]:
    p=pages[name]
    for nodeid,f in mappings.items():
        candidates=p.body.select('#'+nodeid)
        if not candidates and nodeid=='outline-prompt':candidates=p.body.select('#prompt-outline')
        assert len(candidates)==1,(name,nodeid)
        node=candidates[0];code=node.find('code');p.inner(code or node,html.escape(assets[f].rstrip()),'同步頁內提示與下載原檔')

# Simplify chapter entry summaries without changing navigation.
p=pages['index.html']
for card in p.body.select('.unit-card'):
    label=card.select_one('.unit-label').get_text()
    desc=card.select_one('.unit-desc')
    texts={'CH1':'選一份原文，完成自己的工作短文，核對後修一次。','CH2':'寫自己的 Email、短訊息與改寫版，再把完整企劃做成十頁 Gamma 簡報。','CH3':'用三份工作文件產生答覆，點引用查原文，留下待確認事項。','CH4':'比較兩方案，改一項限制後重新判斷，完成一頁建議。'}
    for chapter,text in texts.items():
        if label.startswith(chapter):p.inner(desc,text,'簡化課程入口說明')
for sid,new in {'ch1-1':'選一份工作原文，完成一份短文；核對後修一次並保存。','ch2-1':'寫自己的 Email、短訊息與改寫版，再做十頁 Gamma 提案。','ch3-1':'用同一工作中的三份文件，做一份有依據的 FAQ、交接或待辦。','ch4-1':'比較兩個工作方案，改一項限制後重新判斷，提出一頁建議。'}.items():
    p=pages['module1.html'];section=p.node('#'+sid)
    for n in section.find_all('p',recursive=False):
        if not n.find('a') and not n.find_parent('details'):
            p.inner(n,new if not n.get_text().startswith('180分鐘') else '3 小時｜完成自己的作品，保存後重開確認。','簡化單元入口')
            break
    for n in section.find_all('p',recursive=False):
        if n.get_text().startswith('180分鐘'):p.inner(n,'3 小時｜完成自己的作品，保存後重開確認。','內部時間安排留教案')
for n in pages['module1.html'].body.select('p'):
    if n.get_text().startswith('用自己的真實單位需求'):
        pages['module1.html'].inner(n,'選下週會遇到的一項工作，沿用相關單元的成果即可。換成自己的資料與讀者，不必重抄四份表。','簡化課後整合說明')

# Preserve all existing scripts and append only the local plain-text download behavior.
DOWNLOAD_SCRIPT='''<script id="gamma-text-save-script">
(function () {
  const button = document.getElementById('gamma-save-download');
  const input = document.getElementById('gamma-save-content');
  const kind = document.getElementById('gamma-save-kind');
  const status = document.getElementById('gamma-save-status');
  if (!button || !input || !kind || !status) return;
  button.addEventListener('click', function () {
    if (!input.value.trim()) { status.textContent = '請先貼上全文，再下載。'; input.focus(); return; }
    const url = URL.createObjectURL(new Blob([input.value], {type: 'text/plain;charset=utf-8'}));
    const a = document.createElement('a');
    a.href = url; a.download = kind.value; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    status.textContent = '已送出下載：' + kind.value + '。請到下載資料夾重開確認全文。';
  });
})();
</script>'''
p=pages['PRAC2-1.html'];scripts=p.soup.find_all('script');last=scripts[-1]
p.insert_after(last,DOWNLOAD_SCRIPT,'加入純文字下載，不變更既有複製功能')

rendered={name:p.render() for name,p in pages.items()}
changes=[]
for name,p in pages.items():
    for a,b,new,reason in p.edits:
        changes.append({'file':name,'line':p.source.count('\n',0,a)+1,'reason':reason,'before':p.source[a:b],'after':new})
(OUT/'CONTENT-CHANGES.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')

if '--apply' not in sys.argv:
    print('prepared',len(changes),'DOM changes; use --apply after backup and review')
    sys.exit(0)
manifest=json.loads((OUT/'baseline.json').read_text())
for f,sha in manifest['files'].items():
    assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==sha,('changed since backup',f)

# Update the formal lesson source before HTML: preserve frontmatter/internal notes,
# replace only the delimited learner section with the exact revised HTML content.
for name in ['CH1-1.html','CH2-1.html','CH3-1.html','CH4-1.html','PRAC2-1.html']:
    lesson=name.replace('.html','-LESSON-PLAN.md');source=(BACKUP/lesson).read_text()
    soup=BeautifulSoup(rendered[name],'html.parser');body=soup.select_one('.lesson-body')
    heading=soup.find('h1').get_text(' ',strip=True)
    note='\n## 2026-10-09 教師修訂說明\n\n學員頁依已同意的閱讀審查修訂。下方 learner-content 是本次正式正文，保留原文、提示詞與工作台欄位。版本相容與試跑紀錄留教師區，不要求學員另填表。四章各三小時、Gamma在CH2後半，時間仍待真人試跑；不得把本次文字修改當作平台或真人驗證完成。\n\nCH4的450漢字僅作模型縮稿參考，成品以實際列印一頁、內容可讀與算式／待確認完整檢查。CH2補限制試一次仍錯可依原文人工收尾。Gamma自帶企劃以小標題或支持原句定位，另可用頁內文字下載區存檔。\n\n'
    if name!='CH4-1.html':note=note.replace('CH4的450漢字僅作模型縮稿參考，成品以實際列印一頁、內容可讀與算式／待確認完整檢查。','')
    a=source.index('<!-- learner-content:start -->');b=source.index('<!-- learner-content:end -->')
    replacement='<!-- learner-content:start -->\n# '+heading+'\n\n'+body.decode_contents()+'\n<!-- learner-content:end -->'
    (ROOT/lesson).write_text(source[:a]+note+replacement+source[b+len('<!-- learner-content:end -->'):])
for f,s in assets.items():(ROOT/f).write_text(s)
for name,s in rendered.items():(ROOT/name).write_text(s)
(ROOT/'assets/workplace/gamma/examples/.gitignore').write_text('# Classroom reference PDFs must be included in course releases.\n!case-a-gamma.pdf\n!case-b-gamma.pdf\n')
print('updated',len(rendered),'HTML pages, 5 lesson sources,',len(assets),'source assets')
