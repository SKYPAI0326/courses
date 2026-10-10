---
slug: gemini-ai
unit_id: SUPP-part3-PRAC3-2
title: 專案時程甘特圖
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">需要讓團隊看清楚任務日期和重疊區間時，使用這頁。 準備下方任務範例；自己的日期與工期要先向負責人確認。</p><ol class="step-list"><li>先核對任務起訖日期，再照示範放到同一條時間軸。</li><li>圖上的每段工作區間與日期相符；修改日期後重新核對重疊。</li></ol></section><section class="lesson-section" id="example-start"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">專案窗口要向團隊說明已確認任務的日期、工期和重疊。本單元把每項任務放到共用時間軸，讓人比較工作區間；日期與工期須來自負責人確認的資料。</p><p class="body-text">甘特圖將開始日期和日曆日工期畫成時間區間。重疊只表示日期交疊，不能直接推論衝突；這個簡版不建模依賴、假日、人力或完成率，所以圖表只能協助溝通，不能代替排程確認。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">gantt-chart-generator.html</div>
</div>
<div class="tool-body">
<div class="gantt-header"><div>任務名稱</div><div>開始日期</div><div>天數</div><div></div></div>
<div class="gantt-rows-wrap" id="gantt-rows"></div>
<button class="gantt-add-btn" onclick="addGanttRow()">＋ 新增任務</button>
<button class="gantt-gen-btn" onclick="renderGantt()">生成甘特圖 <span aria-hidden="true">→</span></button>
<div class="gantt-chart-wrap" id="gantt-chart-wrap">
<svg id="gantt-svg"></svg>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">甘特圖按開始日期與日曆日工期畫出區間；它不會自動知道依賴、假日、資源衝突或實際完成度。沒有來源支持的依賴不能靠圖形推斷。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「專案時程甘特圖」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
甘特圖按開始日期與日曆日工期畫出區間；它不會自動知道依賴、假日、資源衝突或實際完成度。沒有來源支持的依賴不能靠圖形推斷。

【操作與輸出】
每列包含任務名稱、開始日期、正整數日曆日工期，可新增及刪除；生成 SVG 時依最早和最晚日期計算共同時間軸，列出任務名稱、日期與工期。

【日期計算】
工期以日曆日計算，開始日算作第 1 日；結束日期＝開始日期＋（工期－1）日。也就是工期 1 日時，結束日等於開始日；工期 2 日時，結束日在開始日之後 1 日。畫面、文字清單與 SVG 時間軸必須採用同一算法。

【例外與安全】
任務名稱不可空白；日期必須有效；工期須為 1 至 365 的整數。任務名以純文字顯示，空表或所有日期無效時不輸出假圖。明確標示時間軸以日曆日顯示，未建模相依關係。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
輸入需求確認（2026-10-01 開始、3 個日曆日）、資料整理（2026-10-03 開始、5 個日曆日）、主管審閱（2026-10-09 開始、2 個日曆日），核對時間軸、重疊、長度和最早／最晚日期。工期改 0、日期清空須提示；任務名輸入尖括號標記只作文字。刪除一列後確認時間軸重算。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>把三項固定任務及日期、日曆日工期填入參考品，記下每列的起訖範圍和整體最早／最晚日期。</li><li>貼上完整提示詞生成甘特圖，保存為 gantt-v1.html，關閉並重新開啟。</li><li>重建三項任務，核對時間軸、長度和標籤；將工期改為 0、清空日期、刪除一列，確認錯誤提示與時間軸更新。</li><li>在任務名稱貼入 &lt;script&gt;alert(1)&lt;/script&gt;，確認只顯示文字；若日期比例錯，核對日曆日算法後修正並重跑全部案例。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">先向專案負責人確認日期和日曆日工期；甘特圖顯示計畫區間，不代表人力已預留、任務依賴已確認或日期沒有衝突。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若時間軸長度或日期位置不符，先核對輸入日期和日曆日算法，再修正計算並重跑全部固定案例；不要拖動圖形掩蓋資料錯誤。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>加入三項工作：需求確認（2026-10-01，3 個日曆日）、資料整理（2026-10-03，5 個日曆日）、主管審閱（2026-10-09，2 個日曆日）。核對時間軸先後、長度比例和最早／最晚日期；工期改 0、日期清空時須提示，任務名輸入 &lt;script&gt;alert(1)&lt;/script&gt; 時只能顯示文字。刪一列後確認時間軸重算。本工具不推斷任務依賴或工作日。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">用時程圖核對工作順序與限制</h2><p class="body-text">保留任務、起訖日期與可開啟的時程圖，確認每個色條都對應實際輸入。改日期後重新查期限與重疊；圖表顯示時程位置，工作是否能按時完成仍需核對依賴與資源。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「用開始日與含起日的工期算結束日」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E08/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E08/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E08/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>準備2026-10-01工期3日、製作2026-10-03工期5日、核對2026-10-09工期2日。</td><td>結束日10/03、10/07、10/10；圖軸10/01至10/10；10/03前兩件重疊。</td></tr><tr><td>B</td><td>短任務2026-11-01工期1日；後續2026-11-02工期2日。</td><td>結束日11/01、11/03；開始日包含在工期內。</td></tr><tr><td>例外</td><td colspan="2">0日、負工期、錯誤日期需停止正常繪圖；修改工期後文字與圖同步。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e08-transfer-case">任務甘特時間軸｜當次案例資料（可替換）

A
準備2026-10-01工期3日、製作2026-10-03工期5日、核對2026-10-09工期2日。

B
短任務2026-11-01工期1日；後續2026-11-02工期2日。

例外
0日、負工期、錯誤日期需停止正常繪圖；修改工期後文字與圖同步。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e08-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e08-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>
<!-- learner-content:end -->
