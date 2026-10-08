---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-11
title: 團隊可用時段回報表
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">跨部門會議需要成員回報幾個候選時段的忙碌情況。本單元用表格彙整「忙、可討論、未知」；固定案例 A＝週一 09:00、B＝週一 10:00。空白必須保持未知，工具沒有讀取日曆或確認出席的能力。</p><p class="body-text">忙碌、稍忙與未知是不同狀態；稍忙代表仍需主持人協調，空白不能當成有空。時段彙整只產生討論候選，最後需確認會議長度、日曆和每位出席者。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">team-heatmap.html</div>
</div>
<div class="tool-body">
<div class="callout info" style="margin-bottom:16px;">
<div aria-hidden="true" class="callout-icon">💡</div>
<div class="callout-body">點擊循環：未確認→空閒→稍忙→忙碌→非常忙→未確認。格子同時以文字與顏色顯示狀態；稍忙代表仍需主持人協調。新增成員或清空資料都回未確認，不可把沒填當作空閒。</div>
</div>
<div class="member-input-wrap">
<input class="member-input" id="new-member" onkeydown="if(event.key==='Enter')addMember()" placeholder="輸入成員名稱後按 Enter 新增"/>
<button class="compose-btn" onclick="addMember()" style="width:auto;padding:8px 16px;font-size:.8rem;">新增成員</button>
</div>
<div class="member-tabs" id="member-tabs"></div>
<div class="heatmap-controls">
<button class="hm-ctrl-btn" onclick="clearCurrentMember()">清除當前成員資料</button>
<button class="hm-ctrl-btn" onclick="removeCurrentMember()">移除當前成員</button>
<button class="hm-ctrl-btn" onclick="resetDemoList()">重設固定案例名單</button>
<button class="hm-ctrl-btn" onclick="showOverall()">顯示整體熱度</button>
<span style="font-size:.75rem;color:var(--c-muted);margin-left:4px;">檢視：<strong id="current-member-label">—</strong></span>
</div>
<div class="heatmap-wrap">
<div class="table-scroll"><table class="heatmap-table" id="heatmap-table"></table></div>
</div>
<div class="heat-legend">
<span>忙碌程度：</span>
<div class="heat-swatch heat-0"></div><span>空閒</span>
<div class="heat-swatch heat-1"></div><span>稍忙（仍需主持人協調）</span>
<div class="heat-swatch heat-2"></div><span>忙碌</span>
<div class="heat-swatch heat-3"></div><span>非常忙</span>
<span>未確認：尚未填資料</span></div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">下方指令包含工具用途、輸入、主要規則、輸出和介面要求。先讀一遍，圈出會影響結果的規則；生成後依第三節的固定案例測試，不用外觀或模型自述代替驗收。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位重視可用性、資料安全與無障礙的前端工程師。請為跨部門會議主持人製作「團隊可用時段回報表」，交付一份可直接以瀏覽器開啟的單一 HTML，CSS 與 JavaScript 都放在檔案內，不使用伺服器、外部 API 或日曆權限。

【工作情境與目的】
主持人先設定參與者名單、日期或星期清單、每日起訖時間與正整數分鐘間隔，再請每人回報各格狀態。名單、日期與時段可新增、修改和刪除；結束須晚於開始，間隔須可完整切分該時段；調整結構後先提示並清除已不適用的回覆，不把舊狀態套在不同日期。這份表只用來整理回覆，不能連線讀取日曆、代替本人確認，亦不能把候選時段視為已約定。

【輸入與操作】
- 可新增成員；去除前後空白，拒絕空名稱和重複名稱，並說明原因。新增者所有格子都從「未確認」開始。
- 以表格呈現成員與星期／時段。點選目前成員的一格時，依序循環：未確認 → 空閒 → 稍忙 → 忙碌 → 非常忙 → 未確認。
- 提供目前成員分頁、整體檢視、清除目前成員資料（需確認，保留成員）與移除目前成員（需確認，至少保留一人）；另提供清空所有回覆操作，確認後保留目前使用者設定的名單與時段，所有回覆回到未確認。
- 明確顯示狀態文字和圖例；不能只用顏色區分。窄螢幕可橫向捲動表格。

【整體彙整規則】
- 任一人標為「忙碌」或「非常忙」時，顯示其中最高忙碌程度。
- 沒有忙碌回覆但至少一人未確認時，整體為「未確認」。
- 只有所有成員都明確回覆「空閒」，才能標示「全員回報空閒」；稍忙時顯示「稍忙」，並說明「仍需主持人協調」，不自動判定可開會。
- 新成員、清除資料及空白欄位都不得預設成空閒；顯示整體狀態的文字說明。

