# Gemini AI 課程路線同步實作計畫

> **For agentic workers:** 使用者選擇 Native 後，必須依 `superpowers:executing-plans` 逐項執行；若選擇 Subagent-driven，改用 `superpowers:subagent-driven-development`。每個任務完成後先驗證，再進下一項。

**Goal:** 將正式路線資料與課程入口同步到已核准的五階段設計：7 個課堂核心單元、32 個課後補充單元、1 個不遷入新版的歷史單元，保留舊頁全文與來源。

**Architecture:** `_source/lesson-map.json` 是核心路線的機器可讀清單，依序列出七個核心頁；大綱、教案與完整課程地圖說明學習目的、補充去向和排除理由。`index.html` 及七個核心頁的前後站導覽與清單一致，驗證器從 manifest 讀取路線長度，避免再寫死 10 站。

**Tech Stack:** Markdown、JSON、HTML、Python、Node.js／Playwright；沿用現有工具，不新增套件。

**Spec:** `_repair/2026-10-07/STAGE3-COURSE-ROUTE-SPEC.md`

## Global Constraints

- 核心路線順序固定為 `part1/CH1-1.html`、`part1/CH1-2.html`、`part1/CH1-3.html`、`part2/CH2-1.html`、`part2/PRAC2-1.html`、`part4/CH4-1.html`、`part4/PRAC4-3.html`。
- 舊教材分流數為 7 個核心、32 個補充、1 個不遷入新版；總數 40。`part2/PRAC2-2.html` 保留歷史檔案，不列新版課程入口。
- 六小時暫按 360 分鐘教學時間計算，不含休息；此為規劃值，未經真人試教。
- 核心工作案例暫定活動預算工具；估算 26,000 元、實支 27,800 元、較估算增加 1,800 元、核定上限 30,000 元時餘額 2,200 元。
- 貪食蛇只作 CH1-1 趣味小型範例；本階段不同步案例教學內容，也不宣稱其提示詞已由授課平台成功生成。只有頁面路線角色變更時，才修正必要的路線身份文字。
- 任何舊單元從核心移到補充時，保留頁面與完整正文；不得折疊、刪除或以摘要取代正文。唯一例外是使用者已決定不遷入新版的時區單元：從新版目錄移除連結，但保留原始檔。
- 修改既有檔案前，先完成具雜湊清單的備份和可執行還原腳本；不得使用 `git add -A`。
- 本階段不改全站共用 `search-index.json` 或 sitemap，不 push，不宣稱課程可授課或學員能獨立完成。

## Review Focus

- 核心清單從 10 站變成 7 站時，首頁清單、進度數字、頁面前後站和測試必須使用同一順序；以解析 JSON／HTML 後比對完整頁面清單與七站導覽驗證。
- 3 個移出核心的頁面 `part3/PRAC3-3.html`、`part6/CH6-1.html`、`part6/PRAC6-1.html` 仍須列在補充教材且可讀；以首頁卡片和實際檔案檢查角色、連結及正文保留。
- `part2/PRAC2-2.html` 不應出現在新版首頁目錄，但歷史檔不得刪除；以首頁 href 集合和檔案存在檢查。
- 核心路線跨 Part 1、2、4，前後站不得仍跳往已移至補充的 KPI 或 AI 交辦；以每頁 `.lesson-nav` 的 prev／next href 與 manifest 順序逐項比對。
- 課程根目錄有其他未提交工作；搜尋索引與 sitemap 不能覆寫其他課程資料；本階段驗證工作樹差異只涉及本計畫明列檔案，並將全站 ops 更新留到頁型試作驗收後。

---

## 範圍盤點

目前 `lesson-map.json` 與首頁都是 10 站；頁面角色統計為 10 核心、27 延伸、3 參考。新的分流會把 3 個原核心頁轉為補充、從新版目錄移除 PRAC2-2，形成 7 核心、32 補充和 1 個保留於歷史來源的頁面。`_tools/README.md` 說明 `build-lessons.py`、`apply-repair.py` 是一次性製作腳本，不作日常重建入口；本計畫不執行這些腳本，避免它們重新寫回 10 站。

