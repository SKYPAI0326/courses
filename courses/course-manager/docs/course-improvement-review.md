# 角色派送、必要檢查與覆核放行

實際呼叫模型請使用[統一執行入口](course-loop-runtime.md)。以下保留底層派送與回交介面；現在也支援每章個別的 review_policy，未指定時沿用佇列共用設定。

本版沿用單章與整課控制器，新增`stages-2`。新試驗的CLI初始化必須提供`review_policy`；既有`stages-1`仍可查詢、接續與確認，不自動遷移，也不能宣稱歷史試作已通過新覆核。程式派出工作任務，尚未接入背景模型API；執行者仍需依任務呼叫指定模型及回交。

## 設定

在原config的來源、用途、輸出目錄之外加入：

```json
{
  "review_policy": {
    "roles": {
      "assessor": "gpt-6.1-sol",
      "writer": "gpt-6-luna",
      "reviewer": "gpt-6.1-sol"
    },
    "checks": [
      {"id": "links", "kind": "local_links", "description": "核對本機教材與素材路徑"},
      {"id": "facts", "kind": "required_text", "description": "保留本例必要數值", "texts": ["每人上限2"]}
    ]
  }
}
```

角色模型名稱由執行環境決定；控制器不查模型是否可用，也不自動切換模型。評估與覆核模型不得等於改寫模型。必要保留文字與檢查種類須按章節用途設定，範例不是所有課程的固定模板。設定在初始化後固定，不可由模型回交刪除。

## 派送與回交

```bash
python3 scripts/course_improvement_loop.py stage-init --config PATH/config.json --state PATH/state.json
python3 scripts/course_improvement_loop.py next --state PATH/state.json
```

`next`包含`assignment.role`、`assignment.model`及`fresh_context_required`。assess交評估者、rewrite與compare交作者、review交覆核者。只使用任務的allowed_inputs，不讓覆核者讀作者的對話或其他試作答案。

覆核任務不提供作者報告與自評等級，只提供來源、候選、必要交接、問題身分與檢查證據。覆核仍需直接讀原文，不以P清單取代全章必要內容檢查。覆核context_id必須未曾在本試驗使用，不能沿用作者、評估者或上一輪覆核的上下文。

```bash
python3 scripts/course_improvement_loop.py accept --state PATH/state.json --response PATH/response.json --role writer --model gpt-6-luna --context-id ACTUAL_CONTEXT_ID
```

role/model/context-id由可信執行端根據實際派送填入，不由模型自由回填。控制器會拒絕角色、模型不符與覆核上下文重用；**這不是身分驗證服務，也不能證明呼叫端真的用了該模型或隔離了對話**。目前僅強制資料與流程契約；真正的模型執行與上下文隔離仍由執行者負責。相同回交及相同執行身分重送維持冪等，身分變更則拒絕。

## 檢查先於覆核

作者compare後固定進入checks；原稿assess若判無需修改，也先進checks，不能直接complete。有必要補證或人工取捨時仍可按原規則先停止，不強迫生成候選。

```bash
python3 scripts/course_improvement_loop.py run-checks --state PATH/state.json --expected-revision N
```

檢查產出獨立JSON，綁定目前原稿或候選的路徑及雜湊，再派review。中斷在報告寫入與state提交之間時，可用相同revision接續；僅接受內容完全相同的既存報告，不覆寫它。

| 檢查 | 真正檢查的範圍 | 不代表什麼 |
| --- | --- | --- |
| local_links | HTML href/src、Markdown行內與參照定義中的本機路徑存在性；解析URL編碼 | 不驗證遠端網址、頁內錨點、所有Markdown方言、學員權限或內容可操作性；跳過目標另列 |
| required_text | 指定字串仍在目前稿件中 | 不驗證數學、語意或改寫後的教學脈絡 |
| external | 接收實際操作或其他檢查報告，綁定目前版本與pass/fail/pending | 不靠程式判斷報告內容是否真實；沒有報告時為pending，不等同失敗 |

需要案例計算、素材內容或工具操作才能判斷時，將該項列為external；由執行者保存實際驗算或操作結果。不能只加local_links便聲稱所有必要操作已驗證。

外部證據可透過`run-checks --evidence-map PATH/map.json`提供。格式為檢查id對應`{"target":{"path":"目前版本絕對路徑","sha256":"目前版本雜湊"},"status":"pass","report":"隔離目錄內報告絕對路徑"}`。報告必須非空且另存；也可引用已經supplement-evidence登記的實測紀錄，不必複製報告。已用其他用途綁定的教材或狀態檔不能當成實測報告。

## 覆核結果與停止

review的response沿用`task_id`、`outputs.report`、`evaluation`，另加`check_resolutions`。每個fail檢查須對應未解P；每個pending必要檢查須對應未解且required的Q。例如`{"links":"P03","operation":"Q01"}`。全數pass時為空物件。檢查不通過卻回全L3、隱藏P/Q或省略對應，都會拒收。

- 覆核發現漏查：交具體P與修法，依剩餘額度回rewrite；原稿無需修改的判斷也適用。
- 必要證據不足：waiting_evidence；補證後重新評估／比較、檢查及覆核，不能直接完成。
- 有候選且覆核通過：先等H3。confirm-h3會核對目前版本的覆核與檢查，不接受提前認可。
- 無候選且覆核確認無需修改：才可complete，不為走流程而改稿。
- 兩版用滿仍有缺口：依原規則受限停止或交人工。覆核不多算一次改稿失敗；換角色與補查不重置版數。
- H3前再發現缺口：沿用recheck-comparison，重新走checks與review；舊覆核不能放行新版本。

程式能阻擋少了覆核、缺檢查或已知檢查失敗卻宣稱通過的情況，不能保證另一模型不再漏查語意。因此H3與必要操作證據仍保留；停止不等於教材驗收。

## 整課與舊資料

新整課manifest可指定共用`review_policy`，也可由各unit明確指定自己的policy；工作票傳遞該章生效設定，單章必須完全符合且使用stages-2。設定初始化後固定，不能在回交時變更，也不能借用舊格式的完成狀態。

checks/review期間仍是未完成，相依下游不能把它當成已完成或單純待H3。只有真正覆核放行後的H3待確認版本，才能按既有相依設定暫定參照。各章完成後仍須原有跨章銜接確認，不自動發布。

本次未替現有Gemini佇列加policy或啟用派送，沒有遷移GTM或兩次Luna試驗。

驗證：`python3 -m unittest tests.test_course_improvement_loop tests.test_course_loop_stages tests.test_course_improvement_queue tests.test_course_loop_review -q`。實際隔離CLI案例與限制見[驗證紀錄](../operations/course-content-scoring/role-review-isolated-verification/驗證紀錄.md)。
