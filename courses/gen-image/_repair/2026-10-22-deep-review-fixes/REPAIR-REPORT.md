# Deep Review Fix Report

## Scope

- task_scope: `content-change`
- changed:
  - `workshop-2h-poster-social.html`
  - `_workshop/AI生圖到設計完稿-2h.md`
  - `_workshop/AI生圖到設計完稿-2h-content-review.md`
  - `_workshop/AI生圖到設計完稿-2h-image-manifest.md`

## Fixed findings

1. HTML 時間徽章改為版型 10 分鐘、線稿 10 分鐘；全部可見分鐘數合計 120。
2. `MODULE C`、`C＿＿`、`C 類型` 改為獨立課程的視覺結構用語。
3. 第一個學員動作移至開場：填目的、讀者、唯一重點、發布尺寸與任務句。
4. HTML 與 Markdown 的最終收件清單統一為任務句、視覺 brief、prompt、兩張 PNG、檢核表。
5. READY 扁平圖新增免費 1:1 路徑：整張等比例縮放、補品牌底色、在留白重建文字；不使用裁切、壓扁或付費分離。
6. 圖片 manifest 補入七筆 `image_gen` 事件輸出與 workspace asset SHA-256；七筆皆 `MATCH`。

## Verification

- HTML structure：PASS；checked 1、blocked 0。
- course structure：PASS；checked 1、blocked 0。
- lint：BLOCKER 0、ERROR 0、WARN 0。
- substance audit：block 0、missing_assets 0、semantic_review PENDING。
- local refs：33、missing 0（以正式 course root 解析）。
- regression：時間 120、殘留代號 0、開場任務／READY 路徑／最終交付清單均存在。
- source/review SHA-256：`95134f195718b59efef50e6423f412c3be7eeb07133d281c015ffc3956e5f1c1`，一致。
- restore script syntax：PASS。
- isolated restore proof：四個目標檔 hash 與備份一致。

## Pending evidence

- 1440／820／390 px browser smoke：PENDING；`file://` 觀察受瀏覽器安全規則阻擋。
- Canva 免費帳號 READY 4:5／1:1 計時實跑：PENDING。
- 120 分鐘真人 cold follow-along：PENDING。
- 參考 PDF 與生成素材 exact／perceptual reuse 獨立檢查：PENDING；生成事件輸出身分已核對，但不能取代相似度驗證。

## Restore

- backup: `_backup/2026-10-22-pre-deep-review-fixes/`
- restore: `_tools/restore-2026-10-22-pre-deep-review-fixes.sh`

## Release status

`MACHINE_CHECKED / NOT RELEASE READY`

本次沒有 commit、push 或發布授權。
