---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-12
title: 行政案件期限追蹤板
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">小型行政案件散落在便條和郵件中，窗口需要看責任人、期限、阻礙和下一步。下方參考品只有基本看板；本單元會把它升級成可匯入案件 CSV、計算期限並備份還原的本機追蹤板。</p><p class="body-text">Kanban 顯示案件目前狀態，不會自動同步同事或發送到期通知。localStorage 只在目前瀏覽器保存；JSON 備份要可重新匯入並核對欄位。</p><p class="body-text">先在參考品新增一張卡片並移動狀態，了解看板基本操作；接著下載 A01–A04 案件資料與改造指令，生成完整版並依本頁驗收。期限、匯入與備份是本單元要完成的增量，不是參考品現有功能。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">kanban-board.html</div>
</div>
<div class="tool-body">
<div class="kanban-board">
<div class="kanban-col" id="col-todo">
<div class="kanban-col-header">
<div class="kanban-col-title">待辦</div>
<span class="kanban-count cnt-todo" id="cnt-todo">0</span>
</div>
<div class="kanban-cards" id="cards-todo"></div>
<div class="kanban-add-wrap">
<textarea class="kanban-add-input" id="new-todo" placeholder="輸入新任務…" rows="2"></textarea>
<button class="kanban-add-btn" onclick="addCard('todo')">+ 新增待辦</button>
</div>
</div>
<div class="kanban-col" id="col-doing">
<div class="kanban-col-header">
<div class="kanban-col-title">進行中</div>
<span class="kanban-count cnt-doing" id="cnt-doing">0</span>
</div>
<div class="kanban-cards" id="cards-doing"></div>
<div class="kanban-add-wrap">
<textarea class="kanban-add-input" id="new-doing" placeholder="輸入新任務…" rows="2"></textarea>
<button class="kanban-add-btn" onclick="addCard('doing')">+ 新增進行中</button>
</div>
</div>
<div class="kanban-col" id="col-done">
<div class="kanban-col-header">
<div class="kanban-col-title">完成</div>
<span class="kanban-count cnt-done" id="cnt-done">0</span>
</div>
<div class="kanban-cards" id="cards-done"></div>
<div class="kanban-add-wrap">
<textarea class="kanban-add-input" id="new-done" placeholder="輸入新任務…" rows="2"></textarea>
<button class="kanban-add-btn" onclick="addCard('done')">+ 新增完成項目</button>
</div>
</div>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">Kanban 欄位表示工作目前狀態，不會自動代表負責人已承接或任務已完成。localStorage 只保存目前瀏覽器；多人協作需另選有權限管理的共同系統。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位熟悉行政案件追蹤與瀏覽器端資料管理的前端工程師。請把簡單的個人 Kanban 升級為「行政案件期限追蹤板」，供單人整理責任人、期限、阻礙與下一步。交付完整單檔 HTML，不呼叫 AI 或外部 API。

【資料與欄位】
CSV 欄位為 case_id、task、owner、due_date、status、blockage、next_action、result。提供CSV匯入欄與可下載空白欄位範本，讓使用者選取自己的資料檔。每張案件卡顯示並可編輯任務、責任人、期限、狀態、阻礙、下一步和結果；case_id 是唯一識別碼。允許匯入 CSV、匯出 CSV、JSON 備份及 JSON 還原。

【期限和狀態】
- 提供可手動指定的「截至日」，避免測試答案隨今天改變。
- 空白期限顯示「期限待確認」，不可當作永不逾期或自行補日期。
- 未完成且期限早於截至日的案件列為逾期；完成案件不計逾期。
- 提供可設定的非負整數「近期日數」；未完成且期限在截至日到該設定日數後（含起訖）列為近期；其餘依待辦／進行中／完成狀態顯示。
- 修改日期、狀態或截至日後，卡片標籤和統計立即重算。

【匯入和資料保存】
- CSV 首列必須符合欄位；無效檔案先提示，原資料不得清空。
- 重複 case_id 要逐筆提示，讓使用者選擇更新既有案件或保留既有資料；絕不建立重複卡片。
- JSON 備份包含 schema version；還原前驗證版本、陣列、欄位型別及唯一 ID。無效備份不得改動現有資料。
- 資料只保存於目前瀏覽器 localStorage；顯示儲存範圍和 JSON 備份方式，不宣稱多人同步或背景通知。儲存失敗需提示且保留本分頁狀態。
- CSV 欄位內容與案件名稱以純文字呈現，不插入 HTML；不要要求輸入機密或敏感個資。



