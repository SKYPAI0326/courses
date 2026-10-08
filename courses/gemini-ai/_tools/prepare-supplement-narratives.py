#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import json, sys, posixpath
sys.path.insert(0,str(Path(__file__).parent))
import importlib.util
spec=importlib.util.spec_from_file_location('chapters',Path(__file__).with_name('build-five-chapters.py'));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
SITE,BEFORE,ROOT=mod.SITE,mod.BEFORE,mod.ROOT

# Specific completion meaning, not interchangeable generic praise.
CLOSE={
'part1/PRAC1-1.html':('保留經試跑的需求，下一次再換資料','組合器幫你整理四個部分，是否漏掉責任人、期限或限制，仍要用模型輸出核對。保留兩版指令與同一份測試資料；下次換會議時，更新案例附件，沿用已核對的處理要求。'),
'part1/PRAC1-2.html':('把比較結果寫成下一次的修改要求','比較紀錄應能指出哪一項判準改善，以及對應的原文與輸出。下一次只修改尚未通過的要求，再保持模型、資料與設定相同重測；用證據選版本，不靠表格看起來整齊。'),
'part1/PRAC1-3.html':('保存模板，也保存需要人工確認的欄位','完成後留下不同會議情境的模板與一份核對過的輸出。下次使用先更新會議資料，將未提供的日期、地點與期限保留待確認；模板降低重複輸入，原文仍是事實來源。'),
'part2/BUDGET-1.html':('把手算基準帶到預算工具製作','本頁完成的是估算、實支、差異與餘額的計算基準。接著閱讀<a href="BUDGET-2.html">預算工具生成與查核</a>，用相同資料核對工具，再改條件測試；當次數值與答案獨立保存，不放進程式的固定結果。'),
'part2/BUDGET-2.html':('讓下一次更新仍能追到金額來源','交付工具、原始明細、備份及報表後，使用者應能更新數量或實支並重新核對。報表上的差異要能回到明細說明原因；未確認費用仍保留待確認，不能為了交出總額而當作零。'),
'part2/CH2-2.html':('用規則解釋有效班表與空缺','這份規格對照用來辨認硬性限制與平均分配偏好。回看自己的班表時，先查可排日、同日一班及需求，再查分配；未排滿時保留空缺與原因。完整製作流程已整併在<a href="../chapters/CH3.html">第三章</a>。'),
'part2/CH2-3.html':('把可讀性與計算正確一起交付','新版需要讓讀者容易找到四個金額，也要維持相同資料的計算答案與例外處理。保留前後版及核對紀錄；之後再改配色或列印版面時，沿用這份基準，才能辨認外觀變更是否影響功能。'),
'part2/PRAC2-3.html':('將配色選擇連到實際閱讀任務','保留選定方案及使用位置，再放到實際工具核對正文、按鈕與錯誤提示。若只看色票而未在畫面試用，還不能判斷讀者是否看得清楚；換風格時同樣保留文字或符號提示。'),
'part3/CH3-1.html':('依讀者的操作選擇呈現方式','你應能說明這次需要固定圖像，還是需要縮放、點選與顯示數值的互動圖。保留這個選擇與可開啟的示例；圖像形式取決於讀者要完成的判斷，後續修改時仍需核對資料與標籤。'),
'part3/CH3-2.html':('讓每個分支都有可追到的結果','流程圖應讓使用者能从起點走到明確的處理結果。保留規則、分支案例與查核紀錄，下一次修改門檻時重跑各條路徑；顏色或連線再清楚，也不能代替分支條件與去向。'),
'part3/CH3-3.html':('把漏斗差異轉成可說明的判斷','保留來源數值、各階段比率與你的判讀，並確認換數字後圖表重新計算。階段下降指出需要進一步查詢的位置，不能單憑圖形就確定原因；交付時一起說明指標定義與資料範圍。'),
'part3/PRAC3-1.html':('保留評估依據，讓雷達圖可被解讀','雷達圖呈現各維度的比較，但每個分數仍需要共同定義與評估依據。保留維度、輸入資料及圖表；調整量尺或維度後重新核對，避免把不同標準的面積直接比較。'),
'part3/PRAC3-2.html':('用時程圖核對工作順序與限制','保留任務、起訖日期與可開啟的時程圖，確認每個色條都對應實際輸入。改日期後重新查期限與重疊；圖表顯示時程位置，工作是否能按時完成仍需核對依賴與資源。'),
'part3/PRAC3-3.html':('用指標方向說明下一個工作行動','留下原資料、指標方向、實際結果及一項工作判斷。越低越好的指標要用相反方向判讀；缺值與零基期保留無法計算或待確認。下次換資料時先核對這些條件，再用圖表討論行動。'),
'part4/CH4-2.html':('讓提示詞能找回，也能判斷是否適用','提示詞庫應連到用途、所需輸入、版本及實際測試紀錄。下次選用先看適用條件，再替換獨立資料；保存了很多文字，還不等於每份指令都能完成工作。'),
'part4/CH4-3.html':('把縮小範圍的成果與未完成處寫清楚','時間有限時，先留下可操作、可核對的核心計算，並記錄尚未實作的要求。日後擴充先從已驗證版本開始；用實際輸入、結果與回復方式說明進度，不以倒數結束宣稱工具完成。'),
'part4/PRAC4-1.html':('依部署證據判斷能否交付','完成清單後，區分已測項目與尚未取得的證據；有缺口就保留未部署狀態。實際部署時按使用環境重新確認帳號、資料位置、費用與撤回方式，不能用勾選取代操作結果。'),
'part4/PRAC4-2.html':('驗證提示詞資料可以保存與找回','留下含用途與版本的提示詞記錄，實際匯出、重開與还原，再查內容是否完整。資料庫用來找回方法與測試紀錄；下一次使用仍須確認案例資料和工作條件。'),
'part4/SUPP4-1.html':('依成果類型選擇保存方式','各案例的檔案、資料與專案入口要分別保存。重開時核對真正需要的輸入與成果；本機檔案不能代替雲端專案，書籤也不能代替資料備份。只回報你實際重開通過的項目。'),
'part4/SUPP4-3.html':('保留改造前後的用途與測試紀錄','選定案例後，留下原版、新規則、修改版與新舊測試結果。不同案例的處理方式不同，不能只换標題重做；缺少生成或模型呼叫證據時，把該項記為待完成，保留可回復的版本。'),
'part5/PRAC5-1.html':('讓通知草稿保留可確認的事實','交付前逐項核對日期、地點、對象與尚未確認的政策，留下人工核對狀態。下一次改期時更新輸入，再從草稿重查事實；工具協助起草，實際寄出仍由承辦人決定。'),
'part5/PRAC5-2.html':('把候選句交給人工判讀','保存候選句、上下文、分類與原文證據。關鍵字只協助尋找可能的行動句，提議、取消與有效交辦需再判斷；下一次換原文仍走這個核對流程，不能把命中直接當成已確認任務。'),
'part5/PRAC5-3.html':('交付可核對的追蹤網址與命名規則','保留命名規則及生成網址，解析參數確認中文字、原查詢與片段都正確。下一次新增渠道沿用命名方法；實際流量歸因還要到分析平台核對，網址產生不代表追蹤已生效。'),
'part5/PRAC5-4.html':('把預覽當作發布前的一次核對','留下原文、預覽及計數規則，指出換行與內容是否完整。發布前回到平台編輯器檢查裁切、連結與媒體；工具中的可調門檻只是你的檢查設定，不能自動代表平台允許發布。'),
'part5/PRAC5-5.html':('讓狀態顏色能連到下一個行動','每筆狀態應能說明責任人、期限、阻塞原因與下一步。保存更新時間與核對紀錄，再用看板討論要處理的問題；下次會議先更新資料，避免沿用已過期的顏色結論。'),
'part5/PRAC5-6.html':('把分數連回共同規準與回答證據','交付共同問題、行為錨點、回答引證與評分紀錄。缺少評分保持未評，不和低分混用；面試小組再依職務需求討論，工具提供比較資料，不能自動決定錄取。'),
'part5/PRAC5-7.html':('區分叫號、略過與實際發言','保留本輪順序與狀態，確認不重複且略過者沒有被記成已發言。下一輪重設時才清除本輪紀錄；主持人仍尊重退出與調整，隨機排列只協助安排順序。'),
'part5/PRAC5-8.html':('連同來源檔交付核對過的報表','對照原文、HTML 預覽與實際 PDF，核對漏字、特殊字元和分頁。交付時保留來源，日後改資料先重新轉換與列印檢查；螢幕預覽正確仍需確認實際輸出。'),
'part5/PRAC5-9.html':('用固定基準日重現日期結果','保留開始、截止與比較基準日，以及倒數、比例和例外狀態。下一次更換日期先重測截止當日與逾期；日期進度描述時間位置，不能當成工作完成率。'),
'part5/PRAC5-10.html':('保留命中依據與人工覆核狀態','交付詞表版本、命中位置與人工閱讀結果。沒有命中只表示本次字串規則沒找到詞，仍要讀上下文；詞表變更後重測大小寫、標點與無命中資料，不把初篩當成正式核准。'),
'part5/PRAC5-11.html':('讓每個候選時段保留未確認資訊','保存各人的回報及整體狀態，確認忙碌不被平均隱藏、空白仍是未知。主持人再確認時長與日曆；下次更新回報時重新核對，不能把單一時段的空閒延伸成整場會議都能出席。'),
'part5/PRAC5-12.html':('交付能還原的案件狀態與期限','保留案件來源、責任人、期限、阻礙與下一步，實際匯出并還原備份。下次更新先核對案件識別與是否已完成；本機期限提示不會自動同步同事或在關閉後通知。'),
'part6/CH6-1.html':('把原文判讀帶到模型生成與查核','本頁先留下有效交辦、取消、提議與未知欄位的判讀基準。接著閱讀<a href="PRAC6-1.html">生成並驗證 AI 會議交辦表</a>，用 A／B 原文查核模型；原文中的最後決議才是填表依據。'),
'part6/PRAC6-1.html':('交付來源、待確認事項與可重開入口','保存逐字稿、交辦結果、人工確認狀態及 Build 專案入口，重開後再用原文核對。語意判斷需要模型且可能誤讀；你要交付能追溯的草稿與待確認原因，不把完整表格當成已核准交辦。'),
'part6/CH6-2.html':('讓分享範圍與撤回方式有依據','保留受眾、權限、資料、用量與撤回方式的決策紀錄；未知項目先查證。需要實際分享時，按當前帳號再次確認，不把能複製網址視為權限已正確或服務長期免費。'),
'part6/CH6-3.html':('把部署版本與回復方法一起保存','交付 repo／版本、部署網址、測試結果與停止服務的方法。實際費用與權限依當前帳號核對；若條件未解決，保留程式與可回復版本，待部署原因與必要證據都明確再處理。'),
}

