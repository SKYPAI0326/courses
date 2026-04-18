# 課程 Style Guide 模板

**使用方式**：新課程建立時複製本檔為 `_outlines/{slug}.style-guide.md`，依需求調整。course-designer、course-lesson-writer、course-reviewer 都會讀取對應的 style guide 強制執行。

---

## 通用語言規範

### 受眾稱呼
- 主稱「**你**」
- **禁用**「您」、「各位」、「學員們」
- 第三人稱用「學員」時只用於規範文件本身，不用於講義正文

### 口吻
- 直接、不夸飾
- **不用 emoji**（除非內容本身是 emoji 主題）
- 不用問候語（「大家好！」「歡迎進入本單元」）
- 不用結語套話（「希望這有幫助」「如有問題請告知」）

### 步驟編號
- 用「**步驟 1**」「**步驟 2**」
- **禁用**「Step 1」「STEP 1」「第一步」混用

---

## 案例主角群（Default — 可依課程覆寫）

所有商業情境案例使用**同一組主角**，跨單元一致，學員建立熟悉感。

### 公司
- **名稱**：弄一下行銷工作室
- **規模**：10 人小公司
- **業務**：數位行銷（SEO、社群、內容、廣告投放）

### 主角三人
- **阿凱**（27 歲，行銷專員）
  - 主角：多數情境默認用他
  - 痛點：手動重複工作多、不想學寫程式、想早點下班
- **雯姊**（35 歲，業務主管）
  - 次主角：涉及客戶/業務/報表時用她
  - 痛點：要整合多個來源資料給客戶報告、時間壓力大
- **老闆**（不命名）
  - 配角：涉及「向上匯報」「老闆想要 X」情境時用他
  - 風格：要的快、要有圖、不看細節

### 主角使用守則
- **同一單元只用 1 個主角當 POV**，避免視角跳躍
- **PRAC（實作）單元可改用學員自身視角**（「換你試試」）
- **不要創造新主角**（「小美」「Alice」）— 所有情境塞進現有三人

---

## 範例資料來源（Default — 可依課程覆寫）

- **預設使用**：Gmail / Google Sheets / Notion
- **次要使用**：Slack / Discord / Google Drive
- **避免**：過於特化的 SaaS（HubSpot / Salesforce / Jira），因為學員通常沒帳號

依 course_type 額外規範：
- **skill-operation**：每單元範例服務數 ≤ 3 個（減少 OAuth 負擔）
- **concept**：範例用公開可查的資料（不要假造數字）
- **programming**：範例資料集用 `range(0, 100)` 類型可重現的

---

## 平台版本聲明

每頁講義 footer 必須含 `platform_version` metadata：

```html
<span class="footer-meta" data-platform-version="n8n v1.58" data-built-at="2026-04-15">
  本頁以 n8n v1.58 製作，2026-04
</span>
```

- 格式：`{工具名} v{版本}` 或 `{工具名} {季度}`
- 若課程涵蓋多工具，填**本單元主要工具**
- 依 R3 維運策略，這是未來 `/course-refresh` 偵測漂移的依據

---

## 術語對照（繁體中文優先）

| 英文原詞 | 繁中譯詞 | 備註 |
|---------|---------|------|
| workflow | 流程 | 不譯「工作流程」（累贅）|
| scenario | 情境流程 | Make.com 專用 |
| node | 節點 | |
| trigger | 觸發器 | |
| action | 動作 | |
| credential | 連線設定 | 不譯「憑證」|
| execution | 執行紀錄 | |
| payload | 資料內容 | 或保留英文 |
| webhook | Webhook | 保留英文 |
| JSON / API / OAuth / URL | 原樣 | 保留英文 |
| AI / LLM | 原樣 | 保留英文 |
| prompt | 提示詞 | |
| token | token 或代幣 | 視上下文 |
| repository | 倉庫 | 或保留英文 |

若課程專屬術語有特殊譯法（例：GTM 的 `container` 譯「容器」），在 course-specific style guide 覆寫本表。

---

## 程式碼與命令格式

- 行內：`<code class="inline-code">` 或 markdown \`\`
- 區塊：`<pre><code class="code-block">`
- 語法著色 span class：
  - `.cm` 註解（綠）
  - `.ky` 關鍵字（藍）
  - `.st` 字串（淡綠）
  - `.vr` 變數（黃）
- **禁止**使用 highlight.js 等 JS 套件（違反「不增加 JavaScript 依賴」規範）

---

## 數字與單位

- 時間：阿拉伯數字 + 單位（「30 分鐘」非「三十分鐘」或「30min」）
- 版本號：保留原格式（`v1.58`、`3.12`）
- 百分比：用符號「80%」非「百分之 80」

---

## 禁用語彙（Ban List）

- 「簡單」「容易」（讓學員卡住時更挫敗）→ 改「只需幾步」「幾分鐘」
- 「當然」「顯然」（預設學員懂）→ 改「依預設」「照設計」
- 「大家都知道」類預設 → 直接解釋
- 過度謙詞「小小的」「一點點」

---

## 長度參考

| 區塊 | 字數建議 |
|------|---------|
| 破題（Context / Hook）| 80–150 字 |
| 單一概念定義 | 20–40 字 |
| 步驟說明（每步）| 60–120 字 |
| 常見錯誤（每條）| 80–150 字（現象+原因+解法）|
| 檢核題題幹 | ≤ 80 字 |

整頁講義 HTML 預期行數：450–900 行（含 CSS inline）。

---

## 課程專屬覆寫規則

建立 `_outlines/{slug}.style-guide.md` 時：

1. 以本檔為起點
2. 只寫**不同的部分**（如主角改用、術語加表、禁用詞增列）
3. 不重寫共通部分（減少維護負擔）
4. frontmatter 加 `extends: _style_guide_template.md` 標註繼承關係

範例（課程專屬 style guide）：

```markdown
---
slug: n8n-pro
extends: _style_guide_template.md
---

# n8n-pro Style Guide 覆寫

## 術語加表
| 英文 | 繁中 |
|------|------|
| Code Node | Code 節點（保留 Code 英文） |
| expression | 表達式 |

## 禁用語彙新增
- 「串接」→ 改「連接」或「整合」（使用者反映「串接」太技術）
```
