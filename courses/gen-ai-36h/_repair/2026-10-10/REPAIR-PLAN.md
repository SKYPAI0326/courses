# Repair Plan: gen-ai-36h — 實作深度修復 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 讓零基礎學員能用多來源、帶有歧義與更新的工作材料，獨立做出可核對、可修訂、可交接的成果，同時保留課程免寫程式定位。

**Architecture:** 以 `_repair/2026-10-09/lesson-plans/` 作為本課正式教案來源，先補工作案例、完整示範、核對答案與修復路徑，再用既有 renderer 更新指定 HTML 的 `.lesson-body`。最後將受影響教案精確同步到全站 `_lessons/gen-ai-36h/`，並以備份、還原腳本、保真檢查及內容審查留下可追溯證據。

**Tech Stack:** Markdown 教案與素材、CSV/TXT/HTML 教學資產、Python 3 renderer（BeautifulSoup、markdown-it-py）、現有課程 lint／結構／內容驗證工具。

**Spec:** `_repair/2026-10-10/CONTENT-REPAIR-DESIGN.md`；問題基線見 `_review/2026-10-10/PRACTICE-DEPTH-REVIEW.md`。

## Global Constraints

- 課程維持零程式、無 AI API、人工覆核與全虛構安全資料。
- 每條核心學習路徑都包含完整示範、帶回饋練習、條件改變後的獨立練習；頁數、資料列數和工具數不作深度門檻。
- 所有新學員正文留在既有 `.lesson-body`；不改頁面殼層、URL、導覽、密碼 gate、CSS 設計或 PRAC6／PRAC7 表單互動。
- Make 的 T01–T07、九欄與四分類、`ReviewedQueue` 核准後才觸發及「只寫未寄出草稿」維持原狀；不加入對外寄送或 API。
- 來源教案只改本計畫列出的單元；同步到全站 `_lessons/gen-ai-36h/` 時只複製同名、同內容的明列檔案。
- 不覆蓋工作樹其他課程或使用者變更；不使用 `git add -A`，不建立混合工作樹提交。
- 人工跟做、Claude／NotebookLM／Make 目標帳號實跑與真人理解測試沒有完成前，驗證狀態維持 `PENDING`，不宣稱 `HUMAN_READY`。

## Review Focus

- 日期、負責人或核准狀態缺漏時，學員應保留未知、指出要問誰與要問什麼，不得自行補值。
- 核准預算上限、實際供應商報價、已被取代的舊條款分別代表不同事實；超出上限不應被誤寫成來源互相矛盾。
- 多重意圖、引用舊訊息、重複提交或資料不足的原文應能導向可解釋的分類、補問或人工接手，而不會進入已核准佇列。
- 計時器、報價與圖表的需求變更應指出受影響的規則和回歸測試；舊測試結果仍可被重現。
- 上游來源改變時，學員應能辨識要重做的下游成果，留下核對證據與接手者可採取的下一步。

---

## Scope

- slug：`gen-ai-36h`
- 近期开課時間：unknown；按高影響教材修訂處理。
- Backup required：yes；fix 開始前備份所有下列既有目標檔並建立可執行還原腳本。
- 唯一已核准設計：`CONTENT-REPAIR-DESIGN.md`。本計畫通過後才進入備份與教材修正。
- 修復前掃描：`_repair/2026-10-10/SCAN.md`；包含 Activity Identity Audit 與 Shared Copy Audit。

### 明列的教材教案來源

在 `_repair/2026-10-09/lesson-plans/` 修改以下 20 份來源教案：

`CH2-1.md`、`CH2-2.md`、`CH2-3.md`、`PRAC2.md`；
`CH3-1.md`、`CH3-2.md`、`PRAC3.md`；
`CH4-1.md`、`CH4-2.md`、`CH4-3.md`、`CH4-4.md`、`PRAC4.md`；
`CH5-3.md`、`PRAC5.md`；
`CH6-2.md`、`PRAC6.md`；
`CH7-1.md`、`CH7-2.md`、`CH7-3.md`、`PRAC7.md`。

PRAC1 已有一項文字任務；只移除與它衝突的舊驗收提示，不擴成多張提示詞卡。

### 明列的學員 HTML

