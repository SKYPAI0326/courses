# n8n 講義修正計畫（2026-09-13）

> 狀態：內容與資產同步修正完成；靜態驗證通過；Docker／Windows／外部服務保留人工驗證。

## Scope

- 課程：`n8n`
- 頁面：`lessons/m0-install-mac.html`、`lessons/m0-install-win.html`、`lessons/m1-1-launch.html`
- 資產：Starter Kit README、Lite Pack ZIP 內 README
- 本次不修改 workflow JSON、Docker Compose 或啟動腳本邏輯；Lite Pack wizard 僅同步 Step 9 的 workflow 數量顯示文字
- 本次不進行 Docker 實機驗證；修正後再由學員依正式流程人工驗證

## 歷史背景

過去曾依照舊版講義成功執行。當前資產已更新為 n8n `2.37.7`、Starter Kit `v1.1.0`、Lite Pack wizard `v1.3.2`，舊結果只作為歷史基線，不能直接視為目前版本通過。

## BLOCKER

### [ASSET_CONTRACT] Phase B 前置條件與 wizard 行為不一致

- 位置：`m0-install-mac.html:427-494`、`m0-install-win.html:439-506`
- 問題：頁面暗示 Gemini 與 Telegram 都可略過；實際 wizard 必須取得 Gemini key，Telegram 才是選配。
- 修法：改成 Gemini 必填、Telegram 選配；明列無 Gemini 時不可使用 wizard，另列手動匯入路徑為未實作選項。
- 驗證：頁面敘述、完成判準、wizard 分支與 credential 數量一致。

### [ASSET_CONTRACT] Lite Pack README 與 ZIP 實際內容過期

- 位置：`assets/n8n-lite-pack.zip` 內 `n8n-lite-pack/README.md`
- 問題：README 仍寫 8 workflow、3 credentials、ntfy、cloudflared 必裝、n8n `2.17.8`；目前 ZIP 是 14 workflow、1～2 credentials、Gemini 必填／Telegram 選配、n8n `2.37.7`。
- 修法：重寫 README 的前置條件、安裝分支、數量、版本、測試範圍與安全界線，使其與 wizard v1.3.2 及課程 M0 一致。
- 驗證：重新解壓 ZIP，比對 README 與腳本／workflow 數量。

### [LEARNER_PATH] B3/B4 完成條件不可能穩定重現

- 位置：Mac/Win B3、B4
- 問題：固定寫 3 個對話框、2 credentials、Telegram 成功訊息；選擇略過 Telegram 時均不成立。B4 標題又誤寫 8 workflow。
- 修法：改成兩條可觀察分支：Gemini-only（1 credential、Telegram skipped）與 Gemini+Telegram（2 credentials、Telegram smoke test passed）。Workflow 固定為 14 個。
- 驗證：兩種分支各有獨立完成判準。

## MAJOR

### [NAV_CONTRACT] 正式入口頁路徑與角色未統一

- 位置：`m0-install-mac.html`、`m0-install-win.html`、`m1-1-launch.html`
- 問題：M0 使用 Downloads 路徑，1.1.2 顯示家目錄路徑；1.1.2 另有命令列備援，未清楚標示其角色。
- 修法：M0 作為正式安裝入口；1.1.2 改為啟動與 Owner Account 示範，保留命令列為明確標示的備援。統一「可放在其他位置，但以下以 Downloads 為例」的寫法。

### [VERSION] 頁尾版本資訊過期

- 位置：Mac/Win M0 footer
- 問題：仍寫 n8n latest、Lite Pack v0.9、2026-05。
- 修法：同步目前版本與建置日期，並標示 Windows 尚需實機驗證。

### [RESET_SAFETY] Step 0 完成判準與輸出不一致

- 位置：`m0-install-mac.html:274-295`
- 問題：container 空結果不會顯示成功標記，卻要求 5 區塊全顯示 `✅`；刪除指令也需更清楚說明範圍。
- 修法：為 container 空結果加入明確成功輸出，並將刪除前確認與影響範圍寫入步驟。

### [PLATFORM] Gatekeeper 說法過於絕對

- 位置：Mac M0 A3、1.1.2 備援說明
- 問題：並非所有 macOS 環境都必然阻擋每個 `.command`。
- 修法：改為「若出現阻擋，依下列流程處理」；保留四個腳本的處理範圍。

### [EVIDENCE] Windows 與外部整合仍無目前實機證據

- 位置：Windows M0、Lite Pack smoke test
- 問題：目前只有歷史／Mac 基線，不能在內容修正後宣稱跨平台與外部服務已通過。
- 修法：頁面保留 `待實機驗證` 標籤；完成文字修正後再做人工驗證。

## MINOR

- M0 頁面 footer 缺少 `data-platform-version` metadata，補上目前版本。
- `m1-1-launch.html` Starter Kit 檔案數量由 9 改為目前實際檔案數。
- M0 頁面 `Step N` 標籤可在內容修正時改成「步驟 N」，避免與正式操作混用。

## Execution Order

1. 建立備份與還原腳本（已完成）
2. 修正 Mac/Win Phase B 分支與數量
3. 同步 Lite Pack ZIP 內 README
4. 統一 M0 與 1.1.2 入口說法、路徑與備援標示
5. 修正 Step 0 判準與頁尾版本 metadata
6. 重新解壓資產並做靜態內容核對
7. 跑 HTML lint 與連結檢查
8. 交由使用者依 M0 A3 開始人工驗證

## Rollback

```bash
bash courses/n8n/_tools/restore-2026-09-13-pre-repair.sh
```
