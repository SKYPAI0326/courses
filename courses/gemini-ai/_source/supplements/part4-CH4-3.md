---
slug: gemini-ai
unit_id: SUPP-part4-CH4-3
title: 限時縮小範圍：差旅費試算工具打樣
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<main class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">出差後需要核對可報金額及預付款差額時，使用這頁。 完成第三章後使用；先以頁內假資料與示例上限練習。</p><ol class="step-list"><li>先跟著範例手算交通、住宿、餐費與預付款，再生成試算工具。</li><li>工具結果與手算一致；正式送件前再核對公司適用制度。</li></ol></section><section class="lesson-section" id="expense-1">
<div class="section-eyebrow">(01)</div>
<h2 class="section-heading">工作情境：出差後要核對可報金額和預付款</h2>
<p class="body-text">同事出差結束後，要整理交通、住宿、餐費和公司預付金。手動計算容易把每日餐費上限漏掉，也容易把「可核銷總額」和「公司還要支付或員工要繳回」混為一談。本單元做一個供核對的差旅費試算原型；公司制度不同，正式送件前仍須以財務規定為準。</p>
<p class="body-text">這一站借用限時打樣的節奏，但時間只用來控制範圍，不保證 20 分鐘內生成出可用工具。先完成核心計算和兩組測試；若平台等待或修復超出時間，就把狀態記為待完成，保留測試時間，不把倒數結束當作通過。</p>
<div class="callout info"><div aria-hidden="true" class="callout-icon">範圍</div><div class="callout-body">本版只處理整數金額、出差天數、住宿晚數、每日餐費上限、交通費與預付款。不處理稅務、匯率、公司簽核或自動送出報銷單。</div></div>
</section>
<section class="lesson-section" id="expense-2">
<div class="section-eyebrow">(02)</div>
<h2 class="section-heading">先算答案，再把規則寫進提示詞</h2>
<p class="body-text">預設案例：出差 3 天、住宿 2 晚、交通來回 1,800 元、每晚住宿 2,500 元、每日實際餐費 500 元、每日餐費上限 400 元，公司預付 3,000 元。可核銷餐費是 400 × 3 = 1,200 元；超過上限的餐費是 100 × 3 = 300 元；可核銷總額是 1,800 + 2,500 × 2 + 1,200 = 8,000 元；扣除預付款後，公司尚應支付 5,000 元。</p>
<p class="body-text">先分清三個數：費用合計、超過上限而不列入核銷的金額、扣掉預付款後的結算額。結算額為正表示公司尚應支付；為負表示員工應繳回差額。提示詞應把這個正負方向寫明白。</p>
<div class="prompt-wrap"><div class="prompt-label">完整生成提示詞｜單檔工具，不連線 API</div><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-policy-1">請製作繁體中文的「差旅費核銷試算」單頁工具，輸出完整單一 HTML，CSS 與原生 JavaScript 內嵌，不用外部套件、不呼叫 AI/API。

輸入欄位：出差天數、住宿晚數、交通來回總額、每晚住宿金額、每日實際餐費、每日餐費核銷上限、公司預付款。所有金額以新台幣整數輸入；天數為正整數，住宿晚數為非負整數且不可大於出差天數；金額不得為負數。欄位空白或格式不合法時停止計算並指出要修正的欄位，不可當作 0。

計算規則：
1. 每日可核銷餐費 = min(每日實際餐費, 每日上限)。
2. 可核銷餐費合計 = 每日可核銷餐費 × 出差天數。
3. 超出上限金額 = max(每日實際餐費 − 每日上限, 0) × 出差天數。
4. 可核銷費用合計 = 交通來回總額 + 每晚住宿金額 × 住宿晚數 + 可核銷餐費合計。
5. 結算額 = 可核銷費用合計 − 公司預付款。正數顯示「公司尚應支付」，負數顯示「員工應繳回」，零顯示「已結清」。

另提供清空與重新計算功能；結果旁顯示上述公式和「示例規則，請依公司制度確認」。不可自動送出、核准或保存真實個資。

介面需有可見欄位標籤、繁體中文錯誤訊息、桌面和手機版面；只輸出從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整程式碼，不要以省略號取代。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-policy-1"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-policy-1-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

3 天、2 晚、交通 1800、每晚住宿 2500、每日餐費 500、每日上限 400、預付款 3000。畫面應顯示可核銷餐費 1200、超額餐費 300、可核銷費用合計 8000、公司尚應支付 5000。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside></div>
</section>
<section class="lesson-section" id="expense-3">
<div class="section-eyebrow">(03)</div>
<h2 class="section-heading">生成後保存，依標準值測試與修復</h2>
<ol class="body-text">
<li>在 AI Studio Chat／對話頁貼上完整提示詞。核對回覆從 &lt;!DOCTYPE html&gt; 開始並包含 &lt;/html&gt;，另存為 travel-expense.html，再以瀏覽器開啟。不可把尚未生成的內容記成已完成。</li>
<li>輸入預設案例，核對可核銷餐費 1,200、超額餐費 300、費用合計 8,000、公司尚應支付 5,000。</li>
<li>只把每日實際餐費改為 350 元。預期可核銷餐費 1,050、超額餐費 0、費用合計 7,850、公司尚應支付 4,850。回復 500 元後再測一次。</li>
<li>把交通費改成 -1、清空住宿晚數，再分別測試；兩種輸入都應停止計算並指出欄位錯誤。若仍顯示舊總額，要求工具清除或標記過期結果，修正後重跑正常與例外測試。</li>
<li>記錄版本、預期、實際和修復；保留舊版，將通過驗收的 HTML、提示詞和使用限制一起保存。限時結束仍未通過，就標為待修，不交給同事正式核銷。</li>
</ol>
<div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>兩組正常數值和兩種錯誤輸入都得到預期反應，版本能重新開啟，且頁面明示金額只依示例上限計算。完成速度、畫面樣式和生成成功提示都不替代結果核對。</div></div>
</section><section class="lesson-section" id="completion"><h2 class="section-heading">把縮小範圍的成果與未完成處寫清楚</h2><p class="body-text">時間有限時，先留下可操作、可核對的核心計算，並記錄尚未實作的要求。日後擴充先從已驗證版本開始；用實際輸入、結果與回復方式說明進度，不以倒數結束宣稱工具完成。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「先依可調口徑算可報額，再算預付款差」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E22/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E22/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E22/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>3日2夜；交通1800、每晚2500、每日餐費500、每日可報上限400、預付款3000。</td><td>餐費可報1200、餐費超額300；可報合計8000、尚可領5000。</td></tr><tr><td>B</td><td>2日1夜；交通1000、每晚2000、每日餐費250、上限300、預付款5000。</td><td>餐費可報500、超額0；合計3500、應繳回1500。</td></tr><tr><td>例外</td><td colspan="2">缺值/負值提示；天數夜數/單位清楚；此為虛構規則，不等同正式機關制度。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e22-transfer-case">出差費用與預付款試算｜當次案例資料（可替換）

A
3日2夜；交通1800、每晚2500、每日餐費500、每日可報上限400、預付款3000。

B
2日1夜；交通1000、每晚2000、每日餐費250、上限300、預付款5000。

例外
缺值/負值提示；天數夜數/單位清楚；此為虛構規則，不等同正式機關制度。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e22-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e22-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></main>
<!-- learner-content:end -->
