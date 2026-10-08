---
slug: gemini-ai
unit_id: SUPP-part1-PRAC1-2
title: 提示詞 A/B 結果比較台
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">你手上有兩版「活動會後摘要」提示詞，想知道改寫是否讓結果更可用。本單元用同一份假資料做前後比較；完成物是有固定判準、原文引證和兩份模型輸出的比較紀錄。</p><p class="body-text">提示詞是本次比較中唯一要改的條件。若模型、原文或設定也改了，就無法判斷差異是否來自提示詞。比較台不會呼叫模型或替你打分，只整理你根據原文做出的人工判讀。</p><p class="body-text">先讀共同假逐字稿，標出提議、最後決議、有效待辦、取消與未知，再操作下方比較台。把提示詞 A、B 分別送入同一模型，貼回結果並逐項引用證據。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">prompt-ab-evaluator.html</div>
</div>
<div class="tool-body"><div class="callout info" style="margin-bottom:16px;"><div aria-hidden="true" class="callout-icon">共同測試資料</div><div class="callout-body">活動檢討會假逐字稿：主持人先問日期要不要調整；小林提議改為 10/22，當時尚待場地回覆。主持人稍後確認最後決議為 10/22。王小明承諾週四下班前確認新場地。退款政策尚待財務確認。陳怡君原本負責 10/20 舊場地預約，該任務已取消。練習時 A、B 都使用這段原文。</div></div>
<div class="ab-grid">
<section class="score-card"><label for="prompt-a"><strong>提示詞 A：模糊版本</strong></label><textarea class="diag-textarea" data-policy-prompt="文字整理比較" id="prompt-a">整理這段活動檢討會議記錄，列出重點和待辦。</textarea><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-a" type="button">複製提示詞 A</button><span aria-live="polite" class="policy-status" id="prompt-a-policy-status" role="status"></span></div><label for="output-a">貼上用提示詞 A 得到的結果</label><textarea class="diag-textarea" id="output-a" placeholder="到 AI Studio 用提示詞 A 和共同逐字稿生成，再貼回結果。"></textarea></section>
<section class="score-card"><label for="prompt-b"><strong>提示詞 B：具體版本</strong></label><textarea class="diag-textarea" data-policy-prompt="文字整理比較" id="prompt-b">只根據原文整理最後決議和仍有效的待辦。區分提議、最後決議、取消和未知；責任人只採用明確承諾者，期限保留原文表述，不把相對日期換算成未提供的日曆日期。原文未確認的政策或資訊須標待確認。每項附支持判斷的原句，輸出「最後決議／有效待辦／已取消／待確認」四區。</textarea><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-b" type="button">複製提示詞 B</button><span aria-live="polite" class="policy-status" id="prompt-b-policy-status" role="status"></span></div><label for="output-b">貼上用提示詞 B 得到的結果</label><textarea class="diag-textarea" id="output-b" placeholder="回到同一個模型對話，用提示詞 B 和相同逐字稿生成，再貼回結果。"></textarea></section>
</div>
<div class="score-card" style="margin-top:14px;"><strong>逐項比對結果</strong><p class="score-hint">讀兩份輸出，按證據選狀態；這裡不會呼叫 AI，也不會替你判定哪份正確。</p><div id="comparison-criteria"></div><button class="diag-btn" onclick="compareResults()" type="button">整理比較紀錄 →</button><div aria-live="polite" class="suggest-list" id="comparison-summary"></div></div></div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">這份提示詞會生成一個人工 A/B 判讀表。它把判斷拆成四個可查證問題，要求貼入原始模型輸出與原文證據；介面不計算提示詞品質分數，也不宣稱比較具有統計效力。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box">你是熟悉可用性、資料安全與無障礙的前端工程師。請製作「提示詞 A/B 結果比較表」，讓行政人員用使用者提供的同一份測試逐字稿、同一個模型與相同設定，檢查改寫提示詞前後的輸出差異。請交付可直接在瀏覽器開啟的單一 HTML，所有 CSS 和 JavaScript 放在檔案內；不呼叫模型、不連網、不把評分包裝成客觀正確率。


