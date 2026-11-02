# 實機與網路查證（第二輪）

日期：2026-11-02。Figma、GitHub：PM 用 Claude in Chrome 在課程負責人已登入的帳號實機操作（Figma Free／Starter 草稿，測試檔「[測試] uiux 講義核對 2026-11-02」；GitHub 只讀查看，未建立任何東西）。Photoshop：本機無軟體，由 fresh-context 子代理以網路資料查證。本檔結論優先於 `改寫規格書.md` 第 5 節與三份 `platform-*.md`。

## Figma（實機）

| 項目 | 實際畫面 | 與規格書差異 |
|---|---|---|
| 建立設計檔 | Drafts 頁右上一排按鈕：Design／FigJam／Slides／Make／More | 沒有「+ Create」，直接點 Design |
| 編輯器左側 | 最左一排圖示：File／Agents／Assets／Tools／Variables；新檔預設開 Agents 對話面板，點 File 才見 Pages 與 Layers | 新增說明 |
| 右側分頁 | Design／Prototype | 一致 |
| 文字樣式 | Typography 右上樣式圖示 → Text styles 面板 ＋（tooltip：Create style）→ Name → Create style | 補中間一步 |
| 文字長高 | Layout 區塊 Resizing 三圖示，中間 tooltip「Auto height」 | 一致 |
| 格線 | Design 面板底部 Layout guide ＋（tooltip：Add layout guide）；預設類型「Grid」10px；下拉 Grid／Columns／Rows；Columns 欄位 Count、Color、Type（Stretch）、Width、Margin、Gutter | 預設叫 Grid，不是 Uniform grid |
| Frame 預設圓角 | 0 | 一致 |
| Auto layout | Shift+A 可用；預設 Gap 10、Padding 10、Hug；Flow 四種（自由、垂直、水平、格狀） | 一致 |
| 建立元件 | 右鍵 Create component（⌥⌘K） | 一致 |
| 主元件右鍵 | Main component → Publish selected components、Add variant；沒有 Create instance | 一致（無 Create instance） |
| **複製主元件** | Cmd+D 產生的是使用處（Instance），不是新主元件 | **A5、A6 原步驟「複製主元件再 Combine as variants」做不出來**，改用 Add variant |
| Add variant | 主元件變元件集（紫色虛線框、下方 ＋ 可再加），預設屬性名「Property 1」 | 新路徑 |
| Shift+I | 按了無反應 | 拿掉 |
| 插入使用處 | 左側 Assets → Created in this file → 拖入 | 一致 |
| Go to main component | 使用處右側「From this file」旁箭頭圖示；右鍵 Main component → Go to main component | 補位置 |
| 重設覆寫 | 元件名稱列 ⋯ → Reset instance／Reset size；右鍵 Reset instance | 不是 Reset all changes |
| 元件屬性 | Properties ＋ → Create property：Variant／Text／Boolean／Instance swap／Slot；Text 視窗 Name、Value → Create property | 一致 |
| 綁定文字屬性 | 選文字層，右側最上方 Content 欄旁圖示（tooltip：Apply variable/property） | 補位置 |
| Prototype 分頁 | Flow starting point ＋、Interactions ＋、Scroll behavior（Position、Overflow） | 一致 |
| Overflow | No scrolling／Horizontal／Vertical／Both directions | 一致 |
| Position | Scroll with parent／Fixed (stay in place)／Sticky (stop at top edge) | 一致 |
| 互動 | Interactions ＋ → Trigger「On click」、Action 預設 None；Action 清單：Navigate to、Change to、Back、Scroll to、Open link、Set variable、Set variable mode、Conditional、Open overlay、Swap overlay、Close overlay、Play/Pause animation、Set playhead | 一致 |
| Flow 自動建立 | 第一次連線後起點畫面上方出現「Flow 1」標籤 | 一致 |
| Animation | Instant／Dissolve／Smart animate／Move in／Move out／Push…；Move in 有 Direction ← → ↓ ↑、Easing 預設 Ease out、Duration 預設 300ms、Animate matching layers 勾選框 | 一致（方向是四個箭頭按鈕） |
| Overlay | Position：Centered、Top left、Top center、Top right、Bottom left、Bottom center、Bottom right、Manual；Close when clicking outside 與 **Background** 兩個勾選框，預設都沒勾 | 遮罩要先勾 Background |
| 預覽 | 右上播放鍵預設 Present（⌥⌘↩）；旁邊小箭頭選單有 Preview（⇧Space） | 補「直接按播放鍵會開 Present」 |
| 選取物件旁的星形圖示 | 點到會跳出對話輸入框，不是連線圓點 | 新增卡住時一列（B2） |
| 主選單 File | Save local copy…、Save to version history…、Export…、Export frames to PDF…、Duplicate | Export frames to PDF 存在 |
| 草稿頁數 | 草稿檔可加到第 4 頁 | 草稿沒有 3 頁限制；「同一頁」保留為作法建議 |

