# Course Manager 課程管理架構設計

**日期**：2026-10-02  
**狀態**：設計已獲採用，待實作計畫審閱  
**適用根目錄**：`/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses`

## 1. 目的

建立一個位於 `course-manager/` 的課程管理控制平面，讓後續每次新增、搬運、拆分、封存或合併課程時，都能先讀取目前資料夾與來源內容，再用可追溯的提案與驗收流程執行。

它服務的是課程資料夾的管理者與 Codex 協作流程，不是 learner-facing 課程網站，也不取代既有的課程設計、HTML contract、課程修復與 release validator。

## 2. 已確認的使用情境

### 2.1 查詢既有課程

使用者詢問「有哪些類似課程」、「某課程目前在哪裡」、「哪些資料夾已有 HTML 講義」或「哪些專案只有來源檔」時，管理工具先讀取索引的新鮮度，再回報證據與路徑，不憑資料夾名稱猜測。

### 2.2 新增課程

使用者提供新主題或一個既有資料夾時，工具先搜尋相似課程、無講義專案、來源文件與相依資產，產生候選比較，然後提出 `建立新專案`、`沿用來源`、`搬運` 或 `合併` 建議。

### 2.3 搬運專案

搬運前分析 HTML、Markdown、設定、腳本、資產與文件中的路徑引用；若涉及 learner-facing HTML、共用資產、備份或管理目錄，預設 BLOCK。只有明確核准的範圍才能進入執行。

### 2.4 合併專案

先比較檔案清單、檔案雜湊、HTML 頁面、教案來源、資產與相依引用。相同內容可標示為 `identical`，不同內容但同一路徑標示為 `conflict`，不自動覆蓋或猜測應保留哪一份。

## 3. 設計原則

1. 先掃描、再分析、再提案、取得核准後才寫入。
2. 「沒有 HTML」只是分類訊號，不是可搬移證據。
3. 正式課程資料夾與共用支援資料夾採保守策略。
4. 每次變更都要有基線、操作清單、回復資訊與驗收結果。
5. 產生的索引可以協助詢問，但若已過期，回答必須標示過期並要求重新掃描。
6. 輸出證據優先於敘事：路徑、檔案類型、引用、雜湊、驗證結果都要能回查。
7. 不使用 `git add -A`，不覆蓋使用者既有未提交變更，不把其他專案的未追蹤檔案納入操作。

## 4. 系統邊界

### 4.1 管理範圍

- 根目錄第一層的課程、來源專案、無講義專案與支援資料夾。
- 子資料夾內的 HTML、Markdown、PDF、DOCX、JSON、JavaScript、CSS、圖片、備份與修復紀錄。
- 專案之間的相對路徑引用、HTML 本地資源引用與明顯的根目錄路徑文字。
- Git tracked/untracked 狀態與目前工作樹差異。

### 4.2 不在第一版範圍

- 不建立 Web UI、資料庫或常駐背景服務。
- 不自動做語意內容合併，不替使用者決定哪份課程文案正確。
- 不自動搬動含 learner-facing HTML 的正式課程資料夾。
- 不自動搬動 `.worktrees`、`_backup`、`_repair`、`_tools`、`_validation`、`assets`、`docs`、`output`、`tmp` 等共用或管理資料夾。
- 不取代既有 HTML lint、course-validator、cold follow-along 或部署檢查。

## 5. 目錄架構

```text
course-manager/
├── README.md
├── manager.py                       # CLI 入口，僅組合各操作服務
├── registry/
│   ├── catalog.json                 # 最近一次成功掃描的查詢索引
│   └── schema.json                  # catalog schema version 1
├── reports/
│   ├── scans/                       # 唯讀掃描報告
│   ├── inspections/                 # 單一專案深度分析
│   └── verifications/               # 搬運／合併後驗收報告
├── proposals/
│   ├── moves/                       # 搬運提案
│   ├── merges/                      # 合併提案
│   └── new-courses/                 # 新課程建案提案
├── operations/
│   ├── manifests/                   # 已核准操作的檔案與雜湊基線
│   └── logs.jsonl                   # append-only 操作摘要
├── policies/
│   ├── folder-classification.md
│   ├── move-safety.md
│   └── merge-safety.md
├── src/
│   ├── catalog.py                   # catalog schema 與讀寫
│   ├── discover.py                  # 資料夾與檔案訊號掃描
│   ├── inspect.py                   # 內容、引用與相依分析
│   ├── proposals.py                 # move/merge/new proposal 產生器
│   ├── operations.py                # 核准後的受限檔案操作
│   └── verify.py                    # 操作後驗收
└── tests/
    ├── test_discover.py
    ├── test_inspect.py
    ├── test_proposals.py
    ├── test_operations.py
    └── test_verify.py
```

`course-manager/` 自身不得產生 learner-facing HTML，且掃描器會把它標記為 `management`，避免把管理報告誤列成課程頁面。

## 6. 分類模型

每個管理對象都有 `kind`、`status`、`evidence` 與 `risk` 四組欄位。

