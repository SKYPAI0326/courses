# 2026-09-13｜n8n Lite Pack 01–14 全流程審查報告

> **檔案狀態**：本檔保留修正前的盤點快照，記錄問題如何被發現；本輪修正後的現況與驗證結果請看同目錄的 [REPAIR-REPORT.md](REPAIR-REPORT.md)。

## 結論先行

目前 14 份 Blueprint 都能解析，Code node 靜態語法也通過；這只能證明「檔案可讀」。課程仍有文件契約漂移，且 #07 的同類風險在先前的檢查機制中沒有被攔截。

### 為什麼現在才發現 #07

1. **先前的人工範圍是 #06**：使用者當時正在逐步驗證 Webhook → Gemini，#07 尚未按目前版本重跑；因此沒有產生 #07 的平台證據。
2. **HTML lint 的檢查邊界太窄**：lint 能抓標籤、連結與基本結構，抓不到 Blueprint 的 `responseMode`、fan-out 後誰回 HTTP、Telegram 回應是否搶走 webhook response，也不會拿頁面文字和 ZIP JSON 比對。
3. **缺少跨資產 contract gate**：過去沒有一個一次掃描 14 個 JSON、14 個講義頁、總覽頁、README 與兩個試跑包的檢查器，方法、模型、節點數與依賴說法可以各自更新而不報錯。
4. **#07 與 #06 是同一類問題**：#06 的人工 curl 暴露了 fan-out + webhook 回應競速，才促使我們檢查下一個同樣含 fan-out 的 webhook。這是流程治理缺口，不是學員操作失誤。
5. **可下載 Starter Kit 與原始模板已分叉**：`n8n/assets/n8n-starter-kit/` 原始資料夾已寫 n8n 2.37.7，但可下載的 `n8n-starter-kit.zip` 仍是 2.17.8；使用者 Downloads 中目前執行的容器也確認為 2.17.8。學員直接下載後，拿到的版本與目前教材基線不同。
6. **使用者 Downloads 的 Lite Pack 也落後一個關鍵修正**：14 份 workflow 中只有 #07 與倉庫目前 ZIP 不同，Downloads 版本仍為 `responseMode:lastNode`；目前 n8n 資料庫匯入的 #07 也確認是 `lastNode`。因此先前看到的 #07 問題確實仍存在於學員現有試跑環境。

## 14 流程矩陣

狀態定義：`PASS`＝該層證據通過；`MAJOR`＝會使學員依文件做出錯誤設定或無法判讀結果；`MINOR`＝不阻止執行，但需在發布前清理；`NOT_RUN`＝沒有目前版本的平台實跑證據。

| # | JSON（節點／觸發） | 執行結構 | 文件對齊 | 目前平台證據 | 主要發現 |
|---|---|---|---|---|---|
| 01 | 2／Webhook GET `lite-hello` | `lastNode`，無 fan-out，風險低 | **MINOR** | 使用者截圖曾見兩節點綠框；需以目前包留證 | 對應頁寫 `lastNode` 與 JSON 一致；總覽仍寫外部 POST，會讓初學者用錯 method。 |
| 02 | 5／Manual | 線性，Gemini 3.6 Flash | **MAJOR** | 使用者曾以 3 份 PDF 看到輸出；需重跑目前包 | 頁面／總覽仍有 Gemini 2.5 與 v0.9／2026-05 文字；目前 helper 已是 3.6。 |
| 03 | 7／Manual | Extract error branch + success/fail 雙路 | **MINOR** | 使用者截圖曾見流程綠框；批次內容仍需留證 | 結構與頁面 7 節點一致；頁尾版本過期。 |
| 04 | 8／Schedule 08:00 | PDF／純文字分流後 Aggregate，無 Webhook response | **MINOR** | 曾執行並產生日報；來源正確性需逐檔核對 | 頁面已寫 8 個功能節點；總覽寫 6；頁尾已更新。 |
| 05 | 3／Manual | 線性 Telegram | **MINOR** | setup wizard／使用者曾收到 Telegram smoke test | 頁尾仍是 v0.9／2026-05；選配 credential 狀態需在頁面保持清楚。 |
| 06 | 8／POST `ai-ask` + GET `ai-ui` | 兩條 responseNode 路徑；主路 Code fan-out 3 | **PASS（目前修正版）** | 使用者已 curl、看到 JSON／檔案／Telegram／`aiError:null` | 主路已改指定 Respond to Webhook；目前未將修正版重新發布到遠端包外驗證。 |
| 07 | 4／GET `external-ping` | Code fan-out Telegram + Respond；已改 responseNode | **PASS（目前修正版）** | `NOT_RUN`（修正版尚未人工重跑） | 舊版是 `lastNode` + fan-out，且文件寫 POST／3 秒／24 小時；目前工作樹修正版已清掉這些落差。 |
| 08 | 4／Manual | 線性 Expression 練習 | **MINOR** | `NOT_RUN` | 課程頁與 JSON 核心一致；總覽仍寫 8 workflows／頁尾過期。 |
| 09 | 7／Gmail polling | Switch 4 路，無 Webhook response | **MINOR** | `NOT_RUN`（需 OAuth） | 頁面寫 8 節點，實際為 7 executable + 1 sticky；應明示計數口徑。 |
| 10 | 11／Manual | Switch + Code fan-out 2，無 Webhook response | **MAJOR** | `NOT_RUN` | 頁面寫 9 節點，實際 11 executable + 1 sticky；頁尾過期。 |
| 11 | 8／Manual | Code fan-out 3，無 Webhook response | **MINOR** | `NOT_RUN` | 頁面 8 節點與 JSON 一致；頁尾過期。 |
| 12 | 14／Manual + POST `kb-ask` + GET `kb-ui` | Part A 分流；`kb-ask` 為線性 `lastNode` → Set | **MAJOR** | `NOT_RUN` | 頁面寫 10 節點且把結尾稱 Respond；實際是 14 executable + 1 sticky，`kb-ask` 的回應節點是 Set。需先釐清教學口徑再實跑。 |
| 13 | 8／Schedule 09:00 | Schedule 雙路 + Code fan-out 2 | **MINOR** | `NOT_RUN` | 頁面寫 9 節點，等於 8 executable + 1 sticky；應標示「含說明卡」。頁尾過期。 |
| 14 | 7／Schedule 15m | Switch 異常路徑，無 Webhook response | **MINOR** | `NOT_RUN` | 頁面寫 8 節點，等於 7 executable + 1 sticky；應標示計數口徑。頁尾過期。 |

