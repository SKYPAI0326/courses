---
slug: gemini-ai
unit_id: SUPP-part2-PRAC2-3
title: 介面配色方案速查器
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">需要為工具選擇清楚可讀的配色時，使用這頁。 完成第二章後使用；準備一組品牌主色，或先用下方示例。</p><ol class="step-list"><li>先看色票參考品，再依範例生成主色、背景與強調色的預覽。</li><li>在文字與按鈕上檢查對比；換一組主色後仍要能辨認內容。</li></ol></section><section class="lesson-section" id="example-start"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">行銷同事需要為一個活動頁面配置主色、背景與強調色，避免文字看不清。本單元從一組品牌主色產出可檢查的色票；完成後以文字對比和實際元件預覽決定採用與否，不能把色票建議當作無障礙認證。</p><p class="body-text">色票工具把主色轉成背景、文字和強調色候選。色相協調不等於文字可讀；確認實際前景／背景對比，並在真實按鈕和長段文字上預覽。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">color-scheme-generator.html</div>
</div>
<div class="tool-body">
<div class="color-input-row">
<div class="color-picker-wrap">
<div class="color-swatch" id="swatch-preview" style="background:#b5703a;">
<input id="color-picker" oninput="onPickerChange()" type="color" value="#b5703a"/>
</div>
</div>
<input class="hex-input" id="hex-input" maxlength="7" oninput="onHexInput()" placeholder="#hex" type="text" value="#b5703a"/>
<select class="style-select" id="style-select">
<option value="muji">無印良品風（自然、簡約）</option>
<option value="pro">商務精煉風（沉穩、有力）</option>
<option value="fresh">清新現代風（明亮、輕盈）</option>
<option value="dark">深色質感風（厚重、精緻）</option>
</select>
<button class="gen-scheme-btn" onclick="generateScheme()">生成配色 <span aria-hidden="true">→</span></button>
</div>
<div class="scheme-result" id="scheme-result">
<div class="scheme-label">GENERATED COLOR SCHEME</div>
<div class="palette-row" id="palette-row"></div>
<div class="colors-detail" id="colors-detail"></div>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">色彩和諧只提供候選色，不能證明文字易讀或符合品牌規範。主色、背景、正文、邊框與強調色要放進真實元件預覽；正文和背景對比需另外檢查。</p><p class="body-text"><strong>實際檢查文字對比：</strong>打開 <a href="https://webaim.org/resources/contrastchecker/" rel="noopener" target="_blank">WebAIM Contrast Checker</a>，把介面中實際文字色 HEX 貼到 Foreground、其背後的底色貼到 Background，讀取對比比例與結果。WCAG 2.2 AA 一般文字需至少 4.5:1；大型文字至少 3:1。標準詳見 <a href="https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html" rel="noopener" target="_blank">W3C 對比度最低標準說明</a>。先用 #336699（文字）與 #FFFFFF（背景）檢查，再挑你生成色票中的正文／背景組合；標準未達時先調整其中一色並重測。檢查結果只適用於這一對顏色，仍需在實際按鈕和長段文字上預覽。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「介面配色方案速查器」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
色彩和諧只提供候選色，不能證明文字易讀或符合品牌規範。主色、背景、正文、邊框與強調色要放進真實元件預覽；正文和背景對比需另外檢查。

【操作與輸出】
提供原生色彩選擇器與 HEX 文字欄、風格選單、生成按鈕、五個用途明確的色票和按鈕／文字預覽。色票可複製色碼；顯示所選 HEX，不把生成結果稱為無障礙通過。

【例外與安全】
接受 #RRGGBB 格式並同步色彩選擇器；錯誤格式時提示且不覆蓋最近有效色。文字標籤說明色彩角色，不能只顯示色塊。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
以 #336699 生成商務配色，核對五種用途和按鈕預覽一致；貼入 #12GG00 應提示格式錯誤且不覆蓋舊色。把 #336699 貼入 WebAIM 的前景色、#FFFFFF 貼入背景色，確認比例達一般文字 4.5:1；再檢查生成色票的正文與背景，未達門檻就調色重測。標準採 WCAG 2.2 AA，結果只代表受測的色彩配對。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>先選一個需要介面配色的實際工作頁面，寫清楚背景、正文、主要按鈕、輔助資訊和警示的用途。</li><li>在參考品輸入 #336699，生成五個角色色；核對長句、按鈕預覽是否一致，並用上方 WebAIM 連結檢查實際正文色／背景色。</li><li>用完整提示詞生成工具，保存為 palette-v1.html，重開後重做案例；再輸入 #12GG00，確認錯誤提示且有效色不被覆蓋。</li><li>將預覽轉為灰階，再把正文色與背景色的 HEX 分別貼進 WebAIM 前景、背景欄；一般文字至少 4.5:1，大型文字至少 3:1。若低於門檻，調整一色後重測並在長句、按鈕預覽覆核；記錄比例、採用色碼和淘汰色碼。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">工具提供的色彩建議不是品牌核准，也不是無障礙認證；重要頁面要用對比檢查器和實際裝置覆核。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若文字難讀，先改前景或背景色其中一項並重算對比，不同時換多種風格。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>以 #336699 產生五種角色色，逐一核對色票、正文、背景和按鈕預覽使用同一組色碼；輸入 #12GG00 須提示格式錯誤並保留最近有效色。閱讀長句並轉看灰階，檢查文字易讀、狀態不只靠顏色辨別；另以對比度檢查器核對正文與背景。保存色碼和未採用理由，不把建議色視為品牌或無障礙認證。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">將配色選擇連到實際閱讀任務</h2><p class="body-text">保留選定方案及使用位置，再放到實際工具核對正文、按鈕與錯誤提示。若只看色票而未在畫面試用，還不能判斷讀者是否看得清楚；換風格時同樣保留文字或符號提示。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「把色碼套到實際文字、背景與按鈕」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E03/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E03/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E03/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>主色#336699；選一種畫面提供的配色方式。</td><td>HEX同步色彩選擇器，五種用途色票及元件預覽更新；不宣稱無障礙已通過。</td></tr><tr><td>B</td><td>主色#884422；改另一種配色方式。</td><td>色票/元件按新設定更新，複製所得為所選色碼。</td></tr><tr><td>例外</td><td colspan="2">輸入#GGGGGG須指出格式錯誤並保留最近有效色；不能只靠色塊傳達用途。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e03-transfer-case">介面配色與元件預覽｜當次案例資料（可替換）

A
主色#336699；選一種畫面提供的配色方式。

B
主色#884422；改另一種配色方式。

例外
輸入#GGGGGG須指出格式錯誤並保留最近有效色；不能只靠色塊傳達用途。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e03-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e03-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>
<!-- learner-content:end -->
