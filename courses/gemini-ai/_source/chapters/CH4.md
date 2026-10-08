---
slug: gemini-ai
unit_id: CH4
title: 追加需求、修正問題並確認結果
course_type: skill-operation
version: 2026-10-09-instructor-repair
duration: 65
dependencies: ["CH3"]
learning_objective: 追加需求、修正問題並確認結果
platform_version: Gemini web; official help checked 2026-10-08; account generation pending
---

# 追加需求、修正問題並確認結果

正式正文以下列learner-content範圍為唯一來源；HTML從此範圍轉製。內部設計依據：課程根目錄 _repair/2026-10-08/CHAPTER-REDESIGN.md。
環境：桌面瀏覽器、可登入的Gemini帳號、UTF-8純文字存檔。引用的作者參考品只能證明操作／規則，不代表授課平台生成。真人跟做及六小時試教待驗。
來源：part4/PRAC4-3.html；跨章交付段落另見遷移紀錄。

<!-- learner-content:start -->
<section class="lesson-section" id="ch4-section-1"><h2 class="section-heading">把新要求做成設定，讓別人也能選</h2><p class="body-text">第三章已完成能承接 A／B 資料的排班初版。現在負責人希望某類班次不要反覆落在同一個人身上，你要把新要求做成「指定班種的每人次數上限」，讓使用者自行選班種、設定上限與開關。新增功能後，原有可排條件、總上限與同日最多一班仍要成立。</p><p class="body-text">修改前先複製已通過 A／B 測試的 <code>schedule-v2.html</code> 與自己的 A／B 備份，將 v2 保留在「歷史版本」資料夾。新程式另存 <code>schedule-v3.html</code>；若修改失敗，就重新開啟 v2。每次修改都留新檔，才能回復上一個通過版本。先用筆記寫出新增的輸入、影響規則、輸出說明與例外，再看下方示例。</p><p class="body-text">先用 A 想清楚：若選早班、上限一，原例安有兩個早班就需改排。換到 B 則可以選收尾，工具也應支援使用者新加的班種；指定班種要取自當次清單，不能只認「早班」。</p><div class="core-table-scroll"><table><thead><tr><th scope="col">要新增的結構</th><th scope="col">應與既有結構連動</th></tr></thead><tbody><tr><td>是否啟用</td><td>開關改動清除舊結果，關閉回原規則</td></tr><tr><td>選擇班種</td><td>選項取自當次班種清單，修改後同步</td></tr><tr><td>每人次數上限</td><td>非負整數，按全部日期累計指定班種</td></tr><tr><td>輸出與保存</td><td>畫面、CSV、列印註明設定；備份還原保存設定</td></tr></tbody></table></div></section>
<section class="lesson-section" id="ch4-section-2"><h2 class="section-heading">生成可設定的新規則，保留原能力</h2><p class="body-text">把自己的工具修改提示詞貼回原對話，要求完整單檔，另存新版本。原可用版保留；下方供對照新設定、舊功能及例外有沒有漏。</p><div class="prompt-wrap"><div class="prompt-header"><div class="prompt-label">新增可設定班種限制的完整提示詞</div></div><p class="policy-guide">貼回原生成對話；新對話先附上已測過的 v2 完整程式。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-solo-schedule">請在目前通過測試的排班規劃工具中，加入一項可設定的規則：「每人在指定班種最多安排幾班」。
提供啟用開關，初次開啟為關閉。使用者啟用後，從目前班種清單選擇一個班種，再輸入非負整數的每人次數上限。零表示該班種不能安排人員。不要寫死任何班種名稱或上限。
以整段排班日期合計該班種的次數；關閉新規則時回到原本排班方式。人員可排日期、每人總班數上限、同日最多一班與每班需求仍必須遵守，仍先盡量安排，再讓總班數盡量接近。
新增、刪除或修改班種後更新選單；指定班種被刪除時清除舊選擇、提示重新指定，在設定完整前阻止排班。修改輸入、開關或上限後清除舊結果並停用匯出。
備份與還原一併保存是否啟用、指定班種及次數上限。讀取沒有新設定的舊版備份時，預設關閉這項新規則，保留原有資料。還原失敗仍保留目前輸入。
畫面、CSV與列印要寫明新規則是否啟用、指定班種與上限。保留其餘可編輯輸入、錯誤提示、備份還原及離線功能。
請回覆完整修正版HTML，不省略、不只回覆差異。我會用不同人數、日期與班種的資料，同時檢查新規則及原功能。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-solo-schedule" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-solo-schedule-policy-status" role="status"></span></div></div><p class="body-text"><a download="" href="../assets/materials/prompt-solo-schedule.txt">完整追加提示詞TXT</a>供保存。若只得到差異片段，先要求完整HTML再存；新增設定也要能在B的不同班種上使用。</p></section>
<section class="lesson-section" id="ch4-section-3"><h2 class="section-heading">用兩組資料驗證新增設定</h2><p class="body-text">先在自己的 <code>schedule-v3.html</code>還原第三章下載的 A／B 備份，確認欄位正確且新規則預設關閉。若使用<a href="../assets/tools/schedule-v2-reference.html" rel="noopener" target="_blank">作者修改版參考工具</a>，請依<a download="" href="../assets/materials/schedule-practice.txt">A／B 文字資料</a>重新填入，再用參考工具自己下載的備份測還原。作者檔名中的 v2 是參考品編號；它示範本章的新規則，和你自己的版本編號分開。兩種工具的備份格式可能不同，不能直接互用；自己的生成版須另測。</p><p class="body-text">作者參考品遇到超過搜尋上限的條件會停止並提示；先縮小資料再試，不能把未搜完的結果宣稱為最多可排人次。這是參考品限制，自己的生成工具也要確認它能正確處理的範圍。</p><p class="body-text">先在新版本還原A。啟用規則、選早班、上限1；仍可六班全滿，例如週一早安晚柏、週二早晴晚明、週三早明晚安。三個早班三位不同人，其他限制仍成立。這個答案只用來核對，不寫進追加提示詞或程式。</p><div class="core-table-scroll"><table><thead><tr><th scope="col">操作</th><th scope="col">驗收標準</th></tr></thead><tbody><tr><td>A：規則關閉</td><td>回原限制，六班與原功能成立</td></tr><tr><td>A：早班上限1</td><td>六班、三個早班三人、總班數2/2/1/1</td></tr><tr><td>A：週三只剩安</td><td>新規則開或關皆最多五班，週三一缺額</td></tr><tr><td>B：收尾上限1</td><td>仍六班，兩日收尾由不同人負責</td></tr><tr><td>B：收尾上限0</td><td>兩個收尾名額空缺，其餘四個需求可滿</td></tr><tr><td>刪除指定班種</td><td>選擇失效時提示重選，未完成前不排班</td></tr><tr><td>切換或改上限</td><td>清除舊結果，重產生前停用匯出</td></tr><tr><td>舊備份／新備份</td><td>舊檔讀取時新規則關閉；新檔恢復開關、指定班種與上限</td></tr></tbody></table></div><p class="body-text">B上限0的結果不能再顯示六班全滿；指定班種被改名後，選單與輸出也需同步，不能還出現舊名字。若功能只在A有效，回對話描述B的實際資料、設定及錯誤，要求修正通用處理，並重跑A與B。</p><p class="body-text">把每項新條件與原功能的觀察填入<a download="" href="../assets/materials/core-acceptance.csv">五章驗收表</a>，留下設定、實際結果與理由。上限零造成的缺額符合新規則，應與違反規則的排班分開判讀。</p></section>
<section class="lesson-section" id="repair"><h2 class="section-heading">用觀察到的差異要求修正</h2><p class="body-text">如果啟用新限制後結果不符，先分開記錄輸入、實際結果與預期結果。假如規則選早班、每人上限一，但同一人仍有兩個早班，就能指出缺少的是班種累計限制；只寫「排錯了」無法定位問題。案例記錄另外附加，修正方法保持可重用；記錄中也要交代新規則的開關、指定班種與上限。</p><details><summary>看一份完整錯誤紀錄：新增上限沒有生效</summary><p class="body-text">這是假設錯誤的教學示例。實際修復時另附自己觀察到的紀錄，讓模型取得資料、操作和理由。</p><div class="prompt-wrap"><div class="prompt-label">新增規則錯誤紀錄示例｜修復時才附加</div><pre class="case-data" data-policy-case="true" id="schedule-rule-error-record">輸入與設定：
A的人員：安、柏、晴、明；週一至週三；早班09:00–13:00、晚班13:00–17:00，每班1人。
可排：安週一、週三；柏週一、週二；晴週二、週三；明三天皆可。
總班數上限2、同日最多1班。新增限制：啟用；指定早班；每人該班種上限1。
操作：還原A，設定以上新限制，再按產生班表。

