# 2026-09-13｜n8n Lite Pack 01–14 修正報告

## 本輪完成

- 重新封裝 `assets/n8n-starter-kit.zip`，並以 `assets/n8n-starter-kit/` 原始資料夾逐檔比對；11 個檔案內容一致，四個 macOS `.command` 腳本保留可執行權限。
- 重新封裝 `assets/n8n-lite-pack.zip`，同步 14 個 workflow、安裝精靈與 README。#07 已固定為 GET `external-ping` + `responseNode`，不再依賴 #06。
- 更新工作流總覽：14 個 workflow、#01／#07 的 GET 方法、Gemini 3.6 Flash、可執行節點與說明卡的計數口徑均對齊目前 ZIP。
- 更新 #12 的三條鏈說明，明確標示 Part A 建索引、Part B `lastNode` 問答 API、Part C `responseNode` 問答 UI，以及索引檔案前置條件。
- 更新各 M0 工作流頁的版本、節點數與 Lite Pack 版本文字，避免以過期的 v0.9／2026-05 內容引導學員。
- 保留本輪修正前的完整備份與還原腳本：`_backup/2026-09-13-pre-all-workflows-fix/`、`_tools/restore-2026-09-13-pre-all-workflows-fix.sh`。

## 靜態驗證結果

| 檢查 | 結果 |
|---|---|
| Lite Pack JSON 解析 | 14／14 通過 |
| workflow contract | 14／14 的節點數、觸發方法與主要回應模式可讀且符合檢查器 |
| Code node 靜態語法 | 18 個通過 |
| 總覽頁過期宣稱 | 0 條 |
| Starter Kit 原始資料夾／ZIP | MATCH |
| n8n HTML lint | 79 頁，BLOCKER 0、ERROR 0（WARN 為既有維運提示） |
| Git diff 格式 | 通過 |

## 尚待明日人工驗證

- 目前 Downloads 內的 Lite Pack #07 仍是舊版 `lastNode`，檢查器會明確回報 1 個 local drift。明天重新下載並解壓最新 `n8n-lite-pack.zip` 後，先替換／重新匯入 #07，再執行 #07 的 Quick Tunnel 實測。
- 本輪沒有宣稱平台全數通過；#07–#14 仍須在新 Starter Kit（n8n 2.37.7）取得實際執行證據，Windows 也需依同一矩陣補測。
- 檢查器若在尚未重新下載前顯示 `FAIL`，原因只會是上述 Downloads #07 漂移，不代表倉庫內 ZIP 契約失敗。

## 明日建議順序

1. 重新下載兩個 ZIP，確認 Starter Kit 啟動後瀏覽器可開 `http://localhost:5678`。
2. 重新執行 Lite Pack 精靈，確認 Workflows 顯示 01–14；需要通知時再補 Telegram credential。
3. 先驗證 #07：Publish（舊版介面可能顯示 Active）→ 啟動 `tunnel-quick` → 呼叫 `/webhook/external-ping` → 核對 JSON、Telegram 與四個節點綠框。
4. 接續依審查報告的 A–D 批次補測 #12、#08、#10、#11、#09、#13、#14，逐項保留輸入、節點狀態與輸出證據。
