---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-7
title: 站立會議發言抽籤器
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">多人想輪流發言，需要一份不重複的建議順序時，使用這頁。 準備自願參與者名單；先用示例名單練習。</p><ol class="step-list"><li>先輸入名單並抽出一次順序，逐一核對有沒有漏人或重複。</li><li>名單成員各出現一次；主持人仍可接受跳過或調整。</li></ol></section><section class="lesson-section" id="example-start"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">每週站會有多人希望輪流發言，主持人需要一個不重複的建議順序。本單元為自願參與者抽出順序；抽籤不等於公平或強制發言，主持人可接受跳過、重抽或調整。</p><p class="body-text">不重複抽取是「無放回」的隨機排列；隨機只決定順序，不代表參與公平。活動需自願，主持人應保留略過、退出和手動調整。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">standup-lottery.html</div>
</div>
<div class="tool-body">
<div class="lottery-setup">
<div style="font-size:.73rem;color:var(--c-a1);letter-spacing:1px;font-weight:500;margin-bottom:8px;">輸入自願參與者（每行一位）</div>
<textarea id="name-list" placeholder="王小明
林小花
陳大偉
張美玲
李志遠" style="width:100%;min-height:100px;padding:12px 14px;border:1px solid var(--c-border);border-radius:4px;font-family:inherit;font-size:.9rem;background:var(--c-bg);resize:vertical;line-height:1.8;"></textarea>
<button class="compose-btn" onclick="startLottery()" style="margin-top:10px;width:auto;padding:10px 24px;">開始抽籤</button>
</div>
<div id="lottery-active" style="display:none;">
<div class="lottery-result">
<div style="font-size:.7rem;color:var(--c-muted);letter-spacing:2px;margin-bottom:12px;">NOW SPEAKING</div>
<div class="lottery-name-display" id="current-name">—</div>
<div class="lottery-sub" id="lottery-sub">按下方按鈕開始</div>
</div>
<div style="text-align:center;">
<button class="next-btn" id="next-btn" onclick="nextPerson()">Next <span aria-hidden="true">→</span></button>
<button class="next-btn" disabled="" id="skip-btn" onclick="skipPerson()">略過此人</button>
<button onclick="resetLottery()" onmouseout="this.style.borderColor='var(--c-border)'" onmouseover="this.style.borderColor='var(--c-a1)'" style="background:none;border:1px solid var(--c-border);padding:10px 20px;border-radius:var(--radius-sm);font-family:inherit;font-size:.8rem;cursor:pointer;color:var(--c-muted);margin-left:8px;transition:border-color .15s;">重置名單</button>
</div>
<div style="margin-top:16px;">
<div style="font-size:.73rem;color:var(--c-muted);letter-spacing:1px;font-weight:500;margin-bottom:8px;">本輪已叫號 · <span id="called-count">0</span> / <span id="total-count">0</span></div>
<div class="called-list" id="called-list"></div>
<p aria-live="polite" id="lottery-status" role="status" style="font-size:.8rem;color:var(--c-muted);"></p>
</div>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">無放回抽取可避免同一人重複出現，但隨機順序不代表發言公平，也不授權主持人強迫參與。參與者應可跳過、退出或由主持人調整。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「自願參與者發言順序抽籤器」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
無放回抽取可避免同一人重複出現，但隨機順序不代表發言公平，也不授權主持人強迫參與。參與者應可跳過、退出或由主持人調整。

【操作與輸出】
輸入每行一位自願參與者，去除首尾空白並建立一份隨機排列；按下一位只移出一人，顯示目前姓名、已抽／剩餘數及已抽名單。提供「略過」按鈕：被略過者留在本輪未發言名單，可稍後再抽；可重設並重新抽取。

【例外與安全】
忽略空行、拒絕重複姓名並指出重複項；空名單不能開始；名單以純文字顯示；抽完後停用按鈕，不能抽出名單外的人。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
加入「甲、乙、丙、丁、戊」五位自願參與者，抽出順序並確認每人只出現一次；按「略過」後抽下一位，確認略過者不算已發言。重設後清空本輪狀態；空名單不可開始，重複姓名須指出並保留可修正名單。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>先確認參與者都是自願加入，準備甲、乙、丙、丁、戊五個測試名稱；先說明抽籤只安排次序，不決定誰必須發言。</li><li>在參考品輸入名單並抽取，核對同一輪不重複；略過一人後抽下一位，區分「略過」和「已發言」。</li><li>貼上完整提示詞生成工具，保存為 volunteer-order-v1.html，重開後重做五人測試；完成一輪再試抽取，應停止。</li><li>測空名單、重複名稱與重設；若略過者仍被列為已發言，修正狀態欄位並重跑整輪測試。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">只用自願參加者名單，尊重跳過或退出；主持人保留調整順序的權限。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若本輪抽到重複人名，檢查名單正規化和已抽集合；重新開始時才清空本輪記錄。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>加入甲、乙、丙、丁、戊五位自願參與者，產生不重複順序；按「略過」後抽下一位，檢查被略過者不會記為已發言。完成一輪後不得再抽，重新開始要清空本輪狀態。測空名單與重複姓名的提示；主持人仍可尊重退出、跳過並人工調整，不強迫發言。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">區分叫號、略過與實際發言</h2><p class="body-text">保留本輪順序與狀態，確認不重複且略過者沒有被記成已發言。下一輪重設時才清除本輪紀錄；主持人仍尊重退出與調整，隨機排列只協助安排順序。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「隨機取樣並區分已點與未點」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E16/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E16/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E16/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>名單=甲、乙、丙；連點三次。</td><td>順序不固定，但三人各出現一次；第四次提示已點完。</td></tr><tr><td>B</td><td>新名單=丁、戊；重設再點兩次。</td><td>只出現丁戊、不保留前組已點狀態。</td></tr><tr><td>例外</td><td colspan="2">空名單提示；首尾空白及重複姓名要核對；不能用固定抽中順序驗收隨機工具。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e16-transfer-case">不重複隨機點名｜當次案例資料（可替換）

A
名單=甲、乙、丙；連點三次。

B
新名單=丁、戊；重設再點兩次。

例外
空名單提示；首尾空白及重複姓名要核對；不能用固定抽中順序驗收隨機工具。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e16-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e16-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>
<!-- learner-content:end -->
