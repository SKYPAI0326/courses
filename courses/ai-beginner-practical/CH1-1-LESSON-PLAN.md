---
title: "第一次用LLM完成工作任務"
slug: ai-beginner-practical
unit_id: CH1-1
chapter: CH1-1
course_type: skill-operation
duration: 3h
audience: "零基礎成人，每人為獨立實作者"
prerequisites: "能使用瀏覽器與複製貼上"
learning_objective: "自選單來源工作任務，以五欄完整提示詞產出短文，核對並只修一項缺口，保存實際版本與待確認"
deliverables:
  - "一份自己的工作短文及完整提示詞／第一版／修正版"
  - "唯一缺口、修正指令、前後差異、待確認與下一步"
  - "unit1-practice-sheet-complete.md"
environment: "可輸入文字與保存回答的LLM；品牌不限"
style_guide: ai-beginner-practical/STYLE-GUIDE.md
platform_version: "LLM通用方法；2026-10-08"
status: draft
---

## Learner Task Contract

|契約|凍結事實|
|---|---|
|角色與情境|教育／服務／業務支援或自己的單位，每人只做一案|
|問題與後果|資料未寫的承諾容易被模型補出，採用前需核對|
|起始材料|三案完整模擬資料、起稿／修復prompt、自己的可用LLM與工作台|
|完成物|一份可用短文，原prompt與第一版、唯一修正、新版／核對／待確認；8文字＋4檢查|
|下一位使用者|自己或所選讀者；CH2承接讀者轉換，不重做五題|
|第一動作|選一案，展開全文，將完整資料代入prompt送出|
|第一結果|一份真的短文，貼回personalPrompt可重載|
|回復|偏題U1-ASK；無變化U1-GAP；保存U1-SAVE；無LLM標待重跑|

## Activity Identity與去重

Demo設備公告／只觀察；Supported practice自己所選資料／首版；Solo同案的一項修正／可用短文與核對。不是另交生活五題、示範副本與轉用卡。與後章分別為單來源任務、多讀者轉換／Gamma、多來源引用、硬限制取捨；只有保存共用。


## 2026-10-09 教師修訂說明

學員頁依已同意的閱讀審查修訂。下方 learner-content 是本次正式正文，保留原文、提示詞與工作台欄位。版本相容與試跑紀錄留教師區，不要求學員另填表。四章各三小時、Gamma在CH2後半，時間仍待真人試跑；不得把本次文字修改當作平台或真人驗證完成。

CH2補限制試一次仍錯可依原文人工收尾。Gamma自帶企劃以小標題或支持原句定位，另可用頁內文字下載區存檔。

## 修訂前帳號觀察與版次紀錄（僅供教師）

以下為舊版記錄，不代表本次修訂提示詞已重跑或真人已通過。

- 180分鐘： 啟動15＋概念示範20＋選題首版25＋核對30＋一項修正45＋保存自查30＋回顧15；每人獨立，時間待真人試跑校正。

- 2026-10-08實跑A最終145字，但模型稱144；B初稿102→修長度後92。C初稿的訪談時程安排原本可用，重問反而添「尚未進行／未完成」；原文只說已安排，應人工改為完成狀態來源未提及。第一次正確可保留無差異，查核的是你的原文與版本，不需重做示例全部情境。

## 2026-10-11 逐步操作修訂

本次正式正文以下方 learner-content 為準。每人獨立選案，依動作、用意、預期結果與必要修復操作；工作台依流程逐欄保存，不新增重抄表格。示範與自己操作分清楚，先產生結果再核對。CH2區分語氣調整與真正更換讀者，Gamma另用完整企劃；CH3先來源與回答再點引用；CH4先驗算再改限制，最後呈現一頁文件。工具按鈕可依介面辨認，但平台帳號及真人跟做尚待重驗。原時數不增加，真人節奏待驗。

## 2026-10-11 白話與步驟精簡

依使用者核准方針修正文案；案例核對資訊集中，共通操作只引用所選案例。刪重複說明，保留原文、提示詞、完成範例、判斷與恢復。CH4文件/PDF拆步，既有欄位與錨點保留。HTML及下方正式正文同步；真人跟做、平台帳號與時數仍待驗。

<!-- learner-content:start -->
# 第一次用 LLM 完成工作任務