- 只移除 B01 所列的 19 個舊 `.callout.info` 操作／成果契約區塊；不移除同頁正文、其他提示框、導航、gate 或 script。
- 依來源教案更新上述 20 頁：`part2/CH2-1.html`、`CH2-2.html`、`CH2-3.html`、`PRAC2.html`；`part3/CH3-1.html`、`CH3-2.html`、`PRAC3.html`；`part4/CH4-1.html`、`CH4-2.html`、`CH4-3.html`、`CH4-4.html`、`PRAC4.html`；`part5/CH5-3.html`、`PRAC5.html`；`part6/CH6-2.html`、`PRAC6.html`；`part7/CH7-1.html`、`CH7-2.html`、`CH7-3.html`、`PRAC7.html`。
- Part 6 名稱需一致，因此另更新 `part6/CH6-1.html` 的 Part 標籤；保留該頁現有單元正文。
- B01 清理頁面：`part1/CH1-1.html`、`CH1-2.html`、`CH1-3.html`、`PRAC1.html`；以及上列 Part 2–4 頁面、`part6/CH6-2.html`、`part7/CH7-2.html`、`CH7-3.html`。總計 19 頁。

### 既有來源、課程索引與驗證目標

- `_repair/2026-10-09/lesson-meta.json`：同步受影響單元標題／完成物，統一 Part 6 名稱與 PRAC 驗收。
- `_tools/render-lessons.py`：更新其 Part 6 顯示名稱，增加可指定本次 evidence 輸出路徑的選項；renderer 仍只替換既有正文容器與指定標題，不得重寫頁面殼層。
- `index.html`、`CLAUDE.md`、`../../_outlines/gen-ai-36h.md`：統一 Part 6 名稱、課程路徑與成果承諾。
- `assets/START-HERE.md`、`assets/prompt-library.md`、`assets/quote-rules.md`、`assets/quote-test-cases.csv`、`assets/sales-expected-results.md`、`assets/reference-timer.html`、`assets/reference-quote.html`、`assets/reference-chart.html`、`assets/showcase-example.html`：只更新本計畫指定的素材說明、需求、參考成品和答案。
- 新驗證另寫到 `_validation/2026-10-10/`；保留 2026-10-09 驗證記錄，不覆寫既有 verdict。
- 正式教案 mirror：只同步上述 20 份教案到 `../../_lessons/gen-ai-36h/` 同名檔。

### 新增素材

- `assets/workplace-cases/part2/`：`START-HERE.md`、`chat-log.md`、`progress-register.csv`、`change-note.md`、`attachment-case.md`、`answer-key.md`。
- `assets/workplace-cases/part3-demo/`：`approval-scope.md`、`change-notice.md`、`vendor-quote.md`、`meeting-extract.md`、`answer-key.md`。
- `assets/workplace-cases/part3-solo/`：`project-brief.md`、`change-record.md`、`supplier-quote.md`、`meeting-notes.md`、`answer-key.md`。
- Part 4：`assets/sales-raw-transactions.csv`、`assets/sales-data-dictionary.md`、`assets/sales-case-answer-key.md`。
- Part 5：`assets/part5-unclassified-messages.csv`、`assets/part5-classification-answer-key.md`。
- Part 6：`assets/part6-workflow-case.md`。
- Part 7：`assets/capstone/START-HERE.md`、`request.md`、`project-status.csv`、`policy-v1.md`、`policy-v2.md`、`meeting-notes.md`、`worked-example.md`、`test-evidence.md`、`answer-key.md`。

## 預計刪除／合併的舊內容：需逐項核准

以下每頁只刪除一個位於 `.lesson-body` 外、舊版 `.callout.info` 區塊。這些區塊要求的任務與現行正文不相符，或要求正文沒有教的技能。表中另列需保留的有效退路／驗收提醒：若正文已有等價步驟便不重複；若沒有，先把精簡、適用的提醒移入該頁相關步驟，再刪除整個舊區塊。其他內容、程式、導覽、權限 gate 均保留。這是 course-repair 規範要求在使用者核准計畫後才可執行的刪除清單。

