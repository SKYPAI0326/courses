# n8n Lite Pack 變更史

本檔記錄 workflow 與 setup-wizard 的版本變動。學員使用 sticky note 看「現在怎麼用」，
這份檔案是給維護者與 reviewer 看「過去發生什麼」。

---

## setup-wizard

| 版本 | 日期 | 主要變動 |
|---|---|---|
| v1.0 | 2026-04 | 首版：14 workflow + credentials 匯入 + Telegram + Gemini smoke test |
| v1.1 | 2026-04 | Telegram 改為可選（GUI Y/N gate）|
| v1.2 | 2026-05 | Gemini 限速防禦 + LP helper 共用骨架注入 |
| v1.2.1 | 2026-05 | 緊急修 v1.2 引入的 ReferenceError |
| v1.2.2 | 2026-05 | #02 / #14 重寫為 lpCall + Codex Q2 修補 |
| v1.2.3 | 2026-05 | Mac 版 Gemini smoke test 加 thinkingConfig.thinkingBudget=0 |
| v1.2.4 | 2026-05 | #14 endpoints 解析 robust（兼容 string / array / 單一 object） |
| v1.3 | 2026-05-13 | **安全修補**：Gemini key 改走 $env.GEMINI_API_KEY 路徑（不再字串替換 workflow JSON） |
| v1.3.1 | 2026-05-13 | 修 Invoke-Native 對 docker compose stderr 過度敏感 → 容器被半截 down 沒 up |
| v1.3.2 | 2026-05-13 | 修舊版偵測 false positive — 加 .env marker comment（# Provisioned by setup-wizard v1.3+）|

---

## n8n-sample-pack（演練素材包）

| 版本 | 日期 | 主要變動 |
|---|---|---|
| v1.0 | 2026-05 | 首版 |
| v1.1 | 2026-05-07 | 加 6 個邊界 case + manifest + validate（Codex L3 採納） |
| v1.3 | 2026-05-07 | pdf-inbox 換 TTF embedded 繁中商業 PDF（修 image-only PDF 無法解析）|
| v1.4 | 2026-05-08 | batch-inbox 預先建 processed/ failed/ 空子資料夾（修 cp -R 蓋掉子結構）|
| v1.5 | 2026-05-08 | batch-inbox 加 4 個有效繁中 PDF + 移除誤導 .txt/.bin（fileSelector 是 *.pdf）|
| v1.6 | 2026-05-13 | 補 #13 ops snapshot 對齊：ops-input/today.csv + ops-history/2026-04-29~05-05.csv（7 個）|

---

## workflow 個別變動

### #02 PDF AI 改名
- v0.5 之前：用 HTTP Request node 打 Gemini，撞 jsonBody expression 解析雷
- v0.6：改用 Code + this.helpers.httpRequest 直接打 Gemini API，從 7 節點簡化為 5 節點
- v1.2：注入 LP helper（lpCall / lpThrottle / lpSizeOK 共用骨架）
- v1.2.2：重寫為 lpCall + Codex Q2 修補
- v1.3：apiKey 從 `'__GEMINI_API_KEY__'` 字串替換改為 `$env.GEMINI_API_KEY`

### #03 批次處理錯誤恢復
- v0.5 之前：HTTP Request node + jsonBody
- v0.6：改 Code + dual-path（onError continueErrorOutput → fail 分支）
- v1.2：LP helper 注入
- v1.3：$env.GEMINI_API_KEY

### #04 定時 AI 日報
- v0.6：基本流程
- v0.7：加 Switch by extension（PDF / 純文字分流）+ Aggregate 改 allItemData + Code 正規化欄位（修 v0.6 PDF 丟進來亂碼）
- v1.2：LP helper
- v1.3：$env.GEMINI_API_KEY

### #06 Webhook → Gemini → 本機檔
- v0.6：Code node 直打 Gemini（取代 HTTP Request）
- v0.7：加 Web UI 分支（GET /ai-ui 回 HTML 表單頁）
- v1.2：LP helper
- v1.3：$env.GEMINI_API_KEY

### #09 Gmail 分類
- v0.9：首版

### #10 客戶資料夾自動整理
- v0.x：早期版本針對個案打補釘
- v2.0（2026-05）：**完整重新設計** — 不再針對個案打補釘
  - Read 為 source of truth（無漏）
  - dedup map（無覆蓋）
  - 3-way Switch（無打結）
  - per-file fallback（一個失敗不拖累整 chunk）
- v1.2：LP helper（與其他 workflow 對齊版號）
- v1.3：$env.GEMINI_API_KEY

### #11 銷售線索 CSV 清洗評分
- v0.9：首版（欄位正規化、去重、AI 評分）
- v1.3：$env.GEMINI_API_KEY

### #12 本地知識庫問答
- v1.0：首版
- v1.1：Part A 加 3-way Switch + filterPrintable（office/binary 不索引避免亂碼）
- v1.3（2026-05-13）：修 4 個 bug
  - Bug #1：chunker textMap 用 pairedItem 對齊（修 indexed=0）
  - Bug #2：kb-ask 用 this.helpers.getBinaryDataBuffer（修 filesystem-v2 binary mode 不相容）
  - Bug #3：Set node sources type=array（修 object vs array 不符）
  - Bug #4：tokenizer 加 CJK bigram + 動態 minScore（修中文無空格 0 命中）

### #13 每日營運快照
- v0.9：首版

### #14 私有 API 監控
- v0.9：首版
- v1.2.4：endpoints 解析 robust

---

## post-llm 教材

| 日期 | 變動 |
|---|---|
| 2026-05-07 | post-llm 全 8 章「課後用 LLM 改 workflow」上線 |
| 2026-05-09 | 第 9 章「跨格式改寫」上線（9 章 + appendix）|
| 2026-05-13 | 合併第 3+4 章為單篇「6 步真詳解」（9 章 → 8 章），Codex 課程審核建議 |

---

## 維護原則

- workflow sticky note 只放「現在怎麼用」（目的 / 測試方法 / 改造方向）
- 版本史一律寫到本檔，不寫進 sticky note
- meta._litePackNote 只留一句穩定說明，不寫版本歷程
- jsCode 內變動以 Codex consult ID 註記，不寫長段版本歷史
