# n8n Lite Pack · 弄一下工作室《AI 資料工廠》

**30 分鐘下載即用版**：8 個預製 n8n 工作流 + 一鍵安裝腳本。設好 Gemini API key 與 Telegram bot token 即可使用，**完全不需要 Google OAuth、不需要自有網域、不需要綁信用卡**。

> 想學「為什麼這樣設」、「如何改成你的場景」？看 `docs/` 資料夾裡每個工作流的原理說明。沒心學原理的學員直接跑 setup-wizard 即可。

---

## 前置需求（請先完成）

1. **n8n 已安裝並啟動**：依課程 1.1 雙擊 `n8n-starter-kit/start.command`，看到「✅ n8n 已啟動」
2. **cloudflared 已安裝**：依課程 1.2 跑 `brew install cloudflared`（Mac）或下載 .exe（Win）
3. **Gemini API key**：到 [aistudio.google.com/apikey](https://aistudio.google.com/apikey) 拿一組，貼到剪貼簿備用
4. **Telegram bot token + Chat ID**：跟 [@BotFather](https://t.me/botfather) 申請新 bot 拿 token；對你自己的 Telegram 發任意訊息給 bot 後，到 `https://api.telegram.org/bot<你的token>/getUpdates` 找到 `chat.id`（一串數字）

---

## 30 分鐘安裝流程

### 步驟 1：解壓 zip 到 `~/n8n-lite-pack/`

從課程網頁下載 `n8n-lite-pack.zip`，雙擊解壓。建議放在家目錄或桌面。

### 步驟 2：雙擊 `setup-wizard.command`（Mac）/ `setup-wizard.bat`（Win）

第一次雙擊會被 macOS Gatekeeper 擋——開「系統設定 → 隱私權與安全性 → 安全性」按「強制打開」。

### 步驟 3：跟著對話框填 4 個值

setup-wizard 會跳出 4 個 GUI 對話框依序問你：

1. **Gemini API key**（必填）
2. **Telegram bot token**（必填）
3. **Telegram Chat ID**（必填，數字）
4. **ntfy.sh topic 名稱**（選填，預設用 `n8n-lite-{你的電腦名}`）

### 步驟 4：等 setup-wizard 跑完

腳本會自動：

1. 驗證 n8n 跑著（curl healthz）
2. 驗證 cloudflared 已裝
3. POST 到 n8n REST API 建 3 個 credentials（Gemini / Telegram / Generic webhook）
4. 自動匯入 8 個 workflows
5. 跑 smoke test（觸發每個 workflow 一次）
6. 報告結果：哪些 ✓ 哪些 ✗

預期 30 分鐘內完成。

### 步驟 5：打開 n8n（[localhost:5678](http://localhost:5678)）確認

左側 Workflows 應該看到 8 個 workflow 全部已匯入並自動關聯 credentials。任一 workflow 點開可立即執行。

---

## 8 個預製 Workflow 清單

| # | 名稱 | 觸發方式 | 你能拿來做什麼 |
|---|------|---------|---------------|
| 1 | Webhook hello-world | Webhook 觸發 | 任何外部服務（Make / IFTTT / 表單）打進來會收到回應，最基本驗證流程 |
| 2 | PDF AI 改名 | Watch Folder 觸發 | 把 PDF 丟進 `~/n8n-lite-pack/sample-data/pdf-inbox/`，AI 讀內容自動改檔名（合約年度月份、發票編號） |
| 3 | 批次處理錯誤恢復 | Watch Folder 觸發 | 同 #2 但加 retry / try-catch / 處理報表，跑 100 份 PDF 失敗 5 份也能交差 |
| 4 | 定時 AI 日報 | Schedule（每天早上 8:00） | 自動讀 `~/n8n-lite-pack/sample-data/daily-input/` 所有檔案，AI 摘要寫成 Markdown 日報存到 `daily-output/` |
| 5 | Telegram 通知測試 | 手動觸發 | 按執行 → Telegram 收到訊息，驗證 Telegram bot 接通 |
| 6 | Webhook → Gemini → 本機檔 | Webhook 觸發 | 外部丟一個問題進來 → AI 生成回答 → 存本機檔 + Telegram 通知 |
| 7 | Quick Tunnel 接 webhook | Tunnel 公開 URL | 用 `tunnel-quick.command` 暴露 #6，讓手機 / Make / IFTTT 都能觸發 |
| 8 | Reference / Optional Chaining 練習 | 手動觸發 | 給你練 n8n expression 語法的範例工作流（學原理用） |

**結業 deliverable**：學員拿走這 8 個 workflow + Lite Pack 的整個 starter kit，可在自家電腦跑、可改造成自己場景。

---

## 想學「為什麼這樣設」、「怎麼改成你的場景」？

看 `docs/` 資料夾：

- `01-webhook-hello-world.md` — 為什麼用 Webhook 不用 Schedule？
- `02-pdf-ai-rename.md` — Watch Folder + Gemini API 整合的關鍵節點
- `03-batch-error-recovery.md` — 為什麼要做錯誤恢復 + 處理報表
- ...（每個 workflow 一份原理說明）

**Builder Track 結業作品**（選修）：把任一 workflow 改造成自己場景的「第 9 個 workflow」，匯出 JSON + 寫 100 字說明。想拿課程證照走這條，沒心的拿 8 個跑通就走人。

---

## 卡關了怎麼辦

setup-wizard 跑出對話框告訴你：

- **「找不到 n8n」** → 回課程 1.1 雙擊 `start.command`
- **「找不到 cloudflared」** → 回課程 1.2 安裝
- **「Gemini API key 格式錯誤」** → 確認你貼的是 `AIza...` 開頭那串
- **「Telegram bot token 無效」** → 確認你貼的是 `123456:ABC-DEF...` 格式
- **「無法連 n8n REST API」** → 確認 n8n 的 .env 沒設 `N8N_BASIC_AUTH_ACTIVE=true`

如果跑完 setup-wizard 任一 workflow 是 ✗，看對應 `docs/{workflow}.md` 的「常見錯誤」段落。仍卡住請聯絡講師並貼 setup-wizard 的最後 50 行 log。

---

## 想要 Gmail / Google Docs / Drive 整合？

那是**Google Pack**（不在本 Lite Pack）—— 需要綁信用卡 + 自建 OAuth App + 60-90 分鐘 guided setup。看課程 m4-google-pack 章節（如已開放）。

Lite Pack 故意不含 Gmail / Docs / Drive，避開 Google OAuth 卡關。8 個工作流純用 Gemini + 本機檔 + Telegram + webhook，**95% 學員 30 分鐘內可完成安裝**。

---

## 維護資訊

- **建置日期**：2026-05-02
- **n8n 測試版本**：2.17.8
- **Gemini 模型**：gemini-2.5-flash
- **設計依據**：`courses/n8n/_reviews/n8n-classroom-pack-design-2026-05-02.md`
- **每季回檢**：依「外部 SaaS 政策變動誠實揭露規則」（見 `_規範/飛輪規則.md`）
