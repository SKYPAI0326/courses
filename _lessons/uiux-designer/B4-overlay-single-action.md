---
slug: uiux-designer
unit_id: B4-overlay-single-action
title: 用一個核心互動完成 Overlay 預覽
course_type: skill-operation
duration: 2h
learning_objective: 在 Figma Starter／Chrome 中建立可預覽的單一 On click → Open overlay 互動，並能用檔案、Preview 與完成品圖片自行驗收。
prerequisites: [A2, A3, A8, B1]
style_guide: ../../_outlines/_style_guide_template.md
platform_version: Figma Starter／Free、Google Chrome（2026-09-16 實測）
---

## 教學流程（Teaching Flow）

### 破題 / Hook

阿凱在弄一下行銷工作室收到一個很小、但很容易被誤解的需求：手機任務清單按下「完成」後，要讓使用者立刻看到「確認完成」。如果只交一張靜態圖，雯姊無法確認這個訊息是不是在正確的時機出現；如果一開始就把登入、清單、Dialog、Toast 全塞進同一個免費 Figma 檔，Starter 可能在第二個 action 時顯示方案限制。

本單元只改變一件事：把一個主畫面接到一個 Overlay。完成物是一個能在 Chrome Preview 點擊後看到 `確認完成` 的最小 Figma 檔；單看 Prototype 面板無法提供這項證據。這個限制讓我們先驗證互動因果，再決定是否需要拆成更多測試檔。

開始前請開啟素材包中的 `source/FIGMA-FILE-URL.txt`。它指向機器已驗證的測試檔；如果你的帳號沒有編輯權，依照下面的 Frame 名稱與尺寸在自己的 Drafts 新建空白檔，能力差異只在於少了預先建立的圖層。

### 概念 / Concepts

- **Prototype action** — 由「觸發條件」和「動作目的」組成的連線；本例只有一條，避免把免費方案限制藏起來。
- **Overlay** — 疊在目前畫面上的另一個 Frame；它適合 Dialog、Menu 或短暫確認訊息，不會把整個任務帶到另一頁。
- **Flow starting point** — Preview 的起點；沒有它，學員可能從錯誤畫面開始，無法判斷自己的互動是否真的成功。
- **Starter 一檔一核心 action** — 這是本次實測採用的課程契約；Figma 其他方案可能有不同能力。同一檔案再建立第二個 action 會跳出 Professional 升級提示，因此多步驟流程改用拆檔策略。

### 操作示範 / Demo

#### Stage B4-1：先固定起始狀態與完成物

示範使用的兩個 Frame 如下：

| Frame | 尺寸 | 角色 | 內容 |
|---|---:|---|---|
| `Screen / Host` | 402×874 | Prototype 起點 | 可以是空白白底，重點是承接點擊 |
| `Dialog / Overlay` | 320×200 | 疊加畫面 | 一個文字層：`確認完成` |

把 `reference/screen-host-blank.png` 當尺寸參考，把 `expected/dialog-overlay.png` 當完成後比對圖。這兩個 PNG 用來核對尺寸與文字；請在 Figma 重新建立可編輯物件，完成物是你自己的 Figma 檔與 Preview。

#### Stage B4-2：示範一條最短路徑

1. 在 Figma 建立一個 402×874 的 Frame，於 Layers 改名為 `Screen / Host`。
2. 在同一頁建立另一個 Frame，改名為 `Dialog / Overlay`，尺寸設為 320×200。
3. 選取 `Dialog / Overlay` 內部，使用 Text 工具輸入 `確認完成`。文字應位於 Overlay 的子層；若出現在畫布外，預覽無法證明 Overlay 正常。
4. 選取 `Screen / Host`，切到右側 `Prototype` 分頁，按 `Add action`。這個 action 是一條「點擊後要做什麼」的規則，現在只建立一條。
5. 在 Interaction 對話框把 Trigger 保持為 `On click`，Action 選 `Open overlay`，Destination 選 `Dialog / Overlay`。
6. 保持 Position 為 `Centered`、Animation 為 `Instant`，按 `Create action`。右側 Interactions 應看到 `Click → Dialog / Overlay`。
7. 按 `Add flow starting point`，確認起點是 `Screen / Host`，再按 `Present` 開啟 Chrome 預覽。
8. 在預覽白色主畫面內點擊一次。畫面應出現 `確認完成`；這是第一個可觀察成果。

**中間判斷**：如果 Interactions 顯示的是 `Click → None`，代表 action 已建立但目的地尚未設定；回到第 5 步，不要繼續猜。若預覽仍然空白，先回 Figma Layers 確認 `確認完成` 是 `Dialog / Overlay` 的子層。

