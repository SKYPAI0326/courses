# Repair Report: uiux-designer

## Changed

- `part2/CH4-overlay-single-action.html`
  - 在第一段補上 Host／Overlay 參考圖、Starter 檔案與 B4 起始頁的取得順序，讓 B4→B5→B6 試讀有明確起點。

- `part2/CH6-prototype-task-test.html`
  - 頁首返回目標從製作層 Blueprint 改為課程總覽。
  - Section 01 的手上材料加入 B6 起始頁連結、用途與本機備援路徑。
- `part2/CH7-figma-handoff-export.html`
  - 頁首返回目標從製作層 Blueprint 改為課程總覽。
  - Section 01 的手上材料加入 B7 起始頁連結、用途與本機備援路徑。
- `part3/CH8-web-git-deploy.html`
  - 頁首返回目標從製作層 Blueprint 改為課程總覽。
  - Section 01 的手上材料加入 B7 來源、輸出與限制清單、README 連結；第一步加入 `web-starter/index.html` 連結與 Markdown 備援。
- `uiux-designer/_tools/learner-entry-smoke.py`
  - 新增語意入口掃描：禁止學員頁連到製作層文件，並要求 B6–B8 的起始材料出現在第一個操作前。
- `../docs/audit-course-substance.py`
  - 頁面發現改為遞迴掃描 `part1/`、`part2/`、`part3/`，避免只掃課程根目錄造成「0 頁」假綠。
  - 依現有課程用語檢查起始材料、完成物、示範、檢核、錯誤修復與交接，產出可供人工抽查的證據清單。
- `_review/HUMAN-REVIEW-START-2026-09-17.md`
  - 新增 B4 → B5 → B6 的人工試讀範圍、30 秒入口檢查、停止條件與記錄欄位，讓人工審查從固定微序列開始。

## Verification

- restore script：`bash -n` 通過。
- learner entry smoke：`PASS (16 learner pages; required first-use checks: 3)`。
- learner relative-link smoke：`PASS (183 links, 0 missing; 47 pages)`。
- HTML lint：`50 pages, 0 BLOCKER, 0 ERROR, 0 WARN`。
- learner-facing copy pattern audit：`0 finding (0 BLOCK, 0 REVIEW)`。
- `git diff --check`：通過。
- Chrome：B4 起始材料可見；B6 → B7 → B8 → 課程總覽導覽通過；三頁頁首均返回課程總覽，沒有 `_design/` 目標。
- Chrome B8 第一段：README 與 `web-starter/index.html` 均在第一次操作前可見；Console error／warning：0。
- course-validator preflight：23 PASS、1 WARN（無 datasets，與本工具操作課型態相符）、0 FAIL。
- course-validator L1–L3：全綠。
- content substance evidence：`16 pages, 0 BLOCK, 0 REVIEW, 16 READY_FOR_HUMAN, 0 missing_assets`；證據檔：`_validation/L5-evidence-manifest.json`。

## Remaining

- 本輪清除學員入口的立即阻塞與內容掃描器的假綠風險；課程整體仍是 `MACHINE_READY_PENDING_HUMAN`。
- Figma Starter 的固定／滾動聯合效果、Swap、Smart Animate、Form 多欄位與 List 動態行為仍需平台實測。
- Photoshop 開檔／輸出、GitHub push、公開部署仍未完成外部 Gate。
- 16 單元真人冷讀、B4→B5→B6 連續跟做與跨帳號重建仍未完成。
- L0、L4a、L4b、L5 仍依驗證系統要求保留人工／Codex consult 狀態。

## Release decision

本輪入口與靜態內容證據的 `BLOCK` 已解除，現在可以安排「入口與前兩個操作」的聚焦人工試讀；尚未達到整門課 `READY`。人工試讀仍應從 B4 → B5 → B6 微序列開始，不直接要求人員完整瀏覽 16 單元。

## Restore

- Backup: `uiux-designer/_backup/2026-09-17-pre-learner-entry-repair/`
- Restore: `uiux-designer/_tools/restore-2026-09-17-pre-learner-entry-repair.sh`
