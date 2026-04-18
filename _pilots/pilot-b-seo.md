---
slug: pilot-b-seo
name: "[試飛 B] SEO 搜尋意圖四類型"
color: "#5a7a5a"
audience: 零基礎上班族，做數位行銷/內容但不懂 SEO 理論分類
institution: 弄一下工作室
duration: 1h
tools: Google 搜尋, Google Sheets
prac: false
# === 課程製作團隊系統擴充欄位 ===
course_type: concept
pilot: true
pilot_purpose: 驗證「概念理解型」課程（無操作步驟、靠案例與反思）是否適配 section-driven 模板
platform_version: Google Search 2026-Q2
---

<!--
試飛單元 B：以「SEO 搜尋意圖四類型」為案例，驗證 concept 類課程通過系統鏈路的能力。
觀察重點：
- Section 03/04 不是 step-by-step，而是案例分析 + 反思，新模板是否 graceful degrade
- 試跑包不是 JSON，是分類練習題答案，設計師是否正確填寫 spec
- 無操作步驟時，步驟 circles 是否正確省略
-->

## 課程定位（Positioning）

讓做數位行銷/內容的上班族在 1 小時內**能區辨 4 種搜尋意圖類型**，並從真實搜尋詞反推該寫哪一型的內容。學完不會讓你變 SEO 專家，但會讓你**不再把知識型關鍵字寫成商品頁**——這是內容 SEO 最常見的錯位問題。

## 受眾畫像（Audience Profile）

- **職業**：行銷專員 / 內容編輯 / 社群經理 / 業務助理
- **技術底子**：不會寫程式、不懂 GA / GSC 後台、但會用 Google 搜尋
- **現有工具棧**：Google 搜尋、ChatGPT、Canva、可能有 Google Ads 基礎
- **痛點 3 條**：
  1. 主管要求「做內容 SEO」，但不知道該寫什麼、寫了流量也沒進來
  2. 關鍵字工具給了一堆詞，不知道哪些值得寫、哪些寫了也沒人點
  3. 看過文章說「要寫對搜尋意圖」，但什麼是搜尋意圖？四種還是三種？沒人講清楚

## 學習成果（Outcomes，4 條）

1. **能**說出 4 種搜尋意圖類型的名稱（Informational / Navigational / Commercial Investigation / Transactional）並用一句話定義各自本質
2. **能**從 10 個真實搜尋詞中每個至少挑對 8 個分類（80% 正確率）
3. **能**解釋「同一關鍵字混合多意圖」時的判斷原則，並列出判斷該打哪一型的 2 個線索（SERP 觀察 + 搜尋動詞）
4. **能**為每種意圖類型說出 2 種具體內容格式（例：Informational → 教學長文 + 整理型清單文；Commercial Investigation → 比較表 + 使用者評論整理；Transactional → 產品頁 + 優惠碼 landing）

## 前置知識依賴鏈（Prerequisite Chain）

```yaml
dependencies:
  CH1-1: []  # 試飛只有 1 單元，無前置
```

## 試跑包交付規格（Verification Assets）

**類型**：concept

**⚠️ 給課程設計師 — 重構版定義**：

> concept 類的「試跑包」應該是一**組可讓學員自己模擬跑一次完整 SEO 意圖分析流程**的資產包。學員從這包東西拿到手開始：有原始 keyword list（像從工具匯出）→ 判斷意圖 → 驗證分類 → 推導內容策略。**不是題庫，是可自運行的迷你實戰**。

與 skill-operation 的 JSON 對應關係：
- skill-operation：workflow.json = 可匯入就能跑的流程
- concept：keyword-list.csv + 解答本 = 可「照包套跑一遍」的完整教學閉環

### 1. 模擬 Keyword List（檔名 `keyword-list.csv`）

10 個中文真實搜尋詞，**模擬從 Ahrefs / SEMrush / Google Keyword Planner 匯出的格式**，含搜尋量欄位增加臨場感。四類型各至少 2 個，並故意摻 2 個陷阱題（表面像 A 類、實際 B 類）。格式：

```csv
keyword,monthly_volume,difficulty
"n8n 是什麼",1200,32
"crm 比較 2026",880,45
"notion 教學",9500,52
...
```

### 2. 分類解答本（檔名 `classification-key.md`）

學員做完分類後開來對答案，**每題解答含 3 欄位**：預期分類 + 判斷線索 + 適合內容格式（呼應 Outcome 4）。範本：

```markdown
| 搜尋詞 | 預期分類 | 判斷線索 | 適合內容格式 |
|--------|---------|---------|------------|
| 「n8n 是什麼」 | Informational | 疑問動詞「是什麼」+ SERP 多為教學文 | 教學長文、概念速查 |
| 「crm 比較 2026」 | Commercial Investigation | 「比較」+ 年份顯示評估階段 | 比較表、使用者評論整理 |
```

### 3. 陷阱題解析（嵌入 `classification-key.md` 最後一節）

3 個學員通常分錯的真實案例，明示「表面像 X 類、實際應為 Y 類」+ 從 SERP 觀察如何得知。例：
- 「Notion 教學」看似 Informational，實為 Navigational — SERP 前 3 名都是 notion.com 官方

### 4. 內容策略輸出範本（檔名 `content-plan-template.md`）

空白範本讓學員完成分類後填入：

```markdown
| 搜尋詞 | 我的分類 | 對應內容格式 | 預計產出 |
|--------|---------|------------|---------|
| 「n8n 是什麼」 | Informational | 教學長文 | 一篇 1500 字入門文 |
| ... | ... | ... | ... |
```

學員填完這份 = 他已經**跑過一次從 keyword 到內容策略的完整流程**，模擬真實業務任務。

### 5. SERP 截圖樣本（選用 · 3 張）

3 個陷阱詞的 Google SERP 截圖，佐證「觀察 SERP 前 3 名判意圖」這條實務線索。

### 檔案擺放

```
_pilots/_trial-packs/pilot-b-seo/
  ├── keyword-list.csv              # 模擬工具匯出
  ├── classification-key.md         # 10 題解答 + 3 陷阱解析
  ├── content-plan-template.md      # 空白策略範本
  └── serp-samples/                 # 選用 SERP 截圖
      ├── trap-1-notion-教學.png
      ├── trap-2-xx.png
      └── trap-3-xx.png
```

## 單元矩陣

### Part 1：試飛（1h，僅 1 單元）

- **CH1-1：SEO 搜尋意圖四類型** — 能區辨 4 類型、從 10 個真實搜尋詞判斷分類（60 min）
