---
slug: gemini-ai
unit_id: CH1
title: 用白話做出第一個小工具
course_type: skill-operation
version: 2026-10-08-five-chapters
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
<p class="body-text">先開啟<a href="../assets/tools/snake-basic-reference.html" rel="noopener" target="_blank">經典版操作參考品</a>，填入下方案例設定，玩一局並觀察分數與結束畫面。這是作者製作的參考檔，供你預覽成果或在生成暫時不可用時練習；自己的生成檔仍要另外完成。原有<a href="../assets/tools/貪食蛇.html" rel="noopener" target="_blank">壽司店延伸示範</a>留在本章末尾，先完成經典版即可。</p>
<p class="body-text">準備可登入的 Google 帳號、桌面瀏覽器，以及能儲存純文字的編輯器。本章使用<a href="https://gemini.google.com/" rel="noopener" target="_blank">Gemini 網頁版</a>對話取得程式；若帳號無法進入，先核對<a href="https://support.google.com/gemini/answer/13278668?hl=zh-Hant" rel="noopener" target="_blank">官方登入說明</a>並記下訊息。你可以先用參考品練操作，登入問題解除後再回到生成步驟。</p></section>

<section class="lesson-section" id="how-it-runs"><h2 class="section-heading">AI 產生程式，瀏覽器依規則執行</h2>
<p class="body-text">「提示詞」就是你交給 AI 的需求說明。送出後，AI 產生程式文字；把這些文字保存成 HTML 檔，再交給瀏覽器開啟，遊戲才會執行。畫面上的蛇依已寫入的規則移動，按方向鍵時不需要重新詢問 AI。</p>
<p class="body-text">HTML 是網頁檔案格式，負責內容與結構；CSS 決定外觀；JavaScript 處理移動、計分和按鈕反應。本章要求三者寫在同一檔案，讓你只需管理一份檔案。生成需要連線；下面提示詞要求遊戲執行時不依賴外部網站，因此存好後可以離線操作。</p>
<p class="body-text">例如「吃到食物後依設定加分」描述的是處理規則；「這次每個食物加十分」是當次設定。規則留在提示詞中，十分放在獨立案例區或操作時填入，未來就能換成其他分數而不必重做工具。</p></section>

<section class="lesson-section" id="prompt-snake-section"><h2 class="section-heading">先取得完整工具，再填入當次設定</h2><p class="body-text">下方提示詞說清楚開始、移動、計分、碰撞及重開時的行為，也要求可修改的設定欄位。先複製整份提示詞；需要跟做本章示例時，再另外附加案例條件。你不必先懂每一句的設計，先核對它是否產生可操作的成果。</p><div class="prompt-wrap"><div class="prompt-label">生成經典貪食蛇的完整提示詞</div><p class="policy-guide">先複製工具結構；需要本章示例時，另外附加案例區的資料。</p><pre class="prompt-box" data-policy-prompt="true" id="prompt-snake">你是一位擅長把明確需求製作成單檔網頁工具的前端工程師。請為第一次使用網頁工具的玩家製作一款完整可玩的經典貪食蛇，讓我能在桌上型電腦或手機瀏覽器開啟。

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
初次開啟時，初始蛇長、初始方向、食物分數與增長格數由玩家在畫面設定。未附案例時不自行填入示例值；設定不完整時指出缺項並阻止開始。若另附遊戲設定，只用來填入可修改的欄位，不能把當次值寫成固定規則。</pre><button class="copy-btn" data-policy-copy="prompt-snake" type="button">複製完整提示詞</button><span aria-live="polite" id="prompt-snake-policy-status" role="status"></span></div><div class="prompt-wrap"><div class="prompt-label">本章跟做設定，可替換</div><p class="policy-guide">這份資料供當次操作使用，可替換；核對答案另外列出。</p><pre class="case-data" data-policy-case="true" id="prompt-snake-case">本次遊戲設定：初始蛇長三格；初始方向向右；每個食物加十分；吃到食物後增長一格。這些是本次示例設定，可換成其他合理值。</pre><button class="copy-btn" data-policy-copy="prompt-snake-case" type="button">複製案例條件</button><span aria-live="polite" id="prompt-snake-case-policy-status" role="status"></span></div><p class="body-text">本次設定用三格蛇身、向右、食物十分及增長一格。吃到第一個食物後，分數應由零變成十、蛇身由三格變成四格；這是核對結果，不要把答案附到生成提示詞。若換成其他分數或增長格數，就依你填的設定重新核對。</p><p class="body-text">需要離線閱讀時，可下載<a download="" href="../assets/materials/prompt-snake.txt">結構提示詞 TXT</a>與<a download="" href="../assets/materials/prompt-snake-case.txt">案例條件 TXT</a>，兩份各自保存。</p></section>

