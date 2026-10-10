---
slug: gemini-ai
unit_id: SUPP-part3-CH3-1
title: 選對呈現方式：靜態圖與互動 SVG
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<main class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">需要呈現季度變化，同時讓讀者查到精確數值時，使用這頁。 完成第三章後使用；下方提供虛構營收資料。</p><ol class="step-list"><li>先閱讀同一組資料的圖表範例，核對季度與數值，再選擇靜態或互動呈現。</li><li>圖表、提示與資料表的數值一致；換資料後仍能核對每季數字。</li></ol></section><section class="lesson-section" id="svg-context">
<h2 class="section-heading">情境：主管需要看季度變化，也要查到單季數字</h2>
<p class="body-text">簡報中的靜態圖適合快速比較；如果讀者還需要查看每季精確數值或來源，互動提示才有用途。本單元用同一組虛構營收資料比較兩種呈現，不把動畫或滑鼠效果當成分析成果。</p>
<div class="prompt-wrap"><div class="prompt-label">固定測試資料</div><pre class="result-box">期間：2026 年第 1 至第 4 季
營收（百萬元）：Q1 12、Q2 18、Q3 15、Q4 22
來源：課程示例資料</pre></div>
<p class="body-text">SVG 是可縮放的向量圖形標記，可以為圖形加上標籤和互動；JPG 截圖只保存像素畫面。若報告只需要快速掃讀，靜態圖較簡單；若讀者要逐季讀取細節或鍵盤操作，再考慮互動 SVG。</p>
</section>
<section class="lesson-section" id="svg-prompt">
<h2 class="section-heading">把圖表問題、數值和可讀性一起寫進提示詞</h2>
<p class="body-text">圖表至少要說明標題、期間、單位、資料來源和零基線。互動資訊不能只藏在滑鼠懸停：重點數值要留在圖面上，操作提示需支援鍵盤，並提供文字摘要。</p>
<div class="prompt-wrap"><div class="prompt-label">季度營收圖完整提示詞</div><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-policy-1">請製作繁體中文的單頁季度營收長條圖，使用內嵌 SVG、CSS 和原生 JavaScript，不呼叫 API、不使用外部套件。提供標題、單位、來源及期間欄；資料列有分類名稱與非負有限數值，可新增、修改和刪除，依使用者輸入順序繪圖。空名稱、重複名稱、空白或無效數值須提示並停止繪圖。

縱軸從 0 開始，標出單位與刻度；每個長條下方顯示當列分類名稱，上方固定顯示數值。長條可用滑鼠或鍵盤聚焦查看同一數值的說明，但不得只靠 hover 才看得到資料。提供圖表文字摘要，依輸入資料計算最高與最低，並列出同值項；不得由數值推論營收變化原因。

版面需適合手機寬度、文字對比清楚、顏色不作唯一區分依據。輸出完整可在瀏覽器直接開啟的單一 HTML，不要只給 SVG 片段或文字說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-policy-1"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-policy-1-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次圖表資料：標題2026年季度營收；單位百萬元；來源課程示例資料；Q1=12、Q2=18、Q3=15、Q4=22。最高Q4、最低Q1。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside></div>
</section>
<section class="lesson-section" id="svg-test">
<h2 class="section-heading">生成、讀圖，再判斷是否需要互動</h2>
<ol class="body-text">
<li>把完整提示詞貼入 AI Studio Chat，確認拿到完整 HTML，另存為 quarterly-revenue.html 後以瀏覽器開啟。</li>
<li>依次核對 Q1 到 Q4 的標籤與 12、18、15、22；縱軸單位是百萬元且從 0 開始，圖表來源標示為示例資料。</li>
<li>用鍵盤 Tab 移到各長條，確認精確數值不只靠滑鼠顯示；縮窄視窗檢查標籤仍看得清。若圖形排序錯誤，記下輸入和實際結果，修復後重跑四季測試。</li>
<li>最後寫一句選圖理由：若讀者只需比較高低，使用靜態圖即可；若需查值，才保留互動細節。</li>
</ol>
<div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">互動圖表不會自動驗證原始營收資料或說明原因。把圖表交付前仍要核對期間、單位、來源和數值。</div></div>
<div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>交付可重開的 HTML、四筆數字核對紀錄、鍵盤與手機檢查結果，以及使用互動或靜態圖的理由。</div></div>
</section><section class="lesson-section" id="completion"><h2 class="section-heading">依讀者的操作選擇呈現方式</h2><p class="body-text">你應能說明這次需要固定圖像，還是需要縮放、點選與顯示數值的互動圖。保留這個選擇與可開啟的示例；圖像形式取決於讀者要完成的判斷，後續修改時仍需核對資料與標籤。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「把類別數值轉成可追查圖表」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E04/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E04/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E04/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>單位=件；Q1=12、Q2=18、Q3=15、Q4=22。</td><td>最高Q4=22、最低Q1=12；圖與明細值一致，零基準清楚。</td></tr><tr><td>B</td><td>單位=人；甲=5、乙=5、丙=0。</td><td>甲乙並列最高，丙為0；標籤和單位替換，不保留Q1到Q4固定欄。</td></tr><tr><td>例外</td><td colspan="2">負值依提示詞範圍提示；缺值不得默認為0；長標籤可讀。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e04-transfer-case">可編輯 SVG 長條圖｜當次案例資料（可替換）

A
單位=件；Q1=12、Q2=18、Q3=15、Q4=22。

B
單位=人；甲=5、乙=5、丙=0。

例外
負值依提示詞範圍提示；缺值不得默認為0；長標籤可讀。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e04-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e04-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></main>
<!-- learner-content:end -->
