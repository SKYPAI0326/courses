---
review_type: course-implementation-completeness
course_slug: n8n
course_name: AI 資料工廠 — 大規模文件處理實戰
duration: 8h
total_units: 40
review_date: 2026-04-30
reviewer: course-designer × Codex L3 異質審核（兩輪）
codex_call_id_1: 63c0b5f7
codex_verdict_1: actionable
codex_call_id_2: 348da75a
codex_verdict_2: actionable
addendum_trigger: 使用者提供代表性 Make scenario「02_AI秘書_進階」作為學員起點水準基準線
---

# n8n 課程實作完整度評估

**評估目標**：對照使用者明定的三條驗收標準，盤點現況、列出缺口、產出可執行的修補與 Make JSON 待提供清單。

**評估標準**：

1. **每一步都讓學員可以有內容操作**（非純觀念講解）
2. **屬於實質工作流搭建**（非單一節點教學或概念示範）
3. **結業時學員持有一份以上的「自動化工作流 + GenAI」**（可帶走、可重用）

**評估方法**：course-designer 自評（Phase A，40 單元逐項 R1/R2/R3 三維評分） + Codex L3 異質審核（Phase B，CALL_ID `63c0b5f7`，verdict `actionable`）

---

## 1. 三條標準達標度總覽

| 標準 | 量化指標 | 達標度 | 一句話結論 |
|------|---------|--------|-----------|
| **#1 每步操作** | R1≥2 / 40 = 50%、R1≥1 / 40 = 92.5% | **勉強及格** | 多數頁面有步驟，但只一半達「step-block + verify-box + 可跑範例」高品質驗收，純參考頁 7+ 拖累分數 |
| **#2 實質工作流搭建** | R2=2 / 40 = 15%（6 單元） | **偏低** | 6/40 完整端到端工作流對 skill-operation 課程偏少；M1 / M2 兩個 Module 全無 R2=2 工作流，前半段體感偏「準備工作」 |
| **#3 結業帶走 GenAI 工作流** | 3 個 working GenAI deliverable | **脆弱達成** | m3-2-rename / m3-3-generate / m4-3-ai 足以兌現「一份以上」承諾，但 5 個 workflow JSON 仍待補；課名「資料工廠」「大規模文件處理」未充分支撐（缺 error handling、批次控速、processed/failed 機制） |

**整體判斷**：課程「可以交付」，但還不能理直氣壯稱為完整的「AI 資料工廠實戰」。骨架紮實、有 3 個強案例支撐承諾，但有 5 個 workflow JSON 待補、7 個純參考頁無實作驗收、課名兌現深度不足。

**Codex 補強判斷**：駁斥「R1≥1 有 92.5%」這個樂觀解讀 — `R1≥1` 只證明頁面不是純文章，不證明符合 skill-operation；對 Make 進階受眾，真正有價值的指標是「至少 60-70% 單元有可驗收操作 + 25-35% 構成完整或半完整 workflow + 每 Module 至少一個可帶走工作流」。當前狀況距此基準仍有 gap。

> ⚠️ **文案誠實度風險**（Codex 第二輪 `348da75a` 駁斥）：課程現行三大差異化主張需要修正措辭，否則對 Make 進階受眾構成誤導：
>
> 1. **「無執行次數限制」** → 改為「以較高的技術責任，換取更低的邊際執行成本與本機能力」 — self-host「免費」是把 SaaS 帳單換成機器/電費/網路/Tunnel/備份/維運時間的隱性成本
> 2. **「機密資料留本機」** → Gmail API 抓信本身在 Google、Gemini API 把信送 Google Cloud inference（Free Tier 還會用資料改善產品）— 對「AI 處理雲端來源資料」場景幾乎不成立。改成威脅模型陳述：「哪些資料留本機（本機 PDF/Excel/CSV）、哪些必送雲端（Gmail/Gemini/Telegram）、哪些可用 local LLM 取代」
> 3. **「Make → n8n 遷移無痛」假設** → n8n vs Make 對等度逐項落差：JSON Parse + UDT 對等度 70%（Make 有 friendly UI，n8n 要教 Code node + JSON Schema）、onerror Ignore 對等度 65%（Continue On Fail 不等於 Make 模組級忽略）、Router 心智模型差異（Make filter on edge vs n8n IF/Switch node）— 不能教成「一鍵搬家」

---

## 2. 單元評分矩陣

評分標準：

- **R1 操作可行性**：0=純觀念｜1=有步驟缺驗收｜2=step-block + verify-box + 可跑
- **R2 工作流完整度**：0=單節點介紹｜1=2-3 節點片段｜2=完整端到端
- **R3 GenAI 整合**：N/A=無關｜0=僅提及｜1=有 prompt 但未串入工作流｜2=GenAI 真正串入 n8n 工作流

### Module 1 — 環境建置與雲地橋接（13 單元）

