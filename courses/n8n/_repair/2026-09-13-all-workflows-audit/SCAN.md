# 2026-09-13｜Lite Pack 14 流程一次性審查：掃描範圍

## 目的

回答「為什麼 #07 到現在才被發現」並一次盤點 01–14，而非只修單一頁面。

本次審查先凍結觀察結果，不在報告內偷偷修改其他流程。每一個結論都標示證據層級：

- **JSON**：`n8n/assets/n8n-lite-pack.zip` 內的 14 份 workflow 是否能解析、節點與連線是否形成預期結構。
- **文件**：對應 HTML、總覽頁與 Lite Pack README 是否描述同一個方法、路徑、回應模式、節點數與版本。
- **平台**：是否有使用者在目前 n8n 2.37.7／Starter Kit 重新匯入後實際按下 Execute／Publish 並取得輸出。沒有證據就記為 `NOT_RUN`，不以 JSON 綠勾或 HTML lint 代替。

## 已執行的檢查

1. 解壓讀取 Lite Pack 14 份 JSON；全部可解析。
2. 逐一列出觸發器、Webhook method/path/responseMode、分支 fan-out 與 Gemini model。
3. 檢查 Webhook + fan-out + `lastNode` 的回應競速風險。
4. 對照 14 個 workflow 頁的 hero／流程段落／測試文字／頁尾版本。
5. 對照 `m0-workflow-tour.html` 的數量、方法、模型與節點數。
6. 檢查 Lite Pack 與 Starter Kit 的資產分工：workflow／setup wizard／tunnel script 是否存在於正確試跑包。
7. 逐檔比對 Starter Kit 原始資料夾與可下載 ZIP，確認學員實際取得的內容沒有漂移。
8. 讀取所有 Code node 的 JavaScript；以目前 n8n Code node 執行語境包裝後通過 `node --check`。
9. 目前課程頁 lint：79 頁、BLOCKER 0、ERROR 0。這只證明 HTML 結構，不能證明 Blueprint 的執行行為。
10. 讀取本機 Docker／n8n：healthz、實際映像版本、資料庫匯入數與 execution status；結果與檔案靜態檢查分開記錄。

## 限制

- 沒有在本輪重裝 Docker、重新匯入 14 份 workflow 或逐一於目前 n8n UI 執行；平台證據沿用使用者已提供的截圖／輸出，並明確標註範圍。
- Windows 尚未進行實機逐流程驗證；只能確認 `.bat`／`.ps1` 與文件資產存在，不能宣稱 Windows 已通過。
- 目前 Downloads 中實際執行的 Starter Kit 為 n8n 2.17.8；倉庫原始模板已更新至 2.37.7，但下載 ZIP 尚未同步，兩者需先重新封裝再做平台驗證。
- 本機資料庫雖有 14 個匯入 workflow 與 9 筆 success execution，但全部是舊版 2.17.8 環境；不能直接代表新包已驗收。
- 預期的 `course-content-substance.md` 治理檔目前不存在，因此本報告補上內容契約與文件對齊檢查，不能假設該檔已替我們完成審查。
