# GA4 自訂事件規格樣本 — 客製化禮品電商

> 5 個虛構但結構真實的事件規格。配合 m7-2 + m9-3 + 案例 ④ ⑤ 復跑用。
> 驗證重點：每個事件埋了 1-2 個 AI 容易漏掉的細節（currency 配對 / 命名規則 / 轉換標記決策），看你能不能在 prompt 完後抓出來。

---

## 事件清單

| # | 事件名 | 行為 | 是否標為轉換 |
|---|--------|------|-------------|
| 1 | `click_quote_btn` | 點擊「立即詢價」按鈕 | ✅ |
| 2 | `download_pdf_proposal` | 下載「企業送禮提案 PDF」 | ❌ |
| 3 | `customize_material_select` | 拖曳客製化頁面的材質滑桿 | ❌ |
| 4 | `video_progress_75` | 觀看「客製化流程」影片至 75% | ❌ |
| 5 | `form_submit_sample` | 提交「免費索取樣品」表單 | ✅ |

---

## 事件 1：`click_quote_btn`

### 觸發場景

產品頁的「立即詢價」按鈕，HTML 大概長這樣：

```html
<button class="quote-btn"
        data-product-id="PRD-001"
        data-product-name="胡桃木禮盒"
        data-product-category="木製禮盒">
  立即詢價
</button>
```

### 參數設計

| 參數名 | 來源 | 範例值 |
|--------|------|--------|
| `product_id` | `data-product-id` | `PRD-001` |
| `product_name` | `data-product-name` | `胡桃木禮盒` |
| `product_category` | `data-product-category` | `木製禮盒` |
| `page_location` | `window.location.href` | `https://wnyx.com/products/walnut-gift-box/` |

### 對應 gtag JavaScript

```javascript
// 監聽所有「立即詢價」按鈕點擊
document.querySelectorAll('.quote-btn').forEach(el => {
  el.addEventListener('click', () => {
    gtag('event', 'click_quote_btn', {
      'product_id': el.dataset.productId,
      'product_name': el.dataset.productName,
      'product_category': el.dataset.productCategory,
      'page_location': window.location.href
    });
  });
});
```

### 驗證重點

- 進 GA4 即時報表 → 點擊 3 個不同產品的「立即詢價」按鈕 → 應該看到 3 筆 `click_quote_btn` 事件、各帶不同 `product_id`
- **常見漏洞**：AI 偶爾只給 `addEventListener('click', () => {})`，但忘了用 `querySelectorAll().forEach()`，導致只抓得到第一個按鈕

---

## 事件 2：`download_pdf_proposal`

### 觸發場景

任何 `<a href="*.pdf">` 連結的點擊。**注意**：GA4 加強型評估的 `file_download` 已會自動追蹤，這個事件是「額外的客製版本」（加自訂參數 `source_page`、`user_type`）。

### 參數設計

| 參數名 | 來源 | 範例值 |
|--------|------|--------|
| `file_name` | URL 末段檔名 | `corporate-proposal-2026.pdf` |
| `source_page` | `document.referrer` 或 `window.location.pathname` | `/blog/corporate-gift-guide/` |
| `user_type` | 從 localStorage 或 cookie 判斷 | `new_visitor` / `returning` / `member` |

### GTM 方案（推薦，不用改網站程式碼）

```
觸發條件：點擊 - 僅連結
觸發設定：部分點擊
條件 1：Click URL  包含  .pdf
條件 2：Click URL  包含  proposal

標籤類型：GA4 事件
事件名稱：download_pdf_proposal
事件參數：
  file_name → {{Click URL}} （要再用 RegEx 變數抽檔名，下方說明）
  source_page → {{Page Path}}
  user_type → {{dl_user_type}} （從 DataLayer 取）
```

### RegEx 抽檔名變數

GTM 變數類型「RegEx Table」：
- 輸入：`{{Click URL}}`
- Pattern：`/([^/]+\.pdf)$`
- 設定取第 1 捕獲組

### 驗證重點

- **常見漏洞**：AI 偶爾建議直接用 `{{Click URL}}` 當 `file_name` → 但完整 URL 不是檔名（會帶 `https://...domain.com/...pdf`），要改用 RegEx Table 抽
- **是否該標轉換**：這個事件**不該**標為轉換——下載 PDF 是「中段意願訊號」不是「業務完成」。若你硬標，會稀釋轉換報表的訊號品質

---

## 事件 3：`customize_material_select`

### 觸發場景

客製化頁面的材質滑桿（HTML5 `<input type="range">`），使用者選擇不同材質時觸發。

```html
<input type="range" id="material-slider"
       min="0" max="3" step="1"
       data-options='["walnut","oak","cherry","bamboo"]'>
```

### 參數設計

| 參數名 | 來源 | 範例值 |
|--------|------|--------|
| `material_name` | 從 data-options + slider value 對應 | `walnut` / `oak` / `cherry` / `bamboo` |
| `product_id` | 從頁面隱藏欄位 `<input id="current-product-id">` | `PRD-001` |
| `interaction_count` | sessionStorage 累計這次 session 內變過幾次 | `1` / `2` / `3`... |