<section class="lesson-section" id="course-purpose">
<div class="section-eyebrow">(00) 先知道為什麼學</div>
<h2 class="section-heading">這門課要讓 AI 的回答可檢查、可修正、可重做</h2>
<div class="intro-band"><div class="intro-label">先看一個會出事的好答案</div><div class="intro-text">阿凱收到林小姐詢問社群貼文方案。已知基礎方案每月 12,000 元、確認需求後約 7 個工作天交付，但只交代「幫我回覆得專業又親切」時，LLM 可能產出一封很順的信，順手補上下週一開始、首次合作 9 折、5 天完成等內容。</div></div>
<p class="body-text">LLM 是依你的指令產生文字的 AI 語言模型。信寫得順，卻多了原資料沒有的日期、折扣與交期。寄出前要逐句核對，避免讓客戶把猜測當成承諾。</p>
<p class="body-text">本課會練寫短文、改寫、查文件與比較方案。找最新公告時先查原網站；用手上的資料起稿時，把原文交給 AI，完成後逐句核對。</p>
<div class="tool-grid">
<div class="tool-card"><div class="tool-name">CH1｜先把任務說清楚</div><div class="tool-tag">輸入可執行</div><div class="tool-summary">用情境、任務、資料、條件、格式交代工作，逐句檢查回答是否真的完成任務。</div><div class="tool-list"><div class="tool-list-item"><span class="tool-check">✓</span>找出漏掉的條件與不該出現的假設</div><div class="tool-list-item"><span class="tool-check">✓</span>只改一個變因，重問並比較結果</div></div></div>
<div class="tool-card"><div class="tool-name">CH2｜讓同一件事適合不同讀者</div><div class="tool-tag">文字可交付</div><div class="tool-summary">先做自己的Email、短訊息與一次讀者轉換，再將完整企劃做成十頁Gamma提案。</div><div class="tool-list"><div class="tool-list-item"><span class="tool-check">✓</span>辨認客戶信件中的未授權內容</div><div class="tool-list-item"><span class="tool-check">✓</span>保留前後版本，知道改了什麼</div></div></div>
<div class="tool-card"><div class="tool-name">CH3｜讓回答回到提供的來源</div><div class="tool-tag">資料可追溯</div><div class="tool-summary">選同情境三文件，做一份FAQ／交接／待辦，回查實際引用、版本權威與未知。</div><div class="tool-list"><div class="tool-list-item"><span class="tool-check">✓</span>知道哪一句能回到哪個來源</div><div class="tool-list-item"><span class="tool-check">✓</span>來源沒有寫的內容保留為未知</div></div></div>
<div class="tool-card"><div class="tool-name">CH4｜讓選擇有標準與取捨</div><div class="tool-tag">決策可說明</div><div class="tool-summary">選補訓或行政交接兩方案，核對硬限制、排序及只改一項條件後的取捨。</div><div class="tool-list"><div class="tool-list-item"><span class="tool-check">✓</span>看出建議依據與仍缺的資料</div><div class="tool-list-item"><span class="tool-check">✓</span>保留人的最後判斷與選擇責任</div></div></div>
</div>
<div class="callout"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>整套課程的完成線</strong>　你會帶走一套讓 AI 輸出可檢查、可修正、可重做的工作方法：先定義任務，再看證據與限制，最後才決定能不能使用。</div></div>
</section><hr class="section-rule"/><section class="lesson-section" id="lesson-start"><div class="section-eyebrow">(01) 今天的完成線</div><h2 class="section-heading">一個自己的工作任務，一份可用短文</h2><p class="body-text">今天選一個與自己工作接近的任務，寫出第一版，找出一個需要修正的地方，再保存新版。每人獨立完成一案。</p><p class="body-text">先看下方設備通知示範，再選自己的材料。<a href="#workplace-practice">看示範與選材料 →</a>　<a href="#practice-workbench">貼回工作台 →</a></p><p class="body-text completion-line">本章安排 3 小時。下方生活題供課後選做。</p></section><section class="lesson-section workplace-materials" id="workplace-practice"><h2 class="section-heading">完成自己的工作短文</h2>
<p class="body-text">可選教育行政課前提醒、服務窗口回覆或業務週摘要。已有獲准使用的原文，也可改用自己的資料；先寫清楚給誰看、希望他做什麼。</p>
<p class="body-text">最後帶走一份短文，並保留原提示詞、第一版、修正指令與新版。這些直接存在同一個工作台。</p>
<h3>先確認能送出一句話</h3>
<p class="body-text">開啟課前與講師確認可用的文字對話工具，依<a href="assets/fallback/text-llm-minimum-start.md" rel="noopener" target="_blank">工具啟動卡</a>做一次送出與複製測試。這是確認帳號可用，避免寫好提示詞後才發現不能送出。本頁工作台只保存文字；AI 回答要在對話工具產生。</p>
<p class="body-text">無法登入或送出時，先請講師協助確認入口。暫時可用作者範例練習找出新增的事實，記下「平台待重跑」；工具可用後再送出自己的提示詞。無法暫存時，立即匯出或用<a href="assets/worksheets/unit1-practice-sheet.md" rel="noopener" target="_blank">離線工作表</a>保存。</p>
<h3>五欄如何讓工作可執行</h3>
<p class="body-text">情境告訴模型誰使用；任務指定它要寫哪一種成品；資料給它可依據的原文；條件限制不能新增什麼；格式讓結果符合工作用途。缺資料時模型可能補出看似合理的日期、電話或承諾。用每句回答對照原文，能看出這些猜測；文句通順不能取代核對。</p>
<p class="body-text">現在只處理一份原文與一份短文。下一章再練不同讀者的寫法。</p>
<h3>先看：一則設備通知怎麼修</h3>
<p class="body-text">設備公告原文只有：「10月23日13:00–14:00影印機保養，期間請使用2樓備用機。」提示詞交代情境為行政通知、任務為三句短提醒、資料為原文、條件為不得新增故障／取消、格式為三句。</p>
<p class="body-text">示範初稿：「10月23日下午影印機故障。請暫停影印，隔天恢復。」它把保養寫成故障，又新增隔天恢復。先修一項「只保留原文明示的時間與狀態」，其他任務與格式維持；示範新版：「10月23日13:00–14:00影印機保養。這段時間請使用2樓備用機。其他安排未提供。」日期、時間與行動可以逐項回原文，沒有故障與隔天承諾。</p>
<p class="body-text">這是作者編寫的示範。你接著用自己的材料起稿；若有多種錯誤，先修最影響使用的一種。每次回答可能略有不同，記下你改了什麼指令、哪一句變好了。</p>
<h3>三種單位材料：擇一完整使用</h3>
<p class="body-text">選最接近工作的 A、B 或 C。讀材料後，用該案「已填好的起稿提示詞」開始；自備原文的用法見「把回答貼回同一個工作台」。</p>
<details class="workplace-materials"><summary>A 教育行政：完整材料與複製</summary>
<p><a download="" href="assets/workplace/tasks/case-a.txt">下載完整文字</a> <button class="wb-action" data-gamma-copy="task-material-0" type="button">複製全文</button><span data-copy-status="" role="status"></span></p>
<pre id="task-material-0">A｜教育行政：課前提醒（完全模擬，非正式通知）
你是青禾學習中心行政人員，要提醒已報名的成人學員。
課程：手機照片整理入門。日期：2026年10月24日，時間09:30–11:30，地點2樓B教室。
報到09:15開始；請學員攜帶充飽電的手機與充電線。
設備借用登記截止2026年10月21日17:00，向行政窗口登記；是否能借到尚未確認，不能保證每人都有。
活動若因不可抗力調整，中心將另行通知；目前沒有取消、改期或線上直播決定。
任務：寫一份150字以內課前提醒，另列待確認，不算在正文長度。只用本資料。
</pre>
</details>
<details class="workplace-materials"><summary>B 服務窗口：完整材料與複製</summary>
<p><a download="" href="assets/workplace/tasks/case-b.txt">下載完整文字</a> <button class="wb-action" data-gamma-copy="task-material-1" type="button">複製全文</button><span data-copy-status="" role="status"></span></p>
<pre id="task-material-1">B｜服務單位：受理回覆（完全模擬，非正式承諾）
你是安行服務站窗口，收到民眾反映公共通道照明故障。
案件S024於2026年10月19日14:20登記。現有資訊：地點是東側入口，民眾尚未提供照片。
窗口將轉交維護人員了解狀況，但目前沒有排定修復日期，也沒有完成現場檢查。
民眾可以回覆案件編號及照片補件；補件沒有指定截止時間。聯絡窗口為服務站，不填未提供的電話。
任務：寫100字以內受理回覆，說明已登記、需要補件及目前尚未確定的事；另列待確認。不能把受理寫成已修復或保證何時完成。
</pre>
</details>
<details class="workplace-materials"><summary>C 業務支援：完整材料與複製</summary>
<p><a download="" href="assets/workplace/tasks/case-c.txt">下載完整文字</a> <button class="wb-action" data-gamma-copy="task-material-2" type="button">複製全文</button><span data-copy-status="" role="status"></span></p>
<pre id="task-material-2">C｜業務支援：週工作摘要（完全模擬，非營收資料）
你要把2026年10月12日至16日四筆工作紀錄整理給主管。
1. 新詢問8件：其中5件已寄初步資料，3件待回覆。
2. 舊案跟進4件：2件安排需求訪談，2件等待客戶補件。
3. 報價草稿3份：2份待主管核定，1份已核定但尚未寄出。
4. 提案展示1場：已完成展示，客戶沒有回覆是否採用。
數量有可能屬於同一案件的不同階段，沒有案件名單，不能加成唯一客戶總數。
任務：整理為「已完成／待處理／需主管協助」三段，每段最多兩點，另列待確認。不能推算成交率、營收或宣稱已成交。
</pre>
</details>
<details class="workplace-materials"><summary>起稿提示詞：完整材料與複製</summary>
<p><a download="" href="assets/workplace/tasks/prompt.txt">下載完整文字</a> <button class="wb-action" data-gamma-copy="task-material-3" type="button">複製全文</button><span data-copy-status="" role="status"></span></p>
<pre id="task-material-3">請協助我完成以下一個小任務。
情境：[我在哪個單位、結果給誰使用]
任務：[課前提醒／受理回覆／工作摘要擇一]
資料：
[貼上所選A、B、C完整材料或已去識別、獲准使用的自備原文]
條件：只用上述資料；保留日期、狀態與行動；未知標待確認；不得增加承諾或把待核定寫成已完成。
格式：[依案例指定的字數／三段結構]；待確認另外列出。
請直接產出初稿，不要只教我怎麼做。
</pre>
</details>
<details class="workplace-materials"><summary>只修一項的提示詞：完整材料與複製</summary>
<p><a download="" href="assets/workplace/tasks/repair.txt">下載完整文字</a> <button class="wb-action" data-gamma-copy="task-material-4" type="button">複製全文</button><span data-copy-status="" role="status"></span></p>
<pre id="task-material-4">以下是同一任務的原始提示詞與第一版回答：
[貼上原提示詞與第一版回答]
我本次只補／修一項：[寫一個具體條件或遺漏，如「設備借用尚未確認，不得保證可借」]
除本次指定一項，其餘資料、讀者、字數上限／段落格式保持不變。
請只針對這項修正產出完整新版；不要新增未提供的日期、電話、批准或承諾。
最後用一句話指出對應變化；若原本已符合這項條件，請明說沒有差異。
已安排不表示已完成，也不能因來源沒說就改成尚未進行；來源未提及的狀態寫「來源未提及」，原文明說未完成的仍保留。若查長度，A／B用不計空白的可見字元數，正文標題、標點／數字／英文字也計，待確認另列不計；最終由本人驗數。
</pre>
</details>
<details class="workplace-materials"><summary>產出後才看作者參考：完整材料與複製</summary>
<p><a download="" href="assets/workplace/tasks/reference.txt">下載完整文字</a> <button class="wb-action" data-gamma-copy="task-material-5" type="button">複製全文</button><span data-copy-status="" role="status"></span></p>
<pre id="task-material-5">作者參考（供第一次產出後比較，不是模型實跑）
A正文：手機照片整理入門於10月24日09:30–11:30在2樓B教室上課，09:15起報到。請帶充飽電的手機與充電線。如需借設備，請於10月21日17:00前向行政窗口登記；借用結果待確認。若有調整，中心另行通知。
A待確認：設備可借數量與是否符合借用需求；不能把登記截止當成上課日。正文不超過150字。
B正文：您的照明反映已於10月19日14:20登記為S024。請回覆案件編號及照片，我們將轉交維護人員了解。尚未完成現場檢查，修復日期仍待確認。
B待確認：照片、現場檢查及修復安排；不得自訂補件截止、電話或保證完成日。正文不超過100字。
C：已完成：5件新詢問已寄初步資料；1場提案展示已完成。待處理：3件新詢問待回覆、2件舊案待補件；1份已核定報價尚未寄出。需主管協助：2份報價草稿待核定；確認已安排的2件需求訪談是否需支援。
C待確認：唯一案件數、成交情況與營收；訪談只是已安排，不說已完成。未列全部原始工作項的摘要，不等於那些工作已取消。
檢查：日期／狀態／行動與原文一致才可用，寫法可以不同。如已正確，單一條件重問沒有差異也可如實記錄，不故意刪資訊製造錯誤。
</pre>
</details>
<h3>短文有沒有新增事實、超過長度？</h3>
<p class="body-text">教育提醒最多150字，服務回覆最多100字。選取交付的正文，以文字工具檢查「不含空白的字元數」；標點、數字與英文也算，另列的待確認不算。若工具不能計數，可看下方分行示範。不要只相信模型報的字數。</p>
<p class="body-text">修短時也要重新核對原文。例如「已安排訪談」不能直接改成「尚未進行」；原文沒有說完成狀態，就寫「完成狀態待確認」。原句已正確時可保留，記下核對依據。</p>
<details class="workbench-disclosure"><summary>實際正文、計數方法與人工修句（展開完整內容）</summary>
<p><a download="" href="assets/workplace/tasks/field-repair-examples.md">下載完整文字</a>；<button data-gamma-copy="task-field-repair-examples" type="button">複製全文</button><span data-copy-status="" role="status"></span></p>
<pre id="task-field-repair-examples"># 短文實算與狀態修復（2026-10-08授課帳號實跑）

這是示例，不需加做A／B／C全部。正文及狀態摘錄來自實際平台輸出；人工校訂另標。原素材全為教學模擬，非正式通知。

## A：正文145可見字元，模型自報144
[正文含下面提醒標題；「課前提醒初稿」是平台區塊名稱，不計入交付正文]
【青禾學習中心｜課前提醒】
您報名的「手機照片整理入門」將於2026年10月24日09:30–11:30在2樓B教室進行，09:15開始報到，請攜帶充飽電的手機與充電線。需借用設備請於10月21日17:00前向行政窗口登記（無法保證人人有）。遇不可抗力將另行通知，目前無取消、改期或線上直播。

本人實算145≤150，模型稱144；採實算。去空白後每個可見字元算1，正文標題、標點、數字、英文字皆計；另列待確認、平台區塊名稱與修改說明不計。

## B：初稿102超100，一次縮短後92
案件S024已於2026年10月19日14:20登記（東側入口照明故障），將轉交維護人員了解狀況。目前未完成現場檢查，亦未排定修復日。您可回覆案號與照片補件，無指定截止時間。安行服務站

先前一次狀態查核無差異，因原本受理／未檢查已正確，沒有造錯；後來獨立發現102字超100，才只修長度，正文以上92字。你的首版若已達標，保留無差異即可，不必照示例加做查核輪次。

## C：修訂可能讓正確原稿退步
原文：「2件安排需求訪談」。初稿只說完成時程安排，沒有證據顯示訪談是否已進行或完成。
平台第二版原句：「僅完成排程，訪談本身尚未進行/未完成」。
人工修句：「已安排2件需求訪談；訪談是否已進行或完成，來源未提及，請業務承辦人確認。」
理由：已安排是已知狀態；來源沉默不能推定未進行。另如B原文明說沒有完成現場檢查，則要保留該已知未完成，不要把所有狀態都改未知。

## 自行驗長度的方法
選取交付正文（含你實際要交付的標題），可用文件工具字元統計並確認含標點／數字且不計空白。工具口徑不同時，複製純文字分行：每行10個可見字元，數完整行×10＋尾行，略過空白與換行；每個數字、標點、英文字也占一格。不採模型自報。超標先只修長度，不能刪日期、案號、必要行動或把未知改保證。

