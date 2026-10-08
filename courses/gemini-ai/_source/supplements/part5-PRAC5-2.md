---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-2
title: 會議行動句關鍵字初篩器
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">會議記錄很長，窗口想先找到可能提到責任或下一步的句子。本單元以關鍵字圈出「疑似行動句」，再由人判斷承諾、提議、取消與更新；它不是語意抽取器，不得把候選清單直接當正式交辦。</p><p class="body-text">關鍵字只比對字串，無法理解否定、提議、取消或後續更新。候選句一定要連同前後文顯示，再由人分類；初篩結果不能成為交辦紀錄。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">meeting-action-extractor.html</div>
</div>
<div class="tool-body">
<textarea id="meeting-text" placeholder="將會議記錄或逐字稿貼入此處……

範例：
請林週五前寄出場地圖。
我提議本次會議也可以直播。
原定邀請寄送已取消。
陳負責餐點詢價，期限未定。" style="width:100%;min-height:160px;padding:14px 16px;border:1px solid var(--c-border);border-radius:4px;font-family:inherit;font-size:.85rem;background:var(--c-bg);resize:vertical;line-height:1.7;"></textarea>
<button class="compose-btn" onclick="extractActions()" style="margin:12px 0;">標記疑似句 <span aria-hidden="true">→</span></button>
<div id="action-result" style="display:none;">
<div style="font-size:.73rem;color:var(--c-muted);letter-spacing:1px;font-weight:500;margin-bottom:10px;">關鍵字候選 · <span id="action-count">0</span> 個句子</div>
<div id="action-list" style="display:flex;flex-direction:column;gap:8px;"></div>
</div>
<div id="action-empty" style="display:none;font-size:.85rem;color:var(--c-muted);padding:16px 0;">目前詞表沒有命中候選句；這不代表沒有交辦。請回看原文或補充搜尋詞。</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">關鍵字只能找出可能相關的原文句子，不能判讀承諾、否定、提議、取消或後續更新。初篩結果必須讓人回看完整上下文並確認。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「會議行動句關鍵字初篩器」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
關鍵字只能找出可能相關的原文句子，不能判讀承諾、否定、提議、取消或後續更新。初篩結果必須讓人回看完整上下文並確認。

【操作與輸出】
貼入會議記錄後，以可查看／修改的詞表找出含詞句子，逐句保留來源原文和前後文；每句由使用者標記「有效待辦／非待辦／待確認」，另記原因，不自動填責任人或期限。

【例外與安全】
無輸入或空詞表要提示；同句多詞只顯示一次；否定、提議、取消和完成句仍只能標成候選。使用 textContent 或文字節點顯示原文，避免輸入變成 HTML。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
貼入「請林週五前寄出場地圖」「我提議本次會議也可以直播」「原定邀請寄送已取消」「陳負責餐點詢價，期限未定」四句，標出字串候選但不替人分類；學員須人工記錄待辦候選、提議、取消與未知期限。貼入 &lt;script&gt;alert(1)&lt;/script&gt; 只應顯示為文字。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>先讀四句測試逐字稿，圈出「可能有行動」的句子，再標明每句是候選、提議、取消或資訊未知；這是人工答案，不由關鍵字推論。</li><li>在參考品輸入同一批原句與詞表，查看候選是否保留來源文字及上下文；掃描器只做字串初篩。</li><li>複製完整提示詞到 AI Studio Chat 生成工具，保存為 action-screener-v1.html，重開後用同一資料重測，再逐句填人工分類與理由。</li><li>加入無命中句、空詞表及 &lt;script&gt;alert(1)&lt;/script&gt; 測安全與空狀態；若取消或提議被預先標成有效待辦，移除自動判斷並重新測試。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">候選句不會區分承諾、提議、否定、取消或更新；正式待辦需人工核對原文。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若取消句被標為有效任務，保留候選但修正文案提示，讓人工分類欄明確顯示取消，不自動確認。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>貼入「請林週五前寄出場地圖」「我提議本次會議也可以直播」「原定邀請寄送已取消」「陳負責餐點詢價，期限未定」。工具只標候選；學員須人工分類為待辦候選、提議、取消、期限未知，並引用原句。不把候選勾選視為確認，也不得補出期限。再貼入 &lt;script&gt;alert(1)&lt;/script&gt;，確認它只作文字顯示。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">把候選句交給人工判讀</h2><p class="body-text">保存候選句、上下文、分類與原文證據。關鍵字只協助尋找可能的行動句，提議、取消與有效交辦需再判斷；下一次換原文仍走這個核對流程，不能把命中直接當成已確認任務。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「先找含詞原句，再由人判讀承諾與否定」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E11/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E11/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E11/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>詞表=寄出、確認；原文「小禾會寄出資料。有人提議確認預算。不需要寄出舊版。這次先討論。」</td><td>前三句為候選、第四句不命中；第三句雖命中，不能自動当成待辦。</td></tr><tr><td>B</td><td>詞表=更新；原文「請更新名單。名單已更新。這次取消更新。」</td><td>三句皆候選；由人標有效/非待辦/待確認并写原因，不猜負責人/期限。</td></tr><tr><td>例外</td><td colspan="2">空詞表/空文提示；同句多詞只列一次；保留前後文。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e11-transfer-case">會議行動句關鍵字初篩｜當次案例資料（可替換）

A
詞表=寄出、確認；原文「小禾會寄出資料。有人提議確認預算。不需要寄出舊版。這次先討論。」

B
詞表=更新；原文「請更新名單。名單已更新。這次取消更新。」

例外
空詞表/空文提示；同句多詞只列一次；保留前後文。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e11-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e11-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>

<!-- learner-content:end -->
