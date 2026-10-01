---
course: uiux-designer
status: MACHINE_BLUEPRINT_DRAFT
official_hours: 42h + 57h = 99h
machine_evidence: PROBE-A-CONDITIONAL / PROBE-B-CONDITIONAL / PROBE-C-CONDITIONAL
---

# Course Blueprint：從介面規則到可交付原型

> 學員任務契約唯一來源：[`LEARNER-CONTRACT-MATRIX-2026-09-17.md`](./LEARNER-CONTRACT-MATRIX-2026-09-17.md)。操作講義、起始材料與完成檢查表只能把同一組角色、問題、材料、成果、下一位使用者、第一個動作與回復路徑轉成適合頁面的說法；若證據尚未存在，保留 `BLOCK` 或 `PENDING_HUMAN`。

## 學員故事

學員接到「工作室任務清單」需求：需要一個手機登入／清單流程，能在 Figma 建立一致的介面規則、呈現錯誤與回饋、做一個可預覽的核心互動，再把視覺資產、檔案、版本與最小網站整理成交付包。學員不預設 Figma、Photoshop、Git 或 JavaScript 經驗；講義必須讓他知道下一步、預期畫面、卡住時回到哪裡。

## 產物依賴圖

```text
色彩 token + Typography scale
  -> 格線規格 + 手機 Frame
    -> Auto Layout 登入／清單畫面
      -> Component + Variant + Instance
        -> Button / Form / List / Dialog / Navigation 視覺狀態
          -> 單一核心 Prototype action（必要時拆檔）
            -> 任務測試與修正紀錄
              -> PNG/PDF/Inspect/Handoff package
                -> 最小 HTML/CSS/JS + Git commit + GitHub 版本紀錄
                  -> 部署候選網址（真人／發布階段確認）
```

## 單元契約

每個單元都必須回答：

1. 學員在什麼工作情境使用它？
2. 開始前拿到哪個檔案、文字或畫面？
3. 這次新增哪個不可由前一單元推測的能力？
4. 完成時留下哪個可重開、可檢查的檔案或紀錄？
5. 下一單元如何直接使用這份產物？
6. 如果操作失敗，能回到哪個安全 checkpoint？

## Part A：介面元素與設計（42h）

| Unit | 核心產物 | 機器證據 | 設計處理 |
|---|---|---|---|
| A1 | 色彩 token、Typography scale、長文字規則 | Probe A 長中文內容 | 先建立用途與判斷規則，不只挑色 |
| A2 | 手機／桌機格線與安全邊界 | Frame 402×874 | 以實際手機畫板作為下一單元輸入 |
| A3 | Auto Layout 壓力測試畫面 | Auto height、固定寬度 200、換行 | 把「內容變長」列為必做驗收 |
| A4 | Component 與 Instance | Assets insert instance | 明示主元件／Instance 編輯邊界 |
| A5 | Variants／Property 狀態表 | Login Heading／Error | 把 property 命名警告寫進修復路徑 |
| A6 | Button／Form 狀態 | Button visual pattern；Form 待補測 | 不宣稱表單行為已由 Probe A 通過 |
| A7 | List 空／錯誤／增刪狀態 | Error helper layer；多列待補測 | 內容變化需用 Auto Layout 回歸 |
| A8 | Toast／Dialog／Navigation 視覺規格 | Overlay 文字與視覺樣式；行為在 B | 結構與行為分開，不重複計時 |

## Part B：UI/UX 原型製作與資料打包（57h）

| Unit | 核心產物 | 機器證據 | 設計處理 |
|---|---|---|---|
| B1 | 任務流程、畫面清單、手機 Prototype 入口 | Probe A/B 檔案 | 先定義完成物，不先教功能清單；入口與 action 分開驗收 |
| B2 | 一個可回歸的核心 action | Navigate／Open overlay UI | 免費主線一檔一 action；多步驟拆檔；Interaction row 與 Preview 分開留證 |
| B3 | 轉場選擇表與一個可預覽動作 | Smart animate 選項 | 面板值與 Preview 分開留證；完整動態效果列 `MACHINE_PASS_PARTIAL` |
| B4 | Dialog／Overlay 測試檔 | Chrome Preview 顯示 `確認完成` | `Close`／`Swap` 另立小檔或條件路徑 |
| B5 | `SCROLL-01` 長內容、Vertical overflow、固定 Header 與 Floating Action 測試 | Vertical 選項、上滑 Expected／Actual | 固定／滾動同時成立尚待測，不假設成功 |
| B6 | 任務測試表、錯誤清單、回歸紀錄 | Probe evidence schema | 將失敗修復寫入學員完成物 |
| B7 | Figma／PS export 與 Handoff package | PNG/PDF/Inspect | Figma export 可教；Photoshop需另驗證 |
| B8 | 最小網站、Git/GitHub、部署候選 | 本地 Git／origin 存在 | push／公開網址保留發布階段 |

## 課程節奏

每個教學單元採固定循環：

`情境與完成物 → 一次完整示範 → 同步操作 → Checkpoint → 單一變因練習 → 錯誤修復 → 交付檢查 → 下一單元接手`

任何活動若沒有新能力或可驗收產物，就不能拿來填滿 99h。

### 頁面角色與轉段契約

每個學員會點開的材料頁、操作講義頁與外部工具工作區，必須在第一次使用前各自標示角色：

| 角色 | 提供內容 | 學員在哪裡完成動作 |
|---|---|---|
| 起始材料頁 | 案例輸入、基準值、完成條件、檢查表 | 只讀取與確認材料 |
| 操作講義頁 | 情境、示範、一步一檢查、卡關修復、交接 | 依段落前往指定工具 |
| 工具工作區 | Figma、Chrome、Photoshop、Git 或部署平台中的實際產物 | 建立、修改與保存成果 |

每個跨頁連結必須同時交代：目前頁面角色、下一頁角色、下一個工具動作，以及返回後的段落錨點。連結文字不能只寫「學習頁」「查看詳情」等無目的名稱。

每個操作型單元的第一個工具流程必須拆成單一狀態變化：取得材料 → 開啟工具 → 建立工作檔 → 建立或命名第一個物件。每一步都要有可觀察結果與停止條件；人工驗證若無法用一句話說明目前頁面、頁面用途與下一個工具動作，該段標記 `BLOCK`，不得繼續。

## 放行邏輯

- Probe 結果目前都是 `CONDITIONAL`，所以 blueprint 先可用於教案設計，但不代表 G1 真人放行。
- 付費提示、分享權限、公開部署、真人可理解性都保留到對應 Gate。
- 第一階段完成後最高只能標 `MACHINE_READY_PENDING_HUMAN`。
- 學員介面發布契約：學員頁只說明情境、工具、第一個動作、可觀察結果、檢查表時機與下一堂；作者試跑、內部驗證路徑、機器狀態碼與 `_validation` 連結不得出現在學員頁。
- 起始材料頁是讀取輸入的頁面；操作講義才是在工具完成工作的頁面；完成檢查表是保存證據並決定能否交接的頁面。三者的角色必須在頁首直接說明。
- 每一堂的學習路徑固定為：課程總覽 → 起始材料 → 操作講義 → 指定工具 → 完成檢查表 → 下一堂。任何跳接都要說明返回位置與失敗時的 checkpoint。
- 方案限制與尚未觀察的行為要用學員看得懂的句子記錄，例如「未執行，請寫下原因」；內部細節留在 `_validation/` 與修復報告。
- 素材頁與檢查表必須能交代保存方式：檔案、截圖、日期與檔名。只有勾選符號而沒有保存位置的檢查表不算完成物。