| # | 單元 | R1 | R2 | R3 | 內容 | 學員成品 |
|---|------|----|----|----|------|---------|
| 1 | m1-1-overview | 1 | 0 | N/A | 安裝旅程 4 步驟總覽與前置檢查 | 完成預檢 |
| 2 | m1-1-install | 2 | 0 | N/A | Docker Desktop 雙平台安裝 | 運作中的 Docker Desktop |
| 3 | m1-1-launch | 2 | 1 | 0 | n8n 啟動 + Webhook hello-world 測試 | localhost:5678 + Webhook 跑通 |
| 4 | m1-1-troubleshoot | 1 | 0 | N/A | 8 大常見錯誤排查手冊 | 自助診斷流程 |
| 5 | m1-1-setup | 1 | 0 | N/A | 1.1 環境建置 Hub 導覽頁 | 無（純導覽） |
| 6 | m1-1-glossary | 0 | 0 | N/A | n8n × Make 術語對照表 | 術語查詢表 |
| 7 | m1-1-nodes | 1 | 0 | N/A | 節點新增、連線、命名速查 | 介面操作熟悉 |
| 8 | m1-2-tunnel | 2 | 1 | 0 | Cloudflare Tunnel 7 步設定 | 公開可用 Webhook URL |
| 9 | m1-2-autostart | 2 | 0 | N/A | cloudflared 自動啟動 | Tunnel 開機自動執行 |
| 10 | m1-2-hostname | 1 | 0 | N/A | 多 Hostname 應用場景 | 設定思路 |
| 11 | m1-3-expression | 0 | 0 | N/A | Expression 語法速查表 | 可查閱的語法參考 |
| 12 | m1-3-json | 2 | 1 | 1 | JSON 基礎 + AI Prompting 結構化輸出 | n8n + LLM 結構化 JSON 輸出 |
| 13 | m1-3-prompt | 1 | 0 | 1 | 4 種文件 AI JSON Prompt 範本 | Prompt 範本（無 n8n 整合） |

**M1 觀察**：環境建置步驟完整、Tunnel 有實作，但「教完環境之後學員不知道要幹什麼」。1.3 給了 Prompt 範本卻沒教「如何在 HTTP Request 節點呼叫 Gemini API + 解析回應」，是承諾兌現的第一個斷點。

### Module 2 — 數據引用與邏輯判斷（9 單元）

| # | 單元 | R1 | R2 | R3 | 內容 | 學員成品 |
|---|------|----|----|----|------|---------|
| 14 | m2-1-reference | 2 | 1 | N/A | 相對/絕對引用語法 | 三節點對照工作流 |
| 15 | m2-1-absolute | 2 | 1 | N/A | 絕對路徑精準定位 | Loop 內安全引用測試 |
| 16 | m2-1-dynamic | 1 | 0 | N/A | 動態欄位名稱（純參考） | 無 |
| 17 | m2-2-optional | 2 | 1 | N/A | Optional Chaining ?. 語法 | null 值保護測試 |
| 18 | m2-2-chaining | 2 | 1 | N/A | ?. 與 ?? 雙防護 | 缺漏欄位預設值處理 |
| 19 | m2-2-default | 1 | 0 | N/A | 預設值與資料驗證（純參考） | 無 |
| 20 | m2-3-logic | 2 | 1 | N/A | If 節點二分流 | 金額判斷分流工作流 |
| 21 | m2-3-switch | 2 | 1 | N/A | Switch 節點多路分流 | 三路 type 分流測試 |
| 22 | m2-3-complex | 1 | 0 | N/A | AND/OR 複合邏輯（純參考） | 無 |

**M2 觀察**：5 實作 + 3 純參考頁分布合理，R3 全 N/A 符合 Module 定位。弱點：3 個純參考頁（dynamic / default / complex）無 step-block，學員容易「看懂了但不會做」。

### Module 3 — 重型文件工廠（9 單元）

| # | 單元 | R1 | R2 | R3 | 內容 | 學員成品 |
|---|------|----|----|----|------|---------|
| 23 | m3-1-watch | 2 | 1 | N/A | Watch Folder 配置 + If 過濾 | 監控資料夾觸發流程 |
| 24 | m3-1-strategy | 1 | 0 | N/A | Watch vs Schedule 決策表（純參考） | 觸發模式選擇思路 |
| 25 | m3-1-filter | 1 | 0 | N/A | 副檔名過濾三方法（純參考） | 過濾規則參考 |
| 26 | **m3-2-rename** | **2** | **2** | **2** | **Watch + Gemini + Rename 完整流** | **PDF AI 改名工作流** |
| 27 | m3-2-batch | 2 | 2 | 1 | Code 讀資料夾 + Loop + 批次 rename | 批次處理工作流 + 日誌 |
| 28 | m3-2-naming | 1 | 0 | N/A | 命名規則（純參考） | 命名策略 |
| 29 | **m3-3-generate** | **2** | **2** | **2** | **Schedule + Gemini + 日報** | **AI 日報自動化工作流** |
| 30 | m3-3-multiformat | 1 | 1 | 1 | 多格式轉換 + Switch 分流 | 邏輯理解（無驗收） |
| 31 | m3-3-schedule | 1 | 0 | N/A | Cron 語法速查（純參考） | 排程設定參考 |

