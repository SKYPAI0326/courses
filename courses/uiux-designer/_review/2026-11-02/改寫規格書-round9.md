# uiux-designer 第九輪：實作走查後的修正

發包人：產品經理（Claude Opus 5.5）。承作：GPT-5.6 Sol（high）。日期：2026-11-02。
課程負責人改用「實作走查」：PM 在 Figma 示範檔照主線實際操作（紀錄見 `platform-inapp.md`「第九輪實作走查」），並核對審查員 H 的 21 項錯誤（`independent-review.md` 最後一節）。本檔把兩者合成逐堂修正。**不加新教學主題、不改評分表、不改時數。** 前八份規格書的必守規則與第四輪主線物件總表有效；本檔第 1 節的卡片鏈取代先前所有關於 `Login / Card` 內容與尺寸的說法。

輸入 `round8/<單元>.md`，輸出 `round9/<單元>.md`（`round9/` 目前是 round8 的複本，直接覆寫你負責的檔）。只改本檔列出的地方，其餘照抄（含截圖行與前後空行）。頁尾 `## 自我檢查` 加「第九輪修改」。

**寫法要求**：每一步的「完成後」要描述學員當下在 Figma 真的看得到的結果；凡是步驟要用到的圖層、元件、變數、畫面，必須在**這一步之前**已經建立（本堂或之前的堂）。寫完請自己從第 1 步依序檢查一遍。

## 1. 登入卡片鏈（A1 → A2 → A3 → A6）

| 堂 | 卡片裡有什麼 | 卡片規格 |
|---|---|---|
| A1 | `Title`「登入工作室」、`Message`「登入後檢視待處理的任務。」、`Hint`「請輸入工作室帳號」、`Button / Draft`（內含 `Label`「登入」） | 一般 Frame（還沒有 Auto layout）；x 24、y 120、W 354、H 208；子層手動擺放：左右留 16，`Title` y 16、`Message` y 64、`Hint` y 104、`Button / Draft` y 142（W 322、H 48） |
| A2 | `Title` 移出卡片改名 `Screen / Heading`（x 24、y 64）；卡片剩 `Message`、`Hint`、`Button / Draft` | 把三個子層一起往上移 48（Y 改 16、56、94），卡片 H 改 160 |
| A3 | 同上三個子層 | 選**原本的**卡片按 Shift+A 轉成 Auto layout（實測：會依原位置推算 Padding、Gap，且把寬度改成 338），再把 Padding 改 16、Gap 改 12、W 改回 354、Height 設 Hug；`Message`、`Hint` 設 Auto height 與 Fill container；卡片高度自動變成 16＋24＋12＋22＋12＋48＋16＝150。`Button / Draft` 也是選**原本的**按鈕按 Shift+A，再設水平置中、Padding 16／12、H 48 |
| A6 | 加入帳號、密碼欄位後刪掉 `Hint`（欄位標籤取代它） | 卡片 Gap 改用 `Space 16`；寫一句原因 |

各堂規格表、步驟、高度算式、Constraints 表都依此改。

### A1
- 第 11 步拆成：按 F 在畫面裡畫 `Login / Card`，**Fill 按 ＋ 再套 `Card`**（巢狀 Frame 預設沒有填色）；到右側 **Layout 區的 W、H** 輸入尺寸，X、Y 在 Position 區。
- 用 T 在卡片裡點一下建立文字，文字層會直接成為卡片子層；刪掉「在 Layers 把…移入卡片」那一步。
- 加一步「在 Layers 雙擊圖層名，依規格表改成 `Title`、`Message`、`Hint`」（Figma 預設用文字內容當圖層名）。
- `Button / Draft` 用 F 畫，Fill 套 `Primary`，裡面用 T 放「登入」並改名 `Label`。
- 卡住時表格加一列：「沒點進數字欄就按數字鍵，圖層變透明｜數字鍵是不透明度快捷鍵｜按 0 回到 100%」。

### A2
- 依第 1 節改：把 `Title` 拖出卡片、改名 `Screen / Heading`、位置 x 24、y 64；再選卡片裡三個子層把 Y 往上移 48、卡片 H 改 160。
- `Desktop / Main` 寫明用 Frame（F）；裡面兩張參考卡片給規格（例如左欄清單卡 W 384、H 120，右欄詳情卡 W 792、H 320，依本堂格線算出的跨欄寬度為準，不得與算式矛盾）。

### A3
- 依第 1 節改寫示範步驟：**不新建** `Message`、`Label`、`Button / Draft`，改成把 A1 已有的圖層轉成 Auto layout。
- 先在 Padding、Gap 填數字 16、12；**本堂後段建立間距變數後**，再回來把它們綁成 `Space 16`、`Space 12`。規格表寫「Padding 16、Gap 12（後段綁成 `Space 16`、`Space 12`）」。
- 「跟著做」第 2 步原本「加入 `Hint`」改成「把 `Hint` 拖到按鈕下方再拖回來，觀察順序改變」；第 3 步「刪除再 Undo」改用 `Hint`。
- Tags 第 7 步：任務卡此時還不存在，改成「把 `Tags` 主元件放在元件區旁邊；做清單那一堂會把它放進任務列」。

## 2. A4、A5 元件

