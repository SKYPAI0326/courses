# 講義技能與專案規範稽核（gen-ai-36h，2026-11-01）

稽核者：fresh context，只讀不改。評分依據只讀了 `_review/2026-11-01/rubric.md`（v1.1），`_review` 下其他檔案都沒讀。
三個問題的簡稱：**P1 不說人話**、**P2 偏離主題（人工作業多於學用 AI）**、**P3 編號複雜**。
標記方式：**【查證】**＝附原文引句與 `檔案:行號`；**【推論】**＝從條文推出的模型行為，沒有實測。

## 0. 範圍與版本說明

**實際載入鏈【查證】**：Claude Code 讀的是 `~/.claude/skills/<name>/SKILL.md`（11–13 行的 shim），內容只有一句「Read and follow `/Users/paichenwei/.agents/skills/course-copywriter/SKILL.md` as the single source of truth」（`~/.claude/skills/course-copywriter/SKILL.md:9`）。因此實際生效的規則是 `~/.agents/skills/`，不過**觸發用的 description 來自 shim，跟 canonical 寫的不一樣**。例如：
- shim `course-handout-designer` 的 description：「Use when designing or rebuilding a complete beginner-friendly course or lesson handout…」（`~/.claude/skills/course-handout-designer/SKILL.md:3`）。
- canonical 的 description：「Use when explicitly requested to design a standalone learner handout. Normal course lesson production uses course-designer」（`~/.agents/skills/course-handout-designer/SKILL.md:3`）。
- 結果【推論】：「重新設計講義」這類請求，在 Claude Code 會觸發 handout-designer；canonical 卻要求一般產製走 course-designer。路由從入口就不一致。
- shim `course-repair` 的 description 寫「missing checkpoints」（`~/.claude/skills/course-repair/SKILL.md:3`），把「補 checkpoint」列成觸發情境，會把模型推向加核對（P2，輕微）。

**共用規範**：六個 skill 都把學員路徑、充分性、語意交給四份共用檔，分別是 `_規範/learner-action-contract.md`、`course-content-substance.md`、`llm-prose-risk-gate.md`、`lesson-plan-template.md`（例如 `course-designer/SKILL.md:27-31`、`course-handout-designer/SKILL.md:16-18`）。這些檔一定會被讀到，所以列在第 11 節。下文路徑簡寫：`$S`＝`/Users/paichenwei/.agents/skills`；`$B`＝課程專用網頁根目錄。

---

## 1. course-handout-designer

**a. 用途與預設產出**【查證】：canonical 的定位是「course-designer 使用的講義設計方法庫」（`SKILL.md:8`）。產出是一份正式學員正文，加上內部設計／證據表（`SKILL.md:34`）。references 分四份：課程脊椎、四課型、品質審查、入口連續性與素材可取得性。

**b. 推向問題的指示**

| 引文 | 位置 | 推向 | 怎麼推 |
|---|---|---|---|
| 「身分｜顯示檔名、格式，以及必要的版本／去敏狀態」 | `references/asset-discoverability-gate.md:11` | P3 | 每項素材都要顯示檔名與版本，檔名、版本標籤會因此進入正文。rubric 3-6 計檔名，3-2 計版本標籤【推論】 |
| 「任一核心資產缺少身分、取得方式、第一次使用時機或備援，判定為 `BLOCKER`」 | `asset-discoverability-gate.md:25` | P3／P2 | 每份素材都附「備援」，還要說明無權限或格式不支援時怎麼辦。條件與限制語因此變多（rubric 2-4）【推論】 |
| 「於重要決策及狀態變化安排檢查與適用的修復」 | `references/lesson-type-contract.md:11`（skill-operation） | P2 | 每次狀態變化都要求檢查與修復。全文沒有一句說核對可以交給 AI，模型預設會寫成學員自己檢查【推論】 |
| 「記錄實際時間與提示」「到第一個 checkpoint 的時間」 | `beginner-continuity-gate.md:7,42` | P3（間接） | 這是冷讀紀錄用語。條文沒有禁止，但也沒有說明不得進入學員正文【推論】 |
| 「凡學員稍後要讀、填或判斷的…欄位、資料結構、錯誤狀態或課堂標籤，第一次出現時都要同時說明」 | `beginner-continuity-gate.md:28-32` | P3（雙面） | 它要求解釋代碼，沒有要求移除代碼。因此預設保留狀態碼與欄位名，只在首次出現時說明一次。rubric 3-3 要求每段第一次出現都重新說明，標準比這裡嚴【查證＋推論】 |

**c. 防止問題的指示**

| 引文 | 位置 | 防 |
|---|---|---|
| 「從問題與用途引入，先解釋必要概念，帶讀完整例子，再讓學員逐步自行判斷與檢查，最後確認結果與使用條件」 | `SKILL.md:25` | P1（開場、收尾） |
| 「自然段落承擔解釋，清單列舉、表格比較、步驟標示順序」 | `SKILL.md:26` | P1 |
| 「不以工具、檔案或時數堆疊章節」 | `SKILL.md:23` | P2（輕） |
| 六題入口測試（情境、為什麼值得處理、材料、成果、驗收、第一步） | `beginner-continuity-gate.md:9-18` | P1-1 |
| 「不要用更多步驟、英文標籤或裝飾性開場掩蓋斷點」 | `beginner-continuity-gate.md:18` | P1／P3 |
| 「`Demo`…`Stage` 只能作為導航；刪除標籤後，正文仍須說明學員為何做」 | `beginner-continuity-gate.md:34` | P1／P3 |
| 「標題不能代替內容，也不要求每個證據各占一張卡片」 | `lesson-type-contract.md:23` | P1 |

