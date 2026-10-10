---
slug: gemini-ai
unit_id: SUPP-part1-PRAC1-3
title: 會議情境指令模板產生器
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">經常整理同類會議，希望下次只需換資料時，使用這頁。 完成第二章後使用；準備下方會議範例與自己的輸出需求。</p><ol class="step-list"><li>先看範例如何把固定規則與可替換欄位分開，再填入模板產生器。</li><li>換一份會議資料測試；模板仍能使用，日期、責任人與決議都要核對。</li></ol></section><section class="lesson-section" id="example-start"><h2 class="section-heading">情境與參考工具</h2><p class="body-text">行政人員每週要把不同會議整理成通知或交辦摘要，重複輸入背景容易漏欄位。本單元做一份可替換欄位的會議指令模板；輸出仍是待核對的草稿，日期、責任人和決議必須回到來源確認。</p><p class="body-text">固定規則放在提示詞，會議類型、日期和對象是每次替換的變數。原文沒有地點或期限時要保留空白或待確認，不可為了讓範本完整而補寫。</p><p class="body-text"><strong>固定測試逐字稿（虛構）</strong><br/>主持人：下週四下午辦產品說明會，地點待確認。<br/>小林：先整理 10 頁簡報提綱。<br/>阿凱：預算等收到報價再決定。<br/>雯姊：會後通知業務與客服，通知時間尚未決定。</p><p class="body-text"><strong>核對答案：</strong>可以整理出下週四下午、簡報提綱由小林處理、預算待報價、會後通知業務與客服；地點、通知期限與精確日期都未提供，應標「待確認」，不可自行補寫。</p><p class="body-text">這份逐字稿刻意沒有精確日期、地點和通知期限，供你測模板能否保留未知資料；「下週四下午」也不能在缺少會議日期時換算成日曆日期。</p><p class="body-text">先操作參考品生成模板，再把完整模板與逐字稿一併貼入 Gemini，核對輸出。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label">meeting-prompt-generator.html</div>
</div>
<div class="tool-body">
<div class="gen-form">
<div class="gen-row">
<div class="gen-field">
<div class="field-label">會議類型</div>
<select class="gen-select" id="g-type">
<option value="客戶提案">客戶提案會議</option>
<option value="內部週會">內部週會</option>
<option value="跨部門協調">跨部門協調會</option>
<option value="行政協調">行政協調會議</option>
<option value="活動籌備">活動籌備會議</option>
<option value="腦力激盪">腦力激盪工作坊</option>
<option value="專案檢討">專案成果檢討會</option>
<option value="一對一面談">一對一主管面談</option>
</select>
</div>
<div class="gen-field">
<div class="field-label">會議目的</div>
<input class="gen-input" id="g-goal" placeholder="例：整理產品說明會決議與後續事項" type="text"/>
</div>
</div>
<div class="gen-row">
<div class="gen-field">
<div class="field-label">與會人員</div>
<input class="gen-input" id="g-attendee" placeholder="例：總務、人事、會計、單位主管" type="text"/>
</div>
<div class="gen-field">
<div class="field-label">輸出格式偏好</div>
<select class="gen-select" id="g-format">
<option value="條列式重點摘要">條列式重點摘要</option>
<option value="表格式行動清單（含負責人與截止日）">表格式行動清單</option>
<option value="段落式會議記錄">段落式會議記錄</option>
<option value="決議事項清單">決議事項清單</option>
</select>
</div>
</div>
<div class="gen-row">
<div class="gen-field">
<div class="field-label">語氣要求</div>
<select class="gen-select" id="g-tone">
<option value="正式、精準">正式、精準</option>
<option value="簡潔、直接">簡潔、直接</option>
<option value="友善、易讀">友善、易讀</option>
</select>
</div>
<div class="gen-field">
<div class="field-label">字數上限</div>
<select class="gen-select" id="g-length">
<option value="300 字以內">300 字以內</option>
<option value="500 字以內">500 字以內</option>
<option value="不限字數，盡量完整">不限字數，完整呈現</option>
</select>
</div>
</div>
</div>
<button class="gen-btn" onclick="generateTemplate()">產生 AI 指令模板 <span aria-hidden="true">→</span></button>
<div class="template-result" id="template-result">
<div class="template-label" style="margin-top:20px;">
<span>GENERATED PROMPT TEMPLATE</span>
<button class="copy-btn" onclick="copyTemplate()">複製</button>
</div>
<div class="template-box" id="template-box"></div>
</div>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">觀念與完整提示詞</h2><p class="body-text">固定要求放在提示詞模板，會議目的和參與者是每次變動的資料。角色可依情境選擇，但不能因「行政會議」之類的標籤就補出原文沒有的決議、人名或期限。</p><div class="tool-wrap">
<div class="tool-topbar">
<div class="tool-dot tool-dot-r"></div>
<div class="tool-dot tool-dot-y"></div>
<div class="tool-dot tool-dot-g"></div>
<div class="tool-label"><span aria-hidden="true">→</span> 複製這段 Prompt 貼入 Gemini</div>
</div>
<div class="tool-body" style="padding:24px 28px;">
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><div class="result-box" data-policy-prompt="工具生成或修改" id="instruction-box">你是一位重視初學者可操作性、資料安全與無障礙的前端工程師。請為工作者製作「會議情境指令模板產生器」，目標是把以下工作需求與工具結構變成可反覆使用、可核對的工具。交付完整單檔 HTML，CSS 與 JavaScript 內嵌，不呼叫外部 API；不要只輸出線框、示意圖或片段。