<section class="lesson-section" id="save-open"><h2 class="section-heading">從生成文字走到能開啟的 HTML 檔</h2>
<p class="body-text">現在已有需求與跟做設定，下一步把它們送入 Gemini，再取得完整程式。你要留下的是本機 HTML 檔；只看見對話中的程式或預覽畫面，還沒完成存檔。</p>
<ol class="step-list">
<li><strong>開新對話並送出需求。</strong>在 Gemini 網頁版開啟新對話，貼上結構提示詞，另附需要的案例設定後送出。等待回覆結束，再取得從 <code>&lt;!DOCTYPE html&gt;</code> 到 <code>&lt;/html&gt;</code> 的內容；不要複製包住程式的三個反引號。</li>
<li><strong>若回覆出現在 Canvas，先取出程式。</strong>Canvas 是同一對話中供你編輯及預覽成果的區域。若它已開啟，可切到右上方「程式碼」取得原始內容；畫面位置不同時對照<a href="https://support.google.com/gemini/answer/16047321?hl=zh-Hant" rel="noopener" target="_blank">官方 Canvas 說明</a>。本章同樣要求取得完整單檔，不必建立公開分享連結。</li>
<li><strong>用純文字保存。</strong>Windows 記事本選「另存新檔」，輸入 <code>snake-v1.html</code>，檔案類型選「所有檔案」、編碼選 UTF-8。Mac「文字編輯」先選「格式 → 製作純文字」，貼入完整程式再存成同名檔案；若詢問副檔名，保留 <code>.html</code>。Mac 路徑也可核對<a href="https://support.apple.com/zh-tw/guide/textedit/txted0b6cd61/mac" rel="noopener" target="_blank">Apple 的 HTML 存檔指引</a>。</li>
<li><strong>找到檔案並開啟。</strong>在檔案管理器確認完整檔名是 <code>snake-v1.html</code>，不是 <code>snake-v1.html.txt</code>。用瀏覽器開啟，應看見設定、遊戲區與開始按鈕；若設定空白，填入案例值再開始。</li>
<li><strong>依行為核對。</strong>用方向鍵、WASD 或方向按鈕移動。先看蛇會不會轉向，再核對食物加分和增長、撞牆結束、重新開始歸零。分數及蛇長依本次設定核對，不只看按鈕有沒有出現。</li>
</ol>
<p class="body-text">若瀏覽器顯示一整頁程式文字，先查副檔名與純文字存檔方式；若只有空白或按鈕無反應，確認程式已完整結束。取得的回覆只有片段時，使用下方補交提示詞；不要自行猜測缺少的程式。</p><div class="prompt-wrap"><div class="prompt-label">要求補交完整成果</div><p class="policy-guide">先複製工具結構；需要本章示例時，另外附加案例區的資料。</p><pre class="prompt-box" data-policy-prompt="true" id="prompt-complete-delivery">請依原規格重新輸出完整單一HTML，不省略任何部分，不以佔位文字或程式片段代替已要求的功能。保留原有可編輯輸入、設定、操作規則與輸出；如有未能完成的規格，先指出缺口。</pre><button class="copy-btn" data-policy-copy="prompt-complete-delivery" type="button">複製完整提示詞</button><span aria-live="polite" id="prompt-complete-delivery-policy-status" role="status"></span></div>
<p class="body-text">功能不符時，在同一對話分開描述「我做了什麼」「實際看見什麼」「預期應發生什麼」，請模型修正並交付完整檔案，再另存後重測。例如填入每個食物十分，吃到食物後卻一直是零，就要查計分行為；這與副檔名錯誤需要不同的修復。</p></section>

