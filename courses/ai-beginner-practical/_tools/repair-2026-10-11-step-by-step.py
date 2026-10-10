#!/usr/bin/env python3
"""Apply the approved readability repair using DOM anchors and source spans."""
from pathlib import Path
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import hashlib, html, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / '_backup/2026-10-11-pre-step-by-step'
OUT = ROOT / '_repair/2026-10-11-step-by-step'
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

def steps(rows):
    return '<div class="steps-wrap">'+''.join(
        f'<div class="step-block" id="{sid}"><div class="step-circle">{i}</div><div class="step-content"><div class="step-heading">{i}. {title}</div><div class="step-body">{body}</div></div></div>'
        for i,(sid,title,body) in enumerate(rows,1))+'</div>'

def prompt_box(sid, title, text, path=None):
    download=f'<a download href="{path}" target="_blank" rel="noopener">下載文字檔</a>' if path else ''
    return f'<details class="workbench-disclosure"><summary>{title}</summary><p><button class="wb-action" data-gamma-copy="{sid}" type="button">複製完整提示詞</button><span data-copy-status="" role="status"></span> {download}</p><pre class="code-block" id="{sid}">{html.escape(text)}</pre></details>'

def label(p,field,title,example):
    node=p.node('[data-field="'+field+'"]')
    p.text('label[for="'+node['id']+'"]',title)
    if node.name=='select': return
    raw=p.raw(node)
    opening=raw[:raw.index('>')+1]
    if 'placeholder=' in opening:
        opening=re.sub(r'placeholder="[^"]*"',lambda m:'placeholder="'+html.escape(example,quote=True)+'"',opening)
    else: opening=opening[:-1]+' placeholder="'+html.escape(example,quote=True)+'">'
    p.replace(node,opening+raw[raw.index('>')+1:],'欄位範例與步驟對應')

pages={f:Page(f) for f in ['index.html','module1.html','CH1-1.html','CH2-1.html','CH3-1.html','CH4-1.html','PRAC2-1.html']}
assets={}

# CH1: keep each original case; provide an assembled starting prompt per case.
p=pages['CH1-1.html']
contexts=[('青禾學習中心行政人員；短文給已報名的成人學員看','課前提醒','150字以內，待確認另外列出'),('安行服務站窗口；短文給反映照明故障的民眾看','受理回覆','100字以內，待確認另外列出'),('業務支援人員；摘要給主管看','週工作摘要','已完成／待處理／需主管協助三段，每段最多兩點；待確認另列')]
ready=[]
for c,(context,task,fmt) in zip('abc',contexts):
    source=(ROOT/f'assets/workplace/tasks/case-{c}.txt').read_text().strip()
    text=f'請協助我完成以下工作。\n情境：{context}。\n任務：請寫一份{task}。\n資料：\n{source}\n條件：只使用上述原文。保留日期、狀態、件數與必要行動；未提供的資訊標待確認，不增加電話、核准、承諾或完成狀態。\n格式：{fmt}。\n請直接產出短文，不要只說明做法。'
    path=f'assets/workplace/tasks/ready-{c}.txt';assets[path]=text+'\n'
    ready.append(prompt_box('ready-'+c,c.upper()+'：已填好的起稿提示詞（選一案即可）',text,path))
p.insert_after(p.node('#workplace-practice h3', '三種單位材料'),paragraph('第一次操作，選最接近工作的 A、B 或 C 即可。下方保留完整原文；到了「步驟2」，使用該案已填好的提示詞。三案不用全部做。自備資料的替換方法放在提示詞後。'),'說明案例與起稿入口')
p.p('先開啟課前與講師確認', '開啟課前與講師確認可用的文字對話工具，依'+link('assets/fallback/text-llm-minimum-start.md','工具啟動卡')+'做一次送出與複製測試。這是確認帳號可用，避免寫好提示詞後才發現不能送出。本頁工作台只保存文字；AI 回答要在對話工具產生。')
ol=p.node('#workplace-practice > ol', '1. 看示範')
rows=[
('ch1-step-1','選一案，先讀原文', '<p>展開上方 A、B 或 C 的完整材料，讀完全文。A 給學員、B 給民眾、C 給主管；只選一案，目的是先練會處理一份資料。</p><p>在下方「工作台」的第一欄先寫案名，例如「A｜課前提醒」。讀完後，應能指出收件者與對方要做的事；A 是帶手機、需要借用時登記，B 是補照片，C 是讓主管掌握待處理工作。</p>'),
('ch1-step-2','準備一份能直接送出的提示詞', '<p>展開下方所選案的「已填好的起稿提示詞」，按「複製完整提示詞」。它已包含五欄與原文，第一次不用自行填方括號，能先看懂完整輸入的樣子。</p><p>回到自己的對話工具，開一個新對話，貼進輸入區。先不要送出：從頭看到尾，確認有「情境、任務、資料、條件、格式」，而且只有自己選的案例。</p>'),
('ch1-step-3','送出，留下提示詞與第一版', '<p>按對話工具的送出按鈕，等回答完成。先複製自己送出的提示詞，回'+link('#practice-workbench','工作台')+'第一欄，接在案名下方；再複製回答，接著寫「第一版：」並貼入全文。兩段都保留，之後才知道是什麼指令產生這個回答。</p><p>確認第一欄同時有原文、提示詞與回答。若 AI 只教寫法，補送「請直接給完整短文，不要說明做法」；保留原回答，標明補送的指令。</p>'),
('ch1-step-4','對照原文，找出一個問題', '<p>把所選原文和第一版並排閱讀，先找日期、狀態或數量。A 看借用是否被保證；B 看登記是否被寫成修復；C 看不同階段件數是否被加成總客戶数。這些錯誤會影響收件者的行動。</p><p>在「要修正的一處」寫三句：原文寫什麼、回答寫什麼、錯用會造成什麼。例：「原文說借用待確認；回答說每人可借；學員可能不帶手機。」第一版正確時，寫自己核對的句子及「符合原文」，不用造錯。</p>'),
('ch1-step-5','只補一项要求，取得新版', '<p>回原對話，送出「只修一項的提示詞」。把方括號換成自己的原提示詞、第一版及剛找到的問題；其他原文、讀者與格式保持不變，才能看出這項要求造成的差異。</p><p>指令貼入「我送出的修正指令」，回答貼入「修正版完整短文」。若第一版已正確，改為確認一項重要條件，記下無差異與核對依據。重問一次仍錯，依原文手動改，標明「人工修正」。</p>'),
('ch1-step-6','再查新版，補上待確認與下一步', '<p>在「修改前後與核對依據」貼原句、新句及支持原文。新版仍要檢查其他日期與狀態，避免修一處卻改錯另一處。</p><p>A／B 依上方字數方法檢查正文，C 確認三段且每段最多兩點。把尚缺的資訊及詢問角色填入「還缺什麼、問誰」；把下一步填入「接下來做什麼」。例：「向行政窗口確認借用結果，確認後更新提醒；日期待確認」。</p>'),
('ch1-step-7','儲存，再確認重新整理後仍在', '<p>在工作台按「儲存到本機」，看到保存訊息後重新整理本頁，確認提示詞、第一版與修正版還在。這是檢查本機暫存，尚未產生可帶走的檔案。</p><p>若重整後遺失，回對話複製自己的版本，直接做下一步匯出；不要關閉仍有文字的對話。工作台的其他選做欄位不用填。</p>'),
('ch1-step-8','下載檔案，重開自己的成果', '<p>按工作台「匯出 Markdown」。開啟瀏覽器下載紀錄或下載資料夾，找到 <code>unit1-practice-sheet-complete.md</code>，用文字編輯器開啟。<code>.md</code> 是文字檔；不會自動開啟時，使用「開啟方式」選文字編輯器。</p><p>在檔案中找到提示詞、第一版、修正版與下一步。這份檔案用來帶走與續做，和留在目前瀏覽器的暫存不同。缺内容時回工作台補齊，再匯出；只留修正版不能還原修改理由。</p>')]
p.replace(ol,''.join(ready)+steps(rows),'六項摘要改成八個操作階段')
p.insert_after(ol if False else p.node('#workplace-practice h3','把回答貼回'),paragraph('使用自己的原文時，展開上方通用「起稿提示詞」：把情境換成自己的單位與收件者；任務換成要寫的成品；資料欄整段換成獲准使用的原文；條件列不能新增的事；格式填字數或段落。刪掉括號內的提示文字，不混用案例日期或金額。送出前再讀一次五欄。'),'補自備資料替換方法')
p.p('起稿後貼回第一版','依上方步驟填工作台：第一欄保留完整提示詞與第一版；修正指令、修正版及核對依據各貼到同名欄位。最後要使用的作品在「修正版完整短文」。其他課後選做欄位可留空。')
p.p('按「儲存」後重新整理','這項檢查已在步驟7–8操作。現在重開 <code>unit1-practice-sheet-complete.md</code>，找出原文、第一版與修正版；若缺內容，回工作台補上再匯出。不用另外重填表格。')
label(p,'personalPrompt','我的案例、完整提示詞與第一版','案名：A｜課前提醒\n提示詞：貼完整五欄與原文\n第一版：貼自己的實際回答')
label(p,'revisionProblem','要修正的一處：原文、回答與影響','原文：借用待確認\n回答：每人可借\n影響：學員可能不帶手機；若原本正確，寫核對符合原文')
label(p,'revisionInstruction','我送出的修正指令','貼實際送出的完整指令；只指定本次一項要求')
label(p,'revisionResponse','修正版完整短文','貼新版全文；若自己修改，先標「人工修正」')
label(p,'revisionKept','修改前後與核對依據','原句：…\n新句：…\n依據：原文…；無差異時記下查過的句子')
label(p,'personalGap','還缺什麼、問誰','設備借用結果待確認；詢問行政窗口')
label(p,'personalNext','接下來做什麼','確認借用結果後更新提醒；負責角色與日期未提供則寫待確認')

