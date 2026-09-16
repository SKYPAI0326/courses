# 合成資料包

## 來源與限制

所有 CSV 都是為課堂計算與判讀製作的合成資料，`source_status=synthetic`。沒有來自真實客戶、網站、帳號或廣告平台的個資與 credential；不得拿來宣稱實際 SEO、GA4 或投放成果。

## 檔案與欄位

### gsc-search-console-synthetic.csv

- `date`：日期。
- `query`：搜尋查詢；`page`：示例頁路徑。
- `country`／`device`：市場與裝置切片。
- `impressions`／`clicks`：曝光與點擊。
- `ctr`：clicks / impressions；`position`：平均排名。
- `source_status`／`source_note`：合成來源與課堂用途。

用途：先分辨查詢意圖，再做頁面與內容優先序；不能推論真實市場需求。

### ga4-content-synthetic.csv

- `date`、`page`、`device`：資料範圍。
- `users`／`sessions`：使用者與工作階段。
- `event_name`：示例事件；`event_count`：事件次數。
- `cta_clicks`／`form_submits`：內容行動與詢問訊號。
- `engagement_rate`：示例互動率；`source_status`／`source_note`：限制與用途。

用途：建立內容假設、檢查事件與轉換定義；不能代替 Google Demo Account 的真實介面驗證。

### ads-budget-two-rounds-synthetic.csv

- `scenario`：保守／基準／擴大。
- `round`：planned、round_1、round_2。
- `channel`／`market`：渠道與市場。
- `budget`／`impressions`／`clicks`／`inquiries`：預算與結果。
- `cpc`／`cpl`：每點擊／每詢問成本。
- `tested_variable`：兩輪主要變因；`guardrail_status`：護欄結果。
- `source_status`／`source_note`：合成來源與可用邊界。

用途：CH5-6 建立情境，CH5-7 固定主要變因並做兩輪判斷；不能執行或回填真實花費。

