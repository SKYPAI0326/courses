# gen-image v4 重構 第二輪 Codex Audit Report

**Audit 時間**：2026-04-26 18:54 CST
**檢查 commit 範圍**：`9e4421d..HEAD` 共 5 commits

## Summary

- 上輪 audit BLOCKER 1 條已修：✅
- 上輪 audit WARN 7 條已修：3/7
  - ✅ 已修：CH5-1 保健品法規語、PRAC3 stretch goal、PRAC4 結尾金句
  - ⚠️ 部分修：日本市場 / 日圓案例只完整修到 CH5-1；callout 收斂只修 CH1-1 / CH3-1 / CH3-2 / PRAC2 / PRAC3，CH1-2 仍超量
  - ❌ 未完全修：CH1-2 平台時效資訊仍含配額 / 付費 / 2026-04 時點表；CH2-2 / CH5-1 details 仍各 17 個且未分級
- 上輪 audit NIT 4 條已修：3/4
  - ✅ `Step \d` regex 已 0 match、CH2-1 / CH2-2 時間保證語已改、CH5-1 固定 2026 日期已移除
  - ❌ CH1-2 平台品牌名密度仍高
- 新引入 BLOCKER：0
- 新引入 WARN：3
- 新引入 NIT：2

## Q1 .layout-mockup 合規性

- ⚠️ 字型階：`.layout-mockup` 主體 `.85rem`、`.lm-cell` `.82rem` 合規；但 `.lm-pct` / `.lm-sub` / `.lm-caption` 使用 `.78rem`，已被 lint 抓為 `CH2-1.html` 非 V4 15 階字型值。建議改 `.8rem` 或 `.75rem`。
- ⚠️ 顏色直寫：新增 CSS 直接寫 `#6b6b6b`、`#9a9a9a`、`rgba(255,255,255,.04)`，不符合 design-tokens「組件 CSS 一律用 var(--c-X)」精神。lint 目前未抓 hex，但這是設計系統債。
- ✅ grid 模式：`1fr 1fr` / `1fr 1fr 1fr` 都在 design-tokens §5 允許的固定欄模式內。
- ⚠️ mobile 適配：Playwright 390px 量測未水平溢出，但 D 版型三欄在 mobile 每欄只剩約 88px。文字目前短所以可讀；若日後換成較長中文會擠壓。建議 `@media(max-width:600px)` 讓 `.lm-cells` 仍保留結構但縮 padding / font，或必要時改單欄。
- ✅ 8 版型視覺一致性：線上 HTML 200 OK；桌機 / mobile 截圖檢查顯示 8 個 mockup 乾淨、一致、無明顯 overlap，已比原 ASCII 更能穩定表達版型結構。

## Q2 Round 1 修補逐項驗證（12 項）

- 1. codex-image-requests.md 數量：✅ 已統一為 12 張 / P0 7 + P1 2 + P2 3；仍保留「原 brief 誤寫 9 張 / P0 5 張」於修訂紀錄，這是歷史說明不是需求矛盾。
- 2. CH5-1 案例 B 法規語：✅ 已有 `callout tip`，含「100 億活菌 / 醫師監修 / 敏感腸友善」概念示意與「實際投放須符合法規、不得做療效保證」。
- 3. CH5-1 5 案例標註：✅ A/B/E 標「日本市場模擬品牌」，C 標「日期僅為示範」，D 標「期間日期僅為示範」。
- 4. CH5-1 案例日期 2026.06.15 等：✅ 未再找到 `2026.06.15` 等固定 2026 日期；案例 C 表格改成 `{YYYY.MM.DD 開課時填}`。案例 D 仍有 `6/1-7/31`、`9/1-10/31`，但已標為期間示範。
- 5. PRAC3 時間盒 stretch goal：✅ tagline / section heading / intro / exercise 都提到合格 3 張、5 張 stretch。另見 Q5 NIT：仍殘留「4 Step」英文寫法。
- 6. PRAC4 結尾金句：✅ 已改為「鎖死 3 件事、系列就是品牌」。
- 7. PRAC2/3 Step N → 步驟 N：✅ `Step \d` 為 0 match；PRAC2/3 仍有「4 Step」字樣，屬語彙一致性 NIT，不再觸發原 lint。
- 8. 12 張新圖接到位：✅ CH2-2 有 v31-v33；CH4-2 有 v34-v37；CH5-1 有 v38-v42，且都在對應 details / case-fold 內。
- 9. CH1-2 「品質拿到 90%」：✅ 已改成「日常商用大致夠用、進階場景可能需另一家補強」。
- 10. 字階非 V4 改 V4 標準：⚠️ 舊提到的 `.98 / 1 / 1.15 / 1.35rem` 已未見；但 CH2-1 新增 `.layout-mockup` 又引入 `.78rem`，造成新的 lint WARN。
- 11. CH2-1 「3 秒決定」：✅ heading / instructor-note 已改「快速決定」；保留「停留 3 秒」作為受眾行為觀察，符合 brief。
- 12. CH2-2 「等 30 秒」「5 分鐘出圖」：✅ 已改「約 30 秒」與「目標 5 分鐘出圖」。

## Q3 callout 收斂

