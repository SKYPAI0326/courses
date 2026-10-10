#!/usr/bin/env python3
"""Approved prose repair: DOM anchors, byte spans, protected source snapshots."""
from pathlib import Path
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import hashlib, html, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / '_backup/2026-10-11-pre-plain-language'
OUT = ROOT / '_repair/2026-10-11-plain-language'
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Spans(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source, self.stack, self.spans = source, [], {}
        self.lines = [0] + [m.end() for m in re.finditer('\n', source)]
        self.feed(source)
    def source_offset(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col
    def handle_starttag(self, tag, attrs):
        pos, start = self.getpos(), self.source_offset()
        if tag in VOID: self.spans[pos] = (start, start + len(self.get_starttag_text()))
        else: self.stack.append((tag, pos, start))
    def handle_startendtag(self, tag, attrs):
        self.spans[self.getpos()] = (self.source_offset(), self.source_offset() + len(self.get_starttag_text()))
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            name, pos, start = self.stack[i]
            if name == tag:
                self.spans[pos] = (start, self.source.index('>', self.source_offset()) + 1)
                del self.stack[i:]
                return

class Page:
    def __init__(self, name):
        self.name = name
        self.source = (BACKUP / name).read_text()
        assert (ROOT / name).read_text() == self.source, (name, 'concurrent change since backup')
        self.soup = BeautifulSoup(self.source, 'html.parser')
        self.body = self.soup.select_one('.lesson-body')
        self.spans, self.edits = Spans(self.source), []
    def node(self, selector, prefix=None):
        nodes = self.soup.select(selector)
        if prefix is not None: nodes = [n for n in nodes if n.get_text(' ',strip=True).startswith(prefix)]
        assert len(nodes) == 1, (self.name, selector, prefix, len(nodes))
        return nodes[0]
    def raw(self, n):
        a, b = self.spans.spans[(n.sourceline,n.sourcepos)]
        return self.source[a:b]
    def replace(self, n, new, why):
        assert n is self.body or n.find_parent(class_='lesson-body') is self.body, (self.name, why)
        a,b = self.spans.spans[(n.sourceline,n.sourcepos)]
        self.edits.append((a,b,new,why))
    def inner(self, n, new, why):
        raw = self.raw(n)
        self.replace(n, raw[:raw.index('>')+1]+new+raw[raw.rfind('</'):], why)
    def p(self, prefix, new):
        self.inner(self.node('.lesson-body p',prefix),new,'精簡：'+prefix[:30])
    def label(self, old, new):
        self.inner(self.node('.lesson-body summary, .lesson-body h2, .lesson-body h3',old), html.escape(new),'標籤：'+old)
    def link(self, sid, href):
        return self.raw(self.node('#'+sid+' a[href="'+href+'"]'))
    def step(self, sid, paras, title=None):
        self.inner(self.node('#'+sid+' .step-body'), ''.join('<p>'+t+'</p>' for t in paras), '操作：'+sid)
        if title:
            self.inner(self.node('#'+sid+' .step-heading'),html.escape(title),'步名：'+sid)
    def before(self, n, content, why):
        assert n.find_parent(class_='lesson-body') is self.body
        a,_ = self.spans.spans[(n.sourceline,n.sourcepos)]
        self.edits.append((a,a,content,why))
    def render(self):
        edits = sorted(self.edits)
        for a,b in zip(edits,edits[1:]): assert a[1] <= b[0], ('overlap',self.name,a[3],b[3])
        data=self.source
        for a,b,new,why in reversed(edits): data=data[:a]+new+data[b:]
        return data

def table(headers,rows):
    esc=lambda x:html.escape(x)
    return '<div class="table-scroll"><table><thead><tr>'+''.join('<th>'+esc(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(c)+'</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table></div>'

def block(sid,number,title,paras):
    return f'<div class="step-block" id="{sid}"><div class="step-circle">{number}</div><div class="step-content"><div class="step-heading">{number}. {title}</div><div class="step-body">'+''.join('<p>'+p+'</p>' for p in paras)+'</div></div></div>'

def optional_labels(p):
    changes={
        '選做：舊題目、首版複本與補充判斷':'課後選做：其他題目與補充判斷',
        '選做：五個生活對話與額外錯誤診斷（舊紀錄保留）':'課後選做：五個生活對話與錯誤診斷',
        '選做：原五題路線與說明（不計目前主線）':'課後選做：五個生活對話的操作說明',
        '選做：原閱讀包檢查':'課後選做：閱讀包檢查',
        '選做：原拆解／生活紀錄欄（舊紀錄保留，無需補填）':'課後選做：閱讀與生活紀錄',
        '選做：原拆解／生活紀錄（舊紀錄保留）':'課後選做：閱讀與生活紀錄',
        '選做：原完整兩份轉換練習':'課後選做：再練一次讀者轉換',
        '展開原完整轉移規格練習（選做）':'課後選做：安排下一次讀者轉換',
        '先同步比較，再完成自己的主卡':'課後選做：購物比較與生活決策卡',
        '同步練習：購物比較':'購物比較範例',
        '先問回答有沒有完成任務':'課後選做：檢查五個生活對話',
        '完成五題、修復一題，再轉用到自己的任務':'課後選做：五個生活對話與一次修正',
        'Demo · 原始輸入：四段都要出現':'示範輸入：四段提示詞',
        'Demo · 示範輸出與品質判準':'示範回答與檢查方法',
        'Demo · 合理錯例與修正':'常見錯句與修正',
    }
    for n in p.soup.select('.lesson-body summary, .lesson-body h2, .lesson-body h3'):
        old=n.get_text(' ',strip=True)
        if old in changes:p.inner(n,html.escape(changes[old]),'移除學員標籤中的維護說明')

def ch1(p):
    cases=table(['所選案例','讀者與要做的事','先核對這一點','成品格式'],[
        ['A：課前提醒','學員帶手機；需要借用時向行政窗口登記','借用待確認，不能保證每人都有','正文最多150字，待確認另列'],
        ['B：受理回覆','民眾回覆案件編號並補照片','已登記不等於已修復；沒有補件期限','正文最多100字，待確認另列'],
        ['C：週工作摘要','主管掌握已完成、待處理與需協助的工作','不同階段件數不能加成總客戶數','三段，每段最多兩點，待確認另列'],
    ])
    wrapper=p.node('#ch1-step-1').parent
    p.before(wrapper,'<p class="body-text">操作時只看自己案例的這一列。</p>'+cases,'案例資訊集中一次')
    p.step('ch1-step-1',[
        '選 A、B 或 C，展開該案材料，讀完全文。依上表找出讀者和對方要做的事。',
        '在工作台「我的案例、完整提示詞與第一版」先寫案名，例如「A｜課前提醒」。'], '1. 選一案，讀原文')
    p.step('ch1-step-2',[
        '找到所選案例的「已填好的起稿提示詞」，按「複製完整提示詞」。提示詞已附上原文，第一次可直接使用。',
        '在對話工具開新對話，貼進輸入區。送出前核對五欄：情境、任務、資料、條件、格式；資料只放所選一案。'],'2. 複製所選案例的提示詞')
    link=p.link('ch1-step-3','#practice-workbench')
    p.step('ch1-step-3',[
        '送出後，等回答完成。將送出的全文貼回'+link+'「我的案例、完整提示詞與第一版」，接著寫「第一版：」並貼上回答。',
        '該欄應保留原文、提示詞和回答。AI 只給寫作建議時，補送「請直接給完整短文，不要說明做法」，並記下補送指令；第一次回答仍保留。'])
    p.step('ch1-step-4',[
        '把原文和第一版並排閱讀，先查上表的核對重點，再查日期、狀態和數量。',
        '在「要修正的一處」寫下原文、回答和錯用的影響。例如：「原文說借用待確認；回答說每人可借；學員可能不帶手機。」已符合原文時，記下核對過的句子。'],'4. 對照原文，找一處要核對的句子')
    p.step('ch1-step-5',[
        '在「本次改哪一欄」選本次改動，例如「一項限制條件」或「輸出格式」。',
        '展開「只修一項的提示詞」，把方括號換成自己的原提示詞、第一版及要修正的問題。回原對話送出，其他資料、讀者和要求沿用第一輪。',
        '指令貼「我送出的修正指令」，回答貼「修正版完整短文」。第一版已正確時，只請模型確認一項重要條件，記下無差異及依據。重問一次仍錯，就依原文手動修正並標「人工修正」。'])
    p.step('ch1-step-6',[
        '在「修改前後與核對依據」貼原句、新句和支持的原文。再查新版其他日期、數量與狀態。',
        '依上表檢查字數或段落；字數計算方法見「短文有沒有新增事實、超過長度？」。在「還缺什麼、問誰」寫缺資料和詢問對象，在「接下來做什麼」寫後續動作。例如：請行政窗口確認借用結果，確認後更新提醒。'])
    p.step('ch1-step-7',[
        '在工作台按「儲存到本機」。看到保存訊息後重新整理，確認提示詞、第一版和修正版還在。',
        '本機儲存留在目前瀏覽器。若重整後遺失，回對話複製版本，再直接匯出檔案；保留仍有文字的對話。'])
    p.step('ch1-step-8',[
        '按「匯出 Markdown」，在下載紀錄找到 <code>unit1-practice-sheet-complete.md</code>，用文字編輯器開啟。<code>.md</code> 是文字檔；無法自動開啟時，用「開啟方式」選文字編輯器。',
        '檔案應有原文、提示詞、第一版、修正版和下一步。缺項回工作台補上，再匯出。',
        '依短文與版本紀錄勾選工作台的完成檢查；課後選做欄位可留空。'])
    p.p('第一次操作，選最接近工作的','選最接近工作的 A、B 或 C。讀材料後，用該案「已填好的起稿提示詞」開始；自備原文的用法見「把回答貼回同一個工作台」。')
    p.p('依上方步驟填工作台','工作台隨操作逐欄填寫。最後交付的短文放在「修正版完整短文」，原提示詞與第一版保留在各自欄位。')
    p.p('使用自己的原文時','自備原文時，展開「起稿提示詞」，依序換成自己的單位與讀者、任務、原文、限制和字數或段落要求。刪掉方括號內的提示文字，核對五欄後再送出。')
    p.p('這項檢查已在步驟7–8操作','重開 <code>unit1-practice-sheet-complete.md</code>，確認原文、第一版與修正版都在。缺內容就回工作台補上再匯出。')

def ch4(p):
    p.step('ch4-step-1',[
        '展開補訓案、行政交接案，或準備自己的兩方案資料。在「我的案例／決策名稱」填案名。',
        '找出原限制、兩方案數值和三個標準的優先順序。第一輪使用原限制；材料中的新增條件留到步驟5。資料不足時先補資料，或使用課程案例。'],'1. 選案例，找出原限制與比較標準')
    p.step('ch4-step-2',[
        '複製「兩方案比較提示詞」，貼入對話工具的新對話，再接上所選案例全文後送出。',
        '送出的全文貼「完整提示詞與案例」，回答貼「第一版比較與建議」。回答要列出兩個方案、算式、至少三項比較標準和暫定選擇。'])
    p.step('ch4-step-3',[
        '從原資料取值，逐一驗算兩方案是否符合限制。課程案例可對照上方驗算表；自備案例用自己的數值，例如「方案費用≤預算上限」。',
        '每個數字附單位，估計值要註明。各角色時間分開查，一次性設定另列。在第一版後寫「我的驗算：」並附算式；算錯時依原資料更正，標「人工更正」。'])
    p.step('ch4-step-4',[
        '先排除不符合限制的方案，再依步驟1的三項標準比較其餘方案。使用同一單位，保持原優先順序。',
        '在第一版下寫選擇的理由及代價，例如「兩場較少安排，但多投入15分鐘且沒有餘裕」。出席時段、設定核准或成效尚未確認時，一併列出；假設工時仍須試辦量測。'],'4. 比較合格方案，寫出選擇與代價')
    p.step('ch4-step-5',[
        '在所選案例找到新增條件，複製「改一項限制的修訂提示詞」，回原對話送出。自備案例使用「自備案例：改一項限制」，填限制名稱、原值、新值和單位。',
        '其餘資料及優先順序沿用第一輪。指令貼「改了哪項限制：實際指令」，回答貼「修正版一頁建議」。換新對話時，先附原資料及第一版。'])
    p.step('ch4-step-6',[
        '用新限制逐方案重算，並核對其他限制仍符合。課程案例看驗算表中所選案例的新限制列；自備案例可寫「費用4,800元＞新預算4,500元，超300元」。',
        '在修正版寫出原選擇、新選擇及造成改選的計算。模型算錯時補明限制再試一次，仍錯就人工更正。兩方案都不合格時，寫「目前無可行方案」，保留必要工作與限制。'])
    template=p.link('ch4-step-7','assets/workplace/decisions/one-page-template.md')
    p.step('ch4-step-7',[
        '將核對後的修正版放入'+template+'：決策與新限制、同欄比較、暫定選擇、得到與放棄、成立條件、待確認與下一步。過程版本留在工作台。',
        '最後建議貼「修正版一頁建議」，後續動作填「接下來由誰做什麼」。太長時刪重複解釋；若用「一頁格式提示詞」縮稿，帶上已核對修訂稿及原案例，縮稿後再查算式與未知事項。'])
    docs=p.link('ch4-step-8','https://docs.google.com/document/')
    help_link=p.link('ch4-step-8','https://support.google.com/docs/answer/143346?hl=zh-Hant')
    old=p.node('#ch4-step-8')
    rows=[
        ('ch4-step-8',8,'把最後建議貼進文件',[
            '開啟'+docs+'並登入，建立空白文件，命名「我的方案建議」。也可使用已有的 Word 或文件工具。',
            '將「修正版一頁建議」貼進文件。文件只放最後建議，第一版及修訂過程留在工作台。']),
        ('ch4-step-8-preview',9,'檢查列印頁面',[
            '選「檔案→列印」，查看預覽。確認只有一頁，數字及單位沒有缺漏，文字可讀。',
            '超過一頁時，回文件刪重複解釋，再看預覽；保留算式、待確認與下一步，字體大小維持可讀。']),
        ('ch4-step-8-export',10,'下載一頁 PDF',[
            '列印預覽出現目的地選單時，選「儲存為 PDF」，檔名用「方案建議.pdf」。若工具直接下載 PDF，就到下載紀錄找到檔案。'+help_link,
            '文件工具無法使用時先匯出文字，標「一頁草稿，頁數待驗」；工具恢復後從貼進文件這一步續做。']),
        ('ch4-step-8-check',11,'重開 PDF，核對內容',[
            '開啟「方案建議.pdf」，再確認頁數是一頁。核對算式、單位、待確認與下一步。',
            '有漏字、截字或頁數不符時，回文件修正，再下載並重開。']),
    ]
    p.replace(old,'\n'.join(block(*r) for r in rows),'一個過長步驟拆成四個有結果的階段')
    p.inner(p.node('#ch4-step-9 .step-circle'),'12','舊錨點保留，顯示序號更新')
    p.step('ch4-step-9',[
        '在工作台按「儲存到本機」，重新整理確認版本仍在，再按「匯出 Markdown」。重開 <code>unit4-decision-card.md</code>，查提示詞、第一版、改限制指令、修正版和驗算。',
        '文字檔留修改過程，PDF 留最後建議。確認兩份都能開啟，再依算式、取捨與下一步勾選完成檢查。缺項回對應步驟補上。'],'12. 保存過程紀錄')
    p.p('第一輪看原限制，第二輪','第一輪用原限制，第二輪只改一項。過程留工作台，最後建議放「修正版一頁建議」，再完成文件與 PDF 步驟。')
    p.p('完成步驟7的已核對修訂稿後','核對後的建議依「把最後建議貼進文件」到「重開 PDF，核對內容」交付。下方模板供整理成品，過程版本仍留工作台。')
    p.p('選補訓、行政交接，或自己','選補訓案、行政交接案，或自己的兩方案資料。沿用前章成果時只取已核對背景與限制；未量測的工時標估計。生活題供課後選做。')
    p.p('展開你選的案例，讀限制','先讀所選案例的限制與兩方案資料，再依下方操作步驟比較。原資料沒有的數字標待確認。')
    p.p('下列原生活／閱讀資產保留','下列生活素材供課後選題或離線使用。課堂只完成所選的一案。')

def ch2(p):
    material=p.link('ch2-step-1','assets/templates/unit2-communication-scenarios.md')
    p.step('ch2-step-1',[
        '第一次可複製「已填好的客戶 Email」。也可從'+material+'選一題，將方括號換成自己的資料；未知內容寫待補，日期與金額用自己的資料。',
        '在「我的 Email 情境」寫案名。送出前核對四段：背景放已知資料，任務寫要做的成品，限制列不能改的條件，格式寫答案形式。'],'1. 選情境，準備 Email 提示詞')
    p.step('ch2-step-2',[
        '在對話工具開新對話，貼提示詞並送出。送出的全文貼「Email：完整提示詞」，回答貼「Email：第一版全文」。',
        '回答應有主旨、正文與署名。只給寫作建議時補送「請直接給整封 Email」；記下補送文字，保留第一次回答。'])
    p.step('ch2-step-3',[
        '對照背景，核對日期、數字與要求。客戶信案例要保留12,000元、約7個工作天、貼文數未確認，並請客戶回覆數量與希望開始時間。自備案例核對自己的日期、數字和要求。',
        '在「Email：核對與改寫理由」寫「事實檢查：……」。新增日期或折扣時，補「只用背景，未知寫待補」再試一次；仍錯就依原文更正並記下理由。核對後才換讀者。'])
    p.step('ch2-step-4',[
        '在「我的短訊息情境」填案名，例如「客戶補需求」。',
        '複製「同一件事的工作短訊息」，或寫自己的收件者、事情與對方下一步。要求2–4句；短訊息直接交代事情與行動，省略 Email 主旨。背景沒給期限，就不加截止日。'])
    p.step('ch2-step-5',[
        '送出訊息提示詞。全文貼「短訊息：完整提示詞」，回答貼「短訊息：第一版全文」。',
        '在「短訊息：核對結果」記下是否2–4句、事實是否符合背景、收件者要做什麼。仍是長信時補「先講事情與下一步，2–4句，直接給訊息」一次；新增事實就依原文更正，保留原回答。'])
    p.step('ch2-step-6',[
        '回原 Email 對話。客戶信案例用「給主管的指令」，把方括號換成自己的第一版客戶信。',
        '自己的案例指定一位新收件者，寫他要知道什麼、要做什麼，以及必須保留的日期、數字和狀態。送出後，指令和回答貼「Email：改寫指令與新讀者版」。'])
    p.step('ch2-step-7',[
        '並排看兩版，核對收件者、最後請求和不變事實。客戶版請補需求，主管版請確認條件；價格與交期仍相同。',
        '在「Email：核對與改寫理由」寫原讀者、新讀者、改了哪一句、保留哪些事實。有漏項時按原文更正並標「人工更正」。'])
    gamma=p.link('ch2-step-8','PRAC2-1.html')
    p.step('ch2-step-8',[
        '按「儲存到本機」，重新整理確認內容仍在，再按「匯出 Markdown」。重開 <code>unit2-communication-pack-complete.md</code>，查 Email 第一版、新讀者版、短訊息及各自的指令和核對理由。',
        '依這三份文字勾選完成檢查，缺項回對應步驟補上。接著開啟'+gamma+'，選另一份完整企劃製作簡報。'])
    p.p('下面保留完整示範輸入','先看四段提示詞如何使用背景資料，再用自己的情境操作。')
    p.p('通過代表你已經能把模糊的','下次可從文字包選一份提示詞，換成自己的資料、讀者與要求，產出後再核對事實。')
    p.p('本單元的核心資產是','工作台保存與匯出文字；素材包提供可選情境、提示詞和課後練習。原始素材保留，成果寫在工作台。')
    p.p('本節是完成主線後的選做','本節課後選做。用已有文字指出新讀者、不變事實和要改的地方，需要時再生成。')

def ch3(p):
    cases=table(['所選案例','筆記本名稱範例','加入的三份來源','第一次用的提示詞','可查的三句'],[
        ['A：教育行政排課','我的排課FAQ','DA1排課規範、DA2試辦公告、DA3協調會議','六題 FAQ 提示詞','R教室容量、申請期限、協助安排；公告18人與會議20人須查核准'],
        ['B：服務案件交接','我的服務交接','DB1案件規範、DB2首次回覆公告、DB3交接會議','一頁交接提示詞','首次回覆期限、結案期限、C017待回覆；1工作天首次回覆不等於結案'],
    ])
    p.before(p.node('#ch3-step-1').parent,'<p class="body-text">操作時只看自己案例的這一列。自備資料則加入同一件工作的三份文件，選 FAQ、交接或待辦其中一種。</p>'+cases,'來源與核對重點集中一次')
    notebook=p.link('ch3-step-1','https://notebooklm.google.com/')
    p.step('ch3-step-1',[
        '開啟'+notebook+'，登入自己的 Google 帳號，選「建立新筆記本」。依所選案例命名，名稱可參考上表。',
        '複製筆記本網址，填入工作台「我的筆記本名稱與連結」。畫面應有來源區和提問區；無法登入或建立時，先處理帳號。'])
    p.step('ch3-step-2',[
        '展開所選案例第一份文件，按「複製全文」。回筆記本選「新增來源／Add sources」→「貼上文字／Copied text」，貼全文並加入，以材料標題命名。',
        '點開來源，核對標題、第一段和最後一段。空白時刪除空來源再加入；保留已正確的來源。'])
    p.step('ch3-step-3',[
        '照相同方法加入所選案例另外兩份文件，三份放在同一筆記本。',
        '勾選這三份來源，逐份確認可讀，名稱與版本填入工作台三個「同案例來源」欄位。混入其他案例時先取消選取，再提問。'])
    p.step('ch3-step-4',[
        '複製上表所選案例的成品提示詞，貼進筆記本提問區並送出。提示詞放提問區，文件放來源區。',
        '指令貼「我送出的成品提示詞」，回答貼「第一版成品」。檢查格式及重要句子旁的引用標記；沒有引用時，補「只根據已選三份來源回答，重要句子附引用」再試一次。仍沒有就記「平台回查待補」。'])
    p.step('ch3-step-5',[
        '從上表核對重點選一句自己的回答，點句旁的引用數字，讀來源名稱及原文。引用數字依當次畫面填寫。',
        '比對原文與回答的數字、期間和狀態，確認原文支持整句。版本較新仍要查核准及適用範圍。'],'5. 點開引用，對照一句回答')
    p.step('ch3-step-6',[
        '在「三句回答的引用核對」先貼回答原句和引用編號，再貼來源名稱、版本及支持的原文短摘。最後寫：原文支持整句、只支持一部分，或沒有寫到。',
        '再選兩句，逐句點引用並記錄。只記來源代號、尚未點開原文時，引用檢查保持未完成。'],'6. 記錄核對結果，再查兩句')
    p.step('ch3-step-7',[
        '在三筆核對中找一個矛盾或缺資料，記在「修正理由與待確認」，寫要問誰、問什麼。容量核准等狀態須有依據，會議日期較新不足以證明核准。',
        '回同一筆記本送「來源查核修訂提示詞」。指令接在「我送出的成品提示詞」後，回答貼「修正版完整成品」，再點查改動句。重問一次仍錯，就依原文人工修正並記下理由；原版已符合時記「無差異」及依據。'])
    p.step('ch3-step-8',[
        '按「儲存到本機」，重整確認仍在，再按「匯出 Markdown」。重開 <code>unit3-notebooklm-reading-pack-complete.md</code>，查第一版、修正版、三筆核對與待確認。',
        '用檔案中的網址回筆記本，再點一筆引用。匯出文字不會帶走可點的引用，網址與原文摘句都要保留。交接前確認對方能取得來源；無法存取時標「人工回查，平台待驗」。',
        '依自己的三筆核對及修正版勾選完成檢查，缺項回對應步驟補上。'])
    p.p('FAQ 是讓新同仁','FAQ 供新同仁查答覆，交接寫目前進度，待辦列動作、負責人與期限。第一次依上表選一種，待辦提示詞另供選用。')
    p.p('下方為作者依原文編製','下方是作者依原文整理的參考答案，完成自己的版本後再對照。自己的回答仍須點引用查原文；選待辦時保留詢問與回覆期限的差別。')
    p.p('下列原生活／閱讀資產保留','下列閱讀素材供課後選題或離線使用。課堂完成自己所選的一份工作文件。')
    p.p('這一單元把回答拆成','閱讀練習先查一句話是否由原文支持，再整理公告影響、書籍筆記或跨來源比較。這些練習供課後選做。')
    p.p('接著使用「把閱讀變成一個小實驗」','選書籍案例時，用「把閱讀變成一個小實驗」提示詞，分開作者主張、自己的理解與下一個行動。')

def gamma(p):
    gamma_link=p.link('gamma-source-3','https://gamma.app/')
    p.step('gamma-source-1',[
        '選 A 報表改善、B 文件交接，或自己的企劃。展開所選企劃，按「複製全文」，保留標題到 P10。',
        '企劃應有方法、時程、人力與核准事項。A 的報表、B 的交接材料是核准後的試行工作，本次先製作提案。'])
    p.step('gamma-source-2',[
        '讀 P01 和 P10，找出請哪位主管核准哪些事項；自備企劃用自己的對應段落。',
        '全文貼入「文字存檔區」，選「來源企劃」，按「下載文字檔」。重開 <code>企劃.txt</code>，核對標題、開頭請求和最後核准事項。'])
    p.step('gamma-source-3',[
        '確認對話工具能送出與複製回答。另開'+gamma_link+'，登入帳號，確認能建立簡報。',
        '找不到入口時請講師協助。遇到付費提示或額度不足時先保存文字，標「Gamma待補」；本課不要求升級。文字存檔區只下載貼入內容，關閉前先下載。'])
    p.step('gamma-outline-1',[
        '複製「十頁大綱提示詞」，貼入對話工具的新對話。在「以下是完整企劃：」下一行，接上 <code>企劃.txt</code> 全文後送出。',
        '送出前查最後一段仍是自己的核准請求，且只包含所選一份企劃。'])
    p.step('gamma-outline-2',[
        '回答貼入文字存檔區，選「十頁大綱」，下載並重開 <code>10頁大綱.md</code>。確認第1到第10頁，封面和核准事項計入；來源清單留作製作筆記。',
        '頁數不符時補「只重整為十頁，封面與核准事項計入，不增加新事實」一次。仍不符可人工整理，保留第一版並標明修改。'])
    p.step('gamma-text-1',[
        '複製「十段文字轉換提示詞」，貼進原對話。在「以下是已核對大綱：」後接大綱全文，再送出。',
        '每頁留標題和2–4個要點。來源表與版面建議留原大綱，供核對；十段文字只放投影片要呈現的內容。'])
    p.step('gamma-text-2',[
        '回答貼入文字存檔區，選「Gamma 貼入文字」，下載並重開 <code>Gamma貼入文字.txt</code>。',
        '確認第1到第10頁，中間有九行獨立的 <code>---</code>。多出的前言、來源表或謝謝頁，依大綱移除；保留第一版及核准條件。'])
    p.step('gamma-handoff-1',[
        '展開「成果檢查與五欄短交接」，填最後五欄：讀者與請求、檔名、Gamma位置、修改與理由、待確認。接在自己的大綱檔末尾即可。',
        '確認企劃、大綱、十段文字、Gamma網址與 PDF 都找得到：企劃查事實，大綱查安排，十段文字供生成，Gamma供編輯，PDF供閱讀。'])
    p.step('gamma-handoff-2',[
        '依清單開啟自己的大綱、Gamma與 PDF。確認十頁 PDF 可重開、Gamma可編輯，並說得出一項修改理由。',
        '未生成或未匯出時，保存已有檔案並標待補。下次換企劃時，重新核對讀者、核准請求及來源。'])
    p.p('完成後，你會留下自己的','保存十頁大綱、可編輯的 Gamma 簡報與十頁 PDF，供提案說明及日後修改。')

phase=sys.argv[1] if len(sys.argv)>1 else 'pilot'
selected={'pilot':{'CH1-1.html':ch1,'CH4-1.html':ch4},'rest':{'CH2-1.html':ch2,'CH3-1.html':ch3,'PRAC2-1.html':gamma}}[phase]
drafts={}
for name,func in selected.items():
    p=Page(name);func(p);optional_labels(p);data=p.render()
    before=p.soup;after=BeautifulSoup(data,'html.parser')
    assert [a.get('href') for a in before.select('a[href]')]==[a.get('href') for a in after.select('a[href]')],(name,'href drift')
    for selector in ['pre','script','style','[data-field]','table']:
        if selector=='table':
            old=[str(x) for x in before.select(selector)];new=[str(x) for x in after.select(selector)]
            assert all(x in new for x in old),(name,'original table drift')
        else:
            assert [str(x) for x in before.select(selector)]==[str(x) for x in after.select(selector)],(name,'protected node drift',selector)
    old_ids=[n['id'] for n in before.select('[id]')];ids=[n['id'] for n in after.select('[id]')]
    assert set(old_ids)<=set(ids) and len(ids)==len(set(ids)),(name,'anchor drift')
    drafts[name]=(p,data)

# Validate all drafts before writing; synchronize the formal source first.
for name,(p,data) in drafts.items():
    target=ROOT/name.replace('.html','-LESSON-PLAN.md')
    source=(BACKUP/target.name).read_text();assert target.read_text()==source,(target.name,'concurrent source change')
    start='<!-- learner-content:start -->';end='<!-- learner-content:end -->'
    a=source.index(start);b=source.index(end)
    title=source[a:b].splitlines()[1]
    body=BeautifulSoup(data,'html.parser').select_one('.lesson-body').decode_contents()
    note='## 2026-10-11 白話與步驟精簡\n\n依使用者核准方針修正文案；案例核對資訊集中，共通操作只引用所選案例。刪重複說明，保留原文、提示詞、完成範例、判斷與恢復。CH4文件/PDF拆步，既有欄位與錨點保留。HTML及下方正式正文同步；真人跟做、平台帳號與時數仍待驗。\n\n'
    target.write_text(source[:a]+note+start+'\n'+title+'\n\n'+body+'\n'+source[b:])
for name,(p,data) in drafts.items():
    (ROOT/name).write_text(data)
    (OUT/(name+'.after.txt')).write_text(BeautifulSoup(data,'html.parser').get_text(' ',strip=True))
    (OUT/(name+'.edits.json')).write_text(json.dumps([{'reason':why,'before':p.source[a:b],'after':new} for a,b,new,why in sorted(p.edits)],ensure_ascii=False,indent=2))
    print(name,len(p.edits),'targeted edits')
