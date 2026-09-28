# Scan — Lite Pack #06/#12 本機介面修補

## 問題與目標

學員從 n8n workflow 的本機 UI 開啟 #06 或 #12 時，被導向課程網站的講義密碼 Gate。目標是提供獨立修補包，更新已安裝實例中的兩個 UI Code node，不要求重新安裝 Lite Pack，也不重建 n8n/Postgres volume。

## 範圍與現況

- 只會觸及 `lite-pack-06-webhook-gemini-file` 與 `lite-pack-12-knowledge-rag` 兩個 workflow。
- 目前 `n8n/assets/n8n-lite-pack.zip` 已包含修正後的兩個 workflow；本修補包以其中版本為來源。
- #06 UI Code node：`code-html-ui-06` / `Code: 組 HTML (ai-ui)`。
- #12 UI Code node：`code-html-ui` / `Code: 組 HTML (kb-ui)`。
- 既有安裝以 Docker Compose 啟動 n8n 2.37.7 + Postgres；n8n workflow/credential DB 位於 named volume，`./shared` 掛載為 `/files/shared`。
- Mac 與 Windows 安裝頁皆在 `section#phaseB.lesson-section`、B1 提供 Lite Pack 下載。新下載連結放在該段落，清楚區分首次安裝與既有安裝修補。
- 兩個安裝頁目前在 HEAD 是乾淨狀態；全 repo 有其他使用者變更，全部保持不動。

## 安全限制

- 不可執行 setup-wizard、`docker compose down -v` 或覆寫整套 Lite Pack。
- 匯出 #06/#12 作為備份；合併器只替換目標 UI Code node 的 `parameters.jsCode`，保留其餘 node、connections、credentials references、workflow IDs、settings、active 狀態與自訂內容。
- 若 workflow ID、node ID/name/type、n8n 版本或匯出格式不符，修補必須在寫入前中止。
- 只短暫停止 `n8n` 服務以套用資料庫匯入；Postgres 與 named volumes 不移除。失敗時從同次備份回復，再啟動 n8n。
- 不把 workflow JSON 匯入真實使用者 Docker 實例作驗證；以 fixture、合約檢查及乾淨暫存測試驗證修補工具。

## 驗收證據

- Node 測試證明只替換兩個指定 UI Code node，且保留 workflow 其餘欄位；非法 ID/node/版本會 fail closed。
- Mac shell 語法、ZIP 完整性與成員清單可在本機驗證；本機沒有 PowerShell 執行環境，因此 Windows 腳本僅做靜態檢閱，尚未實際解析或執行。
- 兩個安裝頁的 HTML 結構、顯示文案與相對下載連結通過檢查。
- 實際跨平台 Docker 執行尚未在本環境做學員端驗證；文件需明示執行前確認 starter-kit 目錄與執行結果。
