---
slug: gemini-ai
unit_id: SUPP-part1-PRAC1-1
title: Prompt 黃金公式組合台
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">同事每次整理會議記錄都要重想角色、任務和輸出格式。本單元把這些決策整理成可複用的提示詞草稿；完成物是一段經實際測試的工作指令，組合器只協助起草，不會替你判斷需求是否完整。</p><p class="body-text">角色、任務、限制和輸出格式各自負責不同資訊。欄位填得完整只能減少模型猜測，不能證明輸出正確；要用固定假資料實際檢查。</p><p class="body-text"><strong>固定測試逐字稿（虛構）</strong><br/>主持人：下週四下午辦產品說明會，地點待確認。<br/>小林：先整理 10 頁簡報提綱。<br/>阿凱：預算等收到報價再決定。<br/>雯姊：會後通知業務與客服，通知時間尚未決定。</p><p class="body-text"><strong>核對答案：</strong>可以整理出下週四下午、簡報提綱由小林處理、預算待報價、會後通知業務與客服；地點、通知期限與精確日期都未提供，應標「待確認」，不可自行補寫。缺少會議當日日期時，不可把「下週四」換算成日曆日期。</p><p class="body-text">先操作下方參考品，觀察四個欄位如何組成指令；再把組合後的提示詞和上方固定逐字稿一起貼入 Gemini 實際試跑。參考品只協助組合，不替你判斷輸出正確性。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">prompt-formula-builder.html</div>
</div>
<div class="tool-body">
<div class="formula-grid">
<div class="formula-field">
<div class="field-label">① 角色（Role）</div>
<div class="field-sub">你要 AI 扮演什麼身分？</div>
<textarea class="field-textarea" id="f-role" placeholder="例：你是一位熟悉公文用語與行政流程的資深行政主管。"></textarea>
</div>
<div class="formula-field">
<div class="field-label">② 任務（Task）</div>
<div class="field-sub">你要 AI 做什麼事？</div>
<textarea class="field-textarea" id="f-task" placeholder="例：把以下散亂的會議記錄，整理成一份清晰的行動摘要。"></textarea>
</div>
<div class="formula-field">
<div class="field-label">③ 限制（Constraint）</div>
<div class="field-sub">有哪些邊界條件？</div>
<textarea class="field-textarea" id="f-constraint" placeholder="例：字數不超過 300 字，語氣正式但不生硬，避免使用技術術語。"></textarea>
</div>
<div class="formula-field">
<div class="field-label">④ 呈現（Format）</div>
<div class="field-sub">希望以什麼格式輸出？</div>
<textarea class="field-textarea" id="f-format" placeholder="例：用條列式呈現，每條開頭標明「負責人」與「截止日期」。"></textarea>
</div>
</div>
<button class="compose-btn" onclick="composePrompt()">組合成完整 Prompt <span aria-hidden="true">→</span></button>
<div class="result-wrap" id="result-wrap">
<div class="result-label">
<span>GENERATED PROMPT</span>
<button class="copy-btn" onclick="copyPrompt()">複製</button>
</div>
<div class="result-box" id="result-box"></div>
<div class="char-tip" id="char-tip"></div>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">角色說明回答角度；任務說清楚要處理什麼材料；限制排除不接受的內容；輸出格式說明結果要長什麼樣。少一欄會增加模型自行猜測的空間，四欄完整也不等於結果已正確。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「Prompt 黃金公式組合台」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
角色說明回答角度；任務說清楚要處理什麼材料；限制排除不接受的內容；輸出格式說明結果要長什麼樣。少一欄會增加模型自行猜測的空間，四欄完整也不等於結果已正確。

【操作與輸出】
提供角色、任務、限制、格式四個多行欄位。按組合後按原順序產生標記清楚的提示詞；空白欄位須顯示待補提醒，不能靜默省略；支援複製結果並回報成功或失敗。

【例外與安全】
欄位內容以純文字組合，不解讀成 HTML。空白時保留原輸入並指出是哪個欄位待補。剪貼簿不可用時，讓使用者仍可選取結果手動複製。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
組合「行政主管／會議紀錄整理／不得補造原文未載資料，300 字內／表格」四欄。把組成的指令和固定逐字稿一併貼入 Gemini。預期列出下週四下午、簡報提綱由小林整理、預算待報價及會後通知業務與客服；地點、通知期限與精確日期須標「待確認」，不可把「下週四」換算成日曆日期。清空限制欄再組合，應指出待補而保留其他欄位；另以尖括號測試確認內容只以文字顯示。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>使用上方固定逐字稿。在四欄分別填「行政主管」、整理會議內容與行動、不得補造原文未載資料且 300 字內、表格格式；將組合結果和逐字稿貼入同一個 Gemini 對話。</li><li>確認角色、任務、限制、格式四段依序保留；對照頁面答案，逐欄檢查模型是否把未知地點、日期或通知期限標成待確認，而沒有補造。</li><li>將字數限制改成 150 字再跑同一份原文，逐項比較輸出；清空限制欄再次組合，確認結果保留其他三欄，並在限制欄與提醒文字指出待補。</li><li>把含尖括號的測試文字貼入輸出欄，確認它只呈現為文字；若模型補造責任人或欄位遺失，修正對應提示詞規則並用原文重測。保存兩版指令、輸出和差異。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">不要貼入公司機密；組合後仍須核對任務、資料來源與輸出格式。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">結果漏欄位時，只補上缺少的輸入或輸出規則，再用同一份假資料重測。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>在組合器填入「行政主管」角色、「整理會議紀錄」任務、「不得補造責任人、300 字以內」限制和表格格式，核對四段順序並複製提示詞。用固定假逐字稿試跑，確認時間保留「下週四下午」且不換算精確日期；檢查輸出不臆造負責人且不超過 300 字。修改字數限制後比較差異。清空限制再組合時，結果仍列出角色、任務與格式，限制欄顯示待補，提醒文字點名限制；尖括號內容只顯示文字。交付兩版指令、同一份假資料與差異紀錄。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">保留經試跑的需求，下一次再換資料</h2><p class="body-text">組合器幫你整理四個部分，是否漏掉責任人、期限或限制，仍要用模型輸出核對。保留兩版指令與同一份測試資料；下次換會議時，更新案例附件，沿用已核對的處理要求。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「四個欄位如何組成可核對需求」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E01/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E01/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E01/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>角色=行政助理；任務=整理輸入清單；限制=保留未知資訊；格式=表格。</td><td>四段按角色、任務、限制、格式原順序保留，輸入不得被當成HTML。</td></tr><tr><td>B</td><td>角色=企劃；任務=摘要使用者文字；限制留空；格式=條列。</td><td>前三個已填值保留；限制欄明示待補，不能默默省略。</td></tr><tr><td>例外</td><td colspan="2">拒絕剪貼簿權限後仍可選取完整結果手動複製。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e01-transfer-case">提示詞黃金公式組合台｜當次案例資料（可替換）

A
角色=行政助理；任務=整理輸入清單；限制=保留未知資訊；格式=表格。

B
角色=企劃；任務=摘要使用者文字；限制留空；格式=條列。

例外
拒絕剪貼簿權限後仍可選取完整結果手動複製。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e01-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e01-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>

<!-- learner-content:end -->
