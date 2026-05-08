---
unit_id: post-llm-9-format-adapt
title: 跨格式改寫 — 從 PDF 跨到 Word / Excel / 圖片 / 純文字
course: n8n / AI 資料工廠
chapter: 第 9 章 / 9（post-llm 系列：課後用 LLM 改 workflow）
description: 商業學員真實業務拿到的不只 PDF — 教你把 #03 改造處理 Word / Excel / 圖片 / 純文字的 5 種格式 dispatch 策略
audience: 商業培訓非工程師、課後用網頁版 LLM 改 workflow
prerequisite: 已看完 ch1-8 + 跑過第 6 章 walkthrough，能改 prompt 換欄位
delivery: 文字導向 HTML 章節（無印風）
created: 2026-05-08
codex_audit: pending
codex_verdict: pending
last_updated: 2026-05-08
---

# 跨格式改寫 — 從 PDF 跨到 Word / Excel / 圖片 / 純文字

> **本章重設計教案** · 對應 `courses/n8n/lessons/post-llm-9-format-adapt.html`

## 重設計內容

## 第 9 章：跨格式改寫 — 從 PDF 跨到 Word / Excel / 圖片 / 純文字

### 1. 學員此時的痛點

學員結業之後，第一個業務需求**極少**還是「PDF 改名」。看 Lite Pack 課後問卷反饋，最常出現的版本是這幾種：

- 「我有 50 個 Word 報價單要照 #03 那種方式改名 + 分類」
- 「主管丟了 200 列的 Excel 客戶清單，要我用 AI 幫每筆寫個 follow-up 摘要」
- 「同事傳了一資料夾 LINE 截圖（.png）要我整理成檔案名」
- 「業務每天匯出 .csv 我要做摘要寄給主管」

學員打開 #02 / #03 看 — 整個 workflow 從 fileSelector `*.pdf` 到 Extract 節點 `operation: pdf` 全在處理 PDF。心理：

- **我要把這份改成 .docx，第一步動哪？**
- **我問 ChatGPT 怎麼改，它一口氣把整份 workflow 重寫，我看不出哪裡是「我要的」哪裡是「它順手加的」**
- **跑了一張看似綠燈，但 AI 改名出來變 `null_null.png` — 跟發票那次一樣的症狀，但這次 input 是圖片，我不知道從哪 debug**

### 2. 核心觀念：跨格式改寫只動 4 層中的前 3 層，不動業務規則

把 #03 workflow 想成 4 層堆疊：

| 層 | 內容 | 跨格式時 |
|---|---|---|
| **入口層** | fileSelector（讀哪些檔）| 必動（換副檔名） |
| **Extract / Decode 層** | Extract from File operation / Read 直接拿 string | 通常會動（換 operation 或跳過）|
| **lpCall helper 層** | retry / 429 / RPM throttle 工具層 | 只有 multimodal（圖片）需要動，加 `contents` 參數 |
| **業務規則層** | prompt 目標（叫 AI 做什麼）/ 改名規則 / Write 寫到哪 | **完全不動** |

**新口號**：「**業務規則層不動**」 — prompt 目標、改名規則、Write 路徑這 3 件事永遠不動，跨格式只動上面 3 層。

**為什麼這個分層比舊口號精準**：舊口號「Extract 策略 ≠ 業務邏輯」會讓學員以為「Code 節點業務邏輯段完全不能動」，但實際 9-C/9-D 都會動 1-2 行 binary 取值（那屬於「Extract/Decode 層」滲入 Code 節點，不是「業務規則」）。新口號明確 — Code 節點裡的 prompt 字串、newFilename 拼接邏輯、Write fileName 表達式才是「業務規則」，這些不動。

學員看完這章後內化的話：「我這次只要動入口層 + Extract/Decode 層（圖片再加 lpCall helper 層），業務規則層 0 動。LLM 給我整份就退回去。」

這跟第 5 章紅線 2「不要讓 LLM 直接產出完整 workflow JSON」直接呼應 — **前 3 層只動 2-3 個欄位（圖片再加 2 行 lpCall helper patch），根本不需要整份重寫**。

### 3. 具體 step-by-step

#### 動線總覽（4 步固定）

不管學員手上是 .docx / .xlsx / 圖片 / 純文字，跨格式改寫永遠是這 4 步：

1. **判斷格式** — 學員手上的檔案副檔名是什麼？是有文字層的（docx / xlsx / txt / csv）還是無文字層的（png / jpg / 掃描 PDF）？
2. **選 Extract 策略** — 對照本章「5 格式 dispatch 對照表」，找到對應策略
3. **動前 3 層（最多 3 個地方）** — 入口層 fileSelector 副檔名 + Extract/Decode 層設定 + （只有圖片格式才需要）lpCall helper 層加 contents 參數
4. **業務規則層保持原狀** — Code 節點裡 prompt 目標字串、改名規則、Write 節點 fileName 表達式全部不動

> **跟第 6 章的差別**：第 6 章 walkthrough 是「同格式（PDF）但業務目標換」，動的是業務規則層。本章是「業務目標一樣（檔案改名 + 分類）但格式換」，動的是前 3 層。**兩章合起來涵蓋學員 90% 的課後改寫場景**。

> **n8n 真實 enum 預先說明**：本章下方提到的 Extract from File 節點 `operation` 欄位，n8n 1.x 實際支援的 enum 值是 `csv` / `html` / `fromIcs` / `fromJson` / `ods` / `pdf` / `rtf` / `text` / `xml` / `xls` / `xlsx` / `binaryToProperty`（Codex 直接查 n8n source 確認）。**沒有 `docx` 這個 operation，也沒有「自動偵測類型抽文字」的 text operation 行為**。所以 .docx 不能跟 .pdf 一樣「換 Extract operation 就好」 — 教案下方 9-A 會走「中介格式策略」誠實處理這個 gap。

---

## 9-A：.docx — 用「中介格式策略」（n8n 沒有原生 docx 抽取）

**誠實先講**：n8n Extract from File 沒有 docx 專屬 operation（n8n 1.x 確認）。直接用 `text` operation 會抽到 zip XML 結構不是內文（Word docx 是 zip + XML 結構，`text` operation 會把 zip 內部當純文字解，學員拿到 `<?xml version="1.0"?>...` 開頭的亂碼）。這代表 .docx 不能跟 .pdf 一樣「換 Extract operation 就好」，要走**中介格式策略**。

### 兩條可走路線

**路線 1（推薦給商業學員）：手動 batch 轉 PDF 再走 #03**

學員業務情境通常是「我有一批 .docx 想用 #03 改名」。最快做法是 Word / Pages / LibreOffice 內建批次 export PDF：
- Word：開啟 → 檔案 → 另存新檔 → 選 PDF（或用 macOS 自動化動作 / Win 巨集 batch 跑）
- Pages（Mac）：批次匯出 → PDF
- LibreOffice：Tools → Macros → 批次 ConvertDocuments

轉完直接用既有 #03 處理。零 workflow 改動。

**路線 2（進階學員）：用 HTTP Request node 接 Microsoft Graph / Google Docs API 抽文字**

不在本章範圍（屬於 #06 webhook + 外部 API 的整合教學）。如果學員量大或要全自動化才走這條。

### 不要走的死路（學員會踩的雷）

- ❌ 把 #03 fileSelector 改 `*.docx` + Extract operation 留 `text` → **會抽到 zip XML 亂碼**，AI 拿到 `<?xml version="1.0"?>...` 開頭的東西亂猜檔名
- ❌ 試圖叫 LLM 寫 docx parser 進 Code 節點 → mammoth 之類的 npm 模組 n8n 預設沒裝，學員裝不了
- ❌ 用 Read 直接拿 binary 後 Code 節點手寫 unzip → 走進工程地獄