本計畫只同步路線、課程入口、必要的頁面角色／導覽和路線驗證器。課堂內容頁稍後依「頁型試作」階段另行重寫；不因路線同步而把新設計宣稱為已出現在學員頁。

## 檔案責任

- `_source/OUTLINE.md`：課程五階段、360 分鐘主線、核心／補充分流摘要。
- `_source/LESSON-PLANS.md`：七個核心單元的目的與銜接；保留三個移出核心頁的完整教案摘要，標示為補充。
- `_source/CURRICULUM-MAP.md`：40 個舊頁的逐頁去向、前置條件、產物、限制；清楚區分「補充」與「不遷入」。
- `_source/lesson-map.json`：七個核心頁的順序、正式標題、短說明和學習成果。
- `index.html`：七站必修清單、完成數、39 個新版可瀏覽頁面及角色標籤；PRAC2-2 不連入新版目錄。
- 七個核心頁 HTML：調整 `.lesson-nav` 前後站 href／標籤；更新最後一站 footer 的總站數；CH1-3 的頁面標題與社群中繼資料須對齊 manifest 的正式標題；不改其他 `.lesson-body` 教學內容。
- 三個移出核心頁 HTML：只將 `.lesson-hero` 的路線角色由 `core` 改為既有的補充角色值；另將 CH6-1 中「必修只測」修成補充案例定位，其餘正文與案例提示詞不改。
- `_tools/verify-static.py`、`_tools/verify-browser.cjs`、`_tools/README.md`：移除「10 站」和不存在的 `#core-route-banner` 假設，讓驗證依 manifest 檢查導覽；輸出寫入本次日期資料夾並略過共享 ops 比對。
- `_repair/2026-10-07/REPAIR-REPORT.md`：記錄變更、驗證、尚待頁型試作的項目和還原位置。

## Scope / Risk / Activity Identity

- slug：`gemini-ai`
- 範圍：路線文件、課程首頁、七個核心頁導覽與總站數、CH1-3 頁面身份標題、三個移出核心頁角色、CH6-1 一句路線身份文案及路線驗證器；不修改其他教學正文與素材內容。
- 近期開課：未知；備份與還原腳本必須完成。
- 發布 BLOCKER：頁型試作尚未完成前，不 push 新版路線供學員使用。六小時是否含休息、這梯學員的工作分布及平台帳號可用性仍需後續確認。
- 內容風險：活動預算主案例依一般行政情境推薦；若班級以業務報價為主，須在頁型試作前回到使用者確認，不可自行替換計價案例。

| 單元 | 角色 | 素材 | 產物 | 學員判斷／新增認知工作 |
|---|---|---|---|---|
| CH1-1 | Demo＋初次跟做 | 完整貪食蛇提示詞、既有遊戲畫面 | 可開啟遊戲及一項修改前後差異 | 白話描述能生成單檔應用；選一項有意義的修改，不研究遊戲演算法 |
| CH1-2 | Together | 貪食蛇提示詞及黃金公式 | 一份能解釋各條件作用的提示詞拆解 | 判斷用途、輸入、規則、例外和交付限制各自解決什麼缺口 |
| CH1-3 | Together／比較 | 單檔工具、計算函數、多條件規則提示詞 | 三種需求類型的規格比較 | 判斷需求中的輸入、公式、條件、例外與輸出；不是重做三套工具 |
| CH2-1 | Demo | `budget-normal.csv` 與已知答案 | 預算計算紀錄 | 區分估算差額和核定餘額 |
| PRAC2-1 | Together | 正常、缺值／負值、移轉 CSV；預算完整提示詞與答案 | 可查核的預算工具和工作報表 | 按明確規則解讀輸入並說明哪些資料不能直接接受 |
| CH4-1 | Check | 已產生成品、資料與 README | 可重開、可交接的成果包 | 確認下次能找到工具、資料、指令和使用說明 |
| PRAC4-3 | Solo | 同一預算工具及一項自選工作變更 | 修改版本、原測試與新測試結果 | 預判修改影響，修復後重新跑回歸，獨立交付 |

