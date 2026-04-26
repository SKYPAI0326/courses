# gen-image v4 重構 — Codex Audit Brief

**建立日期**：2026-04-26
**分支**：`feat/gen-image-course`
**用途**：把本次 v4 互動工作坊重構交給 Codex CLI 做獨立 audit、回 issue list

---

## 0. 變動範圍（給 Codex 看的檔案清單）

```bash
# 完整 diff 範圍
git diff main...HEAD --stat -- \
  courses/gen-image/ \
  _規範/design-tokens.md
```

**新建（2 檔）**：
- `courses/gen-image/_refactor/interactive-workshop-playbook.md` — 929 行重構諮詢報告（v4 設計理由）
- `courses/gen-image/_refactor/codex-image-requests.md` — 9 張新圖生成需求清單

**規範更新（1 檔）**：
- `_規範/design-tokens.md` — 追加「v4 互動工作坊組件」節（8 組件）

**HTML 全頁重寫（2 檔）**：
- `courses/gen-image/CH2-2.html`：1161 → 891 行（5 micro-cycle + 整合任務 + 收束 + instructor-note 折疊）
- `courses/gen-image/CH5-1.html`：1251 → 1046 行（5 cycle + 5 案例 details + 6 NG 對照 + Lookbook 進階收進 instructor-note）

**HTML 補件（3 檔，PRAC）**：
- `courses/gen-image/PRAC2.html`：加 v4 CSS + learner-output 表（2-3 張記錄）+ stuck details
- `courses/gen-image/PRAC3.html`：加 v4 CSS + learner-output 表（5 張 L2 記錄）+ stuck details
- `courses/gen-image/PRAC4.html`：加 v4 CSS + learner-output 表（品牌系列 6 行）+ stuck details

**HTML 微創包裝（3 檔，CH4 系列）**：
- `courses/gen-image/CH4-1.html`：hero today-deliverables + 頁尾 SECTION（learner-output 6 行 + stuck）
- `courses/gen-image/CH4-2.html`：hero today-deliverables + 頁尾整合任務 SECTION
- `courses/gen-image/CH4-3.html`：hero today-deliverables + 頁尾整合任務 SECTION

**HTML 輕量（5 檔，僅 hero today-deliverables）**：
- `courses/gen-image/CH1-1.html`
- `courses/gen-image/CH1-2.html`
- `courses/gen-image/CH2-1.html`
- `courses/gen-image/CH3-1.html`
- `courses/gen-image/CH3-2.html`

---

## 1. Audit 5 大重點（按優先順序）

### Q1【教學完整性】CH2-2 / CH5-1 全頁重寫是否遺失原版關鍵教學素材？

**背景**：兩頁是「全頁重寫」（CH2-2 -270 行、CH5-1 -205 行）。為了壓縮，部分內容被改成 `<details>` 折疊或併入 `instructor-note`。

**請 Codex 比對 git diff `main..HEAD` 中這兩個檔的刪除塊**，確認以下原版核心素材是否仍可在新版找到（即使被折疊）：

| 原版段落 | 應該在新版的位置 |
|---------|----------------|
| CH2-2 brief 六件套 6 欄詳細卡 | cycle 2 + cycle 3 + cycle 4 拆解；instructor-note 展開後可見 |
| CH2-2 商業情境案例（弄一下咖啡完整 brief） | instructor-note → details 「主線 A 完整 brief」 |
| CH2-2 常見錯誤 3 條 + ✕ vs ✓ 範例 | instructor-note → details「常見錯誤 3 條」 |
| CH2-2 Tip 1 文字亂碼 / Tip 2 版權 / Tip 3 meta-prompting | instructor-note → details「完整 prompt 模板 + Tip 1/2/3」 |
| CH2-2 8 版型 prompt 範例對應表 | cycle 3 → details「8 版型對照表」 |
| CH5-1 5 案例完整 brand-dna + L2 + 3 主題 + prompt（A/B/C/D/E） | cycle 2 → 5 個 `<details class="case-fold">` |
| CH5-1 8 troubleshooting 症狀 × 修正話術 | cycle 4 主流程內可見表格 |
| CH5-1 6 組 NG → OK 對照圖（v25-30）| cycle 4 → 6 個 `<details class="compare-fold">` |
| CH5-1 進階挑戰 Lookbook（3 風格 + meta-prompting）| instructor-note → details「進階挑戰｜Lookbook」 |
| CH5-1 個人品牌資產庫 ASCII tree | cycle 5 主流程內 |

