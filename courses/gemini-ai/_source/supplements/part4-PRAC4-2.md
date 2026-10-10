---
slug: gemini-ai
unit_id: SUPP-part4-PRAC4-2
title: 個人 Prompt 庫管理器
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">提示詞越存越多，想搜尋、複製與備份時，使用這頁製作本機提示詞庫。 完成第三章後使用；準備幾份已核對的提示詞，先用假資料測試。</p><ol class="step-list"><li>先試用參考品新增一筆提示詞，再依完整需求生成自己的工具。</li><li>能搜尋、複製、匯出並還原；備份另存檔案，避免只留在瀏覽器。</li></ol></section><section class="lesson-section" id="example-start"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">你想保存常用提示詞，並在下次工作時快速搜尋、複製和帶走。本單元做一個僅存在目前瀏覽器的 Prompt 庫；完成物包含匯出備份和還原測試，localStorage 不會自動跨裝置同步。</p><p class="body-text">瀏覽器 localStorage 以目前網站來源和瀏覽器為範圍。清除網站資料或換裝置可能找不到內容，所以 JSON 匯出是可攜備份，匯入前要先驗證。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">prompt-library.html</div>
</div>
<div class="tool-body">
<div class="plib-toprow">
<input class="plib-search" id="plib-search" oninput="renderCards()" placeholder="搜尋 Prompt 標題或內容…" type="text"/>
<button class="plib-copy-btn" onclick="exportPrompts()" type="button">匯出 JSON</button>
<button class="plib-copy-btn" onclick="document.getElementById('plib-import-file').click()" type="button">匯入 JSON</button>
<input accept="application/json,.json" hidden="" id="plib-import-file" type="file"/>
</div>
<p aria-live="polite" id="plib-status" role="status" style="font-size:.75rem;color:var(--c-muted);"></p>
<div class="plib-tag-filter" id="plib-tags"></div>
<div class="plib-cards" id="plib-cards"></div>
<div class="plib-add-form">
<div class="plib-form-label">＋ 新增 Prompt</div>
<div class="plib-form-row">
<input aria-label="Prompt 標題" class="plib-form-input" id="pf-title" placeholder="Prompt 標題" type="text"/>
<input aria-label="分類標籤" class="plib-form-input" id="pf-tag" placeholder="標籤（例：寫作、分析）" style="max-width:160px" type="text"/>
<input aria-label="Prompt 版本" class="plib-form-input" id="pf-version" placeholder="版本（例：v1）" style="max-width:120px" type="text" value="v1"/>
</div>
<textarea aria-label="完整 Prompt 指令" class="plib-form-textarea" id="pf-body" placeholder="在這裡貼入你的完整 Prompt 指令…"></textarea>
<button class="plib-save-btn" onclick="savePrompt()">儲存到庫</button>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">localStorage 只在目前瀏覽器與網站來源保存資料，不會跨裝置同步；JSON 才是可攜備份。匯入前完整驗證，才能避免損壞檔覆蓋仍可用的資料。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「個人 Prompt 庫管理器」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
localStorage 只在目前瀏覽器與網站來源保存資料，不會跨裝置同步；JSON 才是可攜備份。匯入前完整驗證，才能避免損壞檔覆蓋仍可用的資料。

【操作與輸出】
可新增含標題、分類、版本（例如 v1）、完整提示詞與日期的紀錄；即時搜尋標題／內容、分類篩選、複製、刪除、展開長文；在目前瀏覽器保存。提供版本化 JSON 匯出與匯入。

【例外與安全】
新增必填欄缺漏時保留輸入。舊版紀錄缺少版本欄時載入為 v1。匯入前一次驗證檔案版本、陣列、欄位型別、識別碼唯一性與長度；錯誤檔不動原資料。儲存失敗要明示本分頁暫存，要求下載備份。所有使用者文字只作純文字。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
新增一筆「活動通知」提示詞，分類填「行政」、版本填「v1」，搜尋標題和正文、按分類篩選、複製及展開；匯出後重整頁面，再匯入備份核對標題、分類、版本和內容。匯入格式損毀或重複 ID 的 JSON 時，原資料數量與文字必須保持不變。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>先說明提示詞庫中每筆資料需要標題、用途分類、版本和完整正文；在參考品新增「活動通知／行政／v1」，搜尋標題與內文，再試分類篩選、展開和複製。</li><li>複製完整提示詞至 AI Studio Chat 生成單檔工具，保存為 prompt-library-v1.html，關閉並重新開啟；新增同一筆案例，確認版本可見且重載後仍在。</li><li>匯出 JSON 並保留檔案；清除測試記錄或在測試副本中重新載入後匯入，逐欄核對。另用格式錯誤和重複 ID 的 JSON 測試，確認錯誤提示出現且原資料沒有被覆蓋。</li><li>若分類、版本或正文在重開／匯入後遺失，先檢查欄位結構和驗證規則，再修正並重跑正常與損毀備份案例；最後記錄 localStorage 只屬目前瀏覽器來源。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">不要把 API key、客戶資料或機密放進可匯出的提示詞；備份檔可讀取，需存放在允許的位置。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若無效 JSON 清空了內容，立即保留原始備份；修復為先驗證完整結構再匯入，重測有效和損毀檔。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>新增「活動通知」記錄，分類為「行政」、版本為「v1」；搜尋標題與內文、分類篩選、展開並複製全文。匯出 JSON、重新載入頁面後匯入備份，核對標題、分類、版本和內文；再分別匯入格式錯誤及重複 ID 的 JSON，原資料必須完整保留。交付備份檔與本機保存範圍說明。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">驗證提示詞資料可以保存與找回</h2><p class="body-text">留下含用途與版本的提示詞記錄，實際匯出、重開與還原，再查內容是否完整。資料庫用來找回方法與測試紀錄；下一次使用仍須確認案例資料和工作條件。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「存方法、類別與版本，再用檔案還原」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E23/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E23/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E23/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>新增題名=資料清理、類別=資料、版本=v1、內容=一段可重用結構需求；下載備份。</td><td>四欄完整保存，內容以純文字顯示。</td></tr><tr><td>B</td><td>新增題名=報告整理、類別=文字、版本=v2；還原A備份。</td><td>還原內容與A一致，不混入B；搜尋分類結果與目前資料一致。</td></tr><tr><td>例外</td><td colspan="2">無效JSON保留現有；空題名/空內容提示；備份由工具處理不要求手寫。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e23-transfer-case">提示詞資料庫與版本管理｜當次案例資料（可替換）

A
新增題名=資料清理、類別=資料、版本=v1、內容=一段可重用結構需求；下載備份。

B
新增題名=報告整理、類別=文字、版本=v2；還原A備份。

例外
無效JSON保留現有；空題名/空內容提示；備份由工具處理不要求手寫。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e23-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e23-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>
<!-- learner-content:end -->