| # | HTML | 預計移除的舊要求 | 保留或移入正文的有效提醒 |
|---:|---|---|---|
| 1 | `part1/CH1-1.html` | 四工具比較、任務矩陣與自選任務卡 | 帳號／功能未核實時標 `NOT_RUN`，只在正文沒有同義狀態記錄時保留 |
| 2 | `part1/CH1-2.html` | 建三張 prompt 卡 | 一次只修一個欄位、保留上一版；若正文已有便不複製 |
| 3 | `part1/CH1-3.html` | System/User 拆分與建立助手 | 設定功能不可用時可回退純對話 prompt，不宣稱已建立助手 |
| 4 | `part1/PRAC1.html` | 三張自製卡及逐卡測試 | 用安全練習資料；未在目標工作區跑過的結果標 `NOT_RUN` |
| 5 | `part2/CH2-1.html` | 同一原料重走四種流程並另做自選案例 | 輸出偏題時先重判任務用途，再修指令，不盲目重寫 |
| 6 | `part2/CH2-2.html` | 同一原料輸出 Email、報告、簡報三個版本 | 回到信件骨架修正；不得補入未確認承諾 |
| 7 | `part2/CH2-3.html` | 將週報／會議原料改作多模態練習 | 可用文字備援完成文字整理，但需明示這不算圖片／音訊辨識通過；未實跑標 `NOT_RUN` |
| 8 | `part2/PRAC2.html` | Email pipeline、四回合腳本與另一工作包 | 平台無法實跑時仍可交付文件成果，並如實標記未實跑 |
| 9 | `part3/CH3-1.html` | NotebookLM Audio Overview 全流程 | Audio Overview 是選用功能；未生成或驗證時標 `NOT_RUN`，主線仍核對來源引用 |
| 10 | `part3/CH3-2.html` | 短期／長期雙層知識庫 | 保留資料夾加索引表的手動替代方式；欄位需與正文一致 |
| 11 | `part3/PRAC3.html` | 自建 Notebook 與五個萃取 prompt | 未在目標帳號驗證的分享／檢索功能標 `NOT_RUN`，不作答題門檻 |
| 12 | `part4/CH4-1.html` | 畫三層架構圖並做三筆新工具測試 | 生成失敗時可用規則表／流程圖完成需求核對，不把生成成功當成學習驗收 |
| 13 | `part4/CH4-2.html` | 三個工具至少完成一個可重跑版本 | 修改時保留上一版規則並一次改一個變因 |
| 14 | `part4/CH4-3.html` | 從共用表格做互動 Dashboard | 互動失效時允許交付靜態圖表和資料字典，並標記未驗證互動 |
| 15 | `part4/CH4-4.html` | 風格覆寫、手機版與 GitHub Pages 部署 | 只聲稱已實際保存／重開的成果；未驗證公開部署不得宣稱已上線 |
| 16 | `part4/PRAC4.html` | 三個工具藍圖，至少一個重跑 | 仍只交一件工具；未做的部署測試明示未做 |
| 17 | `part6/CH6-2.html` | 五時段場景地圖與兩項缺口分析 | 工作流程允許全手動；可先紙上畫流程與檢查點，不等待工具串接 |
| 18 | `part7/CH7-2.html` | 統一 MVP、五要素求助與展示腳本 | 保留最後成功版本與已知限制；修訂後重跑受影響測試 |
| 19 | `part7/CH7-3.html` | SBI 回饋卡、兩張同儕回饋與改進承諾 | 若即時平台 demo 未驗證，可用固定案例演示並標 `NOT_RUN`，不可當成 live 驗收 |

`part1/PRAC1.html`、`part2/PRAC2.html`、`part3/PRAC3.html`、`part4/PRAC4.html` 的舊區塊標頭是「成果驗收」；其餘 15 個舊區塊標頭是「本節操作契約」。刪除程序須先確認 19 個目標各命中一次，否則停止，不做猜測式全域替換。

## BLOCKER

### [LEARNER_PATH] 19 頁新舊驗收矛盾

- 問題：正文外舊契約要求與現行 learner-content 不同，且部分新增未教能力。
- 修法：依上表逐一移除舊區塊；正文與 Hero 完成物成為唯一學員主線契約。
- 修復步驟：移除前對照表格的有效提醒；正文已有等價步驟就去除重複，缺少且仍適用就移入最近的操作／修復 checkpoint，過時或不符免程式定位者不保留。
- 驗證：19 頁目標區塊命中數歸零；HTML `.lesson-body`、其餘 callout、nav route、auth script 與修前備份相符。

## MAJOR

