# 課程設計系統可使用性驗證

**驗證日期**：2026-10-19

**系統版本**：`0.1.0`
**驗證範圍**：新課程 G0–G6、16 個 Skill、既有課程修復交易、端到端 proof、clean HOME 安裝與獨立 Git 匯出

**結論**：系統已達 `INDEPENDENT_AI_VERIFIED`，可在受控環境用於新課產製與具備完整 proof 的既有課修復。尚未完成目標學員真人試學，因此不宣稱 `HUMAN_READY`。G6 已通過發布準備驗證，外部 action 仍是 `PUBLISH_APPROVAL_REQUIRED`；未發布、未部署、未改變外部存取權，也未 push。

## 核心能力與證據

| 能力 | 可重現證據 | 結果 |
| --- | --- | --- |
| G0 需求確認 | 正式 requirements schema、重要未知阻擋與 Gate replay | PASS |
| G1 當前研究與 hands-on | 可追溯來源、工具實測、衝突與適配紀錄 | PASS |
| G2 單一主藍圖 | outcome／capability／criterion／unit／時數與依賴覆蓋 | PASS |
| G3 可讀且能跟做的正文 | 完整示範、引導與獨立練習、檢查、修復與文案連續性 | PASS |
| G4 代表單元 | 三種 viewport、basic accessibility smoke、不同情境的獨立 AI 試走 | PASS |
| G5 完整課程 | 全課 coverage matrix、held-out transfer、答案重用負向測試 | PASS |
| G6 發布準備 | 六類 release check 均由實際檔案與 hash 支持 | PASS |
| 外部發布隔離 | action 未授權，`authorization: null`，`external_publication: NOT_EXECUTED` | PASS |
| 既有課修復 | approved plan、before hash、backup、isolated restore proof 與 hard-exit recovery | PASS |
| 可攜安裝 | 16 個 Skill 來源／安裝 hash、clean HOME apply／verify／doctor | PASS |
| 獨立 repo 邊界 | standalone export、逐檔 manifest、Git fsck、`--no-local` clean clone | PASS |

## 端到端 proof

`proofs/campaign-performance-brief/` 由 builder 經中央 Gate routes 重建。checked-in snapshot 與外部 fixture authority 重建結果逐檔相同；所有 contract evidence path 存在且 SHA-256 相符。G4 與 G5 使用不同 runner session／isolated context，只標示 `INDEPENDENT_AI_VERIFIED`；真人驗證維持 `PENDING_HUMAN`。

proof 內的 release proposal 使用固定、不可執行的 logical proof root，確保不同 clone 能產生相同 bytes。真正發布時必須針對實際 governed absolute root 重新建立 proposal，取得該 manifest 的使用者授權 receipt 後才能 apply。

## 維運與安全驗證

- 431 項完整單元與整合測試通過。
- Python compile、全部 JSON parse、shell syntax 與 `git diff --check` 通過。
- 16 個 Skill package source hash 全部通過；執行期 `__pycache__` 不再污染版本雜湊。
- macOS clean HOME 安裝、installed verification 與 read-only doctor 為 `READY`。
- CI 支援 Linux/Python 3.11、Linux/Python 3.12、macOS/Python 3.12；Windows lock 未支援並 fail closed。
- runtime operations、backup、reports 與個人 registry snapshot 已從版本內容移除並忽略，原始碼 portable path 掃描通過。
- standalone export 不含 learner-facing courses 或 runtime 個人資料，可從 clean clone 重做來源驗證。

## 驗證邊界

- 尚無目標學員真人試學，不能宣稱 `HUMAN_READY`、真實學習時數或真人遷移已驗證。
- 示範課使用無登入、無付費的本機素材；第三方平台課程仍需各自取得帳號、權限、locale、方案與 UI hands-on 證據，缺少時維持 `BLOCKED`。
- basic accessibility smoke 不等於 WCAG 2.2 AA conformance；若課程要做 AA 宣告，必須補齊完整頁面與 A／AA success criteria 的人工及自動化證據。
- CI 檔案已完成本機命令等價驗證；遠端 GitHub Actions 尚未執行，因本輪未 push。
