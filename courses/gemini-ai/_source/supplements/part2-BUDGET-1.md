---
slug: gemini-ai
unit_id: SUPP-part2-BUDGET-1
title: 預算補充：差異與剩餘額
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<main class="lesson-body"><section class="lesson-section" id="core-1"><h2 class="section-heading">一筆活動資料，先分清三種金額</h2>
<p class="body-text">活動結束後，承辦人要整理預算與單據，讓負責人能回答兩件事：實際支出比原估多或少多少？核定額度扣除實支後還剩多少？本節先用同一份活動資料手算，留下四個可核對答案；下一課再用這些答案檢查生成工具。</p>
<p class="body-text">估算是依計畫數量和單價推算的金額；實支是依單據記錄的實際費用；核定預算是事前核准可使用的上限。本例核定預算為 30,000 元，費用皆已含必要費用，不另外加稅。下方已直接列出四筆資料，閱讀與手算不需下載檔案；<a download="" href="../assets/materials/budget-normal.csv">四項活動費用 CSV</a>供下一課匯入自製工具時使用。</p>
<p class="body-text">表中的 quantity 是數量、unit_price 是預估單價、actual 是逐項實支、note 是差異原因。actual 已是該項整筆實支，不是每人的單價；估算才使用「數量 × 預估單價」，note 用來說明差異，不改變計算公式。</p>
<div class="core-table-scroll"><table>
<thead><tr><th>項目</th><th>數量</th><th>預估單價</th><th>逐項實支</th><th>備註</th></tr></thead>
<tbody>
<tr><td>講師</td><td>4</td><td>2,500</td><td>10,500</td><td>增加交通費</td></tr>
<tr><td>場地</td><td>1</td><td>8,000</td><td>8,500</td><td>延長使用</td></tr>
<tr><td>餐點</td><td>40</td><td>150</td><td>6,500</td><td>增加配送</td></tr>
<tr><td>印刷</td><td>40</td><td>50</td><td>2,300</td><td>加印</td></tr>
</tbody></table></div></section>
<section class="lesson-section" id="core-2"><h2 class="section-heading">先算估算，再分辨兩個差值</h2>
<p class="body-text">先看講師費這一列：4 人 × 2,500 元 = 10,000 元估算；actual 欄的 10,500 元已是整筆實支，因此此項比原估多 500 元。交通費已包含在實支裡，不再乘上人數。這列示範了其餘項目要沿用的計算方式。</p>
<p class="body-text">依同一規則，先自行算出場地、餐點、印刷三列的估算，再分別加總四列估算與四列實支；在看下方核對表前，先記下兩個合計。獨立算出的答案會成為下一課判斷工具公式是否正確的基準。</p>
<div class="core-table-scroll"><table>
<thead><tr><th>項目</th><th>估算</th><th>逐項實支</th><th>支出差異</th></tr></thead>
<tbody>
<tr><td>講師</td><td>4 × 2,500 = 10,000</td><td>10,500</td><td>+500</td></tr>
<tr><td>場地</td><td>1 × 8,000 = 8,000</td><td>8,500</td><td>+500</td></tr>
<tr><td>餐點</td><td>40 × 150 = 6,000</td><td>6,500</td><td>+500</td></tr>
<tr><td>印刷</td><td>40 × 50 = 2,000</td><td>2,300</td><td>+300</td></tr>
</tbody>
<tfoot><tr><th>合計</th><th>26,000</th><th>27,800</th><th>+1,800</th></tr></tfoot>
</table></div>
<p class="body-text">估算合計 = 10,000 + 8,000 + 6,000 + 2,000 = 26,000 元。實支合計 = 10,500 + 8,500 + 6,500 + 2,300 = 27,800 元。支出差異 = 實支合計 − 估算合計 = 27,800 − 26,000 = +1,800 元；正數表示實支高於原估，負數表示實支低於原估。</p>
<p class="body-text">核定餘額回答另一個問題：核定預算 − 實支合計 = 30,000 − 27,800 = 2,200 元，表示尚有 2,200 元額度。報價也常用數量乘單價，但報價計算向客戶收取的金額，本節核銷資料則比較原估與實際花費並追蹤核定上限；欄位意義不同，不能只因公式相似就沿用同一組資料規則。</p></section>
<section class="lesson-section" id="core-3"><h2 class="section-heading">改一項條件，留下可交接的驗收基準</h2>
<p class="body-text">30,000 元是本例基準，四個核對值為估算 26,000、實支 27,800、支出差異 +1,800、核定餘額 +2,200。先留下這組結果，再只改一項條件，觀察哪個計算會受影響。預算參考工具提供可操作的比較畫面；正式生成工具則留到下一課製作。</p>
<p class="body-text">打開<a href="../assets/tools/budget-reference.html" rel="noopener" target="_blank">活動預算參考品</a>。若畫面保留先前操作，先按「載入標準資料」，確認估算 26,000、實支 27,800、支出差異 +1,800、核定餘額 +2,200；這一步先把比較起點恢復一致。再預測只把核定預算改成 27,000 元時會有什麼變化，然後輸入該數字。明細沒有變，所以估算仍為 26,000、實支仍為 27,800、支出差異仍為 +1,800；核定餘額則是 27,000 − 27,800 = −800 元，畫面應標示超支 800 元。這個比較只改核定上限，說明支出差異不會跟著改。若核定 30,000 元時顯示餘額 4,000 元，代表可能錯把估算合計當成實支合計扣除。</p>
<p class="body-text">測試完成後，把核定預算還原成 30,000 元，作為下一課的起始條件。下一課會沿用同一份標準資料生成工具，再把餐點數量改成 45 人；新增人數會改變估算合計，實支與核定上限則沿用原值，差異和餘額再依各自公式計算。若 27,000 元留在輸入欄，下一課的初始結果就無法與本頁基準對上。</p>
<p class="body-text">例外資料也要保留明確狀態。quantity 空白代表數量待確認，估算不能當成 0 元；unit_price 為負值或輸入非數字時，要指出欄位錯誤並暫停計算；actual 缺漏時，實支總額應標記待確認，不能悄悄略過。下一課會使用正常與例外資料完成生成工具的驗收。</p>
<div class="callout info"><div aria-hidden="true" class="callout-icon">i</div><div class="callout-body"><strong>本頁交接的是計算規則。</strong> 下方摘要保留欄位、公式與例外要求，方便下一課對照；它不是完整生成提示詞。下一課提供的<a href="BUDGET-2.html#prompt-budget">活動預算工具完整提示詞</a>包含角色、用途、欄位、公式、例外與單一 HTML 交付規格；當次資料與已知答案另外列出，可直接複製使用。</div></div>
<div class="prompt-wrap"><div class="prompt-label">計算規則摘要｜供下一課核對，不可單獨生成工具</div><p class="policy-guide">這份摘要用來對照處理規則；完整生成提示詞在接續教材，案例與核對答案另外提供。</p><pre class="prompt-box" data-reference-spec="true" id="prompt-policy-1">製作活動預算核銷表。逐項估算 = 數量 × 單價；支出差異 = 實支合計 − 估算合計；核定餘額 = 核定預算 − 實支合計。actual 欄代表每項整筆實支。空值不能預設為零；負數或非數值要提示。顯示公式口徑、來源資料和超支狀態，交付完整可操作的單頁 HTML。新增資料後先保留原始版本，再測正常值與例外值。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1" type="button">複製規則摘要</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-policy-status" role="status"></span></div></div></section><section class="lesson-section" id="completion"><h2 class="section-heading">把手算基準帶到預算工具製作</h2><p class="body-text">本頁完成的是估算、實支、差異與餘額的計算基準。接著閱讀<a href="BUDGET-2.html">預算工具生成與查核</a>，用相同資料核對工具，再改條件測試；當次數值與答案獨立保存，不放進程式的固定結果。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></main>
<!-- learner-content:end -->