# CH2: demonstrate actual reader change, retain prior tone demonstration as a separate skill.
p=pages['CH2-1.html']
p.insert_after(p.node('script[src="assets/learner-workbench.js"]'),'<script src="assets/gamma-practice.js" defer></script>','CH2完整提示詞使用既有複製功能')
p.text('.page-hero .lesson-start strong','先看完整 Email，再選自己的情境')
p.text('.page-hero .lesson-start-copy','從下方客戶信示範開始，依步驟產生自己的 Email、短訊息與新讀者版。做到哪一步，就把結果貼回工作台；不用先填完整张表。')
node=p.node('.page-hero .lesson-start-link')
p.replace(node,p.raw(node).replace('href="#communication-workbench"','href="#lesson-demo"').replace('開始填寫 →','看示範與開始操作 →'),'第一入口指向示範及操作流程')
client=p.soup.select('#lesson-demo pre')[0].get_text().strip().replace('客戶詢問社群貼文方案。','我是阿凱，林小姐詢問社群貼文方案。')
client=client.replace('依序輸出主旨、正文、署名，','依序輸出主旨、正文、署名阿凱，')
manager='請把同一封客戶信改成給主管看的 Email。\n新讀者：主管。目的：請主管確認基礎方案與交付條件，再回覆客戶。\n必須保留：林小姐詢問社群貼文方案、每月12,000元、確認需求後約7個工作天交付、客戶每月貼文數與希望開始時間尚未確認。\n改動：先說需要主管確認的事，再列已知條件與待確認；不要再請主管回覆自己的貼文需求。\n只用原資料，不新增客戶已同意、主管已核准、折扣或開始日期。\n輸出主旨、正文、署名阿凱，160字內。\n以下是客戶信第一版：\n[貼上自己剛產生的第一版全文]'
message='背景：我是阿凱，林小姐詢問社群貼文方案。已知基礎方案每月12,000元，確認需求後約7個工作天交付；每月貼文數量與希望開始時間尚未確認。\n任務：寫一則給林小姐的工作訊息，請她回覆貼文數量與希望開始時間。\n限制：專業有禮，2至4句；只能使用上述資料，不編造截止日、折扣或交付保證。\n格式：直接給訊息正文，不放主旨、署名或長篇寒暄。'
for file,text in [('email-client',client),('email-manager',manager),('message',message)]: assets[f'assets/workplace/communication/{file}.txt']=text+'\n'
demo=prompt_box('ch2-ready-client','第一次練習：已填好的客戶 Email',client,'assets/workplace/communication/email-client.txt')+prompt_box('ch2-ready-manager','讀者轉換：給主管的指令與參考完成信',manager,'assets/workplace/communication/email-manager.txt')+paragraph('作者參考（不是你的模型回答）：主旨：請確認社群貼文方案回覆條件。主管您好：林小姐詢問社群貼文方案。已知基礎方案每月12,000元，確認需求後約7個工作天交付；客戶的每月貼文數量與希望開始時間仍待確認。請協助確認上述方案與交付條件，確認後我再回覆客戶。阿凱。')+paragraph('客戶版請林小姐補需求；主管版請主管確認回覆條件。收件者與下一步不同，價格與交期沒有改。上方「改得親切一點」則是同一讀者的語氣調整，兩種操作要分清楚。')+prompt_box('ch2-ready-message','第一次練習：同一件事的工作短訊息',message,'assets/workplace/communication/message.txt')
wraps=p.soup.select('#lesson-demo > .steps-wrap');assert len(wraps)==3
rows=[
('ch2-step-1','選情境，準備完整 Email 提示詞','<p>第一次可用上方「已填好的客戶 Email」；它是完整模擬案例，不需要先想題目。也可從'+link('assets/templates/unit2-communication-scenarios.md','Email 情境包')+'選一張，把方括號換成自己的資料。自己的資料不齊時寫待補，不借用模擬案例的日期或金額。</p><p>在工作台「我的 Email 情境」寫案名；讀提示詞四段，確認背景是給 AI 的已知資料、任務是要寫什麼、限制是不能做什麼、格式是答案長相。先看懂輸入，再送出。</p>'),
('ch2-step-2','送出 Email，保存自己的第一版','<p>開一個新對話，貼完整提示詞並送出。等回答完成，將送出的全文貼入「Email：完整提示詞」，回答貼入「Email：第一版全文」。第一版先保留，後面才能比較改寫。</p><p>回答應有主旨、正文與署名。只有写作建議時補送「請直接給整封 Email」；把補送文字接在原提示詞後，不覆蓋第一次回答。</p>'),
('ch2-step-3','核對信裡的事實與對方下一步','<p>逐句對照背景。模擬案例核對12,000元、約7個工作天、貼文數尚未確認；最後應請客戶回覆數量與希望開始時間。自己的情境則查自己的日期、數字及要求。</p><p>在「Email：核對與改寫理由」先寫「事實檢查：……」。新增日期或折扣時，補明「只用背景，未知寫待補」再試一次；仍錯就按原文手動改，並把人工更正與理由接在第一版後。事實正確才換讀者。</p>'),
('ch2-step-4','準備一則短訊息','<p>第一次可複製上方「同一件事的工作短訊息」，讓客戶補需求。使用自己的案例時，換成自己的收件者、事情與希望對方做的動作；指定2–4句，不放 Email 主旨。</p><p>這一步練短訊息的重點與行動，不能只把長信刪掉主旨。背景沒有截止日，就不要加「今天內回覆」。</p>'),
('ch2-step-5','送出短訊息，檢查能否直接使用','<p>把訊息提示詞送到文字對話工具。提示詞貼「短訊息：完整提示詞」，回答貼「短訊息：第一版全文」。在「短訊息：核對結果」寫是否2–4句、事實是否正確、收件者要做什麼。</p><p>若仍是長信，補「先講事情與下一步，2–4句，直接給訊息」一次。新增事實時依原文修正，保留原回答與人工版。</p>'),
('ch2-step-6','指定新讀者，送出改寫指令','<p>回原 Email 對話。模擬案例展開上方「給主管的指令」，把最後方括號换成自己的客戶信第一版全文，再送出。主管要確認方案，客戶要補需求，所以要改開頭與最後請求。</p><p>自己的案例選一位不同收件者，寫出他要知道什麼、希望他做什麼，以及不能改的日期、數字與狀態；不要只說「換個語氣」。指令和新回答都貼入「Email：改寫指令與新讀者版」。</p>'),
('ch2-step-7','比較兩版，確認讀者變了、事實沒變','<p>對照第一版與新讀者版。模擬案例應把「請客戶回覆需求」改為「請主管確認條件」，同時保留價格、交期與需求未確認。用自己的案例時查相同三件事：收件者、最後要求、不變事實。</p><p>在「Email：核對與改寫理由」接著寫「原讀者／新讀者／改了哪一句／保留哪些事實」。例：「客戶→主管；最後改請主管確認；保留12,000元與約7個工作天。」有漏項時按原文修，標明人工更正。</p>'),
('ch2-step-8','保存文字包，再開啟 Gamma 演練','<p>在工作台按「儲存到本機」，重新整理確認內容仍在；按「匯出 Markdown」，到下載紀錄開啟 <code>unit2-communication-pack-complete.md</code>。檔案應有 Email 第一版、短訊息及新讀者版，連同實際指令與核對理由。</p><p>接著開啟'+link('PRAC2-1.html','Gamma 十頁提案演練')+'。Gamma 使用另一份完整企劃，不把剛才的 Email 當企劃；這一步從「文字適合讀者」進一步練「提案適合主管判斷」。</p>')]
p.replace(wraps[0],demo+steps(rows),'示範真讀者轉換及八個操作階段')
for wrap in wraps[1:]:p.replace(wrap,'','合併舊必做摘要到單一流程')
p.inner(p.node('#lesson-demo .callout-body','Email 檢查：'),'<strong>停下來檢查：</strong>工作台已有自己的三份文字、實際指令與核對理由。若缺第一版，回對話複製；若新讀者版事實不符，依原文修正後再匯出。','同步檢查位置')
p.inner(p.node('#lesson-demo .callout-body','文字完成後：'),'<strong>下一個任務：</strong>文字包保存完成，再去 Gamma 選一份完整企劃。兩個任務的來源與保存檔案各自清楚，選做欄位可留空。','交代 Gamma 新輸入')
for field,title,example in [('emailPrompt','Email：完整提示詞','貼送出時的四段全文，包含背景資料'),('emailFirst','Email：第一版全文','貼第一版主旨、正文與署名；人工更正另列，不覆蓋原版'),('emailCheck','Email：核對與改寫理由','事實檢查：…\n原讀者：…／新讀者：…\n改了哪句：…\n保留事實：…'),('emailRevision','Email：改寫指令與新讀者版','改寫指令：貼實際指令\n新讀者版：貼完整信\n人工更正：有才填'),('messagePrompt','短訊息：完整提示詞','貼實際送出的背景、任務、限制與格式'),('messageFirst','短訊息：第一版全文','貼自己的2–4句訊息；更正版本另列'),('messageCheck','短訊息：核對結果','句數：…\n對方下一步：…\n事實是否符合原文：…')]:label(p,field,title,example)
p.text('label[for="ch2-email-scenario"]','我的 Email 情境')
# Replace obsolete references only in the help/optional labels, not in case materials.
for node in p.soup.select('#lesson-assets p, .ts-a, .lesson-body td, #lesson-assets .tool-list-item, details > summary, .step-heading'):
    text=node.get_text(' ',strip=True)
    if node in wraps or node.find_parent(class_='steps-wrap') in wraps:continue
    raw=p.raw(node); new=raw
    for old,newtext in [('工作台步驟4、6、7','Email、短訊息與課後自我介紹練習'),('工作台步驟 4、6、7 選情境與產出','步驟1選 Email 情境、步驟4準備短訊息；自我介紹供課後選做'),('從步驟 4 或示範步驟 2 重跑','回'+link('#ch2-step-3','Email 事實核對')+'修正'),('從步驟 4 重跑','回'+link('#ch2-step-3','Email 事實核對')+'修正'),('從步驟 6 重跑','回'+link('#ch2-step-5','短訊息檢查')+'修正'),('三個提示詞一起從步驟 7 重跑','回「課後自我介紹」重新送出三版提示詞'),('從步驟 7 重跑','回「課後自我介紹」重做'),('從步驟 8 重跑','回'+link('#ch2-step-6','指定新讀者')+'修正'),('選做步驟7：','課後選做：'),('選做步驟10：','課後選做：')]:new=new.replace(old,newtext)
    if new!=raw:p.replace(node,new,'具名入口取代舊步驟編號')

