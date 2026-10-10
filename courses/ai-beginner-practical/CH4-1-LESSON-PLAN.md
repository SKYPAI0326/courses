---
title: "工作方案比較：讓限制與取捨進入決策"
slug: ai-beginner-practical
unit_id: CH4-1
chapter: CH4-1
course_type: skill-operation
duration: 3h
audience: 零基礎成人，各自獨立操作與選題
prerequisites: 基本複製貼上、CH1提示詞方法；可直接用完整材料，不依賴前章成品
learning_objective: 獨立比較至少兩方案，依三標準排序與硬限制判斷，改一項條件後完成修訂決策卡
environment: 任一可用文字LLM；完整工作brief或有資料的生活選題；工具不可用先人工列式
style_guide: ai-beginner-practical/STYLE-GUIDE.md
platform_version: 當期帳號課前確認；介面以功能名稱找，不固定按鈕位置
status: machine-review-pending
---

## 本批凍結學員契約

角色：培訓／行政／自己單位的承辦人；問題：忽略容量、角色額度或假設成效會使方案不可行。起點：自含完整brief兩方案＋提示詞＋自己的LLM。成果：unit4-decision-card.md（實際提示詞、第一版、單一條件變化與修訂矩陣、取捨、未知及下一步）。用途：主管核定或未來自己重新計算。首動作：讀brief的限制與數字，接在compare提示詞後；首結果：送出文字含兩方案與三標準。回復：U4-FRAME／TRADEOFF／MISSING／CHANGE／SAVE；工具不可用先人工列式，保留待重跑。

## 180分鐘與獨立活動

|分鐘|活動|可觀察結果|
|---|---|---|
|0–15|用途、選自己的材料與首動作|已有個人案例及取得的完整資料|
|15–30|必要概念與獨立微型示範|能指出示範的判斷，無需交副本|
|30–60|自己帳號／資料與首輪操作|送出完整brief與比較提示詞|
|60–105|自己的第一版與逐項核對|兩方案硬限制列式及三標準矩陣|
|105–145|獨立判斷與修訂|僅改一項限制，重新判定並說明取捨|
|145–165|修復與保存|匯出檔重開，原版本與未解問題沒有遺失|
|165–180|個人驗收與單位遷移|自己回答成品用途、依據、未知與下一步|

合計180分鐘；尚未真人試跑校正。原完整生活例子選做，不再疊加共同作業。

正式來源為以下learner-content全文，包括完整材料、提示詞與成品參考；HTML須逐段保真。來源包與引用原文必須先於提問可取得。參考成品是作者示例，不宣稱平台已實跑。


## 2026-10-09 教師修訂說明

學員頁依已同意的閱讀審查修訂。下方 learner-content 是本次正式正文，保留原文、提示詞與工作台欄位。版本相容與試跑紀錄留教師區，不要求學員另填表。四章各三小時、Gamma在CH2後半，時間仍待真人試跑；不得把本次文字修改當作平台或真人驗證完成。

CH4的450漢字僅作模型縮稿參考，成品以實際列印一頁、內容可讀與算式／待確認完整檢查。CH2補限制試一次仍錯可依原文人工收尾。Gamma自帶企劃以小標題或支持原句定位，另可用頁內文字下載區存檔。

## 修訂前帳號觀察與版次紀錄（僅供教師）

以下為舊版記錄，不代表本次修訂提示詞已重跑或真人已通過。

- 2026-10-08授課帳號實跑：A改上限後有重複破損句與「實際節省」誤寫，一次精簡回覆「我是一个语言模型，这超出了我的设计用途。」；B一次精簡仍499中文字，超450。這是特定帳號當次結果，不能當所有工具都會拒答。遇到同樣問題，保留原輸出與拒答，不反覆重問同一失敗指令。

## 2026-10-11 逐步操作修訂

本次正式正文以下方 learner-content 為準。每人獨立選案，依動作、用意、預期結果與必要修復操作；工作台依流程逐欄保存，不新增重抄表格。示範與自己操作分清楚，先產生結果再核對。CH2區分語氣調整與真正更換讀者，Gamma另用完整企劃；CH3先來源與回答再點引用；CH4先驗算再改限制，最後呈現一頁文件。工具按鈕可依介面辨認，但平台帳號及真人跟做尚待重驗。原時數不增加，真人節奏待驗。

## 2026-10-11 白話與步驟精簡

依使用者核准方針修正文案；案例核對資訊集中，共通操作只引用所選案例。刪重複說明，保留原文、提示詞、完成範例、判斷與恢復。CH4文件/PDF拆步，既有欄位與錨點保留。HTML及下方正式正文同步；真人跟做、平台帳號與時數仍待驗。

<!-- learner-content:start -->
# 工作方案比較：讓限制與取捨進入決策


<hr class="section-rule"/>
<section class="lesson-section" id="lesson-start"><div class="section-eyebrow">(01) 個人起點與成果</div><h2 class="section-heading">選自己的材料，留下可重開的完成物</h2><p class="body-text">選補訓或行政交接一案，完成一頁建議。每人獨立使用自己的資料與帳號操作。</p><p class="body-text"><a href="#workplace-practice">選一個決策案例 →</a>　<a href="#lesson-check">完成檢查 →</a></p><details class="workbench-disclosure"><summary>展開我的成果保存台：直接貼實際版本</summary><div class="learner-workbench" id="lifestyle-workbench">
<form autocomplete="off" data-export-filename="unit4-decision-card.md" data-export-title="第4單元：工作／生活方案決策卡" data-workbench-form="" data-workbench-key="ai-beginner-practical:CH4-1:lifestyle:v2"><div class="learner-workbench-note">工作台先留空；依下方操作步驟，把自己的提示詞與回答貼入指定欄位。這裡只保存文字，不會產生 AI 回答；課後選做欄位可留空。</div><div class="learner-workbench-header"><div><h3 class="learner-workbench-title">我的實作成果保存台</h3><p class="learner-workbench-lede">提示詞卡用來選題與參考；這裡才是你的主紀錄。把決策問題、標準、比較、取捨與缺資料留在同一頁。</p></div><div class="learner-workbench-progress"><div class="learner-workbench-progress-label" data-workbench-progress-label="">必做欄位填寫 0%</div><div aria-hidden="true" class="learner-workbench-progress-bar"><div class="learner-workbench-progress-fill" data-workbench-progress-fill=""></div></div><div aria-live="polite" class="learner-workbench-status" data-workbench-status="" role="status">尚未開始填寫</div></div></div>
<section class="wb-panel"><h3>我的實際提示詞、第一版與一張修訂卡</h3><p class="wb-panel-lede">直接貼自己的真實操作版本，不重抄另一份分析表；第一版和修訂版都保留。</p><div class="wb-meta"><div class="wb-field"><label for="ch4-name">姓名或代號</label><input data-field="name" id="ch4-name" placeholder="例如：小安" type="text"/></div><div class="wb-field"><label for="ch4-date">開始日期</label><input data-field="date" id="ch4-date" type="date"/></div></div><div class="wb-field"><label for="ch4-card">我的案例／決策名稱</label><input data-field="card" data-required="true" id="ch4-card" placeholder="貼上自己的實際內容；未知寫待確認，工具不可用標待重跑。"/></div><div class="wb-field"><label for="ch4-full-prompt">完整提示詞與案例</label><textarea class="tall" data-field="fullPrompt" data-required="true" id="ch4-full-prompt" placeholder="貼比较指令＋完整案例原文"></textarea></div><div class="wb-field"><label for="ch4-first-answer">第一版比較與建議</label><textarea class="tall" data-field="firstAnswer" data-required="true" id="ch4-first-answer" placeholder="貼第一版全文；後面接「我的驗算」與選擇理由"></textarea></div><div class="wb-field"><label for="ch4-revision-instruction">改了哪項限制：實際指令</label><textarea data-field="revisionInstruction" data-required="true" id="ch4-revision-instruction" placeholder="原值：…／新值：…
貼實際送出的改條件指令"></textarea></div><div class="wb-field"><label for="ch4-revised-answer">修正版一頁建議</label><textarea class="tall" data-field="revisedAnswer" data-required="true" id="ch4-revised-answer" placeholder="貼最後完整建議，保留算式、取捨、待確認與下一步；人工整理請標明"></textarea></div><div class="wb-field"><label for="ch4-next">接下來由誰做什麼</label><textarea data-field="next" data-required="true" id="ch4-next" placeholder="動作：…
負責角色：…
日期未提供寫待確認
PDF檔名／頁數：…"></textarea></div></section><section class="wb-panel"><h3>主線完成檢查（填寫進度不代表品質）</h3><div class="wb-checklist"><label class="wb-check"><input data-field="check1" data-required="true" type="checkbox"/><span>自己的同一需求至少兩方案，三個標準有優先順序</span></label><label class="wb-check"><input data-field="check2" data-required="true" type="checkbox"/><span>硬限制已逐方案列式，角色工時／一次性設定分開</span></label><label class="wb-check"><input data-field="check3" data-required="true" type="checkbox"/><span>只改一項條件，保留第一版與受影響的計算</span></label><label class="wb-check"><input data-field="check4" data-required="true" type="checkbox"/><span>暫定選擇寫代價、成立條件與缺資料，未宣稱核准／實績</span></label><label class="wb-check"><input data-field="check5" data-required="true" type="checkbox"/><span>已匯出重開決策卡，找到實際提示詞與前後版本</span></label></div></section><details class="workbench-disclosure"><summary>課後選做：閱讀與生活紀錄</summary><section class="wb-panel"><h3>一、定義決策問題與選擇標準</h3><p class="wb-panel-lede">從旅遊、購物、學習、健康、家庭中選一項近期決策；先寫標準與優先順序，不知道的數字標「待確認」，不要讓模型代猜。</p><div class="wb-grid"><div class="wb-field"><label for="ch4-goal">我要做的決定</label><input data-field="goal" id="ch4-goal" placeholder="例如：在兩個方案中選出目前較合適的一個"/></div><div class="wb-field"><label for="ch4-time">決策時間與使用情境</label><input data-field="time" id="ch4-time" placeholder="例如：下週前決定；每天使用 6 小時"/></div><div class="wb-field"><label for="ch4-budget">硬限制／預算</label><input data-field="budget" id="ch4-budget" placeholder="沒有預算請填「不適用」或「待確認」"/></div><div class="wb-field"><label for="ch4-preferences">選擇標準與優先順序</label><textarea data-field="preferences" id="ch4-preferences" placeholder="例如：1. 安靜 2. 保固 3. 價格；寫出你為何這樣排序"></textarea></div><div class="wb-field"><label for="ch4-limits">缺資料與人工確認邊界</label><textarea data-field="limits" id="ch4-limits" placeholder="尺寸、安裝費、即時價格、健康／資格等尚未提供或需專業確認的地方"></textarea></div></div></section><section class="wb-panel"><h3>二、把決策框架寫成提示詞</h3><p class="wb-panel-lede">將決策問題、標準、優先順序、已知資料與缺資料寫進提示詞；要求模型比較方案，不直接替你宣布哪個最好。</p><div class="wb-field"><label for="ch4-original">我的決策問題（一句話）</label><textarea data-field="original" id="ch4-original" placeholder="例如：在清風 A12 與節能 B12 中，哪個較符合我的優先標準？"></textarea></div><div class="wb-grid"><div class="wb-field"><label for="ch4-background">已知資料與使用情境</label><textarea data-field="background" id="ch4-background" placeholder="我在哪裡使用、已有什麼資料、哪些條件來自 CH3 證據整理"></textarea></div><div class="wb-field"><label for="ch4-task">比較任務</label><textarea data-field="task" id="ch4-task" placeholder="請依我的標準比較方案，指出符合程度與取捨"></textarea></div><div class="wb-field"><label for="ch4-constraints">資料邊界與缺資料</label><textarea data-field="constraints" id="ch4-constraints" placeholder="只使用提供資料；未提供寫「缺資料」；需要人工／專業確認的地方列出"></textarea></div><div class="wb-field"><label for="ch4-format">比較輸出格式</label><textarea data-field="format" id="ch4-format" placeholder="方案／符合的標準／優點／代價／缺資料／下一步"></textarea></div></div></section><section class="wb-panel"><h3>三、產出方案比較並標記缺資料</h3><p class="wb-panel-lede">先留下模型第一次比較，再逐項檢查標準是否進入結果；不要只保存一個推薦句。</p><div class="wb-field"><label for="ch4-condition-check">標準／證據／缺資料檢查</label><textarea class="tall" data-field="conditionCheck" id="ch4-condition-check" placeholder="哪些標準有比較？哪些資料只支持部分結論？哪些欄位缺資料或需人工確認？"></textarea></div></section><section class="wb-panel"><h3>四、寫出取捨與下一步</h3><p class="wb-panel-lede">根據優先順序說明每個方案得到什麼、放棄什麼；最後寫下一個要查證或由你決定的動作。</p><div class="wb-grid"><div class="wb-field"><label for="ch4-comparison">方案取捨比較</label><textarea data-field="comparison" id="ch4-comparison" placeholder="方案 A 得到什麼／放棄什麼；方案 B 得到什麼／放棄什麼；哪個標準造成差異"></textarea></div></div></section></details>
<div class="wb-actions"><button class="wb-action primary" data-action="save" type="button">儲存到本機</button><button class="wb-action" data-action="export" type="button">匯出 Markdown</button><button class="wb-action" data-action="print" type="button">列印工作台</button><button class="wb-action danger" data-action="reset" type="button">清除本機資料</button></div><p class="wb-footnote">匯出檔保存本次方案建議與前後版。生活提示詞卡及離線範本供課後選用。</p>
</form>
</div></details></section><section class="lesson-section workplace-materials" id="workplace-practice"><div class="section-eyebrow">(02) 自選工作實作</div><h2 class="section-heading">用方案比較，完成主管能判斷的一頁建議</h2>
<p class="body-text">培訓承辦人要讓36位同仁補訓。兩場看起來省事，但講師總時間包含每場準備；行政交接試辦也不能把不同窗口的工時混成一個總數。這一章讓你把完整需求與兩個方案交給LLM，先檢查硬限制，再依自己的標準比較取捨，保留缺資料和成立條件。最後只改一個限制，看原建議是否仍成立。</p>
<p class="body-text">選補訓案、行政交接案，或自己的兩方案資料。沿用前章成果時只取已核對背景與限制；未量測的工時標估計。生活題供課後選做。</p>
<p class="body-text">先讀所選案例的限制與兩方案資料，再依下方操作步驟比較。原資料沒有的數字標待確認。</p>
<h3>選完整工作情境，保留單位與資料邊界</h3>
<p class="body-text">A適合教育、人資或行政培訓：比較場次、座位、準備與授課時間。B適合行政、服務與跨窗口交接：每個角色分別檢查週額度，另外列一次性設定。資料全為教學假設，不是真實報價、實測效率或核准結果。</p>
<details class="workbench-disclosure"><summary>補訓案：兩場集中班與三場小班</summary>
<p><a download="" href="assets/workplace/decisions/case-a/brief.md">下載原檔</a>；<button data-gamma-copy="brief-a" type="button">複製A完整補訓資料</button><span aria-live="polite" data-copy-status="" role="status"></span></p>
<div aria-label="材料閱讀預覽" class="material-preview">
<h4>教學模擬A｜教育行政：補訓場次怎麼排？</h4>
<p>你是培訓承辦人，要在一週內讓36位同仁完成補訓，向主管提出一頁選擇建議。這是自含情境，不需要前章成果。資料版本DC-A-20261008，不是實際報價或工時調查。</p>
<p>硬限制：36人全部有座位、同一講師總投入（授課＋每場準備）最多240分鐘、一週內完成。先過硬限制，再依偏好比較；不能用優點抵銷不合格。
優先順序：1. 場次少、降低通知與分流工作；2. 講師總投入少；3. 保留每場交流時間。這是本案例主管偏好，換自己的情境可以改，但要記錄原因。</p>
<table>
<thead>
<tr>
<th>欄位</th>
<th>方案A：兩場集中班</th>
<th>方案B：三場小班</th>
</tr>
</thead>
<tbody><tr>
<td>場數／每場容量</td>
<td>2場／18人</td>
<td>3場／12人</td>
</tr>
<tr>
<td>每場授課時間</td>
<td>90分鐘</td>
<td>60分鐘</td>
</tr>
<tr>
<td>每場準備時間</td>
<td>30分鐘</td>
<td>15分鐘</td>
</tr>
<tr>
<td>授課內已含交流時間</td>
<td>每場15分鐘</td>
<td>每場10分鐘</td>
</tr>
<tr>
<td>場地與講師時段</td>
<td>本週內已有可安排時段</td>
<td>本週內已有可安排時段</td>
</tr>
<tr>
<td>額外現金支出</td>
<td>使用既有教室與講師，新增現金支出0元</td>
<td>同左</td>
</tr>
</tbody></table>
<p>新增現金0元不代表沒有工時。授課時間已包含交流，不要再加一次。容量表示可安排座位，不保證實際出席；學員可出席時段、缺席補課與效果未提供，仍需確認。</p>
<p>主管新增條件（第二輪只改這一項）：講師總投入上限由240改為228分鐘。其他人數、時段與偏好保持不變。</p>
</div>
<details class="raw-material"><summary>原始文字（保留完整貼入格式）</summary>
<pre id="brief-a"># 教學模擬A｜教育行政：補訓場次怎麼排？