未實測：Variant 組合重複的警告字樣、名稱含「/」的匯出檔名（需下載檔案）、Scroll to 目的地下拉內容。

## GitHub（只讀）

| 項目 | 實際畫面 |
|---|---|
| New repository | Owner、Repository name、Description；Choose visibility 預設 Public；Add README 為 Off 開關；Add .gitignore「No .gitignore」；Add license「No license」；Create repository |
| Pages | Settings 側欄 Code, planning, and automation → Pages；Build and deployment → Source「Deploy from a branch」→ Branch main、/ (root) → Save；上線後顯示「Your site is live at …」與 Visit site |
| Fine-grained token | Token name、Expiration（預設 30 天）、Repository access（Public repositories／All repositories／Only select repositories）、Permissions 用 **Add permissions** 加入、Generate token |

## Photoshop（網路查證，子代理）

| 項目 | 結論 | 可信度 |
|---|---|---|
| 現行版本 | 正式版 27.11（2026-10）；28 為 beta，MAX（11/10–12）可能推出 | 多來源 |
| 存 PSD | File → Save As → Format Photoshop，有 Layers 勾選；首次可能跳 Save to cloud documents／Save on your computer | 官方＋多來源 |
| 透明 PNG | File → Export → Export As：Format PNG、Transparency、Image Size、Scale → Export；27.4 有 unknown error、27.9／27.10 有視窗問題，備援 File → Save a Copy 選 PNG（無白色 Background 時保留透明） | 官方（搜尋摘要）＋論壇 |
| Layers to Files | File → Export → Layers to Files 仍在 | 官方＋多來源 |
| Hue/Saturation | Image → Adjustments → Hue/Saturation（Ctrl／Cmd+U） | 多來源 |
| 安裝 | Creative Cloud → Apps → Install；裝好後 Open | 官方（搜尋摘要） |

## 據此修改

A1（建立檔案、左側圖示列、文字樣式）、A2（Layout guide 位置、預設 Grid）、A4（拿掉 Shift+I、Go to main component 位置、Reset instance、複製主元件會得到使用處）、A5（Add variant 取代複製＋合併、Property 1、屬性 ＋、綁定位置、Reset instance）、A6（Add variant、密碼欄做法）、B1（Preview 與 Present）、B2（星形圖示卡住列）、B4（勾 Background）、B7（Save on your computer、Layers、Transparency、Save a Copy 備援）、B8（New repository 表單、token 的 Add permissions）、COURSE-START。

## 第二輪實機（2026-11-02 下午，Figma 示範檔「工作室任務清單－示範」）

