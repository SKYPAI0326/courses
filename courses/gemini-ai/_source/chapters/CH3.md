---
slug: gemini-ai
unit_id: CH3
title: 製作能處理不同資料的工作工具
course_type: skill-operation
version: 2026-10-08-five-chapters
duration: 130
dependencies: ["CH2"]
learning_objective: 製作能處理不同資料的工作工具
platform_version: Gemini web; official help checked 2026-10-08; account generation pending
---

# 製作能處理不同資料的工作工具

正式正文以下列learner-content範圍為唯一來源；HTML從此範圍轉製。內部設計依據：課程根目錄 _repair/2026-10-08/CHAPTER-REDESIGN.md。
環境：桌面瀏覽器、可登入的Gemini帳號、UTF-8純文字存檔。引用的作者參考品只能證明操作／規則，不代表授課平台生成。真人跟做及六小時試教待驗。
來源：part2/CH2-1.html, part2/PRAC2-1.html；跨章交付段落另見遷移紀錄。

<!-- learner-content:start -->
<section class="lesson-section" id="ch3-section-1"><h2 class="section-heading">從一份名單看出工具需要哪些輸入</h2><p class="body-text">第二章已教你把需求拆成輸入、規則和輸出。現在把方法用在排班工作：承辦人要安排人員值勤，但每次人員、日期和班次不同，也有人只能在特定日期值班。本章從案例抽出可重用工具結構，一路完成生成、填資料與查核，不需要跳到另一個練習單元。</p><p class="body-text">先閱讀下表的案例 A，並對照<a download="" href="../assets/materials/schedule-practice.txt">兩組排班案例 TXT</a>。本章要留下 <code>schedule-v1.html</code>、自己的 A／B 資料備份、班表及核對紀錄。可先開啟<a href="../assets/tools/schedule-reference.html" rel="noopener" target="_blank">作者排班參考品</a>預覽欄位；參考品供操作與查核，自己的生成成果仍要另外完成。</p><p class="body-text">練習A：四人、週一至週三，每日早班09:00–13:00、晚班13:00–17:00，每班需一人，每人總上限2。下表是本課用來理解與查核的資料；請先讀懂誰哪天能來。</p><div class="core-table-scroll"><table><thead><tr><th scope="col">練習A人員</th><th scope="col">週一</th><th scope="col">週二</th><th scope="col">週三</th></tr></thead><tbody><tr><td>安</td><td>可排</td><td>不可排</td><td>可排</td></tr><tr><td>柏</td><td>可排</td><td>可排</td><td>不可排</td></tr><tr><td>晴</td><td>不可排</td><td>可排</td><td>可排</td></tr><tr><td>明</td><td>可排</td><td>可排</td><td>可排</td></tr></tbody></table></div><p class="body-text">安、柏、晴、明是這次填入「姓名欄」的內容；週一至週三是「日期清單」的內容；早晚班和時間是「班種清單」的內容。遇到另一份工作時，應能在工具內新增或刪除這些項目。你要留下的成果是「欄位、設定、處理、輸出」對照表，以及一份可查核的手排示例。</p><p class="body-text">下載<a download="" href="../assets/materials/core-acceptance.csv">五章驗收表</a>，先填預期結果，完成每次操作後再填觀察與狀態。A／B 是兩組不同輸入，請保留各自紀錄，不把新結果覆寫在舊列；未操作的項目保留「待測」。</p></section>