一次修復仍錯或拒答：保留真原稿，直接按原文人工修句，貼回原「新版完整短文」，前後核對記人工修正／原句／新句／依據；不冒稱新模型回覆。
</pre>
</details>
<h3>個人操作與停下來檢查</h3>
<details class="workbench-disclosure"><summary>A：已填好的起稿提示詞（選一案即可）</summary><p><button class="wb-action" data-gamma-copy="ready-a" type="button">複製完整提示詞</button><span data-copy-status="" role="status"></span> <a download="" href="assets/workplace/tasks/ready-a.txt" rel="noopener" target="_blank">下載文字檔</a></p><pre class="code-block" id="ready-a">請協助我完成以下工作。
情境：青禾學習中心行政人員；短文給已報名的成人學員看。
任務：請寫一份課前提醒。
資料：
A｜教育行政：課前提醒（完全模擬，非正式通知）
你是青禾學習中心行政人員，要提醒已報名的成人學員。
課程：手機照片整理入門。日期：2026年10月24日，時間09:30–11:30，地點2樓B教室。
報到09:15開始；請學員攜帶充飽電的手機與充電線。
設備借用登記截止2026年10月21日17:00，向行政窗口登記；是否能借到尚未確認，不能保證每人都有。
活動若因不可抗力調整，中心將另行通知；目前沒有取消、改期或線上直播決定。
任務：寫一份150字以內課前提醒，另列待確認，不算在正文長度。只用本資料。
條件：只使用上述原文。保留日期、狀態、件數與必要行動；未提供的資訊標待確認，不增加電話、核准、承諾或完成狀態。
格式：150字以內，待確認另外列出。
請直接產出短文，不要只說明做法。</pre></details><details class="workbench-disclosure"><summary>B：已填好的起稿提示詞（選一案即可）</summary><p><button class="wb-action" data-gamma-copy="ready-b" type="button">複製完整提示詞</button><span data-copy-status="" role="status"></span> <a download="" href="assets/workplace/tasks/ready-b.txt" rel="noopener" target="_blank">下載文字檔</a></p><pre class="code-block" id="ready-b">請協助我完成以下工作。
情境：安行服務站窗口；短文給反映照明故障的民眾看。
任務：請寫一份受理回覆。
資料：
B｜服務單位：受理回覆（完全模擬，非正式承諾）
你是安行服務站窗口，收到民眾反映公共通道照明故障。
案件S024於2026年10月19日14:20登記。現有資訊：地點是東側入口，民眾尚未提供照片。
窗口將轉交維護人員了解狀況，但目前沒有排定修復日期，也沒有完成現場檢查。
民眾可以回覆案件編號及照片補件；補件沒有指定截止時間。聯絡窗口為服務站，不填未提供的電話。
任務：寫100字以內受理回覆，說明已登記、需要補件及目前尚未確定的事；另列待確認。不能把受理寫成已修復或保證何時完成。
條件：只使用上述原文。保留日期、狀態、件數與必要行動；未提供的資訊標待確認，不增加電話、核准、承諾或完成狀態。
格式：100字以內，待確認另外列出。
請直接產出短文，不要只說明做法。</pre></details><details class="workbench-disclosure"><summary>C：已填好的起稿提示詞（選一案即可）</summary><p><button class="wb-action" data-gamma-copy="ready-c" type="button">複製完整提示詞</button><span data-copy-status="" role="status"></span> <a download="" href="assets/workplace/tasks/ready-c.txt" rel="noopener" target="_blank">下載文字檔</a></p><pre class="code-block" id="ready-c">請協助我完成以下工作。
情境：業務支援人員；摘要給主管看。
任務：請寫一份週工作摘要。
資料：
C｜業務支援：週工作摘要（完全模擬，非營收資料）
你要把2026年10月12日至16日四筆工作紀錄整理給主管。
1. 新詢問8件：其中5件已寄初步資料，3件待回覆。
2. 舊案跟進4件：2件安排需求訪談，2件等待客戶補件。
3. 報價草稿3份：2份待主管核定，1份已核定但尚未寄出。
4. 提案展示1場：已完成展示，客戶沒有回覆是否採用。
數量有可能屬於同一案件的不同階段，沒有案件名單，不能加成唯一客戶總數。
任務：整理為「已完成／待處理／需主管協助」三段，每段最多兩點，另列待確認。不能推算成交率、營收或宣稱已成交。
條件：只使用上述原文。保留日期、狀態、件數與必要行動；未提供的資訊標待確認，不增加電話、核准、承諾或完成狀態。
格式：已完成／待處理／需主管協助三段，每段最多兩點；待確認另列。
請直接產出短文，不要只說明做法。</pre></details><p class="body-text">操作時只看自己案例的這一列。</p><div class="table-scroll"><table class="lesson-table"><thead><tr><th>所選案例</th><th>讀者與要做的事</th><th>先核對這一點</th><th>成品格式</th></tr></thead><tbody><tr><td>A：課前提醒</td><td>學員帶手機；需要借用時向行政窗口登記</td><td>借用待確認，不能保證每人都有</td><td>正文最多150字，待確認另列</td></tr><tr><td>B：受理回覆</td><td>民眾回覆案件編號並補照片</td><td>已登記不等於已修復；沒有補件期限</td><td>正文最多100字，待確認另列</td></tr><tr><td>C：週工作摘要</td><td>主管掌握已完成、待處理與需協助的工作</td><td>不同階段件數不能加成總客戶數</td><td>三段，每段最多兩點，待確認另列</td></tr></tbody></table></div><p class="table-scroll-note">手機可左右滑動表格，查看所選案例的其他欄位。</p><div class="steps-wrap"><div class="step-block" id="ch1-step-1"><div class="step-circle">1</div><div class="step-content"><div class="step-heading">1. 選一案，讀原文</div><div class="step-body"><p>選 A、B 或 C，展開該案材料，讀完全文。依上表找出讀者和對方要做的事。</p><p>在工作台「我的案例、完整提示詞與第一版」先寫案名，例如「A｜課前提醒」。</p></div></div></div><div class="step-block" id="ch1-step-2"><div class="step-circle">2</div><div class="step-content"><div class="step-heading">2. 複製所選案例的提示詞</div><div class="step-body"><p>找到所選案例的「已填好的起稿提示詞」，按「複製完整提示詞」。提示詞已附上原文，第一次可直接使用。</p><p>在對話工具開新對話，貼進輸入區。送出前核對五欄：情境、任務、資料、條件、格式；資料只放所選一案。</p></div></div></div><div class="step-block" id="ch1-step-3"><div class="step-circle">3</div><div class="step-content"><div class="step-heading">3. 送出，留下提示詞與第一版</div><div class="step-body"><p>送出後，等回答完成。將送出的全文貼回<a href="#practice-workbench" rel="noopener" target="_blank">工作台</a>「我的案例、完整提示詞與第一版」，接著寫「第一版：」並貼上回答。</p><p>該欄應保留原文、提示詞和回答。AI 只給寫作建議時，補送「請直接給完整短文，不要說明做法」，並記下補送指令；第一次回答仍保留。</p></div></div></div><div class="step-block" id="ch1-step-4"><div class="step-circle">4</div><div class="step-content"><div class="step-heading">4. 對照原文，找一處要核對的句子</div><div class="step-body"><p>把原文和第一版並排閱讀，先查上表的核對重點，再查日期、狀態和數量。</p><p>在「要修正的一處」寫下原文、回答和錯用的影響。例如：「原文說借用待確認；回答說每人可借；學員可能不帶手機。」已符合原文時，記下核對過的句子。</p></div></div></div><div class="step-block" id="ch1-step-5"><div class="step-circle">5</div><div class="step-content"><div class="step-heading">5. 只補一項要求，取得新版</div><div class="step-body"><p>在「本次改哪一欄」選本次改動，例如「一項限制條件」或「輸出格式」。</p><p>展開「只修一項的提示詞」，把方括號換成自己的原提示詞、第一版及要修正的問題。回原對話送出，其他資料、讀者和要求沿用第一輪。</p><p>指令貼「我送出的修正指令」，回答貼「修正版完整短文」。第一版已正確時，只請模型確認一項重要條件，記下無差異及依據。重問一次仍錯，就依原文手動修正並標「人工修正」。</p></div></div></div><div class="step-block" id="ch1-step-6"><div class="step-circle">6</div><div class="step-content"><div class="step-heading">6. 再查新版，補上待確認與下一步</div><div class="step-body"><p>在「修改前後與核對依據」貼原句、新句和支持的原文。再查新版其他日期、數量與狀態。</p><p>依上表檢查字數或段落；字數計算方法見「短文有沒有新增事實、超過長度？」。在「還缺什麼、問誰」寫缺資料和詢問對象，在「接下來做什麼」寫後續動作。例如：請行政窗口確認借用結果，確認後更新提醒。</p></div></div></div><div class="step-block" id="ch1-step-7"><div class="step-circle">7</div><div class="step-content"><div class="step-heading">7. 儲存，再確認重新整理後仍在</div><div class="step-body"><p>在工作台按「儲存到本機」。看到保存訊息後重新整理，確認提示詞、第一版和修正版還在。</p><p>本機儲存留在目前瀏覽器。若重整後遺失，回對話複製版本，再直接匯出檔案；保留仍有文字的對話。</p></div></div></div><div class="step-block" id="ch1-step-8"><div class="step-circle">8</div><div class="step-content"><div class="step-heading">8. 下載檔案，重開自己的成果</div><div class="step-body"><p>按「匯出 Markdown」，在下載紀錄找到 <code>unit1-practice-sheet-complete.md</code>，用文字編輯器開啟。<code>.md</code> 是文字檔；無法自動開啟時，用「開啟方式」選文字編輯器。</p><p>檔案應有原文、提示詞、第一版、修正版和下一步。缺項回工作台補上，再匯出。</p><p>依短文與版本紀錄勾選工作台的完成檢查；課後選做欄位可留空。</p></div></div></div></div>
<h3>把回答貼回同一個工作台</h3>
<p class="body-text">自備原文時，展開「起稿提示詞」，依序換成自己的單位與讀者、任務、原文、限制和字數或段落要求。刪掉方括號內的提示文字，核對五欄後再送出。</p>
<p class="body-text">工作台隨操作逐欄填寫。最後交付的短文放在「修正版完整短文」，原提示詞與第一版保留在各自欄位。</p>
<h3>卡住時怎麼繼續</h3>
<ul><li>回答改了日期或狀態：回原文找依據，補一項限制試一次；仍錯時人工修正，保留理由。</li><li>資料沒有答案：寫待確認、由誰確認與下一步，不自行補承諾。</li><li>匯出或暫存失敗：立即列印或使用離線工作表，保留已完成內容。</li></ul>
<h3>自我檢查</h3>
<p class="body-text">原文只說「已登記」，能寫成「已修復」嗎？不能，登記沒有證明修復。</p>
<p class="body-text">原文只列各階段件數，沒有唯一案件名單，能相加成總客戶數嗎？不能，階段可能重疊。</p>
</section><hr class="section-rule"/><section class="lesson-section" id="lesson-concept"><details><summary>課後參考：語言模型與搜尋的差別</summary>
<div class="section-eyebrow">(02) 關鍵概念</div>
<h2 class="section-heading">同一句話，可以是搜尋任務，也可以是對話任務</h2>
<p class="body-text">LLM 是能用文字對話協助產生、整理或改寫內容的語言模型。它會依照你提供的文字與條件產生回答；回答是否適合使用，要回到你的任務與條件判斷。</p>
<div class="tool-grid">
<div class="tool-card"><div class="tool-name">搜尋問題</div><div class="tool-tag">找外部資料</div><div class="tool-summary">目標是找到網頁、時間、價格或其他外部資訊。</div><div class="tool-list"><div class="tool-list-item"><span class="tool-check">✓</span>例：查京都目前的營業時間</div><div class="tool-list-item"><span class="tool-check">✓</span>要注意資料日期與來源</div></div></div>
<div class="tool-card"><div class="tool-name">對話任務</div><div class="tool-tag">處理你的要求</div><div class="tool-summary">目標是讓 LLM 依照條件產生初稿、清單或解釋。</div><div class="tool-list"><div class="tool-list-item"><span class="tool-check">✓</span>例：依預算提出晚餐選項</div><div class="tool-list-item"><span class="tool-check">✓</span>要交代讀者、格式與限制</div></div></div>
</div>
<p class="body-text">提示詞是你交給 LLM 的任務說明。這堂課使用五欄框架，先把「事情在哪裡發生、要做什麼、要參考什麼、不能違反什麼、答案要長什麼樣」寫出來。</p>
<table>
<thead><tr><th>欄位</th><th>白話意思</th><th>晚餐例子</th></tr></thead>
<tbody><tr><td>情境</td><td>事情發生在哪裡</td><td>今天下班後要安排晚餐</td></tr><tr><td>任務</td><td>要 LLM 幫你做什麼</td><td>提出三個晚餐選項</td></tr><tr><td>資料</td><td>LLM 必須知道的條件</td><td>兩人、不吃牛、預算 600 元</td></tr><tr><td>條件</td><td>不能違反的限制</td><td>30 分鐘內完成</td></tr><tr><td>格式</td><td>答案要長什麼樣</td><td>表格，列出菜色、時間、預算</td></tr></tbody>
</table>
</details></section><hr class="section-rule"/><section class="lesson-section" id="lesson-example-bank"><details><summary>課後素材：五個生活對話題</summary>
<div class="section-eyebrow">(02-1) 五題回答判讀</div>
<h2 class="section-heading">課後選做：檢查五個生活對話</h2>
<p class="body-text">完成每一題後，用下面的檢查問題判斷回答是否可用。先核對任務，再核對條件，最後才看語氣與長度。</p>
<div class="scenario-grid">
<div class="scenario-row"><div class="scenario-task">第 1 題｜能力邊界</div><div class="scenario-pick">檢查回答是否列出三種具體文字工作，並說明哪些內容需要人回到可靠來源確認；「什麼都能做」不算完成。</div></div>
<div class="scenario-row"><div class="scenario-task">第 2 題｜即時資料邊界</div><div class="scenario-pick">檢查回答是否交代查詢時間與來源；沒有即時資料時，應明確標記無法判斷並指出下一步查哪類官方資訊。</div></div>
<div class="scenario-row"><div class="scenario-task">第 3 題｜晚餐規劃</div><div class="scenario-pick">看回答是否逐一回應人數、飲食、預算與時間，並用指定格式呈現。</div></div>
<div class="scenario-row"><div class="scenario-task">第 4 題｜解釋與推薦分開</div><div class="scenario-pick">檢查回答是否有一句定義、生活化例子與三個待查問題，且沒有替你推薦商品；用自己的話重述「一籃子資產」與「可以交易」。</div></div>
<div class="scenario-row"><div class="scenario-task">第 5 題｜資訊保留</div><div class="scenario-pick">檢查整理後是否仍有日期、所有時間、住戶行動與雨天備案，且沒有自行增加罰則。</div></div>
</div>
<p class="body-text"><strong>先看四個可直接重做的對照案例。</strong>每題都附完整提示詞、示範回答與常見錯誤。先對照回答如何使用輸入條件，再到工作台送出自己的版本。</p>
<div class="scenario-grid">
<div class="scenario-row"><div class="scenario-task">案例 1｜請 LLM 介紹自己</div><div class="scenario-pick"><strong>提示詞：</strong><pre class="code-block"><code>你是誰？請用一般人聽得懂的方式，說明你可以幫我做哪三種事情，以及哪些事情需要我自己再確認。</code></pre><strong>示範回答：</strong>我可以協助整理文字、改寫草稿，也能依照你提供的條件列出選項。若問題涉及最新日期或價格、特定資格或專業判斷，請再核對可靠資料；最後由你確認內容是否適用。<br><strong>常見錯誤：</strong>只寫「我什麼都能做，而且都正確」。回答沒有交代工作範圍與需要確認的事項。</br></div></div>
<div class="scenario-row"><div class="scenario-task">案例 2｜明天台北會下雨嗎</div><div class="scenario-pick"><strong>提示詞：</strong><pre class="code-block"><code>明天台北會下雨嗎？請先說明你回答所根據的時間；如果無法取得即時資料，請告訴我應該查哪一種官方資訊。</code></pre><strong>示範回答：</strong>我目前無法確認明天台北的最新預報，因此不提供降雨結論。請查看中央氣象署的臺北市預報並確認更新時間；你貼上資料後，我可以幫你整理降雨時段與出門準備。<br><strong>常見錯誤：</strong>直接給出 60% 等精確數字，卻沒有時間與來源。</br></div></div>
<div class="scenario-row"><div class="scenario-task">案例 4｜解釋 ETF</div><div class="scenario-pick"><strong>提示詞：</strong><pre class="code-block"><code>請用沒有金融背景的人聽得懂的方式解釋 ETF。先用一句話說明，再用一個生活化例子，最後列出三個我還需要查證的問題。不要直接推薦我買任何商品。</code></pre><strong>示範回答：</strong>ETF 像一個裝著不同資產的提籃，買進基金單位，就持有這個組合的一部分；許多 ETF 也能在交易所買賣。接著可查：它追蹤什麼？費用如何計算？可能有哪些風險？<br/><strong>常見錯誤：</strong>從概念解釋跳成「你應該買哪一檔」。</div></div>
<div class="scenario-row"><div class="scenario-task">案例 5｜整理社區通知</div><div class="scenario-pick"><strong>提示詞：</strong><pre class="code-block"><code>本週社區將於週三晚上七點進行停車場清潔，請住戶在下午六點前移走車輛。若遇雨天，工作順延至週四同一時間。管理室會在當天下午五點再次公告。請整理成三個條列，保留日期、所有時間、住戶行動與雨天備案。</code></pre><strong>示範回答：</strong>① 本週週三 17:00，管理室再次公告。② 請於週三 18:00 前移車，停車場清潔預定週三 19:00 開始。③ 遇雨順延至週四 19:00；待確認：若順延，「當天下午 17:00」是週三還是週四？<br/><strong>常見錯誤：</strong>只留下「週三晚上清潔，請移車」，把雨天備案與再次公告時間刪掉。</div></div>
</div>
<div class="intro-band"><div class="intro-label">五題共同判準</div><div class="intro-text">每題都回答三個問題：它完成了原本的任務嗎？它真的使用了提供的條件嗎？還有哪些地方需要人再確認？</div></div>
</details></section><hr class="section-rule"/><section class="lesson-section" id="lesson-demo"><details><summary>課後示範：資訊不足時怎麼追問</summary>
<div class="section-eyebrow">(03) 完整示範</div>
<h2 class="section-heading">案例 3｜從「幫我想晚餐」變成可用初稿</h2>
<p class="body-text">阿凱想安排晚餐。先看模糊輸入，再看補齊條件後的輸入，最後觀察回答是否真的回應了每個條件。</p>
<div class="steps-wrap">
<div class="step-block"><div class="step-circle">1</div><div class="step-content"><div class="step-heading">模糊輸入</div><div class="step-body">只有「幫我想晚餐」時，LLM 不知道幾個人吃、預算多少、有哪些不能吃的食材，也不知道你要清單、食譜或餐廳建議。</div></div></div>
<div class="step-block"><div class="step-circle">2</div><div class="step-content"><div class="step-heading">補上五欄條件，直接送出這段提示詞</div><div class="step-body"><p>先讀下面的完整輸入；你可以直接複製到可使用的文字型 LLM。工作台用來保存你的回答，這裡則保留示範所需的完整操作內容。</p><div class="code-block">我今天下班後想吃晚餐。請依照以下條件提出三個選項：兩人、預算 600 元、不吃牛、希望 30 分鐘內完成。請用表格列出菜色、預估時間與預算，最後告訴我還缺哪一個條件。</div><p><strong>送出後應看到：</strong>三個選項、時間與預算欄位；若模型補寫所在地或當日價格，先標記為待確認，不把示意值當成查證結果。</p></div></div></div>
<div class="step-block"><div class="step-circle">3</div><div class="step-content"><div class="step-heading">讀回答，檢查條件是否進入結果</div><div class="step-body"><table><thead><tr><th>選項</th><th>菜色</th><th>預估時間</th><th>預算</th></tr></thead><tbody><tr><td>A</td><td>番茄雞肉義大利麵＋沙拉</td><td>25 分鐘</td><td>420 元</td></tr><tr><td>B</td><td>豆腐蔬菜鍋＋白飯</td><td>30 分鐘</td><td>480 元</td></tr><tr><td>C</td><td>蝦仁蛋炒飯＋燙青菜</td><td>20 分鐘</td><td>360 元</td></tr></tbody></table><p>逐一對照：有三個選項嗎？有回應兩人、不吃牛、600 元與 30 分鐘嗎？還可能缺少「家裡現有食材」或「是否需要外帶」等條件。</p><p><strong>只修一個缺口的重問：</strong></p><div class="code-block">請保留剛才的三個晚餐方向、兩人、不吃牛、600 元與 30 分鐘限制，只補上「家中已有番茄、雞蛋與白飯」這一項資料。請重新比較哪些選項最能使用現有食材，並列出仍需確認的內容。</div><p><strong>修正版應出現：</strong>至少一個選項確實使用現有食材，同時保留原本的預算與時間比較；若仍缺少所在地或價格資料，要繼續標示待確認。</p></div></div></div>
</div>
<div class="callout"><div aria-hidden="true" class="callout-icon">i</div><div class="callout-body"><strong>示範的判斷點</strong>　提示詞讓 LLM 先產生規劃初稿；它沒有自動知道你的所在位置、當日價格或店家營業狀態。任務完成要看回答是否回應你交代的條件，文字順不順只是其中一項。</div></div>
<p class="body-text"><strong>失敗影響：</strong>如果只看文字順不順，可能把漏掉飲食限制、超出時間或未查證的價格當成可直接使用的答案；所以每次都要保留第一版，先按條件逐項核對，再決定是否修改。</p>
<p class="body-text">同樣的方式可以用在「四天三夜京都自由行」：先交代預算、偏好、每天可接受的景點數與輸出格式。行程表是初稿；交通班次、票價與營業時間要另查最新資料。</p>
</details></section><hr class="section-rule"/><section class="lesson-section" id="lesson-error-clinic"><details><summary>課後練習：判斷回答錯在哪裡</summary>
<div class="section-eyebrow">(03-1) 錯誤診斷</div>
<h2 class="section-heading">回答看起來順，不代表可以直接使用</h2>
<p class="body-text">下面三個短例子各代表一種不同的錯誤。先保留原回答，指出錯誤類型與可能造成的誤用，再決定只修哪一個欄位。工作台要留下你的判斷理由與答案。</p>
<div class="scenario-grid">
<div class="scenario-row"><div class="scenario-task">錯例 A｜能力邊界</div><div class="scenario-pick"><strong>回答：</strong>「我什麼問題都能處理，而且提供的資訊都一定正確。」<br/><strong>先判斷：</strong>這句話過度承諾，沒有說明能力範圍。<br/><strong>修復方向：</strong>要求它列出能協助的三類工作，並說明哪些內容需要人查證；驗收時看是否留下限制。</div></div>
<div class="scenario-row"><div class="scenario-task">錯例 B｜即時資料</div><div class="scenario-pick"><strong>回答：</strong>「明天台北降雨機率 60%，下午會下雨。」但沒有回答時間或來源。<br/><strong>先判斷：</strong>數字看似精確，卻無法確認資料新舊。<br/><strong>修復方向：</strong>補問資料時間、來源；若模型拿不到即時資料，就把數字標為「待查官方資訊」，不要直接當成事實。</div></div>
<div class="scenario-row"><div class="scenario-task">錯例 C｜資訊遺漏</div><div class="scenario-pick"><strong>回答：</strong>通知摘要只寫「週三晚上清潔停車場，請移車。」<br/><strong>先判斷：</strong>漏掉下午 6 點前移車、雨天順延與下午 5 點再次公告。<br/><strong>修復方向：</strong>回到原文逐項對照；只補回遺漏資訊，不自行增加罰則或新規定。</div></div>
</div>
<div class="intro-band"><div class="intro-label">診斷句型</div><div class="intro-text">「這個回答不能直接使用，因為它漏了／假設了＿＿；可能造成＿＿。我先改＿＿這一欄，再重問並比較＿＿是否真的出現。」</div></div>
</details></section><hr class="section-rule"/><section class="lesson-section" id="lesson-practice"><div class="section-eyebrow">(03) 個人工作台</div><h2 class="section-heading">保存自己的首版與一項修正</h2><p class="body-text">展開後，把自己的提示詞與前後版貼回對應欄位。填完不等於內容正確，請依頁尾清單核對。</p><details class="workbench-disclosure ch1-workbench-disclosure" id="practice-workbench">
<summary class="workbench-title" id="workbench-title">第 1 單元實務工作台</summary>
<div aria-labelledby="workbench-title" class="workbench" id="practice-workbench-panel">
<div class="workbench-header">
<div><p class="workbench-lede">在這裡完成、暫存與檢核；外部 LLM 的回答請複製後貼回對應欄位。</p></div>
<div class="workbench-progress"><div class="workbench-progress-label" id="workbench-progress-label">完成進度 0%</div><div aria-hidden="true" class="workbench-progress-bar"><div class="workbench-progress-fill" id="workbench-progress-fill"></div></div><div aria-live="polite" class="workbench-status" id="workbench-status" role="status">尚未開始填寫</div></div>
</div>
<div class="workbench-note"><strong>先知道：</strong>這裡不會自動讀取任何外部 LLM 對話；你只需要複製回答貼回欄位。資料只暫存在目前瀏覽器，不會上傳雲端；完成一個階段就按「匯出 Markdown」留一份自己的副本。</div>
<form autocomplete="off" id="unit1-workbench"><section aria-labelledby="wb-transfer-title" class="wb-panel">
<div class="wb-meta">
<div class="wb-field"><label for="wb-name">姓名或代號</label><input data-field="name" data-required="false" id="wb-name" placeholder="例如：小安" type="text"/></div>
<div class="wb-field"><label for="wb-date">開始日期</label><input data-field="date" data-required="false" id="wb-date" type="date"/></div>
</div><h3 id="wb-transfer-title">一、自己的工作任務與第一版</h3>
<p class="wb-panel-lede">必填下方完整提示詞與第一版、待確認及下一步；五欄可寫在同一prompt，其他拆解欄選做。先展開材料選一案，沒有自己的資料就用模擬案。</p>
<div class="wb-field"><label for="wb-personal-prompt">我的案例、完整提示詞與第一版</label><textarea class="tall" data-field="personalPrompt" data-required="true" id="wb-personal-prompt" placeholder="案名：A｜課前提醒
提示詞：貼完整五欄與原文
第一版：貼自己的實際回答"></textarea></div>
<div class="wb-grid"><div class="wb-field"><label for="wb-personal-gap">還缺什麼、問誰</label><textarea data-field="personalGap" data-required="true" id="wb-personal-gap" placeholder="設備借用結果待確認；詢問行政窗口"></textarea></div><div class="wb-field"><label for="wb-personal-next">接下來做什麼</label><textarea class="tall" data-field="personalNext" data-required="true" id="wb-personal-next" placeholder="確認借用結果後更新提醒；負責角色與日期未提供則寫待確認"></textarea></div></div>
<details><summary>課後選做：五欄拆解與生活練習</summary><div class="wb-field"><label for="wb-personal-need">我的真實需求</label><textarea data-field="personalNeed" data-required="false" id="wb-personal-need" placeholder="例如：想安排週末、整理住戶通知、向家人解釋一個名詞"></textarea></div><div class="wb-grid"><div class="wb-field"><label for="wb-personal-situation">情境</label><textarea data-field="personalSituation" data-required="false" id="wb-personal-situation" placeholder="事情發生在哪裡？"></textarea></div><div class="wb-field"><label for="wb-personal-task">任務</label><textarea data-field="personalTask" data-required="false" id="wb-personal-task" placeholder="希望 LLM 幫你做什麼？"></textarea></div><div class="wb-field"><label for="wb-personal-data">資料</label><textarea data-field="personalData" data-required="false" id="wb-personal-data" placeholder="LLM 必須知道什麼？"></textarea></div><div class="wb-field"><label for="wb-personal-conditions">條件</label><textarea data-field="personalConditions" data-required="false" id="wb-personal-conditions" placeholder="不能違反的限制"></textarea></div><div class="wb-field"><label for="wb-personal-format">格式</label><textarea data-field="personalFormat" data-required="false" id="wb-personal-format" placeholder="答案要長什麼樣？"></textarea></div></div><div class="wb-field"><label for="wb-transfer-changed-variable">我在這個新任務改變了什麼</label><textarea data-field="transferChangedVariable" data-required="false" id="wb-transfer-changed-variable" placeholder="例如：把晚餐規劃改成社區通知整理，對象改成住戶，並新增「三個條列」的格式要求"></textarea></div></details></section><section aria-labelledby="wb-revision-title" class="wb-panel">
<h3 id="wb-revision-title">二、只修一項並保存新版</h3>
<p class="wb-panel-lede">針對同一份工作短文的一個具體缺口修正。第一版已在上方保存；不要再抄一次，也不要同時換讀者與資料。</p>
<div class="wb-grid"><div class="wb-field"><label for="wb-revision-problem">要修正的一處：原文、回答與影響</label><textarea data-field="revisionProblem" data-required="true" id="wb-revision-problem" placeholder="原文：借用待確認
回答：每人可借
影響：學員可能不帶手機；若原本正確，寫核對符合原文"></textarea></div></div>
<div class="wb-field"><label for="wb-revision-variable">本次改哪一欄</label><select class="wb-select" data-field="revisionVariable" data-required="true" id="wb-revision-variable" placeholder="本次唯一新增／修正條件"><option value="">請選擇</option><option>情境／使用對象</option><option>任務</option><option>資料</option><option>一項限制條件</option><option>輸出格式</option></select><small>選唯一修正欄位；具體新增條件寫在下方指令，例如「不得將受理寫成已修復」。其他資料／讀者／格式維持。</small></div>
<div class="wb-field"><label for="wb-revision-instruction">我送出的修正指令</label><textarea data-field="revisionInstruction" data-required="true" id="wb-revision-instruction" placeholder="貼實際送出的完整指令；只指定本次一項要求"></textarea></div>
<div class="wb-grid"><div class="wb-field"><label for="wb-revision-response">修正版完整短文</label><textarea class="tall" data-field="revisionResponse" data-required="true" id="wb-revision-response" placeholder="貼新版全文；若自己修改，先標「人工修正」"></textarea></div><div class="wb-field"><label for="wb-revision-kept">修改前後與核對依據</label><textarea data-field="revisionKept" data-required="true" id="wb-revision-kept" placeholder="原句：…
新句：…
依據：原文…；無差異時記下查過的句子"></textarea></div></div>
<details><summary>課後選做：其他題目與補充判斷</summary><div class="wb-field"><label for="wb-revision-target">我選擇檢查第幾題</label><select class="wb-select" data-field="revisionTarget" data-required="false" id="wb-revision-target"><option value="">請選擇</option><option>第 1 題｜自我介紹</option><option>第 2 題｜天氣</option><option>第 3 題｜晚餐</option><option>第 4 題｜ETF</option><option>第 5 題｜通知</option></select></div><div class="wb-field"><label for="wb-revision-original">第一版提示詞與回答</label><textarea class="tall" data-field="revisionOriginal" data-required="false" id="wb-revision-original" placeholder="貼上原本送出的提示詞與完整回答，方便回看缺少什麼"></textarea></div><div class="wb-field"><label for="wb-revision-better">現在是否可用／仍缺什麼</label><textarea data-field="revisionBetter" data-required="false" id="wb-revision-better" placeholder="說明補一個條件後改善了什麼；若仍不能使用，寫下下一個要查證的地方"></textarea></div></details></section><section aria-labelledby="wb-check-title" class="wb-panel">
<h3 id="wb-check-title">三、主線完成檢查</h3>
<div class="wb-checklist">
<label class="wb-check"><input data-field="check1" data-required="true" type="checkbox"/><span>我保存自己的完整提示詞、第一版及新版短文。</span></label>
<label class="wb-check"><input data-field="check3" data-required="true" type="checkbox"/><span>我只修一項並保留完整指令及前後核對。</span></label>
<label class="wb-check"><input data-field="check5" data-required="true" type="checkbox"/><span>我列待確認、確認者與下一步，沒有增加原文未有的承諾。</span></label>
<label class="wb-check"><input data-field="check8" data-required="true" type="checkbox"/><span>變化對應唯一條件；若沒有差異，我如實記錄。</span></label>
</div>
<details><summary>課後選做：五個生活對話與錯誤檢查</summary><label class="wb-check"><input data-field="check2" data-required="false" type="checkbox"/><span>第 2–5 題都留下完整回答與我判斷是否可用的理由。</span></label><label class="wb-check"><input data-field="check4" data-required="false" type="checkbox"/><span>每個基本問題都有任務、資料、條件或輸出格式。</span></label><label class="wb-check"><input data-field="check6" data-required="false" type="checkbox"/><span>自己的任務卡填齊五欄，並留下可直接使用、待確認與下一步。</span></label><label class="wb-check"><input data-field="check7" data-required="false" type="checkbox"/><span>我完成一份錯誤診斷，說明錯誤、可能後果、修復方向與可觀察證據。</span></label></details></section><details><summary>課後選做：五個生活對話與錯誤診斷</summary><section aria-labelledby="wb-dialogues-title" class="wb-panel">
<h3 id="wb-dialogues-title">一、五個基本對話</h3>
<p class="wb-panel-lede">每題先把提示詞送給 LLM，再把完整回答貼回；不要只留下最後整理出的幾個字。</p>
<div class="wb-question">
<div class="wb-question-header"><div class="wb-question-title">1｜請 LLM 介紹自己</div><span class="tool-tag">觀察說明能力</span></div>
<div class="wb-prompt"><div class="wb-prompt-label"><span>可直接複製的提示詞</span><button class="wb-copy" data-copy-target="wb-prompt-q1" type="button">複製提示詞</button></div><code id="wb-prompt-q1">你是誰？請用一般人聽得懂的方式，說明你可以幫我做哪三種事情，以及哪些事情需要我自己再確認。</code></div>
<div class="wb-field"><label for="wb-q1-response">LLM 完整回答</label><textarea class="tall" data-field="q1Response" data-required="false" id="wb-q1-response" placeholder="從 LLM 複製完整回答貼在這裡"></textarea></div>
<div class="wb-field"><label for="wb-q1-observation">我觀察到的三類能力與一個確認提醒</label><textarea data-field="q1Observation" data-required="false" id="wb-q1-observation" placeholder="例如：能協助整理文字；提醒日期與價格仍要確認"></textarea></div>
</div>
<div class="wb-question">
<div class="wb-question-header"><div class="wb-question-title">2｜詢問明天台北的天氣</div><span class="tool-tag">辨認資料依據</span></div>
<div class="wb-prompt"><div class="wb-prompt-label"><span>可直接複製的提示詞</span><button class="wb-copy" data-copy-target="wb-prompt-q2" type="button">複製提示詞</button></div><code id="wb-prompt-q2">明天台北會下雨嗎？請先說明你回答所根據的時間；如果無法取得即時資料，請告訴我應該查哪一種官方資訊。</code></div>
<div class="wb-field"><label for="wb-q2-response">LLM 完整回答</label><textarea class="tall" data-field="q2Response" data-required="false" id="wb-q2-response" placeholder="貼上完整回答；沒有即時資料時，也保留它的限制說明"></textarea></div>
<div class="wb-grid"><div class="wb-field"><label for="wb-q2-evidence">回答中的時間／來源，或無法判斷的原因</label><textarea data-field="q2Evidence" data-required="false" id="wb-q2-evidence" placeholder="例如：沒有即時資料，建議查中央氣象署"></textarea></div><div class="wb-field"><label for="wb-q2-observation">我判斷是否可用／理由</label><textarea data-field="q2Observation" data-required="false" id="wb-q2-observation" placeholder="我會先確認資料時間與來源，因為……"></textarea></div></div>
</div>
<div class="wb-question">
<div class="wb-question-header"><div class="wb-question-title">3｜請 LLM 提供晚餐建議</div><span class="tool-tag">核對條件</span></div>
<div class="wb-prompt"><div class="wb-prompt-label"><span>可直接複製的提示詞</span><button class="wb-copy" data-copy-target="wb-prompt-q3" type="button">複製提示詞</button></div><code id="wb-prompt-q3">我今天下班後想吃晚餐。請依照以下條件提出三個選項：兩人、預算 600 元、不吃牛、希望 30 分鐘內完成。請用表格列出菜色、預估時間與預算，最後告訴我還缺哪一個條件。</code></div>
<div class="wb-field"><label for="wb-q3-response">LLM 完整回答</label><textarea class="tall" data-field="q3Response" data-required="false" id="wb-q3-response" placeholder="貼上完整回答"></textarea></div>
<div class="wb-grid"><div class="wb-field"><label for="wb-q3-choice">最符合我的選項</label><textarea data-field="q3Choice" data-required="false" id="wb-q3-choice" placeholder="選項與原因"></textarea></div><div class="wb-field"><label for="wb-q3-observation">我判斷是否可用／理由</label><textarea data-field="q3Observation" data-required="false" id="wb-q3-observation" placeholder="逐一核對兩人、不吃牛、600 元、30 分鐘"></textarea></div></div>
</div>
<div class="wb-question">
<div class="wb-question-header"><div class="wb-question-title">4｜請 LLM 解釋 ETF</div><span class="tool-tag">分辨解釋與推薦</span></div>
<div class="wb-prompt"><div class="wb-prompt-label"><span>可直接複製的提示詞</span><button class="wb-copy" data-copy-target="wb-prompt-q4" type="button">複製提示詞</button></div><code id="wb-prompt-q4">請用沒有金融背景的人聽得懂的方式解釋 ETF。先用一句話說明，再用一個生活化例子，最後列出三個我還需要查證的問題。不要直接推薦我買任何商品。</code></div>
<div class="wb-field"><label for="wb-q4-response">LLM 完整回答</label><textarea class="tall" data-field="q4Response" data-required="false" id="wb-q4-response" placeholder="貼上完整回答"></textarea></div>
<div class="wb-grid"><div class="wb-field"><label for="wb-q4-restate">我能用自己的話重述</label><textarea data-field="q4Restate" data-required="false" id="wb-q4-restate" placeholder="用自己的話說明一籃子資產與交易方式"></textarea></div><div class="wb-field"><label for="wb-q4-observation">我判斷是否可用／理由</label><textarea data-field="q4Observation" data-required="false" id="wb-q4-observation" placeholder="是否有定義、例子、待查問題，且沒有變成推薦"></textarea></div></div>
</div>
<div class="wb-question">
<div class="wb-question-header"><div class="wb-question-title">5｜請 LLM 整理一段通知</div><span class="tool-tag">保留關鍵資訊</span></div>
<div class="wb-prompt"><div class="wb-prompt-label"><span>可直接複製的提示詞</span><button class="wb-copy" data-copy-target="wb-prompt-q5" type="button">複製提示詞</button></div><code id="wb-prompt-q5">本週社區將於週三晚上七點進行停車場清潔，請住戶在下午六點前移走車輛。若遇雨天，工作順延至週四同一時間。管理室會在當天下午五點再次公告。請把上面的通知整理成三個條列重點，保留五項資訊：週三晚上 7 點、下午 6 點前移車、雨天順延至週四同一時間、管理室下午 5 點再次公告、住戶需要採取的行動。</code></div>
<div class="wb-field"><label for="wb-q5-response">LLM 完整回答</label><textarea class="tall" data-field="q5Response" data-required="false" id="wb-q5-response" placeholder="貼上完整回答"></textarea></div>
<div class="wb-grid"><div class="wb-field"><label for="wb-q5-result">整理結果中的三個重點</label><textarea data-field="q5Result" data-required="false" id="wb-q5-result" placeholder="可直接摘錄回答中的三個條列"></textarea></div><div class="wb-field"><label for="wb-q5-observation">我判斷是否可用／理由</label><textarea data-field="q5Observation" data-required="false" id="wb-q5-observation" placeholder="確認日期、所有時間、住戶行動與雨天備案"></textarea></div></div>
</div>
</section><section aria-labelledby="wb-error-title" class="wb-panel">
<h3 id="wb-error-title">二、錯誤診斷與修復方向</h3>
<p class="wb-panel-lede">回看上方三個錯例，選一個最能說明你目前困惑的類型。先寫出錯誤與可能後果，再指定只要修哪一個欄位；這份紀錄要留下判斷與修復依據，文字是否漂亮不是本題的驗收條件。</p>
<div class="wb-field"><label for="wb-error-case">我選擇的錯例</label><select class="wb-select" data-field="errorCase" data-required="false" id="wb-error-case"><option value="">請選擇</option><option>錯例 A｜能力邊界：過度承諾</option><option>錯例 B｜即時資料：沒有時間／來源</option><option>錯例 C｜資訊遺漏：摘要少了行動與備案</option></select></div>
<div class="wb-field"><label for="wb-error-diagnosis">我判斷錯在哪裡、可能造成什麼誤用</label><textarea data-field="errorDiagnosis" data-required="false" id="wb-error-diagnosis" placeholder="例如：回答給了精確數字卻沒有資料時間，讀者可能把舊資料當成明天天氣"></textarea></div>
<div class="wb-grid"><div class="wb-field"><label for="wb-error-repair">我只先修哪一個欄位／要補問什麼</label><textarea data-field="errorRepair" data-required="false" id="wb-error-repair" placeholder="例如：先補「資料時間與來源」，不先改語氣或版面"></textarea></div><div class="wb-field"><label for="wb-error-evidence">修復後我要看見什麼證據</label><textarea data-field="errorEvidence" data-required="false" id="wb-error-evidence" placeholder="例如：回答說明查詢時間，或明確寫出無法取得即時資料與下一步查證位置"></textarea></div></div>
</section></details>
<div class="wb-actions"><button class="wb-action primary" data-action="save" type="button">儲存到本機</button><button class="wb-action" data-action="export" type="button">匯出 Markdown</button><button class="wb-action" data-action="print" type="button">列印工作台</button><button class="wb-action danger" data-action="reset" type="button">清除本機資料</button></div>
<p class="wb-footnote">建議完成每個階段就匯出一次。這份匯出檔才是可帶到下一單元或交給他人檢視的完成物；瀏覽器暫存只是方便你中斷後繼續。</p>
</form>
</div>
</details><details><summary>課後選做：五個生活對話的操作說明</summary>
<div class="section-eyebrow">(04) 實作練習</div>
<h2 class="section-heading">課後選做：五個生活對話與一次修正</h2>
<p class="body-text">看完示範與錯誤判讀後，現在開始操作。請依照下方路線完成紀錄；每個欄位都會成為最後可重做的實務成果。</p>
<div class="intro-band"><div class="intro-label">六站操作路線</div><div class="intro-text">依序完成：步驟 1 建立第一筆回答 → 步驟 2 完成五題並套用判準 → 步驟 3 診斷一個錯誤 → 步驟 4 只改一個變因重問 → 步驟 5 把方法帶回自己的任務 → 步驟 6 匯出並檢查可重做性。提示詞與回答都只在上方工作台處理。</div></div>
<div class="scenario-grid">
<div class="scenario-row"><div class="scenario-task">步驟 1｜U1-START：建立第一筆回答</div><div class="scenario-pick"><strong>操作：</strong>填姓名／日期，從工作台第 1 題複製提示詞，送到你可使用的文字型 LLM，再把完整回答貼回。<br/><strong>完成判準：</strong>回答欄有完整文字、進度有變化、重新整理後仍能恢復。<br/><strong>卡住時：</strong>回到 U1-START；工具不可用時先閱讀離線備援結果，工具恢復後再重做。</div></div>
<div class="scenario-row"><div class="scenario-task">步驟 2｜U1-ASK：完成五題並判讀</div><div class="scenario-pick"><strong>操作：</strong>依工作台順序完成五題，保存原始提示詞、完整回答與判斷。<br/><strong>完成判準：</strong>第 1 題看能力邊界、第 2 題看時間／來源、第 3 題看四個條件、第 4 題分開解釋與推薦、第 5 題確認資訊保留。<br/><strong>卡住時：</strong>回到對應題目，重新檢查任務、條件與輸出格式。</div></div>
<div class="scenario-row"><div class="scenario-task">步驟 3｜U1-DIAG：診斷一個錯誤</div><div class="scenario-pick"><strong>操作：</strong>從三個錯例選一個，寫出錯誤類型、可能後果、修復方向與可觀察證據。<br/><strong>完成判準：</strong>你能指出回答缺少的依據、可能造成的誤用與回修位置；只寫「感覺不太好」不算。<br/><strong>卡住時：</strong>回看錯誤診斷區的診斷句型，先填「漏了／假設了什麼」與「可能造成什麼誤用」。</div></div>
<div class="scenario-row"><div class="scenario-task">步驟 4｜U1-GAP：只改一個變因</div><div class="scenario-pick"><strong>操作：</strong>從五題挑一題，找出最影響結果的一個缺口，指定唯一變因後重問一次。<br/><strong>完成判準：</strong>前後回答的差異能回連到唯一新增條件；若仍不能使用，另外寫出待查資料。<br/><strong>卡住時：</strong>一次只補人數、預算、日期、讀者或格式其中一項，保留第一版作比較。</div></div>
<div class="scenario-row"><div class="scenario-task">步驟 5｜U1-SOLO：帶回自己的任務</div><div class="scenario-pick"><strong>操作：</strong>在工作台的「建立自己的任務卡」區，換一份素材、對象或限制，填情境、任務、資料、條件與格式。<br/><strong>完成判準：</strong>有一份自己的五欄提示詞、第一版回答、改變的地方、待確認與下一步；不需要再回頭重做五題。<br/><strong>卡住時：</strong>先從週末安排、通知整理或陌生名詞 starter 擇一，明確寫出它和晚餐示範不同的素材或對象。</div></div>
<div class="scenario-row"><div class="scenario-task">步驟 6｜U1-SAVE：匯出並檢查</div><div class="scenario-pick"><strong>操作：</strong>完成工作台檢查後匯出 <code>unit1-practice-sheet-complete.md</code>，或在瀏覽器無法下載時列印成 PDF。<br/><strong>完成判準：</strong>沒有參加這堂課的人也能看出你問了什麼、哪個錯誤被修復、只改了什麼、缺什麼資料與下一步。<br/><strong>卡住時：</strong>回到缺少的欄位補齊，先保存目前版本再重新匯出。</div></div>
</div>
<div class="callout"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>Checkpoint U1-CHECK</strong>　通過條件是：五題紀錄、一份錯誤診斷、一次單一變因比較、一張個人任務卡與匯出檔都已完成。打開匯出檔，確認讀者能看出你問了什麼、哪裡不能直接相信、只改了什麼、還缺什麼資料與下一步。</div></div>
</details></section><hr class="section-rule"/><section class="lesson-section" id="lesson-check"><div class="section-eyebrow">(04) 成品檢查</div><h2 class="section-heading">只看匯出檔，能否重做這份短文？</h2><p class="body-text">檢查：原文與提示詞完整；第一版、新版與一次修正都在；重要日期、狀態及數字符合原文；待確認事項有確認者與下一步。</p><p class="body-text">重開 <code>unit1-practice-sheet-complete.md</code>，確認原文、第一版與修正版都在。缺內容就回工作台補上再匯出。</p></section><hr class="section-rule"/><section class="lesson-section" id="lesson-assets"><details><summary>離線工作表與備援範例</summary>
<div class="section-eyebrow">(06) 試跑包</div>
<h2 class="section-heading">本頁用到的材料與備援</h2>
<div class="tool-grid"><div class="tool-card"><div class="tool-name">離線匯出／備援工作表</div><div class="tool-tag">Markdown</div><div class="tool-summary"><a href="assets/worksheets/unit1-practice-sheet.md">開啟 `unit1-practice-sheet.md`</a>。只有在瀏覽器不能暫存、需要離線處理或要手動重建紀錄時使用。</div><div class="tool-list"><div class="tool-list-item"><span class="tool-check">✓</span>可複製到自己的文字編輯器</div><div class="tool-list-item"><span class="tool-check">✓</span>完成後保存成 `unit1-practice-sheet-complete.md`</div></div></div><div class="tool-card"><div class="tool-name">離線備援結果</div><div class="tool-tag">Markdown</div><div class="tool-summary"><a href="assets/fallback/unit1-dialogue-simulator.md">開啟離線備援文件</a>。LLM 暫時不可用時，先練習五題的輸入條件與示例結果。</div><div class="tool-list"><div class="tool-list-item"><span class="tool-check">✓</span>可完成五題的輸入與示例判讀</div><div class="tool-list-item"><span class="tool-check">✓</span>限制：工具恢復後仍要重跑自己的五次對話</div></div></div></div>
</details></section><hr class="section-rule"/><section class="lesson-section"><details><summary>課後查閱：常見問題與處理方法</summary>
<div class="section-eyebrow">(07) 常見錯誤</div>
<h2 class="section-heading">回答不合用時，回到對應階段修</h2>
<div class="troubleshoot"><div class="ts-item"><div class="ts-label">PITFALL 01</div><div class="ts-q">輸入只有「幫我處理一下」，回答看似完整但和需求不相干。</div><div class="ts-a"><strong>原因：</strong>沒有交代任務、條件與輸出格式。<br/><strong>修復：</strong>回到 U1-ASK，先補五欄中最影響結果的一欄，再重跑一個小任務。</div></div><div class="ts-item"><div class="ts-label">PITFALL 02</div><div class="ts-q">補了條件，第二版卻只變短或換了語氣。</div><div class="ts-a"><strong>原因：</strong>重問指令沒有明確要求模型使用新條件，或同時改了多個目的。<br/><strong>修復：</strong>回到 U1-GAP，把「補上的條件」放進任務句，並比較它在輸出中的位置。</div></div><div class="ts-item"><div class="ts-label">PITFALL 03</div><div class="ts-q">只保存最後回答，無法說明原本問了什麼。</div><div class="ts-a"><strong>原因：</strong>沒有把原始提示詞與第一版回答一起保存。<br/><strong>修復：</strong>回到 U1-SAVE，依序保存原始輸入、第一版、補條件指令與第二版。</div></div></div>
</details></section><hr class="section-rule"/><section class="lesson-section" id="lesson-quiz"><details><summary>課後自我檢查</summary>
<div class="section-eyebrow">(08) 自我檢核</div>
<h2 class="section-heading">兩題確認你能把方法帶走</h2>
<div class="quiz-item"><div class="quiz-q">Q1：哪一句最適合交給 LLM 產生晚餐初稿？</div><div class="quiz-opts"><label class="quiz-opt"><input name="q1" type="radio"/><span>A. 晚餐吃什麼？</span></label><label class="quiz-opt"><input name="q1" type="radio"/><span>B. 幫我找晚餐。</span></label><label class="quiz-opt"><input name="q1" type="radio"/><span>C. 兩人、不吃牛、預算 600 元、30 分鐘內完成，請用表格提出三個晚餐選項。</span></label><label class="quiz-opt"><input name="q1" type="radio"/><span>D. 今天很累。</span></label></div><details class="quiz-ans"><summary>顯示答案</summary><div>正確答案：C。它交代了任務、條件與輸出格式，LLM 才能產生可對照的初稿。</div></details></div>
<div class="quiz-item"><div class="quiz-q">Q2：晚餐回答看起來很多，但沒有依你的家庭人數與預算安排。下一輪怎麼問最能檢驗「補條件」是否有效？</div><div class="quiz-opts"><label class="quiz-opt"><input name="q2" type="radio"/><span>A. 請改得更好、更實用。</span></label><label class="quiz-opt"><input name="q2" type="radio"/><span>B. 請改成比較輕鬆的語氣。</span></label><label class="quiz-opt"><input name="q2" type="radio"/><span>C. 補上「兩人、預算 600 元、30 分鐘內」，仍提出三個選項，並標出仍缺的條件。</span></label><label class="quiz-opt"><input name="q2" type="radio"/><span>D. 請再列十個選項。</span></label></div><details class="quiz-ans"><summary>顯示答案</summary><div>正確答案：C。它只補上會影響晚餐選項的條件，並要求模型把未知處留下來，前後差異才可回查。</div></details></div>
</details></section>
<!-- learner-content:end -->

