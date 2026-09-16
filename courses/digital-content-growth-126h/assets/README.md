# digital-content-growth-126h 本機資產包

> 來源：`../_lessons/digital-content-growth-126h/` 的 frontmatter、Verification Asset Spec、交付與驗收段落。  
> 範圍：本目錄只放可複製的文字模板、合成／去識別資料與環境說明；不含二進位檔，不修改教案、_plan、_gates 或 HTML。

## 狀態摘要

- **READY：** 40 份 unit 模板（HTML 閱讀版＋UTF-8 Markdown 下載版）；3 組可用於課堂的 UTF-8 合成 CSV；欄位字典、來源標記、操作 fallback 文件。
- **BLOCK：** LocalWP、GTM、GA4 Demo Account、Google／Meta／LINE 實際帳號與權限；所有外部平台／真實投放／真實客戶資料。此包只提供不需登入的模擬路徑。
- **判定原則：** READY 代表檔案可讀、可複製且不依賴外部登入；BLOCK 代表仍需教師在課前取得、驗證或授權，不能以 placeholder 當完成品。

## 資產索引

| 路徑 | 用途 | 使用時機 | 備援 | 狀態 |
|---|---|---|---|---|
| `templates/<unit-id>.html` | 對應 unit 的可讀模板頁，保留欄位、驗收、來源與恢復欄 | 各 lesson 的動手／交付階段 | 講義內開啟閱讀版；原講義保留在上一頁 | READY |
| `templates/<unit-id>.md` | 對應 unit 的可編輯原始模板，使用 UTF-8 BOM | 各 lesson 的動手／交付階段 | 下載單檔後用文字編輯器編輯；上游缺檔時用「模擬輸入」並標註 | READY |
| `datasets/gsc-search-console-synthetic.csv` | GSC 查詢、頁面、曝光、點擊與排名練習 | CH4-1、CH4-2、PRAC4 | 使用 lesson 內嵌示例；不可宣稱為真實網站資料 | READY |
| `datasets/ga4-content-synthetic.csv` | GA4 內容事件與轉換判讀練習 | CH4-4、CH4-5、CH4-7、PRAC4 | 使用欄位字典與 lesson 示例；無需登入 | READY |
| `datasets/ads-budget-two-rounds-synthetic.csv` | 預算情境、第一／二輪結果與單一變因決策 | CH5-6、CH5-7、PRAC5 | 使用紙筆計算；不執行真實付費投放 | READY |
| `datasets/README.md` | 欄位說明、來源標記、合成限制與使用單元 | 讀資料前 | 以 CSV 標頭與本檔重建欄位 | READY |
| `environment/README.md` | 環境矩陣、權限界線、fallback、課前驗證 | CH4-3～CH5-7、PRAC4～5 | 全部改走本機文字／CSV 模擬路徑 | READY（說明）；外部環境 BLOCK |
| `environment/permission-checklist.md` | 教師課前帳號／權限檢查表 | 課前 setup | 沒有權限時勾選 fallback，不得偽造 READY | READY（檢查表） |

## Unit 模板

每份模板依 lesson 的完成物名稱與目標建立，保留：情境／輸入、判斷或操作、具體輸出、證據與來源、限制、驗收、卡關修復、交接與版本欄。模板本身不代表該 unit 的完整參考完成品；若 lesson 規格要求案例卡、完整成品、外部帳號或實際軟體，仍列 BLOCK。

## 使用與備援規則

1. 從講義開啟對應的 HTML 閱讀版，先確認欄位用途；需要編輯時再下載同頁提供的 UTF-8 Markdown 原始模板。
2. 合成資料欄位一律保留 `source_status=synthetic`；不得改寫成客戶、正式網站或真實廣告成效。
3. 外部平台無法登入時，使用 CSV／文字模板完成「規格、判斷、驗收條件」；缺少真實畫面、事件傳送或平台權限的部分寫入「待正式環境確認」。
4. 任何 credential、授權、付費投放或真實個資都不放進本資產包。
5. 交付前逐檔檢查：檔名、可讀性、來源標記、狀態、備援、恢復路徑與下一個接手 unit。

## 建立紀錄

- 建立日期：2026-09-16
- 資料類型：合成／去識別示例
- 二進位檔：0
