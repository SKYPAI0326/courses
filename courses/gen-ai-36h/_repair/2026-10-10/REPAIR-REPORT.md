# gen-ai-36h 實作深度修復報告

日期：2026-10-10（Asia/Taipei）
範圍：本課 Part 2–7 實作深度、案例資料、學員練習與交接素材；Part 1 僅清理列明的矛盾舊契約。
狀態：教材與靜態／程式驗證完成；瀏覽器、真人及外部平台驗證待執行。
版本控制：修復變更置於 `codex/gen-ai-36h-practice-depth-20261010` 隔離分支，基於最新 `origin/main`；提交範圍只涵蓋本課修復清單。

## 修復結果

- 20 份核心教案與對應學員頁補上多來源工作情境、Demo／Together／Solo 的不同判斷、核對答案、條件變更後修訂及恢復／交接步驟。新增 Part 2–7 可取得工作包，包含聊天／附件、版本文件、交易資料、分類原文、流程案例與結業專題包。
- PRAC2 改為可接手工作紀錄；PRAC3 以不同活動專案練來源判讀；PRAC4 維持一件工具但加入需求變更與回歸；PRAC5 分開驗收業務分類與人工核准後路由；PRAC6 交付可恢復流程卡；PRAC7 核對修訂作品、證據與接手說明。
- Part 4 交易案例獨立重算為 NT$6,950，按區域分別為 North 1,800、South 1,450、West 2,600、East 1,100。報價工具保留計算公式並另行核對核准門檻。
- 刪除 B01 清單中的 19 個舊矛盾 callout；19/19 舊標頭消失，刪除時 `.lesson-body` 位元內容不變。
- Part 6 名稱統一為「個人 AI 工作流程整合」；索引、CLAUDE 說明、教案 meta／renderer、正式課綱一致。正式課綱只相對修復前備份改四處，PRAC2／PRAC7 名稱也已同步。
- 20 份 canonical lesson source 與 `_lessons/gen-ai-36h/` mirror SHA-256 全數一致，明細見 `_validation/2026-10-10/source-sync-hashes.json`。

## 驗證證據

- `_tools/verify-course.py`：PASS，28 頁來源／HTML 保真、本地連結、首頁標題、原有 nav／auth、固定 24 月資料與 JavaScript 語法。
- HTML contract：33 個 HTML checked，0 blocked。
- `lint-page.py`：33 頁，0 BLOCKER、0 ERROR、36 WARN。
- `audit-course-substance.py`：28 頁，0 block、missing assets 0、semantic review PENDING。
- `test-course-functions.cjs`：PASS；`test-form-controller.cjs`：PASS（DOM simulation，不是瀏覽器實證）。
- 三個參考工具內嵌 JavaScript syntax PASS；交易答案由獨立 Python 驗算。
- 79 個修復前目標備份校驗全部符合 manifest；還原腳本 `bash -n` PASS。
- `git diff --check` 對本課、正式 lesson mirror 與課綱通過。依使用者後續 push 指示，改以最新 `origin/main` 為基線，將只含本課修復的隔離分支推送；其他課程及本地 main 的既有提交不納入。
- 語意內容審查由作者自審，沒有獨立 reviewer。Part 5 流程相關工作樹檔案目前有相對 HEAD 的差異，但在本輪寫入清單／備份以外，已保留；不將其差異歸因於本輪，也不聲稱與 HEAD 一致。課綱本輪改動以修復前備份為基線，確認僅四項指定替換。

## 待完成驗證

- Codex in-app browser 因安全政策拒絕本機 `file://` 頁面，並禁止以本機 server 或其他介面繞過；桌機／手機 viewport 與真實互動 smoke test 維持 PENDING。
- Claude、NotebookLM、Google Sheets／Make 目標帳號實跑，以及真人 30 秒入口、完整跟做、理解遷移、同伴交接與連續課試跑，均為 PENDING。
- 課程既有根目錄 validator ledger 維持舊狀態 `BLOCKED`：其中包含 stale artifact hash 及缺少更新後 28 單元的 content/fidelity/technical records。本輪不覆寫歷史 ledger；新證據在 `_validation/2026-10-10/`。
- 因上述狀態，本次不宣告 `LEARNER_READ`、`PLATFORM_VERIFIED` 或 `HUMAN_READY`。

## 還原方式

修復前備份及精確還原腳本保留在原執行工作區（`_backup/2026-10-10-pre-repair/`、`_tools/restore-2026-10-10-pre-repair.sh`）；`_backup/` 由 repo ignore 規則排除，不隨推送分支提交。遠端分支的回復方式是 revert 該修復提交；不要把原工作區快照套用到最新遠端基線。
