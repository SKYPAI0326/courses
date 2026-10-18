# 完整課程設計系統

這份文件是操作手冊。系統的目的，是在保留外部證據、可讀課程文案與真實操作驗證的前提下，快速產出一門學員能獨立閱讀、跟做、修復並完成成果的網頁課程。

## 系統入口

新課一律由 `course-run` 開始。它維護一份 `course-contract.json`，自動調度各能力並在證據通過後推進下一個 Gate。只有五種情況詢問使用者：

1. 缺少的資訊會改變學員、成果、範圍、順序、評量、方式或時數。
2. 有多個證據充分、但會產生不同課程結果的重大判斷。
3. 下一步需要付費。
4. 下一步需要帳號、憑證、私人資料、存取權或著作權判斷。
5. 下一步會發布、部署、註冊、改變存取權或修改外部系統。

其他研究、撰寫、素材、版型、驗證與本機可回復作業由系統繼續完成。

## G0–G6

| Gate | 核心工作 | 必要完成證據 |
|---|---|---|
| G0 | 自適應問答確認學員、情境、成果與限制 | 完整需求事實、假設、未知、驗收條件 |
| G1 | 外部研究與真實工具測試 | 可追溯來源、日期、版本、衝突、未知、hands-on 結果、適配決策 |
| G2 | 建立一份有理由的課程藍圖 | 成果、評量、能力進程、單元、依賴、時數與風險 |
| G3 | 撰寫正式教學內容 | 可讀敘事、完整示範、引導與獨立練習、檢查、修復、遷移與素材引用 |
| G4 | 製作最高風險代表單元 | HTML 忠實度、真實 render、三種裝置、無障礙、素材可用性與獨立 AI 試走 |
| G5 | 整合全課 | 全單元與素材覆蓋、不同學習成果、產物依賴、導覽、最終成果驗收與 full-course trial |
| G6 | 發布就緒與維護治理 | 技術、連結、註冊、存取、備份、回復、維護與 exact-target 發布提案 |

Gate 通過依賴索引過的證據，不依賴使用者逐關按同意。缺必要證據設為 `BLOCKED`；驗證確定失敗設為 `FAIL`；上游語意變更讓下游變成 `STALE`。

## 角色與單一責任

- `course-run`：母系統、G0、Gate 推進、變更控制與提問邊界。
- `course-researcher`：G1 外部資料、版本與 hands-on。
- `course-pm`：G2 單一主藍圖，不重問 G0，也不選固定課型模板。
- `course-designer`：G3 正式課程內容的唯一作者。
- `course-copywriter`：依證據診斷與修正文案連續性，不把正文改成待辦清單。
- `build-course-page`：G4/G5 學員頁製作；版型依主題、學員、任務、密度與裝置自行決定。
- `course-validator`：內容、忠實度、操作與獨立試學的唯一驗證入口。
- `course-ops`：G6 註冊、存取、索引、發布提案、回復與維護。
- `course-reviewer`、`course-register`：舊呼叫相容入口，分別轉送 validator 與 ops。
- `course-refresh`：只讀新鮮度掃描。
- `course-repair`：既有課程可回復修復，與新課流程分離。

## 核心紀錄

所有正式紀錄都有 JSON Schema：

- `contracts/course-contract.schema.json`：生命週期與外部動作。
- `contracts/course-research-record.schema.json`：外部研究。
- `contracts/course-lesson-record.schema.json`：正式教學內容。
- `contracts/course-asset-manifest.schema.json`：素材用途、來源、權利、版本、學員路徑與開啟測試。
- `contracts/course-pilot-record.schema.json`：代表單元與視覺決策。
- `contracts/course-trial-record.schema.json`：隔離的獨立 AI 或真人試學。
- `contracts/course-production-record.schema.json`：全課整合與最終成果。
- `contracts/course-release-record.schema.json`：G6 發布就緒。

長篇研究、正文、畫面、執行紀錄與完成品保留在外部檔案；contract 只索引相對路徑與 SHA-256，避免把內容壓成欄位摘要。

## 教學內容最低條件

每個核心操作都要先交代使用情境、輸入與要完成的成果，再用自然可連續閱讀的文字說明判斷理由。完整示範必須包含輸入、中間判斷、實際動作、結果與驗證；練習要讓學員真的產出東西，並提供可觀察檢查與失敗恢復。

系統會阻擋：

