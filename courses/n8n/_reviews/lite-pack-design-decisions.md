# Lite Pack 內部設計決策紀錄

**用途**：講師參考用。記錄 14 個 workflow 共同遵循的工程設計選擇 + 為什麼這樣寫的真相。學員看的是 m0-workflow-* 拆解頁；這份是講師備課、debug 時的「為什麼」內參。

**狀態**：v1.0 · 2026-05-06 · 可持續累積（新踩的雷補進來）

---

## 1. Code Node 取代 HTTP Request Node 打 AI API

### 場景
所有 workflow 內部需要呼叫 Gemini API（命名、摘要、分類等任務）。

### 設計選擇
**全部用 Code Node 內 `this.helpers.httpRequest()` 直接打 API**，不用 n8n 內建的 HTTP Request Node。

### 原因（連發 #16 驗證）
n8n HTTP Request Node 的 jsonBody 欄位接受 Expression 注入，但實際運作是「先解析整個 jsonBody 字串為 JSON → 再執行 Expression」這個順序有解析陷阱。

實測過 5 種寫法都炸：
- `={{ JSON.stringify({...}) }}` 整段 expression → invalid syntax
- JSON skeleton + backtick template literal `${...}` → invalid JSON
- JSON skeleton + 字串連接 `+` → 仍 invalid JSON
- Code 節點隔離 + 簡單變數 `{{ JSON.stringify($json.prompt) }}` → 仍 invalid JSON
- 各種 escape 嘗試 → 仍失敗

### 結論
**Code Node 內 `this.helpers.httpRequest({...})` 100% 可控** — 不會被 n8n 二次解析、debug 容易、可在同一節點內加 fallback parser。代價：失去 HTTP Request Node 的 UI 設定方便性，但對「打 AI API」這種固定 schema 場景值得。

---

## 2. Gemini 2.5 Flash 強制設 `thinkingBudget: 0`

### 場景
所有打 Gemini API 的 generationConfig 都加這個欄位。

### 設計選擇
```js
generationConfig: {
  temperature: 0.4,
  maxOutputTokens: 200,
  thinkingConfig: { thinkingBudget: 0 }  // ← 必須
}
```

### 原因（連發 #17 驗證）
Gemini 2.5 是 thinking model — 會先「想」再輸出。**thinking tokens 算進總 token quota**。

實測症狀：
- `maxOutputTokens: 100` 設定下
- AI 真實輸出只回 3 個字「202」就被切斷
- `finishReason: MAX_TOKENS`
- thinking 把 token 全用光

### 結論
對「抽取 + 命名 + 分類 + 摘要」這類純格式化任務不需要推理，禁掉 thinking 把 quota 全給輸出。

例外：複雜推理任務（如 #14 API 監控的根因診斷 / #12 RAG 答案合成）可考慮放開 thinkingBudget 換更好質量，但要把 maxOutputTokens 調更大。

---

## 3. 多 item 場景手動 loop（不靠 runOnceForEachItem）

### 場景
處理多份 PDF / 多筆 lead / 多檔 input 的 Code Node。

### 設計選擇
Code Node 一律用 default mode `runOnceForAllItems` + 內部手動 for loop。
**不用** typeVersion 2 的 `runOnceForEachItem` mode。

```js
const items = $input.all();
const allReadItems = $('Read 上游節點').all();
const results = [];
for (let i = 0; i < items.length; i++) {
  // 處理 items[i]
  results.push({ json: {...}, binary: ... });
}
return results;
```

### 原因（連發 #18 驗證 / 03 v0.6 → v0.9 五次迭代）
1. **runOnceForEachItem 模式對 binary 處理有 bug** — `item.binary` 在這個模式下不一定是預期結構，下游 Write 會抱怨 `no binary field 'data'`
2. **runOnceForAllItems 預設多 input 只跑 1 次** — 學員初心者最容易踩的雷（4 份 PDF 只處理 1 份）。手動 for loop 解決
3. **手動 loop 內 fileName / binary 對齊更可控** — 可加 fallback、debug 容易

### 結論
runOnceForEachItem 是 n8n 的「方便糖」但對複雜場景不可靠。手動 for loop 多寫 3 行但 100% 可控。