### 學員實機操作（10 分鐘 — 走路線 1）

1. **批次轉 PDF**：把整個 .docx inbox 在 Word / Pages / LibreOffice 一次 export 成 PDF
2. **直接用既有 #03**：fileSelector / Extract operation / Code 節點全部不動，把轉好的 PDF 丟 batch-inbox 跑

### 範例 prompt（學員問 LLM 確認路線時用）

```
我有 50 個 .docx 報價單想用 #03 batch-error-recovery 改名 + 分類。
我已知 n8n Extract from File 沒有 docx 專屬 operation，也不能用 text operation 直抽（會拿到 zip XML 亂碼）。

請只回我「中介格式策略」的具體執行步驟（路線 1：批次轉 PDF 再走 #03）：
1. 在 Mac / Windows 上怎麼批次把 50 個 .docx 一次 export 成 PDF（給最快做法）
2. 轉完後 #03 要不要動任何設定（我認為不用，請確認）

⚠️ 紅字硬規則：
- 不要建議我改 fileSelector 成 *.docx
- 不要建議我把 Extract operation 改成 text（會抽 zip XML 亂碼）
- 不要建議我寫 Code 節點手 parse docx
- 不要 JSON、不要重寫 workflow

業務規則層 0 改動。
```

### 驗收硬指標（3 條）

1. ✅ .docx 全部已透過 Word / Pages / LibreOffice batch export 成 .pdf，丟 batch-inbox
2. ✅ #03 fileSelector / Extract operation / Code 節點 / Write 節點全部 **0 改動**
3. ✅ 跑 1 份轉好的 PDF → AI 改名輸出合理（例：`20260508_報價單_AA有限公司`）— 跟原 PDF 路線輸出一致

---

#### 格式 B：.xlsx（多一層 — 處理多 sheet 邏輯）

**現況 → 改造**：

```
fileSelector: "*.pdf"  →  "*.xlsx"
operation: "pdf"  →  "xlsx"   ← 這個 enum n8n 真有
```

**比 .docx 多的那一層**：Excel 檔通常有多個 sheet（工作表）。n8n Extract from File 的 xlsx operation 預設行為是「讀第一張 sheet」 — 但學員業務 case 常常不是「永遠取第一張」：

- **常見 case**：客戶清單 .xlsx 第一張 sheet 是「目錄」、第二張才是「客戶資料」
- **常見 case**：報表 .xlsx 多 sheet 是「各部門」，要全部 sheet 一起進 LLM 還是各 sheet 各跑一次？

##### 兩種策略給學員選（依業務複雜度）

**策略 B-1（簡單 — 取第一張 sheet）**：適合「.xlsx 永遠單 sheet」或「我手動把要處理的 sheet 移到第一張」的場景。Extract operation 設 `xlsx`，n8n 預設給第一張，業務規則層拿到的是第一張 sheet 的 row array。

**策略 B-2（複雜 — 多 sheet 都要）**：適合「.xlsx 每張 sheet 都要進 LLM」的場景。需要在 Extract 節點 options 內把「Read All Sheets」打開（n8n UI 上是 Options → Sheet → All）— output 會是「sheet 名稱 → row array」的物件結構，業務規則層需要小幅調整 prompt 加上 sheet 名稱（這就**踩到業務規則層了**，學員要清楚意識到 — 多 sheet 不是純前 3 層改造）。

> **教學重點**：商業學員第一次跨 .xlsx 改寫，**強制走 B-1**。讓他們先把 .xlsx 的「我要哪張 sheet」這個業務決定離開 workflow（手動把目標 sheet 移到第一張、或上傳前先存成只有目標 sheet 的副本）。等流程熟了再升級到 B-2。理由：B-1 的成本是「每次手動整理一下檔案」，B-2 的成本是「workflow 業務規則層被污染」 — 對非工程師學員，前者好維護太多。

##### 範例 prompt（模板 9-B 簡化版，完整見第 4 節）

```
我要把 #03 batch-error-recovery 改成處理 .xlsx 客戶清單，每月 1 份檔案，
我手動把目標 sheet「客戶清單」移到第一張，所以你只要處理「取第一張 sheet」的策略。

請只回我兩個入口節點的設定變更：
1. Read 節點 fileSelector
2. Extract from File 節點 operation

業務規則層不動。AI 改名的 prompt 字串若提到「PDF」這種對人類描述的詞，
也保持原樣 — 我要的是「同一套業務規則處理不同入口」。

不要 JSON、不要重寫 workflow、不要建議多 sheet 處理（我已經決定走 B-1 單 sheet）。
```

##### sample LLM 回應 + 學員會踩的坑

LLM 通常會額外「順手」加 row filter 邏輯（典型擴張），例：

```
1. fileSelector 改成 *.xlsx
2. operation 改成 xlsx

【建議：Code 節點 prompt 補一段】
原本 prompt：「分析以下 PDF 文字，生成語意化檔名」
改成：「分析以下 Excel 客戶清單（每筆 row 是一個客戶），生成語意化檔名」
這樣 Gemini 處理 row array 結構時表現會更好。

【建議】在 Code 節點 loop 內加 row 過濾：
const rows = $input.item.json;
if (!rows.客戶名 || rows.客戶名.trim() === '') return [];  // skip 空白 row
這樣 200 列裡有 5 列空白也不會打亂 batch。
```

**辨認訊號**：上面 3、4 兩條 — 動到 Code 節點業務規則層。

**學員下一步**：模板 5 拒絕。

```
比較你最早的版本（單純改 fileSelector + operation）和現在這個建議：
- 必要的（保留）：fileSelector + operation 兩條
- 新增的擴張（移除）：prompt 字串改寫、空白 row 過濾

我這次只要「同一套業務規則換成跑 xlsx」。row 過濾 / prompt 強化我自己用 #03 跑通後再決定要不要做。請只回 1 和 2。
```

##### 驗收硬指標（4 條）

1. ✅ fileSelector 是 `*.xlsx`
2. ✅ Extract operation 是 `xlsx`
3. ✅ 跑 1 個多 sheet .xlsx → Extract output 是第一張 sheet 的 row array（不是全部 sheet 攤平、不是 binary）
4. ✅ AI 改名後檔名格式合理（例：`20260415_客戶清單_AA有限公司`）— 業務規則層確實沒動，輸出結構跟跑 PDF 時一致

---

#### 格式 C：圖片 .png / .jpg（最大轉折 — 要動 lpCall 用 multimodal）

##### 為什麼這格式特殊

前 4 個格式（pdf / docx / xlsx / csv / txt / md）的共通點：**檔案有「文字層」**。n8n Extract from File 抽得出文字，Code 節點業務規則層拿到的 input 是字串 — 跟 PDF 路線完全一樣，只是字串內容不同。

圖片完全相反：**沒有文字層**。掃描的收據、LINE 截圖、產品照片 — 你 Extract from File 出來只有 binary，沒文字。

於是策略要轉折：**不再走 Extract from File，改用 LLM multimodal**。

n8n #03 用的是 Gemini 2.5 Flash（lpCall helper），它支援 multimodal — 把圖片 base64 餵進去，它「真的看圖」回你內容描述。lpCall 的 contents 結構從「純文字」變成「文字 + inlineData」。

##### lpCall contents 結構從 text 改 inlineData 的具體範例

**原 #03 lpCall 用法**（純文字，see 第 3 章 batch-error-recovery 節點 jsCode）：

