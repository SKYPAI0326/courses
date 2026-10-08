---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-5
title: 專案進度「紅綠燈」看板
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">專案會議需要快速看出哪些工作按期、需注意或已受阻。本單元用狀態定義和更新日期整理看板；紅黃綠只作提示，每筆仍需寫明責任人、期限、阻塞原因和下一個行動。</p><p class="body-text">狀態顏色只標示當下分類。可採取行動的看板還需要責任人、期限、阻塞原因、更新時間和下一步，並由團隊按固定節奏更新。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">project-traffic-light.html</div>
</div>
<div class="tool-body">
<div class="traffic-board" id="project-board"></div>
<button class="add-project-btn" onclick="addProject()">+ 新增專案</button>
<div class="traffic-stats" id="traffic-stats"></div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">紅黃綠只表示約定的風險分類。工作上能採取行動的項目還要有負責人、期限、阻塞原因和下一步；狀態不能靠顏色單獨傳達。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「專案進度紅黃綠狀態看板」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
紅黃綠只表示約定的風險分類。工作上能採取行動的項目還要有負責人、期限、阻塞原因和下一步；狀態不能靠顏色單獨傳達。

【操作與輸出】
每筆專案含名稱、負責人、期限、狀態、阻塞原因與下一行動；允許新增、編輯、刪除及切換狀態。底部統計各狀態筆數，列表以文字標記狀態並可按風險篩選。

【例外與安全】
初始狀態需明確；空名稱或重複項提示；紅色狀態若無阻塞原因或下一行動，顯示待補欄位。輸入當作純文字，不用顏色作唯一提示。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
新增「場地確認」由林小姐負責、10/12 截止、黃色、等待供應商報價、下一步週三追蹤；切成紅色後檢查統計更新。清空阻塞原因時仍顯示需補資料；輸入標記字串只作文字。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>先依團隊定義寫下綠、黃、紅各自代表什麼，避免把顏色當成通用標準；在參考品建立一項場地確認任務。</li><li>複製完整提示詞生成工具，保存為 project-status-v1.html，重開後用同一筆資料測試。</li><li>核對負責人、期限、阻塞原因和下一步；將黃色切為紅色，觀察文字狀態和統計，再清空阻塞原因確認系統提示補資料。</li><li>測試標記字串只以文字呈現；若切換狀態使其他欄位消失，修正更新流程並重測。最後保存能直接支持會議決策的完整清單。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">狀態需依團隊定義更新；不要只用燈號對外承諾進度或取代風險說明。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若切換燈號後任務原因或負責人消失，回修資料結構並確認更新只改狀態欄位。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>新增「場地確認」：林小姐負責、2026-10-12 截止、黃色、阻塞原因為等待供應商報價、下一步為週三追蹤。改成紅色後狀態統計須更新，阻塞原因仍可見；清空阻塞原因後仍須提醒補資料。再輸入 &lt;script&gt;alert(1)&lt;/script&gt; 確認只顯示文字。交付可供會議討論的狀態、責任、期限、原因與下一步。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">讓狀態顏色能連到下一個行動</h2><p class="body-text">每筆狀態應能說明責任人、期限、阻塞原因與下一步。保存更新時間與核對紀錄，再用看板討論要處理的問題；下次會議先更新資料，避免沿用已過期的顏色結論。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「人工標風險並維護阻礙及下一步」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E14/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E14/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E14/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>三項甲綠/乙黃/丙紅；丙負責=示範承辦、期限10/15、阻礙=資料待補、下一步=詢問窗口。</td><td>各狀態1項；丙有可行動資訊；篩選紅只顯示丙。</td></tr><tr><td>B</td><td>將乙改紅并填阻礙/下一步，刪甲。</td><td>紅2、黃0、綠0；修改只影響指定專案。</td></tr><tr><td>例外</td><td colspan="2">空名稱/重複名稱提示；紅色未填阻礙或下一步要指出缺欄，不替人猜風險。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e14-transfer-case">專案風險狀態看板｜當次案例資料（可替換）

A
三項甲綠/乙黃/丙紅；丙負責=示範承辦、期限10/15、阻礙=資料待補、下一步=詢問窗口。

B
將乙改紅并填阻礙/下一步，刪甲。

例外
空名稱/重複名稱提示；紅色未填阻礙或下一步要指出缺欄，不替人猜風險。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e14-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e14-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>

<!-- learner-content:end -->