你是培訓承辦人，要在一週內讓36位同仁完成補訓，向主管提出一頁選擇建議。這是自含情境，不需要前章成果。資料版本DC-A-20261008，不是實際報價或工時調查。

硬限制：36人全部有座位、同一講師總投入（授課＋每場準備）最多240分鐘、一週內完成。先過硬限制，再依偏好比較；不能用優點抵銷不合格。
優先順序：1. 場次少、降低通知與分流工作；2. 講師總投入少；3. 保留每場交流時間。這是本案例主管偏好，換自己的情境可以改，但要記錄原因。

|欄位|方案A：兩場集中班|方案B：三場小班|
|---|---|---|
|場數／每場容量|2場／18人|3場／12人|
|每場授課時間|90分鐘|60分鐘|
|每場準備時間|30分鐘|15分鐘|
|授課內已含交流時間|每場15分鐘|每場10分鐘|
|場地與講師時段|本週內已有可安排時段|本週內已有可安排時段|
|額外現金支出|使用既有教室與講師，新增現金支出0元|同左|

新增現金0元不代表沒有工時。授課時間已包含交流，不要再加一次。容量表示可安排座位，不保證實際出席；學員可出席時段、缺席補課與效果未提供，仍需確認。

主管新增條件（第二輪只改這一項）：講師總投入上限由240改為228分鐘。其他人數、時段與偏好保持不變。
</pre>
</details>
</details>
<details class="workbench-disclosure"><summary>交接案：人工方式與工具方式</summary>
<p><a download="" href="assets/workplace/decisions/case-b/brief.md">下載原檔</a>；<button data-gamma-copy="brief-b" type="button">複製B完整行政交接資料</button><span aria-live="polite" data-copy-status="" role="status"></span></p>
<div aria-label="材料閱讀預覽" class="material-preview">
<h4>教學模擬B｜行政交接：四週試辦採哪個方式？</h4>
<p>你是行政承辦人，向主管比較同一件工作「交接文件更新」的兩種試辦方式。這是獨立模擬情境，尚未核准；沿用Gamma B的四週／既有工具思路，但本檔追加的工時假設不回寫Gamma企劃，也不代表企劃已獲核准。資料版本DC-B-20261008。</p>
<p>硬限制：四週；每週文件窗口最多30分鐘、使用窗口最多30分鐘；既有已允許工具，不新增購買。各角色須個別過限制，不能只加總工時判合格。
優先順序：1. 減少使用窗口每週負擔；2. 降低文件窗口負擔；3. 減少初次設定時間。保持引用可回查是共同品質要求；成效未測量，不能承諾節省比例。</p>
<table>
<thead>
<tr>
<th>欄位</th>
<th>方案A：人工維護固定交接範本</th>
<th>方案B：來源輔助草稿＋人工查核</th>
</tr>
</thead>
<tbody><tr>
<td>文件窗口每週投入</td>
<td>20分鐘</td>
<td>30分鐘，其中含10分鐘人工查核</td>
</tr>
<tr>
<td>使用窗口每週投入</td>
<td>25分鐘</td>
<td>15分鐘</td>
</tr>
<tr>
<td>一次性設定投入（另列）</td>
<td>30分鐘</td>
<td>60分鐘</td>
</tr>
<tr>
<td>新增現金支出</td>
<td>0元，使用既有工具</td>
<td>0元，使用既有允許的來源工具</td>
</tr>
<tr>
<td>交付方式</td>
<td>固定範本＋人工標原文位置</td>
<td>來源產生草稿＋人工點引用修訂</td>
</tr>
<tr>
<td>品質與成效資料</td>
<td>查核合格率、實際處理量與完成時間尚未測量</td>
<td>同左</td>
</tr>
</tbody></table>
<p>所有工時是教學假設，需試辦量測，不能當已發生的節省；一次性設定另需主管安排，尚未核准，不能悄悄算進每週額度或略掉。</p>
<p>主管新增條件（第二輪只改這一項）：文件窗口每週可用時間由30改為25分鐘；使用窗口仍30分鐘，其他條件與偏好不變。</p>
</div>
<details class="raw-material"><summary>原始文字（保留完整貼入格式）</summary>
<pre id="brief-b"># 教學模擬B｜行政交接：四週試辦採哪個方式？

你是行政承辦人，向主管比較同一件工作「交接文件更新」的兩種試辦方式。這是獨立模擬情境，尚未核准；沿用Gamma B的四週／既有工具思路，但本檔追加的工時假設不回寫Gamma企劃，也不代表企劃已獲核准。資料版本DC-B-20261008。

硬限制：四週；每週文件窗口最多30分鐘、使用窗口最多30分鐘；既有已允許工具，不新增購買。各角色須個別過限制，不能只加總工時判合格。
優先順序：1. 減少使用窗口每週負擔；2. 降低文件窗口負擔；3. 減少初次設定時間。保持引用可回查是共同品質要求；成效未測量，不能承諾節省比例。

|欄位|方案A：人工維護固定交接範本|方案B：來源輔助草稿＋人工查核|
|---|---|---|
|文件窗口每週投入|20分鐘|30分鐘，其中含10分鐘人工查核|
|使用窗口每週投入|25分鐘|15分鐘|
|一次性設定投入（另列）|30分鐘|60分鐘|
|新增現金支出|0元，使用既有工具|0元，使用既有允許的來源工具|
|交付方式|固定範本＋人工標原文位置|來源產生草稿＋人工點引用修訂|
|品質與成效資料|查核合格率、實際處理量與完成時間尚未測量|同左|

所有工時是教學假設，需試辦量測，不能當已發生的節省；一次性設定另需主管安排，尚未核准，不能悄悄算進每週額度或略掉。

主管新增條件（第二輪只改這一項）：文件窗口每週可用時間由30改為25分鐘；使用窗口仍30分鐘，其他條件與偏好不變。
</pre>
</details>
</details>
<h3>先分清硬限制、偏好與未知</h3>
<p class="body-text">硬限制是不符合就不能選的條件，如36人都有座位、講師最多240分鐘、每位窗口各自的週額度。偏好是在合格方案之間排序，如場次少或使用窗口負擔少。缺資料是現在還不能判斷的資訊，如可出席時段、缺席補課、實際品質或設定核定；它不會因AI填得流暢就變成事實。</p>
<p class="body-text">把同一個標準放在同一欄比較，寫出數字來自哪一份資料、怎麼算。每場交流已含授課時，不能重複加總；一次性設定與每週例行投入分開。新增現金0元仍有人工投入；座位足夠也無法保證36人全部出席。這些限制直接決定建議是否可執行。</p>
<h3>短示範：先排除不合格，再比較優點</h3>
<p class="body-text">只看這個獨立微型案例，不交示範副本：24人要上課，方案X一場容量20，方案Y兩場各12；主管偏好場次少，但必須每人有座位。中間計算是X只有20＜24，Y有2×12＝24。完成句為：「暫定Y，因X容量不足；接受多一場通知工作。仍需確認24人的時段與實際出席。」若模型選X只因省事，修訂時要求先核對容量，不能偷偷把學員改成20人。</p>
<p class="body-text">使用自己的案例時，先核對會影響選擇的限制，例如預算、人數或各角色時間，再依三個已排序的標準比較。看懂示範後就做自己的一組，不另交示範副本。</p>
<h3>產生一張建議，不另抄分析表</h3>
<p class="body-text">下方提示詞先做第一輪比較。接上所選案例的完整文字，包含限制、優先順序與待確認；不要只貼表格。保存這份完整提示詞與第一版。</p>
<details class="workbench-disclosure"><summary>兩方案比較提示詞（展開完整內容）</summary>
<p><a download="" href="assets/workplace/decisions/prompts/compare.txt">下載原檔</a>；<button data-gamma-copy="prompt-compare" type="button">複製兩方案比較提示詞</button><span aria-live="polite" data-copy-status="" role="status"></span></p>
<pre id="prompt-compare">我將貼上完整案例資料。請為指定主管製作一頁方案建議，只使用提供的數字與條件。
這是第一輪：只採「主管新增條件」之前的原限制；資料最後的新限制留待第二輪，不提前套用。A本輪上限240分鐘；B本輪文件與使用窗口各30分鐘／週；自選資料依所標原值。
先列決策、人數／期間與每項原硬限制，再計算每方案是否符合；不合格方案不能靠偏好加分補過。
依案例原有優先順序，至少用三個標準在同一矩陣比較兩方案。保留計算式與單位，各角色工時分開；一次性與每週投入分開，未提供的資訊標「缺資料」。
寫出暫定選擇、得到什麼、犧牲什麼、選擇成立的條件、至少一項待確認，以及下一步動作與原資料中的負責角色。沒有日期就寫待確認，不自造。
如兩方案都不合格，明示目前無可行方案，列需要調整的限制。不要把容量當出席成效、不要把假設工時當實際節省，也不要把0新增現金寫成無成本。
只輸出建議正文，修正歷程另保留在工作台。正文依一頁模板安排，中文字最多450字（只計漢字；標題與表格內漢字也計入），表格不超過六列比較資料；保留必要算式與單位。450漢字只作精簡參考，不要求學員人工逐字計數；用列印預覽確認正文一頁且可讀。

請以案例和方案的完整名稱稱呼：補訓案用「兩場集中班／三場小班」，交接案用「人工方式／工具方式」，不單獨用A或B。