**M3 觀察**：M3 是課程「核心優勢區」，m3-2-rename 與 m3-3-generate 是高品質實作典範（R1/R2/R3 全 2 分），是課程兌現第三條標準的關鍵兩支柱。但 4 個純參考頁（strategy / filter / naming / schedule）讓 Module 節奏掉回「讀教材」。

### Module 4 — 綜合實戰（9 單元）

| # | 單元 | R1 | R2 | R3 | 內容 | 學員成品 |
|---|------|----|----|----|------|---------|
| 32 | **m4-1-remote** | **2** | **2** | 0 | **Form + Make + Tunnel + n8n 完整鏈路** | **遠端遙控本機 n8n 自動化** |
| 33 | m4-1-control | 2 | 1 | 0 | n8n Switch 分流 + Respond | 多分支回傳工作流 |
| 34 | m4-1-data | 2 | 0 | 0 | Webhook 解析 + 時間轉換 | 資料整理範例 |
| 35 | m4-2-flow | 1 | 0 | N/A | Make vs n8n 任務分配（純參考） | 決策框架 |
| 36 | m4-2-api | 1 | 0 | N/A | Make ↔ n8n 串接細節（純參考） | 串接細節參考 |
| 37 | **m4-2-hybrid** | **2** | **2** | 0 | **Form → Make → n8n 文件 → Gmail** | **雙引擎協作工作流** |
| 38 | **m4-3-ai** | **2** | **2** | **2** | **Webhook + Gemini + Code + Write + Make 回傳** | **AI 企劃生成工作流** |
| 39 | m4-3-docs | 1 | 1 | 1 | Google Docs OAuth + Create + Update | Google Docs 自動化（驗收薄弱） |
| 40 | m4-3-prompt | 0 | 0 | 2 | Prompt 穩定 JSON 範本（純參考） | Prompt 模板 |

**M4 觀察**：壓軸定位**基本兌現** — m4-1-remote、m4-2-hybrid、m4-3-ai 構成「Form → Make → Tunnel → n8n → Gemini → Docs/Gmail」的完整 deliverable 鏈。但 m4-2-flow + m4-2-api 是純概念補充頁、m4-3-docs 改為「新建 Doc」過度簡化（缺 Copy 模板實戰）、m4-3-prompt 給範本但無實作驗收。

### 整體統計

| 維度 | 滿分（2） | 中等（1） | 缺項（0） | N/A | 滿分率 |
|------|----------|---------|----------|-----|-------|
| R1 操作可行性 | 20 | 17 | 3 | — | **50%** |
| R2 工作流完整度 | 6 | 13 | 21 | — | **15%** |
| R3 GenAI 整合 | 4 | 4 | 6 | 26 | 4/14 GenAI 相關單元 = 29% |

**真正可帶走的 working GenAI 工作流**：3 個（m3-2-rename / m3-3-generate / m4-3-ai） — m4-3-prompt 雖 R3=2 但是純參考頁，不算 deliverable。

---

## 3. 結業 deliverables 盤點

學員 8 小時課程結束後，實際能帶走的「成品」清單：

### ✅ 已具備（達成承諾的核心）

1. **跑在自己電腦上的 n8n 站**（Docker Compose + 一鍵腳本，永久可用）
2. **Cloudflare Tunnel 通道**（本機 Webhook 對外公開）
3. **3 個 working GenAI 工作流**：
   - PDF AI 改名（Watch + Gemini + Rename）
   - 定時 AI 日報（Schedule + Gemini + Write File）
   - AI 企劃生成（Webhook + Gemini + Make 雙引擎協作）
4. **2 個非 GenAI 完整工作流**：
   - 遠端遙控本機（Form → Make → n8n）
   - 雙引擎協作（Hybrid + Gmail 通知）
5. **試跑包**（n8n-starter-kit + sample-data 三組範例資料）
   - ⚠️→✅ **本評估初版誤判**：寫成「✓ 已具備」過於樂觀。實際學員演練發現下載動線斷裂（無 zip 包 / 9 個個別檔連結 / macOS quarantine + 失執行權限），於 2026-04-30 修補完成 — 詳見 `_change-log.md` 與 `_規範/飛輪規則.md` § 試跑包交付完整性規則
   - 修補後狀態：zip 一鍵下載 + macOS chmod/xattr 指引 + README 詳細啟動流程 ✅

### ⚠️ 規格內但未交付（5 個 workflow JSON 待補）

| 大綱規格 | 對應單元 | 現況 |
|---------|---------|------|
| `m1-webhook-hello-world.json` | m1-1-launch | 待補 |
| `m2-reference-practice.json` | m2-1-reference | 待補 |
| `m3-folder-watch-demo.json` | m3-1-watch | 待補 |
| `m3-ai-rename-demo.json` | m3-2-rename | 待補（**最關鍵**） |
| `m4-google-form-to-n8n-demo.json` | m4-1-remote | 待補 |

