# 零基礎 Step by Step 文案修復報告

修復日期：2026-10-16

## 結論

10 份正式教案與 10 個學員頁已完成零基礎文案修復。原本較濃縮的功能句改成可跟做的操作順序；學員現在可逐步核對「操作、應看到、Checkpoint／卡住時」。

課程規模保持不變：9 小時、10 課、13 題概念題、40 張操作題路徑卡、9 題代表實作。

## 修復範圍

- Part 1：從 Project、Composition、Layer、Keyframe、Mask／Matte 到輸出與整合練習，改為逐步操作與可觀察結果。
- Part 2：建立固定四步答題法，補上第 1 題完整示範與變式練習步驟。
- Part 3：三組操作題都加入六步讀題法；9 題代表題補成可直接跟做的編號步驟。
- 所有頁面保留原時數、題號、數值、檔名、連結、導航與 HTML 外層結構。

## 回復方式

- 修復前檔案：`_backup/2026-10-16-pre-beginner-rewrite/`
- 回復腳本：`_tools/restore-2026-10-16-pre-beginner-rewrite.sh`
- 腳本已通過 shell 語法檢查，備份抽樣雜湊與修復前原檔相符。

## 驗收證據

```text
python3 _tools/validate-handout.py
PASS — 10 lessons, 14 HTML files, 40 operation cards,
       13 concept questions, 9 representative practices

validate-course-structure.py [10 lesson HTML files]
PASS — checked=10, blocked=0

python3 docs/lint-page.py courses/acp-ae/
PASS — BLOCKER=0, ERROR=0, WARN=0

audit_copy_continuity.py [10 lesson HTML files]
PASS — 每頁 0 warning

python3 docs/audit-course-substance.py acp-ae
PASS — pages=10, block=0, machine_checked=10
```

瀏覽器抽查：

- CH1-5，390 × 844：11 個 step block，無頁面水平溢位。
- CH2-1，430 × 932：四步判斷法與 13 題完整，無頁面水平溢位。
- CH3-3，390 × 844 與 1440 × 900：六步讀題法與三題代表實作可讀，無頁面水平溢位。
- console：0 warning、0 error。

## 尚未解除的限制

- `PLATFORM_VERIFIED = BLOCKED`：目前驗證電腦未安裝 After Effects，必須在實際授課機 v25.x 重跑所有介面路徑與輸出。
- `HUMAN_READY = PENDING`：尚未由零基礎目標學員完成 cold follow-along。

本輪可確認的是文案、結構與瀏覽器呈現已達機器與人工內容審查門檻；不能把這些結果替代實機或真人跟做驗證。
