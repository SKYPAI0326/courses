---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-6
title: 面試評價橫向對比表
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">面試小組要根據職務相關證據比較候選人，而不是被印象或不同問題影響。本單元用同一評分規準記錄回答；分數需附證據、不得自動決定錄取，且只能使用必要且經授權的資料。</p><p class="body-text">同一職務使用相同問題和行為錨點，才能比較回答證據。分數缺漏要標未評，敏感個資最小化；錄取決定仍由面試小組依職務要求討論。</p><p class="body-text"><strong>固定職務與面試案例（皆為虛構）：</strong>職務是行政協調員；所有人回答同一題：「請說明你如何追蹤跨部門行政任務，以及遇到資料尚未到齊時怎麼處理？」任務追蹤：1＝沒有責任人／期限紀錄；3＝有清單但沒有主動追蹤；5＝記錄責任人與期限並主動追蹤。資料缺漏：1＝依猜測補值；3＝標待確認但沒有跟進；5＝標待確認並聯絡來源確認。溝通回報：1＝沒有回報；3＝提供一般進度；5＝說明風險並向適當負責人提出需決定事項。</p><p class="body-text"><strong>甲回答：</strong>「我把每項任務列在表格，寫負責人和期限，前一天追蹤；資料沒到就標待確認、聯絡窗口，再向主管回報可能延誤通知，請主管決定是否先發待確認版。」依序評 5／5／5。<strong>乙回答：</strong>「我照上次活動先估時間，資料不齊就先排下去，會後再問；平時大概記進度。」依序評 1／1／1。評分只依回答中的可觀察行為，不推論人格或錄取結果。</p><p class="body-text">參考品預載兩位虛構候選人的分數與回答證據。逐項核對分數是否符合上方錨點；在「回答證據與備註」欄保留原句，生成版再測未評和新增／刪除流程。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">interview-comparison.html</div>
</div>
<div class="tool-body">
<div style="overflow-x:auto;">
<div class="table-scroll"><table class="interview-table" id="interview-table">
<thead id="interview-head"></thead>
<tbody id="interview-body"></tbody>
</table></div>
</div>
<button class="add-candidate-btn" onclick="addCandidate()">+ 新增候選人</button>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">比較候選人前先訂職務相關的問題與行為錨點。總分只整理同一準則下的評分，不能代替面試小組決策；缺少證據的項目應標未評，不當成零分。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「面試評價橫向對比表」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
比較候選人前先訂職務相關的問題與行為錨點。總分只整理同一準則下的評分，不能代替面試小組決策；缺少證據的項目應標未評，不當成零分。

【操作與輸出】
使用者先填職務、共同面試問題、評分維度及行為錨點；維度可新增、修改和刪除，同次所有候選人共用相同標準，逐項記錄 1–5 分及支持分數的回答原句；可新增候選人、改名、刪除和橫向捲動。未評項目保持空白、不當作 0 分；只有目前所有維度都完成評分時才顯示總分，否則顯示已評項數，不顯示部分合計。總分僅供參考，不自動產生錄取建議。

【例外與安全】
面試資料使用虛構內容且最小化；未評和 1 分是不同狀態，未評不納入分數；僅目前所有維度皆已評分時顯示合計（滿分為維度數乘以五），否則只顯示已評項數、不顯示部分合計。避免與職務無關或受保護個人資料。名字／備註以純文字呈現，總分須可追溯至各項分數。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
職務：行政協調員。共同問題：「請說明你如何追蹤跨部門行政任務，以及遇到資料尚未到齊時怎麼處理？」固定錨點：任務追蹤 1＝無責任人／期限紀錄、3＝有清單但不主動追蹤、5＝記錄責任人／期限並主動追蹤；資料缺漏 1＝猜測補值、3＝標待確認但不跟進、5＝聯絡來源確認；溝通回報 1＝沒有回報、3＝一般進度、5＝說明風險並提出待決事項。甲回答「我把每項任務列在表格，寫負責人和期限，前一天追蹤；資料沒到就標待確認、聯絡窗口，再向主管回報可能延誤通知，請主管決定是否先發待確認版」，依序 5／5／5。乙回答「我照上次活動先估時間，資料不齊就先排下去，會後再問；平時大概記進度」，依序 1／1／1。每項附原句證據；再新增第三人，只評一個維度，確認狀態顯示「已評 1/3」、未評和 1 分不同且不出現部分合計；完成三維評分後才顯示合計；刪除候選人後欄位同步；分數不能自動決定錄取。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>讀取固定的行政協調員職務、共同面試問題、1／3／5 錨點和甲乙兩段回答；先按頁面給的 5／5／5 與 1／1／1 評分，為每個維度圈出支持分數的原句。</li><li>在預載參考品核對三個分數和備註原句；再新增一位候選人，將一個維度留白並確認沒有星星，狀態顯示已評 0/3；只評一項後仍不顯示部分合計。完成三項後才顯示合計。需要按維度保存證據時，在旁邊的紀錄表逐項記「維度｜原句｜錨點｜分數」。</li><li>用完整提示詞生成工具，保存為 interview-compare-v1.html，重新開啟後輸入同一案例；新增第三人並檢查窄螢幕／橫向表格，再刪除確認欄位和統計同步。</li><li>若空白被算為零或分數無法連回證據，修正資料欄位與彙總規則後重跑；交付職務規準、虛構回答、證據及仍需小組討論的問題。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">只用職務相關、經授權且必要的資料；分數不是自動錄取或淘汰規則。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若空白評分被算成零，分開未評與 0 分，並以同一套錨點重算比較。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>行政協調員使用本頁共同問題與三組 1／3／5 錨點。甲按任務追蹤、資料缺漏處理、溝通回報評 5／5／5；乙評 1／1／1；每個分數都能指回回答原句。新增第三位只評一維時，顯示已評 1/3 且不顯示部分合計；填完三維才出現總分。未評與 1 分不同。分數供面試小組討論，不自動錄取或淘汰。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">把分數連回共同規準與回答證據</h2><p class="body-text">交付共同問題、行為錨點、回答引證與評分紀錄。缺少評分保持未評，不和低分混用；面試小組再依職務需求討論，工具提供比較資料，不能自動決定錄取。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「把逐項評分與回答證據一起保存」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E15/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E15/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E15/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>兩題，評分4及3（共同1至5尺度），各填虛構回答證據。</td><td>已評2/2，合計7/10；可回看各題證據。</td></tr><tr><td>B</td><td>新增第三題，先不評分，再填2分。</td><td>未評時顯示已評2/3而無完整總分；填2後總分9/15。</td></tr><tr><td>例外</td><td colspan="2">超尺度或空評分不默認0；分數不能直接產生錄用決定。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e15-transfer-case">面試評分與證據表｜當次案例資料（可替換）

A
兩題，評分4及3（共同1至5尺度），各填虛構回答證據。

B
新增第三題，先不評分，再填2分。

例外
超尺度或空評分不默認0；分數不能直接產生錄用決定。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e15-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e15-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>

<!-- learner-content:end -->
