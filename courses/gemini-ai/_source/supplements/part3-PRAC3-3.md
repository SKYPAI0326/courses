---
slug: gemini-ai
unit_id: SUPP-part3-PRAC3-3
title: 用 KPI 月報做一項工作判斷
course_type: skill-operation
version: 2026-10-08-five-chapters
---

正式來源；保留原教學素材、完整提示詞、範例、操作及答案。作者文案審閱與實測分開記錄。

<!-- learner-content:start -->
<div class="lesson-body"><section class="lesson-section" id="reading-guide"><h2 class="section-heading">這頁怎麼用</h2><p class="body-text">需要把不同方向的 KPI 整理成月報時，使用這頁。 完成第三章後使用；下方提供三項 KPI 資料與月報參考品。</p><ol class="step-list"><li>先下載三項資料，判斷件數、處理時間與錯誤率是越大越好還是越小越好。</li><li>先寫出是否達標的答案，再生成月報核對；零目標與缺值也要測。</li></ol></section><section class="lesson-section" id="core-1"><h2 class="section-heading">先判斷，再生成月報</h2><p class="body-text">下載 <a download="" href="../assets/materials/kpi-normal.csv">三項 KPI 資料</a>。件數越大越好；處理時間與錯誤率越小越好。先寫下 120 件、5 天、1% 各自是否達標，再看 <a href="../assets/tools/kpi-reference.html" rel="noopener" target="_blank">月報參考品</a> · <a download="" href="../assets/tools/kpi-reference.html">下載 HTML 參考檔</a>。</p><details><summary>完成預判後核對答案</summary><p class="body-text">受理件數 120≥100，已達標；處理時間 5&gt;3，未達標；錯誤率 1≤2，已達標。處理時間變長 25%，不能解讀成績效更好。件數較上期 +33.3%；錯誤率較上期 -33.3%。</p></details><p class="body-text"><a download="" href="../assets/materials/prompt-kpi.txt">下載完整生成指令 TXT</a></p><p class="policy-guide">這一區定義可重用的輸入、設定、處理與輸出。案例條件另附；參考品中的預填資料只供示範，可在自己的工具中替換。</p><pre class="result-box" data-policy-prompt="工具生成或修改" id="prompt-kpi">請製作部門 KPI 月報，單一完整 HTML，CSS/JavaScript 全內嵌、不用外部套件，不呼叫 AI。
每個指標有名稱、單位、方向（越大越好／越小越好）、目標、實際、上期、期間與來源。CSV交換欄名使用metric、unit、direction、target、actual、previous、period、source；方向欄用higher或lower。工具提供可下載範本及中文欄位對照，使用者只需填表或匯入，不編寫JSON。可新增編輯；CSV 匯入要驗證欄位、引號及非負數值。缺值不當零。
越大越好時，實際大於或等於目標代表達標；越小越好時，實際小於或等於目標代表達標。達標文字必須遵照方向，不用同一個 實際／目標 百分比當所有指標的分數。圖表顯示目標與實際的比較，補文字、單位和方向，不能只靠顏色。上期變化=（實際−上期）／上期×100%；上期為零 或缺值時顯示不可計算。目標為零 仍可判斷達標，但不計達成率。錯誤率以1代表1%，不可變成100%。
下載月報 CSV、列印另存 PDF、本機保存、JSON備份還原；匯入 JSON 先驗證資料再覆蓋，無效檔案保留目前資料並提示。缺數值可交付但須顯示待確認；指標、單位、期間或來源缺漏須阻止匯出。數字只說結果，不生成沒有證據的原因。手機表格容器可橫向滑動。只輸出完整 HTML 不省略。

【資料與設定的重用方式】
工具依使用者在畫面輸入的資料與設定處理。若另外附上當次案例條件，只用於可修改的示例或測試；未附時顯示空白輸入與操作說明，不自行編造資料。案例的名稱、日期、金額、門檻及預期答案不能成為程式的固定條件或特例。更換資料後仍依同一套規則計算；請保留新增、修改及清除資料的操作。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-kpi" type="button">複製可重用提示詞</button><span aria-live="polite" class="policy-status" id="prompt-kpi-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-kpi"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-kpi-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

