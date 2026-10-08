---
slug: gemini-ai
unit_id: SUPP-part3-CH3-2
title: 把採購規則畫成可檢查的流程圖
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<main class="lesson-body"><section class="lesson-section" id="flow-context">
<h2 class="section-heading">情境：採購申請常卡在退補件與責任交接</h2>
<p class="body-text">新採購申請要經過承辦人、主管、採購和財務。只有直線箭頭會漏掉「退回補件」與「不核准」兩種結果；圖上的每個節點和分支都必須來自實際規則。</p>
<div class="prompt-wrap"><div class="prompt-label">本次流程資料</div><pre class="result-box">提出需求（承辦人）→ 主管審核
主管同意 → 採購詢價 → 財務核准 → 下單
主管要求補件 → 承辦人補件 → 回到主管審核
主管不核准 → 結束（未核准）</pre></div>
<p class="body-text">流程圖用節點表示工作狀態，用箭頭表示允許的交接，用分支標出決策條件。它呈現流程規則，不會真的建立簽核、發通知或讀取專案目前狀態。</p>
</section>
<section class="lesson-section" id="flow-prompt">
<h2 class="section-heading">先寫節點、負責人和轉換條件</h2>
<p class="body-text">在提示詞中分清節點名稱、負責角色、進入下一步的條件和退回路徑。若沒有來源支持期限或負責人，標成待確認，不讓圖表自行補值。</p>
<div class="prompt-wrap"><div class="prompt-label">採購申請流程圖完整提示詞</div><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-policy-1">請製作繁體中文的採購申請流程圖單頁 HTML，使用 SVG 呈現，內嵌 CSS 和原生 JavaScript，不用外部套件、不呼叫 API。提供可編輯的節點與連線清單。每個節點包含唯一識別、名稱、負責角色和工作說明；每條連線包含起點、終點與轉換條件。可新增、修改和刪除節點／連線；未知節點、重複識別、空名稱或連線缺起訖時指出錯誤。依清單繪製流程，不預設採購部門、核准路徑或結束條件。

點擊節點可查看該節點的工作說明，鍵盤也能聚焦並開啟；圖上必須固定顯示完整節點名稱，並用文字標示不同結果，不能只靠顏色。依輸入清楚呈現分支、回圈和終點。未提供的工期、日期或人名不得自行新增。頁面需適合手機閱讀，輸出完整單一 HTML。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-policy-1"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-policy-1-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次流程節點與路徑：
1. 提出需求，負責角色：承辦人。
2. 主管審核；同意後到採購詢價，要求補件則回到承辦人補件，再回主管審核，不核准則到「結束：未核准」。
3. 採購詢價後交財務核准，財務核准後到下單。
4. 每條箭頭標示「同意、補件、不核准、核准」等轉換條件；節點顯示負責角色。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside></div>
</section>
<section class="lesson-section" id="flow-test">
<h2 class="section-heading">核對正常路徑、退件和未核准路徑</h2>
<ol class="body-text">
<li>在 AI Studio Chat 生成流程圖，保存為 procurement-flow.html，重新開啟確認圖表和互動可用。</li>
<li>沿正常路徑逐節核對：提出需求→主管審核→採購詢價→財務核准→下單；再檢查補件回圈會回到主管審核。</li>
<li>確認不核准分支有明確終點，所有節點都顯示負責角色。用鍵盤測試節點操作，手機視窗檢查文字和箭頭。</li>
<li>如果箭頭方向或條件錯誤，只修正相應流程規則，保存新版本並重新走三條路徑。</li>
</ol>
<div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">流程圖只是流程說明，不是可執行簽核系統；正式工作流程要由流程負責人確認節點、例外和權限。</div></div>
<div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>正常、補件和不核准三條路徑都能依來源規則走完，角色和條件標示正確，且未把未提供的日期或人名畫進圖中。</div></div>
</section><section class="lesson-section" id="completion"><h2 class="section-heading">讓每個分支都有可追到的結果</h2><p class="body-text">流程圖應讓使用者能從起點走到明確的處理結果。保留規則、分支案例與查核紀錄，下一次修改門檻時重跑各條路徑；顏色或連線再清楚，也不能代替分支條件與去向。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「用節點和帶條件的連線表示交接」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E05/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E05/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E05/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>節點N1收件/承辦/N2核對/覆核/N3補件/申請人/N4結案/承辦；連線N1→N2、N2→N3條件缺項、N3→N2條件補齊、N2→N4條件完整。</td><td>四節點、四連線，有缺項分支、补件回圈及結案終點；點節點看到角色/說明。</td></tr><tr><td>B</td><td>改為X1提出需求、X2確認內容、X3完成；X1→X2、X2→X3條件確認。</td><td>三節點兩連線，無舊N節點；鍵盤可開啟節點說明。</td></tr><tr><td>例外</td><td colspan="2">新增連線X3→不存在的X4時應報錯；重複識別碼不得繪成看似正常的圖。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e05-transfer-case">可編輯工作流程圖｜當次案例資料（可替換）

A
節點N1收件/承辦/N2核對/覆核/N3補件/申請人/N4結案/承辦；連線N1→N2、N2→N3條件缺項、N3→N2條件補齊、N2→N4條件完整。

B
改為X1提出需求、X2確認內容、X3完成；X1→X2、X2→X3條件確認。

例外
新增連線X3→不存在的X4時應報錯；重複識別碼不得繪成看似正常的圖。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e05-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e05-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></main>

<!-- learner-content:end -->
