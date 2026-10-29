---
unit_id: PRAC1
title: 六秒標題動畫整合檢核
lesson_type: integration-capstone
duration: 30m
platform_version: "Adobe After Effects 2025"
---

<!-- learner-content:start -->

# 六秒標題動畫整合檢核

你會在新的 Composition 中整合前五課，完成一段六秒標題動畫。這次仍保留你的設計選擇，但依照五個階段逐步完成；每一階段通過 checkpoint 後才進到下一階段。

## 整合練習英文名詞複習

| 英文介面名稱 | 中文理解 | 本次用途 |
|---|---|---|
| Composition | 合成 | 本次六秒作品的工作畫布 |
| Transform | 變形屬性 | 控制 Position、Scale、Rotation 與 Opacity |
| Keyframe | 關鍵影格 | 記錄屬性在指定時間的數值 |
| Mask / Track Matte | 遮罩／軌道遮罩 | 建立文字或圖形的揭露範圍 |
| Effect | 效果 | 改變指定圖層的外觀 |
| Render Queue | 渲染佇列 | 檢查設定並輸出六秒檔案 |

## 任務契約

| 欄位 | 內容 |
|---|---|
| 輸入 | `ACP-AE-Lab-v05.aep`、本頁任務簡報、系統字型與 AE 內建 Shape/Solid |
| 完成物 | `PRAC1_Title_6s` Composition、`ACP-AE-Lab-PRAC1.aep`、六秒預覽檔與證據清單 |
| 第一個動作 | 另存 `ACP-AE-Lab-PRAC1.aep`，再建立 `PRAC1_Title_6s` |
| 成功訊號 | 新 Composition 是 1080 × 1080、29.97 fps、6 秒，Timeline 初始為空白 |
| 交接 | Part 2 用此工程解釋概念；Part 3 用其複製版完成代表題 |

## 任務簡報

製作「FOCUS / FRAME / FINISH」三詞標題動畫：

- 0–2 秒：主標題移入並減速停下。
- 2–4 秒：主標題或強調形狀完成第二組 Transform 變化。
- 4–6 秒：標題以 Mask 或 Track Matte 揭露，最後一秒淡出。
- 至少使用一項 Effect，並能說明它作用於哪個圖層。
- 必須有 Text 或 Shape，至少兩種 Transform Keyframe，且進場段使用 Easy Ease。
- 只使用系統字型與 AE 內建素材，確保工程無 Missing Footage。

## Step by Step：完成六秒整合作品

### Step 1（S0）：另存工程並建立 Composition

- **操作**：將 `ACP-AE-Lab-v05.aep` 另存為 `ACP-AE-Lab-PRAC1.aep`。新增 `PRAC1_Title_6s`，設定 1080 × 1080、29.97 fps、6 秒。
- **應看到**：新 Composition 的 Timeline 是空白，舊 Composition 仍保留在 Project 面板。
- **Checkpoint**：重新開啟 Composition Settings，五項規格正確後才繼續。
- **卡住時**：規格錯誤就直接在 Settings 修正；工程未另存就先停止。

### Step 2（S1）：先完成靜態畫面

- **操作**：依任務簡報建立 Text、Shape 與需要的背景層。命名每個圖層，排好上下順序；先不要加 Keyframe。
- **應看到**：任一時間點都能清楚讀到 `FOCUS / FRAME / FINISH`，沒有 Missing Footage。
- **Checkpoint**：Timeline 不應出現 `Shape Layer 1`、`Text 1` 等未命名圖層。
- **卡住時**：回到圖層命名、順序與眼睛開關；靜態畫面未完成前不要進入動畫。

### Step 3（S2）：建立 0–4 秒的 Transform 動畫

