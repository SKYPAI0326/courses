---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-9
title: 截止日期倒數與日曆進度
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">活動團隊需要知道距離固定截止日還有幾天，以及目前經過了多少比例。本單元以明確日期算倒數和進度；跨時區、當日邊界和已過期狀態都要測，倒數畫面不能替代風險溝通。</p><p class="body-text">倒數和進度都依使用者所在時區的日曆日期計算。比較基準日欄預設今天，也能指定固定日期重現測試；截止當天、已過期和起訖同日是不同狀態。若頁面跨午夜持續開啟，重新載入或更新比較基準日。進度比例只描述日期，不代表工作完成率。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">event-countdown.html</div>
</div>
<div class="tool-body">
<div class="countdown-setup">
<div class="cd-field" style="grid-column:1/-1;">
<div class="cd-label">活動名稱</div>
<input class="cd-input" id="cd-name" oninput="updateTitle()" placeholder="例：員工旅遊報名截止"/>
</div>
<div class="cd-field">
<div class="cd-label">開始日期（用於進度條）</div>
<input class="cd-input" id="cd-start" onchange="startCountdown()" type="date"/>
</div>
<div class="cd-field">
<div class="cd-label">目標日期</div>
<input class="cd-input" id="cd-end" onchange="startCountdown()" type="date"/>
</div>
<div class="cd-field">
<div class="cd-label">比較基準日（預設今天；可改作驗收）</div>
<input class="cd-input" id="cd-today" onchange="startCountdown()" type="date"/>
</div>
</div>
<div class="countdown-display">
<div class="cd-event-name" id="cd-title">輸入活動名稱與目標日期後開始倒數</div>
<div class="cd-numbers" id="cd-numbers">
<div class="cd-unit"><div class="cd-num" id="cd-d">—</div><div class="cd-lbl">剩餘日曆日</div></div>
</div>
<div id="cd-state" style="margin-top:10px;font-size:.8rem;color:var(--c-muted);">選擇開始日、目標日和比較基準日。</div>
<div class="cd-progress-wrap" id="cd-progress-wrap" style="display:none;">
<div class="cd-progress-label">
<span id="cd-start-lbl">開始</span>
<span id="cd-end-lbl">目標日</span>
</div>
<div class="cd-progress-track"><div class="cd-progress-fill" id="cd-fill" style="width:0%;"></div></div>
<div class="cd-pct" id="cd-pct">0% 已過</div>
</div>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">倒數描述比較基準日到截止日相差的日曆天數，進度描述該日位於起訖區間的位置；兩者都不代表任務完成率。全部日期按本地 YYYY-MM-DD 比較，不用時分秒。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「截止日期倒數與日曆進度」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
倒數描述比較基準日到截止日相差的日曆天數，進度描述該日位於起訖區間的位置；兩者都不代表任務完成率。全部日期按本地 YYYY-MM-DD 比較，不用時分秒。

【操作與輸出】
輸入活動名稱、開始日期、截止日期和比較基準日（預設本地今天，可手動調整）；依本地 YYYY-MM-DD 日曆日顯示剩餘日數、日期進度（0–100%）與尚未開始／進行中／截止當日／已逾期狀態。比較基準日可重現固定驗收案例。

【例外與安全】
日期缺漏或無效、截止早於開始時提示且不畫正常進度；起訖同日、開始前、截止當日和逾期分別處理。按本地日期欄位比較，不以時分秒計日或透過 UTC 字串改變日期。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
開始日 2026-10-01、截止日 2026-10-11、比較基準日 2026-10-06，應得剩餘 5 個日曆日和 50%。把比較基準日改為 2026-09-30、2026-10-11、2026-10-12，分別核對尚未開始、截止當日、逾期；截止早於開始時不畫出正常進度。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>設定開始日 2026-10-01、截止日 2026-10-11、比較基準日 2026-10-06；應顯示剩 5 個日曆日、進度 50%。</li><li>在參考品輸入三個日期並核對結果，再把比較基準日依序設為 2026-09-30、2026-10-11 和 2026-10-12，觀察尚未開始、截止當日和逾期文字；結果按日曆日計，不隨目前時分秒變動。</li><li>貼完整提示詞生成工具，保存為 deadline-calendar-v1.html，重開後用同一日期組合重測；再測起訖相同、截止早於開始和無效日期。</li><li>若截止早於開始，顯示錯誤且不繪製正常進度；若比例超過 100%，檢查日期序號與起訖同日處理。保存預期值、實際值和用途限制，不把倒數當工作完成率。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">日期和時區未設定清楚時不要公開倒數；倒數不是催辦、風險管理或績效指標。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若截止日顯示負天數或超過 100%，先固定時區並按日曆日計算，再重測截止前、當日與過期。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>開始日 2026-10-01、截止日 2026-10-11、比較基準日 2026-10-06，結果須為剩 5 個日曆日、50%。比較基準日改為 2026-09-30、2026-10-11、2026-10-12 時，狀態分別為尚未開始、截止當日、已逾期；截止早於開始或日期無效時提示，不顯示正常進度。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">用固定基準日重現日期結果</h2><p class="body-text">保留開始、截止與比較基準日，以及倒數、比例和例外狀態。下一次更換日期先重測截止當日與逾期；日期進度描述時間位置，不能當成工作完成率。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「區分日期經過比例與工作完成率」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E18/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E18/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E18/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>開始2026-10-01、截止2026-10-11、比較日2026-10-06。</td><td>餘5日、日曆進度50%、進行中。</td></tr><tr><td>B</td><td>比較日改2026-10-11及2026-10-12。</td><td>截止當日餘0進度100%；翌日已逾期、進度上限100%。</td></tr><tr><td>例外</td><td colspan="2">起訖同日與截止早於開始分別核對；不把日曆進度當任務完成率。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e18-transfer-case">截止日期與日曆進度｜當次案例資料（可替換）

A
開始2026-10-01、截止2026-10-11、比較日2026-10-06。

B
比較日改2026-10-11及2026-10-12。

例外
起訖同日與截止早於開始分別核對；不把日曆進度當任務完成率。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e18-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e18-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>

<!-- learner-content:end -->
