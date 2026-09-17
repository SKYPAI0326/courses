---
course: uiux-designer
status: PASS1_MACHINE_EVIDENCE
source_matrix: 99h-coverage-matrix.md
---

# Coverage Ledger Pass 1：正式項目到原子證據

Pass 1 先鎖定「要教什麼、要留下什麼證據」，不因目前寫不出 HTML 就刪除正式項目。`MACHINE_PASS` 代表平台操作已看到結果，不代表真人學員已理解。

## Part A：42h

| Atom | 正式項目 | 操作 ID | 必須完成物 | 目前狀態 | 證據／缺口 |
|---|---|---|---|---|---|
| A-42-01 | 色彩系統 | OP-A09／視覺規格待建 | token 表與用途判斷 | `NOT_RUN` | Probe 未測顏色角色；需教案夾具 |
| A-42-02 | 字型系統 | OP-A09／長文字 | scale、行高、長文字檢查 | `MACHINE_PASS_PARTIAL` | 長中文換行已見；字型 scale 待測 |
| A-42-03 | 格線系統 | OP-A01–A03 | 手機／桌機格線 | `MACHINE_PASS_PARTIAL` | Frame 已測；格線規格待建 |
| A-42-04 | Auto Layout | OP-A03、A04、A09、A10 | 內容壓力畫面 | `MACHINE_PASS` | PROBE-A |
| A-42-05 | Component | OP-A05、A06 | 主元件與 Instance | `MACHINE_PASS` | PROBE-A |
| A-42-06 | Button | OP-A11 | Button 狀態矩陣 | `CONDITIONAL` | 目前只通過視覺模式 |
| A-42-07 | Form | OP-A09 | 輸入／錯誤／修正 | `NOT_RUN` | Probe A 待補多欄位 |
| A-42-08 | List | OP-A12 | 多列／空／錯誤狀態 | `CONDITIONAL` | 只建 Error helper，未測多列增刪 |
| A-42-09 | Toast | — | 狀態規格與範例 | `NOT_RUN` | 待建立夾具 |
| A-42-10 | Dialog | OP-B04 | 視覺結構與關閉規則 | `MACHINE_PASS_PARTIAL` | Overlay 預覽有文字；關閉待測 |
| A-42-11 | Navigation | OP-B03／B05 | 導覽視覺與置頂規則 | `MACHINE_PASS_PARTIAL` | Overflow 選項已測；固定導覽待測 |
| A-42-12 | Variants | OP-A07、A08 | property 與狀態表 | `MACHINE_PASS_WITH_REPAIR` | Variant 命名警告已記錄 |

## Part B：57h

| Atom | 正式項目 | 操作 ID | 必須完成物 | 目前狀態 | 證據／缺口 |
|---|---|---|---|---|---|
| B-57-01 | 線框／原型／工具／手機介面／元件／動畫基礎 | OP-B01 | 任務、畫面清單、入口 | `MACHINE_PASS_PARTIAL` | B1 教案、學員頁、起始材料與檢查表已建；起始點機器證據完成，真人冷讀待做 |
| B-57-02 | 觸發事件與互動連結 | OP-B02、B03 | 一個核心 action | `CONDITIONAL` | B2 教案、學員頁、起始材料與檢查表已建；一檔一 action，Starter 第二 action 受限 |
| B-57-03 | 互動與轉場 | OP-B06 | 轉場選擇表與 Preview | `MACHINE_PASS_PARTIAL` | B3 教案、學員頁、起始材料與檢查表已建；Animation 選項已確認，Smart animate 完整動態待測 |
| B-57-04 | Overlay 基礎／進階 | OP-B04 | 單一 Overlay Preview | `MACHINE_PASS` | Chrome Preview 顯示確認完成 |
| B-57-05 | Swap＋Overlay | — | Swap 任務檔 | `NOT_RUN` | Starter 拆檔策略待測 |
| B-57-06 | 滾動／置頂／漂浮按鈕 | OP-B05 | Vertical overflow 與固定元素 | `CONDITIONAL` | 選項已測，聯合 Preview 待測 |
| B-57-07 | Smart Animation | OP-B06 | 成功／失敗修復紀錄 | `MACHINE_PASS_PARTIAL` | 選項已測，匹配雙畫面待測 |
| B-57-08 | Figma／PS 發布與輸出 | OP-B07–B09 | PNG／PDF／Inspect／Handoff | `MACHINE_PASS_PARTIAL` | Figma export／Inspect 通過；Photoshop待測 |
| B-57-09 | 網頁入門與雲端部署 | OP-B10 | HTML/CSS/JS、Git、部署 | `CONDITIONAL` | 本地 Git／origin 已確認；push／部署未執行 |

## Ledger 使用規則

- `CONDITIONAL` 不得在 learner-facing HTML 寫成「一定可用」；必須就近顯示方案或拆檔條件。
- `NOT_RUN` 項目可以先寫成待測教案，但不能成為機器可交付的完成物。
- Pass 2 必須把每一列回填到教案段落、素材檔、HTML 錨點與實際證據；若證據不足，狀態退回 `BLOCK` 或 `NOT_RUN`。

## 代表鏈回填（機器階段）

| Atom | learner-facing 教案／HTML | 新增產物 | 判定 |
|---|---|---|---|
| A-42-04 | `../_lessons/uiux-designer/A3-auto-layout-pressure.md`／`part1/CH3-auto-layout-pressure.html` | 長中文壓力、固定寬度 200、Auto height、修復摘要 | `MACHINE_PASS_PARTIAL` |
| B-57-04 | `../_lessons/uiux-designer/B4-overlay-single-action.md`／`part2/CH4-overlay-single-action.html` | Overlay／Swap 測試檔、Preview、來源／目的地、對照 PNG | `MACHINE_PASS_PENDING_HUMAN` |
| B-57-05 | `../_lessons/uiux-designer/B5-scroll-fixed-floating.md`／`part2/CH5-scroll-fixed-floating.html` | `SCROLL-01`、Vertical overflow、上滑 Expected／Actual、固定／漂浮檢查表 | `MACHINE_PASS_PENDING_HUMAN` |
| B-57-04 → B6 測試 | `../_lessons/uiux-designer/B6-prototype-task-test.md`／`part2/CH6-prototype-task-test.html` | 任務腳本、Actual／Expected、回歸紀錄 | `MACHINE_PASS_PENDING_HUMAN` |
| B-57-08 | `../_lessons/uiux-designer/B7-figma-handoff-export.md`／`part2/CH7-figma-handoff-export.html` | PNG／PDF／Inspect、Handoff 清單 | `MACHINE_PASS_PENDING_HUMAN` |
| B-57-09 | `../_lessons/uiux-designer/B8-web-git-deploy.md`／`part3/CH8-web-git-deploy.html` | `web-starter/` 本機網頁、Git diff／commit 路徑 | `MACHINE_PASS_PENDING_HUMAN`（GitHub／部署未跑） |

這些列證明產物鏈可被機器追蹤，但不解鎖未測的 Photoshop、Swap、固定元素聯合滾動、GitHub push 或公開部署。