- **操作**：先寫下 0、2、4、6 秒的時間表。0–2 秒建立主標 Position 移入並套 Easy Ease；2–4 秒再建立主標或強調形狀的第二組 Transform 變化。
- **應看到**：0–2 秒完成移入，2–4 秒有第二段清楚變化，至少使用兩種 Transform 屬性。
- **Checkpoint**：逐點停在 0、2、4 秒，確認數值與畫面，再播放 0–4 秒。
- **卡住時**：刪除多餘 Keyframe，只保留時間表需要的時點；Stopwatch 不要重複關閉。

### Step 4（S3）：加入揭露、Effect 與淡出

- **操作**：4–6 秒使用 Mask 或 Track Matte 完成揭露；加入至少一項 Effect，並在最後一秒用 Opacity 淡出。
- **應看到**：揭露方法有明確控制位置；Effect Controls 可看到效果；6 秒時標題不可見。
- **Checkpoint**：關閉 Mask／Matte 或 Effect 時，能說明畫面哪一部分恢復；打開後結果符合任務簡報。
- **卡住時**：Matte 造成全透明時先設回 None，分別檢查 fill 與 matte，再重新指定來源。

### Step 5（S4）：預覽、輸出並整理證據

- **操作**：把 Work Area 設為 0–6 秒，從頭播放。確認圖層眼睛後加入 Render Queue，依序核對 Render Settings、Output Module、Output To，輸出六秒預覽檔。
- **應看到**：預覽與輸出都是六秒，檔案可開啟；工程、Timeline、Effect Controls 與 Render Queue 證據齊全。
- **Checkpoint**：依下方完成檢查表逐列打勾，缺任何一列就回到對應階段。
- **卡住時**：輸出黑幕或太短時先停止重複 Render，回到 Preview、Work Area 與 Time Span 檢查。

## 完成檢查

| 類別 | 通過標準 | 證據 |
|---|---|---|
| 畫面 | 文字可讀，指定元素在指定時間出現，無意外遮擋 | 0、2、4、6 秒畫面擷圖 |
| 工程 | 圖層名稱清楚，沒有失效效果、離線素材或多餘空層 | Timeline 全圖 |
| 動畫 | 有兩種以上 Transform、Easy Ease、Mask/Matte，無多餘 Keyframe | Timeline 屬性展開圖 |
| 效果 | 至少一項 Effect，作用層級可說明 | Effect Controls 擷圖 |
| 輸出 | 長度 6 秒，輸出尺寸與格式符合規格 | Render Queue 圖與可開啟檔案 |

## Step by Step：變式練習

1. 複製 Composition，改名 `PRAC1_Variant_5s`。
2. 把 Composition 改為 1080 × 1920、5 秒；不要修改六秒原版。
3. 重新安排文字與 Shape 的位置，讓直式畫面仍可讀。
4. 重新計算「進場—變化—離場」的時間，不只縮小 Scale。
5. 將 Work Area 改為 0–5 秒並輸出不同檔名。
6. **通過標準**：五秒直式版保留三段邏輯，版面不是橫式版本硬縮小，原六秒工程仍可重開。
7. **卡住時**：先停在靜態直式畫面正確的狀態，再重排 Keyframe；不要同時改版面與時間。

## 修復

| 現象 | 階段 | 回修位置 | 重跑起點 | 安全停止狀態 |
|---|---|---|---|---|
| 一開始就無法重開 | S0 工程 | Save As 與資料夾權限 | 另存後立即關閉／重開 | 空白 Composition 可開 |
| 畫面對但動畫亂 | S2 動畫 | 時間表與 Timeline | 只保留規格時點 Keyframe | 靜態畫面正確 |
| Matte 後整層消失 | S3 揭露 | Matte 來源、Alpha/Luma、圖層順序 | 設回 None，確認來源可見再重做 | 沒有 Matte 但畫面完整 |
| 輸出黑幕或太短 | S4 輸出 | Work Area、眼睛開關、Time Span | 先在 Preview 完整播放再重加佇列 | Preview 0–6 秒正確 |

<!-- learner-content:end -->
