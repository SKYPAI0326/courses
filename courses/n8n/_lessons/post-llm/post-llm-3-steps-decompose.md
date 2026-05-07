---
unit_id: post-llm-3-steps-decompose
title: 步驟 1-3 真詳解 — 拆需求、讀 JSON、限定範圍
course: n8n / AI 資料工廠
chapter: 第 3 章 / 8（post-llm 系列：課後用 LLM 改 workflow）
description: 用 LLM 改 workflow 的前三步，含可直接複製的 prompt 模板與 sample 回應
audience: 商業培訓非工程師、課後用網頁版 LLM（ChatGPT / Claude / Gemini）改 workflow
prerequisite: 已跑過 Lite Pack 14 個 workflow 至少 1 次；理解 #02 PDF AI 改名範例
delivery: 文字導向 HTML 章節（無印風）
created: 2026-05-07
codex_audit: f3f95415
codex_verdict: actionable（已修補）
last_updated: 2026-05-07
---

# 步驟 1-3 真詳解 — 拆需求、讀 JSON、限定範圍

> **本章重設計教案** · 對應 `courses/n8n/lessons/post-llm-3-steps-decompose.html`

## 重設計內容

## 第 3 章重設計：步驟 1-3 真詳解

### 1. 學員此時的痛點

學員看完第 2 章骨架，到第 3 章他/她要動手。心理狀態：

- **4 格便箋我會填嗎？我寫『發票 PDF』夠嗎？**
- **JSON 怎麼複製出來？credential 真的會被刪嗎？**
- **告訴 LLM「只改節點 X」要怎麼說？我不知道節點叫什麼**
- **如果 LLM 給我整份 JSON，我怎麼判斷是「不是只回節點區段」？**

### 2. 核心要傳遞的 1 個觀念

**前 3 步是地基：步驟 1 寫不清楚，後面 LLM 會自己補 → 步驟 2 沒驗收，後面改錯沒人發現 → 步驟 3 不限範圍，LLM 會重寫整份。地基歪了，後面 30 步都白費。**

### 3. 具體 step-by-step（含可驗收動作）

#### 步驟 1：拆需求（10-15 分鐘，全人工）

1. **打開 4 格便箋範本**（紙、Notes、便利貼皆可）
2. **填第 1 格「原 workflow 編號」**
   - 動作：寫「#XX-XXX」+ 一行「目前在做什麼」
   - **驗收標準（具體例）**：
     - ✅ 可接受：「我要拿 #02 PDF AI rename 改成處理發票」— 直接寫 workflow 編號 + 業務目標一行
     - ✅ 可接受：「複製一份 #02 → 改 prompt 加分類欄位」— 說明改什麼也算
     - ❌ 不可接受：「PDF 工作流」— 沒指名是 #02 還是 #06，不算對；請補 workflow 編號
3. **填第 2 格「目標 input」**
   - 動作：寫「文件類型 + 數量 + 來源資料夾 + 4-6 個關鍵欄位名」
   - **驗收硬指標**：填好的 input 必須包含「具體欄位名」（例：「賣方統編」「稅後合計」），不能只寫「發票資訊」
4. **填第 3 格「目標 output」**
   - 動作：寫「成品檔案/紀錄的格式 + 命名規則 + 存放位置」
   - **驗收硬指標**：output 規則要寫到「肉眼比對能驗證」的程度。例：`{供應商名}_{發票日期}_{稅後金額}.pdf` 完整可變數
5. **填第 4 格「必保留的節點」**
   - 動作：在 n8n UI 看一眼 workflow，把「不應該動」的節點名稱抄下來
   - 驗收：至少寫出 trigger 名 + 1 個其他節點，避免後續 LLM 重寫整份