# Shared workspace wording: tell learners to fill fields as they produce outputs.
for name in ['CH2-1.html','CH3-1.html','CH4-1.html']:
    p=pages[name]
    p.text('.learner-workbench-note','工作台先留空；依下方操作步驟，把自己的提示詞與回答貼入指定欄位。這裡只保存文字，不會產生 AI 回答；課後選做欄位可留空。')

# CH3: examples are observations; the actual sequence generates an answer before citations.
p=pages['CH3-1.html']
p.p('先選下方一組文件，再','先選下方 A 或 B 一組文件。A 是排課答覆，第一次可做六題 FAQ；B 是服務交接，第一次可做一頁交接。下方先示範加入來源與判讀方法，真正操作依「步驟1」開始。三種成品只選一種，不混用兩組文件。')
p.replace(p.node('#workplace-practice > ol','展開下方所選案例'),'<details class="workbench-disclosure"><summary>先看加入來源的操作示範</summary>'+p.raw(p.node('#workplace-practice > ol','展開下方所選案例'))+'</details>','示範與個人操作分清楚')
p.p('選三句重要回答，點旁邊引用','以下先看作者示範，不用立刻找自己的回答。真正操作先在步驟4產生第一版，到了步驟5才點開引用。每句要查的是「來源支持全部、只支持部分、沒有寫，或文件互相矛盾」。')
p.p('把這次看到的資料直接貼入','示範紀錄可寫：「回答：R教室20人；原文：會議建議20人，核准公告18人；判斷：20人未核准，先依18人，請教務確認。」這是判讀寫法。實作時另加自己的筆記本網址、實際引用標記與來源名稱，不能抄作者代號當成自己點過的引用。')
p.p('選FAQ是讓新進同仁','FAQ 是讓新同仁快速找到答覆；交接是讓接手者知道現在做到哪裡；待辦是列動作、負責角色與期限。第一次可用 A＋FAQ 或 B＋交接，下方各有完整提示詞；在步驟4只送所選那一份，現在先看用途。')
rows=[
('ch3-step-1','建立自己的筆記本','<p>選 A 排課或 B 服務交接。開啟'+link('https://notebooklm.google.com/','NotebookLM／Gemini Notebook')+'，登入自己的 Google 帳號，選「建立新筆記本」。把名稱改成「我的排課FAQ」或「我的服務交接」；名稱讓你下次找得到自己的成果。</p><p>複製瀏覽器網址，填入工作台「我的筆記本名稱與連結」。成功時應進入空白筆記本，看到來源區與提問區；找不到入口或無法登入時先處理帳號，不把範例當自己的操作。</p>'),
('ch3-step-2','加入第一份完整來源','<p>回講義展開所選案第一份文件，按「複製全文」。回自己的筆記本，在來源區選「新增來源／Add sources」，選「貼上文字／Copied text」，貼入全文，再加入。來源名稱寫材料標題，例如「DA1排課規範」。</p><p>點開來源，確認標題、第一段與最後一段都在。完整加入才能保留適用範圍，不能只貼一個人數。若內容是空白，刪除空來源後重新複製；不要刪掉已正確的來源。</p>'),
('ch3-step-3','加入另外兩份，確認來源選取','<p>用相同方法加入同案第二、三份文件。A 是 DA1、DA2、DA3；B 是 DB1、DB2、DB3。三份放在同一筆記本，才有辦法比較規範、公告與會議的不同說法。</p><p>在來源列表勾選這三份，逐份點開檢查。把實際名稱與版本貼入工作台三個「同案例來源」欄位。成功時應有三份可讀的來源；意外混入其他案時先取消選取，再提問。</p>'),
('ch3-step-4','提問，取得第一版成品','<p>A 第一次展開「六題 FAQ 提示詞」；B 第一次展開「一頁交接提示詞」。按複製，在筆記本提問區貼上並送出；不要把這段提示詞加成來源。這一步是請 AI 整理你已加入的文件。</p><p>送出的全文貼入「我送出的成品提示詞」，回答貼「第一版成品」。確認成品格式正確，重要句子旁有引用標記。沒有引用時，請它「只根據已選三份來源回答，重要句子附引用」再試一次，仍沒有則標平台回查待補。</p>'),
('ch3-step-5','點開一筆引用，讀支持原文','<p>從自己的回答選一個會影響工作安排的句子：A 可先查 R教室容量，B 可先查首次回覆期限。點該句旁的引用標記，讀開啟的原文與來源名稱；引用標記是當次畫面的數字，不是 DA／DB 編號。</p><p>比較回答與原文的數字、期間及狀態。A 先看18人是否限定試辦期間，再看20人有無變更核准；B 看1工作天是首次回覆，不能變成結案。這是確認引用支持整句，而不只其中一個數字。</p>'),
('ch3-step-6','記下一筆，再獨立核對兩筆','<p>在「三句回答的引用核對」填：回答原句、當次引用標記、來源名稱／版本、原文短摘、自己的判斷。筆記本網址已在上方欄位，不用每筆重抄。例：「回答：R教室20人；引用：填自己畫面數字；來源：會議與核准公告；原文：建議20／公告18；判斷：20未核准」。</p><p>自己再選另兩句，照相同方法點引用查原文。A 可查申請期限及協助安排；B 可查結案期限及C017尚待回覆。只保存來源代號、沒有實際點查時，不能勾引用完成。</p>'),
('ch3-step-7','找出待確認，修成能用的版本','<p>查看三筆核對，將一個矛盾或沒寫的資訊記入「修正理由與待確認」。寫明問誰、問什麼；例：「請教務確認容量變更，確認前並列18／20的來源狀態」。較新的會議不自動等於核准。</p><p>回同一筆記本送「來源查核修訂提示詞」，把指令接在「我送出的成品提示詞」後，回答貼「修正版完整成品」。再次點查改動句；試一次仍錯時按原文人工修，標理由。原本已符合則保留並記無差異及依據。</p>'),
('ch3-step-8','保存，重開文字與來源','<p>按工作台「儲存到本機」，重整確認仍在，再按「匯出 Markdown」。到下載紀錄開啟 <code>unit3-notebooklm-reading-pack-complete.md</code>，確認第一版、修正版、三筆核對與待確認都在。</p><p>從檔案中的網址回自己的筆記本，再點一筆引用，確認能找到原文。文字匯出不會把 NotebookLM 的可點引用完整搬走，所以必須保留網址與原文摘句。要交接給別人時，另外確認對方能取得來源；不能存取時標「人工回查，平台待驗」。</p>')]
p.replace(p.node('#workplace-practice > ol','1. 加入三份來源'),steps(rows),'八階段正確操作順序')
for field,title,example in [('newsPrompt','我送出的成品提示詞','貼實際送出的 FAQ／交接／待辦提示詞；修訂指令接在後面'),('noticePrompt','第一版成品','貼自己的完整 FAQ／交接／待辦，保留原版'),('newsCitations','三句回答的引用核對','第1筆\n回答原句：…\n當次引用：…\n來源名稱／版本：…\n原文短摘：…\n判斷：支持／部分支持／沒寫／矛盾\n另兩筆使用相同寫法'),('newsRevision','修正理由與待確認','改了哪句、原文依據；一個未解問題，以及詢問角色與下一步'),('noticeImpact','修正版完整成品','貼修訂全文；自己整理時標人工修正，與原回答分開')]:label(p,field,title,example)