## 歷史教案（非現行必做契約）

---
title: "第一次與 LLM 對話：把日常問題說清楚"
slug: ai-beginner-practical
unit_id: CH1-1
chapter: CH1-1
course_type: skill-operation
duration: 3h
audience: "第一次系統使用文字型語言模型的零基礎成人學習者"
prerequisites: "能使用瀏覽器、複製貼上與基本文字輸入"
learning_objective: 能用情境、任務、資料、條件、格式五欄定義日常任務，完成五個基本對話，診斷一種錯誤、只改一個變因重問，並把方法轉用到自己的任務
deliverables:
  - "五個日常問題的原始提示詞、完整回答與可用性判斷"
  - "一份錯誤診斷與修復方向紀錄，含錯誤、可能誤用與可觀察證據"
  - "一份只改一個變因、重問與比較的前後紀錄"
  - "一張改變素材或對象後的五欄任務卡，含待確認與下一步"
  - "一份由頁內工作台匯出的 unit1-practice-sheet-complete.md"
environment: "任何能輸入文字、送出問題、複製回答與保存文字的 LLM；本單元不指定平台"
style_guide: ai-beginner-practical/STYLE-GUIDE.md
platform_version: LLM 通用方法（平台中立，2026-09）
status: draft
---

## Learner Task Contract（學員任務契約）