```javascript
const prompt = '分析以下 PDF 文字，生成語意化檔名（不含 .pdf）。'
  + '格式：YYYYMMDD_主題_關鍵字（繁體中文）。\n\n'
  + '<PDF>\n' + pdfText.substring(0, 2500) + '\n</PDF>';

const lpResult = await lpCall.call(this, {
  prompt,                              // ← 整個 contents 就一條 text
  gen: { temperature: 0.3, maxOutputTokens: 200 }
});
```

**改造成圖片 multimodal**（input 是 binary 不是 text）：

```javascript
// 從 Read 節點拿 binary base64（注意：item.binary.data.data 是 base64 字串）
const imgBase64 = item.binary.data.data;
const imgMime = item.binary.data.mimeType || 'image/png';

// 預檢圖片大小（lpCall 內建 lpSizeOK 已涵蓋，但這裡 explicit 寫一次給學員看）
if (!lpSizeOK(imgBase64)) {
  results.push({
    json: { status: 'failed', originalName, errorMsg: '圖片超過 18MB inline 上限' }
  });
  continue;
}

// 把 prompt 從「純 text」改成「multimodal contents」
const lpResult = await lpCall.call(this, {
  contents: [{
    role: 'user',
    parts: [
      { text: '分析以下圖片內容，生成語意化檔名（不含副檔名）。'
            + '格式：YYYYMMDD_主題_關鍵字（繁體中文）。'
            + '沒日期就用 ' + today + '。直接回檔名一行。' },
      { inlineData: { mimeType: imgMime, data: imgBase64 } }
    ]
  }],
  gen: { temperature: 0.3, maxOutputTokens: 200 }
});
```

關鍵差異 3 點：

1. **輸入**：原本傳 `prompt` 字串 → 改成傳 `contents` 陣列（裡面是 parts 陣列）
2. **parts 結構**：原本只有 1 個 `{ text: ... }` → 改成 2 個 part：第 1 個是 text 指令，第 2 個是 `{ inlineData: { mimeType, data } }` 帶 base64
3. **lpCall 介面相容性**：Lite Pack 的 lpCall 原本只認 `prompt` 字串（看 #03 jsCode 開頭那段 helper）— **要學員意識到 lpCall helper 內部的 contents 構造可能要小改**。實務上 Lite Pack v1.2 lpCall 的內部就是把 `prompt` 包成 `contents: [{ parts: [{ text: prompt }] }]`，學員只需要在 lpCall 加一個 `contents` 參數讓它直接吃，或者就在外面構好 contents 直接 httpRequest（教案下方 9-C 模板會給兩條路線讓學員選）。

##### lpCall 兩條路線（給學員選）

**路線 C-1（小幅改 lpCall helper）**：在 lpCall 函式內加一段 `if (contents) use contents; else use [{ parts: [{ text: prompt }] }]`。

優點：lpCall 從此同時支援 text 和 multimodal，未來其他 workflow 都能用。

缺點：動到 lpCall helper 層（雖然 helper 層不是業務規則層，但對非工程師學員是「動深一層」）。

**路線 C-2（外面構好 contents 直接 httpRequest）**：放棄 lpCall，在圖片這個 workflow 直接 `this.helpers.httpRequest({ ... contents: [...] ... })`。

優點：lpCall 不動。對 1-2 個圖片 workflow 來說最快。

缺點：失去 lpCall 內建的 retry / 429 處理 / throttle / size check — 全部要自己重寫。對 5 張圖跑一次的學員可以；對每月 200 張掃描收據的就會撞 RPM 限額。

> **教學決策**：**強制走 C-1**。lpCall 加一個 contents 參數的 patch 是**只有 2 行 jsCode**（簽名加 contents 參數 + body.contents 改條件），加完就一次解鎖 multimodal，未來圖片 / 影片 / 音檔 workflow 都用得上。C-2 看起來簡單，但「失去 retry / RPM 處理」這個代價對商業學員的長期維護是地雷。

### 9-C 步驟 1：fileSelector 設定（避開 brace expansion 風險）

n8n docs 只保證 `*` `**` `?` 三個 wildcard。`*.{png,jpg}` 在不同 fileSelector 實作可能不 match。穩妥做法 2 選 1：

**方案 A（推薦）：統一副檔名**
學員 cp 圖片進 batch-inbox 前先全部統一成 .png（macOS Preview / Win 內建檢視器都能 export 成 png）：
```
fileSelector: /files/shared/batch-inbox/*.png
```

**方案 B（混合 png/jpg）：跑兩次或用兩個 Read node**
加第二個 Read 節點走 `*.jpg`，再用 Merge node 合流。Workflow 多 2 個節點但能處理混合。

**不要做的事**：
- ❌ 直接用 `*.{png,jpg}` 不測試就交付學員
- ❌ 用 `*` 然後 Code 節點過濾副檔名（看似聰明但 multimodal 對 .pdf / .txt 等非圖片會直接撞 API 錯誤）

### 9-C 步驟 2：lpCall helper patch（完整 before/after，2 行改動）

打開 #03 的 Code 節點，找到 lpCall 函式定義（line 30-60 區）。下方 before/after **只示範改動的兩行段落**（`// ...省略...` 處保持原 jsCode 不動）— 學員照位置對齊改即可，不是把整段 paste 取代。

**Before（保留 PDF / 文字模式）：**

```javascript
async function lpCall({ prompt, gen = {}, _att = 0 }) {
  if (!prompt || typeof prompt !== 'string') return { ok: false, text: '', error: 'empty prompt' };
  try {
    const r = await this.helpers.httpRequest({
      // ...省略...
      body: {
        contents: [{ role: 'user', parts: [{ text: prompt }] }],
        // ...省略...
      },
    });
    // ...
```

**After（同時相容 PDF/文字 + 圖片 multimodal）：**

```javascript
async function lpCall({ prompt, contents, gen = {}, _att = 0 }) {
  // 雙路徑：圖片用 contents，文字用 prompt
  if (!prompt && !contents) return { ok: false, text: '', error: 'empty input' };
  try {
    const r = await this.helpers.httpRequest({
      // ...省略...
      body: {
        contents: contents || [{ role: 'user', parts: [{ text: prompt }] }],
        // ...省略...
      },
    });
    // ...
```

**改動只有 2 行**（簽名加 `contents` 參數、body.contents 改條件）。其他 helper 邏輯（retry / 429 / RPM throttle）完全不動。

### 9-C 步驟 3：Code 節點業務段呼叫 multimodal lpCall

把原本（PDF 路線）：

```javascript
const prompt = '分析以下 PDF 文字...' + pdfText.substring(0, 2500) + '...';
const lpResult = await lpCall.call(this, { prompt, gen: {...} });
```

替換成（圖片 multimodal）：

```javascript
const imgBase64 = item.binary.data.data;
const imgMime = item.binary.data.mimeType || 'image/png';

if (!lpSizeOK(imgBase64)) {
  results.push({ json: { status: 'failed', originalName, errorMsg: '圖片超過 18MB' } });
  continue;
}

const lpResult = await lpCall.call(this, {
  contents: [{
    role: 'user',
    parts: [
      { text: '分析以下圖片內容，生成語意化檔名（不含副檔名）。格式：YYYYMMDD_主題_關鍵字（繁體中文）。沒日期用 ' + today + '。直接回檔名一行。' },
      { inlineData: { mimeType: imgMime, data: imgBase64 } }
    ]
  }],
  gen: { temperature: 0.3, maxOutputTokens: 200 }
});
```

下方 `lpResult.text` 解析、檔名清理、`results.push` 全部不動（業務規則層 0 動）。

##### 範例 prompt（模板 9-C 完整版見第 4 節）

