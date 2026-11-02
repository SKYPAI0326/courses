# 第十輪：試跑 A4～A6 修正清單

代理扮演零基礎學員在 Figma 實際操作 A4、A5 全部主線與 A6 示範 1～9。PM 裁定如下，承作照改；實機事實見 `platform-inapp.md` 最後一節。

## A4
1. 示範 2：補一句「主元件從卡片移出後，寬度會從 Fill 變成固定 322，屬正常」。
2. 示範 3：Assets 的 Created in this file 會先列頁面，點進目前頁面才看到元件；格子裡只顯示短名稱（例如 Primary）。截圖圖說同步。從 Assets 拖進卡片後，若落在 `Message` 與 `Hint` 之間，在 Layers 把它拖到最後。
3. 示範 8：Cmd+D 後「把副本往下拖開，否則會和原本那顆疊在一起」。
4. 示範 11：「From this file」旁的圖示平常是菱形，滑鼠移上去變成箭頭再點。
5. 跟著做 2「改主元件字重」：改成「把主元件 `Label` 的填色暫時改成 `Primary Pressed` 以外的另一個顏色變數（例如 `Text`）」或改圓角，避開「套了文字樣式就看不到字重欄」；若保留字重練習，寫明要先 Detach style、改完再套回。
6. 跟著做 4 Reset instance：補「圖層名與寬度設定也會一起回到主元件，Reset 後再把名稱改回 `Test / Cancel`、寬度改回 Hug」。
7. 跟著做 5：在這步之前先把主元件填色改回 `Primary`，再做覆寫比較。
8. 圖示 9：Gap 給數值：改成 8 並綁 `Space 8`（A3 已教過綁法）。
9. 圖示 2：補「若圖示只有一條路徑，按 Cmd+E 不會有變化，名稱直接改成 `Vector` 即可」。

## A5
10. 示範 1：寫明 Add variant 會自動把元件集命名為 `Button`、原版本帶值 Primary；第 3 步「命名為 Button」改成「確認元件集名稱是 `Button`」。
11. 示範 2：加到十個前先把旁邊的 `Tags` 移開（版本會往下長）。
12. 示範 6：「屬性值已存在時，從欄位的下拉選單選，不要直接打字」。
13. 示範 7：Secondary 加 1 px 外框後，「到 Auto layout 進階設定把 **Inside stroke** 改成 **Excluded**，高度才會維持 48」。
14. 圖示屬性：Boolean 預設名稱是「Show 圖層名」，改成 `Show icon`。Instance swap 綁定入口寫成「選圖示使用處，點名稱列上的 Apply instance swap property 圖示」（已實測）。
15. 「把主線元件複製給自己的題目」開頭加：「題目的顏色集合是在第一堂『換你做』建立的；還沒建的話，先照那一節建好題目集合再做這一步」。並寫 Selection colors 預設摺疊，點標題展開。
16. 若變數搜尋清單同時出現兩個集合的同名變數，寫「看清楚變數旁的集合名稱」。

## A6
17. 示範 1、2、4：每建一個文字層就寫明套哪個樣式（`Field / Label` 套 `Type / Label`、`Field / Value` 套 `Type / Body`、`Field / Helper` 套 `Type / Supporting`），並提醒「新文字會沿用上次用過的樣式，記得換」。
18. 示範 7：可寫「也可從文字層 Content 旁的圖示直接建立並綁定 Text property」作為替代路徑。
