# 環境與權限說明

## 總狀態

- **文字／CSV 判斷路徑：READY**：可用本資產包模板與合成資料完成規格、欄位閱讀、決策與驗收條件。
- **LocalWP 示範網站：BLOCK**：需要教師提供已安裝且可開啟的示範站點；本資產包不含站點檔與二進位。
- **GTM 測試容器：BLOCK**：需要教師帳號、容器與 Preview／Debug 權限；本資產包不含容器匯出或 credential。
- **GA4 Demo Account：BLOCK**：需要 Google Demo Account 登入與可見資料；CSV 只能支援欄位閱讀，不能宣稱完成介面驗證。
- **Google／Meta／LINE 權限：BLOCK**：需要教師示範帳號或正式授權；不執行真實付費投放、不收集真實名單。

## LocalWP

課前由教師確認：站點可啟動、首頁與服務頁可開啟、頁面標題／標題層級／連結可讀、可在瀏覽器檢視基本索引提示。學員從 `templates/CH4-3.md` 開始記錄頁面、現象、證據、修正與復測結果。

無法啟動時：改用 lesson 內嵌頁面示例或自建純文字頁面規格；狀態寫 `BLOCK—未完成瀏覽器／LocalWP 實測`，不可勾 READY。

## GTM

課前由教師確認：容器可開啟、Preview 可連接示範站點、學員能看到 tag／trigger／variable 的測試結果。用 `templates/CH4-6.md` 記事件名稱、參數、觸發條件、驗收與證據；用 `templates/CH4-7.md` 記誤觸發、遺漏、重複與轉換判讀。

無權限時：以 `datasets/ga4-content-synthetic.csv` 與事件規格做紙上驗證，並把「GTM Preview／實際事件傳送」列為待正式環境確認。

## GA4 Demo Account

課前由教師確認：能登入 Demo Account、可選指定 property、能讀報表與探索、看得到日期／裝置／頁面維度。學員以 `templates/CH4-4.md`、`templates/CH4-5.md` 記錄假設、範圍、欄位、觀察與限制。

無權限時：使用合成 GA4 CSV；保留資料字典與假設，但把介面截圖、property ID、即時資料與正式轉換設定標為 BLOCK。

## Google／Meta／LINE

課堂只做企劃、素材對照、預算計算與停止條件。教師若提供示範畫面，需去除帳號識別資訊、花費明細中的敏感資料與任何可登入資訊。學員不得建立付款方式、上傳真實名單或啟動投放。

無帳號／無權限時：使用 `templates/CH5-3.md`～`CH5-7.md` 加上合成預算資料，完成廣告結構、素材／頁面對應、護欄與兩輪決策；平台畫面與真實投放結果維持 BLOCK。

## 版本與課前確認

本檔不鎖定會漂移的外部 UI 版本。教師在上課前填 `permission-checklist.md` 的確認日期、平台／工具版本、帳號角色與可見範圍；介面不同時搜尋功能名稱：Page title、Heading hierarchy、GTM Preview、GA4 Events、Conversions、Campaign budget、Audience、LINE consent。

