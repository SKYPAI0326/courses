# gen-image v4 重構 — Codex Audit Brief v2（第二輪檢測）

**建立日期**：2026-04-26（Round 4 + CH2-1 grid 化全部 merge 進 main 後）
**對象 commit 範圍**：`9e4421d..HEAD`（main 上的 5 個 v4 重構 commit）
**用途**：把 v4 重構**完整成果**（含 4 輪修補）交給 Codex 第二輪 audit
**前次 audit 報告**：`courses/gen-image/_refactor/codex-review-report.md`（給 v4 第一版的 1 BLOCKER + 7 WARN + 4 NIT）

---

## 0. 上輪 audit 後的修補軌跡

5 個 commit 累積落地（時間軸由舊到新）：

| Commit | 主題 | 對應 audit 修補 |
|--------|------|--------------|
| `7b57dc1` | v4 互動工作坊重構 13 頁 + 12 張新圖（v31-v42）| Round 1 主體 + 接上一次 Codex audit 12 張新圖 + 法規語 + 案例真實性 |
| `e8fd469` | Round 2 設計系統清理 + NIT | 修「3 秒決定」/「等 30 秒」/ 字階 .78/.98/1/1.15/1.35 → V4 / 案例日期可替換 / Step N → 步驟 N |
| `e699d1f` | Round 4 callout 收斂 CH1-1/CH3-1/CH3-2 | 3 頁 callout 從 10/10/8 → 各 4（Codex Round 1 留下的 callout 超量 WARN）|
| `bdc536f` | CH2-1 code-block white-space:pre | 修使用者回報 ASCII art 換行錯位 |
| `6542126` | CH2-1 8 版型 ASCII → HTML grid 結構 | 根治 CJK 對齊問題（Courier New 對中文無等寬支援）、新增 .layout-mockup CSS |

**累積成果**：lint WARN 從 audit 時 55 → 現在 **39**（-16）。

---

## 1. 當前 lint 分桶

```bash
python3 docs/lint-page.py courses/gen-image/ --by-bucket
```

| 分桶 | 條數 | 跨檔 |
|------|------|------|
| migration-debt | 17 | 17 |
| a11y | 13 | 13 |
| motion | 5 | 5 |
| structural | 4 | 4 |
| **總計** | **39** | — |

**0 BLOCKER / 0 ERROR**。

剩餘 WARN 性質（Codex 不需修、僅供參考）：
- **migration-debt**：箭頭符號 line-based 誤判 + nav-btn `--c-main` 5 處（設計繼承）
- **a11y**：cycle-bridge 內 `→` 是內文視覺符號、line-based lint 誤判
- **motion**：v3 hover 規則
- **structural**：可能是 callout/section count 邊緣案例

---

## 2. Audit 重點（5 個新領域）

### Q1【新元件 .layout-mockup 合規性】CH2-1 新增的 grid mockup 結構

**背景**：CH2-1 8 版型 ASCII art 改用 `.layout-mockup` HTML grid 結構（commit `6542126`）。新 CSS 共 22 條規則：

```css
.layout-mockup{...}
.layout-mockup .lm-frame{border:1px solid #6b6b6b;...}
.layout-mockup .lm-row{display:flex;...border-bottom:1px solid #6b6b6b;...}
.layout-mockup .lm-row.lm-main{background:rgba(255,255,255,.04)}
.layout-mockup .lm-row.lm-tall / .lm-xtall / .lm-short / .lm-center{...}
.layout-mockup .lm-cells{display:grid;border-bottom:1px solid #6b6b6b}
.layout-mockup .lm-cells.lm-3col{grid-template-columns:1fr 1fr 1fr}
.layout-mockup .lm-cells.lm-2col{grid-template-columns:1fr 1fr}
.layout-mockup .lm-cell / .lm-pct / .lm-sub / .lm-caption{...}
```

