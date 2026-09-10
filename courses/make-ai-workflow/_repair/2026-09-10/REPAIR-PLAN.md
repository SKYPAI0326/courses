# Repair Plan：make-ai-workflow（2026-09-10）

## 執行順序

### P0｜跨平台契約補齊

1. 新增 `BRIDGE-1-make-n8n-contract-v1.md`，定義封裝格式、兩種任務型別、轉換前後 JSON、欄位語意與證據模式。
2. 在 CH1-6 的專題與交接段落加入跨平台銜接示範，要求學員先選 `task_type`，再決定原樣傳遞或建立轉換器。
3. 將跨平台契約列入 CH1-6 交接包與試跑包完成條件。
4. 新增 `CH1-6-bridge-worksheet.md`，把 `task_type`、對應欄位、外層封裝與三筆驗收集中到學員可取得的工作表。
5. 將 CH1-6 的 Bridge 練習限制在 `document_request` → n8n M4-1 主線；`customer_feedback` 保留為辨識延伸，避免下游路徑誤接。
6. 在 CH1-6 Bridge Checkpoint 加入 n8n M4-1／M4-2 明確下一頁連結，並把頁面入口順序調整為情境 → 完成物 → 材料 → 模式說明。

### P1｜n8n 對齊

1. n8n Module 4 連結 Make 的共同契約文件。
2. 修正 bridge fixture：`urgency_signal` 缺值時保留為 `null`，不因選填欄位阻斷流程；輸出仍保留 `SIMULATED` 邊界。
3. 在 n8n 的本機核心與外部延伸說明中，標出「資料契約轉換」是必要節點。
4. M1-3 改用 Set 的 `ai_text` → Code `JSON.parse()`，新增固定文字資產與 macOS／Windows 測試指令。
5. M4-1 增加下載後工作目錄、本機／BRIDGE 分流 Checkpoint、必填欄位驗證與契約錯誤出口。
6. M4-2 補 `request_id`、本機 `status`、檔案錯誤恢復與 Gmail `NOT_RUN` 規則；M4-3 分離 API／固定資料驗收並補 Header Auth 前置。

### P2｜驗證與紀錄

1. 檢查所有新增連結與 JSON。
2. 執行 Make、n8n 靜態 lint 與禁用句型掃描。
3. 更新修正報告，記錄尚待真人匯入、重綁連線與跨 OS 試跑的項目。
4. Make CH1-3 補上實際 UI 操作卡；CH1-3～CH1-5 開頭提示移到 page hero 之後。

## 邊界

- 不修改既有 Make 的核心四模組契約。
- 不把兩個不同任務的欄位硬合併成同一個語意。
- 不新增付費連接器、固定帳號、憑證或個資。
- 不宣稱尚未在平台實跑的流程已完成。
