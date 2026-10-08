---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-10
title: 核准詞表文字初篩器
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">審稿人手上有一份已核准詞表，想先找出文件中可能需要覆核的詞。本單元做字串命中提示；完整檢查仍要人工閱讀上下文，工具會漏掉同義表達，也會把無害用法標出。</p><p class="body-text">詞表採逐字子字串比對且區分大小寫，不會忽略或正規化標點；例如詞條「urgent」不會命中「Urgent」，全形逗號「，」也不等於半形逗號「,」。詞表命中可能誤報，也可能漏掉同義表達。沒有命中時，參考工具會顯示「詞表未命中，仍需人工審閱」；這不代表通過。顯示原句和周邊文字供人判讀，不把工具稱為法遵、資安或內容安全檢查。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">keyword-filter.html</div>
</div>
<div class="tool-body">
<div class="filter-layout">
<div class="keyword-area">
<div class="keyword-title">敏感詞清單（每行一個）</div>
<textarea class="kw-input" id="kw-list" placeholder="免費
限時
保證
最低價
點擊
轉發"></textarea>
<div style="font-size:.73rem;color:var(--c-muted);margin-top:6px;">共 <span id="kw-count">0</span> 個關鍵字</div>
</div>
<div class="content-area">
<div>
<div style="font-size:.73rem;color:var(--c-a1);letter-spacing:1px;font-weight:500;margin-bottom:6px;">待審查文字</div>
<textarea class="content-textarea" id="content-text" placeholder="將需要審查的文章或貼文內容貼入此處…"></textarea>
</div>
<button class="compose-btn" onclick="filterContent()">開始掃描 <span aria-hidden="true">→</span></button>
<div id="filter-result" style="display:none;">
<div style="font-size:.73rem;color:var(--c-muted);letter-spacing:1px;font-weight:500;margin-bottom:8px;">掃描結果 · 共找到 <span id="total-matches">0</span> 處</div>
<div class="highlight-result" id="highlight-output"></div>
<div class="match-stats" id="match-stats"></div>
</div>
<div id="filter-clean" style="display:none;padding:16px;background:rgba(181,112,58,.06);border:1px solid rgba(181,112,58,.28);border-radius:4px;font-size:.9rem;color:#765334;">詞表未命中，仍需人工審閱。</div>
</div>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">詞表掃描只找字串，不理解上下文、否定、同義詞或法規。命中代表需要人工查看，不命中也不代表通過審查。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「核准詞表文字初篩器」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
詞表掃描只找字串，不理解上下文、否定、同義詞或法規。命中代表需要人工查看，不命中也不代表通過審查。

【操作與輸出】
每行一個已核准詞，貼入待檢文字後執行掃描；逐字高亮命中並列出每個詞的次數和原文。無命中時顯示「詞表未命中，仍需人工審閱」，不可顯示審查通過。

【例外與安全】
空詞表或空文本提示補資料；特殊字元以字面詞處理；使用者文字安全呈現，命中標籤用 textContent 建立。比對使用大小寫敏感的逐字子字串，不做大小寫轉換或標點正規化；「urgent」不命中「Urgent」，「保密，確認」不命中「保密,確認」。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
詞表填「機密、待確認」，掃描「這是機密資料」「非機密公開資訊」並檢查原句；再掃描同義詞「保密」，確認精確比對可能漏報。貼入 &lt;script&gt;alert(1)&lt;/script&gt; 和沒有命中的乾淨文字；前者只作文字，後者仍提醒人工審閱。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>先定義本次可搜尋的詞表（機密、待確認），並把它理解為精確字串清單，而非法規或語意判斷。</li><li>在參考品逐句掃描「這是機密資料」「非機密公開資訊」及「保密」，查看每個命中位置和原文；記錄可能漏報。另以「urgent」為詞條，分別輸入「urgent」和「Urgent」；再比較「保密，確認」與「保密,確認」，核對大小寫敏感及標點逐字相同。</li><li>用完整提示詞生成並保存工具，重開後重跑同一批文字；另外貼入 &lt;script&gt; 標記和一段完全無命中的文字。</li><li>確認標記字串安全顯示、無命中仍要求人工審閱；若介面宣稱通過審查，移除該結論並重測。交付詞表版本、命中和人工覆核紀錄。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">不可將命中狀態寫成完成法規／資安審查；詞表須有負責人、來源和更新日期。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若高亮改變原文或輸入被當成標籤執行，停止使用並改以安全 DOM 文字節點顯示，再測含尖括號內容。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>詞表加入「機密、待確認」，測試「這是機密資料」與「非機密公開資訊」兩句；兩句都可能含字面命中，須展示完整原文供人工判讀。再測同義詞「保密」，確認可能漏報。加入「urgent／Urgent」和「保密，確認／保密,確認」測試大小寫與全半形標點，再加入 &lt;script&gt;alert(1)&lt;/script&gt; 和無命中的乾淨文字：標記只作文字，乾淨文字仍明示「詞表未命中，仍需人工審閱」。交付詞表版本、命中清單和人工覆核狀態，不標示法遵通過。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">保留命中依據與人工覆核狀態</h2><p class="body-text">交付詞表版本、命中位置與人工閱讀結果。沒有命中只表示本次字串規則沒找到詞，仍要讀上下文；詞表變更後重測大小寫、標點與無命中資料，不把初篩當成正式核准。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「用可替換字面詞表定位需要覆核文字」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E19/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E19/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E19/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>詞表=保密、urgent；原文「保密資料 urgent Urgent」。</td><td>命中保密與小寫urgent，大小寫差異依字面規則；提示人工覆核。</td></tr><tr><td>B</td><td>詞表改=確認；原文不變。</td><td>零命中但仍需人工覆核，不宣稱文字可發布。</td></tr><tr><td>例外</td><td colspan="2">空詞表/空原文提示；分隔符號方式依頁面說明；標記不能改掉原始內容。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e19-transfer-case">自訂詞彙文字初檢｜當次案例資料（可替換）

A
詞表=保密、urgent；原文「保密資料 urgent Urgent」。

B
詞表改=確認；原文不變。

例外
空詞表/空原文提示；分隔符號方式依頁面說明；標記不能改掉原始內容。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e19-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e19-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>

<!-- learner-content:end -->