【工作情境】
固定要求放在提示詞模板，會議目的和參與者是每次變動的資料。角色可依情境選擇，但不能因「行政會議」之類的標籤就補出原文沒有的決議、人名或期限。

【操作與輸出】
提供可新增、修改和刪除的情境選項，每項由使用者設定對應角色；選擇不同情境時使用該項角色，不內建特定行業名單。輸入任務目的（必填），可輸入相關人員，並選擇條列／表格／段落、語氣和字數。依情境帶入對應角色，再產生可編輯、可複製的完整提示詞。

【例外與安全】
任務目的空白時說明並保留其他輸入；沒有與會人員或期限時用待補欄位，不自行創造。選擇不同情境須同步更換角色，不可只改標籤。


【交付要求】
頁面文字使用繁體中文；主要操作有清楚標籤、空狀態、錯誤提示和鍵盤可操作方式。輸入內容以純文字呈現。完成後輸出可直接保存並於瀏覽器重新開啟的完整 HTML 原始碼，附上如何填入資料、核對正常結果及測試例外的簡短說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</div><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="instruction-box-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="instruction-box"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="instruction-box-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次情境選項：客戶提案、內部週會、跨部門協調、行政協調、活動籌備、腦力激盪、專案檢討、一對一面談；每個選項附對應角色，仍可增刪或修改。

測試資料與檢查方式：
以固定逐字稿生成會議整理模板：會議時間保留「下週四下午」，地點、精確日期和通知期限標待確認；簡報提綱由小林整理，預算等報價。若模型補出地點或期限，視為失敗並修正提示詞。清空目的應阻止生成；切到一對一面談時，確認角色與任務同步改變。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="instruction-box-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="instruction-box-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
</div></section><hr class="section-rule"/><section class="lesson-section"><h2 class="section-heading">操作、驗收與修復</h2><ol class="body-text"><li>在參考品選「活動籌備」，填「整理產品說明會決議與後續事項」，在與會人員欄填「總務、人事、會計」，選表格、正式語氣和 300 字限制；產生後確認工具依「活動籌備」自動帶入角色，不需另選角色；把頁面提供的固定逐字稿當作生成版輸入。</li><li>生成模板後逐段確認目的、角色、格式和缺資料時待補的規則；清空目的重試，確認工具阻止生成且沒有清掉其餘設定。</li><li>將模板提示詞和固定逐字稿貼入同一 Gemini 對話；核對地點、精確日期、通知期限皆標待確認，原文中的小林、預算待報價與通知對象則保留。再把情境切到「一對一面談」，確認角色與任務隨之更新。</li><li>若未提供欄位被補寫，修改固定限制為「未知資料標待確認」，用同一假資料重測；保存活動籌備和面談兩版模板及結果。</li></ol><div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">通知和摘要需由人核對日期、姓名、地點與決議；未確認資訊不得自動寄送。</div></div><div class="callout info"><div aria-hidden="true" class="callout-icon">修復</div><div class="callout-body">若模板把空白補成推測內容，要求保留未提供欄位為待確認，並重跑同一會議案例。</div></div><div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>選「活動籌備」情境，目的填「整理產品說明會決議與後續事項」，在與會人員欄填「總務、人事、會計」，選表格、正式語氣和 300 字；確認工具依情境自動帶入角色，不需另選角色。用固定逐字稿試跑，確認時間保留「下週四下午」，地點、精確日期與通知期限標待確認；保留小林整理簡報、預算待報價和通知對象，不可補造。清空目的不得生成。再切換「一對一面談」，確認角色與任務同步改變。保存兩種情境模板和一份已核對示例。</div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">保存模板，也保存需要人工確認的欄位</h2><p class="body-text">完成後留下不同會議情境的模板與一份核對過的輸出。下次使用先更新會議資料，將未提供的日期、地點與期限保留待確認；模板降低重複輸入，原文仍是事實來源。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></div>
<!-- learner-content:end -->
