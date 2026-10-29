# Deep Review 修復計畫

task_scope：`content-change` + validation-state repair；保留既有 DOM wrapper、class、href 行為與課程順序。

## 既有檔案目標

1. `_validation/FINAL-REPORT.md`：由 validator 依現行 evidence 重產為 `BLOCKED`／0 valid。
2. `_validation/validation-result.json`：由同一次 validator run 重產，避免與 FINAL-REPORT 分歧。
3. `_gates.md`：更新頁首 current status，append 2026-10-22 修復與外部阻塞；不刪歷史。
4. `index.html`：B6 完成物由 T01–T07 校正為 T01–T08。
5. `assets/COURSE-START.html`：補 VS Code 官方下載入口、OS 選擇與首次啟動成功判準。
6. `../../_lessons/uiux-designer/B8-web-git-deploy.md`：在第一次要求 VS Code 前補相同工具取得與可觀察結果。
7. `part3/CH8-web-git-deploy.html`：忠實同步 B8 source 的 VS Code 起點，不改 wrapper／class／導覽。

## 新增修復證據

- `_repair/2026-10-22-deep-review/test_findings.py`
- `_repair/2026-10-22-deep-review/browser-smoke.mjs`
- `_repair/2026-10-22-deep-review/browser-smoke.json`
- `_repair/2026-10-22-deep-review/REPAIR-REPORT.md`
- `_backup/2026-10-22-deep-review-pre-repair/**`
- `_tools/restore-2026-10-22-deep-review-pre-repair.sh`

## 驗證

- RED／GREEN：`python3 -m unittest _repair/2026-10-22-deep-review/test_findings.py -v`。
- validator：`course-validator.sh uiux-designer report`，預期 `BLOCKED`、valid 0；此為正確狀態，不是失敗。
- structure：全課 batch 56 頁 0 BLOCK。
- HTML 保真：B8 source 新段落在 HTML 可見；其他 wrapper 與導覽不變。
- browser：index、B6、B7、B8 於 1440、820、390，檢查整頁 overflow、main、導覽、目標區塊與 sticky topbar；結果綁定現行 SHA-256。
- scoped diff、`git diff --check`；不得出現計畫外檔案。

## 明確不宣稱修復

- `.fig` checkpoint 尚無可驗證來源，維持 BLOCK。
- Photoshop、Figma、GitHub Pages、現行 live deployment 與真人學習證據未執行，維持 PENDING／UNKNOWN。
- 不建立 content PASS；需要符合 evidence contract 的 reviewer 對 16 單元正式正文另做完整審查。
