---
slug: gemini-ai
unit_id: SUPP-part4-SUPP4-3
title: 補充：預算、KPI 與會議改造
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="core-1"><h2 class="section-heading">選一個改造，不以工具數量評分</h2><p class="body-text">三條路都要改一項原工具沒有的行為，先保存舊版和原始測試結果，再選一條。預算路線下載 <a download="" href="../assets/materials/budget-transfer.csv">新的活動資料</a>，核定改 25,000，新增「餘額低於核定預算 10%」提醒。KPI 路線使用既有 <a download="" href="../assets/materials/kpi-normal.csv">三項 KPI 資料</a>，新增「未達標且不利差距至少 20% 時標為優先處理」：higher 的不利差距=(target−actual)/target；lower 的不利差距=(actual−target)/target；只在 target&gt;0 時計算。AI 交辦路線下載 <a download="" href="../assets/materials/meeting-c.txt">新逐字稿 C</a> 、<a download="" href="../assets/materials/prompt-meeting.txt">基礎生成指令</a>與 <a download="" href="../assets/materials/prompt-solo-meeting.txt">欄位變更指令</a>，新增依據明確原文填寫前置任務 depends_on，未明確提及時留空。每條路都需保留原功能並用提供的答案核對新規則。行政案件追蹤仍可作之後的延伸，但不代替本次新規則驗收。</p><p class="body-text">用需求單寫「工作用途、改了什麼、預期變化、例外、交付對象」。計時器可用現成品控制課堂節奏；做計時器不等於完成這個工作挑戰。</p><p class="body-text">預算範例：核定 25,000 時，餘額 3,700 不提醒；講師實支改成 11,200 後，實支 23,000、差異 2,400、餘額 2,000，應提醒低餘額。</p></section>
<section class="lesson-section" id="core-2"><h2 class="section-heading">獨立做一次可追溯的修改</h2><ol class="body-text"><li>先保存舊版工具、原始資料與原測試紀錄。寫下新增規則、預期答案與一項例外。</li><li>依所選路線修改指令並保存 v2；先重跑原測試確認沒有退步，再跑變更資料核對差異。</li><li>若結果不同，記錄實際現象，修正需求或生成結果，再跑受影響測試。例外輸入修好後，正常功能仍要可用。</li><li>輸出可再次使用的成品、完整指令、驗收表與 README，關閉後重新開啟再測。</li></ol><details><summary>完成預判後核對答案</summary><p class="body-text">預算：新資料估算 20,600、實支 21,300、差異 +700、餘額 3,700；低於10%提醒關閉。講師實支改 11,200 後餘額 2,000，提醒開啟。KPI：處理時間 5 天、目標 3 天、方向 lower，未達標；不利差距為 66.7%，應標優先處理。改成 2 天後達標並移除優先提示；target=0 時不得除以零或錯報提醒。AI：C 有兩項待辦；「品牌定稿」無前置任務，「安排印刷」depends_on「品牌定稿」，日期和來源句須吻合逐字稿。未提到前置關係的 A/B 任務須為空。</p></details><div class="prompt-wrap"><div class="prompt-label">改造提示詞骨架｜配合所選路線的資料與指令檔</div><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-policy-1">請基於目前可用版本修改工具，新增我另附的新規則，並把其中會變動的門檻、類別或選項做成可調設定。保留原有欄位、計算方式與輸出；不要寫死當次資料或答案。原始測試仍須通過，再用另附新資料檢查新增規則。對空值、零目標或原文未提及的資訊不得猜測。說明修改位置，輸出完整可再次使用的版本。完成後由我依獨立測試紀錄驗收，未通過時保留舊版。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-policy-1"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-policy-1-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

新規則：〔說明觸發條件、處理方式及需要可調的設定〕
當次資料：〔另貼資料或逐字稿〕
核對紀錄：〔列出測試操作、預期與理由；不把答案編入程式〕</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside></div><p class="body-text">三條路已各有完整素材檔：預算、KPI、會議交辦。選一條即可；先保存舊版和原測試，再複製該路線的基礎指令及變更指令，先貼可重用結構；新規則、當次資料與核對紀錄放在下方附加區，會議擴充案例另見 <a download="" href="../assets/materials/prompt-solo-meeting-case.txt">案例與核對 TXT</a>。不要把不同案例的答案混在同一份驗收紀錄。</p></section>
<section class="lesson-section" id="core-3"><h2 class="section-heading">完課驗收：用證據確認</h2><p class="body-text">檢查五件成果：① 可重開的工具或 AI 專案；② 已知答案的輸入與實測結果；③ 一項有效需求變更及再測；④ 可閱讀的交付物；⑤ 保存完整指令與使用說明。說明一個工作判斷，例如超支、指標方向或未定期限。</p><p class="body-text">保存所選案例的生成、修改與重開紀錄；缺少模型呼叫或其他證據時記為待完成。要繼續選用其他案例，回<a href="../index.html#supplement-reuse">改造與保存補充目錄</a>，先確認新的輸入、規則和核對方法。</p></section><section class="lesson-section" id="completion"><h2 class="section-heading">保留改造前後的用途與測試紀錄</h2><p class="body-text">選定案例後，留下原版、新規則、修改版與新舊測試結果。不同案例的處理方式不同，不能只換標題重做；缺少生成或模型呼叫證據時，把該項記為待完成，保留可回復的版本。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></div>
<!-- learner-content:end -->