**d. 衝突**【查證】
- 承接句。installed 版寫「若操作的對象與目的已明確，不新增固定承接句」（`beginner-continuity-gate.md:24`）。rubric 1-2 的 3 分樣子卻是「每段第一句是否接住上一段的結果」。這條在字面上與驗收標準相反。舊 package 版本來要求「剛才完成或看見的具體結果是＿＿，所以現在要＿＿」（見第 12 節）。
- 路由。canonical 說只在明確要求時使用，shim 則對「rebuilding handout」觸發（見第 0 節）。

**e. 判定：修改後可用。** 它是唯一以「完整講義重建」為目的的方法庫，有入口測試與「學員與工具分工」概念。但全文沒有「本課核心方法是指揮 AI」「核對由 AI 協助」「案例以內容稱呼」三條，還要求素材顯示檔名。

---

## 2. course-copywriter

**a. 用途與預設產出**【查證】：二次編輯，處理「內容已經存在，但讀起來不像一門課」（`SKILL.md:12`）。輸入可以是教案 MD 或學員 HTML。產出是修改後的檔案加上文案修訂報告（`SKILL.md:219-230`）。附兩支掃描腳本：
- `audit_copy_continuity.py` 檢查四件事：標題後直接接清單／表格（C1）、箭頭鏈（C2）、連續三個標籤片語（C3）、「接下來／最後」多於因果詞（C4）。
- `audit_teaching_evidence.py` 檢查核心欄位、產物、分流 true/false 去向、終態詞、失敗處理列數。

**b. 推向問題的指示**

| 引文 | 位置 | 推向 | 怎麼推 |
|---|---|---|---|
| 「不負責重新設計課程大綱、發明新案例、改寫操作步驟」 | `SKILL.md:21` | P2（鎖定） | 偏題的根源在活動設計。copywriter 被禁止更動活動，只能讓人工作業讀起來更順 |
| 「下列內容不可因潤飾而改變：學習成果、案例任務、資料值、欄位名、公式、Prompt、JSON、模組名。操作順序、檢查點、預期結果、錯誤處理與安全限制」 | `SKILL.md:61-65` | P2、P3（鎖定） | 欄位名與模組名不能換成內容稱呼（rubric 3-5）。檢查點、錯誤處理、安全限制全部保留（rubric 2-3、2-4）。照字面遵守，P2 與 P3 會原樣留下 |
| 「每個 `true / false`、通過／不通過或分流條件，都要寫出資料去向、負責人或終止狀態；只寫『人工確認』不算完成」 | `SKILL.md:105` | P2 | 人工覆核的分支要寫得更詳細，篇幅因此流向審核流程 |
| 「每條分流路徑都落在已完成、已停止、待修改或待人工確認等明確狀態」 | `SKILL.md:207` | P2、P3 | 強制寫出狀態詞，而且清單裡就有「待人工確認」 |
| 「若單元涉及失敗、審核、Filter、Router 或人工接手，至少說明：觸發條件 → 資料狀態 → 去向／負責人 → 下一步或停止狀態」 | `SKILL.md:116-120` | P2、P1-6 | 每條路徑一句要塞四件事。適用範圍限定「實際含此類任務的課程」（`SKILL.md:88`），本課 Part 5 落在範圍內【推論】 |
| 「若 learning objective 寫『每個模組』的失敗影響，示範表與驗證都要逐列覆蓋」 | `SKILL.md:112`、`references/teaching-evidence.md:37` | P2 | 逐列覆蓋就是 rubric 定義的逐筆、逐欄人工作業 |
| 「學員操作：把 `feedback` 放入提示詞的回饋欄位，並保留 `customer_name`…快速檢查：…」 | `references/rewrite-patterns.md:18-19` | P3、P1 | 範例把英文欄位名直接寫進學員句子，並用「學員操作／快速檢查」標籤開頭 |
| 「`needs_review=true` → 人工確認佇列（狀態：待人工確認）…→ 文件 → 寄信 → message ID（狀態：已完成）」 | `references/teaching-evidence.md:23-30` | P2、P3 | 標準範例本身就是英文欄名加人工佇列加狀態碼 |
| 「承接可由內容本身成立，不逐段補『剛才／現在／所以』」 | `SKILL.md:183` | P1（1-2） | 跟 rubric 1-2 的 3 分範例（「剛才整理好的三點摘要，現在拿去…」）字面相反。模型可以據此省略段首承接【推論】 |
| 「可藉重排或刪除解決時不新增橋接句。只在讀者確實無法連接既有內容時補承接」 | `SKILL.md:84` | P1（1-2、1-4） | 同上，把承接設為例外 |

**c. 防止問題的指示**

| 引文 | 位置 | 防 |
|---|---|---|
| Pipeline Risk Gate 五條（第一區段直接操作；連續兩區段沒有引用上一段結果；連續固定步驟欄位；Demo 後直接進入 Solo；結尾只有檢核） | `SKILL.md:40-46` | P1，幾乎逐項對應 1-1、1-2、1-4 |
| 「缺…；或原定核心方法被人工／其他方法接手取代｜`BLOCK`，退回 `course-designer`」 | `SKILL.md:53` | P2（偵測後退回，不自己修） |
| 「若主要正文仍是交辦清單，直接重寫承載教學的段落…只在清單前後補引言或摘要不算完成」 | `SKILL.md:152` | P1 |
| 「操作完整但只剩程序，不能判定可讀性通過」 | `SKILL.md:165` | P1 |
| 「段落常以工具名稱、欄位名稱或『學員操作：』突然開始」（列為症狀） | `SKILL.md:30` | P1／P3 |
| 「先說目的，再說操作；先給可理解的情境，再引入工具名」 | `SKILL.md:178` | P1-1、P1-3 |
| 「沒有連續多個只含標籤或清單的段落而沒有解釋句」 | `SKILL.md:194` | P1 |
| 「把教案備註原封不動放入 HTML｜學員看到製作過程」 | `SKILL.md:242` | P3（工程碼） |