---

## 4. fileName 對齊不靠 pairedItem

### 場景
Extract PDF Text 節點 onError continueErrorOutput → success 分支跟 error 分支兩條輸出對應到不同的 Read items。

### 設計選擇
**從 input.json.fileName 或 input.binary.data.fileName 反查 Read item**，不用 `pairedItem.item`：

```js
const originalName = item.json.fileName || item.binary?.data?.fileName;
const readItem = allReadItems.find(r => r?.json?.fileName === originalName);
```

### 原因（連發 #18 / 03 v0.8 debug 驗證）
**n8n pairedItem 在 Extract error 分支會誤標成 0**（不是真實上游 index）。

實測：
- Read 抓 5 份 PDF（壞檔在 index 4）
- Extract error 分支推送 1 個壞檔 item
- 該 item 的 `pairedItem.item = 0`（**錯**，應該是 4）
- 用 `readItems[0]` 取到第 1 份合法 PDF 的 binary
- 結果寫進 failed/壞檔.pdf 但內容是合法 PDF（silent failure）

### 結論
pairedItem 在 dual-path workflow 不可靠。fileName 是 Read 節點原生帶的，從來沒被搞亂過 — 用它反查 100% 對齊。

---

## 5. Telegram 節點不傳 parse_mode

### 場景
所有用 Telegram 節點推訊息的 workflow（#05/#06/#07/#09/#10/#11/#13/#14）。

### 設計選擇
Telegram 節點 `additionalFields` 留空 `{}`，**不加 Parse Mode 欄位**。

### 原因（連發 #15 驗證）
n8n Telegram Node typeVersion 1.2 的 Parse Mode dropdown 只給 3 個選項：
- `Markdown (Legacy)`
- `MarkdownV2`
- `HTML`

**沒有 None**。任何一個都會解析訊息內的特殊字元。

實測症狀：
- AI 動態回應內含 `*` `_` `[]` 等 markdown 字元（很常見，Gemini 用 `**bold**` 標重點）
- Telegram API 回 `Bad Request: can't parse entities at byte offset NNN`
- 訊息推不出去

### 結論
**Additional Fields 完全留空** = n8n 不傳 parse_mode 給 Telegram API = Telegram API 預設不解析（pure text 模式）= 安全。

額外保險（#06）：在 Code 節點組訊息時加 `stripMD()` 移除 markdown 字元，雙重防線。

---

## 6. setup-wizard credential placeholder 替換機制

### 場景
所有 workflow JSON 內含 `__GEMINI_API_KEY__` 與 `__TELEGRAM_CHAT_ID__` placeholder，setup-wizard 跑時用學員提供的真實值替換。

### 設計選擇
- workflow JSON source 內 placeholder：`__GEMINI_API_KEY__` / `__TELEGRAM_CHAT_ID__`
- setup-wizard 用 Python `content.replace()` 字串替換
- credentials 用 n8n CLI `import:credentials --decrypted` 自動建

### 原因（連發 #11 / #13 驗證）
- Gemini API key 是 header value，不是 OAuth → 純字串可以塞進 credential JSON
- Telegram chat ID 在 workflow node parameters 內，setup-wizard 用 placeholder 替換
- Telegram bot token 也是純字串 → credential JSON 直接塞

對 Gmail OAuth（#09）這種需要 redirect URI + 授權流程的，setup-wizard 無法自動建，學員必須手動建（半小時 Google Cloud Project 設定）。

### 結論
**Lite Pack 內所有 workflow（除 #09）credential 都能 setup-wizard 自動建**，這是「30 分鐘到能用」哲學的關鍵。Gmail 是唯一例外，學員手動建。

---

## 7. file access 環境變數預埋

### 場景
任何讀寫本機資料夾的 workflow（#02/#03/#04/#10/#11/#12/#13）。

### 設計選擇
n8n-compose.yml 預埋兩個環境變數：

```yaml
- N8N_RESTRICT_FILE_ACCESS_TO=/files/shared
- N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=false
```

### 原因（連發 #14 驗證）
n8n 2.x 預設只允許 `/home/node/.n8n-files` 路徑的檔案存取。Lite Pack 用 `/files/shared`（mount 學員 `~/Downloads/n8n-starter-kit/shared/`）所以必須放開。