實際結果（教學假設）：
週一早安、晚柏；週二早晴、晚明；週三早安、晚晴。安有2個早班。

預期結果與理由：
同一人在整段日期最多1個早班；目前安超過上限，需重新安排。
六班可滿，例如週一早安晚柏、週二早晴晚明、週三早明晚安；總班數2/1/1/2。
這只是核對示例，可採其他符合全部規則的安排，不能把示例班表寫死。</pre><button class="copy-btn" data-policy-copy="schedule-rule-error-record" type="button">複製紀錄</button><span aria-live="polite" id="schedule-rule-error-record-policy-status" role="status"></span></div><ol class="step-list"><li>打開修正版，還原 A，啟用早班上限1，再產生。預期六班全滿，每人的早班次數都不超過1，其他限制仍成立。</li><li>還原 B，指定收尾上限1，預期六班全滿且兩次收尾不同人；只把上限改0，應有兩個收尾缺額，其他四個需求可滿。</li><li>關閉新增限制，重查原 A／B；再下載新備份、關閉重開及還原，核對開關、班種與上限。逐項填觀察與狀態。</li></ol><p class="body-text">填寫示例：若實際看到「A六班滿，三人各1早班」，再核對可排日、同日一班與總上限都成立，這一列才可記通過；B、關閉和還原仍要另列，不能用A的結果代替。</p></details><div class="prompt-wrap"><div class="prompt-header"><div class="prompt-label">以測試紀錄修復工具的提示詞</div></div><p class="policy-guide">貼回原對話，另附自己的錯誤紀錄；三段中的設定也要填完整。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-schedule-repair">請修正目前排班工具。我會另外附上這三段測試紀錄：
輸入與設定：〔人員、日期、班種、需求、可排條件、總班數上限；新增限制是否啟用、指定班種及該班種每人上限〕
實際結果：〔我按了什麼，畫面或下載檔出現什麼錯誤〕
預期結果與理由：〔按哪條規則，應有哪些人次或缺額，哪些既有功能仍應保留〕

