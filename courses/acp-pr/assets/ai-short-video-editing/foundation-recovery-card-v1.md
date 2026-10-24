# Premiere 基礎復原卡 v1

## 改錯但尚未儲存

1. 先停止連續操作。
2. 按 `Ctrl+Z` 一次，觀察哪個狀態回復。
3. 若無法確認，關閉目前序列分頁，不刪除 Project item。
4. 回到 `foundation-main-v1` 複製新的練習副本。

## 改到錯的序列

- 現象：原始序列名稱、長度或內容變動。
- 回復：立即另存專案，保留證據；再從未修改的 starter 或最近副本重建。
- 安全狀態：Project panel 同時保留原序列與新的 practice sequence。

## Media Offline

- 現象：Program Monitor 顯示離線畫面，Project item 出現媒體連結問題。
- 檢查：Windows 中的來源檔是否被移動、改名或拔除磁碟。
- 回復：使用 Link Media／Locate 指向正確檔案。不要選擇刪除磁碟來源。

## 面板不見或工作區跑掉

1. 到 `Window` 選單依名稱重新開啟面板。
2. 必要時選 `Window > Workspaces > Editing`。
3. 使用重設目前工作區的選項後，再確認 Project、Source Monitor、Program Monitor、Timeline 與 Properties／Effect Controls。

## 影音失去同步

- 先 Undo。
- 核對 video 與 audio 的起訖時間。
- 需要重新連結時，同時選取正確的兩個 components，再使用 `Clip > Link`。
- Link 與 Group 的結果不同；不要用 Group 取代影音連結。

## 可以安全停止的狀態

- 原始序列存在且可播放。
- 練習發生在副本。
- 原始媒體仍留在固定資料夾。
- `.prproj` 已另存新版本。
