# Vercel／Render 部署角色一致化設計

## 決策

- `Render Free Web Service` 是本課程含後端部署的主方案。
- `Vercel Hobby` 是個人、非商業作品展示的補充方案。
- `GitHub Pages` 是純靜態頁面且不含私密 API key 時的最簡方案。
- Railway 不再作為免費主路徑；只有在比較或歷史脈絡確有教學價值時才保留，且不得描述為可長期免費使用。

## 教學邊界

### Render 主路徑

適用於 Node.js／Express 後端、需要保護 API key、公司內部工具、接案原型與可能延伸為商業用途的作品。操作型頁面必須使用 Render 的實際介面名稱、`onrender.com` 網址、環境變數設定、Build／Start Command、Deploy Logs 與冷啟動排錯方式。

免費方案限制必須在第一次操作前說明：服務閒置 15 分鐘會休眠，下一次開啟可能等候約一分鐘；超出免費用量且未綁付款方式時服務會暫停，而非自動扣款；免費服務不適合正式 production SLA。

### Vercel 補充路徑

適用於個人作品集、課堂練習與非商業 Demo。核心平台選擇頁須明示 Hobby 限個人、非商業使用；公司內部工具、受薪工作產物、接案交付、商品或服務宣傳、收款與主要靠廣告或聯盟連結獲利的網站，不應使用 Hobby 作為正式部署方案。

Vercel 可以保留在靜態部署與 serverless function 的延伸內容中，但每一條會讓學員實際選擇 Vercel 的操作路徑，至少要有一次就近的用途邊界。純技術敘述若不構成平台推薦，可用簡寫 `Vercel Hobby（個人非商業）`，不重複長篇條款。

### GitHub Pages 靜態路徑

只用於 HTML／CSS／JavaScript 靜態輸出，且程式碼與前端請求中不存在必須保密的 API key。若需要隱藏金鑰，必須改走 Render 後端代理；不能把 key 混淆後留在前端。

## 內容層級

### 核心判斷頁

以下頁面放完整平台判斷與用途邊界：

- `part4/CH4-3.html`
- `part5/CH5-4.html`
- `part5/PRAC5-2.html`
- `part5/PRAC5-4.html`

其中 `CH5-4` 與 `PRAC5-4` 的最短可跑路徑全面改成 Render，不只替換平台名稱；同步更新準備項目、Dashboard 路徑、環境變數、公開網址、成功徵兆、log 排錯、checkpoint 與預期輸出。

### 精簡同步頁

下列既有引用依所在句子的功能校正：

- `fun-apps.html`
- `index.html`
- `my-progress.html`
- `part4/PRAC4-4.html`
- `part5/CH5-3.html`
- `part5/PRAC5-1.html`
- `part5/PRAC5-3.html`
- `part5/PRAC5-15.html`
- `part5/PRAC5-16.html`
- `part6/CH6-2.html`
- `part7/CH7-2.html`
- `part7/CH7-4.html`
- `part7/PRAC7-1.html`
- `part7/PRAC7-4.html`
- `part7/PRAC7-5.html`

規則如下：

1. 個人作品展示保留 Vercel，首次決策點標示 Hobby 非商業邊界。
2. 公司、客戶、受薪工作或可能商用的案例改用 Render 主路徑。
3. 含 Express 長駐後端的步驟不再把 Vercel 當成與 Render 完全等價的一鍵替代品。
4. PRAC5-17 的未來 proxy 範本定位改為個人非商業可分享 Demo；不得暗示可交付公司或客戶使用。
5. 純路徑相容性、技術棧列舉等不構成部署建議的文字，可保留平台名，但不得與相鄰用途邊界矛盾。

### 大綱

更新 `_outlines/gen-ai-140h.md`：

- frontmatter 工具加入 Render，保留 Vercel。
- PRAC5-4 主平台從 Railway 改為 Render。
- PRAC5-2／PRAC5-17 明示 Vercel Hobby 的個人非商業作品定位。
- 大綱與 HTML 的平台角色必須一致。

## 不在本次範圍

- 不重設頁面版型、色彩或互動元件。
- 不新增第三個後端託管平台。
- 不建立或發布 PRAC5-17 尚未存在的 proxy repository。
- 不把 Render Free 描述為正式 production 或永久不變的免費承諾。
- 不改寫與部署平台角色無關的案例、prompt 或課程活動。

## 修復安全

正式修改前必須備份所有納入 scope 的既有 HTML 與大綱，並建立可執行的 restore script。既有 mixed worktree 變更不納入本次 staging 或 commit；所有 Git 操作只指定本次檔案。

## 驗收標準

1. `rg -n -i 'Vercel|Railway|Render'` 檢查全課，每個部署建議都符合三平台角色。
2. `CH5-4` 與 `PRAC5-4` 的 Render 主線具備準備、操作、預期結果、checkpoint 與對應排錯，沒有殘留 Railway UI、網址或 log 指示。
3. Vercel 操作頁在學員做平台決策之前，看得到 Hobby 個人非商業邊界。
4. 公司／客戶／接案案例不把 Vercel Hobby 當正式部署建議。
5. 每個修改的 HTML 通過 `docs/lint-page.py`，再執行整課 lint。
6. 重建 search index 與 sitemap，確認課程導覽與連結未受影響。
7. 重跑 Shared Copy Audit：完整條款集中在核心頁，其餘只用精簡標註，不讓重複警語擠壓操作內容。
