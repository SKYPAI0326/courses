---
name: course-ops
description: Use for G6 release readiness, registration, access controls, indexes, deployment proposals, rollback evidence, and post-launch maintenance governance.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# 課程發布與維運

`course-ops` 是 G6 的唯一責任角色。它整合技術稽核、連結、SEO、密碼與存取、課程註冊、入口頁、搜尋索引、sitemap、部署提案、備份、回復與維護排程。教學內容與獨立試學仍由 `course-validator` 判定。

先讀 [release-policy.json](references/release-policy.json)。所有發布紀錄使用 `contracts/course-release-record.schema.json`，操作使用 `scripts/course_release.py`。

## G6 的完成意義

G6 `PASS` 只表示 `READY_TO_PUBLISH`：G5 已通過、正式檔案與素材可追溯、技術與存取檢查完成、註冊和索引變更已準備、備份與回復路徑可執行、維護責任已登錄。此時尚未發布，也不得把 `published` 寫成 `true`。

## 準備發布紀錄

1. 確認 G5 PASS，並讀取全課製作與獨立試學證據。
2. 在隔離的 staging 路徑準備要發布的精確檔案，不直接改正式目標。
3. 執行並保存 technical、links、registration、access、rollback、maintenance 六類檢查。每筆證據都有相對路徑與 SHA-256。
4. 註冊工作包含密碼 hash 與 storage key、`inject_gate.py` 條目、`COURSES.md`、課程入口卡、搜尋索引與 sitemap。密碼或私密憑證不寫入可公開的 manifest。
5. 建立 release record；通過驗證後讓 course-run 以證據使 G6 PASS。

常用命令：

```bash
python3 scripts/course_release.py validate --record RELEASE_RECORD
python3 scripts/course_release.py propose --root COURSE_ROOT --record RELEASE_RECORD --output RELEASE_PROPOSAL
```

## 外部變更授權

發布提案會列出每個 source／target、變更前後雜湊、備份路徑與逐檔回復資訊。先把提案的 `manifest_sha256` 登錄成 contract external action，再向使用者說明目標、影響、備份與回復方式並取得明確授權。

套用前重新驗證：

- 提案仍為 `PENDING_AUTHORIZATION`，尚未使用。
- contract 授權的 action ID 與 manifest SHA-256 完全相同。
- 每個正式目標仍符合授權時的 before SHA-256。
- 每個 staging 來源仍符合 after SHA-256。
- 所有路徑都在授權的 course root 內，且沒有 manifest 以外的目標。

```bash
python3 scripts/course_release.py apply --proposal RELEASE_PROPOSAL --contract COURSE_CONTRACT
```

套用會先原位保存並驗證備份，再逐檔原子替換。授權在開始套用時即消耗；成功記為 `APPLIED`，失敗會回復已動目標並記為 `FAILED_AUTHORIZATION_CONSUMED`。同一提案不能再次套用。任何新 manifest 都要重新取得授權。

## 維護

發布前登錄 owner、cadence、freshness sources 與 next review。後續 `course-refresh` 只產生唯讀報告；它不升 metadata、不改頁、不重新發布。報告確認實際漂移後，交 `course-repair` 提案修正，再重跑受影響 Gate 與發布流程。

## 邊界

- 不把 G6 PASS、local build、lint PASS 或 Git commit 說成已發布。
- 未取得精確 manifest 授權前，不修改正式入口、密碼、索引、部署或外部平台。
- 不使用 `git add -A`，不把密碼、token 或私人資料放進發布證據。
- 不直接改教學正文來消除驗證問題；依失敗代碼回送責任 Gate。
- HTML 變更仍遵守 `course-html-contract`，並保留 DOM、文字、RWD 與 browser smoke 證據。
