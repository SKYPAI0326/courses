---
slug: gemini-ai
unit_id: SUPP-part4-SUPP4-3
title: 補充：貪食蛇、預算、KPI 與會議改造
course_type: skill-operation
version: 2026-10-09-instructor-repair
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="core-1"><h2 class="section-heading">先選一項修改，保存原版與測試紀錄</h2><p class="body-text">三條路都要改一項原工具沒有的行為，先保存舊版和原始測試結果，再選一條。預算路線下載 <a download="" href="../assets/materials/budget-transfer.csv">新的活動資料</a>，核定改 25,000，新增「餘額低於核定預算 10%」提醒。KPI 路線使用既有 <a download="" href="../assets/materials/kpi-normal.csv">三項 KPI 資料</a>，新增「未達標且不利差距至少 20% 時標為優先處理」：higher 的不利差距=(target−actual)/target；lower 的不利差距=(actual−target)/target；只在 target&gt;0 時計算。AI 交辦路線下載 <a download="" href="../assets/materials/meeting-c.txt">新逐字稿 C</a> 、<a download="" href="../assets/materials/prompt-meeting.txt">基礎生成指令</a>與 <a download="" href="../assets/materials/prompt-solo-meeting.txt">欄位變更指令</a>，新增依據明確原文填寫前置任務 depends_on，未明確提及時留空。每條路都需保留原功能並用提供的答案核對新規則。行政案件追蹤仍可作之後的延伸，但不代替本次新規則驗收。</p><p class="body-text">用需求單寫「工作用途、改了什麼、預期變化、例外、交付對象」。計時器可用現成品控制課堂節奏；做計時器不等於完成這個工作挑戰。</p><p class="body-text">預算範例：核定 25,000 時，餘額 3,700 不提醒；講師實支改成 11,200 後，實支 23,000、差異 2,400、餘額 2,000，應提醒低餘額。</p></section>
<section class="lesson-section" id="core-2"><h2 class="section-heading">獨立做一次可追溯的修改</h2><ol class="body-text"><li>先保存舊版工具、原始資料與原測試紀錄。寫下新增規則、預期答案與一項例外。</li><li>依所選路線修改指令並保存 v2；先重跑原測試確認沒有退步，再跑變更資料核對差異。</li><li>若結果不同，記錄實際現象，修正需求或生成結果，再跑受影響測試。例外輸入修好後，正常功能仍要可用。</li><li>輸出可再次使用的成品、完整指令、驗收表與 README，關閉後重新開啟再測。</li></ol><details><summary>完成預判後核對答案</summary><p class="body-text">預算：新資料估算 20,600、實支 21,300、差異 +700、餘額 3,700；低於10%提醒關閉。講師實支改 11,200 後餘額 2,000，提醒開啟。KPI：處理時間 5 天、目標 3 天、方向 lower，未達標；不利差距為 66.7%，應標優先處理。改成 2 天後達標並移除優先提示；target=0 時不得除以零或錯報提醒。AI：C 有兩項待辦；「品牌定稿」無前置任務，「安排印刷」depends_on「品牌定稿」，日期和來源句須吻合逐字稿。未提到前置關係的 A/B 任務須為空。</p></details><div class="prompt-wrap"><div class="prompt-label">改造提示詞骨架｜配合所選路線的資料與指令檔</div><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-policy-1">請基於目前可用版本修改工具，新增我另附的新規則，並把其中會變動的門檻、類別或選項做成可調設定。保留原有欄位、計算方式與輸出；不要寫死當次資料或答案。原始測試仍須通過，再用另附新資料檢查新增規則。對空值、零目標或原文未提及的資訊不得猜測。說明修改位置，輸出完整可再次使用的版本。完成後由我依獨立測試紀錄驗收，未通過時保留舊版。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-policy-1"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-policy-1-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