**d. 衝突**【查證】
- 承接要求（`SKILL.md:84,183`）與 rubric 1-2、1-4 衝突。
- 本 skill 要求保留欄位名與檢查點（`:63-64`），改寫需求卻是「案例用內容稱呼」「核對交給 AI」。
- 與 `操作型講義.md:31` 衝突：該檔把「為什麼」砍到一句以下；本 skill 和 v0.6 則要求理由放在需要的位置。
- 與 course-designer 是互相退件的關係：本 skill 偵測到人工取代核心方法就退回 designer（`:53`），designer 又把連貫性交給本 skill（`course-designer/SKILL.md:45`）。分工本身合理，但 P2 的修正只能在 designer 那一層發生。

**e. 判定：不適用於「重設計活動與完成物」。** 它明文不改案例與操作，還凍結欄位名與檢查點。重設計完成後的文字層可以修改後使用：要改 `:63-65` 的凍結範圍與 `:84,183` 的承接例外。

---

## 3. course-designer

**a. 用途與預設產出**【查證】：G3 內容主責，「產出完整學員正文、示範、練習與答案」（`SKILL.md:9`）。輸出 `_lessons/{slug}/{unit-id}.md` 加 lesson record（`SKILL.md:21,43`），前提是 G0–G2 都已 PASS（`SKILL.md:13`）。

**b. 推向問題的指示**

| 引文 | 位置 | 推向 | 怎麼推 |
|---|---|---|---|
| 「起始材料保留要學員處理的特徵；不要先替學員分類、標註答案或修好問題。完整提示詞可用於示範，複製後取得正確輸出不等於學員能自行判斷。獨立練習要留下待學員完成的選擇或操作」 | `SKILL.md:40` | P2 | 把能力證據定義成「學員自己判斷」。全文沒有區分「學員判斷 AI 指出的 3 處」與「學員逐筆人工比對」，模型容易落到後者【推論】 |
| 「完整示範必須呈現輸入、理由、動作、結果與驗證，跟做與獨立練習則要有可觀察結果與修復路徑」 | `SKILL.md:13` | P2（輕） | 每段都要有驗證與修復，但沒有指定由 AI 協助驗證 |
| 「操作指令逐項記錄目的、起始狀態、動作與預期結果，素材以穩定 ID 引用」 | `SKILL.md:43` | P3、P1 | 內部紀錄以 ID 與固定欄位組成。條文要求「不逐項印成正文」，但寫正文時 ID 容易跟著外漏【推論】 |
| `required_sections`：13 個區段，含 `checks`、`recovery`、`transfer`；`instruction_fields`：purpose／start_state／action／expected_result | `references/learner-content-contract.json:11-31` | P1、P2 | 固定欄位契約，每一單元都要有 checks 與 recovery【推論：容易被照欄位組段】 |
| 「尚未實跑要明示」「仍未跑通就保留缺口」 | `SKILL.md:39` | P3（間接） | 未實跑標記本該留在內部紀錄，條文沒有說不得進入學員正文【推論】 |

**c. 防止問題的指示**

| 引文 | 位置 | 防 |
|---|---|---|
| 「確定完成物與本課要學的核心方法，在既有設計中說清學員與工具各自承擔的工作」 | `SKILL.md:37` | P2（有分工概念，沒有方向） |
| 「作者以人工、程式或其他工具補出的成品，只能作核對參考，不能代替核心方法成功的證據…改變核心方法或縮小目標須明示範圍變更並取得使用者同意」 | `SKILL.md:39` | P2（核心方法若定為 AI，人工替代不算成功） |
| 「正文依學員理解問題的進展安排…不能只依工具操作順序排列…理由放在影響選擇的地方」 | `SKILL.md:41` | P1 |
| 「檔名與跨課用途在需要時交代，不以『這一課／下一課』反覆代替內容承接」 | `SKILL.md:41` | P3-4（輕） |
| 「這些欄位供作者查缺漏，不逐項印成正文或固定卡片…不向學員暴露內部編碼檔名」 | `SKILL.md:43` | P1、P3（只管到「內部編碼檔名」） |
| 「完整句與連續推理是產出責任，不能留給排版或 copywriter 發明」 | `SKILL.md:49` | P1 |
| 示例三：被否定版本「交代了作業與動作，但讀者尚未理解為什麼需要專案或序列」 | `references/teaching-writing-examples.md:65` | P1 |
| 「每步重印目的、操作、結果、檢查、意義｜…依閱讀關係合成段落」 | `teaching-writing-examples.md:83` | P1（防表單化） |

**d. 衝突**【查證】
- `SKILL.md:41`（不以「這一課／下一課」代替承接）與 rubric 1-4（「你現在有了 X，下一節會拿它做 Y」）。程度不同，不算直接矛盾：rubric 要的是內容加上去向，designer 禁的是只寫去向不寫內容。
- 前提閘門「G0、G1、G2 為 `PASS`」（`:13`）不適合既有課改寫，要靠 course-repair 包一層。

**e. 判定：修改後可用（建議作為改寫主責）。** 它握有正文所有權，也允許在使用者同意下改核心方法。還缺三條：核心方法是「學員指揮 AI」、核對由 AI 協助、識別碼不得外露。另外 `:40` 要說清楚「學員判斷」指的是對 AI 產出做抽看與決策。

---

## 4. course-repair

**a. 用途與預設產出**【查證】：既有課程修復，分兩種模式（`SKILL.md:15-16`）。
- 受限修復：備份、修改，只重驗受影響範圍。
- 治理修復：`scan → plan → backup → fix → verify`，加上 `REPAIR-PLAN.md`／`REPAIR-REPORT.md`。
- G3 內容問題交 course-designer 處理（`SKILL.md:85`）。

**b. 推向問題的指示**

