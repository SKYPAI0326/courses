# 課程改善 loop 使用說明

第一次使用請先看[開始使用教學](course-loop-quickstart.md)，內含對話指令、可複製設定與操作順序。

本入口將既有單章與整課控制器接上 Codex CLI；文案專用run可選擇只把`rewrite`階段接到Antigravity CLI。適用於有人負責補證、閱讀確認的有限範圍改善；以終端前景執行，關閉後不會在背景自動修課。候選稿另存，不會覆蓋正式講義。舊試作不遷移、不重置。

## 準備課程

在 course-manager 目錄使用 Python 3.11 以上、已安裝並登入的Codex CLI。採「文案迭代改」時也須安裝並登入Antigravity CLI。先在與 `work` 相同的執行權限下執行 `python3 scripts/course_loop.py doctor`；它會不呼叫模型地檢查Codex app-server及agy模型清單。登入、程序啟動及模型列在清單中，仍不等於該帳戶一定能生成；模型失敗即停止，不自動換模型。

建立一份 JSON 設定，所有檔案路徑建議使用絕對路徑。下面的路徑須替換為實際檔案；先只放已授權的一章。

```json
{
  "id": "my-course-pilot",
  "roles": {"assessor": "gpt-6.1-sol", "writer": "gpt-6-luna", "reviewer": "gpt-6.1-sol"},
  "rules": ["/absolute/path/三原則判斷等級與修正交接-v0.7.md", "/absolute/path/單章課程改善流程-v0.10.md", "/absolute/path/講義文案撰寫基準-v0.3.md"],
  "limits": {"max_model_calls": 8, "timeout_seconds": 120, "max_input_chars": 180000, "reasoning_effort": "low"},
  "units": [{
    "id": "CH1", "title": "章節名稱", "purpose": "本章學員應理解或完成的具體事情",
    "source": "/absolute/path/CH1.html", "materials": [], "dependencies": [],
    "checks": [{"id": "links", "kind": "local_links", "description": "本章本機素材與連結存在"}]
  }]
}
```

`rules` 放現行規範，`materials` 放本章必要來源或操作紀錄。輸入須為 UTF-8 文字；ZIP、PDF、影片等須先提供可讀摘錄或外部檢查紀錄。不能用讀不到材料代替教材缺失。每章 `checks` 必須按用途制定，不能只照抄範例：`required_text` 另附 `texts` 陣列；需核對實際操作、下載或產物時加入 `{"id":"operation","kind":"external","description":"實際完成本章操作並核對產物"}`。外部檢查無證據即 pending。

若日後授權多章，`units` 按處理順序排列；後章的相依可寫為 `[{"unit":"CH1","reason":"沿用前章產物","allow_h3_provisional":false}]`，必須指向清單中的前章。暫定參照規則見[佇列說明](course-improvement-queue.md)。各章可有不同檢查。不可拿舊試作完成狀態冒充新章完成。

## 啟動與查看

以下 `RUN`、`SPEC` 代表你選定的路徑；run 必須是尚不存在的新目錄。prepare 只建快照和清單，不呼叫模型。

```bash
python3 scripts/course_loop.py prepare --spec SPEC --run RUN
python3 scripts/course_loop.py status --run RUN
python3 scripts/course_loop.py start --run RUN --actor "執行者" --note "本次授權章節與處理範圍"
python3 scripts/course_loop.py work --run RUN --max-tasks 1
python3 scripts/course_loop.py report --run RUN
```

`work` 每次最多執行指定數量的模型任務，預設一個；再次執行接續同一 run。一般一次候選需要評估、改寫、自查、覆核四次模型呼叫，必要檢查由程式處理。呼叫總上限另由 `limits` 固定，沒有自動加額度；呼叫數不等於費用上限，實際 token 用量保留於各工作紀錄。

每次 CLI 模型任務前會依provider以相同執行權限檢查Codex app-server或agy模型清單；檢查失敗即停止，不建立執行job或增加呼叫計數。這不能保證後續模型必定成功；啟動檢查通過後仍按原規則先記一次呼叫，若結果不明則不自動重送。已發生的失敗與用量不回溯更改。