6. **自驗：對人講 1 分鐘**
   - 動作：對另一個人/或對著手機錄音講一遍 4 格內容
   - **驗收（具體例 — 取代抽象「沒打結」）**：
     - ✅ 算過：你能在 60 秒內，依序講出「原 workflow 編號 #02 → input 是供應商發票 PDF（200 張/月，4 個欄位：賣方/統編/稅後合計/發票日期）→ output 改名為 `{YYYYMMDD}_發票_{賣方名}_{稅後合計}.pdf` → 必保留 4 個 trigger/節點」 — 結構完整 + 可量化
     - ✅ 算過：對方聽完不需要追問，能複述「你要把 200 張供應商發票改名」
     - ❌ 不算過：你講超過 90 秒還沒講完 4 格 → 表示便箋寫太散
     - ❌ 不算過：對方追問「你說的『發票資訊』是什麼意思？」「output 的格式怎麼長的？」 → 表示便箋第 2/3 格寫太抽象，回去補具體欄位名 / 命名格式

#### 步驟 2：讀 JSON（5-10 分鐘，學員 + LLM）

1. **n8n UI export workflow（不含 credential）**
   - 動作：在 workflow 開啟畫面，點右上角三個點 → Download → 確認跳出視窗的選項是「Without credentials」（如果不是，切換）
   - **驗收硬指標**：下載到的 .json 檔，用 VS Code 或記事本打開，按 Cmd+F 搜尋這 4 個字串：`apiKey`、`accessToken`、`password`、`token`，**4 個全部找不到**才算過
2. **打開你慣用的網頁版 LLM**（ChatGPT / Claude / Gemini）
3. **貼模板 2 + JSON**（見下方第 4 節）
4. **驗收 LLM 回應**
   - 動作：讀 LLM 回的「節點清單」，到 n8n UI 對照「節點數量是否一致 + 名稱對得上」
   - **驗收硬指標**：
     - **(a) 節點數量正確**：n8n UI 編輯器畫面數一遍節點圖示有幾個（5 個就 5 個），LLM 回的清單編號也要 5。差 1 個都不行。
     - **(b) 至少 80% 節點角色對得上**（具體例）：
       - ✅ 算對：LLM 說「Read PDF — 讀 /files/pdf-inbox/ 內所有 PDF，輸出每張的 binary」→ 你在 n8n UI 看到節點名是「Read PDF」+ parameter 的 path 是 `/files/pdf-inbox/` → 完全對應 = 算對
       - ✅ 算對（容許小落差）：LLM 說「Code 節點打 Gemini API」實際你看到 Code 節點裡用 `this.helpers.httpRequest` 呼叫 Gemini → **核心動作（呼叫 Gemini）對 + 細節（用什麼 helper）有落差**= 算對
       - ❌ 不算對：LLM 說「Read PDF — 從 Google Drive 讀 PDF」實際你看到 path 是 `/files/pdf-inbox/`（本機路徑）→ **資料來源根本講錯** = 不算對，回頭追問「Read PDF 節點的 path 寫的是 `/files/pdf-inbox/`，不是 Google Drive，請重講這個節點的角色」
       - ❌ 不算對：LLM 把「Code: AI 改名」說成「Code: 一般資料處理」→ **節點意圖完全失準** = 不算對，回頭追問
       - **量化方式**：5 個節點裡，你認為「對」的至少要 4 個（80% = 4/5）。3 個（60%）以下表示 LLM 看 JSON 的能力對你的 workflow 不可靠，換另一家 LLM（或重貼模板 2 + 補一段 workflow 中文描述）

#### 步驟 3：限定修改範圍（10-15 分鐘，學員 + LLM 多輪）

1. **決定「我要動哪幾個節點」**（基於步驟 1 的便箋）
   - 動作：在 4 格便箋的「目標 output」對照節點清單，圈出 1-3 個要改的節點名
2. **在 n8n UI 備份這幾個節點**
   - 動作：點要改的節點 → Cmd+C → 貼到一個 .txt 檔（命名 `XX-backup.txt`）
   - 驗收：.txt 檔有節點 JSON 內容（看到 `{ "parameters": ...`）
3. **貼模板 3 給 LLM**（見下方第 4 節）
4. **驗收 LLM 回的 JSON**
   - **驗收硬指標 1（區段 vs 整份）**：看 LLM 回的第一個非空白字元和第二行：
     - 第一行 `{` 第二行 `"name":` → **整份**（要追問）
     - 第一行 `{` 第二行 `"parameters":` → **單個節點區段**（OK）
     - 第一行 `[` → 多個節點陣列（OK）
   - **驗收硬指標 2（節點名沒被改）**：LLM 回的節點裡 `"name":` 那行的值，必須跟你 n8n UI 上看到的節點名一字不差。LLM 偶爾會「順手」改名（例：把「Code」改成「Code: AI 改名」）— 這會讓步驟 5 的回報失準
