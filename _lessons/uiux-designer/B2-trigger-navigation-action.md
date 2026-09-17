---
course: uiux-designer
unit: B2
title: 觸發事件與互動連結
hours: 6h
lesson_type: prototype-operation
prerequisite: B1、A4（能找到兩個具辨識文字的 Frame）
platform: Figma Starter／Free + Chrome
status: MACHINE_READY_PENDING_HUMAN
---

<!--
教案 B2 · 觸發事件與互動連結

本單元使用 B1 的 Flow / Login 與 Flow / List，建立一個可在 Preview 操作的核心 action：On click → Navigate to。操作前先寫 Actual／Expected 與單一 action 邊界；操作後用 Chrome Preview 回歸。Starter 多 action、Variables、Conditional 受方案限制，另立條件紀錄。
-->

## 教學流程（Teaching Flow）

> **課型：prototype-operation**。順序：接手 B1 產物 → 任務與驗收條件 → action 概念 → 示範 → 同步操作 → 單一變因 → 修復與回歸。
> **本節完成物：** 一個獨立 Figma Starter 測試檔、一條 `On click → Navigate to`、Chrome Preview 的 Actual／Expected 紀錄與未測邊界。

## 1. 情境與問題（Hook）

B1 已經有 Login 與 List 兩個畫面，使用者按下「登入」後還停留在原畫面。這時要處理的是一個明確的互動：在 Login 的主要按鈕上觸發一次 Click，預覽後進入 List。

本堂只處理這一條路徑。把多個按鈕與多個去向一次塞進 Starter 檔，會讓方案限制、錯誤來源與回歸結果混在一起；本課程把每個核心 action 放在可單獨檢查的測試檔，並把後續轉場、Overlay、滾動移到各自單元。

## 2. 先理解四個判斷點（Concepts）

| 判斷點 | 要回答的問題 | 本堂證據 |
|---|---|---|
| Trigger | 哪個物件接收 Click／Tap？ | `Button / Login` 被選取；Interaction row 顯示觸發。 |
| Action | 點擊後要做哪件事？ | `Navigate to`，目的地為 `Flow / List`。 |
| Destination | 預覽要到哪個可辨識畫面？ | List Frame 有標題與兩列資料。 |
| 回歸 | Preview 實際看到什麼？ | Actual／Expected、瀏覽器與日期、失敗位置。 |

### 免費方案的工作邊界

- 一個測試檔只驗收一條核心 action，讓問題能回到同一個觸發、目的地或預覽步驟。
- Figma 面板出現多 action、Variables 或 Conditional 方案提示時，截圖並寫入檢查表；不要用替代文字把受限功能寫成已完成。
- `Flow starting point` 是 Preview 入口；它與按鈕的 `Navigate to` action 是兩個獨立證據。

## 3. 示範（Demo）

### 3.1 先寫驗收卡

```
CASE-B2-01｜登入後到清單
Input：B1 的 Flow / Login、Flow / List
Trigger：Button / Login
Expected：點擊一次後 Preview 顯示 Flow / List
限制：此檔只保留一條 action；不設定轉場、Overlay、變數
```

### 3.2 在 Prototype 面板建立 action

1. 複製或另建 B2 測試檔，保留兩個具辨識文字的 Frame。
2. 在 `Flow / Login` 內建立或選取 `Button / Login`。
3. 切換 Prototype 面板，按下節點旁的 `+` 或 `Add action`。
4. 觸發選 `On click`，動作選 `Navigate to`，目的地選 `Flow / List`。
5. 先保留 `Instant`，讓第一次回歸只回答「是否換到正確畫面」。
6. 開啟 Preview，點擊一次 Login 按鈕，記錄 Actual 與 Expected。
7. 截圖包含 Interaction row、目的地名稱與 Preview 的 List 內容。

### 示範的判斷

畫面上有兩個 Frame，只證明素材存在；Interaction row 才是 action 設定證據；Preview 的 List 畫面才是行為回歸證據。三者要放在同一份 CASE-B2-01 紀錄裡。

## 4. 跟著做（Together）