| 契約欄位 | 本單元凍結事實 |
|---|---|
| 角色與工作情境 | 你是第一次系統使用文字型語言模型的成人學習者，正在處理解釋、整理、規劃與查詢邊界不同的日常小任務。 |
| 問題與後果 | 只輸入「幫我想一下」或「這是什麼」容易得到泛泛、漏條件或無法查證的回答；不保留原始輸入與判斷，就無法重做。 |
| 起始材料 | CH1-1 頁內工作台、五個示範問題、任何可用的文字型 LLM；瀏覽器表單不可用時才用 assets/worksheets/unit1-practice-sheet.md，工具不可用時用 assets/fallback/unit1-dialogue-simulator.md。 |
| 目標完成物 | 五題完整紀錄、一份錯誤診斷、一次單一變因比較、一張個人五欄任務卡與八項完成檢查；匯出為 unit1-practice-sheet-complete.md。 |
| 下一位使用者與用途 | 未來的你可以依任務卡重做；CH2-1 直接承接五欄任務定義，進一步處理讀者、目的、語氣與格式，不重播五題流程。 |
| 第一個動作 | 開啟頁內工作台，填姓名／日期，複製第 1 題提示詞到自己能使用的文字型 LLM，再把完整回答貼回。 |
| 第一個可觀察結果 | 工作台出現第 1 題回答與進度變化；重新整理後仍能看到暫存內容，否則回 U1-START。 |
| 失敗時的回復位置 | 回答偏題回 U1-ASK；說不出錯誤與後果回 U1-DIAG；補條件後無差異回 U1-GAP；暫存失敗先匯出或列印，工具不可用則標記待重跑。 |

