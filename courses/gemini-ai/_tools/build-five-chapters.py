#!/usr/bin/env python3
"""Build reviewed learner bodies in the review workspace; never publish or commit."""
from pathlib import Path
from bs4 import BeautifulSoup
from copy import deepcopy
import html, json, hashlib, re, posixpath

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_review/prompt-controls-2026-10-08/site/courses/gemini-ai'
BEFORE = ROOT / '_source/render-shells'
OUT = ROOT / '_repair/2026-10-08/chapter-build'
TITLES = ['用白話做出第一個小工具', '把需求寫成可重用的提示詞', '製作能處理不同資料的工作工具', '追加需求、修正問題並確認結果', '保存、交付並套用到自己的工作']
OLD = ['part1/CH1-1.html','part1/CH1-2.html','part1/CH1-3.html','part2/CH2-1.html','part2/PRAC2-1.html','part4/PRAC4-3.html','part4/CH4-1.html']
MAP = {f: f'chapters/CH{n}.html' for f,n in zip(OLD,[1,2,2,3,3,4,5])}
SOURCES = {f: BeautifulSoup((BEFORE/f).read_text(), 'html.parser') for f in OLD}

def soup(text): return BeautifulSoup(text, 'html.parser')
def p(text): return soup(f'<p class="body-text">{text}</p>').p
def section(ident, heading, content):
    return soup(f'<section class="lesson-section" id="{ident}"><h2 class="section-heading">{heading}</h2>{content}</section>').section
def prompt(ident, label, text, case=False):
    kind='data-policy-case' if case else 'data-policy-prompt'
    cls='case-data' if case else 'prompt-box'
    note='這份資料供當次操作使用，可替換；核對答案另外列出。' if case else '先複製工具結構；需要本章示例時，另外附加案例區的資料。'
    return f'<div class="prompt-wrap"><div class="prompt-label">{label}</div><p class="policy-guide">{note}</p><pre class="{cls}" id="{ident}" {kind}="true">{html.escape(text)}</pre><button class="copy-btn" type="button" data-policy-copy="{ident}">複製{("案例條件" if case else "完整提示詞")}</button><span id="{ident}-policy-status" role="status" aria-live="polite"></span></div>'
def clone(file, ident):
    item=deepcopy(SOURCES[file].select_one('#'+ident));item['data-source-page']=file;return item
def body_sections(file):
    items=[deepcopy(x) for x in SOURCES[file].select('.lesson-body > .lesson-section')]
    for item in items:item['data-source-page']=file
    return items
def set_paragraph(sec, index, value):
    nodes=sec.select(':scope > p.body-text')
    nodes[index].replace_with(p(value))
def reword(node, pairs):
    # Scoped text nodes only: never rewrite prompts, code, links or scripts.
    for text in list(node.find_all(string=True)):
        if text.find_parent(['pre','code','script','style']): continue
        new=str(text)
        for old,value in pairs: new=new.replace(old,value)
        if new!=str(text): text.replace_with(new)

