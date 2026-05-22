---
slug: gemini-notebooklm-workshop
name: Gemini × NotebookLM 跨部門 AI 工作坊
color: "#5a7a5a"
audience: 跨部門上班族（財務 / 業務 / 電商 / 倉儲 / 商品採購），零代碼，希望導入 AI 協助個人工作
institution: 弄一下工作室
duration: 8h
tools: Gemini（免費版）, NotebookLM（免費版）
prac: false
# === 課程製作團隊系統擴充欄位 ===
course_type: skill-operation
pilot: false
platform_version: 2026-Q2（Gemini 免費版 / NotebookLM 免費版）
related_course: office-ai-cases（同系列「指定雙工具版」，並行不衝突）
schedule: 2 天 × 4h（半日制）
maintenance_window: 3 個月（開課後）
codex_review: [24e13252]（L3 異質審核 actionable，7 建議全採納）
---

<!--
本檔由 course-pm skill 在「業主回覆 8 答」+「Codex L3 審查」之後產出。
上游 brief：_outlines/gemini-notebooklm-workshop.brief.md
下游：course-designer 寫教案 → course-lesson-writer 套 lesson-template-v3.html

本課特殊性：
1. 與 office-ai-cases（多平台不指派版）並行不衝突，本課**指定 Gemini + NotebookLM 雙工具**
2. 8h 切 2 天 × 4h，半日制節奏
3. 5 案例（4 共通 + 1 跨來源壓軸），每案例配 5 部門變體素材包（共 20 個變體 + 5 主版）
4. 不繳交、帶走素材包（30-40 課堂必用 prompts + 80+ 延伸庫）
5. 結訓 加「個人工作流改造卡」（每人 1 張，落實效果驗收）
6. 跨來源整合 = 跨部門協作的命名替換，占 9.4% < 15% 業主上限
7. 3 個月維護期 → 走完整 course-web-builder + course-lesson-writer pipeline
-->

## 課程定位（Positioning）

把 Gemini 與 NotebookLM **從「聽過但沒系統用過」變成「跨部門上班族能套進個人業務的雙工具工作流」**——
用 5 個案例（會議紀錄 / 文件查詢 / 競品標竿 / 數據簡報 / 跨來源彙報），8 小時內帶著 **30-40 套課堂 prompt + 5 份範例資料 + 5 部門變體素材 + 個人工作流改造卡** 回部門直接套用。

## 受眾畫像（Audience Profile）

- **職業**：跨部門代表（財務 / 業務 / 電商 / 倉儲 / 商品採購），業務數據導向
- **技術底子**：零代碼、Office 一般熟、ChatGPT 用過幾次但沒系統練過 Gemini / NotebookLM
- **現有工具棧**：Office 三件 + Gmail / Outlook + ERP / 電商平台後台（Shopify / 蝦皮 / momo 等）/ 採購系統 / WMS 倉儲系統 / CRM
- **資料現況**：日常處理的資料**多是從上述系統匯出的 CSV / Excel**，常含部門代碼、合併儲存格、空白列、欄位名稱不統一——**手上資料不一定乾淨**，sample dataset 要刻意做「有點髒」讓學員學會用 wrapper 清資料
- **痛點 3 條**：
  1. Gemini 跟 NotebookLM 都聽過但不知道「自己日常工作哪些場景該用誰」
  2. 試過 NotebookLM 但不會建好的知識庫、查詢結果不夠準
  3. 部門間共享資料時不知道哪些可以丟給 AI、哪些不行

## Brand Brief（品牌調性）

- **tone_register**：實作為主的工作坊，每案例「示範 → 上機 → 驗證」完整循環，不講概念散文
- **mood_keywords**：上機、案例、帶走、5 部門變體、個人工作流
- **differentiation**：與 office-ai-cases（6h 多平台不指派）區隔——本課 8h 指定雙工具、5 部門變體素材全備齊、**跨來源整合作為品牌線索從 CH0 貫穿到 CH2-1 壓軸**、3 個月可維護網頁講義

## 學習成果（Outcomes，6 條，動詞開頭、可驗證）

