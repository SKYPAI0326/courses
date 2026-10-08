---
slug: gemini-ai
unit_id: CH2
title: 把需求寫成可重用的提示詞
course_type: skill-operation
version: 2026-10-09-instructor-repair
duration: 75
dependencies: ["CH1"]
learning_objective: 把需求寫成可重用的提示詞
platform_version: Gemini web; official help checked 2026-10-08; account generation pending
---

# 把需求寫成可重用的提示詞

正式正文以下列learner-content範圍為唯一來源；HTML從此範圍轉製。內部設計依據：課程根目錄 _repair/2026-10-08/CHAPTER-REDESIGN.md。
環境：桌面瀏覽器、可登入的Gemini帳號、UTF-8純文字存檔。引用的作者參考品只能證明操作／規則，不代表授課平台生成。真人跟做及六小時試教待驗。
來源：part1/CH1-2.html, part1/CH1-3.html；跨章交付段落另見遷移紀錄。

<!-- learner-content:start -->
<section class="lesson-section" id="ch2-section-1"><h2 class="section-heading">這一章，要寫出自己工作用的需求</h2><p class="body-text">第一章已有能開啟的小工具，也改過一次配色。現在換你自己說清楚要做什麼。本章用活動預算示範：從一句模糊要求，補上欄位、算法、錯誤處理與交付方式，寫成完整提示詞。看完示範就寫自己的需求，不必把所有案例都生成一次。</p><p class="body-text">本章完成物是兩份分開的文字：一份描述可重複使用的工具；另一份放這次的人名、日期、金額或設定。操作後的核對答案另外記，不跟初次生成一起貼給 AI。</p></section><section class="lesson-section" id="ch2-section-2"><h2 class="section-heading">從一句話開始，找出 AI 還不知道的事</h2><p class="body-text">原始需求：「幫我做一個活動預算工具。」這句說了用途，但沒有說明誰要填什麼、怎麼算、錯誤時怎麼辦，以及最後要拿到什麼。先用日常話把答案補出來：</p><div class="core-table-scroll"><table class="course-table" style="width:100%;border-collapse:collapse;font-size:.9rem;line-height:1.7"><thead><tr><th scope="col" style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">還缺哪件事</th><th scope="col" style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">補成能操作與核對的需求</th></tr></thead><tbody><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">使用者要填什麼？</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">每列填項目、數量、單價、實支與備註；核定預算另填，可增刪明細。</td></tr><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">工具怎麼算？</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">每列估算＝數量×單價；加總估算與實支，再算實支減估算、核定減實支。</td></tr><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">遇到錯誤怎麼辦？</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">數量空白、負數或不是數字時指出欄位，停止顯示正常總額，保留其餘輸入供修改。</td></tr><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">畫面要顯示什麼？</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">各列估算、兩種合計、差異及餘額；修改輸入後更新。</td></tr><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">最後要拿到什麼？</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">一份完整網頁檔，存好後能用瀏覽器離線開啟。</td></tr></tbody></table></div><p class="body-text">整理需求時也可檢查四件事：請誰協助、要做什麼、要遵守什麼、最後交付什麼。原先的「角色、任務、限制、交付格式」就對應這四問；不用背名稱，能把需求說清楚即可。</p></section><section class="lesson-section" id="ch2-section-3"><h2 class="section-heading">說清楚交付方式，才能照第一章存檔</h2><p class="body-text">本課要求「完整單一 HTML」，就是把畫面、外觀和操作放在同一份網頁檔。提示詞中的 CSS 與 JavaScript 全內嵌，是請 AI 把外觀和操作程式一起放進去。你仍按第一章方式保存及開啟，不需安裝其他軟體。</p><details><summary>為什麼還要求不使用外部套件或服務？</summary><p class="body-text">工具若載入其他網站的程式、圖片或服務，離線時可能無法使用，也會增加需要管理的檔案與權限。本課先限定單檔、離線操作。這些交付限制方便保存，公式與行為是否正確仍要實測。</p></details></section><section class="lesson-section" id="ch2-section-6">
<h2 class="section-heading">把補齊的需求寫成完整提示詞</h2>
<p class="body-text">下面把剛才的答案連成一份完整提示詞。讀的時候找出輸入、公式、錯誤處理、結果及交付方式；它們是你寫其他工具時也要交代的內容。</p>
<p class="body-text">講師先帶你對照規則，不要求現在再生成一個預算工具。想看計算如何隨輸入改變，可開下方作者參考品；自己的主要任務在下一節。</p>
<div class="prompt-wrap">
<div class="prompt-label">完整提示詞 A｜固定計算：活動預算差異試算器</div>
<p class="policy-guide">這份只描述工具；當次金額在下方另列。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-calculation">你是一位擅長把固定行政計算做成簡單網頁工具的前端工程師。
工作情境：活動承辦人每次整理預算時，要重算各項估算金額、實際支出、估算差異與核定餘額。希望同一套公式可以重複使用，減少手動重寫公式的機會。

