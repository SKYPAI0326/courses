# 課程改善 loop 控制程式

本程式依v0.10管理課程改善紀錄，保存章節狀態、候選歷史、P／Q與人工回饋。原有紀錄模式保留；另提供單章AI階段任務收送，由目前對話中的AI實際評估、改寫與比較，程式檢查回交後決定下一步。程式本身不呼叫模型API、不下載素材、不執行網站操作或正式修復套用；關閉對話後不會自行工作。

新試驗的CLI初始化現在必須指定review_policy，採用[角色派送、必要檢查與覆核放行](course-improvement-review.md)的stages-2流程。下列為既有stages-1流程及共用接口說明；舊state原樣保留。新版accept另需role/model/context-id，作者compare不能直接結案；原稿判無需修改也須檢查與覆核。不要用舊格式重新初始化來繞過新版關卡。

## 單章AI接入模式

隔離試驗先準備config，固定章節用途、來源及規則檔案雜湊，指定與state同目錄的output_root。`artifacts`沿用既有`path`／`sha256`格式，`source`指向原稿參照鍵。初始狀態為未評估，不假造L3或待判定資料。

```bash
python3 scripts/course_improvement_loop.py stage-init --config PATH/config.json --state PATH/state.json
python3 scripts/course_improvement_loop.py next --state PATH/state.json
python3 scripts/course_improvement_loop.py accept --state PATH/state.json --response PATH/assessment-response.json
python3 scripts/course_improvement_loop.py resume --state PATH/state.json
```

`PATH`替換成實際隔離試驗目錄。已存在狀態只用resume／next，不再stage-init。next將派出的任務存入state，回傳固定任務識別碼、階段、允許輸入及輸出位置；同任務尚未完成時重取不建立新任務。AI依任務產檔後，以response回交，不能直接寫state。

| 階段 | response內容 | 接收後 |
| --- | --- | --- |
| assess | task_id、outputs含report與handoff；evaluation含problems、questions、grades、regression、next_fix | 綁定原稿評估；依v0.10決定派改寫或停止 |
| rewrite | task_id、outputs含candidate與report；不得附評級或人工認可 | 保存新候選參照並立即計版，進入compare；尚未比較不算通過 |
| compare | task_id、outputs含report；evaluation同評估欄位 | 綁定目前候選，比對P/Q歷史，更新停止判斷或允許局部續修 |

outputs是隔離目錄內新檔的絕對路徑；接收時由程式計算雜湊。評估資料格式沿用紀錄模式，basis由程式綁定本輪報告；AI不能回填human、額度、用途或限制。既有P/Q身分及核心／必要性不得刪除或降低。改寫後H3固定為pending，沒有讓AI代確認的入口。

同任務完全相同response重送只回duplicate=true，不改state或重複計版；相同任務不同內容拒絕。任務、receipt與階段轉換同筆原子保存；候選接收後即使比較尚未進行，中斷恢復也只回到compare。未通過接收的檔案仍留在隔離目錄供診斷，不能把它們當成已接收候選；輸出若已人工評閱仍須遵循v0.10版本記帳，不得透過拒絕回交規避。

目前輸入版本改變會停止並拒絕繼續；沒有自動搬移／重綁或H1/H2決策解除入口。遇到這些情況保留紀錄，另依具體授權接續，不手動改JSON假裝通過。既有record模式的checkpoint不可直接寫入stages-1狀態。

人工已明確認可閱讀時，先另存回饋原文、適用版本及確認範圍，再由有權登記者執行：

```bash
python3 scripts/course_improvement_loop.py confirm-h3 --state PATH/state.json --feedback PATH/human-feedback.md --candidate-sha256 CANDIDATE_SHA256 --expected-revision CURRENT_REVISION --actor 使用者
```

此入口限已完成比較並停止的章節，核對候選雜湊、目前revision及新回饋檔，原子記錄人工事件並重算狀態。AI任務的accept仍不能回填H3；登記者須依實際人工回饋使用此入口，CLI不具使用者身分驗證能力。相同確認重送不重複寫入；不同回饋、錯版或過期revision拒絕。H3不解除必要Q、H1/H2或用量限制；全部必要條件成立才變complete。resume與next仍不會自動改稿，next在完成後只回停止結果。

本模式是同一對話AI的分階段作者自查，不是獨立審查。控制器驗證格式與狀態，不能判定AI引用或評級的語意真實性。`auto_rewrite=false`表示控制器不自行呼叫模型，不代表本次對話未實際產稿。

待補證案件可用`supplement-evidence --state FILE --evidence FILE --expected-revision N`另行接收新證據，再回評估／比較；不會清除候選或重置額度。有使用者限制時拒絕補證。完整用法與跨章相依見[整課佇列說明](course-improvement-queue.md)。此入口不解除H1/H2，也不將新證據自動判為通過。

若候選已停止等待H3，但人工確認前發現具體漏查，可用`recheck-comparison --state FILE --evidence NEW_REPORT --expected-revision N`將新證據另存後重開比較。此入口只接受尚未確認H3、無其他限制且輸入版本未變的案件；不能重開已完成或H1/H2案件。它保留原報告、receipt、問題歷史與候選用量，只重新派compare，不直接准許改寫。比較須登記新缺口與修法，再由原停止規則決定是否使用剩餘版本；兩版用滿仍不得產第三版。補查不計為一次新改稿失敗，也不能取代H3。

