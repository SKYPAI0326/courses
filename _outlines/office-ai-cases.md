---
slug: office-ai-cases
name: 辦公室 AI 工具案例應用
color: "#c9963a"
audience: 多部門上班族（業務 / 財務 / 電商 / 行政 / 主管），無程式背景，**無行銷部門**
institution: 弄一下工作室
duration: 6h
tools: ChatGPT, Gemini, Copilot, NotebookLM, Claude（皆免費版可跑、僅 NotebookLM 為指定工具）
prac: false
# === 課程製作團隊系統擴充欄位 ===
course_type: skill-operation
pilot: false
platform_version: 2026-05（ChatGPT GPT-5.5 free / Gemini 32K free / Copilot Edge free / NotebookLM free / Claude.ai free）
related_course: office-ai（既有「辦公室 AI 工具實務應用」並行不衝突）
codex_review: [570b65c1, 104f4c30]（兩輪 L3 異質審核 accepted）
---

<!--
本檔由 PM skill 在 Codex L3 兩輪審核（570b65c1 + 104f4c30，總體 8.5/10）後產出。
下游：course-designer 寫教案、course-lesson-writer 套 lesson-template-v3.html。

本課特殊性：
1. 與既有 office-ai 並行不影響（不修改既有任何一個字）
2. 大量上機演練 + 不繳交 + 帶走完整提示詞庫 (56 套) + 4 sample datasets
3. 教「通用 prompt + 平台 wrapper」（除 NotebookLM 外不指定平台）
4. 簡報承諾邊界：「6-8 頁可貼進簡報的內容包」，不承諾「直接下載漂亮 .pptx」
-->

## 課程定位（Positioning）

這門課把生成式 AI **從「會聊天」變成「會解決部門日常工作」**——
用 4 個跨部門共通的真實案例（週報 / 業務財務 / 電商銷售 / 數據簡報組裝），
讓學員 6 小時內帶著 **56 套提示詞 + 4 份 sample 資料 + 完整 AI 輸出範例** 回辦公室直接套用。

## 受眾畫像（Audience Profile）

- **職業**：多部門混合（業務 / 財務 / 電商 / 行政 / 主管），**無行銷部門**
- **技術底子**：零代碼、Office 一般熟、AI 工具用過但沒系統練過
- **現有工具棧**：Office 三件 + Gmail / Outlook + 各家 ERP/CRM 後台
- **痛點 3 條**：
  1. AI 工具知道有但不知怎麼跑「自己部門的真實任務」
  2. 試過 ChatGPT 但結果太籠統、不能直接拿來交差
  3. 不知哪些功能要付費、怕踩到機密外洩風險

## Brand Brief（品牌調性）

- **tone_register**：實作為主、不講概念（與既有 office-ai 的「綜合通用版」區隔）
- **mood_keywords**：上機、案例、帶走、零繳交
- **differentiation**：既有 office-ai 6h 是「綜合 5 Parts 含行銷」、本課 6h 是「4 部門案例 + 帶走素材包 + 通用 prompt」

## 學習成果（Outcomes，4 條，動詞開頭、可驗證）

1. **能說出**生成式 AI 運作機制（Token / Context / Hallucination）與 Prompt Engineering 5 個常見失敗
2. **能寫出**通用 prompt 5 大骨架（角色 / 資料 / 任務 / 輸出 / 驗證），並依平台限制加 wrapper
3. **能跑出** 4 個部門案例的完整成果（週報 / 業務財務分析 / 電商商品分析 / 數據簡報內容包）
4. **能驗證** AI 結果（每案例「結果驗證卡」：總筆數 / 加總金額 / 前三大 / 異常規則）

## 前置知識依賴鏈（Prerequisite Chain）

```yaml
dependencies:
  CH0: []
  CH1-1: [CH0]                # 週報需先懂 prompt 骨架
  CH1-2: [CH0, CH1-1]         # 業務財務需先熱身過週報
  CH2-1: [CH0, CH1-2]         # 電商承接表格分析
  CH2-2: [CH1-1, CH1-2, CH2-1]  # 簡報組裝需前 3 案例的投影片素材
```

## 試跑包交付規格（Verification Assets）

本課為 **skill-operation** 類型 — 不繳交，但每案例必交付給學員帶走：

每案例最低帶走項：
- 1 份 sample CSV / TXT（30-500 筆）
- 7 套 prompt（3 主 + 3 變奏 + 1 風險檢查）
- 1 份完整 AI 輸出範例
- 2 條 trouble-shooting
- 1 張結果驗證卡（總筆數 / 加總金額 / 前三大 / 異常規則）
- 3 行平台差異備註
- 3 張投影片素材（給壓軸案例 ④ 組裝）

