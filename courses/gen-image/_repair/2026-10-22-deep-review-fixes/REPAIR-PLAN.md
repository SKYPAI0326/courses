# Deep Review Fix Plan

## Scope

- task_scope: `content-change`
- `workshop-2h-poster-social.html`
- `_workshop/AI生圖到設計完稿-2h.md`
- `_workshop/AI生圖到設計完稿-2h-content-review.md`
- `_workshop/AI生圖到設計完稿-2h-image-manifest.md`

## Approved findings

1. 將 HTML 前 20 分鐘拆為版型 10 分鐘、線稿 10 分鐘，使可見時間合計 120 分鐘。
2. 將 `MODULE C`、`C＿＿＿＿`、`正確的 C 類型` 改為獨立課程用語，並補回歸掃描。
3. 將「目的、讀者、唯一重點、發布尺寸」四格與任務句移至學員開場的第一個動作。
4. 將 HTML 最終收件清單同步為任務句、視覺 brief、prompt、兩張 PNG、完稿檢核。
5. 為單層 READY PNG 增加不拆分元素的 1:1 備援路徑：整張等比例縮放、補品牌底色、在留白重建文字。
6. 補強圖片生成事件與 workspace asset hash 紀錄；不宣稱這取代獨立相似度驗證。

## Allowed visible-text changes

- 新增開場四格與任務句。
- 將模組代號改為「視覺結構」或實際結構名稱。
- 增加 READY 扁平圖的 1:1 操作說明。
- 統一最終收件清單。
- 調整章節分鐘數，不更動 120 分鐘路線圖。

## DOM impact

- 僅在既有第一個 `.lesson-section` 內新增一個既有樣式的 callout 與 code block。
- 其餘只改既有文字節點；不更動 `.lesson-body`、section、nav 或 footer 層級。

## Verification

- 時間徽章合計 120。
- learner-visible text 不得命中 `MODULE C`、`C＿`、`C 類型`、`CH6`、`模組 C`、`C1`–`C6`。
- HTML structure、lint、substance audit、local refs 與 Markdown/HTML contract check。
- 1440／820／390 browser smoke 仍受 `file://` 安全限制時維持 `PENDING`，不得宣告 release ready。

## Backup and restore

- `_backup/2026-10-22-pre-deep-review-fixes/`
- `_tools/restore-2026-10-22-pre-deep-review-fixes.sh`
