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
- `pdfimages -list`：第 19 頁含三張 1600×1200 JPEG；重新渲染第 19 頁後確認三張照片預覽可見，先前的 lazy-loading 阻擋已排除。
- PDF 絕對素材網址已修正為 `https://skypai0326.github.io/courses/courses/simple-ai/assets/`，避免 GitHub Pages 少一層 `/courses/` 導致 404。
- `git diff --check`：通過。

## 尚未放行／待明確授權

- GitHub Pages 尚未部署 `4bc8f89` 之後的修正版，因此線上素材 404 需在隔離 release 分支部署後重測。
- G3 內容審核仍等待使用者完成三分鐘跟讀並簽核；詳見 `courses/simple-ai/_review/G3-CONTENT-REVIEW.md`。
