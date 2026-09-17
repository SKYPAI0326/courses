---
slug: uiux-designer
unit_id: A4-component-instance
title: 建立主元件與第一個 Instance
course_type: skill-operation
duration: 5h
learning_objective: 在 Figma Starter／Chrome 中，從手機登入區塊建立一個可從 Assets 重用的主元件，插入一個 Instance，並說明兩者的編輯邊界。
prerequisites: [A3-auto-layout-pressure]
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: Figma Starter／Free、Google Chrome（2026-09-16 Probe A 機器證據）
---

## 教學流程（Teaching Flow）

### 破題 / Hook

阿凱把登入區塊放進兩個畫面：登入頁需要一份，活動報名頁也需要同樣的標題結構。直接複製圖層會留下兩份各自修改的內容，之後很難確認哪一份才是最新版。本單元把 A3 已經調整好的登入區塊建立成主元件，再從 Assets 插入一個 Instance。完成物是一個可被找到、可被插入，而且有清楚編輯邊界的元件。

### 概念 / Concepts

- **主元件（Main component）** — 保存元件結構的來源；A4 只建立單一狀態，狀態切換留給 A5。
- **Instance** — 從主元件插入的可重用物件；它的來源關係可在右側面板確認。
- **Assets** — Figma 顯示本檔可重用元件的位置；建立後要在這裡確認結果。
- **編輯邊界** — Instance 的主版面控制可能呈唯讀或 disabled；需要改結構時回到主元件。
- **可追溯命名** — `Login / Heading` 與 `Instance / Login heading` 讓 Layers、Assets、交接紀錄指向同一個成果。

### 操作示範 / Demo

示範從 `Mobile / Login & List` 的登入區塊開始。來源容器已經有垂直 Auto Layout 與文字 `登入`；建立主元件時要選容器，不要只選文字。示範終點包含 Layers 的主元件、Assets 的本檔 component，以及畫布上的一個 Instance。

| 步驟 | 操作 | 看到的結果 | 快速檢查 |
|---:|---|---|---|
| 1 | 開啟 A4 起始材料的 Figma 檔；若無編輯權，依起始頁重建 402×874 Frame | 能選取 `Mobile / Login & List` | 右側尺寸是 402×874 |
| 2 | 在 Layers 選取包含 `登入` 的 Auto Layout 容器 | 整個登入區塊被框選 | 文字是子層，容器是目前選取對象 |
| 3 | 執行 `Create component` | Figma 顯示 component 設定，來源容器變成主元件 | Assets 可準備搜尋本檔 component |
| 4 | 將主元件命名為 `Login / Heading` | Layers 顯示可讀的分組名稱 | 名稱使用 `/` 分出功能與部位 |
| 5 | 從 Assets 找到本檔 component，執行 `Insert instance` | 畫布上出現一個 Instance | 右側可看出它來自本檔 |
| 6 | 將 Instance 命名為 `Instance / Login heading` | Layers 同時有來源與使用處 | 名稱不改動主元件名稱 |
| 7 | 選取 Instance，觀察右側 Auto Layout 控制 | 主版面控制可能呈唯讀或 disabled | 這是來源關係的提示，不是錯誤 |
| 8 | 重新選取主元件，確認來源名稱與 A3 的文字仍在 | 主元件與 Instance 都留在檔案中 | 沒有建立 Variant 或 Property |

**示範完成物**：`Login / Heading` 主元件、`Instance / Login heading` Instance、A4 完成檢查表與 Figma 檔連結。這三項會交給 A5，作為加入 Variants 與 Property 的起點。

### 動手 / Hands-on

先照示範建立第一個主元件，再用同一套路徑完成一個 `Notice / Helper` 元件。Solo 只改一個主要變因：把來源文字從 `登入` 換成 `請確認帳號`；Frame 尺寸、Auto Layout 方向與驗收方式維持不變。

| 步驟 | 模式 | 你的操作 | 預期結果 | 快速檢查 | 卡住時的修復 |
|---:|---|---|---|---|---|
| 1 | Together | 開啟起始檔並找到 `Mobile / Login & List` | A3 的手機畫面仍在 | Frame 為 402×874 | 切到 Design，從 Layers 選 Frame |
| 2 | Together | 選取包含 `登入` 的 Auto Layout 容器 | 整個容器被框選 | 子層文字沒有單獨被選取 | 在 Layers 往上一層選取容器 |
| 3 | Together | 執行 `Create component` | Assets 出現本檔 component | 右側顯示 component 設定 | 若按鈕不存在，先確認選取的是容器 |
| 4 | Checkpoint | 命名 `Login / Heading` 並查看 Layers | 名稱可讀且沒有重複 | 來源名稱與 Instance 名稱尚未混用 | 只在 Layers 重新命名來源 |
| 5 | Together | 從 Assets 插入一個 Instance | 畫布出現可選取的 Instance | 右側顯示來源關係 | 開啟 Assets 的本檔分類再搜尋 |
| 6 | Together | 命名 `Instance / Login heading` | 使用處可被辨識 | `/` 前後的功能一致 | 先選 Instance 再改名，不要改來源 |
| 7 | Checkpoint | 選取 Instance，查看 Auto Layout 控制 | 主版面控制呈唯讀或 disabled | 知道要回主元件修改 | 重新選來源主元件比較兩者面板 |
| 8 | Solo | 複製 A3 的登入區塊，將文字改為 `請確認帳號`，重做主元件與 Instance | Assets 多一個可辨識的本檔 component | 只改文字，其餘設定不變 | 回到 A3 的容器設定，重新確認 Auto Layout |
| 9 | Check | 開啟完成檢查表並記錄檔案連結 | 有可交接的 A4 證據 | 來源、Instance、限制都有紀錄 | 先保存 Figma，再補寫紀錄 |

