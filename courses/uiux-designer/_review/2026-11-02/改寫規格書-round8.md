# uiux-designer 第八輪：元件順序、表單鏈、預約示範資料

發包人：產品經理（Claude Opus 5.5）。承作：GPT-5.6 Sol（high）。日期：2026-11-02。
課程負責人指示「修前三項」：審查員 G 前五項的第 1～3 項（照做會卡住的錯誤）。**不改評分表、不改練習範圍、不改時數、不加新教學內容。** 前七份規格書的必守規則與第四輪主線物件總表全部有效。

輸入 `round7/<單元>.md`，輸出 `round8/<單元>.md`。只改本檔列出的地方，其餘照抄（含截圖行與前後空行）。頁尾 `## 自我檢查` 加「第八輪修改」。

## 1. A2、A4、A5：元件鏈的先後順序

- **A2**：不要新增第二個「登入工作室」。把卡片內原有的標題移到卡片外、成為 `Screen / Login` 的直接子層，再改名 `Screen / Heading`（原步驟「在卡片上方建立『登入工作室』」改成「把卡片裡的標題拖到卡片外」）。規格表與 A1 的 `Title` 說法一致：A1 的標題在 A2 移出卡片後改名。
- **A4 第 1 步**：寫明把 `Login / Card` 裡原本的 `Button / Draft` 轉成主元件 `Button / Primary` 後，**移到元件區**，登入卡片裡改放它的使用處 `Button / Login`；卡片裡不留兩顆按鈕。
- **A4「把主線元件複製給自己的題目」整節移到 A5**，放在 A5 做完按鈕元件集（Add variant 之後）的位置。A4 練習改成：在題目區另建自己的主要按鈕主元件（照本堂主線做法），不複製元件集。A5 那一節的步驟照原文（選整個元件集 `Button` → Cmd／Ctrl+D → 拖到題目區 → 改名 → Selection colors 換綁），並加一步：**間距變數不會出現在 Selection colors**，要選取元件集後在 Padding、Gap 欄位逐一換成題目的間距變數；若題目沒另建間距變數，就沿用 `Studio` 的間距並在練習裡寫明「間距共用」。
- **題目元件命名統一**：題目的 Section 叫 `Components / 你的題目名`（例如 `Components / Booking`）；題目元件用 `題目名 / 元件名`（例如 `Booking / Button`、`Booking / Icon / Check`）。A4、A5 練習裡「在 Assets 找到 Button 與 Icon 兩個家族」改成「在 Assets 找到 `Booking` 這個家族」之類對應寫法。
- **A4 圖示顏色**：第 6～8 步加兩件事：(1) 做圖示元件時先選圖示內所有線條按 **Cmd／Ctrl+E（Flatten）** 合成一個向量並命名 `Vector`，六個圖示都一樣，這樣交換時顏色設定比較容易保留；(2) 交換成另一個圖示後，**檢查圖示是否仍是白色**，若變回深色就再對該使用處的圖示套一次 `Card`。
- **A4 第 9 步**：「一般畫面的勾選圖示會同步」改成可在當下看到的結果（例如「元件區裡 `Icon / Check` 主元件與按鈕裡的勾選同時改變」）。
- **A4 練習的使用處位置**：不要求放在還沒做的表單或確認畫面；改成「放在題目開頭畫面與題目元件區各一個」。

## 2. A6、B2：表單鏈