def build_bodies():
    first=SOURCES[OLD[0]]
    base=first.select_one('#prompt-snake').get_text().split('【資料與設定的重用方式】')[0].rstrip()
    base+='\n\n【設定與案例分離】\n初次開啟時，初始蛇長、初始方向、食物分數與增長格數由玩家在畫面設定。未附案例時不自行填入示例值；設定不完整時指出缺項並阻止開始。若另附遊戲設定，只用來填入可修改的欄位，不能把當次值寫成固定規則。'
    revision=first.select_one('#prompt-snake-revision').get_text().split('【資料與設定的重用方式】')[0].rstrip()
    revision+='\n色彩由畫面上的設定調整；未附樣式條件時保留目前外觀。改變色彩後，重新開始或重設仍使用玩家設定，不能把案例顏色固定在程式中。'
    case=first.select_one('#prompt-snake-case').get_text().split('本次遊戲設定：')[-1]
    case='本次遊戲設定：'+case
    stylecase=first.select_one('#prompt-snake-revision-case').get_text().split('本次外觀條件：')[-1]
    stylecase='本次外觀條件：'+stylecase
    repair=first.select_one('#prompt-complete-delivery').get_text()
    (SITE/'assets/materials/prompt-snake.txt').write_text(base+'\n')
    (SITE/'assets/materials/prompt-snake-case.txt').write_text(case+'\n')
    (SITE/'assets/materials/prompt-snake-revision.txt').write_text(revision+'\n')
    ch1=[section('start','先做出成果，觀察白話如何改變工具', '''
<p class="body-text">當你想做一個小工具，往往能說出需要的功能，卻不知道如何把它變成程式。這一章先讓你完成一次「描述需求、取得程式、開啟操作、接續修改」，看到白話要求如何影響畫面與行為。</p>
<p class="body-text">我們沿用貪食蛇作為第一個例子：按下開始、改變方向、吃到食物與撞牆都有可見的反應，方便核對要求是否實現。這次先留下能玩的 <code>snake-v1.html</code>，再改一項外觀或功能，另存 <code>snake-v2.html</code>。下一章才回頭拆解提示詞，讓你能自行寫出其他工具的需求。</p>
<p class="body-text">先開啟<a href="../assets/tools/snake-basic-reference.html" target="_blank" rel="noopener">經典版操作參考品</a>，填入下方案例設定，玩一局並觀察分數與結束畫面。這是作者製作的參考檔，供你預覽成果或在生成暫時不可用時練習；自己的生成檔仍要另外完成。原有<a href="../assets/tools/貪食蛇.html" target="_blank" rel="noopener">壽司店延伸示範</a>留在本章末尾，先完成經典版即可。</p>
<p class="body-text">準備可登入的 Google 帳號、桌面瀏覽器，以及能儲存純文字的編輯器。本章使用<a href="https://gemini.google.com/" target="_blank" rel="noopener">Gemini 網頁版</a>對話取得程式；若帳號無法進入，先核對<a href="https://support.google.com/gemini/answer/13278668?hl=zh-Hant" target="_blank" rel="noopener">官方登入說明</a>並記下訊息。你可以先用參考品練操作，登入問題解除後再回到生成步驟。</p>'''),
    section('how-it-runs','AI 產生程式，瀏覽器依規則執行', '''
<p class="body-text">「提示詞」就是你交給 AI 的需求說明。送出後，AI 產生程式文字；把這些文字保存成 HTML 檔，再交給瀏覽器開啟，遊戲才會執行。畫面上的蛇依已寫入的规则移動，按方向鍵時不需要重新詢問 AI。</p>
<p class="body-text">HTML 是網頁檔案格式，負責內容與結構；CSS 決定外觀；JavaScript 處理移動、計分和按鈕反應。本章要求三者寫在同一檔案，讓你只需管理一份檔案。生成需要連線；下面提示詞要求遊戲執行時不依賴外部網站，因此存好後可以離線操作。</p>
<p class="body-text">例如「吃到食物後依設定加分」描述的是處理規則；「這次每個食物加十分」是當次設定。規則留在提示詞中，十分放在獨立案例區或操作時填入，未來就能換成其他分數而不必重做工具。</p>'''),
    section('prompt-snake-section','先取得完整工具，再填入當次設定',
    '<p class="body-text">下方提示詞說清楚開始、移動、計分、碰撞及重開時的行為，也要求可修改的設定欄位。先複製整份提示詞；需要跟做本章示例時，再另外附加案例條件。你不必先懂每一句的設計，先核對它是否產生可操作的成果。</p>'+prompt('prompt-snake','生成經典貪食蛇的完整提示詞',base)+prompt('prompt-snake-case','本章跟做設定，可替換',case,True)+
    '<p class="body-text">本次設定用三格蛇身、向右、食物十分及增長一格。吃到第一個食物後，分數應由零變成十、蛇身由三格變成四格；這是核對結果，不要把答案附到生成提示詞。若換成其他分數或增長格數，就依你填的設定重新核對。</p><p class="body-text">需要離線閱讀時，可下載<a href="../assets/materials/prompt-snake.txt" download>結構提示詞 TXT</a>與<a href="../assets/materials/prompt-snake-case.txt" download>案例條件 TXT</a>，兩份各自保存。</p>'),
    section('save-open','從生成文字走到能開啟的 HTML 檔', '''
<p class="body-text">現在已有需求與跟做設定，下一步把它們送入 Gemini，再取得完整程式。你要留下的是本機 HTML 檔；只看見對話中的程式或預覽畫面，還沒完成存檔。</p>
<ol class="step-list">
<li><strong>開新對話並送出需求。</strong>在 Gemini 網頁版開啟新對話，貼上結構提示詞，另附需要的案例設定後送出。等待回覆結束，再取得從 <code>&lt;!DOCTYPE html&gt;</code> 到 <code>&lt;/html&gt;</code> 的內容；不要複製包住程式的三個反引號。</li>
<li><strong>若回覆出現在 Canvas，先取出程式。</strong>Canvas 是同一對話中供你編輯及預覽成果的區域。若它已開啟，可切到右上方「程式碼」取得原始內容；畫面位置不同時對照<a href="https://support.google.com/gemini/answer/16047321?hl=zh-Hant" target="_blank" rel="noopener">官方 Canvas 說明</a>。本章同樣要求取得完整單檔，不必建立公開分享連結。</li>
<li><strong>用純文字保存。</strong>Windows 記事本選「另存新檔」，輸入 <code>snake-v1.html</code>，檔案類型選「所有檔案」、編碼選 UTF-8。Mac「文字編輯」先選「格式 → 製作純文字」，貼入完整程式再存成同名檔案；若詢問副檔名，保留 <code>.html</code>。Mac 路徑也可核對<a href="https://support.apple.com/zh-tw/guide/textedit/txted0b6cd61/mac" target="_blank" rel="noopener">Apple 的 HTML 存檔指引</a>。</li>
<li><strong>找到檔案並開啟。</strong>在檔案管理器確認完整檔名是 <code>snake-v1.html</code>，不是 <code>snake-v1.html.txt</code>。用瀏覽器開啟，應看見設定、遊戲區與開始按鈕；若設定空白，填入案例值再開始。</li>
<li><strong>依行為核對。</strong>用方向鍵、WASD 或方向按鈕移動。先看蛇會不會轉向，再核對食物加分和增長、撞牆結束、重新開始歸零。分數及蛇長依本次設定核對，不只看按鈕有沒有出現。</li>
</ol>
<p class="body-text">若瀏覽器顯示一整頁程式文字，先查副檔名與純文字存檔方式；若只有空白或按鈕無反應，確認程式已完整結束。取得的回覆只有片段時，使用下方補交提示詞；不要自行猜測缺少的程式。</p>'''+prompt('prompt-complete-delivery','要求補交完整成果',repair)+'''
<p class="body-text">功能不符時，在同一對話分開描述「我做了什麼」「實際看見什麼」「預期應發生什麼」，請模型修正並交付完整檔案，再另存後重測。例如填入每個食物十分，吃到食物後卻一直是零，就要查計分行為；這與副檔名錯誤需要不同的修復。</p>'''),
    section('modify','改一項要求，觀察新舊版本的差異',
    '<p class="body-text">v1 已能開始、移動與計分，現在先示範改配色。這次要改變外觀，並保留已驗證的玩法。提示詞要求可調色彩欄位，當次顏色另附，之後才不用為每種顏色重新製作工具。</p>'+prompt('prompt-snake-revision','新增可調配色的完整修改提示詞',revision)+prompt('prompt-snake-revision-case','本次配色條件，可替換',stylecase,True)+'''
<ol class="step-list"><li>在原對話貼上修改提示詞，另附自己的配色條件。若改用新對話，先附上 v1 完整程式，讓模型取得要修改的起點。</li><li>取得完整修正版，另存 <code>snake-v2.html</code>，保留 v1。重新開啟，確認新外觀及可調設定出現。</li><li>再操作開始、移動、計分、碰撞與重新開始。若外觀改了但計分失效，提供實際／預期結果請模型修復；v1 可作回復與比較起點。</li></ol>
<p class="body-text">完成示例後，自己選另一組色彩，在同一工具的設定中修改，說明哪些畫面改變、哪些玩法仍相同。若想改功能，先只選一項，寫清楚變更與保留範圍，再另存版本，方便找到差異的原因。</p>''')]
    optional=clone(OLD[0],'core-6'); optional['id']='snake-extensions'
    optional.select_one('h2').string='課後延伸：逐次加入視覺與互動功能'
    ch1.append(optional)
    ch1.append(section('finish','帶著生成經驗，進入需求設計', '''
<p class="body-text">這一章應留下可開啟的 v1、保留原功能的 v2，以及你能說明的一項差異。請關閉檔案後，從存檔位置重新開啟兩版，確認成果已保存在自己的電腦，而不只留在模型對話中。</p>
<p class="body-text">你已看見白話要求如何變成程式，也看過追加要求可能影響原功能。下一章回頭拆解這些提示詞，說明怎麼把用途、輸入、規則和交付寫清楚，讓你能自行設計工作工具。</p>'''))

    ch2=body_sections(OLD[1])+body_sections(OLD[2])
    set_paragraph(ch2[0],0,'第一章已完成能操作的貪食蛇，也提出過一項修改。現在回看自己的提示詞：模型為何知道要提供方向按鈕、如何計分，以及最後要交付 HTML？這一章把那些資訊拆成可檢查的需求，讓你能自己描述下一個工具。')
    # Remove the old close before the formerly separate type-selection page.
    last=ch2[3].select(':scope > p.body-text')[-1]
    last.replace_with(p('你已能分辨一份提示詞的角色、任務、限制與呈現。接著比較互動、固定計算和條件判斷的需求，確認不同任務各自需要哪些規則；分類會影響你補什麼內容。'))
    set_paragraph(ch2[4],0,'寫清楚四個部分後，還要說明工具主要如何處理資料。按鈕改變畫面、依公式計算、依條件列出提醒，需要的規則各不相同；一個工具也可以同時使用這些方法。下面用既有完整例子比較設計重點，不要求你把每個例子都重新生成。')
    lastsec=ch2[-1]
    for node in list(lastsec.select(':scope > p.body-text'))[-2:]: node.decompose()
    lastsec.append(p('請選一個你想處理的工作需求，寫出使用者要填哪些資料、哪些條件可以設定、工具如何處理、要顯示什麼結果，以及錯誤時如何提醒。再用四個部分整理成完整白話提示詞；當次人名、日期或金額另外附加。若你只寫「做一個好用工具」，回到上方對照表補齊可操作與可核對的要求。'))
    lastsec.append(p('核對你的提示詞：換一份資料是否仍能使用？結果是否有可檢查的规则？是否要求完整成果而非片段？第二章留下的是可重用需求與分開的案例。第三章將用這個方法，完整製作一個處理可排日期與班次需求的工作工具。'))

    ch3=body_sections(OLD[3])+body_sections(OLD[4])
    set_paragraph(ch3[0],0,'第二章已教你把需求拆成輸入、規則和輸出。現在把方法用在排班工作：承辦人要安排人員值勤，但每次人員、日期和班次不同，也有人只能在特定日期值班。本章從案例抽出可重用工具結構，一路完成生成、填資料與查核，不需要跳到另一個練習單元。')
    ch3[0].insert(2,p('先閱讀下表的案例 A，並對照<a href="../assets/materials/schedule-practice.txt" download>兩組排班案例 TXT</a>。本章要留下 <code>schedule-v1.html</code>、自己的 A／B 資料備份、班表及核對紀錄。可先開啟<a href="../assets/tools/schedule-reference.html" target="_blank" rel="noopener">作者排班參考品</a>預覽欄位；參考品供操作與查核，自己的生成成果仍要另外完成。'))
    set_paragraph(ch3[4],0,'沿用第一章的 Gemini 網頁版，貼完整工具提示詞取得程式，再按第一章方式存成 HTML。帳號無法生成時先記錄平台問題；參考工具可供操作與規則核對，自己的生成成果仍須另測。')
    ch3[0].append(p('下載<a href="../assets/materials/core-acceptance.csv" download>五章驗收表</a>，先填預期結果，完成每次操作後再填觀察與狀態。A／B 是兩組不同輸入，請保留各自紀錄，不把新結果覆寫在舊列；未操作的項目保留「待測」。'))
    set_paragraph(ch3[3],0,'剛才已把案例中的名字、日期與班次抽成欄位，也手排一份可行班表。現在用下方完整提示詞生成空白工具，再由你把資料填到介面；工具依當次資料處理，不把手排答案當成程式的一部分。')
    ch3[2].select(':scope > p.body-text')[-1].replace_with(p('把完成的資料／結構對照表保存。接著使用完整工具提示詞生成空白介面，再填入案例 A，換成不同人數與班種的案例 B。原活動預算案例留在<a href="../part2/BUDGET-1.html">預算補充教材</a>，不需要先完成預算才能繼續。'))
    # First list item gives a named platform and a concrete fallback chapter.
    platform=ch3[4].find('li')
    if platform:
        platform.clear(); platform.append(soup('開啟第一章使用的 <a href="https://gemini.google.com/" target="_blank" rel="noopener">Gemini 網頁版</a>，在新對話貼上完整排班工具提示詞，取得完整 HTML。存檔方式見<a href="CH1.html#save-open">第一章存檔步驟</a>；登入或生成暫時不可用時，記錄訊息並用作者參考品練操作。'))
    ch3.append(section('finish','帶著經查核的初版，處理下一個工作要求', '''
<p class="body-text">A 與 B 改變了人數、日期與班種；同一份工具仍能依輸入產生結果，才表示它支援重用。請把核對紀錄寫成「資料與設定、實際結果、預期結果、通過或需修正」，保留未排滿的原因與處理方式。</p>
<p class="body-text">完成本章後，你有可用初版及兩組備份。下一章不重新做另一個工具，會在這份初版加入可調新規則，並查明原功能是否仍正常，讓你能管理工作需求的變更。</p>'''))
    reword(ch3[5],[('下一章用它們驗證交付','下一章用它們核對新增規則與原功能')])

    ch4=body_sections(OLD[5])[:3]
    set_paragraph(ch4[0],0,'第三章已完成能承接 A／B 資料的排班初版。現在負責人希望某類班次不要反覆落在同一個人身上，你要把新要求做成「指定班種的每人次數上限」，讓使用者自行選班種、設定上限與開關。新增功能後，原有可排條件、總上限與同日最多一班仍要成立。')
    ch4[0].insert(2,p('修改前先複製 <code>schedule-v1.html</code> 與自己的 A／B 備份，保留在「歷史版本」資料夾。新程式另存 <code>schedule-v2.html</code>，錯誤時回到 v1 重開；只有檔名不同但覆蓋原檔，就無法回復。先用筆記寫出新增的輸入、影響規則、輸出說明與例外，再看下方示例。'))
    set_paragraph(ch4[0],2,'先用 A 想清楚：若選早班、上限一，原例安有兩個早班就需改排。換到 B 則可以選收尾，工具也應支援使用者新加的班種；指定班種要取自當次清單，不能只認「早班」。')
    ch4[2].append(p('把每項新條件與原功能的觀察填入<a href="../assets/materials/core-acceptance.csv" download>五章驗收表</a>，留下設定、實際結果與理由。上限零造成的缺額符合新規則，應與違反規則的排班分開判讀。'))
    ch4.append(section('repair','用觀察到的差異要求修正', '<p class="body-text">如果啟用新限制後結果不符，先分開記錄輸入、實際結果與預期結果。假如規則選早班、每人上限一，但同一人仍有兩個早班，就能指出缺少的是班種累計限制；只寫「排錯了」無法定位問題。案例記錄另外附加，修正方法保持可重用；記錄中也要交代新規則的開關、指定班種與上限。</p>'+str(deepcopy(SOURCES[OLD[4]].select_one('#prompt-schedule-repair').parent))+
    '<p class="body-text">請模型提供完整修正版，另存後重新測 A／B，包含規則關閉、啟用、上限零與錯誤設定。新功能通過時，再確認舊功能、備份與還原仍可使用；未通過的版本留在歷史區，繼續用 v1 處理已驗證的工作。</p>'))
    ch4.append(section('finish','完成修改版，準備讓下次也能使用', '''
<p class="body-text">本章留下 v2、保留的 v1，以及能指出原功能和新规则結果的紀錄。你應能說明新增了哪個設定、它如何影響班表，以及關閉後如何回到原方式。</p>
<p class="body-text">工具功能已查核後，第五章會實際關閉與重開、還原 A／B 資料，並整理接手者能照做的使用說明。這一步確認成果能離開目前操作環境，繼續在下一次工作使用。</p>'''))

    ch5=body_sections(OLD[6])
    set_paragraph(ch5[0],0,'第四章已留下通過原／新條件測試的修改版，以及可回復的初版。現在把成果整理成下次能使用、他人能接手的交付包：工具檔负责執行，資料備份保存輸入與設定，提示詞保存製作與修改方法。三者用途不同，需要分開保存。')
    # Existing v1 document becomes an explicit example to customize to the actual final version.
    ch5[0].insert(2,p('本章交付第四章完成的 v2。先在 v2 還原 A／B，再分別設定並核對新增規則，重新下載兩組備份。備份格式由工具自行處理，你只需下載、選檔還原，不必手寫 JSON。重開後除了人員與班次，也要核對新規則的開關、指定班種與上限。'))
    set_paragraph(ch5[2],0,'把下方完整說明存成 README.txt，再依自己的實際檔名、設定及測試結果修改。README 是讓接手者知道從哪裡開始的使用說明；它要說清楚新規則如何開關、如何選班種，以及哪些結果已核對。')
    readme=ch5[2].find('pre')
    if readme:
        readme.string='''用途：小型排班規劃；使用者建立人員、日期、班種、時段與需求，再設定可排日期與限制。
入口：工具/schedule-v2.html；雙擊用瀏覽器離線開啟。完整工具不需安裝套件或重新呼叫模型。
支援：1–8人、1–7日期、1–4班種，每班需1–4人。正式人事規定、資格與法定工時需另確認。
新工作：新增、修改或刪除人員、日期、班種；填時段與需要人數，勾可排日期，設定每人總班數上限，再產生。
新增規則：預設關閉。啟用「指定班種每人次數上限」後，從目前清單選一個班種並填非負整數；零代表該班種不安排人員。關閉時使用原排班方式。
改資料：原結果失效，重新產生後才下載CSV或列印。指定班種被刪除時，先重新選擇並核對設定。
保存：資料/schedule-A.json和schedule-B.json由工具下載，保存原輸入與新增設定；關閉前先下載，不靠分頁保留資料。
重開：重新開啟工具，選「還原資料」載入自己的備份；先核對人員、日期、班種、可排日、總上限與新規則，再產生班表。
錯誤：還原失敗保留原輸入；檢查是否選到本版本適用的備份。功能出錯時回歷史版本/schedule-v1.html，修正另存後重測。
已核對資料：填上自己A/B案例、新規則設定、實際結果及測試日期；未測項目明列待確認。
檢查方法：核對需求、可排日期、同日一班、總班數及指定班種上限；缺額保留原因，由負責人調整工作條件。
方法來源：指令/prompt-schedule.txt及prompt-solo-schedule.txt是結構與修改方法；案例資料另存，不把人名或答案寫死。
交付限制：工具是教學驗證的小型規劃成果；未核對正式組織規則，不直接視為已核准班表。'''
    for sec in ch5:
        for text in list(sec.find_all(string=True)):
            if text.find_parent(['script','style']) or text.find_parent(attrs={'data-policy-prompt':True}):continue
            if 'schedule-v1.html' in str(text) and not text.find_parent('pre'):
                text.replace_with(str(text).replace('schedule-v1.html','schedule-v2.html'))
        for pre in sec.select('pre:not([data-policy-prompt])'):
            if 'AI工作工具/' in pre.get_text():pre.string=pre.get_text().replace('工具/schedule-v1.html','工具/schedule-v2.html').replace('  歷史版本/','  歷史版本/schedule-v1.html')
    final=clone(OLD[5],'core-4'); final['id']='handover'
    reword(ch5[2],[('下一站會沿用輸入結構，加入可設定的班種次數限制。','完成後將已核對的結果與未測條件寫入交付說明。'),('下一章會沿用輸入結構，加入可設定的班種次數限制。','完成後將已核對的結果與未測條件寫入交付說明。')])
    ch5[1].append(p('沿用<a href="../assets/materials/core-acceptance.csv" download>五章驗收表</a>記錄重開與還原。測 A／B 原規則時先關閉新增限制；再啟用各自已核對的新設定重測。核對備份中的設定與班表結果，不只比較人名。'))
    tail=final.select(':scope > p.body-text')
    if tail and '最後用' in tail[-1].get_text():tail[-1].decompose()
    ch5.append(final)
    ch5.append(section('transfer','為自己的下一個工作需求整理規格', '''
<p class="body-text">你已走過需求、生成、查核、修改與交付。現在用<a href="../assets/materials/tool-structure-worksheet.md" download>工具結構工作表</a>寫一項自己的需求：使用者輸入什麼、規則能調整什麼、工具如何處理、結果如何核對。課堂先完成規格，不要求你再趕做第二個完整工具。</p>
<p class="body-text">例如換到預算工作，輸入要改為項目、數量、單價與實支，處理方式改為計算合計和差異；排班的可排勾選及同日一班已不適用。可重用的是第二章整理需求的方法，以及後續查核、修改和保存的方法，不只替換名字或故事。</p>
<p class="body-text">要繼續製作時，回<a href="../index.html#supplements">補充教材目錄</a>依用途選擇：提示詞設計與比較、計算排班與表單、介面圖表、行政行銷與會議、改造保存、分享部署。先看該頁先備、材料與完成物，再選擇符合你工作需求的一份完整案例。</p>
<p class="body-text">最後關閉工具，依自己的 README 重新開啟與還原資料；核對人員、日期、班次、原規則與新增設定，重新產生後再對照已知結果。能完成這次重開及核對，才證明交付包足以支援下一次操作。保留工具適用範圍與未測條件，供接手者判斷使用方式。</p>'''))
    bodies=[ch1,ch2,ch3,ch4,ch5]
    for n,sections in enumerate(bodies,1):
        ids=set()
        for i,sec in enumerate(sections,1):
            if sec.get('id','').startswith('core-'): sec['id']=f'ch{n}-section-{i}'
            for item in [sec]+sec.select('[id]'):
                ident=item.get('id')
                if ident in ids: item['id']=f'ch{n}-{i}-{ident}'
                if item.get('id'): ids.add(item['id'])
            reword(sec,[('上一站','前一節'),('下一站','下一章'),('本單元','本章'),('CH1-1','第一章'),('CH1-2','第二章'),('CH1-3','第二章'),('规则','規則'),('负责','負責'),('不是把「畫面有結果」當成正確','仍需用已知答案核對結果')])
        # Old relative links are mapped based on each cloned link's original section source later.
    return bodies