```
我要把 #03 batch-error-recovery 改成處理圖片（.png — 走方案 A，jpg 我會先 export 成 png），
用 Gemini 2.5 Flash multimodal 看圖回語意化檔名。

請給我三個東西：

1. 入口節點變更：
   - Read 節點 fileSelector 改成 *.png（不要用 *.{png,jpg} brace expansion，n8n docs 只保證 * ** ?）
   - Extract from File 節點 — 圖片不需要 Extract，這個節點該怎麼處理？
     （是刪除？disable？還是其他？選一個並說明）

2. lpCall helper 的 patch（路線 C-1，給完整 before/after 對照）：
   告訴我 lpCall 函式定義那段，before 與 after 完整貼出來（包含函式簽名 + body.contents 那行）。
   只動 2 行（簽名加 contents 參數 + body.contents 改條件），其他 helper 邏輯（retry / 429 / throttle）完全不動。

3. 業務段 Code 節點呼叫端要怎麼換成 multimodal contents：
   給可直接複製貼上的 const imgBase64 = ... + lpCall.call({ contents: [...] }) 完整段落。

⚠️ 紅字硬規則：
- 業務規則層 0 改動（lpResult.text 解析、檔名清理、results.push、Write 節點全部保留）
- 不要 JSON、不要重寫整份 workflow
- 不要建議加 try/catch / 自寫 retry（lpCall 內建已有）
- 不要建議自動檔案類型偵測（我另開一條圖片專用 workflow）
- 不要建議圖片預處理（resize / grayscale）
```

### 9-C ChatGPT 可能歪掉的 5 種樣子

| 變體 | LLM 回應症狀 | 學員下一步 |
|------|------------|---------|
| **A 重寫整份 workflow** | 回 5+ 個節點 JSON，動到 Read / Write / Switch 等不該動的 | 用模板 5 拒絕：「請只回 lpCall 函式 patch 的 before/after，其他節點不要動」 |
| **B 漏改 lpCall 簽名** | 給的 contents 構造對，但 lpCall 函式定義沒加 `contents` 參數 | 「你忘了在 lpCall 函式簽名加 contents 參數，請補完整 patch」 |
| **C 只傳 text 沒傳 inlineData** | 構造的 contents 只有 `{ parts: [{ text: '分析圖片...' }] }`，沒給圖片資料 | 「prompt 沒帶圖片 base64 等於 LLM 看不到圖片，請補 inlineData 段」 |
| **D 自加 streaming / generationConfig 高玩** | 加 `streamGenerateContent` / `responseSchema` 等本工作流不需要的進階參數 | 「我們不需要 streaming，請維持原本 generateContent endpoint」 |
| **E 自寫 retry / try-catch** | 在 Code 節點業務規則層加 try/catch 包 lpCall（lpCall 已有 retry） | 「lpCall helper 已內建 retry，請移除這層 try-catch」 |

##### 驗收硬指標（5 條）

1. ✅ fileSelector 走方案 A（`*.png`）或方案 B（兩個 Read node 各走 `*.png` / `*.jpg`），**不是** `*.{png,jpg}` brace expansion。跑 1 張測試圖片有抓到
2. ✅ Extract from File 節點被 disable（灰色，旁邊有暫停圖示），連線從 Read → Code 直連
3. ✅ lpCall 函式簽名加了 `contents` 參數，呼叫端傳 contents 時走 multimodal、傳 prompt 時走原邏輯（兩種都能跑）
4. ✅ 業務規則層保留：lpCall 的 retry / lpThrottle / lpSizeOK / 檔名清理 + Write 節點都沒動
5. ✅ **真的「看內容」測試**：拿一張簡單名片或收據截圖跑 → AI 改名是「能反映內容語意」的合理檔名（例：`20260508_名片_張先生`、`20260508_收據_全聯_385元`）— **不是檔案 metadata 隨機字串**、**不是 null_null**

##### 圖片格式 size 注意事項

lpCall 內建 `LP.maxInlineBytes = 18 * 1024 * 1024`（18 MB，留 buffer 到 Gemini API 20 MB hard limit）。對下面這些圖片型態夠用：

- ✅ LINE 截圖、手機拍的名片 / 收據（通常 < 2 MB）
- ✅ Office 文件 export PDF 後再截的 page 圖（通常 < 5 MB）

下面這些**會撞上限**，要學員預先處理：

- ❌ 動畫 GIF（單檔常 10-30 MB）— 用 Preview / 線上工具轉成第一幀 PNG 再進
- ❌ 高解析掃描（300dpi 以上的全頁 A4 PNG，常 15-25 MB）— 用 Preview Export 降成 150dpi 或 JPG 80% 品質
- ❌ HEIC（iPhone 預設格式，n8n 對 HEIC 支援不一致）— 在 Mac Preview 開檔 → File → Export 成 PNG / JPG

教 lpCall 內 `lpSizeOK()` 預檢已經會把這類撞上限的標 `failed` 不送 Gemini，但學員要知道為什麼會撞，知道怎麼預先處理。

---

#### 格式 D：.txt / .md / .csv（最簡單 — 跳過 Extract）

##### 為什麼這格式更簡單

.txt / .md 本身就是純文字檔，n8n Read 節點讀進來 binary 解 utf8 就拿到字串。**不需要 Extract from File 節點**。

.csv 在 Extract from File 有專屬 operation `csv`（會幫你解析欄位），但很多商業 case 學員只要「整段 CSV 字串塞給 LLM 讓它語意化摘要」 — 不需要結構化解析。這種 case 也跳過 Extract 走 raw text。

##### 改造路線（兩種給學員選）

**路線 D-1（純文字 + 跳過 Extract）**：適合 .txt / .md / .csv「我只要 LLM 看內容」場景。

```
fileSelector: "*.txt"（先用單一副檔名，n8n docs 只保證 * ** ? 三 wildcard）
Extract from File：disable（保留節點 placeholder 將來方便重啟）
連線：Read → Code 直連
Code 節點 Extract/Decode 滲入段：拿到 binary 後 utf8 decode 成字串 → 餵 lpCall.prompt（原 PDF 路線一模一樣，業務規則層 0 動）
```

⚠️ **混合 .txt / .md / .csv 三副檔名一起跑**：不要用 `*.{txt,md,csv}` brace expansion（與 .png/.jpg 同風險），改用 3 個 Read node 各走一個副檔名 + Merge 合流。或第一次先統一成單一副檔名跑通再擴充。

**路線 D-2（CSV 結構化 + 用 Extract csv operation）**：適合「.csv 每一 row 各跑一次 LLM」場景。

```
fileSelector: "*.csv"
Extract from File：operation = csv（n8n 解析成 row array）
業務規則層：原 PDF 路線改一點點 — input 從「字串」變「row 物件 array」，要 loop 每 row 跑 lpCall（這就踩到業務規則層了）
```

> **教學決策**：第一次跨 .csv 強制走 D-1（整段 CSV 當文字）。理由跟 xlsx 一樣 — 把「結構化處理」這個業務決定推遲到「我跑通 PDF 一樣的形狀後再升級」。

##### Read 節點怎麼拿 binary 變字串

n8n 1.x 的 Read 節點 output 是 `item.binary.data` 物件（含 `data: base64`、`mimeType`、`fileName`）。對純文字檔要解 utf8：

```javascript
const binaryData = item.binary.data.data;  // base64 字串
const text = Buffer.from(binaryData, 'base64').toString('utf8');
// 或者直接走 n8n helper
// const text = await this.helpers.binaryToBuffer(binaryData).then(b => b.toString('utf8'));
```

##### 範例 prompt（模板 9-D 完整版見第 4 節）