# CH4: teach both meaningful calculations, then use the learner's chosen case only.
p=pages['CH4-1.html']
p.p('把修訂建議放入下方一頁模板','完成步驟7的已核對修訂稿後，依步驟8放進文件、檢查一頁並保存 PDF。下方一頁模板只提供成品結構，不是另一份必填作業。過程版本留工作台，交給主管的文件只放最後建議。')
p.p('主管要看的結果貼到', '主管要看的結果貼到「修正版一頁建議」；完整提示詞、第一版及改條件指令仍留原工作台。') if any(n.get_text(' ',strip=True).startswith('主管要看的結果貼到') for n in p.body.select('p')) else None
calculation=paragraph('先看完整算式，再查自己的回答。只看一種案例的列就好；表中是作者驗算，不是你的模型回答。')+'''<table><thead><tr><th>案例與原限制</th><th>怎麼算</th><th>判斷與理由</th></tr></thead><tbody><tr><td>補訓：36人；講師最多240分鐘</td><td>兩場：2×18＝36席；2×(90＋30)＝240分鐘。三場：3×12＝36席；3×(60＋15)＝225分鐘。</td><td>兩者都合格。原偏好先看場次少，所以暫選兩場；代價是多15分鐘投入且沒有餘裕。交流已含授課，不能再加。</td></tr><tr><td>補訓：只改上限為228分鐘</td><td>兩場240−228＝超12分鐘；三場228−225＝餘3分鐘。</td><td>改選三場，接受多一場安排；可出席時段與缺席補課仍待確認。</td></tr><tr><td>交接：每位窗口每週最多30分鐘</td><td>人工：文件20≤30、使用25≤30；工具：文件30≤30、使用15≤30。設定30／60分鐘另列。</td><td>兩者每週均合格。先減使用窗口負擔，暫選工具；代價是文件多10分鐘、設定多30分鐘。工具的10分鐘查核已含30分鐘，不能再加。</td></tr><tr><td>交接：只把文件窗口改成25分鐘</td><td>人工文件20≤25；工具文件30−25＝超5分鐘。使用窗口25／15仍各≤30。</td><td>改選人工；不能刪10分鐘查核湊額度。一次性設定仍要主管安排，成效待量測。</td></tr></tbody></table>'''
rows=[
('ch4-step-1','選一份完整案例，讀原限制','<p>展開補訓或行政交接其中一案。先讀任務、不能超過的限制及主管的比較順序，把案名填入「我的案例／決策名稱」。補訓比較兩場集中班／三場小班，交接比較人工／工具方式。</p><p>本次第一輪只用原上限：補訓240分鐘；交接各窗口30分鐘／週。材料最後的「主管新增條件」先留第二輪，避免第一版直接跳過原條件。</p>'),
('ch4-step-2','把比較指令接上案例全文','<p>展開「完整比較提示詞」，按複製，貼入自己的文字對話工具新對話。接著回講義複製所選案例全文，貼在指令最後，再送出。AI 需要完整人數、時間及優先順序，只有案例名稱不能計算。</p><p>實際送出的全部文字貼入「完整提示詞與案例」，回答貼「第一版比較與建議」。確認回答包含兩方案、算式、至少三個比較標準及暫定選擇。</p>'),
('ch4-step-3','自己驗算，確認兩方案是否合格','<p>依上方算式表，只查自己一案。補訓從原文取場數、容量、授課與每場準備；先加每場時間，再乘場數。交接分別查文件窗口與使用窗口，不能用總工時代替個別額度，設定時間也不能塞進每週數。</p><p>在第一版後接「我的驗算：」及自己的算式。這是檢查模型，不照抄模型結論。有算錯就按原資料修正，標明人工更正。先過限制，才進下一步比較偏好。</p>'),
('ch4-step-4','依原優先順序，讀懂得到與放棄','<p>補訓先看場次少，再看總投入與每場交流；交接先看使用窗口，再看文件窗口與設定。確認兩方案使用同一標準與單位，不能只寫「效率好」。</p><p>在第一版建議下記一句理由：例如「兩場較少安排，但投入多15分鐘且沒餘裕」。自己的未知也保留，例如出席時段、設定核准或成效；假設工時不是實際已節省的時間。</p>'),
('ch4-step-5','只改一項限制，重新提問','<p>回同一對話，複製下方「改一項限制的修訂提示詞」並送出。補訓只把上限240改228分鐘；交接只把文件窗口30改25分鐘／週，使用窗口仍30。保留其他資料，才能知道改選是否由這項限制引起。</p><p>將指令貼「改了哪項限制：實際指令」，回答先貼「修正版一頁建議」。不用另開一個沒有原資料的對話；若換對話，須附原案例與第一版。</p>'),
('ch4-step-6','重算受影響部分，確認要不要改選','<p>補訓重算240與225是否符合228；交接只重查文件窗口20／30是否符合25。對照上方示範，查回答有没有偷改人數、時間或刪人工查核。</p><p>在修正版中明寫「原選什麼→新選什麼→哪項計算造成變化」。錯誤先補限制再試一次，仍錯依原資料人工整理。自己的真實案例若兩者都不合格，就寫目前無可行方案，不能硬選。</p>'),
('ch4-step-7','整理最後建議，保留必要條件','<p>只取已核對修正版，依下方'+link('assets/workplace/decisions/one-page-template.md','一頁模板')+'安排：決策與新限制、同欄比較、暫定選擇、得到／放棄、成立條件／待確認、下一步。不要把第一版與修改歷程一起交給主管。</p><p>正文貼回「修正版一頁建議」，下一步填「接下來由誰做什麼」。字太多時先縮重複解釋；需要 AI 縮稿時用下方「一頁格式提示詞」，將方括號換成已核對修訂稿和原案例，再核對一次，不刪算式與未知。</p>'),
('ch4-step-8','放入文件，檢查一頁並下載 PDF','<p>第一次可用'+link('https://docs.google.com/document/','Google 文件')+'：登入自己的 Google 帳號，建立空白文件，命名「我的方案建議」。複製剛才的最後建議，貼進文件；已有可用 Word 或其他文件工具，也可用相同的貼入與列印流程。</p><p>選「檔案→列印」，看預覽頁數。若環境直接下載 PDF，就開啟它看頁數；瀏覽器顯示列印預覽時，目的地選儲存為 PDF。確認只有一頁、數字及單位完整、文字可讀。超頁先回文件縮短重複解釋，不能靠把字縮得看不清楚。</p><p>將 PDF 保存為「方案建議.pdf」並重開，再核對算式、待確認與下一步。無法使用文件工具時先匯出文字，標「一頁草稿，頁數待驗」，不要把未驗頁數的文字算成正式一頁成品。'+link('https://support.google.com/docs/answer/143346?hl=zh-Hant','Google 文件列印說明')+'</p>'),
('ch4-step-9','保存過程，確認能重做','<p>按工作台「儲存到本機」，重新整理後確認版本還在，再「匯出 Markdown」。到下載紀錄開啟 <code>unit4-decision-card.md</code>，查完整提示詞、第一版、改限制指令、修正版與自己的驗算都在。</p><p>文字檔保留怎麼判斷與修改，PDF 是交給主管的最後建議；兩份都保留。只看這兩份，應能說出原限制、新限制與改選原因。缺資料回對應步驟補，不重新跑其他案例。</p>')]
p.replace(p.node('#workplace-practice > ol','1. 選一案起稿'),calculation+steps(rows),'完整驗算與一頁交付路徑')
p.p('先按原限制比較，再按新限制','第一輪看原限制，第二輪只改一項限制。完整過程存工作台；交付正文放「修正版一頁建議」，依上方步驟8檢查一頁。')
for field,title,example in [('fullPrompt','完整提示詞與案例','貼比较指令＋完整案例原文'),('firstAnswer','第一版比較與建議','貼第一版全文；後面接「我的驗算」與選擇理由'),('revisionInstruction','改了哪項限制：實際指令','原值：…／新值：…\n貼實際送出的改條件指令'),('revisedAnswer','修正版一頁建議','貼最後完整建議，保留算式、取捨、待確認與下一步；人工整理請標明'),('next','接下來由誰做什麼','動作：…\n負責角色：…\n日期未提供寫待確認\nPDF檔名／頁數：…')]:label(p,field,title,example)

