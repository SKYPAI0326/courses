# Lite Pack 本機 UI 修補包 1.0.0

這個修補包用於已經安裝 Lite Pack 的學員：如果 #06「Webhook → Gemini → 本機檔」或 #12「本地知識庫問答」的本機操作頁錯誤地顯示課程網站密碼頁，可只更新這兩個頁面的程式碼，保留原本安裝與其他練習。

## 開始前

1. 確認 Docker Desktop 已開啟，原本的 `n8n-starter-kit` 正在執行，瀏覽器可開啟 <http://localhost:5678>。
2. 先儲存並關閉 n8n 中 #06、#12 的編輯畫面，避免修補期間同時編輯。
3. 將此 ZIP 解壓縮，然後把解出的 `n8n-lite-pack-ui-fix` 資料夾放在原本的 `n8n-starter-kit` 資料夾裡，與 `n8n-compose.yml` 同一層。不要放進 `shared`。

資料夾應如下：

```text
n8n-starter-kit/
├── n8n-compose.yml
├── shared/
└── n8n-lite-pack-ui-fix/
    ├── apply-fix.command
    ├── apply-fix.bat
    └── apply-fix.ps1
```

## 執行修補

- **Mac**：在 Finder 開啟 `n8n-lite-pack-ui-fix`，雙擊 `apply-fix.command`。若 macOS 阻擋，請開啟 Terminal，先輸入 `bash `（最後保留空格），再把 `apply-fix.command` 檔案拖進視窗並按 Enter。
- **Windows**：雙擊 `apply-fix.bat`，在 PowerShell 視窗按畫面提示完成。
- 工具會先確認 n8n 是課程版 2.37.7，再要求輸入 `YES` 才開始匯出備份與套用；輸入其他內容會取消。

執行期間 n8n 會短暫停止再啟動，通常約 1–2 分鐘。這段期間先不要使用本機 n8n 或呼叫它的 webhook；Postgres、Docker volumes 和 `shared` 檔案不會刪除。

## 修補做了什麼

- 只匯出並更新 workflow ID `lite-pack-06-webhook-gemini-file`、`lite-pack-12-knowledge-rag`。
- 只替換各 workflow 中本機 UI 的 Code node JavaScript；不匯入整套範例，也不更動其他節點、連線、憑證參照、名稱、設定或你的自訂欄位。
- 在 `n8n-starter-kit/shared/lite-pack-ui-fix-日期時間/backup/` 保留修補前兩份 workflow 備份。
- 修補失敗時會嘗試自動匯回備份並重新啟動 n8n。
- 若目前 n8n 版本不是課程 starter-kit 的 2.37.7、workflow/node 身分不符或匯出內容不完整，會在匯入前停止，不做猜測式修改。
- 若已發布 workflow 與目前草稿內容不同，會在停止 n8n 前中止；請先在 n8n 處理或發布原有草稿，再重新執行，避免修補時意外發布其他未完成修改。

## 完成後檢查

1. 看見「修補完成」後，開啟 #06 的本機 UI URL（`http://localhost:5678/webhook/ai-ui`）與 #12 的本機 UI URL（`http://localhost:5678/webhook/kb-ui`）。
2. 確認頁面顯示本機問答介面，而非課程網站密碼頁。
3. 在 n8n 分別打開 #06、#12，確認原有節點與憑證選擇仍在。#06 若尚未設定 Telegram 憑證，仍需照原課程步驟設定；此修補不會替你新增或修改憑證。
4. 若 workflow 原本未發布，腳本會保留未發布狀態；要使用 production URL 時，請回 n8n 依原課程步驟手動發布該 workflow。

修補包不會執行 `setup-wizard`、不會重裝 Lite Pack，也不會執行 `docker compose down -v`。若腳本中途被手動關閉，先回到原本的 `n8n-starter-kit` 執行 `start.command`（Mac）或 `start.bat`（Windows），不要刪除 `shared` 或 Docker volumes；保留畫面訊息與備份資料夾供排錯。
