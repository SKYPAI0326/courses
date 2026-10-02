# Course Manager

這是課程資料夾的管理控制平面，不是 learner-facing 課程頁面。

標準流程：

    scan → find/inspect → propose → approval → apply → verify

`scan`、`find`、`inspect` 與 `verify` 對課程資料夾唯讀；`propose-*` 只寫入管理專案自己的提案檔。正式課程 HTML、共用資產、備份、修復、工具、驗證與輸出資料夾預設不可搬動；必須先有提案、核准檔、manifest 與驗收結果。

## 使用流程

```sh
python3 course-manager/manager.py scan --write
python3 course-manager/manager.py find <keyword>
python3 course-manager/manager.py find <keyword> --json
python3 course-manager/manager.py inspect <folder>
python3 course-manager/manager.py propose-move <source> <destination>
python3 course-manager/manager.py propose-merge <source> <target>
python3 course-manager/manager.py verify
```

`propose-*` 只會在 `course-manager/proposals/` 產生 JSON 提案。只有提案狀態可執行、核准檔含有相同 `proposal_id` 且 `approved: true` 時，`apply` 才會依 manifest 操作；`rollback` 使用同一份核准檔回復。正式課程 HTML、支援目錄、引用更新與檔案衝突預設會進入 BLOCK 或需要人工決定。

管理工具自身不產生 learner-facing HTML。掃描、提案、操作與驗收紀錄都保存在 `course-manager/`，不會替其他課程資料夾自動建立頁面或執行 Git staging。

`find` 預設列出每個匹配專案的完整 `PROJECT_PATH`，並附上可直接貼到 macOS 終端機執行的 `OPEN_COMMAND`。需要完整 catalog 欄位時使用 `find <keyword> --json`，每筆結果也會包含 `open_path`。`inspect` 的 JSON 會在開頭附上 `absolute_path`。
