---
slug: uiux-designer
unit_id: B6-prototype-task-test
title: 用固定任務測試修正 Prototype
course_type: skill-operation
duration: 6h
learning_objective: 使用 B4 的 Overlay 原型執行固定任務測試，分類問題、只改一個主要變因並留下可回歸的修正紀錄。
prerequisites: [B2, B3, B4, B5]
style_guide: ../../_outlines/_style_guide_template.md
platform_version: Figma Starter／Free、Google Chrome（2026-09-16 機器證據）
---

## 教學流程（Teaching Flow）

### 破題 / Hook

阿凱把 B4 的 `Screen / Host` 與 `Dialog / Overlay` 交給雯姊試用。雯姊說：「我看得到畫面，但不知道點擊後是不是應該出現這個訊息。」問題出在任務、操作與預期結果沒有被固定下來。本單元把「我覺得可以」整理成一張可重跑的測試表。

本節接手 B4 的產物：一條 `On click → Open overlay → Dialog / Overlay`。不新增第二個 action，不把未測的完整登入流程當成已完成。完成物是測試紀錄、問題分類、最小修正與一次回歸結果。

### 概念 / Concepts

- **任務腳本**：用角色、起始狀態、單一任務、操作與預期結果描述測試，不用「試看看」作為步驟。
- **可觀察結果**：學員或測試者能看到、點到或記錄的結果，例如 Preview 顯示 `確認完成`。
- **問題分類**：把問題分成內容、結構、互動、可讀性與方案限制，避免所有問題都被叫作「Figma 壞掉」。
- **單一變因修正**：一次只改文字、目的地或起點其中一項，才能知道回歸結果來自哪個修正。

### 操作示範 / Demo

#### Stage B6-1：先建立測試基準

1. 開啟 B4 Figma 檔，確認 Host、Overlay、文字與 interaction 都存在。
2. 在測試表填入：測試者「雯姊」、起始狀態「Preview 從 Host 開始」、任務「完成一個任務並確認回饋」、操作「點擊 Host 一次」、預期「出現確認完成 Overlay」。
3. 實際按一次，記錄「通過」或「未通過」，不要先修正。

#### Stage B6-2：示範分類與修正

| 現象 | 分類 | 最小修正 | 不要做的事 |
|---|---|---|---|
| 點擊後沒有目的地 | 互動 | 指定 `Dialog / Overlay` | 重建所有 Frame |
| 顯示文字不是預期內容 | 內容 | 只修改文字層 | 同時改尺寸與動畫 |
| 預覽從錯誤畫面開始 | 結構 | 把 Host 設為 Flow 起點 | 把空白畫布當成通過 |
| 第二個 action 跳升級 | 方案限制 | 拆成另一份測試檔 | 按 Upgrade 或輸入付款 |

### 動手 / Hands-on

#### 起始狀態

- B4 Figma 檔或自己的等價重建檔。
- Chrome Preview 可開啟。
- `uiux-designer/assets/B6-prototype-task-test/START-HERE.html` 與測試表。

#### 固定任務測試

| 步驟 | 模式 | 學員操作 | 觀察結果 | Checkpoint／修復 |
|---:|---|---|---|---|
| 1 | Together | 填寫角色、起始狀態、任務、操作、預期 | 測試者不需要講師口頭補充 | 缺一欄就停下補齊 |
| 2 | Demo | 從 Host 開 Preview，點擊一次 | 實際看到或看不到 Overlay | 只記錄，不立即修 |
| 3 | Checkpoint | 對照 `Dialog / Overlay` 與預期 PNG | 內容、層級、目的地可判讀 | 找不到證據就標 `BLOCK` |
| 4 | Solo | 只改一個主要變因 | 修正前後差異可描述 | 不同時改字、尺寸、action |
| 5 | Check | 重跑同一任務 | 回歸結果可重現 | 通過才進 B7 |

#### 測試紀錄欄位

`case_id`、`date`、`platform`、`starting_state`、`task`、`action`、`expected`、`actual`、`severity`、`root_cause`、`repair`、`rerun_result`、`evidence_path`。

### 檢核 / Verification

- [ ] 任務可以由另一個人照表執行，不依賴「大概點這裡」。
- [ ] Actual 與 Expected 分開記錄，沒有把預期答案填成結果。
- [ ] 每次修正只有一個主要變因。
- [ ] 回歸測試重跑同一條 action，沒有順手新增第二條。
- [ ] 方案限制被記為條件，不被偽裝成互動失敗。

### 商業情境案例（Case）

阿凱要交付一份能讓雯姊審稿的測試紀錄。紀錄要回答四件事：從哪裡開始、做什麼、應看到什麼、如果沒看到要怎麼分類與回修。本單元的交付物是這份可回溯紀錄；口頭說明不具備同樣的回溯性。

### 動手練習題（Hands-on Exercise）

先把 B4 的預期文字改成「已儲存，回到任務清單」，只改內容；再用同一腳本回歸。最後另開一筆測試，故意把 Destination 留空，記錄為互動問題並修復。不要同時改 Animation。

### 常見錯誤 3 條（Common Pitfalls）

1. **只寫「成功」**：沒有起始狀態與預期，無法重跑。解法：補齊固定欄位。
2. **一次修很多地方**：無法知道哪個修正有效。解法：撤回到上一個可重開檔，只改一個變因。
3. **把方案限制當 Bug**：Starter 第二 action 的提示是平台邊界。解法：另建測試檔並在紀錄標記 `CONDITIONAL`。

### 檢核題 2 條（Quiz）

**Q1**：為什麼要先記錄 Actual，再進行修正？
**答案要點**：保留原始失敗證據，才能判斷修正是否真的改善同一個任務。

**Q2**：修正文字後是否能順手調整 Overlay 尺寸與動畫？
**答案要點**：本次回歸只改一個主要變因；其他調整另開測試案例。

### 講師授課筆記（不進講義）

把 B4 的 Chrome Preview 畫面當作共同基準。若學生無法編輯原檔，使用自己的等價重建；不可因權限問題直接把測試改成看投影片。所有 `BLOCK` 先進 Run Log，再決定回修教案、素材或平台契約。