### ❌ 課名「資料工廠」「大規模文件處理」承諾下的缺口

- 批次控速（SplitInBatches + Wait + API rate limit 處理）
- AI 輸出 JSON Schema 驗證與修復
- processed / failed 資料夾分流機制
- 處理 summary 報表（哪幾份成功、哪幾份失敗、log）
- 重試邏輯（partial failure recovery）

---

## 4. 缺口排序

### 🔴 P0 必補（影響「結業帶走」承諾）

| 缺口 | 對應單元 | 修補類型 | 預估工時 |
|------|---------|---------|---------|
| 補 `m3-ai-rename-demo.json` | m3-2-rename | 補 workflow JSON 範本 | 1.5h |
| 補 `m4-google-form-to-n8n-demo.json` | m4-1-remote | 補 workflow JSON 範本 | 2h |
| 補 `m3-folder-watch-demo.json` | m3-1-watch | 補 workflow JSON 範本 | 1h |
| **新增 M3-4 單元：批次處理錯誤恢復與處理報表** | （新單元） | 新教案 + 新 HTML + workflow JSON | 4-5h |
| 補 m1-3-prompt 的 n8n 整合範例（HTTP Request → Gemini → 解析） | m1-3-prompt | HTML 補強 + 1 個 workflow JSON | 2h |
| **🆕 P0-NEW：新增「Make AI 秘書 → n8n 完整遷移」單元（M4-4 或替代 m4-3-ai）** | （新單元，使用者提供 Make scenario 作為起點） | 新教案 + 新 HTML + workflow JSON + 對照表 | 5-6h |
| **修正大綱 § Brand Brief 與 index.html 文案中三大差異化主張** | `_outlines/n8n.md` + `index.html` + 相關 hero / FAQ 區塊 | 文案重寫 + 加「決策表」（Make Cloud / n8n Cloud / n8n local / VPS / Python cron 五選） | 2h |

**P0 合計**：~17-19h（含 P0-NEW + 文案修正），是兌現「Make 進階轉 n8n」承諾與避免文案誤導的最低必要修補。

**P0-NEW 詳細需求**（基於使用者提供的「02_AI秘書_進階」Make scenario）：

| 區塊 | 內容 |
|------|------|
| 場景 | 把學員既有 Make AI 秘書（Gmail trigger + Aggregate + Gemini 4 區 JSON + Feeder + Router 4 路 + TG/Email/Docs/HTTP）在 n8n 完整重建 |
| 對照表 | Make Module ↔ n8n Node 1:1 對照（含對等度 % 與差異警示，引用 Codex `348da75a` 表格） |
| 開場 demo | 跑 Make 版本，展示 1000 ops 焦慮 + 機密信件路徑分析 |
| 結尾 demo | 跑 n8n 版本，展示同功能 + 可選擇用 Ollama local LLM 處理機密信件（去識別化版） |
| Workflow JSON | `m4-4-ai-secretary-migration.json`（n8n 版本，含 Gmail Trigger / Aggregate / HTTP Gemini / JSON Schema 驗證 / Split Out / IF×4 路由 / Telegram / Gmail / Docs / HTTP + Continue On Fail） |
| 教學重點 | (1) Aggregate 5 items → 1 array 的兩種寫法（Aggregate node vs Code node `items.map`）<br>(2) AI 字串包 JSON 解析的 Code node 實作<br>(3) 多 boolean flag 並行分發 vs Switch 單值分支差異<br>(4) Continue On Fail 在 JSON Parse 上的設定<br>(5) Make UDT vs n8n JSON Schema 對應做法<br>(6) **威脅模型講解**：哪些步驟資料離開本機 + 哪些可改用 local LLM |
| 結業 deliverable | 學員拿著自己的 Make scenario 走出教室，已經完成 1:1 重建版本，可立即在自家 n8n 站運行 |

### 🟡 P1 應補（影響「實質工作流」評價）

| 缺口 | 對應單元 | 修補類型 | 預估工時 |
|------|---------|---------|---------|
| 補 `m2-reference-practice.json` + 升級 m2 純參考頁為迷你練習 | m2-1-dynamic / m2-2-default / m2-3-complex | 3 個迷你工作流（10-15min/個） | 3h |
| 升級 m3 純參考頁為迷你練習 | m3-1-strategy / m3-1-filter / m3-2-naming / m3-3-schedule | 4 個迷你工作流 | 4h |
| 補 `m1-webhook-hello-world.json` + 強化 m1-1-launch verify-box | m1-1-launch | workflow JSON + verify 強化 | 1h |
| m4-2-flow / m4-2-api 升級為「決策框架 + 1 個對照工作流」 | m4-2-flow / m4-2-api | 教學重構 + 1 workflow | 3h |
| m4-3-docs 補「Copy 模板 + Replace」實戰 | m4-3-docs | HTML 強化 + workflow 補完整 | 2h |

**P1 合計**：~13h，補完後課程實作完整度從「勉強及格」提升到「定位可信」。

### 🟢 P2 可補（驗收框 / 文字優化）

