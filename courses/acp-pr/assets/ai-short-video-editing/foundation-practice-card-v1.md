# Premiere 基礎練習卡 v1

適用素材：`premiere-foundation-starter/`

## 起始狀態

1. 建立 `ACP-PR-你的座號-v1.prproj`。
2. 匯入 `clip-01-lighthouse.mp4`、`clip-02-city.mp4`、`clip-03-workshop.mp4`、`audio-01-voice.wav` 與三張 PNG。
3. 以 `clip-01-lighthouse.mp4` 建立序列，命名 `foundation-main-v1`。
4. 將 clip 02 與 clip 03 依序接在 V1。三段原始長度為 12、10、14 秒，未修改時序列總長為 36 秒。
5. 複製序列並命名 `foundation-practice-v1`；所有練習只在副本執行。

## 練習一：Razor 與 Ripple

- 在 `00:00:04:00` 與 `00:00:07:00` 切開第一段 linked clip。
- 先用一般 Delete 觀察 3 秒 gap，再 Undo。
- 對相同區段執行 Ripple Delete。

通過條件：第一段中間 3 秒消失、後方內容前移、序列總長由 36 秒變為 33 秒，其他片段播放速度維持 100%。

## 練習二：Unlink、單獨選取與重新連結

- 對 `clip-02-city.mp4` 執行 `Clip > Unlink`。
- 點空白處後，分別單選 video 與 audio component。
- Undo 回復連結；再按住 Alt 單選 audio component，移到 A2，左右時間位置不變。
- 同時選取對應 video 與 audio，執行 `Clip > Link`。

通過條件：audio 位於 A2，起訖仍與 video 對齊；選取 video 時會同時選到 audio。

## 練習三：Overwrite 與 Insert

- 在 Source Monitor 開啟 `clip-03-workshop.mp4`，設定 In `00:00:02:00`、Out `00:00:05:00`。
- 將播放頭放在 `00:00:10:00`。
- 先使用 Overwrite，記錄被取代的時間範圍，再 Undo。
- 改用 Insert，記錄後方內容如何移動。

通過條件：Out point 包含最後一格；此範圍在 25 fps 下為 `00:00:03:01`。Overwrite 不推動後方全部內容；Insert 讓後方內容整體向右 `00:00:03:01`。兩次操作使用相同 In／Out。

## 練習四：軌道狀態與 Extract

- 將 `audio-01-voice.wav` 放到 A2，起點對齊序列起點。
- 在 A1 軌道標頭按 M；確認 A2 仍可聽見。
- 設 sequence In `00:00:14:00`、Out `00:00:16:00`。
- 先比較 Lift 的 gap，再 Undo 並以 Extract 作為最後結果。

通過條件：Out point 包含最後一格；指定 `00:00:02:01` 範圍消失、後方內容前移 `00:00:02:01`、Timeline 沒有 gap；A1 Mute、A2 可聽。

## 輸出

- Format：H.264
- Range：Entire Source／目前完整序列
- File Name：`practice-cut-v1.mp4`

在 Windows 播放器開啟，確認有畫面、有聲音，而且內容來自 `foundation-practice-v1`。
