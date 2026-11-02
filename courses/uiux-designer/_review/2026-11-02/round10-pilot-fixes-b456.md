# 第十輪：試跑 B4～B6 修正清單

PM 裁定如下，承作照改；實機事實見 `platform-inapp.md` 最後一節。

## B4
1. 示範 2：寫成「`Button / Complete` 已有一條 On click → Navigate to `Screen / List Done` 的連線，點開它把 Action 改成 **Open overlay**（不要另加第二條）」。
2. 示範 3：「Overlay」欄位選 `Overlay / Confirm`（畫面上的欄位名是 Overlay）。
3. 示範 9、11：彈窗兩顆按鈕先在 Layers 改名 `Button / Cancel`、`Button / Confirm`（依按鈕文字分辨）。
4. 跟著做 1：`Overlay / Menu` 規格：Frame W 280、Vertical、Padding `Space 16`、Gap `Space 12`、Fill `Card`、1 px `Border` 外框、圓角 8；標題套 `Type / Section title`、一段內文套 `Type / Body`（Fill container、Auto height）、一顆 `Button` 使用處（Secondary、Label「檢視說明」）。`Overlay / Help`、`Overlay / Sort` 同樣底色與外框。
5. 跟著做 2：Help 的內文就是 Menu 內文那一層，改字即可（Menu 規格已含內文）。
6. 跟著做 4：「說明」按鈕放在 `Top Bar` 右側（`Top Bar` 內，標題之後）。
7. 跟著做 9：「排序」按鈕放在 `Header / Fixed` 右側；若尚未做頁首，先放在清單標題右側。
8. 跟著做 10：從新 Frame 建 `Overlay / Sort`（不要複製 Menu，避免把 Swap 互動一起複製）；若複製了，刪掉複製來的互動。
9. 跟著做 15 選取狀態：「目前選取的選項左側放 `Icon / Check` 使用處，未選的不放」；排序選項在原型裡不需要互動（寫明）。
10. 成功提示 1～2：「先把 `Screen / List Done` 上原本那個 `Toast` 使用處刪掉（之後改由彈層出現）。再插入一個 `Toast` 使用處放在畫面外，改名 `Toast / Success`；它是元件使用處，可以直接當 Overlay」。結尾描述同步。

## B5
11. 頁首：寫明「選取清單標題按 Cmd+Opt+G 包成 Frame，命名 `Header / Fixed`，依規格設尺寸與 Fill `Card`；標題在頁首內設 X 24、Y 24」。
12. 漂浮按鈕圖示改白：「選圖示使用處，在 Selection colors 把 `Text` 換成 `Card`」。
13. 跟著做 3：複製畫面命名 `Screen / List Sticky`。
14. `Section / Sticky` 規格補 Fill `Surface`。
15. 橫向卡片：放在 `Screen / List` 的 `List / Content` 裡、第三筆任務之後（主線測試會用到）；包成 Auto layout 後「若是垂直，點 Horizontal；外框 W Fill、H Hug，每張卡 W 200 Fixed」，外框 Overflow 選 Horizontal、Clip content。

## B6
16. 任務測試紀錄的「第二筆標記完成沒反應」：在 B6 走查範例或卡住時表格加一列「只有第一筆接了完成流程，其他筆的完成鈕沒連線是預期現象；測試任務只用整理交付包」。
17. 測試計畫與紀錄放在哪：「在主線 Section 外用 T 建文字框，命名 `Test Plan`、`Test Log`；或直接填測試紀錄表」。
