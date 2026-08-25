# simple-ai 內容等價修復計畫

## Scope

- 修復 `CH1-3.html`、`CH1-4.html`、`CH2-4.html` 的教案表格未以 learner-facing 等價資訊呈現問題。
- 不改動其他課程頁、全站搜尋索引、sitemap 或尚未驗證的真人試跑證據。

## Backup / restore

- 備份：`_backup/2026-08-25-content-fidelity/{CH1-3.html,CH1-4.html,CH2-4.html}`
- 還原：`_tools/restore-2026-08-25-content-fidelity.sh`
- 驗收：`bash -n`、三頁 `cmp`。

## Required fixes

1. CH1-3：補回「症狀 / 原因 / Plan B」五列完整拍照與 Email 卡關表。
2. CH1-4：補回「症狀 / Plan B」四列資安紅線卡關表，並保留現有六陷阱與錯誤修復內容。
3. CH2-4：補回「學員狀況 / Plan B」五列 FAQ 現場卡關表，並保留現有練習區。

## Acceptance

- `python3 docs/audit-course-substance.py simple-ai --page ...` 三頁皆 PASS。
- 三頁 lint、`git diff --check` PASS。
- 全課 substance audit 只剩不可由代理人代簽的真人三分鐘跟讀／跟做 gate，或在使用者完成後全數 PASS。