- 以名詞清單、待辦事項或內部編碼檔名取代說明。
- 沒有前因後果的操作指令。
- 只有範本欄位、placeholder 或「請自行完成」。
- Demo、Together、Solo 改標籤後重複同一工作。
- 核心素材只有檔名，學員找不到、打不開或不知道用途。
- HTML 把 lesson 中的表格、prompt、範例、理由或修復內容壓成摘要。

validator 只指出缺口與回送責任，不為了讓欄位齊全而替作者發明正文。

## 主題差異化與版型

共同標準固定在成果可驗收、來源可追溯、內容可讀、操作可執行、素材可取得、錯誤可恢復與證據可重現。課程不套用固定整體版型。

G1/G2 依學員差距、真實任務、工具依賴、內容變動、錯誤成本與所需證據決定教學策略。G4 再依主題、學員、任務、內容密度與主要裝置，選擇課程專屬的導覽、排版、色彩、資訊層級與 RWD 策略，同時維持可讀性、鍵盤操作、focus、閱讀順序與無水平溢位等共同底線。

## 獨立試學

G4 試走代表單元，G5 試走完整課程。執行 AI 必須未參與作者、頁面製作、review 或 validation，並使用全新的隔離情境。它只能看到學員會拿到的頁面與素材，不能取得 contract、研究摘要、作者筆記、答案鍵或製作對話。

試走紀錄包含入口、逐步動作、提示來源、卡點、修復、完成品 hash 與驗收結果。G5 不能沿用 G4 context。完成品不完整、無法驗證、讀到內部資料或執行者不獨立都不能通過。

失敗依原因回送：來源／工具到 G1；順序／難度到 G2；解釋／練習到 G3；介面／素材到 G4；全課整合到 G5；存取／部署到 G6。

## 發布

G6 `PASS` 等於 `READY_TO_PUBLISH`，不等於已發布。`course-ops` 先在 staging 準備檔案，建立包含 target、before hash、after hash、backup 與 rollback 的 deterministic manifest。使用者授權的是該份 manifest 的 SHA-256。

套用時若授權缺失、hash 不符、來源被改、正式目標被改或授權已使用，就停止。開始套用會消耗授權；成功逐檔原子替換並記錄結果，失敗回復已動目標。新 manifest 必須重新授權。

## 維護與修復

`course-refresh` 只讀 metadata 與官方資訊，產生 severity、affected Gate 與 next action。日期老化只是重查優先順序。確認內容真的漂移後，由 `course-repair` 依 `scan → plan → backup → fix → verify` 處理。

修復可使用 validator 證據格式，但不宣稱補齊一套新課 Gate 歷史。若修復要重定義主要學員、核心成果或全課架構，建立新的 G0 contract。

## 驗證與安裝

```bash
export COURSE_DESIGN_SYSTEM_ROOT=/absolute/path/to/course-design-system
export COURSE_WEB_ROOT=/absolute/path/to/managed-courses
export SKILLS_ROOT=/absolute/path/to/skills
export COURSE_DESIGN_STATE_ROOT=/absolute/path/to/course-design-state

python3 -m unittest discover -s tests -v

python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/install_course_skill_foundation.py" \
  --verify-source

python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/install_course_skill_foundation.py" \
  --dry-run --skills-root "$SKILLS_ROOT"

python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/install_course_skill_foundation.py" \
  --apply --skills-root "$SKILLS_ROOT" \
  --allow-update course-run \
  --allow-update course-validator

python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/install_course_skill_foundation.py" \
  --verify-installed --skills-root "$SKILLS_ROOT"

python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/course_run.py" doctor

# 中斷的 PREPARED/EXECUTING 安裝必須先回復，才可重跑 apply。
python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/install_course_skill_foundation.py" \
  --recover-operation "$COURSE_DESIGN_STATE_ROOT/operations/course-skill-foundation/OPERATION_ID"
```

每個 package 都由 manifest hash 鎖定。安裝前顯示 `ADD`、`UPDATE`、`UNCHANGED`；更新先備份。Recovery 與 rollback 另以呼叫端提供的三個 root 和 operations root 下的唯讀 authority receipt 核對 operation identity、package set、target 與 hash；operation manifest 被改寫或安裝後內容有變更時會 fail closed。

`operations`、registry、report 與 backup 預設寫入 repo 外的 `COURSE_DESIGN_STATE_ROOT`。runtime 與 doctor 支援 POSIX macOS/Linux；Windows 的 lock 語意尚未實作，會 fail closed。`course-repair fix` 也維持 fail closed，直到 Task 8 把 approved plan hash、before hashes、完整 backup 與 isolated restore proof 接入中央 transaction。
