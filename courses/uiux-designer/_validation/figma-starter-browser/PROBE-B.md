# Probe B：Prototype 與互動限制

**課程**：`uiux-designer`  
**Run ID**：`20260916-figma-starter-browser-001`  
**測試日期**：2026-09-16  
**工具**：Google Chrome（Figma 網頁版）  
**方案**：Figma Starter／Free  
**工作檔**：`Codex Figma Starter Audit - Probe B Overlay`  
**工作檔 URL**：`https://www.figma.com/design/OdwdoNhWJCsC9a8wq17Dy3/Codex-Figma-Starter-Audit---Probe-B-Overlay?node-id=1-6&t=jtKgRBGCgpow3bxF-0`  
**整體判定**：`CONDITIONAL`

## 實測步驟與結果

| Step | 操作 | 實際觀察 | 判定 |
|---|---|---|---|
| B-01 | 在獨立頁建立 `Screen / Host`（402×874）與 `Dialog / Overlay`（320×200），在 Overlay 放入 `確認完成` | 兩個同層畫面可建立；Overlay 文字在編輯器中可見 | `MACHINE_PASS` |
| B-02 | Prototype → `Add action`，查看 Action 選單 | 選單提供 `Navigate to`、`Back`、`Scroll to`、`Open overlay`、`Swap overlay`、`Close overlay`、`Open link` 等；也列出變數／條件相關動作 | `MACHINE_PASS` |
| B-03 | 設定 `On click → Open overlay → Dialog / Overlay`，保留 Centered 與 Instant；加入 Flow starting point 後開啟 Present | Figma 顯示單一 `Click → Dialog / Overlay` 互動；在 Chrome 預覽中點擊主畫面後，畫面出現 Overlay 文字 `確認完成` | `MACHINE_PASS` |
| B-04 | 嘗試在同一 Starter 原型再建立第二個 action | 直接跳出 `You cannot create multiple actions with your current plan`；對話框列出 Starter 的 `Interactive prototypes`，並將 Professional 的 `Multiple action prototypes`、`Variables in prototypes`、`Conditional prototypes` 列為升級項目 | `CONDITIONAL` |
| B-05 | 在 Probe A 的 `Navigate to` 動作檢查 Animation | 下拉選單實際包含 `Instant`、`Dissolve`、`Smart animate`、`Move in`、`Move out`、`Push`、`Slide in`、`Slide out`；已將現有導覽動作選為 `Smart animate` | `MACHINE_PASS_PARTIAL` |
| B-06 | 在 Probe A 選取清單畫面，檢查 Scroll behavior | `Overflow` 提供 `No scrolling`、`Horizontal`、`Vertical`、`Both directions`；已設為 `Vertical` | `MACHINE_PASS` |

## 已驗證的課程邊界

- 免費 Starter 瀏覽器版可以建立並預覽一個單一 Overlay 互動。
- Overlay 設定面板提供置中位置、`Close when clicking outside`、背景與動畫欄位；本輪只以預設 `Centered`／`Instant` 驗證開啟，不把關閉規則宣稱為已通過的獨立測試。
- `Navigate to` 的 `Smart animate` 選項在實際面板存在；若要教圖層匹配與多步驟流程，必須先處理 Starter 的單一 action 限制。
- Prototype 預覽的實際畫面應使用可辨識內容；空白 Frame 即使連線成功，也不容易在預覽中判斷是否真的換頁。

## 方案限制對課程的影響

課程的免費主線不能把「登入 → 清單 → Dialog → Toast」寫成同一個可連續操作的 Figma Starter 原型。可行的教學契約是：每個檔案只驗收一個核心互動（例如 `On click → Open overlay`），再以獨立小檔案示範另一種動作；若課程要求同一檔案多個 action、Variables 或 Conditional，必須明示 Professional／付費方案條件，不能列為免費主線完成物。

## 尚待補測

- `Close overlay`、`Swap overlay` 的獨立預覽行為。
- `Smart animate` 兩個有相同圖層名稱的畫面之間的實際動態效果；本輪已確認選項存在，但未另建有差異內容的雙畫面驗收檔。
- 固定元素與垂直滾動同時成立的 Preview 驗收。
- Toast、Dialog、Navigation 的完整任務串接；受 Starter 單一 action 限制，不能在同一檔案直接宣稱通過。

## Probe B 結論

Probe B 放行「單一互動可驗收」的教學活動，並將多 action 原型改為方案條件／拆檔策略。G1 仍不能放行完整 Prototype 課程，直到課程矩陣明確標示每一個免費檔案的單一 action 邊界，以及人工後續要檢查的互動細節。