def write_sources(bodies):
    (SITE/'_source/chapters').mkdir(parents=True,exist_ok=True)
    for n,sections in enumerate(bodies,1):
        # The old folder depth is identical to chapters/, so shared asset links stay valid.
        for sec in sections:
            origin=sec.get('data-source-page')
            for a in sec.select('a[href]'):
                href=a['href']
                if origin and not href.startswith(('http:','https:','#','mailto:')):
                    target=posixpath.normpath(posixpath.join(posixpath.dirname(origin),href.split('#')[0]))
                    if target in MAP:
                        anchor=href.split('#',1)[1] if '#' in href else ''
                        if anchor.startswith('core-'):anchor=''
                        a['href']=posixpath.relpath(MAP[target],'chapters')+('#'+anchor if anchor else '')
                        continue
                    if (SITE/target).exists():
                        a['href']=posixpath.relpath(target,'chapters')+(('#'+href.split('#',1)[1]) if '#' in href else '')
                        continue
                for old,target in MAP.items():
                    leaf=old.split('/')[-1]
                    if href.split('#')[0] in [leaf,'../'+old]:
                        anchor=('#'+href.split('#',1)[1]) if '#' in href else ''
                        a['href']=target.split('/')[-1]+anchor
            sec.attrs.pop('data-source-page',None)
        content='\n\n'.join(str(x) for x in sections)
        path=SITE/f'_source/chapters/CH{n}.md'
        text=f'''---
slug: gemini-ai
unit_id: CH{n}
title: {TITLES[n-1]}
course_type: skill-operation
version: 2026-10-08-five-chapters
duration: {[45,75,130,65,45][n-1]}
dependencies: {json.dumps([] if n==1 else [f'CH{n-1}'])}
learning_objective: {TITLES[n-1]}
platform_version: Gemini web; official help checked 2026-10-08; account generation pending
---

# {TITLES[n-1]}

正式正文以下列learner-content範圍為唯一來源；HTML從此範圍轉製。內部設計依據：課程根目錄 _repair/2026-10-08/CHAPTER-REDESIGN.md。
環境：桌面瀏覽器、可登入的Gemini帳號、UTF-8純文字存檔。引用的作者參考品只能證明操作／規則，不代表授課平台生成。真人跟做及六小時試教待驗。
來源：{', '.join(k for k,v in MAP.items() if v==f'chapters/CH{n}.html')}；跨章交付段落另見遷移紀錄。

<!-- learner-content:start -->
{content}
<!-- learner-content:end -->
'''
        path.write_text(text)
    (OUT/'migration.json').write_text(json.dumps({'task_scope':'content-change','old_core_to_chapters':MAP,'chapter4_to5':'PRAC4-3 core-4 handover','preserved_optional_snake':'CH1 snake-extensions','public_supplements':36,'platform_generation':'PENDING','human_follow_along':'PENDING'},ensure_ascii=False,indent=2))

if __name__=='__main__':
    assert BEFORE.exists(), '先建立備份'
    OUT.mkdir(parents=True,exist_ok=True)
    write_sources(build_bodies())
    print('已產出五章正式正文來源；HTML需在內容審查後另行轉製。')