- **M01/M02/M04，Part 2：**保留短例作首次示範；新「門市退貨 SOP 更新」工作包含多角色聊天、追蹤表、核准更新、依賴、重複資訊及未確認欄位。CH2-1 教用途與取捨，CH2-2 核對承諾後修信，CH2-3 以未預先標記的附件紀錄判斷提案／條件同意／撤回／待確認，PRAC2 獨立交付摘要、待辦、依賴、待決策與接手提醒。`prompt-library.md` 說明 20 項是同一舊情境的輸出參考庫。
- **M03，Part 3：**星河 v1 保留為引用入門。新跨來源示範分開列核准上限 NT$22,000、供應商報價 NT$25,000、v2 更新的交付範圍與未核准的追加款；核對答案說明「超過核准」不等於「來源衝突」。Solo 改用另一個活動場地專案文件組，答案在完成任務後提供。
- **M05/M07，Part 4：**保留報價算法、尾差、拒絕條件與 24 月資料。新增交易層 CSV，明確包含一筆重複 ID、一筆缺日期、一筆退款及一筆取消；欄位字典說明保留、排除或待查規則；答案鍵列出清理後總和與限制。CH4-1 增加可調工作／休息時間及範圍限制；CH4-2 加核准門檻條件；CH4-3 回答分組趨勢與資料限制；PRAC4 仍只交一件工具但須提交一項需求變更、受影響規則和相關回歸結果；參考成品與測試表同步支援。
- **M06，Part 5：**保留 T01–T07 不改。新原文批次包含多重意圖、引用舊信、重複來源鍵、缺必要資料及一般詢問；答案鍵逐列列出主要分類、九欄修訂、補問或人工接手理由。CH5-3 示範一筆後讓學員自行覆核；PRAC5 分開核對業務分類與已核准列才進 `ReviewedQueue` 的流程證據。
- **M08，Part 6：**保留七欄卡、local save 與 JSON 備份。CH6-2 用一條人工可執行的流程，從會議紀錄到來源核對、通知草稿與交接；來源改版後重查受影響輸出。PRAC6 至少交一張含新條件、檢查點與恢復路徑的工作流程卡；表單 schema 不變。課名統一為「個人 AI 工作流程整合」。
- **M09，Part 7：**提供一包完整虛構專題材料、一份文件型端到端完成範例與可追溯證據。CH7-1 界定任務；CH7-2 按作品類型選測試且處理一項會改變結果的新條件；CH7-3 依觀察到的回饋修改並重測。PRAC7 保留填表／匯出互動，另驗收可取得成果、已處理變更、核對證據、交接說明與修訂狀態。

## Activity Identity Audit