1. **能說出** Gemini 與 NotebookLM 的工作分流（生成 / 改寫 / 比較 vs 限定來源查詢 / 引用），並依個人業務場景選對工具
2. **能用** Gemini 把 30 分鐘會議逐字稿轉成決議卡、個人行動表、跟進信草稿（含 5-7 套 prompt 主 / 追問 / 驗證）
3. **能用** NotebookLM 建立部門專屬知識庫（20 份 SOP / 政策），跑 source-grounded 提問取得帶引用的查詢結果
4. **能用** Gemini 對 100+ 筆業務數據做分析、組裝成 6-8 頁可貼進簡報的內容包（不承諾直接生 .pptx）
5. **能在 45 分鐘內** 完成「NotebookLM 取證 3 份來源 → Gemini 整合 → 產出 1 頁可貼進簡報的內容包」完整工作流，並能指出兩工具切換時機（什麼資料丟哪個工具、結果如何驗證）
6. **能識別** AI 應用的資安紅線（哪些資料能丟 / 不能丟）與 5 種常見「以為 AI 會自己理解」失敗模式

## 前置知識依賴鏈（Prerequisite Chain）

```yaml
dependencies:
  CH0:   []                       # 開場 / 工具定位 / 資安
  CH1-1: [CH0]                    # 會議紀錄（Gemini 入門）
  CH1-2: [CH0]                    # 文件查詢（NotebookLM 入門）
  CH1-3: [CH0, CH1-1]             # 競品標竿：Gemini 進階
  CH1-4: [CH0, CH1-1, CH1-3]      # 數據簡報：壓軸，需前兩個 Gemini 熱身
  CH2-1: [CH1-2, CH1-4]           # 跨來源整合：NotebookLM 取證 + Gemini 整合
```

## 試跑包交付規格（Verification Assets）

本課為 **skill-operation** 類型 — 不繳交，但每案例必交付給學員帶走：

### 課堂必用包（每案例最低帶走項）

- 1 份主版 sample dataset
- **5 份部門變體 dataset**（財務 / 業務 / 電商 / 倉儲 / 採購）
- 5-7 套 prompt（主 / 追問 / 驗證）
- 1 份 AI 完整輸出範例（含每次略有差異 note）
- 1 張結果驗證卡（總筆數 / 加總金額 / 前三大 / 異常規則）
- 2 條 trouble-shooting（免費版限制下的常見卡點）

### 課後延伸模板庫（不在課堂消化、課後素材包附錄）

- 80+ 延伸 prompts（部門變體 prompt + bonus 場景）
- 個人工作流改造卡空白模板
- 雙工具速查表（單頁 A4）
- platform-guide.html（Gemini 免費版 vs NotebookLM 免費版能力速查）

## 單元矩陣（8h = 480 min，2 天 × 4h）

### Day 1（240 min · 工具入門 + 個人辦公兩案）

#### Part 0：開場（35 min · CH0）

- **CH0：工具定位 / 資安邊界 / 失敗實例 / 跨來源整合預告**（35 min）
  - Gemini 強項（生成 / 改寫 / 比較 / 數據摘要 / 工作草稿）
  - NotebookLM 強項（限定來源問答 / 多文件摘要 / 引用 / 降幻覺）
  - 工具切換決策 6 題（什麼場景用誰）
  - 5 個常見「我以為 AI 會自己理解」失敗示範
  - 資安紅線：哪些資料能丟 / 不能丟 / 課堂全用 sample data
  - **跨來源整合線索**（CH2-1 預告）：本課最後會做「兩工具聯動跨來源彙報」，前 4 個案例的成果都是壓軸的素材，從 Day 1 就埋鉤子

#### Part 1：Gemini 入門案例（70 min · CH1-1）

- **CH1-1：會議紀錄整理（Gemini）**
  - 主角：自己（剛開完跨部門會）
  - 主版素材：30 min 跨部門會議逐字稿 + 工作日誌 50 條
  - 5 部門變體：月底結帳檢討會 / 業務週會 / 電商月度檢討會 / 庫存盤點會議 / 供應商議價會議
  - 帶走：5-7 prompt + 決議卡 + 個人行動表 + 跟進信草稿
  - 結構：場景設定 5 → 講師示範 15 → Prompt 拆解 10 → 學員上機 35 → 驗證變奏 5

