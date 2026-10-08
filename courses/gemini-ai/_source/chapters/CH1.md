---
slug: gemini-ai
unit_id: CH1
title: 用白話做出第一個小工具
course_type: skill-operation
version: 2026-10-09-instructor-repair
duration: 45
dependencies: []
learning_objective: 用白話做出第一個小工具
platform_version: Gemini web; official help checked 2026-10-08; account generation pending
---

# 用白話做出第一個小工具

正式正文以下列learner-content範圍為唯一來源；HTML從此範圍轉製。內部設計依據：課程根目錄 _repair/2026-10-08/CHAPTER-REDESIGN.md。
環境：桌面瀏覽器、可登入的Gemini帳號、UTF-8純文字存檔。引用的作者參考品只能證明操作／規則，不代表授課平台生成。真人跟做及六小時試教待驗。
來源：part1/CH1-1.html；跨章交付段落另見遷移紀錄。

<!-- learner-content:start -->
<section class="lesson-section" id="start"><h2 class="section-heading">先做出成果，觀察白話如何改變工具</h2>
<p class="body-text">當你想做一個小工具，往往能說出需要的功能，卻不知道如何把它變成程式。這一章先讓你完成一次「描述需求、取得程式、開啟操作、接續修改」，看到白話要求如何影響畫面與行為。</p>
<p class="body-text">我們沿用貪食蛇作為第一個例子：按下開始、改變方向、吃到食物與撞牆都有可見的反應，方便核對要求是否實現。這次先留下能玩的 <code>snake-v1.html</code>，再改一項外觀或功能，另存 <code>snake-v2.html</code>。下一章才回頭拆解提示詞，讓你能自行寫出其他工具的需求。</p>
<p class="body-text">先開啟<a href="../assets/tools/snake-basic-reference.html" rel="noopener" target="_blank">經典版操作參考品</a>，填入下方案例設定，玩一局並觀察分數與結束畫面。這是作者製作的參考檔，供你預覽成果；生成暫時不可用時也能先練操作。自己的生成檔仍需另外完成。</p>
<p class="body-text">準備可登入的 Google 帳號、桌面瀏覽器，以及能儲存純文字的編輯器。本章使用<a href="https://gemini.google.com/" rel="noopener" target="_blank">Gemini 網頁版</a>對話取得程式；若帳號無法進入，先核對<a href="https://support.google.com/gemini/answer/13278668?hl=zh-Hant" rel="noopener" target="_blank">官方登入說明</a>並記下訊息。你可以先用參考品練操作，登入問題解除後再回到生成步驟。</p></section>
<section class="lesson-section" id="how-it-runs"><h2 class="section-heading">AI 產生程式，瀏覽器依規則執行</h2>
<p class="body-text">「提示詞」就是你交給 AI 的需求說明。送出後，AI 產生程式文字；把這些文字保存成 HTML 檔，再交給瀏覽器開啟，遊戲才會執行。畫面上的蛇依已寫入的規則移動，按方向鍵時不需要重新詢問 AI。</p>
<p class="body-text">HTML 是網頁檔案格式，負責內容與結構；CSS 決定外觀；JavaScript 處理移動、計分和按鈕反應。本章要求三者寫在同一檔案，讓你只需管理一份檔案。生成需要連線；下面提示詞要求遊戲執行時不依賴外部網站，因此存好後可以離線操作。</p>
<p class="body-text">例如「吃到食物後依設定加分」描述的是處理規則；「這次每個食物加十分」是當次設定。規則留在提示詞中，十分放在獨立案例區或操作時填入，未來就能換成其他分數而不必重做工具。</p></section>
<section class="lesson-section" id="prompt-snake-section"><h2 class="section-heading">先取得完整工具，再填入當次設定</h2><p class="body-text">下方提示詞說清楚開始、移動、計分、碰撞及重開時的行為，也要求可修改的設定欄位。先複製整份提示詞；需要跟做本章示例時，再另外附加案例條件。你不必先懂每一句的設計，先核對它是否產生可操作的成果。</p><div class="prompt-wrap"><div class="prompt-label">生成經典貪食蛇的完整提示詞</div><p class="policy-guide">先複製這份工具需求；跟做設定另有按鈕，兩區分開複製。</p><pre class="prompt-box" data-policy-prompt="true" id="prompt-snake">你是一位擅長把明確需求製作成單檔網頁工具的前端工程師。請為第一次使用網頁工具的玩家製作一款完整可玩的經典貪食蛇，讓我能在桌上型電腦或手機瀏覽器開啟。

