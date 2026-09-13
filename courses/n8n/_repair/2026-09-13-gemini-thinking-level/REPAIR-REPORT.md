# Repair Report: Gemini 3.6 thinking 參數同步

## 結果

已將 Gemini 3.6 Flash 的請求設定由舊版 `thinkingBudget: 0` 統一改為 `thinkingLevel: 'minimal'`（PowerShell 使用等價語法）。Lite Pack 版本升至 v1.3.5，macOS 與 Windows 精靈、共用 helper、10 個 workflow 及兩套課程頁同步更新。

## 證據

- 使用同一把 AQ Key 實測 `gemini-3.6-flash:generateContent`：`thinkingLevel: minimal` 回傳 HTTP 200 與 `OK`。
- Lite Pack ZIP `unzip -t` 通過，14 個 workflow JSON 全部解析成功。
- ZIP workflow／helper executable code 已無 `thinkingBudget`；共 11 個 workflow／helper 檔案包含 `thinkingLevel`。
- Mac／Windows 下載連結與頁尾版本均為 v1.3.5。
- macOS 課程頁 lint 通過；完整回復備份位於 `_backup/2026-09-13-pre-gemini-thinking-level/`。

## 尚待人工驗證

- 目前仍以 Mac 實機為主；Windows PowerShell、SmartScreen、路徑與 Docker Desktop 尚未在 Windows 實機執行。
- 目前 n8n 重新匯入的 14 個 workflow 尚需人工挑選基準案例，確認 Gemini 節點實際輸出。