預設：受理件數 件 higher 目標100 實際120 上期90；處理時間 天 lower 目標3 實際5 上期4；錯誤率 % lower 目標2 實際1 上期1.5。期間2026-09，來源分別案件台帳、結案台帳、複核紀錄。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-kpi-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-kpi-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p><p><a download="" href="../assets/materials/prompt-kpi-case.txt">下載此區案例TXT</a>，可獨立附加或換成自己的資料。</p></aside></section>
<section class="lesson-section" id="core-2"><h2 class="section-heading">同步操作：讓資料可以更新</h2><p class="body-text">沿用<a href="../chapters/CH1.html#save-open">第一章的存檔方法</a>，將這次完整 HTML 保存為 <strong>department-kpi.html</strong>。雙擊後應開成工具；看到程式文字時，回存檔步驟檢查純文字格式與 .html 副檔名。若修復後另存 v2，完成重測後以通過驗收的版本作為交付入口，保留舊版作歷史。</p><ol class="body-text"><li>生成後核對三個達標狀態與上期變化，檢查圖表單位；每個測試在驗收表新增一列，先填版本、資料條件與預期答案。</li><li>在原始 5 天資料下下載 JSON 備份，命名 <strong>department-kpi-backup.json</strong>，存入「資料」資料夾。</li><li>將處理時間由 5 改成 2 天，先預判再操作；應改為已達標。工作判讀寫：「本期處理時間為 2 天，低於 3 天目標；較上期 4 天縮短 50%。」註明結案台帳為來源，不推測原因。</li><li>保存此狀態的 CSV 與 PDF，再用 department-kpi-backup.json 還原；三項數值應回到 120 件、5 天、1%。將還原觀察記入另一列，保留這份 JSON，供多案例成果保存補充頁的重開測試使用。</li></ol></section>
<section class="lesson-section" id="core-3"><h2 class="section-heading">例外：基期零、缺值與零目標</h2><p class="body-text">匯入 <a download="" href="../assets/materials/kpi-exceptions.csv">例外資料</a>。新增服務上期為 0，本期 12：可判達標，但變化百分比不可計算。回覆時間實際缺漏：狀態待確認。錯誤率目標 0、實際 0：達標，不算 actual/target。</p><p class="body-text">出現不符合規則的結果時，先另記操作、實際結果與預期，再使用下方通用修復指令，保存修正版並重測。</p><pre class="prompt-box" data-policy-prompt="工具修復" id="prompt-kpi-repair">請修正目前KPI工具的缺值與比較規則：空值保持未知，基期為零時不計變化率；依每個指標設定的越高或越低越好判讀，不以達成率統一判所有指標。依另附的測試操作、實際結果與預期找出原因，不按特定指標名稱或數值寫特例。保留原有輸入、匯入匯出與備份，交付完整修正版，讓我重測正常與例外資料。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-kpi-repair" type="button">複製通用修復提示詞</button><span aria-live="polite" class="policy-status" id="prompt-kpi-repair-policy-status" role="status"></span></div><aside class="policy-case" data-policy-case="prompt-kpi-repair"><h3>當次案例條件與核對紀錄｜可替換</h3><p>先複製上方提示詞建立工具。需要本課示例時，可另外附加這一區，或在工具完成後填入相應欄位。未附案例時，仍須能建立工具；更換案例資料時不必重寫處理規則。</p><pre id="prompt-kpi-repair-case">【當次案例附加資料，可替換】
以下僅供本次示例與測試。請把資料放入可修改的輸入或設定；核對答案只用於驗收，不能編成程式的固定結果。

