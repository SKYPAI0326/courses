---
slug: n8n
name: AI 資料工廠 — 大規模文件處理實戰
color: "#5a7a5a"
audience: 已熟 Make 基礎、想學本機檔案處理與雲地分工，並願意承擔自架環境責任的自動化工作者
institution: 弄一下工作室
duration: 8h
optional_duration: 1.7h
tools: n8n (Community Edition self-host), Docker Desktop, Cloudflare Tunnel, Make
prac: true
# === 課程製作團隊系統擴充欄位 ===
course_type: skill-operation
pilot: false
platform_version: n8n Docker image（課前驗證版本）／Docker Desktop／Cloudflare Tunnel（課前驗證方案）
---

<!--
本大綱於 2026-04-23 補建（既有課程已上線但無對應大綱）
觸發事件：n8n Desktop App 於 2025-08-15 由官方封存（read-only），原以「n8n Desktop」為主軸的 Module 1.1 安裝章節需轉軌
詳細執行計畫：~/.claude/plans/n8n-desktop-velvety-giraffe.md
-->

## 課程定位（Positioning）

教 Make 進階使用者用 n8n 本機版（Docker Desktop + Compose）補上雲端流程不適合直接處理的能力：**本機檔案直接讀寫**與**可控的批次處理**；同時評估雲端方案額度、維運成本、資料邊界與雲地協作方式。

## 受眾畫像（Audience Profile）

- **職業**：行銷企劃、營運、知識工作者、小型工作室主理人
- **技術底子**：會用 Make、看得懂第一階段產出的資料契約與測試案例、敢開瀏覽器點 localhost；不需指令列基礎，但願意裝 Docker Desktop 並處理基本環境問題
- **現有工具棧**：Make、Google Workspace、ChatGPT/Claude 等 LLM；是否需要轉換，依任務用量、資料位置與維運責任評估
- **痛點 3 條**：
  1. 雲端方案的額度、等待時間或執行量不適合某些批次任務，需要比較替代架構
  2. 想自動處理本機資料夾裡的 PDF／文件，雲端流程不適合直接讀寫本機檔案
  3. 需要知道哪些資料會留在本機、哪些資料會送往雲端服務或 LLM，再決定處理方式

## Brand Brief（品牌調性）

- **tone_register**：技術友善（清楚、實作導向，不端架子）
- **mood_keywords**：職人感、可靠、工廠秩序
- **differentiation**：以較高的技術責任，換取本機檔案處理與可控的批次能力 — 學員會帶走一個跑在自己電腦上、可持續維護的 n8n 工作站，並具備「把雲端 SaaS 自動化轉成本機可控資料管線」的工程化能力

### 文案誠實度規則（Brand Honesty Rules）

依 Codex L3 兩輪審核（CALL_ID 63c0b5f7 / 348da75a）結論，下列三大主張**禁止**用於課程文案、行銷頁、招生敘述：

| ❌ 不要說 | ✅ 改成 |
|----------|--------|
| 「無執行次數限制」「免費」 | 「以較高技術責任換取更低邊際執行成本」（self-host 把 SaaS 帳單換成電費/維運/備份/升級的隱性成本，要誠實揭露） |
| 「機密資料留本機」 | 「支援本機資料處理與可選的本機 AI；若使用雲端 LLM（Gemini API），資料仍會離開本機」（Gmail API 抓信代表資料仍在 Google；Free Tier 還會用資料改善產品） |
| 「Make → n8n 一鍵搬家」「無腦遷移」 | 「Make ↔ n8n 對等度多在 65–95% 之間，需學會資料形狀轉換、分發 vs 分支差異、JSON Schema 約束、錯誤處理對等」 |

每篇單元教案、首頁 hero、FAQ、招生頁敘述，違反上述規則的文字必須修正。

## 學習成果（Outcomes，動詞開頭、可驗證）