自備案例使用原資料中的方案名稱、原限制、單位與三項優先順序；不套用補訓或交接案例的數字與角色。</pre>
</details>
<p class="body-text">先看完整算式，再查自己的回答。只看一種案例的列就好；表中是作者驗算，不是你的模型回答。</p><table><thead><tr><th>案例與原限制</th><th>怎麼算</th><th>判斷與理由</th></tr></thead><tbody><tr><td>補訓：36人；講師最多240分鐘</td><td>兩場：2×18＝36席；2×(90＋30)＝240分鐘。三場：3×12＝36席；3×(60＋15)＝225分鐘。</td><td>兩者都合格。原偏好先看場次少，所以暫選兩場；代價是多15分鐘投入且沒有餘裕。交流已含授課，不能再加。</td></tr><tr><td>補訓：只改上限為228分鐘</td><td>兩場240−228＝超12分鐘；三場228−225＝餘3分鐘。</td><td>改選三場，接受多一場安排；可出席時段與缺席補課仍待確認。</td></tr><tr><td>交接：每位窗口每週最多30分鐘</td><td>人工：文件20≤30、使用25≤30；工具：文件30≤30、使用15≤30。設定30／60分鐘另列。</td><td>兩者每週均合格。先減使用窗口負擔，暫選工具；代價是文件多10分鐘、設定多30分鐘。工具的10分鐘查核已含30分鐘，不能再加。</td></tr><tr><td>交接：只把文件窗口改成25分鐘</td><td>人工文件20≤25；工具文件30−25＝超5分鐘。使用窗口25／15仍各≤30。</td><td>改選人工；不能刪10分鐘查核湊額度。一次性設定仍要主管安排，成效待量測。</td></tr></tbody></table><div class="steps-wrap"><div class="step-block" id="ch4-step-1"><div class="step-circle">1</div><div class="step-content"><div class="step-heading">1. 選案例，找出原限制與比較標準</div><div class="step-body"><p>展開補訓案、行政交接案，或準備自己的兩方案資料。在「我的案例／決策名稱」填案名。</p><p>找出原限制、兩方案數值和三個標準的優先順序。第一輪使用原限制；材料中的新增條件留到步驟5。資料不足時先補資料，或使用課程案例。</p></div></div></div><div class="step-block" id="ch4-step-2"><div class="step-circle">2</div><div class="step-content"><div class="step-heading">2. 把比較指令接上案例全文</div><div class="step-body"><p>複製「兩方案比較提示詞」，貼入對話工具的新對話，再接上所選案例全文後送出。</p><p>送出的全文貼「完整提示詞與案例」，回答貼「第一版比較與建議」。回答要列出兩個方案、算式、至少三項比較標準和暫定選擇。</p></div></div></div><div class="step-block" id="ch4-step-3"><div class="step-circle">3</div><div class="step-content"><div class="step-heading">3. 自己驗算，確認兩方案是否合格</div><div class="step-body"><p>從原資料取值，逐一驗算兩方案是否符合限制。課程案例可對照上方驗算表；自備案例用自己的數值，例如「方案費用≤預算上限」。</p><p>每個數字附單位，估計值要註明。各角色時間分開查，一次性設定另列。在第一版後寫「我的驗算：」並附算式；算錯時依原資料更正，標「人工更正」。</p></div></div></div><div class="step-block" id="ch4-step-4"><div class="step-circle">4</div><div class="step-content"><div class="step-heading">4. 比較合格方案，寫出選擇與代價</div><div class="step-body"><p>先排除不符合限制的方案，再依步驟1的三項標準比較其餘方案。使用同一單位，保持原優先順序。</p><p>在第一版下寫選擇的理由及代價，例如「兩場較少安排，但多投入15分鐘且沒有餘裕」。出席時段、設定核准或成效尚未確認時，一併列出；假設工時仍須試辦量測。</p></div></div></div><div class="step-block" id="ch4-step-5"><div class="step-circle">5</div><div class="step-content"><div class="step-heading">5. 只改一項限制，重新提問</div><div class="step-body"><p>在所選案例找到新增條件，複製「改一項限制的修訂提示詞」，回原對話送出。自備案例使用「自備案例：改一項限制」，填限制名稱、原值、新值和單位。</p><p>其餘資料及優先順序沿用第一輪。指令貼「改了哪項限制：實際指令」，回答貼「修正版一頁建議」。換新對話時，先附原資料及第一版。</p></div></div></div><div class="step-block" id="ch4-step-6"><div class="step-circle">6</div><div class="step-content"><div class="step-heading">6. 重算受影響部分，確認要不要改選</div><div class="step-body"><p>用新限制逐方案重算，並核對其他限制仍符合。課程案例看驗算表中所選案例的新限制列；自備案例可寫「費用4,800元＞新預算4,500元，超300元」。</p><p>在修正版寫出原選擇、新選擇及造成改選的計算。模型算錯時補明限制再試一次，仍錯就人工更正。兩方案都不合格時，寫「目前無可行方案」，保留必要工作與限制。</p></div></div></div><div class="step-block" id="ch4-step-7"><div class="step-circle">7</div><div class="step-content"><div class="step-heading">7. 整理最後建議，保留必要條件</div><div class="step-body"><p>將核對後的修正版放入<a href="assets/workplace/decisions/one-page-template.md" rel="noopener" target="_blank">一頁模板</a>：決策與新限制、同欄比較、暫定選擇、得到與放棄、成立條件、待確認與下一步。過程版本留在工作台。</p><p>最後建議貼「修正版一頁建議」，後續動作填「接下來由誰做什麼」。太長時刪重複解釋；若用「一頁格式提示詞」縮稿，帶上已核對修訂稿及原案例，縮稿後再查算式與未知事項。</p></div></div></div><div class="step-block" id="ch4-step-8"><div class="step-circle">8</div><div class="step-content"><div class="step-heading">8. 把最後建議貼進文件</div><div class="step-body"><p>開啟<a href="https://docs.google.com/document/" rel="noopener" target="_blank">Google 文件</a>並登入，建立空白文件，命名「我的方案建議」。也可使用已有的 Word 或文件工具。</p><p>將「修正版一頁建議」貼進文件。文件只放最後建議，第一版及修訂過程留在工作台。</p></div></div></div>
<div class="step-block" id="ch4-step-8-preview"><div class="step-circle">9</div><div class="step-content"><div class="step-heading">9. 檢查列印頁面</div><div class="step-body"><p>選「檔案→列印」，查看預覽。確認只有一頁，數字及單位沒有缺漏，文字可讀。</p><p>超過一頁時，回文件刪重複解釋，再看預覽；保留算式、待確認與下一步，字體大小維持可讀。</p></div></div></div>
<div class="step-block" id="ch4-step-8-export"><div class="step-circle">10</div><div class="step-content"><div class="step-heading">10. 下載一頁 PDF</div><div class="step-body"><p>列印預覽出現目的地選單時，選「儲存為 PDF」，檔名用「方案建議.pdf」。若工具直接下載 PDF，就到下載紀錄找到檔案。<a href="https://support.google.com/docs/answer/143346?hl=zh-Hant" rel="noopener" target="_blank">Google 文件列印說明</a></p><p>文件工具無法使用時先匯出文字，標「一頁草稿，頁數待驗」；工具恢復後從貼進文件這一步續做。</p></div></div></div>
<div class="step-block" id="ch4-step-8-check"><div class="step-circle">11</div><div class="step-content"><div class="step-heading">11. 重開 PDF，核對內容</div><div class="step-body"><p>開啟「方案建議.pdf」，再確認頁數是一頁。核對算式、單位、待確認與下一步。</p><p>有漏字、截字或頁數不符時，回文件修正，再下載並重開。</p></div></div></div><div class="step-block" id="ch4-step-9"><div class="step-circle">12</div><div class="step-content"><div class="step-heading">12. 保存過程紀錄</div><div class="step-body"><p>在工作台按「儲存到本機」，重新整理確認版本仍在，再按「匯出 Markdown」。重開 <code>unit4-decision-card.md</code>，查提示詞、第一版、改限制指令、修正版和驗算。</p><p>文字檔留修改過程，PDF 留最後建議。確認兩份都能開啟，再依算式、取捨與下一步勾選完成檢查。缺項回對應步驟補上。</p></div></div></div></div>
<details class="workbench-disclosure"><summary>改一項限制的修訂提示詞（展開完整內容）</summary>
<p><a download="" href="assets/workplace/decisions/prompts/change.txt">下載原檔</a>；<button data-gamma-copy="prompt-change" type="button">複製改一項限制的修訂提示詞</button><span aria-live="polite" data-copy-status="" role="status"></span></p>
<pre id="prompt-change">這是第二輪。請保留第一版（補訓案原上限240分鐘；交接案文件／使用原上限各30分鐘／週），只依資料最後的「主管新增條件」改一項硬限制，其餘數字、偏好與條件不動。
重新計算兩方案可行性，列「原條件／新條件／受到影響的計算與結論」，再給一頁修訂建議。
若需改選，指出是哪項限制造成；若不改選，指出仍成立的依據。任一方案不合格不可偷偷降低人數、刪人工查核或增加額度。
保留缺資料、成立條件與需由主管確認的下一步；若兩者皆不可行就明示無可行方案。
本輪補訓案只改講師上限228分鐘；交接案只改文件窗口25分鐘／週，使用窗口仍30。請將修訂建議正文與「原／新條件及變化」過程說明分開，正文沿用一頁模板、最多450中文字，保留至少三項比較標準、完整關鍵算式及未知；用列印預覽確認正文一頁且可讀。

請以案例和方案的完整名稱稱呼：補訓案用「兩場集中班／三場小班」，交接案用「人工方式／工具方式」，不單獨用A或B。</pre>
</details>
<details class="workbench-disclosure" id="own-case-revision"><summary>自備案例：改一項限制（展開指令與替換示例）</summary>
<p class="body-text">在步驟5使用。只複製下方指令，把四個方括號換成自己的資料；送出前確認已沒有方括號提示。回原對話送出，第一輪的完整資料不用重抄。換新對話時，先貼自己的完整原資料與第一版，再接這份指令。</p>
<p><a download="" href="assets/workplace/decisions/prompts/change-own.txt" rel="noopener" target="_blank">下載自備案例指令</a>；<button data-gamma-copy="prompt-change-own" type="button">複製自備案例修訂提示詞</button><span aria-live="polite" data-copy-status="" role="status"></span></p>
<pre class="code-block" id="prompt-change-own">這是同一決策的第二輪。請沿用本對話中的完整原資料與第一版，只改下列一項硬限制。
要改的限制：[限制名稱]
原值：[原值及單位]
新值：[新值及單位]
保持不變：[其他硬限制、兩方案資料、三項比較標準及原優先順序]

請使用我自己的方案名稱、角色與數字，不套用課程補訓或交接案例。
逐方案列出受影響的算式與單位，再核對其他硬限制。先排除不合格方案，再依原優先順序比較；若兩者都不合格，就寫目前無可行方案。
先列「原值／新值／受影響的計算／是否改選及理由」，再提供修訂建議正文。保留得到與放棄、成立條件、缺資料、確認角色及下一步；不補造日期、核准或成效。
只有估計值時標明估計；比較只說在所列資料與假設下成立。第一版與原資料保留，不覆蓋。</pre>
<details><summary>先看替換示例：活動租金5,000→4,500元</summary><p class="body-text">這段只示範如何換自己的限制，不另交作業。先看原資料與第一輪判斷，再看已填好的第二輪指令，最後用作者驗算核對改選理由。</p><pre class="code-block" id="own-case-change-example">教學模擬：活動場地選擇，並非實際報價。
原資料：36人，租金上限5,000元；青松教室36席、租金4,000元、交通20分鐘；河岸教室40席、租金4,800元、交通10分鐘。
比較順序：1.交通時間短；2.租金低；3.剩餘座位多。須先符合人數與租金上限；可預約時段、其他費用與實際出席仍待活動承辦人確認。
第一輪作者驗算：兩案均至少36席，且租金不超5,000元；依交通優先，暫選河岸。代價是租金多800元。

填好後的第二輪指令：
這是同一決策的第二輪。請沿用上述完整原資料與第一版，只改下列一項硬限制。
要改的限制：場地租金上限
原值：5,000元
新值：4,500元
保持不變：36人、兩教室容量、租金與交通時間，以及交通時間→租金→剩餘座位的比較順序。
請逐方案驗算新限制，保留其他限制、待確認與下一步，再說明是否改選及取捨。不補造可預約或核准結果。

第二輪作者驗算（不是模型實跑）：青松4,000≤4,500，餘500元；河岸4,800＞4,500，超300元，不合格。座位條件未改，青松36席仍符合36人。
參考完成句：暫改選青松，因河岸超新上限300元；接受交通多10分鐘、無剩餘座位。此選擇只依所列資料成立，活動承辦人仍須確認時段、其他費用與出席安排；未確認前不宣稱已預約。</pre></details>
<p class="body-text">送出後應看到原值、新值、兩方案受影響的計算與是否改選。回答誤用課程數字時，補明「只用我提供的原資料與新限制」試一次；仍錯就按自己的資料人工修正，保留模型版與核對依據。其餘保存流程沿用步驟5–9。</p></details>
<p class="body-text"><span aria-live="polite" data-gamma-copy-status="" role="status">展開所選案例即可複製完整資料或提示詞。</span></p>
<h3>長稿留作過程，交付只留一頁建議</h3>
<p class="body-text">第一輪用原限制，第二輪只改一項。過程留工作台，最後建議放「修正版一頁建議」，再完成文件與 PDF 步驟。</p>
<p class="body-text">核對後的建議依「把最後建議貼進文件」到「重開 PDF，核對內容」交付。下方模板供整理成品，過程版本仍留工作台。</p>
<p class="body-text">模型拒答、文字破損或精簡後仍太長時，保留原回答，依已核對資料手動填一頁模板，標明「人工整理」。不必反覆送出同一個失敗指令。</p>
<p class="body-text">人工整理只驗算自己的一案：補訓案兩場集中班需240分鐘，超新上限12分鐘；三場小班需225分鐘，尚餘3分鐘。交接案文件窗口的人工方式需20分鐘／週，工具方式需30分鐘／週，後者超新上限5分鐘；使用窗口25／15分鐘均未超30。保留10分鐘人工查核，不能刪掉來湊額度。算式不清楚時請講師協助。</p>
<details class="workbench-disclosure"><summary>一頁格式提示詞（展開完整內容）</summary>
<p><a download="" href="assets/workplace/decisions/prompts/one-page.txt">下載完整文字</a>；<button data-gamma-copy="prompt-one-page" type="button">複製全文</button><span data-copy-status="" role="status"></span></p>
<pre id="prompt-one-page">請把下面「已驗算的修訂建議」整理成一頁提案正文，只改呈現，不改資料、限制、選擇與未知。不是重新研究或換方案。
正文依序為：決策／期間／新限制；兩方案同欄比較矩陣（不超過六列資料，涵蓋硬限制、原優先順序至少三標準，必要時同列保留週與四週數）；暫定選擇及原→新條件造成的變化；得到／犧牲；成立條件／待確認；下一步與來源角色／日期未知。
中文字最多450字，只計漢字，標題與表格內漢字也計入。保留算式與單位，各角色分開，每週與一次性設定分開，不刪人工查核，不將假設差額寫成實際節省，不補完成、核准或日期。
只輸出正文，勿重貼舊稿、修正表與長篇說明。450漢字只作精簡參考，不要求學員人工逐字計數；以列印預覽確認正文一頁且可讀。
[貼上已核對的修訂建議及所選完整原資料；將原／新限制標清楚]

請以案例和方案的完整名稱稱呼：補訓案用「兩場集中班／三場小班」，交接案用「人工方式／工具方式」，不單獨用A或B。</pre>
</details>
<details class="workbench-disclosure"><summary>一頁提案模板（展開完整內容）</summary>
<p><a download="" href="assets/workplace/decisions/one-page-template.md">下載完整文字</a>；<button data-gamma-copy="decision-one-page-template" type="button">複製全文</button><span data-copy-status="" role="status"></span></p>
<pre id="decision-one-page-template"># 一頁方案建議模板（沿用原成果保存台）

這是交付正文的結構參考，不是另一張必填作業表。把方括號換成已核對的內容，完整稿貼回「修訂決策卡」。兩輪長稿、實際指令與拒答仍留原過程欄位。正文最多450中文字；標題／表格內漢字也計入，只計漢字、不計標點／數字／英文字。此字數不是CH1的可見字元口徑。

## [決策名稱]（教學模擬／真資料請標版本）

決策與限制：[給誰、期間／人數、原限制→新限制；第二輪只改一項]

|檢核／比較標準（同欄同單位）|方案A|方案B|
|---|---|---|
|硬限制與算式|[容量或各角色額度，合格／超額多少]|[同一標準及單位]|
|第一偏好|[值或取捨]|[同欄比較]|
|第二偏好|[值；各角色週／四週分開]|[同欄比較]|
|第三偏好|[值；一次性設定另列]|[同欄比較]|

暫定選擇與變化：[原選何案，新限制導致哪案超額；兩案都不合格就寫無可行方案]
得到／犧牲：[依據資料，不宣稱實際節省、出席或效果]
成立條件／待確認：[保留缺資料及設定是否核定；日期未知不補造]
下一步：[來源負責角色、可做動作、日期／待確認]