# Gamma: keep the full proposals and prompts, rewrite the operating paragraphs.
p=pages['PRAC2-1.html']
def gamma_stage(sid, input_text, rows):
    nodes=p.soup.select('#'+sid+' > p.body-text')
    assert nodes, sid
    p.replace(nodes[0],paragraph('<strong>現在使用：</strong>'+input_text)+steps(rows),'Gamma 階段的輸入、動作、目的與結果')
    for node in nodes[1:]:p.replace(node,'','合併同階段操作摘要')

gamma_stage('gamma-source','一份完整企劃。這是新的提案任務，不使用 CH2 的 Email。',[
('gamma-source-1','選企劃，複製全文','<p>從下表選 A 報表改善、B 文件交接，或已備好的完整個人企劃。沒有自己的企劃，先選最接近工作的一案。展開本頁所選企劃，按「複製全文」，保留標題到P10，不只複製目的段落。</p><p>完整來源讓 AI 有方法、時程、人力與核准事項可用。A 不必先做 Excel，B 的文件是核准後才取得的試行材料；本次每人獨立製作簡報，不找同學扮演窗口。</p>'),
('gamma-source-2','讀目的與請求，保存來源','<p>先讀 P01 和 P10，說出要請誰核准什麼。A 是部門主管核准四週報表試行、兩位窗口與檢討；B 是單位主管核准四週文件交接試行、兩位窗口及暫定投入。自己的企劃要有相同的明確請求。</p><p>把全文貼到下方文字存檔區，選「來源企劃」，按「下載文字檔」。到下載紀錄開啟 <code>企劃.txt</code>，確認標題、P01與P10都在。來源先留一份，後面改錯時才有基準可查。</p>'),
('gamma-source-3','確認兩個工具都能使用','<p>文字對話工具應能送出與複製；另開'+link('https://gamma.app/','Gamma')+'並登入自己的帳號，確認能建立簡報。找不到入口時請講師協助；有付費提示或額度不足時先保存文字成果並標「Gamma待補」，本課不要求升級。</p><p>本頁文字存檔區只下載文字，不會送給 AI，也不會自動保存。下一步先看主管需要的資訊，再依「產生大綱」操作。</p>')])
p.p('複製企劃或模型回答的全文','這是三個階段共用的下載工具。①複製來源或回答全文，貼入「貼入全文」。②選檔案用途：來源企劃、十頁大綱或 Gamma 貼入文字。③按「下載文字檔」。④到下載紀錄重開檔案，查看第一段和最後一段。每次先保存目前成果，再用新內容取代輸入框；此處不會自動保存。')
gamma_stage('gamma-outline','剛保存的 <code>企劃.txt</code>。產出：<code>10頁大綱.md</code>；供你核對內容，不直接全部貼入 Gamma。',[
('gamma-outline-1','把大綱指令接上完整企劃','<p>展開本節「十頁大綱提示詞」，按「複製全文」。在文字對話工具開新對話，貼指令；游標放到「以下是完整企劃：」下一行，再貼所選企劃全文，接著送出。只有提示詞沒有企劃時，AI 無法整理你的提案。</p><p>送出前看最後一段，應是自己企劃的核准請求；不要把 A 與 B 混在同一次輸入。</p>'),
('gamma-outline-2','保存回答，確認有十頁','<p>等回答完成，複製全文，貼入文字存檔區。選「十頁大綱」，下載並重開 <code>10頁大綱.md</code>。找到第1到第10頁，封面與核准事項也算在內；最後的來源清單不是第11頁。</p><p>缺頁或多頁時，回原對話要求「只重整為十頁，封面與核准事項計入，不增加新事實」。保留第一次回答；再試一次仍不符，可依已有内容人工調整並標明。</p>'),
('gamma-outline-3','依每頁來源，核對數字與狀態','<p>看每頁的「來源對應」，回所選企劃的對應小節。逐頁查重要數字、單位、角色、期間與核准事項；自己的企劃用原文小標題或支持句定位，不必造 P 編號。</p><p>A 看「9,601元待確認」有没有變成損失；B 看「預計六題問答」有没有變成已完成。四週與窗口安排都應保留原文狀態；新增採購零元也不能變成沒有任何工時成本。核對後保存修正版大綱，下一步才轉十段文字。</p>')])
gamma_stage('gamma-text','已核對的 <code>10頁大綱.md</code>。產出：<code>Gamma貼入文字.txt</code>；這份才是投影片文字。',[
('gamma-text-1','移除製作說明，留下每頁要點','<p>展開本節「十段文字轉換提示詞」，複製到原文字對話。把已核對大綱全文接在「以下是已核對大綱：」後，再送出。這次只改呈現，不新增資料。</p><p>大綱中的主旨、來源表與版面建議是你的製作筆記；若全部交給 Gamma，可能多出頁面或塞滿畫面。原大綱保留這些資訊，投影片文字只留標題與2–4個要點。</p>'),
('gamma-text-2','保存十段文字，檢查分隔','<p>複製回答到文字存檔區，選「Gamma 貼入文字」，下載並重開 <code>Gamma貼入文字.txt</code>。應有「第1頁」到「第10頁」，中間九行獨立的 <code>---</code>；分隔讓 Gamma 分辨頁面。</p><p>若多出前言、來源表或謝謝頁，依已核對大綱移除額外段落，保留自己的第一版。每頁只有標題和要點，不能為了短而刪核准條件。</p>'),
('gamma-text-3','對照大綱，再確認內容未改','<p>比對十段文字與原大綱：第1頁保留模擬與尚未執行，第10頁保留核准請求；其他頁的重要數字、單位與待確認狀態也相同。真實企劃依其實際狀態，不套模擬標示。</p><p>轉換改錯時，以已核對大綱為基準修十段文字，或重轉一次；不要反過來改正確來源。下方 A／B 參考文字可協助比對，但不是自己產生的版本。</p>')])
gamma_stage('gamma-generate','已核對的 <code>Gamma貼入文字.txt</code>。產出：可編輯的十張 Gamma 卡片；卡片就是簡報的一頁。',[
('gamma-generate-1','依自己的畫面選一條入口','<p>開啟 Gamma。首頁有訊息輸入框時，使用對話式入口（Agent）：展開下方生成指令，複製到輸入框，再接自己的十段文字並送出。這段指令要求繁體中文、十張、保留原文，讓 Gamma 負責排版。</p><p>若首頁提供「Use classic generator／使用經典生成器」，使用下方替代路徑即可。兩條只做一條，不重做兩份簡報。</p>'),
('gamma-generate-2','生成前，檢查十張大綱','<p>看到大綱時，數到十張；檢查封面、四週時程、人力資源，以及最後核准事項。若多出附錄或謝謝頁，要求移除額外卡片；若改了數字，要求依你提供的十段文字還原。</p><p>確認後才按畫面的生成控制。若要求選版型，選字易讀的簡潔版型；不需要先找圖片。若工具直接生成，完成後先做同樣核對，修正前不匯出交付。</p>'),
('gamma-generate-3','保留自己的可編輯位置','<p>生成完成，查看卡片列表是否十張。複製瀏覽器網址，先放到自己的大綱檔末尾並標「Gamma文件位置」；這個網址用來回原簡報修改，PDF不能取代它。</p><p>帳號不能生成時保存大綱與十段文字，記下卡住的位置，標「Gamma待補」。待工具可用從這一階段續做，不重新寫企劃。</p>')])
classic= '<details class="workbench-disclosure"><summary>替代路徑：畫面提供經典生成器時</summary><ol><li>選「Use classic generator」，再選「Paste in text／貼上文字」，貼入自己的十段文字。</li><li>指定簡報、十張卡片及繁體中文；文字處理選「Preserve this exact text／保留原文」，避免再改寫已核對內容。</li><li>數到十張並核對後生成；若轉進訊息介面，改用上方 Agent 路徑，不需兩條都做。</li></ol>'+paragraph(link('https://help.gamma.app/en/articles/11047840-how-can-i-import-slides-or-content-into-gamma','Gamma 官方貼入與保留原文說明'))+'</details>'
p.insert_after(p.node('#gamma-generate > details'),classic,'折疊替代介面路徑')
gamma_stage('gamma-export','自己的十張 Gamma 卡片。產出：至少一項有理由的修訂與重開確認的 <code>提案.pdf</code>。',[
('gamma-export-1','先查事實，再改一項閱讀問題','<p>逐張對照已核對的十段文字，先查數字、期間、角色、模擬與待確認，再看段落或表格是否太密。選一項實際問題修改，例如把四週時程分成四列，讓每週交付看得出來。</p><p>可在原卡片直接編輯，或對 Agent 指定卡片與修改內容，並要求其他事實不變。自己的頁碼及角色要自己換，不能照貼另一案的數字。內容已正確時，可把最後核准請求分行或加粗，並記下為何較易讀，不需故意製造錯誤。</p>'),
('gamma-export-2','播放檢查，匯出全部卡片','<p>用簡報播放視圖從第1張看到第10張。播放畫面接近匯出樣子，先檢查標題、表格與文字是否可讀；修改後再看一次被改的卡片。</p><p>選右上「分享→匯出」，或右上「⋯→匯出」。在範圍下拉選「All cards／全部卡片」，再選 PDF；選目前卡片可能只下載一頁。這個操作是下載，不更動分享權限。'+link('https://help.gamma.app/en/articles/8022861-what-s-the-easiest-way-to-export-my-gamma','Gamma 官方匯出說明')+'</p>'),
('gamma-export-3','重開 PDF，逐頁確認','<p>到下載紀錄找到檔案，另存名稱 <code>提案.pdf</code> 並開啟。確認十頁，依序看有無截字、漏字、數字改變或字小到不能讀；不要只看封面。</p><p>只有一頁時回匯出改「全部卡片」；太密或截字時回原卡片調整段落或表格，保留必要內容，再匯出重開。A 試跑第7頁曾把第四週擠成窄直欄，修法是改成四個上下排列段落；修後仍需檢查 PDF 第7頁與總頁數，工具回報通過不能代替閱讀。</p>')])
gamma_stage('gamma-handoff','來源企劃、大綱、十段文字、Gamma 文件位置與 PDF。沿用下方五欄短交接，不重抄十頁。',[
('gamma-handoff-1','寫一段能續做的交接','<p>展開下方「成果檢查與五欄短交接」，只取最後五欄，填自己的讀者與請求、檔名、Gamma位置、修改與理由、待確認。可接在自己的大綱檔末尾，不另交一張同內容作業表。</p><p>原企劃是查事實，大綱保留來源與安排，十段文字供重新生成，Gamma用來編輯，PDF用來閱讀。確認這些檔案與網址都找得到，之後來源更新才知道該改哪一頁。</p>'),
('gamma-handoff-2','依完成物確認本次狀態','<p>對照檢查清單，在自己的大綱、Gamma與PDF上確認，不填作者範例的結果。能重開十頁PDF、回Gamma修改，且解釋一项修改理由，才算完成。</p><p>未生成或未匯出時，把已完成檔案保存並標待補。下次換自己的企劃，先換讀者、核准請求與來源，再沿相同步驟製作；不要只替換封面名稱。</p>')])