<section class="lesson-section" id="ch3-section-2"><h2 class="section-heading">把會換的資料與可設定規則抽出來</h2><p class="body-text">先示範如何抽出欄位：看到「安週一可排」，設計的是「每位人員對每個日期都有可排勾選」。工具不應只知道安和週一，而要能對任何已加入的人員與日期建立這個勾選。再看「每人最多兩班」，設計的是可調整的總班數上限，本次操作時才填2。</p><div class="core-table-scroll"><table><thead><tr><th scope="col">這次例子</th><th scope="col">工具要提供的結構</th><th scope="col">換一份工作怎麼用</th></tr></thead><tbody><tr><td>四位人員</td><td>可新增、刪除與修改的人員清單</td><td>換姓名或新增第五位</td></tr><tr><td>週一至週三</td><td>可編輯的日期清單</td><td>改成兩個日期或新增日期</td></tr><tr><td>早班、晚班及時間</td><td>可編輯的班種、時段、需求人數</td><td>改成開場、服務、收尾</td></tr><tr><td>誰哪天可排</td><td>隨人員與日期更新的可排表</td><td>重新勾選新名單的可排日</td></tr><tr><td>每人最多兩班</td><td>非負整數的每人總班數上限</td><td>填新的上限，0代表不能安排</td></tr><tr><td>同日不能兩班</td><td>通用的排班限制</td><td>每份資料都照這條規則檢查</td></tr></tbody></table></div><p class="body-text">資料描述當次有哪些人和班；設定決定本次允許安排多少；處理負責檢查並產生班表；輸出讓使用者核對與帶走。先遵守可排日、總班數上限及同日一班，再盡量安排，最後比較工作量是否接近。四人六班的示例中，兩人各兩班、兩人各一班就比三人各兩班、另一人沒班更符合平均偏好。</p><p class="body-text">請在筆記補一列「每班需要幾人」：它應放在哪個欄位？使用者改成兩人時，輸出要怎麼變？完成後核對：它屬於班種需求的設定；工具要顯示需求、已安排與缺額，不能繼續只列一個名字。這是把案例轉成結構的練習。</p></section>

<section class="lesson-section" id="ch3-section-3"><h2 class="section-heading">用案例檢查規則，再寫成可重用的規格</h2><p class="body-text">現在依練習A手排六個班，逐格核對可排日、同日是否重複、每人是否超過兩班。先做完再看例子；不同名字順序可以接受。</p><pre class="result-box">週一早班：安　　週一晚班：柏
週二早班：晴　　週二晚班：明
週三早班：安　　週三晚班：晴
班數：安2、柏1、晴2、明1。</pre><p class="body-text">再只取消柏、晴、明的週三可排。週三剩安一人，卻有兩班需求；同日最多一班，因此最多五班、週三必留一個空缺。空缺要交由負責人調整條件，不能由工具偷偷放寬規則。</p><div class="core-table-scroll"><table><thead><tr><th scope="col">工具設計要回答</th><th scope="col">可重用的規格</th></tr></thead><tbody><tr><td>輸入</td><td>人員、日期、班種與需求人數都由使用者新增或修改</td></tr><tr><td>設定</td><td>可排勾選與每人總班數上限</td></tr><tr><td>處理</td><td>先驗證、按限制安排、盡量填滿再平均</td></tr><tr><td>輸出</td><td>班表、需求與缺額、每人班數、CSV、資料備份</td></tr><tr><td>例外</td><td>非法資料阻擋；缺人明示；改輸入後清除舊結果</td></tr></tbody></table></div><p class="body-text">把完成的資料／結構對照表保存。接著使用完整工具提示詞生成空白介面，再填入案例 A，換成不同人數與班種的案例 B。原活動預算案例留在<a href="../part2/BUDGET-1.html">預算補充教材</a>，不需要先完成預算才能繼續。</p></section>

<section class="lesson-section" id="ch3-section-4"><h2 class="section-heading">先描述工具的輸入、設定與功能</h2><p class="body-text">剛才已把案例中的名字、日期與班次抽成欄位，也手排一份可行班表。現在用下方完整提示詞生成空白工具，再由你把資料填到介面；工具依當次資料處理，不把手排答案當成程式的一部分。</p><p class="body-text">閱讀提示詞時，逐句找出使用者能輸入的項目、能設定的規則、工具的處理與輸出。比如「提供人員清單，可新增、刪除與修改姓名」要求一種能力；實際有哪些人留到操作工具時輸入。這樣學員往後可以沿用結構，替換欄位與規則設計自己的工具。</p><div class="core-table-scroll"><table><thead><tr><th scope="col">設計面向</th><th scope="col">使用者應能做的事</th></tr></thead><tbody><tr><td>輸入</td><td>編輯人員、日期、班種、時段與需求人數</td></tr><tr><td>設定</td><td>勾選可排日、設定總班數上限</td></tr><tr><td>處理</td><td>驗證資料、按限制排班、清除失效舊結果</td></tr><tr><td>輸出與例外</td><td>核對班表和缺額、備份還原、匯出與錯誤提示</td></tr></tbody></table></div><p class="body-text"><a download="" href="../assets/materials/prompt-schedule.txt">完整工具結構提示詞 TXT</a>與下方內容相同。先複製整段生成工具；<a download="" href="../assets/materials/schedule-practice.txt">兩組操作練習 TXT</a>留到下一節填入工具，不需貼進生成提示詞。也可下載<a download="" href="../assets/materials/tool-structure-worksheet.md">工具結構工作表</a>，練習把其他工作拆成相同設計面向。</p><div class="prompt-wrap"><div class="prompt-header"><div class="prompt-label">可重用排班工具的完整提示詞</div></div><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-schedule">請製作一個繁體中文的排班規劃工具，讓使用者在網頁上輸入資料、設定規則、產生班表、檢查空缺並保存成果。工具處理使用者當次輸入的內容，初次開啟顯示空白表單，不預填任何人名、日期、班種或排班答案。

