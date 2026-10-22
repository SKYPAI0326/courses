# Canva Deep Review 修復計畫

> **For Codex:** 執行時遵守 `course-repair` 的 scan → plan → backup → fix → verify；只修正 Deep Review Judge 接受的六項，不把真人或平台未驗證事項寫成已通過。

**Goal:** 修正 38 秒分支、無 v1 起始路徑、EXT1 證據分類、離線包、證據狀態與 Gate，使目前機器狀態可由現行檔案重現。

**Scope:** CH2-1、CH2-3 的正式來源與對應學員頁；直接依賴的搜尋索引、文字包、離線包；`evidence.json`、產物清單、validator 輸出與 `_gates.md`。不修改其他課程、不執行真人測試、不新增 Canva 平台通過宣稱、不 commit／push。

**Baseline:** Deep Review case `canva-video-teaching-deep-review-20261022`；artifact digest `f25922ac503996df9c39f2a2509096350514e4533c3d6892f8c921c87c27b97d`；evidence digest `bf5faf109d9b0fdbf71fa1f9b2f8805e64a5ff1826264a978d0b6e9e1b8506c3`。

---

### Task 1：建立可回復基線

- [x] 備份所有預計修改的既有檔案到 `_backup/2026-10-22-deep-review-fixes-pre-repair/`。
- [x] 建立 `_tools/restore-2026-10-22-deep-review-fixes-pre-repair.sh`。
- [x] 以隔離暫存目錄執行 restore rehearsal，核對備份前後 SHA-256。

### Task 2：先建立會失敗的裁決驗收

- [x] 建立 `verify_deep_review_fixes.py`，固定六項裁決的機器可驗證條件。
- [x] 在修正前執行，確認至少偵測：CH2-3 固定秒數、CH2-1 無平面備援、EXT1 標記錯誤、離線包過期、Gate 日期過期。

### Task 3：修正學員路徑

- [x] CH2-1：加入可直接下載的 36 秒平面備援；明確說明可完成聲音／字幕練習，但不能分層修改原文字與背景；完整可編輯路徑仍回四片段底稿。
- [x] CH2-3：改以實際片段起點判斷接句；明列 36 秒、38 秒與較短版本的配樂處理，不再把 36 秒配樂寫成必然覆蓋全片。
- [x] 同步兩頁 HTML learner body，保留既有 layout wrapper、gate、連結屬性與 action-step 樣式。

### Task 4：重建直接依賴產物

- [x] 更新 `search-index.json` 與 `Canva完整操作步驟.txt`。
- [x] 重建 `canva-text-pack.zip`、`canva-handouts-offline.zip`。
- [x] 驗證 ZIP 內頁面／CSS 與現行檔案雜湊一致，且無路徑跳脫或缺檔。
- [x] 更新 `_validation/continuity-artifact-inventory.json`。

### Task 5：刷新證據與狀態

- [x] 將 EXT1 設為 `platform_required: true`，平台狀態維持 PENDING。
- [x] 建立新的 author self-check／tool-run 紀錄，所有 log 與 artifact snapshot 使用現行 SHA-256。
- [x] 執行 course validator；預期不再是 stale-evidence `BLOCKED`，但真人／平台／sequence 未完成時仍不得升為 HUMAN_READY。
- [x] 以當次實際結果更新 `_gates.md`，移除「未推送」等過期敘述。

### Task 6：完成驗收

- [x] 執行 `verify_deep_review_fixes.py`。
- [x] 執行現有 HTML／連結／內容 lint 與 `course-validator status`。
- [x] 檢查 `git diff --check` 及 scoped status；只回報本次檔案，不 stage、不 commit、不 push。
- [x] 在 `REPAIR-REPORT.md` 記錄已修正、仍待真人／平台驗證及回復方式。