請找出造成錯誤的通用處理方式，不把這次人名、日期、班種或預期班表寫成特例。
新增限制啟用時，要按整段日期累計每人在指定班種的次數，遵守使用者設定的上限；零表示該班種不安排人。關閉時回原排班方式。
保留人員可排日、總班數上限、同日最多一班及每班需求；仍先盡量安排，再讓總班數盡量接近。指定班種從當前清單選取；刪除後提示重新指定，設定不完整時阻止排班。
保留可編輯輸入、備份還原、CSV、列印與離線功能。改資料或設定要清除舊結果。新備份保存新增設定；沒有新增設定的舊備份載入時關閉新限制。還原失敗保留目前資料。
交付完整修正版HTML。我會重測原錯誤，再用不同人數及班種測啟用、關閉、零上限、備份還原和原功能。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-schedule-repair" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-schedule-repair-policy-status" role="status"></span></div></div><p class="body-text">完整修正版仍存為 <code>schedule-v3.html</code>；若已有失敗的 v3，先將它另名移到歷史版本。重測 A／B 的關閉、啟用、上限零、錯誤設定及備份還原。未通過時，用已測過的 <code>schedule-v2.html</code>處理原規則；v2 沒有新增限制。<a download="" href="../assets/materials/prompt-schedule-rule-repair.txt">本章修復提示詞 TXT</a>可保存。</p></section>
<section class="lesson-section" id="transfer-budget-change"><h2 class="section-heading">選讀：同一修改方法如何用在預算工具</h2><details><summary>選讀：在預算工具加入可調的低餘額提醒</summary><p class="body-text">排班新增的是安排限制；預算新增的是結果提醒。兩者都要先保留原版，描述新設定與舊功能的關係，再測新功能和原功能。預算同事想在餘額偏低時先看提醒，你需讓每次活動自行設定門檻，不能把某次3000元的要求寫成工具固定值。</p><p class="body-text">先保存原預算工具為budget-v1.html，追加後另存budget-v2.html。可以先開<a href="../assets/tools/budget-warning-reference.html" target="_blank">作者修改版參考工具</a>試操作：首次資料空白，填核定30000，展開「貼上素材CSV匯入」，再貼入<a href="../assets/materials/budget-normal.csv">預算A素材</a>；兩版提示詞與素材可在<a href="../part2/BUDGET-2.html">預算案例</a>取得。</p><div class="prompt-wrap"><div class="prompt-label">預算工具追加提示詞｜門檻由使用者設定</div><p class="policy-guide">先提供原工具，再貼此修改方法；案例數字留在下方獨立測試。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-budget-warning">請在目前的活動預算工具加入「低餘額提醒」。

