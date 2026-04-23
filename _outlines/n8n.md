---
slug: n8n
name: AI 資料工廠 — 大規模文件處理實戰
color: "#5a7a5a"
audience: 已熟 Make 基礎、想突破 1000 ops/月限制與本機檔案存取限制的自動化工作者
institution: 弄一下工作室
duration: 8h
tools: n8n (Community Edition self-host), Docker Desktop, Cloudflare Tunnel, Make
prac: false
# === 課程製作團隊系統擴充欄位 ===
course_type: skill-operation
pilot: false
platform_version: n8n latest (Docker image n8nio/n8n) / Docker Desktop / Cloudflare Tunnel free tier
---

<!--
本大綱於 2026-04-23 補建（既有課程已上線但無對應大綱）
觸發事件：n8n Desktop App 於 2025-08-15 由官方封存（read-only），原以「n8n Desktop」為主軸的 Module 1.1 安裝章節需轉軌
詳細執行計畫：~/.claude/plans/n8n-desktop-velvety-giraffe.md
-->

## 課程定位（Positioning）

教 Make 進階使用者用 n8n 本機版（Docker Desktop + Compose）補上 Make 做不到的兩件事：**無執行次數限制**與**本機檔案直接讀寫**；產出可立即套用的雲地協作自動化系統。

## 受眾畫像（Audience Profile）

- **職業**：行銷企劃、營運、知識工作者、小型工作室主理人
- **技術底子**：會用 Make、看得懂 JSON、敢開瀏覽器點 localhost；不需指令列基礎，但願意裝 Docker Desktop
- **現有工具棧**：Make（已碰到 ops 上限）、Google Workspace、ChatGPT/Claude 等 LLM
- **痛點 3 條**：
  1. Make 免費版 1,000 ops/月 不夠用，但又不想花錢升級
  2. 想自動處理本機資料夾裡的 PDF / 文件，Make 完全做不到
  3. 客戶資料 / 機密文件不想丟到第三方 SaaS 處理

## Brand Brief（品牌調性）

- **tone_register**：技術友善（清楚、實作導向，不端架子）
- **mood_keywords**：職人感、可靠、工廠秩序
- **differentiation**：與其他 AI 課程強調「概念」不同，本課程強調「自架基礎建設能力」— 學員會帶走一個跑在自己電腦上、可永久使用的 n8n 工作站，而不只是工具操作技巧

## 學習成果（Outcomes，動詞開頭、可驗證）

1. **能在自己電腦上完成 n8n 本機環境建置**（Docker Desktop + Compose、開到 localhost:5678 並完成首次設定）
2. **能設定 Cloudflare Tunnel 把本機 n8n Webhook 對外公開**，給雲端服務（如 Make）回打
3. **能用 Optional Chaining 與 If/Switch 節點**處理巢狀 JSON 與分支邏輯，避免 undefined 錯誤
4. **能設計 Watch Folder 工作流**監控本機資料夾、自動觸發批次處理（如 PDF 改名、文件彙整）
5. **能組合 Make 與 n8n 的雲地協作架構**，把雲端訊號（表單、Webhook）導到本機跑批次任務
6. **能診斷常見 n8n 自架環境錯誤**（埠衝突、Docker 沒開、權限問題、ERR_CONNECTION_REFUSED）並自助排除

## 環境風險聲明（必讀）

**n8n Desktop App 已退役**：n8n 官方自 2024 年起停止 Desktop App 開發，GitHub 倉庫 `n8n-io/n8n-desktop-app` 於 **2025-08-15 封存（read-only）**。本課程**不使用** Desktop App，改採官方推薦的 **Docker Desktop + Docker Compose** 方案 — 學員體驗仍是「桌面應用」（Docker Desktop 有 GUI），但 n8n 本身以容器形式跑在背景，啟動透過課程提供的一鍵腳本（`start.command` / `start.bat`）完成，不需學員手打 docker 指令。

**因應措施**：
- 1.1 安裝章節拆 4 子單元（overview / install / launch / troubleshoot），自助補課友善
- 提供 `n8n-starter-kit` 試跑包（compose YAML + 各平台一鍵腳本 + .env 範本 + README）
- troubleshoot 子頁專處理 8 大常見錯誤（埠衝突、WSL2、Apple Silicon platform、權限等）

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
  CH3-1: [CH1-1-launch, CH2-3]    # Watch Folder 需要環境 + 邏輯
  CH3-2: [CH3-1]                  # PDF 批次建立在 Watch Folder 之上
  CH3-3: [CH2-3]                  # 定時彙整需要邏輯但不需要 Watch
  CH4-1: [CH1-2, CH2-1]           # Google 表單遙控需要 Tunnel + 引用
  CH4-2: [CH4-1]                  # Make+n8n 雙引擎延伸自表單遙控
  CH4-3: [CH4-2, CH3-2]           # 全自動企劃整合所有
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