完成後用文件工具的列印預覽確認頁數，逐句與算式回原素材。若超過一頁，縮短重複解釋；不要刪掉計算、取捨或未知。列印版面尚未驗就標「一頁草稿，頁數待驗」。
</pre>
</details>
<p class="body-text">以下兩份完整人工稿供你完成自己版本後核對。它們以原資料與前兩輪真輸出校訂；不是新模型輸出、真人成品或核准結果。</p>
<details class="workbench-disclosure"><summary>A完整人工整理參考（展開完整內容）</summary>
<p><a download="" href="assets/workplace/decisions/case-a/one-page-manual.md">下載完整文字</a>；<button data-gamma-copy="decision-one-page-a" type="button">複製全文</button><span data-copy-status="" role="status"></span></p>
<pre id="decision-one-page-a"># CH4-A 人工整理交付版

作者依完整原素材與真實前兩輪回答整理；平台精簡請求拒答，故本版不是模型第三輪輸出或真人成品。一頁結構草稿；中文字含正文標題／表格均由作者實算，列印頁數仍待本人預覽。

## 補訓場次修訂建議（教學模擬）

決策：一週內為36人安排座位；講師授課＋準備最多228分鐘。交流已含授課，新增現金0元仍有工時成本。

|檢核與比較|A兩場集中|B三場小班|
|---|---|---|
|容量|2×18＝36席|3×12＝36席|
|講師總投入|2×(90＋30)＝240分，超12分，不合格|3×(60＋15)＝225分，餘3分，合格|
|本週時段|有可安排時段|有可安排時段|
|場次（第一偏好）|2場|3場|
|講師投入（第二偏好）|240分|225分|
|每場交流（第三偏好）|15分|10分|

暫改選B：原240分上限兩案合格、偏好A；改228後A不合格，場次優點無法補過。得到符合上限與較小單班容量；犧牲場次少、單場交流較長的偏好。225分是教學估算，差15分不是實際已節省。

成立條件：36人可分配至三個本週時段，講師可依所列授課與準備執行。座位不保證出席；可出席名單、缺席補課、成效與承辦人工時缺資料。

下一步：培訓承辦人確認學員時段與缺席安排，請主管確認暫定方案；日期待確認。
</pre>
</details>
<details class="workbench-disclosure"><summary>B完整人工整理參考（展開完整內容）</summary>
<p><a download="" href="assets/workplace/decisions/case-b/one-page-manual.md">下載完整文字</a>；<button data-gamma-copy="decision-one-page-b" type="button">複製全文</button><span data-copy-status="" role="status"></span></p>
<pre id="decision-one-page-b"># CH4-B 人工整理交付版

作者依完整原素材及平台前兩輪回答整理。模型精簡稿仍499中文字，未符合本次450字要求；本版不是新增模型輸出或真人成品。一頁結構草稿；中文字含正文標題／表格均由作者實算，列印頁數仍待本人預覽。

## 交接更新四週試辦建議（教學模擬，尚未核准）

用既有已允許工具、不新增購買；新增現金0元仍有工時成本。文件窗口每週最多25分，使用窗口仍30分，須各別過限制。

|檢核與比較|A固定範本人工維護|B來源草稿＋人工查核|
|---|---|---|
|文件窗口／週|20≤25分，餘5分|30＞25分，超5分，不合格；含10分查核不能刪|
|使用窗口／週（第一偏好）|25≤30分|15≤30分|
|文件負擔（第二偏好）|20分|30分|
|設定一次性（第三偏好，另列）|30分，待安排核准|60分，待安排核准|
|四週假設投入（分角色）|文件20×4＝80分；使用25×4＝100分|文件30×4＝120分；使用15×4＝60分|

原每週文件上限30分，兩案合格，優先減使用負擔暫選B；改25分後B超5分，暫改選A。得到可行與較少設定投入，犧牲使用窗口每週較低負擔。不能靠偏好補過、刪查核或增額。

成立條件：主管另核准A設定30分；人工標原文位置可回查。人數、實際工時、品質與成效未提供／未測，估算不當已發生節省。

下一步：主管確認設定投入，行政承辦人準備四週量測；日期待確認。
</pre>
</details>
<h3>完成自己的版本後才核對作者參考</h3>
<p class="body-text">補訓案原上限240分鐘時，可先選兩場集中班；改228後，應改三場小班，並確認上課安排。交接案原額度下可先選工具方式；文件窗口改25分鐘後，應改人工方式。以下參考供你完成後核對計算與理由，不當成自己的模型輸出。</p>
<details class="workbench-disclosure"><summary>A完整決策參考（展開完整內容）</summary>
<p><a download="" href="assets/workplace/decisions/case-a/reference.md">下載原檔</a>；<button data-gamma-copy="decision-reference-a" type="button">複製A完整決策參考</button><span aria-live="polite" data-copy-status="" role="status"></span></p>
<div aria-label="材料閱讀預覽" class="material-preview">
<h4>教學A作者參考｜一頁補訓方案建議</h4>
<p>原條件：36人，一週內，講師上限240分鐘；先過硬限制，再以場次少優先。</p>
<table>
<thead>
<tr>
<th>比較標準</th>
<th>A兩場集中班</th>
<th>B三場小班</th>
</tr>
</thead>
<tbody><tr>
<td>容量硬限制</td>
<td>2×18＝36，符合</td>
<td>3×12＝36，符合</td>
</tr>
<tr>
<td>總投入硬限制</td>
<td>2×(90＋30)＝240分鐘，符合且無餘裕</td>
<td>3×(60＋15)＝225分鐘，符合，餘15分鐘</td>
</tr>
<tr>
<td>通知與分流場次（第一偏好）</td>
<td>2場</td>
<td>3場，多1場</td>
</tr>
<tr>
<td>講師總投入（第二偏好）</td>
<td>240分鐘</td>
<td>225分鐘，少15分鐘</td>
</tr>
<tr>
<td>每場交流（第三偏好）</td>
<td>15分鐘，已含授課</td>
<td>10分鐘，已含授課</td>
</tr>
</tbody></table>
<p>暫定A：兩者均符合原限制，A符合場次少優先，但放棄B少15分鐘投入與15分鐘餘裕。成立條件：36人能分成兩場各18人並實際出席；容量不是出席保證。待確認：可出席時段與缺席補課。下一步：培訓承辦人確認時段與分流，請主管核定，日期來源未提供。</p>
<p>第二輪只改上限228分鐘：A240＞228，不合格，超12分鐘；B225≤228，合格，餘3分鐘。修訂暫定B：接受多一場通知與每場交流較短，換取符合上限；不要擅改課程時間或人數讓A過關。出席、補課與主管核定仍待確認。</p>
</div>
<details class="raw-material"><summary>原始文字（保留完整貼入格式）</summary>
<pre id="decision-reference-a"># 教學A作者參考｜一頁補訓方案建議

原條件：36人，一週內，講師上限240分鐘；先過硬限制，再以場次少優先。

|比較標準|A兩場集中班|B三場小班|
|---|---|---|
|容量硬限制|2×18＝36，符合|3×12＝36，符合|
|總投入硬限制|2×(90＋30)＝240分鐘，符合且無餘裕|3×(60＋15)＝225分鐘，符合，餘15分鐘|
|通知與分流場次（第一偏好）|2場|3場，多1場|
|講師總投入（第二偏好）|240分鐘|225分鐘，少15分鐘|
|每場交流（第三偏好）|15分鐘，已含授課|10分鐘，已含授課|

暫定A：兩者均符合原限制，A符合場次少優先，但放棄B少15分鐘投入與15分鐘餘裕。成立條件：36人能分成兩場各18人並實際出席；容量不是出席保證。待確認：可出席時段與缺席補課。下一步：培訓承辦人確認時段與分流，請主管核定，日期來源未提供。

第二輪只改上限228分鐘：A240＞228，不合格，超12分鐘；B225≤228，合格，餘3分鐘。修訂暫定B：接受多一場通知與每場交流較短，換取符合上限；不要擅改課程時間或人數讓A過關。出席、補課與主管核定仍待確認。
</pre>
</details>
</details>
<details class="workbench-disclosure"><summary>B完整決策參考（展開完整內容）</summary>
<p><a download="" href="assets/workplace/decisions/case-b/reference.md">下載原檔</a>；<button data-gamma-copy="decision-reference-b" type="button">複製B完整決策參考</button><span aria-live="polite" data-copy-status="" role="status"></span></p>
<div aria-label="材料閱讀預覽" class="material-preview">
<h4>教學B作者參考｜一頁行政交接試辦建議</h4>
<p>原條件：四週，每個角色每週上限30分鐘，既有工具、不新增購買；設定另需核定。</p>
<table>
<thead>
<tr>
<th>比較標準</th>
<th>A人工固定範本</th>
<th>B來源草稿＋人工查核</th>
</tr>
</thead>
<tbody><tr>
<td>文件窗口每週硬限制</td>
<td>20≤30，符合</td>
<td>30≤30，符合，其中10分鐘查核保留</td>
</tr>
<tr>
<td>使用窗口每週硬限制</td>
<td>25≤30，符合</td>
<td>15≤30，符合</td>
</tr>
<tr>
<td>使用窗口負擔（第一偏好）</td>
<td>四週4×25＝100分鐘</td>
<td>四週4×15＝60分鐘</td>
</tr>
<tr>
<td>文件窗口負擔（第二偏好）</td>
<td>四週4×20＝80分鐘</td>
<td>四週4×30＝120分鐘</td>
</tr>
<tr>
<td>一次性設定（第三偏好）</td>
<td>30分鐘，另列待核定</td>
<td>60分鐘，另列待核定</td>
</tr>
<tr>
<td>現金／品質資料</td>
<td>新增現金0；查核、處理量與成效未測</td>
<td>同左；不能保證節省比例</td>
</tr>
</tbody></table>
<p>暫定B：原每週限制均符合，依使用窗口負擔優先選B；接受文件窗口多40分鐘／四週、設定多30分鐘。這些都是資料假設的比較，不能稱已達成節省。成立條件：設定時間取得核定，實測每週投入不超額且引用人工查核達標。下一步：行政承辦人把60分鐘設定及待量測項目送主管核定，核定日期未提供；尚未核定前不可宣稱已啟動。</p>
<p>第二輪只改文件窗口上限25分鐘：A20≤25合格；B30＞25不合格，超5分鐘／週。修訂暫定A：保留使用窗口上限30、人工查核與其他條件，接受使用窗口較高負擔。不能把兩角色加總後用45分鐘掩蓋B文件窗口超額，也不能刪掉10分鐘人工查核讓B通過。A設定30分鐘仍需核定；實測品質與工時待確認。</p>
</div>
<details class="raw-material"><summary>原始文字（保留完整貼入格式）</summary>
<pre id="decision-reference-b"># 教學B作者參考｜一頁行政交接試辦建議

原條件：四週，每個角色每週上限30分鐘，既有工具、不新增購買；設定另需核定。

|比較標準|A人工固定範本|B來源草稿＋人工查核|
|---|---|---|
|文件窗口每週硬限制|20≤30，符合|30≤30，符合，其中10分鐘查核保留|
|使用窗口每週硬限制|25≤30，符合|15≤30，符合|
|使用窗口負擔（第一偏好）|四週4×25＝100分鐘|四週4×15＝60分鐘|
|文件窗口負擔（第二偏好）|四週4×20＝80分鐘|四週4×30＝120分鐘|
|一次性設定（第三偏好）|30分鐘，另列待核定|60分鐘，另列待核定|
|現金／品質資料|新增現金0；查核、處理量與成效未測|同左；不能保證節省比例|

暫定B：原每週限制均符合，依使用窗口負擔優先選B；接受文件窗口多40分鐘／四週、設定多30分鐘。這些都是資料假設的比較，不能稱已達成節省。成立條件：設定時間取得核定，實測每週投入不超額且引用人工查核達標。下一步：行政承辦人把60分鐘設定及待量測項目送主管核定，核定日期未提供；尚未核定前不可宣稱已啟動。