| 缺口 | 對應單元 | 修補類型 | 預估工時 |
|------|---------|---------|---------|
| 補 5 頁「預期輸出」驗收框（既有 B2 backlog） | m1-2-tunnel / m3-2-rename / m3-3-generate / m4-1-remote / m4-3-docs | verify-box 文字 | 1h |
| Gemini rate limit / quota 警告集中 | m4-3-ai / m3-2-batch | 警告框統一 | 0.5h |
| m4-3-prompt 補「整合進工作流」連結 | m4-3-prompt | 純文字補連結 | 0.3h |

**P2 合計**：~2h，屬精修細節，不影響承諾兌現。

---

## 5. 待使用者提供 Make JSON 清單

使用者承諾可提供 Make.com 工作流 JSON 作為**邏輯範本**（注意：Make export JSON 結構與 n8n workflow JSON **完全不同**，無法直接 import；需作為「業務邏輯參考骨架」由 course-designer 後續做 n8n 重建）。

按 Codex 建議的 P0 優先順序，請使用者提供下列 Make 工作流 JSON：

### 🔴 最關鍵兩個（請優先提供）

| # | Make 工作流主題 | 對應 n8n 單元 | 期望邏輯結構 | 為何 Make 範本有用 |
|---|---------------|--------------|------------|-----------------|
| 1 | **PDF / 文件批次處理 + AI 抽取/改名** | m3-2-rename / m3-2-batch | trigger（dropbox/google drive watch / scheduler）→ filter PDF → text extraction（OCR or PDF parser）→ Gemini API call → JSON parse → rename / move | 學員是 Make 用戶，看到熟悉的 Make 邏輯能對照「相同業務在 n8n 裡的做法」，加速心智模型轉移；同時讓 course-designer 知道 Make 用戶實際在做什麼工作流 |
| 2 | **Google Form → 後端處理 → 通知** | m4-1-remote / m4-2-hybrid / m4-3-ai | Form trigger → router by 類型 → 不同 module 處理（簡單回 Email vs 重型生成）→ Sheets log + Gmail 通知 | M4 是課程壓軸的 deliverable 鏈核心，使用者既有 Make 表單流可直接示範「哪些步驟適合留 Make、哪些遷移到 n8n」 |

### 🟡 應提供（補完整 deliverable 矩陣）

| # | Make 工作流主題 | 對應 n8n 單元 | 期望邏輯結構 |
|---|---------------|--------------|------------|
| 3 | 資料夾監控 + 簡單觸發處理 | m3-1-watch / m3-folder-watch-demo | watch trigger → process → notify |
| 4 | 定時排程彙整任務（多源讀取 + 寫出） | m3-3-generate / m3-3-schedule | Schedule → Multi-source read → AI summarize → Multi-format write |
| 5 | API 整合（HTTP Request + Auth + Error Handling） | m4-2-api | external API call → retry → error route → success route |

### 🟢 加分項（如有，可補強 P1 缺口）

| # | Make 工作流主題 | 對應 n8n 單元 |
|---|---------------|--------------|
| 6 | 巢狀資料 / 動態欄位引用練習工作流 | m2-1-dynamic / m2-2-default |
| 7 | 多分支邏輯判斷（含 AND/OR 複合條件） | m2-3-complex |
| 8 | 錯誤處理 / failed folder 機制 | （新單元 M3-4） |

### 提供方式建議

1. **格式**：Make Scenario 的 JSON export（Make UI 右上角 ⋯ → Export Blueprint）
2. **路徑**：直接貼到對話、或放到 `/讓我提供/make-templates/` 都可
3. **檢查**：請先確認 JSON 內無 API key / token / password 真實字串（Make export 可能保留某些參數）
4. **註解**：每個 JSON 簡短一句說明「業務目的」與「現在實際每月跑幾次」（這幫助評估流量規模適配 n8n 設計）

---

## 6. Codex 第二意見摘要

**CALL_ID**：`63c0b5f7`
**Verdict**：`actionable`（已 mark-verdict）

### Codex 建議重點

1. **比 Phase A 更嚴格**：5 個待補 workflow JSON 不是小瑕疵，是「結業交付物完整度的核心缺口」
2. **駁斥樂觀解讀**：`R1≥1=92.5%` 只證明頁面不是純文章，不證明符合 skill-operation；對 Make 進階受眾，真正基準應是「至少 60-70% 單元有可驗收操作 + 25-35% 構成完整工作流 + 每 Module 至少一個可帶走工作流」
3. **deliverable 不足支撐課名**：3 個 working GenAI 工作流可最低限度兌現「一份以上」承諾，但不足支撐「資料工廠」「大規模文件處理」 — 缺批次處理一整個資料夾、CSV/Excel 大量資料、API rate limit / retry / partial failure、AI JSON Schema 驗證、processed/failed folder、處理 summary
4. **JSON 補強優先順序**：m3-ai-rename-demo > m4-google-form-to-n8n-demo > m3-folder-watch-demo > m2-reference-practice > m1-webhook-hello-world（如時間只能補一個，補第一個）
5. **M2 / M3-1 純參考頁應升級**：不要刪掉速查表，但每個速查表至少附一個「10-15 分鐘可跑的最小 workflow」，符合 skill-operation 課程定位
6. **若只能加 1 個單元**：建議加「**M3-4：批次文件處理的錯誤恢復與處理報表**」 — Watch → Read → Gemini → Validate JSON → Success/Failed 分流 → Move File → Append Log → Generate Summary。這個單元能直接補強課名裡的「工廠」感，比 Vector DB 或 Self-hosted LLM 更務實

