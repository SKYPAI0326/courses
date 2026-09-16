---
course: uiux-designer
status: MACHINE_VERIFIED_BASELINE
verified_at: 2026-09-16
---

# Environment Contract：Figma 免費瀏覽器課程

本契約是教案、素材、Computer Use、HTML 講義與驗收共同使用的環境邊界。凡是沒有在這份契約或 Probe 證據中出現的操作，不得寫成「學員一定可以完成」。

## 基線

| 欄位 | 已驗證值 | 證據 |
|---|---|---|
| 設計工具 | Figma 網頁版 | `PROBE-A.md`、`PROBE-B.md` |
| 方案 | Starter／Free | Figma UI 顯示 `Free`、`2 free pages left` |
| 瀏覽器 | Google Chrome | 三組 Probe 均在 Chrome 完成 |
| 工作檔 | Codex Figma Starter Audit - Probe A／Probe B Overlay | Probe 工作檔 URL 與匯出檔 |
| 語言材料 | 繁體中文、長文字、錯誤訊息 | Probe A 長中文內容 |
| 版本交付 | 本地 Git 工作樹，`origin` 指向 GitHub | Probe C、Git commit |
| 真人狀態 | 尚未進入真人試跑 | `_gates.md`，不得標記 `HUMAN_PASS` |

## 可列入免費主線的能力

- Frame 尺寸與命名、Auto Layout、Component、Variant、Instance。
- 長中文換行、Auto height、固定寬度與基本按鈕／錯誤輔助列結構。
- 每個測試檔一個核心 Prototype action；單一 `On click → Open overlay` 已在 Preview 重現。
- `Navigate to` 面板中的轉場選項、`Smart animate` 選項、Vertical overflow 控制。
- PNG／JPEG／SVG／PDF 匯出與 Dev Mode CSS／Inspect 入口。

## 方案與可靠性限制

| 限制 | 課程處理 |
|---|---|
| Starter 同一原型建立第二個 action 會顯示方案限制 | 免費主線採「一個測試檔、一個核心互動」；多步驟故事拆成多個小檔，或標示 Professional 條件 |
| Variables／Conditional prototypes 出現在升級提示 | 不列免費必修；只作方案辨識練習 |
| Instance 的主 Auto Layout 控制呈 disabled | 講義明示回主元件修改，不把 disabled 誤判為錯誤 |
| Variant 直接命名可能出現 property 格式警告 | 用右側 Property 值管理狀態，提供失敗／修復段落 |
| 直接對畫布 contenteditable 重填可能串接舊字串 | 優先使用右側 Content textarea，做畫布與面板雙重檢查 |
| Share 權限、GitHub push、公開部署改變外部狀態 | 機器階段只檢查入口與本地交付；不代替使用者公開或付費 |

## 備援路徑

1. Figma 登入或方案畫面不同：先記錄 UI 版本與可見方案，再停止宣稱功能通過。
2. 免費檔案或頁面數量不足：使用已有獨立測試檔，不刪除正式檔或改變分享權限。
3. Prototype 第二個 action 被擋：把該操作拆到新測試檔，並在學習成果標示「拆檔」而非隱藏限制。
4. 匯出按鈕不存在：保留 Figma 檔與 Inspect 證據，將輸出項目降為 `CONDITIONAL`，不以截圖替代正式匯出。
5. 機器階段無法判斷學員是否理解：標為 `MACHINE_READY_PENDING_HUMAN`，等待真人冷跟做。

## 重跑規則

- Figma／Chrome 版本、方案、登入帳號或 UI 主要控件改變時，先重跑 Probe A／B／C。
- 先修正契約與操作清單，再回修教案與 HTML；不直接批次替換所有頁面文字。
- 所有重跑追加到 `uiux-designer/_validation/autonomous-run/RUN-LOG.jsonl`，保留原始結果與回復方法。