| 引文 | 位置 | 推向 | 怎麼推 |
|---|---|---|---|
| Scan 清單：「學員入口、材料、第一個動作、預期結果、快速檢查或修復路徑是否中斷」 | `SKILL.md:52-57` | P2（輕） | 掃描項偏重檢查與修復路徑的完整性。清單裡沒有「是否在學用 AI」 |
| shim description「missing checkpoints」 | `~/.claude/skills/course-repair/SKILL.md:3` | P2（輕） | 把「缺 checkpoint」當成觸發與修復目標 |
| 「備份…記錄原始 SHA-256…restore」「驗證輸出沿用 course-validator 的 evidence format」 | `SKILL.md:73-77,96` | （不直接） | 證據保留屬於製作端，條文沒有要求寫進學員正文 |

**c. 防止問題的指示**

| 引文 | 位置 | 防 |
|---|---|---|
| 「任何模式都不得為了驗證而拆碎自然課程敘事」 | `SKILL.md:18` | P1 |
| 「不要把正常段落改成名詞清單、待辦事項、內部編碼檔名或沒有前因後果的操作要求」 | `SKILL.md:90` | P1、P3 |
| 「不因 lint 綠燈、欄位齊全或文案變長而宣稱可用」 | `SKILL.md:103` | P1 |

**d. 衝突**【查證】
- 「重新定義課程要交付的核心成果或驗收方式」就必須「停止 repair 並建立新的 G0 contract」（`SKILL.md:22-25`）。改寫需求要「重新設計活動與完成物」，可能被判為 `outcome_reframe`（`references/new-system-routing.json:74`），整條改走 G0–G6。但 `:28` 又說「局部更新…練習、素材…仍屬 repair」。兩條之間的界線需要使用者裁決【推論】。

**e. 判定：修改後可用（當外殼）。** 備份、範圍、驗證流程可以沿用。先請使用者裁定「完成物改由 AI 產出」屬於局部練習更新（repair），還是核心成果重定義（G0）。內容本身仍交 course-designer。

---

## 5. course-reviewer

**a. 用途與預設產出**【查證】：舊入口的相容層，「不再維護第二套檢核矩陣」（`SKILL.md:9`），預設做局部評估。輸出是 Issue List 相容格式（`SKILL.md:33-39`），而且「不自行編輯課程正文或 HTML」（`SKILL.md:45`）。

**b. 推向問題的指示**：沒有直接條文。它把標準交給 `learner-action-contract.md` 與 course-validator（`SKILL.md:9`），因此會繼承第 11 節的偏向。範例 issue 的碼名（`explanation_gap`）屬於審查端用語，不會進入學員頁。

**c. 防止問題的指示**：「不另外定義品質分數…或風格偏好」（`SKILL.md:46`），也就是說它不會補上三個問題的檢查；「不讓 lint、格式齊全…取代實際跟做」（`:48`）。

**d. 衝突**【查證】：「不另外定義品質分數」（`:46`）跟本次 rubric 的 0–3 分制不相容。審查時要用 rubric，不能用 reviewer。

**e. 判定：不適用。** 它不改檔，也沒有 P1–P3 的判準；這次審查以 rubric 取代。

---

## 6. build-course-page

**a. 用途與預設產出**【查證】：把已審查正文轉成 HTML（`SKILL.md:9`）。產出 `courses/{slug}/partN/{unit}.html`，接著重建索引、跑 substance 稽核與文案 Gate（`SKILL.md:347-383`）。

**b. 推向問題的指示**

| 引文 | 位置 | 推向 | 怎麼推 |
|---|---|---|---|
| 「`<strong>卡住時：</strong>{錯誤現象 → stage ID → 回到哪裡修正 → 從哪裡重跑 → 是否清除錯誤資料 → 安全停止狀態}`」 | `SKILL.md:261` | **P3（明確成因）**、P2、P1-6 | 範本明文要求填「stage ID」，rubric 把階段碼列為工程碼（3-2）。一格塞六件事，偏重防錯 |
| 「`學員操作：`…`預期結果：`…`快速檢查：`…`卡住時：`」（learner-step 範本，標為「操作型頁面的主體」） | `SKILL.md:250-262` | P1、P2 | 固定四欄標籤構成主體，讀起來像待辦清單；每一步都有檢查與排錯【推論：範本前後雖有兩個 `<p>` 承接，固定欄位仍是主結構】 |
| 「若使用 step card，每張卡應包含適用的學員操作、預期結果、快速檢查與卡住時」 | `SKILL.md:155` | P1、P2 | 同上 |
| 「在關鍵決策或狀態轉換處插入 Checkpoint block；Checkpoint 要寫『現在應該看到 / 若沒看到 / 通過後才能繼續』」 | `SKILL.md:156`、範本 `:268-277` | P2（2-4 限制語）、P1 | 「通過後才能繼續」屬於條件限制語；數量按狀態轉換計，沒有上限 |
| 「常見錯誤…若能對應到某步，必須在該 step 附近用 `callout warn`」 | `SKILL.md:157` | P2（2-4） | 警語就近插在步驟旁，限制語密度上升 |
| 「寫明檔名／格式、用途、使用時機與備援」 | `SKILL.md:164` | P3（3-6） | 檔名必須出現 |
| 「完整保留成果與適用的修復資訊」 | `SKILL.md:170` | P2 | 修復資訊不能刪 |

**c. 防止問題的指示**

| 引文 | 位置 | 防 |
|---|---|---|
| 「不得把標籤或卡片當成教學證據；連續自然段落、表格或混合呈現…就可以通過」 | `SKILL.md:154` | P1 |
| 範本中的「`<p>{本階段的目的，以及它如何承接上一階段的具體結果。}</p>`」「`<p>{本階段完成了什麼，以及這個結果為何是下一階段的起點。}</p>`」 | `SKILL.md:257,262` | P1-2、P1-4 |
| 條件式文案 Gate：「第一個主要區段直接操作、兩個主要區段間沒有結果—目的承接…必須使用 `course-copywriter`」 | `SKILL.md:365` | P1 |
| 「不得為套版把連續正文重組為『目的／步驟／檢查／交付』卡片」「若完成物雖存在，但正文將原定核心方法改由人工或其他方法完成，退回 designer 確認」 | `SKILL.md:422` | P1、P2 |
| 「不以摘要取代教學…完整示範與可理解文字優先於卡片數量」 | `SKILL.md:394` | P1 |

