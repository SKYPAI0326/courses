---
course: uiux-designer
unit: A7
title: List 與內容變化
hours: 4h
lesson_type: skill-operation
prerequisite: A6
platform: Figma Starter／Free + Chrome
status: MACHINE_READY_PENDING_HUMAN
---

<!--
教案 A7 · List 與內容變化

本單元承接 A6 的 Button／Form 圖層與內容壓力。學員建立兩個可辨識的 List row，加入長標題與空狀態提示，再用固定寬度與 Auto height 檢查內容變長後的版面。Probe A 的 A-17～A-19 已確認視覺列、長文字與空狀態圖層可在 Starter／Free 建立。

本堂的完成條件集中在視覺結構、命名與內容壓力；動態資料、真正的增刪按鈕、資料切換與多列聯合滾動要在後續 Prototype／測試 Gate 補測。
-->

## 教學流程（Teaching Flow）

> **課型：skill-operation**。順序：接手成果 → 情境 → 概念 → 示範 → 同步操作 → 變因練習 → 驗收與交接。
> **本節完成物：** `List / Item / Row 01`、`Row 02`、長標題、`List / Empty / Message` 與內容壓力紀錄。

## 1. 情境與問題（Hook）

登入後的清單畫面會遇到三種內容：有資料時要讀得快、標題變長時不能遮住下一列、沒有資料時要讓使用者知道下一步。畫面只放一個灰色矩形，下一位工作者無法判斷它是列、空狀態還是按鈕。

這一堂把每個結果留在 Layers 可讀的名稱，並用一個長標題改變內容高度。你會得到一份能交給 A8 的視覺清單規格；資料更新與互動流程留到 Prototype 階段。

## 2. 先理解三個判斷點（Concepts）

| 判斷點 | 你要回答的問題 | 本堂證據 |
|---|---|---|
| Row 結構 | 清單中的一筆資料由哪個層級承載？ | Layers 有 `List / Item / Row 01`、`Row 02`。 |
| 內容壓力 | 標題變長時，哪個尺寸跟著內容變化？ | `List / Item / Title` 寬 180、Auto height、文字換行。 |
| 空狀態 | 沒有列時，畫面要顯示什麼訊息？ | Layers 有 `List / Empty / Message`，文字為「目前沒有清單項目」。 |

### 名稱規則

- `List / Item / Row 01` 與 `Row 02` 表示兩筆視覺列。
- `List / Item / Title` 表示列中的標題文字層。
- `List / Empty / Message` 表示沒有資料時的提示層。
- 名稱能協助交接與檢查；名稱本身不會產生資料，也不會自動控制顯示條件。

## 3. 示範（Demo）

示範沿用 A6 的 `Screen / List Top` Frame。先畫一列，再複製成第二列；接著建立長標題與空狀態提示。每一步都在 Layers 或右側面板確認。

1. 在清單區域建立 `300×40` Rectangle，命名 `List / Item / Row 01`。
2. 複製 Row 01，將副本命名 `List / Item / Row 02`，讓兩列在畫布上保持可辨識的間距。
3. 建立文字層 `List / Item / Title`，輸入「這是一段需要在清單項目中換行的長標題」。
4. 把 Title 設為 Fixed width，寬度輸入 `180`；再選 Auto height。
5. 觀察右側 Height 與畫布換行結果，截圖前後差異。
6. 建立文字層 `List / Empty / Message`，輸入「目前沒有清單項目」。
7. 截圖 Layers、Title 的 W/H、空狀態文字，填入 A7 完成檢查表。

### 示範的判斷

Row 01 與 Row 02 是兩個視覺列；長標題是內容壓力材料；Empty Message 是另一種畫面狀態。這些圖層能被找到、能被重讀，才有交接價值。

## 4. 跟著做（Together）

每完成一列就停下來讀取預期結果。沒看到時，先在同一個步驟修復。