```
我要把 #03 batch-error-recovery 改成處理 .txt / .md / .csv 純文字檔，整段內容當字串
餵給 Gemini 做摘要 + 改名（不要結構化解析 CSV）。

請只給我：
1. fileSelector 怎麼寫（同時匹配 .txt .md .csv 三種）
2. Extract from File 節點的處理方式（disable？刪除？換 operation？選一個並說明）
3. Code 節點 Extract/Decode 滲入段（拿 pdfText 那行）要改成「從 binary 解 utf8 拿字串」 —
   給最小 patch，不要重寫整個 Code 節點

業務規則層（prompt 字串、改名 template、Write 節點）全部不動。
```

##### sample LLM 理想回應

```
1. fileSelector（單一副檔名穩妥；混合請走多個 Read node — 見章節「對照表」備註）
   /files/shared/batch-inbox/*.txt

2. Extract from File 節點
   建議 disable（右鍵 Deactivate），保留節點 placeholder。連線從 Read 直接到 Code。
   理由：純文字檔不需要 Extract 抽文字層，binary 解 utf8 就拿到字串。

3. Code 節點 Extract/Decode 滲入段最小 patch（業務規則層不動）
   原本：
     const pdfText = item.json.text || '';
   替換成：
     const rawBinary = item.binary?.data?.data;
     const pdfText = rawBinary
       ? Buffer.from(rawBinary, 'base64').toString('utf8')
       : '';
     // 註：變數名仍叫 pdfText 是為了業務規則層下方所有引用都不用改
     // 雖然語意上現在裝的是 .txt / .md / .csv 內容，
     // 但「同一套業務規則處理不同入口格式」就是要讓變數名穩定

   下方 prompt 構造、lpCall、檔名清理、results.push 全部不動。
```

##### 歪掉變體：LLM 建議改變數名 + 「為了可讀性」refactor

```
為了讓 code 更可讀，我建議：
- pdfText 改名為 fileContent（更通用）
- 把 binary 解 utf8 抽成 helper 函式
- 加一段檢查 binary 編碼（萬一不是 utf8 而是 big5）
```

**辨認訊號**：

- 主動 refactor 變數名（pdfText → fileContent）— 學員沒要
- 抽 helper 函式 — 學員沒要
- 加編碼檢查 — 業務沒要求

**學員下一步**：拒絕。理由講清楚：「我故意保留 pdfText 變數名，因為下方有十幾處引用 — 改名等於動到業務規則層的整段。我這次只要『同一套業務規則處理不同入口』。」

##### 驗收硬指標（4 條）

1. ✅ fileSelector 用單一副檔名 `*.txt`（或 `*.md` / `*.csv` 擇一）— 不用 brace expansion 避開 n8n docs 未明列的風險
2. ✅ Extract from File 是 disable 狀態（不是刪除），連線 Read → Code 直連
3. ✅ Code 節點 jsCode 只動了 `pdfText` 那一行的取值方式（從 `item.json.text` 改成 binary 解 utf8）— 業務規則層（prompt 構造、lpCall、檔名清理、results.push）下方完全沒動
4. ✅ 跑 1 個 .txt → 拿到 raw 字串 → AI 改名輸出合理（例：`20260508_會議紀錄_週會筆記`）

---

### 4. 5 條 prompt 模板（學員可直接複製貼上）

每個模板長度 5-15 行，含「業務規則層不動」紅字硬規則。學員依手上格式選一張貼進 LLM 對話。

#### 模板 9-A：把 #03 改成 .docx（中介格式策略，路線 1）

```
我有一批 .docx 想用 #03 batch-error-recovery 改名 + 分類。
我已知 n8n Extract from File 沒有 docx 專屬 operation，也不能用 text operation 直抽
（會拿到 zip XML 亂碼）。請走路線 1：批次轉 PDF 再走 #03。

請只回我兩件事：
1. 在 Mac / Windows 上怎麼批次把 .docx 一次 export 成 PDF（給最快做法）
2. 轉完後 #03 要不要動任何設定（我認為不用，請確認）

⚠️ 紅字硬規則：
- 不要建議我改 fileSelector 成 *.docx
- 不要建議我把 Extract operation 改成 text（會抽 zip XML 亂碼）
- 不要建議我寫 Code 節點手 parse docx
- 業務規則層 0 改動（我跑既有 #03 就好）

不要 JSON、不要重寫 workflow。
```

#### 模板 9-B：把 #03 改成 .xlsx（強制走 B-1 單 sheet 策略）

```
我要把 #03 batch-error-recovery 改成處理 .xlsx 客戶清單，每月 1 份檔案。
我手動把目標 sheet 移到第一張，所以你只要處理「取第一張 sheet」策略（B-1），
不要建議多 sheet 處理。

請只回兩個前 3 層的設定變更：
1. Read 節點 fileSelector
2. Extract from File 節點 operation

⚠️ 紅字硬規則：業務規則層 0 改動。AI 改名 prompt 若提到「PDF」這種對人類描述用詞也保持原樣。
我要的是「同一套業務規則處理不同入口」，不是「為 xlsx 客製化新邏輯」。

不要 JSON、不要重寫 workflow、不要加 row filter / 空白檢查（我跑通後再決定）。
```

#### 模板 9-C：把 #03 改成圖片（multimodal，路線 C-1）

```
我要把 #03 batch-error-recovery 改成處理圖片（.png — 走方案 A，jpg 我會先 export 成 png），
用 Gemini 2.5 Flash multimodal 看圖回語意化檔名。
請走路線 C-1（lpCall helper 加 contents 參數，不要走 C-2 自寫 httpRequest）。

請給我三件事：

1. 入口節點變更
   - fileSelector：改成 *.png（不要用 *.{png,jpg} brace expansion，n8n docs 只保證 * ** ?）
   - Extract from File 節點：disable / 刪除 / 換 operation 三選一並說明

2. lpCall helper patch（給完整 before/after 對照，2 行改動）
   lpCall 函式定義那段 before 與 after 完整貼出來（包含函式簽名 + body.contents 那行）。

3. Code 節點業務段呼叫端 multimodal contents 替換段
   給可直接複製貼上的「const imgBase64 = ...; const lpResult = await lpCall.call({ contents: [...] })」整段。

⚠️ 紅字硬規則：
- 業務規則層 0 改動（lpResult.text 解析、檔名清理、results.push、Write 節點全部保留）
- 不要重寫整個 Code 節點
- 不要建議自動檔案類型偵測（我另開一條圖片專用 workflow）
- 不要加圖片預處理（resize / grayscale）
- 不要加 retry / try/catch（lpCall 內建已經有）

不要 JSON、不要重寫 workflow。
```

#### 模板 9-D：把 #03 改成 .csv（純文字路線 D-1）

```
我要把 #03 batch-error-recovery 改成處理 .csv（每月匯出的業務報表，整段內容當字串
餵給 Gemini 做摘要 + 改名）。請走路線 D-1（純文字、不要結構化 row 解析）。

請只回三件事：
1. fileSelector 怎麼寫
2. Extract from File 節點處理方式（disable / 刪除 / 換 operation 三選一）
3. Code 節點 Extract/Decode 滲入段「拿 pdfText」那行的最小 patch（從 binary 解 utf8）

⚠️ 紅字硬規則：
- 變數名 pdfText 不要改
- 業務規則層（prompt 構造、lpCall、檔名清理、Write）0 改動
- 不要建議 refactor、抽 helper、加編碼偵測

不要 JSON、不要重寫 workflow。
```

#### 模板 9-E：把 #03 改成 .txt / .md（純文字路線 D-1，多副檔名）

