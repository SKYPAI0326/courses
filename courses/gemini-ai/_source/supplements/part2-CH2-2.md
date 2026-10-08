---
slug: gemini-ai
unit_id: SUPP-part2-CH2-2
title: 排班規則：從工作條件到可檢查的排班表
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<main class="lesson-body"><section class="lesson-section" id="schedule-core-note"><h2 class="section-heading">核心案例的完整規格對照</h2><p class="body-text">第三章已完整教過排班工具的設計、生成與查核。本頁保留規格對照，方便回看硬性限制與平均分配偏好；初次製作請從<a href="../chapters/CH3.html">第三章完整流程</a>開始。</p></section><section class="lesson-section" id="schedule-1">
<h2 class="section-heading">情境：活動支援小組如何排出三天值勤</h2>
<p class="body-text">活動主管要安排週一至週三的前台值勤。每天有早班 09:00–13:00 和晚班 13:00–17:00，各需要一人。四位同事的可排日期不同；排錯會造成現場缺人，也可能讓同一人被排兩個重疊班次。</p>
<p class="body-text">這是「依條件挑選組合」的問題。先把條件分成兩類：硬性限制必須遵守，例如不可排日期、每班需要人數、每人最多兩班、同一天不能排兩班；偏好用來改善結果，例如工作量盡量平均。若硬性限制互相衝突，正確結果是指出未排滿的班次，不可把違規排班包裝成完成。</p>
<div class="callout info"><div aria-hidden="true" class="callout-icon">情境資料</div><div class="callout-body">安：週二不可排；柏：週三不可排；晴：週一不可排；明：三天皆可。每人最多兩班。每個時段都需要一位同事。</div></div>
</section>
<section class="lesson-section" id="schedule-2">
<h2 class="section-heading">先手排一份答案，確認規則沒有互相打架</h2>
<p class="body-text">先不要生成工具，自己試排一次。下表是一個符合條件的答案：週一早班安、晚班柏；週二早班晴、晚班明；週三早班安、晚班晴。班數分別是安 2、柏 1、晴 2、明 1，最多班數相差一班。</p>
<div class="prompt-wrap"><div class="prompt-label">一份有效排班例</div><pre class="result-box">             週一       週二       週三
早班 09–13     安         晴         安
晚班 13–17     柏         明         晴
個人班數       安 2       柏 1       晴 2       明 1</pre></div>
<p class="body-text">這只是可行答案之一，不要求生成器排出完全相同的順序。驗收時檢查每班是否有人、每人班數是否超過上限、不可排日期是否被遵守，以及同日是否有人重複值勤。</p>
</section>
<section class="lesson-section" id="schedule-3">
<h2 class="section-heading">把工作資料和判斷規則寫進完整提示詞</h2>
<p class="body-text">提示詞中的人員與日期是輸入；班次需求和上限是硬性規則；工作量平均是偏好；未滿班次清單是衝突回報。把這些分開寫，生成後才知道應該檢查哪個結果。</p>
<div class="prompt-wrap"><div class="prompt-label">可直接貼入 AI Studio Chat 的完整生成指令</div><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-policy-1">請製作一個繁體中文的排班規劃工具，讓使用者在網頁上輸入資料、設定規則、產生班表、檢查空缺並保存成果。工具處理使用者當次輸入的內容，初次開啟顯示空白表單，不預填任何人名、日期、班種或排班答案。

使用者能輸入什麼：
提供人員清單，可新增、刪除與修改姓名。
提供日期清單，可新增、刪除與修改日期或日期標籤；順序由使用者設定。
提供班種清單，可新增、刪除與修改班種名稱、開始及結束時間，以及每班需要的人數。
讓使用者勾選每位人員在哪些日期可以值班。可排代表該日各班種都能安排，但仍要遵守下面的規則。
人員、日期或班種改動後，可排表與班表欄位要同步更新，保留仍適用的資料，新增的可排日期先不勾選。

哪些規則能設定：
提供每人總班數上限，可由使用者設定零至目前日期數的整數，因為同一天最多一班；零表示本次所有人都不能排班。
同一人同一天最多安排一班，只能安排在勾選可排的日期，每班安排人數不得超過該班的需求人數。
先遵守以上規則並安排盡量多的班，再在安排人數相同的情況下，讓大家總班數盡量接近。請在畫面說明這個先後順序。
適用範圍限小型排班：一至八位人員、一至七個日期、一至四種班種，每班需要一至四人。超出範圍時明確提示並阻止計算，不省略人員、不截斷資料。

