---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-1
title: 活動異動通知草稿產生器
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">行政同事要回覆一封活動變更通知，需保留已核實的日期和地點，語氣禮貌但清楚。本單元生成郵件草稿；寄出前逐項核對事實、收件人和個資，模板不能自動授權寄送。</p><p class="body-text">範本只把已確認資料放進草稿；缺少的事實留成待補欄位。生成文字不是核准，也不應自動寄出。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">email-template-generator.html</div>
</div>
<div class="tool-body"><div class="email-input-grid">
<div><label for="ei-recipient">收件對象</label><input id="ei-recipient" oninput="renderEmail()" placeholder="例：已報名者" value="已報名者"/></div>
<div><label for="ei-event">活動名稱</label><input id="ei-event" oninput="renderEmail()" placeholder="請填活動名稱" value="年度交流活動"/></div>
<div><label for="ei-old-date">原日期</label><input id="ei-old-date" oninput="renderEmail()" placeholder="YYYY/MM/DD" value="2026/10/20"/></div>
<div><label for="ei-new-date">新日期</label><input id="ei-new-date" oninput="renderEmail()" placeholder="YYYY/MM/DD" value="2026/10/22"/></div>
<div><label for="ei-venue">地點</label><input id="ei-venue" oninput="renderEmail()" placeholder="只填已確認資訊" value="原場地不變"/></div>
</div>
<div style="margin:12px 0;"><label><input id="ei-policy-confirmed" onchange="renderEmail()" type="checkbox"/> 退款政策已由負責單位確認</label><input id="ei-policy" oninput="renderEmail()" placeholder="已確認時才填入政策原文" style="width:100%;margin-top:8px;"/></div>
<div style="font-size:.73rem;color:var(--c-muted);margin:14px 0 8px;display:flex;align-items:center;justify-content:space-between;"><span>郵件草稿預覽（不會寄出）</span><button class="copy-btn" onclick="copyEmail()">複製草稿</button></div>
<div id="email-preview" style="background:#2c2b28;color:#e8e4dc;font-family:'Courier New',monospace;font-size:.8rem;line-height:1.9;padding:20px 24px;border-radius:4px;white-space:pre-wrap;min-height:150px;border:1px solid rgba(107,127,163,.2);"></div></div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">下方指令包含工具用途、輸入、主要規則、輸出和介面要求。先讀一遍，圈出會影響結果的規則；生成後依第三節的固定案例測試，不用外觀或模型自述代替驗收。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位熟悉行政溝通、表單驗證和資料安全的前端工程師。請為活動承辦人製作「活動異動通知草稿產生器」，用於把已確認的日期異動整理成可人工覆核的郵件。交付一份可直接在瀏覽器開啟的單一 HTML；CSS 與 JavaScript 內嵌，不呼叫寄信服務、不連接 API、不自動寄送。

【輸入欄位】
頁面欄位包含收件對象、活動名稱、原日期、新日期、地點，以及退款政策是否已確認的核取方塊和政策文字欄。初次開啟欄位留空，政策確認先不勾選；所有資料由使用者輸入或另附可替換示例。

【生成規則】
- 輸入改變時更新郵件預覽，內容包括主旨、稱呼、已確認的日期異動、地點與結尾提醒。
- 未填欄位以明確的「待補」文字呈現，不可直接省略成看似已確認。
- 退款核取方塊未勾選時，一律顯示政策仍待確認，不能從文字欄推斷政策；勾選但政策內容空白時，也不得聲稱已確認。
- 預覽區有複製草稿按鈕和複製成功提示；複製操作不代表郵件已核准或寄出。

【資料與安全】
- 所有使用者輸入只以純文字顯示，不插入 HTML，不執行輸入內容。
- 不要求輸入真實收件者個資；用假資料示範。頁面不儲存或傳送欄位內容。
- 表單有可見標籤；用鍵盤能操作核取方塊和複製按鈕，窄螢幕欄位改為單欄排列。



介面使用繁體中文並說明這只是草稿工具。輸出完整 HTML 原始碼，不要省略表單、驗證、預覽、複製和安全處理。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次通知條件：活動原訂2026/10/20，改為2026/10/22；地點維持原場地；退款政策尚待財務確認。這些是測試資料，後續在表單修改。

測試資料與檢查方式：
保留預填案例時，草稿須呈現 10/20 改為 10/22、地點不變及退款政策待確認。把活動名稱清空，預覽須顯示待補提醒；未勾選政策確認時，即使政策欄有文字也不得把它放進已確認承諾。勾選並填入「依報名規則辦理」後，才可逐字呈現該政策。輸入 &lt;script&gt;alert(1)&lt;/script&gt; 時，預覽只顯示原文字，不執行。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>先讀清楚案例中已確認的日期與地點，並標出仍未知的退款政策；在參考品檢查 10/20、10/22、地點不變是否進入草稿。</li><li>複製完整提示詞到 AI Studio Chat 生成工具，存為 event-change-email-v1.html，重新開啟並用自己的非敏感假資料重做一次。</li><li>測試清空活動名稱、未勾選政策確認但填入政策文字、勾選並填入已核准政策三種情況；記錄預覽和預期是否一致，並測試複製。</li><li>若未確認政策仍出現在承諾文字，只修正政策判斷，再重跑三種狀況；保存通過版本與測試紀錄，人工核准後才自行寄出。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">使用假資料練習；收件人、日期、金額、附件和語氣由寄件人核對後才寄出。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若草稿編造地點或承諾，回到提示詞指定只使用輸入資料並將未知標待補，再檢查完整郵件。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>輸入一封活動改期假資料：日期從 10/20 改到 10/22、地點不變、收件人為報名者。核對草稿只改已確認的日期，未知退款政策標為待確認；最後再由人檢查稱呼、語氣、連結與個資，保存核准版而不自動寄出。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">讓通知草稿保留可確認的事實</h2><p class="body-text">交付前逐項核對日期、地點、對象與尚未確認的政策，留下人工核對狀態。下一次改期時更新輸入，再從草稿重查事實；工具協助起草，實際寄出仍由承辦人決定。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「把已確認欄位代入通知，保留未知」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E10/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E10/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E10/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>對象=示範參與者；活動=讀書聚會；原日2026-10-10、新日2026-10-17、地點=示範教室；退款政策未確認。</td><td>主旨/日期/地點來自欄位；退款顯示待確認，複製不等於寄出。</td></tr><tr><td>B</td><td>活動=工具交流；新日2026-11-04；勾政策確認並填「可於示範期限前提出取消申請」；其餘自行填入。</td><td>新名稱/日期和明確政策代入，未填欄位仍標待補。</td></tr><tr><td>例外</td><td colspan="2">勾選確認但政策空白不得宣稱確認；輸入HTML字串只顯示文字。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e10-transfer-case">活動異動通知草稿｜當次案例資料（可替換）

A
對象=示範參與者；活動=讀書聚會；原日2026-10-10、新日2026-10-17、地點=示範教室；退款政策未確認。

B
活動=工具交流；新日2026-11-04；勾政策確認並填「可於示範期限前提出取消申請」；其餘自行填入。

例外
勾選確認但政策空白不得宣稱確認；輸入HTML字串只顯示文字。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e10-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e10-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>

<!-- learner-content:end -->
