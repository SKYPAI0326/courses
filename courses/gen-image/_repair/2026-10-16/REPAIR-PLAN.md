# Gen Image 2026 Current-Practice Repair Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修正 `gen-image` 的教材缺檔、AI 自我驗收、權利風險與 2026-10 圖像生成工作流缺口，使學員能取得材料、完成練習、用可觀測證據驗收並形成安全的商用交付包。

**Architecture:** 採 source-first：先修 outline／style guide 與真實下載資產，再更新 13 份 lesson source，最後同步 41 個 learner-facing HTML。平台資訊改為「長效能力條件 + 開課日檢查卡」，商用與品質要求集中在可執行 release gate，各單元只保留當下需要的證據與修復路徑。

**Tech Stack:** Markdown 教案與下載資產、單檔 HTML/CSS/JS、既有 Python lint／substance／structure validators、browser smoke test。

**Spec:** `courses/gen-image/_repair/2026-10-16/SCAN.md`

## Global Constraints

- 維持 8 小時課程、既有 6 個 module 導覽與「參考 → 解構 → 再造」主軸；不新增頂層章節。
- `task_scope = content-change`；只修改計畫明列的文字節點與教學區塊，保留既有 wrapper、class、導航、gate 與圖片路徑。
- 先備份再修；沒有 `_backup/2026-10-16-pre-repair/` 與可通過 `bash -n` 的 restore script 就停止。
- 正式 HTML 前先修 `_outlines`、`_lessons` 與 learner assets；執行時若沒有父層寫入權限，標記 `BLOCK`，不得只改 HTML。
- learner-facing 資產以 `courses/gen-image/assets/downloads/` 為唯一可下載 SSOT；不再讓學員依賴不存在或不公開的 `_sources/gen-image/`。
- AI 自檢只提供待核對線索；通過必須有人工判斷與可觀測證據。
- 不宣稱任何平台、方案或素材「保證無侵權」「版權乾淨」或「可商用」；逐案查輸入權利、條款、方案與輸出。
- 不下載未授權的 IG／Pinterest／電商圖片上傳模型；人物素材須有同意與資料處理路徑。
- 不以 metadata bump 代替內容 refresh；全頁核對完成後才更新 `platform_version`／`built-at`。
- 不重排全頁、不順手美化；每批 1–3 頁，通過結構與內容檢查後再進下一批。
- mixed worktree 僅顯式 staging；未獲授權不 commit／push。

## Review Focus

1. 缺檔 fallback：所有正文提到的下載檔必須存在、可點擊、第一次使用前說明用途；任一缺檔維持 BLOCK。
2. 模型不遵循指令：選區外改動、張數不足、文字／色票／字型不可靠時，學員仍有可觀測檢查與安全停止路徑。
3. 權利不明素材：來源、授權、人物同意或客戶資料任一為 UNKNOWN 時，練習改用課程 reference pack，不得上傳原素材。
4. 平台漂移或服務不可用：課堂不依賴固定秒數、日額度或單一方案；提供等待、切換與預製 fallback。
5. 視覺交付只有圖片：每個 release candidate 必須同時具備 alt、純文字文案、文字校稿、對比檢查與 provenance 記錄。

---

## Approved Repair Design Pending User Review

### 範圍決策

- 一次處理審查的 3 BLOCKER、7 MAJOR、3 MINOR。
- 以替換過時或錯誤內容取得教學時間；不在 8 小時課上疊加新章。
- `CH4-1` 承接 reference-first 核心示範；`CH5-1` 承接商用 release gate；人物與資訊圖規範留在對應 CH6 頁。
- 既有 62 張圖片可保留作「參考輸出」，不得宣稱標準答案；只有來源／權利狀態為 READY 的圖片才能進 PRAC3 reference pack。

### 明列替換／移除

- 移除或改寫：「不用自己的眼睛判斷」「以 AI 自檢為主要依據」「AI 自檢較客觀」。
- 移除或改寫：「版權保險」「版權乾淨」「無版權負擔」「重製後即可商用」。
- 移除 PRAC3 的「下載 IG／Pinterest／電商圖片再上傳」必要路徑；搜尋僅保留為不下載、不上傳的觀察活動。
- 移除正文中的固定日額度、固定月費、固定點數與 20–30 秒保證；移到開課日檢查卡或改為查核步驟。
- 將 MUJI／Apple／Nike 等品牌捷徑改成可觀測風格屬性；保留品牌名時只作邊界案例。