| 項目 | 實際畫面 |
|---|---|
| Variables 入口 | 左側圖示列 **Variables** → 整頁變數表；空檔時中央 **Create** → Color／Number／String／Boolean／Timing／Easing。第一個變數建立時自動產生「Collection 1」，左欄雙擊可改名 |
| 變數表 | 欄位 Name、Value；底部 **Create variable**；名稱直接打字，Tab 跳到 Value；顏色值點色塊輸入 Hex |
| 模式限制 | 表頭右側 ＋ 新增模式會跳升級視窗：Starter「1 mode for variables」「3 files to work in」 |
| 套用顏色變數 | 選圖層 → Fill 標題列的四點圖示（styles and variables）→ **Libraries** 分頁，最上方是本檔變數，下方另有 Figma 內建的 iOS 套件變數 → 點選後 Fill 欄顯示變數名 |
| 套用數字變數 | 滑鼠移到 Padding／Gap 數值欄，右端出現變數圖示 → 點開清單選變數 |
| Constraints | 選非 Auto layout 父層裡的物件 → Position 區 X／Y 右側的小圖示展開 **Constraints**：水平 Left／Right／Left + Right／Center／Scale，垂直 Top 等 |
| Min／Max | Auto layout 物件 W 欄的下拉箭頭：Fixed width、Hug contents、**Add min width…**、**Add max width…**、Apply variable…（在 Auto layout 父層內的子層另有 Fill container） |
| Wrap | Auto layout 的 Flow 四個按鈕右邊，tooltip「Wrap」 |
| 顯示開關屬性 | 選元件內圖層 → Appearance 標題列眼睛旁的圖示（tooltip：Apply variable/property）→ ＋ → 「Create property or variable」視窗：Create＝Property、Name 預設「Show 圖層名」、Value True → Create property |
| 元件互動 | 選某個 Variant → Prototype 分頁 Interactions ＋ → Trigger 清單：On click、On drag、**While hovering**、While pressing、Key/Gamepad、Mouse enter／leave／down／up、**After delay** → Action **Change to** → 下方出現屬性下拉選目標 Variant；Animation 預設 Instant |
| Dev Mode | 底部工具列 Dev Mode 圖示 → 「Upgrade to work in Dev Mode」，Starter 不能用；標註改用自製標註元件 |
| 匯出 | Export 列倍率：0.5x、0.75x、1x、1.5x、2x、3x、4x、512w、512h；格式 PNG、JPEG、SVG、PDF；Export 標題 ＋ 可再加一列（新列預設 2x），按「Export 圖層名」一次輸出 |
| 形狀工具 | 底部矩形工具旁下拉：Rectangle R、Line L、**Arrow ⇧L**、Ellipse O、Polygon、Star、**Image/video… ⇧⌘K** |
| Section | Frame 工具旁下拉：Frame F、**Section ⇧S**、Slice S |
| 圖片填色 | Fill 色塊 → 類型圖示列第四個 **Image** → **Upload from computer**；縮放模式 Fill／Fit／Crop／Tile；同面板有曝光、對比等滑桿。面板中另一個產圖按鈕屬生成功能，本課不用 |
| 底部工具列 | Draw、Design、Motion（Beta）、Dev Mode；Code（B）等其他圖示本課不用 |

決定：流程圖畫在同一個設計檔（Section＋矩形＋Arrow），不另開 FigJam，避免占用 Starter 的 3 個檔案額度。給工程師的標註用自製「Note」元件＋量測截圖。

## 第四、七輪補測（2026-11-02 晚，示範檔）

| 項目 | 實際結果 |
|---|---|
| Text property 綁到不同 Variant | 同一個 Text property 綁到 Variant2 的文字層後，Variant2 原本的「錯誤句」被換成屬性預設值「登入」。錯誤句要在使用處的屬性欄輸入 |
| Selection colors 換綁 | 選元件集，Selection colors 列出變數名（綁了變數）與色碼（沒綁）；點變數色塊 → Libraries → 選另一變數，整個元件集一次換綁 |
| 複製元件集 | 選取**整個元件集**按 Cmd+D，得到新的元件集（圖層圖示仍是元件集、含 2 Variants 與原屬性）；單一主元件按 Cmd+D 才會得到使用處（第一輪已記） |
| 外部剪貼簿 | 由瀏覽器擴充送出的 Cmd+C／Cmd+V 不會經過 Figma 剪貼簿（貼上了系統剪貼簿文字，已復原）；講義教學以 Cmd+D 為準 |

## 第九輪實作走查（2026-11-02 深夜，示範檔新頁「走查」，照 A1→A3 主線實際操作）