**d. 衝突**【查證】
- 範本內部互相矛盾：範本要求每步前後寫承接 `<p>`（`:257,262`）；`:170` 卻說「不為每個區段新增引言或結語」，`:422` 又說「不得…增寫重述的本課／下課段落」。後兩條還與 rubric 1-4 衝突。
- README 過期：README 寫「Gemini 負責生成教學內容」（`README.md:8`）、`/build-course-page step 2.1`（`README.md:51`）；SKILL 卻寫「舊的 Gemini 直出與 Step Page 內容路徑已退場」（`SKILL.md:406`）。
- 專案規範 `gen-ai-36h/CLAUDE.md:100` 仍指示「用 build-course-page skill 的 step-page 範本建立 HTML」，跟 `SKILL.md:406` 衝突。

**e. 判定：修改後可用（只做 HTML 轉製）。** 它不負責改寫內容。至少要把 `:261` 的「stage ID」刪掉，並把 `:155-156` 的固定四欄與 Checkpoint 改成選用。

---

## 7. 「文案迭代」共用流程（course-copy-profile v0.6＋quickstart）

**a. 用途與預設產出**【查證】：用於「資料已有、但語氣不合適、段落跳躍、像待辦清單、術語突然出現」的講義（`course-copy-quickstart.md:3`）。流程是控制器依序派 Sol 評估、Luna 改寫、Sol 覆核，產出隔離的 Markdown 候選，交使用者做 H3 閱讀確認（`quickstart.md:41-51,81`）。

**b. 推向問題的指示**

| 引文 | 位置 | 推向 | 怎麼推 |
|---|---|---|---|
| 「原有數字、提示詞、案例、操作、條件及連結保留；必要事實確實缺少才依原P／Q界線回交」 | `course-copy-profile-v0.6.md:16` | P2（鎖定） | 人工活動與條件全數保留 |
| 「發現缺素材、技術矛盾、錯誤數據或需要改操作時，提供原文與回交理由，停下交人工決策…不自動改成整課修復」 | `quickstart.md:110` | P2（鎖定） | 偏題需要改操作，這個流程會停下 |
| 「涉及新素材、案例或教學目標應回交，不直接當本章文案未通過」 | `profile-v0.6.md:24` | P2 | 同上 |
| 「避免在交辦清單前後堆引言、摘要或轉場」 | `profile-v0.6.md:10` | P1（1-2、1-4 輕微） | 反填充條文，可能被讀成「不寫段首承接與收尾」【推論】 |

**c. 防止問題的指示**

| 引文 | 位置 | 防 |
|---|---|---|
| 「讀者應能說出誰要完成什麼、遇到什麼問題、目前缺什麼，以及下一步由誰做、為什麼」 | `profile-v0.6.md:7` | P1-1、P1-5 |
| 「先用日常語言交代角色和工作問題，再引入檔名、訊息編號或縮寫作為查找依據；它們不能代替故事」 | `profile-v0.6.md:8` | **P3（最直接的防止條文）** |
| 「`reading_load`說明日期、代碼、條件、例外和操作是否堆在一起」 | `profile-v0.6.md:10` | P3、P1-6 |
| 「理由放在需要的位置」 | `profile-v0.6.md:9` | P1-3 |
| 「作者直接修原有主要段落，不能只增加前言」 | `profile-v0.6.md:16` | P1 |
| 「你的連續閱讀回饋若否定候選，須記錄為本稿未通過的證據；AI的B L3…不能取代這項判斷」 | `quickstart.md:108` | 流程保證，三個問題都適用 |

**d. 衝突**【查證】
- `AGENTS.md:7` 要求「套用course-copywriter的事實保留邊界」，所以 copywriter `:63-65` 凍結欄位名的規定一併適用，跟 profile `:8`「代碼不能代替故事」有張力：代碼要保留，只能在前面補日常說明。
- 改寫需求要求案例改用內容稱呼，代碼本身可能必須移除，這一點超出本流程的權限【推論】。

**e. 判定：不適用於重設計；文字層修改後可用。** 四項讀者檢查跟 P1、P3 對得很準，但流程的定位就是不改操作與案例。

---

## 8. gen-ai-36h/CLAUDE.md（課程專案規範）

**a. 用途**：課程定位、檔案結構、設計規範、新增頁面流程，以及 2026-10-09 修訂摘要。

**b. 推向問題的指示**

| 引文 | 位置 | 推向 | 怎麼推 |
|---|---|---|---|
| 「主軸：基本對話與核對 + 來源筆記 + 小工具測試 + 人工覆核後 Make 自動化 + 結業專題」 | `:10` | **P2（明確成因）** | 課程主軸直接寫進「核對」「測試」「人工覆核」。五項主軸裡有三項是驗證或人工作業 |
| 「part5/ 人工覆核與 Make 自動化」 | `:38`、`:57` | P2（rubric 2-6） | Part 名稱以人工防錯為主軸；rubric 2-6 規定「標題以人工防錯為主軸 → 0」 |
| 「本課九欄教學資料、已覆核新列與 Make 測試流程」 | `:87` | P2、P3 | 把九欄、覆核、測試列為 Part 5 素材來源 |
| 「七欄工具卡統一…Make使用ReviewedQueue新列觸發，九欄、四分類、待覆核／已覆核，只寫未寄出草稿。教學工作區已跑T01–T07」 | `:112` | **P2、P3（明確成因）** | 寫成已定案的事實，一起列出英文表名、狀態詞、測試碼範圍。與 copywriter「不可破壞的教學事實」合用時，這些內容會被當成不可改動的事實保留【推論】 |
| 「正式正文由 `_repair/2026-10-09/lesson-plans/` 的 learner-content 範圍轉製…28頁URL、設計、導覽與密碼關卡保留」 | `:111` | P2（鎖定） | 指定既有教案為正文來源 |
| 「對照『內容資產來源』表，先讀來源課程的對應頁面，避免重新發明」 | `:98` | P1、P2（間接） | 來源課程 office-ai 就是《操作型講義》的樣板（見第 10 節），會沿用它的元件與檢核習慣【推論】 |

