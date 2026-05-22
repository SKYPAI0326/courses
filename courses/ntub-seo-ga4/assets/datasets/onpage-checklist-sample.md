# On-Page 改寫樣本 — 客製化禮品電商「弄一下文創」

> 一個虛構但結構真實的演練網站。配合 m4-3 + m5-1 + 案例 ② ③ 復跑用。
> 場景：5 個頁面狀態都「不及格」，要逐頁套 AI 寫 Title + Meta + H1 + Alt + 內部連結。
> 驗證重點：每頁標 3 個刻意設計的問題，看你 AI 改寫後能不能修對。

---

## 網站結構

| 路徑 | 頁面類型 | 主要意圖 |
|------|---------|---------|
| `/` | 首頁 | 導航型 + 品牌詞 |
| `/products/walnut-gift-box/` | 產品頁 | 交易型 |
| `/blog/corporate-gift-guide/` | 部落格文章 | 資訊型 → 商業型 |
| `/blog/wedding-favor-2026/` | 部落格文章 | 資訊型 → 交易型 |
| `/contact/` | 聯絡頁 | 導航型 + 轉換頁 |

---

## 頁面 1：首頁 `/`

### 改寫前狀態

```
<title>首頁 - 弄一下文創</title>
<meta name="description" content="歡迎來到弄一下文創。我們提供各種商品。">
<h1>弄一下文創</h1>
```

### 已知問題（3 個刻意埋的）

1. **Title 沒含目標關鍵字「客製化禮品」**——只有品牌名，不知道在賣什麼
2. **Meta Description 完全沒號召詞**——「歡迎來到」「各種商品」是萬用廢話
3. **H1 跟 Title 一樣只有品牌名**——浪費首頁這個高權威頁的 SEO 機會

### 復跑任務

套 [prompts-all.md](prompts-all.md) 的 **P4-3-A Title 三件套生成** prompt，請 AI 改寫。

**驗證重點**：AI 給的 Title 是否含主關鍵字「客製化禮品」+ 至少一個數字？AI 偶爾會用「精選」「優質」這種空話填充，要追問「換成具體數字」。

---

## 頁面 2：產品頁 `/products/walnut-gift-box/`

### 改寫前狀態

```
<title>胡桃木禮盒</title>
<meta name="description" content="">
<h1>胡桃木禮盒</h1>

<!-- 頁面內圖片 -->
<img src="walnut-01.jpg" alt="">
<img src="walnut-02.jpg" alt="walnut-02.jpg">
<img src="walnut-03.jpg" alt="image">
<img src="walnut-04.jpg" alt="">
<img src="walnut-05.jpg" alt="客製化禮品胡桃木禮盒客製化禮品">
```

### 已知問題（3 個刻意埋的）

1. **Meta Description 完全空白**——Google 會自動抓內文摘要，但通常品質低
2. **5 張圖 alt 都壞**：2 張空、1 張檔名、1 張 `image` 三字、1 張關鍵字填充
3. **內部連結 0 個**——產品頁應該連到「企業詢價表單」「客製化流程說明」這類轉換頁

### 復跑任務

- 套 **P4-3-A** 改 Title + Meta + H1
- 套 **P5-1-A 批次補 Alt** 改 5 張圖

**驗證重點**：第 5 張圖原本的 alt「客製化禮品胡桃木禮盒客製化禮品」是經典關鍵字填充。AI 改寫後**絕對不能還是長那樣**——必須改成「描述圖片實際內容」。

---

## 頁面 3：部落格文章 `/blog/corporate-gift-guide/`

### 改寫前狀態

```
<title>企業送禮指南 - 弄一下文創</title>
<meta name="description" content="企業送禮指南，告訴您如何挑選禮品。">
<h1>企業送禮指南</h1>

<!-- 內文結構 -->
<p>企業送禮是一門學問...</p>
<h2>為什麼要送禮</h2>
<p>...</p>
<h3>送禮的歷史</h3>
<p>...</p>
<h2>怎麼挑選</h2>
<p>...</p>
<h4>挑選的步驟</h4>  <!-- 跳到 H4 -->
<p>...</p>
```

