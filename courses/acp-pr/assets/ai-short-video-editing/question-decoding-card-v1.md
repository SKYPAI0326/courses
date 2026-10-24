# 題幹拆解卡 v1

每題操作前先填六格。家族可重疊；分類理由要能連到作用物件、功能入口與驗證方式。

| 作用物件 | 動作 | 功能位置 | 目標狀態 | 限制 | 驗證 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 固定練習題

### Q1

將指定 timeline clip 的 Scale 設為 200%，維持 Position 與 Anchor Point 原值。

### Q2

在指定時間把 Source Monitor 已設定 In／Out 的片段加入 V1。原有片段的任何畫格都不能被覆蓋。

### Q3

刪除 sequence 的指定 In／Out 範圍，後方內容向前補位，不留下 gap，也不延長任何 clip。

### Q4

將 sequence item 改名，刪除所有空白 video／audio tracks，並把 A1 整條音訊軌靜音。

## 答案與判分依據

### Q1

- 作用物件：指定 timeline clip。
- 動作：修改 Scale。
- 位置：選取片段後的 Properties／Effect Controls。
- 目標：Scale 200%。
- 限制：Position、Anchor Point 不變。
- 驗證：面板數值與原值對照；只看 Program Monitor 不足以證明限制成立。

### Q2

- 作用物件：source clip、目標 sequence 與 V1。
- 動作：Insert。
- 位置：Source Monitor、Source Patching、Timeline。
- 目標：指定時間與軌道出現新片段。
- 限制：沿用既有 In／Out；原畫格不得被覆蓋。
- 驗證：序列總長增加，原有內容完整並向後移。

### Q3

- 作用物件：sequence In／Out 範圍。
- 動作：Extract。
- 位置：Timeline／Program Monitor／Sequence 選單。
- 目標：指定範圍消失，後方內容補位。
- 限制：無 gap；clip duration 不增加。
- 驗證：接點、序列總長與 clip duration。

### Q4

- 作用物件：Project panel 的 sequence item、Timeline 的 empty tracks、A1 track。
- 動作：改名、Delete Tracks、Mute Track。
- 位置：Project panel、Sequence 選單、A1 track header。
- 目標：名稱正確，只保留有用軌道，A1 的 M 啟用。
- 限制：不刪有內容的軌道，不以停用單一 audio clip 代替 track mute。
- 驗證：Project panel 名稱、軌道數量與 A1 的 M 狀態。
