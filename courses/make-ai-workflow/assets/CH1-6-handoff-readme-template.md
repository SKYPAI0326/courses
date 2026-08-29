# handoff-pack-v1

## 先讀這裡

本資料夾是從 `scenario-v1`（Make 路徑）或 `scenario-v1-offline-map`（離線路徑）延伸的單一變因變體。正式原版保持不變；所有 JSON 與測試資料都已去敏。先填執行模式，再依序閱讀本 README、規格、契約／映射、差異、測試；只有 `MAKE` 模式才可在自己的 Make 工作區重綁連線並補實際證據。

## 目錄

```text
handoff-pack-v1/
├── README.md
├── variant-v1.md
├── contract-and-mapping.md
├── blueprint-safe-v1.json
├── diff-log-v1.md
├── test-cases-v1.md
├── limitations.md
├── restore.md
└── demo-record-v1.md
```

## 這個版本改了什麼

- 需求：
- 唯一主要變因：
- 明確不變：

## 執行模式與證據界線

- 執行模式：`MAKE`／`SIMULATED`
- `MAKE` 的執行 ID／Docs URL／停止訊息：
- `SIMULATED` 的固定輸出與預期路由：
- 尚未在平台驗證的項目：

## 如何開始驗證

1. 先確認沒有 credential、token、固定帳號、檔案 ID 或個資。
2. 閱讀 `variant-v1.md` 與 `contract-and-mapping.md`。
3. 依 `test-cases-v1.md` 執行或模擬成功、待人工、缺值三條路徑。
4. `MAKE` 模式將實際輸出、停止位置與文件 URL 寫回測試紀錄；`SIMULATED` 模式改填預期輸出與 `{{simulated_document_url}}`，不得填虛構 URL。

## 限制與還原

- 尚未驗證的部分：
- 目前負責人：
- 還原來源：`scenario-v1`／`blueprint-safe-v1.json`
- 還原步驟：
