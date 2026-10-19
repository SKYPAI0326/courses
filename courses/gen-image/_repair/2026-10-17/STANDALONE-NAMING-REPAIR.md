# Standalone Naming Repair

## Scope

- `workshop-2h-poster-social.html`
- `_workshop/AI生圖到設計完稿-2h.md`
- `_workshop/AI生圖到設計完稿-2h-content-review.md`
- `_workshop/AI生圖到設計完稿-2h-image-manifest.md`

## Task scope

`content-change`

## Problem

兩小時獨立課程的學員沒有前置章節脈絡。`CH6`、`模組 C` 與 `C1～C6` 會被誤解為另一本講義的內部編號，課後連往 `CH6-*` 頁面也削弱本課程的獨立性。

## Approved changes

1. 將 `CH6 模組 C` 改為「六種社群視覺結構」。
2. 將 `C1～C6` 改為各結構的實際名稱：Bento Grid、Comparison、Step by Step、Founder Portrait、Sticker Set、Lookbook Grid。
3. 移除指向 `CH6-*` 詳細卡片與補充頁的延伸連結。
4. 保留既有教學順序、操作步驟、圖片檔案、下載連結與 HTML wrapper。

## Verification

- 全範圍掃描不得再出現 `CH6`、`Chapter 6`、`模組 C` 或學員向的 `C1～C6` 編號。
- HTML 結構、lint、內容 audit 與本地素材解析必須通過。
- 以 1440、390、430 px 做 browser smoke test。

## Backup

- `_backup/2026-10-17-pre-standalone-naming/`
- `_tools/restore-2026-10-17-pre-standalone-naming.sh`
