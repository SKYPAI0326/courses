# office-ai 案例故事情境修補報告

## 結果

已修正 `courses/office-ai/index.html` 的課程核心案例，補足雅雯的角色、工作情境、客戶問題、資料缺口、LLM 產出、寄出前風險與 PM 介入點。案例現在能完整說明：流暢的文字若未經查證與授權，可能直接變成公司的對外承諾。

## 實際變更

- 案例標題改為「雅雯回覆一封客戶詢價信，差點替公司做出承諾」。
- 故事依序交代：業務專員 → 收到客戶詢價 → 缺少最新資料與核准 → 只給 LLM 一句要求 → LLM 補出未確認承諾 → 寄出前發現風險 → PM 分離已知、未知並要求人工核准。
- 保留原有五個風險缺口與「你在課程中會練的 PM 工作」區塊。
- 沒有改動 HTML wrapper、class、導覽、其他課程內容或搜尋摘要。

## 可回復資產

- 備份：`office-ai/_backup/2026-09-22-pre-case-narrative/index.html`
- 備份清單：`office-ai/_backup/2026-09-22-pre-case-narrative/MANIFEST.json`
- 還原工具：`office-ai/_tools/restore-2026-09-22-pre-case-narrative.sh`

## 驗收證據

- HTML lint：1 頁，`BLOCKER 0 / ERROR 0 / WARN 0`。
- 課程結構檢查：`office-ai/index.html` 通過；office-ai 四個固定回歸目標通過，`blocked=0`。
- 文案連貫性檢查：`0 warning(s)`。
- 課程內容實質檢查：`block=0 / missing_assets=0`；語意審查仍由人工完成。
- `git diff --check`：通過。
- 瀏覽器 smoke：`http://127.0.0.1:8766/courses/office-ai/` 可正常載入，案例標題、完整故事、五個缺口與 PM 練習框均可見。

本次只完成工作區修改，未建立 commit，也未 push。
