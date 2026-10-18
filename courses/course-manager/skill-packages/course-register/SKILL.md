---
name: course-register
description: Use as a compatibility entry for legacy course registration calls; dispatches registration and access work to course-ops under the governed G6 release process.
allowed-tools: Read, Glob, Grep, Bash
---

# 課程註冊相容入口

這個 skill 保留舊有 `/course-register <slug>` 呼叫方式。註冊、密碼關卡、入口頁、課程清單、搜尋索引與 sitemap 現在都由 `course-ops` 統一負責，避免註冊完成後又出現另一套發布狀態。

收到舊呼叫時：

1. 載入同層 `../course-ops/SKILL.md` 與 `../course-ops/references/release-policy.json`。
2. 把 `--check` 轉成 G6 registration／access 唯讀檢查。
3. 把註冊或密碼要求轉成 release record 的 staging 變更，不直接修改正式檔。
4. 由 course-ops 建立含精確目標、雜湊、備份與回復資訊的發布提案。
5. 取得對該 manifest 的明確授權後，才由 course-ops 套用。

此相容入口不自行產生密碼、不編輯 `inject_gate.py`、`COURSES.md`、入口頁或索引，也不執行部署。它只把舊呼叫導向同一套 G6 證據與授權流程。
