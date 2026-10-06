# 學員素材包

全部是虛構教學資料。CSV 為 UTF-8（含 BOM），可用試算表開啟，也可匯入參考工具；逐字稿 TXT 為完整輸入。`reference-answers.json` 是答案，先預判再展開核對。

預算：`budget-normal.csv` 配核定 30000；`budget-invalid.csv` 查缺值與負數防呆；`budget-transfer.csv` 配核定 25000，供獨立遷移與低餘額提醒驗收。

KPI：`kpi-normal.csv` 查越大越好／越小越好的方向；`kpi-exceptions.csv` 查零基期、缺值與零目標。

交辦：`meeting-a.txt` 練第一次判讀；`meeting-b.txt` 驗證更新、取消與未知；`meeting-c.txt` 用於 capstone 新增前置任務欄位。

`prompt-budget.txt`、`prompt-kpi.txt`、`prompt-meeting.txt` 是基礎生成指令；`prompt-solo-meeting.txt` 是 AI 交辦 capstone 的欄位變更指令。`requirements-template.txt` 用來寫工作需求；`acceptance-template.csv` 有正常、變更、例外、修復、備份重開與 capstone 待測列。

## 驗收表怎麼填

每個測試保留一列，不要把新資料的結果覆寫在舊列。**先填**工具檔名／版本、測試情境、輸入條件、來源模式與預期答案；**做完再填**觀察、狀態、修復指令及修復後結果。來源模式填「學員生成」或「參考品」；使用參考品時，不可記成學員生成通過。沒有執行就保留「待測」。

作者格式示例（只說明填法，不是學員實測）：`department-kpi.html v1｜處理時間 5→2 天｜學員生成｜預期：lower、目標3、實際2為已達標，較上期4天縮短50%｜觀察：作者範例，待本人操作｜待測`。這一例展示工具版本、資料變更、預期和觀察如何分開；請依自己的實際檔名與結果記錄。

## 檔案交接

工作資料夾內分成「工具」「資料」「指令」「報告」「驗收」「歷史版本」。工具資料夾只放各項最後通過驗收的版本，並照實記錄檔名，例如 `meeting-timer-v2.html`；未通過的 v1 放「歷史版本」。KPI 在第6站下載的 `department-kpi-backup.json` 放「資料」，第9站用它還原原始 120 件、5 天、1% 狀態。JSON 用於可驗證地備份／還原工具資料；CSV 與 PDF 用於閱讀及交付報表。

AI Studio Build 的專案網址可加入瀏覽器書籤。關閉後以書籤回到相同專案、確認標題與預覽，再執行 A，才算完成重開測試；登入、權限或額度受阻時，記錄狀態並標待完成。

參考工具位於 `../tools/`。它們是完成品與故障備援，不是學員生成成果；AI 交辦參考頁只顯示人工核對的固定答案，沒有呼叫模型。