| page | Demo | Together adds | Solo transfer | overlap verdict |
|---|---|---|---|---|
| CH2-1 | 舊簡例：判斷週報應摘要／分類何者，形成短輸出 | 用多角色更新包合併重複狀態並指出依賴 | 用未揭示的工作目的寫主管摘要並指出取捨理由 | 相同材料時只提取理由；Solo 改任務與不確定資訊 |
| CH2-2 | 已知／未知事實寫延期信 | 同一工作包核對可承諾範圍並修草稿 | 收到更正後提交可審核新版，標未確認欄位 | 延續素材但增加承諾邊界和修訂責任 |
| CH2-3 | 清楚標註素材做圖片／音訊辨識與人工校對 | 提取原句／位置，辨認條件同意 | 另一份未標狀態紀錄，分類並保留無法辨識處 | 新增語意判斷；文字備援不算多模態通過 |
| PRAC2 | 工作包一則更新到主管摘要示範 | 同資料抽取待辦與依賴，學員先提判斷 | 另一段完整材料交接摘要、待辦、待決策與接手提醒 | 新產物為可行動工作交接，不是多格式重寫 |
| CH3-1 | 星河 v1 查一事實並定位來源 | 多文件組回答一題，說明採用來源 | 新文件組回答一個範圍與一個未知問題 | 從單來源定位升為跨來源證據 |
| CH3-2 | 比較 v1/v2 的交付條件 | 依來源日期判斷條款適用範圍 | 匿名變更包判斷可執行／超核准／待追問 | 不與 CH3-1 重複查單一事實 |
| PRAC3 | 只示範 Notebook/引用入口，不展示 Solo 答案 | 練追溯與來源範圍 | 另一個場地專案獨立交付證據表和待問清單 | 新專案、新決策、答案後置 |
| CH4-1 | 三分鐘計時器完整規格與狀態測試 | 改可調時間並核對上下限 | 面對新增工作／休息切換需求補測狀態 | 增加輸入範圍和狀態轉換決策 |
| CH4-2 | 24 月 CSV 計算示範保留作參照 | 手算報價及追加條件核准門檻 | 用新條件更新規則並測拒絕情況 | 保留原數學，新增業務條件 |
| CH4-3 | 24 月圖表計算核對 | 從交易列按區域彙總、解釋異常標記 | 換一個資料來源後重做分組並說出缺口 | 增加資料品質判斷與問題解讀 |
| CH4-4 | 用既有工具說明檔案保存 | 讓同伴在不同檔案位置重開與使用 | 交付含來源、版本和限制的完整檔 | 專注可復用交付，不加未驗證雲端發布 |
| PRAC4 | 一件已完整示範的工具 | 學員選一條路線，提出與示範不同的需求變更 | 自己修改、測相關案例、跑舊回歸並交接 | 同一件工具可保留；有新規則和新測試 |
| CH5-3 | 一筆分類、人工更正與核准示範 | 從新原文判斷九欄，說明更正依據 | 對含歧義的新紀錄決定覆核／補問／停止 | 增加業務判斷，T01–T07 不變 |
| PRAC5 | 原文到已核准列範例 | 人工檢查其他原文列及路由結果 | 只讓核准的新列進 ReviewedQueue 並核對草稿 | 業務分類和流程工程分開評分 |
| CH6-2 | 示範上游會議紀錄到下游通知草稿 | 共同改一個來源條件並追蹤影響 | 自己挑另一處變更，重查並留下人工檢查 | 真正做一次跨單元工作交接 |
| PRAC6 | 一張七欄卡與本機保存 | 把一個流程步驟和產物寫入卡片 | 匯出／還原並用新條件驗證交接資訊 | 卡片仍是產物，欄位內容改為工作流程 |
| CH7-1 | 從一份委託界定任務 | 同專題包辨認使用者、輸入、限制 | 提案選擇一個實際可檢驗的新條件 | 使用者需自行界定而非照抄答案 |
| CH7-2 | 文件型案例：資料→初稿→引用查核 | 從案例包選測試並指出結果差異 | 新條件影響結論時修訂、重跑並留證 | 完整答案在任務與提交初稿後才可看 |
| CH7-3 | 觀察使用者操作並找出一個可重現問題 | 將回饋分成事實錯誤／可用性／新增範圍 | 修一項可測問題並重跑原測試 | 回饋必須對應修改與重測證據 |
| PRAC7 | 完整交付包示例含材料、成品、重測和 handoff | 填表／匯出後核對來源與版本 | 交付自己的可取得作品、變更證據與接手步驟 | 表單互動維持原樣；內容下限提高 |

## Shared Copy Audit

| repeated material/copy | pages | allowed reason | action |
|---|---|---|---|
| `prompt-library.md` 20 prompts / same workshop facts | Part 1 reference and Part 2 prompt selection | 同一材料展示輸出形式有教學價值，但不能聲稱是 20 種案例 | 開頭明說單一情境；PRAC2 改用不同工作包 |
| Part 2 update packet | CH2-1、CH2-2、CH2-3、PRAC2 | 同一工作逐步形成決策摘要、核對信件、辨識附件、交接紀錄 | 每頁列明新增判斷與產物；避免完整重跑相同輸出 |
| Part 3 demo packet | CH3-1、CH3-2 | 先做定位引用，再做版本／範圍判斷 | 用不同問題；答案只出現於完成 checkpoint 後 |
| Part 7 capstone case | CH7-1、CH7-2、CH7-3、PRAC7 | 以同一專題完成提案、初版、回饋修訂和 handoff | PRAC7 最終核對完整成品；提供另一條獨立條件遷移 |
| safety / no-guess wording | 單元必要 checkpoint | 對高風險輸出是不同任務共通檢查 | 保留一行本節專屬使用方式，不複製整段口號 |

## Execution Order

### Task 1: 建立修復前備份與還原路徑

**Files:** create `_backup/2026-10-10-pre-repair/`、`_tools/restore-2026-10-10-pre-repair.sh`；內容包括本計畫所有已存在的本課 HTML、來源教案、meta、renderer、課程索引、既有素材與 `_outlines`／`_lessons` 的當前版本。新素材與新驗證檔無需預先備份。

- [x] 依本計畫 manifest 建立保留相對路徑的備份，對全站正式教案檔也先存一份課程內副本。
- [x] 還原腳本只含 manifest 中的精確路徑；不得遍歷全課程或其他課程目錄。
- [x] 執行 `bash -n _tools/restore-2026-10-10-pre-repair.sh`，逐檔比較備份與來源 SHA-256：79 個檔案，checksum mismatch 為 0。
- [x] 將初始來源與工作樹目標狀態寫入 `_repair/2026-10-10/backup-manifest.json`；備份與還原路徑核驗通過。

