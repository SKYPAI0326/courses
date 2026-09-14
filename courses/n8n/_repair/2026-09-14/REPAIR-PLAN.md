# 2026-09-14｜n8n 講義過時內容修正計畫

## 修正目的

依目前課程驗證基線（Docker Desktop／n8n 2.37.7、Lite Pack wizard v1.3.5、Gemini 3.6 Flash）修正仍會讓學員走錯路的講義與模板文字。Mac 是目前人工驗證基線；Windows 仍保留「尚待實機驗證」標記。

## 範圍

- learner-facing `n8n/lessons/`：修正 `/files/shared/...` 路徑、n8n 目前 `Publish` 介面、#01／#07／#12 的驗收描述、過時頁尾版本資訊，以及 docx 行為的版本範圍。
- 來源教案 `n8n/_lessons/post-llm/`：同步路徑與 docx 的版本限定，避免日後重建 HTML 時復原舊說法。
- Lite Pack 來源與 ZIP：同步 #06／#12 Web UI 的發布提示、#09 Gmail 說明卡的發布提示，重新注入並封裝。

## 風險與處理

1. 路徑錯誤會讓容器找不到學員放入的檔案；所有 self-host 操作例統一使用 `/files/shared/...`。
2. n8n 2.37.7 顯示 `Publish`／`Published`；保留必要的「舊版可能顯示 Active」說明，但不再把 Active 當目前按鈕。
3. docx 抽取行為尚未在本課 2.37.7 實機重驗；改成明確的歷史觀察與待驗證提示，不把 n8n 1.x 行為冒充現行固定結論。
4. #07 的成功判準改以 Executions 分頁的成功結果為準，避免把編輯器畫布綠框當成必然持久狀態。

## 執行順序

1. 先保留 `_backup/2026-09-14-pre-repair/` 與還原腳本。
2. 先修來源 Markdown，再修 learner-facing HTML 與 Lite Pack Web UI／說明卡。
3. 注入 Web UI、重建 `assets/n8n-lite-pack.zip`，以 ZIP 內容作為可下載交付物。
4. 執行 HTML lint、Lite Pack contract、ZIP integrity、搜尋殘留過時字串與 search index build。
5. 產出 `REPAIR-REPORT.md`；平台人工驗證維持由學員在 Mac／Windows 依現場證據完成。

## 明確不在本輪

- 不修改 `_backup/**`、其他課程或學員 Downloads 中已解壓的舊副本。
- 不宣稱 docx、Windows 或所有進階頁已完成實機驗證。
