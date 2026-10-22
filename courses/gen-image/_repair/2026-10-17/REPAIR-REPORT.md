# Repair Report: two-hour standalone naming

## Changed

- `workshop-2h-poster-social.html`
  - 移除學員可見的 `CH6`、`模組 C`、`C1～C6` 編號。
  - 六種形式改用 Bento Grid、Comparison、Step by Step、Founder Portrait、Sticker Set、Lookbook Grid 的實際名稱。
  - 移除所有指向 `CH6-*` 詳細卡片與補充頁的延伸連結。
- `_workshop/AI生圖到設計完稿-2h.md`
  - 同步學習目標、流程、選型表、示範、備援與檢核用語。
  - 移除依賴其他章節的課後延伸區塊。
- `_workshop/AI生圖到設計完稿-2h-image-manifest.md`
  - 將六張素材標題改為獨立課程名稱。
- `_workshop/AI生圖到設計完稿-2h-content-review.md`
  - 同步審查名稱與來源 SHA-256。

## Verification

- learner-facing token scan：`CH6`、`Chapter 6`、`模組 C`、`C1～C6` 均為 0。
- HTML structure：PASS；`.lesson-body` 1 個、`.lesson-section` 11 個、body 外 section 0、重複 id 0。
- lint：BLOCKER 0、ERROR 0、WARN 0。
- substance audit：block 0、missing_assets 0、semantic_review PENDING。
- local refs：33，missing 0。
- source/review SHA-256：一致，`0ccf70dc602b2406fb26832cfadb2dd944de09931116c56685085d9c9f747222`。
- browser smoke：PENDING。本輪自動瀏覽器受 `file://` URL 安全限制，無法取得頁面觀察權限；需在已開啟頁面重新整理後人工確認 1440、390、430 px。

## Remaining

- 人工重新整理頁面，確認三種寬度沒有因較長的格式名稱產生異常斷行或溢出。

## Restore

- backup：`_backup/2026-10-17-pre-standalone-naming/`
- restore：`_tools/restore-2026-10-17-pre-standalone-naming.sh`
- restore syntax：PASS
