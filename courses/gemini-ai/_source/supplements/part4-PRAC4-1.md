---
slug: gemini-ai
unit_id: SUPP-part4-PRAC4-1
title: 工具上線前部署清單
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">同事要試用一個由 AI 生成的單頁工具，交付前需要確認功能、資料邊界、手機可用性和版本。本單元用具體證據逐項做 preflight；打勾本身不證明安全或部署成功，需附實際測試結果。</p><p class="body-text">頁內參考品只是一個 16 項勾選計數器，沒有證據欄，也沒有不適用狀態；全勾只代表按過 16 項。正式測試另在筆記或表格建立紀錄：項目｜操作｜預期｜實際｜證據位置｜狀態。不適用須寫理由，失敗須留待修正。</p><p class="body-text">先操作下方參考品，觀察輸入如何變成結果。它用來熟悉流程；你後續生成的版本仍要獨立保存並按驗收資料測試。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">deployment-checklist.html</div>
</div>
<div class="tool-body">
<div class="checklist-header">
<div class="checklist-title">工具部署前確認清單</div>
<div class="checklist-progress" id="ck-progress">0 / 16</div>
</div>
<div class="checklist-prog-bg"><div class="checklist-prog-fill" id="ck-fill" style="width:0%"></div></div>
<div id="checklist-body"></div>
<button class="reset-btn" onclick="resetChecklist()">↺ 重置所有項目</button>
<div class="done-banner" id="done-banner">16 項均已勾選；仍須人工覆核測試證據、權限與部署條件。</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">清單是決策輔助，不會替你測出功能、安全或權限。每一項都要附實際證據；勾選只表示目前檢查通過，不代表平台替工具背書。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「工具上線前部署清單」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
生成版要具備逐項狀態、證據欄和人工覆核提示；頁內參考品只顯示勾選數量，沒有證據欄或不適用狀態，不能拿它當發布判定。完整紀錄仍不等於安全認證。

【操作與輸出】
依功能與資料、相容性、使用體驗、權限／部署四類呈現核對項目；生成版每項可記錄待檢查／已測有證據／不適用（須填理由），並有操作、預期、實際和證據位置欄；參考品仍只計勾選數量。顯示未完成數量，提供重設。

【例外與安全】
生成版初始全部待檢查；已測狀態須有實際證據，不適用必須填理由；有未完成或無證據項目時顯示「仍待處理」。全部有紀錄後也只顯示「項目已記錄，須人工覆核」，不得推論可發布、可分享或安全通過。重設前確認。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

測試資料與檢查方式：
用課程計時器測試重開、手機操作、無效輸入、資料保存及分享權限；每項要記操作、預期、實際、證據位置與狀態。漏一項或不適用沒有理由時仍待處理；重設後所有狀態回待檢查。即使全部有紀錄，也只提示人工覆核。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>選課程計時器作為受測工具；先重開檔案、調窄至手機寬度，再輸入空值與無效值，逐項記錄操作、預期及實際結果。</li><li>用參考清單逐項勾選，觀察它只更新 0／16 計數；另外在筆記或試算表按「項目｜操作｜預期｜實際｜證據位置｜狀態」記錄五項測試。勾選計數不會保存這些證據。</li><li>在外部紀錄表將一項列為不適用，先不寫理由並保持待補，再補上與課程計時器相關的理由。這個參考計數器沒有不適用欄，故不在此測試；生成版要阻止空白理由。</li><li>貼上完整提示詞生成個人清單，保存並重開後重複同一測試；若沒有證據卻顯示全部完成，修正彙總規則並重測。清單是檢查紀錄，不是安全或部署認證。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">只在獲准的測試環境檢查權限；公開部署、個資和 API 金鑰需另按組織規則核對。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若測試失敗，記錄具體輸入與觀察，修復後重測該項及受影響功能；保留未通過狀態。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>在外部紀錄表分別記錄課程計時器重新開啟、手機寬度、無效輸入、資料保存及分享權限的操作、預期、實際、證據位置與狀態。參考品只驗收勾選計數和重設，不把它當證據欄；生成版清單須阻止空白的不適用理由，並在全數有紀錄後仍提醒人工覆核。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">依部署證據判斷能否交付</h2><p class="body-text">完成清單後，區分已測項目與尚未取得的證據；有缺口就保留未部署狀態。實際部署時按使用環境重新確認帳號、資料位置、費用與撤回方式，不能用勾選取代操作結果。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></div>
<!-- learner-content:end -->