### A6
- `Field / Input` 改成 **W Fill container**（隨 `Field` 寬度），`Field` 本身在主線是 322；題目在 360 寬畫面裡讓 `Field` Fill container（欄寬 312），輸入區會跟著變。規格表同步。
- **錯誤句統一**：主線帳號欄示範的情境是「只輸入 studio，沒有 @」，錯誤句一律用「帳號格式不正確，請輸入完整電子郵件」；密碼錯誤句「密碼不足 8 個字元」。第 9 步「請輸入工作室帳號」改掉。`Show helper` 維持預設 False（由 PM 同步起始材料）。
- **A6 畫面命名**（B2 會用）：`Screen / Login`（正常）、`Screen / Login Error`（錯誤）、`Screen / Login Fixed`（修正後）；`Screen / New Task`（空白）、`Screen / New Task Filled`（已填）、`Screen / New Task Reminder`（提醒開關打開、多一個欄位）。正文第一次出現時寫明名稱，焦點、停用等其他狀態畫面若有，也各給名稱。
- **新增任務表單步驟重複**：第 9 步只放「標題文字與欄位的使用處」，控制項（Radio、Toggle、Multiline、Button）統一在第 11～14 步插入，不要兩處都加。
- **眼睛圖示**：第 3、4 步改成「到四個 Variant 各放一個 20×20 圓形」只寫一次，不要讓 Default 被放兩次。
- **`Field / Multiline`**：寫明做法「選取 `Field` 元件集按 Cmd／Ctrl+D 得到新元件集，改名 `Field / Multiline`，把輸入區高度改 96」。
- **練習「複製或自建」二選一**：題目的表單元件一律「從主線複製並換綁」（做法同按鈕元件那一堂）；刪掉「建立 Checkbox 與 Radio 元件集」的重複要求；刪掉「若已做 `Radio Group`」（那是下一堂才做的）。
- 間距變數換綁同第 1 節說法（Selection colors 只換顏色）。

### B2
- 正式起點寫明：Preview 從 `Screen / Login` 開始；登入流程用 `Screen / Login` → `Screen / List`；模擬填寫用 `Screen / New Task` → `Screen / New Task Filled`；提醒開關用 `Screen / New Task Filled` → `Screen / New Task Reminder`。
- **開關的兩組互動不要疊在同一個 trigger**：「開關打開才出現欄位」改成在開關那一列**上方放一個透明熱區 Frame**（Fill 0%、命名 `Hotspot / Reminder`），由熱區 On click → Navigate to `Screen / New Task Reminder`；開關元件自己的 Change to 保留。寫一句：「熱區在最上層，點下去會先觸發熱區的換頁。」
- **Radio Group**：寫明 A6 新增任務畫面上的三個單選，要換成 `Radio Group` 的使用處；題目的單選（寵物體型、付款方式）照同樣做法另建自己的群組，選項文字用 Text property 或直接改各 Variant 的文字。
- 換你做自我檢查「Preview 從清單開始」改成「從開頭畫面開始」。
- **預約示範資料**（三處同步：規格表、步驟、事實核對）：
  - 示範日改為 **11/10（星期二）**。
  - 11:00、15:00 額滿的理由改成「示範資料：那兩個時段店裡的美容師都已排滿」，**不要**說對應 `BOOKING-MINE.csv`。
  - 時段：需求頁說「早上十點開始，最後一個是下午六點」，所以時段起點是 10:00～18:00；需求頁沒說幾點打烊，示範先假設 **19:00 打烊**，並寫一句「實際案子要問店主，先寫進需求初稿『還沒想清楚的』」。
  - 大型犬全套 180 分鐘：能選的起點要後面連續三格都空、且 19:00 前結束；依此重新推算並寫出一組正確例子（例如選 12:00 顯示「12:00～15:00，共 3 小時」—— 15:00 額滿，所以 12:00 起的三小時是 12、13、14 點，結束於 15:00，不佔用 15:00 那格；若你判斷這和「佔用 15:00 那格」有衝突，改用 16:00 起「16:00～19:00」並寫出理由）。13:00、14:00 起點因會碰到 15:00 額滿而 Unavailable；17:00、18:00 起點因超過打烊而 Unavailable。事實核對寫出完整推算。

## 3. B8
- 第一個 commit 的 `git add` 加入 `my-screen.html`（`git add index.html styles.css app.js README.md my-screen.html assets/status-badge.png`），之後 `git status` 才會乾淨。正文若說明下載包有哪些檔，補上 `my-screen.html`。

## 4. 起始材料（PM 另派工）
起始材料 `assets/*/START-HERE.html` 會在本輪講義定稿後，由 PM 另派一個承作依講義規格表同步。講義裡**不要**為了配合舊的起始材料改名稱。

## 5. 分組與交付
- 跑 `python3 _review/2026-11-02/check-pages.py _review/2026-11-02/round8` 修到 OK。
- 不 git、不詢問、不用 course-* 技能、不上網。
