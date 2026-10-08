---
slug: gemini-ai
unit_id: SUPP-part5-PRAC5-4
title: 社群貼文多平台預覽器
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->

<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">社群小編要確認一段已核准文案在不同平台的換行和預覽。本單元把同一份文字放進多個預覽，避免逐一複製錯版；字數和平台限制會更新，發布前須到當前官方介面再核對。</p><p class="body-text">預覽是版面草圖，平台仍可能改變字數計算、連結卡片或裁切方式。頁面內建門檻預設為 120，供本課測試且可逐平台調整，不是官方限制；頁面以 JavaScript String.length 計算 UTF-16 code units，部分 Emoji 會占多個單位。發布前在平台當前介面核對。</p><p class="body-text"><strong>固定測試文案（請逐字貼入，兩行之間保留換行）：</strong></p><pre style="white-space:pre-wrap;background:var(--c-surface);padding:14px 16px;border-radius:4px;margin:-8px 0 20px;font-family:inherit;font-size:.88rem;line-height:1.8;">新品體驗活動開放報名！詳情：https://example.com/demo 😊
請於 10/10 前填表，名額有限。</pre><p class="body-text">用 JavaScript String.length 計算，這段含中間換行的文案共 60 個 UTF-16 code units；其中 😊 計為兩個單位。先操作下方參考品，觀察輸入如何變成結果，再用同一份固定文字驗收生成版。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">social-post-previewer.html</div>
</div>
<div class="tool-body">
<div class="platform-tabs">
<button class="ptab active" onclick="setPlatform('fb',this)">Facebook</button>
<button class="ptab" onclick="setPlatform('ig',this)">Instagram</button>
<button class="ptab" onclick="setPlatform('x',this)">X / Twitter</button>
</div>
<div class="preview-layout">
<div>
<div style="font-size:.73rem;color:var(--c-a1);letter-spacing:1px;font-weight:500;margin-bottom:8px;">撰寫貼文內容</div>
<textarea id="post-text" oninput="updatePreview()" placeholder="在此輸入你的貼文內容……" style="width:100%;min-height:180px;padding:12px 14px;border:1px solid var(--c-border);border-radius:4px;font-family:inherit;font-size:.9rem;background:var(--c-bg);resize:vertical;line-height:1.7;"></textarea>
<label for="example-limit" style="display:block;font-size:.78rem;margin-top:8px;">可調示例門檻（非平台官方限制）：<input id="example-limit" max="1000000" min="1" oninput="setExampleLimit(this.value)" step="1" style="width:100px;margin-left:6px;" type="number" value="120"/></label>
<div class="char-counter" id="char-count">0 / 120 個 JavaScript UTF-16 字元</div>
<div id="char-status" style="font-size:.78rem;margin-top:4px;color:var(--c-muted);">輸入文字後比較示例門檻；發布前請用平台編輯器確認。</div>
</div>
<div>
<div style="font-size:.73rem;color:var(--c-a1);letter-spacing:1px;font-weight:500;margin-bottom:8px;">預覽效果</div>
<div class="phone-frame">
<div class="phone-screen">
<div class="phone-header">
<div class="phone-avatar"></div>
<div><div class="phone-name" id="preview-name">弄一下工作室</div><div style="font-size:.68rem;color:#999;">剛剛</div></div>
</div>
<div class="phone-content" id="preview-content">在此輸入文字後即時預覽…</div>
</div>
</div>
</div>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">預覽只模擬排版和文字長度，不等同平台實際顯示。工具提供每個平台可單獨調整的 120 字元示例門檻，不稱為官方上限；計數採 JavaScript UTF-16 code units，不猜測網址或 Emoji 的平台折算。發布前以平台當前介面核對。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box" style="font-size:.8rem;">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「社群貼文多平台預覽器」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
預覽只模擬排版和文字長度，不等同平台實際顯示。工具提供每個平台可單獨調整的 示例門檻輸入欄，不稱為官方上限；計數採 JavaScript UTF-16 code units，不猜測網址或 Emoji 的平台折算。發布前以平台當前介面核對。