```
我要把 #03 batch-error-recovery 改成同時處理 .txt 和 .md 純文字檔（會議紀錄、筆記、待辦清單），
整段內容當字串餵給 Gemini 做摘要 + 改名。

請只回三件事：
1. fileSelector 同時匹配 .txt 和 .md 怎麼寫（brace expansion）
2. Extract from File 節點處理方式
3. Code 節點 Extract/Decode 滲入段「拿 pdfText」那行的最小 patch

⚠️ 紅字硬規則：
- 變數名 pdfText 保留（下方有 10 多處引用，動了等於動業務規則層）
- 業務規則層（prompt 字串、改名 template、Write）全部 0 改動
- 不要建議「為了可讀性」改名或 refactor

不要 JSON、不要重寫 workflow。
```

---

### 5. 範例 LLM 回應（每模板各一個 ideal + 1 個歪掉變體）

每個模板的 ideal 回應 + 歪掉變體已寫在第 3 節各格式 step-by-step 內。整理成查找表如下，學員看 LLM 回應前先掃這張表 30 秒辨認自己拿到的是哪型：

| 模板 | ideal 回應特徵 | 最常見歪掉變體 | 學員下一步 |
|------|--------------|----------------|----------|
| 9-A docx | 條列 2 條：批次轉 PDF 做法 + 確認 #03 不動（中介格式策略） | LLM 建議改 fileSelector 成 *.docx + Extract operation=text（會抽 zip XML 亂碼）| 拒絕，要求走中介格式策略路線 1：Word/Pages/LibreOffice 批次 export PDF |
| 9-B xlsx | 條列 2 條：fileSelector + operation=xlsx | LLM 加 row filter / 空白檢查（業務沒要） | 模板 5 拒絕 |
| 9-C 圖片 | 三段：入口變更（fileSelector 走方案 A *.png）+ lpCall 2 行 before/after patch + Code 段呼叫端替換 | LLM 「為相容性」重寫整個 Code 節點，或漏改 lpCall 簽名，或只給 text 沒給 inlineData，或加 streaming，或自寫 retry | 模板 5 拒絕，要求回到 before/after 完整對照 |
| 9-D csv | 三段：fileSelector + Extract disable + binary 解 utf8 patch | LLM 改變數名 / 抽 helper / 加編碼偵測 | 拒絕，pdfText 變數名保留 |
| 9-E txt/md | 三段（同 9-D） | 同 9-D | 同 9-D |

> **辨認訊號通用版**（不分模板）：LLM 回應裡只要出現下面任一個關鍵字，就是擴張 — 用模板 5 拒絕：
> - 「為了相容性 / 可讀性 / 可維護性」
> - 「順手 / 另外建議 / 同時建議」
> - 「重寫整個 / 全新 / 改造後的完整 workflow」
> - 「加 try/catch / retry / fallback」（lpCall 內建已有）
> - 「自動偵測檔案類型」（學員沒要混合相容）

---

### 6. 5 格式 dispatch 對照表（學員當 cheat sheet 用，建議列印 A4 貼螢幕邊）

| 格式 | fileSelector 範例 | Extract 策略 | 動 lpCall helper 層？ | 動業務規則層？ | 注意事項 |
|------|------------------|------------|------------|--------------|---------|
| .pdf | `*.pdf` | Extract operation=pdf | ❌ 不動 | ❌ 不動 | 預設 #02/#03 路線 |
| .docx | `*.pdf`（中介策略） | **不能用 Extract** — 走中介格式策略：Word/Pages/LibreOffice 批次 export 成 PDF 再走既有 #03 | ❌ 不動 | ❌ 不動 | n8n Extract from File 沒有 docx 專屬 operation；用 text operation 直抽會拿到 zip XML 亂碼 |
| .xlsx | `*.xlsx` | Extract operation=xlsx | ❌ 不動 | ❌ 不動（B-1 單 sheet） | 預設取第一張 sheet；多 sheet 強制走 B-1（手動把目標 sheet 移第一）；B-2 多 sheet 會踩到業務規則層 |
| .csv（純字串） | `*.csv` | Extract disable，Read → Code 直連 | ❌ 不動 | 動 1 行（pdfText 取值方式） | 整段 CSV 當文字餵 LLM；不結構化解析 |
| .csv（結構化） | `*.csv` | Extract operation=csv | ❌ 不動 | 動（loop row 跑 lpCall） | 進階用法，初次強制走純字串路線 |
| .txt / .md | `*.txt`（單一）或兩個 Read 各走 `*.txt` / `*.md`（混合） | Extract disable，Read → Code 直連 | ❌ 不動 | 動 1 行（pdfText 取值方式） | ⚠️ 不要用 `*.{txt,md}` brace expansion（與 .png/.jpg 同風險）；binary 解 utf8 即可；注意 BOM（極少見） |
| .png / .jpg | `*.png`（方案 A 統一）或兩個 Read 各走 `*.png` / `*.jpg`（方案 B 混合） | Extract disable，Read → Code 直連 | **動**（lpCall 加 contents 參數，2 行 patch — 簽名 + body.contents） | 動（呼叫端 prompt 改成 contents + inlineData，業務規則層的 lpResult.text 解析以下不動） | ⚠️ 不要用 `*.{png,jpg}` brace expansion（n8n docs 只保證 `*` `**` `?`）；18MB 上限；HEIC / 高解析掃描 / 動畫 GIF 要預先處理 |

**列印建議**：把這張表 + 第 5 節「LLM 回應辨認訊號」+ 5 條模板各一張印 A4，雙欄排版，貼螢幕邊。每次要跨格式改寫前掃 30 秒。

---

### 7. 驗收標準（章末通用 5 條 — 不分格式都要過）

跨格式改寫不論走哪條路線，學員自驗時都要對 5 條：

- [ ] **前 3 層改了，業務規則層沒動**：n8n UI 點 Code 節點 → 看 jsCode 的 prompt 字串、改名 template、results.push 結構 — 跟原 #03 完全一樣（除非走圖片或 D-1 純文字路線那 1 行 binary 取值是 Extract/Decode 層滲入，不算業務規則層）
- [ ] **fileSelector 對得上格式**：副檔名清單跟學員手上實際檔案副檔名一字不差
- [ ] **Extract 節點該 disable 的 disable，該換 operation 的換**：對照第 6 節 dispatch 對照表的「Extract 策略」欄
- [ ] **跑 1 個測試檔通過 + AI 改名肉眼看合理**：不是 null_null、不是 binary garbage 截字串、檔名語意能反映檔案內容
- [ ] **跑 5-10 個測試檔通過率 ≥ 80%**：少數邊界 case（圖片是純圖無可辨識內容、xlsx 第一張 sheet 真的是空目錄）記備注人工處理，不為 1-2 張改流程（紅線 8 / 第 6 章 walkthrough Step 6）

---

### 8. 常見錯誤 + 怎麼解

#### 錯誤 1：「.docx 我把 fileSelector 改 *.docx + Extract operation 改 text，AI 改名輸出亂猜的字」

**症狀**：fileSelector + operation 都改了，Extract 沒紅燈，但 AI 改名出來變成 `20260508_文件_xml1document` 這種看似有抓到內容但跟原 docx 內文無關的字串。

**根因**：n8n 的 `text` operation 不會「自動偵測類型抽純文字」 — 它把檔案 binary 當純文字解。Word .docx 是 zip + XML 結構，`text` operation 會抽到 zip 內部的 `<?xml version="1.0"?>...` XML 標籤亂碼。AI 拿到的 input 不是 docx 內文，是 zip XML。

**解法**：放棄直抽路線，走 **9-A 中介格式策略路線 1** — Word / Pages / LibreOffice 批次 export 成 PDF，再走既有 #03（fileSelector / Extract operation / 業務規則層全部回到 PDF 路線預設）。

**預防**：把第 6 節 dispatch 對照表貼螢幕邊 — .docx 那行明確寫「不能用 Extract」+ 走中介策略。

#### 錯誤 2：「圖片 multimodal 沒看 maxInlineBytes，撞 Gemini 20MB API limit」

