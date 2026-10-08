---
slug: gemini-ai
unit_id: CH2
title: 把需求寫成可重用的提示詞
course_type: skill-operation
version: 2026-10-08-five-chapters
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

<section class="lesson-section" id="ch2-section-1">
<h2 class="section-heading">做出來之後，回頭看提示詞如何提供方向</h2>
<p class="body-text">第一章已完成能操作的貪食蛇，也提出過一項修改。現在回看自己的提示詞：模型為何知道要提供方向按鈕、如何計分，以及最後要交付 HTML？這一章把那些資訊拆成可檢查的需求，讓你能自己描述下一個工具。</p>
<p class="body-text">起草時可使用「黃金公式」整理四個欄位：<strong>角色、任務、限制、交付格式</strong>。工作情境置於公式前，說明工具的用途；四欄提供檢查需求是否完整的架構。模型生成後，仍須依規格實際核對結果。</p>
</section>
<section class="lesson-section" id="ch2-section-2">
<h2 class="section-heading">黃金公式四個欄位，各自解決什麼問題</h2>
<div class="core-table-scroll"><table class="spec-map">
<thead><tr><th>部分</th><th>要交代的事</th><th>貪食蛇提示詞中的例子與作用</th></tr></thead>
<tbody>
<tr><td>角色 Role</td><td>指定模型從哪種工作角度協助；角色名稱提供回應角度，生成內容仍須依規格核對專業性與正確性。</td><td>「擅長把明確需求製作成單檔網頁工具的前端工程師」讓它知道要以網頁製作角度回應。</td></tr>
<tr><td>任務 Task</td><td>說清楚要完成的成果與誰會使用；只有「做得好看」無法定義完成。</td><td>「請為第一次使用網頁工具的玩家製作一款完整可玩的經典貪食蛇」先交代使用對象與成果。</td></tr>
<tr><td>限制 Constraint</td><td>列出輸入、操作規則、例外、技術邊界及不能改變的條件。</td><td>不可直接反向移動；食物不能與蛇身重疊；撞牆或撞到自己時結束；遊戲交付為單一 HTML。</td></tr>
<tr><td>交付格式 Format</td><td>規定模型最後要交付的檔案或文字形式；畫面有哪些元素應寫在任務或規則中。</td><td>只輸出從 <code>&lt;!DOCTYPE html&gt;</code> 到 <code>&lt;/html&gt;</code> 的完整單一 HTML，供學員另存並重新開啟。</td></tr>
</tbody>
</table></div>
<p class="body-text">情境回答「為什麼要做」；四欄公式再把需求整理成「誰協助、要做什麼、要遵守什麼、最後交付什麼格式」。提示詞可將角色、任務、限制與交付格式自然寫入句子，欄位名稱則作為檢查架構。</p>
<p class="body-text">可<a href="CH1.html#prompt-snake">回到 第一章 的完整貪食蛇提示詞</a>逐句對照。此處沿用同一個已生成案例，目標是辨認各項條件的用途，無須另外下載相同提示詞。</p>
</section>
<section class="lesson-section" id="ch2-section-3">
<h2 class="section-heading">為什麼要求單一 HTML、內嵌 CSS 與原生 JavaScript</h2>
<p class="body-text">「單一 HTML」是交付方式：把網頁需要的內容放在一個可存檔的檔案裡。HTML 描述結構，CSS 控制外觀，JavaScript 處理固定互動。第一次實作時，學員只需保存和開啟一個檔案，不必先建立專案、安裝套件或管理多個檔案。</p>
<p class="body-text">「CSS 和 JavaScript 全內嵌」進一步說明程式碼放在哪裡；「不使用外部套件、CDN、圖片或外部／雲端 API」則排除網路服務和額外資產依賴。若只寫「做一個網頁遊戲」，模型可能交付多個檔案、使用外部資源，或只給示意碼。把交付限制說清楚，之後才容易保存、分享和在沒有網路時操作。</p>
<p class="body-text">注意：單一檔案可簡化交付。程式正確性與資料安全仍須另外檢查；若工具使用外部連線、儲存重要資料或處理敏感內容，還要確認權限、資料位置和風險。本課的貪食蛇不使用雲端 API，也不放工作資料。</p>
<div class="callout info"><div aria-hidden="true" class="callout-icon">i</div><div class="callout-body"><strong>快速判讀：</strong>看到「輸出一份完整 HTML」就知道要交一個檔案；看到「CSS 寫在 style、JavaScript 寫在 script」就知道程式放在檔案內；看到「不使用 CDN 或外部／雲端 API」就知道執行時不依賴外部服務。三句解決的是不同的交付問題。</div></div>
</section>
<section class="lesson-section" id="ch2-section-4">
<h2 class="section-heading">把一句模糊修改寫成可核對的要求</h2>
<p class="body-text">回想 第一章 的配色修改，再看下方「新增通關目標」的完整提示詞。若只寫「幫我變好看」或「再加一個功能」，模型還需要猜測改什麼、能否動到其他行為、最後要交付完整檔案還是程式片段。用黃金公式把這些資訊補齊，才能在生成後逐項核對。</p>
<p class="body-text">以下是可以直接貼在原生成對話中的完整示例。請把表格中的四個答案對照這一份「新增通關目標」提示詞；它指定新規則、保留範圍和交付格式。因為前一段對話已包含原始 HTML，這份追加指令可直接接續使用，不必先完成 第一章 的自選延伸功能。</p>
<div class="prompt-wrap">
<div class="prompt-label">完整修改提示詞示例｜可直接接在 第一章 的生成對話後</div>
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-revision-example">請在目前對話中剛生成的貪食蛇單一 HTML 遊戲新增「通關目標」：提供開始前可輸入的正整數目標個數，每吃到一個食物就累計一個；達到目前設定目標後，顯示「挑戰完成！」並停止移動。每個食物仍依目前分數設定加分，完成畫面保留「重新開始」按鈕。
【判斷與保留範圍】尚未達到目標個數時不要顯示完成。若先撞牆或撞到自己，仍依原規則結束遊戲。按「重新開始」時，分數與已吃食物數都歸零。保留原本的移動方式、食物生成、碰撞、開始和重新開始功能，不新增難度、暫停或最高分。
【交付與檢查】請確認未達目標時遊戲會繼續；達到目標後顯示完成並停止移動；若先碰撞則顯示原有結束狀態；重新開始後分數和食物數都歸零且可再次遊玩。最後只輸出更新後從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML，不要只回傳差異或程式片段，也不要加 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-revision-example" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-revision-example-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-revision-example"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-revision-example-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次通關條件：目標五個食物，每個食物十分；吃前四個仍繼續，第五個顯示挑戰完成，分數五十分。先碰撞則按原規則結束。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-revision-example-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-revision-example-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
<p class="body-text">練習時先選一項待調整的需求，依四欄各補一句，再貼到原生成對話。修改後核對兩件事：新要求是否出現；原有核心功能是否仍可操作。若改做全新的工具，需另行交代情境、任務、限制和交付方式，因為新對話沒有舊生成內容可供承接。</p>
<div class="core-table-scroll"><table>
<thead><tr><th>檢查部分</th><th>檢核問題</th><th>示例答案</th></tr></thead>
<tbody>
<tr><td>角色</td><td>模型要用什麼角度協助？</td><td>承接原對話中的前端工程師角色；若另開新對話，需補上角色與原遊戲背景。</td></tr>
<tr><td>任務</td><td>這次具體要變更什麼？</td><td>在既有貪食蛇加入「吃到第 5 個食物就完成本局」的目標。</td></tr>
<tr><td>限制</td><td>新規則的數值、例外和保留範圍是什麼？</td><td>第 5 個食物後顯示完成並停止；碰撞仍結束；重新開始時食物數與分數歸零；其餘核心玩法不變。</td></tr>
<tr><td>交付格式</td><td>最後要交付什麼形式？</td><td>交付從 <code>&lt;!DOCTYPE html&gt;</code> 到 <code>&lt;/html&gt;</code> 的完整單一 HTML。</td></tr>
</tbody>
</table></div>
<p class="body-text">你已能分辨一份提示詞的角色、任務、限制與呈現。接著比較互動、固定計算和條件判斷的需求，確認不同任務各自需要哪些規則；分類會影響你補什麼內容。</p>
</section>
<section class="lesson-section" id="ch2-section-5">
<h2 class="section-heading">提示詞要先說清楚工作主要在做什麼</h2>
<p class="body-text">寫清楚四個部分後，還要說明工具主要如何處理資料。按鈕改變畫面、依公式計算、依條件列出提醒，需要的規則各不相同；一個工具也可以同時使用這些方法。下面用既有完整例子比較設計重點，不要求你把每個例子都重新生成。</p>
<div class="core-table-scroll"><table>
<thead><tr><th>提示詞類型</th><th>主要工作</th><th>規格最不能漏的內容</th><th>課程例子</th></tr></thead>
<tbody>
<tr><td>單檔互動工具</td><td>讓使用者透過表單、按鈕或鍵盤操作，畫面隨之更新。</td><td>使用者輸入、可做的操作、每個操作後的畫面反應、保存方式與交付格式。</td><td><a href="CH1.html#prompt-snake">第一章 的貪食蛇完整提示詞</a>：移動、得分、碰撞和重新開始。</td></tr>
<tr><td>固定計算函數</td><td>把相同輸入依固定公式轉成可重複核對的數字。</td><td>每個輸入的意義、公式、單位、小數處理、缺值／無效值和已知答案。</td><td>下方的活動預算差異試算器；後面的主線課程會再用完整資料實作。</td></tr>
<tr><td>多條件判斷</td><td>依明確的條件組合，列出結果分類和觸發原因。</td><td>條件順序、同時符合多項時怎麼處理、例外、輸出文字與人工覆核界線。</td><td>下方的請款資料初檢工具；規則只作課堂示例，不代表正式機關規定。</td></tr>
</tbody>
</table><p class="body-text">這裡所說的「函數」可以先想成一個固定規則的小單位：把輸入值交給它，它依照公式算出結果。學員不需要在這裡學 JavaScript 寫法；重要的是能說清楚輸入代表什麼、公式怎麼算、無效值要怎麼處理。</p></div>
<p class="body-text">如果主要任務是「按鈕操作後改變畫面」，先描述互動；如果主要任務是「照公式反覆計算」，先定義每個數值和算式；如果主要任務是「符合哪些條件、要提醒什麼」，先寫清楚規則和同時符合時的結果。不要把三種範例都生成一次；這一站要練的是讀懂需求、選類型和找出提示詞不可缺的資訊。</p>
</section>
<section class="lesson-section" id="ch2-section-6">
<h2 class="section-heading">固定計算：公式要能用已知答案核對</h2>
<p class="body-text">Excel 很適合整理和計算資料，也能設定資料驗證或保護公式；風險在於使用者可能誤改公式、複製錯誤儲存格，或把不同意義的數字放進同一欄。把固定計算包在小工具裡，可以讓使用者主要透過欄位輸入，由程式反覆套用同一組規則；這會降低某些誤操作機會，但不代表公式天生正確，也不能免除已知答案測試。</p>
<p class="body-text">以下提示詞定義可重用的欄位、公式、例外與輸出；預算資料與預期總額放在獨立案例區。先用本次已知答案核對，再換其他項目與金額。後續排班主線也採相同方式：抽出工具結構，再用不同案例檢查。</p>
<div class="prompt-wrap">
<div class="prompt-label">完整提示詞 A｜固定計算：活動預算差異試算器</div>
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-calculation">你是一位擅長把固定行政計算做成簡單網頁工具的前端工程師。
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
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-calculation" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-calculation-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-calculation"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-calculation-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次預算資料：講師 4 × 2500，實支 10500；場地 1 × 8000，實支 8500；餐點 40 × 150，實支 6500；印刷 40 × 50，實支 2300；核定預算 30000。