**請 Codex 檢查**：
1. 字型尺寸（.85 / .82 / .78rem）是否全在 V4 15 階白名單內
2. 顏色 `#6b6b6b` `#9a9a9a` `rgba(255,255,255,.04)` 是不是直接寫死、會不會被 lint 抓「自創 hex」（design-tokens 規定組件 CSS 走 var(--c-X)）
3. `grid-template-columns:1fr 1fr 1fr` / `1fr 1fr` 是不是允許的 grid 模式（design-tokens §5）
4. mobile（max-width:600px）下 .lm-cells 是否需要降為單欄（目前沒 media query 處理、可能在窄螢幕擠壓）
5. 8 個版型的 mockup 結構視覺是否一致（建議用瀏覽器看 https://skypai0326.github.io/courses/courses/gen-image/CH2-1.html）

### Q2【Round 1 修補真的修好了嗎】回頭驗證

請 Codex 對以下項目**逐一抽查**，確認 Round 1 audit 提的問題真的修好（用 git diff 或瀏覽 main 內容）：

1. **codex-image-requests.md 數量矛盾**：應為 12 張 / P0 7 + P1 2 + P2 3（不再有「9 張」「P0 5 張」字樣）
2. **CH5-1 案例 B 法規語**：應有 callout-tip「100 億活菌 / 醫師監修…實際投放須符合法規」
3. **CH5-1 5 案例「日本市場模擬」標註**：A/B/E 應標註「日本市場模擬品牌」、C 應標註「日期僅為示範」、D 應標註「期間日期僅為示範」
4. **CH5-1 案例日期 2026.06.15 等**：應改成 `{YYYY.MM.DD 開課時填}` 替換語法
5. **PRAC3 時間盒 stretch goal**：tagline / section-heading / intro / exercise 4 處應一致提「合格 3 張、5 張為 stretch goal」
6. **PRAC4 結尾金句**：應為「鎖死 3 件事、系列就是品牌」（不是「多看多拆多練、版型力自然提升」）
7. **PRAC2/3 Step N → 步驟 N**：應 0 個 `Step \d` match
8. **CH2-2 cycle 4 v31-33 / CH4-2 v34-37 / CH5-1 v38-42 圖片接到位**：12 張新圖都應在對應 details 內顯示
9. **CH1-2 「品質拿到 90%」**：應改成「日常商用大致夠用、進階可能需另一家補強」
10. **字階非 V4 改 V4 標準**：.78/.98/1/1.15/1.35rem 都應改成 .8/.95/1.05/1.1/1.45rem
11. **CH2-1 「3 秒決定」**：應改成「快速決定」（保留「停留 3 秒」這個受眾行為觀察）
12. **CH2-2 「等 30 秒」「5 分鐘出圖」**：應改成「約 30 秒」「目標 5 分鐘出圖」

### Q3【Round 4 callout 收斂效果】CH1-1 / CH3-1 / CH3-2 lint 應 0 callout warning

**請 Codex 跑**：
```bash
python3 docs/lint-page.py courses/gen-image/CH1-1.html courses/gen-image/CH3-1.html courses/gen-image/CH3-2.html | grep callout
```

**預期**：無 callout warning（3 頁都應 ≤ 4）。

如果還有 warning，請告訴我哪頁、哪個 callout 沒收斂到。

### Q4【新「aside-tip」class 是否合規】

**背景**：Round 4 把 `blockquote.tip-callout` 重命名為 `blockquote.aside-tip`（避開 lint regex `\bcallout\b` 誤判）。CSS 同步改名。

**請 Codex 檢查**：
1. CH1-1 / CH3-1 / CH3-2 內的 `aside-tip` 元素數量與 CSS 定義數量一致
2. 視覺渲染是否仍是「左灰邊線 blockquote」（重命名前後外觀一致）
3. design-tokens.md 是否需要把 `aside-tip` 加進 v4 組件白名單（目前沒加、可能算自製）

### Q5【新內容問題搜尋】Round 2-4 修補時是否引入新問題

請 Codex 抽樣以下類別、找新引入的瑕疵：