1. **能在自己電腦上完成 n8n 本機環境建置**（Docker Desktop + Compose、開到 localhost:5678 並完成首次設定）
2. **能設定 Cloudflare Tunnel 把本機 n8n Webhook 對外公開**，給雲端服務（如 Make）回打
3. **能用 Optional Chaining 與 If/Switch 節點**處理巢狀 JSON 與分支邏輯，避免 undefined 錯誤
4. **能設計資料夾檔案處理工作流**，先用 Manual Trigger + Read/Write Files from Disk 完成可重現的批次處理；即時監控資料夾為依版本與環境驗證的延伸
5. **能組合 Make 與 n8n 的雲地協作架構**，把雲端訊號（表單、Webhook）導到本機跑批次任務
6. **能診斷常見 n8n 自架環境錯誤**（埠衝突、Docker 沒開、權限問題、ERR_CONNECTION_REFUSED）並自助排除
7. **在另備複雜 Make scenario 時，能把它在 n8n 逐步重建**（含 Aggregate / 分發式路由 / JSON Parse 防禦 / Continue On Fail），並對工作流每一步做威脅模型分析；此為進階選修，不列為核心完成條件

## 環境風險聲明（必讀）

**n8n Desktop App 已退役**：n8n 官方自 2024 年起停止 Desktop App 開發，GitHub 倉庫 `n8n-io/n8n-desktop-app` 於 **2025-08-15 封存（read-only）**。本課程**不使用** Desktop App，改採官方推薦的 **Docker Desktop + Docker Compose** 方案 — 學員體驗仍是「桌面應用」（Docker Desktop 有 GUI），但 n8n 本身以容器形式跑在背景，啟動透過課程提供的一鍵腳本（`start.command` / `start.bat`）完成，不需學員手打 docker 指令。

**因應措施**：
- 1.1 安裝章節拆 4 子單元（overview / install / launch / troubleshoot），自助補課友善
- 提供 `n8n-starter-kit` 試跑包（compose YAML + 各平台一鍵腳本 + .env 範本 + README）
- troubleshoot 子頁專處理 8 大常見錯誤（埠衝突、WSL2、Apple Silicon platform、權限等）
- 課前先執行參與門檻 Gate：核心實作要求 8GB RAM、20GB 可用磁碟、可啟動 Docker；Windows 另要求 Win 10 22H2 build 19045／Win 11 23H2 build 22631 以上、WSL 2.1.5 以上、SLAT 與 BIOS/UEFI 硬體虛擬化。未通過者改用借用機／遠端備援或先由 IT 解鎖，不在課堂現場臨時修 BIOS。
- Gemma 4 + Ollama、Cloudflare Tunnel、Gemini API、Telegram 是延伸能力，不列為 Docker/n8n 核心入場門檻；本課核心不要求 GPU。

## 前置知識依賴鏈（Prerequisite Chain）

```yaml
dependencies:
  CH1-1: []                       # 環境建置（Docker + n8n）為一切起點
  CH1-1-overview: []
  CH1-1-install: [CH1-1-overview]
  CH1-1-launch: [CH1-1-install]
  CH1-1-troubleshoot: []          # 排錯手冊獨立可跳查
  CH1-2: [CH1-1-launch]           # Tunnel 需要先有可跑的 n8n
  CH1-3: [CH1-1-launch]           # JSON/Expression 需要 n8n 介面熟悉
  CH2-1: [CH1-3]                  # 數據引用建立在 Expression 之上
  CH2-2: [CH2-1]                  # Optional Chaining 是引用的進階
  CH2-3: [CH2-1]                  # 邏輯分支建立在引用之上
  CH3-1: [CH1-1-launch, CH2-3]    # 本機檔案基線需要環境 + 邏輯
  CH3-2: [CH3-1]                  # PDF 批次建立在檔案處理基線之上
  CH3-3: [CH2-3]                  # 定時彙整需要邏輯，不依賴即時監控
  CH4-1: [CH1-2, CH2-1]           # Google 表單遙控需要 Tunnel + 引用
  CH4-2: [CH4-1]                  # Make+n8n 雙引擎延伸自表單遙控
  CH4-3: [CH4-2, CH3-2]           # 企劃草稿產出整合檔案與 AI
  CH4-4: [CH1-3, CH2-1, CH2-3, CH3-2, CH4-3]  # AI 秘書遷移整合 prompt + 引用 + 邏輯 + 批次 + AI 整合
```

