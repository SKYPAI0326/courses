---
slug: gemini-ai
unit_id: SUPP-part2-CH2-3
title: 讓預算工具更易讀，並保留計算功能
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<main class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">預算算對了，畫面卻不容易看懂時，使用這頁改造介面。 先完成<a href="BUDGET-2.html">預算工具製作</a>，保存能正確計算的原版 HTML。</p><ol class="step-list"><li>先填入原測試資料並記下四個金額，再閱讀下方畫面改造範例。</li><li>修改後金額仍與原版一致；標題、差異與餘額更容易找到，手機也能閱讀。</li></ol></section><section class="lesson-section" id="budget-ui-1">
<h2 class="section-heading">情境：數字正確，讀表的人卻找不到重點</h2>
<p class="body-text">沿用預算補充 BUDGET-2 已驗算的活動預算工具 activity-budget.html。承辦人要在會議中快速看出估算、實支、支出差異與核定餘額；如果欄位擠在一起，或只用紅綠色代表狀態，同事仍可能讀錯數字。</p>
<p class="body-text">本單元只改版面、層次和文字可讀性，不新增欄位、不改計算公式、不改 CSV 匯入／匯出和錯誤處理。這樣才能把「介面改得更清楚」和「功能被意外改壞」分開驗收。開始前若沒有自己的預算工具，先完成 <a href="BUDGET-2.html">活動預算實作</a>；參考品只能用來預演，不能當成自己已驗收的成品。</p>
</section>
<section class="lesson-section" id="budget-ui-2">
<h2 class="section-heading">記錄基準，再決定讀者要先看到什麼</h2><p class="body-text"><strong>先備份並打開原始碼：</strong>在檔案管理器找到已驗收的 <code>activity-budget.html</code>，先複製一份並命名為 <code>activity-budget-v1-backup.html</code>。建議用 VS Code 從「檔案 → 開啟檔案」選取原始碼；Windows 也可用記事本。Mac 若用 TextEdit，先到「TextEdit → 設定 → 開啟與儲存」，勾選「將 HTML 檔案以 HTML 程式碼顯示而非格式化文字」，再開啟檔案。看到 &lt;html&gt;、&lt;head&gt;、&lt;script&gt; 等標籤後按全選、複製；不要從瀏覽器畫面複製。稍後先貼入 AI Studio Chat，再貼本節指令。若開啟後仍看到網頁，改用「開啟檔案方式」選文字編輯器。</p>
<p class="body-text">打開 <a download="" href="../assets/materials/budget-normal.csv">標準活動資料</a>，在目前版本輸入核定預算 30,000 元。改版前記下四個答案：估算 26,000、實支 27,800、支出差異 +1,800、核定餘額 2,200。再打開 <a download="" href="../assets/materials/budget-invalid.csv">例外資料</a>，確認空值或負數會停止計算或匯出並提示。</p>
<p class="body-text">讀者的工作問題依序是「總額是否可用、哪裡超出估算、還剩多少額度、哪些資料待確認」。介面先呈現摘要，再保留每筆明細；狀態文字要搭配標籤，不可只靠顏色。手機檢查欄位是否可閱讀，列印檢查是否保留標題與數值。</p>
<div class="prompt-wrap"><div class="prompt-label">完整介面修訂指令｜需在 AI 能讀到原始碼的對話中使用</div><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-policy-1">請只修改目前活動預算工具的視覺呈現與資訊層次，保留所有既有欄位、欄位名稱、元素 id、事件處理、計算公式、CSV 匯入／匯出、驗證、錯誤提示和資料格式。不得刪除或改變任何功能，不新增計算規則。

讓承辦人先看懂四項結果：估算合計、實支合計、支出差異（實支−估算）、核定餘額（核定預算−實支）。摘要放在明細表之前；每項以清楚文字標籤和金額呈現。差異的正負方向與原有文字保持一致，超支狀態同時使用文字與色彩，不可只用紅綠色。

依另附的樣式條件調整背景、標題、主要按鈕與分隔區；未附時沿用目前樣式。色彩須維持文字可辨識；金額使用易掃讀且對齊的字體。所有輸入欄位保留可見標籤，不以 placeholder 取代標籤；錯誤訊息靠近欄位並使用文字說明。保持繁體中文、單一 HTML、無外部套件、離線可開啟。桌面表格清楚，手機寬度時欄位可換行或在明細區橫向捲動，文字與按鈕不得重疊。列印版保留報表標題、日期、結果和明細，隱藏操作按鈕。

先檢查原始程式碼並說明你會保留的功能，再輸出完整 HTML。若無法確認某個原功能，不要猜測或刪除，請先指出需要確認的部分。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-policy-1"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-policy-1-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次樣式：白色背景、深藍標題與主要按鈕、淺灰分隔區；金額用易掃讀且對齊的字體。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside></div>
</section>
<section class="lesson-section" id="budget-ui-3">
<h2 class="section-heading">改成新版本，再跑相同測試</h2>
<ol class="body-text">
<li>保留通過驗收的 activity-budget.html。確認生成對話能讀取現有程式碼；若新對話讀不到，先貼入完整原始碼或使用平台允許的檔案方式提供。</li>
<li>將上方指令貼到同一個能讀取工具程式碼的 AI Studio Chat 對話，要求輸出完整單檔 HTML。保存為 activity-budget-v2.html，不覆蓋舊版。</li>
<li>在 v2 載入同一份 CSV，核對四個結果仍是 26,000、27,800、+1,800、2,200；再測缺值／負數，必須提示且不可產生看似完整的總額。</li>
<li>縮窄瀏覽器視窗檢查手機版；用瀏覽器列印預覽檢查報表標題、金額與明細。將預期、實際、版本和問題寫入驗收表。</li>
<li>若功能改變，指出具體差異，例如「空值現在被算成 0」；要求恢復原計算及驗證，只保留視覺修改，再跑全部基準測試。未通過時以 v1 作可用版本。</li>
</ol>
<div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>交付 v2 與前後測試紀錄。四個基準數字、缺值行為與匯出仍正確；標籤清楚，手機可讀，列印資訊完整。外觀變化不能代替功能回歸測試。</div></div>
</section><section class="lesson-section" id="completion"><h2 class="section-heading">把可讀性與計算正確一起交付</h2><p class="body-text">新版需要讓讀者容易找到四個金額，也要維持相同資料的計算答案與例外處理。保留前後版及核對紀錄；之後再改配色或列印版面時，沿用這份基準，才能辨認外觀變更是否影響功能。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></main>
<!-- learner-content:end -->