無這兩條 env vars → Read PDF 節點報 `Access to file is not allowed`。

### 結論
starter-kit zip 預埋這兩條 env vars + setup-wizard 偵測缺失時用 awk patch 補上。學員零感知。

---

## 8. workflow 預設 Active = false

### 場景
所有 14 個 workflow source JSON 都設 `"active": false`。

### 設計選擇
import 後 workflow 不自動啟動。學員必須手動 Active 才會真的跑 Schedule / Webhook polling。

### 原因
- Schedule Trigger 一啟動就會在背景每 N 分鐘 poll → 學員還沒設好 credential 會狂噴錯誤
- Webhook 啟動才會持續 listen → 學員可能不知道 endpoint 已 expose
- Gmail Trigger 啟動會去 polling Gmail，credential 沒設會 OAuth 錯誤

### 結論
**保護學員不被「import 完立刻噴錯」的體驗困擾**。學員設好 credential + 確認對應資料夾後，自己決定哪個 workflow Active。

---

## 9. 結構化 JSON 輸出 prompt 設計

### 場景
所有需要 AI 回「分類結果」的 workflow（#09/#10/#11/#13/#14）。

### 設計選擇
Prompt 內**強制限定 enum + 要求 JSON 格式 + 不要 markdown 包裹**：

```
請對信件分類成 4 類之一：客訴 / 詢問 / 合約 / 其他。
回 JSON 格式（不要 markdown 包裹）：
{"category": "客訴", "urgency": "high", "reason": "..."}
```

### 原因
1. **Enum 限制避免 AI 發明新類別**（如「重要」「待辦」這種太模糊的）
2. **JSON 格式讓下游 jsCode 能 reliably parse**
3. **「不要 markdown 包裹」對抗 Gemini 預設用 ` ```json ` 包訊息**

### 配套：fallback parser
即使有上述設計，AI 仍可能：
- 回多餘文字（「好的，我認為這是...{json}」）
- 換成 markdown 包裹
- 完全不照格式

對策：jsCode 內用 regex `match(/\{[\s\S]*?\}/)` 從任意文字中抓 JSON 物件。多層 fallback：嚴格 JSON.parse → regex extract → 預設值。

---

## 10. only-on-anomaly 呼叫 AI

### 場景
「監控 / 對比 / 異常偵測」類 workflow（#13 營運快照 / #14 API 監控）。

### 設計選擇
**先用 jsCode 算數值對比**（差異百分比、status code 是否 200），**只有異常時才打 AI 摘要**：

```js
if (anomalies.length > 0) {
  // 只在這時打 AI
  aiSummary = await this.helpers.httpRequest({...});
}
```

### 原因
- 雲端 LLM API 有 cost / rate limit
- 月跑 30 天，平常 25-29 天都正常 → 沒必要每次都打 AI
- 異常才真的需要 AI 解釋「可能根因 + 建議下一步」
- 學員容易理解這個 cost-conscious 設計

### 結論
n8n 的 jsCode 讓「條件式呼叫 AI」很容易（一個 if 即可）。Make 也能做但需要 Router + Filter 比較囉嗦。

---

## 待補規範（明天課堂後可累積）

- 連發 #19+ 新發現的雷 → 補進來
- 學員實測新踩的坑 → 補進來
- workflow 重大改版（如 RAG 升級成 vector DB）→ 補進來

---

## 參考檔案

- 飛輪規則總表：`_規範/飛輪規則.md`
- workflow JSON source：`courses/n8n/assets/n8n-lite-pack/workflows/*.json`
- setup-wizard.command：`courses/n8n/assets/n8n-lite-pack/setup-wizard.command`
- 學員看的拆解頁：`courses/n8n/lessons/m0-workflow-*.html`

---

## Codex 審核紀錄

- **CALL_ID f64e0b44** (2026-05-06)：擴充 lite-pack 從 9 → 14 個 workflow 的建議。verdict: actionable（5/5 採納，未採用 #13 客服 FAQ + #15 會議逐字稿）。詳見對話紀錄。
