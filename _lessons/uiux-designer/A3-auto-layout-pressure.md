---
slug: uiux-designer
unit_id: A3-auto-layout-pressure
title: 用 Auto Layout 撐住長文字與內容變化
course_type: skill-operation
duration: 6h
learning_objective: 在 Figma Starter／Chrome 中建立可隨內容增長的手機介面，驗證長中文、固定寬度與 Auto height，並能指出尚未測的多列清單邊界。
prerequisites: [A2]
style_guide: ../../_outlines/_style_guide_template.md
platform_version: Figma Starter／Free、Google Chrome（2026-09-16 Probe A 機器證據）
---

## 教學流程（Teaching Flow）

### 破題 / Hook

阿凱做了一張登入錯誤畫面，短句看起來整齊；換成「密碼至少需要包含一個英文大寫字母與一個數字」後，文字被裁掉。問題不是把字縮小，而是版面沒有對內容變化負責。本單元用 Auto Layout、固定寬度與 Auto height 建立可重開的壓力測試。

### 概念 / Concepts

- **固定寬度**控制文字行寬；**Auto height** 讓容器隨換行增高。
- **內容壓力測試**先改文字，再觀察容器、按鈕與相鄰元件是否被推開。
- **主元件與 Instance**要分開判斷；本節先驗證文字與容器，不把 Form／List 行為混進來。

### 操作示範 / Demo

1. 建立手機 Frame，選取文字層，將寬度設為 200。
2. 用右側 Content 欄位輸入一段長中文，避免直接在畫布上誤選外層。
3. 將高度設為 Auto／Hug，重新觀察文字換行與容器高度。
4. 把錯誤輔助文字放在輸入區塊下方，確認它是同一元件樹的子層。
5. 記錄原始短句、壓力文字、容器尺寸與修復結果。

### 動手 / Hands-on

| 步驟 | 模式 | 操作 | 期待結果 |
|---:|---|---|---|
| 1 | Together | 建立手機 Frame 與登入區塊 | 有可選取的文字／容器 |
| 2 | Demo | 固定文字寬度 200 | 長句會換行而非無限橫向延伸 |
| 3 | Checkpoint | 輸入長中文錯誤訊息 | 高度增加，文字完整可讀 |
| 4 | Solo | 只替換另一句長文字 | 容器與相鄰元件仍可重排 |
| 5 | Check | 記錄尺寸與截圖 | 有可重開的壓力測試證據 |

### 檢核 / Verification

- [ ] 短句與長句都能在 200 寬度內完整顯示。
- [ ] Auto height 會隨換行增加，不裁切文字。
- [ ] 錯誤輔助文字仍位於輸入區塊子層。
- [ ] 我沒有用縮小字級掩蓋內容壓力。
- [ ] 我知道多列 List 增刪與 Form 行為仍是後續測試。

### 商業情境案例（Case）

雯姊要審一個手機登入流程，文字可能由產品、客服或翻譯人員改寫。Auto Layout 的價值不是讓畫面「自動變漂亮」，而是讓內容變化有可預期的反應與修復紀錄。

### 動手練習題（Hands-on Exercise）

把錯誤文字換成「密碼至少需要包含一個英文大寫字母與一個數字」，只改文字；再換成兩行更長的版本，觀察容器是否仍完整。若裁切，先回到寬度／高度設定，不要刪除文字。

### 常見錯誤 3 條（Common Pitfalls）

1. **直接在畫布輸入造成文字串接**：先用 Layers 選文字層，再走右側 Content。
2. **只加大 Frame**：這會掩蓋內層寬度問題；先檢查文字固定寬度與 Auto height。
3. **把 List 多列當成已驗證**：本節只證明文字壓力；多列增刪另列 `NOT_RUN`。

### 檢核題 2 條（Quiz）

**Q1**：長中文換行後高度不變，先檢查什麼？
**答案要點**：文字容器的高度模式與是否啟用 Auto height／Hug。

**Q2**：為什麼不直接把整張手機 Frame 放大？
**答案要點**：Frame 放大會掩蓋元件內部的寬度與內容關係，無法驗證真實手機版面。

### 講師授課筆記（不進講義）

Probe A 的長中文、Auto height 與右側 Content 修復是本節機器證據；Component、Variant 已在同一 Probe 出現，但不要把它們重教成 A3 的新成果。Form／List 多列仍需獨立夾具。
