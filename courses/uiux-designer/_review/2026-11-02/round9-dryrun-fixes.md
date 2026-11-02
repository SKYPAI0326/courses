# 第九輪模擬走查修正清單

兩個模擬學員代理照主線逐步模擬 round9，共找出 38 個照做會卡住的步驟（對比 0 個）。下列是 PM 裁定的改法，承作照改；`改寫規格書-round9.md` 與前幾份規格書的規則仍有效。實機事實見 `platform-inapp.md` 最後兩節。

## A1
1. 步驟 11、16：用 F 畫出後各補「在 Layers 雙擊改名為 `Login / Card`／`Button / Draft`」。
2. 跟著做 1～2：長句測試改在**卡片外複製的一段 `Message` 副本**上做：先把副本 W 設 322，再把文字尺寸模式切成 Auto height，觀察換行；寫一句「卡片還是固定高度，正式卡片裡的長句會壓到下面的提示，下一次用 Auto layout 解決」。測完刪除副本；正式 `Message` 維持規格表短句。
3. `Button / Draft` 在 A1 就設圓角 8（規格表同步）。

## A2
4. `Desktop / Main` 規格表補 H（例如 540）與兩張參考卡片的 x、y，數值要和本堂格線算式一致。
5. 跟著做 1「在手機登入卡片加入較長的用途說明」改成在卡片外的副本上測試，測完刪除；正式卡片維持 `Message`、`Hint`、`Button / Draft` 三個子層。

## A3
6. 示範步驟 3：`Button / Draft` 轉成 Auto layout 後，**W 改回 322（Fixed）**。Min width 示範改在「複製出來、寬度 Hug 的按鈕副本」上做，正式按鈕不加 Min width；測完刪除副本。
7. 跟著做 4 窄版副本：命名 `Login / Card 360`，把副本裡的按鈕暫時改成 Fill container，再觀察換行；完成描述加「按鈕跟著變窄」。
8. 間距變數綁定：寫明 Padding 有**水平、垂直兩個欄位**，兩欄都綁 `Space 16`（已實測）。
9. Min／Max 小節步驟 1、5：改成「複製登入卡片，放進一個 Auto layout 的桌面測試 Frame，把副本寬度設為 Fill container」，測完刪除測試 Frame；正式卡片不移動。
10. Tags 步驟 7：放在「主線 Section 裡、手機畫面外的空白處；下一堂建立 `Components` 後再移入」。

## A4
11. 示範步驟 2：「把圓角設為 8」改成「確認圓角是 8」（A1 已設）。
12. 三個使用處的寬度：步驟各補設定——`Button / Login` Fill container；`Button / Complete`、`Button / Cancel` Hug contents。
13. 圖示步驟 10 完成描述改成：「元件區的 `Icon / Check` 主元件改變；按鈕裡已把描邊覆寫成白色的勾選維持白色——這就是覆寫會蓋過主元件的例子」。

## A5
14. 跟著做 1：改成「選取既有的 `Button / Login`，確認它是 Primary／Default」，不另插按鈕。
15. Instance swap 建立入口：改成「選取**元件集**，在 Properties 按 ＋ 選 **Instance swap**，預設值選 `Icon / Check`，按 Create property；再選各 Variant 裡的圖示使用處，在右側使用處名稱列的屬性圖示把它綁到 `Icon`（入口位置以畫面為準）」。

## A6
16. `Field / Input` 規格表補「Horizontal、垂直置中」（單一文字按 Shift+A 實測就是水平）；步驟 5 補「Gap 改 8 並綁 `Space 8`」。
17. 步驟 15「標＊為必填」：先另起一步「按 T 建立『標＊為必填』，套 `Type / Supporting`，命名 `Required Note`」，再放入卡片。
18. Select 建立方式：「插入一個 `Field` 使用處，右鍵 **Detach instance**，在輸入區右側放 `Icon / Chevron Right` 並旋轉 90 度，再 Create component 命名 `Select`」。
19. 「優先順序」：步驟 11 前加「在類別欄下方按 T 建立『優先順序』，套 `Type / Label`」。
20. `Radio`、`Toggle` 規格表與步驟 4、5：寫明「控制圖形與文字層一起放在最小高度 44 的水平 Auto layout」，並在建立步驟加入文字層（Radio 預設「選項」、Toggle 預設「提醒我」）；文字建 Text property `Label`，使用處才能改字。

## A7
21. 步驟 6 `Tags`：「保留高優先與交付」改成「在 Layers 關掉其餘三個標籤的眼睛（隱藏）；使用處裡的子層只能隱藏，不能刪除」。
22. Text property：先綁定再 Add variant（照 A6 做法），預設值 `Title`＝「整理交付包」、`Due`＝「今天18:00」；若順序無法調整，寫明 Todo 與 Done 兩個 Variant 都要綁。
23. 步驟 11 後加「把 `Row / Task` 元件集移到 `Components`」。
24. 跟著做 6：Done 範例副本要**移到清單外**（`Components` 旁），清單維持十二筆。
25. 載入畫面：畫面命名 `Screen / List Loading`，加一步刪除複製來的 `List / Content`；三列 Skeleton 選起來按 Shift+A 命名 `List / Loading`（Vertical）。兩張規格表同步。

## A8
26. Error 圖示：寫明 Error 也用 `Icon / Alert`，Stroke 套 `Error`。
27. `Toast` Text property：先綁定再 Add variant，或寫明三個 Variant 都要綁；預設值「已完成」。
28. 動作列兩顆按鈕各 130：A3 已改成正式按鈕不加 Min width（第 6 項），這裡加一句「若按鈕設過 Min width，先移除」。
29. `Nav / Bottom` 數值（W 402、H 64、兩項各 201、Gap 0、y 810、`Card` 底）放進規格表；加一步「把 `Nav / Bottom` 複製到 `Screen / List Done`，把『已完成』標成目前分頁」。
30. `Top Bar`：規格改成 x 24、W 354（`Screen / Detail` 不是 Auto layout，選不到 Fill container）。
31. 返回圖示觸控範圍：「選 `Icon / Arrow Left` 按 Shift+A，W／H 設 44（Fixed），對齊選置中，命名 `Button / Back`」。
32. 步驟 1 加「刪除詳情裡原本的『← 返回清單』文字」（返回只留 `Button / Back`）。

## B2
33. 示範步驟 1～5：登入到清單的連線在做需求與流程那一堂已建立；改成「選 `Button / Login`，核對既有連線是 On click → Navigate to → `Screen / List`、Instant」。
34. 熱區：補「選熱區，在右側開啟 **Ignore auto layout**（熱區才不會被表單排進去），再拖到開關列上方」，並寫一句這個設定下次捲動那堂會再用到。

## B5
35. `Button / Floating`：加建立步驟——按 F 建 48×48、圓角 24、Fill `Primary`；放 `Icon / Chevron Right` 旋轉 -90 度、Stroke `Card`、置中。
36. `Section / Sticky`：拿掉「起始 y 180」，改成「放在第一列任務之後」。
37. 回頂按鈕目的地：在捲動畫面最上方放一個透明、高 1 的 Frame `Anchor / Top`（直接子層），Scroll to 選它；刪掉選 `List / Content` 的寫法（避免第一列被固定頁首蓋住）。
38. `Nav / Bottom` 規格表加「`Card` 底」，與頁首一致。
