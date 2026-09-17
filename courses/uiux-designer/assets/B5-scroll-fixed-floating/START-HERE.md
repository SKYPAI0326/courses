# B5 起始材料：滾動、置頂導覽與漂浮按鈕

## 工作情境

阿凱的手機任務清單已超過一個視窗。這一單元先驗證長內容的 `Vertical` overflow，再分開檢查固定 Header 與 Floating Action 的可見性與遮擋。

## 起始條件

- Chrome 已登入 Figma Starter／Free。
- 從 B4 Host 複製一份檔案，或在 Drafts 建立自己的 402×874 Frame。
- 不需要 Share、付款或公開權限。

## 測試卡

```text
SCROLL-01｜任務清單閱讀
Frame：Screen / Task list · 402×874
內容：標題、十筆任務、底部說明
Overflow Before：____________
Overflow After：Vertical
Expected：上滑後看見第 10 筆，沒有水平位移
Actual：____________________
尚未測：固定 Header 與 Floating Action 的聯合行為
```

## 操作順序

1. 複製 B4 Host，改名 `SCROLL-01`。
2. 加入十筆任務，讓內容高度超過 874 px。
3. 選取 Frame，記錄 Overflow 原值，再選 `Vertical`。
4. 從起點開 Chrome Preview，上滑一次，寫 Expected／Actual。
5. 複製測試，加入 `Navigation / Header` 與 `Floating / Action`，分別觀察固定與遮擋。
6. Solo 只把十筆改成十二筆，重跑同一條上滑腳本。

## 證據邊界

Probe B B-06 已確認 Overflow menu 有 `No scrolling`、`Horizontal`、`Vertical`、`Both directions`。固定圖層與滾動同時成立的效果仍需人工回歸；未觀察項目填 `NOT_RUN` 或 `MACHINE_PASS_PARTIAL`。