請製作「活動預算差異試算器」，讓使用者輸入明細並即時核對結果。

【輸入與操作】
- 每列包含項目名稱、數量、單價、實支金額、備註。
- 可新增或刪除明細列；核定預算在明細表外獨立輸入。
- 所有金額皆為已確認的最終金額，不另加稅。

【計算規則】
- 每列估算金額 = 數量 × 單價。
- 估算合計 = 各列估算金額加總。
- 實支合計 = 各列實支金額加總。
- 較估算差異 = 實支合計 − 估算合計；正數代表實支較估算多，負數代表實支較估算少。
- 核定餘額 = 核定預算 − 實支合計；負數要明確標示超支金額。

【例外與顯示】
- 數量必須是非負整數；單價、實支金額與核定預算必須是非負、有限數值，最多兩位小數。
- 空白、負值、非數字或超過兩位小數時，顯示明確欄位錯誤，停止計算；不可默認為 0。
- 金額以分為最小單位計算，避免小數累加誤差。
- 畫面同時顯示各列估算金額、估算合計、實支合計、較估算差異與核定餘額；使用者修改任一輸入後更新結果。

【交付與驗收】
- 使用繁體中文，欄位標示清楚，桌機和手機都能閱讀。
- 只交付一個完整 HTML 檔案；HTML、CSS、原生 JavaScript 全寫在同一檔，不用外部套件、框架、CDN、圖片；不呼叫外部／雲端 API 或伺服器。
- 初次開啟讓使用者填入自己的明細與核定預算；另附資料可作示例，所有欄位仍可修改。
- 修改一項實支金額後，相關合計和差異應更新；清空數量或輸入負數後，應看到錯誤且不得顯示看似有效的總額。
- 請檢查以上正常和例外情況，最後只輸出從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整 HTML 原始碼，不加說明或 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-calculation" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-calculation-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-calculation"><h3>當次練習資料，可替換</h3><p>需要示例時另外附加，或在工具完成後填入欄位。</p><pre id="prompt-calculation-case">本次預算資料，可替換：
核定預算30000元。
講師：數量4、單價2500、實支10500，備註交通費。
場地：數量1、單價8000、實支8500，備註延長。
餐點：數量40、單價150、實支6500，備註配送。
印刷：數量40、單價50、實支2300，備註加印。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-calculation-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-calculation-case-policy-status" role="status"></span></div></aside>
</div>
<details><summary>先按公式算，再展開核對答案</summary><p class="body-text">各列估算10000、8000、6000、2000；合計26000元。實支合計27800元，比估算多1800元；核定30000減實支後，餘額2200元。答案只在此核對區，案例複製不包含它。</p><p class="body-text">只把餐點數量40改45，估算增加750，成為26750；實支仍27800、差異1050、餘額2200。餘額不變，因為它扣的是實支。</p></details>
<p class="body-text">可開<a href="../assets/tools/budget-reference.html" rel="noopener" target="_blank">預算作者參考工具</a>，載入標準資料、填核定30000，再改餐點數量，核對上方差異。完整匯入、備份及交付例留在<a href="../part2/BUDGET-2.html">活動預算案例</a>。下載<a download="" href="../assets/materials/prompt-budget-case.txt">當次預算資料 TXT</a>只含輸入；答案在核對區。</p></section><section class="lesson-section" id="write-own"><h2 class="section-heading">現在寫一份自己的需求</h2><p class="body-text">選一件自己常做、規則能說清楚的小工作，例如出差費用試算或案件期限追蹤。先只處理一個主要問題，按下面問題補成白話句子；不確定的制度先標「待確認」，不讓 AI 猜。</p><ol class="step-list"><li>先寫誰在什麼時候要用，現在最常花時間或出錯的是哪一步。</li><li>列出使用者會填的欄位，以及可以新增、刪除或修改的資料。</li><li>用文字或算式說明如何處理；再寫一種錯誤輸入及應有提醒。</li><li>說明畫面要顯示什麼、要保存什麼；要求完整單檔，方便存好後重開。</li><li>另外列一組小量測試資料。自己先算或判斷答案，存到驗收表，不貼入初次生成提示詞。</li></ol><div class="prompt-wrap"><div class="prompt-label">自己的工具需求草稿｜先替換括號再使用</div><p class="policy-guide">這是寫作草稿；括號沒補齊以前，先不要直接交給 AI。</p><pre class="prompt-box" data-policy-prompt="true" id="prompt-own-requirement">請幫我製作一個可以重複使用的網頁工具。
用途與使用者：〔誰在什麼工作中要使用，要省下哪一步時間或減少哪種錯誤〕
使用者能填與修改的資料：〔欄位、類型、哪些清單可增刪〕
可以調整的設定：〔門檻、選項或上限；沒有就寫無〕
處理規則：〔如何計算或判斷，多項符合時怎麼處理〕
錯誤處理：〔哪些空值或錯值要阻擋，如何提醒並保留資料〕
結果與保存：〔畫面要顯示什麼，使用者要帶走哪些檔案〕
交付完整單一HTML，外觀與操作都放在同一檔，無外部套件或服務，離線可用。初次顯示空白輸入與操作說明；當次資料另附，不能把人名、日期、金額或答案寫成固定規則。只輸出完整程式，不省略。</pre><button class="copy-btn" data-policy-copy="prompt-own-requirement" type="button">複製完整提示詞</button><span aria-live="polite" id="prompt-own-requirement-policy-status" role="status"></span></div><p class="body-text">可下載<a download="" href="../assets/materials/prompt-own-requirement.txt">需求草稿 TXT</a>填寫；先補完括號，再交給 AI。</p><p class="body-text">完成後，請講師或同伴只看文字回答：要填什麼？如何處理？錯誤時怎麼辦？要拿到什麼？答不出來的地方再補一句。也可下載<a download="" href="../assets/materials/requirements-template.txt">需求記錄表</a>或<a download="" href="../assets/materials/tool-structure-worksheet.md">工具欄位工作表</a>整理；記錄表含測試答案，不能整張當生成提示詞貼出。</p><div class="prac-box"><p class="body-text"><strong>本章檢查：</strong>交出已補齊的工具需求，以及獨立的當次資料與核對答案。換另一組資料時，需求中的處理規則應仍能沿用。下一章會按這個方法製作排班工具。</p></div></section><section class="lesson-section" id="calculation-vs-rules"><h2 class="section-heading">需要另一種規則時，再看對照例</h2><p class="body-text">不同工作要交代的重點會不同。下表幫你檢查自己的需求；選用長例需要時再展開，不是本章額外必做任務。</p><div class="core-table-scroll"><table class="course-table" style="width:100%;border-collapse:collapse;font-size:.9rem;line-height:1.7"><thead><tr><th scope="col" style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">工作怎麼處理</th><th scope="col" style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">優先寫清楚</th><th scope="col" style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">例子</th></tr></thead><tbody><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">操作後改變畫面</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">操作、狀態、開始與重設</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">貪食蛇通關目標</td></tr><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">按公式算數字</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">數值意義、算式、錯值處理</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">本章預算示範</td></tr><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">符合條件就提醒</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">條件、順序、多項同時符合</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">請款資料缺漏初檢</td></tr></tbody></table></div><details><summary>選讀：貪食蛇通關的完整修改示例</summary><section class="optional-example" id="ch2-section-4">
<h2 class="section-heading">互動例：新增可以設定的通關目標</h2>
<p class="body-text">如果需求主要是按鈕或遊戲操作，要說清楚何時開始、何時停止、重新開始要清除什麼。下例在第一章遊戲新增目標；目標數字留在獨立案例區。</p>
<p class="body-text">想試這項延伸時，貼回原生成對話；新對話要先附完整遊戲。要求新增目標，也說清楚原玩法哪些要保留。</p>
<div class="prompt-wrap">
<div class="prompt-label">完整修改提示詞示例｜可直接接在 第一章 的生成對話後</div>
<p class="policy-guide">這是追加功能，接在自己的遊戲程式後使用。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-revision-example">請在目前對話中剛生成的貪食蛇單一 HTML 遊戲新增「通關目標」：提供開始前可輸入的正整數目標個數，每吃到一個食物就累計一個；達到目前設定目標後，顯示「挑戰完成！」並停止移動。每個食物仍依目前分數設定加分，完成畫面保留「重新開始」按鈕。
【判斷與保留範圍】尚未達到目標個數時不要顯示完成。若先撞牆或撞到自己，仍依原規則結束遊戲。按「重新開始」時，分數與已吃食物數都歸零。保留原本的移動方式、食物生成、碰撞、開始和重新開始功能，不新增難度、暫停或最高分。
【交付與檢查】請確認未達目標時遊戲會繼續；達到目標後顯示完成並停止移動；若先碰撞則顯示原有結束狀態；重新開始後分數和食物數都歸零且可再次遊玩。最後只輸出更新後從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML，不要只回傳差異或程式片段，也不要加 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-revision-example" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-revision-example-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-revision-example"><h3>這次的通關設定</h3><p>目標與分數另附，之後仍可在工具調整。</p><pre id="prompt-revision-example-case">本次通關設定：目標5個食物；每個食物10分。設定可換成其他正整數目標與合理分數。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-revision-example-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-revision-example-case-policy-status" role="status"></span></div></aside>
</div>
<div class="core-table-scroll"><table>
<thead><tr><th>檢查部分</th><th>檢核問題</th><th>示例答案</th></tr></thead>
<tbody>
<tr><td>角色</td><td>模型要用什麼角度協助？</td><td>承接原對話中的前端工程師角色；若另開新對話，需補上角色與原遊戲背景。</td></tr>
<tr><td>任務</td><td>這次具體要變更什麼？</td><td>在既有貪食蛇加入「吃到第 5 個食物就完成本局」的目標。</td></tr>
<tr><td>限制</td><td>新規則的數值、例外和保留範圍是什麼？</td><td>第 5 個食物後顯示完成並停止；碰撞仍結束；重新開始時食物數與分數歸零；其餘核心玩法不變。</td></tr>
<tr><td>交付格式</td><td>最後要交付什麼形式？</td><td>交付從 <code>&lt;!DOCTYPE html&gt;</code> 到 <code>&lt;/html&gt;</code> 的完整單一 HTML。</td></tr>
</tbody>
</table></div>
<details><summary>操作後核對目標與原玩法</summary><p class="body-text">吃前四個仍繼續；第五個顯示挑戰完成，分數50且停止移動。先碰撞仍按原規則結束；重新開始食物數及分數歸零。再換另一個目標，確認它依設定判斷。</p></details></section></details><details><summary>選讀：請款資料初檢的完整示例</summary><section class="optional-example" id="ch2-section-7">
<h2 class="section-heading">判斷例：缺少哪些資料，就列出哪些提醒</h2>
<p class="body-text">有些工作不只計算，還要依幾項條件決定要提醒什麼。這裡用一個虛構的請款資料初檢例子說明規則如何組合：金額不合法時停止分類；有效金額和類別確認後，憑證、資產標籤、主管確認可以各自產生提醒；多項同時成立，就要全部列出。</p>
<p class="body-text">下面的門檻和檢查項目是本課為了教學而設定的假資料，不是法律、會計準則、學校或公司的正式核銷政策。工具只列缺漏與待確認事項，不得用「核准」或「可付款」替代主管判斷。</p>
<div class="prompt-wrap">
<div class="prompt-label">完整提示詞 B｜多條件判斷：請款資料初檢工具</div>
<p class="policy-guide">規則寫在這裡；類別、門檻及測試資料另外附加。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-multi-condition">你是一位擅長製作單檔行政檢核工具的前端工程師。
工作情境：承辦人收到請款資料時，要先確認欄位是否齊全，再交由主管人工核對。這個工具只整理資料缺漏，不代替主管核准，也不代表法規或任何機關的正式規定。