### 各單元工作流匯出（每單元 1 個 .json）
- M1：Webhook hello-world（驗證 1.1 安裝完成）、Tunnel 測試流（驗證 1.2）
- M2：Optional Chaining 範例流、If/Switch 分支示例
- M3：Watch Folder + PDF 改名工作流、定時彙整日報工作流
- M4：Google 表單遙控完整流、Make + n8n 雙引擎協作流、全自動企劃產出流

### Setup Checklist（每單元前置）
- 需要哪些 credential（Google Drive / Google Sheets / OpenAI 等）
- 需要的環境變數
- 需要手動準備的測試檔案 / 資料夾

## 單元矩陣

### Module 1：環境建置與雲地橋接（預計 2.5h）

> M1 為環境基礎，最高優先順序，跑通才能進 M2-M4

- **CH1-1：n8n 本機環境建置（Docker Desktop）— 1h，拆 4 子單元**
  - **CH1-1-overview：流程總覽 + 前置檢查（10m）** — 能說明本課程為何用 Docker、檢查自己環境是否符合（OS / 磁碟 / CPU 架構）
  - **CH1-1-install：Docker Desktop 安裝（25m）** — 能依 Mac Intel / Apple Silicon / Win + WSL2 對應路徑完成 Docker Desktop 安裝並驗證 `docker --version`
  - **CH1-1-launch：啟動 n8n 並完成首次設定（15m）** — 能用試跑包雙擊腳本啟動 n8n、開 localhost:5678、建管理者帳號、跑通 Webhook hello-world
  - **CH1-1-troubleshoot：常見錯誤排查手冊（10m）** — 能對照 8 大常見錯誤（埠衝突、Docker 沒開、WSL2、platform mismatch、權限、ERR_CONNECTION_REFUSED 等）自助修復，並知道卡死時要貼哪 3 行診斷給講師
- **CH1-2：Cloudflare Tunnel 設定 — 45m** — 能設定免費 Cloudflare Tunnel 把本機 n8n Webhook 對外公開（含自動重啟、多 Hostname 管理）
- **CH1-3：JSON 完整入門 + Expression 語法 — 45m** — 能讀懂 n8n 介面的 JSON 樹狀結構、用 `{{ }}` Expression 引用上一節點資料

### Module 2：點名抓取法與複雜邏輯（預計 1.5h）

- **CH2-1：數據引用技巧（相對 / 絕對 / 動態）— 30m** — 能在多節點工作流中精準引用任一前序節點的特定欄位
- **CH2-2：Optional Chaining (`?.`) 與預設值 — 30m** — 能用 `?.` 處理可能缺失的巢狀欄位、避免 undefined 錯誤；能設計 fallback 預設值
- **CH2-3：If / Switch 邏輯判斷與分支 — 30m** — 能設計 If 雙分支與 Switch 多分支工作流，處理條件邏輯

### Module 3：重型文件工廠 — 批次處理大師（預計 2h）

> M3 是 n8n 相對 Make 的核心優勢區，本機檔案直接讀寫

- **CH3-1：資料夾監控（Watch Folder）— 40m** — 能設計 Watch Folder 工作流，監控本機資料夾、新檔案落地立刻觸發處理
- **CH3-2：PDF 批次改名 — 40m** — 能組合 Watch Folder + LLM 抽取內容 + 改檔名，處理大量 PDF 自動歸檔
- **CH3-3：定時彙整日報（Schedule Trigger + Cron）— 40m** — 能設定 Schedule Trigger / Cron 排程，每日定時跑彙整與多格式輸出

### Module 4：綜合實戰 — 一站式行動辦公室（預計 2h）

> M4 是 Make + n8n 雲地協作的最終整合

- **CH4-1：Google 表單遙控本機任務 — 40m** — 能用 Google 表單觸發 Make → 透過 Tunnel 打到本機 n8n → 跑批次任務 → 結果回傳
- **CH4-2：Make + n8n 雙引擎協作 — 40m** — 能規劃哪些步驟放 Make（雲端訊號）、哪些放 n8n（本機批次），並設計 API 介接（含 timeout 處理）
- **CH4-3：全自動企劃產出（AI + n8n + Docs）— 40m** — 能組合 LLM、n8n、Google Docs 模板，從一個指令產出完整企劃文件

---

## 與既有課程結構的相容性說明

- 既有 `courses/n8n/lessons/` 已用 `m1-1-*.html` 命名，與本系統推薦的 `CH1-1.html` 不同，本次轉軌**保留 m1-1 命名**避免大規模 rename 衝擊既有外部連結
- 1.1 拆 4 子單元後，舊 `m1-1-setup.html` 改為 Hub 入口頁（導向 4 子頁）
- 其餘 11 單元內容與啟動方式無關，本次**不重寫教案**，僅做全站「n8n Desktop」→「n8n 本機版」文案替換