### 對應 JavaScript

```javascript
const slider = document.getElementById('material-slider');
const options = JSON.parse(slider.dataset.options);
let count = parseInt(sessionStorage.getItem('material_count') || '0', 10);

slider.addEventListener('change', () => {
  count += 1;
  sessionStorage.setItem('material_count', String(count));

  gtag('event', 'customize_material_select', {
    'material_name': options[slider.value],
    'product_id': document.getElementById('current-product-id').value,
    'interaction_count': count
  });
});
```

### 驗證重點

- 用 `change` 事件而非 `input` 事件——`input` 在拖曳過程連續觸發（一秒可能 30 次），會把 GA4 配額燒光
- **常見漏洞**：AI 預設用 `input` 事件，要追問「改成 change，只在使用者放開滑桿時觸發」

---

## 事件 4：`video_progress_75`

### 觸發場景

YouTube 或 HTML5 `<video>` 元素，觀看進度到達 75%。

### 參數設計

| 參數名 | 來源 | 範例值 |
|--------|------|--------|
| `video_title` | `<video data-title>` 屬性 | `客製化禮品製作流程` |
| `video_duration` | `video.duration`（秒） | `120` |
| `page_location` | `window.location.href` | `/products/walnut-gift-box/` |

### 對應 JavaScript

```javascript
const video = document.querySelector('video[data-track="true"]');
let fired = false;

video.addEventListener('timeupdate', () => {
  if (fired) return;
  const progress = video.currentTime / video.duration;
  if (progress >= 0.75) {
    fired = true;
    gtag('event', 'video_progress_75', {
      'video_title': video.dataset.title,
      'video_duration': Math.round(video.duration),
      'page_location': window.location.href
    });
  }
});
```

### 驗證重點

- `fired` flag 避免事件被連續送（timeupdate 一秒觸發 4 次）
- **常見漏洞**：AI 偶爾忘了 `fired` 機制 → 一次觀看會送 N 筆 `video_progress_75` 事件，數據完全失準
- **設計取捨**：要追蹤 25% / 50% / 75% / 100% 四個進度，可改成單一 `video_progress` 事件 + `progress_percent` 參數（更省事件配額）

---

## 事件 5：`form_submit_sample`

### 觸發場景

「免費索取樣品」表單成功提交後跳轉到 `/thank-you/sample/` 頁面。

### 參數設計

| 參數名 | 來源 | 範例值 |
|--------|------|--------|
| `form_location` | 來源頁的 URL | `/products/walnut-gift-box/` |
| `sample_type` | 表單 select 欄位 | `walnut` / `oak` / `cherry` |
| `user_email_domain` | email 的 @ 後段 | `gmail.com` / `company.com.tw` |
| `value` | 估算的潛在訂單金額 | `2000`（TWD）|
| `currency` | 貨幣代碼 | `TWD` |

### GTM 方案（追蹤感謝頁面瀏覽 = 最準確）

```
觸發條件：頁面瀏覽
條件：Page Path  等於  /thank-you/sample/

DataLayer 在原表單提交時 push：
window.dataLayer.push({
  'event': 'form_submit_sample_data',
  'form_location': document.referrer,
  'sample_type': sampleSelect.value,
  'user_email_domain': emailInput.value.split('@')[1],
  'value': 2000,
  'currency': 'TWD'
});

標籤類型：GA4 事件
事件名稱：form_submit_sample
事件參數：對應 5 個 DataLayer Variable
```

### 驗證重點

- **value + currency 必須一起出現**——GA4 電商報表的「轉換價值」欄位只認得「value 配對 currency」的事件。AI 漏 currency 是最常見的錯
- **標為轉換** ✅：form_submit_sample 是真正的業務轉換訊號（願意留資料 + 留聯絡方式）
- **email 隱私處理**：只送「email 網域」（gmail.com / company.com.tw），不要送完整 email——GA4 一律不應該收個人識別資料 (PII)

---

## 課後練習任務

### 任務 1：寫 prompt 跟 AI 設計（10 分鐘）

挑事件 1（最簡單）或事件 5（最複雜），用 **P7-2-A 事件結構設計** prompt 請 AI 從零設計，**不要看上面的答案**，跑完後對照。

### 任務 2：找出 AI 漏掉的細節（10 分鐘）

AI 通常會漏：
- 事件 1：`forEach` 多按鈕處理
- 事件 2：RegEx 抽檔名
- 事件 3：`change` vs `input` 事件選擇
- 事件 4：`fired` flag 防重送
- 事件 5：currency 配對 / email 網域處理

對照後追問 AI 補上，把補完的版本當作你的「最終版」貼進實作。

### 任務 3：在 LocalWP 上實作 1 個事件（15 分鐘）

選你最熟的事件（推薦事件 1）→ 在 LocalWP 站建一個有 `.quote-btn` class 的按鈕 → 用 Head & Footer Code 外掛貼 JS → 觸發 → GA4 即時報表確認看到事件。

**通關標準**：你能在 GA4 DebugView 看到 `click_quote_btn` 事件，且 `product_id`、`product_name`、`product_category` 三個參數都正確帶出。
