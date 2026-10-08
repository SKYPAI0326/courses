---
slug: gemini-ai
unit_id: CH5
title: 保存、交付並套用到自己的工作
course_type: skill-operation
version: 2026-10-08-five-chapters
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

<section class="lesson-section" id="ch5-section-1"><h2 class="section-heading">交付工具，也交付兩組可還原的輸入</h2><p class="body-text">第四章已留下通過原／新條件測試的修改版，以及可回復的初版。現在把成果整理成下次能使用、他人能接手的交付包：工具檔負責執行，資料備份保存輸入與設定，提示詞保存製作與修改方法。三者用途不同，需要分開保存。</p><p class="body-text">本章交付第四章完成的 v2。先在 v2 還原 A／B，再分別設定並核對新增規則，重新下載兩組備份。備份格式由工具自行處理，你只需下載、選檔還原，不必手寫 JSON。重開後除了人員與班次，也要核對新規則的開關、指定班種與上限。</p><p class="body-text">在「AI工作工具」下建立工具、資料、指令、報告、驗收、歷史版本。工具只放目前最後通過測試的版本；README寫實際檔名，失敗與舊版放歷史版本。從工具分別下載A、B資料備份，不能用課堂其他工具的檔案替代。</p><pre class="result-box">AI工作工具/
  README.txt
  工具/schedule-v2.html
  資料/schedule-A.json
  資料/schedule-B.json
  指令/prompt-schedule.txt
  報告/schedule-A.csv
  報告/schedule-B.csv
  驗收/acceptance.csv
  歷史版本/schedule-v1.html</pre><p class="body-text"><a download="" href="../assets/materials/prompt-schedule.txt">工具生成提示詞</a>、使用過的修復提示詞存入指令資料夾。CSV與列印結果放報告，A、B及例外的實際紀錄放驗收。資料備份保存當次輸入與設定；提示詞描述工具能力，兩者用途要在說明中交代清楚。</p></section>