使用者能輸入什麼：
提供人員清單，可新增、刪除與修改姓名。
提供日期清單，可新增、刪除與修改日期或日期標籤；順序由使用者設定。
提供班種清單，可新增、刪除與修改班種名稱、開始及結束時間，以及每班需要的人數。
讓使用者勾選每位人員在哪些日期可以值班。可排代表該日各班種都能安排，但仍要遵守下面的規則。
人員、日期或班種改動後，可排表與班表欄位要同步更新，保留仍適用的資料，新增的可排日期先不勾選。

哪些規則能設定：
提供每人總班數上限，可由使用者設定零至目前日期數的整數，因為同一天最多一班；零表示本次所有人都不能排班。
同一人同一天最多安排一班，只能安排在勾選可排的日期，每班安排人數不得超過該班的需求人數。
先遵守以上規則並安排盡量多的班，再在安排人數相同的情況下，讓大家總班數盡量接近。請在畫面說明這個先後順序。
適用範圍限小型排班：一至八位人員、一至七個日期、一至四種班種，每班需要一至四人。超出範圍時明確提示並阻止計算，不省略人員、不截斷資料。

工具如何處理與呈現：
先檢查輸入，再依當次資料與設定排班。姓名或日期重複、必填欄位沒填、班種名稱重複、結束時間不晚於開始時間、人數或上限不正確時，指出問題並保留欄位供修正。
不能只試一次順序就說沒有可行安排。請在上述支援規模內找出最多可安排人次的班表，再依平均分配偏好選擇結果。不能為了排滿而違反限制。
結果列出日期、班種、時段、需要人數、已安排人員、缺額、每人總班數與已排／未排統計。缺人時保留空缺，說明受哪些限制影響，交由使用者調整條件。
任何輸入、設定或還原資料改變後，清除舊結果、停用班表下載與列印，提示重新產生。

資料與成果如何帶走：
提供「清空資料」「產生班表」「下載資料備份」「還原資料」「下載班表CSV」及列印。
清空資料前請使用者確認；下載備份要保存人員、日期、班種、可排條件與規則設定，副檔名用.json，格式由工具處理。還原時先檢查整份資料；失敗保留原輸入並說明原因，成功後先核對欄位，再由使用者重新產生班表。
CSV和列印包含班表、需求與缺額；中文與含逗號的文字要正確，輸入文字不得變成試算表公式。資料不自動保存，關閉或重新整理後回空白表單，畫面要提醒先下載備份。

交付與操作要求：
交付完整單一HTML檔，外觀與功能都在同一檔案；存檔後離線用瀏覽器開啟即可操作，使用時不再呼叫模型，不需要連線、金鑰或其他套件。
欄位、按鈕及錯誤提示要清楚，鍵盤能操作，手機也能閱讀；過寬表格只在自己的區域捲動。
請只回覆從&lt;!DOCTYPE html&gt;到&lt;/html&gt;的完整內容，不省略，不附其他說明。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-schedule" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-schedule-policy-status" role="status"></span></div></div></section>

