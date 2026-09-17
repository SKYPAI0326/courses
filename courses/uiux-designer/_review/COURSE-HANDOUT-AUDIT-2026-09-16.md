---
course: uiux-designer
review: learner-handout-and-copy
date: 2026-09-17
status: MACHINE_READY_PENDING_HUMAN
---

# UI/UX 講義與文案品質審查

## 審查目的

確認學員只拿到入口頁、單元頁與列出的素材，就能理解工作情境、取得起始材料、完成一個可觀察成果，並把成果交給下一個單元。文案審查依 `uiux-designer/_design/COPY-RISK-GATE.md` 檢查公式化對比、空泛過場、模糊權威、宣傳詞與結構指紋；掃描器只把公式化對比列為 BLOCK，其他訊號交給人工判讀。

## 課綱主軸對照

正式大綱的主軸是：

```text
介面元素與設計（42h）
→ UI/UX 原型製作與資料打包（57h）
→ 可測試、可交接、可版本化的設計成果
```

目前已有 99h 的學員頁／教案內容；A1～A8、B1～B8 均有 learner-facing 頁面與對應教案，並完成本機結構檢查或機器試點。真人冷讀、跨帳號重跑與外部工具驗證仍待完成：

| 試點單元 | 時數 | 新增能力 | 交給下一段的成果 |
|---|---:|---|---|
| A1 視覺基礎 | 5h | 色彩角色、Typography scale、兩段長錯誤訊息檢查 | `Visual foundations` 頁面、色彩／文字樣式表、完成檢查紀錄 |
| A2 格線與版面基準 | 6h | 手機／桌面 Frame、欄數、邊界、間距與對齊壓力 | 手機與桌面 Frame、格線設定表、對齊檢查紀錄 |
| A3 Auto Layout | 6h | 固定寬度、Auto height、長文字壓力測試 | 手機 Frame、設定值、壓力紀錄 |
| A4 Component／Instance | 5h | 從 Auto Layout 容器建立主元件、從 Assets 插入 Instance、辨認編輯邊界 | `Login / Heading` 主元件、Instance、Layers／Assets 證據 |
| A5 Variants／Properties | 6h | 從單一主元件建立 Default／Error，讀取 Property／Value 並切換 Instance | `Login / Heading` component set、兩個 Value、狀態截圖與修復紀錄 |
| A6 Button／Form | 6h | 建立 Button component set、Primary／Disabled Value，整理 Form 三層圖層與互動邊界 | `Button / Primary` component set、Form Label／Input／Helper、未測試邊界紀錄 |
| A7 List／內容變化 | 4h | 建立兩個 List row、長標題與空狀態，使用 Auto height 檢查內容壓力 | `Row 01`／`Row 02`、Title W/H、`Empty / Message` 與壓力紀錄 |
| A8 Toast／Dialog／Navigation | 4h | 建立回饋、彈窗與導覽的視覺層、尺寸與文字責任 | `Toast / Success`、`Dialog / Confirm`、`Navigation / Header` 與狀態表 |
| B1 線框／原型／手機入口 | 7h | 將任務寫成畫面清單，建立兩個手機 Frame 與 Prototype 起始點 | `TASK-01`、`SCR-01`／`SCR-02`、`Flow / Login`、`Flow / List`、起始點截圖 |
| B2 觸發事件／互動連結 | 6h | 在獨立 Starter 測試檔建立一個核心 Navigate action，使用 Preview 回歸 | `CASE-B2-01`、Interaction row、Actual／Expected、方案邊界紀錄 |
| B3 轉場／動效目的 | 6h | 依任務目的選擇 Animation，分開記錄面板設定與 Preview 實際效果 | `MOTION-01`、轉場選擇表、Expected／Actual、Smart animate 邊界 |
| B4 Overlay／Swap | 7h | 一檔一核心 action、Open overlay、Swap 分支、Chrome Preview | Overlay／Swap 測試檔、來源／目的地與 Preview 證據 |
| B5 滾動／固定／漂浮 | 6h | Vertical overflow、長內容 Preview、固定 Header 與 Floating Action 的分項檢查 | `SCROLL-01`、`CASE-B5-01`、上滑 Expected／Actual、固定／遮擋邊界 |
| B6 任務測試 | 6h | 任務腳本、Actual／Expected、單一變因回歸 | 測試表與修正紀錄 |
| B7 Handoff | 6h | PNG／PDF／Inspect、限制清單 | 可追溯的 Handoff 包 |
| B8 網頁與 Git | 13h | 最小 HTML／CSS／JavaScript、本機驗證、Git commit | 可在 Chrome 開啟的網站與版本紀錄 |

B4 已補到正式 7h 範圍，加入 Overlay／Swap 的概念差異、`SWAP-01` 獨立測試、Expected／Actual 與方案邊界。A1～A8、B1～B8 的畫面規格、操作步驟、單一變因、回修路徑與交接條件均已寫入；B6 補上固定任務測試的完整欄位與回歸流程，B7 補上 Handoff 輸出與版本條件，B8 補上 Chrome／手機寬度／Git 的檢查與回修路徑。真人冷讀與跨帳號重跑仍未完成，課程狀態維持待驗證。

## 零基礎學員路徑

目前 A3 等操作單元已按下列順序組織；入口頁則只保留學員需要的課程故事與兩階段地圖：

```text
情境與代價
→ 起始材料與取得方式
→ 完成物預覽
→ 白話概念與判斷規則
→ 完整示範
→ 同步跟做
→ 單一變因練習
→ Checkpoint 與修復
→ 驗收與下一單元接手
```