### 我的判斷（accepted）

**接受**：

- ✅ JSON 補強優先順序（精準排序，符合受眾痛點與課程定位）
- ✅ M3-4 新單元（這正是課名「資料工廠」與「大規模處理」的兌現關鍵 — 不解決「100 份跑到 73 份失敗怎麼辦」就稱不上工廠）
- ✅ 純參考頁應附最小工作流（已納入 P1 缺口）
- ✅ 對「R1≥1=92.5%」的駁斥（已調整總覽結論：標準#1 從「合格邊緣」改為「勉強及格」）

**部分採納**：

- ⚠️ Codex 建議「把環境/語法改成嵌入式教學」 — 理論方向對，但實際課程已上線、結構已成型，本次評估不觸及課程結構重構，只列入「未來改版可考慮」備註
- ⚠️ Codex 提到「批次/CSV/Excel 大量資料」 — 第一階段先做 M3-4 error handling 即足以兌現課名；CSV/Excel 大量處理可作為 M3-4 之後的進階單元考慮，但本次評估報告先不列為 P0

**不採納**：無

### 理由

Codex 站在自動化教育者第二意見立場，避開 Phase A 內部評分時可能的「對自家評分標準的自我合理化」，駁斥精準到位。三條核心建議（JSON 順序 / M3-4 / 純參考頁升級）皆有可立即執行的 actionable 修補路徑，且預估工時合理（P0 ~10-11h、P1 ~13h），不至於變成另一個課程重做。

---

## 7. 建議下一步

### 推薦執行路徑

```
Step 1（即刻） → Step 2（1 週內） → Step 3（2 週內） → Step 4（1 個月）
```

| Step | 動作 | 觸發條件 | 對應 skill |
|------|------|---------|-----------|
| **1. 收 Make JSON 範本** | 向使用者收 § 5 的 #1 + #2 兩支關鍵 Make 工作流 | 立即 | 對話索取 |
| **2. 補 P0 三支 workflow JSON** | m3-ai-rename-demo / m4-google-form-to-n8n-demo / m3-folder-watch-demo | 收到 Make 範本後 | course-designer（規劃 n8n workflow 邏輯）→ 手動在 n8n UI 建構 → 匯出 JSON → grep 檢查無敏感字串 → 放 `assets/workflows/` |
| **3. 新增 M3-4 單元** | 教案 + HTML + workflow JSON 三件套 | P0 完成後 | course-designer → build-course-page → lint-page.py → build-search-index → build-sitemap |
| **4. 處理 P1 純參考頁升級 + m1-3-prompt 整合** | 7 個迷你工作流 + 1 個整合範例 | M3-4 上線後 | course-designer + build-course-page 並行 |

### 不建議現在做

- ❌ 重構環境/語法為嵌入式教學（傷及既有結構，課程已上線）
- ❌ 補 Vector DB / Self-hosted LLM / Webhook 安全等「擴寬」單元（會讓課程失焦，先把「資料工廠」承諾兌現再說）
- ❌ 把全部 7 個純參考頁升級為完整 workflow（迷你練習 10-15 分鐘即可，避免吃掉太多課時）

### 開新 plan 的觸發

本評估報告為**唯讀產出**，不修改任何課程內容。

- 確認執行 P0 修補 → 開新 plan：`n8n-p0-workflow-json-{動物名}.md`
- 確認新增 M3-4 → 開新 plan：`n8n-m3-4-error-handling-{動物名}.md`
- 確認執行 P1 升級 → 開新 plan：`n8n-p1-mini-workflow-upgrade-{動物名}.md`

每個 plan 應走 course-designer → course-reviewer → build-course-page → course-ops 完整 G2-G4 流程。

---

## 附錄：本次評估的事實基礎

- **大綱**：`_outlines/n8n.md`（2026-04-23 補建，6 項學習成果、9 項 workflow JSON deliverable 規格）
- **教案 SSOT 缺口**：`_lessons/n8n/` 僅 4 個 .md（M1.1 子單元）— 其餘 36 單元 HTML 無對應教案，本次評估以 HTML 為事實來源
- **試跑包**：`courses/n8n/assets/n8n-starter-kit/`（compose + scripts + .env） + `sample-data/`（invoices / daily-report / forms）
- **既有 backlog**：`courses/n8n/_change-log.md` 已記錄 5 頁 verify-box 補強 + 5 個 workflow JSON 待補
- **設計系統 SSOT**：`_規範/design-tokens.md` + `_規範/lesson-template-v3.html` + `docs/lint-page.py`（機器強制）
- **Codex L3**：`~/.claude/orchestration/codex_workflow.json` 已啟用（global enabled=true，Phase B 手動模式）

