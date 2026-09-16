# Codex-first Autonomous Run

**run_id**：`20260916-figma-starter-browser-001`  
**開始日期**：2026-09-16  
**目標**：由 Codex 使用 Skills、檔案工具、靜態檢查與 Computer Use，完成 UI/UX 課程的設計、製作、跨平台測試與自我修補。

## 執行邊界

- Figma 測試只使用 Starter 免費方案與瀏覽器版。
- 測試檔必須是獨立檔案；不修改正式課程檔、其他課程或使用者私人資料。
- Codex 可以建立、編輯、匯出與測試課程所需檔案。
- 不自動分享、公開發布、刪除檔案或變更帳號安全設定；遇到不可逆外部動作先停下。
- `MACHINE_PASS` 只表示機器可重現；不得當作真人 `HUMAN_PASS`。

## 每次 Run 的記錄欄位

每一筆 `RUN-LOG.jsonl` 事件包含：

`run_id`、`timestamp`、`phase`、`tool`、`platform`、`step_id`、`input`、`action`、`visible_result`、`evidence_path`、`expected`、`actual`、`verdict`、`repair_commit`、`rollback`。

## 判定值

- `NOT_RUN`：尚未執行。
- `SIMULATED_PASS`：Codex 只讀檔案或講義模擬通過，未接觸真實平台。
- `MACHINE_PASS`：已由本機工具或 Computer Use 重現並保存證據。
- `MACHINE_READY_PENDING_HUMAN`：第一階段全部硬門檻完成，等待真人驗證。
- `BLOCK`：缺少權限、素材、平台能力或修復路徑。
- `HUMAN_PASS`：只有使用者或真人學員實際完成後才能使用。

## 執行順序

1. 讀取當前 Gate、計畫與工作樹，建立可回復基線。
2. 以 Chrome／Figma 完成 Probe A、B、C。
3. 依實測結果重建 Blueprint、Core Operation Inventory、Coverage Ledger 與時間帳本。
4. 製作代表單元、素材包與 learner-facing HTML。
5. 以 Codex 自主冷跟做、Computer Use 真跑與跨平台矩陣反覆修補。
6. 批次製作其餘單元並完成驗收報告。
7. 只在達到 `MACHINE_READY_PENDING_HUMAN` 後，交給真人做第二階段驗證。