代表性結果：

- A3 已補上短句／壓力句、402×874 Frame、200 px 寬度、Auto height／Hug、Layers 層級、6 步跟做、2 個 Checkpoint、錯誤修復與下一步 B4。
- A4 已補上主元件／Instance 的情境、完成物、起始材料、8 步示範、8 步同步操作、單一變因練習、編輯邊界修復與第 05 堂交接條件；Variants 與 Property 明確留給下一堂。
- B4 已補到 7h：包含 Figma Starter／Chrome 的環境契約、Frame 尺寸、Overlay action、Swap 分支、Preview 結果、方案限制、Solo 變化與 B5／B6 接手條件。
- B1 已補上任務情境、任務卡、畫面清單、Frame 基準、Prototype 起始點、8 步跟做、Solo 長標題、修復路徑與 B2 交接條件；起始點與互動 action 分開驗收。
- B2 已補上單一 action 情境、CASE 驗收卡、Trigger／Action／Destination 概念、7 步跟做、Solo 標題替換、修復路徑與 B3／B4 交接條件；多 action、Variables、Conditional 與後續互動均保留方案邊界。
- B3 已補上轉場問題、任務目的選擇表、Dissolve／Instant 示範、Smart animate Solo、7 步跟做、修復路徑與 B4／B5／B6 交接條件；面板選項與實際動態效果分開記錄。
- B5 已補上長清單情境、Overflow 判斷、Vertical 示範、8 步跟做、十二筆 Solo 變化、固定／漂浮修復路徑與 B6 交接條件；設定值、上滑結果與固定／滾動聯合行為分開記錄。
- B6、B7、B8 已補齊九段 learner-facing 結構並保留產物鏈；真人冷讀與跨帳號重做仍待人工 Gate。

### 入口頁重建（2026-09-16）

上一版入口把 A3、B4、B6、B7、B8 的製作編號、機器試點狀態與教師驗證連結直接放在學員視線內，學員無法從頁面判斷「我正在處理什麼工作、先留下什麼、下一步為何」。這與正式大綱的零基礎順序和學員入口規則不一致。

新版入口移除試點卡片與內部狀態，改為：

- 先用登入與內容列表的工作情境交代問題與後果。
- 用成果表說明介面規則、Figma 元件、可測試原型、交付與網站之間的關係。
- 用連續流程說明每個單元的學習節奏：情境、示範、跟做、變化、驗收與交接。
- 用「介面元素與設計 42h」及「UI/UX 原型製作與資料打包 57h」對照正式課綱，保留 Photoshop、Git/GitHub 與部署範圍。
- 製作紀錄與機器證據留在 `_review`、`_validation`，不再放入學員入口。
- 入口 → 視覺基礎 → 格線與版面 → Auto Layout → Component → Variants → Button／Form 的連結已在 Chrome 實際點擊；每一堂的下一個連結只在對應頁面產出後開放。

## 文案修訂規則

### 本次移除的生成式對比句型

學員頁與六份試點教案已通過 `docs/audit-copy-patterns.py --strict`，目前為 `0 BLOCK / 0 REVIEW`。原本的句型已改成直接描述：

- 說明學員要做的工作與可見結果。
- 說明平台限制與可用的備援路徑。
- 說明錯誤現象、回修位置與重跑條件。
- 說明上一段產物如何成為下一段輸入。

本輪曾出現的 REVIEW 例子已改成可觀察的文字、尺寸與操作結果；後續新增內容仍需逐行人工判讀，不能只看掃描器結果。

### 仍可使用的否定句

操作需要排除錯誤時，可以寫「若高度仍為 Fixed height，回到第 5 步」，因為它指向可觀察狀態與修復位置。品質閘門禁止的是反覆用抽象對比句濃縮課程定位，不禁止必要的錯誤提示。

## 審查命令與結果

```text
python3 docs/audit-copy-patterns.py --strict uiux-designer ../_lessons/uiux-designer
Copy pattern audit: 0 finding(s) (0 BLOCK, 0 REVIEW)

python3 .../audit_copy_continuity.py <each learner page and lesson plan>
All current UI/UX pilot pages: 0 warning(s)
```

另外已檢查入口頁與 A3 頁的本地連結，素材檔、起始頁、Probe 摘要與下一單元連結均存在。入口頁已在 Chrome 實際載入並以可及性樹與畫面檢查。

## 尚未放行的內容

- A1～A8、B1～B8 雖已產出，真人冷讀與跨帳號重跑仍待完成；B6～B8 已完成頁面結構與路徑對齊，仍需人工確認學習節奏與工具操作。
- Form 多欄位、List 多列增刪、Swap、固定元素與滾動同時成立、完整 Smart Animate、Photoshop 實際輸出、GitHub push、公開部署仍維持 `CONDITIONAL` 或 `NOT_RUN`。
- A3、B4、B5、B6、B7、B8 尚未完成真人冷讀、跨帳號重建與連續單元人工微序列驗收。

## 結論

目前完成的是「A1～A8、B1～B8 共 99h 的講義與教案、機器檢查及本機互動試跑」，但不是 99h 正式放行課程。下一個循環應安排全 16 單元的冷讀與跨帳號重跑，並完成固定／滾動聯合行為、Swap、Photoshop、GitHub／部署等外部或方案邊界驗證，再依同一份 Blueprint、Coverage Ledger、Environment Contract 與文案閘門回填證據。
