---
unit_id: post-llm-6-walkthrough
title: Walkthrough — 把 #02 改成處理發票
course: n8n / AI 資料工廠
chapter: 第 6 章 / 8（post-llm 系列：課後用 LLM 改 workflow）
description: 完整 LLM 對話劇本，從零跟讀到通，含 4 個故意岔路示範學員會踩的雷
audience: 商業培訓非工程師、課後用網頁版 LLM（ChatGPT / Claude / Gemini）改 workflow
prerequisite: 已跑過 Lite Pack 14 個 workflow 至少 1 次；理解 #02 PDF AI 改名範例
delivery: 文字導向 HTML 章節（無印風）
created: 2026-05-07
codex_audit: f1cbc6ff
codex_verdict: actionable（已修補）
last_updated: 2026-05-07
---

# Walkthrough — 把 #02 改成處理發票

> **本章重設計教案** · 對應 `courses/n8n/lessons/post-llm-6-walkthrough.html`

## 重設計內容

## 第 6 章重設計：發票 walkthrough（核心交付，銜接 Phase C）

> **重要說明**：第 6 章的詳細 LLM 對話實寫見下方 [Phase C 章節](#phase-c)。本節給「教學設計層」的 8 點規格，Phase C 給「實機可貼可跑」的對話劇本。

### 1. 學員此時的痛點

學員到第 6 章是整個系列「最重」的一頁。心理狀態兩種：

- **路線 A**：第 1-5 章順著看下來，到第 6 章想看「我學的東西實際操作長什麼樣」
- **路線 B**：跳讀模式，直接從第 1 章 timeline Story A 跳過來，沒看 2-5 章

**這章必須能讓路線 B 也讀得通**（不能依賴前 5 章的概念）。心裡的話：

- **我現在要把 #02 改成處理發票，第一步該打開什麼？**
- **每個對話 turn 我要打什麼字？打完 LLM 會回什麼？**
- **如果 LLM 回的跟你寫的不一樣，我要怎麼調？**
- **跑通的瞬間我會看到什麼？跑失敗會看到什麼訊息？**

### 2. 核心要傳遞的 1 個觀念

**「我可以了」拐點 = 完整看完一次別人怎麼從零跑到 200 張發票自動歸檔。看到對話 turn 的真實樣貌 → 看到 n8n UI 真實畫面 → 看到 Finder 真實結果。看完後學員的內在改變：「原來這套流程實際做下來是這個感覺」。**

### 3. 具體 step-by-step

完整劇本見 Phase C。本節列**章內結構**（10 節），每節對應 Phase C 一個對話劇場：

1. **設定情境（5 分鐘讀）**：行銷企劃 A 的工作背景 + 200 張發票任務 + 為什麼選 #02 為基底
2. **步驟 1 拆需求（10 分鐘讀+寫）**：A 填 4 格便箋 → 對同事講 → 補一格 → 過關
3. **步驟 2 讀 JSON（5 分鐘讀+5 分鐘做）**：n8n UI export → 4 字串搜尋 → 貼模板 2 → LLM 回節點清單 → A 對照確認
4. **步驟 3 限定範圍（10 分鐘讀+10 分鐘做）**：A 圈出要改的節點（只動 Code）→ 備份 → 貼模板 3 → LLM 第 1 輪回**整份**（反例）→ A 用追問模板 → LLM 回單節點區段 → A 替換到 n8n UI
5. **步驟 4 匯入測試（10 分鐘讀+5 分鐘做）**：Duplicate → 確認 OFF → 放 1 張測試 PDF → Execute → 紅燈或綠燈
6. **步驟 5 錯誤回報（劇情高潮，15 分鐘讀+10 分鐘做）**：發現 newFilename 是「null_null」→ 找紅燈節點 → 複製三件套（錯誤訊息+input+parameter）→ 貼模板 4 → LLM 第 1 輪「精準診斷」回應 → A 替換 → 重跑通過
7. **步驟 6 收斂（10 分鐘讀+15 分鐘做）**：1 張通過 → 換 10 張不同供應商 → 9 張過 1 張稅後合計 0（退款單）→ A 決定不改流程，記備注 → LLM 主動建議加 try/catch（**示範拒絕**）→ A 用模板 5 拒絕
8. **驗收交付（5 分鐘讀+1 小時做）**：200 張全量跑 → Finder 確認 → workflow 改名為 v1.0 + archive 原版
9. **回顧：6 步流程在這個案例上的時間分配**：拆需求 15 / 讀 JSON 10 / 限定範圍 20 / 測試 5 / 錯誤回報 10 / 收斂 + 全量 25 = 約 85 分鐘（A 第一次走，預期 60-90 分鐘）
10. **彩蛋：A 的便箋備注怎麼存**：在 n8n workflow 描述欄、便利貼、團隊文檔三選一

### 4-7. Prompt 模板 + sample LLM 回應 + 驗收 + 錯誤

完整內容見 Phase C 對話劇本（每個 step 都有：學員真實 prompt + LLM 真實 sample 回應 + 驗收訊號 + 常見岔路）。

### 8. 回到課程動線

- **章末「我跑完了」**：→ 第 8 章自我驗收（5 條對照 + 進階 2 題）
- **章末「我卡在 X 步」**：→ 第 7 章錯誤分流
- **章末「我想再改別的 workflow」**：→ 第 8 章進階練習 1（#04 改 Notion）+ 進階練習 2（#11 改評分維度）

### 9. 對現有 HTML 的具體變更

| 動作 | 原 line | 改成 |
|---|---|---|
| 砍掉 | 528-534「對製作者的提醒」整段 | 移到本檔 _local，HTML 不放 maintainer note |
| 改寫 | 293-295 步驟 2 LLM 對話 placeholder | 用 Phase C step 3 的對話劇場替換 |
| 改寫 | 351-365 步驟 3 對話 placeholder（兩段） | 用 Phase C step 4 的對話劇場替換（含整份反例 + 追問 + 區段成功） |
| 改寫 | 454-456 步驟 5 對話 placeholder | 用 Phase C step 6 的對話劇場替換 |
| 改寫 | 482-484 步驟 6 try/catch 拒絕 placeholder | 用 Phase C step 7 的對話劇場替換 |
| 保留 | 165-209 為什麼選 #02 對照表 | 內容合理，保留 |
| 保留 | 215-227 設定情境（A 的故事） | 內容合理，保留，但 line 224 之後可加一句 anchor「這個故事 = Story A，第 1 章 timeline 第 1 個」 |
| 改寫 | 截圖 placeholder（11 個 `[需截圖：]`） | 標 `[實機需錄：圖 N — XX 畫面]`，保留為「待補入清單」但**不算空話**（Phase C 改寫對話本身已足夠讓學員照做） |
| 新增 | 章末（取代 528 maintainer note） | 加「6 步時間分配回顧」表 + 「彩蛋：備注怎麼存」3 選 1 動線 |

> **截圖佔位符的處理判斷**：使用者 brief 沒明確要求消除截圖 placeholder，且我沒有實機跑，截圖必須現場錄。但**對話的 placeholder 可以由我寫 sample**（這是教學設計層的工作，不是錄製層）。Phase C 把對話實寫出來，截圖 placeholder 保留，並在每個截圖位置寫一行「在等截圖期間，學員照對話劇本+文字描述也能照做」。


---

---

## Phase C — 完整對話劇本（教學重點）

本章核心交付。以下劇本詳細展示 A 用 ChatGPT 改 #02 的完整對話流程，含 4 個故意岔路與精準 vs 模糊 LLM 回應對照表。HTML 章節以此為主體呈現。

## Phase C — Walkthrough 章對話劇本（第 6 章核心交付）

### 設計目標

- **每個 LLM turn 寫真實樣的 prompt 字串 + 真實樣的 LLM 回應**（學員可直接對照）
- **故意安排 4 個岔路**：步驟 3 LLM 第 1 輪給整份（學員需追問）、步驟 4 跑出 null_null（劇情錯誤）、步驟 5 LLM 給「精準」回應（區別於模糊型）、步驟 6 LLM 在某些情境下會主動加 try/catch（示範學員怎麼拒絕擴張，不一定每次都會發生）
- **每 turn 配「下一步該做什麼判斷」標註**

### 主角設定（保留原 HTML 設定，加 anchor）

- **行銷企劃 A**（對應第 1 章 timeline Story A）
- 結業 3 週，今天上午接到主管轉信：每月 200 張供應商發票要按 `/檔案/2026/發票/{月份}/{供應商名}_{稅後金額}.pdf` 歸檔
- 手邊有：n8n self-host（Docker Desktop），#02-pdf-ai-rename 已跑通合約版本
- 手邊還沒有 200 張，但有 1 張上週收到的測試發票
- 用網頁版 ChatGPT，沒有 Claude Code

### 開場：A 在 ChatGPT 開新對話視窗

A 在 ChatGPT 上點「New Chat」開新視窗。她先打基底 prompt（環境感知 prefix）：

```
我用 n8n self-host (Docker Desktop)，n8n 版本 latest。
我要把 #02-pdf-ai-rename workflow（合約改名版）改成處理供應商發票，
每月 200 張，要產出 {YYYYMMDD}_發票_{賣方名}_{稅後合計}.pdf 檔名格式。
我會貼模板和 JSON 給你，請以結果為主、不解釋原理。
你準備好了嗎？

ChatGPT 預期回（sample）：
好的，我準備好了。請貼第一個任務的內容，我會以結果為主，不寫程式碼解釋。
```

> **這個開場 turn 的價值**：把環境（self-host Docker）、目的（200 張發票）、語氣（不解釋原理）一次傳給 LLM。後面每個 turn 都不用重述。

---

### Step 1：拆需求（A 自己填便箋，不對 LLM）

A 打開 macOS 的 Notes app，建一條新筆記，貼上 4 格範本。她邊看 #02 的 Code 節點 prompt（看到「甲乙方+合約金額+簽訂日」字樣）邊填。10 分鐘後，4 格內容如下：

```
【4 格便箋 — 把 #02 改成處理發票】

1. 原 workflow 編號
   #02-pdf-ai-rename（v0.6 合約版）
   目前 prompt 抓：甲乙方、合約金額、簽訂日

2. 目標 input
   供應商發票 PDF（每月 200 張，目前手邊先 1 張測試）
   來源資料夾：/files/pdf-inbox/
   每張 PDF 含：
   - 賣方公司全名（PDF 上中文寫「賣方」）
   - 統編（8 碼）
   - 品項清單（多行）
   - 稅後合計（PDF 上寫「稅後合計」，含元字）
   - 發票日期（YYYY/MM/DD）

3. 目標 output
   改名後 PDF，命名格式：
   {YYYYMMDD}_發票_{賣方名}_{稅後合計}.pdf
   例：20260506_發票_弄一下工作室股份有限公司_15750.pdf
   存到：/files/pdf-renamed/2026/{月份}/

4. 必保留的節點
   Manual Trigger（保留）
   Read PDF（保留）
   Extract PDF Text（保留）
   Write 改名輸出（保留路徑邏輯）
   只改：Code: AI 改名 節點裡的 prompt 字串 + 檔名 template
```

A 把這 4 格唸給隔壁工位的 B 聽，1 分鐘內講完。B 問：

> 「賣方公司全名要不要去掉『股份有限公司』後綴？」

A 想了 5 秒，回到便箋第 2 格補一行：

```
- 賣方公司全名：保留「股份有限公司」「有限公司」等後綴，不截短
```

**驗收訊號達成** — 對人講 1 分鐘沒打結，對方追問的細節能補進便箋。

---

### Step 2：讀 JSON

#### 2.1 A 在 n8n UI export #02

打開 n8n UI（`http://localhost:5678`）→ 進到 #02 → 點右上角 `⋮` → 選 Download → 跳出視窗，下拉選單原本是「Default」，A 切到「**Without credentials**」→ 點 Download。下載到 `02-pdf-ai-rename.json`。

#### 2.2 A 用 VS Code 搜尋 4 個字串

A 在 VS Code 打開 .json，按 Cmd+F：
- 搜 `apiKey` → 0 個結果
- 搜 `accessToken` → 0 個結果
- 搜 `password` → 0 個結果
- 搜 `token` → 0 個結果

**4 字串全 0，過關**。

#### 2.3 A 貼模板 2 給 ChatGPT

A 切回 ChatGPT 視窗（剛才開場那個），貼：

```
我是 n8n 非工程師使用者，請以結果為主、不解釋原理。
以下是一份 n8n workflow JSON（已移除 credential）。請：
1. 用一段話講它做了什麼。
2. 列出每個節點的角色與資料流向（節點名稱 → 它輸出什麼 → 下一個節點吃什麼）。
不要建議改進、不要寫程式碼。

{
  "name": "02-pdf-ai-rename",
  "nodes": [
    {
      "parameters": {},
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      ... (整份 JSON 約 200 行) ...
    }
  ],
  "connections": { ... }
}
```

#### 2.4 ChatGPT 回應（sample）

```
這份 workflow 做什麼：
從 /files/pdf-inbox/ 讀取資料夾內所有 PDF，用 Gemini API 分析每份 PDF 的
文字內容後產出一個語意化檔名（格式 YYYYMMDD_類型_關鍵字），最後把原 PDF
用新檔名移到 /files/pdf-renamed/ 資料夾。整套流程是手動觸發。

節點清單（5 個）：
1. Manual Trigger
   - 角色：手動觸發點
   - 輸出：空訊息（觸發訊號）
   - 下一個節點吃：觸發訊號

2. Read PDF
   - 角色：列出 /files/pdf-inbox/ 內所有 .pdf 檔
   - 輸出：每張 PDF 的 binary data + 原始檔名
   - 下一個節點吃：binary

3. Extract PDF Text
   - 角色：把 PDF binary 轉成純文字
   - 輸出：pdfTextPreview 欄位（純文字）
   - 下一個節點吃：pdfTextPreview

4. Code: AI 改名（內含 Gemini call）
   - 角色：呼叫 Gemini API，根據 PDF 文字產出新檔名字串
   - 輸出：newFilename 欄位（字串）
   - 下一個節點吃：newFilename + 原 binary

5. Write
   - 角色：把原 PDF 用 newFilename 改名後寫到 /files/pdf-renamed/
   - 輸出：寫入結果（成功/失敗）
   - 下一個節點：（流程結束）

資料流向：Manual Trigger → Read PDF → Extract PDF Text → Code → Write
```

#### 2.5 A 對照 n8n UI 確認

A 切回 n8n UI 的 #02 編輯畫面，照著 ChatGPT 給的清單確認：
- 節點數量：5 ✓
- 節點順序：和我看到的左到右一致 ✓
- 「Code: AI 改名」描述「內含 Gemini call」對得上 ✓

**驗收訊號達成** — 80% 以上節點對得上。A 用自己的話複述：「讀 inbox 資料夾的 PDF，用 Gemini 給檔名，存到 renamed 資料夾。」30 秒講完。

---

### Step 3：限定修改範圍（含岔路：LLM 第 1 輪給整份）

#### 3.1 A 決定只動 1 個節點

回到 4 格便箋第 4 格「必保留節點」，看到只有 Code 節點是要改的。其他 4 個節點完全不動。

#### 3.2 A 在 n8n UI 備份 Code 節點

點 Code 節點 → Cmd+C → 在 macOS Notes 開一條新筆記 `code-backup-2026-05-07.txt` → 貼上。看到內容開頭是 `{ "parameters": ...`，存檔。

#### 3.3 A 貼模板 3 給 ChatGPT

```
基於剛才那份 workflow，只改節點「Code: AI 改名」（其他節點不動）。
我要的修改：
- prompt 字串改成抽取賣方公司全名（保留「股份有限公司」等後綴）、
  稅後合計（純數字，不含元）、發票日期（YYYYMMDD 格式）
- 檔名 template 改成：{YYYYMMDD}_發票_{賣方名}_{稅後合計}.pdf
- 類型欄位固定填「發票」，不要讓 AI 自己判斷
- 其他邏輯（fallback、parseMethod、httpError 處理）全部保留

請回傳「只有這個 Code 節點」的 JSON 區段（不要整份 workflow）。
回應格式：直接給 JSON 物件，最外層 `{` 後面第二行是 `"parameters":`，
不要 markdown code fence。
```

#### 3.4 岔路：ChatGPT 第 1 輪回**整份**（反例）

```
好的，這是改造後的 workflow：

```json
{
  "name": "02-pdf-ai-rename-invoice",
  "nodes": [
    { "parameters": {...}, "name": "Manual Trigger", ... },
    { "parameters": {...}, "name": "Read PDF", ... },
    { "parameters": {...}, "name": "Extract PDF Text", ... },
    {
      "parameters": {
        "mode": "runOnceForEachItem",
        "jsCode": "const text = $input.item.json.pdfTextPreview;\nconst prompt = `請從以下發票文字抽取：賣方公司全名、稅後合計（純數字）、發票日期（YYYYMMDD）...`;\n..."
      },
      "name": "Code: AI 改名",
      ...
    },
    { "parameters": {...}, "name": "Write", ... }
  ],
  "connections": {
    "Manual Trigger": { "main": [[{"node": "Read PDF", ...}]] },
    ...
  }
}
```

希望這份能直接匯入！
```

#### 3.5 A 立刻發現問題

A 用驗收硬指標 1：看 LLM 回的開頭，第一行 `{`，第二行 `"name":`，第三行 `"nodes":` — **這是整份 workflow，不是區段**。

A 心想：好險我看到「nodes」陣列了，要追問。

#### 3.6 A 用追問模板

```
你給的是整份 workflow（最外層有 "name" 和 "nodes"）。
我只要 Code 節點的單個 JSON 物件（從 { "parameters": 開始，到 } 結束）。
請重新只給這個節點。
```

#### 3.7 ChatGPT 第 2 輪修正

```
抱歉理解錯。這次只給 Code 節點：

{
  "parameters": {
    "mode": "runOnceForEachItem",
    "jsCode": "const text = $input.item.json.pdfTextPreview;\nconst prompt = `請從以下發票文字抽取：賣方公司全名（保留「股份有限公司」後綴）、稅後合計（純數字，不含元字）、發票日期（YYYYMMDD 格式）。回傳 JSON：{seller, totalAmount, invoiceDate}。發票文字：${text}`;\n\ntry {\n  const response = await this.helpers.httpRequest({\n    method: 'POST',\n    url: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',\n    body: { contents: [{ parts: [{ text: prompt }] }] },\n    json: true\n  });\n  const result = JSON.parse(response.candidates[0].content.parts[0].text);\n  const newFilename = `${result.invoiceDate}_發票_${result.seller}_${result.totalAmount}.pdf`;\n  return { json: { newFilename, originalFilename: $input.item.json.fileName, ...result } };\n} catch (e) {\n  // fallback：保留原檔名加上_unparsed suffix\n  return { json: { newFilename: `${$input.item.json.fileName}_unparsed.pdf`, error: e.message } };\n}"
  },
  "name": "Code: AI 改名",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [820, 300]
}
```

#### 3.7.1 但 ChatGPT 可能還會回成這幾種樣子（不是每次都這麼乾淨）

現實是 LLM 第二輪修正不會永遠像 3.7 這麼漂亮。你**可能**會看到下面 3 種「歪掉但常見」的回應，學員必須能辨認後決定下一步：

**變體 A：LLM 又夾雜其他節點解說**

```
抱歉理解錯。這次我給你 Code 節點。但在那之前，建議你先確認 Read PDF
節點的 fileExtensions 設定是 .pdf；另外 Manual Trigger 不需要任何設定，
Extract PDF Text 你可以選 raw 或 structured 模式⋯⋯

{ "parameters": { ... }, "name": "Code: AI 改名", ... }
```

- **辨認訊號**：回應字數突然變多、提到 Trigger / Read PDF / Extract PDF Text 等你模板 3 已經寫「不動」的節點
- **學員下一步**：再貼一次「精簡追問」：「請只回我問的 Code 節點 JSON，不要說明其他節點。」貼完就是第 3 輪重來，不要試圖從這段 mixed response 裡摘出 Code 節點

**變體 B：LLM 改了但漏了 1 個欄位**

```
{
  "parameters": {
    "mode": "runOnceForEachItem",
    "jsCode": "..."
  },
  "name": "Code: AI 改名",
  "type": "n8n-nodes-base.code"
}
```

- **辨認訊號**：對照模板 3 你列的欄位清單（這裡參考 3.7 的完整版），發現少了 `typeVersion` 與 `position`
- **學員下一步**：不用再叫 LLM 重來，自己手補回去就好（從 3.2 的 backup 抓 `"typeVersion": 2` 與 `"position": [820, 300]` 兩行貼回來）。LLM 第 3 輪重做的成本比手補高

**變體 C：LLM 突然轉去解釋「為什麼這樣設計」**

```
針對你的需求，我先說明設計考量：因為發票 PDF 的格式變化大，所以我把 prompt
寫得比較具體；同時為了避免 Gemini 回 JSON 解析失敗，我保留了原本的 fallback
邏輯⋯⋯（接著一整段說明）

{ "parameters": { ... }, "name": "Code: AI 改名", ... }
```

- **辨認訊號**：回應第 1 段是「設計考量／我這樣做是為了⋯⋯」這類說明文，不是直接 JSON
- **學員下一步**：把這段說明文整段忽略，直接 scroll 找 `{ "parameters":` 開頭那段 code 拿來貼。不需要再追問，這只是 LLM 想多講話而已

> **這 3 種變體的共通教學價值**：LLM 第 2 輪不會永遠乾淨，但**乾淨與否其實不影響學員能不能完成任務** — 只要你能辨認「這段是垃圾、那段是我要的 Code 節點」，剩下的動作（追問 / 手補 / 直接拿 code 段）都很短。卡學員的不是 LLM 不乾淨，是學員以為「LLM 一回不乾淨就要重新來過」。

---

#### 3.8 A 驗收

A 看：
- 第一行 `{` ✓
- 第二行 `"parameters":` ✓ — **是區段格式**
- 節點 name 是「Code: AI 改名」（沒被改名）✓
- typeVersion 2（跟原 #02 一致，A 之前 export 的 backup 確認）✓

#### 3.9 A 替換到 n8n UI

> ⚠️ **學員容易卡 5-10 分鐘的點**：n8n UI 的 Code 節點切換到 JS 模式 → 全選清空 → 貼新 code 這個動作對非工程師不直觀。Code 節點的 parameter view 跟一般節點不一樣（左半 mode 切換 + 右半 jsCode 編輯區），第一次替換很容易：(a) 不知道怎麼切到 JS 模式 (b) 想把整個 JSON 物件貼進 jsCode 框結果報錯 (c) 不確定要貼整段 `{ "parameters": ... }` 還是只貼 `jsCode` 字串。建議第一次跑時：**保留舊 Code 節點 disabled（右鍵 → Deactivate）放旁邊，不要直接覆蓋** — 在原 workflow 上新增一個 Code 節點，把 ChatGPT 給的內容貼到新節點，跑通後再把舊的刪除。這樣壞了能 fallback。

n8n UI 上點 Code 節點 → Cmd+C 暫存（再加一份保險）→ 點節點 → 右鍵 → Paste → 貼 ChatGPT 給的內容。看 5 個節點還在原位、連線實線沒斷 ✓。

點開 Code 節點看 jsCode，搜尋「賣方」 — 出現了 ✓；搜尋「合約」「甲方」 — 都不見了 ✓。

**驗收訊號達成** — 區段格式 + 節點原位 + 連線完整 + 字串內容正確替換。

---

### Step 4：匯入測試（含岔路：跑出 null_null 劇情錯誤）

#### 4.1 A Duplicate workflow

n8n UI workflow 列表 → #02 那條右側三點 → Duplicate → 跳出新 workflow 名為「02-pdf-ai-rename copy」 → A 改名為「02-pdf-ai-rename-invoice-edit」。

#### 4.2 A 驗收 Duplicate

回 workflow 列表，看到原 `02-pdf-ai-rename` + 新 `02-pdf-ai-rename-invoice-edit` 兩條 ✓。

進到 -edit 版，看右上角 Active 開關：**灰色 OFF** ✓（n8n Duplicate 時預設不啟用）。

#### 4.3 A 把 Code 節點的修改複製到 -edit 版

> ⚠️ **教學示範：A 這次的順序顛倒了，正確做法是「先 Duplicate 再改」**
>
> 商業培訓非工程師第一次走流程，**很常順序顛倒** — 在原 #02 上先動了刀，跑到這 step 才想起紅線 7 要 Duplicate。劇本如實呈現這個現實 case，並示範「順序顛倒了還是有救」的還原動線。
>
> **正確的下次順序**（請 hard-code 進你的肌肉記憶）：
>
> 1. **先**在 workflow 列表 Duplicate 原 workflow 變 -edit 版
> 2. **檢查 -edit 版 Active 開關 OFF**（灰色）
> 3. **在 -edit 版上改 Code 節點**（不是在原 workflow 上改）
> 4. 跑通後才考慮把 -edit 版改名為 v2、原版改名為 v1-archived
>
> A 這次順序是 (1)(3)(2) 反過來，所以有了下面的「補救動作」 — 但**正常情況不該需要補救**。

剛才 3.9 是改在原 #02 — 等等，A 想了一下：紅線 7 說 **不在 production 上改**。她意識到剛才應該先 Duplicate 再改。但 #02 不是 production（沒打開 Active），算 OK。為了安全（補救動作）：

- 在原 #02 上把 Code 節點 Cmd+C
- 切到 -edit 版，點 Code 節點 → Cmd+V → 替換
- **同時** 把原 #02 的 Code 節點還原回 backup（用 macOS Notes 那份 code-backup）

> **這段教學價值**：示範學員第一次走流程時容易顛倒順序（先改後 Duplicate）。沒關係，回頭還原即可，但下次嚴格走「Duplicate → 開關 OFF → 在 -edit 上改」這個固定 3 步動線。

#### 4.4 A 準備測試 PDF

把上週收到的 1 張測試發票 PDF（檔名 `inv_20260430_001.pdf`）放到 `/files/pdf-inbox/`。

#### 4.5 A 點 Execute Workflow

n8n UI 下方紫色按鈕 Execute Workflow。

#### 4.6 跑完 — 全綠燈，但⋯⋯

5 個節點全綠燈。A 開心了 2 秒。她點 Code 節點看 Output panel：

```json
{
  "newFilename": "20260506_發票_null_null.pdf",
  "originalFilename": "inv_20260430_001.pdf",
  "seller": null,
  "totalAmount": null,
  "invoiceDate": "20260506"
}
```

`seller: null`、`totalAmount: null`！A 心想：「綠燈不代表對啊」（紅線 5：LLM 輸出當草稿）。

她去 `/files/pdf-renamed/` 看 — 真的多了一個 `20260506_發票_null_null.pdf`。

進入 Step 5 錯誤回報。

> **這個劇情 null_null 的教學價值**：第 4 章紅線 5 講「LLM 輸出當草稿」是抽象的；這裡 A 實際看到「全綠燈但 null_null」是具象的。學員看完內化「綠燈不等於對，要看 output 內容」。

---

### Step 5：錯誤回報（含 sample 精準型 LLM 回應）

> ⚠️ **學員容易卡 10-15 分鐘的點**（涵蓋 5.1-5.3）：n8n UI 的「View input / View output / Debug」面板切換邏輯 + JSON 結構閱讀，對非工程師是雙重門檻：(a) input panel 與 output panel 在哪、怎麼切 — n8n UI 是把 input/output 放在節點右側、預設只顯示其中一個，要點上方 tab 切；(b) 看 JSON 找關鍵欄位 — 即使切到 output 看到了 `{...}`，也不容易快速定位「seller / totalAmount 是 null」。建議：**跟 #02 已經跑過的成功 output 開兩個視窗對照看**（左邊放 #02 合約版的 output panel、右邊放這次 -invoice-edit 版的 output panel），不要憑空想像「正常 output 長什麼樣」 — 對照看你會立刻發現「合約版 output 有完整 seller 字串、發票版是 null」這個差異。

#### 5.1 A 找到「問題節點」

雖然沒紅燈，但 A 知道問題在 Code 節點（output 是 null）。她點 Code 節點，看 Input panel：

```json
{
  "pdfTextPreview": "電子發票...賣方：弄一下工作室股份有限公司...統一編號：12345678...品項：n8n 工作坊...稅後合計：15,750 元...發票日期：2026/04/30..."
}
```

A 看到 **PDF 上的關鍵字是「賣方」（不是「供應商」）和「稅後合計」（不是「稅後金額」）**。

她在 Step 1 便箋裡寫過「PDF 上中文寫『賣方』」，但 Step 3 給 ChatGPT 的模板 3 用的是「賣方公司全名」— ChatGPT 在 jsCode 的 prompt 字串裡可能擅自改了詞。

#### 5.2 A 複製三件套

- **錯誤訊息**：沒有紅燈訊息，但 output 顯示 `seller: null, totalAmount: null` — 這就是「軟錯誤」。她直接寫「不是紅燈，但 output 的 seller 和 totalAmount 都是 null」
- **input panel JSON**：上面那段 `pdfTextPreview` 全文
- **parameter**：點 Code 節點旁齒輪 → 看到 jsCode 全文，用 Cmd+A 複製。**搜尋 apiKey/accessToken/password/token 都 0 個結果** ✓

#### 5.3 A 貼模板 4 給 ChatGPT

```
我把節點「Code: AI 改名」替換成你上一輪給的內容後，跑了 1 張測試發票。
不是紅燈，但 Code 節點 output 顯示：
  seller: null
  totalAmount: null

該節點 input（pdfTextPreview 摘要）：
"電子發票...賣方：弄一下工作室股份有限公司...統一編號：12345678...
品項：n8n 工作坊...稅後合計：15,750 元...發票日期：2026/04/30..."

該節點當前 parameter 的 jsCode（搜尋過無 credential）：
const text = $input.item.json.pdfTextPreview;
const prompt = `請從以下發票文字抽取：賣方公司全名（保留「股份有限公司」後綴）、
稅後合計（純數字，不含元字）、發票日期（YYYYMMDD 格式）。
回傳 JSON：{seller, totalAmount, invoiceDate}。
發票文字：${text}`;
... (httpRequest 邏輯保留) ...

請只指出：
1. 問題在哪個欄位（精確到行）
2. 最小修改是什麼（給出具體新值）

不要重寫整個節點、不要建議換做法、不要加 try/catch。
```

#### 5.4 ChatGPT 第 1 輪「精準診斷」（sample）

```
從你貼的 input / output 看，問題應該在 prompt 字串對「格式轉換」的指示
不夠明確，不是 jsCode 解析邏輯本身錯。具體來說 — 你看 jsCode 的 prompt
字串第 2-4 行寫「稅後合計（純數字，不含元字）」、「發票日期（YYYYMMDD
格式）」，這兩條指示對 Gemini 來說太模糊。

input panel 的 pdfTextPreview 你貼的內容是：
- PDF 用「稅後合計：15,750 元」— 帶千分位逗號
- PDF 用「發票日期：2026/04/30」— 是 YYYY/MM/DD 不是 YYYYMMDD

Gemini 看到 prompt 只說「純數字」沒講「去除逗號」，回的 JSON 很可能是
"totalAmount": "15,750"（字串帶逗號），jsCode 拿去組檔名變成 `null` 或
parseInt 掉精度。同樣 invoiceDate 沒給轉換規則，Gemini 多半直接回原字串
"2026/04/30"，組檔名時 jsCode 認不出。所以根因是 prompt 對 Gemini 的
**格式轉換指示**不夠具體，而不是 jsCode 的 try/catch 或 fallback 壞掉。

修法 A（建議）：在 prompt 字串第 3-4 行加明確的「轉換動作 + 範例」：

新 prompt（第 3-5 行替換成下面 3 行）：
  「賣方公司全名（保留「股份有限公司」後綴）」
  「**稅後合計（去除逗號和「元」字，只保留純數字。例：「15,750 元」→ 15750）**」
  「**發票日期（從 YYYY/MM/DD 格式轉成 YYYYMMDD。例：「2026/04/30」→ 20260430）**」

修法 B：如果你不想改 prompt、想在 jsCode 端修，那就在 `JSON.parse` 後加
`result.totalAmount = parseInt(String(result.totalAmount).replace(/[,元]/g,''))`
這類後處理 — 但這樣每次 Gemini 回的格式變一點點你就要再改 jsCode，A 路較划算。

其他不動。
```

#### 5.4.1 紅綠對照表（看完 LLM 回應立刻判斷）

5.4 那段 sample 之所以叫「精準型」，不是因為它讀起來順，是因為它**同時滿足 3 條訊號**。學員下次貼模板 4 拿到回應時，先用這張表判斷再決定要不要採用：

| 訊號 | 🟢 精準型有 | 🔴 模糊型沒有 |
|---|---|---|
| 指出**具體欄位**（newFilename / parseMethod / prompt 第幾行 / jsCode 哪個變數） | ✅「在 jsCode 的 prompt 字串第 2-4 行」 | ❌「請檢查 prompt 描述是否清楚」 |
| 引用你貼的 **input / output 內容**當證據 | ✅「你貼的 pdfTextPreview 顯示『稅後合計：15,750 元』」 | ❌「PDF 內容看起來⋯⋯」（沒引用具體字串） |
| 給可**直接貼上**的新值（新字串 / 新 code 段） | ✅「把第 3 行替換成：『稅後合計（去除逗號和「元」字，只保留純數字。例：「15,750 元」→ 15750）』」 | ❌「建議讓 prompt 結構更明確」（沒給文字） |

**判斷規則**（30 秒內做完）：

- **3 條全 🟢** → 直接信、貼、再驗收（走 5.5 / 5.6）
- **任一 🔴** → 再貼模板 4 一次，把缺的訊號補成具體要求：
  - 缺欄位 → 加一句「請指出具體在哪個欄位 / 哪一行」
  - 缺 input 引用 → 加一句「請引用我貼的 pdfTextPreview 原文當證據」
  - 缺新值 → 加一句「請給可直接貼上的新字串 / 新 code，不要只給方向」
- **3 條全 🔴**（最壞情況）→ **換對話視窗從頭開始**（這個對話已經被你前面幾輪的 context 帶歪了，硬追問 LLM 回應只會越來越鬆）

> **這張表的價值**：「精準 vs 模糊」不是模糊的感覺，是 3 個可數的訊號。學員不用「是不是精準的我看不出來」憑感覺猜。

---

#### 5.5 A 驗收 LLM 回應

A 用第 4 章驗收硬指標：
- (a) 指出具體欄位 ✓（jsCode 的 prompt 字串第 2-4 行）
- (b) 給出具體修改值 ✓（兩段新指示文字）
- (c) 引用 input 內容當證據 ✓（PDF 上是「2026/04/30」）

**這是「精準型」回應，不是「太模糊」（模糊型會說「建議調整 prompt」沒給具體字）**。

#### 5.6 A 替換並重跑

A 在 n8n UI Code 節點裡，把 prompt 字串第 3-5 行手動改成 LLM 給的新版（也可以再叫 LLM 給完整節點區段，但這裡只改 3 行 A 自己改更快）。

重跑：5 節點全綠 ✓。Code Output：

```json
{
  "newFilename": "20260430_發票_弄一下工作室股份有限公司_15750.pdf",
  "originalFilename": "inv_20260430_001.pdf",
  "seller": "弄一下工作室股份有限公司",
  "totalAmount": 15750,
  "invoiceDate": "20260430"
}
```

`/files/pdf-renamed/` 多一個 `20260430_發票_弄一下工作室股份有限公司_15750.pdf` ✓。

**驗收訊號達成** — 1 張測試 PDF 改名成功。

---

### Step 6：收斂（含岔路：LLM 主動加 try/catch，A 拒絕）

#### 6.1 A 換 10 張不同供應商發票測試

A 把 `pdf-inbox` 換成 10 張不同供應商的真實發票（手邊的存量），Execute Workflow。

跑完：5 節點全綠 ✓。10 張 newFilename 看：
- 9 張正常（例：`20260415_發票_AA有限公司_8420.pdf`）
- 1 張有問題：`20260420_發票_BB商業有限公司_0.pdf` — 稅後合計 0 元

A 翻 BB 公司那張原 PDF — 是退款單，稅後合計欄位真的是 `NT$ 0`。

#### 6.2 A 決定不改流程

A 想：「這是邊界 case，本次 200 張裡退款單可能有 1-2 張，數量不大。我不要為了 1 張改流程，記備注就好。」

她在 n8n UI 上點 -edit 版的 workflow → 找 Settings 或 Description 欄 → 寫一行：

```
備注（2026-05-07）：
邊界 case：稅後合計 0 元 = 退款單，本版照 0 元改名（不過濾），人工檢查時注意。
範例：20260420_發票_BB商業有限公司_0.pdf
```

#### 6.3 A 找 ChatGPT 確認 — 但這個情境多半不會被勸開 try/catch

A 為了確認，回 ChatGPT 對話視窗貼：

```
我跑了 10 張，9 張過，1 張是退款單稅後合計 0。
我打算不改流程（人工注意 0 元的）。你覺得 OK 嗎？
```

ChatGPT 在這個對話脈絡下（A 從 Step 3 起一路明確說「只動 X 欄位」「不要加 try/catch」「不要建議換做法」），實際多半會回得很收斂：

```
9/10 通過 + 退款單人工處理是合理選擇。本次規模 10 張、退款單比例 1/10
本來就低，不值得為這個 case 加流程複雜度。維持現狀即可。
```

A 放心了 — 不改流程，繼續走全量。

#### 6.4 但別的情境裡，LLM 仍會主動建議擴張（這時用模板 5 拒絕）

> **這個情境 ChatGPT 多半不會自己加 try/catch（但別的情境會）**
>
> 在我們這個對話脈絡下，ChatGPT 看到 A 已經明確要求過「只動 X 欄位」「不要建議換做法」「不要加 try/catch」會傾向收斂、不主動擴張。但你**可能**遇到下面 2 種情況，建議仍會冒出來：
>
> - **換用 Claude / Gemini 同樣問法**：他們對 robustness 的偏好比 ChatGPT 高，可能會主動建議「我幫你加個 try/catch 防 PDF 解析失敗」「順便加個 `_refund` 後綴自動標記退款單」
> - **同 ChatGPT 但你 prompt 給得鬆**：如果 Step 3 模板 3 沒寫「只動 X」、Step 5 模板 4 沒寫「不要加 try/catch」，ChatGPT 看到你問「你覺得 OK 嗎」也可能順手建議加防禦
>
> 不論哪一個 LLM 主動建議擴張，**答案永遠是用模板 5 拒絕**：

```
請用一句話比較你最早給我的版本與現在這個建議：
- 哪些是「為了我原始需求必要的」？
- 哪些是「你新增的防禦邏輯」（try/catch、新欄位、新邏輯）？

請保留必要的、移除新增的。我這次只要 9/10 過 + 人工處理 1 張，
不需要 _refund 自動標記。
```

LLM 拿到這段後典型會收斂回：

```
比較：

必要的（保留）：
- prompt 字串的欄位修正（賣方/稅後合計）
- prompt 對日期格式 YYYY/MM/DD → YYYYMMDD 的轉換指示

新增的防禦邏輯（移除）：
- try/catch 包住整個 API call
- _refund 後綴自動標記

清理後的版本就是你現在用的版本，不需要再改。9/10 過 + 人工處理 1 張是合理選擇。
```

> **這個 turn 的教學價值**：示範學員如何「對 LLM 說不」。LLM 不一定每次都主動擴張，但只要它擴張，學員就要會踩煞車。理由：學員自己沒測過的 try/catch 反而會吃掉錯誤訊號讓 debug 更難。模板 5 是煞車。

---

### Step 7：全量執行 + 驗收交付

#### 7.1 A 把 200 張全放 pdf-inbox

從共享資料夾複製當月 200 張供應商發票到 `/files/pdf-inbox/`。

#### 7.2 Execute Workflow（全量）

n8n UI 點 Execute Workflow。等了 4 分鐘（每張 PDF 平均 1.2 秒）。

#### 7.3 看執行結果

n8n UI 下方執行紀錄：
- Read PDF：200 張全部讀取 ✓
- Extract PDF Text：200 張全部 ✓
- Code: AI 改名：199 張綠燈，1 張紅燈 ✗
- Write：199 張寫入

點紅燈那張 Code 節點 → 看到錯誤訊息：`SyntaxError: JSON.parse failed at position 42`。

A 看 input — 那張 PDF 的 pdfTextPreview 是「[圖片，無文字]」 — 是純掃描的圖片發票，OCR 沒抽到文字。

#### 7.4 A 處理 1 張失敗

A 把那張 PDF 從 `pdf-inbox` 移到一個叫 `_manual_review/` 的子資料夾，記到 workflow Description：

```
備注 (2026-05-07 全量跑)：
1 張掃描圖片發票無文字內容，已移到 _manual_review/，需人工處理。
```

#### 7.5 Finder 確認

打開 Finder，去 `/files/pdf-renamed/`：
- 199 個檔案（不是 200，因為 1 張失敗）
- 抽查 5 個檔名格式：
  - `20260415_發票_AA有限公司_8420.pdf` ✓
  - `20260420_發票_BB商業有限公司_0.pdf` ✓（退款單，已記備注）
  - `20260425_發票_CC企業股份有限公司_3450.pdf` ✓
  - `20260428_發票_DD國際有限公司_22100.pdf` ✓
  - `20260430_發票_弄一下工作室股份有限公司_15750.pdf` ✓（測試那張）

格式全部正確，**驗收交付通過**。

#### 7.6 整理 workflow 版本

A 在 n8n UI workflow 列表：
- 把 `02-pdf-ai-rename-invoice-edit` 改名為 `#02b-pdf-invoice-rename (v1.0)`
- 原 `02-pdf-ai-rename` 改名為 `#02-pdf-contract-rename (v0.6)` 並維持 OFF（之後處理合約還是用這個）
- 兩條 workflow 同時存在，將來合約 / 發票任務各用對應版本

---

### Step 8：6 步流程時間分配回顧

A 是工程背景偏弱的非工程師、第 1 次走完整流程，從上午 10:00 開始到 11:30 結束，總計 **90 分鐘**。但她事前其實已經有兩個有利條件：(a) #02 合約版她跑過 → n8n UI 不陌生 (b) 中間沒被 Slack / 會議打斷。**多數非工程師學員第一次走，會落在 90-120 分鐘區間，更接近 120 端**：

| 步驟 | 動作 | A 實際時間 | 學員預期區間 |
|---|---|---|---|
| 1 | 拆需求（4 格便箋 + 對 B 講 + 補一格） | 15 分鐘 | 15-20 分鐘 |
| 2 | 讀 JSON（export + 4 字串搜尋 + LLM 翻譯） | 10 分鐘 | 10-15 分鐘 |
| 3 | 限定範圍（備份 + LLM 第 1 輪整份 + 追問 + 替換 UI） | 20 分鐘 | 25-35 分鐘 ⚠️ |
| 4 | 匯入測試（Duplicate + 1 張測試 + 發現 null_null） | 10 分鐘 | 10-15 分鐘 |
| 5 | 錯誤回報（找問題 + 三件套 + LLM 精準診斷 + 重跑通過） | 15 分鐘 | 20-30 分鐘 ⚠️ |
| 6 | 收斂（10 張測試 + 1 張退款邊界 + LLM 擴張拒絕） | 10 分鐘 | 10-15 分鐘 |
| 7 | 全量 + 驗收（200 張跑 4 分鐘 + 1 張失敗處理 + Finder 確認） | 10 分鐘 | 10-15 分鐘 |
| **合計** | | **90 分鐘** | **90-120 分鐘** |

⚠️ 標記的 Step 3 與 Step 5 是學員最容易超時的兩段。原因見各 step 段首的「⚠️ 學員容易卡」標籤 — 不是 LLM 對話的問題，是 n8n UI 操作 + JSON / Output panel 閱讀對非工程師是雙重門檻。

A 心算：第 2 次再做這種改造（例：把另一個 workflow 改成處理收據），預估 30-40 分鐘。第 5 次大概 15-20 分鐘。她在便箋最後寫：

```
心得：90-120 分鐘的首次投資，省下 200 張 × 30 秒手動分類 = 100 分鐘（單次）。
但更重要：下個月 200 張、再下個月 200 張⋯⋯一年省 20 小時。
```

---

### Phase C 章末：A 給其他學員的 5 個提醒

（這部分是 walkthrough 結尾的學員視角總結，比 maintainer note 有用）

1. **第 1 步別跳**：4 格便箋花 15 分鐘，省下後面 60-90 分鐘
2. **LLM 第 1 輪很常給整份**：別怕，用追問模板要它重給就好；給歪的變體（混入其他節點 / 漏欄位 / 一堆說明文）見 3.7.1 三種辨認法
3. **綠燈不等於對**：永遠看 output 的關鍵欄位是不是 null
4. **LLM 不一定每次都建議加 try/catch**（ChatGPT 在你明確說「只動 X」時多半收斂；換 Claude / Gemini 或 prompt 鬆了它就會擴張）：**只要它建議擴張，就用模板 5 拒絕**；保持簡單才好驗收
5. **20 / 80 原則**：邊界 case（退款單、掃描圖片）先記備注人工處理，不為 1-2 張改流程

---

<a id="followup"></a>

---

## 設計記錄（Phase A 診斷）

本章原始 HTML 章節的「空話」診斷清單，作為重設計的問題對應表：

### 第 6 章 post-llm-6-walkthrough — 把 #02 改成處理發票

**整體判定**：使用者提示「這章該是最 hands-on 的卻可能最浮泛」是準的。**這章從頭到尾用「敘事第三人稱」描寫主角 A 的操作，但沒有真的把 LLM 對話 turn 寫出來**——line 293-295、352-354、362-364、453-455、482-484 等位置全部用 `[需錄製：LLM 對話截圖 — ...]` 占位符，把這章從「實機 walkthrough」降級成「行為大綱」。Phase C 必須完整重做這章（見 Phase C 章節）。

| # | line | 原文摘要 | 違反 | 為什麼會卡住學員 |
|---|---|---|---|---|
| A6-1 | 293-295 | `[需錄製：LLM 對話截圖 — 步驟 2 翻譯回應]` | 1, 2 | 整個步驟 2 的核心 LLM turn**整段不存在**，只剩一個括號描述「應該長什麼樣」。學員看不到 LLM 真實會回什麼，也不知道驗收的對照基準是什麼 |
| A6-2 | 296-299 | `[需截圖：n8n UI 畫面 — #02 workflow 全景]` | 2 | walkthrough 章的核心是「我照做就會看到一樣的畫面」，但 11 個截圖佔位符全是括號描述。如果這章是「行為大綱」可以理解，但整章被宣告為「實作示範」，這就是空話 |
| A6-3 | 351-354 | 「第一輪的對話佔位符」+ `[需錄製：LLM 對話截圖 — 步驟 3 第一輪]` | 1 | 步驟 3 是「最容易跳步」的核心 step，但這章沒有把 LLM 第一輪實際回應 paste 出來。學員想學「怎麼判斷 LLM 給的是區段不是整份」，必須看到對照樣本 |
| A6-4 | 356 | 「但這裡有個常見反例要示範——如果 LLM 第一輪回傳的是整份 workflow 怎麼辦？」+ 緊接 placeholder | 3 | 「常見反例要示範」但**沒示範**——對話佔位符塞在這。整個「示範」只有 placeholder 框，沒有內容 |
| A6-5 | 405-408 | 「這份 walkthrough 故意安排了一個錯誤：『甲方』vs『賣方』」+「進步驟 5 示範如何回報這個錯誤」 | (具體度尚可，但接下來的步驟 5 又掉進 placeholder) | 這個故意錯誤是好設計，但步驟 5 的 LLM 回報對話又是 placeholder（line 454-456），等於設計了戲劇性高潮但沒演。需要把 LLM 回應實寫出來 |
| A6-6 | 478 | 「9 張正確，1 張出現……稅後金額變成了 0……她去翻那張 PDF 的原始文字，發現那張發票的『稅後合計』欄位是『NT$ 0（退款單）』」 | (具體度高，但) | 這個邊界 case 處理寫得不錯，但「她決定這個邊界情況不在這次的改造範圍內，記了一筆備注給未來的自己」——「記備注」具體記在哪？學員需要明確的 action（例：在 n8n workflow 設定的 description 欄寫一行「邊界 case：金額 0 = 退款單，本版未處理」） |
| A6-7 | 482-484 | `[需錄製：LLM 對話截圖 — 收斂迴圈，含 try/catch 拒絕]` | 1 | 「拒絕 try/catch」的 turn 全在 placeholder。這個 turn 是學員整個系列的「我可以了」拐點之一（學員第一次「對 LLM 說不」），不寫出來等於沒教 |
| A6-8 | 511-516 | `[需截圖：n8n UI 畫面 — 改造後的 workflow]`+`[需截圖：Finder — pdf-renamed 資料夾]` | 2 | 最終驗收畫面是 placeholder。學員不知道「我跑完看到 Finder 變什麼樣才算對」 |
| A6-9 | 528-534 | 「對製作者的提醒」整段 | (不算空話但) | 這節對學員無用，是給 maintainer 看的。應該刪除或移到 _local/，不應該保留在學員看的 HTML |

**第 6 章空話小計：9 條**（其中 7 條是 placeholder 直接構成的空話）

---
