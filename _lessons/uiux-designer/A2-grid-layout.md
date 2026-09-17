---
slug: uiux-designer
unit_id: A2
title: 格線與版面基準
course_type: skill-operation
duration: 6h
learning_objective: 能沿用 A1 的色彩與文字規則，在 Figma 建立手機與桌機格線，檢查欄數、邊界、欄間距與縮窄後的內容位置，並把手機 Frame 交給下一堂。
prerequisites: [A1]
style_guide: _outlines/uiux-designer.style-guide.md
platform_version: Google Chrome；Figma 網頁版 Starter／Free（Columns 面板以 Count、Stretch、Offset、Gutter 設定格線）
---

<!--
教案 A2 · 格線與版面基準

本單元承接 A1 的 `Visual foundations` 頁面與樣式名稱。學員建立 `Grid foundations` 頁面，完成 402×874 手機 Frame、1440×900 桌機 Frame，並用欄數、Offset（設計上的左右 Margin）、Gutter 與安全邊界檢查標題和列表的位置。成果會交給 A3，作為 Auto Layout 的父層與內容壓力測試輸入。

Layout guide、Columns、Frame 尺寸與縮窄後的格線結果已在 Figma Starter／Free＋Chrome 測到；Columns 的左右邊界要以 `Stretch` 模式下的 `Offset` 輸入，學員仍要自行讀取面板並完成對齊檢查。真人冷讀與跨帳號重跑前，維持 MACHINE_READY_PENDING_HUMAN。
-->

## 教學流程（Teaching Flow）

> **課型：skill-operation**。順序：接手成果 → 概念 → 示範 → 同步操作 → 變因練習 → 驗收與交接。
> **本節完成物：** `Grid foundations` Figma 頁面、手機／桌機格線設定、對齊截圖與縮窄觀察紀錄。

### 破題 / Hook

阿凱把登入與內容列表放進手機和桌機畫面。每個區塊都從不同位置開始，標題與列表沒有共同左線；下一堂要把內容放進 Auto Layout 時，也找不到穩定的父層邊界。

這一堂先把「看起來差不多」改成可以重讀的數值。你要建立兩個 Frame，讓不同寬度的畫面各自有欄數、左右邊界與欄間距，並在手機縮窄後重新檢查內容是否仍在安全區。

**起始材料：** `courses/uiux-designer/assets/A2-grid-layout/START-HERE.html`。
**前置成果：** A1 的 `Visual foundations` 頁面、`color-*` 色彩角色與 `type-*` 文字樣式；缺少時先回 A1 補齊。
**交付位置：** 同一個 Figma 檔新增 `Grid foundations` 頁面，完成檢查填入 `reference/EXPECTED-CHECK.html`。

### 概念 / Concepts

#### Frame／畫板

Frame 是承載畫面內容與版面規則的容器。尺寸先固定，格線才有可比較的範圍。

#### Columns／欄

欄是內容可以跨越的垂直區域。欄數決定同一個畫面能有幾個共同對齊的落點。

#### Margin／左右邊界

Margin 是內容離 Frame 左右邊緣的距離。它把文字與元件留在可讀區，不讓內容貼住邊緣。在 Figma 的 Columns／Stretch 設定中，這個左右邊界會填在 `Offset`；本課把設計概念稱為 Margin，把操作欄位稱為 Offset。

#### Gutter／欄間距

Gutter 是兩欄之間的空隙。它保持相鄰內容的距離一致，避免每一區塊自行猜間距。

#### 安全邊界

安全邊界是內容不能跨過的左右範圍。Frame 縮窄、文字變長或列表增加時，都要重新讀取這條界線。

### 示範 / Demo

示範固定兩組輸入：手機 402×874、4 欄、Stretch、16 px Offset（左右 Margin）、16 px Gutter；桌機 1440×900、12 欄、Stretch、80 px Offset、24 px Gutter。兩個 Frame 都沿用 A1 的色彩與文字樣式。

1. 建立頁面 `Grid foundations`，新增 402×874 Frame，命名 `Mobile / Login & List`。
2. 在 Layout guide 新增 Columns，選 `Stretch`，填入 Count 4、Offset 16、Gutter 16。
3. 放入標題與列表區塊，讓兩者左邊落在同一條欄線。
4. 新增 1440×900 Frame，命名 `Desktop / Login & List`，填入 Count 12、Offset 80、Gutter 24。
5. 把同一個標題與列表區塊放到桌機 Frame，檢查是否仍沿用共同左線。
6. 截圖兩個 Frame 的格線面板與內容位置，記錄 Count、Offset、Gutter 與 Frame 尺寸。

示範完成時，學員能從 Layers 找到兩個 Frame，也能在右側面板讀到欄數、Offset 與 Gutter。單看畫面位置但讀不到設定值，不能算完成。

### 同步操作 / Together