<section class="lesson-section" id="ch5-section-2"><h2 class="section-heading">只靠文件還原兩組不同資料</h2><p class="body-text">重新開啟工具應回空白。還原驗收要確定整個輸入結構會換回來；只比姓名，可能漏掉日期、班種或需求人數。</p><ol class="body-text"><li>關閉工具，從成果資料夾開目前版本。核對空白表單，不應自動帶入A或B班表。</li><li>按「還原資料」選 schedule-A.json，確認四人、三日、兩班種、可排勾選與上限2。先沒有結果，再產生後應六班全滿、班數兩人兩班與兩人一班。</li><li>還原 schedule-B.json，確認五人、兩日、三班種及各自時間，可排皆勾選、上限2。重新產生應六個需求全滿，一人兩班、四人各一班。</li><li>在B狀態嘗試還原<a download="" href="../assets/materials/roster-invalid.json">錯誤資料檔</a>，應拒絕且保留B的完整輸入。重新產生仍有效，CSV應符合B，不能混有A的日期或班種。</li></ol><p class="body-text">資料缺項時，先確認備份來自同一份工具及正確版本。還原失敗抹掉現有資料，或A還原後仍保留B欄位，都需回生成對話修復，再重測A、B與錯誤檔。記錄尚未通過的項目，不能用「畫面有出現」代替。</p><p class="body-text">沿用<a download="" href="../assets/materials/core-acceptance.csv">五章驗收表</a>記錄重開與還原。測 A／B 原規則時先關閉新增限制；再啟用各自已核對的新設定重測。核對備份中的設定與班表結果，不只比較人名。</p></section>
<section class="lesson-section" id="ch5-section-3"><h2 class="section-heading">把可重用的操作方法寫進說明</h2><p class="body-text">把下方完整說明存成 README.txt，再依自己的實際檔名、設定及測試結果修改。README 是讓接手者知道從哪裡開始的使用說明；它要說清楚新規則如何開關、如何選班種，以及哪些結果已核對。</p><pre class="result-box">用途：小型排班規劃；使用者建立人員、日期、班種、時段與需求，再設定可排日期與限制。
入口：工具/schedule-v2.html；雙擊用瀏覽器離線開啟。完整工具不需安裝套件或重新呼叫模型。
支援：1–8人、1–7日期、1–4班種，每班需1–4人。正式人事規定、資格與法定工時需另確認。
新工作：新增、修改或刪除人員、日期、班種；填時段與需要人數，勾可排日期，設定每人總班數上限，再產生。
新增規則：預設關閉。啟用「指定班種每人次數上限」後，從目前清單選一個班種並填非負整數；零代表該班種不安排人員。關閉時使用原排班方式。
改資料：原結果失效，重新產生後才下載CSV或列印。指定班種被刪除時，先重新選擇並核對設定。
保存：資料/schedule-A.json和schedule-B.json由工具下載，保存原輸入與新增設定；關閉前先下載，不靠分頁保留資料。
重開：重新開啟工具，選「還原資料」載入自己的備份；先核對人員、日期、班種、可排日、總上限與新規則，再產生班表。
錯誤：還原失敗保留原輸入；檢查是否選到本版本適用的備份。功能出錯時回歷史版本/schedule-v1.html，修正另存後重測。
已核對資料：填上自己A/B案例、新規則設定、實際結果及測試日期；未測項目明列待確認。
檢查方法：核對需求、可排日期、同日一班、總班數及指定班種上限；缺額保留原因，由負責人調整工作條件。
方法來源：指令/prompt-schedule.txt及prompt-solo-schedule.txt是結構與修改方法；案例資料另存，不把人名或答案寫死。
交付限制：工具是教學驗證的小型規劃成果；未核對正式組織規則，不直接視為已核准班表。</pre><p class="body-text">找一位沒參與製作的人，請他照README換一組自己的資料，或由自己關閉全部分頁後只照文件操作，記為作者自測。卡在人員、日期或班種怎麼新增時，先補上說明或修工具，再測。完成後將已核對的結果與未測條件寫入交付說明。</p><p class="body-text">其他案例保存方式留在<a href="../part4/SUPP4-1.html">多案例成果保存補充頁</a>；本次成果是可換資料的排班工具與實際驗收證據。</p></section>
<section class="lesson-section" id="handover"><h2 class="section-heading">交付工具結構、使用方法與測試證據</h2><p class="body-text">README新增「指定班種次數限制」的開關、班種選擇、上限與例外。保存新版本、完整追加指令、A/B新備份、CSV與測試紀錄，舊版留在歷史版本。關閉後還原兩份新備份，核對不同人數、日期、班種與新設定。</p><p class="body-text">最後用<a download="" href="../assets/materials/tool-structure-worksheet.md">工具結構工作表</a>寫一項自己的工作：哪些資料由使用者填、哪些規則可設定、工具怎麼處理、要留下什麼結果、錯誤如何保留與修正。選預算或交辦工作也可以，但只換標題、人名或故事不算新的工具設計；必須指出欄位、處理與驗收如何改變。</p><p class="body-text">交付物是能換資料的工具、自己寫的完整規格及驗收證據。未驗證的動態欄位、輸出與還原要照實標示。其他挑戰保留在<a href="../part4/SUPP4-3.html">多案例改造補充頁</a>。</p></section>
<section class="lesson-section" id="transfer"><h2 class="section-heading">用資料清理完成一次跨工具交付</h2><p class="body-text">前面已交付排班工具，現在用另一種工作驗證能否獨立重用方法。假設每次收到CSV，你都需要找出必填空白、錯誤數字與重複識別碼；處理方式改為逐列檢查及分流，不能沿用排班的可排條件。這個任務有新工具結構、兩組不同欄位和明確完成物。</p><p class="body-text">到<a href="../playground/PG01.html">CSV清理完整案例</a>先讀背景與示範，下載<a href="../assets/playground/PG01/prompt.txt">可重用提示詞</a>、<a href="../assets/playground/PG01/cases.txt">A／B欄位設定</a>、<a href="../assets/playground/PG01/input-a.csv">A資料</a>、<a href="../assets/playground/PG01/input-b.csv">B資料</a>。先自行生成一個空白可操作單檔工具，保存為csv-check-v1.html；遇到生成失敗，可先操作案例的作者參考品確認規則，再回對話修正自己的版本。</p><ol class="step-list"><li>依A設定唯一鍵record_id、必填欄及數字規則，匯入6列。先預測哪些列有效，再逐列核對原因。</li><li>結果應有2列有效、4列待修正。兩份輸出列數合計仍6，不得默默刪掉重複或錯誤列。逐列核對原值和原因，再重新匯入下載檔確認欄位對齊。</li><li>切換B：唯一鍵case_no，改用另一組必填及數字欄，不能沿用A欄名。4列中3列有效、1列待修正，缺值不補成0。</li><li>修正A中一筆錯誤數字再重跑，預期有效列增加、待修正減少；另新增重複鍵，原始列仍保留並指出原因。任何不符都記入自己的驗收表再修復。</li><li>交付工具、兩組原始CSV、各組有效/待修正輸出、提示詞及README。README寫唯一鍵與規則怎麼選、如何匯入匯出，以及哪些項目實際測過。</li></ol><p class="body-text">完成標準是別人只靠README能用兩組資料重現你記錄的結果。列數、欄名、原因、輸出均需核對；只有寫一份新需求還不足以完成這項任務。此跨工具任務可作課後完整交付，不以趕做時間省略驗收。</p><p class="body-text">再用<a download="" href="../assets/materials/tool-structure-worksheet.md">工具結構工作表</a>整理自己的下一項需求；到<a href="../playground/index.html">案例遊樂園</a>選不同處理方式參考，必要時讀<a href="../index.html#supplements">保存與部署延伸參考</a>。五章主線到此完成，遊樂園依工作用途選用。</p></section>

<!-- learner-content:end -->