## 教學流程與 180 分鐘節奏

### 1. 破題：先看完成物（0–15 分）

展示一份「只有最後答案」與一份「原始提示詞、回答、判斷、待確認、修復前後差異」並列的紀錄。學員指出哪一份能讓下一個人重做，建立本課完成線：五題、一份錯誤診斷、一次單一變因比較、一張自己的任務卡。

### 2. 概念：五欄不是格式作業（15–35 分）

- 情境：事情在哪裡發生、誰會使用結果。
- 任務：希望模型完成哪個動作。
- 資料：模型必須知道的已知資訊。
- 條件：不能違反的限制，以及仍待確認的資料。
- 格式：答案要長什麼樣，方便閱讀或採取行動。

五欄用來定義任務，不是要學員把同一題重寫三次；本單元只在一次練習中補一個最關鍵條件。

### 3. 一筆完整示範（35–65 分）

晚餐題是本單元唯一完整 worked example，從模糊輸入、補五欄、讀回答到判斷缺資料。講師再展示一個漏掉條件的短回答，只修一個條件並對照差異。這一段由講師示範與全班判讀，不要求學員先填自己的五題，避免示範與操作重疊。

### 4. 錯誤診斷與變因實驗（65–100 分）

學員先用頁面提供的三個短錯例，分辨能力過度承諾、即時資料無時間／來源、摘要遺漏三種錯誤。接著在工作台選一個錯例，寫下可能誤用、修復方向與可觀察證據。講師帶全班比較「只改一個欄位」和「整段重寫」的差異。