### 已知問題（3 個刻意埋的）

1. **H 標籤層級跳號**：H2 → H3 → H2 → H4（中間缺 H3）
2. **內文結構鋪陳太多**：「企業送禮是一門學問」開場、「送禮的歷史」段落 → 商業意圖文章在講歷史是浪費 word count
3. **沒有 FAQ 區塊**——這篇是「指南」類型，最該加 FAQ 提升 AI Overview 引用機率（m3-3 重點）

### 復跑任務

- 套 **P4-3-A** 改 Title（這次目標：放「2026 完整指南」這種時效詞）
- 套 **P3-3-A 列 FAQ 5 題** 補文章底部 FAQ
- **手動修 H 結構**——AI 改不了你 WordPress 文章的 H 階層，自己進編輯器改

**驗證重點**：用瀏覽器開發者工具搜 `<h2>` `<h3>` `<h4>`，確認改完後沒有跳號。

---

## 頁面 4：部落格文章 `/blog/wedding-favor-2026/`

### 改寫前狀態

```
<title>婚禮小物 - 弄一下文創</title>
<meta name="description" content="弄一下文創提供各種婚禮小物，歡迎參考。">
<h1>婚禮小物</h1>

<!-- URL 結構 -->
網址：/blog/wedding-favor-2026/

<!-- 內部連結 -->
<a href="/products/">點擊這裡看商品</a>
<a href="/contact/">更多資訊請聯絡我們</a>
```

### 已知問題（3 個刻意埋的）

1. **Title 太短沒差異化**——「婚禮小物」3 字就完，沒帶任何具體性（沒年份、沒價位、沒場景）
2. **URL 中英混用且過短**——`/blog/wedding-favor-2026/` 結尾「2026」沒對應 Title 的年份
3. **內部連結用「點擊這裡」「更多資訊」**——anchor text 沒含關鍵字

### 復跑任務

- 套 **P4-3-A** 改 Title（這次目標：差異化、加價位區間或新人風格）
- **手動改 anchor text**：「點擊這裡看商品」改「精選婚禮小物商品」、「更多資訊請聯絡我們」改「索取婚禮小物報價單」

**驗證重點**：anchor text 改完後，把鼠標停在連結上看「狀態列顯示的目標 URL」是否吻合 anchor text 的描述。如果寫「索取報價單」但連到 /contact/（聯絡頁），那不算合格——應該另建 /quote/ 報價單專頁或連到表單 anchor。

---

## 頁面 5：聯絡頁 `/contact/`

### 改寫前狀態

```
<title>聯絡我們 - 弄一下文創</title>
<meta name="description" content="聯絡我們，我們會盡快回覆您。">
<h1>聯絡我們</h1>

<!-- 沒有任何 schema.org 標記 -->
```

### 已知問題（3 個刻意埋的）

1. **完全沒有 LocalBusiness schema**——聯絡頁是 LocalBusiness schema 最該放的地方，缺它 Google Maps 結果不會帶你的網站
2. **Meta Description 萬用範本**——「我們會盡快回覆您」幾百萬個聯絡頁都這樣寫
3. **沒有「上班時段」「服務區域」這些實際資訊**——使用者真正需要的轉換訊息缺失

### 復跑任務

- 套 **P4-3-A** 改 Title + Meta（加上服務區域 / 回應時效）
- 套 **P3-3-A 加 Schema** prompt，請 AI 寫 LocalBusiness JSON-LD（地址用「台北市信義區 OO 路 OO 號」這種具名虛構地址）

**驗證重點**：把 AI 給的 JSON-LD 貼進 [Rich Results Test](https://search.google.com/test/rich-results) → 應該識別為「Local business」→ 沒識別到就是欄位缺漏，追問 AI 補。
