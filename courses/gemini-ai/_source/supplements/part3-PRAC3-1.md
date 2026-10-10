---
slug: gemini-ai
unit_id: SUPP-part3-PRAC3-1
title: 技能評估雷達圖
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">想比較不同技能的練習進度時，使用這頁製作雷達圖。 先準備下方 1–5 分評分規準和各項分數的依據。</p><ol class="step-list"><li>先讀評分範例，確認每個分數代表什麼，再輸入圖表資料。</li><li>圖上分數能對回原資料；每項都有證據，不用面積直接判斷能力。</li></ol></section><section class="lesson-section" id="example-start"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">訓練主管想比較學員在不同技能上的練習進度。本單元用同一把 1–5 分規準建立雷達圖；完成物含每個分數的證據，不把圖形面積或總分當作員工能力結論。</p><p class="body-text">雷達圖把各維度分數換成方向與半徑，方便看出強弱分布。技能是不同面向，圖形面積不是總能力；每個分數必須能回到一條可觀察的行為證據。</p><p class="body-text"><strong>共用行為錨點與案例：</strong>文件整理：1 分＝檔案散亂、無法說明命名；3 分＝依分類歸檔但偶有漏項；5 分＝命名一致且能快速找到最新版。資料分析：1 分＝照抄數字、未核來源；3 分＝公式正確但漏檢空值；5 分＝核對來源、公式並說明異常。口頭簡報：1 分＝只讀數字、說不出原因；3 分＝先講結論並列一項證據；5 分＝結論、證據與不確定性都清楚且能回答追問。固定虛構學員評分為文件整理 5、資料分析 3、口頭簡報 1；各分數分別記錄「找到最新版不到 30 秒」、「公式正確但未檢查空值」、「只念數字且說不出變動原因」。2、4 分可用於兩錨點之間，必須附觀察證據和理由。</p><p class="body-text">先操作參考品輸入上方三項固定評分，確認名稱和數字出現在同一頂點；再按更新重畫。生成自己的版本時也用同組資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">skill-radar-chart.html</div>
</div>
<div class="tool-body">
<div class="radar-layout">
<div>
<div style="font-size:.73rem;color:var(--c-muted);letter-spacing:1px;font-weight:500;margin-bottom:10px;">技能名稱 ／ 分數（1–5）</div>
<div class="radar-inputs" id="radar-inputs"></div>
<button class="radar-add-btn" onclick="addRadarRow()">＋ 新增技能</button>
<button class="radar-gen-btn" onclick="renderRadar()">更新雷達圖 <span aria-hidden="true">→</span></button>
</div>
<div class="radar-svg-wrap" id="radar-svg-wrap">
<svg height="300" id="radar-svg" viewbox="0 0 300 300" width="300"></svg>
</div>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">雷達圖適合展示同一對象在多個共同尺度上的概況，不適合拿不同尺度或未定義的分數做排名。圖形面積容易誇大差距，讀者仍要看到分數與尺度說明。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「技能評估雷達圖」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
雷達圖適合展示同一對象在多個共同尺度上的概況，不適合拿不同尺度或未定義的分數做排名。圖形面積容易誇大差距，讀者仍要看到分數與尺度說明。


【尺度設定】
提供每個技能名稱對應的行為錨點與觀察證據欄，可修改。所有維度共用1–5分尺度；使用者須先定義尺度再評分，工具不由技能名稱猜測評分標準。

【操作與輸出】
可輸入 3 至 8 個技能名稱及 1 至 5 的整數分數，動態新增／刪除，按更新後繪製內嵌 SVG；固定顯示名稱、數值和 1–5 刻度。

【例外與安全】
少於 3 個維度、多於 8 個、重複名稱、空名稱、非整數或不在 1–5 時指出問題，不靜默改值。文字標籤以純文字呈現；圖表外提供同一份數值清單。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次行為錨點：
文件整理：1＝檔案散亂無法說明命名；3＝依分類歸檔但偶有漏項；5＝命名一致且能快速找到最新版。資料分析：1＝照抄數字、未核來源；3＝公式正確但漏檢空值；5＝核對來源、公式並說明異常。口頭簡報：1＝只讀數字、說不出原因；3＝先講結論並列一項證據；5＝結論、證據和不確定性清楚且能回答追問。中間分數須附觀察證據與理由。

測試資料與檢查方式：
使用虛構學員「文件整理 5、資料分析 3、口頭簡報 1」生成雷達圖，核對標籤、數值與 1–5 刻度，並把分數連回固定行為錨點。另測只剩兩個維度、加入到八個維度及嘗試第九個維度；輸入空名稱、重複名稱、6 和文字都應明確提示，不得靜默改值。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>先閱讀頁面提供的三組 1／3／5 行為錨點與逐項證據；在參考品輸入文件整理 5、資料分析 3、口頭簡報 1，確認標籤和數值對應。</li><li>複製完整提示詞到 AI Studio Chat，生成單檔 HTML；保存為 skill-radar-v1.html，關閉後重新開啟。</li><li>用 5、3、1 測試生成版，再把維度減至 2、增加至 8 和嘗試第 9 項；另測空名稱、重複名稱、文字與 6 分。</li><li>若圖形標籤或數值不符，依輸入表逐項定位修正並重測；另附分數證據表，說明尺度僅供回顧，不產生人事排名。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">使用虛構或已授權的評分資料；不要把雷達圖面積或平均分當作唯一人事結論。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若標籤對不上分數，先核對技能順序與 SVG 頂點，再重畫並比對原始數值。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>以固定虛構學員的文件整理 5、資料分析 3、口頭簡報 1 生成雷達圖，核對三個標籤、1–5 刻度與原始數值；依頁面錨點附上三條證據。刪至兩項須提示不足，八項可繪圖，第九項不可新增，輸入 6 或文字須提示。圖表供討論，不用面積或平均分單獨判定能力。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">保留評估依據，讓雷達圖可被解讀</h2><p class="body-text">雷達圖呈現各維度的比較，但每個分數仍需要共同定義與評估依據。保留維度、輸入資料及圖表；調整量尺或維度後重新核對，避免把不同標準的面積直接比較。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「以同尺度呈現多個評分軸」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E07/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E07/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E07/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>三軸溝通5、規劃3、整理1；共同尺度1至5。</td><td>三軸值依序5/3/1，圖表與表格一致。</td></tr><tr><td>B</td><td>四軸品質2、時效2、協作4、記錄5；尺度仍1至5。</td><td>四軸與新標籤同步；兩個2等距，不延用原三軸。</td></tr><tr><td>例外</td><td colspan="2">輸入6或重複軸名須提示；圖形面積不當作績效總分。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e07-transfer-case">多維度雷達圖｜當次案例資料（可替換）

A
三軸溝通5、規劃3、整理1；共同尺度1至5。

B
四軸品質2、時效2、協作4、記錄5；尺度仍1至5。

例外
輸入6或重複軸名須提示；圖形面積不當作績效總分。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e07-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e07-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>
<!-- learner-content:end -->
