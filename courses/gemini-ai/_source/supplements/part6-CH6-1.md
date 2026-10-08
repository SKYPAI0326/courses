---
slug: gemini-ai
unit_id: SUPP-part6-CH6-1
title: 會議交辦：先分辨決議與提議
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<main class="lesson-body"><section class="lesson-section" id="core-1"><h2 class="section-heading">用原文建立欄位答案</h2><p class="body-text">會議常同時出現提議、承諾、取消與後續更新。若把每句「要做」都當作有效任務，會交辦已取消的事項，或補出不存在的期限。本頁先根據原文建立判讀答案，下一份補充教材再拿這份基準核對模型輸出。</p><p class="body-text">下載 <a download="" href="../assets/materials/meeting-a.txt">完整逐字稿 A</a>，先圈出確定要做的事項。林承諾確認場地；陳承諾餐點詢價但未定期限；直播只是提議；邀請寄送已取消。最後兩者都不應成為有效待辦。</p><p class="body-text">有效交辦的欄位是任務、責任人、期限、狀態、來源原文、待確認原因與人工確認。未出現的期限應保留未知，不能因「明天」出現在取消句中就補給其他任務。</p><details><summary>完成預判後核對答案</summary><p class="body-text">兩項有效交辦：林／確認場地／2026-10-09；陳／餐點詢價／期限待確認。未人工核對前，confirmed 都是 false。</p></details></section>
<section class="lesson-section" id="core-2"><h2 class="section-heading">這次轉入 Build</h2><p class="body-text">前段 Chat 生成的單檔工具，執行時只跑固定規則；這次要把逐字稿送入模型整理。在 AI Studio 找到 <a href="https://aistudio.google.com/apps" rel="noopener" target="_blank">Build</a>，建立網頁應用，貼「生成並驗證 AI 會議交辦表」補充頁的完整生成描述；待程式生成後，在預覽內的逐字稿欄貼 A。描述框與應用輸入框是兩個不同位置。預覽和 A 測試完成後，記下畫面上的專案標題與瀏覽器網址，將目前專案網址加入書籤並用標題命名；這個書籤用來稍後回到同一專案，不是公開分享網址。</p><p class="body-text">此補充案例示範 Build 預覽與結果保存，不需要公開網址。不把下載的專案 ZIP 當成可雙擊 HTML。依 <a href="https://ai.google.dev/gemini-api/docs/aistudio-build-mode" rel="noopener" target="_blank">官方 Build 說明</a>，生成後會顯示程式與即時預覽，Gemini API key 以伺服器端 secret 使用；不要把金鑰貼到瀏覽器或逐字稿欄。平台額度與帳號限制依當時畫面確認，不能保證全部免費。</p><p class="body-text">為什麼不只用關鍵字？「直播」可能出現在提議、取消或已確認的句子裡；工具必須讀懂否定、時間順序和最後決定，才知道該列入什麼。固定規則工具適合公式和明確條件；遇到語意判斷才使用模型，但模型會誤讀，所以每筆結果仍要附原句並由人確認。</p><div class="prompt-wrap"><div class="prompt-label">會議生成補充頁的 Build 描述的核心規則｜先辨認，不急著發布</div><pre class="prompt-box" data-reference-spec="true" id="prompt-policy-1">讀取使用者貼上的會議逐字稿，只整理最後明確成立且尚未完成的交辦。每筆列出任務、責任人、期限、原文和待確認原因。提議、取消、已完成的事項分開說明；原文未提供的責任人或日期保持未知，不得推測。結果先標示未確認，讓使用者核對後再匯出。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1" type="button">複製規則摘要</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-policy-status" role="status"></span></div></div><p class="body-text">這是本課的系統規格摘要，不代表模型已正確執行。會議生成補充頁提供完整可複製的 Build 指令和兩份有標準答案的逐字稿，實際檢查模型輸出。</p></section>
<section class="lesson-section" id="core-3"><h2 class="section-heading">先確認工作結果，再處理發布</h2><p class="body-text">AI 輸出是草稿。人工核對來源、期限與最後決議後，才可勾選確認。若原文沒有資料，詢問會議主持人，或標待確認；不讓工具自動寄信或寫入日曆。會議生成補充頁會用 B 測試責任人變更、已完成與取消。公開發布、React／SDK 與 GitHub 部署都在選修。</p></section><section class="lesson-section" id="completion"><h2 class="section-heading">把原文判讀帶到模型生成與查核</h2><p class="body-text">本頁先留下有效交辦、取消、提議與未知欄位的判讀基準。接著閱讀<a href="PRAC6-1.html">生成並驗證 AI 會議交辦表</a>，用 A／B 原文查核模型；原文中的最後決議才是填表依據。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></main>
<!-- learner-content:end -->
