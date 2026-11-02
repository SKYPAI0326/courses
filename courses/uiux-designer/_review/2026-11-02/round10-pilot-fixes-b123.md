# 第十輪：試跑 B1～B3 修正清單

PM 裁定如下，承作照改；實機事實見 `platform-inapp.md` 最後一節。

## B1
1. 需求摘要、畫面清單：寫明「在主線 Section 外、IA 區旁用 T 各建一個文字框，命名 `Requirements`、`Screen List`」。
2. IA 第 1 步：「在主線 Section 旁的空白處」（流程圖下一節才畫）；Section 改名寫「雙擊 Section 名稱或在 Layers 雙擊改名」。
3. IA 第 2 步：「用 R 畫矩形，再用 T 在矩形上加文字（矩形本身不能打字）」。
4. IA「已完成」既是內容又是組名：組名用較大的文字標在一組上方，不另做矩形。
5. IA 第 5 步：改成「打開 `Screen / List` 看底部的 `Nav / Bottom` 對照網站地圖；要加第三個分頁時，在 `Nav / Bottom` 裡選『已完成』那一項按 Cmd+D 複製，再改字成『我的』」。
6. IA 第 7 步 `Screen / Me`：402×874，Fill `Surface`，標題套 `Type / Page title`。
7. Flow 節點文字：套 `Type / Body`（預設 12px 太小）。
8. 示範第 1 步：「在完成清單附近的空白處」新增手機 Frame。
9. 跟著做第 6 步：「滑過 Flows 清單裡的流程名稱，點右側的播放圖示」（單擊名稱會進入改名）。

## B2
10. 示範 1～5：「若沒有這條連線（例如做需求那一堂沒做完），照下列設定新增」。
11. 跟著做第 4～5 步：「複製畫面時 Back 的連線已一起帶過來，只要確認目的地」。
12. 預約題：附上資料連結 `../assets/shared/practice/BOOKING-DATA.csv`、`BOOKING-MINE.csv`（相對路徑依講義位置）；日期列包 Auto layout 後子項改 Hug；`Slot` 規格表補外觀：W 96、H 56、圓角 8，兩行文字（時間 `Type / Label`、狀態 `Type / Supporting`），Available＝`Card` 底＋`Control Border` 外框、Selected＝`Primary` 底白字、Full＝`Disabled` 底＋`Disabled Text` 字、Unavailable＝`Card` 底＋`Muted` 字；示範日 11/10 標成已選日期（`Primary Soft` 底）。
13. Hover／Pressed：Change to 下方寫「會出現 Type 與 State 兩個下拉，Type 保持原值，State 選 Hover（或 Pressed）」。
14. Checkbox／Toggle：Change to 的目標「是開關樣式，切到相反值」。
15. Radio Group：寫成「在 Design 分頁雙擊進入 `Radio Group` 的某個 Variant、選到其中一個選項的使用處，再切到 Prototype 分頁加互動；Change to 的 Selected 下拉會列出高、中、低三個值，選這個選項對應的值。三個 Variant 各三個選項，共 9 條（點自己那一項的也要設，否則點了沒反應）」。
16. 熱區：建立方式改成「在畫面上用 F 畫一個 Frame 蓋住開關那一列（它會是畫面的直接子層，不會被表單排進去），不加填色，命名 `Hotspot / Reminder`，在 Layers 確認它在表單之上」；刪掉 Ignore auto layout 那句。

## B3
17. Move in 方向：「從右邊進來選 ←」，Move out 返回選 →。
18. Smart Animate：「Before／After 的標籤文字先手動命名為 `Status / Label`，再改字（否則圖層名會跟著文字改，配不起來）」。
19. `Button / Animate`：寫明用 `Button` 元件的使用處。
20. `Status / Check`：用 `Icon / Check` 使用處（不要用文字符號）。