#### 中場休息（15 min）

#### Part 2：NotebookLM 入門案例（75 min · CH1-2）

- **CH1-2：公司文件智能查詢（NotebookLM）**
  - 主角：自己（手上有 20 份工作文件）
  - 主版素材：20 份 SOP / 政策 / 規範 PDF
  - 5 部門變體：會計政策 SOP / 業務手冊 / 平台規範 / 倉儲 SOP / 採購流程
  - 帶走：5-7 source-grounded prompt + 引用核對 checklist + 查詢卡
  - 結構：場景設定 5 → 知識庫建置示範 20 → source-grounded prompt 拆解 10 → 學員上機 35 → 驗證變奏 5

#### Day 1 收尾（5 min）

- Day 2 預告 + 帳號 / 上傳 troubleshoot 結算

#### Day 1 緩衝（40 min）

- Q&A / 上機卡關處理 / 環境補強

### Day 2（240 min · 進階應用 + 跨來源整合 + 結訓）

#### Day 2 開場（10 min）

- Day 1 工具熟練度回顧 + Day 2 路線圖

#### Part 3：Gemini 進階案例（75 min · CH1-3）

- **CH1-3：競品 / 標竿資料整理（Gemini + 來源核）**
  - 主角：自己（被指派做市調 / 標竿研究）
  - 主版素材：5 篇同業競品文章 + 3 段業界訪談
  - 5 部門變體：同業財報 / 客戶分析 / 平台競品 / 倉儲效率標竿 / 同業採購條件
  - 帶走：5-7 prompt + 來源檢核卡 + SWOT 模板 + 1 頁主管報告草稿
  - 結構：場景設定 5 → 講師示範 15 → Prompt 拆解 10 → 學員上機 40 → 驗證變奏 5

#### 中場休息（15 min）

#### Part 4：Gemini 壓軸主案例（80 min · CH1-4 · **本課最沒把握、最需要慎重設計的單元**）

- **CH1-4：數據快速分析 + 主管彙報組裝（Gemini 壓軸）**
  - 主角：自己（手上有 Excel 要做月報）
  - 主版素材：100 筆業績 + 50 SKU + 200 筆費用（**刻意做髒** — 含部門代碼、合併儲存格、空白列，貼近學員真實資料）
  - 5 部門變體：月度財報 / 業績達成 / 電商 SKU 矩陣 / 庫存週轉 / 採購績效
  - 帶走：5-7 prompt + 觀察重點清單 + 6-8 頁簡報內容包 + **「無投影片設計、只給內容」明確 template**
  - 簡報承諾邊界：「**可貼進簡報的內容包**」，不承諾「直接下載漂亮 .pptx」
  - 結構：
    - 場景設定（5 min）
    - 講師示範主版 + 5 部門變體 demo（20 min · 每個變體 ~3 min × 5 = 15 min + 主版串接 5 min）
    - Prompt 拆解（10 min · 含 Gemini 免費版 32K 限制下的分批貼資料 wrapper）
    - 學員上機（40 min · 每人選自己部門變體跑）
    - 驗證變奏（5 min）
  - trouble-shooting：免費版 Gemini 32K 上下文限制下 100 筆資料怎麼分批；合併儲存格 / 空白列 wrapper
  - **跨來源伏筆**：示範段末提示「下一個案例會把這個成果跟採購、業務的來源整合」

#### Part 5：跨來源整合壓軸（45 min · CH2-1 · 9.4% < 15%）

- **CH2-1：跨來源綜合彙報（NotebookLM 取證 + Gemini 整合）**
  - 情境：自己收到採購 + 業務 + 倉儲三份資料，要整理給主管的一頁綜合報告
  - 命名：「跨來源資料整合」（不是「跨部門協作共創」）
  - 主版素材：新品引進的綜合決策資料包（跨 3 部門）
  - 替代主版：月度業績檢討（財務 + 業務 + 電商）
  - 帶走：完整工作流範本（NotebookLM 取證 → Gemini 整合 → 簡報內容包）+ 跨來源責任分工卡
  - 結構：情境設定 5 → 兩工具聯動示範 15 → 學員上機 20 → 驗證 5

