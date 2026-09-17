# Repair Plan: uiux-designer

## Scope

- slug: `uiux-designer`
- pages:
  - `part2/CH6-prototype-task-test.html`
  - `part2/CH7-figma-handoff-export.html`
  - `part3/CH8-web-git-deploy.html`
- lessons: 本輪不改教案 Markdown，只修正已確認的學員入口與資產順序。

### Scope extension after substance audit

- `part2/CH4-overlay-single-action.html`: 補上起始材料、用途與取得時機，讓 B4→B5→B6 試讀可以從同一個材料契約開始。
- `../docs/audit-course-substance.py`: 修正課程頁面遞迴發現，並對現有 HTML 的起始材料、操作示範、檢核與修復詞彙做可追溯掃描；這是共用驗證工具的最小修正，不改課程時數或正文流程。

## Risk

- near-term class: unknown
- backup required: yes
- backup: `_backup/2026-09-17-pre-learner-entry-repair/`
- restore: `_tools/restore-2026-09-17-pre-learner-entry-repair.sh`

## BLOCKER

### [ASSET_DISCOVERABILITY] 起始材料必須先於第一次操作

- 問題：B6、B7、B8 的第一個操作先要求學員開啟檔案，連結在後段才出現。
- 修法：在 Section 01 的「手上有什麼／第一步」表格中加入可點擊起始材料、用途、使用時機與無法開啟時的本機路徑。
- 驗證：semantic smoke 必須確認第一個操作前已有起始材料 href，且 href 可解析。

## MAJOR

### [NAV_OPS] 學員頁不得連到 Blueprint

- 問題：B6、B7、B8 頁首「返回課程藍圖」指向內部 `_design/COURSE-BLUEPRINT.md`。
- 修法：改為「返回課程總覽」，指向課程 `index.html`。
- 驗證：掃描所有 learner-facing HTML，禁止 href 進入 `_design/`、`_backup/`、`_repair/` 或製作層 Markdown。

## Execution Order

1. 建立本輪備份與還原腳本。
2. 修 B6、B7、B8 的頁首導覽。
3. 將起始材料入口放到第一次操作之前。
4. 跑 semantic smoke、lint、copy pattern、continuity、relative links。
5. 用 Chrome 從入口頁開啟 B6 → B7 → B8 → 課程總覽，確認第一屏與連結。
6. 更新修復報告與驗證狀態；若任何一項失敗，維持 `BLOCK`。

## Activity Identity Audit

本輪不改活動的素材、產物、操作路徑或學員決策；只修入口。詳細表見 `SCAN.md`。

## Shared Copy Audit

本輪不刪除教學內容，不合併重複段落。只改三個頁首連結文字與三個第一段材料入口。
