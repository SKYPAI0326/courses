---
slug: gemini-ai
unit_id: SUPP-part4-SUPP4-4
title: 貪食蛇改造：外觀、難度與遊戲功能
course_type: skill-operation
version: 2026-10-11-supplement-guidance
---

原貪食蛇延伸的獨立正式來源；保留三組提示詞與獨立案例條件。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">先完成<a href="../chapters/CH1.html">第一章</a>，準備自己最新的可玩 HTML；原版另存備份。</p><ol class="step-list"><li>先看<a href="#snake-extensions">延伸示範</a>，再從下方選外觀、難度或音效與代打一項修改。</li><li>新增功能能使用，原來的開始、移動、得分、碰撞和重新開始也都正常。</li></ol></section><section class="lesson-section" id="snake-extensions">
<h2 class="section-heading">先看成果，再選一項改造</h2>
<p class="body-text">先開啟<a href="../assets/tools/貪食蛇.html" rel="noopener" target="_blank">壽司店延伸示範</a>，觀察外觀、難度與音效等功能。它是成果參考；接下來要修改的是你自己的遊戲。三組提示詞分別處理外觀、難度、音效與代打，每次選一組即可。</p>
<ul class="step-list"><li><a href="#snake-style">外觀改造</a>：第一次延伸可先從這項開始，玩法容易對照。</li><li><a href="#snake-features">難度、暫停與最高分</a>：加入可調規則並測保存。</li><li><a href="#snake-polish">音效與代打</a>：已有難度和最高分功能時，再接續這項。</li></ul></section><section class="lesson-section" id="snake-style"><h2 class="section-heading">改造一：調整外觀，保留玩法</h2><p class="body-text">原本的玩法已能使用，這次讓配色、棋盤與按鈕更符合自己的喜好。先保存最新遊戲，再複製提示詞；壽司店配色是附加示例，你也可以換成自己的設定。</p><div class="prompt-wrap">
<div class="prompt-label">延伸提示詞 1｜加入壽司店視覺，保留核心玩法</div>
<p class="policy-guide">貼回最新遊戲的生成對話；樣式設定另附。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-snake-style">請在目前對話中最新的經典貪食蛇單一 HTML 上，加入可調整的樣式設定，包含主題、背景、蛇頭、蛇身、食物顏色及棋盤尺寸、格線大小；棋盤尺寸須為格線大小的整數倍並能容納蛇身，無效設定要提示。依另附樣式條件套用，未附時保留目前外觀；加上清楚的遊戲標題、分數區、開始畫面和結束畫面，按鈕與字體風格一致，文字使用繁體中文，桌機和手機版都不能水平捲動。
這次先改畫面，不改蛇的移動、吃食物加分、碰撞、鍵盤與觸控操作、開始或重新開始規則。不要載入外部圖片、字型、CDN、框架，也不要呼叫外部／雲端 API。
交付修改後從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML，不能只回傳 CSS、差異、程式片段或 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-style" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-snake-style-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-snake-style"><h3>這次的設定，可替換</h3><p>按需要另附設定，或在生成後填入工具畫面。</p><pre id="prompt-snake-style-case">本次樣式條件：壽司店復古街機；邏輯畫布400×400、格線20px；背景淺米色、蛇頭鮭魚橘、蛇身醋飯白、食物抹茶綠。手機上仍須縮放，不以邏輯尺寸撐寬頁面。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-style-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-snake-style-case-policy-status" role="status"></span></div><p>換一組棋盤尺寸與配色，核對格線、對比及原有計分。</p></aside>
</div><p class="body-text">修改後先看格線、文字和食物是否清楚，再玩一局確認移動、得分與碰撞和原版相同。只改外觀卻造成計分失效時，先回原版核對，再描述問題請 AI 修復。</p></section><section class="lesson-section" id="snake-features"><h2 class="section-heading">改造二：加入難度、暫停與最高分</h2><p class="body-text">已確認遊戲與外觀正常後，可以加入不同速度和邊界規則。先寫下你想要的難度設定；移動間隔指蛇每走一格之間的時間，數值越小移動越快。</p><div class="prompt-wrap">
<div class="prompt-label">延伸提示詞 2｜加入難度、暫停與本機最高分</div>
<p class="policy-guide">先完成可玩的版本，再貼此修改要求；難度數值另附。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-snake-features">請在目前對話中最新的貪食蛇單一 HTML 上，新增可設定的難度清單，使用者能新增、修改與刪除難度名稱、初始移動間隔、吃食物後加速幅度、最短移動間隔，以及碰到邊界時結束或穿越的規則，並選擇本局難度。移動間隔須為正數，加速後不能低於最短間隔；難度清單不可空白。未另附設定時保留既有玩法。
新增暫停／繼續、重設和重新開始；重設要清除本局蛇身與分數，但保留最高分。遊戲結束時顯示本局分數及該難度的最高分，最高分只保存在目前瀏覽器的 localStorage，不得宣稱跨瀏覽器或跨裝置同步。保留鍵盤控制，並確保手機觸控方向按鈕及在棋盤上滑動都能改變方向，遊戲時不意外捲動頁面。
保留既有視覺、分數規則與核心玩法，不使用外部函式庫、框架、CDN、伺服器或外部 API；localStorage 是瀏覽器內建能力，資料只留在本機。交付修改後從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML，並確認新難度及原有核心行為都能使用；不要只回傳程式片段或 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-features" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-snake-features-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-snake-features"><h3>這次的設定，可替換</h3><p>按需要另附設定，或在生成後填入工具畫面。</p><pre id="prompt-snake-features-case">本次難度條件：入門、標準、進階三種，初始選標準；入門可穿越邊界且最慢；標準和進階撞邊界結束；進階最快。可依遊玩需要修改各級設定。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-features-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-snake-features-case-policy-status" role="status"></span></div><p>換另一組速度與邊界設定，核對暫停、重開及最高分保存。</p></aside>
</div><p class="body-text">分別切換難度，測暫停與繼續、重新開始，以及該難度的最高分。重開同一瀏覽器後，最高分應保留；本局分數重新開始時歸零。換瀏覽器或裝置不會自動帶走紀錄。</p></section><section class="lesson-section" id="snake-polish"><h2 class="section-heading">改造三：加入音效與代打示範</h2><p class="body-text">先完成難度與最高分改造，再增加音效及代打。代打是讓遊戲在本機自動控制蛇，方便觀看示範；它不需要呼叫雲端 AI。這組提示詞會保留前兩項功能。</p><div class="prompt-wrap">
<div class="prompt-label">延伸提示詞 3｜加入音效、代打示範與視覺回饋</div>
<p class="policy-guide">接在可玩的版本後；音效與代打設定另附。</p><pre class="prompt-box" data-policy-prompt="工具生成或修改" id="prompt-snake-polish">請在目前對話中最新的貪食蛇單一 HTML 上，增加預設關閉的音效開關；啟用時使用瀏覽器內建 Web Audio API 合成簡短音效，不載入音效檔。若瀏覽器不支援音效，遊戲仍須正常進行。
新增「觀看 DEMO」和遊戲中的「代打」功能：由本機 JavaScript 自動控制蛇，優先朝食物移動並避開撞牆或撞到蛇身；找不到安全路線時選擇可存活方向。提供可輸入的 DEMO 時間上限，須為正整數秒；時間到即停止並回到可開始畫面；遊戲中可切回手動控制，暫停、重設和手動接管不可造成狀態錯亂。提供粒子與震動的獨立開關，開啟後分別在吃到食物與遊戲結束時顯示效果；DEMO 時間到時顯示簡短提示；效果不能遮住分數和操作按鈕。
不要呼叫雲端 AI、外部／雲端 API 或伺服器；Web Audio API 是瀏覽器內建能力。保留既有玩法、視覺、難度和最高分功能。交付修改後從 &lt;!DOCTYPE html&gt; 到 &lt;/html&gt; 的完整單一 HTML，確認代打不會連網；不得只回傳程式片段或 Markdown 圍欄。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-polish" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-snake-polish-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-snake-polish"><h3>這次的設定，可替換</h3><p>按需要另附設定，或在生成後填入工具畫面。</p><pre id="prompt-snake-polish-case">本次示範條件：DEMO最長30秒；吃到食物顯示短暫粒子；遊戲結束時棋盤輕微震動。音效初次開啟保持關閉。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-snake-polish-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-snake-polish-case-policy-status" role="status"></span></div><p>切換音效及代打設定，結束後確認仍可回到玩家操作。</p></aside>
</div><p class="body-text">先在音效關閉時玩一局，再開啟音效測試；觀看示範後切回手動控制，確認能繼續操作。示範到達設定時間會停止，暫停和重新開始也應正常。</p></section><section class="lesson-section" id="completion"><h2 class="section-heading">保存改造版，確認原玩法仍正常</h2><p class="body-text">每完成一份延伸提示詞，就重新開啟最新版本，確認新增功能，並重測開始、移動、得分、碰撞和重新開始。若功能沒有出現，將預期行為與實際畫面描述給模型，請模型只修正該項。依序追加可逐步擴充簡單版本，避免一次要求模型完成所有功能。</p><p class="body-text">另存新的 HTML，保留原版與簡短測試紀錄。這份延伸完成後，可回<a href="../chapters/CH2.html">第二章</a>練習自行寫需求，或回<a href="../index.html#supplement-reuse">延伸參考目錄</a>選其他教材。</p></section></div>
<!-- learner-content:end -->
