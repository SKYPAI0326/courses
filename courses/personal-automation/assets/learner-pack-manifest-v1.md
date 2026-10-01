# Learner Pack Manifest v1｜學員素材索引

**根目錄**：`courses/`
**用途**：保證學員、講師與 RAG 系統能用一致檔名找到同一份素材。路徑不以本文件所在資料夾為根。

## Make 核心素材

| asset_id | 路徑 | 第一次使用 | 用途 | 無法取得時 | 狀態 |
|---|---|---|---|---|---|
| `MAKE-REF-BLUEPRINT` | `make-ai-workflow/assets/CH1-1-reference-4module.sanitized.blueprint.json` | MAKE-CH1-1 | 讀取原始四模組的資料流 | `make-ai-workflow/assets/CH1-1-import-map.md` 列印版 | READY／參考 |
| `MAKE-CONTRACT-SPEC` | `make-ai-workflow/assets/CH1-3-contract-driven-v1.blueprint.spec.json` | MAKE-CH1-3 | 契約驅動流程規格 | 使用同頁 module cards 與固定輸出 | DRAFT_NOT_IMPORTABLE |
| `MAKE-INPUT-FIXTURE` | `make-ai-workflow/assets/CH1-3-test-data.csv` | MAKE-CH1-2 | 契約版輸入資料 | 教師提供同版 CSV | READY |
| `MAKE-OUTPUT-FIXTURE` | `make-ai-workflow/assets/CH1-3-gemini-output-fixtures.json` | MAKE-CH1-3 | A／B／C 固定輸出與型別錯誤 | `CH1-3-offline-run-fixture.md` | READY／SIMULATED |
| `MAKE-HANDOFF-TEMPLATE` | `make-ai-workflow/assets/CH1-6-handoff-readme-template.md` | MAKE-CH1-6 | 封裝交接包 | 列印版欄位表 | READY |

## Bridge 與 n8n 素材

| asset_id | 路徑 | 第一次使用 | 用途 | 無法取得時 | 狀態 |
|---|---|---|---|---|---|
| `BRIDGE-PLATFORM-MAP` | `personal-automation/assets/platform-map-v1.md` | BRIDGE-1 | 記錄 Make／n8n 的責任差異與重測 | 使用 Bridge-1 完成範例表 | READY |
| `BRIDGE-CAPSTONE-CONTRACT` | `personal-automation/assets/integration-capstone-contract-v1.md` | BRIDGE-1／N8N-M4 | 核對成功、待人工、缺值三種終態 | 教師提供同版列印版 | READY |
| `N8N-BRIDGE-FIXTURE` | `n8n/assets/workflows/m4-bridge-contract-fixture.json` | N8N-M1-3／整合 spine | 無 credential 的契約檢查與 A／B／C 分流候選 | 依 integration spine 手動建立 | DRAFT_IMPORT_CANDIDATE |
| `N8N-STARTER-KIT` | `n8n/assets/n8n-starter-kit.zip` | N8N-M1-1 | Docker、Compose、跨 OS 啟動素材 | 教師示範或模擬紀錄 | READY／環境待驗證 |
| `N8N-SAMPLE-PACK` | `n8n/assets/n8n-sample-pack.zip` | N8N-M3 | 本機 PDF／文字檔固定資料 | 教師提供同版資料夾 | READY |

## 取得與證據規則

1. 第一次使用資產前，正文必須引用本 manifest 的 `asset_id`、檔名、用途與狀態。
2. `DRAFT`、`DRAFT_IMPORT_CANDIDATE` 與 `SIMULATED` 不得寫成已匯入或已執行。
3. 學員包若改變資料夾結構，必須同步更新本 manifest、正文引用與授課版回指。
4. 缺檔時只能走指定替代路徑；不得要求學員自行生成另一份不同版本的 fixture。
