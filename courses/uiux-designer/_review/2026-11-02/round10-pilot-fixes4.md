# 第十輪：試跑 A7 後半與 A8 修正清單

PM 裁定如下，承作照改；實機事實見 `platform-inapp.md` 最後一節。

## A7
1. 示範 19：Assets 只顯示名稱最後一段，「搜尋 Task（`Row / Task` 在 Assets 顯示為 Task），點縮圖後按 Insert instance」；插入後的使用處在畫面最上層，「選 `List / Content` 裡現有的一列再按 Shift+I 插入，新列會接在後面」，或複製既有列（Cmd+D）最快。
2. 示範 24 換行測試：指定加在第 2 筆「確認活動報名資料並補上聯絡電話」。
3. 示範 25：使用處裡的標題層名稱會顯示文字內容；寫成「主元件裡叫 `Row / Title`」。
4. 跟著做 1～3：寫明「畫面高 874 會裁掉超出的列，增刪結果在 Layers 看；或暫時取消畫面的 Clip content」；複製出的列記得改名（例如 `Row / T13`）；Cmd+Z 若只還原選取，再按一次。
5. 空清單：兩句空狀態文字給樣式與位置（標題 `Type / Section title`、說明 `Type / Body`，放在 `List / Content` 裡第一位）。
6. 詳情：按 F 建畫面後「把名稱改成 `Screen / Detail`（F 會沿用上一個名稱與尺寸）」；第 8 步的 Fill container 移到包成 Auto layout 之後；第 9 步從 Assets 選 `Button` 時「看 Details 顯示 10 variants 的那個（元件區的元件集）」，插入後「確認它在 `Screen / Detail` 底下，不在最上層」；第 10 步「若按鈕和文字在不同父層，先把文字包起來，再選最後一段文字按 Shift+I 插入 Button」。
7. 附件：`Detail / Attachment` 規格補 H 160；Fill 類型列寫「先點色塊打開取色器」。
8. 載入中：Skeleton 三種矩形給尺寸（標題 220×16、摘要 300×12、標籤 72×24，Fill `Border`）；`Skeleton / Row` 包好後 Fill `Card`、圓角 8、Padding 16；「保留頁首」改成「保留畫面標題」。
9. Done 範例副本：「從 Assets 插入一個使用處、切 Done，放在 `Components` 區下方」（不要在清單內複製）。

## A8
10. Toast 建立：`Toast / Message` 套 `Type / Body`，包好後設 Fill container、Auto height。
11. Add variant：「在主元件上**按右鍵** → Main component → Add variant」；屬性預設名 Property 1 改成 `Type`。
12. 換成 `Icon / Alert`：「選圖示使用處，用右側元件名稱旁的下拉換成 `Icon / Alert`；換完把描邊改套 `Warning`／`Error`（原本的 `Success` 會保留）」；選變數時看清楚是本檔的。
13. 三個 Toast 使用處：插入後用 X／Y 排開（會斜向疊在一起）。
14. `Overlay / Confirm`：按 F 建立後改名、W 改 320；對它按 Shift+A 後「W、Gap、Padding 會被推算成別的值，依規格改回 320、16、24」。
15. 確認彈窗兩顆按鈕：插入後關掉 `Show icon`（取消、確認不需要勾勾）。第 61 步「移除 Min width」：若選單裡沒有 Min width 就略過。
16. List Done／Detail Warning／Detail Error 的 Toast 位置：放在畫面最上層、x 24、y 72（標題下方、不蓋住標題）；不要放進 `Detail / Content`。
17. `Nav / Bottom`：包好後 Gap 若顯示 Auto，改成 0；目前分頁的底線在 Typography → Type settings → Decoration 設定。複製到 `Screen / List Done` 用「選 `Nav / Bottom` 按 Cmd+C，選 `Screen / List Done` 按 Cmd+V 貼到同位置」？——不可教 Cmd+V 以外的不確定做法；改寫成「選 `Nav / Bottom` 按 Cmd+D，把副本的 X 改到 `Screen / List Done` 的範圍、Y 810，再在 Layers 確認它在 `Screen / List Done` 底下（若沒有，把它拖進去）」。
18. Top Bar：返回鈕與標題按 Shift+A 若得到 Vertical，點 Horizontal；`Top Bar` 對齊選垂直置中；`Top Bar` 是 `Screen / Detail` 的直接子層（x 24、y 16），`Detail / Content` 往下移。
19. 觸控檢查外框：新增 Stroke 預設黑色，「改套 `Border`」再檢查、檢查完移除。
20. 從 Layers 選文字要改字時：「在畫布上雙擊文字」。
