# 課程講義版面契約

這份參考檔提供課程講義 HTML 修正時的固定殼層、插入位置與畫面驗證表。它不能取代任務範圍判定，也不能授權自行新增學習內容。

## 允許的頁面階層

典型講義頁面應維持以下責任分工：

```html
<body>
  <nav class="topbar">...</nav>
  <div class="progress-strip">...</div>
  <main class="lesson-page">
    <section class="lesson-hero">...</section>
    <div class="lesson-body">
      <div class="lesson-section">...</div>
      <div class="lesson-section">...</div>
    </div>
  </main>
  <nav class="lesson-nav">...</nav>
</body>
```

`.lesson-section`、`.body-text`、`.step-list`、`.prac-box` 等主要內容節點必須是 `.lesson-body` 的後代。新內容只能放在已確認的 `.lesson-body` 子樹中：

```html
<div class="lesson-body">
  <!-- 先確認不存在同一區塊，再在此局部插入 -->
  <div class="lesson-section">...</div>
</div>
```

以下結構會讓版面責任錯置，必須阻擋：

```html
<section class="lesson-hero">...</section>
<div class="lesson-section">...</div>
<div class="lesson-body">...</div>
```

不得在 hero 與 body 之間插入段落、為了插入內容新增全寬度外層容器、改變既有 wrapper 的順序或寬度責任，也不得在未獲明確要求時更換 tag 或 class。

## 插入前確認

使用 DOM/parser 找到目標 `.lesson-body` 的開始與結束位置，確認同一區塊不存在、內容確實屬於該 body，並檢查不會產生重複 id 或重複內容。若只能使用文字處理，先圈出完整容器範圍，再做局部修改；不可依賴第一個 `</div>`、第一個 class 或全域正規表示式。

## 瀏覽器 smoke checklist

靜態檢查後，至少選一個代表頁面在瀏覽器檢查：

- 桌面寬度 `1440px`：頁面頂端、修改區塊、中段、頁面底部。
- 行動寬度 `390px` 與 `430px`：完整走過同一頁。
- 修改區塊和鄰近正文使用相同內容寬度，沒有突然滿版。
- 標題、卡片、表格、程式碼區塊沒有裁切、異常斷行或水平捲軸。
- sticky header 沒有遮住標題；上一單元、下一單元、返回按鈕仍可使用。
- 首次開啟與重新整理後捲動位置合理。

若頁面用 `localStorage` 保存 scroll state，先清除舊 state，再測試重新整理、從頂端進入與從中段直接載入。不能用恢復舊捲動位置掩蓋版面錯誤。

## Sticky header

錨點跳轉要保留 header 高度；優先使用 `scroll-margin-top` 或 `scroll-padding-top`。不可用負 margin 或任意 top offset 作局部補丁，除非已確認不會影響其他頁面。

## 常見阻擋案例

- `.lesson-section` 或其他內容 class 位於 `.lesson-body` 外。
- `lesson-body` 數量不符合該頁預期，或存在重複 id。
- syntax/layout-only 前後可見文字、href 或課程順序不同。
- CSS media query 括號不完整，或頁面出現水平捲軸。
- lint 通過但瀏覽器仍有滿版內容、sticky header 遮擋或導覽失效。

遇到任一案例，回復該次修改或使用備份，標記 `BLOCK`，不要以 lint 通過宣告完成。
