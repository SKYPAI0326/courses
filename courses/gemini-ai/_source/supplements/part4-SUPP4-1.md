---
slug: gemini-ai
unit_id: SUPP-part4-SUPP4-1
title: 補充：多案例成果保存與重開
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<main class="lesson-body"><section class="lesson-section" id="core-1"><h2 class="section-heading">整理交付包，不再建一個保存工具</h2><p class="body-text">在 AI工作工具 資料夾建立「工具」「資料」「指令」「報告」「驗收」「歷史版本」六個子資料夾。每種工具只把最後通過驗收的檔案放在「工具」：例如 meeting-timer-v2.html、activity-budget-v2.html、department-kpi.html。實際檔名依你的驗收紀錄填入 README；沒修過的工具仍可用原檔名。未通過的舊版放「歷史版本」，不要讓它成為開啟入口。CSV、逐字稿與 JSON 放「資料」；完整生成與修復指令放「指令」；PDF 與交辦 CSV 放「報告」。</p><p class="body-text">AI 交辦需要 Build 專案與伺服器模型呼叫；在 README 寫下專案標題、可重開的書籤網址、登入條件與重新測試方法。專案 ZIP 是程式碼備份，不能取代平台內專案重開與預覽測試。</p><p class="body-text">資料夾可以長這樣：<code>AI工作工具/工具</code> 放驗收通過的 HTML；<code>資料</code> 放 CSV、逐字稿與 JSON；<code>指令</code> 放完整生成及修復提示詞；<code>報告</code> 放 CSV／PDF 輸出；<code>驗收</code> 放預期／實際紀錄；<code>歷史版本</code> 放不再作為入口的舊版。版本名稱寫清楚，例如 <code>activity-budget-v2.html</code>，README 只指向目前通過的版本。</p></section>
<section class="lesson-section" id="core-2"><h2 class="section-heading">關閉、重開、更新、再輸出</h2><ol class="body-text"><li>依 README 的實際檔名，關閉單檔工具分頁後從「工具」資料夾重開；核對資料或匯入備份。KPI 資料未保留時，匯入KPI 補充頁下載的 department-kpi-backup.json，確認回到 120 件、5 天、1%；無效備份不能覆蓋正常資料。</li><li>預算改一個備註再輸出；KPI 改一個實際值，先預判狀態、再輸出月報。打開新 CSV／PDF，確認內容更新，並把這個測試記在新列。</li><li>點 AI Studio 專案書籤；確認專案標題和既有預覽回來後，用 A 重跑，核對至少兩項有效交辦與原文。若書籤沒有回到同一專案，依當下畫面找同名專案；仍找不到時保存網址、標題與登入／權限狀態，標記「平台重開待完成」，回看<a href="https://ai.google.dev/gemini-api/docs/aistudio-build-mode" rel="noopener" target="_blank">官方 Build 說明</a>和帳號存取條件。不能以 Share 或 ZIP 代替重開證據。</li><li>從資料夾開交辦 CSV，確認原文、未知、確認欄都在。打開驗收表，記實際檔名與版本，區分學員生成、參考品及待完成，不以捲動進度代替工作成果。</li></ol><p class="body-text">做一次「資料真的能帶走」測試：先下載 JSON 備份，關閉頁面後重開，再匯入備份；核對 26,000／27,800／1,800／2,200。匯入破損檔時，原資料應保留並出現錯誤提示。AI Studio Build 專案則以專案書籤重新開啟，確認預覽還在，再用逐字稿 A 重跑；ZIP 是程式碼備份，不能證明平台專案可重新開啟。</p></section>
<section class="lesson-section" id="core-3"><h2 class="section-heading">使用說明與修復入口</h2><p class="body-text">新增 README.txt，寫「工具用途、打開方式、資料來源、正常答案、未知如何處理、備份位置、失敗回到哪個步驟」。例如預算公式錯回預算生成對話；副檔名錯回存檔；AI 整理錯回 Build 規則並重測 A/B。不要在修復時刪掉所有原資料。</p><p class="body-text">本機文件含資料時，只交給需要使用的人。公開網址、多人同步與背景通知另學；保存好檔案、可重新查核與更新，已能支持下次工作。</p><div class="prompt-wrap"><div class="prompt-label">README 使用說明範本</div><pre class="prompt-box">用途：
打開方式：
需要的輸入與資料來源：
一筆已知答案：
空值／錯誤資料會怎麼處理：
資料與 JSON 備份位置：
目前通過驗收的檔名／版本：
失敗時回到哪個步驟：
仍待完成的限制：</pre></div><p class="body-text">讓未參與製作的同事照 README 找到工具、輸入標準資料並比對答案；若他需要詢問你「哪個版本能用」或「資料從哪裡來」，交付說明還不完整。外部分享或部署另有權限和費用，不由本機保存流程自動解決。</p></section><section class="lesson-section" id="completion"><h2 class="section-heading">依成果類型選擇保存方式</h2><p class="body-text">各案例的檔案、資料與專案入口要分別保存。重開時核對真正需要的輸入與成果；本機檔案不能代替雲端專案，書籤也不能代替資料備份。只回報你實際重開通過的項目。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></main>
<!-- learner-content:end -->