### Task 2: 清除 B01 矛盾並對齊 Part 6 名稱

**Files:** 上表 19 個 callout HTML；`index.html`、`CLAUDE.md`、`../../_outlines/gen-ai-36h.md`、`_repair/2026-10-09/lesson-meta.json`、`_tools/render-lessons.py`，以及 `part6/CH6-1.html`。

- [x] 依上方 19 項刪除清單逐一核對 block 內容，僅移除指定 `.callout.info` 元素；每頁必須剛好命中一次。
- [x] 將 Part 6 顯示名統一為「個人 AI 工作流程整合」，學習路徑第六項寫出上游輸入、人工決策、下游成果與條件變更後重查。
- [x] 讓 `lesson-meta.json`、renderer 的 Part 6 顯示名、課程首頁與 CLAUDE 說明一致；不改 CH6-1 正文。
- [x] 為 renderer 加入 `--evidence-output PATH` 選項，保留現有預設輸出行為；修復時明確把 evidence 寫到 `_validation/2026-10-10/render-evidence.json`，不覆寫 2026-10-09 歷史紀錄。
- [x] 執行逐頁 DOM 檢查：19 個舊 block 不存在、所有 28 頁仍有唯一 `.lesson-body`、nav URL／auth script 與備份一致。

### Task 3: 補強 Part 2 文件工作與素材

**Files:** 四份 Part 2 教案與 HTML；`assets/prompt-library.md`、`assets/START-HERE.md`；`assets/workplace-cases/part2/` 六個新素材檔。

- [x] 先完成新素材：角色聊天、現況追蹤表、正式更新、附件紀錄與教師答案；標示來源、日期、版次、已核准、尚未決定和依賴。
- [x] 在各教案為 Demo、Together、Solo 寫明素材、產物、操作、學員決策和支援程度；Solo 不先透露分類答案。
- [x] 把 PRAC2 完成物固定為一份主管可採取行動的摘要、待辦、依賴、待決策和交接提醒；不得猜未確認日期／負責人。
- [x] `prompt-library.md` 標註 20 項是相同案例的輸出參考；START-HERE 在首次使用前列檔名、用途、取得方式、備援與答案位置。
- [x] 在來源中核對每個 Markdown 素材連結都指向已新增檔案；回答中的事實能回到原始聊天、追蹤表或更新文字。
- [x] 以答案鍵逐項回查引用行、日期、狀態、依賴和未確認欄位；至少人工驗算一份 PRAC2 完成稿。

### Task 4: 補強 Part 3 跨文件證據判斷

**Files:** 三份 Part 3 教案與 HTML；`assets/START-HERE.md`；`assets/workplace-cases/part3-demo/` 五檔及 `part3-solo/` 五檔。

- [x] 先凍結文件日期、版本、核准上限 NT$22,000、報價 NT$25,000、被取代範圍和待決策項目；兩個金額的性質不得混為衝突。
- [x] 在 CH3-1 將星河 v1 保留為單一事實引用短示範，再展示一題跨來源回答和來源位置。
- [x] 在 CH3-2 不提前揭露變更答案；要求說明版本適用範圍及採用理由。
- [x] 在 PRAC3 改用不同活動專案，學員先交答案，再開核對段；區分可執行、超出核准與待追問。
- [x] 檢查素材連結與每個答案的來源錨點，核准上限、報價和新版條件可彼此獨立追溯。

### Task 5: 補強 Part 4 資料、需求變更與回歸測試

**Files:** 五份 Part 4 教案與 HTML；`assets/quote-rules.md`、`quote-test-cases.csv`、`sales-expected-results.md`、`reference-timer.html`、`reference-quote.html`、`reference-chart.html`、`START-HERE.md`；Part 4 三份新資料檔。

- [x] 建立原始交易 CSV 與資料字典，恰含一個重複交易 ID、一個缺日期、一筆退款、一筆取消；為每例明訂保留、排除或待查規則與預期總和。
- [x] 用獨立 Python 計算或手算重算清理後彙總，核對答案鍵；確認退款符號、重複去除、取消排除與缺日期待查沒有重複計入。
- [x] 更新計時器參考版支援可調工作／休息時間與合理上下限；更新報價參考版及案例支援核准門檻；更新圖表參考版支援指定分組與新資料來源。
- [x] PRAC4 仍只要求一件作品；三條路線各有對應新條件、受影響規則、至少一項新增測試和原有回歸測試。
- [x] 執行既有 JS syntax check 和指定路線的正常／邊界／保存測試。