第二輪只改文件窗口上限25分鐘：A20≤25合格；B30＞25不合格，超5分鐘／週。修訂暫定A：保留使用窗口上限30、人工查核與其他條件，接受使用窗口較高負擔。不能把兩角色加總後用45分鐘掩蓋B文件窗口超額，也不能刪掉10分鐘人工查核讓B通過。A設定30分鐘仍需核定；實測品質與工時待確認。
</pre>
</details>
</details>
<h3>讓下一位使用者知道何時可採用</h3>
<p class="body-text">一頁建議要讓主管看出選擇理由與成立條件。完成後依頁尾清單核對；填寫進度不表示算式正確或已核准。</p>
<p class="body-text">帶回單位使用時，換成真實需求和兩方案資料，確認工時是估計或實測、設定是否核准，再提出建議。</p>
<p class="body-text">工具不能用時，先用<a href="assets/workplace/decisions/fallback.md" rel="noopener" target="_blank">決策離線備援</a>計算並填一頁模板，標「模型待重跑」。恢復後送原資料與兩輪提示詞，保存真回答。想練自己的單位需求，可用<a href="assets/worksheets/course-capstone-handoff.md" rel="noopener" target="_blank">課後短交接</a>，沿用已完成資料。</p>
</section>
<hr class="section-rule"/>
<section class="lesson-section" id="lesson-concept"><details class="workbench-disclosure"><summary>課後參考：生活方案與比較方法</summary>
<div class="section-eyebrow">(02) 關鍵概念</div>
<h2 class="section-heading">選擇標準、優先順序、取捨與缺資料</h2>
<p class="body-text">本單元和前面「把條件放進提示詞」不同：你要先決定什麼叫做適合，再要求工具用同一組標準比較。沒有標準，模型很容易把熱門、便宜或看似完整誤當成答案；沒有缺資料清單，你也不知道最後要查什麼。</p>
<div class="tool-grid">
<div class="tool-card"><div class="tool-name">選擇標準</div><div class="tool-tag">先定義怎麼判斷</div><div class="tool-summary">把「適合」拆成可觀察的項目，並排出優先順序。</div><div class="tool-list"><div class="tool-list-item"><span class="tool-check">✓</span>至少三項標準</div><div class="tool-list-item"><span class="tool-check">✓</span>分清楚硬限制與偏好</div><div class="tool-list-item"><span class="tool-check">✓</span>說明為何這樣排序</div></div></div>
<div class="tool-card"><div class="tool-name">取捨與缺資料</div><div class="tool-tag">保留決定權</div><div class="tool-summary">比較每個方案得到什麼、放棄什麼，並列出尚未能判斷的資料。</div><div class="tool-list"><div class="tool-list-item"><span class="tool-check">✓</span>每個方案都用同一組標準</div><div class="tool-list-item"><span class="tool-check">✓</span>缺資料不補成事實</div><div class="tool-list-item"><span class="tool-check">✓</span>最後選擇由人做</div></div></div>
</div>
<table>
<thead><tr><th>欄位</th><th>白話意思</th><th>京都行程例子</th></tr></thead>
<tbody>
<tr><td>目標</td><td>完成後要得到什麼</td><td>產出四天三夜行程初稿</td></tr>
<tr><td>時間</td><td>日期、天數、每天可用時間</td><td>四天三夜，每天 09:00–20:00</td></tr>
<tr><td>預算</td><td>總額或單項上限，並說明是否含交通住宿</td><td>每人 40,000 元，不含國際機票</td></tr>
<tr><td>偏好</td><td>喜歡什麼、不要什麼、優先順序</td><td>寺廟、美食；每天不超過兩個主要景點</td></tr>
<tr><td>限制</td><td>必須避開或必須確認的條件</td><td>第一天抵達較晚；交通要寫移動方式與估計時間</td></tr>
</tbody>
</table>
<p class="body-text">「幫我選一台冷氣」讓工具替你猜；「安靜排第一、預算上限 32,000 元、適用 4–6 坪、比較能源效率／保固／價格，缺資料列出，最後寫取捨」才是一份可以逐項檢查的決策說明。</p>
<div class="scenario-grid"><div class="scenario-row"><div class="scenario-task">只要一個結論</div><div class="scenario-pick">→ 要求「請替我決定最適合的」時，你看不到取捨依據。改成列出標準、選項、代價與待確認事項，最後決定仍由你做。</div></div><div class="scenario-row"><div class="scenario-task">標準互相衝突</div><div class="scenario-pick">→ 先說明優先順序，例如安靜高於價格；若兩個方案各有優勢，就保留取捨，不硬湊唯一答案。</div></div></div>
</details></section>
<hr class="section-rule"/>
<section class="lesson-section" id="lesson-demo"><details class="workbench-disclosure"><summary>課後示範：旅遊與購物方案</summary><p>完成本章作品後，可依需要查看下方範例。請自行核對，不需要其他學員的檔案。</p>
<div class="section-eyebrow">(03) 完整示範</div>
<h2 class="section-heading">京都四天三夜：看標準如何形成取捨</h2>
<p class="body-text">完整示範先從原始需求開始。阿凱知道每人預算 40,000 元、喜歡寺廟與美食、每天最多兩個主要景點；同行人數、住宿區域、抵達時間、機票是否計入仍未確定。這次先把「節奏寬鬆、符合偏好、預算不超過」排成標準，再比較每個安排的代價與缺資料。</p>
<table>
<thead><tr><th>已知</th><th>待補或待查</th></tr></thead>
<tbody><tr><td>京都、四天三夜；每人 40,000 元；喜歡寺廟與美食；每天最多兩個主要景點。</td><td>同行人數、住宿區域、抵達時間、是否包含國際機票；門票、交通票券、餐廳訂位與即時價格。</td></tr></tbody>
</table>
<p class="body-text">先看模糊輸入的差異，再看完整輸入：</p>
<div class="scenario-grid"><div class="scenario-row"><div class="scenario-task">原始輸入</div><div class="scenario-pick">「幫我規劃京都。」工具必須自行猜天數、預算、節奏與輸出格式，結果難以檢查。</div></div><div class="scenario-row"><div class="scenario-task">條件化輸入</div><div class="scenario-pick">四天三夜、每人 40,000 元、喜歡寺廟和美食、每天最多兩個主要景點，並標出待確認資料與預算區間。</div></div></div>
<div class="steps-wrap">
<div class="step-block"><div class="step-circle">1</div><div class="step-content"><div class="step-heading">把已知與未知分開</div><div class="step-body"><p>先把「40,000 元」放在預算欄，把尚未決定的同行人數、住宿區域、抵達時間與機票是否計入保留為待確認。這一步的結果是可使用的條件清單，下一步可以把條件寫進任務說明。</p></div></div></div>
<div class="step-block"><div class="step-circle">2</div><div class="step-content"><div class="step-heading">步驟 2｜貼上決策框架提示詞</div><div class="step-body"><p>下面這段是完整輸入。它先指定選擇標準與優先順序，再要求比較、取捨與缺資料，不把模型輸出當成最後決定。</p><div class="code-block">【背景】
我要規劃京都四天三夜自由行。目前已知：每人預算 40,000 元、喜歡寺廟和美食、每天最多安排兩個主要景點。同行人數、住宿區域、抵達時間、是否包含國際機票尚未確定。

【任務】
請提出一份四天三夜行程初稿，讓我能比較每日景點、用餐與移動安排。

【限制】
- 使用繁體中文，行程節奏寬鬆，不把每天排滿。
- 優先安排寺廟與美食；每天最多兩個主要景點。
- 不要自行假定機票、住宿、票券或餐廳的即時價格；缺少資料的地方標示「待確認」。
- 先給預算分配區間，不要把估算寫成實際報價。

