---
course: uiux-designer
status: PASS1_MACHINE_EVIDENCE
---

# Core Operation Inventory：核心操作清單

每一列是一個學員可以重播、觀察與修復的操作。功能名稱本身不是學習成果；可見結果與驗收方式才是。

| ID | 單元 | 前置 | 輸入／動作 | 可見結果 | 驗收 | 失敗／修復 | 證據 |
|---|---|---|---|---|---|---|---|
| OP-A01 | A2 | 空白頁 | Frame → W402、H874 | 手機畫板出現 | 尺寸與命名可讀 | 找不到欄位時切 Design 面板 | PROBE-A A-01 |
| OP-A02 | A2 | Frame | Layers rename | `Mobile / Login & List` | 名稱可在 Layers 找到 | 雙擊 row 重命名 | PROBE-A A-02 |
| OP-A03 | A3 | Frame／容器 | Toggle auto layout → Vertical | 右側勾選、方向可見 | 長文字不重疊 | 回到父層再開啟 | PROBE-A A-03 |
| OP-A04 | A3 | Text | Text → canvas → `登入` → Shift+A | 文字被 Auto Layout 包住 | Layers 層級正確 | 先選文字再 Shift+A | PROBE-A A-04 |
| OP-A05 | A4 | Auto Layout | Create component | Assets 有 component | 可插入 instance | 選取容器而非子文字 | PROBE-A A-05 |
| OP-A06 | A4 | Component | Assets → Insert instance | 畫布出現 instance | 右側顯示 From this file | 找不到 component 時開 Assets | PROBE-A A-07 |
| OP-A07 | A5 | Component set | Add variant | 出現第二 variant | Property 值可切換 | 單一詞命名會警告；改 Property 值 | PROBE-A A-06 |
| OP-A08 | A5 | Instance | Property 1 → Error | Instance 顯示 Error 狀態 | combobox 值正確 | 回主元件檢查 property | PROBE-A A-07 |
| OP-A09 | A3 | Text layer | 右側 Content textarea 填長中文 | 畫布換行 | 內容與面板一致 | 避免直接 contenteditable；重填右側 textarea | PROBE-A A-08 |
| OP-A10 | A3 | Long text | Auto height、W200 | H Hug、內容換行 | 不重疊 | 重選 Auto height | PROBE-A A-08 |
| OP-A11 | A6 | Component variant | Rectangle W280×H48、rename Button / Primary | 按鈕視覺層 | 尺寸／命名存在 | 已在 component set 內時只作視覺模式 | PROBE-A A-09 |
| OP-A12 | A7 | Long text | Duplicate、rename List / Error helper | 錯誤輔助列層 | Layers 可找 | 重新選 row 再命名 | PROBE-A A-10 |
| OP-B01 | B1 | 任務需求 | 寫畫面清單與起始 Frame | Flow 起點清楚 | 有第一個完成物 | 先寫任務再開 Prototype | PROBE-B B-01 |
| OP-B02 | B2 | 兩個同層 Frame | Prototype → Add action | Interaction row 出現 | action 目的清楚 | Starter 只保留一個 action | PROBE-B B-04 |
| OP-B03 | B2 | Host／Destination | On click → Navigate to | 目的地可選 | Preview 可操作 | 空 Frame 無法判讀時加辨識文字 | PROBE-B B-05 |
| OP-B04 | B4 | Host／Overlay | On click → Open overlay | Overlay action row | Preview 顯示對話框 | 目的地需是獨立 Frame | PROBE-B B-03 |
| OP-B05 | B5 | Frame | Overflow → Vertical | 右側值改變 | 長內容有滾動條件 | 若預覽無滾動，降為待測 | PROBE-B B-06 |
| OP-B06 | B3 | Navigate action | Animation → Smart animate | 下拉值為 Smart animate | matching layers 待回歸 | 用相同命名／層級重建雙畫面 | PROBE-B B-05 |
| OP-B07 | B7 | Selected Frame | Add export settings | Export row 與 Export button | 格式可選 | 無 Export 時切 Design | PROBE-C C-01 |
| OP-B08 | B7 | Export row | File type → PNG／PDF → Export | 下載 zip 內含檔案 | file／尺寸可驗證 | 檢查 Downloads 與 zip 內容 | PROBE-C C-02–C-04 |
| OP-B09 | B7 | Selected layer | Toolbelt → Dev Mode | Inspect／Code／CSS | 可讀 Layout／Colors | Back to Design Mode 恢復 | PROBE-C C-05 |
| OP-B10 | B8 | 本地專案 | git status／commit | 版本可重現 | commit 與證據對應 | 不使用 git add -A | PROBE-C C-06 |

## 未通過或尚待補測的操作

`Form` 多欄位、`List` 多列增刪、`Close overlay`、`Swap overlay`、固定元素與滾動同時成立、完整 Smart Animate 預覽、Photoshop 實際輸出、GitHub push、公開部署，都不能由相鄰操作推定完成；各自維持 `CONDITIONAL` 或 `NOT_RUN`。

