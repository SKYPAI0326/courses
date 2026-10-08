# Gemini AI 學員素材包

五章依序完成生成體驗、可重用需求、排班初版、追加規則與保存交付。第三至第五章沿用同一份排班工具；獨立遊樂園有29例，另有13份延伸參考。全部案例是虛構教學資料。

## 從章節找到需要的檔案

| 章節 | 使用素材 | 留下的成果 |
| --- | --- | --- |
| 第一章：第一個小工具 | prompt-snake.txt；prompt-snake-case.txt；prompt-snake-revision.txt | 自己生成的 snake-v1.html、v2 及差異說明 |
| 第二章：可重用提示詞 | tool-structure-worksheet.md；requirements-template.txt | 完整白話需求；當次案例另存；操作計算與多條件判斷 |
| 第三章：工作工具初版 | prompt-schedule.txt；schedule-practice.txt；schedule-answers.md；core-acceptance.csv | schedule-v1.html、自己下載的 A／B 備份、班表和測試紀錄 |
| 第四章：追加與修正 | prompt-solo-schedule.txt；prompt-schedule-repair.txt；prompt-budget-warning.txt；core-acceptance.csv | schedule-v3.html、保留 v1 與 v2、新舊規則測試紀錄 |
| 第五章：保存與交付 | 同一份驗收表；自己下載的 v3 備份；講義 README 範例 | 排班交付包；另用PG01 CSV清理完成A/B及交付 |

## 提示詞與當次條件如何搭配

先貼 prompt-*.txt 中的工具結構，說明可編輯輸入、規則、處理、輸出和例外。若需要課堂示例，再獨立附加 prompt-*-case.txt，或在工具完成後填入畫面。案例名稱、日期、數值及核對答案都不能變成程式特例；未附案例也應能建立空白工具。

排班的 A／B 資料見 schedule-practice.txt。先手排或預判，再用 schedule-answers.md 核對；排法可以不同，只要滿足相同需求與限制。第四章新增的班種限制也應由畫面選擇與設定。備份 JSON 由工具下載和讀取，不需要學員手寫 JSON。不同工具與版本的備份格式不保證互通；第五章先用自己的同版備份還原。

## 驗收表怎麼填

core-acceptance.csv 對應五章主線；acceptance-template.csv 保留預算、KPI、會議等補充案例的測試。兩份 CSV 都是 UTF-8（含 BOM），可用試算表開啟。

每個測試保留一列。操作前填工具檔名／版本、輸入設定與預期答案；操作後填觀察、狀態，以及需要時的修復指令和重測結果。來源方式填「學員生成」或「參考品」，未操作就保留「待測」。參考品通過不能記為自己的生成成果通過。

例如填入三格蛇身、食物十分、增長一格，預期第一次吃到食物後分數十、蛇長四；操作後才填實際看到的數字。這是填法說明，並非學員實測紀錄。排班換 B 或追加規則時新增測試列，保留 A 的原紀錄。

## 補充教材素材

預算：budget-normal.csv 搭配核定 30000；budget-invalid.csv 用來查缺值與負數；budget-transfer.csv 搭配核定 25000，核對新資料及低餘額提醒。

KPI：kpi-normal.csv 核對越大越好／越小越好的方向；kpi-exceptions.csv 核對零基期、缺值與零目標。

會議：meeting-a.txt 核對初次判讀；meeting-b.txt 核對更新、取消與未知；meeting-c.txt 核對新增前置任務欄位。prompt-meeting.txt 與 prompt-solo-meeting.txt 分別描述生成和修改方法。AI Studio Build 的模型功能需在實際帳號環境另測。

其餘 prompt-*.txt 與各自案例檔供對應補充頁使用。reference-answers.json 是作者核對答案；先判斷再展開。roster-normal/transfer/conflict/invalid.json 是保留的舊版小型案例資料，不能直接取代自己生成工具的備份。

## 保存與重開

按照第五章建立「工具、資料、指令、報告、驗收、歷史版本」資料夾。工具只放實際通過測試的目前版本；舊版保留於歷史版本。README 寫自己的檔名、操作、資料還原方法、新規則設定與已測／未測範圍。關閉工具後，只照文件重開並還原 A／B，再核對原規則與新增規則。

作者參考品位於 ../tools/：snake-basic-reference.html 供第一章經典操作；snake-color-reference.html 供配色修改前後比較；schedule-reference.html 供基礎排班核對。schedule-v2-reference.html是第四章指定班種上限的作者修改版；claim-check-reference.html供第二章條件初檢，budget-warning-reference.html供第四章可調提醒。會議固定答案參考頁沒有呼叫模型。參考品都不是學員生成證據。

遊樂園材料在 ../playground/：每例有prompt.txt、cases.txt及answers.md。PG01至PG06另有CSV及作者工具。playground-materials.zip包含29例材料與本核心素材；提示詞描述結構、案例另附，真人與Gemini結果均須自行測試。

materials.zip 逐檔包含本目錄素材（不含 ZIP 本身）。