<section class="lesson-section" id="ch3-section-5"><h2 class="section-heading">生成空白工具，再在畫面填入練習A</h2><p class="body-text">沿用第一章的 Gemini 網頁版，貼完整工具提示詞取得程式，再按第一章方式存成 HTML。帳號無法生成時先記錄平台問題；參考工具可供操作與規則核對，自己的生成成果仍須另測。</p><ol class="body-text"><li>開啟第一章使用的 <a href="https://gemini.google.com/" rel="noopener" target="_blank">Gemini 網頁版</a>，在新對話貼上完整排班工具提示詞，取得完整 HTML。存檔方式見<a href="CH1.html#save-open">第一章存檔步驟</a>；登入或生成暫時不可用時，記錄訊息並用作者參考品練操作。</li><li>雙擊開啟，先檢查空白表單是否有新增／刪除人員、日期、班種與需求，以及可排表和上限。輸入尚未完整時，產生應顯示缺漏，不應出現預先完成的班表。</li><li>按畫面按鈕建立下方練習A的人員、日期與班種。填每班需一人、上限2，依下表勾選可排日，再按「產生班表」。</li><li>逐格核對六班全滿、可排日皆成立、同日不同人、每人最多兩班；班數合計六，分布兩人兩班、兩人一班。保存CSV並按「下載資料備份」另存 schedule-A.json。</li></ol><p class="body-text">練習A：四人、週一至週三，每日早班09:00–13:00、晚班13:00–17:00，每班需一人，每人總上限2。</p><div class="core-table-scroll"><table><thead><tr><th scope="col">練習A人員</th><th scope="col">週一</th><th scope="col">週二</th><th scope="col">週三</th></tr></thead><tbody><tr><td>安</td><td>可排</td><td>不可排</td><td>可排</td></tr><tr><td>柏</td><td>可排</td><td>可排</td><td>不可排</td></tr><tr><td>晴</td><td>不可排</td><td>可排</td><td>可排</td></tr><tr><td>明</td><td>可排</td><td>可排</td><td>可排</td></tr></tbody></table></div><pre class="result-box">週一早班：安　　週一晚班：柏
週二早班：晴　　週二晚班：明
週三早班：安　　週三晚班：晴
班數：安2、柏1、晴2、明1。</pre><p class="body-text">卡關時可開<a href="../assets/tools/schedule-reference.html" rel="noopener" target="_blank">可編輯輸入的離線參考工具</a>或<a download="" href="../assets/tools/schedule-reference.html">下載參考HTML</a>比對。它是作者製作的示範，不是模型生成證據。測試表可用<a download="" href="../assets/materials/acceptance-template.csv">預期／實際紀錄CSV</a>；每列記資料、設定、預期、實際及版本。</p></section>

<section class="lesson-section" id="ch3-section-6"><h2 class="section-heading">改條件查例外，修復處理方式</h2><p class="body-text">先測原資料的單一變更：取消安週一可排。舊班表應消失，下載與列印停用；重新產生後仍六班全滿，安沒有週一值勤。先還原自己的 schedule-A.json，再取消柏、晴、明的週三可排；預期最多五班、週三一個空缺，並顯示受哪些限制影響。</p><p class="body-text">每組回到自己的A備份後再測：上限改1最多四班，改0全六班空缺；姓名空白或重複應阻擋並指出問題。還原<a download="" href="../assets/materials/roster-invalid.json">錯誤資料檔</a>時，無論因姓名或格式不符而被拒絕，都必須保留目前輸入。你只需選取檔案，不需讀寫檔案內容。</p><div class="core-table-scroll"><table><thead><tr><th scope="col">測試A的操作</th><th scope="col">核對結果</th></tr></thead><tbody><tr><td>取消安週一可排</td><td>仍六班；安不值週一</td></tr><tr><td>週三只剩安</td><td>最多五班、週三缺一班、有說明</td></tr><tr><td>上限1／0</td><td>最多四班／全部空缺</td></tr><tr><td>姓名空白／重複</td><td>阻擋並提示修正</td></tr><tr><td>任何資料更改</td><td>清除舊班表，重新產生前停用匯出</td></tr></tbody></table></div><p class="body-text">有錯時先保存失敗版本，再記「填了什麼、畫面出現什麼、按哪條規則應有什麼結果」。把下方三個括號替換成這份紀錄，再貼回原生成對話。模型要修正所有資料都會經過的處理方式，不能只把本次正確答案塞進程式。</p><div class="prompt-wrap"><div class="prompt-header"><div class="prompt-label">以測試紀錄修復工具的提示詞</div></div><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-schedule-repair">請修正目前的排班規劃工具。我會在下列三行補上測試紀錄：
我在工具填入的資料與規則：〔貼上當次的人員、日期、班種、可排條件與上限〕
畫面實際出現的結果：〔寫出可觀察的錯誤，例如安排在不可排日期、同一天重複人員，或改資料後仍顯示舊結果〕
依原有規則應得到的結果與理由：〔寫出預期及判斷理由〕