**症狀**：跑了 10 張圖，前 8 張綠燈、第 9 張紅燈，Code 節點錯誤 `Request too large` 或 `Payload exceeds maximum size`。

**根因**：第 9 張可能是 HEIC（iPhone 拍）或 300dpi 全頁掃描，binary > 20 MB。

**解法**：

- 短期：把那張圖在 macOS Preview 開 → File → Export → 選 JPG 80% 品質，重新放回 inbox
- 長期：lpCall 內建 `lpSizeOK()` 預檢已經會把這類撞上限的標 `failed` — 確認 Code 節點呼叫端有用 `lpSizeOK(imgBase64)` 預檢（看 9-C 步驟 3 的範例段落，已經放進去了）

**預防**：模板 9-C 的 ideal 回應段落有 `lpSizeOK` 預檢，學員替換 Code 節點時不要把這段砍掉。

#### 錯誤 3：「.xlsx 多 sheet 不知道 LLM 拿到哪張，AI 改名跑出莫名其妙的內容」

**症狀**：跑了一份 5 sheet 的 .xlsx，AI 改名出來的檔名是 sheet 名「目錄」「索引」這種沒業務意義的字。

**根因**：n8n Extract from File `xlsx` operation 預設讀第一張 sheet — 學員的 .xlsx 第一張剛好是「目錄」sheet，真正想處理的「客戶清單」在第二張。

**解法（B-1 路線）**：

- 在 macOS Numbers / Excel 裡把目標 sheet 移到第一張，存檔
- 或上傳前先存一份只有目標 sheet 的副本（`xxx-清單only.xlsx`）

**解法（B-2 升級路線，不建議第一次跨格式就走）**：

- Extract 節點 Options → Sheet → 設為 `Read All Sheets` 或指定 sheet 名稱
- 業務規則層 prompt 加上 sheet 名稱讓 LLM 知道在處理哪張 — **這就踩到業務規則層了**，要清楚意識到這不是純前 3 層改造

**預防**：跨 .xlsx 改寫第一次強制走 B-1，把「我要哪張 sheet」這個業務決定離開 workflow。

#### 錯誤 4：「圖片 fileSelector 用了 *.{png,jpg} brace expansion，但跑起來只抓到 .png 不抓 .jpg（或反過來）」

**症狀**：學員在 batch-inbox 放了 5 張 .png + 5 張 .jpg，跑 Read 節點只跑 5 張（其中一邊副檔名），另一邊全沒進。

**根因**：n8n docs 只保證 `*` `**` `?` 三個 wildcard。`*.{png,jpg}` brace expansion 在不同 fileSelector 實作不一定 match — 不是穩定可靠的寫法。

**解法**（2 選 1）：

- **方案 A（推薦）**：把 jpg 全 export 成 png（macOS Preview / Win 內建檢視器都能 batch export），fileSelector 統一用 `*.png`
- **方案 B**：workflow 加第二個 Read 節點走 `*.jpg`，再用 Merge node 合流（多 2 個節點，但能處理混合）

**預防**：模板 9-C 已強制走方案 A（先 export 成 png）；對照表 .png/.jpg 那行也明確標 ⚠️ 不要用 brace expansion。第一次跨圖片改寫直接走方案 A。

---

### 9. 回到課程動線

#### 這一章的位置

**post-llm 系列「實用篇」收尾**。前 8 章的關係是：

- ch1-2：核心觀念 + 6 步流程骨架
- ch3-4：步驟 1-3 / 4-6 詳解
- ch5：紅線 + 章末對照表
- ch6：完整 walkthrough（同格式但業務目標換）
- ch7：錯誤分流
- ch8：環境設定
- **ch9（本章）：跨格式改寫（業務目標一樣但格式換）**

第 6 章 + 第 9 章合起來涵蓋學員 90% 的課後改寫場景。

#### 走完本章後學員應該能做

- 拿到 .docx / .xlsx / .csv / .txt / .md / 圖片 任一格式 — 在 30 分鐘內把 #03（或 #02）改成處理該格式
- 看到 LLM 回應 30 秒內辨認「是純前 3 層改造」還是「擴張到業務規則層」，後者拒絕
- 列印第 6 節 dispatch 對照表貼螢幕邊，每次改寫前掃 30 秒

#### 進階動線（給走完本章還想再深入的學員）

**進階 1：混合格式 inbox**（同一資料夾混合 .pdf / .docx / .png）

回 **#10 folder-organize**（Lite Pack 14 個 workflow 之一）為基底 — **不是改 #03**。理由：#10 設計上就有 Switch 節點按副檔名分流到不同 Extract 策略，本來就是混合格式 inbox 的對應 workflow。

**進階 2：xlsx 結構化處理（B-2 路線）**

走 #03 的 B-2 路線（Extract operation=xlsx + Read All Sheets + 業務規則層加 sheet 名稱 prompt）— 這時就要承認動到業務規則層，跑驗收的標準從第 7 節 5 條變成第 6 章 walkthrough Step 5 那種「精準型 LLM 回應 + sample 驗證」。

**進階 3：圖片更深的應用（OCR 結構化、產品照片分類、收據拆帳）**

從本章 9-C 模板的 multimodal 為基底，把 prompt 從「生成檔名」升級到「抽結構化 JSON」（例：收據拆帳場景，prompt 要 Gemini 回 `{ vendor, items[], total, date }`）— 這時 prompt 工程的權重會超過格式改造的權重，改去看 Lite Pack `#08-receipt-itemize`（如有）或自己參考 prompt-engineering 系列課程。

#### 章末「我跑完了」 / 「我卡在 X」 / 「我想做 Y」三條動線

| 學員心理 | 去哪一章 |
|---------|---------|
| 「我跨 .docx 跑通了，想試另一格式」 | 同章選下一個格式重跑（5 個格式各 30 分鐘 = 一個下午跑完） |
| 「我跨 .xlsx 跑紅燈了，看不懂錯誤」 | 第 7 章錯誤分流 |
| 「我把 LLM 給的整份 JSON 直接匯入結果炸了」 | 第 5 章紅線 2 + 紅線 5 |
| 「圖片我做完了，想擴大到產品照片分類」 | 上面進階 3 |
| 「我有 200 個檔案混合 .pdf / .docx / .png」 | 上面進階 1（#10 folder-organize 為基底） |
| 「我做完整章了，想再回去看核心觀念」 | 第 1 章 timeline Story A/B + 第 2 章骨架 |

---

## 設計記錄（Phase A 設計筆記）

第 9 章是新章節，沒有「原 HTML 空話診斷」。本節記錄設計決策依據，供 Codex audit + 未來維護參考。

### 9.1 設計依據（來自使用者反饋）

**反饋來源**：使用者明確指出「改寫成其他格式是最容易被學員需要的調整方向」。

**對應到課程動線**：post-llm 系列前 8 章把「同格式（PDF）但業務目標換」教完了（第 6 章 walkthrough）。**「業務目標一樣但格式換」這條是平行軸的另一半，沒有被任何章節覆蓋**。第 9 章補上這個 gap。

### 9.2 為什麼選 5 個格式（docx / xlsx / png+jpg / csv / txt+md）

對應「商業學員結業後第一個業務需求」最高頻 5 種：

| 格式 | 商業 case | 頻率（依 Lite Pack 課後問卷反饋） |
|------|----------|---------------------------------|
| .docx | Word 報價單 / 會議紀錄 / 通知單 | 高 |
| .xlsx | Excel 客戶清單 / 業務報表 / 庫存表 | 高 |
| .png/.jpg | LINE 截圖 / 名片 / 收據 / 產品照 | 中 |
| .csv | 業務報表匯出 / 系統 dump | 中 |
| .txt / .md | 會議紀錄 / 待辦清單 / 筆記 | 低-中 |

