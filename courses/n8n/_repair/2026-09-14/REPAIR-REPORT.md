# 2026-09-14｜n8n 講義與 Lite Pack 過時內容修復報告

## 結論

本輪已修正會讓學員走錯路的高風險文案與模板契約，並重新注入、封裝可下載的 Lite Pack。Mac 是目前人工驗證基線；Windows、docx 2.37.7 行為與所有進階案例仍保留實機驗證標記。

## 已處理

- 統一 self-host 操作路徑為 `/files/shared/...`，修正 PDF、日報、資料夾與知識庫相關教材及來源教案。
- 依 n8n 2.37.7 介面改用 `Publish`／`Published`；舊版 `Active` 僅保留為版本差異提示。
- #07 成功判準改以 `Executions` 分頁成功結果與節點輸出為主，不再要求畫布綠框持久存在。
- #01 導覽與 #12 節點名稱同步目前模板（Webhook／Set、Respond 說明）。
- #09 docx 全頁改為「先用 1 份測試檔確認 operation 與 Output；若不支援或不可讀，再採中介格式」；同步來源 Markdown。
- 更新選定 learner-facing 頁尾的版本與驗證範圍，標示 Docker Desktop／n8n 2.37.7、Lite Pack wizard v1.3.5 及 Windows 待驗證狀態。
- 同步 Lite Pack #06／#07／#09／#12 說明，重新注入 #06／#12 Web UI，並重封裝 `n8n/assets/n8n-lite-pack.zip`。
- 補上本次修復的 Lite Pack `_change-log.md` 紀錄。

## 契約與可回復性

- 備份：`n8n/_backup/2026-09-14-pre-repair/`（40 份原始檔，含封裝前 ZIP 與所有本輪修改的來源檔）。
- 還原：`n8n/_tools/restore-2026-09-14-pre-repair.sh`。
- 修復計畫：`n8n/_repair/2026-09-14/REPAIR-PLAN.md`。
- Lite Pack 仍維持外層 `n8n-lite-pack/` 目錄；14 份 workflow 的 JSON 與 webhook response 設定未被重封裝破壞：#06 POST／GET、#07 GET、#12 GET 使用 `responseNode`。

## 驗證結果

| 檢查 | 結果 | 證據 |
|---|---|---|
| HTML lint | 通過 | 掃描 76 頁；BLOCKER 0、ERROR 0、WARN 155 |
| Lite Pack contract（隔離 HOME，排除舊 Downloads 副本） | 通過 | 14 workflow JSON；Overview flags none；Starter Kit archive MATCH；Result PASS |
| ZIP integrity | 通過 | `unzip -t n8n/assets/n8n-lite-pack.zip` 無錯誤 |
| 來源／ZIP 一致性 | 通過 | 解壓後與 `_work/2026-09-13-aq-key-format/n8n-lite-pack` `diff -ru` 無差異 |
| 還原腳本語法 | 通過 | `bash -n n8n/_tools/restore-2026-09-14-pre-repair.sh` |
| stale high-risk scan | 通過 | 無舊 `/files/pdf-inbox`／`pdf-renamed`、Gemini 2.5、`n8n latest`、`Active = ON` 或舊 docx 絕對化字串 |
| 搜尋索引 | 完成 | `search-index.json` 寫入 660 筆 |

## 外部副本與待驗證

若以目前使用者的 `~/Downloads/n8n-lite-pack` 參與合約檢查，會顯示 5 份舊檔 drift：`06`、`07`、`08`、`09`、`12`。這是先前解壓副本尚未重新下載造成，不是 repository ZIP 契約失敗；明天請重新下載並解壓新版 Lite Pack 後再驗證。

本報告不宣稱 Windows 已完成實機試跑，也不宣稱 docx 在 n8n 2.37.7 已完成實機確認；兩者均由後續人工驗證補證據。