## Target File Map

### Create learner assets

- `assets/downloads/README.md`：入口、用途、使用時機、備援與版本日期。
- `assets/downloads/10-industries-brief-library.md`
- `assets/downloads/8-version-library.md`
- `assets/downloads/8-prompt-examples.md`
- `assets/downloads/prompt-templates.md`
- `assets/downloads/anti-patterns.md`
- `assets/downloads/brand-dna-template.md`
- `assets/downloads/7-brand-style-system.md`
- `assets/downloads/l2-skeleton-library.md`
- `assets/downloads/skeleton-quick-card.html`
- `assets/downloads/skeleton-quick-card.pdf`
- `assets/downloads/reference-pack-manifest.md`
- `assets/downloads/human-qa-and-release-gate.md`
- `assets/downloads/platform-check-card.md`

### Modify canonical course sources

- `../../_outlines/gen-image.md`
- `../../_outlines/gen-image.style-guide.md`
- `../../_lessons/gen-image/*.md`（13 份 metadata；依下列 task 修改內容）

### Modify learner-facing HTML

- Core content：`CH1-1.html`、`CH1-2.html`、`CH2-1.html`、`CH2-2.html`、`PRAC2.html`、`CH3-1.html`、`PRAC3.html`、`CH4-1.html`、`CH4-3.html`、`PRAC4.html`、`CH5-1.html`
- Navigation／promise：`index.html`、`module1.html`～`module6.html`
- Targeted CH6：`CH6-1.html`、`CH6-A2.html`、`CH6-B5.html`、`CH6-C1.html`～`CH6-C4.html`、`CH6-supplement-typography.html`
- Version review：其餘 CH6 頁；確認內容後更新 metadata，不做盲目全域替換。

---

### Task 0: Backup and Frozen Baseline

**Files:**
- Create: `_backup/2026-10-16-pre-repair/`
- Create: `_tools/restore-2026-10-16-pre-repair.sh`
- Create: `_repair/2026-10-16/baseline/`

**Produces:** 可還原的 scope snapshot、可見文字／DOM／關鍵字／metadata 基線。

- [ ] 依 Target File Map 複製預計修改檔，保留相對路徑；父層 outline／lesson 也納入備份。
- [ ] 建立 restore script，只還原本計畫 scope，不碰其他課程或 unrelated changes。
- [ ] 執行 `bash -n courses/gen-image/_tools/restore-2026-10-16-pre-repair.sh`；Expected：exit 0。
- [ ] 保存 41 頁 footer metadata、核心 11 頁可見文字與 DOM 結構摘要。
- [ ] 執行 `git status --short` 並把既有 unrelated changes 記入 baseline；後續不得 stage 它們。

### Task 1: Deliver Real Learner Assets

**Files:** Create the 14 files under `assets/downloads/` listed above; modify outline、style guide、`CH2-1.md`、`CH2-2.md`、`PRAC2.md`、`CH3-1.md`、`PRAC3.md`、`CH4-1.md`～`CH5-1.md` references.

**Produces:** 每個教材引用都有真實、可下載、可單獨理解的檔案。

- [ ] 先跑存在性紅燈：`test -f courses/gen-image/assets/downloads/10-industries-brief-library.md`；Expected：目前 FAIL。
- [ ] 建立 `README.md`，逐檔列出檔名、格式、用途、第一次使用單元、備援與版本日期。
- [ ] 補齊既有正文已引用的 8 個核心教材；每份含完整模板／例子／使用條件，不以需求清單代替成品。
- [ ] 將 5 種 L2 骨架放在獨立 `l2-skeleton-library.md`；8 種用途版型維持 `8-version-library.md`，不得混成同一套分類。
- [ ] 以 `skeleton-quick-card.html` 作 A4 雙面印刷真相源，依 `course-pdf` 產出並逐頁核對 `skeleton-quick-card.pdf`；index 與 CH2-1 提供下載入口。
- [ ] `reference-pack-manifest.md` 為每張候選圖記錄檔名、來源、作者／生成者、日期、授權／同意、允許用途、provenance 狀態；任一 UNKNOWN 不得標 READY。
- [ ] 先稽核現有 62 張圖片；若不足 5 張可標 READY，停止 reference pack 製作並等待使用者授權重新產製替代圖，不自行生成或補寫來源。
- [ ] 更新 outline／lessons 的路徑為 `courses/gen-image/assets/downloads/...`，HTML 使用可點擊的 `assets/downloads/...`。
- [ ] 執行 `rg -n '_sources/gen-image|10-industries-brief-library\.md|prompt-templates\.md' _outlines/gen-image* _lessons/gen-image courses/gen-image`；Expected：不再有不可解析的 `_sources/gen-image`，每個 learner-facing 引用有 `href` 或完整內嵌內容。
- [ ] 重新做 PRAC2 入口測試：30 秒內找到業種庫、選擇一題、知道產出與 fallback。