| 共用內容 | 涉及位置 | 保留理由 | 處理方式 |
|---|---|---|---|
| 五階段與七站路線短摘要 | OUTLINE、LESSON-PLANS、CURRICULUM-MAP、index | 每份文件需有足夠上下文才能獨立導航 | 保留各自必要摘要；不複製整段教學正文或完整提示詞 |
| 單檔工具規格與完整提示詞標準 | 設計契約及 CH1／補充案例頁 | 需在源頭定義一次，案例內按用途完整實例化 | 契約保留通則；頁面放自己的完整提示詞，不以「沿用上例」省略 |

## Execution Order

### Task 1：建立本次範圍備份與還原腳本

**Files:**
- Create: `_backup/2026-10-07-stage3-route-pre-sync/`，保留 `_source/`、`index.html`、10 個目前核心／移出核心頁、兩支 verifier 和 `_tools/README.md` 的相對路徑。
- Create: `_tools/restore-2026-10-07-stage3-route-pre-sync.sh`
- Create: `_backup/2026-10-07-stage3-route-pre-sync/SHA256SUMS`

**Interfaces:**
- Consumes: 本計畫「檔案責任」列出的現行檔案。
- Produces: 可將該範圍還原到修改前內容的腳本及每檔 SHA-256 基準。

- [ ] **Step 1: 建立備份目錄並複製列明檔案**

  使用 `mkdir -p` 建立備份目錄；以 `cp --parents` 不可用的 macOS 環境為前提，逐檔建立目的端父目錄後複製，保留相對路徑。

- [ ] **Step 2: 記錄備份雜湊**

  對備份目錄內每個檔案執行 `shasum -a 256`，輸出到 `SHA256SUMS`；確認路線文件、入口及 10 個 HTML 頁都在清單中。

- [ ] **Step 3: 建立還原腳本並檢查語法**

  腳本以自身位置推導課程根目錄，逐一從備份相對路徑複製回原位置；執行 `bash -n _tools/restore-2026-10-07-stage3-route-pre-sync.sh`，並以備份檔重新計算 SHA-256 比對 `SHA256SUMS`。

### Task 2：同步正式課程設計來源

**Files:**
- Modify: `_source/OUTLINE.md`
- Modify: `_source/LESSON-PLANS.md`
- Modify: `_source/CURRICULUM-MAP.md`
- Modify: `_source/lesson-map.json`

**Interfaces:**
- Consumes: 已核准規格中的五階段、時間、40 頁分流表和七站核心順序。
- Produces: 四份內容一致的路線來源；`lesson-map.json` 僅含七個核心頁，順序與規格一致。

- [ ] **Step 1: 將大綱改成五階段路線**

  在 `OUTLINE.md` 寫明 360 分鐘（休息另計）的五階段、七個核心頁和一個預算工作案例；標示 32 個補充頁與 1 個不遷入新版頁。將六小時和行政班級適配標成規劃假設，不寫成試教結論。

- [ ] **Step 2: 重排教案索引並保留移出頁摘要**

  `LESSON-PLANS.md` 的核心路徑只列 CH1-1、CH1-2、CH1-3、CH2-1、PRAC2-1、CH4-1、PRAC4-3。將 PRAC3-3、CH6-1、PRAC6-1 的既有摘要移到「補充案例」段落，不刪正文、不聲稱其補充頁已重寫。CH1-1 明列貪食蛇為小型趣味範例；CH1-2 說明黃金公式；CH1-3 聚焦單檔、計算函數和多條件提示詞類型。

- [ ] **Step 3: 逐頁更新 40 筆分流與理由**

  `CURRICULUM-MAP.md` 每個舊頁保留一筆：核心 7、補充 32、時區案例 1 筆標示「不遷入新版／歷史檔保留」。將薪資案例標為補充且待官方規則核實；PRAC5-6 保留內容安全審查前暫緩開放的限制。

- [ ] **Step 4: 將核心 manifest 改成指定七站**

  `lesson-map.json` 只保留上述七個 key，依規格順序排列；每筆 title、tagline、outcomes 與單元功能相符。CH1-3 的標題和成果標示為提示詞類型比較；不在此改寫任何 fragment 或 HTML 正文。

