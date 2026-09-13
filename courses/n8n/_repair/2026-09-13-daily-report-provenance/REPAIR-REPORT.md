# #04 定時 AI 日報：來源追蹤修正報告

日期：2026-09-13
範圍：`n8n-lite-pack.zip` 的 #04 workflow、#04 網頁講義、Mac／Windows 安裝驗收段落

## 修正結果

1. #04 Code 節點會從 Read 節點回查 binary 檔名，保留 `fileName` 與 `sourcePath`；每次輸出 JSON 另提供 `filesCount`、`filesProcessed`、`sourceFiles`。
2. AI prompt 增加來源標記、未指定欄位與衝突資訊規則：輸入沒有提供的人名、日期、金額或狀態不補寫；不同來源的數字或決策並列標示。Code 另設來源標記閘門，任一檔名未被 AI 回應引用時改為人工核對狀態。
3. 日報產出前移除 `<br>` 標籤，檔尾固定附「來源檔案」清單與人工核對提醒。
4. #04 網頁講義改為 8 個功能節點（另有 1 張說明卡），補上 Switch 分流、兩條抽取路徑、`aggregateAllItemData` 與來源欄位的實際行為。
5. Mac／Windows C5 驗收新增三項可觀察證據：`filesCount` 等於成功抽取且可摘要的檔案數、`filesProcessed` 列出實際檔名、日報檔尾含來源清單；所有格式受支援且內容足夠時，該數量應與輸入檔數相等。發現未提供的欄位時須回原檔人工核對。

## 備份與回復

修正前檔案存於：`n8n/_backup/2026-09-13-pre-daily-report-provenance/`。
回復腳本：`n8n/_tools/restore-2026-09-13-pre-daily-report-provenance.sh`。

## 驗證證據

- ZIP 內 workflow JSON：14 份，全部可解析。
- #04 功能節點：8 個；Sticky Note：1 張。
- #04 Code JavaScript：`node --check` 通過。
- 模擬執行：兩份來源均被列入 `filesProcessed`、`sourceFiles`，並成功產生來源清單；刻意缺少一個來源標記時，輸出轉為人工核對狀態且 `aiError` 記錄缺少檔名。
- 來源防線字串：`filesCount`、`filesProcessed`、`sourceFiles`、`未指定`、`衝突`、binary 檔名回查與 `<br>` 清理均存在。
- `bash -n n8n/_tools/restore-2026-09-13-pre-daily-report-provenance.sh` 通過。
- `docs/lint-page.py` 掃描 3 頁：BLOCKER 0、ERROR 0（WARN 8 為既有頁面提示）。
- `git diff --check` 通過。

## 尚待人工驗證

Mac 的 #04 平台執行已可用輸出 JSON 與日報來源清單驗證；Windows 文件已同步，Windows Docker Desktop 實機仍需依 C5 流程試跑。若 AI 回應與來源不一致，保留輸出並回查原始檔案，不以 `aiError: null` 單獨判定內容正確。
