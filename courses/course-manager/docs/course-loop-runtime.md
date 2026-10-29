# 課程改善 loop 使用說明

第一次使用請先看[開始使用教學](course-loop-quickstart.md)，內含對話指令、可複製設定與操作順序。

本入口將既有單章與整課控制器接上 Codex CLI。適用於有人負責補證、閱讀確認的有限範圍改善；以終端前景執行，關閉後不會在背景自動修課。候選稿另存，不會覆蓋正式講義。舊試作不遷移、不重置。

## 準備課程

在 course-manager 目錄使用 Python 3.11 以上、已安裝並登入的 Codex CLI。先執行 `python3 scripts/course_loop.py doctor`；登入成功不等於指定模型有使用權限。模型名稱依帳戶可用模型設定，無法使用即停止，不自動換模型。

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

流程為評估與修正交接 → 完整候選 → 作者比較 → 必要檢查 → 新上下文覆核。未改寫的原稿也須檢查及覆核。作者說通過不能直接結案；必要檢查漏做、失敗或未知會阻止放行。候選最多兩版，達標便停改，不為用滿額度而改寫。

`REPORT.md` 提供候選與報告連結。`status` 列出當前狀態、候選雜湊、child_revision、待補證及模型呼叫數；程序回傳錯誤或 `last_error` 不為空時先處理原因。

## 人工確認與補證

候選通過覆核後停在 `waiting_human`，請人工比較閱讀脈絡、必要解釋與原有優點。收到實際認可後，將原話存成 UTF-8 檔，再以 status 顯示的版本登記：

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

明確失敗且沒有答案的任務，才可使用 `retry --run RUN --unit CH1 --reason "已確認原因及補救"`，最多一次，仍占總呼叫額度。有答案但格式或內容遭拒時不會自動重新生成，須先辨認原因。不要刪 state、另開同章 run 或改 spec 來繞過上限。來源、規範或設定變更會停止，不默默重綁新稿。

舊 schema 的 `level=L1, cap=L1` 可無損轉為 `cap=null`；只移除冗餘表示，不改等級。原始 answer、response 與 normalization 都保留；其他不合法判級仍拒收。

## 執行與驗證界線

每次以全新 Codex 程序、空工作目錄及唯讀沙箱執行，只接受資料回傳，主控制器負責存檔。覆核不帶作者評分答案；若事件顯示使用未授權工具，拒收結果。這是上下文隔離，不是限制所有檔案讀取的作業系統隔離。完整來源與規範會送往指定模型，應只提供獲准處理的材料。

Codex CLI 沿用本機登入；不複製 API 金鑰。本機若限制 Codex 自身狀態檔寫入，須由執行環境核准必要啟動權限，不能把模型改為任意寫入模式來繞過。相關 CLI 行為參考 [OpenAI 非互動模式說明](https://learn.chatgpt.com/docs/non-interactive-mode)。

控制流程測試使用暫存合成資料；實際模型試跑與限制見[驗證紀錄](../operations/course-content-scoring/runtime-release-verification/驗證紀錄.md)。不代表所有課程內容品質均已驗證。