【操作與輸出】
同一文案可切換三種平台外觀，即時更新純文字預覽與 JavaScript String.length 計數；每個平台提供由使用者填入的非負整數示例門檻，未填時提示先設定 並清楚標示非官方限制。門檻調整後立即重算差值和狀態。

【例外與安全】
不要把示例數字描述為官方限制；空白文案顯示說明狀態。明確說明 JavaScript String.length 計算 UTF-16 code units，部分 Emoji 占多個單位；不猜測平台對網址、Emoji 的折算。文案只作文字呈現，低於示例門檻不得顯示為可發布。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次示例門檻：三個平台各120個UTF-16 code units，皆可修改，並非官方上限。

測試資料與檢查方式：
逐字輸入本頁固定兩行文案「新品體驗活動開放報名！詳情：https://example.com/demo 😊」及「請於 10/10 前填表，名額有限。」，兩行間保留換行；JavaScript String.length 預期為 60 個 UTF-16 code units。切換平台確認預覽一致且計數不變。三個平台初始門檻均為可編輯的 120 示意值，不能稱為平台上限；把 X 門檻從 20 調至 500，確認狀態隨之更新但不出現「可發布」結論。最後到平台當前編輯器核對。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>先逐字輸入上方固定測試文案，保留兩行間的換行；JavaScript String.length 預期為 60 個 UTF-16 code units，記下原文與計數。</li><li>在參考品逐一切換三種平台；每次檢查可調門檻欄初始為 120。把門檻改成 20，再輸入超過 20 個 UTF-16 code units 的文字，觀察示例警示；改成 500 後確認狀態更新且仍無發布通過宣稱。</li><li>貼上完整提示詞生成工具並保存、重開；用相同文案檢查預覽、字數和門檻，再修改一字並調高門檻觀察警示更新。</li><li>若字數不同，先確認是否按 UTF-16 code units 計數，再用平台正式編輯器核對網址、換行和媒體裁切，記錄頁面示意與平台實際結果差異。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">頁面字數和預覽可能落後平台現況，不得用作發布資格判定；以發布平台預覽為準。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若修改文字後預覽未更新，檢查 input 事件和平台分流，再以相同文案重測三個視圖。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>逐字輸入上方固定兩行文案並保留換行，計數應為 60 個 UTF-16 code units；切換三種平台確認預覽和計數一致。把 X 的示例門檻從 20 改為 500，確認差值和警示更新，且介面不表示「可發布」；修改一個字確認預覽即時更新。發布前回平台編輯器核對裁切、連結和媒體呈現。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">把預覽當作發布前的一次核對</h2><p class="body-text">留下原文、預覽及計數規則，指出換行與內容是否完整。發布前回到平台編輯器檢查裁切、連結與媒體；工具中的可調門檻只是你的檢查設定，不能自動代表平台允許發布。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「依輸入長度和可調門檻顯示預覽」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E13/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E13/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E13/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>文字A😊；將其中一種版型的提醒門檻設為2。</td><td>按JavaScript UTF-16計數長度3，顯示超過設定門檻；預覽保留完整內容。</td></tr><tr><td>B</td><td>同文字；門檻改為3。</td><td>長度3且未超過門檻，提醒同步改變。</td></tr><tr><td>例外</td><td colspan="2">不同平台門檻為使用者設定，不能宣稱等於平台正式發布限制；HTML當文字。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e13-transfer-case">社群文案版型預覽｜當次案例資料（可替換）

A
文字A😊；將其中一種版型的提醒門檻設為2。

B
同文字；門檻改為3。

例外
不同平台門檻為使用者設定，不能宣稱等於平台正式發布限制；HTML當文字。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e13-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e13-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>

<!-- learner-content:end -->
