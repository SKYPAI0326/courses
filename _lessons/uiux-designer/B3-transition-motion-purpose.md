---
course: uiux-designer
unit: B3
title: 常見轉場與動效目的
hours: 6h
lesson_type: prototype-operation
prerequisite: B2（已有一條可回歸的 Navigate action）
platform: Figma Starter／Free + Chrome
status: MACHINE_READY_PENDING_HUMAN
---

<!--
教案 B3 · 常見轉場與動效目的

本單元沿用 B2 的一條 Navigate action，先用任務目的選擇轉場，再在 Figma 面板設定一種 Animation，並記錄 Preview 的實際觀察。Probe B B-05 已確認 Instant、Dissolve、Smart animate、Move in、Move out、Push、Slide in、Slide out 等選項存在；Smart animate 的圖層匹配與動態效果仍需人工回歸。
-->

## 教學流程（Teaching Flow）

> **課型：prototype-operation**。順序：接手 B2 action → 動效問題 → 選擇規則 → 示範 → 同步操作 → 單一變因 → 回修與驗收。
> **本節完成物：** 一份轉場選擇表、一條設定好的 Animation、Preview 的觀察紀錄與 `MACHINE_PASS_PARTIAL` 邊界說明。

## 1. 情境與問題（Hook）

B2 的 Login → List 已經能到達目的地，但兩個畫面瞬間切換時，使用者不一定知道發生了什麼。轉場需要服務任務：短距離的確認可以保持快速；需要提示空間關係時，可以使用方向；兩個畫面有相同層級與命名時，才有條件評估 Smart animate。

本堂不追求把所有下拉選項都套過一遍。你要留下選擇理由，並把「面板有這個選項」與「Preview 動態符合預期」分成兩筆證據。

## 2. 先理解三個判斷點（Concepts）

| 判斷點 | 問題 | 可留下的證據 |
|---|---|---|
| 任務目的 | 使用者需要快速確認、看見方向，還是看見同一物件的狀態變化？ | `MOTION-01` 選擇理由。 |
| Animation | 面板目前提供哪個設定？ | Interaction row 的 Animation 欄位截圖。 |
| 實際效果 | Preview 中速度、方向與內容是否符合預期？ | Actual／Expected 與錄影或截圖；若沒測就寫 `NOT_RUN`。 |

### 選擇表

| 任務目的 | 優先試的設定 | 檢查重點 |
|---|---|---|
| 只要快速到達下一頁 | `Instant` | 操作回應快，沒有多餘裝飾。 |
| 需要柔和的畫面替換 | `Dissolve` | 內容是否仍能辨識，速度是否造成等待感。 |
| 需要呈現同一物件的位移或狀態變化 | `Smart animate` | 兩畫面層級、名稱與可匹配的物件是否一致。 |
| 下一頁從側邊進入 | `Move in`／`Push` | 方向是否與流程方向一致，是否遮住主要內容。 |

## 3. 示範（Demo）

### 3.1 寫動效選擇卡

```
MOTION-01｜登入後顯示清單
來源：B2 Button / Login → Flow / List
任務目的：讓使用者知道已離開登入頁，快速看見待處理資料
初始選擇：Dissolve（待 Preview 回歸）
比較設定：Instant
未測項目：Smart animate 的匹配效果
```

### 3.2 設定並記錄

1. 開啟 B2 測試檔的 Interaction row，保留 Trigger 與 Destination。
2. 在 Animation 選單選 `Dissolve`，保留可讀的速度設定。
3. 截圖顯示 Animation 值與目的地，填入選擇表。
4. 從起始點開 Preview，依 B2 的同一腳本點擊一次。
5. 把 Expected（淡入切換、內容可辨識）與 Actual（實際看見的畫面）分開記錄。
6. 再複製測試檔改為 `Instant`，只比較速度感，不改 Trigger 或 Destination。

### 示範的判斷

面板的下拉值是設定證據；Preview 的速度、方向與內容閱讀才是行為證據。若沒有錄影或人工觀察，不把 Smart animate 的效果寫成已通過。

## 4. 跟著做（Together）

