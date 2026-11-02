# 第十輪：試跑 B7 修正清單

PM 裁定如下，承作照改；實機事實見 `platform-inapp.md` 最後一節。

1. Save local copy 移到 Note 標註與作品集頁**之後**（或在完成條件前加「最後再存一次」），讓 .fig 含標註與作品集。
2. 匯出：寫明「圖層名含『/』時，按 Export 會下載一個 zip，圖檔在 zip 裡的子資料夾；先解壓，再依交付清單改檔名」。
3. 1x＋2x：新增的第二列會出現在**上方**；改名規則：2x 檔名加 `@2x`（例如 `dialog-confirm@2x.png`）。
4. 四張主要畫面的檔名寫清楚：`screen-login.png`（用正常狀態的 `Screen / Login`）、`screen-list.png`、`screen-detail.png`、`screen-list-done.png`；規格表同步。
5. 量規格：寫明「在 Layers 選 `Row / T01`（或在畫布雙擊進到單一列）；單擊會選到外層 `List / Content`」；字型與字重「點文字樣式名稱 → Edit style 查看，不要改名稱欄」；Alt／Option 量距離維持原寫法。
6. 「確認完成」按鈕：寫明在 `Overlay / Confirm` 裡；互動表格的範例改成「詳情的『標記完成』開啟確認彈窗，彈窗的『確認完成』前往完成清單」。
7. 長標題列：量高度改用加長標題的測試（例如暫時把 T02 加上「（含客戶名與地點）」）再量，測完改回；或刪掉「長標題列較高」的比較。
8. 規格表寫在哪：在交付資料夾建 `spec/visual-rules.md`（照 `handoff-example.json` 的結構）。
9. Import：「檔案首頁右上 **More** → Import → Import from computer，選 .fig（對話框沒列出 .fig 也可以選）」。
10. Photoshop：素材的 Background 圖層預設已隱藏；改成「確認 Background 的眼睛是關閉的，四角會顯示透明棋盤格；點開眼睛會看到白底，再關掉」。
11. `Note` 元件規格：編號圓點 24×24、Fill `Primary`，裡面用 T 放白色數字（套 `Type / Label`、置中）；說明文字套 `Type / Supporting`；Gap `Space 8`；圓點與說明包成水平 Auto layout 後 Create component，編號與說明各建 Text property（`Number`、`Text`）。
12. Note 放置：第 1～4 條放在清單畫面旁，第 5～8 條（返回鈕、附件圖、焦點順序等）放在詳情畫面旁。
13. 作品集 Frame：「在所有 Section 外的空白處按 F 建立（點在 Section 範圍內會被包進去）」；W 1440、H 先設 2600。流程圖縮圖與畫面縮圖：複製後用 K（縮放工具）縮到合適寬度再放進作品集 Frame。
14. 作品集的測試資料：寫明「從做任務測試那一堂的測試紀錄取一個發現；若沒有，用觀察紀錄頁的參考問題『確認後只寫已更新』與它的修正」。
