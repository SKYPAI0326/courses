---
slug: gemini-ai
unit_id: SUPP-part3-CH3-3
title: 數據儀表板：實作互動式銷售漏斗
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<main class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">需要比較同一批資料在各階段留下多少人時，使用這頁。 準備下方曝光到購買的範例；各階段須採用一致的資料範圍。</p><ol class="step-list"><li>先確認各階段人數，跟著示例算相對上一階段的比例與流失數。</li><li>漏斗與表格的數值一致；缺值和異常要顯示，流失原因另行查證。</li></ol></section><section class="lesson-section" id="funnel-context">
<h2 class="section-heading">情境：哪一段銷售流程需要進一步查證</h2>
<p class="body-text">團隊想知道同一批訪客從曝光到購買的數量變化。漏斗可以顯示每一步留下多少人、相對上一階段的比例和流失數；它本身不能說明為什麼有人離開。</p>
<div class="prompt-wrap"><div class="prompt-label">同一期間的示例資料</div><pre class="result-box">曝光 10,000 → 商品頁 3,200 → 加入購物車 680 → 開始結帳 185 → 完成購買 42
期間：2026 年 9 月；來源：課程示例資料；各階段為同一批訪客</pre></div>
<p class="body-text">階段轉換率 = 下一階段人數 ÷ 目前階段人數。流失數 = 目前階段人數 − 下一階段人數。必須先確認口徑和觀察期間一致，否則各階段的比值不能直接比較。</p>
</section>
<section class="lesson-section" id="funnel-prompt">
<h2 class="section-heading">完整提示詞：把分母、缺值和資料異常說清楚</h2>
<p class="body-text">圖上應直接寫出每一個轉換率的分子與分母。零分母顯示「無法計算」，人數上升時先標示資料口徑異常，不產生負流失數或自行替數字找原因。</p>
<div class="prompt-wrap"><div class="prompt-label">銷售漏斗圖完整生成指令</div><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-policy-1">請製作繁體中文的單頁銷售漏斗儀表板，使用 SVG、內嵌 CSS 和原生 JavaScript，不使用外部套件、不呼叫 API。提供標題、來源、期間與資料口徑欄；階段清單包含名稱與同一批對象的人數，可新增、修改、刪除和調整順序，至少保留兩階段。空名稱、重複名稱、空白或非整數人數須提示。

每階段顯示人數、相對前階段轉換率、流失人數和計算所用分子／分母；整體轉換率顯示 最後階段人數／第一階段人數。輸入人數不得為負數。若前一階段為 0，轉換率顯示「無法計算」；若後階段高於前階段，標示資料或口徑需確認，不可顯示負流失數。所有數字顯示千分位與百分比，並可修改資料後重算。

顯示來源、期間和口徑提醒；不得由流失數推測原因。圖形須有可閱讀的文字標籤，手機版不截斷。輸出完整可開啟的單檔 HTML。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-policy-1"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-policy-1-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次漏斗資料：標題2026年9月銷售漏斗；來源課程示例資料；同一批訪客依序曝光10000、商品頁3200、加入購物車680、開始結帳185、完成購買42。整體轉換率42／10000。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside></div>
</section>
<section class="lesson-section" id="funnel-test">
<h2 class="section-heading">手算標準答案，再用異常資料檢查</h2>
<ol class="body-text">
<li>在 AI Studio Chat 生成檔案，保存為 sales-funnel.html，重新開啟後輸入示例數據。</li>
<li>核對階段轉換率：32%、21.25%、約 27.2%、約 22.7%；整體曝光到購買為 0.42%。最後一階段流失 143 人。</li>
<li>把商品頁人數改為 0，後續轉換率應顯示無法計算；再把加購人數改為 700，高於商品頁的 0，需標示資料口徑待確認，不可輸出負流失。</li>
<li>保存輸入、預期和實際結果；若公式不同，逐段修正分子或分母並重跑原始數據。</li>
</ol>
<div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">漏斗數字指出變化位置，不能證明原因。改善決策需另查訪談、事件定義或其他資料。</div></div>
<div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>交付可重開的圖表、四段轉換率與整體轉換率核對、零分母和數量上升測試，以及資料口徑限制說明。</div></div>
</section><section class="lesson-section" id="completion"><h2 class="section-heading">把漏斗差異轉成可說明的判斷</h2><p class="body-text">保留來源數值、各階段比率與你的判讀，並確認換數字後圖表重新計算。階段下降指出需要進一步查詢的位置，不能單憑圖形就確定原因；交付時一起說明指標定義與資料範圍。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「逐段計算轉換率，指出需查證段落」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E06/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E06/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E06/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>五段數量10000、3200、680、185、42。</td><td>相鄰轉換率32%、21.25%、約27.21%、約22.70%；首尾0.42%。</td></tr><tr><td>B</td><td>三段100、50、25。</td><td>相鄰50%、50%；首尾25%；階段數可變。</td></tr><tr><td>例外</td><td colspan="2">前段0時轉換率未定義；後段大於前段須提示口徑疑問，不能直接編原因。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e06-transfer-case">銷售流程漏斗｜當次案例資料（可替換）

A
五段數量10000、3200、680、185、42。

B
三段100、50、25。

例外
前段0時轉換率未定義；後段大於前段須提示口徑疑問，不能直接編原因。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e06-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e06-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></main>
<!-- learner-content:end -->