驗證指令：`python3 -m unittest tests.test_course_improvement_loop tests.test_course_loop_stages -v`。本地單章試驗位於`operations/course-content-scoring/loop-trial-gemini-ai-ch2-1/`，原有GTM狀態仍保留在loop-control-v1。

## 已有紀錄模式

從course-manager目錄執行：

```bash
python3 scripts/course_improvement_loop.py status --state operations/course-content-scoring/loop-control-v1/state.json
python3 scripts/course_improvement_loop.py resume --state operations/course-content-scoring/loop-control-v1/state.json
```

`status`與`resume`均為唯讀。恢復表示讀取同一份持久狀態並重新計算可做的動作，不重置額度、不重跑教材修復。檔案版本變動時回報H1待確認，不自動採用新來源。CLI回傳0表示查詢成功，不代表教材已完成；請讀每章的`status`。

## 指令與資料

| 指令 | 行為 |
| --- | --- |
| `init --manifest FILE --state FILE` | 從人工結構化的已有紀錄建立狀態；驗證參照檔案及雜湊，既有state不得覆寫 |
| `status --state FILE` | 查看章節狀態、原因、並存限制及候選用量 |
| `resume --state FILE` | 讀取已保存狀態；本版不派送任何工作 |
| `checkpoint --state FILE --unit FILE --expected-revision N --actor NAME --note TEXT` | 登記一章的完整新紀錄；驗證版本、證據參照、用量與限制後原子保存。錯誤回傳2，拒絕的更新不改state |

manifest包含`units`清單；每章欄位可參考既有GTM manifest。`checkpoint --unit`讀單一章節物件，不是整份manifest。路徑使用絕對路徑，檔案參照包含SHA-256；搬移資料後須明確處理來源變更，本版不自動重新綁定。

每章包含：用途與歷史規則版本、來源及證據參照、候選版本清單、綁定目前版本的評估、P／Q及其核心／必要性、A／B／C、H3回饋版本、H1／H2決策、失敗與修法歷史、使用者限制及下一個具體修法。已解問題保留原識別碼並標記關閉，不能刪掉歷史或降低必要性。

控制程式檢查資料與狀態是否一致，不能判定紀錄文字或人工認可是否真實。輸入須由有權執行者依原文與證據整理；雜湊只辨認版本，不證明內容正確。輸出等級沿用輸入評估，不是程式自動評分。它不是防止使用者直接編輯JSON的防竄改系統。

## 強制規則

- 固定兩個候選版本，清單只能追加一版，不能刪除或改寫舊版；新候選須有新評估及修法歷史。
- 沒有未解P、材料不足、已完成、等待人工或用量耗盡時，拒絕新增候選。
- 待判定須引用必要Q；L1封頂須引用已知核心P。尚未實測不能單獨成為封頂依據。
- H3認可須指向目前候選及回饋紀錄；新候選不能繼承舊H3。既有H3要求不能改成不適用。
- 同一問題失敗兩次轉H2；失敗次數與修法歷史不能清零，有失敗後的補救不可重複同一修法。
- 額度耗盡但已達完成條件可完成；有必要Q則以等待補證為主要狀態，並列額度、H3及使用者限制。
- 來源、用途、使用者限制及兩版上限不能透過checkpoint更改。本版未提供擴大授權或遷移入口。
- `ready_for_revision`只表示可登記外部已產出的候選，仍不會執行改寫。所有狀態均回報`auto_rewrite=false`及`can_execute_course_operations=false`。

## 恢復與儲存

state在同一JSON內保存目前各章及每次checkpoint歷史。更新使用檔案鎖、expected revision、暫存檔寫入與fsync後原子替換，避免兩個執行者覆蓋新進度或中斷留下半份JSON。此實作使用POSIX檔案鎖，適用目前macOS／Linux環境。

重新執行`resume`會讀取最後成功保存的狀態。寫入在替換前失敗，舊狀態保留；替換成功後即以新狀態為準。JSON損毀或不符合版本時拒絕讀入，不猜測或重建已用額度。它不復原外部教材或模型執行，因為本版不執行那些動作。

## 驗證

```bash
python3 -m unittest tests.test_course_improvement_loop -v
python3 operations/course-content-scoring/loop-control-v1/verify_gtm_records.py
```

單元測試使用暫存材料，覆蓋狀態優先序、版本上限、失敗補救、來源變動、H3綁定、舊revision拒絕，以及寫入中斷保留舊狀態。GTM驗證讀既有三次紀錄的結構化摘錄，拒絕案例只在暫存狀態副本執行；不改正式state、教材或候選稿。

目前GTM狀態：CH1-1等待H3、2／2；CH1-2完成、1／2；CH1-3等待補證、2／2、H3未確認且使用者暫不下載。CH1-1屬歷史回溯，並非當時已由兩版上限控制；原始規則版本保留在`historical_rules`。本版只驗證控制流程，不重新評估三章。

實作位置：[控制器](../src/course_improvement_loop.py)、[CLI](../scripts/course_improvement_loop.py)、[測試](../tests/test_course_improvement_loop.py)。本地GTM資料放在`operations/course-content-scoring/loop-control-v1/`，沿用專案既有operations忽略規則；程式及測試不依賴這份個人資料才可執行單元測試。