1. **PRAC2/3 段內 strong 段（Round 2 callout 收斂後）** — 是否破壞原 callout 的視覺重點？學員是否還能一眼看出「預期差異」「PM 思維」這些關鍵提醒？
2. **CH5-1 案例情境句加註的「日本市場模擬」「日期示範」**等 — 是否破壞流暢度？建議改寫法？
3. **CH2-1 .layout-mockup 8 版型 mockup** — 跟原 ASCII art 比、是否仍能傳達「版型結構」概念？
4. **PRAC3 時間盒 4 處改寫**（合格 3 張 / stretch 5 張） — 是否前後一致無矛盾？
5. **整體 CH2-2 / CH5-1 details 折疊**（共 16+17 個）— 是否仍有「主流程指令說『查 X 表』但表只在 details 內」的 broken link？

---

## 3. Audit 期望產出格式

請 Codex 用以下 markdown 格式回 issue list、存為 `courses/gen-image/_refactor/codex-review-report-v2.md`：

```markdown
# gen-image v4 重構 第二輪 Codex Audit Report

**Audit 時間**：2026-04-26 HH:MM
**檢查 commit 範圍**：`9e4421d..HEAD` 共 5 commits

## Summary

- 上輪 audit BLOCKER 1 條已修：✅ / ❌
- 上輪 audit WARN 7 條已修：N/7
- 上輪 audit NIT 4 條已修：N/4
- 新引入 BLOCKER：N
- 新引入 WARN：N
- 新引入 NIT：N

## Q1 .layout-mockup 合規性
- ✅ / ⚠️ / ❌ 字型階
- ✅ / ⚠️ / ❌ 顏色直寫
- ✅ / ⚠️ / ❌ grid 模式
- ✅ / ⚠️ / ❌ mobile 適配
- ✅ / ⚠️ / ❌ 8 版型視覺一致性

## Q2 Round 1 修補逐項驗證（12 項）
- 1. codex-image-requests.md 數量：✅ / ❌ 細節
- 2. CH5-1 案例 B 法規語：✅ / ❌
- ...

## Q3 callout 收斂
- CH1-1 / CH3-1 / CH3-2：lint 抓到 X 條（預期 0）

## Q4 aside-tip class
- 數量一致：✅
- 視覺一致：✅
- design-tokens 註冊建議：✅ 應加 / ⏭ 可不加

## Q5 新引入問題
- ...

## 修補優先順序
1. [BLOCKER] ...
2. [WARN] ...
```

---

## 4. 跑 Codex 的建議命令

```bash
cd "/Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁"

# 取 v4 重構完整 diff
git diff 9e4421d..HEAD -- courses/gen-image/ _規範/design-tokens.md > /tmp/v4-full.diff

# Codex CLI 互動模式：
# 1. 把本 brief（codex-audit-brief-v2.md）丟進 Codex 對話
# 2. 把 /tmp/v4-full.diff 也丟進去
# 3. 要求按上方 Q1-Q5 + Summary 格式回 codex-review-report-v2.md
# 4. Codex 完成後把報告存到 courses/gen-image/_refactor/
```

---

## 5. Audit 後動作

Codex 回 `codex-review-report-v2.md` 後：

1. **新 BLOCKER** → Claude 立刻修
2. **舊 BLOCKER/WARN 標 ❌**（沒修好的）→ Claude 補修
3. **新 WARN/NIT** → 評估是否進 Round 5 或留下次

修完 commit + push + 開 PR + merge + Pages 驗證（同前 4 輪流程）。

---

## 6. 補充 reference

- v4 設計理由：`courses/gen-image/_refactor/interactive-workshop-playbook.md`（929 行）
- 上輪 Codex 報告：`courses/gen-image/_refactor/codex-review-report.md` / `claude-code-handoff.md`
- 上輪 Claude 修補紀錄：`courses/gen-image/_refactor/codex-fix-report.md`
- v4 新元件規範：`_規範/design-tokens.md` § v4 互動工作坊組件
- lint 真相源：`docs/lint-page.py`（line 304-323 字型 15 階白名單）
- 線上預覽：https://skypai0326.github.io/courses/courses/gen-image/
