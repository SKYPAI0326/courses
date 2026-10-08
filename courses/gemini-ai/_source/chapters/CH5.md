---
slug: gemini-ai
unit_id: CH5
title: 保存、交付並套用到自己的工作
course_type: skill-operation
version: 2026-10-09-instructor-repair
duration: 45
dependencies: ["CH4"]
learning_objective: 保存、交付並套用到自己的工作
platform_version: Gemini web; official help checked 2026-10-08; account generation pending
---

# 保存、交付並套用到自己的工作

正式正文以下列learner-content範圍為唯一來源；HTML從此範圍轉製。內部設計依據：課程根目錄 _repair/2026-10-08/CHAPTER-REDESIGN.md。
環境：桌面瀏覽器、可登入的Gemini帳號、UTF-8純文字存檔。引用的作者參考品只能證明操作／規則，不代表授課平台生成。真人跟做及六小時試教待驗。
來源：part4/CH4-1.html；跨章交付段落另見遷移紀錄。

<!-- learner-content:start -->
<section class="lesson-section" id="ch5-section-1"><h2 class="section-heading">整理排班交付包，留下兩組能還原的資料</h2><p class="body-text">第四章已留下測過新舊規則的 <code>schedule-v3.html</code>，以及可回復的 v2。這一章先在課堂完成排班交付包，再於課後獨立製作 CSV 清理工具，用兩組資料測試並交付。課內45分鐘是規劃值，第二個工具的完整交付不計入這段時間。</p><p class="body-text">打開 <code>schedule-v3.html</code>，先還原第三章由自己工具下載的 A／B 舊備份，確認新限制關閉。分別設定本章要保存的新增限制：A 啟用早班上限1，B 啟用收尾上限1；重新產生並核對後，下載新備份，另命名 <code>schedule-A-v3.json</code>和 <code>schedule-B-v3.json</code>。舊備份留在歷史版本，先不要覆寫。JSON 是工具處理的備份檔，你只需下載及選檔還原，不必改內容。</p><p class="body-text">在「AI工作工具」資料夾建立工具、資料、指令、報告、驗收、歷史版本。工具只放最後通過測試的版本；README 使用說明寫實際檔名。資料存 v3 下載的新備份，舊工具與舊備份放歷史版本。範例如下：</p><pre class="result-box">AI工作工具/
  README.txt
  工具/schedule-v3.html
  資料/schedule-A-v3.json
  資料/schedule-B-v3.json
  指令/prompt-schedule.txt
  指令/prompt-solo-schedule.txt
  指令/prompt-schedule-rule-repair.txt（用過修復時保存）
  報告/schedule-A.csv
  報告/schedule-B.csv
  驗收/acceptance.csv
  歷史版本/schedule-v1.html
  歷史版本/schedule-v2.html
  歷史版本/schedule-A.json
  歷史版本/schedule-B.json</pre><p class="body-text"><a download="" href="../assets/materials/prompt-schedule.txt">工具生成提示詞</a>、使用過的修復提示詞存入指令資料夾。CSV與列印結果放報告，A、B及例外的實際紀錄放驗收。資料備份保存當次輸入與設定；提示詞描述工具能力，兩者用途要在說明中交代清楚。</p></section>
