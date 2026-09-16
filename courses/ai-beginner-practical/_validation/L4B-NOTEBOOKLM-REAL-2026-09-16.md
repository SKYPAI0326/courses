# L4b NotebookLM 實機 Sentinel

**日期**：2026-09-16（Asia/Taipei）
**狀態**：`PASS — single real sentinel`

## 測試範圍

在已登入的 NotebookLM 網頁環境建立測試筆記本，匯入課程提供的三份無個資模擬來源：

- `news-community-fridge.txt`
- `notice-tax-filing.txt`
- `book-excerpt-learning-notes.txt`

NotebookLM 自動建立筆記本標題為「閱讀實踐與思考筆記心法」，並顯示 3 個來源。

## 實際操作與結果

| 步驟 | 結果 | 證據 |
|---|---|---|
| 建立筆記本 | PASS | 成功進入 NotebookLM 筆記本工作區 |
| 加入來源 | PASS | 3 個 `.txt` 來源均出現在來源清單 |
| 依來源提問 | PASS | 問：「請只根據『教學新聞｜社區共享冰箱試辦』回答：試辦前四週的食物取用次數是多少？請保留來源引用。」 |
| 回答正確性 | PASS | 回答為「試辦前四週共記錄 286 次取用」 |
| 引用回查 | PASS | 回覆顯示 `1: news-community-fridge.txt`；點擊後開啟來源內容，並定位到含 `[N01-P03]` 的原文段落 |

## 判定邊界

本次證明 CH3-1 的 NotebookLM 核心路徑「加入來源 → 提問 → 取得引用 → 點擊回看」可實際完成。它是單一實機 sentinel，不代表所有帳號、瀏覽器、檔案類型或全課程情境都已通過；L4a 外部案例真跑與 L5 冷跟做仍維持待授權／待執行。
