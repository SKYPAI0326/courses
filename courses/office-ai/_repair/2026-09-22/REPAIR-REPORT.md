# Repair Report: office-ai

**日期**：2026-09-22  
**狀態**：`MACHINE_READY_PENDING_HUMAN`
**本輪內容修改**：4 個概念單元 HTML；19 個正式 source；0 個素材檔案

## 已完成

- 重新掃描 20 頁 HTML，產出 `SCAN.md`。
- 產出依新規則整理的 `REPAIR-PLAN.md`。
- 建立本輪 20 頁 HTML 快照：`office-ai/_backup/2026-09-22-pre-repair/`。
- 建立並通過 shell 語法檢查的還原腳本：`office-ai/_tools/restore-2026-09-22-pre-repair.sh`。
- 從 19 個現有 learner-facing HTML 重建 `_lessons/office-ai/CH*.md`，每份保留唯一 learner-content 邊界、課型、目標、素材與來源狀態。
- 建立 `_outlines/office-ai.style-guide.md`，把完整句、起始材料、第一個動作、完成物、快速檢查、修復與平台誠實標記列為本課規則。
- 建立 `_review/` 的 19 份 content review、19 份 fidelity review 與 1 份 technical review；作者自審均明示不代表真人學會。
- 為 `CH1-1`、`CH1-2`、`CH6-2`、`CH6-3` 補上概念型任務契約，並同步 source 與 HTML。
- 建立 `_validation/evidence.json`，涵蓋 19 個單元、來源、頁面、資產與大綱 hash。
- 建立 `_validation/HUMAN-VALIDATION-CHECKLIST.md`，定義 19 單元入口／完成／理解／遷移、平台實跑與三課 sequence 的回填方式。
- 建立 learner-only AI context、兩版 prompt contract、19 份 stage-1 simulated learner logs、8 單元／9 份 stage-2 adversarial logs 與 `AI-TRIAGE-REPORT.md`。
- 將 88 筆 `independent-ai` records 合併進 evidence；原有 author/tool records 保留，AI 結果明示 `simulated_not_human: true`。

## Verification

- `docs/lint-page.py courses/office-ai/ --summary --by-bucket`：20 頁；0 BLOCKER、0 ERROR、21 WARN。
- 本地相對連結：117；斷鏈 0。
- 本地資產連結：12；缺失 0。
- 密碼 gate：20 / 20 頁存在。
- `audit-course-substance.py`：抽查頁面為 `MACHINE_CHECKED`；語意審查仍 `PENDING`。
- `course-validator office-ai status`：`MACHINE_READY_PENDING_HUMAN`，errors 0，valid records 39。
- `course-validator office-ai preflight`：`MACHINE_READY_PENDING_HUMAN`，errors 0。
- `course-validator office-ai all`：已產出 `validation-result.json`、`FINAL-REPORT.md` 與 evidence manifest；待驗項目集中在真人完成／理解／遷移、三課 sequence 與兩個需平台實跑的單元。
- AI workflow：context 19/19、stage-1 19/19、stage-2 9 logs、AI records 88；輸出 validator、scope selector、merge tests 均通過。

## Remaining

1. 由獨立 reviewer 逐單元重看來源的充分性、語句完整性、去重與完成物用途；目前 source 狀態仍是 `legacy-reconstructed-draft`。
2. 實跑 `CH1-2` NotebookLM 與 `CH5-1` Google 文件語音輸入，記錄實際平台、權限、版本與失敗恢復。
3. 完成 19 單元的入口、完整跟做、理解、遷移與三課 sequence evidence；目前 validator 正確保留 pending。
4. 如要上線，再處理 21 條 lint migration-debt 警告與瀏覽器視覺 fidelity。
5. 依 `office-ai/_validation/ai-simulated/AI-TRIAGE-REPORT.md` 的順序執行真人檢測；AI PASS 不解除 human pending。

## Restore

```bash
bash courses/office-ai/_tools/restore-2026-09-22-pre-repair.sh
```

還原腳本可將 20 頁 HTML 還原到本輪開始前狀態；本輪新增的 `_lessons/`、`_review/`、`_validation/` 與 style guide 需另行保留或刪除，不由該腳本處理。