新規則：〔說明觸發條件、處理方式及需要可調的設定〕
當次資料：〔另貼資料或逐字稿〕
核對紀錄：〔列出測試操作、預期與理由；不把答案編入程式〕</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside></div><p class="body-text">三條路已各有完整素材檔：預算、KPI、會議交辦。選一條即可；先保存舊版和原測試，再複製該路線的基礎指令及變更指令，先貼可重用結構；新規則、當次資料與核對紀錄放在下方附加區，會議擴充案例另見 <a download="" href="../assets/materials/prompt-solo-meeting-case.txt">案例與核對 TXT</a>。不要把不同案例的答案混在同一份驗收紀錄。</p></section>
<section class="lesson-section" id="snake-extensions">
<h2 class="section-heading">選用：把貪食蛇逐次改成自己的遊戲</h2>
<p class="body-text">第一章完成經典遊戲與一次配色修改後，可從這裡繼續。先開啟<a href="../assets/tools/貪食蛇.html" rel="noopener" target="_blank">壽司店延伸示範</a>看成果，再選下方一項修改。三份完整提示詞各自改視覺、難度與最高分、音效與代打；每次只貼一份，取得完整檔後另存新版本，再重查原玩法。這些是選用延伸，不列入第一章必做任務。</p>
<div class="prompt-wrap">
<div class="prompt-label">延伸提示詞 1｜加入壽司店視覺，保留核心玩法</div>
<p class="policy-guide">貼回最新遊戲的生成對話；樣式設定另附。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-snake-style">請在目前對話中最新的經典貪食蛇單一 HTML 上，加入可調整的樣式設定，包含主題、背景、蛇頭、蛇身、食物顏色及棋盤尺寸、格線大小；棋盤尺寸須為格線大小的整數倍並能容納蛇身，無效設定要提示。依另附樣式條件套用，未附時保留目前外觀；加上清楚的遊戲標題、分數區、開始畫面和結束畫面，按鈕與字體風格一致，文字使用繁體中文，桌機和手機版都不能水平捲動。
這次先改畫面，不改蛇的移動、吃食物加分、碰撞、鍵盤與觸控操作、開始或重新開始規則。不要載入外部圖片、字型、CDN、框架，也不要呼叫外部／雲端 API。
交付修改後從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML，不能只回傳 CSS、差異、程式片段或 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-style" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-snake-style-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-snake-style"><h3>這次的設定，可替換</h3><p>按需要另附設定，或在生成後填入工具畫面。</p><pre id="prompt-snake-style-case">本次樣式條件：壽司店復古街機；邏輯畫布400×400、格線20px；背景淺米色、蛇頭鮭魚橘、蛇身醋飯白、食物抹茶綠。手機上仍須縮放，不以邏輯尺寸撐寬頁面。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-style-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-snake-style-case-policy-status" role="status"></span></div><p>換一組棋盤尺寸與配色，核對格線、對比及原有計分。</p></aside>
</div>
<div class="prompt-wrap">
<div class="prompt-label">延伸提示詞 2｜加入難度、暫停與本機最高分</div>
<p class="policy-guide">先完成可玩的版本，再貼此修改要求；難度數值另附。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-snake-features">請在目前對話中最新的貪食蛇單一 HTML 上，新增可設定的難度清單，使用者能新增、修改與刪除難度名稱、初始移動間隔、吃食物後加速幅度、最短移動間隔，以及碰到邊界時結束或穿越的規則，並選擇本局難度。移動間隔須為正數，加速後不能低於最短間隔；難度清單不可空白。未另附設定時保留既有玩法。
新增暫停／繼續、重設和重新開始；重設要清除本局蛇身與分數，但保留最高分。遊戲結束時顯示本局分數及該難度的最高分，最高分只保存在目前瀏覽器的 localStorage，不得宣稱跨瀏覽器或跨裝置同步。保留鍵盤控制，並確保手機觸控方向按鈕及在棋盤上滑動都能改變方向，遊戲時不意外捲動頁面。
保留既有視覺、分數規則與核心玩法，不使用外部函式庫、框架、CDN、伺服器或外部 API；localStorage 是瀏覽器內建能力，資料只留在本機。交付修改後從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML，並確認新難度及原有核心行為都能使用；不要只回傳程式片段或 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-features" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-snake-features-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-snake-features"><h3>這次的設定，可替換</h3><p>按需要另附設定，或在生成後填入工具畫面。</p><pre id="prompt-snake-features-case">本次難度條件：入門、標準、進階三種，初始選標準；入門可穿越邊界且最慢；標準和進階撞邊界結束；進階最快。可依遊玩需要修改各級設定。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-features-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-snake-features-case-policy-status" role="status"></span></div><p>換另一組速度與邊界設定，核對暫停、重開及最高分保存。</p></aside>
</div>
<div class="prompt-wrap">
<div class="prompt-label">延伸提示詞 3｜加入音效、代打示範與視覺回饋</div>
<p class="policy-guide">接在可玩的版本後；音效與代打設定另附。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-snake-polish">請在目前對話中最新的貪食蛇單一 HTML 上，增加預設關閉的音效開關；啟用時使用瀏覽器內建 Web Audio API 合成簡短音效，不載入音效檔。若瀏覽器不支援音效，遊戲仍須正常進行。
新增「觀看 DEMO」和遊戲中的「代打」功能：由本機 JavaScript 自動控制蛇，優先朝食物移動並避開撞牆或撞到蛇身；找不到安全路線時選擇可存活方向。提供可輸入的 DEMO 時間上限，須為正整數秒；時間到即停止並回到可開始畫面；遊戲中可切回手動控制，暫停、重設和手動接管不可造成狀態錯亂。提供粒子與震動的獨立開關，開啟後分別在吃到食物與遊戲結束時顯示效果；DEMO 時間到時顯示簡短提示；效果不能遮住分數和操作按鈕。
不要呼叫雲端 AI、外部／雲端 API 或伺服器；Web Audio API 是瀏覽器內建能力。保留既有玩法、視覺、難度和最高分功能。交付修改後從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML，確認代打不會連網；不得只回傳程式片段或 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-polish" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-snake-polish-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-snake-polish"><h3>這次的設定，可替換</h3><p>按需要另附設定，或在生成後填入工具畫面。</p><pre id="prompt-snake-polish-case">本次示範條件：DEMO最長30秒；吃到食物顯示短暫粒子；遊戲結束時棋盤輕微震動。音效初次開啟保持關閉。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-polish-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-snake-polish-case-policy-status" role="status"></span></div><p>切換音效及代打設定，結束後確認仍可回到玩家操作。</p></aside>
</div>
<p class="body-text">每完成一份延伸提示詞，就重新開啟最新版本，確認新增功能，並重測開始、移動、得分、碰撞和重新開始。若功能沒有出現，將預期行為與實際畫面描述給模型，請模型只修正該項。依序追加可逐步擴充簡單版本，避免一次要求模型完成所有功能。</p>
</section><section class="lesson-section" id="core-3"><h2 class="section-heading">完課驗收：用證據確認</h2><p class="body-text">檢查五件成果：① 可重開的工具或 AI 專案；② 已知答案的輸入與實測結果；③ 一項有效需求變更及再測；④ 可閱讀的交付物；⑤ 保存完整指令與使用說明。說明一個工作判斷，例如超支、指標方向或未定期限。</p><p class="body-text">保存所選案例的生成、修改與重開紀錄；缺少模型呼叫或其他證據時記為待完成。要繼續選用其他案例，回<a href="../index.html#supplement-reuse">改造與保存補充目錄</a>，先確認新的輸入、規則和核對方法。</p></section><section class="lesson-section" id="completion"><h2 class="section-heading">保留改造前後的用途與測試紀錄</h2><p class="body-text">選定案例後，留下原版、新規則、修改版與新舊測試結果。不同案例的處理方式不同，不能只換標題重做；缺少生成或模型呼叫證據時，把該項記為待完成，保留可回復的版本。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></div>
<!-- learner-content:end -->