<section class="lesson-section" id="modify"><h2 class="section-heading">改一項要求，觀察新舊版本的差異</h2><p class="body-text">v1 已能開始、移動與計分，現在先示範改配色。這次要改變外觀，並保留已驗證的玩法。提示詞要求可調色彩欄位，當次顏色另附，之後才不用為每種顏色重新製作工具。</p><div class="prompt-wrap"><div class="prompt-label">新增可調配色的完整修改提示詞</div><p class="policy-guide">先複製工具結構；需要本章示例時，另外附加案例區的資料。</p><pre class="prompt-box" data-policy-prompt="true" id="prompt-snake-revision">請只修改我在目前對話中剛生成的經典貪食蛇單一 HTML：提供遊戲區背景、蛇頭、蛇身與食物的可調色彩設定，依另外附上的樣式條件套用；未附條件時保留目前外觀。調整後文字、食物和背景仍須清楚可辨識。
這次只改外觀，不改遊戲規則、鍵盤與觸控操作、分數、開始或重新開始功能；保留目前版本已能正常使用的行為。
修改後請交付一份從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML 原始碼，不要只給差異、程式片段、說明或 Markdown 圍欄。
色彩由畫面上的設定調整；未附樣式條件時保留目前外觀。改變色彩後，重新開始或重設仍使用玩家設定，不能把案例顏色固定在程式中。</pre><button class="copy-btn" data-policy-copy="prompt-snake-revision" type="button">複製完整提示詞</button><span aria-live="polite" id="prompt-snake-revision-policy-status" role="status"></span></div><div class="prompt-wrap"><div class="prompt-label">本次配色條件，可替換</div><p class="policy-guide">這份資料供當次操作使用，可替換；核對答案另外列出。</p><pre class="case-data" data-policy-case="true" id="prompt-snake-revision-case">本次外觀條件：遊戲區背景淺米色、蛇頭鮭魚橘、蛇身抹茶綠；食物和背景保持清楚對比。</pre><button class="copy-btn" data-policy-copy="prompt-snake-revision-case" type="button">複製案例條件</button><span aria-live="polite" id="prompt-snake-revision-case-policy-status" role="status"></span></div>
<ol class="step-list"><li>在原對話貼上修改提示詞，另附自己的配色條件。若改用新對話，先附上 v1 完整程式，讓模型取得要修改的起點。</li><li>取得完整修正版，另存 <code>snake-v2.html</code>，保留 v1。重新開啟，確認新外觀及可調設定出現。</li><li>再操作開始、移動、計分、碰撞與重新開始。若外觀改了但計分失效，提供實際／預期結果請模型修復；v1 可作回復與比較起點。</li></ol>
<p class="body-text">完成示例後，自己選另一組色彩，在同一工具的設定中修改，說明哪些畫面改變、哪些玩法仍相同。若想改功能，先只選一項，寫清楚變更與保留範圍，再另存版本，方便找到差異的原因。</p></section>

