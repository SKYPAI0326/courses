# Repair Plan: n8n #04 daily report provenance

## Scope

- slug: `n8n`
- asset: `assets/n8n-lite-pack.zip`（#04 workflow 與 `_change-log.md`）
- pages: `m0-workflow-04-daily.html`, `m0-install-mac.html`, `m0-install-win.html`
- platforms: macOS + Windows；Windows 維持待實機驗證標記

## Risk

- backup required: yes
- learner risk: 日報看似成功，但無法證明四份輸入都被讀取，也可能把未提供的人名與未決策事項寫成事實

## BLOCKER

### [DATA_LINEAGE] 保留輸入檔名

- 修法：Code 正規化加入 `it.binary?.data?.fileName`，並在輸出 JSON 回傳 `filesProcessed`、`sourceFiles`。
- 驗證：重新執行後 `filesProcessed` 列出四個實際檔名。

## MAJOR

### [TRUST / PROMPT] 限制模型推定

- 修法：要求來源標記；未指定責任人填 `未指定`；衝突數字並列，分別標註來源。
- 驗證：重新執行後日報含來源清單，且不自行產生責任人姓名。

### [TEACHING_ALIGNMENT] 補上可觀察驗收

- 修法：完整講義與 Mac／Windows quickstart 增加 `filesCount`、`filesProcessed`、`aiError` 的檢查。
- 驗證：文字錨點與 workflow JSON 欄位一致。

## MINOR

### [OUTPUT_FORMAT] Markdown 淨化

- 修法：寫檔前把 `<br>` 轉為換行，避免學員打開 Markdown 看到 HTML 標籤。
- 驗證：產出內容不含 `<br>`。

## Activity Identity Audit

本次修正既有 #04 活動的資料血緣與驗收證據，不新增 Demo / Together / Solo，不產生重複活動。

## Execution Order

1. backup 與 restore script
2. 修正 ZIP #04 Code、便箋、change-log
3. 修正三個 HTML 頁面的驗收說明
4. ZIP parse、全文 lint、文字錨點與 diff 驗證
5. 產出 REPAIR-REPORT.md
6. 精準 commit 與 push