# Entry pages describe real actions and first-tool preparation.
p=pages['index.html']
p.p('你使用可取得的文字型','每人選最接近工作的案例，使用自己的帳號完成與保存，不需要全班共同作業。依第1到第4單元學習：寫工作短文、改寫給不同讀者、查文件依據、比較方案；Gamma 演練安排在第2單元。')
p.insert_after(p.node('.lesson-body p','你使用可取得的文字型'),paragraph('第一次上課先確認文字對話工具能登入、送出與複製，依'+link('assets/fallback/text-llm-minimum-start.md','工具啟動卡')+'完成一次測試。第2單元另需 Gamma，第3單元需自己的 Google 帳號使用 NotebookLM。沒有工作資料也可用課程完整模擬案例，各章只選一案。'),'課程起點與工具準備')
p=pages['module1.html']
p.replace(p.node('#ch1-1 .course-card','CH2-1'),'','合併重複 CH2 入口到正式區')
p.p('四個單元留下的是不同用途','選一件下週會遇到的工作，例如回覆詢問、整理交接或比較兩個安排。沿用最相關單元的成果，把資料與讀者換成自己的，再核對一次；不需要重做四章或重抄四份表。下方有完成範例，先看再改自己的副本。')
p.p('留下背景、任務、資料、條件','保留自己送出的完整提示詞、第一版及最後成品。另寫一處檢查或修改的理由，以及還缺什麼、接下來由誰確認。')
p.p('沒看過課程的人能看懂','只看檔案，接手的人應知道這份文件給誰、原資料在哪裡、哪些內容已核對，以及下一次要換什麼。')
p.insert_after(p.node('#ch1-1 > h2'),paragraph('依下面順序學習，每章各自選一案。講義中的「先看」是作者示範，「步驟」才是自己操作；工作台依做到的步驟填，不必一開始填完整張。'),'說明學員閱讀與操作順序')