**期望產出**：
- 「✅ 全部找到」or
- 「❌ 缺失：[段落名] 在新版找不到、應從原版 line X-Y 還原」

### Q2【設計系統合規】v4 新增 8 組件 class 與既有 design-tokens.md / lint-page.py 是否衝突？

**背景**：本次新增 8 組件、註冊在 `_規範/design-tokens.md` v4 區、未動 `docs/lint-page.py`（理由：lint 此版不做 class whitelist 檢查）。

**請 Codex 檢查**：
1. 新 class 命名是否與既有 §3 內容組件 / 輔助組件 / Pilot A 禁用組件衝突
   ```
   .today-deliverables / .micro-cycle / .cycle-eyebrow / .cycle-question
   .cycle-bridge / .closer / .wrong-example / .task-card (+ -large/-master/-stuck)
   .learner-output (+ -table/-blank/-label) / .self-check / .concept-pair
   .instructor-note / .case-fold / .compare-fold
   ```
2. CSS 屬性值是否全部走 V4 15 階字型（`docs/lint-page.py` line 304-323 白名單）
3. 新 class 是否引入 box-shadow / gradient / `var(--c-a*)` 直接引用 / hover > 2 屬性
4. callout 仍 ≤ 4 個 / lesson-section 仍 ≥ 5 個

**期望產出**：每條 class 一行「✅ 合規」or「⚠️ 違規 + 原因 + 建議修法」

### Q3【PM 定位一致性】所有 cycle 是否仍訓練 PM 三身份（需求判定 / 骨架驗收 / 系列把關），沒滑成設計師？

**背景**：v4 互動化的風險是任務變多、學員可能誤以為「練美感」。

**請 Codex 抽樣檢查**這 12 個 task-card / learner-output 區的「動詞」與「完成物」：
- CH2-2 cycle 1-5 + 整合任務（共 7 個 task-card）
- CH5-1 cycle 1-5（共 5 個 task-card）
- CH4-1 / CH4-2 / CH4-3 整合任務 section 各 1 個（3 個）
- PRAC2 / 3 / 4 learner-output 表（3 個）

**判準**：
- ✅ 動詞偏 PM：填 / 寫 / 判斷 / 對照 / 驗收 / 挑選 / 對比 / 分類 / 紀錄
- ❌ 動詞偏設計師：畫 / 配色 / 美化 / 排版 / 修圖 / 「再好看一點」

**期望產出**：列出有疑慮的 task-card、引用具體文字、建議改寫方向。

### Q4【內容降級無損】從主流程移到 instructor-note 的內容是否真的「不影響教學」？

**背景**：CH2-2 / CH5-1 兩頁把試跑包 / 案例 / 常見錯誤 / Lookbook 等都包進 `<details class="instructor-note">` 折疊區、預設 closed。

**請 Codex 模擬「學員從頭瀏覽不展開任何 details」的閱讀體驗**：
1. 主流程能否完整完成 today-deliverables 的 3 件交付？
2. 是否有「任務指令說『查 8 版型對照表』但表在 details 內、學員不會主動展開」的 broken link？
3. 是否有「self-check 的判準需要展開 details 才能對照」的隱性依賴？

**期望產出**：列出 broken-link 類問題（如有），給「在主流程加 1 行提示展開」的修補建議。

### Q5【執行細節】HTML / CSS / 連結 / 圖片是否有破洞？

**請 Codex 跑以下技術檢查**：

