# n8n Lite Pack · 弄一下工作室《AI 資料工廠》

Lite Pack 是課程用的本機練習包。它把 14 個可匯入的 workflow、安裝腳本與測試資料放在同一個資料夾，讓你先完成一條可驗證的路徑，再逐步修改成自己的工作流。

## 開始前先確認

1. Docker Desktop 已啟動。
2. 課程的 Starter Kit 已啟動，瀏覽器可開 `http://localhost:5678`，並已完成 n8n Owner Account。
3. **Gemini API key 是必要條件**：到 [Google AI Studio](https://aistudio.google.com/apikey) 建立金鑰。新帳號常見 `AQ.` 開頭的 authorization key，舊的 standard key 可能是 `AIza...`；精靈接受完整非空白內容，最後以 Gemini smoke test 驗證是否可用。
4. Telegram bot token 與 chat ID 是選配，只在要測試 Telegram 通知時準備。
5. `cloudflared` 只供 workflow 07 的公開 webhook 示範使用；本機 workflow 不需要它。

## 安裝流程

### 1. 下載與解壓

從課程頁下載 `n8n-lite-pack.zip`。

- macOS：建議解壓到 `~/Downloads/n8n-lite-pack/`
- Windows：建議解壓到 `%USERPROFILE%\\Downloads\\n8n-lite-pack\\`

最後要直接看到 `setup-wizard.command`、`setup-wizard.bat` 與 `workflows/`。若多出一層同名資料夾，請把內層資料夾移到 Downloads 後再執行。

### 2. 啟動精靈

- macOS：雙擊 `setup-wizard.command`。若 Gatekeeper 顯示無法打開，依課程頁的「隱私權與安全性 → 安全性 → 強制打開」處理；沒有被擋時直接繼續。
- Windows：雙擊 `setup-wizard.bat`。若 SmartScreen 出現警告，選「更多資訊 → 仍要執行」。

精靈會先檢查 n8n，再要求 Gemini API key，接著詢問是否啟用 Telegram。選擇 Telegram 時才填 bot token 與 chat ID；略過時走 Gemini-only 路徑。

精靈會建立必要的環境設定、Starter Kit 的 `shared/` 與 24 個子資料夾、1 個 Gemini credential（啟用 Telegram 時再加 1 個 Telegram credential），並匯入 14 個 workflow。Gemini smoke test 必須成功；Telegram smoke test 只在啟用 Telegram 時執行。略過 Telegram 時，含 Telegram 節點的 8 個案例（05／06／07／09／10／11／13／14）會保留在清單中，但要等你在 n8n 補上 Telegram credential 才能執行。

### 3. 完成判準

在 `http://localhost:5678` 的 Workflows 清單看到 01～14 共 14 個項目。Credentials 會依分支顯示 1 個（Gemini-only）或 2 個（Gemini + Telegram）。精靈最後應顯示 Gemini `OK`；略過 Telegram 時會標示 `Telegram skipped`。

## 14 個 Workflow

| 編號 | 名稱 | 觸發方式 | 練習重點 |
|---|---|---|---|
| 01 | Webhook hello-world | Webhook | 用最小流程確認 webhook 收得到資料並回應 |
| 02 | PDF AI 改名 | 手動／資料夾素材 | 讀取 PDF，請 Gemini 產生檔名，再寫回本機 |
| 03 | 批次處理錯誤恢復 | 手動／批次資料 | 逐檔處理、記錄成功與失敗、保留重試線索 |
| 04 | 定時 AI 日報 | Schedule | 讀取 daily-input，產生 Markdown 日報到 daily-output |
| 05 | Telegram 通知測試 | 手動 | 確認選配的 Telegram credential 與訊息傳送 |
| 06 | Webhook → Gemini → 本機檔 | Webhook | 將外部問題交給 Gemini，保存回答並可通知 Telegram |
| 07 | Quick Tunnel 接 webhook | cloudflared URL | 以短期公開 URL 示範外部觸發；先啟動 Starter Kit，再啟用並發布 #07 |
| 08 | Expression practice | 手動 | 練習 n8n expression、參照與 optional chaining |
| 09 | Gmail 分類 | 手動／Gmail | 以 Gmail 資料示範分類邏輯；需自行設定 Google credential |
| 10 | 客戶資料夾整理 | 手動／資料夾素材 | 依規則搬移與整理客戶檔案 |
| 11 | CSV 清洗評分 | 手動／CSV | 清理欄位、計算分數、輸出結果 |
| 12 | Knowledge RAG | 手動／知識文件 | 將文件整理成可供檢索的資料結構 |
| 13 | 每日營運快照 | Schedule | 彙整每日輸入，產生營運快照 |
| 14 | API 監控 | Schedule／HTTP | 呼叫 API、檢查狀態並留下監控結果 |

Google、Gmail 或其他外部服務的 workflow 會依帳號權限與 credential 狀態判定；課堂先以可匯入與可讀懂為目標，再由講師帶著完成所需連線。

## 路徑與資料安全

主機資料夾位於 Starter Kit 的 `shared/`。在 n8n 節點中一律使用容器路徑 `/files/shared/...`，不要直接填 macOS 或 Windows 的主機路徑。API key 寫入 Starter Kit 的 `.env`，不放進 workflow JSON，也不要把金鑰提交到 Git 或分享給他人。

## 常見問題

- **找不到 n8n**：先啟動 Starter Kit，再重新執行精靈。
- **Gemini smoke test 失敗**：檢查 key 是否完整、網路是否可用，並確認 `.env` 使用最新金鑰後重啟 n8n。
- **Telegram 測試失敗**：確認 bot token、chat ID 與 bot 對話紀錄；也可以回到 Gemini-only 路徑先完成課程。
- **Workflow 數量不對**：確認解壓後的 `workflows/` 內有 01～14 共 14 個 JSON，再重新執行匯入。
- **workflow 07 無法觸發**：確認 Starter Kit 正在執行、#07 已按目前版本的 Publish（舊版可能顯示 Active），再依課程步驟執行 `tunnel-quick`；cloudflared 僅在這個示範需要。#07 自己接收 `external-ping`，不依賴 #06。

## 版本資訊

- Lite Pack wizard：v1.3.5
- Starter Kit：v1.1.0
- n8n Docker image：2.37.7（`n8nio/n8n:2.37.7`）
- Gemini smoke test／共用 helper：`gemini-3.6-flash` + `thinkingLevel: minimal`
- 文件校訂：2026-09-13
- Windows 實機流程：待課堂人工驗證