## 本機平台重複檢核（2026-09-13）

- `http://localhost:5678/healthz` 回應 `{"status":"ok"}`。
- Docker 容器正在運作，但實際映像是 **n8nio/n8n:2.17.8**；這與原始模板／教材目前標示的 2.37.7 不一致。
- n8n 資料庫中確認已匯入 **14 個 workflow**，名稱為 Lite Pack #01–#14，全部目前為 inactive。
- 執行紀錄共 **9 筆，全部 success**：#01（2 次）、#02、#03、#04、#05、#06（3 次）。#07–#14 目前沒有執行紀錄。
- Downloads 的 Lite Pack 有 14 份 JSON，但 #07 是舊版 `lastNode`；倉庫目前修正版 ZIP 已改為 `responseNode`，尚未同步到這台 n8n。
- 因這 9 筆是以舊版 2.17.8／舊下載 ZIP 產生，只能證明「舊模板在舊版本曾跑通」；不能直接當成 2.37.7 目標包的驗收證據。

## 高優先問題（目前應先處理）

### A. 總覽頁是跨流程的入口錯誤

`n8n/lessons/m0-workflow-tour.html` 仍寫「8 個 workflow」，但 Lite Pack 已有 14 個；#01／#07 仍寫 POST，#02 仍寫 Gemini 2.5；#04／#10／#12 的節點數也過期。這些文字位於學員進入各頁前的位置，優先級高於頁尾美化。

### B. #07 修正版必須重新同步並取得平台證據

目前工作樹已完成：GET、`responseNode`、固定 JSON response、Mac／Windows Quick Tunnel 步驟與清理說明；ZIP parse、頁面 lint、Code syntax 均通過。但使用者 Downloads 與資料庫仍是舊 #07，尚未同步新 ZIP，也尚未在目標 n8n 2.37.7 實際啟動 tunnel、Publish、呼叫 production URL，因此只能標示 `STATIC_PASS / PLATFORM_NOT_RUN`。

### C. #12 是下一個需要人工優先驗證的 webhook

它目前沒有 #06／#07 那種 fan-out 回應競速，因為 `kb-ask` 路徑是線性的；仍有文件把 Set 稱為 Respond、節點數不一致、索引素材與問答輸入前置條件需要核對等問題。應在人工驗證 #08–#12 前先修正文案契約。

### D. README 的 #07 依賴說法不準

Lite Pack README 的表格／FAQ寫「workflow 07 需先啟動 workflow 06」。目前 #07 JSON 自己接收 `external-ping`、通知 Telegram、回 Respond；它需要 Starter Kit 的 `tunnel-quick` 與（若啟用通知）Telegram credential，沒有資料流依賴 #06。這會讓學員多做一步，應改成「先啟動 Starter Kit，再啟動 #07 並發布」。

### E. 下載包不是目前原始模板

一次性比對原始 Starter Kit 與下載 ZIP，11 個檔案中有 6 個內容不同：`.env.example`、`README.md`、`n8n-compose.yml`、`start.bat`、`start.command`、`tunnel-quick.command`。其中最關鍵的是 `n8n-compose.yml` 的映像版本（ZIP：2.17.8；原始資料夾：2.37.7）與啟動／環境變數設定。這是目前「給學員直接套用」的 **BLOCKER**；在重新封裝並重新下載前，不能宣稱模板已與教材基線一致。

## 目前可以宣稱的範圍

- **可匯入檔案**：14／14 JSON 可解析；沒有發現 Gemini 2.5 仍存在於目前 ZIP workflow 內。
- **靜態程式**：18 個 Code node 以 n8n Code 語境檢查通過。
- **下載包一致性**：Lite Pack ZIP 自洽，但 Starter Kit 下載 ZIP 與原始模板有 6 檔漂移；目前使用者容器為 n8n 2.17.8，與教材標示 2.37.7 不一致。
- **學員現有解壓資料**：Lite Pack 只有 #07 落後目前修正版；資料庫也已匯入舊 #07，需重新下載／匯入或明確提供更新步驟。
- **已人工看到結果**：#01、#02、#03、#04（曾產生日報，內容正確性仍需逐檔來源核對）、#05、#06；其中 #06 是目前修正版證據。
- **尚未取得目前版本平台證據**：#07 修正版、#08、#09、#10、#11、#12、#13、#14；Windows 全部流程也尚未完成實機矩陣。
- **目前本機執行環境**：2.17.8 舊包；即使 #01–#06 有 success，也要在重新封裝的 2.37.7 包上重跑代表流程。

## 不應再使用的完成宣告

- 「HTML lint 全綠，所以 14 個流程可用」
- 「JSON 能匯入，所以 webhook 回應正確」
- 「有綠色外框，所以 AI 真的讀到來源檔」
- 「Mac 測過，所以 Windows 同步通過」