使用[文案迭代改](course-copy-quickstart.md#文案迭代改)時，`rewrite`任務明確綁定`provider=agy`及`gemini-3.8-flash-low`；assess、compare、review仍依既有角色設定使用Codex。Agy以一次性headless程序、空暫存工作目錄、sandbox、stream-json及schema執行，完整記錄命令、提示與schema雜湊、stderr及事件流。`init.tools`只是可用工具清單，不視為已使用；`step_update.step_type=tool`中唯一允許的是schema綁定的`finish`結構化輸出提交，且仍須通過SUCCESS、單回合及schema核對。其他工具或子代理、模型不符、非SUCCESS或缺少結構化輸出時拒收且不自動重送；原事件完整時`recover`沿用原事件，`retry`沿用原provider及模型。

agy預檢使用`agy models`確認CLI可啟動且固定模型列在清單中，不會產生模型回合；它不保證帳戶有生成權限或額度。請在與`work`相同的執行權限下先執行`doctor`；預檢失敗時不建立執行job、不增加模型呼叫計數。Codex會優先使用Codex Desktop提供的`CODEX_APP_RUNTIME_CLI_PATH`，並清除宿主注入的其他`CODEX_*`環境變數後啟動；找不到該執行檔才使用PATH中的`codex`。

流程為評估與修正交接 → 完整候選 → 作者比較 → 必要檢查 → 新上下文覆核。未改寫的原稿也須檢查及覆核。作者說通過不能直接結案；必要檢查漏做、失敗或未知會阻止放行。候選最多兩版，達標便停改，不為用滿額度而改寫。

`REPORT.md` 提供候選與報告連結。`status` 列出當前狀態、候選雜湊、child_revision、待補證及模型呼叫數，也顯示各模型階段／重試耗時、自動檢查、控制器接收及人工H3等待時間；尚待人工確認時，H3數字是截至查詢當下的經過時間。`run.json`另保存每段計時的毫秒數及UTC起訖時間；模型數值是CLI往返時間，包含本機啟動和接收結果，不代表供應商純生成時間。`REPORT.md`顯示可讀的秒數摘要。舊run沒有計時欄位時標為未量測，不回推或估算。程序回傳錯誤或 `last_error` 不為空時先處理原因。

## 人工確認與補證

候選通過覆核後停在 `waiting_human`，請人工比較閱讀脈絡、必要解釋與原有優點。收到實際認可後，將原話存成 UTF-8 檔，再以 status 顯示的版本登記：

若來源是HTML且預計沿用該頁版型，在登記H3前先對該候選做唯讀相容性預檢：

```bash
python3 scripts/course_handout_apply.py --preflight \
  --source '/完整路徑/原講義.html' \
  --candidate '/完整路徑/候選.md' \
  --output '/隔離工作目錄/preflight.json'
```

`blocked`表示候選不能直接套入這份HTML；若同一版本要同時做H3認可與後續套用，先完成對齊，並讓H3綁定對齊後的檔案。`passed`只表示基本檢查通過。報告會列原頁複合元件與區段數差異，後續仍須建立明確映射並做預覽檢查。預檢只判HTML相容性，不判文案品質、不修改run的H3狀態、不呼叫模型、不產生HTML，也不等於正式套用授權。

```bash
python3 scripts/course_loop.py confirm-h3 --run RUN --unit CH1 --feedback FEEDBACK.md --candidate-sha256 SHA --expected-revision N --actor "紀錄者"
python3 scripts/course_loop.py work --run RUN --max-tasks 1
```

不可替使用者填認可。閱讀有問題時保留停止狀態，交人工判斷修正範圍，不用 confirm-h3 駁回後強行結案；本入口尚未提供任意人工追加缺口或重設版本功能。H1／H2同樣交人工處理，不自動解除。

外部檢查待補證時，實際完成檢查後提供報告與目前版本 SHA；原稿尚無候選時使用 `version.sha256`：

```bash
python3 scripts/course_loop.py supply-check --run RUN --unit CH1 --check operation --result pass --evidence EVIDENCE.md --candidate-sha256 SHA
python3 scripts/course_loop.py work --run RUN --max-tasks 1
```

結果也可為 `fail` 或 `pending`，須如實紀錄；補證不重設兩版用量。程式確認證據與版本綁定，不能證明報告內容屬實，登記者須負責核對。等待補證的相依章節阻塞；沒有相依的授權章節可依序處理。

所有章節完成後，另核對跨章承接與產物版本，保存報告，使用 queue 的 revision 結案：

```bash
python3 scripts/course_loop.py finish --run RUN --evidence INTEGRATION.md --expected-revision N --actor "核對者"
```

這是改善試作完成，不是正式上架或覆寫授權。

## 中斷恢復

先 `status`，再對同一 run 執行 `work`。已有完整模型結果會接收快取，不重呼模型或重複計版。若模型已完成、但執行端尚未保存完成紀錄，用 `recover --run RUN --unit CH1` 檢查原事件並接收；這個命令不呼叫模型。

明確失敗且沒有答案的任務，可使用 `retry --run RUN --unit CH1 --reason "已確認原因及補救"` 一次；compare／review雖有答案但遭接收器拒收時，也可在先辨認原因後補跑一次。後者建立獨立 `-retry` 工作目錄，原始答案、事件與報告留在舊目錄，不重寫候選。所有補救均占同一 run 呼叫額度，會立即執行模型，須先在相同權限下通過 `doctor`。不要刪 state、另開同章 run 或改 spec 來繞過上限。來源、規範或設定變更會停止，不默默重綁新稿。

v0.6 評估已完整回傳、但只有 `next_fix.problem` 把多個仍未解的 P 編號合寫而被拒收時，可用 `repair-assess-plan --run RUN --unit CH1 --problem P01 --reason "原因" --actor "紀錄者"` 指定其中一個原有 P。此命令不呼叫模型、不重置用量；它另存原答案雜湊與更正紀錄，只更正修法索引，原評級、問題狀態、修法文字及原始回交不動。其他評估拒收原因不得使用此命令。

v0.6 比較或覆核已完整回傳，且 `remaining_gap` 寫了「無。」等明示沒有缺口的文字、同段 `problem_id` 為 null、三項讀者檢查都為 supported，卻因該欄非空而被拒收時，可用 `repair-no-gap-rows --run RUN --unit CH1 --reason "原因" --actor "紀錄者"` 清空這些段落的 `remaining_gap`。此命令保留原答案並記錄逐段更正，不改真實缺口、評級、問題或模型用量；有實質缺口的段落會拒絕更正。

舊 schema 的 `level=L1, cap=L1` 可無損轉為 `cap=null`；只移除冗餘表示，不改等級。原始 answer、response 與 normalization 都保留；其他不合法判級仍拒收。

## 已回交比較報告的格式更正

`retry`仍不得重抽已有答案。若使用者明確要求更正v0.6作者比較報告，且拒收原因是逐字引文不符或引用已關閉P／Q，可使用：

```bash
python3 scripts/course_loop.py repair-report --run RUN --unit CH1 --actor '紀錄者' --reason '本次明確授權與已確認的格式錯誤'
```

每份失敗比較報告僅一次，使用原作者模型與low／既有設定，計入同一run原總額，不重置候選或已用呼叫。原任務ID保留；原始答案、response、報告與拒收檔案不動，更正另存`-report-repair`目錄，job保留原檔位置、SHA、原因與紀錄者。

更正不再重交整份報告，只交`replacements`：每項為原passages的零起算索引`passage`、`quote_ref`及`support_refs`。位置包含`block`段落ID、`start`及`end`字元位置；選整段可用0至該段length。控制器從目前候選擷取原文，將局部更正套到原答案副本，保留全部P／Q紀錄、等級、問題狀態、修法與閱讀結論；評級中原已關閉的引用由程式移除，不改高等級。含evaluation等其他欄位的patch直接拒收。

原始patch保留在answer.json，組裝結果另存assembled-answer.json，原拒收答案及報告不動。接收仍核對原答案SHA與不可變欄位，再走原驗證器；格式可接收不等於內容通過。更正仍有問題即停止，不再次重抽。這不重設舊run已經用過的更正次數。

接收後如果原問題仍open，照原控制器決定是否需要第二版；只有實際改稿、比較、必要檢查與新上下文覆核完成才停H3。額度不足、相同缺口再次失敗或其他停止條件照原規則處理，不能因更正報告而直接跳過。

## 執行與驗證界線

每次以全新 Codex 程序、空工作目錄及唯讀沙箱執行，只接受資料回傳，主控制器負責存檔。覆核不帶作者評分答案；若事件顯示使用未授權工具，拒收結果。這是上下文隔離，不是限制所有檔案讀取的作業系統隔離。完整來源與規範會送往指定模型，應只提供獲准處理的材料。

Codex CLI 沿用本機登入；不複製 API 金鑰。本機若限制 Codex 自身狀態檔寫入，須由執行環境核准必要啟動權限，不能把模型改為任意寫入模式來繞過。相關 CLI 行為參考 [OpenAI 非互動模式說明](https://learn.chatgpt.com/docs/non-interactive-mode)。

控制流程測試使用暫存合成資料；實際模型試跑與限制見[驗證紀錄](../operations/course-content-scoring/runtime-release-verification/驗證紀錄.md)。不代表所有課程內容品質均已驗證。