- CH1-1 / CH3-1 / CH3-2：lint 抓到 0 條 callout warning（預期 0）。
- 實際命令結果仍有 6 條 WARN，但都來自箭頭 a11y 與 `--c-main` migration-debt，不是 callout。
- 補充：全站仍有 CH1-2、CH4-1、CH4-3、PRAC4 callout 超過 4 個；這不是本輪 Q3 指定頁，但仍是前輪 WARN 的殘留。

## Q4 aside-tip class

- 數量一致：✅ CH1-1 有 2 個、CH3-1 有 4 個、CH3-2 有 2 個；三頁都有 `blockquote.aside-tip` 與 `blockquote.aside-tip strong` CSS 定義。
- 視覺一致：✅ CSS 仍是 `border-left:2px solid var(--c-text)`、`background:var(--c-surface)`、blockquote 左邊線樣式，符合原「左灰邊線 blockquote」用途。
- design-tokens 註冊建議：✅ 應加。`aside-tip` 目前不在 design-tokens 白名單；同批 v4 新組件如 `today-deliverables`、`learner-output`、`task-card-stuck` 也大量使用但未進 §3 白名單。lint 目前不抓 unknown class，但人類規範已寫「自製組件 = reviewer BLOCKER」，建議補一節「v4 互動工作坊組件」。

## Q5 新引入問題

- PRAC2/3 段內 strong 段：✅ 可讀性尚可。`預期差異`、`PM 思維`、`底線` 等提醒雖從 callout 降為段落 / list strong，但仍可一眼掃到；PRAC2/3 callout lint 已不超量。
- CH5-1 案例加註：✅ 流暢度可接受。A/B/E「日本市場模擬品牌」、C/D「日期示範」放在情境句尾，不破壞主流程。若要更順，可把括號改成 `案例設定：...` 的短 meta 行。
- CH2-1 8 版型 mockup：✅ 比 ASCII 更穩定，且 mobile 無水平溢出；概念仍清楚。唯一風險是三欄 mockup 在 390px 下每欄約 88px，長文會擠。
- PRAC3 時間盒改寫：⚠️ 核心目標一致，但仍殘留「每張走 4 Step」「單張 4 Step 流程」等英文語彙。這不再是原 `Step \d` 問題，但與 Round 2 中文化方向不一致。
- CH2-2 / CH5-1 details broken link：✅ 未發現「主流程要求查 X 表但表只藏在 details 且無提示」的硬斷點。CH5-1 troubleshooting 表是主流程可見；CH2-2 延伸表 / preset 表 summary 都明確標「按需展開」。但 details 數量仍高：CH2-2 17 個、CH5-1 17 個，尚未做到「必看 / 卡關 / 課後」視覺分級。

## 新引入問題清單

1. [WARN] CH2-1 `.layout-mockup` 新增 `.78rem`，造成 lint 仍報非 V4 字階。
   - 位置：`courses/gen-image/CH2-1.html` CSS `.lm-pct` / `.lm-sub` / `.lm-caption`
   - 建議：改為 `.8rem` 或 `.75rem`。

2. [WARN] CH2-1 `.layout-mockup` 直接寫死色彩值，未走 design token。
   - 位置：`courses/gen-image/CH2-1.html` CSS `#6b6b6b` / `#9a9a9a` / `rgba(255,255,255,.04)`
   - 建議：以既有 token 或新增語義 token 取代，例如 border 用 `rgba(232,228,220,.35)` 也應先註冊為 component token。

3. [WARN] v4 新 class 未同步註冊到 design-tokens 白名單。
   - 位置：`_規範/design-tokens.md`
   - 影響：`aside-tip`、`layout-mockup`、`today-deliverables`、`micro-cycle`、`task-card`、`learner-output`、`self-check` 等都已實作，但人類規範仍說未列入白名單的自製組件是 BLOCKER。

4. [NIT] `.layout-mockup` mobile 三欄未降階，短文字可用但擴充性弱。
   - 位置：`courses/gen-image/CH2-1.html` `.lm-cells.lm-3col`
   - 證據：Playwright 390px 量測每欄約 88px，無 overflow，但已接近壓縮邊界。

5. [NIT] PRAC3 仍殘留「4 Step」英文語彙。
   - 位置：`courses/gen-image/PRAC3.html` tagline、section heading、intro、exercise list
   - 建議：改「4 步流程」或「步驟 1-4」，維持前次中文化方向。

## 修補優先順序

1. [WARN] 修 CH2-1 `.layout-mockup` `.78rem`，讓 lint 從 39 降到 38，避免新元件帶入已淘汰字階。
2. [WARN] 把 `.layout-mockup` 色彩改成 token 化寫法，或在 design-tokens 補正式 component token 後再引用。
3. [WARN] 在 `_規範/design-tokens.md` 補 v4 互動工作坊組件白名單，至少涵蓋 `aside-tip` 與 `layout-mockup`；最好一併整理 `today-deliverables` / `task-card` / `learner-output` / `self-check`。
4. [NIT] PRAC3「4 Step」改「4 步流程」。
5. [NIT] 視需要加 `.layout-mockup` mobile 規則，保護未來長字串不擠壓。