本次核對答案：估算合計26000、實支合計27800、較估算多1800、核定餘額2200元。先按公式核對，再換一組項目與金額重算，不把這些答案寫入程式。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-calculation-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-calculation-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
<p class="body-text">對照答案：四列估算分別是 10000、8000、6000、2000 元，估算合計 26000 元；實支合計 27800 元，因此實支較估算多 1800 元；核定 30000 元扣除實支後，餘額 2200 元。這四個數字放在獨立案例與核對紀錄，未寫進結構提示詞。生成後填入相同資料核對，再換另一組明細測試。</p>
</section>
<section class="lesson-section" id="ch2-section-7">
<h2 class="section-heading">多條件判斷：先定義規則，再看哪些提醒同時出現</h2>
<p class="body-text">有些工作不只計算，還要依幾項條件決定要提醒什麼。這裡用一個虛構的請款資料初檢例子說明規則如何組合：金額不合法時停止分類；有效金額和類別確認後，憑證、資產標籤、主管確認可以各自產生提醒；多項同時成立，就要全部列出。</p>
<p class="body-text">下面的門檻和檢查項目是本課為了教學而設定的假資料，不是法律、會計準則、學校或公司的正式核銷政策。工具只列缺漏與待確認事項，不得用「核准」或「可付款」替代主管判斷。</p>
<div class="prompt-wrap">
<div class="prompt-label">完整提示詞 B｜多條件判斷：請款資料初檢工具</div>
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-multi-condition">你是一位擅長製作單檔行政檢核工具的前端工程師。
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
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-multi-condition" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-multi-condition-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-multi-condition"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-multi-condition-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次示例設定：費用類別設備、耗材、餐費、其他；設備需要資產標籤；主管確認門檻5000元。這是課堂示例制度，可依已確認制度調整。