請製作「請款資料初檢工具」，讓使用者輸入一筆資料後，看到需要補齊或確認的項目。

【輸入欄位】
- 項目名稱：必填文字，不可空白。
- 費用類別：從使用者可設定的類別清單選一項；可新增、修改和刪除類別。
- 金額。
- 是否已有憑證：是／否。
- 是否已有主管確認：是／否。
- 資產標籤：文字；由使用者設定哪些費用類別要求填寫。

【可調設定】
使用者可設定費用類別、要求資產標籤的類別及主管確認金額門檻；資料未設定完整時提示補齊，不套用未經確認的制度。

【判斷規則與順序】
1. 金額空白、非數字、無限值或小於等於 0：顯示「金額需為大於 0 的數字」，停止後續分類。
2. 項目名稱空白：顯示「請輸入項目名稱」，停止後續分類。
3. 費用類別未選：顯示「請先選擇費用類別」，停止後續分類。
4. 金額有效、項目名稱完整且類別已選時，逐項檢查：沒有憑證時列出「需補憑證」；類別被設定為需要資產標籤但該欄空白時列出「需補資產標籤」；金額大於或等於使用者設定的非負主管確認門檻且沒有主管確認時列出「需主管確認」。
5. 多項條件同時成立時，必須同時列出所有提醒，不可只顯示第一項。
6. 沒有任何提醒時，顯示「資料欄位完整，仍待人工核對」，不得顯示「已核准」或「可付款」。