| 步驟 | 學員動作 | 預期結果 | 快速檢查 | 卡住時的回修 |
|---|---|---|---|---|
| 1 | 開啟 A1 檢查表與 A2 起始材料，在 Figma 新增 `Grid foundations` 頁面。 | Pages 區可找到新頁面，A1 樣式仍可用。 | 重新點選 A1 的文字層，確認 `type-*` 樣式仍在。 | 回 A1 檢查表補齊樣式，不在 A2 另建相同名稱。 |
| 2 | 建立 402×874 Frame，命名 `Mobile / Login & List`。 | Layers 有可讀的手機 Frame。 | 讀右側 W/H 是否為 402／874。 | 先在 Layers 選 Frame row，再改尺寸與名稱。 |
| 3 | 新增 Columns 格線，選 `Stretch`，設定 Count 4、Offset 16、Gutter 16。 | 四欄平均分布，左右各留 16 px。 | 重新選取 Frame，讀 Count、Offset、Gutter。 | 確認格線類型是 Columns；若看到的是 Grid，先切換類型，再重填三個值。 |
| 4 | 放入 A1 的標題與一個列表區塊，讓左邊對齊同一條欄線。 | 兩個區塊共享左線，未跨出 Margin。 | 關閉格線後仍能看出兩個區塊同線。 | 開回格線，先移動標題，再移動列表；不要一次拖兩個物件猜位置。 |
| 5 | 建立 1440×900 Frame，命名 `Desktop / Login & List`，選 `Stretch`，設定 Count 12、Offset 80、Gutter 24。 | 十二欄平均分布，內容區離邊緣 80 px。 | W/H、Count、Offset、Gutter 都能從面板讀到。 | 檢查 Offset 與 Gutter 是否對調，從數值欄重新填寫。 |
| 6 | 複製標題與列表到桌機 Frame，依欄線重新放置。 | 桌機兩個區塊共享左線，使用同一套色彩與文字樣式。 | 點選文字層，確認沒有另建一套樣式。 | 回 A1 頁面尋找樣式；不要把顏色或字級改成局部值。 |
| 7 | 截圖兩個 Frame 的格線面板與內容對齊位置，填入完成檢查表。 | 有可交接的數值與畫面證據。 | 關閉再開啟 Figma 檔，能找到兩個 Frame。 | 先保存 Figma 檔，再補寫檢查表；缺數值就回對應 Frame 重讀。 |

**Checkpoint：** 步驟 3 後確認手機格線的三個值；步驟 5 後確認桌機三個值；兩者都通過才進入縮窄練習。

### 變因練習 / Solo

複製手機 Frame，只改一個條件：把寬度從 402 改成 360。保留 4 欄、16 px Offset、16 px Gutter、A1 文字樣式與標題／列表內容。

請記錄：

1. 標題與列表是否仍在左右安全邊界內。
2. 兩個區塊是否仍共享左線。
3. 哪一個文字或間距先出現壓力。
4. 你修正了哪一個位置，修正後的 Frame 與格線數值是否仍可讀。

不要直接刪除內容來讓畫面看起來整齊；要保留縮窄前後截圖，讓 A3 能接手同一個手機 Frame 做 Auto Layout 壓力測試。

### 驗收 / Verify

#### 完成條件

- Figma 頁面名為 `Grid foundations`。
- 手機 Frame 為 402×874、4 欄、Stretch、16 px Offset、16 px Gutter。
- 桌機 Frame 為 1440×900、12 欄、Stretch、80 px Offset、24 px Gutter。
- 標題與列表在兩個 Frame 都有共同左線，沒有跨出左右安全邊界。
- 360 px 縮窄版本保留內容與格線規則，並有前後觀察紀錄。
- 完成檢查表含 Figma 連結、面板截圖、數值與一個修正點。

#### 常見錯誤與修復

| 現象 | 原因 | 回修位置 | 重跑起點 |
|---|---|---|---|
| 四欄看起來不平均 | 格線類型不是 Columns，或 Count 仍是預設值。 | Layout guide 的類型與 Count。 | 步驟 3，重新讀取四欄結果。 |
| 內容貼住 Frame 邊緣 | Offset 填成 0，或物件沒有對齊欄線。 | Offset 與物件 X 位置。 | 步驟 3／4，先修數值再調物件。 |
| 桌機的標題與列表左線不同 | 複製後用畫布目測，沒有沿用共同欄線。 | 桌機 Frame 的欄線與兩個物件位置。 | 步驟 6，分別選取兩個物件重對齊。 |
| 360 px 版本把文字刪掉才放得下 | 用刪除內容掩蓋窄版壓力。 | Frame 寬度、Offset、文字框位置。 | Solo 練習，保留原文字再調整版面。 |

#### 檢核題

1. Margin 與 Gutter 都是間距數值，它們分別回答哪一個版面問題？
2. 360 px 版本仍在安全邊界內，但標題與列表沒有共同左線，你會先修數值還是物件位置？為什麼？

#### 交接給 A3

保留 `Mobile / Login & List`、`Desktop / Login & List`、格線設定與縮窄紀錄。A3 會使用手機 Frame 與 A1 的文字樣式，將長錯誤訊息放入內容容器，檢查 Auto Layout 是否能跟著內容增高；A3 不會重新決定手機格線的欄數與 Offset。

## 授課前驗證待辦

- [x] 在目前 Figma Starter／Free 與 Chrome 實際重跑 Layout guide、Columns、Offset、Gutter；已記錄於 `PROBE-A.md` 的 A-13。
- [ ] 用新帳號或乾淨 Draft 重跑一次，記錄面板名稱與方案限制。
- [x] 在 Probe A 將手機 Frame 從 402 px 縮窄至 360 px；Layout guide 保留，文字仍在 Frame 內（A-14）。
- [ ] 真人冷讀完成，確認學員能從 A1 交接物走到 A2 檢查表。
- [ ] 通過前維持 `MACHINE_READY_PENDING_HUMAN`，不得標示 `READY`。