【輸出格式】
先列出 3 個選擇標準與優先順序，再列出需要我補充的 4 個問題；用表格列出 Day 1–Day 4：時段、活動、移動方式、用餐方向、預估花費、待確認事項。最後列出預算分配、每個安排的取捨與仍不能判斷的資料。</div></div></div></div>
<div class="step-block"><div class="step-circle">3</div><div class="step-content"><div class="step-heading">讀回答中的中間結果</div><div class="step-body"><p>先找四個待補問題：同行人數、住宿區域、抵達時間、機票是否計入。再找預算欄是否用區間表示，以及每天是否最多兩個主要景點。這些可觀察結果會告訴你條件真的進入了輸出。</p><table><thead><tr><th>日程</th><th>時段</th><th>活動</th><th>移動／用餐方向</th><th>預估花費</th><th>待確認</th></tr></thead><tbody><tr><td>Day 1</td><td>下午至晚上</td><td>抵達後安排一個寺廟或周邊散步</td><td>依抵達機場與住宿位置調整；晚餐選住宿區附近</td><td>以區間表示</td><td>抵達時間、住宿區域</td></tr><tr><td>Day 2</td><td>上午至晚上</td><td>兩個寺廟景點，中間保留午餐與休息</td><td>先確認兩景點是否適合同日串聯</td><td>以區間表示</td><td>門票、交通票券</td></tr><tr><td>Day 3</td><td>上午至晚上</td><td>一個主要寺廟，下午安排美食或市場</td><td>依當日人流調整</td><td>以區間表示</td><td>餐廳是否需預約</td></tr><tr><td>Day 4</td><td>上午至返程</td><td>一個近住宿地點的景點，再前往返程交通點</td><td>預留行李與移動緩衝</td><td>以區間表示</td><td>返程時間</td></tr></tbody></table></div></div></div>
</div>
<table>
<thead><tr><th>你交代的條件</th><th>在完成品中檢查哪裡</th><th>判斷理由</th></tr></thead>
<tbody><tr><td>每人 40,000 元</td><td>最後的預算分配區間與各日預估花費</td><td>不能把區間寫成已查證的實際報價，也要留下機票是否計入的待確認位置。</td></tr><tr><td>寺廟與美食</td><td>活動與用餐方向</td><td>偏好要反映在內容裡；只寫在提示詞中還不夠。</td></tr><tr><td>每天最多兩個主要景點</td><td>Day 1–Day 4 的活動數量</td><td>可直接數出主要景點，並看見休息與緩衝。</td></tr><tr><td>尚未確定的資料</td><td>開頭四個問題與各日待確認欄</td><td>未知資料被標示出來，沒有變成看似確定的事實。</td></tr></tbody>
</table>
<p class="body-text">預算可先拆為住宿、當地交通、餐食、門票與備用金五類；國際機票是否納入仍是待確認事項。這份表用來讓阿凱看見要補的資料與取捨；當期價格仍需另外查證。</p>
<p class="body-text"><strong>教學用區間示意（非即時報價）：</strong>以下先以每人 40,000 元、國際機票未計入為例；實際金額要依同行人數、日期、住宿與交通查證後再改寫。</p>
<table><thead><tr><th>預算項目</th><th>示意區間</th><th>目前狀態</th></tr></thead><tbody><tr><td>住宿</td><td>18,000–22,000 元</td><td>待確認住宿區域與房型</td></tr><tr><td>當地交通</td><td>3,000–5,000 元</td><td>待確認機場、住宿與景點位置</td></tr><tr><td>餐食</td><td>6,000–8,000 元</td><td>依餐廳等級與用餐次數調整</td></tr><tr><td>門票</td><td>2,000–3,000 元</td><td>待確認實際景點與票種</td></tr><tr><td>備用金</td><td>2,000–4,000 元</td><td>保留彈性，不等於必要支出</td></tr><tr><td><strong>小計</strong></td><td><strong>31,000–42,000 元</strong></td><td>可能超出 40,000，需做取捨</td></tr></tbody></table>
<p class="body-text">如果第一版每天塞入三到四個景點，這一輪檢查「行程密度改變後，哪些取捨與缺資料會跟著改變」：</p>
<div class="code-block">請保留原本四天的景點方向與預算分配，把每天的主要景點上限改成 1 個。請另外列出：因此增加的緩衝、可能失去的景點、交通與用餐安排是否需要重新確認。其他原始偏好不要自行改寫。</div>
<div class="scenario-grid"><div class="scenario-row"><div class="scenario-task">第一版</div><div class="scenario-pick">可能每天安排三到四個景點；先保留原版，記下原本的移動壓力與待確認資料。</div></div><div class="scenario-row"><div class="scenario-task">條件敏感性版本</div><div class="scenario-pick">每天最多一個主要景點；寺廟、美食、預算分配與四天方向保持不變，同時列出增加的休息、放棄的景點與需要重查的交通時間。</div></div><div class="scenario-row"><div class="scenario-task">決策判讀</div><div class="scenario-pick">這次比較要找出密度變化造成的取捨，不能因此宣布任何版本一定更好。若同時改日期、預算、交通方式或休息時間，就不能判斷是哪個條件造成差異。</div></div></div>
<div class="scenario-grid"><div class="scenario-row"><div class="scenario-task">轉移練習的規則</div><div class="scenario-pick">冷氣比較不重播完整 Demo。進入下方同步練習後，才開啟<a href="assets/datasets/unit4-air-conditioner-comparison.md">自選素材</a>，用同一組標準比較兩個方案；這裡只保留規則：相同欄位、缺資料標記、取捨與人工確認。</div></div><div class="scenario-row"><div class="scenario-task">唯一變因</div><div class="scenario-pick">京都 Demo 改變的是「每天最多兩個主要景點」；冷氣同步練習改變的是「資料素材與方案」，不再同時展示另一份完整表格。學員要指出哪個標準造成差異。</div></div></div>
<div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>示範判斷點</strong>　提示詞產生的是規劃初稿；它沒有自動知道你的同行人數、所在位置、當日價格或營業狀態。完成判斷要看條件是否進入結果，也要看哪些內容仍標示為待確認。</div></div>
</details></section>
<hr class="section-rule"/>
<section class="lesson-section" id="lesson-practice"><details class="workbench-disclosure"><summary>課後練習：用自己的生活需求比較方案</summary><p>完成本章作品後，可依需要查看下方範例。請自行核對，不需要其他學員的檔案。</p>
<div class="section-eyebrow">(04) 個人化實作</div>
<h2 class="section-heading">課後選做：購物比較與生活決策卡</h2>
<p class="body-text">剛才看到「40,000 元」如何從已知條件進入預算區間，也看到行程密度改變後哪些取捨與待確認資料跟著變化。現在把同一個「標準 → 證據 → 取捨 → 下一步」方法帶到購物，再選一張真正和你有關的卡完成自己的應用卡。</p>
<h3 class="section-heading">購物比較範例</h3>
<p class="body-text">先開啟 <a href="assets/datasets/unit4-air-conditioner-comparison.md">課堂冷氣比較自選素材</a>，把兩款冷氣的規格與價格貼入工具。這裡的「只使用提供資料」意思是：規格表沒有寫的內容就寫「未提供」，不把模型自行產生的評價當成查證資料；本次 Together 固定使用這份自選素材，避免每個人的商品資料不同。</p>
<div class="code-block">請根據我提供的兩款冷氣規格與價格，整理比較表：冷房能力、能源效率、噪音、保固、價格、適合的房間條件。只使用提供的資料，沒有資料就寫「未提供」。最後列出 3 個購買前需要人工確認的問題，不要直接宣布哪一台一定比較好。</div>
<p class="body-text"><strong>先看一份合格輸出，再操作自己的版本：</strong>這份結果只使用自選素材；它保留取捨，但不替人宣布最後答案。</p>
<table>
<thead><tr><th>比較欄位</th><th>清風 A12</th><th>節能 B12</th><th>判讀</th></tr></thead>
<tbody>
<tr><td>冷房能力</td><td>2.8 kW</td><td>2.8 kW</td><td>素材沒有提供差異</td></tr>
<tr><td>能源效率</td><td>CSPF 5.8</td><td>CSPF 6.4</td><td>B12 數值較高，但長期電費仍需依使用情境估算</td></tr>
<tr><td>噪音</td><td>最低 23 dB</td><td>最低 25 dB</td><td>A12 的最低噪音數值較低；仍要確認實際運轉模式</td></tr>
<tr><td>保固</td><td>全機 1 年、壓縮機 5 年</td><td>全機 2 年、壓縮機 5 年</td><td>B12 的全機保固較長</td></tr>
<tr><td>練習價格</td><td>26,900 元</td><td>31,900 元</td><td>A12 價格較低；這不是即時報價</td></tr>
<tr><td>尺寸／安裝費／促銷</td><td colspan="2">未提供</td><td>不能從表格推算，需向店家確認</td></tr>
</tbody>
</table>
<p class="body-text"><strong>示範判斷：</strong>如果最在意價格與較低噪音，A12 目前較符合；如果更重視能源效率與全機保固，B12 有優勢。最後仍要確認室內機尺寸、安裝費與當期價格。這是依標準說明取捨，不是替所有人做同一個推薦。</p>
<div class="scenario-grid"><div class="scenario-row"><div class="scenario-task">第一次檢查</div><div class="scenario-pick">是否把冷房能力、能源效率、噪音、保固、價格與房間條件分開列出；沒有資料的格子是否寫「未提供」。</div></div><div class="scenario-row"><div class="scenario-task">出現額外評價</div><div class="scenario-pick">補上「只使用提供資料」後重問；保留第一版，標記哪些句子來自素材、哪些內容仍待確認。</div></div></div>
<p class="body-text">第一次使用「Checkpoint」前先定義它：Checkpoint 是操作中的停站檢查，會告訴你現在應該看到什麼、沒看到時回哪裡、通過後才能做什麼。這次每一站都改變一個決策狀態：先定義問題，再建立標準，再比較證據。</p>
<div class="steps-wrap">
<div class="step-block"><div class="step-circle">1</div><div class="step-content"><div class="step-heading">步驟 1｜定義一個真正要做的決定｜U4-FRAME</div><div class="step-body"><strong>學員操作：</strong>到上方<a href="#lifestyle-workbench">生活決策工作台</a>，從旅遊、購物、學習、健康、家庭中選一個近期決定；寫成「我要在 A 與 B 之間依哪些標準做選擇」，不要只寫「幫我規劃」。<br><strong>預期結果：</strong>工作台出現決策問題、至少三項選擇標準與優先順序。<br><strong>快速檢查：</strong>標準能被比較，例如安靜、總成本、所需時間；「感覺好」無法驗收。<br/><strong>卡住時：</strong>標準太抽象 → 追問「我要觀察什麼才知道符合」；資料未知 → 先填「待確認」，不要自行補上。</br></br></div><p>你完成的是判斷規則，接著再讓工具依規則整理選項。</p></div></div>
<div class="step-block"><div class="step-circle">2</div><div class="step-content"><div class="step-heading">步驟 2｜用同一組標準比較方案｜U4-TRADEOFF</div><div class="step-body"><strong>學員操作：</strong>使用冷氣自選素材或自己的兩個方案，把決策問題、標準、優先順序與資料邊界送給文字型 LLM；要求每個方案逐項對照同一組標準。<br/><strong>預期結果：</strong>得到方案／符合標準／優點／代價／缺資料的比較表。<br/><strong>快速檢查：</strong>每個方案都被同樣比較，沒有只替其中一個方案寫理由。<br/><strong>卡住時：</strong>回答只剩推薦句 → 回到 U4-TRADEOFF，補上「每個方案都列優點、代價與待確認事項」。</div><p>這一步把「哪個最好」改成可檢查的取捨。</p></div></div>
<div class="step-block"><div class="step-circle">3</div><div class="step-content"><div class="step-heading">步驟 3｜把缺資料與邊界標出來｜U4-MISSING</div><div class="step-body"><strong>學員操作：</strong>逐項對照比較表，將未提供的價格、尺寸、安裝、庫存、資格或專業判定列入缺資料清單；分開「可以用現有資料判斷」與「必須人工確認」。<br/><strong>預期結果：</strong>工作台的檢查欄位能指出哪些結論只有部分支持，以及下一個要查的資料。<br/><strong>快速檢查：</strong>沒有把練習價格當即時報價，也沒有把模型的推論當成商品保證。<br/><strong>卡住時：</strong>不確定是否能判斷 → 回到 U4-MISSING，先寫「目前無法由提供資料判斷」，再列出一個確認問題。</div><p>缺資料要保留在決策卡中，並標記人工確認。</p></div></div>
</div>
<div class="callout tip"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>Checkpoint 1｜決策框架完整</strong>　現在應該看到：一個近期決策、至少三項標準與優先順序、一張用同一組標準製成的比較表，以及至少一個缺資料／人工確認位置。若沒看到：回到 U4-FRAME 補標準，不要先接受模型推薦。</div></div>
<div class="steps-wrap">
<div class="step-block"><div class="step-circle">4</div><div class="step-content"><div class="step-heading">步驟 4｜處理互相衝突的條件｜U4-TRADEOFF</div><div class="step-body"><strong>學員操作：</strong>從比較表選一組互相衝突的條件，例如預算與安靜；寫出優先順序、保留什麼、犧牲什麼，再把「若這項條件改變，方案排序如何改」寫進工作台的取捨欄。<br/><strong>預期結果：</strong>工作台有一段可追溯的取捨說明，並附上推薦理由與依據。<br/><strong>快速檢查：</strong>能指出哪個標準造成差異，且沒有把未提供資料補成事實。<br/><strong>卡住時：</strong>兩個條件都想保留 → 回到 U4-TRADEOFF，先只選一個優先標準，再重寫取捨。</div><p>這一步把比較結果轉成可解釋的暫定選擇，下一步才進入邊界與人工確認。</p></div></div>
<div class="step-block"><div class="step-circle">5</div><div class="step-content"><div class="step-heading">步驟 5｜寫出取捨與暫定選擇｜U4-BOUNDARY</div><div class="step-body"><strong>學員操作：</strong>根據優先順序，寫出每個方案得到什麼、放棄什麼，以及你目前偏向哪個方案；若關鍵資料尚未確認，就把選擇寫成「暫定」並列出確認問題。<br/><strong>預期結果：</strong>決策卡還要包含取捨說明、暫定選擇與下一步。<br/><strong>快速檢查：</strong>能用一句話說出「哪個標準造成差異」與「最後仍由誰確認」。<br/><strong>卡住時：</strong>想把未知補成肯定 → 回到 U4-BOUNDARY，改成「目前無法判斷」並保留人工確認。</div><p>你把工具的整理結果轉成自己的決策依據，同時保留決定權。</p></div></div>
<div class="step-block"><div class="step-circle">6</div><div class="step-content"><div class="step-heading">步驟 6（Solo）｜把一項真實任務完成為決策卡｜U4-SOLO</div><div class="step-body"><strong>學員操作：</strong>從 30 張卡中選一個和自己近期任務相關的主題，重做步驟 1–5；健康類只能做規劃、整理或就醫提問清單，專業判定寫「需要向專業人員確認」。<br/><strong>預期結果：</strong>你有一份自己的決策問題、標準／優先順序、比較、取捨、缺資料與下一步。<br/><strong>快速檢查：</strong>這份卡換一個日期、預算或偏好後仍能重做，而且不把工具當成最後決策者。<br/><strong>卡住時：</strong>主題太大 → 只保留一個決策；資料不足 → 先完成比較框架並列出要查的問題。</div><p>這才是 30 張提示詞卡的用途：提供不同問題入口，不把 30 張重複做成課堂時數。</p></div></div>
<div class="step-block"><div class="step-circle">7</div><div class="step-content"><div class="step-heading">步驟 7｜從工作台匯出生活決策卡｜U4-SAVE</div><div class="step-body"><strong>學員操作：</strong>回到工作台確認決策問題、標準／優先順序、比較結果、取捨、缺資料、下一步與完成檢核都已填寫，按「匯出 Markdown」下載 <code>unit4-decision-card.md</code>。<br/><strong>預期結果：</strong>匯出文件不靠課堂口頭說明，也能看出你依什麼標準比較、哪些地方不能由現有資料判斷。<br/><strong>快速檢查：</strong>打開匯出文件，能找到方案取捨與下一個人工確認問題。<br/><strong>卡住時：</strong>缺少標準或缺資料 → 回到工作台對應欄位補回；匯出失敗時改用「列印工作台」保存 PDF，或開啟 Markdown 離線備援。</div><p>決策卡是你的課後起點；下次只替換資料與條件，就能保留同一套比較規格重新產生。</p></div></div>
</div>
<div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>Checkpoint 2｜生活決策卡可重做</strong>　現在應該看到：決策問題、至少三項標準與優先順序、方案比較、取捨、缺資料、下一步與完成檢核都在同一份文件；未知資訊沒有被寫成事實，最後選擇仍由你確認。若沒看到：回到 U4-SAVE 補缺少的段落。通過後才能把這張卡帶回下週的真實任務。</div></div>
</details></section>
<hr class="section-rule"/>
<section class="lesson-section" id="lesson-check"><div class="section-eyebrow">(05) 個人驗收</div><h2 class="section-heading">完成後，重開檔案做最後檢查</h2><p class="body-text">檢查：兩方案與三項標準都有比較；限制有算式；只改一項條件後重新判斷；取捨、待確認與下一步都在；正文已預覽為一頁；匯出檔能重開。人工整理或模型待重跑請如實標記。</p><div class="verify-box"><p class="verify-text">只看匯出檔，回答「交給誰、依據在哪裡、還缺什麼、下一步由誰做」。答不出時，回自己的資料與修訂步驟補齊。</p></div><p class="body-text"><a href="#lifestyle-workbench">回保存台匯出</a>；<a href="#workplace-practice">回工作實作步驟修復</a>。</p></section>
<hr class="section-rule"/>
<section class="lesson-section" id="lesson-assets"><details class="workbench-disclosure"><summary>課後素材與離線備援</summary><p class="body-text">下列生活素材供課後選題或離線使用。課堂只完成所選的一案。</p>
<div class="section-eyebrow">(06) 試跑包</div>
<h2 class="section-heading">把 30 張決策入口卡帶走</h2>
<p class="body-text">這一節是課後工具箱，不要求你把 30 張全部跑完。前面已用京都與冷氣完成「標準—比較—取捨—缺資料」示範，現在保留各類卡片，讓你下次從不同生活問題開始，再回到同一套決策框架。也可以再次開啟 <a href="assets/prompts/unit4-lifestyle-prompts.md">原始 Markdown 提示詞資產</a>；若連結無法使用，以下內容就是可複製的備援。</p>
<div class="tool-grid">
<div class="tool-card"><div class="tool-name">先看五種生活案例的完成樣子</div><div class="tool-tag">示範對照</div><div class="tool-summary">30 張卡提供選題；下面五個短案例先讓你看到同一套「條件—比較—缺資料—下一步」如何落地。</div><div class="scenario-grid">
<div class="scenario-row"><div class="scenario-task">旅遊</div><div class="scenario-pick"><strong>輸入：</strong>四天三夜京都、每人 40,000 元、喜歡寺廟和美食、每天最多兩個主要景點。<br/><strong>成品應有：</strong>每日行程、預算區間、休息緩衝與交通／票價待確認。</div></div>
<div class="scenario-row"><div class="scenario-task">購物</div><div class="scenario-pick"><strong>輸入：</strong>清風 A12 與節能 B12 的共同規格表。<br/><strong>成品應有：</strong>相同欄位比較、各自優點與代價、尺寸／安裝費／當期價格的確認問題。</div></div>
<div class="scenario-row"><div class="scenario-task">學習</div><div class="scenario-pick"><strong>輸入：</strong>三個月學會基礎日文，每週投入 4 小時，目前只會平假名。<br/><strong>成品應有：</strong>每週目標、練習、完成證據與落後時的替代任務；不能只列教材清單。</div></div>
<div class="scenario-row"><div class="scenario-task">健康整理</div><div class="scenario-pick"><strong>輸入：</strong>整理最近一週的症狀時間線，準備下次就醫提問。<br/><strong>成品應有：</strong>觀察到的事實、時間線、想詢問的問題與需要專業確認的地方，不做診斷。</div></div>
<div class="scenario-row"><div class="scenario-task">家庭安排</div><div class="scenario-pick"><strong>輸入：</strong>四人家庭一週晚餐，預算 2,800 元，每天最多 30 分鐘，家中已有米和雞蛋。<br/><strong>成品應有：</strong>菜單、準備時間、採買清單、可重複使用的食材與過敏／營養需求待確認。</div></div>
</div></div>
<div class="tool-card"><div class="tool-name">A. 旅遊規劃｜01–06</div><div class="tool-tag">6 張</div><div class="tool-summary">把地點、天數、人數、預算、偏好與待確認資訊放進旅行初稿。</div>
<details><summary>01｜行程規劃</summary><p><strong>背景：</strong>我要安排[地點]的[天數]天旅行，同行[人數]人，預算每人[金額]，喜歡[偏好]，每天可活動[時段]。</p><p><strong>任務：</strong>請提出一份適合我的行程初稿。</p><p><strong>限制：</strong>每天最多[主要景點數]個主要景點，保留[休息時間]；沒有日期、即時價格或營業時間就標「待確認」。</p><p><strong>輸出格式：</strong>表格列出日期／時段／活動／移動方向／用餐方向／預算區間／待確認。</p></details>
<details><summary>02｜景點推薦</summary><p><strong>背景：</strong>我會在[地點]停留[天數]天，喜歡[興趣]，不喜歡[避開事項]，同行者有[年齡或行動需求]。</p><p><strong>任務：</strong>請推薦[數量]個景點，讓我能依偏好挑選。</p><p><strong>限制：</strong>每個景點說明適合原因、可能負擔與需要先確認的資訊，不要只用熱門程度排序。</p><p><strong>輸出格式：</strong>表格列出景點／符合的偏好／所需時間／可能限制／待查資訊。</p></details>
<details><summary>03｜預算試算</summary><p><strong>背景：</strong>我要去[地點][天數]天，[人數]人，總預算[金額]；已知住宿約[金額]、交通約[金額]、每日餐食上限[金額]。</p><p><strong>任務：</strong>請協助我建立預算分配與三種花費情境。</p><p><strong>限制：</strong>只能使用上述數字；未知費用用區間或「待確認」，不要假裝是即時報價。</p><p><strong>輸出格式：</strong>列出基本／節省／寬鬆三種情境，各含項目、估算、剩餘與超支風險。</p></details>
<details><summary>04｜交通安排</summary><p><strong>背景：</strong>我要從[出發地]前往[目的地]，旅行期間為[日期或天數]，同行[人數]人；希望[省錢／省時間／少轉乘]。</p><p><strong>任務：</strong>請比較[數量]種交通安排。</p><p><strong>限制：</strong>分開列出已知與需查的票價、班次、轉乘與時間，不要捏造即時班次。</p><p><strong>輸出格式：</strong>表格列出方案／優點／代價／適合情況／使用前要確認。</p></details>
<details><summary>05｜餐廳挑選</summary><p><strong>背景：</strong>我在[地點]想找[餐別]，預算每人[金額]，同行者有[飲食偏好或限制]，用餐時間約[時間]。</p><p><strong>任務：</strong>請建立挑選餐廳的條件與候選清單。</p><p><strong>限制：</strong>沒有即時營業、訂位或菜單資料就標「待確認」；不要用未提供的評價替餐廳排名。</p><p><strong>輸出格式：</strong>先列篩選條件，再列[3–5]個候選方向、適合原因與確認事項。</p></details>
<details><summary>06｜行李打包</summary><p><strong>背景：</strong>我要去[地點]旅行[天數]天，季節／天氣條件為[條件]，活動包含[活動]，只帶[行李限制]。</p><p><strong>任務：</strong>請整理一份不容易漏帶的行李清單。</p><p><strong>限制：</strong>依活動與天數分組，標示必帶／可選／出發前確認；不推測當地天氣，需查的內容標出。</p><p><strong>輸出格式：</strong>衣物、盥洗、文件、電子用品、活動用品、備用物品六類清單。</p></details>
</div>
</div>
<div class="tool-grid">
<div class="tool-card"><div class="tool-name">B. 購物決策｜07–12</div><div class="tool-tag">6 張</div><div class="tool-summary">保留規格、價格、取捨與購買前待確認問題。</div>
<details><summary>07｜商品比較</summary><p><strong>背景：</strong>我在比較[商品 A]與[商品 B]，使用情境是[情境]，預算上限[金額]，最在意[優先條件]。</p><p><strong>任務：</strong>請根據我提供的規格與價格建立比較表。</p><p><strong>限制：</strong>只使用提供資料；缺少規格寫「未提供」；不要直接宣布哪個一定最好。</p><p><strong>輸出格式：</strong>規格／價格／符合需求程度／取捨／購買前待確認問題。</p></details>
<details><summary>08｜規格分析</summary><p><strong>背景：</strong>我想買[商品類型]，空間／使用量／頻率為[條件]，目前看到的規格有[規格資料]。</p><p><strong>任務：</strong>請把規格翻成一般人能理解的使用差異。</p><p><strong>限制：</strong>保留原始單位與數字；不把規格推成未提供的實際效能。</p><p><strong>輸出格式：</strong>規格欄位／白話意思／對我的影響／還缺哪項資料。</p></details>
<details><summary>09｜評價彙整</summary><p><strong>背景：</strong>我有[商品]的多則使用者評價，購買時最在意[耐用／操作／售後等]。</p><p><strong>任務：</strong>請依主題整理評價中反覆出現的支持與抱怨。</p><p><strong>限制：</strong>區分「多人提到」與「單一個案」；不要把評價推論成所有人都會遇到。</p><p><strong>輸出格式：</strong>主題／支持觀察／疑慮／出現次數或原文依據／我還要確認什麼。</p></details>
<details><summary>10｜議價話術</summary><p><strong>背景：</strong>我想向[賣方]詢問[商品]，目前看到的價格是[金額]，我能接受的預算是[金額]，希望保持[禮貌／直接]。</p><p><strong>任務：</strong>請寫出三種不失禮的詢問價格或加購方案說法。</p><p><strong>限制：</strong>不威脅、不假裝有其他報價；明確分開「詢問」與「已談定」。</p><p><strong>輸出格式：</strong>保守版／直接版／詢問附加服務版，每版 2–3 句。</p></details>
<details><summary>11｜退貨應對</summary><p><strong>背景：</strong>我在[日期]於[通路]購買[商品]，遇到[問題]，目前有[訂單／保固／照片等資料]。</p><p><strong>任務：</strong>請幫我整理一段客觀的退貨或售後詢問文字。</p><p><strong>限制：</strong>只陳述我提供的事實，不宣稱對方一定違約或一定能退款；把需要依規定確認的地方列出。</p><p><strong>輸出格式：</strong>事情摘要／希望對方協助／附件或資料／待確認條件。</p></details>
<details><summary>12｜購買時機建議</summary><p><strong>背景：</strong>我想買[商品]，預算[金額]，使用期限是[日期或情境]，現在有[價格或促銷資訊]。</p><p><strong>任務：</strong>請用「現在買／等待／先租借或替代」三種方案幫我比較。</p><p><strong>限制：</strong>不要假定未提供的降價日期；將急用程度、總成本與等待代價分開。</p><p><strong>輸出格式：</strong>方案／適合條件／好處／代價／我需要補查的資訊。</p></details>
</div>
</div>
<div class="tool-grid">
<div class="tool-card"><div class="tool-name">C. 學習進修｜13–18</div><div class="tool-tag">6 張</div><div class="tool-summary">把期限、程度、投入時間與完成證據變成可以追蹤的學習任務。</div>
<details><summary>13｜讀書計畫</summary><p><strong>背景：</strong>我想在[期限]前學會[主題]，每週可投入[時間]，目前程度是[程度]，目標是[可觀察成果]。</p><p><strong>任務：</strong>請安排一份可執行的學習計畫。</p><p><strong>限制：</strong>每週最多安排[時數]；每一週要有練習與檢查，閱讀清單不能單獨作為完成證據。</p><p><strong>輸出格式：</strong>週次／本週目標／練習／完成證據／卡住時的替代任務。</p></details>
<details><summary>14｜知識解釋</summary><p><strong>背景：</strong>我想理解[概念]，目前知道[已有理解]，會用在[情境]。</p><p><strong>任務：</strong>請用由簡入深的方式解釋。</p><p><strong>限制：</strong>先用一句話，再用生活例子；把容易混淆的概念列出；不確定處標示需查證。</p><p><strong>輸出格式：</strong>一句話／例子／三個重點／常見誤解／自我檢查題。</p></details>
<details><summary>15｜考試準備</summary><p><strong>背景：</strong>我要準備[考試或測驗]，距離考試[天數]天，範圍是[範圍]，弱點是[弱點]，每天可讀[時間]。</p><p><strong>任務：</strong>請安排複習順序與練習節奏。</p><p><strong>限制：</strong>保留休息與回顧時間；不要保證一定能考到某分數；每個階段要有檢查方式。</p><p><strong>輸出格式：</strong>日期／主題／練習／檢查／若落後一天怎麼調整。</p></details>
<details><summary>16｜教材推薦</summary><p><strong>背景：</strong>我想學[主題]，程度[程度]，預算[金額]，偏好[影片／書籍／實作]，每週[時間]。</p><p><strong>任務：</strong>請建立選教材的條件與候選類型。</p><p><strong>限制：</strong>不要捏造不存在的教材或最新評價；先給挑選標準，再列待查方向。</p><p><strong>輸出格式：</strong>挑選條件／適合的教材類型／優缺點／開始前要確認。</p></details>
<details><summary>17｜進度追蹤</summary><p><strong>背景：</strong>我的學習目標是[目標]，已完成[已完成事項]，剩下[待完成事項]，本週可用時間[時間]。</p><p><strong>任務：</strong>請把進度整理成下週可執行的任務表。</p><p><strong>限制：</strong>不要把「看過」算成「會做」；每項任務都要有完成證據。</p><p><strong>輸出格式：</strong>任務／預計時間／完成證據／依賴事項／下次檢查日。</p></details>
<details><summary>18｜學習瓶頸排解</summary><p><strong>背景：</strong>我在學[主題]，目前卡在[具體問題]，已試過[方法]，能投入[時間]。</p><p><strong>任務：</strong>請提出三種可能原因與低成本測試方法。</p><p><strong>限制：</strong>先問最多 3 個關鍵澄清問題；不要只用「更努力」當建議。</p><p><strong>輸出格式：</strong>可能原因／10–30 分鐘測試／觀察結果／下一步。</p></details>
</div>
</div>
<div class="tool-grid">
<div class="tool-card"><div class="tool-name">D. 健康生活｜19–24</div><div class="tool-tag">6 張</div><div class="tool-summary">只協助整理與規劃；涉及症狀、藥品、檢查結果或治療判定時，改成準備向專業人員詢問的問題。</div>
<details><summary>19｜飲食建議</summary><p><strong>背景：</strong>我想安排[天數]天的日常飲食，作息是[作息]，偏好[口味]，不吃[食材]，每餐預算約[金額]。</p><p><strong>任務：</strong>請提出容易執行的餐點方向與採買清單。</p><p><strong>限制：</strong>不做疾病治療或個人營養診斷；將需要依個人狀況確認的地方標出。</p><p><strong>輸出格式：</strong>每日餐次／餐點方向／準備時間／採買清單／需要專業確認。</p></details>
<details><summary>20｜運動規劃</summary><p><strong>背景：</strong>我想在[期限]前建立每週[次數]次運動習慣，每次[分鐘]，目前活動量[程度]，可使用的場地或器材是[條件]。</p><p><strong>任務：</strong>請排一份循序漸進的入門運動計畫。</p><p><strong>限制：</strong>以習慣建立為主，不宣稱治療或保證效果；列出停止或尋求專業建議的情況。</p><p><strong>輸出格式：</strong>週次／運動內容／時間／強度感受／替代方案／需要確認。</p></details>
<details><summary>21｜症狀說明</summary><p><strong>背景：</strong>我想整理自己觀察到的[症狀描述]，開始時間[時間]，頻率[頻率]，伴隨現象[現象]。</p><p><strong>任務：</strong>請幫我整理成就醫時可以清楚說明的紀錄與提問清單。</p><p><strong>限制：</strong>不要診斷、不要推測病因、不要建議自行停藥；不確定內容標成待向專業人員確認。</p><p><strong>輸出格式：</strong>時間線／已觀察現象／影響日常的地方／想詢問的問題／就醫前要帶的紀錄。</p></details>
<details><summary>22｜藥品說明</summary><p><strong>背景：</strong>我需要理解一份藥品或處方說明，已知資料是[說明文字]，我想了解[用法／注意事項／需要詢問的地方]。</p><p><strong>任務：</strong>請把文字改寫成一般人能讀懂的重點。</p><p><strong>限制：</strong>只解釋提供的文字，不替我決定是否服用、調整劑量或混用；不清楚的地方列為詢問事項。</p><p><strong>輸出格式：</strong>用途文字／使用方式／注意事項／原文未說明／要向專業人員確認。</p></details>
<details><summary>23｜就醫準備</summary><p><strong>背景：</strong>我要為[就醫目的]準備，最近的狀況與紀錄是[資料]，希望在有限時間內問清楚[問題]。</p><p><strong>任務：</strong>請整理一份就醫前摘要與問題清單。</p><p><strong>限制：</strong>分開「我觀察到的事實」與「我想知道的問題」；不要先替我下結論。</p><p><strong>輸出格式：</strong>30 秒摘要／時間線／目前用藥或檢查資料欄位／優先提問 5 題。</p></details>
<details><summary>24｜健檢報告解讀</summary><p><strong>背景：</strong>我想理解健檢報告中的[項目]，報告原文是[貼上可使用的文字]，我想知道它在報告中代表什麼。</p><p><strong>任務：</strong>請逐項用白話解釋報告文字，並整理回診時要問的問題。</p><p><strong>限制：</strong>不要診斷或預測；保留數值、單位、參考範圍與報告日期；無法從文字判定的地方標出。</p><p><strong>輸出格式：</strong>項目／報告數值／參考範圍／白話說明／需要專業確認的問題。</p></details>
</div>
</div>
<div class="tool-grid">
<div class="tool-card"><div class="tool-name">E. 家庭應用｜25–30</div><div class="tool-tag">6 張</div><div class="tool-summary">把家庭成員、時間、預算、材料與備案寫成可共同使用的安排。</div>
<details><summary>25｜家庭菜單</summary><p><strong>背景：</strong>家中有[人數與年齡]，一週晚餐預算[金額]，不吃[食材]，可下廚時間[時間]，家中已有[食材]。</p><p><strong>任務：</strong>請安排一週晚餐與採買清單。</p><p><strong>限制：</strong>重複利用部分食材以減少浪費；每餐標準備時間；未提供的過敏或營養需求列為要確認。</p><p><strong>輸出格式：</strong>日期／菜色／準備時間／可提前處理／採買清單／待確認。</p></details>
<details><summary>26｜節慶安排</summary><p><strong>背景：</strong>我們要在[日期]安排[節慶活動]，參加者有[人數與年齡]，預算[金額]，希望有[傳統／簡單／親子]氣氛。</p><p><strong>任務：</strong>請提出一份從準備到收尾的活動流程。</p><p><strong>限制：</strong>每天或每段活動保留緩衝；把需要先預訂或購買的項目列出，不自行假定場地可用。</p><p><strong>輸出格式：</strong>時間／活動／負責人／材料／預算／備案。</p></details>
<details><summary>27｜家事管理</summary><p><strong>背景：</strong>家中有[人數]，房間與家事包括[清單]，每週可共同整理[時間]，目前最困擾的是[問題]。</p><p><strong>任務：</strong>請建立公平且容易維持的家事分工表。</p><p><strong>限制：</strong>考慮每個人的可用時間與能力；每項任務要有頻率與完成標準，不用責備語氣。</p><p><strong>輸出格式：</strong>任務／頻率／預估時間／負責人／共同完成標準／備援。</p></details>
<details><summary>28｜親子活動</summary><p><strong>背景：</strong>我想和[年齡]歲孩子在[時間長度]內做活動，場地[室內／戶外]，可用材料[材料]，希望練習[能力或主題]。</p><p><strong>任務：</strong>請提出三個適齡活動。</p><p><strong>限制：</strong>活動步驟不超過[步數]；材料以現有物品為主；列出需要大人陪同與可調整難度的地方。</p><p><strong>輸出格式：</strong>活動名稱／準備／步驟／孩子可做的部分／大人協助／收尾提問。</p></details>
<details><summary>29｜家庭旅遊</summary><p><strong>背景：</strong>我們有[人數與年齡]要去[地點][天數]天，預算[金額]，成員偏好與需要照顧的條件是[條件]。</p><p><strong>任務：</strong>請安排一份不趕行程的家庭旅遊初稿。</p><p><strong>限制：</strong>每天最多[景點數]個主要活動，安排休息與雨天備案；交通、票價、營業時間未知處列為待確認。</p><p><strong>輸出格式：</strong>日期／活動／移動／休息／餐食方向／預算區間／家庭成員注意事項。</p></details>
<details><summary>30｜年節禮品選購</summary><p><strong>背景：</strong>我要為[對象人數與關係]準備禮品，總預算[金額]，希望符合[口味／實用／方便攜帶]，避免[限制]。</p><p><strong>任務：</strong>請提出三種採買組合。</p><p><strong>限制：</strong>不假定收件者一定喜歡；把價格、保存、攜帶與替代方案分開；即時庫存與價格標為待確認。</p><p><strong>輸出格式：</strong>組合／適合對象／內容方向／預算／優點／取捨／購買前確認。</p></details>
</div>
</div>
<div class="tool-card"><div class="tool-name">生活決策卡工作表</div><div class="tool-tag">離線／印刷備援</div><div class="tool-summary">頁面工作台是主線；這份 Markdown 只在離線、列印或頁面暫時無法使用時，承接決策問題、標準、比較、取捨與缺資料。</div><div class="code-block">我選的決策情境：＿＿＿＿＿＿＿＿＿＿