**評估範圍邊界**：本評估**不修改**任何課程 HTML / 教案 / workflow JSON。所有修補執行均待使用者看完本報告後另起 plan 觸發。

---

## 8. 補充審核：技術可行性 + 文案誠實度（Codex 第二輪）

**觸發**：使用者提供代表性 Make scenario「02_AI秘書_進階」（Gmail Trigger + Aggregator + Gemini 4 區 JSON + Feeder + Router 4 路 + TG/Email/Docs/HTTP）作為**學員 Make 起點水準基準線**，要求審核 (1) n8n 能否 1:1 重建 (2) 平台點數限制與本機檔案差異化是否真成立 (3) 其他觀點。

**Codex CALL_ID**：`348da75a`（verdict: `actionable`）

### 8.1 Make ↔ n8n 1:1 重建可行性逐項評估

| Make 節點 | n8n 對應做法 | 對等度 | 教學風險 |
|-----------|------------|-------:|---------|
| Gmail Search Module | Gmail node → Get Many（Search / Read Status / Limit）| 85% | 預設 simplified 可能只拿 metadata，body 要 Get full/raw |
| BasicAggregator（5 items → 1 array 餵 AI）| Aggregate node → All Item Data 或 Code node `items.map` | 90% | Gemini 子節點 expression 解析有「只取第一 item」的坑 |
| Gemini 2.5 Flash Module | Gemini node / Chat Model / HTTP Request 直打 | 80% | 要完全控制 model / response schema / safety / thinking budget，**HTTP Request 反而更穩** |
| JSON Parse + UDT 自定資料結構 | Structured Output Parser JSON Schema 或 Code node `JSON.parse` + schema validation | **70%** | Make UDT 對非工程使用者友善，n8n 沒有 1:1 對等的 friendly UI；要教 JSON Schema 或 Code node，**門檻提高** |
| BasicFeeder | Split Out node | 95% | 幾乎等價 |
| Router 4 路 boolean filter | IF / Switch / Filter，多分支連線 | 90% | n8n 多分支執行順序、item pairing、merge 行為要教清楚（**Make 心智模型不能直接套用**）|
| Telegram SendReplyMessage | Telegram node Send Message | 90% | 「回覆某則訊息」需有 message ID |
| onerror: Ignore | Continue On Fail / Error Workflow / Code try/catch | **65%** | 不是 Make 模組級 `onerror=Ignore` 同等體驗；錯誤忽略後資料形狀會改變，後續節點要防呆 |

**Codex 結論**：適合當遷移示範，但**不能教成「一鍵搬家」或「1:1 無腦重建」**。真正要教的是資料結構轉換、錯誤處理、AI schema 約束、分支語義差異。

### 8.2 「規避平台點數限制」聲稱的工程現實

**流量重新計算**（駁斥課程隱含假設）：

- 使用情境：每 15 分鐘 × 5 封打包成 1 次 Gemini call
- 實際每月 workflow executions：~2,880 次/月
- ⚠️ **這個數字根本沒打到 Make 免費 1,000 ops 痛點之外多遠**（Make Pro $9/月給 10K ops 已遠超過）
- 真正打到 30K ops 的場景：每封信獨立呼叫 Gemini × 96 次/天 × 30 天 = ~14,400 ops（也仍在 Pro 範圍）

**結論**：**這個 AI 秘書 scenario 拿來當「規避點數限制」demo，說服力薄弱。** Codex 駁斥：「對行銷企劃 / 營運 / 知識工作者，『免費』不是好主張。更誠實的主張是：用較高的技術責任，換取更低的邊際執行成本與本機能力。」

**TCO 真實狀況**：

| 比較項 | Make Pro $9/月 | n8n self-host |
|--------|---------------|---------------|
| 月直接費用 | $9 | 電費 ~$2-5（24/7 開機）|
| 隱性成本 | 0 | 機器折舊 + Tunnel 維護 + 備份 + 升級 + log 監控 + 故障排除（時數 × 時薪）|
| 技術責任 | SaaS 全包 | 學員自負 |
| 適用情況 | 一般行銷企劃 / 營運 | 高頻大量 / 本機檔案內網需求 / 願意維運 |

Codex 判斷：**「n8n self-host 只在三種情況明顯划算：高頻大量流程、本機檔案/內網需求、或學員本來就願意維運。」**

### 8.3 「機密資料留本機」聲稱的威脅模型缺口

**對這個 AI 秘書 scenario 幾乎不成立**：

```
Gmail（Google 雲）→ Gmail API 抓信（仍在 Google）→ 本機 n8n
   ↓
   信件 body 已在本機 → Gemini API 呼叫
   ↓
   Gemini 收到 信件全文（送回 Google Cloud inference）
   ↓
   ⚠️ Free Tier 還會用資料改善產品（官方 pricing 明示）
```