**c. 防止問題的指示**：沒有直接條文。`:9` 寫「不涵蓋：API / RAG / Agent」，只限縮範圍。

**d. 衝突**【查證】
- `:100`「用 build-course-page skill 的 step-page 範本」對上 `build-course-page/SKILL.md:406`「Step Page 內容路徑已退場」。
- `:101` 要求把卡片從 `locked` 改為可學習，屬於建置期的過時流程。
- `:10` 的主軸與改寫需求「學員主要是在指揮 AI 做事、核對工作也交給 AI 協助」**正面衝突**。

**e. 判定：修改後可用。** 改寫前必須先改 `:10`、`:38/57`、`:87`、`:112`，否則任何 skill 照專案規範都會保留人工覆核主軸。

---

## 9. courses/AGENTS.md（課程目錄共用入口）

**a. 用途**【查證】：把「文案迭代／文案迭代改」導向 course-manager 的 v0.6 控制器（`:5-19`）。

**b. 推向問題的指示**
- 「套用course-copywriter的事實保留邊界」（`:7`）把 copywriter 的凍結範圍帶進來，P2、P3 會被鎖定。
- 「缺必要事實或需改操作時依現行規範回交，不虛構補齊」（`:13`）。

**c. 防止問題的指示**：「依四項讀者檢查修正與覆核，不用機械檢查或AI分數代替實際理解」（`:12`），可防 P1。

**d. 衝突**：沒有額外衝突。它與 profile v0.6 一致，繼承第 7 節的張力。

**e. 判定：不適用於重設計；文字層適用。** 它只是路由，沒有內容規則。

---

## 10. _規範/操作型講義.md

**a. 用途**【查證】：「低原理、高操作」內容組織 SSOT，提供 dialog-box、expected-output、demo-flow 三個元件與課後素材包（`:3`、`:48-56`、`:253`）。觸發詞是「低原理高操作」等（根目錄 `CLAUDE.md:113`），不會自動套用到本課。不過本課的素材來源 office-ai 就是它的樣板課（`:448`）。

**b. 推向問題的指示**

| 引文 | 位置 | 推向 | 怎麼推 |
|---|---|---|---|
| 「『為什麼』可以保留，但要砍到一句話以下；超過一句話就改為『實例示範』」 | `:31` | P1（1-3） | 理由被壓縮到一句以下 |
| 「『為什麼要這樣』（原理）｜砍掉，移到 demo 結束後的 `demo-takeaway`」 | `:210` | P1（1-3） | 理由移到段後，執行指令的當下沒有理由 |
| 「grep 該頁無『為什麼／原理是／之所以』開頭段落」 | `:427` | P1 | 用驗收條件禁止解釋段 |
| 「步驟 5：驗證輸出（5-9 分鐘）— **這步絕對不能省**」「AI 是助手不是主管，簽核責任永遠在你」 | `:287`、`:292` | P2 | 強調由人負責驗證，沒有教 AI 協助核對 |
| 「含驗證點：刻意埋『AI 容易誤判的陷阱』」 | `:298` | P2 | 練習素材的設計目的是讓人去抓 AI 的錯 |
| 「按 Part 分類、按場景編號（P1-1, P1-2, P2-1...）」 | `:303` | P3 | 提示詞以編號命名 |
| 「該頁仍有 ≥ 5 個 `.lesson-section`」 | `:428` | P1（輕） | 以區段數作為驗收條件 |

**c. 防止問題的指示**

| 引文 | 位置 | 防 |
|---|---|---|
| 三大要素：「可直接複製的 prompt」「AI 大概會回什麼的示範」 | `:40-44` | **P2（全部稽核對象中唯一以 AI 對話為主體的規範）** |
| 「示範完整流程 → 學員模仿 → 一句話 takeaway」 | `:36` | P2 |
| 「抽象例子…換成具名情境（給對象、時間、地點、字數）」 | `:211` | P1-1、P3 |

**d. 衝突**【查證】
- `:31,210,427` 跟 `course-content-substance.md:7`（「說明術語、原理、成立條件與使用方法」）、`profile-v0.6.md:9`、copywriter `:178`，以及 rubric 1-3 都衝突。
- `:395`「第 1 批完成後必須暫停」與 `:413-415`「git add … git push」屬於流程指示，跟根目錄 CLAUDE.md 的 commit 流程重疊，與本題無關。

**e. 判定：修改後可用。** 它是唯一把「AI 對話」放在中心的規範，可借用 dialog-box／expected-output 來修 P2。使用前要先撤除 `:31,210,427` 的砍理由條文，並把「驗證」改成「請 AI 標出處或交叉檢查，學員抽看」。

---

## 11. 共用規範（所有 skill 都會讀到）