### Task 2: Repair the Canonical Contract and Course Promise

**Files:** Modify `../../_outlines/gen-image.md`、`../../_outlines/gen-image.style-guide.md` and all 13 lesson frontmatters.

**Produces:** 長效、可驗收且不以錯誤權利保證為前提的課程契約。

- [ ] 將 Outcome 3 改為「人類依清單與可觀測證據驗收，AI 提供待核對線索」；Outcome 4／5 加入 reference fidelity 與第三方辨識證據。
- [ ] 把「不備固定示範圖」改成「不提供標準答案圖」：允許有來源紀錄的參考輸出與 fallback，明示輸出可不同。
- [ ] 將學員自蒐規則改為「只觀察不下載／不上傳」；實際圖生圖練習使用自有、教師自製或 reference pack 素材。
- [ ] 把 Firefly／Canva 從「保險」改為工具選項；商用判定交給 release gate。
- [ ] 全部 13 lesson `platform_version` 改為當次驗證字串，正文採能力描述；具體型號只放 platform check card。
- [ ] 記錄 8 小時重新配時：刪除平台價格講解與重複 AI 自檢所得時間，移給 reference-first 與 release gate；總時數不增加。
- [ ] Review checkpoint：對照 SCAN 的 13 個 issue，確認每項都有 canonical owner。

### Task 3: Replace Generator Self-Judging with Human QA

**Files:** Modify `CH1-1.md`、`CH3-1.md`、`CH4-1.md`、`CH4-3.md`、`PRAC4.md`、`CH5-1.md` and matching HTML; create/update `human-qa-and-release-gate.md`.

**Produces:** AI 自評、人工判斷與工具證據三者責任清楚；通過條件可被第三人重做。

- [ ] 先跑語句紅燈：`rg -n '不用自己的眼睛|以 AI 自檢為主要依據|AI 自檢.*較客觀' _lessons/gen-image courses/gen-image`；Expected：目前有命中。
- [ ] 定義三層 QA：AI 列待查項目；學員目視判斷；取色器、文字讀取、尺寸、安全區、縮圖與第三人盲評提供證據。
- [ ] A／B／C 清單逐項標記「誰判、用什麼證據、失敗回哪一階段」；AI 無法可靠證明實際字型或精確 hex。
- [ ] 把 CH3-1、CH4-3 的數字通過門檻改成「必要項全過 + 可選項記錄」，避免模型自己打分即放行。
- [ ] PRAC4 與 CH5-1 增加一份實際 QA 紀錄作交付物。
- [ ] 重跑紅燈命令；Expected：0 命中，且 `rg -n '人工|可觀測|取色|第三人'` 可定位新證據。

### Task 4: Install Rights, Consent, Privacy, and Provenance Gates

**Files:** Modify outline／style guide、`CH1-2.md`、`CH2-2.md`、`PRAC3.md`、`CH4-1.md`、`CH5-1.md` and matching HTML; modify `module5.html`、`CH6-C4.html`; update release gate and reference manifest.

**Produces:** 每份輸入與輸出都能判斷是否可上傳、可練習、可交付、需揭露或必須停止。

- [ ] 先跑禁語紅燈：`rg -n '版權保險|版權乾淨|無版權負擔' _outlines _lessons/gen-image courses/gen-image`；Expected：目前有命中。
- [ ] 建立商用五關：輸入權利／人物同意、平台條款與方案、素材個別授權、相似性／商標／trade dress、揭露與證據留存。
- [ ] PRAC3 改用 READY reference pack；保留搜尋活動時明示只觀察、不下載、不上傳、不重製。
- [ ] 人物 gate 加入：可辨識人物同意、未成年人停止或升級審查、公共人物／冒充／深偽禁用、客戶檔案去識別、帳號資料控制與刪除。
- [ ] provenance 記錄包含模型／版本、日期、prompt、reference、授權、人工修改、C2PA／Content Credentials／SynthID 檢查與揭露文字；明確區分畫面文字與 metadata。
- [ ] Firefly／Canva 說法改為條件式；附官方條款連結與「非法律保證」。
- [ ] 重跑禁語紅燈；Expected：0 命中。以一個「權利未知」案例驗證流程必須停止並切換 reference pack。