### 6.1 `kind`

| kind | 判定意義 |
|---|---|
| `course-html` | 目前含 learner-facing HTML，並有章節、實作或課程入口訊號 |
| `source-only` | 有教案、outline、lesson plan 或課程素材，但目前沒有 learner-facing HTML |
| `no-handout-project` | 獨立專案，目前沒有網頁講義，且不只是共用支援資料夾 |
| `support` | 備份、工具、資產、驗證、輸出或管理資料夾 |
| `management` | `course-manager/` 自身及其產物 |
| `unknown` | 證據不足，必須人工 inspect |

### 6.2 `status`

`active`、`candidate`、`blocked`、`archived`、`needs-review`。

`blocked` 表示不能安全搬運或合併，不表示內容不存在；`needs-review` 表示掃描器無法只靠結構訊號判斷用途。

### 6.3 `evidence`

至少記錄以下計數或布林值：

- `html_count`、`learner_html_count`、`index_count`。
- `lesson_signal_count`：`CH*`、`PRAC*`、`lessons/`、`module*` 等檔案。
- `source_signal_count`：`*.md`、`*.docx`、`*.pdf`、`_plan`、`_gates`、`COURSE-*` 等。
- `asset_signal_count`：圖片、CSS、JS、資料、fixture 與素材資料夾。
- `has_backup`、`has_restore_script`、`has_outline`、`has_ag`。
- `reference_count`、`unknown_reference_count`。

掃描器只記錄訊號；最終分類仍要保留 `classification_reason`，讓後續詢問能說明判斷依據。

## 7. Catalog 資料契約

`registry/catalog.json` 使用明確的 schema version，最小記錄如下：

```json
{
  "schema_version": 1,
  "root": ".",
  "scanned_at": "2026-10-02T00:00:00+08:00",
  "git": {
    "branch": "main",
    "worktree_dirty": true
  },
  "items": [
    {
      "id": "admin-ai-assistant",
      "name": "admin-ai-assistant",
      "path": "admin-ai-assistant",
      "kind": "course-html",
      "status": "active",
      "html_count": 8,
      "learner_html_count": 8,
      "signals": {
        "has_index": true,
        "lesson_signal_count": 6,
        "source_signal_count": 4,
        "asset_signal_count": 3
      },
      "risk": {
        "move": "blocked-by-default",
        "merge": "requires-review",
        "reasons": ["contains learner-facing HTML"]
      },
      "references": {
        "outgoing": [],
        "incoming": [],
        "unknown": []
      },
      "fingerprint": {
        "file_count": 0,
        "content_hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
      },
      "last_verified_at": null
    }
  ]
}
```

實作時 `fingerprint.file_count` 與 `content_hash` 必須填入實際值；上例的 `0` 與全零雜湊只用來展示欄位形狀，不得寫入初始 catalog。

## 8. CLI 與操作介面

第一版採 Python 標準函式庫，不引入第三方依賴。所有指令預設唯讀，寫入動作必須使用明確旗標或核准檔。

```text
python3 course-manager/manager.py scan [--write]
python3 course-manager/manager.py find <query> [--kind <kind>] [--stale-ok]
python3 course-manager/manager.py inspect <path> [--deep]
python3 course-manager/manager.py propose-new <topic-or-path>
python3 course-manager/manager.py propose-move <source> <destination>
python3 course-manager/manager.py propose-merge <source> <target>
python3 course-manager/manager.py verify [--baseline <manifest>]
python3 course-manager/manager.py apply <proposal> --approval <approval-file>
```

### 8.1 `scan`

掃描資料夾、分類訊號、Git 狀態與相依引用。沒有 `--write` 時只輸出報告；使用 `--write` 才更新 `registry/catalog.json` 與掃描報告。

### 8.2 `find`

先顯示 catalog 的 `scanned_at` 與工作樹變更提示，再依名稱、路徑、kind、HTML 數量、主題文字與來源文件名稱搜尋。若索引過期，不得把結果描述為目前確認狀態。

### 8.3 `inspect`

讀取指定資料夾的目錄樹、關鍵文件標題、HTML metadata、來源文件、相依引用與目前分類理由。`--deep` 才讀取較大量的正文；預設輸出檔案清單與摘要，避免一次載入整個課程。

### 8.4 `propose-*`

只產生 Markdown 與 JSON 提案，不改動來源。提案必須列出候選來源、目的地、檔案差異、引用風險、現有 HTML 影響、預計回復方式與待使用者決定的衝突。

### 8.5 `apply`

只接受指定提案與核准檔。執行前再次確認來源雜湊、目的地狀態與工作樹沒有出現未預期變更；不符合就停止，不自行重算方案。

## 9. 搬運安全契約

搬運流程固定為：

```text
discover → inspect → propose → explicit approval → manifest/backup
→ scoped move → reference update only if listed → verify → operation log
```

### 9.1 預設 BLOCK 條件