當次錯誤紀錄：例外資料中未知實際值被顯示為0%；預期保持未知。保存v2，再測正常三項與例外三項。</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="prompt-kpi-repair-case" type="button">複製當次案例附加資料</button><span aria-live="polite" class="policy-status" id="prompt-kpi-repair-case-policy-status" role="status"></span></div><p>完成本次核對後，至少再換一組不同名稱、數值或清單長度測試，確認結果來自輸入與規則。</p></aside></section><section class="lesson-section" id="completion"><h2 class="section-heading">用指標方向說明下一個工作行動</h2><p class="body-text">留下原資料、指標方向、實際結果及一項工作判斷。越低越好的指標要用相反方向判讀；缺值與零基期保留無法計算或待確認。下次換資料時先核對這些條件，再用圖表討論行動。</p><p class="body-text">回到<a href="../index.html#supplements">補充教材目錄</a>，依下一個工作需求選擇教材。</p></section><section class="lesson-section" id="playground-acceptance"><h2 class="section-heading">在遊樂園換一組資料，確認學會這個工具的結構</h2><p class="body-text">前面的示範讓你看見「依越高/越低越好讀取差異」如何落到畫面。本區把兩組資料和核對結果分開，讓你確認工具能承接新輸入。先依本頁完整提示詞生成工具，再按第一章方法保存和重開；可先操作本頁作者參考品理解反應，兩者的測試紀錄分開保存。</p><p class="body-text"><a download="" href="../assets/playground/E09/prompt.txt">下載可重用結構提示詞</a>、<a download="" href="../assets/playground/E09/cases.txt">A／B案例資料</a>與<a href="../assets/playground/E09/answers.md">核對依據</a>。素材為虛構或測試資料，依本頁表單逐欄輸入；原參考畫面的預填值只供示範。</p><div class="core-table-scroll"><table><thead><tr><th>測試</th><th>本次輸入與操作</th><th>核對結果</th></tr></thead><tbody><tr><td>A</td><td>越高越好：目標100、實際120、前期90；越低越好：目標3日、實際5日、前期4日。</td><td>第一項達標且比前期提高33.33%；第二項未達標且變差，不能把增加當改善。</td></tr><tr><td>B</td><td>越低越好：目標2%、實際1%、前期1.5%。</td><td>達標；比前期減少0.5個百分點，相對下降33.33%，兩種差異名稱分開。</td></tr><tr><td>例外</td><td colspan="2">前期0時相對變動未定義；缺值/未知方向列待確認，不編改善原因。</td></tr></tbody></table></div><div class="prompt-wrap"><div class="prompt-label">A／B與例外｜當次資料另附</div><pre id="e09-transfer-case">KPI 月報與方向判斷｜當次案例資料（可替換）

A
越高越好：目標100、實際120、前期90；越低越好：目標3日、實際5日、前期4日。

B
越低越好：目標2%、實際1%、前期1.5%。

例外
前期0時相對變動未定義；缺值/未知方向列待確認，不編改善原因。

先生成空白可操作工具，案例只用於輸入與查核。依頁面欄位填入或貼入資料，不把答案寫成工具固定輸出。
</pre><div class="policy-copy-row"><button class="copy-btn" data-policy-copy="e09-transfer-case" type="button">複製當次測試資料</button><span aria-live="polite" class="policy-status" id="e09-transfer-case-policy-status" role="status"></span></div></div><ol class="step-list"><li>先只讀資料，寫下你預期的中間結果及畫面反應。</li><li>輸入A，逐欄核對，不只確認畫面有出現。</li><li>清除或替換為B，確認同一工具依新資料重算；有匯出功能時核對下載內容。</li><li>測試例外；失敗時記輸入、實際、預期，依第四章要求修復，再重跑A與B。</li><li>按第五章保存工具、資料、提示詞與說明，留下自己的實際測試紀錄。</li></ol><p class="body-text">完成後回<a href="../playground/index.html">案例遊樂園</a>選另一種處理方式。換案例時先改輸入、設定和核對依據，工具的處理規則保持清楚；若工作方法不同，重新整理需求再生成。</p></section></div>
<!-- learner-content:end -->