本次測試資料與預期：A. 項目名稱「筆電採購」、設備、6200 元、無憑證、無主管確認、資產標籤空白，應同時顯示三項提醒；B. 項目名稱「影印紙」、耗材、2400 元、有憑證、無主管確認，應顯示「資料欄位完整，仍待人工核對」；C. 項目名稱「影印紙」、耗材、金額 0 元，應只顯示金額錯誤並停止分類；D. 項目名稱空白、其他、1200 元，應顯示名稱錯誤並停止分類。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-multi-condition-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-multi-condition-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
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
</section>
<section class="lesson-section" id="calculation-vs-rules"><h2 class="section-heading">親手改一次數字，再改一次條件</h2><p class="body-text">看完兩份提示詞，先用作者參考工具操作，觀察不同規則會改變什麼。預算工具輸出數字；請款初檢工具輸出需要补齊的項目。這一段完成兩份短測試紀錄，再選與自己工作相近的一份提示詞生成工具，保存並重開核對。</p><ol class="step-list"><li>開啟<a href="../assets/tools/budget-reference.html" target="_blank">預算作者參考工具</a>，載入標準資料，核定預算填30000。確認估算26000、實支27800、差異1800、餘額2200。估算是數量乘單價再加總，實支按實際填值加總。</li><li>只把餐點數量40改45，其他不動。估算增加5×150=750，成為26750；實支仍27800，差異變1050，餘額仍2200。若餘額也跟著改，就要回頭检查它是否錯用了估算。</li><li>開啟<a href="../assets/tools/claim-check-reference.html" target="_blank">請款初檢作者參考工具</a>。設定類別「設備、耗材、其他」、要求資產標籤類別「設備」、主管確認門檻5000。輸入筆電採購/設備/6200，憑證、主管確認皆不勾，資產標籤留空。三項提醒應同時出現；不是只選其中一項。</li><li>只勾「已有憑證」，應剩資產標籤與主管確認兩項。再把金額改0，應停止正常判斷並顯示金額錯誤，不能沿用舊提醒。恢復有效值才重新判斷。</li></ol><div class="core-table-scroll"><table><thead><tr><th>觀察</th><th>計算工具</th><th>條件初檢工具</th></tr></thead><tbody><tr><td>修改的輸入</td><td>餐點數量</td><td>憑證勾選與金額</td></tr><tr><td>中間處理</td><td>數量差×單價，再更新估算與差異</td><td>先驗輸入，再逐條判斷，保留所有命中提醒</td></tr><tr><td>結果</td><td>數值、單位與公式依據</td><td>待補項目及觸發理由</td></tr></tbody></table></div><p class="body-text">把「只改了什麼、哪些結果應變、哪些應保留」各寫一行。若想換工作案例，先選主要處理方式，重寫輸入、規則、例外和結果；第三章會把這種需求整理方式用於排班，練習以两組資料核對同一工具。</p></section><section class="lesson-section" id="ch2-section-8">
<h2 class="section-heading">選一種主要工作，再把規則交代完整</h2>
<p class="body-text">先讀三個需求，暫停一下，自己判斷主要是哪一類，再看下面的核對理由。選類型不是替工具貼標籤，而是提醒自己優先說清楚哪種規則。</p>
<ol class="body-text">
<li>新增品項後顯示名稱、數量和狀態，並能標記完成、編輯或刪除。</li>
<li>把活動明細的數量乘單價，算出估算合計，再比較實支與核定額度。</li>
<li>若金額到達指定門檻就提醒主管確認；若類別是設備且缺資產標籤也提醒，兩項都成立時都要列出。</li>
</ol>
<h3 class="section-subheading">核對理由</h3>
<div class="core-table-scroll"><table>
<thead><tr><th>需求</th><th>主要類型</th><th>先補清楚的資訊</th></tr></thead>
<tbody>
<tr><td>1</td><td>單檔互動工具</td><td>每種操作後畫面如何更新，編輯和刪除作用在哪一筆資料。</td></tr>
<tr><td>2</td><td>固定計算</td><td>欄位意義、公式、單位、無效輸入及至少一組核對答案。</td></tr>
<tr><td>3</td><td>多條件判斷</td><td>門檻、同時成立時的輸出，以及結果不能代替誰做正式決定。</td></tr>
</tbody>
</table></div>
<p class="body-text">請選一個你想處理的工作需求，寫出使用者要填哪些資料、哪些條件可以設定、工具如何處理、要顯示什麼結果，以及錯誤時如何提醒。再用四個部分整理成完整白話提示詞；當次人名、日期或金額另外附加。若你只寫「做一個好用工具」，回到上方對照表補齊可操作與可核對的要求。</p><p class="body-text">核對你的提示詞：換一份資料是否仍能使用？結果是否有可檢查的規則？是否要求完整成果而非片段？第二章留下的是可重用需求與分開的案例。第三章將用這個方法，完整製作一個處理可排日期與班次需求的工作工具。</p></section>

<!-- learner-content:end -->