- **A4 圖示顏色**：明寫是 **Stroke**（圖示只有線條、沒有填色）：「選圖示裡的向量，在右側 **Stroke** 套用 `Text`；不要加 Fill，否則線條圍出的區域會被填滿」。Primary 按鈕內的圖示也是改 Stroke 成 `Card`。
- **A4、A5 題目元件只走一條路：複製並換綁**。A4 練習改成：在題目開頭畫面放主線按鈕的使用處並改文字、換圖示（練習使用處與覆寫），**不自建**題目按鈕；寫一句「題目自己的元件，等下一堂按鈕做成元件集後一次複製」。A5 的複製換綁節維持。
- **A5 狀態標籤**（主線沒有可複製的）：練習改成在題目區**自建** `題目名 / Status`，給規格：Auto layout，Padding 上下 4、左右 8（`Space 4`、`Space 8`），圓角 8，文字套 `Type / Supporting`；Variant `State` 的外觀：可預約／供應中／可兌換＝`Primary Soft` 底、`Primary Pressed` 字；本週額滿／售完／已兌完＝`Disabled` 底、`Disabled Text` 字；點數不足＝`Card` 底、`Control Border` 1 px 外框、`Text` 字。刪掉「做法同元件那一堂」的說法。
- **A5 Focus**：改成「外加 2 px `Focus Ring` 描邊，Stroke 選 **Outside**」，刪掉「保留 2 px 間隔」。
- **A5 Secondary Pressed**：內文改成與規格表一致（`Primary Soft` 底、`Control Border` 1 px 外框），刪掉「外框較明顯」。
- **A5 Primary／Disabled 圖示**：停用狀態的圖示 Stroke 用 `Disabled Text`（對 `Disabled` 5.18:1），規格表與步驟同步；寫一句「白色圖示在停用底色上只有 1.23:1，看不清」。
- A5 顯示開關截圖的圖說補一句：「截圖以文字層示範，圖示層的入口相同」。

## 3. A6 表單

- **Fill container 的順序**：`Field / Input` 在第 3 步先設**固定寬 322**；第 5 步建立外層 Auto layout 後，再把 `Field / Input`、`Field / Helper` 改成 Fill container，並把外層 `Field` 的 W 設 322。規格表寫明「`Field` W 322；內層 Fill container」。
- **`Field / Multiline`**：寫明複製 `Field` 元件集後，刪掉 Disabled 那個 Variant（只留 Default、Focus、Error），把輸入區高度改 96、`Value` 文字設 Auto height、對齊改上方。
- **Select 選項**：主線「任務類別」給四個選項：設計、行政、客戶、財務；展開畫面列出這四項。
- **第 19 步必填勾選**：主線改用新增任務表單加一個必填勾選「我已確認期限」，錯誤句「請先確認期限」；錯誤句是勾選列**下方另放的一段文字**（套 `Type / Supporting` 與 `Error`），不放進勾選框元件裡。題目的「同意注意事項」留在練習。
- 加入帳號、密碼欄位後刪掉 `Hint`（見第 1 節）。

## 4. A7、A8

- **A7 時間圖示**：第 8 步之前加一步：「選 `Icon / Clock` 使用處與期限文字按 Shift+A，命名 `Row / Due`，Gap `Space 4`」；第 8 步改選 `Title`、`Row / Due`、`Row / Tags`、詳情線索。
- **A8 `Toast` 規格**補齊：W 354（固定）、Fill `Card`、1 px `Control Border` 外框、圓角 8、Padding 16／12、Gap 8；文字 Fill container、Auto height（長句會換行）；圖示 Stroke 依 Type 套 `Success`、`Warning`、`Error`。
- **A8 錯誤提示範例**：題目三欄的錯誤句改成有下一步，例如「網路中斷，請確認連線後再按一次『送出預約』」（點餐、會員對應各自的主要動作）。同步改 `round2-topics.md` 第 1 節表格的錯誤句（PM 已授權承作 A8 的組修改這一行）。
- **A8 `Screen / List Done`**：改成**只顯示已完成的任務**：複製 `Screen / List` 後，標題改「已完成」，刪掉其他待處理列，只留「整理交付包」並把它的 `Status` 切成 Done；底部導覽的「已完成」分頁指向這張。B1、B3、B4、B6 若描述完成清單內容，改成一致（承作 A8 的組一併檢查這四堂的描述，只改描述句）。

## 5. B2、B4、B5

- **B2 不重建 A6 已有的畫面**：第 11、14 步改成「打開做表單那一堂建好的 `Screen / New Task Filled`、`Screen / New Task Reminder`」，並檢查 Reminder 那張的開關是 On。
- **B2 `Radio Group`**：主元件建在 `Components` 區，再把使用處放進畫面。
- **B4** 成功提示文字與 A8 一致（以 A8 的文字為準）。
- **B5**：`Header / Fixed` 建立後，把清單原本的標題移進頁首（不要留在下面被蓋住）；`Section / Sticky` 寬度改成 Fill container（跟著 `List / Content` 的 354），規格表同步。

## 6. 分組與交付
- 跑 `python3 _review/2026-11-02/check-pages.py _review/2026-11-02/round9` 修到 OK。
- 不 git、不詢問、不用 course-* 技能、不上網。