### Task 5: Refresh Platforms Without Reintroducing Drift

**Files:** Modify outline、style guide、all lesson frontmatters、`CH1-2`、所有含舊模型／配額／價格／時間保證的 HTML、`platform-check-card.md`.

**Produces:** 正文長效，開課日卡片承接易變資訊，服務失敗不會卡死課程。

- [ ] 先跑漂移紅燈：`rg -n 'GPT-image-1|GPT-image-2|Gemini Advanced|Banana Pro|30.?50 張|25 積分|20.?30 秒' _outlines _lessons/gen-image courses/gen-image`；保存命中基線。
- [ ] `platform-check-card.md` 設欄位：查核日期、方案名稱、可否上傳 reference、可否局部編修、張數／額度、資料控制、生成等待、fallback。
- [ ] CH1-2 改成依能力與帳號條件決策，不推薦固定雙訂閱，也不把月費寫死在正文。
- [ ] PRAC 的活動時間保留；模型等待改成可變，逾時分支為「等候／切換／使用預製 fallback」，不承諾秒數。
- [ ] CH6 JSON／API 片段逐頁對照官方文件；只改已確認漂移的 model／endpoint，不做推測性全域替換。
- [ ] 內容與平台重跑完成後才更新 41 頁 metadata；built-at 使用實際驗證日。
- [ ] 重跑漂移紅燈；Expected：舊名稱只可存在於有日期的歷史說明或來源引用，不能作操作指令與現行建議。

### Task 6: Add a Reference-First, Local-Edit Workflow

**Files:** Modify `CH4-1.md`、`CH4-3.md`、`PRAC4.md`、`CH5-1.md` and matching HTML; update prompt／brand assets.

**Produces:** 一個完整必修鏈：合法 reference → 角色分工 → 初稿 → 局部修改 → fidelity QA → 修訂紀錄。

- [ ] CH4-1 將 reference 分成商品、角色、構圖、品牌四種角色；限制每張只承擔清楚用途。
- [ ] 示範多 reference 後，要求學員說出哪些元素必須保留、可以變、禁止帶入。
- [ ] 加入選區／遮罩或文字指定局部修改；驗收選區外是否被改動。
- [ ] CH4-3／PRAC4 以 reference fidelity、identity、商品外觀、品牌 DNA、構圖五項作系列檢查。
- [ ] CH5-1 的交付包加入 reference manifest 與修改歷程；無紀錄不得進 release gate。
- [ ] 用一個「局部修改越界」失敗案例走完現象、回修位置、重跑起點與安全停止。

### Task 7: Add Accessibility and Bias Evidence

**Files:** Modify `CH5-1.md`／HTML、`CH6-B5.html`、`CH6-C1.html`～`CH6-C4.html`、`CH6-supplement-typography.html`; update release gate.

**Produces:** 商業圖同時具有可讀文字與可檢查的表示風險。

- [ ] release gate 要求 alt、純文字文案、圖片文字逐字校稿、色彩對比與純圖失效備援。
- [ ] C1～C3 每種資訊圖列出同步交付的完整文字版；B5 檢查 banner 關鍵文字不可只存在圖片中。
- [ ] C4 加入人物表示矩陣、成對 prompt 測試與人類複核；敏感屬性只有與 brief 直接相關且取得同意才可使用。
- [ ] 中文文字能力改為「已改善但仍需校稿」；精確品牌字型、價格、法規文字維持後製。
- [ ] 服務與字型價格改成官方連結 + 開課日查核，不留固定月費。
- [ ] 以一個人物刻板印象案例與一個純圖資訊圖案例驗證 gate 會阻擋交付。

### Task 8: Render Sources into HTML Without Breaking Structure

**Files:** All learner-facing files listed in Target File Map.

**Produces:** lesson source 與 HTML 教學證據一致，DOM／導覽／RWD 不退化。

