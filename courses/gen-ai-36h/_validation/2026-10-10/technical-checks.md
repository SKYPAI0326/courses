# gen-ai-36h 修復技術檢查

日期：2026-10-10（Asia/Taipei）
範圍：本次修復目標頁、素材與全課機器檢查。

## 本輪結果

- `python3 _tools/render-lessons.py --evidence-output _validation/2026-10-10/render-evidence.json ...`：完整指定清單 21 頁已轉製；正文維持 `.lesson-body`，PRAC6/7 表單由 renderer 保留。
- `python3 _tools/verify-course.py`：PASS。28 頁來源至 HTML 保真、所有本地連結、原始 nav/auth、首頁 28 卡、24 月固定資料與 JS syntax。
- Course HTML contract validator `validate-course-structure.py --batch .`：33 個 HTML（含素材工具）checked，0 blocked。
- `python3 ../../docs/lint-page.py "$PWD" --summary`：掃描 33 頁，0 BLOCKER、0 ERROR、36 WARN。警告主要為既有字級 token／hover 建議；本次參考工具沒有 blocker。
- `python3 ../../docs/audit-course-substance.py gen-ai-36h`：28 頁、0 block、missing assets 0；`semantic_review=PENDING`。
- `node _tools/test-course-functions.cjs`：PASS（報價邊界、彙總、路由／去重、JSON、儲存失敗與 HTML escape）。
- `node _tools/test-form-controller.cjs`：PASS（表單保存／重載、壞 JSON、恢復備份、容量失敗匯出）。此測試為 DOM simulation，非瀏覽器證據。
- 三個新增／改寫的 timer、quote、chart HTML 內嵌 JavaScript：Node syntax check PASS；原始交易清理由獨立 Python 驗算為 NT$6,950。
- B01 指定 19 個舊 callout：19/19 刪除紀錄存在，指定舊標頭不存在；刪除當時 `.lesson-body` 位元組完全相同。
- 既有 Make `T01–T07`、Blueprint、九欄規格：此次未修改；保留於原工作樹。
- 備份：79 個目標檔，建立前 checksum mismatch 0；還原腳本 `bash -n` PASS。

## 尚未完成的驗證

- 本地互動瀏覽器 smoke：PENDING。嘗試在 Codex in-app browser 開啟本機 `file://` 課程頁時，瀏覽器安全政策拒絕該 protocol，並明確禁止以本機 server、替代 browser surface 或其他間接方式繞過。故未執行桌面 1440px／手機 390px、430px 的視覺與互動檢查。
- 目標帳號：Claude、NotebookLM、Google Sheets／Make 實跑均 PENDING。
- 真人學員：30 秒入口、完整跟做、理解／遷移與同伴交接均 PENDING；本次沒有 `LEARNER_READ`、`PLATFORM_VERIFIED` 或 `HUMAN_READY` 證據。
- 獨立 reviewer：無；語意紀錄標為 author-self-check。

## 既有 validator ledger

執行唯讀 `course-validator.sh gen-ai-36h status` 後，現有根目錄 `_validation/evidence.json` 顯示 `BLOCKED`：既有全課紀錄有 `assets/prompt-library.md` 與 `part5/CH5-3.html` stale artifact，且缺少 28 單元更新後的有效 content/fidelity/technical records。此次未覆寫根目錄的歷史 evidence、validation-result、L5 manifest 或 FINAL-REPORT；本輪命令結果保存在 `_validation/2026-10-10/`。正式 validator ledger 尚須依新的來源／頁面／素材 hash 更新後再重跑。


## 範圍與基線說明

- 20 份正式教案 mirror 已逐檔 SHA-256 比對一致；雜湊清單見 `source-sync-hashes.json`。
- `_outlines/gen-ai-36h.md` 修復前已為 modified；依修復前備份比對，這次只增加四項已列明的標題／學習路徑替換。
- Part 5 既有表單紀錄、九欄輸入契約、T01–T07 測試檔不在本輪寫入清單或 79 檔修復備份；目前可見相對 HEAD 的工作樹差異；它們不在本輪寫入清單與修復備份中，已保留且未歸因於本輪，也沒有宣稱與 HEAD 相同。
- `course-validator.sh gen-ai-36h status` 的舊根目錄 ledger 仍是 `BLOCKED`（stale artifact hash、缺少有效的 28 單元紀錄）。本輪日期化靜態證據通過，但 semantic review、瀏覽器 smoke、真人與目標平台實跑仍為 `PENDING`，故不標 `HUMAN_READY`。

- 在基於最新 `origin/main` 的隔離工作樹重跑 `course-validator.sh gen-ai-36h status`：`BLOCKED`。原因包含大綱／20 份 lesson mirror hash 更新後舊 content/fidelity/technical records 過期或缺失；真人／平台驗證待完成。
