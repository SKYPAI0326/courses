# Repair Report：AI 入門即戰力

**日期**：2026-09-16  
**範圍**：入口頁、模組導覽、CH1-1～CH4-1、學員工作表、課程驗證與運維紀錄

## 本輪完成

- 補上平台中立的文字型 LLM 最小啟動卡，說明取得路徑、必要畫面能力、保存位置與工具不可用時的停點。
- 六頁入口關卡明示「講師發放密碼後自學」，未取得或遺失時回原報名／課堂通知管道申請或重發。
- CH1 明確區分核心與延伸；延伸仍須保留五欄，且每輪只改一個主要條件並保存版本。
- CH2 明示 LINE／短訊息，補齊完整訊息示範與三版自我介紹示範。
- CH3 明確區分手寫段落編號與 NotebookLM 平台產生的可點擊引用；離線備援不計入正式引用驗收。
- CH4 補齊冷氣完整比較表、京都四天第一版與四天修正版，並標示手機表格左右滑動提示。
- 課後整合工作表、Blueprint 與 Coverage Ledger 統一使用 `course-capstone-handoff.md`。
- 更新模組卡片、課程索引、學員 evidence manifest 與運維報告。

## 驗證證據

| 檢查 | 結果 |
|---|---|
| cold-follow contract | PASS |
| UI／practicality contract | PASS |
| learner evidence manifest | PASS；6 頁、20 個學員素材 |
| HTML lint | PASS；0 BLOCKER、0 ERROR、3 WARN（教學提示框數量） |
| local links | PASS；89 個本地引用、broken 0 |
| SEO／密碼關卡 | PASS；6 頁完整 |
| search index | PASS；重建為 667 筆 |
| sitemap | PASS；42 筆；受密碼保護的本課程頁依規則排除 |
| course-validator L1–L3 | PASS；run `r-20260916-005519` |
| NotebookLM 實機 sentinel | PASS；3 個來源、依來源回答、引用點擊回查成功；詳見 `_validation/L4B-NOTEBOOKLM-REAL-2026-09-16.md` |
| L4a bridge 外部案例 | DEGRADED；case1／case2 已獲授權送出，均 300 秒 timeout，無模型輸出與評分；詳見 `_validation/L4A-MANUAL-REVIEW.md` |
| diff／restore 語法 | PASS；`git diff --check`、restore script `bash -n` |

## 模擬學員結果

- 零基礎學員 Agent 重跑：0 頁 BLOCK；CH1 延伸邊界已補強，CH3 仍以實機引用為條件。
- Reviewer Agent：確認案例完整輸出、核心／延伸邊界、總覽與終點導航已具備；指出的存取說明、檔名一致性與手機閱讀提示已回補。

## 尚未宣告完成的項目

1. NotebookLM 單一實機 sentinel 已完成；仍未涵蓋多帳號、不同瀏覽器／檔案類型與全課程多情境，也尚未完成真人冷跟做。
2. L4a bridge 已獲資料傳送授權但服務連續兩案 timeout，case3／case4 尚未執行；L5 真人或零基礎冷跟做仍需實際學員／授權測試環境。
3. 密碼頁已說明取得與重發管道，但正式上線端仍須確保報名或課堂通知流程真的會發放密碼，不能只依賴頁面文字。

## 回復

本輪修正前備份與回復腳本：

- `_backup/2026-09-16-pre-repair/`
- `_backup/2026-09-16-pre-followup/`
- `_tools/restore-2026-09-16-pre-repair.sh`
- `_tools/restore-2026-09-16-pre-followup.sh`

## 發布判定

目前為 **CONTENT_AND_STATIC_PASS；G5 CONDITIONAL**。課程內容、頁面操作路徑與靜態運維檢查已通過，NotebookLM 單一端到端引用 sentinel 已通過；L4a bridge 連續兩案 timeout，L4a 剩餘案例、跨環境覆蓋與實際冷跟做仍是正式使用前的驗收條件。本輪未 commit、未 push。