### Task 6: 補強 Part 5 業務分類而保留 Make 工程驗收

**Files:** `CH5-3.md`、`PRAC5.md` 與兩頁 HTML；`assets/START-HERE.md`；Part 5 新原文 CSV 與分類答案鍵。

- [x] 新批次至少各含一筆多重意圖、引用舊訊息、重複來源 ID、缺必要欄位、明確一般詢問；每筆帶原始文字和可追溯 ID。
- [x] 答案鍵逐筆列主要分類、九欄值、採用原句、需補問／人工接手與「不可進 ReviewedQueue」條件。
- [x] 本次寫入清單與 renderer 均不包含既有 T01–T07／Make Blueprint／九欄流程檔；沿用工作樹目前契約核對「只有已人工核准的新列可進 ReviewedQueue，且只寫未寄出草稿」。這些既有檔案不在 79 檔修復備份內，不宣稱可做位元級前後比較。
- [x] 以表格核對所有歧義案例的分類、核准狀態及路由預期。

### Task 7: 讓 Part 6 有一條可恢復的工作交接

**Files:** `CH6-2.md`、`PRAC6.md` 與兩頁 HTML；`assets/part6-workflow-case.md`；`lesson-meta.json`；既有 PRAC6 表單只作不變性驗證。

- [x] 寫出上游會議輸入、人工狀態判斷、來源條件更新、下游通知草稿、接手說明與一項變更後需重做的檢查。
- [x] PRAC6 要求一張含新條件、核對方法與恢復路徑的流程卡；七欄 schema、local save、JSON 匯入／匯出與 `data-gen36-form` 不變。
- [x] 確認來源保留原七欄 schema，表單互動檔案不在修改清單。

### Task 8: 建立 Part 7 可示範、可獨立遷移的專題交付

**Files:** 四份 Part 7 教案與 HTML；`assets/showcase-example.html`、`assets/START-HERE.md`；`assets/capstone/` 九個素材檔。

- [x] 新專題包包含委託要求、狀態 CSV、兩版政策、會議紀錄、完整文件型解答、測試證據及答案鍵；各檔標明版本與來源。
- [x] 完整示範依序展示材料→初稿→逐來源核對→條件變更→修訂→重測→交接；任務指令後才顯示教師核對段。
- [x] CH7-2 各作品路線採可觀察的適用測試；每條路線都處理一項會改變結果的新條件，不要求多工具或公開部署。
- [x] PRAC7 的成功門檻為可取得的成果、一項處理過的變更、核對證據、接手者使用說明和修訂狀態；表單欄位／匯出行為不變。
- [x] 對完成範例逐條核對引用、變更理由、重測結果與交接步驟。

### Task 9: 同步正式教案、完整驗證並交付修復報告

**Files:** 只同步 Scope 列出的 20 份 Markdown 到 `../../_lessons/gen-ai-36h/`；新建 `_validation/2026-10-10/` 證據；新建 `_repair/2026-10-10/REPAIR-REPORT.md`。

- [x] 逐一比較本地教案與 20 份正式 mirror；只有在本地內容審查通過後，精確複製同名檔，並對來源／目的檔計算 SHA-256。
- [x] 建立 `_validation/2026-10-10/` 後執行一次指定單元 renderer，將所有受影響 HTML 與 `CH6-1` 傳入同一命令，輸出至 `_validation/2026-10-10/render-evidence.json`；修復 renderer 輸出或內容時，仍以相同完整單元清單重跑。
- [x] renderer 單元清單：`CH2-1 CH2-2 CH2-3 PRAC2 CH3-1 CH3-2 PRAC3 CH4-1 CH4-2 CH4-3 CH4-4 PRAC4 CH5-3 PRAC5 CH6-1 CH6-2 PRAC6 CH7-1 CH7-2 CH7-3 PRAC7`。
- [x] 確認 `python3 _tools/render-lessons.py --help` 顯示 `--evidence-output` 後，執行：

  ```bash
  python3 _tools/render-lessons.py --evidence-output _validation/2026-10-10/render-evidence.json CH2-1 CH2-2 CH2-3 PRAC2 CH3-1 CH3-2 PRAC3 CH4-1 CH4-2 CH4-3 CH4-4 PRAC4 CH5-3 PRAC5 CH6-1 CH6-2 PRAC6 CH7-1 CH7-2 CH7-3 PRAC7
  ```

