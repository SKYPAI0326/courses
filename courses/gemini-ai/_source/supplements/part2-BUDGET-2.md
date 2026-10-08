---
slug: gemini-ai
unit_id: SUPP-part2-BUDGET-2
title: 預算補充：生成與查核工具
course_type: skill-operation
version: 2026-10-09-instructor-repair
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="core-1"><h2 class="section-heading">生成與載入標準資料</h2><p class="body-text">你已在<a href="BUDGET-1.html">預算金額與公式</a>手算出估算、實支、差異和餘額。現在用完整提示詞把同一套規則做成可輸入明細的工具，再換數量、測缺值與保存成果，確認計算方法真的被實作。尚未建立手算基準時，先完成前頁的四個答案。</p><p class="body-text"><strong>本頁只做一種工作判斷：</strong>用活動預算資料核對估算、實支、差異與餘額，產物是 activity-budget.html。報價也會用數量乘單價，但報價和核銷有不同欄位與責任；不要拿報價總額替代本課的實支答案。</p><p class="body-text"><a download="" href="../assets/materials/prompt-budget.txt">下載完整生成指令 TXT</a></p><p class="policy-guide">先生成可編輯的工具；本次預算明細另外提供。</p><pre class="result-box" data-policy-prompt="工具生成或修改" id="prompt-budget">請製作活動預算與核銷差異表，單一完整 HTML，CSS/JavaScript 全內嵌，不用外部套件、不呼叫 AI/API。
欄位：項目、數量（非負整數）、單價、實支總額、備註；可新增刪除明細。核定預算獨立輸入。空值、負數、非有限數值應阻止計算與匯出，不能默認零；金額最多兩位小數。所有費用已包含必要費用，不另外加稅。
逐項估算=數量×單價；估算合計加總逐項；實支合計加總實支總額；較估算差異=實支合計-估算合計；核定餘額=核定-實支合計，負餘額顯示超支。金額以分為單位計算避免小數累加誤差。
支援以 item,quantity,unit_price,actual,note 欄位貼上 CSV 匯入（中文與引號可用）；錯誤資料不覆蓋原資料。下載明細 CSV 與總額；列印／另存 PDF；本機保存；備份 JSON 並可還原，還原先驗證再覆蓋。手機表格在自己的容器內橫向滑動。
只輸出 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整內容，不省略。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-budget" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-budget-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-budget"><h3>本次練習資料，可替換</h3><p>這區只含輸入；可另附到提示詞，或在工具完成後填入。答案留在操作核對區。</p><pre id="prompt-budget-case">本次預算資料，可替換：
核定預算30000元。
講師：數量4、單價2500、實支10500，備註交通費。
場地：數量1、單價8000、實支8500，備註延長。
餐點：數量40、單價150、實支6500，備註配送。
印刷：數量40、單價50、實支2300，備註加印。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-budget-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-budget-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p><p>再換 B 的項目、金額與明細列數，核對工具仍依同一公式計算。</p></aside><h3 class="section-heading">讀一條規則，預測它會擋住什麼</h3><p class="body-text">提示詞中的「空值、負數與非有限數值應阻止計算和匯出，不能默認零」是在保護工作判斷：缺資料不是 0 元。先讀 <a download="" href="../assets/materials/budget-invalid.csv">缺值／負數例外資料</a>，預測匯入失敗後原明細會不會被覆蓋、匯出按鈕是否應可用，再實際操作並記錄結果。這項檢查同時驗證提示詞規則和工具行為。</p><p class="body-text">再把核定預算由 30,000 改成 27,000。資料沒有變，估算 26,000、實支 27,800、差異 1,800 應維持；餘額則為 -800，應顯示超支。這是資料條件的改變，不要同時改提示詞中的公式，否則無法判斷差異來自哪裡。</p><p class="body-text">沿用<a href="#budget-save">本頁存檔方法</a>，將這次完整HTML保存為 <strong>activity-budget.html</strong>。雙擊後應開成工具；看到程式文字時，回存檔步驟檢查純文字格式與 .html 副檔名。保留上一版，不用覆蓋原有計時器。</p><p class="body-text">打開自製工具，核定填 30,000。把 <a download="" href="../assets/materials/budget-normal.csv">標準資料</a> 以純文字打開，貼入 CSV 匯入區。核對 26,000／27,800／1,800／2,200 四個值；來源檔 actual 是逐項實支總額，不再乘數量。</p></section>
<section class="lesson-section" id="core-2"><h2 class="section-heading">同步修改：餐點改為 45 人</h2><p class="body-text">每個測試各新增一列驗收紀錄。操作前先填工具檔名／版本、資料條件、來源模式和預期答案；操作後再填觀察結果與結論，不覆寫原本的正常測試。</p><ol class="body-text"><li>先預判哪個值會改。只把餐點數量改 45，單價與實支暫時不動。</li><li>重新核對：估算、實支、差異與餘額。告訴同桌為什麼餘額沒有跟著改。</li><li>核定改 27,000，應顯示超支；改回 30,000。每個狀態分開記錄，修復後另新增一列再測。</li></ol><details><summary>完成預判後核對答案</summary><p class="body-text">餐點估算 6,750；總估算 26,750；實支仍 27,800；差異 1,050；餘額仍 2,200。核定 27,000 時餘額 -800。</p></details></section>
<section class="lesson-section" id="core-3"><h2 class="section-heading">例外與修復：未知不能當零</h2><p class="body-text">下載 <a download="" href="../assets/materials/budget-invalid.csv">缺值／負數資料</a>，先不要覆蓋已完成資料。匯入應拒絕並保留目前明細；或直接清空餐點數量，工具應停止總額與匯出。填回 45 後應恢復。</p><p class="body-text">若空值被當零，先另記當次操作、畫面結果及預期；用下方通用修復提示詞回原對話修改。保存 v2，重跑正常與空值測試。只修改提示而仍顯示舊總額不算修好。</p><pre class="prompt-box" data-policy-prompt="工具修復" id="prompt-budget-repair">請修正目前預算工具的輸入驗證：任何必填數值空白、負值或非有限數值時，指出欄位錯誤、停止計算與匯出，並清除舊總額；填回有效值後恢復正常功能。依另附的測試紀錄找出原因，不把當次項目名稱、金額或答案寫成特例。保留既有欄位、公式、匯入匯出與備份功能。交付完整單一HTML，讓我用原案例及另一組不同明細重測。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-budget-repair" type="button">複製通用修復提示詞</button><span aria-live="polite" class="policy-status" id="prompt-budget-repair-policy-status" role="status"></span></div><p class="body-text">當次案例紀錄（另附）：餐點數量留空，實際仍顯示總額；預期指出數量待補、清除總額並停用匯出。</p></section>
<section class="lesson-section" id="core-4"><h2 class="section-heading">交付並確認可再次更新</h2><ol class="body-text"><li>下載明細 CSV，用試算表打開，確認中文、逐項估算與總額。</li><li>選列印，目的地選「另存 PDF」，保存 activity-budget-report.pdf，開檔核對四個總額與備註。</li><li>下載 JSON 備份，關閉工具後重開；修改一個備註，重新輸出。若換電腦，以 JSON 還原並核對。</li><li>保存完整指令與驗收紀錄。若修復另存了 v2，先完成原測試再以 v2 作為交付版本；在 README 寫明實際檔名，把未通過的舊版移至「歷史版本」。工具資料只存在目前瀏覽器時，必須交付資料備份。</li></ol><p class="body-text">卡關時可用 <a href="../assets/tools/budget-reference.html" rel="noopener" target="_blank">參考預算工具</a> · <a download="" href="../assets/tools/budget-reference.html">下載 HTML 參考檔</a> 比對公式、匯入與輸出，記錄哪些步驟仍是待完成。</p></section><section class="lesson-section" id="budget-save"><h2 class="section-heading">補充案例的存檔方法</h2><p class="body-text">複製完整HTML本體，不含前後反引號。在純文字編輯器貼上：Mac文字編輯先選格式→製作純文字；Windows可用記事本。以UTF-8另存activity-budget.html，確認不是.html.txt。雙擊開啟應看到表單；看見原始碼時先核對副檔名、純文字格式與完整起訖，再回存檔重做。保留前一版，修復另存v2。</p></section><section class="lesson-section" id="completion"><h2 class="section-heading">讓下一次更新仍能追到金額來源</h2><p class="body-text">交付工具、原始明細、備份及報表後，使用者應能更新數量或實支並重新核對。報表上的差異要能回到明細說明原因；未確認費用仍保留待確認，不能為了交出總額而當作零。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「以金額算式核對預算餘額」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E02/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E02/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E02/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>核定30000；明細：講師4×2500實支10500、場地1×8000實支8500、餐點40×150實支6500、印刷40×50實支2300。</td><td>估算26000，實支27800，差異1800，餘額2200。</td></tr><tr><td>B</td><td>核定5000；材料2×1000實支2100、包裝3×200實支550。</td><td>估算2600，實支2650，差異50，餘額2350。</td></tr><tr><td>例外</td><td colspan="2">單價留空或輸入-1應停止計算；錯誤備份不能清空目前資料。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e02-transfer-case">活動預算與實支差異｜當次案例資料（可替換）

A
核定30000；明細：講師4×2500實支10500、場地1×8000實支8500、餐點40×150實支6500、印刷40×50實支2300。

B
核定5000；材料2×1000實支2100、包裝3×200實支550。

例外
單價留空或輸入-1應停止計算；錯誤備份不能清空目前資料。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e02-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e02-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>
<!-- learner-content:end -->
