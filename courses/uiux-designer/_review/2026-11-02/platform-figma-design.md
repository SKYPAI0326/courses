# Part A 平台現況核對（Figma 設計段）

核對：fresh-context 子代理，2026-11-02，唯讀。範圍：part1 CH1～CH8、對應 START-HERE、COURSE-START。

## 需修改

| 頁 | 講義原句 | 現況 | 來源 | 嚴重度 |
|---|---|---|---|---|
| COURSE-START、A1 | 進入 Drafts，建立 New design file | Drafts 頁右上 **+ Create** → Design | help.figma.com/hc/en-us/articles/360038511153 | 誤導 |
| COURSE-START | 不要選 FigJam、Slides 或 Make | 另有 Sites、Buzz | help.figma.com/hc/en-us/articles/13838684089751 | 輕微 |
| A1 | 在右側 Text 設定字級 | UI3 區塊名是 **Typography** | help.figma.com/hc/en-us/articles/30938465113751 | 誤導 |
| A1 | 文字樣式入口通常在 Text 樣式圖示 | Typography 區塊的樣式圖示 → Create style | help.figma.com/hc/en-us/articles/360039957034 | 輕微 |
| A1、A3、A6～A8 | Auto height（未寫位置） | 文字尺寸模式在右側 **Layout** 區塊 | help.figma.com/hc/en-us/articles/27378154668951 | 輕微（跨 5 頁） |
| A2 | Layout guides／Layout grid | 2025-05 起名為 **Layout guide**，入口 Add layout guide；只有 Frame 能加；開關 Shift+G | help.figma.com/hc/en-us/articles/360040450513 | 輕微 |
| A2 | 若只看到方格 Grid，改成 Columns | 新增後預設 **Uniform grid**，從類型下拉改 Columns；Auto layout 的「Grid」是另一功能 | 同上 | 誤導 |
| A3 | 父 Hug、子 Fill 會互相等待 | 子層設 Fill 後父層在該軸自動變 Fixed | help.figma.com/hc/en-us/articles/360040451373 | 輕微 |
| A4 | 主元件右鍵 Create instance | 無此選項；改用 Assets 拖曳、Shift+I、Insert instance、複製既有 Instance | help.figma.com/hc/en-us/articles/360039150173 | 阻斷 |
| A4 | Corner radius 從 4 改成 12，再還原為 8 | 前一堂沒設圓角，預設 0；4 與 8 前後矛盾 | — | 誤導 |
| A4 | Reset overrides | 現名 **Reset → Reset all changes**，也可單項重設 | help.figma.com/hc/en-us/articles/360039150733 | 誤導 |
| A5 | 文字內容設定旁找 Create text property | 選主元件或元件集 → **Properties** 區塊新增 → Text → Create property；再選各 Variant 文字層，用 **Apply variable/property** 綁定 | help.figma.com/hc/en-us/articles/5579474826519 | 阻斷（連帶 A6～A8 改 Label） |
| A5 | 建立另一個 Variant property | Add property 旁新增鈕 → Variant | help.figma.com/hc/en-us/articles/360056440594 | 輕微 |

## Starter 方案現行事實（查閱日 2026-11-02）

- 檔案：Design＋Sites 共 3 個、FigJam 3、Slides 3，放在唯一資料夾；**Drafts 不限數量**，只能邀請 can view。
- 版本紀錄 30 天；無 Team library、Dev Mode、Sites 發佈。
- 原型：同一觸發多動作與條件只開放付費方案（講義寫法正確）。
- Starter Design 檔限 3 頁；草稿是否同限未確證。本課作品放在單一頁面即可避開。
- 來源：help.figma.com/hc/en-us/articles/13838684089751、figma.com/pricing

## 待實機確認

草稿檔頁數上限；Shift+A 建出 Frame 的預設圓角；元件重複組合的警告字樣；右鍵是否有 Combine as variants；「屬性=值」命名是否自動建立屬性；Auto height 圖示位置；存檔同步狀態顯示位置。
