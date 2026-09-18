# CH1-1 網頁實務工作台修正報告

日期：2026-09-18

## 結論

已將 CH1-1 的主要學員路徑改為頁內實務工作台。學員不必先下載 Markdown、另開文字編輯器或手動辨識欄位；可在同一頁完成五題對話、回答判讀、一次單一變因修改、個人轉移練習與完成檢查，再匯出交付檔。

Markdown 工作表仍保留，但定位改為瀏覽器無法暫存、需要離線處理或手動重建紀錄時的備援，不再是預設入口。

## 實際修正

- CH1-1 的「先開始」按鈕改為直接跳到 `#practice-workbench`。
- 新增 `#unit1-workbench` 頁內表單，包含姓名／日期、五個提示詞與回答欄、觀察判斷、修改前後版本、個人三段練習與六項完成檢查。
- 加入目前瀏覽器的 `localStorage` 暫存與重新整理恢復；頁面明確說明不會自動讀取或上傳外部 LLM 對話。
- 加入「儲存到本機」「匯出 Markdown」「列印工作台」「清除本機資料」四個操作。
- 匯出檔固定為 `unit1-practice-sheet-complete.md`，保留原始提示詞、回答、判斷、版本差異、個人轉移與完成檢查。
- 更新 CH1-1 教案、課程藍圖、Coverage Ledger，使起始材料、第一個動作、完成物與備援路徑一致。
- 新增 `test_workbench_contract.py`，並把工作台要求納入 cold-follow 與 UI practicality regression。

## 驗證結果

| 檢查 | 結果 |
|---|---|
| 四頁 page lint | PASS；4/4，0 BLOCKER、0 ERROR、0 WARN |
| `audit-course-substance.py` | PASS；4 pages、0 block、0 review、4 ready_for_human、0 missing_assets |
| workbench contract | PASS |
| cold-follow contract | PASS |
| UI／practicality contract | PASS |
| L0 truth table | PASS |
| learner-agent evidence manifest | PASS；6 pages、19 learner assets |
| course-validator preflight | PASS；24 PASS、0 WARN、0 FAIL |
| course-validator L1–L3 | PASS；7 pages、0 BLOCKER、0 ERROR、0 WARN；L3 因無 `prompts-*.md` 合理跳過 |
| 本地連結解析 | PASS；92 條 checked、0 missing |
| 內嵌 JavaScript 語法 | PASS；3 scripts |
| `git diff --check` | PASS |
| restore script syntax | PASS；`bash -n` |
| 搜尋索引 | 已重建；949 筆 |

## 仍需真人確認

- 以實際瀏覽器完成一次「填一題 → 重新整理 → 恢復 → 匯出 → 列印」冷跟做。
- 確認瀏覽器的檔案頁面權限允許 `localStorage` 與下載；若不允許，應依頁面提示使用匯出或離線工作表。
- 確認手機窄版輸入長回答與列印分頁的實際閱讀感受。

本輪判定維持 `MACHINE_READY_PENDING_HUMAN`；已消除「下載文字表格才可開始」的主要學員阻塞，但不把靜態驗證誤稱為真人正式上線驗收。