- [x] 執行 `python3 _tools/verify-course.py`；處理 28 頁來源保真、素材連結、原始 auth/nav、首頁 28 卡和程式語法錯誤。
- [x] 執行 `python3 ../../docs/lint-page.py "$PWD" --summary` 與 `python3 ../../docs/audit-course-substance.py gen-ai-36h`；記錄實際頁數、blocker、error、warning 和 semantic verdict，不由靜態通過推導 HUMAN_READY。
- [x] 逐頁重做本計畫的 Activity Identity／Shared Copy audit，檢查答案是否提前洩漏、舊要求是否殘留、工作資料是否可取得、答案是否可追溯，並記錄作者自審。
- [x] 在 `_validation/2026-10-10/` 記錄真實執行的測試、雜湊與未完成驗項；真人跟做、NotebookLM／Claude／Make 目標帳號實跑、瀏覽器煙霧測試若未執行就標 `PENDING`。
- [x] `git diff --check`；只檢視本計畫目標路徑。收到使用者 push 指示後，改在以最新 `origin/main` 為基線的隔離分支顯式 staging 本課修復清單，不納入其他課程或本地既有提交。
- [x] 寫 `_repair/2026-10-10/REPAIR-REPORT.md`，列出變更、刪除清單結果、lint／reviewer／validator／asset／restore 檢查與剩餘待真人實測項目。

## 驗收門檻

- 19 個舊契約區塊只按明列清單移除；19 頁不再有矛盾或首次出現才要求、且正文未教的 learner-facing 任務。
- 核心教材有可取得的工作資料、明確起始狀態、決策步驟、可核對答案、錯誤修復與新條件 Solo；新案例不是單純替舊 prompt 換名稱。
- 日期、金額、分類、資料品質和測試答案可由引用或獨立計算重現；答案只在學員完成對應動作後出現。
- PRAC1／2／4／6／7 的必做數量分別維持一項文字任務、一份工作交接、一件工具、一條可恢復流程卡、一件修訂後作品。
- Make T01–T07 流程檔與 PRAC6／7 表單不在本次寫入清單；程式／DOM simulation 測試通過，頁面 nav／gate 保真檢查通過。未納入修復備份的既有檔案不宣稱位元級前後一致；瀏覽器互動仍 PENDING。
- 28 頁 source-to-HTML 保真、所有本地連結、結構與 lint 結果有紀錄；未實跑的人工／平台驗證明示 `PENDING`。
- 還原腳本語法正確、manifest 檔案數與校驗碼一致；腳本不會觸及任何未列檔案。

## 風險與限制

- 本工作樹含其他課程和全站來源的未提交修改。備份、渲染、mirror 同步和驗證都必須限定到本計畫清單；全站索引／sitemap 不在本次 scope。
- `_outlines/gen-ai-36h.md` 與 `_lessons/gen-ai-36h/` 位於課程目錄外；已依授權精確更新課綱並同步 20 份同名教案，來源／mirror SHA-256 全數相同。
- 假案例可提高情境判斷需求，但不能證明真人遷移能力；需另做真人跟做與平台實跑後才能提高驗收狀態。

## 自我檢查

- Spec coverage：B01、M01–M09、Part 2–7 素材與活動、素材索引、Part 6 標題、Part 7 完整示範、19 項刪除清單、備份／還原、來源同步和驗收均有對應任務。
- Placeholder scan：沒有待填欄位或未定義的實作步驟；活動內容、資料形態、答案責任與驗證均已指明。
- Scope check：此為同一既有課程的相互依賴修復，按教案來源分批交付；沒有重構其他課程或全站模板。
- Execution method：使用本工作階段原生逐批執行；先等使用者核准本計畫，且 Task 1 backup／restore 通過後才改教材。

## Approval

**狀態：使用者已核准；Task 1–9 已完成教材修復、正式來源同步與靜態／程式驗證。依後續 push 指示，正在最新 `origin/main` 上建立隔離修復分支。瀏覽器 smoke、真人跟做與目標平台實跑仍為 PENDING，不宣告 HUMAN_READY。** 設計與計畫核准日：2026-10-10。依 Task 1 → Task 9 順序執行。