| 引文 | 位置 | 推／防 | 說明 |
|---|---|---|---|
| 「目標完成物｜本節留下的檔案、畫面、設定、決策、**測試紀錄**或交付物…以及須透過哪個核心方法完成、學員與工具的分工」 | `learner-action-contract.md:30` | 推 P2 | 測試紀錄被明列為合格完成物。rubric 2-2 規定「主項是核對、證據、測試紀錄 → 1」。契約有「分工」欄，但沒有指定方向 |
| 「失敗時的回復位置｜現象、原因、回修位置、重跑起點、資料是否清除、安全停止狀態」 | `learner-action-contract.md:34` | 推 P2（2-4）、P1-6 | 每單元都必填，排錯與限制語因此變多【推論】 |
| 「空白、placeholder…都算 `BLOCKED`」 | `learner-action-contract.md:23` | 推 P2（間接） | 八欄全都必填，連 recovery 也是 |
| 「契約欄位用於查缺漏，不逐項轉成章節、卡片或待辦清單…『接著／這一課／下一課』不能代替推理」 | `learner-action-contract.md:54` | 防 P1 | — |
| 「內部契約、欄位、角色標籤與證據格式只支援製作，不得取代自然、完整且可閱讀的正式內容」 | `learner-action-contract.md:15` | 防 P1、P3 | — |
| 「心得、定義填句、自評及照貼完整提示詞的結果，不能單獨證明數位實作能力」 | `course-content-substance.md:13` | 推 P2 | 「用 AI 產出」本身被降格為不足以證明能力，模型會補上學員自己做的判斷或核對【推論】 |
| 「正式學員正文必須可獨立閱讀：從可理解的問題與目的起步…最後回到問題、核對成果並說明使用條件」 | `course-content-substance.md:9` | 防 P1 | — |
| 「收束時回到起始問題及使用條件」 | `lesson-plan-template.md:39` | 防 P1-4（部分） | 沒有要求指向下一節 |
| 「代詞『它、這個、上述』須能唯一指向對象」 | `llm-prose-risk-gate.md:122` | 防 P3-3（間接） | 只管代詞，沒有管代碼 |
| 「第一個句子直接交代情境、任務或判準」 | `llm-prose-risk-gate.md:95` | 防 P1-1 | — |

---

## 12. skill-packages 與安裝版的差異

`diff -r`（< package，> installed）。六個 skill 都有差異；安裝版另有 `course-designer/references/teaching-writing-examples.md`，package 沒有。

| skill | 主要差異 | 對三個問題的影響 |
|---|---|---|
| 全部 | package 用 `$COURSE_WEB_ROOT`／`$SKILLS_ROOT`，「未設定時停止」；installed 寫死絕對路徑 | 換成 package 版時，沒設環境變數會直接停止。與內容無關 |
| course-copywriter | package `:82`：「補足能回答『為什麼現在進入下一步』的橋接句…『剛才已確認…現在把…』」；package `:198`：「每一段操作前先回答『我們剛才看到什麼，所以現在要做什麼』」；package `:211`：「第一個學員動作前已交代情境、手上材料、完成物」。installed 改成「不新增橋接句」「不逐段補『剛才／現在／所以』」 | **P1：package 版較符合 rubric 1-2，installed 版放寬了承接要求。** installed 另外新增 `:53`「核心方法被人工…取代 → BLOCK」，對 P2 有利。package `:191-192` 有「文案迭代」與「內部製作用語須…轉成具體說明」，installed 刪掉了，對 P3 稍有不利 |
| course-copywriter | package `:94`：「編輯前建立這張矩陣；任何一格空白都要補內容或標記為 `BLOCK`」；`:144`：名詞表加「白話定義」欄 | package 版的證據矩陣更硬，對 P2 的推力更強；名詞表對 P3 有利 |
| course-handout-designer `beginner-continuity-gate.md` | package `:22-38` 要求「第一個學員動作前必須形成這條因果鏈」，並要求主要階段之間能填入「剛才…所以現在要…目的是…」；installed 改成「不新增固定承接句」 | P1：理由同上，package 較符合 rubric 1-2 |
| course-designer | package 有 outcome_ids／criterion_ids／capability_ids／learning_coverage 欄位（`learner-content-contract.json:12-15,30-39`），並要求逐項記錄教學、練習、評量證據。installed 新增 `:37,39,40,41,43` 的核心方法、實跑、正文組織條文 | package 版的 ID 帳更重，P3 外漏風險較高；installed 的 `:39`（人工替代不算核心方法成功）與 `:41`（依理解進展組織）對 P1、P2 有利 |
| course-repair | package 只有 scan→plan→backup→fix→verify 一種模式；Verify 規定「操作或成果改動重做獨立試學；跨單元改動重做 full-course trial」 | package 版的驗證負擔較重，但這些在製作端，不會直接進入學員頁 |
| course-reviewer | package 以 validator 為唯一標準，`site` 會跑完整驗收 | 對三個問題沒有直接影響 |
| build-course-page | package `:158`：「若版面過長，優先壓縮背景文案，不刪操作、checkpoint、修復資訊」；`:160`：「背景可壓縮」；`:170`：「每個主要區段先寫目的與上一段的具體結果」。installed 改成「不為每個區段新增引言或結語」 | **package 版對 P1、P2 推力更強**：壓縮背景、保留 checkpoint。但它的 `:170` 承接要求較符合 rubric。兩版的 `:261` 都有「stage ID」 |

結論【查證＋推論】：installed 版比 package 新。它削弱了固定承接句要求（對 rubric 1-2、1-4 不利），同時新增了「人工替代核心方法 → 退回」與「依理解進展組織」（對 P1、P2 有利）。兩版都沒有「核對交給 AI」或「案例用內容稱呼」的條文。

---

## 13. 衝突彙整

1. **承接與收尾 vs rubric 1-2、1-4**：installed 的 copywriter `:84,183`、beginner-gate `:24`、build-course-page `:170,422`、profile v0.6 `:10`，都把段首承接與「下一節會用到」寫成例外或禁止的填充。rubric 卻把它們當成 3 分樣子。
2. **理由壓縮 vs 理由就位**：`操作型講義.md:31,210,427`，對上 copywriter `:178`、profile `:9`、`course-content-substance.md:7`、rubric 1-3。
3. **事實凍結 vs 改寫需求**：copywriter `:21,61-65`、AGENTS `:7,13`、quickstart `:110`、`gen-ai-36h/CLAUDE.md:111-112`，凍結了操作、檢查點、欄位名與 Part 5 設計。改寫需求要的是重設計。
4. **課程主軸 vs 改寫需求**：`gen-ai-36h/CLAUDE.md:10,38` 寫「人工覆核」，改寫需求要「核對交給 AI」。
5. **build-course-page 範本內部**：`:257,262` 要求承接 `<p>`，`:170,422` 卻禁止增寫引言與結語。
6. **路由**：shim 與 canonical 的 description 不一致，handout-designer 和 course-designer 都可能被觸發；course-repair `:22-25` 與 `:28` 對「改完成物」屬於哪一層的界線不清。
7. **過期指示**：`gen-ai-36h/CLAUDE.md:100-101`、`build-course-page/README.md:8,51`，對上 `build-course-page/SKILL.md:406`。