| 步驟 | 學員動作 | 應看到的結果 | 沒看到時的回修 |
|---:|---|---|---|
| 1 | 開啟 B2 起始材料與 B1 檢查表，建立 `CASE-B2-01`。 | Input、Trigger、Expected、限制都寫好。 | 回 B1 確認兩個 Frame 名稱與起始點。 |
| 2 | 建立獨立測試檔，放入 Login／List 兩個可辨識 Frame。 | 畫布有兩個 Frame，文字不再是空白占位。 | 重新匯入或複製 B1 Frame；不要在空白 Frame 上猜 Preview。 |
| 3 | 在 Login 放置或選取 `Button / Login`。 | Layers 可找到按鈕，畫布能辨識它是主要操作。 | 回 A6 檢查 Button 名稱與選取層級。 |
| 4 | 開 Prototype，按 `Add action`。 | Interaction row 出現。 | 確認選的是 Button／Instance，不是外層 Frame。 |
| 5 | 設定 `On click → Navigate to → Flow / List`。 | row 顯示觸發與目的地。 | 重新選目的地；若看不到 List，檢查 Frame 是否同一頁。 |
| 6 | 保留 `Instant`，開 Preview，按一次 Login。 | Preview 顯示 List 標題與兩列資料。 | 檢查起始點、按鈕選取與目的地文字。 |
| 7 | 填寫 Actual／Expected，保存三類截圖。 | 互動設定、目的地、預覽結果各有證據。 | 補拍缺少的 row 或畫面；不要只寫「可以」。 |

> **Checkpoint 1**：你能在同一份紀錄中指出 Trigger、Action、Destination；Preview 點擊一次後確實看到 List。

## 5. 自己改一個條件（Solo）

複製 B2 測試檔，保留一條 action，只替換 List Frame 的標題為「待處理申請」。

1. 不改 Trigger、Action、Destination 與起始點。
2. 開 Preview，點擊 Login 一次。
3. 記錄 Actual 是否讀到「待處理申請」，以及兩列資料是否仍然可辨識。
4. 若改動文字後目的地消失，回到 Layers 查找是否誤刪或移動了 List Frame。

> **Checkpoint 2**：Solo 版本仍只有一條 Navigate action；Preview 顯示新標題；檢查表保留原版與修改版的檔案／截圖位置。

## 6. 卡住時怎麼回修

| 現象 | 可能原因 | 回修位置 | 重跑起點 |
|---|---|---|---|
| 點擊沒有反應 | action 建在外層 Frame 或尚未設定 Trigger。 | Layers、Prototype Interaction row。 | 回第 3／4 步。 |
| 目的地清單找不到 List | List 不是同一頁的 Frame，或名稱不清楚。 | Layers 與 Frame 名稱。 | 回第 2／5 步。 |
| Preview 顯示空白頁 | Destination 是空 Frame，或沒有可辨識文字。 | List Frame 內容。 | 回第 2／6 步。 |
| Preview 一開始就顯示 List | Flow starting point 放錯位置。 | Prototype 起始標記。 | 回第 6 步前先重設 Login。 |
| 第二次新增 action 出現方案提示 | Starter 的多 action 限制。 | 方案訊息截圖與 CASE 限制欄。 | 保留第一條 action，另開測試檔。 |
| Solo 改標題後按鈕不見 | 修改時選到整個 Frame 或移動了層級。 | Layers 與畫布。 | 回 Solo 第 1 步，重新複製乾淨版本。 |

把現象、回修位置與重跑結果寫入<a href="../courses/uiux-designer/assets/B2-trigger-navigation-action/reference/EXPECTED-CHECK.html">B2 完成檢查表</a>。轉場、Overlay、Swap、滾動與多步驟流程寫入待測欄，留給後續單元。

## 7. 驗收與交接（Verify）

- B2 測試檔含具辨識文字的 Login／List Frame。
- `Button / Login` 是實際 Trigger，Interaction row 顯示 `On click → Navigate to → Flow / List`。
- Preview 以指定起始點開始，點擊一次後看到 List 標題與兩列資料。
- CASE-B2-01 有 Actual／Expected、瀏覽器／日期與三類截圖位置。
- Solo 版本只改一個條件，仍保留單一 action 與可讀目的地。
- 多 action、Variables、Conditional、轉場、Overlay、Swap、滾動均列為尚未測試或後續單元。

### 交給 B3／B4

保留 B2 的 Interaction row、Preview 截圖與回歸紀錄。B3 使用同一條 Navigate action 選擇有目的的轉場；B4 使用 A8 的 Dialog 建立獨立 Overlay 測試。每個單元都要保留自己的行為證據。

### 課前驗證待辦

- [ ] 由另一位學員只看本頁與起始材料，完成一次單一 action 冷讀。
- [ ] 以不同 Figma 帳號重做，記錄 Prototype 面板與 Starter 限制差異。
- [ ] 不把第二 action、Variables 或 Conditional 的方案提示當成通過證據。
