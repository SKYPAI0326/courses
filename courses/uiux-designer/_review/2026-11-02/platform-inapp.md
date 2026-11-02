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
