# Figma Starter／瀏覽器版實務稽核

**課程**：uiux-designer  
**建立日期**：2026-09-07  
**目前狀態**：`NOT_RUN`  
**適用環境**：Figma Starter 免費方案、瀏覽器版

## 稽核目的

確認 99h 課程中的每一項必修操作，都能在學員實際使用的免費瀏覽器環境中完成。沒有實際畫面、操作路徑與失敗紀錄，不宣稱功能可教，也不鎖定單元時數。

## 已知方案邊界（需以實際帳號再確認）

依 Figma 官方說明，Starter 可使用 Auto Layout、Components、Prototypes 與 Inspect；Variables／expressions／conditional logic、Libraries 與 Dev Mode 涉及較高方案或席次限制。Overlay、Smart Animate、靜態匯出雖可用，但仍須以實際 UI 路徑與限制驗證。

- [Figma plans and features](https://help.figma.com/hc/en-us/articles/360040328273-Figma-plans-and-features)
- [Guide to auto layout](https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout)
- [Create overlays in your prototypes](https://help.figma.com/hc/en-us/articles/360039818254-Create-Overlays-in-your-Prototypes)
- [Smart animate layers between frames](https://help.figma.com/hc/en-us/articles/360039818874-Smart-animate-layers-between-frames)
- [Export static designs from Figma](https://help.figma.com/hc/en-us/articles/360040028114-Export-static-designs-from-Figma)

## 三組最小實測

### Probe A：介面系統與內容壓力

- **範圍**：Frame、Auto Layout、Component、Instance、Variants、Button、Form、List。
- **測試材料**：一個手機登入／清單畫面；加入長中文、空狀態、錯誤狀態與增刪項目。
- **必須記錄**：實際按鈕與面板名稱、文字是否推動版面、元件狀態是否同步、是否出現重疊或不可編輯狀態。
- **完成證據**：一張可重開的 Figma 檔案、操作截圖、問題與修復紀錄。

### Probe B：Prototype 與互動限制

- **範圍**：觸發事件、互動連結、轉場、Overlay、Swap、Scroll、固定元素、Smart Animate。
- **測試材料**：登入 → 清單 → Dialog → Toast 的手機任務流程。
- **必須記錄**：互動是否能在 Preview 重現、Overlay 關閉規則、滾動與固定元素是否同時成立、Smart Animate 是否因圖層命名／Overlay 限制失效。
- **完成證據**：一個可操作 Prototype、任務腳本、錯誤清單與修正版。

### Probe C：輸出與交付

- **範圍**：PNG／JPG／PDF 匯出、分享權限、Inspect、資產命名、Git/GitHub 交付與公開部署。
- **測試材料**：同一份手機頁面與一個最小 HTML/CSS 網頁。
- **必須記錄**：免費方案可否完成每個交付步驟、連結權限、下載格式、Git/GitHub 是否只是課程外部交付流程。
- **完成證據**：匯出檔、分享連結、Git commit、公開網址與回復步驟。

## 判定規則

| 狀態 | 判定 |
|---|---|
| `PASS` | 講師可在免費瀏覽器版重現，學員可依步驟完成，且有成品證據。 |
| `CONDITIONAL` | 功能可用但有方案、權限、介面版本或可靠性限制，改列限定情境或選修。 |
| `BLOCK` | 免費方案不可用、操作路徑不穩定、需要付費席次，或沒有可交付成果。 |
| `NOT_RUN` | 尚未在實際帳號與瀏覽器完成測試；不得寫入正式教案作為已驗證功能。 |

## 目前結果

| Probe | 結果 | 原因 |
|---|---|---|
| A 介面系統與內容壓力 | `NOT_RUN` | 尚未取得實際 Figma Starter 工作檔與操作紀錄。 |
| B Prototype 與互動限制 | `NOT_RUN` | 尚未取得實際 Figma Starter Prototype 與 Preview 紀錄。 |
| C 輸出與交付 | `NOT_RUN` | 尚未完成免費方案的匯出、分享、Git/GitHub、部署連續流程。 |

## 放行條件

1. 三組 Probe 都有可重開的檔案、截圖或錄影、步驟與結果。
2. 任何付費限定功能都從必修主線移出，並標示方案條件。
3. 以 60–90 分鐘零基礎試教驗證至少一條代表路徑。
4. 試教前不鎖定 99h 時數、不建立正式講義或 HTML。
