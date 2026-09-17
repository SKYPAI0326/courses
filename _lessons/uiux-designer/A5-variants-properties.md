---
slug: uiux-designer
unit_id: A5
title: Variants、Properties 與狀態
course_type: skill-operation
duration: 6h
learning_objective: 能從 A4 的 Login / Heading 主元件建立 Default 與 Error 兩個 Variant，讀懂 Property 與 Value 的關係，在 Instance 切換狀態並保存可追蹤的狀態證據。
prerequisites: [A4]
style_guide: _outlines/uiux-designer.style-guide.md
platform_version: Google Chrome；Figma 網頁版 Starter／Free（Variant property 介面依目前面板實測撰寫）
---

<!--
教案 A5 · Variants、Properties 與狀態

本單元承接 A4 的 `Login / Heading` 主元件與 Instance。學員先保留 Default 狀態，再加入 Error 狀態，使用 Figma 自動建立的 Variant property 管理值；完成後能在 Instance 切換狀態，並把狀態規則交給 A6 的 Button 與 Form。

Figma Starter／Free 的 Variant 建立、Property value 切換與 Variant 命名錯誤已在 Probe A 的 A-06／A-07 實測。真人冷讀、跨帳號重跑與其他 Property 類型（Boolean／Text／Instance swap）仍未放行，本堂只教 Variant property 的狀態切換。
-->

## 教學流程（Teaching Flow）

> **課型：skill-operation**。順序：接手成果 → 概念 → 示範 → 同步操作 → 變因練習 → 驗收與交接。
> **本節完成物：** `Login / Heading` 的 Default／Error component set、一個能切換狀態的 Instance、狀態檢查表與一段回修紀錄。

### 破題 / Hook

登入畫面有兩種工作結果：第一次進入時顯示標題；送出錯誤資料後，標題區要顯示錯誤提示。若兩種畫面各自複製一份，文字、間距和顏色會逐次分叉。這一堂把它們收進同一個 component set，讓使用處只切換狀態值。

**起始材料：** `courses/uiux-designer/assets/A5-variants-properties/START-HERE.html`。
**前置成果：** A4 的 `Login / Heading` 主元件與 `Instance / Login heading`；缺少時先回 A4 重建，不在 A5 重新教 Component。
**交付位置：** 同一個 Figma 檔保留來源 component set、Instance、狀態截圖，並完成 `reference/EXPECTED-CHECK.html`。

### 概念 / Concepts

#### Component set

Component set 把同一個來源的多個 Variant 收在一起。它保留共同結構，也讓每個狀態有清楚的 Value。

#### Variant

Variant 是一個狀態版本。本堂只建立 `Default` 與 `Error`，兩個版本共用登入標題的結構。

#### Property 與 Value

Property 是狀態欄位，Value 是該欄位的一個選項。Figma 可能先顯示 `Property 1`；本堂先用這個欄位完成切換，再將 Value 設為 `Default`、`Error`。若介面允許重新命名，可把 Property 改成 `State`，並在檢查表記錄實際面板名稱。

#### Instance 的狀態切換

Instance 從 component set 取得狀態清單。切換 Value 會換到另一個 Variant；修改共同結構仍要回到主元件。

### 示範 / Demo

示範固定 A4 的 `Login / Heading`。先讓 Default 保持短標題，再建立 Error 版本，把文字換成「帳號或密碼不正確，請檢查後再試一次」。不另教 Button、Form 或 Boolean property。

1. 在 Layers 選取 `Login / Heading` 主元件，確認目前只有一個來源狀態。
2. 執行 `Add variant`，讓 Figma 建立第二個 Variant。
3. 在右側 Property 欄讀取自動建立的 `Property 1`，把兩個 Value 分別整理為 `Default`、`Error`。
4. 若直接把 Variant Layers 命名為 `Error` 出現格式警告，回到 Property value 修改；不要用 Layers 名稱代替 Property。
5. 在 Error Variant 的文字層改成長錯誤訊息，保留 A4 的 Auto Layout 與文字樣式。
6. 切到 Assets 插入或重新選取 `Instance / Login heading`，在 Instance 的 Property 欄切換 `Default`／`Error`。
7. 截圖 component set 的兩個 Value，以及 Instance 顯示 Error 的畫面。

示範完成時，學員能在同一個 Instance 看到兩種狀態，並能指出哪個欄位是 Property、哪個選項是 Value。只看到兩個相似畫面，卻讀不到欄位與值，不能算完成。

### 同步操作 / Together

