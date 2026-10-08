---
slug: gemini-ai
unit_id: SUPP-part6-PRAC6-1
title: 生成並驗證 AI 會議交辦表
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="core-1"><h2 class="section-heading">Build 描述與第一筆輸入</h2><p class="body-text">承辦人要從會議原文整理有效交辦，同時保留取消、提議與尚未確認的欄位。先完成<a href="CH6-1.html">原文判讀基準</a>，再用下方完整 Build 描述製作應用；當次逐字稿放到生成後的輸入框，生成描述與待處理資料分開。完成物是可重開的專案、原文、交辦資料及人工核對紀錄。</p><p class="body-text"><a download="" href="../assets/materials/prompt-meeting.txt">下載完整生成指令 TXT</a></p><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="result-box" data-policy-prompt="工具生成或修改" id="prompt-meeting">製作繁體中文的會議交辦確認表網頁應用，在 AI Studio Build 預覽可用。
使用者在應用的逐字稿輸入框貼文字，按整理。伺服器呼叫 Gemini 進行語意分析，不得以正則或關鍵字命中冒充模型。金鑰僅放伺服器端環境，不送到瀏覽器。輸出 JSON 並驗證欄位與語意；錯誤時保留原文和上一版已確認資料，清楚顯示失敗，允許重試。
有效待辦只收本次最後明確成立且未完成的交辦；提議、取消、已完成另列排除清單與理由。重複回報合併；後續更新責任人與期限取代舊值，但保留更新原文。
欄位：task_id、task、owner（未知null）、due_date（YYYY-MM-DD或未知null）、status、source_text（逐字引用）、uncertain_reason、confirmed（預設false）。task_id 需非空且在目前結果中唯一，例如 A-01、A-02；答案中的 ID 是格式示例，驗收時檢查非空與唯一，不要求模型生成相同字串。不要猜期限或責任人。缺任務、原文或無法解析的日期須標為待確認，不默認成功。使用者可修改欄位，查看原文，勾選人工確認；匯出CSV標明確認狀態，不得自動寄送。
空白輸入應停止整理；模型或網路失敗顯示失敗與重試，不輸出假結果。支援下載逐字稿、結果 JSON、交辦 CSV；提供重新匯入 JSON 功能，驗證後才覆蓋。確認與未知不等同，責任人/期限未定的資料即使已核對仍保留待確認原因。
畫面提供標準逐字稿按鈕但清楚標示示例；不要把預設範例硬編碼當作新文字的分析結果。使用可讀表格與手機表格容器。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。