工具如何處理與呈現：
先檢查輸入，再依當次資料與設定排班。姓名或日期重複、必填欄位沒填、班種名稱重複、結束時間不晚於開始時間、人數或上限不正確時，指出問題並保留欄位供修正。
不能只試一次順序就說沒有可行安排。請在上述支援規模內找出最多可安排人次的班表，再依平均分配偏好選擇結果。不能為了排滿而違反限制。
結果列出日期、班種、時段、需要人數、已安排人員、缺額、每人總班數與已排／未排統計。缺人時保留空缺，說明受哪些限制影響，交由使用者調整條件。
任何輸入、設定或還原資料改變後，清除舊結果、停用班表下載與列印，提示重新產生。

資料與成果如何帶走：
提供「清空資料」「產生班表」「下載資料備份」「還原資料」「下載班表CSV」及列印。
清空資料前請使用者確認；下載備份要保存人員、日期、班種、可排條件與規則設定，副檔名用.json，格式由工具處理。還原時先檢查整份資料；失敗保留原輸入並說明原因，成功後先核對欄位，再由使用者重新產生班表。
CSV和列印包含班表、需求與缺額；中文與含逗號的文字要正確，輸入文字不得變成試算表公式。資料不自動保存，關閉或重新整理後回空白表單，畫面要提醒先下載備份。

交付與操作要求：
交付完整單一HTML檔，外觀與功能都在同一檔案；存檔後離線用瀏覽器開啟即可操作，使用時不再呼叫模型，不需要連線、金鑰或其他套件。
欄位、按鈕及錯誤提示要清楚，鍵盤能操作，手機也能閱讀；過寬表格只在自己的區域捲動。
請只回覆從&lt;!DOCTYPE html&gt;到&lt;/html&gt;的完整內容，不省略，不附其他說明。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-policy-1"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-policy-1-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

日期標籤為週一、週二、週三。每天有早班 09:00–13:00 與晚班 13:00–17:00，每班各需要 1 人。
人員：安、柏、晴、明。
不可排日期：安不可排週二；柏不可排週三；晴不可排週一；明沒有不可排日期。

本次共同上限：每人兩班；同日最多一班。標準資料應排滿六班；每人班數為兩、兩、一、一；換班表順序仍可，只要全部限制成立。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside></div>
</section>
<section class="lesson-section" id="schedule-4">
<h2 class="section-heading">操作、查核，再測一次無法排滿的情況</h2>
<ol class="body-text">
<li>在 AI Studio Chat／對話頁貼上完整指令，等待完整 HTML 輸出；確認有結尾標籤，另存為 schedule.html，再用瀏覽器打開。</li>
<li>按產生排班，逐格核對六個時段、每人班數、不可排日期與同日班次。記下預期與實際結果；順序不同但所有硬性規則都符合，也算有效。</li>
<li>修改資料：週三只讓安可排，其他三人都設為不可排。週三兩個班次不能由安一人兼任，因此必須明示其中一個班次未排滿；若工具安排安兼兩班，這筆測試不通過。</li>
<li><p class="body-text">出現不符合規則的結果時，先另記操作、實際結果與預期，再使用下方通用修復指令，保存修正版並重測。</p><pre class="prompt-box" data-policy-prompt="工具修復" id="prompt-schedule-inline-repair">請依原有排班規則修正違規結果。只安排在可排日期，同一人同日最多一班；無法滿足需求時保留空缺，列出受影響的日期、班種與原因，不放寬限制。依我另附的實際輸入與錯誤紀錄定位原因，不把本次人名、日期或答案寫成特例。保留可編輯輸入、規則設定與CSV匯出，交付完整修正版HTML。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-schedule-inline-repair" type="button">複製通用修復提示詞</button><span aria-live="polite" class="policy-status" id="prompt-schedule-inline-repair-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-schedule-inline-repair"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-schedule-inline-repair-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

當次錯誤紀錄：週三只剩安可排，卻安排安同日兩班；應留一班空缺。保存修正版後重跑可行與缺人兩組資料。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-schedule-inline-repair-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-schedule-inline-repair-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside></li>
</ol>
<div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>交付排班 HTML、當次案例資料的通過紀錄，以及無解案例中清楚列出的空缺。隨機看起來平均不代表符合條件；正式排班仍需主管核准。</div></div>
</section><section class="lesson-section" id="completion"><h2 class="section-heading">用規則解釋有效班表與空缺</h2><p class="body-text">這份規格對照用來辨認硬性限制與平均分配偏好。回看自己的班表時，先查可排日、同日一班及需求，再查分配；未排滿時保留空缺與原因。完整製作流程已整併在<a href="../chapters/CH3.html">第三章</a>。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></main>
<!-- learner-content:end -->