## 試跑包交付規格（Verification Assets）

依 course_type = skill-operation：

### 環境試跑包（M1 共用）
路徑：`courses/n8n/assets/n8n-starter-kit/`

- **n8n-compose.yml**：
  - 服務：n8n（latest image）+ PostgreSQL（持久化資料）
  - Volumes：n8n_data（workflows + credentials）、本機資料夾掛載示例（`./shared:/files/shared`，為 Module 3 鋪路）
  - 環境變數：基本帳號、時區、Webhook URL（搭配 Tunnel 預留）
  - 註解：每段配置標明用途，方便學員看懂
- **start.command**（Mac，雙擊執行）：`docker compose up -d` + `open http://localhost:5678`
- **start.bat**（Windows，雙擊執行）：等效 + `start http://localhost:5678`
- **stop.command** / **stop.bat**：`docker compose down`
- **update.command** / **update.bat**：`docker compose pull && docker compose up -d`
- **.env.example**：時區、管理者帳密、Webhook URL 範本（含註解）
- **README.md**：試跑包說明、各檔用途、最小執行流程、卡關時去 troubleshoot 子頁

### 各單元素材與匯入邊界

核心單元以「學員在目前 Docker／n8n 版本逐步建立」為主，不再假設每個單元都有可直接匯入的 JSON。只有明確標示為 fixture 的檔案才承諾可匯入；匯入後仍需重新綁定憑證、路徑與 Webhook。
- M1：Webhook hello-world（驗證 1.1 安裝完成）、Tunnel 測試流（驗證 1.2；依課前方案測試）
- M2：Optional Chaining 範例流、If/Switch 分支示例（以課堂逐步建置為主）
- M3：Manual Trigger + Read/Write Files from Disk 的 PDF 改名基線、定時彙整日報工作流（即時監控為延伸）
- M4：Google 表單遙控完整流、Make + n8n 雙引擎協作流、AI 計劃產出流、**M4-4 AI 秘書遷移完整流（11 節點 / 4 路分發 / 對應 Make 02_AI秘書_進階 scenario）**

### Setup Checklist（每單元前置）
- 需要哪些 credential（Google Drive / Google Sheets / OpenAI 等）
- 需要的環境變數
- 需要手動準備的測試檔案 / 資料夾

## 單元矩陣

### Module 1：環境建置與雲地橋接（預計 2.5h）

> M1 為環境基礎，最高優先順序，跑通才能進 M2-M4

- **CH1-1：n8n 本機環境建置（Docker Desktop）— 1h，拆 4 子單元**
  - **CH1-1-overview：參與門檻 Gate + 前置檢查（10–15m）** — 能依 OS、CPU 架構、RAM、磁碟、Windows BIOS/UEFI 虛擬化、WSL2、權限與 Docker smoke test 判定 PASS / CONDITIONAL / BLOCK，並提交課前環境證據
  - **CH1-1-install：Docker Desktop 安裝（25m）** — 能依 Mac Intel / Apple Silicon / Win + WSL2 對應路徑完成 Docker Desktop 安裝並驗證 `docker --version`
  - **CH1-1-launch：啟動 n8n 並完成首次設定（15m）** — 能用試跑包雙擊腳本啟動 n8n、開 localhost:5678、建管理者帳號、跑通 Webhook hello-world
  - **CH1-1-troubleshoot：常見錯誤排查手冊（10m）** — 能對照 8 大常見錯誤（埠衝突、Docker 沒開、WSL2、platform mismatch、權限、ERR_CONNECTION_REFUSED 等）自助修復，並知道卡死時要貼哪 3 行診斷給講師