我的目標：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
我的時間：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
我的預算：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
我的偏好：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
我的限制：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
必須出現在輸出的條件：＿＿＿＿＿＿＿＿＿＿＿＿

第一版中沒有出現的條件或缺資料：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
我本輪補查／補上的條件：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
方案 A／B 各自得到與放棄什麼：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
我的暫定選擇、下一步與人工確認：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</div></div>
</details></section>
<hr class="section-rule"/>
<section class="lesson-section"><details class="workbench-disclosure"><summary>課後查閱：常見問題與修正方法</summary>
<div class="section-eyebrow">(07) 常見錯誤</div>
<h2 class="section-heading">結果不合用時，回到對應階段修</h2>
<p class="body-text">常見問題是輸入裡少了一個可檢查的條件，或修訂時同時改了太多事情。先辨認現象，再回到指定階段；保留原版，才有可比較的修復證據。</p>
<div class="troubleshoot">
<div class="ts-item"><div class="ts-label">PITFALL 01</div><div class="ts-q">比較結果只有漂亮的推薦句。</div><div class="ts-a"><strong>原因：</strong>沒有先寫選擇標準與優先順序。<br/><strong>修復：</strong>回到 U4-FRAME，補至少三項可觀察標準，再要求每個方案用同一組標準比較。</div></div>
<div class="ts-item"><div class="ts-label">PITFALL 02</div><div class="ts-q">比較表看似完整，但缺少關鍵資料。</div><div class="ts-a"><strong>原因：</strong>把「未提供」當成模型可以自行補上的欄位。<br/><strong>修復：</strong>回到 U4-MISSING，把缺資料與人工確認列成下一步，不把練習價格、資格或專業判定寫成事實。</div></div>
<div class="ts-item"><div class="ts-label">PITFALL 03</div><div class="ts-q">模型直接替你做健康或購買決定。</div><div class="ts-a"><strong>原因：</strong>問題使用「適不適合」「一定要不要買」等單一結論問法。<br/><strong>修復：</strong>回到 U4-BOUNDARY，改問差異、取捨、依據與待確認問題；健康題目改成資料整理或就醫提問清單，保留人工或專業判斷位置。</div></div>
</div>
<table>
<thead><tr><th>另一個常見現象</th><th>回復路徑</th></tr></thead>
<tbody><tr><td>方案之間不知道差在哪裡。</td><td>回到 U4-TRADEOFF，使用同一組標準列出各方案的符合處、代價與取捨。</td></tr><tr><td>輸出超出預算或缺少關鍵資料。</td><td>回到 U4-MISSING，將未知資料列為待查問題，不要求模型猜數字。</td></tr><tr><td>只有最後回答，沒有決策依據。</td><td>回到 U4-SAVE，補回決策問題、標準、比較、取捨與下一步；不要用最後回答推測原始條件。</td></tr></tbody>
</table>
</details></section>
<hr class="section-rule"/>
<section class="lesson-section" id="lesson-quiz"><details class="workbench-disclosure"><summary>課後自我檢查</summary><p>完成本章作品後，可依需要查看下方範例。請自行核對，不需要其他學員的檔案。</p>
<div class="section-eyebrow">(08) 自我檢核</div>
<h2 class="section-heading">兩題確認你能把方法帶回生活</h2>
<div class="quiz-item"><div class="quiz-q">Q1：哪一項最能把生活問題變成可比較的決策？</div><div class="quiz-opts"><label class="quiz-opt"><input name="q1" type="radio"/><span>A. 請幫我選最好的。</span></label><label class="quiz-opt"><input name="q1" type="radio"/><span>B. 請依安靜、總成本、保固三項標準比較兩個方案，標出各自代價與缺資料。</span></label><label class="quiz-opt"><input name="q1" type="radio"/><span>C. 請給我網路上最熱門的選項。</span></label><label class="quiz-opt"><input name="q1" type="radio"/><span>D. 請直接替我決定。</span></label></div><details class="quiz-ans"><summary>顯示答案</summary><div>正確答案：B。它先定義共同標準，再留下取捨與缺資料，最後決定仍由人確認。</div></details></div>
<div class="quiz-item"><div class="quiz-q">Q2：比較表缺少安裝費資料，哪個回應符合本課方法？</div><div class="quiz-opts"><label class="quiz-opt"><input name="q2" type="radio"/><span>A. 讓模型估一個看起來合理的數字。</span></label><label class="quiz-opt"><input name="q2" type="radio"/><span>B. 直接選價格較低的方案。</span></label><label class="quiz-opt correct"><input name="q2" type="radio"/><span>C. 標記「未提供」，列出向店家確認的問題，不先做最後決定。</span></label><label class="quiz-opt"><input name="q2" type="radio"/><span>D. 刪除整張比較表。</span></label></div><details class="quiz-ans"><summary>顯示答案</summary><div>正確答案：C。缺資料要成為下一步，不能被模型補成事實。</div></details></div>
</details></section>

