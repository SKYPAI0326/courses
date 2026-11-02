# 第九輪模擬走查修正清單（第二次）

第二次模擬：A1～A3、A6 共 12 項；A4、A5、A7、A8、B2、B5 共 11 項（第一次 38 → 第二次 23）。PM 裁定如下，承作照改。實機事實見 `platform-inapp.md` 最後兩節（含多選 Shift+A 為垂直且 Padding 0、旋轉 90 為逆時針）。

## A1
1. 跟著做 4「暫時把主要按鈕改成次要灰色」改成「Fill 暫時改套 `Muted`」。

## A3
2. 跟著做 4、6：複製卡片後加「把副本拖到手機畫面外的空白處」，正式卡片留在畫面裡。
3. 間距變數第 6 步：檢查對象改為「登入卡片與練習按鈕」（`Hint` 是文字層，沒有 Gap、Padding）。
4. Wrap 第 1～2 步：先把五個標籤**左右排成一列**再多選按 Shift+A；補一句「若 Flow 顯示垂直，點水平那一格」。

## A6
5. 示範第 5 步：多選包框實測 Padding 為 0，不必另設；但把 `Field / Label` 也設為 Fill container（與 Input、Helper 一起）。
6. `Field / Multiline`：改成「在三個 Variant 各選 `Field / Input`，H 設 96，Auto layout 對齊改為靠上」。
7. Checkbox、Radio、Toggle 的 true 版本：每個元件各補一步「選 true 版本，依共用規格表改外觀」——Checkbox 底色 `Primary` 並放入 `Icon / Check`（Stroke `Card`）；Radio 加 10×10 `Primary` 內點；Toggle 底色改 `Primary`、圓鈕移到右側。
8. Checkbox 補 Text property `Label`（預設「記住我」），綁定後再 Add variant。
9. Select：Detach 後、Create component 前，把標籤改「類別」、內容改「設計」；向下箭頭用 `Icon / Chevron Right` **旋轉 -90 度**。
10. `Screen / New Task` 規格：402 × 874，Fill 套 `Surface`。
11. 「記住我」與「我已確認期限」勾選框：移到**複製出其他狀態畫面之前**加入（或明寫各張副本也要加入），讓同組畫面一致。

## A4
12. 跟著做第 5 步「只重設一個個別屬性」改成「把那一項手動改回來源值（例如 Fill 重新套 `Primary`）」；卡住時表格同步。
13. `Components` 一節加一步「把上一堂的 `Tags` 主元件移入 `Components`」。
14. 測試區使用處改名 `Test / Complete`、`Test / Cancel`，本堂結尾刪除測試區（避免和之後畫面裡的 `Button / Complete`、`Button / Cancel` 同名）。

## A5
15. 「把主線元件複製給自己的題目」整節移到「讓圖示能顯示、隱藏」**之後**（題目副本才帶有 `Show icon`、`Icon` 屬性）。

## B2
16. 熱區：改成「在表單的 Auto layout 容器裡建立熱區，開啟 Ignore auto layout，再拖到開關列上方」；「Fill 設為 0%」改成「不加填色」。
17. 預約示範第 5 步前補「在時段格下方按 T 加入摘要『12:00～15:00，共 3 小時』」。

## B5
18. 第 3 步改成「確認十二筆已超出外框下緣」；第 4 步「在其中兩列填入較長的任務名稱」刪掉（或改在副本上測試）。最後一筆維持「寄出月底請款單」。
19. `Button / Floating` 描述「藍底」改「深綠底」。
20. 向上箭頭：`Icon / Chevron Right` **旋轉 90 度**（實測 90 為逆時針）。
21. `Anchor / Top` 與 `Button / Floating`：寫明「先在畫布空白處建立，再到 Layers 拖到 `Screen / List` 底下，成為直接子層」。
22. `Spacer / Bottom` 改 H 140（最後一列才不會被漂浮按鈕蓋住），規格表同步。
