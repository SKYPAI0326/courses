# 2026-09-13｜全流程修正順序

本檔只排順序，不代表本輪已完成所有修正。每一批修正都要在該批完成後重新產生 audit report，並保留平台 `NOT_RUN` 狀態直到人工證據回來。

## Gate 0：保留目前狀態

- [x] #07 修正版已有 backup、restore script 與 repair report。
- [x] 對本次總覽／README／各頁版本文字建立 backup。
- [x] 將本報告、掃描器與還原腳本納入本次修正提交，避免線上檔案與人工驗證版本漂移。

## Gate 1：入口與高風險回應（靜態修正已完成，平台驗證仍待人工）

1. 重新封裝 `n8n-starter-kit.zip`，使下載包與 `assets/n8n-starter-kit/` 原始模板逐檔一致；版本以 2.37.7 為準。
2. 重新下載／同步 Lite Pack，確認 #07 不再是 `lastNode`；在 n8n UI 以更新後 JSON 取代舊 #07，避免資料庫繼續執行舊版。
3. 修正總覽頁：14 個 workflow、#01 GET、#07 GET、#02 Gemini 3.6、各節點數的計數口徑。
4. 修正 Lite Pack README：移除 #07 必須先啟動 #06 的錯誤依賴；清楚說明 Lite Pack（workflow）與 Starter Kit（Docker／tunnel）分工。
5. 對 #12 補上實際 Set + `lastNode` 回應說明、索引素材前置條件與通過判準。
6. 重新跑所有頁的 stale claim scan、lint 與 ZIP parse。

## Gate 2：文件版本與計數口徑

- 將仍寫 `Lite Pack v0.9／2026-05` 的頁尾統一為目前驗證基線，並標示 Windows 尚待實機驗證。
- 每頁的節點數統一標示「可執行節點」；若另計 sticky note，明確寫「另含 1 張說明卡」。
- 不把縮寫節點名稱誤判為 JSON 失配；以節點類型、method、path、response mode 與欄位契約為準。

## Gate 3：平台人工驗證矩陣

依序一次跑一個 workflow；每個流程都留下：匯入截圖、觸發動作、輸入檔／請求、節點綠框、輸出檔或回應、錯誤／重試證據。

| 批次 | 流程 | 優先原因 |
|---|---|---|
| A | #07、#12 | Webhook response／素材前置條件；先排除會卡住後續教學的入口。 |
| B | #08、#10、#11 | Expression、檔案 fan-out、CSV 產出；確認資料對齊與檔案數。 |
| C | #09 | 需要 Gmail OAuth，另留 credential／polling 證據。 |
| D | #13、#14 | Schedule、歷史檔、異常分支；需確認「無異常不通知」與輸出檔。 |

## Gate 4：跨平台

- Mac：重新下載同步後，使用 Starter Kit 指定的 n8n 2.37.7 實跑；目前 Downloads 中的 2.17.8 只能列為舊版證據。
- Windows：同一份 Lite Pack、同一份 Starter Kit，至少重跑 A～D 每批一個代表流程，再補齊所有流程的匯入／輸出證據。
- 路徑一律使用容器 `/files/shared/...`；主機差異只出現在 Downloads、`.command`／`.bat` 與 PowerShell 操作。

## 完成條件

只有同時滿足下列條件，才可宣稱「14 個流程已驗證」：

1. 下載 Starter Kit ZIP 與原始模板逐檔一致，且映像版本為目前驗證基線。
2. JSON 14／14 可匯入，無未解析 placeholder 或舊 Gemini model。
3. 14 個頁面與 JSON 的觸發方法、path、輸出欄位、節點數口徑一致。
4. 總覽與 README 不再提供過期方法、模型、數量或錯誤依賴。
5. Mac 與 Windows 均有可追溯平台證據；沒有證據的流程維持 `NOT_RUN`。