提供可開關的提醒設定，以及由使用者輸入的非負金額門檻，不預設正式制度或案例數字。關閉時沿用原有計算；啟用時核定預算減實支合計小於門檻才提醒，等於門檻不提醒。負餘額另顯示超支；兩條提醒都命中時全部列出。

新增設定時清楚顯示目前開關與門檻。所有合計、差異仍按原公式計算，修改門檻不能改動明細或總額。錯誤或缺值停止正常輸出，不能顯示上一筆正常結果。

把提醒設定一併保存到工具下載的備份；還原前驗證，無效備份保留目前資料。舊備份沒有提醒設定時，依相容方式載入並關閉新提醒，說明尚未設定門檻。CSV和列印注明新設定及提醒結果。

保留新增、編輯、刪除明細、CSV匯入匯出、備份還原及原有檢核。所有輸入與設定可在畫面修改，首次開啟空白；只交付完整修正版單一HTML，原生程式、離線可用，無外部套件或API。案例數值與核對答案另附，不能寫成固定輸出。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-budget-warning" type="button">複製追加提示詞</button><span aria-live="polite" class="policy-status" id="prompt-budget-warning-policy-status" role="status"></span></div><p class="body-text"><a download="" href="../assets/materials/prompt-budget-warning.txt">保存追加提示詞TXT</a></p><aside class="policy-case" data-policy-case="budget-warning-case"><h3>本次測試資料｜可替換</h3><pre id="budget-warning-case">A：核定30000，明細使用budget-normal.csv。啟用低餘額提醒，門檻3000。
B：保持相同明細，只把門檻改2200。
例外：核定改27000，門檻仍2200；再將門檻清空；最後測備份還原。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="budget-warning-case" type="button">複製本次條件</button><span aria-live="polite" class="policy-status" id="budget-warning-case-policy-status" role="status"></span></div></aside></div><ol class="step-list"><li>A的估算26000、實支27800、差異1800、餘額2200，因2200小於3000所以提醒；原合計都不能因啟用而改變。</li><li>B的餘額仍2200，等於門檻2200，所以不提醒。關閉新規則後，原合計和匯出仍成立。</li><li>核定改27000，餘額為-800；同時顯示超支與低餘額提醒。啟用時門檻空白，應停止正常結果，指明缺欄。</li><li>下載備份，清空後還原，核對明細、核定、開關、門檻與提醒。載入舊版備份時新規則關閉；錯誤檔不能覆蓋目前資料。</li><li>核對CSV與列印內容包含新設定。記錄失敗的輸入、實際、預期，修復後重跑A與B，最後依第五章交付。</li></ol><p class="body-text">這次增加的是可調提醒，沒有改變估算和實支公式。往後不管改排班、預算或資料整理，都用同樣方法交代「新增什麼、與哪些既有規則連動、換資料如何驗證」。</p></details></section><section class="lesson-section" id="finish"><h2 class="section-heading">完成修改版，準備讓下次也能使用</h2>
<p class="body-text">排班主線完成後，留下已測過的 <code>schedule-v3.html</code>、A／B 新設定紀錄，以及歷史版本中的 v1、v2。新增限制關閉時，班表仍須符合原規則。本頁的預算改造是選讀，用不同工具對照同一修改方法。</p>
<p class="body-text">工具功能已查核後，第五章會實際關閉與重開、還原 A／B 資料，並整理接手者能照做的使用說明。這一步確認成果能離開目前操作環境，繼續在下一次工作使用。</p></section>
<!-- learner-content:end -->