<!-- learner-content:end -->

## 教師／歷史附錄（不列本批必做量）

以下為2026-10-08補強前的完整教案快照，保留舊流程與例子供追溯；新契約、時數與必做量依上方正文，原HTML案例已改為選做。

<details><summary>舊教案全文（歷史紀錄）</summary>

---
title: "生活決策支援：用 AI 整理條件、取捨與下一步"
slug: ai-beginner-practical
unit_id: CH4-1
chapter: CH4-1
course_type: skill-operation
duration: 3h
audience: "已完成前面單元、手上有近期生活任務的成人學習者"
prerequisites: "能讀懂 CH1 的基本提示詞、CH2 的讀者與格式判斷、CH3 的來源與待確認標記"
learning_objective: 能把一項生活需求轉成選擇標準與取捨矩陣，處理缺少資料與互相衝突的條件，完成一份可交接的生活決策卡
deliverables:
  - "一份生活任務的選擇標準與條件優先順序"
  - "一份以課堂共同資料完成的方案比較表與待確認清單"
  - "一份個人生活決策卡：選項、取捨、缺資料、第一版判斷與下一步"
  - "一個保留原始條件、修訂理由與課後重做情境的可重用完成物"
environment: "任一可輸入文字並複製回答的 LLM／對話工具（平台中立）；30 張生活任務卡作為選題庫；冷氣比較共同素材作為同步練習"
style_guide: ai-beginner-practical/STYLE-GUIDE.md
platform_version: LLM 通用方法（平台中立，NotebookLM 僅於 CH3-1 固定使用）
status: draft
---

## Learner Task Contract（學員任務契約）

| 契約欄位 | 本單元凍結事實 |
|---|---|
| 角色與工作情境 | 你手上有一項近期會遇到的旅遊、購物、學習、健康或家庭任務，需要整理選項與取捨，而不是把最後決定交給工具。 |
| 問題與後果 | 只問「幫我規劃」會讓模型猜時間、預算與偏好；若沒有列出標準與缺資料，結果可能排太滿、超預算、忽略風險或越過專業判斷。 |
| 起始材料 | CH4-1 生活應用工作台、`assets/prompts/unit4-lifestyle-prompts.md`、`assets/datasets/unit4-air-conditioner-comparison.md`、個人近期任務與可使用的文字型 LLM；工具不可用時先填條件並標待重跑。 |
| 目標完成物 | `unit4-lifestyle-application-card.md`：任務背景、選擇標準、優先順序、方案比較、缺少資料、取捨說明、下一步與人工／專業確認。 |
| 下一位使用者與用途 | 未來的你、家人或同事可用這張卡理解選項與取捨；下次只替換條件與資料，不必重新猜測決策標準。 |
| 第一個動作 | 從 30 張卡選一項近期任務，在工作台寫出目標、可用時間、預算、偏好、限制與「我最後需要做的決定」。 |
| 第一個可觀察結果 | 工作台有一個具體決定、至少三個選擇標準與一項待確認資料；沒有看到時回 `U4-FRAME`。 |
| 失敗時的回復位置 | 標準互相衝突回 `U4-TRADEOFF`；資料不足回 `U4-MISSING`；工具替你下結論回 `U4-BOUNDARY`；完成物不完整回 `U4-SAVE`。 |

## 教學流程與 180 分鐘節奏

### 1. 破題：從「推薦我一個」改成「幫我看清取捨」（0–15 分）

比較一份只給結論的購物回答與一份列出標準、證據、代價與待確認事項的決策卡。學員找出哪一份能讓另一個人理解為什麼選、如果條件改變要怎麼重做。

### 2. 概念：標準、權衡、缺資料（15–35 分）

- **選擇標準**：用來比較方案的欄位，例如價格、時間、耐用、方便。
- **優先順序**：當標準衝突時，先保留哪一項。
- **取捨**：每個方案得到什麼、犧牲什麼。
- **缺資料**：目前不能判斷，必須列出查證方式。
- **決策邊界**：工具可以整理選項，但最後的健康、財務、法律與家庭決定仍由人確認。

### 3. 完整示範：京都行程與取捨矩陣（35–70 分）

使用京都四天三夜作第一個完整 Demo，再用冷氣共同素材完成第二個完整比較案例。京都示範條件如何進入行程、預算區間、取捨與待確認清單；冷氣案例展示同一組標準如何形成比較表、缺資料與條件式判斷。HTML 另提供旅遊、購物、學習、健康整理與家庭安排五種短案例，讓學員先看完成物再選自己的生活任務。

### 4. 動手：從共同判斷到個人決策卡（70–165 分）

| 時間 | 活動 | 學員新增決策 | 產物 |
|---|---|---|---|
| 70–85 分 | Checkpoint 1：定義決策 | 這次真正要決定什麼、不能用哪個單一結論代替 | 決策句與標準清單 |
| 85–110 分 | Together：冷氣取捨 | 哪些差異是素材支持，哪些仍需查證 | 比較矩陣與確認清單 |
| 110–140 分 | Solo：個人任務 | 哪三個標準最影響自己的選擇 | 個人方案表 |
| 140–155 分 | Repair：處理衝突條件 | 預算、時間、品質衝突時保留什麼 | 取捨說明 |
| 155–165 分 | Transfer | 如果一項條件改變，決策如何變 | 情境比較與下一步 |

### HTML 顯示步驟映射

HTML 依學員每一站都要看到「操作／結果／快速檢查／卡住時」拆成連續 7 步；教案中的 Repair 活動具體落在步驟 4，不是只靠重新編號補齊畫面：

| HTML 步驟 | 回復位置 | 新增的學員判斷 |
|---|---|---|
| 1 | U4-FRAME | 定義一個近期決策與至少三項標準 |
| 2 | U4-TRADEOFF | 用同一組標準比較方案 |
| 3 | U4-MISSING | 分開已知資料、缺資料與人工確認 |
| 4 | U4-TRADEOFF | 處理互相衝突的條件，寫出保留與犧牲 |
| 5 | U4-BOUNDARY | 寫出取捨與暫定選擇，保留決定權 |
| 6 | U4-SOLO | 重做步驟 1–5，把一項近期生活任務完成為決策卡 |
| 7 | U4-SAVE | 匯出並重新開啟完成物確認可交接 |

### 5. 檢核與交接（165–180 分）

學員匯出決策卡，讓同桌只看完成物回答：這張卡要做什麼決定？比較標準是什麼？哪個資料還沒確認？如果預算或時間改變，先改哪一欄？回答不出來就回 `U4-FRAME`、`U4-TRADEOFF` 或 `U4-MISSING`。

## 完整 worked example：京都四天三夜的取捨

### 原始問題與條件化輸入

「幫我規劃京都」沒有天數、預算、偏好、節奏與輸出格式。完整提示詞只在 HTML Demo 出現一次；學員從工作台或 Demo 取得，不在同步練習重新複製。

### 教師示範判斷

| 條件 | 完成品要檢查的地方 | 判斷 |
|---|---|---|
| 每人 40,000 元 | 預算以區間呈現，且標出機票是否計入的未知 | 估算不能冒充即時報價 |
| 寺廟與美食 | 景點與用餐方向真的出現在四天安排 | 偏好不能只停在提示詞 |
| 每天最多兩個主要景點 | 可直接數出每天的主要景點與休息緩衝 | 不能用排滿行程換取完整感 |
| 未知資料 | 同行人數、住宿、抵達時間與機票列為待確認 | 不讓模型補成事實 |

如果改變「每天最多一個主要景點」，學員只比較這一個變因造成的緩衝、放棄項目與重查資料。冷氣資料留到 Together，作為不同素材的轉移，不在 Demo 內再放完整比較表。

## Demo / Together / Solo 的 Activity Identity

| 活動 | 素材 | 產物 | 操作路徑 | 學員決策 |
|---|---|---|---|---|
| Demo | 京都四天三夜條件 | 行程／預算／取捨初稿 | 從模糊需求補條件、讀中間結果、列待確認 | 哪個條件造成哪個取捨 |
| Together | 冷氣共同資料 | 方案比較與 3 個人工確認問題 | 固定欄位、比較兩方案、標未提供 | 哪些內容不能由模型補寫 |
| Solo | 30 張卡中一項近期生活任務 | 個人決策卡 | 建立標準、方案、取捨與下一步 | 預算／時間／品質衝突時先保留什麼 |

## 動手練習與驗收

1. 從 30 張卡選一項近期任務，寫出一個具體決策句。
2. 列出至少三個選擇標準，標記其中一個最重要標準與理由。
3. 讓 LLM 產出兩到三個方案，但要求分開優點、代價、依據與待確認資料。
4. 找出一個缺少資料或互相衝突的條件，寫出取捨與下一步，不要求模型直接決定。
5. 只替換時間或預算其中一項，說明方案排序是否改變，以及哪些資料要重新查。

## 試跑包需求清單

- `assets/prompts/unit4-lifestyle-prompts.md`：30 張卡作為選題與條件庫，不是 30 個課堂必做任務。
- `assets/datasets/unit4-air-conditioner-comparison.md`：Together 固定素材；只使用提供資料，沒有資料寫「未提供」。
- `assets/worksheets/unit4-lifestyle-application-card.md`：離線／印刷備援；主線由頁面工作台匯出。
- 頁面工作台：保存決策句、選擇標準、方案比較、缺資料、取捨與下一步。

## 商業情境案例

阿凱要替工作室採買冷氣。老闆問「哪台比較好」，但工作室還沒確認房間尺寸、安裝費與當期價格。阿凱不能只交一個答案，而要交一份能讓老闆看懂差異、知道缺什麼資料、依不同優先順序做決定的比較卡。

## 常見錯誤 3 條

1. **只有單一推薦**：原因是沒有列選擇標準與代價。回 `U4-FRAME` 補標準，再要求條件式結論。
2. **把缺資料補成事實**：原因是模型想讓表格看起來完整。回 `U4-MISSING`，標成「未提供」並列查證方式。
3. **衝突條件一起消失**：原因是只追求一個最終答案。回 `U4-TRADEOFF`，明列保留與犧牲的條件，再產出下一步。

## 檢核題 2 條

1. 比較兩款商品時，哪一種輸出最有助於人做最後決定？
   - A. 直接宣布哪款最好。
   - B. 只列模型的偏好。
   - C. 列出標準、差異、優點、代價、缺資料與待確認事項。
   - D. 把所有未提供資訊補齊。
   - **答案：C。**它保留人的決策位置，也讓取捨可被檢查。
2. 預算與品質互相衝突時，最合適的下一步是什麼？
   - A. 讓模型自行決定。
   - B. 把其中一個條件刪掉。
   - C. 說明保留哪個條件、犧牲哪個條件，並列出需要再確認的資料。
   - D. 重新問「哪個最適合我」。
   - **答案：C。**取捨必須透明，不能被一句推薦掩蓋。

</details>