### 5. 唯一操作區：工作台六站（100–170 分）

學員只在 HTML 第 04 節的唯一工作台操作：完成五題、完成一份錯誤診斷、指定一個變因重問、建立一份不同素材或對象的任務卡，最後匯出。工作台是產出入口；本節的六站路線只說明順序、完成判準與回復位置，不在其他區段重印提示詞或回答。

### 6. 匯出與交接（170–180 分）

學員完成工作台檢查並匯出。兩人互看完成物，只回答四題：原本要做什麼？哪裡不能直接相信？只改了哪一個變因？下一步還要確認什麼？答不出來就回 U1-SAVE、U1-DIAG 或 U1-GAP；不另開第二份表格。

## 完整 worked example

### 示範輸入

學員從頁面工作台第 3 題複製完整提示詞；本教案不再於其他段落重印同一輸入。

### 教師示範輸出

| 選項 | 菜色 | 預估時間 | 預算 |
|---|---|---:|---:|
| A | 番茄雞肉義大利麵＋沙拉 | 25 分鐘 | 420 元 |
| B | 豆腐蔬菜鍋＋白飯 | 30 分鐘 | 480 元 |
| C | 蝦仁蛋炒飯＋燙青菜 | 20 分鐘 | 360 元 |

### 教師示範判斷

