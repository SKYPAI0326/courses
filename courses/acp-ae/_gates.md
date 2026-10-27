# ACP-AE 課程 Gate 狀態

更新日期：2026-10-16

| Gate | 狀態 | 證據 |
|---|---|---|
| G0 範圍與來源 | PASS | 9 小時、10 單元、PDF／PPTX／大綱與授權邊界已凍結 |
| G1 正式正文 | PASS | `_lessons/acp-ae/` 10 份 learner-content 正文 |
| G2 網頁轉製 | PASS | 課程首頁、3 個 Part 入口與 10 個單元；讀題方法與完成檢查已放回使用情境內 |
| G3 技術品質 | PASS | `validate-handout.py` 通過；10 個學員頁結構 10/10；copy audit 每頁 0 warning；全站 lint 0/0/0 |
| G4 瀏覽器抽查 | PASS | 零基礎修復後抽查 CH1-5、CH2-1、CH3-3；390、430、1440px 無頁面水平溢位，console 無 warning/error；搜尋索引含 14 頁 |
| G5 平台實測 | BLOCKED | 本機沒有 After Effects；須在授課機 v25.x 完成全流程 |
| G6 真人跟做 | PENDING | 尚未執行目標學員 cold follow-along |
| G7 上線註冊 | NOT_STARTED | 尚未要求註冊、密碼注入或部署 |

目前可交付狀態：`MACHINE_CHECKED`、`BROWSER_CHECKED`。尚不可標示：`PLATFORM_VERIFIED`、`HUMAN_READY`。