- 來源或目的地含 learner-facing HTML，且提案沒有明確列出影響範圍。
- 有 HTML、Markdown、腳本或設定引用來源路徑，但沒有路徑更新計畫。
- 目的地已存在同名檔案，且未分類為 identical 或 conflict。
- 來源是共用資產、備份、修復、工具、驗證或輸出資料夾。
- 工作樹在提案產生後變更，或來源 fingerprint 不一致。
- 不能建立可回復的操作 manifest。

### 9.2 可執行搬運的最低證據

- 完整來源與目的地檔案清單。
- 每個受影響檔案的 SHA-256。
- incoming/outgoing references 清單。
- 搬運前正式課程 HTML 基線數量。
- 受影響引用的精確替換表。
- 明確的 rollback 操作順序。
- 使用者核准的 proposal id。

不以 `git add -A` 建立基線；只操作 proposal 列出的來源與目的地。

## 10. 合併安全契約

合併比較以相對路徑為鍵：

| 狀態 | 行為 |
|---|---|
| destination 不存在 | 標記為可新增，仍需核准 |
| 同路徑且 SHA-256 相同 | 標記 `identical`，不重複覆蓋 |
| 同路徑且內容不同 | 標記 `conflict`，BLOCK 自動合併 |
| 任一方含 learner-facing HTML | 至少人工審查頁面與資產引用 |
| 任一方含課程來源但另一方有同名來源 | 要求內容責任人決定保留、改名或合併 |

第一版只產生衝突表，不嘗試語意合併 Markdown、HTML、DOCX 或 PDF。

## 11. 驗收契約

`verify` 至少檢查：

1. 正式課程 HTML 數量與搬運前基線一致，除非 proposal 明確宣告變化。
2. 正式課程資料夾的 HTML 本地 `href`、`src`、`poster` 目標存在。
3. 受影響的 incoming/outgoing references 已更新，未列入的引用不被靜默修改。
4. 搬運來源已不存在或符合 proposal 的 compatibility 設計。
5. 目的地檔案雜湊與預期一致。
6. `git diff --check` 通過；未追蹤檔案與既有變更沒有被意外納入。
7. rollback manifest 能定位每個搬入、搬出與更新檔案。
8. catalog 的路徑、kind、fingerprint 與最新工作樹一致。

驗收報告需明確區分 `PASS`、`WARN`、`BLOCK`；lint 通過不能取代頁面、素材與實際學員路徑驗證。

## 12. 新課程建案流程

使用者提出新課程時，Codex 依序執行：

1. `scan` 或確認 catalog 新鮮度。
2. 依主題、檔名、標題、outline 與來源內容做候選搜尋。
3. `inspect` 候選資料夾，讀取足以判斷用途的文件與頁面摘要。
4. 產生候選比較：沿用、複製、搬運、合併、重新建立或暫不處理。
5. 在 `proposals/new-courses/` 保存決策理由與證據。
6. 使用者核准後，依 move 或 merge 安全契約執行。
7. 建立新課程的資料夾契約、來源索引與驗收清單。
8. 重新掃描並記錄操作結果。

如果候選只是內容相似但教學成果、受眾、工具環境或素材契約不同，預設建議新專案，不直接合併。

## 13. 初始資料遷移範圍

第一版實作啟動時只建立管理專案與 catalog，不重新搬運目前已完成的資料夾。初始掃描應識別：

- 正式 HTML 課程資料夾。
- `no-web-handouts/` 及其中已搬入的獨立專案。
- `accounting-function-lab` 等尚未搬移、但有來源或計畫的專案。
- 共用、備份、修復、工具、輸出與驗證資料夾。
- 目前工作樹的未追蹤檔案與既有 Git 狀態。

初始 catalog 不得假裝所有分類都已人工確認；對證據不足者使用 `unknown` 或 `needs-review`。

## 14. 驗收標準

架構第一版完成的條件：

- 可在不修改資料夾的情況下產生完整 catalog 與掃描報告。
- 可依名稱、kind、HTML 數量與關鍵字找到正式課程與無講義專案。
- `inspect` 能回報來源文件、HTML、資產與引用證據。
- `propose-move` 與 `propose-merge` 預設不寫入課程資料夾，且能明確指出 BLOCK 原因。
- `apply` 沒有核准檔時拒絕執行。
- `verify` 能偵測 HTML 數量變化、失效本地連結、目的地衝突與 fingerprint 漂移。
- 測試涵蓋 HTML 課程、無講義專案、共用資料夾、空資料夾、未追蹤檔案與同名衝突。
- README 說明未來使用者如何查詢、提案、核准、驗收與回復。

## 15. 後續實作順序

1. 建立標準分類政策、schema 與最小 scanner。
2. 建立 catalog 讀寫與 `scan`／`find`／`inspect`。
3. 建立 move/merge proposal 與衝突報告。
4. 建立 manifest、受限 apply 與 rollback。
5. 建立 verify 與正式課程 HTML／本地連結驗收。
6. 對目前工作樹執行初始掃描，人工抽查分類，再把 catalog 視為可查詢基線。