- 已回應：兩人、不吃牛、600 元、30 分鐘、三個選項與表格。
- 仍未知：家中現有食材、所在地、當日價格、是否需要外帶。
- 可重做紀錄：保留提示詞、完整回答、逐欄核對與待確認，不把示意價格當成事實。

### 缺條件比較

第一版只有「請幫我想晚餐，列出三個選項」。重問時只補「兩人」這一個變因，其他輸入、輸出格式與任務保持不變。若第二版沒有出現適合兩人的份量或安排，就回到 U1-GAP 重跑；不能同時改預算、時間與語氣，否則無法知道差異來自哪裡。

### 錯誤診斷示範

教師展示「明天台北降雨機率 60%，下午會下雨」但沒有時間或來源的回答。學員先說出可能誤用（把舊資料當成即時事實），再指定修復欄位（資料時間／來源），最後定義證據（回答交代查詢時間，或明確標示無法取得即時資料與下一步）。

### 轉用示範

教師不再重做晚餐題，改用「把社區公告整理成住戶看得懂的三個條列」作為轉用材料。學員指出新素材、讀者與格式，並說明這三項和晚餐規劃不同；只套用五欄方法，不複製晚餐內容。

### 五題案例對照

HTML 在五題工作台前提供四個快速對照案例：自我介紹、即時天氣、ETF 解釋與社區通知。每個案例都保留完整提示詞、具體示範回答與常見錯誤；學員先比較回答如何使用輸入條件，再送出自己的回答。天氣範例不捏造即時預報，社區通知保留「當天」的歧義並標示待確認。這些案例是教學證據，不取代學員保存自己的實際輸出。

## Activity Identity

| 活動 | 素材 | 產物 | 操作路徑 | 學員決策 |
|---|---|---|---|---|
| Demo | 晚餐案例 | 五欄提示詞與條件核對 | 看輸入、回答、逐欄判讀 | 哪些資料已知、哪些仍未知 |
| Error clinic | 三個短錯例 | 一份錯誤診斷與修復方向 | 選錯誤類型，寫可能誤用與證據 | 先修哪一個欄位，不把問題改成語氣偏好 |
| Variable experiment | 五題中的一題 | 單一變因前後比較 | 保留第一版，只新增一個變因後重問 | 差異是否真的由這個變因造成 |
| Transfer practice | 不同素材、對象或限制的個人任務 | 五欄任務卡、第一版回答與待確認 | 在同一工作台建立新任務並匯出 | 如何把方法轉用，而不是複製示範 |

## 動手練習與驗收

1. 步驟 1｜U1-START：跳到第 04 節唯一工作台，填姓名／日期並完成第一筆回答。
2. 步驟 2｜U1-ASK：完成五題，保存提示詞、完整回答與自己的判斷。
3. 步驟 3｜U1-DIAG：從三個短錯例選一個，寫錯誤、可能誤用、修復方向與證據。
4. 步驟 4｜U1-GAP：選一題只改一個變因，保存前後版本與差異。
5. 步驟 5｜U1-SOLO：換一份素材、對象或限制，在同一工作台填自己的五欄任務卡，送出一版並記下待確認。
6. 步驟 6｜U1-SAVE：完成檢查並匯出；打開匯出檔確認欄位沒有遺失。

### 通過標準

- 五題都有完整回答，且第 2–5 題有可用性判斷。
- 完成一份錯誤診斷，能說出錯誤、可能誤用、修復方向與可觀察證據。
- 至少一題完成「找缺口 → 只改一個變因 → 重問 → 比較」，前後差異可回連到該變因。
- 個人任務卡五欄完整，且使用不同素材、對象或限制；待確認與下一步不是空白。
- 完成物不把模型補寫的日期、價格、資格或事實當成已確認資訊。
- 另一個人只看匯出檔即可重做或指出下一步。

## 試跑包需求清單

- CH1-1.html：第 04 節唯一主線工作台與六站操作路線；第 01 節只保留任務契約。
- assets/worksheets/unit1-practice-sheet.md：表單不可用時的離線備援，不是預設入口。
- assets/fallback/unit1-dialogue-simulator.md：工具不可用時的示範判讀，恢復後必須重跑正式對話。
- 所有輸出欄位都要與頁內工作台的 data-field 和匯出 JS 對齊。

## 常見錯誤 4 條

1. 只寫「幫我處理」：回 U1-ASK，先補任務或輸出格式，再重跑小任務。
2. 補條件後只變短：回 U1-GAP，把新增條件放進任務句，並指出它在結果中的位置。
3. 只保存最後答案：回 U1-SAVE，補回原始提示詞、第一版、判斷與待確認。
4. 一次改很多地方：回 U1-GAP，只保留一個變因，否則無法判斷是哪個改動造成差異。

## 檢核題 2 條

1. 晚餐回答沒有說明人數與預算，最有效的下一步是什麼？
   答案：只補上兩人與預算等最關鍵條件，重問後比較；不要只要求「更好」。
2. 天氣回答沒有資料時間或來源，能不能直接當成明天天氣？
   答案：不能。要記下無法判定的原因與下一步查證位置。