**沒選的格式**（刻意排除，避免章節過長）：

- .json / .xml — 非典型商業學員 case（程式工程 / API 串接居多）
- .heic / .tiff — 走「先 export 成 png/jpg」fallback
- 影片 / 音檔 — 走 Gemini multimodal 但流量 / size 處理跟圖片差太多，獨立章節
- .pptx — 商業 case 較少，且 PowerPoint export 成 PDF 後走 PDF 路線最直接

### 9.3 為什麼把「業務規則層不動」當核心觀念（取代舊口號「Extract 策略 ≠ 業務邏輯」）

**根因**：商業學員第一次用 LLM 改 workflow，最常踩的不是「LLM 改錯」而是「LLM 改太多」。看 ch5 紅線 2 + ch6 walkthrough Step 6 都在處理同個問題的不同面向。本章是這個 mental model 的第三個應用場景：「跨格式」這種看起來很大的改造，實際上只動 2-3 個欄位 — 學員一旦把這條觀念內化，後續任何「我要改 X」的對話都能控制 LLM 不擴張。

**為什麼用「業務規則層不動」取代「Extract 策略 ≠ 業務邏輯」**：舊口號的問題是學員會以為「Code 節點業務邏輯段完全不能動」，但實際 9-C / 9-D 都會動 1-2 行 binary 取值（屬於 Extract/Decode 層滲入 Code 節點）。新口號用 4 層分層精確定位：「業務規則 = prompt 目標 + newFilename 拼接 + Write fileName 表達式」，這 3 件事永遠不動，其他 3 層按格式需要動。

### 9.4 圖片 multimodal 路線決策（C-1 vs C-2）

**強制走 C-1（lpCall 加 contents 參數，2 行 patch）**而不是 C-2（外面構好 contents 直接 httpRequest）的理由已在第 3 節格式 C 內寫清楚。這裡補充一個 meta 理由：

C-2 看起來「不動 lpCall」，但實際上失去 retry / 429 / RPM 處理 — **這就違反了 4 層分層的「業務規則層不動」口號**（C-2 是把 lpCall 整個 helper 跳過，等於動到 infrastructure 層比動業務規則層還深）。C-1 反而是真正最小改動 — lpCall helper 加 2 行讓它支援 multimodal，這 2 行屬於 lpCall helper 層，不算業務規則也不算 Extract 策略，是「infrastructure 一次性升級」。升級完整個 #03 / #02 / 未來其他 workflow 都受惠。

### 9.5 待裁決小議題（給 Codex audit + user 看）

- **n8n Extract operation 的 enum 名稱（已隨 Codex audit d8de790f 修正）**：原教案曾寫「.docx 走 `operation: text`」是基於對 n8n 1.x enum 的不正確假設。Codex 直接查 n8n source 確認真實 enum 是 `csv / html / fromIcs / fromJson / ods / pdf / rtf / text / xml / xls / xlsx / binaryToProperty`，且 `text` operation 對 .docx 直抽會拿到 zip XML 亂碼。本章 9-A 已改為「中介格式策略」（路線 1：批次轉 PDF 再走 #03）。對照表 .docx 行也對應改成「不能用 Extract」。

- **lpCall 2 行 patch 的具體版本相依**：本教案 9-C 步驟 2 的 lpCall before/after patch，**假設 #03 lpCall 函式定義跟 batch-error-recovery v0.9 jsCode 一致**。如果未來 #03 升級 v1.0+ 換了 helper 寫法，本章 9-C 步驟 2 的 before/after 段需要對應更新。建議在 Codex audit 時順便檢查 lpCall 是否已演進。

- **xlsx B-2 多 sheet 路線是否要寫進章節**：目前 9.5 進階 2 只用一段帶過。如果使用者反饋顯示 B-2 需求很高，下次迭代可考慮把它升級到「格式 B-bonus」獨立段落。

- **HEIC / 高解析掃描的處理**：目前第 3 節格式 C size 注意事項只給「macOS Preview Export」單一解。對 Windows 學員（用 PC 跑 n8n self-host 的 case）需要補一個 Windows 對應方案（建議用「線上轉檔工具 cloudconvert.com」+ 警告「不要傳含敏感資料的檔案」）。第一次 Codex audit 時確認是否需要補。

- **核心口號用詞精準度（已隨 Codex audit d8de790f 升級）**：原口號「Extract 策略 ≠ 業務邏輯」會讓學員以為 Code 節點業務邏輯段完全不能動，但實際 9-C / 9-D 都會動 1-2 行 binary 取值。已升級為 4 層分層 + 「業務規則層不動」新口號（第 2 段表格定義 4 層 + 業務規則 = prompt 目標 + newFilename 拼接 + Write fileName 表達式）。整章後續引用已同步換成「業務規則層 0 動」/「踩到業務規則層」用詞。

- **fileSelector brace expansion 風險（已隨 Codex audit d8de790f 修正）**：原 9-C 步驟用 `*.{png,jpg}` brace expansion，但 n8n docs 只保證 `*` `**` `?` 三個 wildcard。已改成方案 A（統一 .png）/ 方案 B（兩個 Read node 各走 .png / .jpg）2 選 1，模板 9-C 強制走方案 A；對照表 .png/.jpg 行已對應更新。.txt / .md 場景 `*.{txt,md}` 暫時保留（屬於同類風險，但 .txt/.md 的學員實際 case 通常單一副檔名居多，下次 Codex audit 時可確認是否一併改）。

---

## Phase C — 預期 HTML 章節結構（給 lesson-writer 後續用）

第 9 章作為新章節，沒有現成 HTML。lesson-writer 後續產出 HTML 時建議結構：

| HTML 區塊 | 對應教案章節 | 大小 |
|----------|-------------|-----|
| Hero / Lead | 1（學員此時的痛點） | 短 (3-4 段) |
| 核心觀念 callout | 2（核心觀念） | 1 段 + 加重 box |
| 動線總覽圖 | 3 動線總覽 | 4 步固定 + 圖示 |
| 格式 A.docx 區塊 | 3 格式 A | 5 個 sub-step + sample 對話 + 4 條驗收 |
| 格式 B.xlsx 區塊 | 3 格式 B | B-1/B-2 兩策略對照 + sample + 4 條驗收 |
| 格式 C 圖片區塊（**最大段，建議獨立 anchor**） | 3 格式 C | 介紹 + lpCall 兩路線 + 步驟 1 fileSelector 方案 A/B + 步驟 2 lpCall before/after 2 行 patch + 步驟 3 Code 段呼叫端替換 + 5 種歪掉變體表 + size 注意 + 5 條驗收 |
| 格式 D 純文字區塊 | 3 格式 D | D-1/D-2 兩策略 + binary 解 utf8 patch + 4 條驗收 |
| 5 條 prompt 模板（可複製 box） | 4 | 5 張 code box 加複製按鈕 |
| LLM 回應辨認查找表 | 5 | 5 列表格 + 通用辨認訊號 callout |
| 5 格式 dispatch 對照表（cheat sheet） | 6 | 7 列 6 欄表（含 csv 兩種策略） |
| 通用驗收 5 條 | 7 | checkbox 列表 |
| 常見錯誤 4 條（含症狀 / 根因 / 解 / 預防四欄） | 8 | 4 個 expandable card |
| 章末動線（去哪章 + 進階 3 動線） | 9 | 6 列導引表 |

**字數預估**：教案 .md 約 880 行（與 ch3 / ch4 同量級）。HTML 預估 1100-1300 行（HTML 加 wrapper / nav / metadata 後）。

---