【操作與交付】
- 提供清楚的表單標籤、「檢查」與「清除」按鈕；畫面以清單呈現結果和觸發原因。
- 錯誤或提醒文字需可讀，手機上不出現水平捲動。
- 所有規則只在本機瀏覽器執行，不呼叫外部／雲端 API、外部服務或伺服器。
- 只交付一個完整 HTML 檔案；HTML、CSS、原生 JavaScript 全內嵌，不使用外部套件、框架、CDN、圖片或字型檔。
- 最後只輸出從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整 HTML 原始碼，不加說明或 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-multi-condition" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-multi-condition-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-multi-condition"><h3>本次制度設定與測試資料</h3><p>這區只提供設定與輸入；答案在下方，複製不包含答案。</p><pre id="prompt-multi-condition-case">本次示例設定，可替換：
類別：設備、耗材、餐費、其他；設備要求資產標籤；主管確認門檻5000元。
這是虛構課堂制度，實際使用前改成已確認的制度。

測試資料：
A：筆電採購；設備；6200元；無憑證、無主管確認；資產標籤空白。
B：影印紙；耗材；2400元；有憑證、無主管確認；資產標籤空白。
C：影印紙；耗材；0元；有憑證、無主管確認；資產標籤空白。
D：項目名稱空白；其他；1200元；有憑證、無主管確認；資產標籤空白。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-multi-condition-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-multi-condition-case-policy-status" role="status"></span></div></aside>
</div>
<div class="core-table-scroll"><table>
<thead><tr><th>測試輸入</th><th>應看到的結果</th><th>為什麼這樣判斷</th></tr></thead>
<tbody>
<tr><td>筆電採購、設備、6200 元、三項資料缺漏</td><td>同時列出「需補憑證」、「需補資產標籤」、「需主管確認」。</td><td>金額和類別有效，三條提醒各自成立，不能只顯示第一條。</td></tr>
<tr><td>影印紙、耗材、2400 元、有憑證</td><td>顯示「資料欄位完整，仍待人工核對」。</td><td>低於課堂示例門檻，其他必填條件也齊全；完整不等於已核准。</td></tr>
<tr><td>影印紙、耗材、金額 0 元</td><td>顯示金額錯誤，停止後續分類。</td><td>金額驗證優先於名稱與分類後續檢查，錯誤資料不可被當成有效請款。</td></tr>
<tr><td>項目名稱空白、其他、1200 元</td><td>顯示「請輸入項目名稱」，停止後續分類。</td><td>初檢結果要能辨識是哪一筆資料；欄位規則需明定，不交由模型猜測。</td></tr>
</tbody>
</table></div>
<details><summary>先預判，再展開四筆核對答案</summary><p class="body-text">A同時提醒補憑證、補資產標籤、主管確認；B資料欄位完整，仍待人工核對；C顯示金額錯誤並停止分類；D顯示名稱錯誤並停止分類。A只勾「已有憑證」後，應剩資產標籤及主管確認兩項。</p></details><p class="body-text">可開<a href="../assets/tools/claim-check-reference.html" rel="noopener" target="_blank">請款初檢作者參考工具</a>試填 A，再只勾已有憑證，觀察哪些提醒改變。參考品不代替自己的生成成果。</p></section></details></section><section class="lesson-section" id="ch2-section-8"><h2 class="section-heading">帶著寫好的需求，下一章做工作工具</h2><p class="body-text">檢查自己的文字是否說清楚輸入、設定、規則、錯誤與結果，並要求完整檔案。當次資料另存，答案只供核對。第三章用排班帶你從這份說明走到可操作的工具，再換兩組資料檢查。</p></section>
<!-- learner-content:end -->
