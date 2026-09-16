# B8 最小網站起始專案

這個小專案接手 B7 Handoff 的最低成果：一個可在瀏覽器開啟的任務清單、一個可觀察的完成狀態與最小 JavaScript 事件。

## 本機驗收

1. 從 `uiux-designer/web-starter/` 啟動本地靜態伺服器。
2. 用 Chrome 開啟 `index.html`。
3. 點擊「標記完成」。預期看到按鈕停用、狀態變成「已完成」、回饋文字出現。
4. 重整頁面，確認目前沒有宣稱資料庫或雲端保存。

## Git 路徑

```text
git status
git diff
git add uiux-designer/web-starter/index.html uiux-designer/web-starter/styles.css uiux-designer/web-starter/app.js
git commit -m "feat: add task completion interaction"
```

GitHub push、Pages 或其他部署平台不在本機自動步驟內；需經 release gate 後再執行。