【畫面與操作】
- 開始前顯示遊戲名稱、簡短操作說明和「開始」按鈕；遊戲中持續顯示分數；遊戲結束後顯示本局分數和「重新開始」按鈕。
- 蛇和食物要清楚可辨識，格線大小一致，畫面對比足夠。遊戲區在手機上縮放到螢幕寬度內，不出現水平捲動。
- 桌機使用方向鍵或 W、A、S、D 移動。手機提供上、下、左、右的大型觸控按鈕，點按時不要意外捲動頁面。

【遊戲規則】
- 提供開始前可調整的初始蛇長、初始方向、每個食物分數與增長格數；蛇長及增長格數是正整數，分數是非負整數，蛇必須能放進棋盤。開始時分數為 0，每次移動一格。
- 蛇每次只能往上、下、左、右移動，不可直接反向撞回自己的身體。
- 食物隨機出現在空格，不可和蛇身重疊。吃到食物後依設定增加分數與蛇身長度，並在新的空格出現下一個食物。
- 蛇撞到牆壁或自己的身體時，遊戲結束並停止移動。
- 按「重新開始」後，蛇回到目前設定的初始長度、分數歸零，遊戲可再次開始；重複點擊開始或重新開始，不可讓遊戲速度越來越快。

【交付限制】
- 只交付一份完整 HTML 檔案；HTML、CSS 和原生 JavaScript 全部寫在同一檔案內。
- 不使用外部函式庫、框架、CDN、圖片、字型檔；不呼叫外部／雲端 API 或伺服器。遊戲在離線時仍可遊玩，字型使用系統字型。
- 按鈕要有清楚的繁體中文名稱和足夠的點擊範圍。畫面文字簡短易懂，不使用尚未實作的按鈕或占位內容。

【完成前自我檢查】
請確認：開始後方向鍵或觸控按鈕可以移動蛇；吃到食物會依設定增加分數且蛇身變長；食物不會出現在蛇身上；撞牆或撞到自己會停止並顯示結束畫面；重新開始會重設蛇和分數。最後只輸出從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整 HTML 原始碼，不加說明或 Markdown 圍欄。