5. **如果是整份 JSON**：追問模板（見下方）
6. **【硬性前置】先 Duplicate 一份 -edit workflow，再替換**

   <span style="color:#c00;font-weight:700;">⚠️ 紅字硬規則：步驟 3 的所有替換動作只發生在 -edit workflow，不動原版。</span>

   - **為什麼**：你要替換的 JSON 是 LLM 草稿，跑壞會壞節點 / 連線 / 甚至 n8n 編輯器顯示。在 production workflow 上直接貼，等於拿活的訂單系統當實驗田 — 一旦不小心又把 Active 切回 ON（n8n 介面手滑常事），就真的觸發 200 張 LLM API call 燒錢、或誤改 production 資料庫。
   - **動作（依序）**：
     1. n8n UI 左側選單 → Workflows → 找到原 #02 → 滑鼠移到該行 → 右側出現 ⋮ 三點按鈕
     2. 點 ⋮ → 選「Duplicate」（不是 Open / Share / Delete，看清楚）
     3. n8n 自動產生新檔，預設名稱長這樣：`02-pdf-ai-rename Copy`
     4. 點該新 workflow 的標題 → 進編輯器 → 點頂部標題列 → 改名為 `02-pdf-ai-rename-edit`（**結尾加 `-edit` 後綴**，這是全課統一規約，第 4 章測試時要靠它識別）
     5. 確認新 workflow 右上角 Active 開關是「灰色 OFF」（Duplicate 預設會關，但仍要肉眼確認一次）
   - **驗收硬指標**：
     - ✅ Workflows 列表現在有兩條：原版 `02-pdf-ai-rename` + 新版 `02-pdf-ai-rename-edit`
     - ✅ 你接下來貼 JSON 的瀏覽器分頁，網址列尾巴的 workflow ID 不是原版的 ID
     - ❌ 如果你發現自己正在原版 workflow 上要按 Paste，**Cmd+Z 撤銷 → 退回此步重做**

7. **替換到 -edit workflow 的 n8n UI**
   - 動作：**確認你在 `-edit` workflow 編輯器**（看頂部標題列） → 點要改的節點 → 右鍵 Paste → 貼上 LLM 給的 JSON
   - 驗收：節點還在原位、連線沒斷、節點名相同
   - **再驗一次**：頂部標題列必須顯示 `02-pdf-ai-rename-edit`（不是原版名）

### 4. 完整範例 prompt 模板

#### 模板 1（步驟 1 自我檢查，選用）

```
我要改 n8n workflow #02-pdf-ai-rename（合約改名版，目前抓甲乙方+合約金額+簽訂日）。
目標 input：供應商發票 PDF，每月 200 張，每張含：
  - 賣方公司全名
  - 統編
  - 品項清單
  - 稅後合計（金額含元）
  - 發票日期（YYYYMMDD）
目標 output：改名後 PDF，命名格式 {YYYYMMDD}_發票_{賣方名}_{稅後合計}.pdf，存到 /files/pdf-renamed/
必保留節點：Manual Trigger、Read PDF、Extract PDF Text、Write（4 個都不能換掉）

請問我的需求有哪一格還沒講清楚？只指出空白，不要幫我補。
```

#### 【SOP-A】`[貼 JSON]`（整份 workflow JSON）怎麼擷取

**這是模板 2 用的 — 你要給 LLM「整份 workflow 結構」**

1. n8n UI 點該 workflow → 編輯器右上角 ⋮ 三點按鈕 → **Download**
2. 跳出對話框，**勾選「Without credentials」**（如果預設沒勾，自己勾起來）→ 確認下載
3. 下載到的 `.json` 檔，用 VS Code 或記事本打開 → Cmd+A 全選 → Cmd+C 複製
4. **貼之前最後檢查**（搜尋 4 個字串都應找不到）：`apiKey` / `accessToken` / `password` / `token`
   - 4 個全找不到 = OK
   - 任一個搜得到 = 你下載時沒勾「Without credentials」，重做步驟 1-2
