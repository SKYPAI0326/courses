---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-3
title: UTM 廣告連結管理員
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">需要為同一活動建立一致的追蹤網址時，使用這頁。 完成第三章後使用；準備原始網址與三個渠道的命名規則。</p><ol class="step-list"><li>先閱讀網址範例，辨認來源、媒介與活動名稱，再輸入網址組合工具。</li><li>逐一核對編碼與參數；開啟後仍能到達原始頁面。</li></ol></section><section class="lesson-section" id="example-start"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">行銷同事需要為三個來源渠道建立一致的追蹤網址。本單元依命名規則組出 UTM 參數；完成後核對原始網址、編碼與 source／medium／campaign，追蹤結果仍以實際分析平台為準。</p><p class="body-text">UTM 是網址上的來源、媒介與活動代碼。命名一致才能在分析報表中合併；工具可以檢查格式，不能保證分析平台已收到或正確歸因。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">utm-link-manager.html</div>
</div>
<div class="tool-body">
<div class="utm-grid">
<div class="utm-field" style="grid-column:1/-1;">
<div class="utm-label">基礎網址 (Base URL)</div>
<input class="utm-input" id="u-base" placeholder="https://example.com/landing-page"/>
</div>
<div class="utm-field">
<div class="utm-label">來源 utm_source</div>
<div class="utm-optional">例：google, facebook, email</div>
<input class="utm-input" id="u-source" placeholder="facebook"/>
</div>
<div class="utm-field">
<div class="utm-label">媒介 utm_medium</div>
<div class="utm-optional">例：cpc, social, newsletter</div>
<input class="utm-input" id="u-medium" placeholder="social"/>
</div>
<div class="utm-field" style="grid-column:1/-1;">
<div class="utm-label">活動名稱 utm_campaign</div>
<div class="utm-optional">例：summer_sale_2025</div>
<input class="utm-input" id="u-campaign" placeholder="summer_sale_2025"/>
</div>
<div class="utm-field" style="grid-column:1/-1;">
<div class="utm-label">內容識別 utm_content <span style="color:var(--c-muted);font-weight:400;">（選填）</span></div>
<input class="utm-input" id="u-content" placeholder="banner_top"/>
</div>
</div>
<button class="compose-btn" onclick="generateUTM()" style="margin:16px 0 0;">產生 UTM 連結 <span aria-hidden="true">→</span></button>
<div id="utm-result" style="display:none;margin-top:16px;">
<div style="font-size:.73rem;color:var(--c-muted);letter-spacing:1px;font-weight:500;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;"><span>產生的連結</span><button class="copy-btn" onclick="copyUTM()">複製連結</button></div>
<div id="utm-url" style="background:#2c2b28;color:#e8e4dc;font-family:'Courier New',monospace;font-size:.8rem;padding:14px 16px;border-radius:4px;word-break:break-all;line-height:1.6;"></div>
</div>
<div id="history-section" style="margin-top:28px;display:none;">
<div style="font-size:.73rem;color:var(--c-muted);letter-spacing:1px;font-weight:500;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;"><span>歷史記錄 · <span id="hist-count">0</span> 筆</span><button class="copy-btn" onclick="clearHistory()">清除全部</button></div>
<div style="background:var(--c-card);border:1px solid var(--c-border);border-radius:4px;overflow:hidden;overflow-x:auto;"><div class="table-scroll"><table class="history-table"><thead><tr><th>活動</th><th>來源</th><th>連結</th><th></th></tr></thead><tbody id="hist-body"></tbody></table></div></div>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">UTM 參數供分析系統分類流量；命名需一致且不得放個資。URL API 能保留既有參數並正確編碼，手動串接容易弄壞特殊字元或重複問號。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「UTM 廣告連結管理員」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
UTM 參數供分析系統分類流量；命名需一致且不得放個資。URL API 能保留既有參數並正確編碼，手動串接容易弄壞特殊字元或重複問號。

【操作與輸出】
輸入完整 HTTP／HTTPS 網址、source、campaign，medium 和 content 選填；使用 URL 與 searchParams 設定參數，顯示和複製結果，保留其他既有 query。可檢視、刪除最近本機歷史。

【例外與安全】
拒絕無效網址、javascript: 等非 HTTP(S) 協定；空白必填欄不生成；中英文和空格由 URL API 編碼。歷史只在本瀏覽器保存，使用文字節點顯示，禁止將客戶或個資寫入參數。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
使用 https://example.org/page?ref=mail，先建立 source=newsletter、medium=email、campaign=october_event，確認 ref 保留且參數不重複；再將 source 改為「電子報」、campaign 改為「秋季 活動」，解析網址確認中文字和空格往返一致。javascript:alert(1) 或缺 source 不得產生網址；刪除一筆歷史後其餘紀錄需保留。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>先決定 source、medium、campaign 的固定命名規則，避免同一渠道混用中英文；用帶既有 ref 參數的網址建立第一筆。</li><li>貼完整提示詞到 AI Studio Chat 生成工具，保存為 utm-manager-v1.html，重開後照命名規則重建網址。</li><li>查看生成網址解析後的每個參數：ref 保留、UTM 不重複、空格與中文往返一致；再測 javascript: 協定和缺少必填欄。</li><li>新增兩筆歷史後刪除其中一筆，確認另一筆保留；若結果錯誤，逐項檢查 URL API 輸入和參數設定，不手動改結果來掩蓋錯誤。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">網址可能含追蹤資訊；不要放個資。先在內部測試網址解析，再由行銷平台確認報表歸因。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若中文或 &amp; 符號解析錯誤，檢查 URL 編碼和重複參數，再用同一個 URL 測試解析值。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>先用 https://example.org/page?ref=mail 建立 source=newsletter、medium=email、campaign=october_event，核對既有 ref 保留且每個參數只出現一次。再將 source 改為「電子報」、campaign 改為「秋季 活動」，解析生成網址確認中文字和空格往返不變；測試 javascript:alert(1) 與缺少 source 均不得產生網址。刪除一筆歷史後確認其餘紀錄仍在。交付命名規則和可複製的網址清單；本機歷史不等於備份。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">交付可核對的追蹤網址與命名規則</h2><p class="body-text">保留命名規則及生成網址，解析參數確認中文字、原查詢與片段都正確。下一次新增渠道沿用命名方法；實際流量歸因還要到分析平台核對，網址產生不代表追蹤已生效。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「保留原網址並編碼追蹤參數」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E12/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E12/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E12/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>網址https://example.org/page?ref=mail#part；source=newsletter、medium=email、campaign=秋季 示範。</td><td>保留ref與#part；三個utm參數各一次，解碼後值與輸入相同。</td></tr><tr><td>B</td><td>網址https://example.org/page?utm_source=old&amp;x=1；source=新來源、medium=social、campaign=試用。</td><td>更新utm_source為新值，不重複附加；x=1保留。</td></tr><tr><td>例外</td><td colspan="2">拒絕javascript:和非http(s)網址；空必填參數指出欄位，不產生正常結果。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e12-transfer-case">UTM 連結組裝｜當次案例資料（可替換）

A
網址https://example.org/page?ref=mail#part；source=newsletter、medium=email、campaign=秋季 示範。

B
網址https://example.org/page?utm_source=old&amp;x=1；source=新來源、medium=social、campaign=試用。

例外
拒絕javascript:和非http(s)網址；空必填參數指出欄位，不產生正常結果。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e12-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e12-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>
<!-- learner-content:end -->
