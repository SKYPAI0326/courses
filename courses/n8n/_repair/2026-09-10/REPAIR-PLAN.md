# Repair Plan: n8n

## Scope

- slug：`n8n`
- 目標：讓沒有講師口頭補充的初學者，能沿著清楚路徑完成核心頁面並知道每一步的材料、結果與回復點。
- 本批會修改的頁面：
  - `lessons/index.html`
  - `lessons/m1-1-setup.html`
  - `lessons/m1-3-json.html`
  - `lessons/m4-1-remote.html`
  - `lessons/m3-1-watch.html`
  - `lessons/m3-2-rename.html`
  - `lessons/m4-2-hybrid.html`
  - `lessons/m0-install-mac.html`
  - `lessons/m0-install-win.html`
- `lessons/m0-workflow-01-webhook.html`
- `assets/m1-3-ai-output-text.txt`

## Risk

- 近期授課：未提供
- 備份：required，已建立同日備份與還原腳本
- 平台實跑：本批不宣稱已實跑；保留 `NOT_RUN`／`SIMULATED` 邊界

## BLOCKER（P0）

### [NAV_OPS] `lessons/index.html`

- 問題：Path B 將學員帶往模組摘要與 anchor，沒有列出核心實作頁的必修順序、起始材料、完成物與下一頁。
- 修法：建立 M0 → M1 → M2 → M3 → M4 的學習路徑區塊，將摘要頁定位為導覽，讓每個核心單元直接連到實作頁並標示延伸頁。
- 驗證：總覽頁可從入口點擊到每個核心頁；每段有完成物與下一步說明。

### [LEARNER_PATH] `lessons/m1-3-json.html`

- 問題：核心 Set／JSON Parse 操作可由講師代做，且缺固定輸入、起始 workflow、完整節點狀態與中途 Checkpoint。
- 修法：補固定 payload、固定 AI 文字、Set 的 `ai_text`、Code `JSON.parse()`、逐步可見結果、Step 3／4／7 Checkpoint、卡住時回復位置與 macOS／Windows 指令；依目前版本移除不存在的 JSON Parse 節點依賴。
- 驗證：遮住講師備註後，學員可依頁面建立 Webhook → Set → Code 並檢查輸出。

### [LEARNER_PATH] `lessons/m4-1-remote.html`

- 問題：同時要求 Google Forms、Make、Apps Script、Cloudflare Tunnel 與 n8n Webhook，缺少前置條件、固定測試資料與無外部服務替代路徑。
- 修法：首屏列出帳號／權限／環境檢核；提供固定 payload 與本機 fixture 路徑；每個服務階段加入完成物、Checkpoint 與停止狀態。
- 驗證：有連線與無連線兩條路徑都能說明輸入、結果、限制與下一步。

## MAJOR（P1）

- `lessons/m3-2-rename.html`：補 starter workflow、輸出資料夾與 API 選配界線。
- `lessons/m3-1-watch.html`：在放檔、binary 輸出與分流前加入 Checkpoint。
- `lessons/m4-2-hybrid.html`：回指 M4-1 完成證據，補兩個 Scenario 的起始檔與固定 payload。
- `lessons/m0-install-mac.html`、`lessons/m0-install-win.html`：拆出環境檢查、安裝、啟動、登入、hello-world Checkpoint。
- `lessons/m4-3-ai.html`：保留 15–20 分鐘可完成的基準主線，完整串接改為選做，不將核心交給講師 Live Demo。
- `lessons/m2-2-chaining.html`、`lessons/m2-3-logic.html`：補起始 workflow、fixture、第一個可見結果與下一步。
- `lessons/m4-2-hybrid.html`、`lessons/m4-3-ai.html`：補 `request_id`、本機 `status`、檔案恢復、Gmail `NOT_RUN` 與 API／固定資料雙模式驗收。

## MINOR（P2）

- `lessons/m0-workflow-01-webhook.html`：頁首與總覽卡片標記為「閱讀／設計參考」，避免誤認為必修實作。
- `lessons/index.html`：核心時數與選修時數改與 `_outlines/n8n.md` 一致，明列核心 8h、選修 1.7h、M0 另計。

## 整合結果

- Make `CH1-6.html` 與 n8n `m4-1-remote.html`／`m4-2-hybrid.html` 已共用 `BRIDGE-1-make-n8n-contract-v1.md`。
- BRIDGE-1 已列出 Make 完成物、n8n 接收欄位、轉換責任與成功／待人工／契約錯誤三條終態。
- n8n bridge fixture 已修正選填 `urgency_signal=null` 的驗證規則。

## Execution Order

1. 備份本批頁面與建立還原腳本。
2. P0：總覽路徑 → M1-3 JSON → M4-1 Remote。
3. 跑 lint、連結與資產存在檢查，記錄結果。
4. P1：M3-1、M3-2、M4-2、Mac／Windows 安裝、M4-3、M2 chaining／logic。
5. P2：標記 M0 參考頁、修正時數文字。
6. 做 n8n cold follow-along。
7. Make／n8n Bridge 的真人匯入、重綁連線與跨 OS 實跑列為後續驗證，不以靜態檢查代替。
