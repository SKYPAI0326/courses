# 第十輪：真人角色試跑 A1～A3 修正清單

代理扮演零基礎學員在 Figma 實際操作 A1～A3 主線（已排除試跑工具本身的限制）。PM 裁定如下，承作照改；實機事實見 `platform-inapp.md` 最後一節。

## 課前準備頁 `assets/COURSE-START.html`（PM 自己改）與 A1
1. Section：按 ⇧S 後拖出**約 3000×2000** 的區域（之後放手機與桌面畫面都夠用）；`Screen / Login` 放在 Section 內 **x 0、y 0**（A2 的參考區座標以此為準）。A1 開頭提到 Section 處同步。
2. A1 示範 2～5：寫明變數表是全螢幕；每按一次 Create variable 都要再選 Color；Value 欄可直接打 Hex；打開時先確認左欄選的是自己的集合。改完按左側 **File** 回畫布確認（主色用法第 5 步同步）。
3. A1 文字樣式：寫明存檔後名稱會顯示成「Type/Page title」（空格被去掉，屬正常）；清單或 Libraries 若出現 Figma 內建套件的樣式或 Error 變數，選本檔的那一個。
4. A1 示範 16–17：`Label` 放在按鈕內左右置中、上下置中（Auto layout 前先手動置中即可）。
5. A1 對比檢查器：寫明連結在本堂起始材料頁，也可直接點講義連結；粗體大字門檻寫「字級約 19（18.7）以上且粗體」，與檢查器一致。
6. A1 跟著做 1：順序改成「先把副本文字尺寸模式改 **Auto height**，再把 W 設 322」；寫一句「沒點進 W 欄就打數字會改到不透明度，按 0 恢復」。
7. A1 主色四種用法 1–3：複製出的按鈕放在手機畫面外、`Rules` 旁；淺底提示區用 F 建 Frame（Fill `Primary Soft`）再放文字。

## A2
8. 示範 8 參考區座標：以 `Screen / Login` 在 Section 的 x 0、y 0 為準（課前已規定），並加一句「若你的手機不在左上角，改放在手機框下方 40 的位置」。
9. 示範 9：桌面框放進去前先把 Section 拉寬（例如 3000 以上）。
10. 示範 10–12：參考卡片用 **F**（Frame）；`Desktop / Aside` 高度與標題位置給數值（與 `Desktop / Main` 一致的 H，標題 y 16）。
11. 跟著做 1：副本先改 Auto height 並設寬度（例如 322）再觀察換行。
12. Constraints 1：改成「在 Position 下方的 Constraints 下拉選單設定（若沒看到，點 X／Y 右側的小圖示展開）」。
13. Layout guide 的 Type 欄：寫明維持預設 Stretch。

## A3
14. 示範 3（按鈕）：順序改成「Shift+A → 先把 W 改回 322 並確認 X 為 16 → 再設置中與 Padding 16／12、H 48」；刪掉具體推算值的描述，改成「Figma 會依原位置推算內距，數字和規格不同是正常的，照規格改回」。
15. 示範 4（卡片）：刪掉「W 會先顯示 338」，改成「寬度與內距會依原位置推算，接著照規格改」。
16. 示範 6：寫成「確認 `Message`、`Hint` 是 Fill container 與 Auto height（若不是就改）」。
17. 跟著做 Fixed 比較：「在 W 欄直接輸入一個數字（例如 200），就會變成固定寬度」。
18. Number 變數 4：完成描述改成「Padding 數字會出現外框，代表已綁定變數」；寫明 Padding 水平、垂直兩欄各綁一次。
19. Number 變數 5（Gap）：「點 Gap 欄的 ▾ → **Apply variable…** → 選 `Space 12`」。
20. Number 變數 6：按鈕內 Gap（Shift+A 預設 10）改成 8 並綁 `Space 8`（按鈕只有一個子層，Gap 不影響外觀，但保持數列一致）。
21. Number 變數 1：打開 Variables 時先在左欄點自己的集合。
22. Min／Max 5、所有「寫下紀錄」的步驟：寫明「用 T 在**空白處**點一下新建文字；點到既有文字會插進那段文字裡」。
23. Wrap 1：標籤包好後，在 Fill 按 ＋ 套 `Primary Soft`（淺底），Padding 改 `Space 4`／`Space 8`。
24. Wrap 結尾：把 `Tags` 寬度恢復成能排成一列的寬度。