提供清楚的狀態文字、空狀態和錯誤提示；日期計算採日曆日期，手機可操作。輸出完整 HTML 原始碼，不省略 CSV/JSON 匯入匯出、期限計算、重複識別和驗收功能。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次資料檔：cases.csv；截至日2026-10-06；近期視窗三個日曆日。資料檔只供匯入測試，可換相同欄位的其他檔案。

測試資料與檢查方式：
以截至日 2026-10-06 匯入課程 CSV：A01 期限 10/09，列為近期；A02 無期限，列為期限待確認；A03 期限 10/05 且待辦，列為逾期；A04 期限 10/06 且完成，不列逾期。把 A03 改為完成後，逾期數減一。再次匯入相同 CSV 時，A01–A04 不得重複；對 A01 選擇更新時也只能保留一張卡。匯出 JSON、重新載入頁面再還原，核對責任人與期限；匯入損毀 JSON 時原卡片全部保留。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p><p><a download="" href="../assets/materials/prompt-cases-case.txt">下載此區案例TXT</a>，可獨立附加或換成自己的資料。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>先操作參考看板新增一筆任務並移動一次，確認欄位變化；再下載 cases.csv 和本頁完整改造指令，了解 A01–A04 的責任人、期限與狀態。</li><li>把完整指令貼入 AI Studio Chat，保存生成頁為 admin-cases-v1.html，重新開啟並匯入 CSV；將截至日設為 2026-10-06。</li><li>核對 A01 近期、A02 期限待確認、A03 逾期、A04 完成；把 A03 改完成後確認逾期數減一，再匯入相同檔案測試重複 ID 選擇。</li><li>匯出 JSON、重新載入後還原；再用損毀 JSON 測試原資料是否保留。若重複案件或期限分類錯，只修正對應規則並重跑整套案例。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">避免存放敏感個資；localStorage 可能被清除且不支援跨裝置協作，定期匯出備份。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若重複匯入產生重複案件，先定義唯一案件 ID，再測相同 ID 更新而不新增第二筆。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元完整驗收：</strong>先下載 <a download="True" href="../assets/materials/cases.csv">案件資料 CSV</a> 和 <a download="True" href="../assets/materials/prompt-cases.txt">改造指令</a>，將 A01–A04 匯入新版工具並把截至日設為 2026-10-06：A01 近期、A02 期限待確認、A03 逾期、A04 完成。把 A03 改完成後逾期數減一；再次匯入 A01 時不得產生第二張卡。匯出 JSON、重開並還原，核對責任人與日期；損毀備份不得覆蓋原資料。資料只在目前瀏覽器保存，不代表多人同步或關閉後通知。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">交付能還原的案件狀態與期限</h2><p class="body-text">保留案件來源、責任人、期限、阻礙與下一步，實際匯出並還原備份。下次更新先核對案件識別與是否已完成；本機期限提示不會自動同步同事或在關閉後通知。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「依截止日/完成狀態算逾期與近期」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E21/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E21/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E21/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>截至2026-10-08、近期2日；A未完成期限10/07、B未完成期限10/08、C完成期限10/07、D未完成期限空白。</td><td>A逾期、B近期、C不計逾期、D期限待確認。</td></tr><tr><td>B</td><td>新增E未完成期限10/10及F期限10/11；將A改完成。</td><td>E近期（含2日邊界）、F非近期；A不再逾期。</td></tr><tr><td>例外</td><td colspan="2">重複case_id需選更新/保留，不新增重複卡；無效CSV/備份不能清空既有。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e21-transfer-case">行政案件期限追蹤板｜當次案例資料（可替換）

A
截至2026-10-08、近期2日；A未完成期限10/07、B未完成期限10/08、C完成期限10/07、D未完成期限空白。

B
新增E未完成期限10/10及F期限10/11；將A改完成。

例外
重複case_id需選更新/保留，不新增重複卡；無效CSV/備份不能清空既有。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e21-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e21-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>

<!-- learner-content:end -->