| 步驟 | 學員動作 | 預期結果 | 快速檢查 | 卡住時的回修 |
|---:|---|---|---|---|
| 1 | 開啟 A6 檔與 A7 起始材料，選取 `Screen / List Top`。 | Frame 與 A6 Button／Form 仍可找到。 | Layers 的父層正確。 | 回 A6 檢查檔案與 Frame 名稱。 |
| 2 | 建立 300×40 Rectangle，命名 `List / Item / Row 01`。 | Layers 顯示 Row 01。 | 讀右側 W/H。 | 重新選 Rectangle，再改名稱與尺寸。 |
| 3 | 複製 Row 01，命名 `List / Item / Row 02`。 | Layers 有兩列，畫布位置可分辨。 | 選兩列確認名稱不同。 | 選副本重新命名；不要改掉來源列。 |
| 4 | 建立 `List / Item / Title`，輸入長標題。 | Layers 顯示 Title，畫布出現文字。 | 文字內容與 Layers 名稱分開確認。 | 選文字層，從右側 Content 重填。 |
| 5 | 將 Title 設為 Fixed width 180、Auto height。 | 文字換行，Height 隨內容變為 30 左右。 | 讀取 W/H 與文字是否被裁切。 | 先選 Auto height，再重填 Width 180。 |
| 6 | 建立 `List / Empty / Message`，輸入空狀態文字。 | Layers 有 Empty Message。 | 文字清楚且未與 Row 重疊。 | 移到清單區域外暫存，再重新排列。 |
| 7 | 填寫檢查表，保存截圖與修正紀錄。 | 交付物可被下一堂找到。 | 有 Layers、W/H、空狀態三類證據。 | 逐項補拍，不能只寫「已完成」。 |

> **Checkpoint 1**：你能指出兩個 Row、長標題的 W/H、空狀態提示；三項都能在 Layers 找到。

## 5. 自己改一個條件（Solo）

只改 Title 文字，其他設定保持不動。將文字換成「本週待處理的申請共有十二筆，請選取一筆查看詳細內容」。

1. 只選 `List / Item / Title`，透過右側 Content 替換文字。
2. 保留 Fixed width 180 與 Auto height，觀察 Height 是否增加。
3. 確認 Row 01、Row 02 與 Empty Message 名稱沒有改動。
4. 記錄行數、Height 與需要修正的位置。

> **Checkpoint 2**：長標題沒有被裁切；兩列名稱仍可讀；空狀態訊息仍在；檢查表記下至少一個觀察或修正。

## 6. 卡住時怎麼回修

| 現象 | 可能原因 | 回修位置 | 重跑起點 |
|---|---|---|---|
| 只有一列 | 副本仍與來源重疊，或沒有完成命名。 | Layers 與畫布位置。 | 回第 3 步複製與排列。 |
| Title 長句被裁切 | Width 是 Auto，或高度仍為 Fixed。 | Title 的 Resizing。 | 回第 5 步設 Width 180、Auto height。 |
| Empty Message 被當成 Row | 名稱沒有分出 `Empty` 狀態。 | Layers 名稱與父層。 | 回第 6 步重新命名。 |
| 長文字改到錯的物件 | 目前選取了 Row 或另一個文字層。 | Layers 的選取列。 | 回第 1／4 步重新選 Title。 |

把現象、回修位置與重跑結果寫入<a href="../courses/uiux-designer/assets/A7-list-content/reference/EXPECTED-CHECK.html">A7 完成檢查表</a>。動態增刪與資料切換仍標成未測，不用圖層名稱代替行為證據。

## 7. 驗收與交接（Verify）

- `List / Item / Row 01`、`Row 02` 在同一個 Frame 內，尺寸與位置可讀。
- `List / Item / Title` 寬 180、Auto height，長標題能換行。
- `List / Empty / Message` 顯示「目前沒有清單項目」。
- Solo 版本的行數、Height 與修正點已記錄。
- 截圖、Figma 檔連結與未測試邊界已保存。

### 交給 A8

保留兩個 Row、Title 的內容壓力設定與 Empty Message。A8 會把這些視覺狀態整理成 Toast、Dialog 與 Navigation 的回饋規則；List 的動態增刪與資料切換要另立測試案例。

### 課前驗證待辦

- [ ] 以乾淨 Draft 重做兩個 Row 與長標題。
- [ ] 由另一位學員依頁面完成一次冷讀。
- [ ] 以不同 Figma 帳號重跑並記錄權限差異。