【保存、例外與安全】
- 可在目前瀏覽器保存成員與回覆，並清楚說明資料不會自動同步到其他裝置；儲存失敗時顯示提示，頁面仍可操作。
- 所有成員名稱都當作純文字顯示，不把輸入內容當作 HTML 或程式執行。
- 不要求或暗示學員輸入真實敏感行程；使用假名與假時段練習。



輸出完整 HTML 原始碼，不要省略 CSS、事件處理、狀態計算或驗收功能；頁面文字使用繁體中文，標題、欄位與錯誤提示清楚易懂。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次回報設定：三人甲、乙、丙；週一至週五，每天09:00–17:00，每格一小時。可改名單、日期與時段。

測試資料與檢查方式：
新增甲、乙、丙三人。A＝週一 09:00、B＝週一 10:00：甲在 A 設「忙碌」，乙在 B 設「忙碌」，丙兩格留「未確認」。整體不得把未知算成空閒。把丙兩格改為「空閒」後，A、B 仍分別顯示有人忙。再選週一 11:00，將三人該格都設為「空閒」，才可顯示「全員回報空閒」。清除一人資料後該人回未確認，整體也不能維持空閒結論。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>每次開始固定案例先按「重設固定案例名單」並確認；名單會回到甲、乙、丙，所有回覆清空為未確認，舊成員不會留在整體計算中。A 是表格的週一 09:00 格，B 是週一 10:00 格；從未確認開始，各點擊三次，把甲 A 設忙碌、乙 B 設忙碌，丙兩格保持未確認。每格都有可見狀態文字，不必靠顏色或滑鼠提示判讀。</li><li>複製完整提示詞到 AI Studio Chat，生成後存成 team-availability-v1.html，從資料夾重新開啟，確認可新增、清除及移除成員；取消移除時資料不變，至少保留一人。</li><li>再將丙 A、B 設為空閒，確認兩時段仍各有忙碌；在週一 12:00，先將甲設稍忙、乙與丙明確設空閒，整體應顯示稍忙；再將乙改為未確認，整體應回到未確認；乙恢復空閒後又顯示稍忙。圖例仍需提醒主持人協調。於週一 11:00 將三人都設為空閒，確認只有這一格可顯示全員回報空閒。清除甲資料後確認甲回未確認且整體不保留空閒結論，記錄狀態文字而不只記顏色。</li><li>若空白被當成空閒，要求只修正初始值與彙整規則，另存 v2，重跑四個案例並保留兩版結果。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">不要把候選交集稱為已確認空檔；未知回覆要追問本人或查正式日曆。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若空白格變成可用時段，修正預設狀態為未知，再用一位未回覆者重測彙整。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>A＝週一 09:00、B＝週一 10:00；甲 A 忙、乙 B 忙、丙兩格未知。整體不能把未知算成空閒。丙兩格設空閒後，A、B 仍各有忙碌；週一 11:00 三人都明確設空閒才可顯示全員回報空閒。清除甲資料後，甲回未知且整體撤回空閒結論。另驗證三人狀態：甲稍忙、乙與丙空閒時，整體為稍忙；把乙改為未確認時，整體改為未確認；乙恢復空閒後才顯示稍忙，並提示仍需主持人協調。主持人仍須確認會議長度與日曆。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">讓每個候選時段保留未確認資訊</h2><p class="body-text">保存各人的回報及整體狀態，確認忙碌不被平均隱藏、空白仍是未知。主持人再確認時長與日曆；下次更新回報時重新核對，不能把單一時段的空閒延伸成整場會議都能出席。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「依未回報/忙碌等優先順序彙整時段」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E20/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E20/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E20/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>三人甲乙丙，兩時段09:00、10:00；甲09忙、乙10忙、丙皆未回報；其他格空白。</td><td>09與10均顯示忙碌，不因其他未回報蓋過忙碌；不自动建立會議。</td></tr><tr><td>B</td><td>同三人11:00皆可用；另12:00一人未回報、其餘可用。</td><td>11全員回報可用；12待確認；清掉11任何一人改待確認。</td></tr><tr><td>例外</td><td colspan="2">開始必早於結束、粒度正整數；不推定未回報是可用或替人填狀態。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e20-transfer-case">團隊可用時間彙整｜當次案例資料（可替換）

A
三人甲乙丙，兩時段09:00、10:00；甲09忙、乙10忙、丙皆未回報；其他格空白。

B
同三人11:00皆可用；另12:00一人未回報、其餘可用。

例外
開始必早於結束、粒度正整數；不推定未回報是可用或替人填狀態。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e20-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e20-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>

<!-- learner-content:end -->