# Avoid typo drift in newly authored text only.
for p in pages.values():
    p.edits=[(a,b,new.replace('内容','內容').replace('有没有','有沒有').replace('换成','換成').replace('写作','寫作').replace('贴比较','貼比較').replace('客户数','客戶數').replace('客戶数','客戶數').replace('一项','一項').replace('张','張'),reason) for a,b,new,reason in p.edits]

# Produce all drafts and lesson sources before touching public HTML.
# Make every required field discoverable in the operational route.
for page_name, sid, sentence in [
 ('CH1-1.html','ch1-step-5','送出前，在「本次改哪一欄」下拉選單選「一項限制條件」；具體要求寫在修正指令，例如「借用結果未確認，不保證可借」。若自己修的是格式，就選「輸出格式」。這讓你日後知道比較的是哪種改動。'),
 ('CH2-1.html','ch2-step-4','在工作台「我的短訊息情境」填「客戶補需求」或自己的情境名稱，讓保存檔能辨認這則訊息用途。')]:
    p=pages[page_name]
    updated=[]
    for a,b,new,reason in p.edits:
        if f'id="{sid}"' in new:
            marker=f'<div class="step-block" id="{sid}">'
            start=new.index(marker);at=new.index('<div class="step-body">',start)+len('<div class="step-body">')
            new=new[:at]+'<p>'+sentence+'</p>'+new[at:]
        updated.append((a,b,new,reason))
    p.edits=updated
p=pages['CH1-1.html']
label(p,'revisionVariable','本次改哪一欄','')
p=pages['CH2-1.html']
p.text('label[for="ch2-message-scenario"]','我的短訊息情境')
p.text('#ch2-message-prompt',message)
p.text('#ch2-email-prompt',client)
for p in [pages[x] for x in ['CH1-1.html','CH2-1.html','CH3-1.html','CH4-1.html']]:
    for i,(a,b,new,reason) in enumerate(p.edits):
        if 'class="steps-wrap"' in new and '步驟' not in reason:
            pass
        if 'class="steps-wrap"' in new:
            end=new.rfind('</div></div></div></div>')
            if end!=-1:
                new=new[:end]+'<p>保存前，閱讀工作台的完成檢查，符合的項目才勾選；未完成的回對應步驟補齊。填寫進度只表示已留紀錄，不代表內容一定正確。</p>'+new[end:]
                p.edits[i]=(a,b,new,reason)

step_margin='\n.lesson-page .step-block[id],.lesson-page .lesson-section[id],.lesson-page .learner-workbench[id]{scroll-margin-top:144px;}\n'
gamma_margin='\n@media(max-width:760px){.lesson-page .step-block[id],.lesson-page .lesson-section[id],.lesson-page .learner-workbench[id]{scroll-margin-top:192px;}}\n'
gamma_steps='\n.lesson-page .step-block{padding:18px 0;border-bottom:1px solid var(--c-border);}.lesson-page .step-circle{display:none;}.lesson-page .step-heading{font-weight:700;line-height:1.6;margin-bottom:8px;}\n'
for name in ['CH1-1.html','CH2-1.html','CH3-1.html','CH4-1.html','PRAC2-1.html']:
    p=pages[name]; node=p.node('style', ':root')
    a,b=p.parser.spans[(node.sourceline,node.sourcepos)]
    raw=p.raw(node);p.edits.append((a,b,raw[:-len('</style>')]+step_margin+(gamma_margin+gamma_steps if name=='PRAC2-1.html' else '')+'</style>','新步驟錨點避開固定頁首，Gamma步驟可辨認'))