### 動手 / Hands-on

#### 起始狀態

- Chrome 已登入 Figma Starter／Free，停在可編輯的 Figma 設計檔。
- 你能取得 `uiux-designer/assets/B4-overlay-single-action/START-HERE.md` 與其中列出的三份檔案。
- 你知道本節只驗收一條 action；不需要升級方案、不需要分享檔案。

#### 同步演練：一條 Overlay 互動

| 步驟 | 模式 | 學員操作 | 預期結果 | 快速檢查 | 卡住時 |
|---:|---|---|---|---|---|
| 1 | Together | 開啟 Figma，建立 402×874 Frame 並命名 `Screen / Host` | Layers 出現 Host | 右側 Width=`402`、Height=`874` | 切到 Design，選取真正的 Frame row 再改尺寸 |
| 2 | Together | 建立 320×200 Frame，命名 `Dialog / Overlay` | 兩個同層 Frame 可見 | Layers 顯示 Overlay 與 Host 同層 | 若縮排錯誤，重新在空白畫布建立 Frame，或複製後移到同層 |
| 3 | Demo | 在 Overlay 內輸入 `確認完成` | 文字出現在 Overlay 白底內 | 點選文字時 Layers 顯示它是 Overlay 子層 | 若文字出現在畫布外，刪除該文字，先選 Overlay row 再用 Text 工具點擊其內部 |
| 4 | Together | 選 Host → Prototype → Add action，Trigger=`On click`、Action=`Open overlay`、Destination=`Dialog / Overlay` | Interactions 顯示 `Click → Dialog / Overlay` | 沒有 `None` | 點開該 interaction row，回到 Destination 欄位修正 |
| 5 | Checkpoint | 加入 Flow starting point，按 Present，點擊白色主畫面一次 | Preview 出現 `確認完成` | 文字與 `expected/dialog-overlay.png` 相同 | 回到 Stage B4-2 第 5 步；保留兩個 Frame，不要重建整個檔案 |
| 6 | Solo | 只把 Overlay 文字改成 `任務已完成`，其餘尺寸、觸發、目的地不變 | 同一個 Overlay 出現新文字 | 只改一個主要變因，action 仍只有一條 | 先確認文字層仍在 Overlay 子層，再重新 Present |
| 7 | Check | 打開 `reference/EXPECTED-CHECK.md`，逐項勾選 Frame 名稱、尺寸、action 與 Preview | 有一份可交付的自我檢查紀錄 | 檔案可重開、Preview 可重現 | 沒有任何一項就先停在本 Checkpoint，不往 B5 前進 |

#### Checkpoint B4-1

現在應該看到兩個同層 Frame、Overlay 內有文字、Prototype 面板有一條 `Click → Dialog / Overlay`。如果沒有看到，回到第 2 或第 4 步；通過後才能做變化練習。不要把「Present 按鈕能開」誤當成互動已驗證。

#### 變化練習：只改內容，不改互動

把 `確認完成` 改成「已儲存，回到任務清單」，保持 Host 尺寸、Overlay 尺寸、Trigger、Action、Destination、Centered 與 Instant 都不變。這次只檢查內容變長時的 Overlay；第二條 action 會改變測試條件，留到另一份測試檔處理。若字串換行或超出 320×200，回到 A3 的 Auto Layout／文字壓力單元處理，不要用縮小字級掩蓋問題。

### 檢核 / Verification

完成本單元代表：你能從一個空白 Figma 檔建立兩個可辨識 Frame，設定單一 Overlay action，在 Chrome Preview 點擊後看到指定文字，並能指出 Starter 為何不適合在同一檔案繼續堆第二個 action。這份 Figma 檔下一次由 B6 任務測試使用；B6 會把「點擊後是否真的看到 Overlay」寫成固定測試步驟。

#### 自我驗收

- [ ] `Screen / Host` 是 402×874，並被設定為 Flow starting point。
- [ ] `Dialog / Overlay` 是 320×200，文字 `確認完成` 位於它的子層。
- [ ] Interactions 只保留一條 `On click → Open overlay → Dialog / Overlay`。
- [ ] Chrome Preview 點擊 Host 後看得到 `確認完成`；若畫面空白，依錯誤修復表回到文字層與 Flow 起點檢查。
- [ ] 我能說明第二個 action 會觸發 Starter 方案限制，並知道拆檔是目前備援。

## 試跑包需求清單（Verification Asset Spec）

