---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-8
title: Markdown 轉專業報表樣式
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">主管已核准的 Markdown 月報要輸出成容易閱讀和列印的版面。本單元比較原文與渲染結果，尤其檢查標題、清單、連結和特殊字元；預覽正確後還需打開 PDF 核對實際分頁。</p><p class="body-text">Markdown 標記會轉成標題、清單和連結；特殊字元必須正確跳脫，避免文字變成可執行 HTML。預覽正確也不保證列印後分頁正確。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">markdown-to-report.html</div>
</div>
<div class="tool-body">
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
<div style="font-size:.73rem;color:var(--c-muted);">左側輸入 Markdown，右側即時預覽排版效果</div>
<button class="print-btn" onclick="window.print()">列印為 PDF</button>
</div>
<div class="md-layout">
<div>
<div class="md-panel-label">Markdown 輸入</div>
<textarea class="md-input" id="md-input" oninput="renderMd()" placeholder="# 五月份行政工作報告

## 一、摘要

本月公文如期結案率達 **96%**，重點工作如下：

- 完成第二季辦公用品採購請購
- 辦理新進人員教育訓練 2 場
- 會議室預約系統改版上線

## 二、下一步行動

1. 完成年中財產盤點規劃
2. 發送全體員工健檢通知
3. 提交會議室設備汰換簽呈"></textarea>
</div>
<div>
<div class="md-panel-label">預覽（可列印）</div>
<div class="md-output" id="md-output"><p style="color:var(--c-muted);font-size:.85rem;">在左側輸入 Markdown 後即時預覽…</p></div>
</div>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">Markdown 是輕量文字標記；只支援宣告過的語法才可預測結果。不可直接把原文當 HTML 插入，否則外部文字可能執行程式。列印後的分頁也要另行檢查。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「Markdown 轉可列印報表」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
Markdown 是輕量文字標記；只支援宣告過的語法才可預測結果。不可直接把原文當 HTML 插入，否則外部文字可能執行程式。列印後的分頁也要另行檢查。

【操作與輸出】
左側輸入 Markdown，右側即時預覽標題、粗體、斜體、清單、引用、行內程式碼和安全連結；提供列印／另存 PDF 操作說明。

【例外與安全】
先把輸入跳脫成文字，再只轉換白名單語法；連結僅允許 http／https，拒絕 javascript:。未知語法保持原文字，空內容顯示提示。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
輸入標題、兩個清單項目、粗體、連結及 &lt;script&gt;alert(1)&lt;/script&gt;；前五項按說明渲染，script 保持可見文字不執行。輸入 javascript: 連結須視為純文字；列印預覽檢查標題和清單沒有被切斷。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>準備一段已核准的 Markdown 片段，包含 # 標題、兩項清單、粗體、中文括號和有效網址；另加入 script 標記與 javascript: 連結作安全測試。</li><li>在參考品逐項比對原始 Markdown 和預覽：標題層級、清單順序、粗體、連結及特殊字元是否完整，script 與危險協定應保持安全文字。</li><li>貼完整提示詞生成轉換工具，保存為 markdown-report-v1.html，關閉後重新開啟並重跑同一片段；再使用列印預覽輸出 PDF，檢查標題、清單和表格換頁。</li><li>若漏字或文字被當作標籤執行，修正跳脫／轉換規則後重跑安全樣本；若 PDF 換頁截斷，調整版面並再次列印。交付來源 Markdown、HTML 預覽和核對後 PDF。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">只轉換已核准內容；列印後逐頁檢查換頁、網址、表格和特殊字元。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若特殊字元變成標籤或 script，先停止使用，修正為安全跳脫純文字後再測中文括號、&amp; 和網址。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>輸入含 # 標題、清單、粗體、中文括號與網址的月報片段，逐項對照 Markdown 原文和預覽；列印為 PDF 後檢查標題是否被截斷、表格是否超出頁面。發現漏字時修正轉換規則後重測，再交付 PDF 與來源檔。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">連同來源檔交付核對過的報表</h2><p class="body-text">對照原文、HTML 預覽與實際 PDF，核對漏字、特殊字元和分頁。交付時保留來源，日後改資料先重新轉換與列印檢查；螢幕預覽正確仍需確認實際輸出。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「把文字標記轉成可讀報告」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E17/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E17/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E17/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>原文「# 週報

**完成**

- 核對資料
- 保存工具」。</td><td>一級標題、粗體及兩項清單；原文可修改，列印預覽保留階層。</td></tr><tr><td>B</td><td>原文「## 下一步

&gt; 等待覆核

`code`」。</td><td>二級標題、引用和行內程式文字。</td></tr><tr><td>例外</td><td colspan="2">輸入&lt;script&gt;只顯示文字不能執行；不支援語法保留原文；PDF需另核對分頁。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e17-transfer-case">Markdown 報告預覽與列印｜當次案例資料（可替換）

A
原文「# 週報

**完成**

- 核對資料
- 保存工具」。

B
原文「## 下一步

&gt; 等待覆核

`code`」。

例外
輸入&lt;script&gt;只顯示文字不能執行；不支援語法保留原文；PDF需另核對分頁。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e17-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e17-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>

<!-- learner-content:end -->
