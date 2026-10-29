# 開始使用：SQL Server 講師訓練交接包

## 這包資料的用途

目標是在約三個月內，讓學員準備教授 SQL Server 基礎 28 小時、管理與維護 35 小時，以及 Cloud Data／Modern Data Stack 簡介 7 小時；同時能完成課綱範圍內的實機操作與常見問題排查。

此資料夾包含訓練規劃、能力證據紀錄、兩份起步課、參考資料及 SQL labs。教材已備妥不等於學員已學會。交接時所有能力都仍待本人作答、操作與驗收。

## 把工作區交給另一台電腦上的 Codex

1. 將本資料夾或同名 ZIP 複製到 G14，解壓縮後在 Codex 中開啟 `sql-server-instructor-training` 資料夾。
2. 若 Codex 未自動讀取資料夾的 `AGENTS.md`，請把 `CODEX-HANDOFF.md` 全文貼到新對話。
3. 讓 Codex 先讀本檔、`MISSION.md`、`ROADMAP.md`、`EVIDENCE-LEDGER.md`、`NOTES.md` 及 `RESOURCES.md`，再依首堂 lesson 開始；不要要求它把既有檔案當成學習成果。
4. 先完成起點與環境盤點。安裝、管理員權限、付費雲端服務及任何資料重設都要先取得本人同意。

## 第一次對話要確認

請學員一次用簡短文字回答：

1. 你做過哪些 SQL、資料庫或系統管理工作？請列實際做過的操作；完全沒做過也直接寫零基礎。
2. 接下來每週能固定投入幾小時？哪些日子或時段可用？
3. 三個月訓練從哪一天開始？原訂目標日是 2027-01-02；開始日不同時須重新計算。
4. G14 的 Windows／Linux 版本、CPU 型號、RAM、可用磁碟空間及 SQL Server 安裝狀態目前知道多少？不知道的項目再由 Codex 帶著做唯讀檢查。
5. 三個月內能否安排一位真人接受 30–45 分鐘試教並提供回饋？

先依答案判斷時程。現行粗估為每週約 11–13 小時，含正式內容學習與額外練習。若每週只能投入明顯少於此數，或起點為零且操作環境無法及早建好，三個月達成「會教也能排查常見問題」就不應保證；調整時數、目標範圍或期限。

## G14 環境檢查原則

使用者只回報 G14 有 AMD CPU 與 NVIDIA 獨立顯卡；OS、CPU 型號、RAM、磁碟、SQL Server 版本／服務都尚未確認。GPU 對本課 SQL Server 實驗通常不是關鍵條件。優先確認 x64 作業系統、足夠記憶體與磁碟，以及可實際連線的 SQL Server 執行個體。

若是 Windows，可由 Codex 指導使用以下唯讀 PowerShell 查詢；若系統不同，Codex 應先確認 OS 再改用相符方式：

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
Get-CimInstance Win32_Processor | Select-Object Name, AddressWidth, NumberOfCores, NumberOfLogicalProcessors
Get-CimInstance Win32_ComputerSystem | Select-Object @{Name='RAM_GB';Expression={[math]::Round($_.TotalPhysicalMemory / 1GB, 1)}}
Get-Volume -DriveLetter C | Select-Object DriveLetter, FileSystem, @{Name='FreeGB';Expression={[math]::Round($_.SizeRemaining / 1GB, 1)}}
Get-Service -Name 'MSSQL*' -ErrorAction SilentlyContinue | Select-Object Name, Status
Get-Command sqlcmd -ErrorAction SilentlyContinue | Select-Object Name, Source
```

查詢不到服務或 `sqlcmd` 不足以證明系統完全沒有 SQL Server；還要確認其他安裝方式與實際連線。安裝任何版本前，Codex 應依目前官方需求文件核對 OS／CPU 支援，並先說明版本用途、授權和系統變更，再等本人同意。

## 起步學習路徑

1. 回答 `lessons/0001-sql-server-object-hierarchy.html` 的閉卷檢核，說明用戶端連線的物件層級。答案是學員本人證據，Codex 不代答。
2. 在確認可用的 SQL Server 實例後，才執行 `labs/00-instance-inventory.sql` 並保留原始結果；沒有可用實例時先處理環境，不把紙上推演算成實作。
3. 完成 `lessons/0002-keys-and-referential-integrity.html`，再由本人執行 `labs/01-inspect-adventureworks-keys.sql`。AdventureWorks 是官方教學範例資料，不代表實際客戶資料或生產事故。
4. 依 `ROADMAP.md` 推進；每週把真實完成證據與未解問題記入 `EVIDENCE-LEDGER.md`。

## 實際授課範圍界線

三個月目標限定在所列 70 小時課綱及其常見入門問題。管理與維護只有有限時數介紹權限、備份還原、SQL Agent、監控；它不涵蓋完整企業 DBA、HA／DR 深度或重大事故指揮。Cloud Data 7 小時以概念、產品定位及單一平台的入門路徑為主；雲端帳號／方案未確認前不建立資源、不產生費用。

## 文件索引

- `AGENTS.md`：交給另一個 Codex 的持續工作規則。
- `CODEX-HANDOFF.md`：可直接貼到新 Codex 對話的完整提示。
- `MISSION.md`：目標、限制與完成條件。
- `ROADMAP.md`：12 週初稿、時數拆分、風險與驗收閘門。
- `EVIDENCE-LEDGER.md`：目前各能力的真實驗證狀態。
- `NOTES.md`：學習偏好與實驗規則。
- `RESOURCES.md`：官方技術資料來源、環境差距與雲端範圍提醒。
- `lessons/`、`reference/`、`labs/`：兩堂短課、速查資料與 SQL 實驗腳本。
