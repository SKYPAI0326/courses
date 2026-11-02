# 第十輪：試跑 A6 後半與 A7 前半修正清單

PM 裁定如下，承作照改；實機事實見 `platform-inapp.md` 最後一節。

## A6
1. 跟著做 2（Helper 改「密碼不足 8 個字元」）：寫成「先把 `Show helper` 打開，右側才會出現 Helper 欄；改完字再關掉」。
2. 跟著做 3～5 眼睛圓點：開頭加「先確認四個 Variant 的 `Field / Value` 都是 Fill container」。
3. 表單包框（New Task）與所有「全選後按 Shift+A 建垂直 Auto layout」處：補「若 Flow 顯示 Grid，點 Vertical；再確認每個子層的 H 是 Hug」。
4. `Field / Multiline`：輸入區改高 96 後，「把元件集外框拉大，並把三個 Variant 上下拉開不重疊」。
5. Select：寫明 Detach 後原本的文字屬性會失效（`Select` 只有 Open 屬性，類別文字直接改字即可）；展開版建好後「把元件集外框拉大到看得見四個選項」。
6. Select Open、Filled 加錯誤句等「改成 Hug contents」處：畫面是一般 Frame 沒有 Hug，改寫成「把畫面 H 加高到放得下（例如 1100）」；做原型那堂會改回手機高度。
7. 錯誤句示範：另存一張 `Screen / New Task Error`（複製 Filled 後加錯誤句），Filled 保持無錯誤；不要「修正後移除」導致錯誤畫面消失。
8. Radio：「Frame 20×20 圓角設 10 才會是圓形」；內點 10×10 圓角 5。
9. Radio、Toggle、Select 的 Label：照 Checkbox 的順序——先建文字並綁 Text property，再 Add variant。
10. Checkbox 勾號改白色：「選勾號使用處，在 Selection colors 把 `Text` 換成 `Card`」（使用處 Stroke 區可能是空的）。
11. 控制項文字：寫明套 `Type / Body`（新文字可能預設 Inter 12）。
12. 「必填 Checkbox 放在前一個欄位之後」：明寫放在「提醒我」那列之後、「新增任務」按鈕之前。
13. 巢狀選取：第一次需要時寫「按住 Cmd（Windows 為 Ctrl）點擊可直接選到內層；按 Shift+Enter 往上選父層」。
14. 從 Assets 插入按鈕時：「選 `Components` 裡的 `Button` 元件集（不要選畫面上的使用處）」。

## A7
15. Tags 標籤圖層：在 A3 做標籤時就把每個小 Frame 改名為標籤文字（「高優先」等）；A7 第 6 步照名稱隱藏。（A3 也要改：承作 A7 的組同時修改 A3 的 Wrap 第 1 步加改名。）
16. `Row / Due` 包框後：「若時鐘排到文字後面，在 Layers 把它移到前面（或選它按 Ctrl+Alt+↑）」——用學員看得懂的說法即可。
17. `Row / Task` 包框：同第 3 項的 Grid 提醒；子層 H 保持 Hug，換行增高才有效。
18. Add variant 後的命名：寫明「名稱含斜線的元件加 Variant 後會被拆開：元件集叫 Row、值叫 Task。把元件集改名回 `Row / Task`，屬性改名 `Status`，值改成 `Todo`」。
19. 規格表補 `Row / Task` 的白底（`Card`）與圓角 8 何時設定（建立元件前）。
