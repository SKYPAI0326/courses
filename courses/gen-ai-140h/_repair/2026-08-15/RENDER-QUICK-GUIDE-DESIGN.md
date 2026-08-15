# Render 快速部署指南設計規格

## 目標

建立一份獨立、通用的 HTML 快速指南，讓第一次部署含後端 AI App 的使用者，能沿單一路徑把 GitHub 專案部署到 Render，取得公開網址並完成基本驗收。成品不提特定課程、時數、機構或觀看對象，避免非特定課程使用者誤解適用範圍。

## 輸出

- 檔案：`courses/gen-ai-140h/render-deploy-quick-guide.html`
- 形式：單一 HTML，CSS 與必要互動皆內嵌。
- 發布：不加入課程導覽、搜尋索引或 sitemap；不 push 到 GitHub。
- 語言：繁體中文，採初學者可理解的寫法，技術介面名稱保留英文；不在頁面宣告「這份文件給誰看」。

## 使用情境

使用者已有可執行的 Node.js 專案，且專案需要後端保護 API key。專案可能來自 AI Studio 或其他開發方式；這份指南不教學前置建置、不比較多個平台，也不涵蓋正式商業服務架構，只處理 Render 的最短部署與排錯路徑。

## 資訊架構

頁面採由上而下的單一路徑操作卡：

1. **開始前先知道**：Render Free 閒置 15 分鐘會休眠，冷啟動可能約一分鐘；免費服務適合練習、原型與低流量作品，不保證正式 production SLA。
2. **準備清單**：GitHub 帳號、Render 帳號、AI API key、已能在本機執行的 Node.js 專案，以及必要的 `package.json`、啟動指令與 `.gitignore`。
3. **最短部署六步**：推送 GitHub、建立 Web Service、設定 Runtime／Build Command／Start Command、加入 Environment Variable、啟動 Deploy、取得 `.onrender.com` 網址。
4. **完成驗收**：正式網址可開、能收到 AI 回應、API key 不在前端或 GitHub、手機畫面可用。
5. **常見錯誤速查**：Start Command、`process.env.PORT`／`0.0.0.0`、環境變數名稱、dependencies 遺漏、冷啟動與 Logs 判讀。

## 頁面設計

- 使用網站既有暖白底、棕色主色與 editorial 卡片語彙，但不複製完整網站導覽。
- 首屏直接顯示用途、預估時間與完成標準。
- 六個步驟以編號卡呈現，每張卡只保留一個主要動作、介面路徑與成功徵兆。
- 指令與設定值使用可橫向捲動的 code block；可加入純 JavaScript 複製按鈕，但不引入外部依賴。
- 手機寬度下維持單欄、按鈕可點擊、程式碼不撐破版面。
- 不使用需要連網載入才能理解內容的圖片；Render 介面變動時，文字路徑仍可獨立使用。

## 邊界與安全

- 不宣稱 Render 永久免費。
- 不要求綁定信用卡；說明未設定付款方式且超出免費額度時可能暫停服務。
- 不示範把真實 API key 寫進 HTML、JavaScript、GitHub 或畫面截圖。
- 不把前端混淆描述為保護金鑰的方法。
- 不將 Vercel、Railway 或 Google 部署流程加入本頁。

## 驗收標準

1. 使用者可在不閱讀其他課程頁的情況下完成六步操作，且頁面內沒有特定課程、時數或學員身分用語。
2. 頁面第一次要求建立 Render 服務前，已顯示 Free 方案限制。
3. Build Command、Start Command、Environment、Logs 與 `.onrender.com` 均有明確操作或驗收說明。
4. 五類常見錯誤各自提供「看到什麼、去哪裡查、怎麼修」。
5. HTML 通過 `docs/lint-page.py`，無 BLOCKER 或 ERROR。
6. 所有外部連結使用 HTTPS 並可由靜態檢查確認格式正確。
7. 檔案不加入 index、search-index 或 sitemap，不執行 push。