5. **token 量大概**：典型 5-10 節點 workflow JSON 在 5K-30K tokens 之間，貼 ChatGPT/Claude/Gemini 的網頁版都吃得下；若超過 50K（>40 個節點），分段貼

#### 模板 2（步驟 2 讀 JSON）

```
我是 n8n 非工程師使用者，請以結果為主、不解釋原理。
以下是一份 n8n workflow JSON（已移除 credential）。請：
1. 用一段話講它做了什麼。
2. 列出每個節點的角色與資料流向（節點名稱 → 它輸出什麼 → 下一個節點吃什麼）。
不要建議改進、不要寫程式碼。

[貼 JSON]    ← 這是 SOP-A 步驟 3 複製到的整份 workflow JSON
```

#### 模板 3（步驟 3 限定修改範圍）

```
我是 n8n 非工程師使用者，請以結果為主、不解釋原理。
基於剛才那份 workflow，只改節點「Code: AI 改名」（其他節點不動）。
我要的修改：
- prompt 字串改成抽取賣方公司全名、稅後合計、發票日期（YYYYMMDD）
- 檔名 template 改成：{YYYYMMDD}_發票_{賣方名}_{稅後合計}.pdf
- 類型欄位固定填「發票」，不要讓 AI 自己判斷
- 其他邏輯（fallback、parseMethod、httpError 處理）全部保留

請回傳「只有這個 Code 節點」的 JSON 區段（不要整份 workflow）。
回應格式要求：直接給 JSON 物件，最外層 `{` 後面第二行是 `"parameters":`，不要 markdown code fence。
```

#### 模板 3-追問（LLM 給整份時）

```
你給的 JSON 是整份 workflow（最外層有 "name" 和 "nodes"）。
我只要 Code 節點的單個 JSON 物件（從 { "parameters": 開始，到 } 結束）。
請重新只給這個節點。
```

### 5. 範例 LLM 回應

#### 步驟 1 模板 1 sample 回應

```
你的需求有 2 個地方還沒講清楚：

1. 「賣方公司全名」格式要不要去除「股份有限公司」「有限公司」這類後綴？
   例如：「弄一下工作室股份有限公司」要存成全名還是「弄一下工作室」？

2. 「稅後合計」如果是 0 元（退款單）要怎麼處理？
   是照填 0、跳過該張、還是把檔名標記為「退款」？

請補完這 2 點再進步驟 2。其他 4 格內容已足夠進入流程。
```

#### 步驟 2 模板 2 sample 回應（同第 2 章那段，這裡再列以方便獨立讀）

##### 變體 A：理想型（過關 — 直接進步驟 3）

```
這份 workflow 做什麼：
從 pdf-inbox 資料夾讀取所有 PDF，用 Gemini 分析內文後給每張 PDF
一個語意化檔名，並把檔案改名後存到 pdf-renamed 資料夾。手動觸發。

節點清單：
1. Manual Trigger — 手動觸發，不接收 input。
2. Read PDF — 讀 /files/pdf-inbox/ 內所有 PDF，輸出每張的 binary。
3. Extract PDF Text — 把 binary 轉純文字（pdfTextPreview）。
4. Code: AI 改名 — 用 Gemini API 分析文字，輸出 newFilename。
5. Write — 把 PDF 用 newFilename 改名後寫到 /files/pdf-renamed/。

資料流向：Manual Trigger → Read PDF → Extract PDF Text → Code → Write
```

##### 變體 B：歪掉 1 — LLM 補太多技術細節

```
節點清單：
1. Manual Trigger (n8n-nodes-base.manualTrigger, typeVersion: 1) — emits empty trigger payload, fires on UI button click...
2. Read Binary Files (n8n-nodes-base.readBinaryFiles, typeVersion: 1) — uses fs.readdirSync internally...
[後面繼續講 typeVersion / position / 內部實作細節]
```

- **辨認訊號**：每個節點後面括號開始出現 `typeVersion`、`n8n-nodes-base.xxx`、`position`、講「internally」「under the hood」
- **學員下一步**：追問「請只用我看得懂的中文形容詞描述每個節點做什麼，不要列 typeVersion、不要講內部實作」 → 通常 LLM 會重給一份簡化版

##### 變體 C：歪掉 2 — LLM 漏節點 / 把多個節點合併講

```
節點清單：
1. Manual Trigger — 手動觸發。
2. PDF 讀取與處理 — 讀 inbox 內 PDF 並轉成文字。
3. Code 節點 — 呼叫 Gemini 分析文字並命名後寫檔。
```

- **辨認訊號**：你 n8n UI 上實際看到 5 個節點，LLM 卻只列 3 個；或 LLM 把「Read PDF + Extract PDF Text」合併成一條、把「Code + Write」合併成一條
- **學員下一步**：追問「我在 n8n UI 看到 5 個節點，你只列了 3 個。請逐個列出並『不合併』。我會貼節點名給你對照：[貼 5 個節點名]」 → LLM 會分開重列

##### 變體 D：歪掉 3 — LLM 自作主張提改進建議

```
節點清單：
[5 個節點正確列出]

不過我發現這個 workflow 有幾個可以改進的地方：
1. 建議加上 try/catch 處理 PDF 讀取失敗
2. 建議用 Switch 節點分流不同類型的 PDF
3. Code 節點的 prompt 可以加上 few-shot 範例增強準確度
...
```

- **辨認訊號**：LLM 給完節點清單後，自動接一段「不過 / 此外 / 建議」
- **學員下一步**：忽略「建議」段落，**只用節點清單那段進步驟 3**。模板 2 已寫「不要建議改進」但 LLM 偶爾會犯規 — 不必追問改正，這次過了就好（追問會浪費 token）

#### 步驟 3 模板 3 sample 回應（成功 — 區段格式）

##### 變體 A：理想型（過關 — 直接 Paste 到 n8n -edit workflow）

```json
{
  "parameters": {
    "mode": "runOnceForEachItem",
    "jsCode": "const text = $input.item.json.pdfTextPreview;\nconst prompt = `請從以下發票文字抽取：賣方公司全名、稅後合計（純數字）、發票日期（YYYYMMDD 格式）。回傳 JSON：{seller, totalAmount, invoiceDate}。發票文字：${text}`;\n// ... 後續呼叫 Gemini 與 fallback 邏輯保留 ...\nconst newFilename = `${invoiceDate}_發票_${seller}_${totalAmount}.pdf`;\nreturn { json: { newFilename, ... } };"
  },
  "name": "Code: AI 改名",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [820, 300]
}
```

##### 變體 B：歪掉 1 — LLM 給整份不只目標節點

```json
{
  "name": "02-pdf-ai-rename-invoice",
  "nodes": [
    { "parameters": { ... }, "name": "Manual Trigger", ... },
    { "parameters": { ... }, "name": "Read PDF", ... },
    ...
  ],
  "connections": { ... }
}
```

- **辨認訊號**：第一行 `{` 後第二行是 `"name":`（不是 `"parameters":`）+ 看到 `"nodes":` 陣列 + 看到 `"connections":`
- **學員下一步**：用「模板 3-追問」要它重給單節點區段；不要 Paste 這整份到 n8n（會破壞整個 workflow 結構）

##### 變體 C：歪掉 2 — LLM 加 markdown code fence 包裹

````
這是修改後的 Code 節點：

```json
{
  "parameters": { ... },
  "name": "Code: AI 改名",
  ...
}
```

修改說明：
- prompt 改成抽取發票欄位...
- 檔名 template 改成發票格式...
````

- **辨認訊號**：JSON 前後有 ``` ` ` ` ``` 圍住、JSON 前後有「這是修改後的」「修改說明」中文段落
- **學員下一步**：複製 JSON 時**只複製 ``` ` ` ` ``` 之間那段**（n8n 的 Paste 不吃 markdown fence，連 ``` ` ` ` ``` 一起貼會壞掉）；不需要追問 LLM，自己手動切就好

##### 變體 D：歪掉 3 — LLM 在 JSON 中混雜中文註釋

```json
{
  "parameters": {
    "mode": "runOnceForEachItem",
    "jsCode": "const text = $input.item.json.pdfTextPreview;  // 從 PDF 讀取的文字\nconst prompt = `請從以下發票文字抽取...`;  // 改成發票欄位\n..."
    // 這裡保留原本的 fallback 邏輯
  },
  "name": "Code: AI 改名",
  ...
}
```

- **辨認訊號**：JSON 內出現 `// 中文註解` 形式的行（**JSON 規格不允許註解**，n8n Paste 進去會直接報語法錯誤）
- **學員下一步**：追問「JSON 規格不允許 `//` 註解，請移除所有 `//` 那行 + 行內註解（jsCode 字串裡的 `//` 是 JS 註解可以保留，但 JSON 結構層的 `//` 要刪掉）。重給一次純 JSON。」

#### 步驟 3 失敗 sample（LLM 給整份 — 同變體 B 詳述）

LLM 可能會回（**這是不對的**）：

```json
{
  "name": "02-pdf-ai-rename-invoice",
  "nodes": [
    { "parameters": { ... }, "name": "Manual Trigger", ... },
    { "parameters": { ... }, "name": "Read PDF", ... },
    ...
  ],
  "connections": { ... }
}
```

看到第二行是 `"name":`（不是 `"parameters":`）+ 第三行是 `"nodes":`，就是整份，**用追問模板要它重給**。

### 6. 驗收標準

整章讀完 + 動完後過關：

- [ ] 4 格便箋每格都填了具體值（不是「發票」這種模糊詞）
- [ ] 自驗對人講 1 分鐘沒有打結
- [ ] 從 n8n UI export 出 .json 檔，搜尋 `apiKey/accessToken/password/token` 全部找不到
- [ ] 貼模板 2 後，LLM 回的節點清單和 n8n UI 對得上 80% 以上
- [ ] 貼模板 3 後拿到的 JSON 開頭符合「`{` + `"parameters":`」格式
- [ ] 替換到 n8n UI 後，workflow 上節點數量沒變、連線沒斷

### 7. 常見錯誤 + 怎麼解

**錯誤 1：「填 4 格時，input 那格我寫『發票』就好」**
- 解：「發票」不夠。LLM 看到「發票」會自己腦補欄位（你以為發票上有「品項」但實際上你的發票沒有品項，只有總額）。最低限度要寫出 4-6 個欄位名 + 該欄位在 PDF 上的中文寫法（「賣方」不是「供應商」）

**錯誤 2：「我貼了模板 2，LLM 卻直接開始建議改進」**
- 解：模板 2 最後一行是「不要建議改進、不要寫程式碼」。如果 LLM 還是建議，追問：「你建議的改進我不需要，請只回答 1 和 2 兩題（描述 + 節點清單）」

**錯誤 3：「LLM 給的 JSON 看起來怪怪的，我不確定是區段還是整份」**
- 解：用驗收硬指標 1 的判斷法（看第二行）。如果還不確定，把 LLM 回應前 5 行貼回去問：「我給你看你回應的前 5 行，這是整份還是單節點區段？」

**錯誤 4：「LLM 把節點改名了，我不知道」**
- 解：步驟 3 替換到 n8n UI 後，**用 Cmd+F 搜尋你便箋上記的「必保留節點名」**——如果搜不到，代表 LLM 改名了，要回頭追問

### 8. 回到課程動線

- **下一頁 (第 4 章)**：步驟 4-6（測試、回報、收斂）+ 模板 4-5
- **如果你卡在步驟 3 LLM 一直給整份**：看模板 3-追問 + 第 5 章紅線 6
- **如果你卡在 credential 處理**：看第 5 章紅線 1 + 第 7 章類別 2

### 9. 對現有 HTML 的具體變更

| 動作 | 原 line | 改成 |
|---|---|---|
| 新增 | 步驟 1 後 | 補「自驗：對人講 1 分鐘」具體做法（不是「能講清楚」這種抽象驗收）+ 沒人講可錄音回放 |
| 新增 | 步驟 1 後 | 補 3 個不同改造類型的 4 格便箋 sample（合約改發票、Sheet 改 Notion、加 Drive trigger），不只 Story A |
| 新增 | 模板 1 之後 | 加 sample LLM 回應 box（如上第 5 節） |
| 改寫 | 254 callout | 把「在 n8n UI 開啟 → 三點選單 → Download → Without credentials」做成 4 步條列 + 截圖描述位置（截圖是預埋占位） |
| 新增 | 步驟 2 「驗收訊號」格 | 補「驗收硬指標」：搜尋 4 個字串都找不到 + 節點對得上 80% |
| 改寫 | 304-307「示範形狀法」一行帶過 | 拆成獨立小節，4 步動作 + sample LLM 回應 |
| 新增 | 模板 3 之後 | 加 sample LLM 回應（成功格式 + 失敗整份格式）+ 追問模板 |
| 改寫 | 333「JSON 最外層」段 | 翻譯成「看 LLM 回應的第一個 `{` 後面那一行是不是 `"parameters":`」這種非工程師能照做的判斷法 |


---

---

## 設計記錄（Phase A 診斷）

本章原始 HTML 章節的「空話」診斷清單，作為重設計的問題對應表：

### 第 3 章 post-llm-3-steps-decompose — 步驟 1-3 詳解

**整體判定**：這章已經是 8 章裡最有具體內容的（有 prompt 模板、有 4 格便箋範例）。但仍然有**判定 1**（步驟 1 的「填 4 格便箋」沒給「填的標準」，學員會填出垃圾自己也不知道）和**判定 4**（步驟 2 引用「示範形狀法」是引用未來內容，當下沒講透）。

| # | line | 原文摘要 | 違反 | 為什麼會卡住學員 |
|---|---|---|---|---|
| A3-1 | 161 | 步驟 1 動作「用一句話寫下『我要改成什麼』，再用 3 個追問填滿」 | 1, 2 | 3 個追問本身有列（input/output/保留節點），但「input 是什麼」這格學員填什麼算對？只填「發票 PDF」夠不夠？應該給「夠 vs 不夠」的對比範例，例如「『發票 PDF』不夠，『供應商發票 PDF，每張含統編+品項+稅後金額+發票日期 4 個欄位』才夠」 |
| A3-2 | 181-199 | 4 格便箋以 Story A 為例 | (還可以) | 這個範例其實 OK，但**只有一個範例**——商業培訓不同學員場景差距大。應該至少 3 個範例（合約改發票、Sheet 改 Notion、加 Drive trigger）讓學員找最接近自己的對照填 |
| A3-3 | 201-211 | Prompt 模板 1「請問我的需求有哪一格還沒講清楚？只指出空白，不要幫我補」 | 2 | 學員貼這 prompt 後，LLM 會回什麼？沒給 sample output。學員不知道「LLM 回我『output 那格再具體一點』要怎麼補」，因為他覺得自己已經寫了「改名後的 PDF」。應該給一個 sample LLM 回應 + 學員照著補完的版本 |
| A3-4 | 264 | 「LLM 把 JSON 翻成人話。回傳格式大約是：節點名稱 → 它輸出什麼 → 下一個節點吃什麼」 | 1 | 這是「期望 LLM 回什麼」的描述但**沒給 sample output**。學員拿到 LLM 真實回應時會發現格式可能是 markdown 表格、可能是條列、可能是分段——不知道哪種叫「對」。需要至少 1 個 sample output 範例 |
| A3-5 | 304-307 | 「示範形狀法」只在這格裡用一句話帶過 | 4 | 「示範形狀法」是個有獨立價值的技巧（Notion 換節點、Slack 換節點都能用），但這章只在「雷區」這格塞 3 行。應該獨立切出小節，給 step-by-step：「(1) 在 n8n UI 拉新節點 (2) 隨便填一個值 (3) 用『複製為 JSON』(4) 貼給 LLM 標註『這是目標形狀範本』」+ sample LLM 回應 |
| A3-6 | 333 | 「如果你收到 LLM 給的 JSON，不確定它是『區段』還是『整份』，有個快速判斷法：看 JSON 最外層有沒有『name』和『nodes』兩個頂層 key」 | 5 | 對非工程師：「JSON 最外層」「頂層 key」就是純技術名詞。學員看 LLM 給的長 JSON 會頭暈，根本找不到「最外層」在哪。應該配截圖：「對著 LLM 回答的開頭看，如果第一個字是 `{` 然後第二行是 `"name":` 就是整份，要它重給」 |

**第 3 章空話小計：6 條**

---