請找出造成這項錯誤的處理方式，讓所有符合支援範圍的輸入都能依同一套規則處理。不能把我這次的人名、日期或預期班表寫進程式當作答案。
保留新增、刪除與修改人員、日期、班種的功能，可排條件與上限仍由使用者輸入。仍需先遵守限制、盡量安排，再考慮工作量接近；無法排滿時保留缺額與原因。
保留資料備份、還原、CSV、列印與離線單檔功能。輸入改變要清除舊班表；還原失敗要保留原資料。
請交付完整修正版HTML，不只回覆差異片段。我會用原測試和另一組不同人員、日期、班種的資料重測。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-schedule-repair" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-schedule-repair-policy-status" role="status"></span></div></div><p class="body-text"><a download="" href="../assets/materials/prompt-schedule-repair.txt">修復提示詞TXT</a>供保存。另存修正版 schedule-v2.html，重新跑A各組測試，並繼續下一節的B測試；通過單一案例不足以驗收。</p></section>

<section class="lesson-section" id="ch3-section-7"><h2 class="section-heading">換人數與班種，驗證同一工具可以重用</h2><p class="body-text">現在保留A備份，清空資料；只操作同一份HTML的新增、刪除與修改功能，填入練習B。先在筆記預測需要幾個欄位、可排表如何變，以及最多能安排幾人次；完成後再核對下方示例。</p><p class="body-text">練習B：小芸、志宏、怡君、家豪、雅婷，共五人；日期為10/12、10/13。班種改成開場08:00–10:00、服務10:00–12:00、收尾12:00–14:00，每班需一人。所有人兩日皆可，每人總上限2，同日最多一班。</p><div class="core-table-scroll"><table><thead><tr><th scope="col">要檢查的變化</th><th scope="col">通過標準</th></tr></thead><tbody><tr><td>四人變五人</td><td>可新增第五位，可排表有五位，不能忽略最後一人</td></tr><tr><td>三日變兩日</td><td>舊日期移除，班表只列兩日</td></tr><tr><td>兩班種變三班種</td><td>可編輯三個名稱與時段，班表隨清單更新</td></tr><tr><td>同一份工具</td><td>更換資料即可重新安排，不需改提示詞或重新生成HTML</td></tr><tr><td>結果</td><td>六個需求全滿，一人兩班、四人各一班</td></tr></tbody></table></div><pre class="result-box">10/12：開場小芸、服務志宏、收尾怡君
10/13：開場家豪、服務雅婷、收尾小芸
六個需求全滿；一人兩班、四人各一班。</pre><p class="body-text">接著只把「收尾」每班需求改成兩人，其餘不變。總需求從六人次變八人次；兩天各需四位不同人，五人都可排、每人最多兩班，因此八人次能滿。班數三人兩班、兩人一班。核對輸出會顯示兩位收尾人員與正確需求，不能沿用每格只容納一人的結果。</p><p class="body-text">恢復B每班一人，下載 schedule-B.json 與班表CSV。關閉再重開應回空白；還原A應回四人三日兩班種，還原B應回五人兩日三班種，各需重新產生才有班表。保存A與B測試紀錄，下一章用它們驗證交付。</p></section>

<section class="lesson-section" id="finish"><h2 class="section-heading">帶著經查核的初版，處理下一個工作要求</h2>
<p class="body-text">A 與 B 改變了人數、日期與班種；同一份工具仍能依輸入產生結果，才表示它支援重用。請把核對紀錄寫成「資料與設定、實際結果、預期結果、通過或需修正」，保留未排滿的原因與處理方式。</p>
<p class="body-text">完成本章後，你有可用初版及兩組備份。下一章不重新做另一個工具，會在這份初版加入可調新規則，並查明原功能是否仍正常，讓你能管理工作需求的變更。</p></section>
<!-- learner-content:end -->