| 步驟 | 學員動作 | 預期結果 | 快速檢查與修復 |
|---|---|---|---|
| 1 | 開啟 A4 檔與 A5 起始材料，選取 `Login / Heading`。 | Layers 顯示主元件，右側可看到 Component 設定。 | 選到 Instance 時回 Layers 找來源；缺來源就回 A4。 |
| 2 | 執行 `Add variant`。 | 出現第二個 Variant，兩者位於同一個 component set。 | 按鈕不存在時確認選取的是主元件，不是外層 Frame。 |
| 3 | 讀取 `Property 1`，把兩個 Value 整理為 `Default`、`Error`。 | Property 欄有兩個可選狀態。 | 出現格式警告時改 Property value，不改 Layers 顯示名稱。 |
| 4 | 在 Error Variant 的文字層輸入指定錯誤訊息。 | Error 狀態的文字變長，Auto Layout 仍保留。 | 文字被裁切時回文字層確認 Auto height 與容器寬度。 |
| 5 | 選取 Instance，切換 Default／Error。 | 同一個使用處能顯示兩個狀態。 | 切不到值時確認 Instance 來源仍是本檔 component set。 |
| 6 | 截圖主元件的 Property／Value 與 Instance 的 Error 狀態。 | 狀態規則和使用結果各有一份證據。 | 截圖前關閉多餘面板，讓名稱與值同時可讀。 |
| 7 | 填寫完成檢查表，寫下一次錯誤修復。 | A5 成果可交給 A6。 | 先保存 Figma 檔，再補寫檢查表的實際 Property 名稱。 |

**Checkpoint：** 步驟 3 後確認兩個 Value；步驟 5 後確認同一個 Instance 可以切換；兩項都通過才進入自己的變因練習。

### 變因練習 / Solo

複製 `Login / Heading` component set，只改一個主要變因：把 Error Value 的文字換成「驗證碼已過期，請重新取得」，保留 Property 名稱、Default Value、Frame 寬度、Auto Layout 與文字樣式。

請記錄：

1. 新錯誤訊息是否沒有被裁切。
2. Instance 切換到 Error 時，是否仍使用同一個 Property。
3. 哪個位置需要回修，以及回修後 Default 狀態是否未受影響。

不要新增第三個狀態來掩蓋問題；A6 會把狀態規則接到 Button 與 Form。

### 驗收 / Verify

#### 完成條件

- Figma 檔保留 A4 的 `Login / Heading` component set。
- component set 內有 `Default`、`Error` 兩個 Value；Property 名稱依面板記錄為 `State` 或 `Property 1`。
- Error Variant 顯示指定長錯誤訊息，Auto Layout 沒有裁切內容。
- 同一個 Instance 可以在 Default／Error 之間切換，來源關係仍保留。
- 完成檢查表含 Figma 檔連結、Property／Value 截圖、Instance 狀態截圖與一個修正點。

#### 常見錯誤與修復

| 現象 | 原因 | 回修位置 | 重跑起點 |
|---|---|---|---|
| Add variant 後只看到一個來源 | 選到 Instance 或外層 Frame。 | Layers 的主元件選取。 | 步驟 1／2，重新選來源。 |
| Variant 名稱出現格式警告 | 直接把 Layers 名稱當成 Property 語法。 | Property 欄的 Name／Value。 | 步驟 3，改成 `Property 1=Error` 的 Value。 |
| Error 狀態的文字被裁切 | 文字層或父容器仍是 Fixed height。 | Error Variant 的文字層與 Auto Layout。 | 步驟 4，先恢復 Auto height，再檢查寬度。 |
| Instance 沒有 Error 選項 | Instance 不是來自 component set，或尚未重新選取。 | Instance 來源與右側 Property。 | 步驟 5，回 Assets 找本檔來源。 |

#### 檢核題

1. `Property 1` 與 `Error` 的角色各是什麼？
2. 你修改 Error Variant 的長文字後，Default 狀態也變長，先查哪一層？

#### 交接給 A6

保留 component set、兩個 Value、可切換的 Instance 與錯誤修復紀錄。A6 會沿用 `State`／`Property 1` 的狀態欄位，將它接到 Button 與 Form 的可用、錯誤與修正畫面；A6 不會重新建立 Component set。

## 授課前驗證待辦

- [x] 在目前 Figma Starter／Free 與 Chrome 實測 Add variant、Property value 與 Instance 狀態切換；證據在 `PROBE-A.md` 的 A-06／A-07。
- [ ] 用乾淨 Draft 重跑一次，記錄面板名稱與權限差異。
- [ ] 真人冷讀完成，確認學員能從 A4 交接物走到 A5 檢查表。
- [ ] 通過前維持 `MACHINE_READY_PENDING_HUMAN`，不得標示 `READY`。