<section class="lesson-section" id="ch5-section-2"><h2 class="section-heading">只靠文件還原兩組不同資料</h2><p class="body-text">重新開啟工具應回空白。還原驗收要確定整個輸入結構會換回來；只比姓名，可能漏掉日期、班種或需求人數。</p><ol class="body-text"><li>關閉工具，從成果資料夾開目前版本。核對空白表單，不應自動帶入A或B班表。</li><li>選「還原資料」，載入 <code>schedule-A-v3.json</code>。確認四人、三日、兩班種、可排日、總上限2，新增限制啟用、早班上限1。先沒有班表；產生後應六班全滿，三個早班由不同人負責，其他規則仍成立。</li><li>再載入 <code>schedule-B-v3.json</code>。確認五人、兩日、三班種與時段、可排皆勾選、總上限2，新增限制啟用、收尾上限1。重新產生應六班全滿，兩次收尾由不同人負責。</li><li>在B狀態嘗試還原<a download="" href="../assets/materials/roster-invalid.json">錯誤資料檔</a>，應拒絕且保留B的完整輸入。重新產生仍有效，CSV應符合B，不能混有A的日期或班種。</li></ol><p class="body-text">資料缺項時，先確認備份來自同一份工具及正確版本。還原失敗抹掉現有資料，或A還原後仍保留B欄位，都需回生成對話修復，再重測A、B與錯誤檔。記錄尚未通過的項目，不能用「畫面有出現」代替。</p><p class="body-text">沿用<a download="" href="../assets/materials/core-acceptance.csv">五章驗收表</a>記錄重開與還原。測 A／B 原規則時先關閉新增限制；再啟用各自已核對的新設定重測。核對備份中的設定與班表結果，不只比較人名。</p></section>
<section class="lesson-section" id="ch5-section-3"><h2 class="section-heading">把可重用的操作方法寫進說明</h2><p class="body-text">把下方完整說明存成 README.txt，再依自己的實際檔名、設定及測試結果修改。README 是讓接手者知道從哪裡開始的使用說明；它要說清楚新規則如何開關、如何選班種，以及哪些結果已核對。</p><pre class="result-box">用途：小型排班規劃；使用者建立人員、日期、班種、時段與需求，再設定可排日期與限制。
入口：工具/schedule-v3.html；雙擊用瀏覽器離線開啟。完整工具不需安裝套件或重新呼叫模型。
支援：1–8人、1–7日期、1–4班種，每班需1–4人。正式人事規定、資格與法定工時需另確認。
新工作：新增、修改或刪除人員、日期、班種；填時段與需要人數，勾可排日期，設定每人總班數上限，再產生。
新增規則：預設關閉。啟用「指定班種每人次數上限」後，從目前清單選一個班種並填非負整數；零代表該班種不安排人員。關閉時使用原排班方式。
改資料：原結果失效，重新產生後才下載CSV或列印。指定班種被刪除時，先重新選擇並核對設定。
保存：資料/schedule-A-v3.json和schedule-B-v3.json由工具下載，保存原輸入與新增設定；關閉前先下載，不靠分頁保留資料。
重開：重新開啟工具，選「還原資料」載入自己的備份；先核對人員、日期、班種、可排日、總上限與新規則，再產生班表。
錯誤：還原失敗保留原輸入；檢查是否選到本版本適用的備份。功能出錯時先回歷史版本/schedule-v2.html及它適用的舊備份，按原規則處理；v2不提供新增班種限制。修復v3後再測，不直接把v3新備份交給v2。
已核對資料：填上自己A/B案例、新規則設定、實際結果及測試日期；未測項目明列待確認。
檢查方法：核對需求、可排日期、同日一班、總班數及指定班種上限；缺額保留原因，由負責人調整工作條件。
方法來源：指令/prompt-schedule.txt及prompt-solo-schedule.txt是結構與修改方法；案例資料另存，不把人名或答案寫死。
交付限制：工具是教學驗證的小型規劃成果；未核對正式組織規則，不直接視為已核准班表。</pre><p class="body-text">找一位沒參與製作的人，請他照README換一組自己的資料，或由自己關閉全部分頁後只照文件操作，記為作者自測。卡在人員、日期或班種怎麼新增時，先補上說明或修工具，再測。完成後將已核對的結果與未測條件寫入交付說明。</p><p class="body-text">其他案例保存方式留在<a href="../part4/SUPP4-1.html">多案例成果保存補充頁</a>；本次成果是可換資料的排班工具與實際驗收證據。</p></section>
<section class="lesson-section" id="handover"><h2 class="section-heading">交付工具結構、使用方法與測試證據</h2><p class="body-text">README新增「指定班種次數限制」的開關、班種選擇、上限與例外。保存新版本、完整追加指令、A/B新備份、CSV與測試紀錄，舊版留在歷史版本。關閉後還原兩份新備份，核對不同人數、日期、班種與新設定。</p><p class="body-text">最後用<a download="" href="../assets/materials/tool-structure-worksheet.md">工具結構工作表</a>寫一項自己的工作：哪些資料由使用者填、哪些規則可設定、工具怎麼處理、要留下什麼結果、錯誤如何保留與修正。選預算或交辦工作也可以，但只換標題、人名或故事不算新的工具設計；必須指出欄位、處理與驗收如何改變。</p><p class="body-text">交付物是能換資料的工具、自己寫的完整規格及驗收證據。未驗證的動態欄位、輸出與還原要照實標示。其他挑戰保留在<a href="../part4/SUPP4-3.html">多案例改造補充頁</a>。</p><div class="prac-box"><p class="body-text"><strong>課堂完成點：</strong>交付包包含 v3、v1/v2 歷史版本、A／B 新備份、兩份班表、製作與修改指令、使用說明及測試紀錄。關閉所有工具分頁後，只照 README 重開、還原 A／B 並重現記錄結果，才完成課內任務。</p></div></section>
<section class="lesson-section" id="transfer"><h2 class="section-heading">必做課後任務：再做一個資料清理工具並交付</h2><p class="body-text">課堂內先讀清任務並確認能下載材料；完整製作與驗收安排在課後。繳交日期由講師在上課時宣布，請記入自己的驗收表。若自學，完成下列交付及重開測試後，再將這項能力記為完成。</p><p class="body-text">前面已交付排班工具，現在用另一種工作驗證能否獨立重用方法。假設每次收到CSV，你都需要找出必填空白、錯誤數字與重複識別碼；處理方式改為逐列檢查及分流，不能沿用排班的可排條件。這個任務有新工具結構、兩組不同欄位和明確完成物。</p><p class="body-text">到<a href="../playground/PG01.html">CSV清理完整案例</a>先讀背景與示範，下載<a href="../assets/playground/PG01/prompt.txt">可重用提示詞</a>、<a href="../assets/playground/PG01/cases.txt">A／B欄位設定</a>、<a href="../assets/playground/PG01/input-a.csv">A資料</a>、<a href="../assets/playground/PG01/input-b.csv">B資料</a>。先自行生成一個空白可操作單檔工具，保存為csv-check-v1.html；遇到生成失敗，可先操作案例的作者參考品確認規則，再回對話修正自己的版本。</p><ol class="step-list"><li>依A設定唯一鍵record_id、必填欄及數字規則，匯入6列。先預測哪些列有效，再逐列核對原因。</li><li>結果應有2列有效、4列待修正。兩份輸出列數合計仍6，不得默默刪掉重複或錯誤列。逐列核對原值和原因，再重新匯入下載檔確認欄位對齊。</li><li>切換B：唯一鍵case_no，改用另一組必填及數字欄，不能沿用A欄名。4列中3列有效、1列待修正，缺值不補成0。</li><li>修正A中一筆錯誤數字再重跑，預期有效列增加、待修正減少；另新增重複鍵，原始列仍保留並指出原因。任何不符都記入自己的驗收表再修復。</li><li>交付工具、兩組原始CSV、各組有效/待修正輸出、提示詞及README。README寫唯一鍵與規則怎麼選、如何匯入匯出，以及哪些項目實際測過。</li></ol><p class="body-text">完成標準：接手者只靠 README，能以 A／B 原始資料和各自設定重現你記錄的有效列、待修正列與原因，並打開輸出確認欄位正確。課後需交付完整工具、兩組輸入與輸出、提示詞、README 及驗收表。只有新需求或參考工具操作紀錄，尚未完成這項獨立製作任務。</p><p class="body-text">再用<a download="" href="../assets/materials/tool-structure-worksheet.md">工具結構工作表</a>整理自己的下一項需求；到<a href="../playground/index.html">案例遊樂園</a>選不同處理方式參考，必要時讀<a href="../index.html#supplements">保存與部署延伸參考</a>。五章主線到此完成，遊樂園依工作用途選用。</p></section>
<!-- learner-content:end -->
