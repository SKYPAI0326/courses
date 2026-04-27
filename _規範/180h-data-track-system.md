# 180h ↔ 140h Data-Track 系統 SOP

> 對應 `_報告/2026-04-27-互動性審核.md` §10.2 第 4 條保留項。
> 框架建立 commit：（待 commit hash 填回）。
> 實作版本：v1（2026-04-27）。

## 為什麼有這個系統

`gen-ai-140h` 課程的講義內容是從 180h 實體班遷移而來。140h 班是壓縮版，但既有 HTML 沒有標註哪些段落是「180h 班才有」、哪些是「140h 班可跳」。學員看不出哪些是核心、哪些可緩。

本系統用 `data-track` 屬性對 `<section>`、`<div>` 等 wrapper 標記，讓視覺上清楚誰是核心、誰是可跳、誰是 180h 補充。

## 三種 Track（§10.2 框架本次新增）

| 值 | 視覺 | 何時用 |
|----|------|--------|
| `data-track="140h-core"` | 預設無樣式 | 140h 班必修段落（不必明寫，這是預設值） |
| `data-track="140h-skip"` | 段首「140h 可跳過」灰色膠囊標籤 + 段末灰色虛線 | 140h 班可選跳過、但仍顯示在頁面（不隱藏，給學員選擇） |
| `data-track="180h-extra"` | 左側 3px 虛線 + 「180h 班補充」斜體標籤 | 純 180h 班才有的延伸內容；140h 班視同 bonus |

額外（Phase 3.3 DualPath 既有，本系統一併納入合法值）：

| 值 | 用途 |
|----|------|
| `data-track="basic"` | 基礎章節（pre-test 高分學員可跳） |
| `data-track="advanced"` | 進階章節（pre-test 低分學員緩做） |

5 個值都是合法的。lint 規則 `gen140-track-value`（在 `docs/lint-page.py` 內）會擋非合法值（產 WARN，不擋 commit）。

## 視覺策略：不隱藏內容

⚠ 三種值**都不用 `display:none` 隱藏**。140h 班學員仍看得到 `180h-extra` 段落（避免「藏起來會更難找」），標籤只是讓他知道「這段你可以略過」。

對應 §10.2 評語：「不要只標 skip，還要在 index 與講師指引同步顯示。」

## 套用流程

### 角色：course-designer 或 course-pm

1. 讀 `_講師指引/part{X}.md` 的「180h 建議」欄，找出「180h 多出來的時間放哪」
2. 對照網頁該 PRAC/CH 頁，找出「多出來的段落是哪一段」（通常是某 mini-prac、某延伸案例、或 sp-builder 的進階欄位）
3. 在該段的 `<section>` 或 `<div>` 上加 `data-track="180h-extra"`
4. 對於 140h 已有但可跳過的段落（例：對熟練者太基礎），標 `data-track="140h-skip"`
5. 跑 lint 確認沒違規：

   ```bash
   python3 docs/lint-page.py courses/gen-ai-140h/
   ```

6. commit 訊息引用本 SOP 並說明改了哪幾個段落

### 套用範圍

- **本 commit 不全課套用**（需設計師逐 section 深度判斷，留給 Phase 4 PM 介入）
- 已有 1 個 sample（PRAC1-4 內 sp-builder 的「Few-shot」欄位）作為 pattern
- 目標（後續）：每個 PRAC/CH 平均 1-2 個 `data-track` 標記

## 套用範例（PRAC1-4 sp-builder Few-shot 欄位）

PRAC1-4 的 System Prompt Builder（line 586 附近）共有 6 個欄位：persona / boundary / output / refusal / **fewshot** / **guard**。後兩個是進階配置：Few-shot examples 與 Guardrails。140h 班學員在配置教學時可先停在 4 欄為止；180h 班才完整跑 6 欄。

所以 fewshot 欄位 wrapper：

```html
<div class="sp-field" data-track="180h-extra">
  <label>5. 範例 Few-shot（選填）</label>
  <textarea class="iv-textarea" data-sp="fewshot" rows="3" placeholder="..."></textarea>
</div>
```

> 註：本次只標 1 個 sample。其他欄位（如 guard）、其他 PRAC、其他 CH 待 PM 階段套用。

## CSS 邏輯

樣式定義在 `courses/gen-ai-140h/_assets/interactivity-v1.css` 末段。視覺上：

- `140h-skip`：段首加灰色「可跳過」膠囊標籤
- `180h-extra`：左側 3px 虛線 + 「180h 補充」斜體標籤
- 兩者都**不隱藏內容**

## Lint 規則

`docs/lint-page.py` 內 `check_gen140_track` 函式：

- 抽出頁面所有 `data-track="..."` 值
- 不在合法集合內 → WARN
- 合法集合：`140h-core / 140h-skip / 180h-extra / basic / advanced`

執行：

```bash
python3 docs/lint-page.py courses/gen-ai-140h/
```

合法集合若日後需擴充（例：加 `90h-extra`），同步改 SOP（本檔表格）+ `lint-page.py` 的 `valid` set。

## 變更紀錄

- 2026-04-27 v1 框架建立。CSS + lint rule + 1 sample（PRAC1-4 fewshot 欄位）。後續設計師逐單元套用留 Phase 4。