---

## 14. 適用判定一覽

| 對象 | 判定 | 理由 |
|---|---|---|
| course-handout-designer | 修改後可用 | 唯一以重建講義為目的的方法庫，但沒有 AI 為主的分工規則，還要求素材顯示檔名 |
| course-copywriter | 不適用（重設計）／修改後可用（文字層） | 明文不改案例與操作，凍結欄位名與檢查點；P1 Gate 很好用 |
| course-designer | 修改後可用（建議主責） | 握有正文所有權，可在使用者同意下改核心方法；缺 AI 核對與識別碼規則 |
| course-repair | 修改後可用（外殼） | 備份與驗證流程可沿用；「改完成物」可能被判成 G0，需使用者裁決 |
| course-reviewer | 不適用 | 不改檔、沒有評分制，審查以 rubric 取代 |
| build-course-page | 修改後可用（只轉 HTML） | 範本的 stage ID、固定四欄與 Checkpoint 要先改 |
| 文案迭代 v0.6＋quickstart | 不適用（重設計）／修改後可用（文字層） | 四項讀者檢查對 P1、P3 很準，但禁止改操作 |
| gen-ai-36h/CLAUDE.md | 修改後可用（必須先改） | 主軸與 Part 5 名稱直接寫進人工覆核；`:112` 凍結代碼與流程 |
| courses/AGENTS.md | 不適用（重設計）／適用（文字層路由） | 只是路由，繼承 copywriter 的凍結範圍 |
| _規範/操作型講義.md | 修改後可用 | 以 AI 對話為主體，可用來修 P2；但砍理由的條文會加重 P1 |

---

## 15. 整體結論

**P1 不說人話**
- 【查證】沒有任何條文要求寫成待辦清單。反清單條文很多，最直接的是 copywriter `:40-46,152,194`、`learner-action-contract.md:54`、course-repair `:90`。
- 局部成因【查證】：build-course-page 的固定四欄 step card 與 Checkpoint 範本（`:155-156,250-277`）、`learner-content-contract.json` 的固定區段、`操作型講義.md:31,210,427` 的砍理由條文。
- 放寬之處【查證】：installed 版刻意放寬了段首承接與收尾（第 13 節第 1 點），跟 rubric 1-2、1-4 字面衝突。
- 【推論】照字面遵守**不會必然**產出 P1，但允許省略承接與收尾，也允許以固定欄位組段。

**P2 偏離主題**
- 【查證】六個 skill 都沒有規定「本課核心方法是學員指揮 AI」或「核對交給 AI」。
- 明確成因在專案層：`gen-ai-36h/CLAUDE.md:10,38,87,112` 把人工覆核、測試、九欄寫成主軸與既定事實。
- 共用契約允許測試紀錄當完成物（`learner-action-contract.md:30`），每單元必填修復欄（`:34`），還把照貼提示詞的結果降格（`course-content-substance.md:13`）。
- copywriter 的分流與終態規則（`:105,116,207`）把篇幅推向人工佇列。
- 【推論】照字面遵守專案規範加上 copywriter 與 v0.6 的事實保留，Part 5 一帶的 P2 會**必然保留**。其餘頁面屬於技能**放任**：沒有方向規則，要靠模型自行判斷。

**P3 編號複雜**
- 明確成因【查證】：build-course-page `:261`「stage ID」、asset gate `:11`「顯示檔名、格式…版本」、copywriter `:63` 凍結欄位名與模組名、copywriter 範例本身（`rewrite-patterns.md:18`、`teaching-evidence.md:23-30`）、`gen-ai-36h/CLAUDE.md:112`。
- 防止條文【查證】：profile v0.6 `:8,10`、beginner-gate `:28-32`、designer `:43`。
- 放任：「代碼當主詞」（3-3）與「章節碼跨頁引用」（3-4）沒有任何條文管到。
- 【推論】這是部分成因加部分放任，不必然發生，但很容易發生。

**建議**：以 course-designer 為改寫主責，方法參考 handout-designer，外面包 course-repair 受限或治理模式負責備份與驗證；文字層再交 copywriter 或文案迭代；HTML 交 build-course-page。動手前至少要改以下幾處：
1. `gen-ai-36h/CLAUDE.md:10,38/57,87,112`：主軸改成「指揮 AI 產出＋AI 協助核對」，並註明 2026-10-09 的設計事實不再凍結。
2. `learner-action-contract.md:30` 與 `course-designer/SKILL.md:37,40`：明定本課核心方法與分工。完成物主項必須是 AI 成果；核對由 AI 標出處或交叉檢查，學員只抽看 3 處以內；測試紀錄不得作為主完成物。
3. `build-course-page/SKILL.md:261`：刪除「stage ID」；`:155-156` 的固定四欄與 Checkpoint 改成選用。
4. `course-copywriter/SKILL.md:61-65`：允許把識別碼與英文欄名改成內容稱呼，只有學員必須照填的地方保留。新增「代碼不當主詞、跨頁引用用內容」。
5. `course-copywriter/SKILL.md:84,183`、`beginner-continuity-gate.md:24`、`build-course-page/SKILL.md:170,422`：改成與 rubric 1-2、1-4 一致。段首要接住上一段的結果，結尾要收回成果並指出下一節用途，這兩者不算填充。
6. `asset-discoverability-gate.md:11`：檔名只出現在取得連結處，正文用內容稱呼。
7. 使用者需要先裁定 course-repair `:22-25`：「完成物改由 AI 產出」屬於 repair 還是 G0。