【測試材料輸入】
提供共同原文的可編輯輸入區；A、B 共用同一份資料。另附案例只供本次測試，不把人物、日期、決議或答案寫入判讀規則。

【操作畫面】
- 並排呈現提示詞 A、提示詞 B，各有可編輯文字區；讓使用者分別輸入一段模糊提示詞和一段明確規則提示詞。
- 每個版本各有模型輸出貼上區。明確提醒使用者須在同一模型／設定下分別生成，再把真實輸出貼回；空白時不可假造結果。
- 建立四列人工判讀表，每列可分別為 A 與 B 選「通過／未通過／需確認」，並留一個證據摘要欄。檢查項目為：有否區分提議與最後決議、有否只保留有效待辦及正確責任人、有否把相對期限或原文未確認的資訊擅自補成事實、有否保留取消狀態並引用原文。
- 按「整理比較紀錄」後，先檢查兩份輸出與每一項判讀是否填妥；缺資料時逐項指出，不顯示分數或勝負。資料完整時，分別統計 A、B 的通過／未通過／需確認數量，並列出證據摘要。
- 設「清除本次比較」功能，清除兩份輸出、證據與選擇狀態，不改動提示詞；不將資料上傳或保存到瀏覽器外。

【判讀邊界】
工具只整理學員的人工判讀，不自動讀取或比較模型文字。不要把 A/B 結果稱為品質分數、準確率或因果證明；只有同模型、同資料、同設定並逐項對照原文，才能做有限度比較。所有事實、期限、責任人與取消狀態都要回到逐字稿確認。



【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次共同資料：
頁面說明本單元的假情境：活動日期先出現 10/22 提議，之後才有改為 10/22 的最後決議；王小明承諾週四下班前確認新場地；退款政策仍待財務確認；陳怡君原負責的 10/20 舊場地預約已取消。提供同一份完整逐字稿，讓使用者分別複製到兩個提示詞版本中測試。

測試資料與檢查方式：
把 A、B 的輸出分別貼入，四項判讀各選一個狀態並寫支持原文。少貼一份輸出時應要求補資料；某項未選時應提示該列；完成後只顯示各版本逐項狀態及證據。輸出惡意標記文字如 &lt;script&gt; 必須只作文字顯示，不得執行。清除後判讀欄歸空、提示詞仍保留。

介面使用繁體中文，欄位名稱清楚，表單有可見標籤、鍵盤可操作、窄螢幕可閱讀。輸出完整原始碼，不得省略互動、錯誤處理或驗收功能。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>讀共同假逐字稿；記下可確認的最後決議、有效待辦、責任人、原文期限及未知事項。</li><li>在同一個 AI Studio Chat 模型和相同設定下，先貼提示詞 A 與原文，再貼提示詞 B 與同一原文；逐份保存完整輸出，不要只抄結論。</li><li>把兩份輸出貼回參考比較台，四項判準各自選通過、未通過或需確認，並引用逐字稿或輸出作為證據。</li><li>若 B 仍把提議當決議或補出未知期限，只修改相關提示詞規則，再以相同模型、資料與設定重測 A/B；保留修改前後紀錄。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">比較台只整理人工判讀，不會自行分析輸出或計算品質分數；測試用假資料並保存兩版完整原始輸出。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若兩次輸出條件不同，先還原相同模型、相同資料和相同驗收項，再比較提示詞差異。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>用同一份假資料分別測試模糊版與具體版提示詞，逐項記錄「決議是否正確、待辦是否仍有效、未知是否保留、是否附原文證據」。不計總分；交付兩份原始輸出、比較紀錄和下一次要修改的一條提示詞規則。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">把比較結果寫成下一次的修改要求</h2><p class="body-text">比較紀錄應能指出哪一項判準改善，以及對應的原文與輸出。下一次只修改尚未通過的要求，再保持模型、資料與設定相同重測；用證據選版本，不靠表格看起來整齊。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></div>
<!-- learner-content:end -->