<section class="lesson-section" id="snake-extensions">
<h2 class="section-heading">課後延伸：逐次加入視覺與互動功能</h2>
<p class="body-text">完成一項自選修改並核對結果後，可選擇將下方三份提示詞依序接在同一段生成對話中。每次只追加一份，取得完整新檔後另存並重新開啟，確認原有操作仍正常。三份提示詞依序調整視覺、增加難度與本機最高分、加入音效和代打示範；每份都列出完整要求，適合作為課後延伸。核心任務只要求完成一項自選修改並核對結果，三份提示詞可視需要使用。</p>
<div class="prompt-wrap">
<div class="prompt-label">延伸提示詞 1｜加入壽司店視覺，保留核心玩法</div>
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-snake-style">請在目前對話中最新的經典貪食蛇單一 HTML 上，加入可調整的樣式設定，包含主題、背景、蛇頭、蛇身、食物顏色及棋盤尺寸、格線大小；棋盤尺寸須為格線大小的整數倍並能容納蛇身，無效設定要提示。依另附樣式條件套用，未附時保留目前外觀；加上清楚的遊戲標題、分數區、開始畫面和結束畫面，按鈕與字體風格一致，文字使用繁體中文，桌機和手機版都不能水平捲動。
這次先改畫面，不改蛇的移動、吃食物加分、碰撞、鍵盤與觸控操作、開始或重新開始規則。不要載入外部圖片、字型、CDN、框架，也不要呼叫外部／雲端 API。
交付修改後從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML，不能只回傳 CSS、差異、程式片段或 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-style" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-snake-style-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-snake-style"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-snake-style-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次樣式條件：壽司店復古街機；邏輯畫布400×400、格線20px；背景淺米色、蛇頭鮭魚橘、蛇身醋飯白、食物抹茶綠。手機上仍須縮放，不以邏輯尺寸撐寬頁面。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-style-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-snake-style-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
<div class="prompt-wrap">
<div class="prompt-label">延伸提示詞 2｜加入難度、暫停與本機最高分</div>
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-snake-features">請在目前對話中最新的貪食蛇單一 HTML 上，新增可設定的難度清單，使用者能新增、修改與刪除難度名稱、初始移動間隔、吃食物後加速幅度、最短移動間隔，以及碰到邊界時結束或穿越的規則，並選擇本局難度。移動間隔須為正數，加速後不能低於最短間隔；難度清單不可空白。未另附設定時保留既有玩法。
新增暫停／繼續、重設和重新開始；重設要清除本局蛇身與分數，但保留最高分。遊戲結束時顯示本局分數及該難度的最高分，最高分只保存在目前瀏覽器的 localStorage，不得宣稱跨瀏覽器或跨裝置同步。保留鍵盤控制，並確保手機觸控方向按鈕及在棋盤上滑動都能改變方向，遊戲時不意外捲動頁面。
保留既有視覺、分數規則與核心玩法，不使用外部函式庫、框架、CDN、伺服器或外部 API；localStorage 是瀏覽器內建能力，資料只留在本機。交付修改後從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML，並確認新難度及原有核心行為都能使用；不要只回傳程式片段或 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-features" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-snake-features-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-snake-features"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-snake-features-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次難度条件：入門、標準、進階三種，初始選標準；入門可穿越邊界且最慢；標準和進階撞邊界結束；進階最快。可依遊玩需要修改各級設定。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-features-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-snake-features-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
<div class="prompt-wrap">
<div class="prompt-label">延伸提示詞 3｜加入音效、代打示範與視覺回饋</div>
<p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-snake-polish">請在目前對話中最新的貪食蛇單一 HTML 上，增加預設關閉的音效開關；啟用時使用瀏覽器內建 Web Audio API 合成簡短音效，不載入音效檔。若瀏覽器不支援音效，遊戲仍須正常進行。
新增「觀看 DEMO」和遊戲中的「代打」功能：由本機 JavaScript 自動控制蛇，優先朝食物移動並避開撞牆或撞到蛇身；找不到安全路線時選擇可存活方向。提供可輸入的 DEMO 時間上限，須為正整數秒；時間到即停止並回到可開始畫面；遊戲中可切回手動控制，暫停、重設和手動接管不可造成狀態錯亂。提供粒子與震動的獨立開關，開啟後分別在吃到食物與遊戲結束時顯示效果；DEMO 時間到時顯示簡短提示；效果不能遮住分數和操作按鈕。
不要呼叫雲端 AI、外部／雲端 API 或伺服器；Web Audio API 是瀏覽器內建能力。保留既有玩法、視覺、難度和最高分功能。交付修改後從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML，確認代打不會連網；不得只回傳程式片段或 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-polish" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-snake-polish-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-snake-polish"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-snake-polish-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

本次示範條件：DEMO最長30秒；吃到食物顯示短暫粒子；遊戲結束時棋盤輕微震動。音效初次開啟保持關閉。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-polish-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-snake-polish-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside>
</div>
<p class="body-text">每完成一份延伸提示詞，就重新開啟最新版本，確認新增功能，並重測開始、移動、得分、碰撞和重新開始。若功能沒有出現，將預期行為與實際畫面描述給模型，請模型只修正該項。依序追加可逐步擴充簡單版本，避免一次要求模型完成所有功能。</p>
</section>

<section class="lesson-section" id="finish"><h2 class="section-heading">帶著生成經驗，進入需求設計</h2>
<p class="body-text">這一章應留下可開啟的 v1、保留原功能的 v2，以及你能說明的一項差異。請關閉檔案後，從存檔位置重新開啟兩版，確認成果已保存在自己的電腦，而不只留在模型對話中。</p>
<p class="body-text">你已看見白話要求如何變成程式，也看過追加要求可能影響原功能。下一章回頭拆解這些提示詞，說明怎麼把用途、輸入、規則和交付寫清楚，讓你能自行設計工作工具。</p></section>
<!-- learner-content:end -->
