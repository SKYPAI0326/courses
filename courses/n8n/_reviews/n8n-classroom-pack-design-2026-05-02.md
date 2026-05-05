---
review_type: course-redesign-proposal
course_slug: n8n
proposal_date: 2026-05-02
trigger: 連續 8+ 學員壓測卡關後，使用者明示「學員訴求是落地（template marketplace），不是學原理」
codex_call_id: 3514dbca
codex_verdict: actionable（但教育設計駁斥被使用者反向駁回）
status: 待動手實作
---

# n8n classroom pack 三層設計提案

## 前情：為何要做這個

n8n 課程「AI 資料工廠」（8h，已上線）經 8+ 連發學員實測壓測後，funnel rate 估 < 30%——學員從 0 走到「跑通自己的 AI 工作流」過程中，卡在環境建置、credentials、ISP 擋協議、UI 不熟、Google OAuth 等門檻。

評估報告 § 8 已點出：3 個 GenAI deliverable 全部沒實測過、5 個 workflow JSON 仍待補。傳統「教學員從 0 自己建」的講義路徑對這群受眾（行銷企劃 / 營運 / 知識工作者，非工程師）門檻過高。

## 哲學定位（使用者明示）

> **「學員的訴求是面對現實，他們不見得想要學，有時只是想索取，所以能落地是第一優先，但我們同步提供步驟搭建的原理與說明，讓有心的同學可以學習，沒心的可以套用」**

這個哲學駁回了 Codex CALL_ID 3514dbca 的「教育上危險，不要淪為 template marketplace」論點。Codex 是自學工程師教育視角；本課程是商業培訓視角，學員真實訴求是結果而非原理。

設計優先序：

1. **能落地**（80% 學員 30 分鐘有成品可帶走）
2. **提供原理**（20% 學員可深入查、可改造、可擴充）
3. **不強制學原理**（沒心的拿模板走人也是合理的價值交付）

## 三層架構

### 層 1：Lite Pack（必出，30 分鐘必成）

**目標學員**：80% 想拿就走的學員、課堂時間有限的工作坊參與者。

**承諾**：下載 zip → 雙擊 setup-wizard → 填 2 個值（Gemini API key、Telegram bot token）→ 30 分鐘內 8 個工作流可用。

**避開**：Google OAuth 全部（Gmail / Docs / Drive / Form）— Codex 駁斥的真正卡點。

**包含 8 個工作流**（純 Gemini + 本機 + Telegram + webhook，不含 Google OAuth）：

| # | Workflow | Trigger | 處理 | 輸出 | 用到的 credential |
|---|---------|---------|------|------|------------------|
| 1 | Webhook hello-world | Webhook | Set | Respond | （無） |
| 2 | PDF AI 改名（核心 demo） | Watch Folder | Read PDF + HTTP Gemini + Code parse | Rename File | Gemini API |
| 3 | 批次處理錯誤恢復（M3-4 新單元） | Watch Folder | Loop + Gemini + try/catch | processed/failed folder + log | Gemini API |
| 4 | 定時 AI 日報 | Schedule | Read local files + Gemini | Write local Markdown | Gemini API |
| 5 | Telegram 通知測試 | Manual | Set | Telegram Send | Telegram bot |
| 6 | Webhook → Gemini → 本機檔 | Webhook | Gemini | Write File + Telegram 通知 | Gemini + Telegram |
| 7 | Quick Tunnel 接 webhook（含 cloudflared 整合） | Webhook（外部觸發）| Set | Respond | （無，但需 cloudflared 跑） |
| 8 | Reference / Optional Chaining 練習 | Manual | Code 範例 | Set | （無） |

**結構**：

```
n8n-lite-pack/
├── workflows/                  ← 8 個 .json
├── setup-wizard.command        ← Mac 一鍵
├── setup-wizard.bat            ← Win 一鍵
├── personalization.env         ← 學員填 chatId / topic
├── sample-data/                ← PDF / 文字 / CSV 範例素材
└── README.md                   ← 「先看這份」3 段：環境檢查 / 30 分鐘流程 / 卡關回報
```

**setup-wizard 行為**（純 GUI，不下指令）：

1. 偵測 n8n 是否跑著（curl `localhost:5678/healthz`）
2. 偵測 cloudflared 是否裝（`which cloudflared`）
3. GUI 對話框問 Gemini API key + Telegram bot token + Telegram chat ID
4. 自動 POST 到 n8n REST API 建 credentials（type 為 `httpHeaderAuth` / `telegramApi`）
5. 自動匯入 8 個 workflows + 自動關聯 credentials
6. 跑 smoke test（觸發每個 workflow 一次）
7. GUI 報告：8 個 workflow 哪些 ✓ 哪些 ✗（學員下次要查哪一個）

### 層 2：Google Pack（要出，60-90 分鐘 guided）

**目標學員**：真實工作場景含 Gmail / Docs / Drive 的學員、想做完整 AI 秘書 workflow 的學員。

**承諾**：明確標示「需要 Google OAuth + 約 60-90 分鐘 + 5% 機率卡 Workspace admin」，提供圖文 wizard，不承諾 100% 成功但提供卡關回報機制。

**包含 4 個工作流**：

| # | Workflow | 用到的 OAuth |
|---|---------|---------------|
| 9 | Gmail Send 通知 | Gmail OAuth |
| 10 | Google Docs Create + Update | Docs OAuth |
| 11 | Google Form → n8n（M4-1 完整版） | Form via Apps Script + Gmail |
| 12 | AI 秘書完整版（M4-4） | Gmail + Gemini + Docs + Telegram |

**setup-wizard-google 行為**：