- [ ] 每批先列允許變更文字清單與目標節點父鏈；使用 DOM parser 定位 `.lesson-body`，禁止第一個字串／全域 regex 插入。
- [ ] 批次順序：B1 資產頁 → B2 QA 頁 → B3/M3/M4 權利頁 → M1/M2 平台與 reference → M6/M7 CH6 → MINOR。
- [ ] 每批 1–3 頁跑 `validate-course-structure.py`、`lint-page.py --summary --v3-soft`、`audit-course-substance.py --page` 與目標 diff。
- [ ] index／module 只更新真實承諾與下載入口；不把內部治理清單整段搬給學員。
- [ ] 更新所有下載連結並跑 link audit；任一 404 或裸檔名維持 BLOCK。
- [ ] 代表頁 `PRAC2`、`CH3-1`、`CH4-1`、`CH5-1`、`CH6-C4` 做 1440／390／430 px browser smoke，檢查水平捲軸、sticky header、表格與折疊區。

### Task 9: Independent Verification and Release Decision

**Files:** Create `_repair/2026-10-16/REPAIR-REPORT.md`; refresh course-validator evidence for changed sources and pages.

**Produces:** 可重現的修復證據與明確 release status。

- [ ] 執行 `python3 docs/lint-page.py courses/gen-image --summary --v3-soft`；Expected：BLOCKER 0、ERROR 0，新增 WARN 0。
- [ ] 執行 `python3 docs/audit-course-substance.py gen-image`；Expected：machine checks通過，但不據此宣告 learner-ready。
- [ ] 執行 `python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py --batch gen-image`；Expected：所有頁結構通過。
- [ ] 執行 `git diff --check` 與 scoped diff；Expected：無 whitespace error、wrapper 大段漂移或非 scope 變更。
- [ ] 重跑 Activity Identity Audit 與 Shared Copy Audit；Expected：Together 有新判斷／支援遞減，共用安全文案集中且未擠壓實作。
- [ ] 由 fresh reviewer 依 course-reviewer 重審 13 個 issues；Expected：B1–B3 關閉，M1–M7 有頁面證據，MINOR 無誤導殘留。
- [ ] 做 cold follow-along：`PRAC2 → CH3-1 → PRAC3 → CH4-1 → CH5-1`，使用乾淨帳號與 learner-facing 連結；記錄每個 stage 的輸入、結果、檢查與修復。
- [ ] 做平台重跑至少 ChatGPT 與 Gemini 各一路；無真人證據時最高只能標 `MACHINE_READY_PENDING_HUMAN`。
- [ ] 產出 `REPAIR-REPORT.md`，列 changed files、驗證命令／結果、剩餘 owner、backup 與 restore path。

## Execution Order and Gates

1. 使用者核准本計畫。
2. Task 0 backup；Gate：restore script 通過。
3. Task 1–2 資產與 canonical contract；Gate：所有 learner asset 可取得。
4. Task 3–4 QA 與權利；Gate：三個 BLOCKER 關閉。
5. Task 5–7 current workflow、a11y、bias；Gate：7 個 MAJOR 有可觀察證據。
6. Task 8 HTML fidelity；Gate：structure／lint／RWD／links 通過。
7. Task 9 reviewer、validator、cold follow-along；Gate：依證據標示 release status。

## User Decision Required Before Task 1 Completes

- 若現有 62 張圖片不足 5 張能提供可核實的作者／生成來源、日期、授權與人物同意紀錄，是否允許另行產製一套只供本課使用的 reference pack？未取得回答前，Task 1 可完成其他文字教材，但 B1／B3 與 PRAC3 保持 `BLOCK`。

## Plan Self-Review

- Spec coverage：13 個 reviewer issues 均有 task owner；B1→Task 1、B2→Task 3、B3→Task 4、M1→Task 5、M2→Task 6、M3／M4→Task 4、M5→Task 4/8、M6／M7→Task 7、MINOR→Task 5/7。
- Scope control：保留 8 小時與既有導航；新增內容由刪除過時價格比較、錯誤 AI 自評與重複安全提醒取得空間。
- Source fidelity：outline／style guide／lessons 先行，HTML 不臨場發明事實。
- Recovery：未建立 backup + restore 前不得進 content-change。
- Release semantics：lint 與 machine checks 不代表 learner-ready；冷跟做與平台重跑分開記錄。