```bash
# 1. lint（已驗、預期通過）
python3 docs/lint-page.py courses/gen-image/

# 2. 找壞連結（指向不存在的頁 / 圖）
grep -E 'href="[^"]+\.html"|src="[^"]+\.png"' courses/gen-image/*.html | \
  awk -F'"' '{print $2}' | sort -u | \
  while read f; do
    [ -f "courses/gen-image/$(dirname courses/gen-image/CH2-2.html | xargs basename)/$f" ] || \
    [ -f "courses/gen-image/$f" ] || \
    echo "BROKEN: $f"
  done

# 3. 確認所有重構頁的 footer-meta data-built-at 都更新
grep 'data-built-at' courses/gen-image/CH2-2.html courses/gen-image/CH5-1.html

# 4. 找重複 / 孤兒 ID
grep -oE 'id="[^"]+"' courses/gen-image/CH5-1.html | sort | uniq -c | sort -rn | head

# 5. 找閉合不平衡
python3 -c "
import re
for f in ['courses/gen-image/CH2-2.html', 'courses/gen-image/CH5-1.html']:
    html = open(f).read()
    opens = len(re.findall(r'<section', html))
    closes = len(re.findall(r'</section>', html))
    print(f, 'open:', opens, 'close:', closes, 'balanced' if opens==closes else 'BROKEN')
"
```

**期望產出**：每條問題的具體位置 + 修法建議。

---

## 2. Audit 期望產出格式

請 Codex 用以下 markdown 格式回 issue list：

```markdown
# gen-image v4 重構 Codex Audit Report

**Audit 時間**：2026-04-26 HH:MM
**檢查 commit 範圍**：`main..feat/gen-image-course`

## Summary
- BLOCKER：N 條（must fix before merge）
- WARN：N 條（建議修、不擋）
- INFO：N 條（觀察、未必要動）

## Q1 教學完整性（10 段比對）
- ✅ CH2-2 brief 六件套：找到於 cycle 2/3/4
- ❌ [若有缺失] CH5-1 案例 X 的 prompt 模板：原版 line 290-345、新版找不到
...

## Q2 設計系統合規（13 class）
- ✅ .today-deliverables：合規
- ⚠️ .case-fold：summary 用 `font-size:.95rem`、不在 V4 15 階（建議改 .92 或 1.05）
...

## Q3 PM 定位（12 任務卡抽樣）
- ✅ CH2-2 cycle 2 task-card：動詞「填 / 寫」、完成物「brief 前 3 欄」
- ⚠️ CH5-1 cycle 5：「寫一週計畫」太抽象、建議改「列出 3 件可執行小事」
...

## Q4 降級無損
- ✅ CH2-2 主流程不展開 details 也能跑完 3 件交付
- ❌ CH5-1 cycle 4：self-check 提到「查表」但表只在 details 內、需加提示
...

## Q5 執行細節
- BROKEN: courses/gen-image/CH5-1.html line 234 連到 img/v40-x.png（檔不存在）
- WARN: CH4-2 footer data-built-at 仍是 2026-04-24（應改 2026-04-26）
...

## 修補優先順序建議
1. [BLOCKER] ...
2. [WARN] ...
3. [INFO] ...
```

---

## 3. 跑 Codex 的建議命令

```bash
# 在專案根目錄
cd "/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁"

# 把 brief + diff 餵給 Codex CLI
codex audit \
  --brief courses/gen-image/_refactor/codex-audit-brief.md \
  --diff "git diff main...HEAD -- courses/gen-image/ _規範/design-tokens.md" \
  --output courses/gen-image/_refactor/codex-audit-report.md

# 或用 OpenAI Codex CLI 互動模式：
# 1. 把本檔丟進 Codex 對話
# 2. 把 git diff 貼進去
# 3. 要求按上方「Q1-Q5 + Summary」格式回 issue list
```

---

## 4. Audit 完成後動作

Codex 回 `codex-audit-report.md` 後：

1. **BLOCKER** → Claude 立刻修
2. **WARN** → 評估後選擇性修（影響大的修、純偏好的留）
3. **INFO** → 進 `_規範/飛輪規則.md` 累積、下次重構引用

修完後重跑：
```bash
python3 docs/lint-page.py courses/gen-image/ --no-warn
python3 docs/build-search-index.py
python3 docs/build-sitemap.py
```

確認全綠後 commit。

---

## 5. 給 Codex 的補充上下文（可選讀）

- v4 設計理由：`courses/gen-image/_refactor/interactive-workshop-playbook.md`（929 行、重構諮詢報告）
- v4 新元件規範：`_規範/design-tokens.md` § v4 互動工作坊組件（line 400+ 區）
- lint 真相源：`docs/lint-page.py`（特別 line 304-323 字型 15 階白名單）
- 圖片需求：`courses/gen-image/_refactor/codex-image-requests.md`（9 張新圖、不需 audit、僅 reference）
