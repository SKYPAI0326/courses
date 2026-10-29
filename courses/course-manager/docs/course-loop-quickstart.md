# 開始使用「課程迭代」

候選完成H3後，可用[講義套用](course-handout-apply.md)銜接原HTML版型，先交隔離預覽；文案認可不代表正式覆蓋或發布。

對話啟動詞為「課程迭代」，例如「課程迭代：Gemini CH3-1，沿用兩版上限，完成後交我閱讀」。它對應既有評估、改寫、覆核及停止流程；不是新的終端命令，底層程式仍使用loop名稱。若只說啟動詞而未指定對象，先確認課程與章節，不自動啟動整課。

啟動方式已登記於[專案入口AGENTS.md](../AGENTS.md)。在course-manager專案開新對話，只輸入「課程迭代」即可要求載入本教學、操作規範、模型分工與目前進度，不必每次指定檔案。建議主對話選GPT-6.1 Sol；入口不會切換對話模型，流程內仍由設定檔分別派送Sol與Luna。其他專案的新對話不保證載入本入口。

目前本機執行環境已可用，Codex CLI已登入，Sol評估／覆核及Luna改寫／比較已實際跑過。Gemini CH2-2第一版候選也已取得使用者H3閱讀確認，重啟不再改稿。這套工具以單章或明確授權的清單為範圍，產出獨立候選，正式採用仍另行決定。

## 最方便的用法：在對話裡交付一章

在這個專案的對話貼上以下文字，換掉方括號內容即可。已有試作的章節要提供既有run，不能另外初始化來重置版數。

> 課程迭代：［課程名稱］的［章節或檔案路徑］。這一章的用途是［主課／補充查閱／練習，以及學員要學會什麼］，學員起點是［背景］。相關素材與前後章是［路徑或位置］。請先確認是否已有run；有則接續，沒有才建立隔離run。沿用Sol評估與新上下文覆核、Luna改寫與比較，最多兩版、八次模型呼叫、low。不覆蓋正式講義、不擴大範圍；交付原稿、完整候選與前後比較，到H3停下讓我讀。必要實測缺證據就如實保留待補證，CH1-3維持待補證。

不必先替模型列出所有缺點；你要提供的是章節用途、材料與界線。補充頁不會因為沒有完整主課流程就必須擴寫；操作頁也不能只改文案就宣稱操作通過。

收到候選後，直接連續閱讀全文。重點看情境是否交代清楚、例子是否讓人理解、段落能否接起來，以及原本有用的內容是否保留。若可接受，可以說：

> ［章節］候選v［版本］的閱讀脈絡與新增解釋沒有問題。請登記H3並驗證重啟不再改稿；保留候選，不覆蓋正式講義。

若不接受，指出具體段落與讀不懂的原因。系統先保留停止狀態，由執行者判斷必要修正與剩餘版本；不會把負面回饋記成H3認可，也不會無限改稿。現行統一入口尚無自動處理任意人工新增缺口的指令。

## 自行操作：複製設定，再執行

本機[單章設定範本](../examples/course-loop/single-unit.template.json)已填入模型、現行規範與資源上限。它刻意沒有指向任何真實章節，不會誤啟動CH2-2或舊佇列。先將它複製成新的設定檔，修改以下內容：

| 欄位 | 要填什麼 |
| --- | --- |
| id | 本次run識別，例如gemini-part3-ch3-1；限英數、底線、連字號 |
| units[0].id、title | 章節識別與名稱 |
| purpose | 本章用途、學員起點、理解或完成目標 |
| source | 原稿HTML或Markdown的絕對路徑 |
| materials | 必要素材、前後章或實測紀錄的絕對路徑陣列 |
| checks | 按本章用途補上必要檢查，不只沿用本機連結檢查 |

需要保留數值或文字可加 `required_text`；需要實測的章節加 `external`。例如：

```json
{"id":"operation","kind":"external","description":"依本章路徑取得素材、完成操作，核對產物可重開"}
```

外部檢查沒有紀錄會停待補證，不表示教材已確認有錯。不要為了能跑到完成而刪除必要檢查。二進位素材要提供可讀說明或檢查報告；只給ZIP不會自動完成實測。

在終端先切到專案目錄：

```bash
cd '/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/course-manager'
python3 scripts/course_loop.py doctor
```

以下兩個路徑要換成你剛存好的設定及新run位置；run目錄必須尚不存在。變數加引號可處理路徑空白。

```bash
loop_spec='/你的設定檔完整路徑/spec.json'
loop_run='/你的隔離輸出完整路徑/run'
python3 scripts/course_loop.py prepare --spec "$loop_spec" --run "$loop_run"
python3 scripts/course_loop.py status --run "$loop_run"
```

prepare只準備資料，不呼叫模型。檢查清單、章節及上限正確後才啟動：

```bash
python3 scripts/course_loop.py start --run "$loop_run" --actor '你的名字' --note '僅本章，兩版上限，不覆蓋正式講義'
python3 scripts/course_loop.py work --run "$loop_run" --max-tasks 8
python3 scripts/course_loop.py report --run "$loop_run"
```

`--max-tasks 8`是本次最多派八項模型任務，不是生成八版；run的總呼叫上限與兩版限制仍生效。遇到H3、補證或其他停止條件會提前停。你也可改成1，一次走一個模型階段。程式在終端前景運作，不是排程或背景服務。

打開run裡的 `REPORT.md`，即可找到候選與評估報告。不要以模型L3取代自己的閱讀；同樣不要因為只是程式停止就判定成功。

## 看到狀態後要做什麼

| 狀態或訊息 | 下一步 |
| --- | --- |
| in_progress | 尚在流程中；對同一run繼續work |
| waiting_human／H3 | 閱讀候選，明確提供認可或具體問題；模型不自填認可 |
| waiting_evidence | 取得所缺證據後再接續，不盲目重寫 |
| dependency_blocked | 等待所依賴的前章，不把它當成本章缺失 |
| H1／H2、上限或last_error | 先辨認原因與剩餘額度，不重建run繞過限制 |
| 單章complete | 該章停止改稿；若run尚未complete，仍需做範圍內的結案核對 |
| run complete | 本run改善工作完成，不代表正式發布 |

人工確認、補證及run結案的精確命令見[完整操作說明](course-loop-runtime.md#人工確認與補證)。H3用該章 `child_revision` 及候選SHA，finish用run／queue的 `revision`，兩者不能混用。

## 中斷後如何繼續

重新打開終端，再設定同一個 `loop_run`，先status，再work；不要再次prepare。若完整模型結果已落盤，會接收快取；沒有完成證據時會停下。recover只檢查已有結果，不再呼叫模型；retry只用於已確認失敗且沒有答案的任務，最多一次。具體操作見[中斷恢復](course-loop-runtime.md#中斷恢復)。

目前已完成的CH2-2可用來練習「只查詢」，不會再改稿：

```bash
python3 scripts/course_loop.py status --run operations/course-content-scoring/loop-trial-gemini-ai-ch2-2/run
```

這個run只含CH2-2。Gemini整課佇列仍未啟動，GTM CH1-3仍待補證。若未來要跑整課，先確定章節清單、相依與各章檢查，再另行授權，不能把本次教學視為整課啟動指令。