【設定與案例分離】
初次開啟時，初始蛇長、初始方向、食物分數與增長格數由玩家在畫面設定。未附案例時不自行填入示例值；設定不完整時指出缺項並阻止開始。若另附遊戲設定，只用來填入可修改的欄位，不能把當次值寫成固定規則。</pre><button class="copy-btn" data-policy-copy="prompt-snake" type="button">複製完整提示詞</button><span aria-live="polite" id="prompt-snake-policy-status" role="status"></span></div><div class="prompt-wrap"><div class="prompt-label">本章跟做設定，可替換</div><p class="policy-guide">可貼在工具需求之後，也可等工具完成再填入畫面。</p><pre class="case-data" data-policy-case="true" id="prompt-snake-case">本次遊戲設定：初始蛇長三格；初始方向向右；每個食物加十分；吃到食物後增長一格。這些是本次示例設定，可換成其他合理值。</pre><button class="copy-btn" data-policy-copy="prompt-snake-case" type="button">複製案例條件</button><span aria-live="polite" id="prompt-snake-case-policy-status" role="status"></span></div><p class="body-text">本次設定用三格蛇身、向右、食物十分及增長一格。吃到第一個食物後，分數應由零變成十、蛇身由三格變成四格；這是核對結果，不要把答案附到生成提示詞。若換成其他分數或增長格數，就依你填的設定重新核對。</p><p class="body-text">需要離線閱讀時，可下載<a download="" href="../assets/materials/prompt-snake.txt">結構提示詞 TXT</a>與<a download="" href="../assets/materials/prompt-snake-case.txt">案例條件 TXT</a>，兩份各自保存。</p></section>
<section class="lesson-section" id="save-open"><h2 class="section-heading">把 AI 回覆存成網頁檔，再打開</h2>
<p class="body-text">先在 <a href="https://gemini.google.com/" rel="noopener" target="_blank">Gemini 網頁版</a>開新對話，貼完整提示詞，需要時另附案例設定，等待回覆結束。接著要把程式文字存到電腦；對話中的預覽還不是本機檔案。</p>
<h3>第一步：從回覆取出完整程式</h3>
<p class="body-text">原始碼就是 AI 回覆的程式文字。你不必讀懂它，先確認開頭、結尾及複製範圍。下面是辨認位置的示例，不是整份程式，也不是實際 Gemini 回覆的截圖：</p>
<div class="core-table-scroll"><table class="course-table" style="width:100%;border-collapse:collapse;font-size:.9rem;line-height:1.7"><thead><tr><th scope="col" style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">位置</th><th scope="col" style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">應看見的內容</th><th scope="col" style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">你要做的事</th></tr></thead><tbody>
<tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">開頭</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)"><code>&lt;!DOCTYPE html&gt;</code>，接著是 <code>&lt;html…&gt;</code></td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">從這一行開始保留。</td></tr>
<tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">中間</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">網頁、外觀與操作的程式文字</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">全部複製；不要只取畫面上看見的一部分。</td></tr>
<tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">結尾</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)"><code>&lt;/html&gt;</code></td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">連這一行一起複製。</td></tr>
<tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">外部解說</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">解說句子、包住程式的三個反引號</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">不要貼進檔案。</td></tr></tbody></table></div>
<details><summary>回覆在一般對話中</summary><ol class="step-list"><li>找到完整程式區塊。若區塊提供複製功能，用它取得程式；否則選取開頭到結尾的整段文字。</li><li>貼入純文字編輯器，檢查第一行與最後一行；不要把整個聊天畫面全選貼入。缺少結尾時，用下方補交提示詞。</li></ol></details>
<details><summary>回覆在 Canvas 預覽區中</summary><p class="body-text">Canvas 是對話旁可預覽或編輯成果的區域。切到右上方「程式碼」，取出完整程式，再貼入純文字編輯器核對起訖。介面不同時對照<a href="https://support.google.com/gemini/answer/16047321?hl=zh-Hant" rel="noopener" target="_blank">官方 Canvas 說明</a>。本章保存本機檔，不必先公開分享。</p></details>
<h3>第二步：只讀自己的電腦存檔方式</h3>
<details><summary>Windows：用記事本存成 snake-v1.html</summary><ol class="step-list"><li>打開記事本，貼入完整程式。</li><li>選「另存新檔」，檔名輸入 <code>snake-v1.html</code>；檔案類型選「所有檔案」，編碼選 UTF-8。</li><li>選容易找到的資料夾，例如「AI工作工具」，記住位置後儲存。確認完整檔名是 <code>snake-v1.html</code>。</li></ol></details>
<details><summary>Mac：用文字編輯存成 snake-v1.html</summary><ol class="step-list"><li>打開「文字編輯」，先選「格式 → 製作純文字格式」，再貼入完整程式；若選單顯示「製作 RTF 格式」，表示目前已是純文字。</li><li>儲存到容易找到的資料夾，檔名輸入 <code>snake-v1.html</code>。詢問副檔名時選「使用 .html」，避免存成 .txt。</li><li>確認完整檔名及位置。詳細操作見<a href="https://support.apple.com/zh-tw/guide/textedit/txted0b6cd61/mac" rel="noopener" target="_blank">Apple HTML 存檔說明</a>。</li></ol></details>
<h3>第三步：打開檔案，核對看見的畫面</h3>
<ol class="step-list"><li>在資料夾找到 <code>snake-v1.html</code>，用瀏覽器開啟；若雙擊打開編輯器，改用「開啟方式」選瀏覽器。</li><li>網址列應指向電腦中的檔案，開頭為 <code>file:///</code>。畫面應有設定、遊戲區及開始按鈕；不是 Gemini 聊天頁。</li><li>填初始蛇長3、方向向右、食物10分、增長1格。開始後測移動、第一次吃食物、碰撞與重新開始。預期第一次分數10、蛇長4；重開分數歸零。</li></ol>
<div class="core-table-scroll"><table class="course-table" style="width:100%;border-collapse:collapse;font-size:.9rem;line-height:1.7"><thead><tr><th scope="col" style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">看到的狀況</th><th scope="col" style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">回哪一步處理</th></tr></thead><tbody><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">檔名是 snake-v1.html.txt</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">回存檔步驟，保留 .html 副檔名，再用瀏覽器開。</td></tr><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">整頁都是程式文字</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">查完整副檔名及是否用純文字保存。</td></tr><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">空白或按鈕無反應</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">查程式是否完整到 &lt;/html&gt;；缺漏時請 AI 補交完整檔。</td></tr><tr><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">可操作，計分卻不符設定</td><td style="padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--c-border)">記下填的設定、實際數字及預期，貼回原對話要求修正；保留失敗檔。</td></tr></tbody></table></div>
<div class="prompt-wrap"><div class="prompt-label">要求補交完整成果</div><p class="policy-guide">原回覆只有片段或缺少結尾時，貼回同一個對話要求補交。</p><pre class="prompt-box" data-policy-prompt="true" id="prompt-complete-delivery">請依原規格重新輸出完整單一HTML，不省略任何部分，不以佔位文字或程式片段代替已要求的功能。保留原有可編輯輸入、設定、操作規則與輸出；如有未能完成的規格，先指出缺口。</pre><button class="copy-btn" data-policy-copy="prompt-complete-delivery" type="button">複製完整提示詞</button><span aria-live="polite" id="prompt-complete-delivery-policy-status" role="status"></span></div><p class="body-text">存好後先關閉，再從資料夾重新開啟。能再次設定並開始，才完成保存；接著在原生成對話修改配色，另存 v2。</p></section>
<section class="lesson-section" id="modify"><h2 class="section-heading">改一項要求，觀察新舊版本的差異</h2><p class="body-text">v1 已能開始、移動與計分，現在先示範改配色。這次要改變外觀，並保留已驗證的玩法。提示詞要求可調色彩欄位，當次顏色另附，之後才不用為每種顏色重新製作工具。</p><div class="prompt-wrap"><div class="prompt-label">新增可調配色的完整修改提示詞</div><p class="policy-guide">貼回原對話；需要本次配色時，再另附下方條件。</p><pre class="prompt-box" data-policy-prompt="true" id="prompt-snake-revision">請只修改我在目前對話中剛生成的經典貪食蛇單一 HTML：提供遊戲區背景、蛇頭、蛇身與食物的可調色彩設定，依另外附上的樣式條件套用；未附條件時保留目前外觀。調整後文字、食物和背景仍須清楚可辨識。
這次只改外觀，不改遊戲規則、鍵盤與觸控操作、分數、開始或重新開始功能；保留目前版本已能正常使用的行為。
修改後請交付一份從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML 原始碼，不要只給差異、程式片段、說明或 Markdown 圍欄。
色彩由畫面上的設定調整；未附樣式條件時保留目前外觀。改變色彩後，重新開始或重設仍使用玩家設定，不能把案例顏色固定在程式中。</pre><button class="copy-btn" data-policy-copy="prompt-snake-revision" type="button">複製完整提示詞</button><span aria-live="polite" id="prompt-snake-revision-policy-status" role="status"></span></div><div class="prompt-wrap"><div class="prompt-label">本次配色條件，可替換</div><p class="policy-guide">也可以自己換另一組顏色，再核對畫面與玩法。</p><pre class="case-data" data-policy-case="true" id="prompt-snake-revision-case">本次外觀條件：遊戲區背景淺米色、蛇頭鮭魚橘、蛇身抹茶綠；食物和背景保持清楚對比。</pre><button class="copy-btn" data-policy-copy="prompt-snake-revision-case" type="button">複製案例條件</button><span aria-live="polite" id="prompt-snake-revision-case-policy-status" role="status"></span></div>
<ol class="step-list"><li>在原對話貼上修改提示詞，另附自己的配色條件。若改用新對話，先附上 v1 完整程式，讓模型取得要修改的起點。</li><li>取得完整修正版，另存 <code>snake-v2.html</code>，保留 v1。重新開啟，確認新外觀及可調設定出現。</li><li>再操作開始、移動、計分、碰撞與重新開始。若外觀改了但計分失效，提供實際／預期結果請模型修復；v1 可作回復與比較起點。</li></ol>
<p class="body-text">完成示例後，自己選另一組色彩，在同一工具的設定中修改，說明哪些畫面改變、哪些玩法仍相同。若想改功能，先只選一項，寫清楚變更與保留範圍，再另存版本，方便找到差異的原因。</p></section>
<section class="lesson-section" id="snake-extensions"><h2 class="section-heading">想繼續改遊戲，課後再選一項</h2><p class="body-text">完整的視覺、難度、最高分、音效與代打提示詞已放在<a href="../part4/SUPP4-3.html#snake-extensions">貪食蛇改造補充頁</a>。本章先確認自己的 v1 能玩、v2 能修改並重開，再繼續第二章。</p></section><section class="lesson-section" id="finish"><h2 class="section-heading">保存兩個版本，下一章練習自己寫需求</h2>
<p class="body-text">這一章應留下可開啟的 v1、保留原功能的 v2，以及你能說明的一項差異。請關閉檔案後，從存檔位置重新開啟兩版，確認成果已保存在自己的電腦，而不只留在模型對話中。</p>
<p class="body-text">你已看見白話要求如何變成程式，也看過追加要求可能影響原功能。下一章回頭拆解這些提示詞，說明怎麼把用途、輸入、規則和交付寫清楚，讓你能自行設計工作工具。</p></section>
<!-- learner-content:end -->