### 檢核 / Verification

- [ ] `Login / Heading` 在 Layers 中是主元件。
- [ ] Assets 能找到本檔建立的 component。
- [ ] 畫布上有 `Instance / Login heading`。
- [ ] 選取 Instance 時，我能指出它的來源與主版面控制邊界。
- [ ] 我沒有把 Variant、Property、Button、Form 或 List 的功能提前算入 A4 成果。
- [ ] 我已保存 Figma 檔連結與 A4 完成檢查表。

**交給下一單元**：A5 會使用 `Login / Heading` 主元件加入第二個狀態，並示範 Property 名稱與 Value 的正確關係。A5 不需要重新教 Frame、Auto Layout 或 Instance 插入。

## 試跑包需求清單（Verification Asset Spec）

- 起始材料：[A4 起始材料](../../uiux-designer/assets/A4-component-instance/START-HERE.html)。
- 完成檢查：[A4 完成檢查表](../../uiux-designer/assets/A4-component-instance/reference/EXPECTED-CHECK.html)。
- 實測來源：[Probe A](../../uiux-designer/_validation/figma-starter-browser/PROBE-A.md)，對應 A-05、A-07。
- 外部工作檔：[Codex Figma Starter Audit｜Probe A](https://www.figma.com/design/tSpQYGtYKwGLT9YtIFk9uC/Codex-Figma-Starter-Audit---Probe-A?node-id=1-15&t=dayHaBLEXHGo96a6-0)。
- 平台邊界：Figma Starter／Free、Chrome；如果工作檔無法編輯，使用路徑二重建，不按 Upgrade。
- 交付證據：Figma 檔連結、Layers 截圖、Assets 截圖、完成檢查表。

## 商業情境案例（Case）

**角色**：阿凱，弄一下行銷工作室行銷專員

**任務**：把登入區塊整理成可重用主元件，讓另一個手機畫面能插入同一個來源並留下可追溯的命名。

**本單元要他學會**：建立主元件、從 Assets 插入 Instance、辨認來源與使用處的編輯邊界。

## 動手練習題（Hands-on Exercise）

在同一個 Figma 檔中完成一份 `Notice / Helper` 主元件與一個 Instance。沿用 A3 的 402×874 Frame、垂直 Auto Layout 與 200 px 文字寬度，只替換文字為 `請確認帳號`。不要建立 Variant；狀態管理會在 A5 處理。

**預期成果**：`Login / Heading` 與 `Notice / Helper` 兩個可在 Assets 找到的本檔 component，以及至少一個可辨識來源的 Instance。

**完成標準**（self-check）：
- [ ] 每個主元件都有清楚的 `/` 命名。
- [ ] 每個練習 Instance 都能在右側指出來源。
- [ ] 來源容器保留 A3 的 Auto Layout 與文字寬度設定。
- [ ] 檔案連結、截圖與限制說明已保存。

## 常見錯誤 3 條（Common Pitfalls）

1. **只選到文字層**：Create component 後只包住 `登入`，外層 Auto Layout 沒有被重用。原因是 Layers 選取層級太深。回到 Layers 往上一層，確認整個登入區塊被框選，再重新建立主元件。

2. **建立後找不到 component**：畫面上看似完成，Assets 卻沒有結果。原因是還停在畫布選取狀態，沒有切到 Assets 的本檔分類。先開啟 Assets，再搜尋 `Login / Heading`；仍找不到時回到來源主元件檢查是否真的執行 Create component。

3. **把 Instance 的 disabled 當成故障**：選取 Instance 後，主 Auto Layout 控制呈唯讀或 disabled。這表示結構由來源主元件管理。回到 `Login / Heading` 修改來源；A4 不用 Detach，也不把 Instance 當成新的主元件。

## 檢核題 2 條（Quiz）

**Q1（概念驗證）**：哪一個物件保存可重用的來源結構？

**答案**：主元件 `Login / Heading`。Instance 是從來源插入的使用處。

**Q2（應用驗證）**：選取 Instance 後，Auto Layout 主版面控制呈 disabled，你會怎麼做？

**答案要點**：先確認右側顯示來源關係；需要改結構時回到主元件；保留 Instance 關係，不用 Detach 掩蓋問題。

## 講師授課筆記（不進講義）

- 建議先讓學員打開起始材料，再示範一次「選容器而非文字」；這是 A4 最常見的層級判斷。
- 5h 可依「示範 60 分鐘、同步操作 120 分鐘、Solo 90 分鐘、檢查與交接 30 分鐘」調度；時間只供授課安排，不進學員頁。
- 如果 Probe A 工作檔內容已包含 Variant，不要在 A4 展開 Property；請另開頁面或沿路徑二建立單一主元件。
- `MACHINE_READY_PENDING_HUMAN` 的證據只代表機器路徑可跑；完成真人冷讀、跨帳號重跑與頁面連結檢查後，才能把 A4 改成 READY。
