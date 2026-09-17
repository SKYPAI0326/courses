# 產物鏈審查：B4 → B5 → B6 → B7 → B8

| 前一單元產物 | 下一單元輸入 | 下一單元新產物 | 機器判定 |
|---|---|---|---|
| B4 Overlay／Swap Figma 檔、Preview 證據 | B5 長內容與固定元素測試 | `SCROLL-01`、Overflow、固定／漂浮檢查紀錄 | `MACHINE_PASS_PENDING_HUMAN` |
| B5 `SCROLL-01`、固定／漂浮邊界 | B6 任務腳本起始狀態 | Actual／Expected、問題分類、單一變因修正、回歸紀錄 | `MACHINE_PASS_PENDING_HUMAN` |
| B6 回歸通過的 case_id 與版本 | B7 Handoff 起始材料 | Host PNG／PDF、Overlay PNG、Inspect 筆記、限制清單 | `MACHINE_PASS_PENDING_HUMAN` |
| B7 Handoff 包 | B8 最小網站／Git/GitHub 路徑 | `web-starter/` 的 HTML/CSS/JS、local Chrome 結果、Git 操作說明 | `MACHINE_PASS_PENDING_HUMAN` |

## 檢查結果

- B5 頁面明確引用 B4 的可預覽原型，先處理長內容與固定／漂浮層；B6 再接手 B4／B5 的任務條件，不重新發明畫面。
- B7 頁面明確要求 B6 的 `case_id` 與回歸結果，不接受沒有版本的截圖。
- B7 將 Photoshop、Share、GitHub push、公開部署列為未驗證邊界。
- B4、B5、B6、B7、B8 五頁均可在 Chrome localhost 開啟；頁面 lint 均為 0 BLOCKER／0 ERROR／0 WARN。
- 尚未真人從 B4 連續完成到 B8；B8 已完成本機網站與 Git 路徑機器測試，但 GitHub push／公開部署仍未執行。

## Gate 判定

這條鏈已具備機器階段的可追溯結構，可進入真人試跑；不能宣稱整門 99h 課程完成，也不能把 Photoshop、GitHub push 或公開部署標成通過。