drafts={name:p.render() for name,p in pages.items()}
for name,data in drafts.items():
    soup=BeautifulSoup(data,'html.parser')
    assert len(soup.select('.lesson-body'))==1, name
    ids=[x['id'] for x in soup.select('[id]')]; assert len(ids)==len(set(ids)),(name,'duplicate IDs')
    before=pages[name].soup
    assert [(x.get('data-field'),x.get('id')) for x in before.select('[data-field]')]==[(x.get('data-field'),x.get('id')) for x in soup.select('[data-field]')],(name,'field keys changed')
    assert [x.get_text() for x in before.select('script:not([src])')]==[x.get_text() for x in soup.select('script:not([src])')],(name,'inline script drift')
    assert [str(x) for x in before.select('style')]==[str(x).replace(step_margin,'').replace(gamma_margin,'').replace(gamma_steps,'') for x in soup.select('style')],(name,'CSS drift')
for name,data in drafts.items():
    lesson=ROOT/(name.replace('.html','-LESSON-PLAN.md'))
    if not lesson.exists():continue
    source=(BACKUP/lesson.name).read_text()
    a=source.index('<!-- learner-content:start -->');b=source.index('<!-- learner-content:end -->')
    old=source[a:b];heading=old.splitlines()[1]
    body=BeautifulSoup(data,'html.parser').select_one('.lesson-body').decode_contents()
    note='## 2026-10-11 逐步操作修訂\n\n本次正式正文以下方 learner-content 為準。每人獨立選案，依動作、用意、預期結果與必要修復操作；工作台依流程逐欄保存，不新增重抄表格。示範與自己操作分清楚，先產生結果再核對。CH2區分語氣調整與真正更換讀者，Gamma另用完整企劃；CH3先來源與回答再點引用；CH4先驗算再改限制，最後呈現一頁文件。工具按鈕可依介面辨認，但平台帳號及真人跟做尚待重驗。原時數不增加，真人節奏待驗。\n\n'
    lesson.write_text(source[:a]+note+'<!-- learner-content:start -->\n'+heading+'\n\n'+body+'\n<!-- learner-content:end -->'+source[b+len('<!-- learner-content:end -->'):])
for name,data in assets.items():
    dest=ROOT/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(data)
for name,data in drafts.items():(ROOT/name).write_text(data)

for name in ['COURSE-OUTLINE.md','COURSE-BLUEPRINT.md']:
    source=(BACKUP/name).read_text()
    source+='\n\n## 2026-10-11 全課逐步操作補強\n\n保持四章各3小時，每人獨立選案。各章「先看」與正式操作分開；完整材料先於輸入，步驟交代位置、用意、預期結果與修復。CH1提供三案已填起稿prompt並教本機儲存、下載及重開；CH2示範客戶→主管真正讀者轉換及工作短訊息；Gamma使用新的完整企劃，分清來源、大綱、貼入文字、可編輯文件及PDF；CH3來源→第一版→引用核對→修訂；CH4原限制→同標準驗算→只改一限制→一頁PDF。已有工作台鍵與選做資料保留，不新增全班共同作業或重抄記錄。\n\n本次驗收以 _repair/2026-10-11-step-by-step/REPAIR-REPORT.md 為準；不能沿用舊hash的PASS。平台帳號實跑與真人節奏須依新正文另驗，不能把作者文字審查當成已證明教學可用。\n'
    (ROOT/name).write_text(source)
fallback=(BACKUP/'assets/fallback/text-llm-minimum-start.md').read_text()
fallback=fallback.replace('5. 回講義開始自己的任務。','這次小測試只確認工具能送出與複製，不另交作業。看到貼回的文字後再回講義。\n\n## 第一次保存正式任務\n\n1. 回講義開始自己的任務。').replace('6. 重新整理頁面','2. 重新整理頁面')
fallback=fallback.replace('先完成一次「送出、看到回答、複製、保存」','先完成一次「送出、看到回答、複製、貼回」')
(ROOT/'assets/fallback/text-llm-minimum-start.md').write_text(fallback)
template=(BACKUP/'assets/workplace/decisions/one-page-template.md').read_text().replace('「修訂決策卡」','「修正版一頁建議」')
template+='\n\n## 第一次做一頁文件\n\n1. 開啟自己的 Google 文件並建立空白文件（已有 Word 等文件工具也可使用），命名「我的方案建議」。\n2. 將最後建議貼入，只放正文，第一版與修正歷程留工作台。\n3. 選檔案→列印，檢查預覽；環境直接下載PDF時就開啟PDF看頁數。\n4. 正文須一頁、文字可讀，保留算式與單位、待確認及下一步。超頁先縮重複解釋，不用小到不能讀的字體湊一頁。\n5. 儲存PDF為「方案建議.pdf」並重開，確認頁數與內容。不能使用文件工具時標「一頁草稿，頁數待驗」。\n\nGoogle官方列印說明：https://support.google.com/docs/answer/143346?hl=zh-Hant\n'
(ROOT/'assets/workplace/decisions/one-page-template.md').write_text(template)
communication=(BACKUP/'assets/templates/unit2-communication-scenarios.md').read_text()
intro='\n## 第一次操作：不用先填所有方括號\n\n先在 CH2-1 講義選「已填好的客戶Email」，或用本包一張卡完整換成自己的資料；兩者只選一種，不混用案例事實。\n\n可直接使用的完整模擬輸入：\n- [客戶Email](../workplace/communication/email-client.txt)：新對話送出，保存第一版，再核對價格、交期及客戶下一步。\n- [工作短訊息](../workplace/communication/message.txt)：同事情改成2–4句，確認收件者知道要回覆什麼。\n- [主管改寫指令](../workplace/communication/email-manager.txt)：最後方括號貼上自己第一版客戶信；回原對話送出。比較讀者及最後請求，原價格與交期不變。\n\n保存時依講義工作台欄位逐步貼入。客戶→主管是更換讀者；同一客戶的正式→親切是調整語氣，不混為同一種操作。\n'
pos=communication.index('## 四段式提示詞骨架')
(ROOT/'assets/templates/unit2-communication-scenarios.md').write_text(communication[:pos]+intro+'\n'+communication[pos:])
viewer_source=(BACKUP/'assets/templates/unit2-communication-scenarios.html').read_text()
viewer=BeautifulSoup(viewer_source,'html.parser');viewer_spans=Spans(viewer_source)
target=[n for n in viewer.select('.asset-note p') if n.get_text().startswith('回到 CH2-1')]
assert len(target)==1 and target[0].find_parent('main') is not None
a,b=viewer_spans.spans[(target[0].sourceline,target[0].sourcepos)]
new='<p>在 CH2-1 的「選情境」步驟取一張卡，完整換成自己的資料再送出。第一次也可直接用'+link('../workplace/communication/email-client.txt','完整客戶Email')+'，接著做'+link('../workplace/communication/message.txt','工作短訊息')+'與'+link('../workplace/communication/email-manager.txt','主管改寫')+'。每種只做自己的版本，提示詞與回答逐步貼回工作台。三版自我介紹供課後選做。</p>'
(ROOT/'assets/templates/unit2-communication-scenarios.html').write_text(viewer_source[:a]+new+viewer_source[b:])
(OUT/'edits.json').write_text(json.dumps({name:[reason for a,b,new,reason in p.edits] for name,p in pages.items()},ensure_ascii=False,indent=2))
print('修正7頁；同步5份教案、2份課程文件、3份操作素材；新增6份完整提示詞。')