1. 偵測 Lite Pack 已安裝
2. GUI 對話框引導：
   - 開瀏覽器到 console.cloud.google.com
   - 顯示 step-by-step 圖文指引（含截圖）
   - 每步驟有「我做完了」按鈕進下一步
   - 收 client_id + client_secret
3. 自動寫入 n8n credentials
4. 開 n8n credential 頁面讓學員按「Connect」完成 OAuth flow（這步無法繞過）
5. 跑 smoke test
6. 卡關報告：列出哪步失敗 + 對應 troubleshoot 連結

### 層 3：原理說明文件（給有心學員）

**位置**：每個工作流獨立 .md，可在 docs/ 資料夾或內嵌講義折疊段落。

**結構**（每個工作流一份）：

```markdown
# {workflow-name} 原理說明

## 為什麼這樣設計？
（業務情境 + 技術選擇理由）

## 節點 by 節點解釋
1. {Node 1}：做什麼，為什麼用這個 type，可替代方案
2. {Node 2}：...

## 怎麼改成你的場景？
- 換 trigger（從 Watch → Schedule / Webhook）
- 換資料源（PDF → Excel / CSV / Notion）
- 換 AI（Gemini → Claude / OpenAI / Ollama）
- 換輸出（本機 → Telegram / Gmail / Sheets）

## 常見錯誤 + 修法

## 進階：加錯誤恢復、加批次控速、加 schema 驗證
```

**Builder Track 評量**（選修）：學員必須把任一 Lite Pack 工作流改造成自己情境的「第 9 個 workflow」，匯出 JSON + 寫 100 字說明改了什麼為什麼改 = 結業作品。想拿證照走這條；沒心的拿 8+4 跑通就走人。

## 對課程結構的影響

### 講義路徑改寫

| 既有 | 新版 |
|------|------|
| m1.1 啟動 n8n | 不變（仍是環境建置） |
| m1.2 Tunnel | 不變（已重整為 Quick Tunnel 主流程） |
| m1.3 / m2 / m3 / m4 各單元主路徑 | **全部改寫為「成品演示」**：學員先看 setup-wizard 安裝完的成果，講義講「為什麼這個工作流要這樣設」 |
| 結業 deliverable | 從「跟著教做的工作流」改為「Lite Pack + Google Pack 的 12 個成品 + Builder Track 改造作品」 |

### 既有講義的活化

m3 / m4 各單元講義不丟掉，改成「**這個工作流在 Lite Pack 第 X 個，原理在這裡看**」 — 維持深度教學內容，但不再是學員的主動線。

## 與 Codex 第二意見的關係

Codex 第二意見的技術駁斥（CALL_ID 3514dbca）**全部接受**：
- ✅ Google OAuth 是真正卡點 → 隔離到 Google Pack，明確標示風險
- ✅ Shared OAuth App 合規風險 → 不採用，每個學員自建 client（或用 Google Pack 提供的 sandbox account）
- ✅ 維護成本集中 → 列入長期維護 budget（每季回檢 + workflow JSON 版本鎖定）

Codex 第二意見的教育設計駁斥（「淪為 template marketplace」）**部分採納**：
- ⚠️ 風險真實存在，但對本課程受眾不適用
- ⚠️ Builder Track 是 Codex 建議的「能改造才算結業」，本案保留為**選修**而非強制（迎合「沒心的學員」）

## 工時估算

| 工項 | 工時 |
|------|------|
| 設計 Lite Pack 8 個 workflow JSON | 16-24h（每個 2-3h，含實測） |
| Lite Pack setup-wizard.command + .bat | 8-12h（含 GUI 對話框 + n8n API 整合 + smoke test） |
| Lite Pack README + sample-data | 4h |
| Google Pack 4 個 workflow JSON | 8-12h |
| Google Pack setup-wizard 含 Google Console 圖文引導 | 12-16h（最複雜） |
| 原理說明文件 12 份（每個 workflow 一份） | 24h |
| 講義路徑改寫（m3 / m4 各單元加「成品演示 + 原理連結」） | 16h |
| 全程實測一輪（從 zero 到結業作品）| 8h |
| 文案 + 招生頁 + 大綱對齊新承諾 | 6h |
| **合計** | **~102-130h（約 13-16 個工作天）** |

## 風險與緩解

| 風險 | 緩解 |
|------|------|
| n8n 升級導致 workflow JSON 不相容 | n8n image 鎖 patch 版本（已做）+ 每季回檢 |
| Gemini API 改版 | 用 Generic Auth + 直打 HTTPS API（不用 n8n 內建 Gemini node） |
| Google OAuth scope 政策變動 | Google Pack 明確標示「目前 2026-05 規則」+ 每季回檢 |
| setup-wizard 在某些 macOS / Win 版本失敗 | 主測 macOS 14+ / Win 11，舊版本標示「不保證」 |
| 學員「只用不學」變成課程貶值 | Builder Track 提供進修通道，課程定位文案明示「快裝 + 進階」雙模式 |

## 建議下一步

1. **使用者確認三層架構方向**（不再變更）
2. **開新 plan 檔**：細化 Lite Pack 8 個 workflow 的節點規格
3. **動手第一個 workflow JSON**（從 PDF AI 改名開始，這是 M3 核心 deliverable）
4. **同步動手 setup-wizard 雛型**（先做 macOS 版本驗證流程）
5. **使用者實測一輪**（從 zero 走完整動線）
6. **依實測修補後正式上線**

## 飛輪規則新增（建議）

把「**商業培訓 vs 自學工程師：學員真實訴求驅動設計**」寫進飛輪規則，提醒未來課程設計時不要套用「學員應該想學原理」這個自學工程師假設。

詳見 `_規範/飛輪規則.md` 待新增章節。
