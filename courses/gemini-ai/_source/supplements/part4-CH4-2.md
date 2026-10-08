---
slug: gemini-ai
unit_id: SUPP-part4-CH4-2
title: 建立專屬 Prompt 庫：打造你的數位資產
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<main class="lesson-body"><section class="lesson-section" id="prompt-card-context">
<h2 class="section-heading">情境：月報提示詞每次重寫，容易漏掉同一條規則</h2>
<p class="body-text">每月要把部門 KPI 整理成主管看得懂的摘要。若只保存一句「幫我分析數據」，下次可能漏掉指標方向、來源、零基期或「不可推測原因」等規則。本單元的交付物是一張可重用、可測試和可更新的提示詞卡。</p>
<div class="prompt-wrap"><div class="prompt-label">提示詞卡需要保存的欄位</div><pre class="result-box">名稱與用途｜適用輸入｜需替換欄位｜完整提示詞｜測試資料與預期答案｜最後測試日期｜版本｜限制與負責人</pre></div>
<p class="body-text">提示詞是工作規格的一部分，不是通用魔法句。只保存經過測試的版本，並記錄上一版在哪些資料和條件下有效；換模型或輸入格式後仍需重新測試。</p>
</section>
<section class="lesson-section" id="prompt-card-example">
<h2 class="section-heading">把 KPI 月報規則寫成一張完整提示詞卡</h2>
<p class="body-text">使用三項示例指標，先分清「件數越高越好」與「處理時間、錯誤率越低越好」。提示詞要求模型只整理資料，不解釋沒有來源支持的原因。</p>
<div class="prompt-wrap"><div class="prompt-label">提示詞卡：部門 KPI 月報摘要 V1</div><pre class="prompt-box" data-policy-prompt="文字分析" id="prompt-policy-1">你是部門營運分析助理。請只根據我提供的 KPI 表格撰寫本月工作摘要，不補充表格沒有的事實。

每筆資料包含：指標、單位、方向（higher 越高越好／lower 越低越好）、目標、實際、上期、期間和來源。
請輸出：
1. 每項指標的實際值、目標、是否達標、上期變化與來源。
2. 兩至三句主管摘要，指出達標項、未達標項和需要追問的資料。
3. 缺值或來源不明時標「待確認」；上期為 0 或缺值時，不計算變化率。
4. 不要把相關變化寫成原因，不要把百分比和百分點混用；以繁體中文呈現。

使用前先確認方向和資料期間；若欄位缺少方向、單位或來源，先列出缺欄，不要推論。輸出保持簡潔、可追溯，每個結論都附上表格欄位依據。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-policy-1" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-policy-1-policy-status" role="status"></span></div></div>
</section>
<section class="lesson-section" id="prompt-card-test">
<h2 class="section-heading">用固定資料測試，改版後保留舊答案</h2>
<ol class="body-text">
<li>把提示詞保存為一張卡，填入名稱「部門 KPI 月報摘要」、用途、欄位格式、版本 V1 和最後測試日期。</li>
<li>載入 <a download="" href="../assets/materials/kpi-normal.csv">課程 KPI 資料</a>。預期：受理件數 120/100，higher，達標；處理時間 5/3，lower，未達標；錯誤率 1%/2%，lower，達標。上期變化依序約 +33.3%、+25%、−33.3%。</li>
<li>把處理時間改為 2 天再測；應變為達標，較上期 4 天減少 50%。若模型推測原因，記下來源不足並修正提示詞，只允許描述數字本身。</li>
<li>在 V2 卡中記錄改動項和測試結果，保留 V1 歷史。將驗證通過的卡片匯入下一單元的 Prompt 庫，測試搜尋、匯出和還原。</li>
</ol>
<div class="callout info"><div aria-hidden="true" class="callout-icon">注意</div><div class="callout-body">使用假資料或經核准的資料；提示詞卡不是資料庫，也不自動更新平台模型或規則。不得把機密或 API 金鑰放進卡片。</div></div>
<div class="callout key"><div aria-hidden="true" class="callout-icon">✓</div><div class="callout-body"><strong>本單元驗收：</strong>交付一張含完整提示詞、三筆預期答案、版本紀錄和限制的卡片；修改一項規則後，能用相同資料重跑並說明差異。</div></div>
</section><section class="lesson-section" id="completion"><h2 class="section-heading">讓提示詞能找回，也能判斷是否適用</h2><p class="body-text">提示詞庫應連到用途、所需輸入、版本及實際測試紀錄。下次選用先看適用條件，再替換獨立資料；保存了很多文字，還不等於每份指令都能完成工作。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section></main>
<!-- learner-content:end -->