#### Part 6：結訓（15 min）

- **個人工作流改造卡 + 素材包導覽 + 課後維護期說明**
  - 每人完成 1 張「個人工作流改造卡」（≥ 1 個下週要試的場景，落實效果驗收）
  - 課後素材包導覽（延伸模板庫 80+ prompts / 5 部門變體 dataset / 雙工具速查表）
  - 3 個月維護邊界：工具介面變動 / 模板更新 → 設計師修網頁 → 業主發信通知

## 與既有 office-ai-cases 的差異對照

| 維度 | office-ai-cases（多平台版） | 本課 gemini-notebooklm-workshop（指定雙工具版） |
|------|------|------|
| 時數 | 6h 嚴控 | 8h（2 天 × 4h 半日制） |
| 受眾 | 業務 / 財務 / 電商 / 行政 / 主管（無行銷） | 財務 / 業務 / 電商 / 倉儲 / 採購（業務數據導向 5 部門） |
| 平台策略 | 多工具混搭、除 NotebookLM 外不指派 | **指定 Gemini + NotebookLM 雙工具** |
| 案例數 | 4（不含 CH0） | 5（不含 CH0） |
| 跨部門占比 | 無跨部門特化 | **CH2-1 跨來源整合 9.4%** |
| 部門變體 | 通用主版 | **5 部門變體素材全備齊（20 個變體 + 5 主版）** |
| 帶走包 | 56 prompts + 4 datasets | **30-40 課堂必用 + 80+ 延伸庫 + 25 份 dataset** |
| 結訓設計 | 56 prompts 帶走 + 課後實作建議 | **個人工作流改造卡（每人 1 張）+ 3 月維護** |
| 課後維護 | — | **3 個月內可修網頁、業主發信通知** |

## 品牌風格指引（與 design-tokens.md + 操作型講義.md 對齊）

- **禁用詞**：賦能 / 數位轉型 / 高效 / 痛點 / 您 / 我們（除引號講師話術）
- **改用**：做法 / 卡住的事 / 你
- **平台指派**：**本課指定 Gemini + NotebookLM，主案例 prompt 直接寫「在 Gemini」「在 NotebookLM」**（與 office-ai-cases 的「不指派」風格區別）
- **付費功能標記**：免費版限制要明寫，付費版（Gemini Advanced）僅在 trouble-shooting 段提及，標 💰
- **簡報承諾邊界**：「可貼進簡報的內容包」「可人工檢核改寫的初稿」，禁「自動生成可直接交付的報告」「直接下載 .pptx」
- **資安語氣**：明確紅線 + 課堂全用 sample data，不講「應該注意」

## G1 強制檢核結果（2026-05-22 通過）

| 題 | 使用者答 | 對應修訂 |
|---|---|---|
| Q1 最沒把握 | CH1-4 數據簡報壓軸 | CH1-4 結構拆細：5 部門變體 demo 時間分配（每變體 ~3 min × 5）、髒 dataset 設計、32K 分批 wrapper、跨來源伏筆、「無投影片設計只給內容」template |
| Q2 受眾對不上 | 「現有工具棧」需補充 | 補 ERP / 電商後台 / 採購系統 / WMS / CRM 與「資料現況」段（學員手上資料常是髒的 CSV / Excel），影響案例 sample dataset 設計風格 |
| Q3 最浮泛學習成果 | Outcome 5 兩工具工作流 | Outcome 5 改寫為「45 分鐘內完成 NotebookLM 取證 3 份 → Gemini 整合 → 1 頁簡報內容包 + 能指出切換時機」可驗證版 |
| Q4 與 office-ai-cases 差異 | 「跨來源整合是品牌錢幣但還不夠重」 | differentiation 加「跨來源整合作為品牌線索從 CH0 貫穿到 CH2-1 壓軸」；CH0 加跨來源預告埋鉤；CH1-4 示範段末加「下一案例會整合採購業務來源」過渡語 |

**G1 結論**：通過，可進 course-designer 階段。
