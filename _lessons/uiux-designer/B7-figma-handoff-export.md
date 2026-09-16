---
slug: uiux-designer
unit_id: B7-figma-handoff-export
title: 把 Figma 原型整理成可交付的 Handoff 包
course_type: skill-operation
duration: 6h
learning_objective: 從已回歸的 Prototype 產出可重開的 PNG／PDF／Inspect 證據與 Handoff 清單，並正確標示 Photoshop 尚未驗證的範圍。
prerequisites: [B3, B6]
style_guide: ../../_outlines/_style_guide_template.md
platform_version: Figma Starter／Free、Google Chrome（2026-09-16 機器證據）
---

## 教學流程（Teaching Flow）

### 破題 / Hook

雯姊收到 Figma 連結時，還需要回答三個問題：哪個畫面是交付版本？輸出檔是否能在沒有 Figma 時被查看？開發者要從哪裡讀尺寸、顏色與資產？本單元把 B6 的測試紀錄與 B4 的 Figma 檔整理成 Handoff 包，避免「有連結」被誤認成「可交付」。

### 概念 / Concepts

- **來源檔**：Figma 檔是可重開的真實來源，不能只交截圖。
- **輸出檔**：PNG 適合快速視覺比對，PDF 適合單頁查看；兩者都要保留尺寸與命名。
- **Inspect**：Dev Mode 的 Layout、Colors、Assets 與 CSS 只是交接線索，不能代替設計意圖說明。
- **發布邊界**：本節驗證本地匯出與 Inspect；Share 權限、GitHub push、公開部署與 Photoshop 開檔另列待辦。

### 操作示範 / Demo

#### Stage B7-1：先凍結可交付來源

1. 開啟 B6 回歸通過的 Figma 檔，確認目前頁面與 Frame 名稱。
2. 在交付表記錄 Figma URL、日期、方案、起點、測試 case_id 與最後通過結果。
3. 不在交付前偷偷改文字、尺寸或 Prototype；若要改，先新增版本欄位並重新回歸。

#### Stage B7-2：輸出與 Inspect

| 動作 | 預期證據 | 失敗時 |
|---|---|---|
| 對 `Screen / Host` 加 Export | PNG／PDF 下載項目存在 | 先檢查選取的是 Frame，不是畫布空白處 |
| 對 `Dialog / Overlay` 加 PNG Export | 320×200 Overlay 圖含預期文字 | 回到 Layers 確認文字是子層 |
| 切換 Dev Mode | 可見 Inspect、Layout、Colors、Assets | 只記錄可見控件，不宣稱程式碼已完成 |
| 更新 Handoff 清單 | 來源、輸出、限制、驗收證據集中 | 缺欄就標 `BLOCK` |

### 動手 / Hands-on

#### 起始狀態

- B6 測試紀錄已標示回歸結果。
- B4 Figma 檔保留在自己的 Drafts。
- `uiux-designer/assets/B7-figma-handoff-export/START-HERE.html` 與 Handoff 清單可讀取。

#### 同步演練與交付表

| 步驟 | 模式 | 學員操作 | 預期結果 |
|---:|---|---|---|
| 1 | Together | 填入 URL、方案、日期、case_id | 來源可追溯 |
| 2 | Demo | Export Host PNG 與 PDF | 下載檔名含 Screen / Host |
| 3 | Together | Export Overlay PNG | 320×200 圖可比對文字 |
| 4 | Checkpoint | 驗證檔案存在、尺寸與來源 | 不存在就停，不進 Inspect |
| 5 | Solo | 切 Dev Mode，記錄 Layout／Colors／Assets | 有一筆可重現的 Inspect 筆記 |
| 6 | Check | 將 Handoff 清單交給下一位讀者 | 對方能知道哪些已驗證、哪些未驗證 |

### 檢核 / Verification

- [ ] Figma 來源檔與日期／方案已記錄。
- [ ] Host PNG、Host PDF、Overlay PNG 均能重開或查看。
- [ ] PNG 尺寸與 Frame 尺寸一致；Overlay 圖含預期文字。
- [ ] Dev Mode Inspect 的可見欄位被記錄，沒有把 CSS 當成完成網站。
- [ ] Handoff 清單明確列出 Share、GitHub、部署與 Photoshop 的狀態。

### 商業情境案例（Case）

阿凱要把成果交給外部接案夥伴。夥伴不一定有 Figma 帳號，因此需要來源檔、PNG、PDF、Inspect 筆記與限制說明。好的 Handoff 讓對方知道哪些能直接使用，哪些必須回到 Figma 或等待 Photoshop／部署驗證。

### 動手練習題（Hands-on Exercise）

用 B6 的最後通過版本建立 Handoff 包。故意漏掉 Overlay PNG，再按照 Checkpoint 找回漏件；最後在清單中把 Photoshop 狀態填成 `NOT_RUN`，不可用 Figma PNG 冒充 Photoshop 輸出。

### 常見錯誤 3 條（Common Pitfalls）

1. **只交 PNG**：看得到畫面卻無法追溯來源。解法：附 Figma URL 與版本欄位。
2. **把 Dev Mode CSS 當網站**：Inspect 是交接資訊，不是已部署的 HTML。解法：分開記錄 Inspect 與 B8 網站產物。
3. **把 Photoshop 寫成已完成**：目前沒有機器證據。解法：標 `NOT_RUN`，列出下一個測試動作。

### 檢核題 2 條（Quiz）

**Q1**：PNG 與 Figma 來源檔各自解決什麼問題？
**答案要點**：PNG 解決快速視覺查看；Figma 保留可重開、可檢查的來源與互動。

**Q2**：為什麼 Handoff 清單要寫未驗證的平台？
**答案要點**：讓接收者知道證據邊界，避免把未測能力當成可交付承諾。

### 講師授課筆記（不進講義）

使用已取得的 Probe C 檔案證據示範。若學員的方案或 UI 不同，保留欄位與判斷邏輯，不把檔名或版面差異誤判成學員錯誤。Photoshop 需另安排實機測試後才可更新課程狀態。