- [ ] **Step 5: 驗證來源文件和 JSON**

  執行 `python3 -m json.tool _source/lesson-map.json`，再用以下檢查確認來源路線、分流數及 fragment 均可解析：

  ```bash
  python3 - <<'PY'
  from pathlib import Path
  import json, re
  expected = ['part1/CH1-1.html','part1/CH1-2.html','part1/CH1-3.html','part2/CH2-1.html','part2/PRAC2-1.html','part4/CH4-1.html','part4/PRAC4-3.html']
  meta = json.loads(Path('_source/lesson-map.json').read_text())
  assert list(meta) == expected
  assert all((Path('_source/fragments') / item['fragment']).is_file() for item in meta.values())
  lines = Path('_source/CURRICULUM-MAP.md').read_text().splitlines()
  rows = [line for line in lines if re.match(r'^\|\s*`?part\d+/[^|`]+?\.html`?\s*\|', line)]
  assert len(rows) == 40
  counts = {'core': 0, 'supplement': 0, 'excluded': 0}
  for line in rows:
      cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
      role = cells[1]
      counts['core' if '核心' in role or '主線' in role else 'excluded' if '不遷入' in role else 'supplement'] += 1
  assert counts == {'core': 7, 'supplement': 32, 'excluded': 1}, counts
  print('PASS', len(meta), counts)
  PY
  ```

  最後搜尋四份來源文件，確認沒有把「10 站必修／3 個工作主案例」寫成目前路線。

### Task 3：同步首頁必修路線和新版目錄

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: `_source/lesson-map.json` 七站清單與 `_source/CURRICULUM-MAP.md` 39 個遷入頁的角色。
- Produces: 7 項完成清單、7 項進度總數、39 張可瀏覽新版教材卡；時區舊頁不出現在新版目錄。

- [ ] **Step 1: 更新首頁路線敘述和進度數字**

  將必修路線描述改為 7 站與一個主工作案例，進度起始文字為 `0 / 7`；五階段和六小時不含休息的假設需與規格一致。

- [ ] **Step 2: 依 manifest 更新七站名稱、順序與完成證據**

  首頁 `#required-route` 的七個 href 必須和 manifest 順序完全相同；每項核對文字描述學習成果，不使用計時器細節作為課程完成目標。

- [ ] **Step 3: 更新補充目錄角色並排除 PRAC2-2 連結**

  將 PRAC3-3、CH6-1、PRAC6-1 的卡片從核心改成補充；其餘 32 個補充頁維持可見與可點擊；移除 `part2/PRAC2-2.html` 的新版目錄卡片但保留其實際檔案。首頁說明新版目錄含 39 頁，歷史檔案不因未列目錄而刪除。

- [ ] **Step 4: 核對首頁卡片集合及進度 DOM**

  用 BeautifulSoup 解析 `index.html`，確認核心 checkbox 路徑恰為 manifest 的 7 個 key、補充卡片 32 張、可瀏覽新版卡片共 39 張、PRAC2-2 href 為 0，且完成數節點仍有 `id="core-progress-count"`。

### Task 4：同步七站頁面導覽與移出頁角色

**Files:**
- Modify: `part1/CH1-1.html`, `part1/CH1-2.html`, `part1/CH1-3.html`
- Modify: `part2/CH2-1.html`, `part2/PRAC2-1.html`
- Modify: `part4/CH4-1.html`, `part4/PRAC4-3.html`
- Modify: `part3/PRAC3-3.html`, `part6/CH6-1.html`, `part6/PRAC6-1.html`

**Interfaces:**
- Consumes: Task 2 manifest 的核心順序。
- Produces: 七個核心頁形成完整前後站鏈；三個移出核心頁保持可瀏覽並標示補充角色。

- [ ] **Step 1: 先讀 HTML 保護契約**

  修改前讀取 `/Users/paichenwei/.agents/skills/course-html-contract/SKILL.md`，在變更紀錄標註本批為 `content-change`：只改 `.lesson-nav`、`.lesson-hero` 路線角色、CH1-3 頁面身份標題（與 manifest 完全一致），以及 CH6-1 的「必修只測 Build 預覽與結果保存」句子，改成「此補充案例示範 Build 預覽與結果保存」。不碰其他教學文案、提示詞、示範或舊內容。

- [ ] **Step 2: 依七站順序更新核心頁前後站**

  建立 prev／next 對照：CH1-1（index／CH1-2）、CH1-2（CH1-1／CH1-3）、CH1-3（CH1-2／CH2-1）、CH2-1（CH1-3／PRAC2-1）、PRAC2-1（CH2-1／CH4-1）、CH4-1（PRAC2-1／PRAC4-3）、PRAC4-3（CH4-1／index）。標籤名稱同步目前核心頁標題，並把 PRAC4-3 footer 的「必修 10／10」改為「必修 7／7」。

- [ ] **Step 3: 將三個原核心頁改為補充角色**

  把 PRAC3-3、CH6-1、PRAC6-1 的 `.lesson-hero[data-learning-role]` 從 `core` 改為現有延伸頁使用的角色值；只在 CH6-1 修正「必修只測」的路線身份句，其餘正文、指令、素材和歷史導覽內容保持原樣。

- [ ] **Step 4: 用結構檢查比對前後站和正文快照**

  Python／BeautifulSoup 讀七個核心頁，逐項比對 prev／next href 與 manifest 前後項；讀三個移出頁確認角色不再是 core。以修改前備份比較正文、prompt 區塊和連結，唯一允許的正文差異是 CH6-1 上述必修／補充定位修正，另允許 PRAC4-3 footer 的總站數由 10 改成 7；再執行共用結構檢查器。

### Task 5：移除驗證器的固定 10 站假設並跑課程檢查

**Files:**
- Modify: `_tools/verify-static.py`
- Modify: `_tools/verify-browser.cjs`
- Modify: `_tools/README.md`
- Create: `_repair/2026-10-07/route-sync-check.json`

**Interfaces:**
- Consumes: 七站 `lesson-map.json`、首頁 checkbox 和頁面導覽。
- Produces: 不依賴固定站數的靜態／瀏覽器檢查，以及本次路線驗證結果。

- [ ] **Step 1: 將靜態驗證輸出改為 manifest 長度**

  `verify-static.py` 繼續檢查所有 lesson HTML 的相對連結、錨點、重複 ID、素材 ZIP 和片段保真；核心路線筆數用 `len(route)` 輸出，並檢查首頁 checkbox 集合及首頁目錄中 39 個遷入單元。加入 `--out-dir`，預設本次輸出指定資料夾；加入 `--skip-shared-ops`，讓本課靜態檢查不比較或寫入共用 search-index／sitemap。錯誤時以非零狀態結束。

- [ ] **Step 2: 將瀏覽器進度測試改為動態站數**

  `verify-browser.cjs` 將固定字串 `1 / 10` 改成依 `route.length` 組合預期值；移除不存在的 `#core-route-banner` 查詢，改為比對每頁 next href、點擊後實際 URL 與 manifest 下一站；進度勾選後 reload 應是 `1 / 7`，取消勾選後仍可恢復 `0 / 7`。加入 `--out-dir`，讓 screenshots、browser-results 和 browser-failure 寫到 `_repair/2026-10-07/evidence/`，不覆蓋 2026-10-06 證據。保留其餘頁面操作及 RWD smoke checks。

- [ ] **Step 3: 更新工具說明中的路線來源**

  `_tools/README.md` 說明 verifier 讀取 manifest 決定核心路線，不寫固定的 10 站；記錄 `--out-dir` 和 `--skip-shared-ops` 用法；標明 `build-lessons.py` 與 `apply-repair.py` 是一次性腳本且不得用來重建本次路線。

- [ ] **Step 4: 執行靜態與頁面 lint**

  從課程根目錄執行 `python3 _tools/verify-static.py --out-dir _repair/2026-10-07 --skip-shared-ops`；從網站根目錄執行 `python3 docs/lint-page.py courses/gemini-ai --summary`。確認 `_repair/2026-10-06/link-and-copy-audit.json` 及既有瀏覽器證據雜湊未變。若靜態檢查失敗，修正擁有該行為的路線或 verifier，不略過失敗。

- [ ] **Step 5: 執行瀏覽器驗證**

  在課程根目錄啟動 `python3 -m http.server 31876 --bind 127.0.0.1`，另一終端執行 `node _tools/verify-browser.cjs --out-dir _repair/2026-10-07/evidence`；核對 7 站連結、首頁 `1 / 7` 進度、七站前後導覽和桌面／手機無水平溢位。結束後停止伺服器。

- [ ] **Step 6: 記錄路線結果與限制**

  `route-sync-check.json` 寫入核心 key 清單、40 頁分流數、首頁遷入頁數、頁面連結／導覽檢查結果和執行時間；只記錄實際通過項。全站 search-index、sitemap 及平台登入／模型生成留到後續 `course-ops`／頁型試作，不把現有驗證報告改寫成新證據。

### Task 6：產出修復紀錄並停止於頁型試作關卡

**Files:**
- Create: `_repair/2026-10-07/REPAIR-REPORT.md`

**Interfaces:**
- Consumes: 變更檔案清單、`route-sync-check.json`、備份雜湊和實際命令輸出。
- Produces: 可回查本次路線同步範圍與限制的報告，以及一筆只含本計畫檔案的本機 commit。

- [ ] **Step 1: 記錄本次變更與驗證**

  報告列出改動檔案、核心 7／補充 32／不遷入 1、備份與還原腳本、靜態／lint／瀏覽器實測結果及未執行的全站 ops。

- [ ] **Step 2: 明列尚未完成項目**

  記錄 CH1-1 至 CH1-3 和其餘核心／補充頁正文尚未依路線重寫；貪食蛇提示詞尚未平台生成測試；補充教材完整提示詞和操作仍待逐案完成；學員 agent 冷讀、使用者人工審閱及六小時真人試教尚未執行。此路線同步完成不等同課程完成。

- [ ] **Step 3: 檢查差異並限定提交範圍**

  執行 `git diff --check`、`git status --short` 和 `git diff --name-only`；只 stage 本計畫列出的檔案，不納入其他課程或共用搜尋索引的未提交變更。確認暫存區檔案清單後，以 `docs(gemini-ai): sync stage 3 route` 建立本機 commit。不 push；需要對外提供人工驗證時另依已核准的章節試作流程處理。

  明確 stage 清單：

  ```bash
  git add -- \
    _backup/2026-10-07-stage3-route-pre-sync/ \
    _tools/restore-2026-10-07-stage3-route-pre-sync.sh \
    _source/OUTLINE.md _source/LESSON-PLANS.md _source/CURRICULUM-MAP.md _source/lesson-map.json \
    _source/fragments/part6-CH6-1.fragment \
    index.html \
    part1/CH1-1.html part1/CH1-2.html part1/CH1-3.html \
    part2/CH2-1.html part2/PRAC2-1.html \
    part3/PRAC3-3.html part4/CH4-1.html part4/PRAC4-3.html \
    part6/CH6-1.html part6/PRAC6-1.html \
    _tools/verify-static.py _tools/verify-browser.cjs _tools/README.md \
    _repair/2026-10-07/REPAIR-PLAN.md _repair/2026-10-07/route-sync-check.json \
    _repair/2026-10-07/REPAIR-REPORT.md
  git diff --cached --check
  git diff --cached --name-only
  git commit -m "docs(gemini-ai): sync stage 3 route"
  ```

## 遺留給頁型試作的內容

1. 依已核准的五階段設計重寫 CH1-1、CH1-2、CH1-3 的完整學員講義；CH1-1 內含貪食蛇完整單一 HTML 提示詞和清楚的操作目的。
2. 將貪食蛇來源檔複製到課程素材位置前，核對來源 SHA-256；完成可點擊預覽／開啟方式與作者平台試跑。
3. 完成後依使用者先前要求，交由學員 agent 冷讀，再交使用者人工審閱；修正通過前不批次改寫其他補充頁。