| 步驟 | 實際結果 | 對講義的影響 |
|---|---|---|
| 在畫面裡按 F 畫卡片 | 巢狀 Frame 預設**沒有填色**（Fill 只有 ＋），不是白色 | A1 要寫「Fill 按 ＋，再套 `Card`」 |
| Frame 的寬高位置 | 右側 **Layout** 區的 Dimensions（W、H）；巢狀 Frame 另有 Constraints 區，面板會往下推 | A1 指 W／H 位置時寫「Layout 區的 W、H」 |
| 數字欄位外按數字鍵 | 會直接改圖層不透明度（按 0 回 100%） | 卡住時表格加一列 |
| 在卡片內按 T 點一下 | 文字層直接成為卡片子層，圖層名自動等於文字內容 | A1 不必「移入卡片」；要加「把標題圖層改名 `Title`」 |
| 對已有子層的卡片按 Shift+A | 原地轉成垂直 Auto layout，子層順序保留；**Padding、Gap 依原位置推算**（實測 35／32、28），**寬度被改成 338** | A3 寫「選原本的卡片按 Shift+A，再把 Padding、Gap 改成變數、W 改回 354」，不重建子層 |
| Effects ＋ | Inner shadow、Drop shadow、Layer blur、Background blur、Noise、Texture、Glass；Drop shadow 有 Spread，但**沒有填色的圖層 Spread 是灰的** | 焦點環不用「2 px 間隔」做法 |
| Shift+G | 畫面提示「Layout guides hidden／visible」 | 確認可用 |

決定：Focus 狀態改為 2 px `Focus Ring` 外側描邊（Stroke 選 Outside），不留間隔；外側描邊對白底有足夠對比即可。
| 對單一文字按 Shift+A | 建出**水平**（Horizontal）Auto layout，Padding 水平 10、垂直 10，Gap 10，寬高 Hug，Clip content 未勾 | 按鈕、輸入區可直接得到水平排列 |
| Auto layout 的 Padding | 兩個欄位：左邊是**水平**（左右）、右邊是**垂直**（上下）；變數要兩欄各綁一次 | A3 綁 `Space 16` 要寫兩欄 |
| 新建 Frame 的 Clip content | 一般 Frame 預設勾選（內容超出會被裁切） | 卡片、畫面放不下時內容會被切掉 |
| 多選後按 Shift+A | 上下排列的兩段文字 → **垂直** Auto layout，**Padding 0／0**，Gap 依原間距推算（實測 70）；方向依物件原本排列決定 | 標籤要先左右排好，或包好後把 Flow 改成水平；多選包框不必再把 Padding 歸 0 |
| 旋轉欄位正負 | 輸入 90 → 逆時針轉 90 度（文字由下往上） | 向右箭頭：90＝向上、-90＝向下 |

## 第十輪：代理扮演零基礎學員實際試跑 A1～A3（示範檔「試跑 A1-A3」頁）

| 項目 | 實際結果 |
|---|---|
| 自動寬度文字的 W 欄 | 灰色不能輸入；在欄位外打數字會改成不透明度。要先把文字尺寸模式改 Auto height（或 Fixed）才能填 W |
| Create variable | 每按一次都要再選類型（Color、Number…）；Value 欄可以直接打 Hex |
| 變數表 | 全螢幕，看不到畫布；要按左側 File 回畫布確認；打開時不一定停在要用的集合 |
| 文字樣式名稱 | 輸入「Type / Page title」存檔後顯示「Type/Page title」（斜線兩側空格被去掉），分組仍正常 |
| 樣式與 Libraries 清單 | 會混入 Figma 內建套件（例如 Material 3）的樣式與 Error 變數；選的時候看清楚是本檔 |
| Constraints | 巢狀物件選取時，Constraints 下拉通常已顯示在 Position 下方 |
| Shift+A 推算數值 | 依原本位置推算；按鈕實測左右 Padding 116、上下 10；卡片實測 W 322、左右 Padding 0（與先前一次 338 不同）——講義不寫具體推算值 |
| Padding 綁定變數後 | 欄位顯示被框起來的數字（例如框住的 16），不是變數名稱 |
| Gap 綁定變數 | 欄位右端沒有變數圖示，要點 Gap 欄的 ▾ → **Apply variable…** |
| W 欄 Fixed | 沒有「Fixed」選項字樣；直接輸入一個數字就是固定寬度 |
| ⇧S Section | 拖出多大就是多大；手機畫面放進去前要先拉大 Section |
| 用 T 點到既有文字 | 會在那段文字裡插入，不會新建文字層 |
