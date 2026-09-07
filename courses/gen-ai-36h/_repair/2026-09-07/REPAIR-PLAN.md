# gen-ai-36h 修復批次：2026-09-07

## 狀態

- 修復前備份：READY
- Restore script：READY
- 內容修正：STATIC_VERIFIED
- SaaS 實跑：NOT_RUN
- 真人 cold follow-along：NOT_RUN

## 本批次目標

1. 解開大綱「不含 API」與 Part 5 API 主流程的矛盾。
2. 提供 Part 5 可複製的輸入素材、欄位與測試案例。
3. 為核心操作補上預期結果、快速檢查、恢復點與安全停止。
4. 讓 PRAC6／PRAC7 不需修改 HTML 原始碼即可產出成果。
5. 保留靜態教材、SaaS 實跑與真人試跑的證據邊界。

## 變更範圍

- Part 5：`CH5-1`、`CH5-2`、`CH5-3`、`CH5-4`、`PRAC5`
- Part 6：`CH6-1`、`CH6-2`、`PRAC6`
- Part 7：`CH7-1`、`CH7-2`、`CH7-3`、`PRAC7`
- 新增 `assets/` 測試素材與欄位契約
- 不修改其他 Part，除非驗證發現必要的導覽或連結修正

## 回復方式

在 `gen-ai-36h/` 目錄執行：

```bash
./_tools/restore-2026-09-07-pre-repair.sh
```

腳本只覆蓋備份中存在的修復前檔案；本批次新增的資產與報告需按報告記錄另行處理。

## 第二批：Part 1–4 操作契約

- 為 16 個 CH／PRAC 頁補上 Demo、Together、Solo、Check 的可觀察交付契約。
- 明示預期結果、測試資料、人工檢查、恢復點與 `NOT_RUN` 邊界。
- 不把帳號登入、外部部署或工具功能可用性寫成已驗證。

驗收：Part 1–4 的頁面均有頁面級操作契約，且整課 lint 無 BLOCKER／ERROR。
