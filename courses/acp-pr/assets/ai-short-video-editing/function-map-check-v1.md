# 功能地圖固定檢核 v1

作答規則：功能家族可以重疊。回答一個或多個家族都可以，但必須同時說明作用物件、最可能入口與完成證據。

## 五個陌生任務

1. 將選定的 timeline clip 解除影音連結，保留兩個 component 的原時間位置。
2. 建立原 sequence 的直式 9:16 Auto Reframed Sequence，原 sequence 必須保留。
3. 刪除 sequence 的指定 In／Out 範圍，後方內容補位，不留下 gap。
4. 將 A1 整條音訊軌靜音，但其他軌道仍能播放與編輯。
5. 從 Project panel 移除所有未使用項目，磁碟來源檔必須保留。

## 可接受答案

### 1. Unlink

- 家族：時間軸剪輯與片段關係；音訊、連結與軌道狀態。
- 作用物件：timeline clip 的 video／audio components。
- 入口：Timeline、`Clip > Unlink`。
- 驗證：video 與 audio 可分別選取，兩者起訖與位置未改變。

### 2. Auto Reframe 9:16

- 家族：序列、時間碼與軌道；影像規格、效果與輸出。
- 作用物件：原 sequence 與新建的 Auto Reframed Sequence。
- 入口：Project panel 選取 sequence、`Sequence > Auto Reframe Sequence`。
- 驗證：Project panel 出現新的 9:16 sequence，原 sequence 仍存在。

### 3. Extract

- 家族：時間軸剪輯與片段關係。
- 作用物件：sequence In／Out 範圍與後方 timeline clips。
- 入口：Timeline／Program Monitor／Sequence 選單的 Extract。
- 驗證：指定範圍消失、後方內容補位、沒有 gap、clip duration 未增加。

### 4. Track Mute

- 家族：序列、時間碼與軌道；音訊、連結與軌道狀態。
- 作用物件：A1 audio track。
- 入口：Timeline 的 A1 track header，按 M。
- 驗證：A1 的 M 啟用；沒有刪除或停用單一 audio clip。

### 5. Remove Unused

- 家族：專案與素材管理。
- 作用物件：未被 sequence 使用的 Project items。
- 入口：Project panel 選單的 Remove Unused；若教室版沒有該命令，依 Usage 欄位手動選取。
- 驗證：未使用項目離開 Project panel，使用中素材與 sequence 可播放，Windows 中的來源檔仍存在。