請交付完整可運作的應用版本與操作說明，不省略輸入、模型呼叫、驗證、人工確認及匯出功能。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-meeting" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-meeting-policy-status" role="status"></span></div><h3 class="section-heading">讀懂規則再分析逐字稿</h3><p class="body-text">生成描述中的「不要猜期限或責任人」「逐字引用來源」「未確認時留空並說明原因」是避免編造的核心規則。AI 的表格即使看起來完整，也必須能回到原句核對。先讀 <a download="" href="../assets/materials/meeting-a.txt">逐字稿 A</a>，指出哪一句是提議、哪一項取消、哪筆期限未知；再執行後檢查這幾條規則是否生效。</p><p class="body-text">在逐字稿 B 中，責任人與期限會改變，另有一項未明確交辦的任務。先在驗收表寫出你的答案，再貼入應用；未提供的欄位應保留未知，不能沿用 A 的答案。若結果填了不存在的日期，修復提示詞的「不要猜」規則，保留 A/B 回歸測試。</p><ol class="body-text"><li>在 AI Studio Build 描述框貼完整指令，選網頁應用並開始生成。看到預覽後，確認有逐字稿輸入與整理按鈕。</li><li>下載 <a download="" href="../assets/materials/meeting-a.txt">逐字稿 A</a>，開啟 TXT，全選文字貼到「應用預覽內」的逐字稿輸入框，按整理。</li><li>核對是否有兩項有效交辦。若只完成描述表單但未貼逐字稿執行，這一步尚未完成。</li><li>查看林與陳的原文，確認林的期限與陳的未知；直播與取消邀請不能在有效待辦中。核對後才勾人工確認。</li></ol></section>
<section class="lesson-section" id="core-2"><h2 class="section-heading">新資料 B：需要重新判斷</h2><p class="body-text">下載 <a download="" href="../assets/materials/meeting-b.txt">逐字稿 B</a>。先寫出最後有效的任務、責任人、期限及排除原因，再貼到同一應用整理。這次會變更原有負責人與期限，不能只複製 A 的答案。</p><details><summary>完成預判後核對答案</summary><p class="body-text">三項有效待辦：陳／餐點詢價／2026-10-12；整理報名名單／負責人與期限待確認；王／海報／2026-10-13。場地已完成可放歷史，問卷只是提議，邀請仍取消。海報的林／2026-10-10 已被更新取代。</p></details><p class="body-text">完整欄位見 <a download="" href="../assets/materials/reference-answers.json">答案 JSON</a> 或 <a href="../assets/tools/meeting-reference.html" rel="noopener" target="_blank">可閱讀的答案頁</a> · <a download="" href="../assets/tools/meeting-reference.html">下載 HTML 參考檔</a>。措辭可以不同，但任務意思、原文、責任人、日期與未知狀態都要符合。</p></section>
<section class="lesson-section" id="core-3"><h2 class="section-heading">修復並重跑，不能改成固定答案</h2><p class="body-text">出現不符合規則的結果時，先另記操作、實際結果與預期，再使用下方通用修復指令，保存修正版並重測。</p><pre class="prompt-box" data-policy-prompt="工具修復" id="prompt-meeting-repair">請修正會議交辦工具的判讀規則：辨識原文最後明確成立的決議；提議、取消與已完成另列排除理由；後續明確更新的責任人及期限取代舊值，並保留支持判斷的原句。不把另附逐字稿中的人名、任務或答案硬編碼。保留未知狀態、人工確認、模型失敗提示與匯出功能，交付完整可運作版本，讓我用原測試及另一份不同逐字稿重測。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-meeting-repair" type="button">複製通用修復提示詞</button><span aria-live="polite" class="policy-status" id="prompt-meeting-repair-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-meeting-repair"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-meeting-repair-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

當次錯誤紀錄：逐字稿A已取消的邀請被列成有效待辦；B海報責任人未採用最後更新。修正後重跑A與B並記錄。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-meeting-repair-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-meeting-repair-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside><p class="body-text">空白輸入應停止；呼叫失敗應顯示失敗與重試，不能輸出空表當成功。權限、額度或連線限制時，保存逐字稿與畫面，把 AI 生成／呼叫記為待完成；使用答案頁練查核，不宣稱模型成功。</p></section>
<section class="lesson-section" id="core-4"><h2 class="section-heading">把交辦表交付給人</h2><ol class="body-text"><li>下載交辦 CSV、結果 JSON 與逐字稿。CSV 中應看得到待確認原因與人工確認狀態；task_id 要非空且唯一，ID 字串可不同於答案示例。</li><li>重新載入 JSON，核對資料沒有少列；匯入無效 JSON 應保留原資料並提示。</li><li>記下 Build 專案標題與網址，將專案頁加入瀏覽器書籤並用標題命名。關閉專案分頁後點書籤，確認同一標題、程式與預覽重新出現，再貼 A 執行一次。若未回到同一專案，依當下畫面找同名專案；仍找不到時保存網址、標題和登入／權限狀態並標記平台重開待完成，不以 Share／ZIP 代替。</li><li>記錄 B 的三項結果與排除項，保存完整生成描述與修復指令。完成後回補充目錄選擇後續用途；公開 Share／Publish 不屬於此步通過條件。</li></ol></section><section class="lesson-section" id="completion"><h2 class="section-heading">交付來源、待確認事項與可重開入口</h2><p class="body-text">保存逐字稿、交辦結果、人工確認狀態及 Build 專案入口，重開後再用原文核對。語意判斷需要模型且可能誤讀；你要交付能追溯的草稿與待確認原因，不把完整表格當成已核准交辦。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></div>
<!-- learner-content:end -->