| 步驟 | 學員動作 | 應看到的結果 | 沒看到時的回修 |
|---:|---|---|---|
| 1 | 複製 B2 測試檔，建立 `MOTION-01`。 | Trigger／Destination 與 B2 一致。 | 回 B2 先確認 action 可回歸。 |
| 2 | 寫任務目的與初始選擇。 | 選擇表有理由，不只填功能名稱。 | 回第 2 節用任務目的重寫。 |
| 3 | 在 Animation 選單選 `Dissolve`。 | Interaction row 顯示 Dissolve。 | 重新選取 action row，不要選到 Frame。 |
| 4 | 截圖 Animation、目的地與速度欄位。 | 設定證據可被接手者讀取。 | 展開互動設定，再補拍整列資訊。 |
| 5 | 開 Preview，從 Login 點擊一次。 | 看到 List，並可觀察切換感受。 | 先確認起始點、Trigger、Destination。 |
| 6 | 寫 Expected／Actual 與一個觀察。 | 設定與實際結果分開。 | 若沒有觀察，標記 `NOT_RUN`，不要猜測。 |
| 7 | 複製版本改成 `Instant`，只比較速度。 | 第二份紀錄仍只有一條 action。 | 重新複製 B2 乾淨版本。 |

> **Checkpoint 1**：你能解釋選擇 Dissolve 的任務理由，指出 Animation 欄位，並在 Preview 紀錄實際觀察。

## 5. 自己改一個條件（Solo）

複製 `MOTION-01`，把 Animation 改為 `Smart animate`，保留 B2 的 Trigger、Destination 與兩個畫面內容。

1. 記錄兩個畫面中可匹配的層級名稱，例如相同的 Header 或 List title。
2. 截圖 Smart animate 的面板選項。
3. 開 Preview，寫下實際是否看見連續位移、淡入或其他效果；看不到時填 `NOT_RUN` 或 `MACHINE_PASS_PARTIAL`，並說明原因。
4. 回到選擇表，判斷 Smart animate 是否值得保留，理由要連到任務目的。

> **Checkpoint 2**：Solo 版本沒有改 Trigger 或 Destination；Smart animate 的設定證據、匹配層名稱與 Preview 實際結果分開保存。

## 6. 卡住時怎麼回修

| 現象 | 可能原因 | 回修位置 | 重跑起點 |
|---|---|---|---|
| 找不到 Animation 選單 | 選到 Frame 或起始點，不是 Interaction row。 | Prototype 面板。 | 回第 3 步。 |
| 設定有 Dissolve，Preview 卻沒有到 List | B2 的 Trigger 或 Destination 已被改動。 | Interaction row／起始點。 | 回 B2 的 CASE-B2-01。 |
| Smart animate 只顯示瞬間切換 | 層級名稱或結構沒有匹配，或尚未人工回歸。 | 兩個 Frame 的 Layers、Preview 紀錄。 | 回 Solo 第 1／3 步。 |
| 轉場讓人找不到目前位置 | 方向與任務流程不一致，或速度過慢。 | 動效選擇表、Preview Actual。 | 回第 2／6 步重選。 |
| 兩個版本一起出現多個 action | 複製時把不需要的互動帶入。 | Interaction row。 | 回 B2 乾淨測試檔重新複製。 |

把現象、回修位置與重跑結果寫入<a href="../courses/uiux-designer/assets/B3-transition-motion-purpose/reference/EXPECTED-CHECK.html">B3 完成檢查表</a>。Smart animate 效果、固定元素與多步驟串接仍需後續測試。

## 7. 驗收與交接（Verify）

- `MOTION-01` 含任務目的、初始選擇與比較設定。
- Interaction row 顯示一個 Animation 值，Trigger／Destination 沒有被改動。
- Dissolve 或 Instant 的 Preview 有 Expected／Actual 紀錄；沒有觀察的項目標為 `NOT_RUN`。
- Solo Smart animate 版本有面板截圖、匹配層名稱與 Preview 實際結果。
- 選擇理由與任務流程有關，不以「看起來比較酷」作為唯一理由。
- Smart animate 效果、Overlay、Swap、滾動、固定與多 action 均列為後續範圍。

### 交給 B4／B6

保留 B3 的 action、轉場選擇表與 Preview 紀錄。B4 使用 A8 的 Dialog 做單一 Overlay；B6 會把可回歸互動放進任務測試表。任何未通過的動效先保留失敗紀錄，再決定是否修正。

### 課前驗證待辦

- [ ] 由另一位學員只看本頁完成一次轉場選擇與回歸。
- [ ] 以不同 Figma 帳號重做，記錄 Animation 選項與方案差異。
- [ ] 用兩個有相同層級名稱的 Frame 實際檢查 Smart animate，再決定是否放行效果敘述。