- **CH1-2：Cloudflare Tunnel 設定 — 45m** — 能依課前核對的方案與安全條件設定 Cloudflare Tunnel，把本機 n8n Webhook 對外公開（含自動重啟、多 Hostname 管理）
- **CH1-3：JSON 完整入門 + Expression 語法 — 45m** — 能讀懂 n8n 介面的 JSON 樹狀結構、用 `{{ }}` Expression 引用上一節點資料

### Module 2：點名抓取法與複雜邏輯（預計 1.5h）

- **CH2-1：數據引用技巧（相對 / 絕對 / 動態）— 30m** — 能在多節點工作流中精準引用任一前序節點的特定欄位
- **CH2-2：Optional Chaining (`?.`) 與預設值 — 30m** — 能用 `?.` 處理可能缺失的巢狀欄位、避免 undefined 錯誤；能設計 fallback 預設值
- **CH2-3：If / Switch 邏輯判斷與分支 — 30m** — 能設計 If 雙分支與 Switch 多分支工作流，處理條件邏輯

### Module 3：重型文件工廠 — 批次處理大師（預計 2h）

> M3 是 n8n 相對 Make 的核心優勢區，本機檔案直接讀寫

- **CH3-1：資料夾檔案處理基線 — 40m** — 能用 Manual Trigger + Read/Write Files from Disk 讀取掛載資料夾、用 If 篩選 PDF；即時監控為延伸
- **CH3-2：PDF 批次改名 — 40m** — 能在檔案處理基線上加入 LLM 抽取內容與改檔名，處理多份 PDF；即時觸發需另行驗證
- **CH3-3：定時彙整日報（Schedule Trigger + Cron）— 40m** — 能設定 Schedule Trigger / Cron 排程，每日定時跑彙整與多格式輸出

### Module 4：綜合實戰 — 一站式行動辦公室（核心 2h；AI 秘書遷移另列 1.7h 選修）

> M4 是 Make + n8n 雲地協作的最終整合；AI 秘書遷移另列為進階選修

- **CH4-1：Google 表單遙控本機任務 — 40m** — 能用 Google 表單觸發 Make → 透過 Tunnel 打到本機 n8n → 跑批次任務 → 結果回傳
- **CH4-2：Make + n8n 雙引擎協作 — 40m** — 能規劃哪些步驟放 Make（雲端訊號）、哪些放 n8n（本機批次），並設計 API 介接（含 timeout 處理）
- **CH4-3：企劃草稿產出（AI + n8n + Markdown）— 40m** — 能組合 LLM、n8n 與本機 Markdown 檔案，從一個指令產出可閱讀的企劃草稿；Google Docs 為需另行授權的延伸
- **CH4-4：AI 秘書工作流：從 Make 遷移到 n8n（進階選修）— 100m** — 在另備複雜 Make AI 秘書 scenario 的前提下，能在 n8n 重建（Gmail Trigger + Aggregate + Gemini 4 區 JSON + Split Out + IF×4 並排路由 + TG/Email/Docs/HTTP + Continue On Fail），並對工作流每一步做威脅模型分析；不列為核心課程完成條件
  - **設計依據**：Codex L3 兩輪審核（CALL_ID 63c0b5f7 / 348da75a）的 P0-NEW 缺口
  - **教學重點**：Make ↔ n8n 對等度逐項對照（11 列）+ 4 大心智模型落差（資料形狀 / 分發 vs 分支 / JSON Parse / 錯誤處理）+ 威脅模型決策表
  - **學員 deliverable**：可帶走的 11 節點 n8n workflow JSON（`m4-4-ai-secretary-migration.json`）+ 機密 NDA 處理變體設計

---

## 與既有課程結構的相容性說明

- 既有 `courses/n8n/lessons/` 已用 `m1-1-*.html` 命名，與本系統推薦的 `CH1-1.html` 不同，本次轉軌**保留 m1-1 命名**避免大規模 rename 衝擊既有外部連結
- 1.1 拆 4 子單元後，舊 `m1-1-setup.html` 改為 Hub 入口頁（導向 4 子頁）
- 其餘 11 單元內容與啟動方式無關，本次**不重寫教案**，僅做全站「n8n Desktop」→「n8n 本機版」文案替換
