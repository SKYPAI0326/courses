# Codex 冷啟動跟做紀錄：B4 Overlay

## 執行契約

- 起點：只知道課程頁 URL，不依賴講師口頭補充。
- 平台：Google Chrome、Figma Starter／Free。
- 目標：在自己的 Draft 建立 `Screen / Host` 402×874、`Dialog / Overlay` 320×200，完成一條 Open overlay 並在 Preview 看到 `確認完成`。
- 禁止：Upgrade、付款、Share 權限修改、公開部署。

## 跟做檢查

| # | 冷啟動問題 | 結果 |
|---:|---|---|
| 1 | 能否從素材包找到 Figma URL 與備援材料？ | PASS；START-HERE 與 URL 檔案提供兩條路徑 |
| 2 | 是否知道要建立哪些物件與尺寸？ | PASS；兩個 Frame、名稱、尺寸在教案與 HTML 同時出現 |
| 3 | 是否知道文字要放在哪一層？ | PASS；反覆指定 Overlay 子層，並列出畫布外錯誤修復 |
| 4 | 是否知道 action 的完整欄位？ | PASS；Trigger、Action、Destination、Position、Animation、Flow 起點均列出 |
| 5 | 是否有中間停點而非一路猜？ | PASS；Checkpoint B4-1 在第 4 步後阻擋錯誤延伸 |
| 6 | 是否能自行驗收 Preview？ | PASS；Chrome 點擊與 `確認完成` 是明確可觀察結果 |
| 7 | 卡住時能否安全恢復？ | PASS；None、方案限制、空白 Preview 各有最小修復或停止路徑 |
| 8 | 是否會誤把靜態畫布當成互動完成？ | PASS；三層證據表要求結構、Prototype、Preview 同時存在 |

## 結論

機器可依講義完成跟做路徑，並與 Probe B 的真實 Chrome/Figma 證據對接。狀態為 `MACHINE_PASS_PENDING_HUMAN`：尚缺真人在不同帳號與網路狀態下的重跑，以及後續 Photoshop／部署鏈路。