def main():
    rows=json.loads((ROOT/'_source/page-inventory.json').read_text())
    expected={r['path'] for r in rows if r['role']!='core' and r['listed_in_index']}
    assert set(CLOSE)==expected
    dst=SITE/'_source/supplements';dst.mkdir(parents=True,exist_ok=True)
    records=[]
    for row in rows:
        file=row['path']
        if file not in CLOSE:continue
        doc=BeautifulSoup((BEFORE/file).read_text(),'html.parser');body=doc.select_one('.lesson-body')
        if file=='part2/BUDGET-2.html':
            first=body.select_one('.lesson-section');first.insert(1,mod.p('你已在<a href="BUDGET-1.html">預算金額與公式</a>手算出估算、實支、差異和餘額。現在用完整提示詞把同一套規則做成可輸入明細的工具，再換數量、測缺值與保存成果，確認計算方法真的被實作。尚未建立手算基準時，先完成前頁的四個答案。'))
        elif file=='part6/PRAC6-1.html':
            body.select_one('.lesson-section').insert(1,mod.p('承辦人要從會議原文整理有效交辦，同時保留取消、提議與尚未確認的欄位。先完成<a href="CH6-1.html">原文判讀基準</a>，再用下方完整 Build 描述製作應用；當次逐字稿放到生成後的輸入框，生成描述與待處理資料分開。完成物是可重開的專案、原文、交辦資料及人工核對紀錄。'))
        elif file=='part6/CH6-1.html':
            body.select_one('.lesson-section').insert(1,mod.p('會議常同時出現提議、承諾、取消與後續更新。若把每句「要做」都當作有效任務，會交辦已取消的事項，或補出不存在的期限。本頁先根據原文建立判讀答案，下一份補充教材再拿這份基準核對模型輸出。'))
        elif file=='part2/CH2-2.html':
            first=body.select_one('.lesson-section').select_one('p.body-text')
            first.replace_with(mod.p('第三章已完整教過排班工具的設計、生成與查核。本頁保留規格對照，方便回看硬性限制與平均分配偏好；初次製作請從<a href="../chapters/CH3.html">第三章完整流程</a>開始。'))
        # A specification summary is not a full generative prompt. Label it honestly.
        if file in ['part2/BUDGET-1.html','part6/CH6-1.html']:
            for pre in body.select('pre[data-policy-prompt]'):
                del pre['data-policy-prompt'];pre['data-reference-spec']='true'
                wrap=pre.find_parent(class_='prompt-wrap')
                if wrap:
                    guide=wrap.select_one('.policy-guide')
                    if guide:guide.string='這份摘要用來對照處理規則；完整生成提示詞在接續教材，案例與核對答案另外提供。'
                    for button in wrap.select('[data-policy-copy]'):button.string='複製規則摘要'
        # Correct a now-invalid claim about embedded data/answers, outside prompts.
        mod.reword(body,[('包含角色、用途、欄位、完整資料、公式、例外、單一 HTML 交付規格及已知答案','包含角色、用途、欄位、公式、例外與單一 HTML 交付規格；當次資料與已知答案另外列出'),('第二章核心','第三章核心'),('下一站整理所有成果','完成後回補充目錄選擇後續用途'),('回 目錄成果清單 勾選','保存該案例的完成證據'),('从起點','從起點'),('还原','還原'),('只换','只換'),('匯出并','匯出並')])
        if file=='part3/PRAC3-3.html':
            mod.reword(body,[('保留這份 JSON 並交給第9站','保留這份 JSON，供多案例成果保存補充頁的重開測試使用')])
        if file=='part4/SUPP4-1.html':
            mod.reword(body,[('第6站的 department-kpi-backup.json','KPI 補充頁下載的 department-kpi-backup.json')])
        if file=='part6/CH6-1.html':
            mod.reword(body,[('下一站的生成描述','「生成並驗證 AI 會議交辦表」補充頁的完整生成描述'),('下一站 Build 描述','會議生成補充頁的 Build 描述'),('下一站會提供','會議生成補充頁提供'),('下一站會用 B 測試','會議生成補充頁會用 B 測試')])
        # Existing explanations and demonstrations remain in place; do not pad every
        # transition with an interchangeable generic paragraph.
        title,conclusion=CLOSE[file]
        for a,b in [('从','從'),('还原','還原'),('换','換'),('并','並')]:conclusion=conclusion.replace(a,b)
        body.append(mod.section('completion',title,f'<p class="body-text">{conclusion}</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p>'))
        # Remap old core destinations, preserving same-page examples and appendix pairs.
        for a in body.select('a[href]'):
            href=a['href']
            if href.startswith(('http:','https:','#','mailto:')):continue
            target=posixpath.normpath(posixpath.join(posixpath.dirname(file),href.split('#')[0]))
            if target in mod.MAP:a['href']=posixpath.relpath(mod.MAP[target],posixpath.dirname(file))+(('#'+href.split('#',1)[1]) if '#' in href else '')
        if file=='part3/PRAC3-3.html':
            for a in body.select('a[href]'):
                if a['href']=='../chapters/CH2.html#core-2':
                    a['href']='../chapters/CH1.html#save-open';a.string='第一章的存檔方法'
        if file=='part4/SUPP4-3.html':
            for a in body.select('a[href]'):
                if '#required-route' in a['href']:
                    a['href']='../index.html#supplement-reuse'
                    a.parent.replace_with(mod.p('保存所選案例的生成、修改與重開紀錄；缺少模型呼叫或其他證據時記為待完成。要繼續選用其他案例，回<a href="../index.html#supplement-reuse">改造與保存補充目錄</a>，先確認新的輸入、規則和核對方法。'))
        source=dst/(file.replace('/','-').removesuffix('.html')+'.md')
        source.write_text(f'---\nslug: gemini-ai\nunit_id: SUPP-{file.replace("/","-").removesuffix(".html")}\ntitle: {row["title"]}\ncourse_type: skill-operation\nversion: 2026-10-08-five-chapters\n---\n\n正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。\n\n<!-- learner-content:start -->\n'+str(body)+'\n<!-- learner-content:end -->\n')
        records.append({'page':file,'source':str(source.relative_to(SITE)),'closure':title,'prompt_change':file in ['part2/BUDGET-1.html','part6/CH6-1.html'],'platform_generation':'PENDING'})
    (mod.OUT/'supplement-migration.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    print('已建立36份補充正文來源，保留教學材料並整理入口、承接、成果用途與返回目錄。')

if __name__=='__main__':main()
