# simple-ai 審核修正報告

日期：2026-08-25

## 已完成

- 建立還原點：`_backup/2026-08-25-review-fixes/` 與 `_tools/restore-2026-08-25-review-fixes.sh`。
- 補上 `_outlines/simple-ai.environment.md`：免費／付費邊界、起始狀態、登入與配額恢復、圖片備援、課前驗收。
- CH1-3 新增三張可下載的虛構文件照片（報價單、名片、菜單），另附 `ch1-3-photo-assets.txt` 文字核對版；照片內不含真實個資。
- CH1-3 改成「照片主線、文字備援」，並將遮蔽改為複製、裁切／不透明覆蓋、另存、封存原圖、放大確認的五步。
- CH2-2 → CH2-3 明確交接 `ch2-2-positioning-final.txt`；fallback 標為示範，不再充當完成證據。
- CH2-3 將價格、折扣、座位與預約承諾改成 `[待查證]`，並把剪輯 App 降為可選延伸。
- CH2-4 新增「我的一條工作流路徑」必做產物、下載模板與保存證據；A／B／C 改為課後延伸選一。
- 模組導覽頁標註課堂核心／課後延伸；移除未納入主線的 Perplexity 必修暗示與過度斷言。
- `handbook.html` 與建置腳本同步：素材／照片／工作流連結改為 HTTPS，PDF 內不再產生 `file://` 連結。

## 驗證證據

- `python3 docs/lint-page.py courses/simple-ai/ --summary`：14 頁、BLOCKER 0、ERROR 0、WARN 21。
- 本地 HTML `href`／`src` 解析：missing 0。
- `pdfinfo`：完整版 65 頁；A4 精華版 2 頁。
- 完整版 PDF `/Annots`：18 個 URI，`file_links=0`、`https_links=18`；包含三張照片、文字核對版與工作流模板下載入口。
- `git diff --check`：通過。

## BLOCKED／待明確授權

- 逐頁檢查發現 PDF 的照片預覽在目前已輸出的 PDF 中仍未顯示；章節 HTML 與 `handbook.html` 已移除 lazy-loading，下一次需重新啟動主機 Chrome 才能確認修復。
- 主機安全護欄拒絕同一圖片載入問題的第二次自動補救重建；本輪未繞過護欄，也未宣稱 PDF 預覽已完成。
