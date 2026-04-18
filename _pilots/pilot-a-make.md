---
slug: pilot-a-make
name: "[試飛 A] Make 定時抓網頁"
color: "#8a7a9e"
audience: 零基礎上班族，需每天/每週做重複性網頁資料整理
institution: 弄一下工作室
duration: 1h
tools: Make.com
prac: false
# === 課程製作團隊系統擴充欄位 ===
course_type: skill-operation
pilot: true
pilot_purpose: 驗證「技能操作型」課程在課程製作團隊系統中的通過性
platform_version: Make.com 2026-04
---

<!--
試飛單元 A：以 Make.com 定時抓網頁為案例，驗證 skill-operation 類課程能否順利通過 PM → 設計師 → 講義 → 檢核 四角色鏈。
產出後，檢視：
- 教案結構是否塞得下「觸發器 + HTTP + Sheets 寫入」這種 3-module 的 scenario
- 講義 HTML 的 step-by-step 區塊是否適配
- 試跑包需求（scenario JSON + OAuth setup）是否被設計師正確列出
-->

## 課程定位（Positioning）

讓零基礎上班族在 1 小時內從不懂 Make.com，到**能自行用定時觸發器 + HTTP/RSS 模組，把外部網頁資料每日同步到 Google Sheets**。不求能做複雜整合，求能獨立搞定「定時抓一個網頁、把結果存起來」。

## 受眾畫像（Audience Profile）

- **職業**：行銷專員 / 助理 / 業助 / 內容編輯
- **技術底子**：會用 Gmail、Sheets、Notion，不會寫程式，沒用過 API，聽過「自動化」但沒實作過
- **現有工具棧**：Gmail、Google Sheets、Notion、Chrome（基本而已）
- **痛點 3 條**：
  1. 每天/每週要去特定網站看有沒有更新（新聞、競品官網、招標公告），累人且常忘記
  2. 看到新內容還要手動複製到 Sheets 做紀錄或分類，容易漏掉
  3. 想自動化但 coding 門檻太高，找免費工具又怕學了沒用

## 學習成果（Outcomes，4 條）

1. **能**在紙上/白板畫出 Scenario/Module/Trigger/Connection 四個概念的層級關係圖（Scenario 包 Module、Trigger 是 Module 之一、Connection 綁定外部帳號、並標出哪個概念屬於「帳號級」哪個屬於「流程級」）
2. **能**獨立建立一個「每日 09:00 自動觸發」的 Scenario，並**在 Make 畫面上看到下一次預定執行時間**
3. **能**串接 HTTP 或 RSS Module 從外部網頁抓取資料，並從 Make 的 Output Bundle panel **指出至少 3 個可使用的欄位名稱**
4. **能**把抓到的資料寫入 Google Sheets 指定工作表，**在 Sheet 中親眼看到新增的一列**

## 前置知識依賴鏈（Prerequisite Chain）

```yaml
dependencies:
  CH1-1: []  # 試飛只有 1 單元，無前置
```

## 試跑包交付規格（Verification Assets）

**類型**：skill-operation

**⚠️ 給課程設計師：這個區塊要寫到「使用者照這清單就能在 Make 介面產出 JSON」的具體度。不可用「需要 Gmail OAuth」這種抽象敘述，要用「需要 XXX 模組、YYY 欄位填 ZZZ」這種可執行度。**

每單元提供：

### 1. Scenario 匯出 JSON（檔名 `pilot-a-make.blueprint.json`）

完整可匯入的 Make blueprint，**必含以下 3 個 Module 依序**：

| # | Module 類型 | Module ID | 關鍵參數 | 可變欄位 |
|---|-----------|----------|---------|---------|
| 1 | Schedule / Every Day | `builtin:BasicTrigger` | `scheduling.type: "every"`、`scheduling.interval: 1440`（分鐘，= 1 天）| 時間點 |
| 2 | HTTP > Make a request / RSS > Retrieve RSS feed items | `http:ActionMakeApiRequest` 或 `rss:TriggerNewFeedItem` | `url` = RSS 目標 URL、`method: GET` | URL |
| 3 | Google Sheets > Add a Row | `google-sheets:addRow` | `spreadsheetId`、`sheetName`、`values[0..n]` 綁前一 module 輸出 | Sheet ID |

### 2. Setup Checklist（檔名 `setup.md`）

- **Make.com 帳號**：Free Plan（1,000 ops/month 足夠反覆試玩這個 pilot ~100 次）
- **Google 帳號 Connection**：
  - 在 Make 建立 Connection 時選「Google Sheets」
  - OAuth scope 必須包含：`https://www.googleapis.com/auth/spreadsheets`、`https://www.googleapis.com/auth/drive.file`
  - Connection 名稱建議：`gsheets-pilot`
- **目標 Google Sheet**：
  - 學員需先手動建一個 Sheet，命名 `Make 抓取紀錄`
  - 第一列（表頭）固定為：`抓取時間` / `標題` / `連結` / `摘要`
  - **把該 Sheet 的 URL 貼進設定**（spreadsheetId 從 URL 擷取）
- **目標網頁 RSS URL**：
  - 預設：`https://feeds.bbci.co.uk/news/rss.xml`（BBC News，穩定公開）
  - 備案：`https://news.google.com/rss`（若 BBC 被擋）

### 3. 範例資料

- **預期結果截圖**：`expected-result.png`，顯示 Sheet 中 3–5 筆成功抓取的資料列
- **錯誤樣貌截圖**：`common-errors.png`，顯示 RSS URL 打錯時 Make 的錯誤訊息長什麼樣

### 4. 試跑包產出流程（給使用者）

1. 在 Make.com 手動建立 Scenario（依講義步驟）
2. 試跑執行一次、確認 Sheet 有新列
3. Scenario 頁面右上 `...` → Export Blueprint → 儲存為 `pilot-a-make.blueprint.json`
4. 把 JSON 放進 `_pilots/_trial-packs/pilot-a-make/` 資料夾
5. 把截圖與 setup.md 一起放進同資料夾

## 單元矩陣

### Part 1：試飛（1h，僅 1 單元）

- **CH1-1：Make 定時抓網頁入門** — 能建立一個定時觸發 + HTTP 抓 RSS + 寫 Sheets 的完整 scenario（60 min）
