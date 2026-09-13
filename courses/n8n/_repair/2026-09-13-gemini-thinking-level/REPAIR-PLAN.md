# Repair Plan: Gemini 3.6 thinking 參數同步

## 觸發原因

Lite Pack v1.3.4 已把模型更新為 `gemini-3.6-flash`，但仍沿用 Gemini 2.x 的 `thinkingBudget: 0`。Mac smoke test 實跑回傳 `400 INVALID_ARGUMENT`；移除 thinking 設定則可能讓最小回應只剩空內容。

## 修正範圍

1. macOS／Windows setup wizard 的 Gemini smoke test。
2. Lite Pack 共用 helper、含 Gemini 的 10 個 workflow 與 helper template。
3. Mac／Windows 課程頁的可執行範例、診斷說明與下載版本。
4. ZIP 完整性、JSON 結構與可回復備份。

## 驗收條件

- 兩套 smoke test 使用 `thinkingConfig.thinkingLevel = minimal`。
- 14 個 workflow JSON 可解析，且 executable code 不含 `thinkingBudget`。
- 同一把 AQ Key 對 Gemini 3.6 Flash 的最小請求回傳 HTTP 200 且文字為 `OK`。
- Mac／Windows 文件都指向 Lite Pack v1.3.5。
- 保留可執行的回復腳本與修正前備份。