**真正能兌現「機密留本機」的場景**（Codex 列舉）：

1. ✅ 本機 PDF / Excel / CSV 清理（不送外部 API）
2. ✅ 內網資料庫、NAS、ERP 匯出檔
3. ✅ Ollama / llama.cpp / LM Studio 跑 local LLM
4. ✅ 本機 OCR + 規則抽取 + embedding 到本機 Qdrant/SQLite
5. ✅ 只把**去識別化摘要**送雲端模型，而非原文

**對應到課程現況**：

- M3-1-watch / M3-2-rename / M3-3-generate 的本機 PDF / Excel 處理場景 → 確實兌現 1, 2, 3 部分（但 m3-2-rename / m3-3-generate 仍呼叫 Gemini API，所以資料離開本機）
- **完全沒覆蓋**：Ollama / local LLM / 去識別化處理
- m4-3-ai 的 Webhook + Gemini + Docs 整合 → **資料路徑全部走雲端**，不該被歸類為「機密留本機」demo

**課程文案修正建議**：

- ❌ 不要說：「機密資料留本機」
- ✅ 改成：「支援本機資料處理與可選的本機 AI；若使用雲端 LLM，資料仍會離開本機」
- ✅ 加教學單元：「威脅模型決策表」— 哪些資料留本機、哪些必送雲端、哪些可用 local LLM 取代

### 8.4 Codex 點出的盲點（5 條）

1. **真正競品不是 Make Pro**，而是 `cron + Python + Gmail API + Gemini API`。進階 Make 使用者願意碰 n8n Code node，下一步可能直接 code-first，n8n 只是過渡
2. **n8n Cloud ≠ n8n self-host**：「本機檔案讀寫」在 n8n Cloud 不成立（官方 docs 明確）。課程文案不能模糊兩者
3. **受眾會分裂**：願意自架的人可能已自學 Docker；不願自架的會被 24/7 + Tunnel + 備份嚇走 → 課程應雙軌設計（local-first + managed/VPS-first）
4. **「AI 資料工廠」≠「AI 秘書」**：差異化應展示「大量檔案批次 + 資料清洗 + schema validation + 錯誤重跑 + local storage + 可追溯資料管線」 — 與 § 4 P0 的 M3-4 新單元方向一致
5. **安全承諾要改成威脅模型**：不要說「機密留本機」，要說「哪些資料留本機、哪些送雲端、哪些可用 local LLM 取代」 — 對工程背景學員更專業、不會被一眼打穿

### 8.5 教育設計建議（Codex）

- **「Make → n8n 遷移」不能是 0 分鐘** — 對這個受眾應是課程主線，至少 90-120 分鐘
- **黃金 demo 設計**：開場展示 Make 版本限制（credits / 檔案 / schema 錯誤 / log）→ 結尾展示 n8n 重建（同功能 + 少額度焦慮 + 可讀寫本機 + 可插 local LLM + 可保存錯誤樣本）
- **必列決策表**：Make Cloud / n8n Cloud / n8n local Mac/PC / n8n VPS / Python cron 五選 — 篩選對的人，而不是把所有人推向 self-host

### 8.6 我的判斷（accepted）

**接受**：

- ✅ 流量計算駁斥（這個 scenario 沒打到 Make 點數痛點，論證薄弱）
- ✅ 「機密留本機」威脅模型修正（必須改文案，否則對工程背景學員會被打穿）
- ✅ Make ↔ n8n 對等度逐項落差（不能教成 1:1 搬家）
- ✅ 雙軌教學設計（local-first + managed-first）
- ✅ 決策表必加（Make Cloud / n8n Cloud / n8n local / VPS / Python cron）
- ✅ M4-4 新增「Make AI 秘書 → n8n 完整遷移」90-120 分鐘黃金 demo（已加入 § 4 P0-NEW）

**部分採納**：

- ⚠️ Codex 提「真正競品是 cron + Python」 — 教育市場現實上仍可以站「visual builder + Code node 過渡」位，不需要完全改定位；但教學中應**誠實提及這條路線**作為高階學員的 next step

**不採納**：無

### 8.7 對課程定位的最終建議

從這份審核結論，課程現有定位「**Make 進階搭檔 · n8n 本機自動化實戰**」應改為更精準的：

> **「Make 進階使用者的 n8n 工程化過渡課 — 把雲端 SaaS 自動化轉成本機可控資料管線」**

聚焦在三件 Make 做不到、n8n 真能兌現的事：
1. **本機批次資料處理**（PDF / Excel / CSV，不必呼叫雲端）
2. **可選的去識別化 + local LLM**（用 Ollama 處理機密原文，再把摘要送雲端）
3. **錯誤恢復 + 處理報表的工程化能力**（partial failure / retry / log，這正是 § 4 P0 的 M3-4 新單元方向）

而**不是**：
- ❌ 「免費規避 Make 點數」（薄弱）
- ❌ 「機密資料留本機」（誤導）
- ❌ 「無腦從 Make 一鍵搬家」（不存在）