額外 bonus（放 prompt-library.html）：
- 9 套 bonus prompts（防呆追問 4 + 對象變奏 4 + wrapper 2）
- 5 套 NotebookLM 專用 prompt
- 1 份 NotebookLM 示範用「假公司知識庫 3 份文件」

## 單元矩陣（6h = 360 min）

### Block 0：開場（30 min · CH0）

- **CH0：AI 運作機制 + Prompt Engineering + 風險瑕疵**（30 min）
  - Token / Context / 為何 hallucination
  - 5 個常見 Prompt 失敗示範
  - 風險：機密外洩 / 過時資料 / 偏見 / 幻覺
  - 平台差異 5 min 帶過（不指派、課堂中性介紹）

### Block 1：通用週報案例（75 min · CH1-1）

- **CH1-1：週報生成（基礎熱身）**
  - 場景設定（5）→ 講師示範多平台對比（15）→ Prompt 拆解（10）→ 學員上機（40）→ 結果驗證 + 變奏（5）
  - 素材包：work-log-5day.txt（5 天 × 10 條 = 50 條）+ 7 prompts + AI 輸出範例 3 種平台對比
  - 產出：1 張投影片素材「本週重點摘要」

### Block 2：業務+財務雙合案例（75 min · CH1-2）

- **CH1-2：行程規劃 + 業績分析 + 費用異常偵測（表格分析 1）**
  - 子場景 A：拜訪行程規劃（25 min）
  - 子場景 B：業績報表分析（25 min）
  - 子場景 C：費用異常偵測（25 min）
  - 素材包：visit-30.csv + sales-50.csv + expense-200.csv（含異常埋點 5-10 筆）+ 21 prompts
  - 產出：3 張投影片素材「行程 / 業績趨勢 / 異常清單」

### Block 3：電商銷售案例（75 min · CH2-1）

- **CH2-1：電商銷售商品分析（表格分析 2）**
  - 場景設定（5）→ 示範（15）→ 拆解（10）→ 上機（40）→ 驗證變奏（5）
  - 素材包：ecom-orders-500.csv + sku-50.csv（含 ABC 分布 / 長尾 / 季節性）+ 7 prompts
  - 產出：3 張投影片素材「商品矩陣 / Top SKU / 推薦清單」

### Block 4：AI 數據簡報組裝案例（75 min · CH2-2）

- **CH2-2：AI 數據分析簡報組裝（壓軸）**
  - 用前 3 案例（CH1-1 / CH1-2 / CH2-1）累積的 7 張投影片素材 → 組成 5-8 頁完整簡報
  - 簡報承諾邊界：**「可貼進簡報的內容包」**，不承諾「直接下載漂亮 .pptx」
  - 素材包：slides-template.md + 7 prompts（結構 + 圖表 + 自動生 slides wrapper）

### Block 5：收尾（30 min）

- **Q&A + 素材包帶走清單 + 結訓**
  - 56 prompts 帶走清單
  - 4 datasets + 7+ AI 輸出範例帶走
  - platform-guide.html 速查表
  - 課後第一週實作建議

## 與既有 office-ai 的差異對照（招生頁可用）

| 維度 | 既有 office-ai（實務應用） | 本課 office-ai-cases（案例應用） |
|------|-------------------------|------------------------------|
| 時數 | 6h+（含行銷 Part 5） | 6h 嚴控（無行銷） |
| 受眾 | 含行銷部門 | 業務 / 財務 / 電商 / 行政 / 主管 |
| 教學風格 | 通用文書 + 會議 + 三職業特化 | 4 部門案例 + 帶走素材包 |
| 主課產出 | 個人 AI 工作流 | 4 案例完整輸出（含簡報內容包） |
| 平台策略 | 多工具混搭 | 通用 prompt + Wrapper（除 NotebookLM） |
| 提示詞數量 | 課堂示範用 | **56 套打包帶走** |
| Sample datasets | — | **4 份 800+ 筆真實感資料** |
| 課後繳交 | 有 PRAC1-4 | **不繳交、改為帶走** |

## 品牌風格指引（與 style-guide.md 對齊）

- 不要用「賦能 / 數位轉型 / 高效」等空氣詞
- 不要寫「您」、用「你」
- 不可承諾「直接下載漂亮 .pptx」、改「6-8 頁可貼進簡報內容包」
- 不可在主案例（除 NotebookLM bonus）寫「請用 ChatGPT」「請用 Gemini」這類指派
- 平台付費功能必須加 💰 標記