- **帳號與權限**：Figma Starter／Free、Chrome；只需能在自己的 Drafts 建立／編輯檔案。不要求 Share、付款或公開權限。
- **起始材料**：講義頁面優先連到可在 Chrome 直接閱讀的 `START-HERE.html` 與 `reference/EXPECTED-CHECK.html`；原始 `START-HERE.md`、`source/FIGMA-FILE-URL.txt`、`reference/EXPECTED-CHECK.md` 保留作版本化來源，另含兩份 PNG 對照品。
- **完成品對照**：`expected/dialog-overlay.png`（320×200）；若不能開啟 Figma URL，仍可依尺寸、名稱與文字重建，但要在紀錄中標記「無預先檔案」備援。
- **平台限制**：Starter 同檔第二 action 會跳出升級提示；本單元不點 Upgrade、不輸入付款資料。

## 商業情境案例（Case）

**角色**：阿凱（行銷專員）
**公司**：弄一下行銷工作室
**任務**：為工作室內部任務清單做一個「完成後立即確認」的手機 Overlay，讓雯姊在審稿時能看懂點擊與回饋的因果。
**本單元要他學會**：用一條可預覽的核心 action 交付可重現的 Overlay；靜態圖只能用來比對畫面，不能代替互動證據。

## 動手練習題（Hands-on Exercise）

**題目**：從空白檔建立 `Screen / Host` 與 `Dialog / Overlay`，將 `確認完成` 接成單一 `On click → Open overlay`，在 Chrome Preview 點擊驗收，再把文字換成「已儲存，回到任務清單」。

**預期成果**：一個可重開 Figma 檔、一條可見的 Prototype interaction、一張可對照的 Overlay 完成畫面與一份自我檢查紀錄。

**完成標準**（self-check）：

- [ ] 兩個 Frame 名稱與尺寸正確。
- [ ] Overlay 文字是子層，Preview 點擊後可見。
- [ ] 同一檔案沒有為了展示功能而建立第二個 action。

## 常見錯誤 3 條（Common Pitfalls）

1. **錯誤現象**：點開 interaction 後 Destination 仍是 `None`。
   **原因**：只建立了 action 外殼，還沒有選 Overlay Frame。
   **解法**：回到 Stage B4-2 第 5 步，選 `Open overlay` 與 `Dialog / Overlay`，再回到 Checkpoint。

2. **錯誤現象**：Starter 顯示「You cannot create multiple actions with your current plan」。
   **原因**：同一個免費原型檔已經有一條 action；本單元的契約是一檔一核心 action。
   **解法**：不要按 Upgrade；移除多餘的空白 interaction，或建立新的獨立測試檔。保留原檔，並在交付紀錄寫明拆檔。

3. **錯誤現象**：Preview 點擊後仍是空白。
   **原因**：`確認完成` 被建立在畫布外或 Host，沒有放入 Overlay 子層；也可能沒有設定 Flow starting point。
   **解法**：在 Layers 逐層展開 `Dialog / Overlay`，用右側 Content 檢查文字；設定起點後重新 Present。無法修復時，安全停止在 B4-1，不刪掉整個檔案。

## 檢核題 2 條（Quiz）

**Q1（概念驗證）**：為什麼本單元把 `Dialog / Overlay` 做成獨立 Frame？如果文字直接放在 `Screen / Host`，預覽會少掉哪一項證據？

- [ ] 因為 Overlay 的檔名一定要用英文。
- [ ] 因為獨立 Frame 才能作為 Open overlay 的目的地，Preview 才能驗證疊加關係。 ← 正確
- [ ] 因為 Host 不能放文字。
- [ ] 因為 Free 方案只允許白色背景。

**Q2（應用驗證）**：你需要登入 → 清單 → Dialog 三個畫面，但 Starter 在第二個 action 跳出限制。你會怎麼交付第一個可驗收版本？

**預期答案要點**：先保留一檔一核心 action，交付登入或清單到 Dialog 的最小 Preview；第二段另建獨立測試檔並在交付說明標記方案限制；不以空白畫面或「看起來有連線」假裝三段互動已完成。

## 講師授課筆記（不進講義）

- 建議節奏：20 分鐘情境與概念、35 分鐘 Demo/Together、35 分鐘 Solo、20 分鐘 Preview／修復、10 分鐘交付檢查。
- 若學生帳號無法編輯機器測試檔，直接採空白檔備援；不可把「無權限」轉成學員錯誤。
- 方案提示出現時停在畫面，讓學生把限制抄入紀錄；不要替學生點 Upgrade。
- 這個單元的真實 Figma 證據在 `uiux-designer/_validation/figma-starter-browser/PROBE-B.md`，匯出完成品在 `uiux-designer/_validation/figma-starter-browser/exports/`。
