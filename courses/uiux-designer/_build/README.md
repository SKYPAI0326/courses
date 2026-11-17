# UI/UX 共學講義：網頁建置

講義文字的唯一真相源在 `01-PROJECTS/UIUX共學講義/<章>/_src/*.tpl`。這個資料夾只負責外觀與上架，不改講義文字。

| 檔案 | 用途 |
|---|---|
| `chapters.json` | 課程名稱與首頁文字、兩個階段（`phases`）、16 章清單、每章是否開放（`open`／`soon`，`soon` 在總目錄顯示「陸續開放中」）、來源資料夾與輸出資料夾 |
| `theme.css` | 外殼，沿用舊版正式講義的冷色版面（Shippori Mincho 標題、`#167D8D` 主色、頂部列、上下頁按鈕、首頁總覽表），加上步驟卡、複製框、檢查器與手機寬度規則 |
| `build.py` | 讀 `_src`、套外殼、內嵌圖片、產出課程首頁與各章頁面，並逐頁比對 `<main>` 和來源一致 |

## 重建

在課程 repo 根目錄：

```bash
python3 courses/uiux-designer/_build/build.py
```

先看預覽、不動正式檔案：

```bash
python3 courses/uiux-designer/_build/build.py --out courses/uiux-designer/_local/preview
```

講義來源改了（例如修一段文字、換一張截圖），重跑同一行即可；接著依 repo 規範跑 lint、搜尋索引、sitemap，再 commit。

## 開放新的一章

1. 共學端把該章做完：`UIUX共學講義/CH0N-XX/` 裡有 `_src/目錄.tpl`、`_src/R0-*.tpl`（可沒有）、`_src/L<數字>-*.tpl`，圖片在 `CH0N-XX/圖/`，`.tpl` 用 `{{IMG:圖/檔名.png}}` 引圖。
2. 改 `chapters.json` 那一章：`"status": "open"`，補上 `"src": "CH0N-XX"`、`"dir": "ch0N"`；標題若和大綱不同就改 `title`。
3. 跑上面的建置指令。檔名規則：`目錄.tpl → ch0N/index.html`、`R0-* → CH{N}-0.html`、`L{k}-* → CH{N}-{k}.html`。課程總目錄會自動把這章從「陸續開放中」改成「已開放」，並列出它的每一份講義連結。
4. 跑 `python3 docs/lint-page.py courses/uiux-designer/` 確認無 BLOCKER，再 `python3 docs/build-search-index.py`、`python3 docs/build-sitemap.py`。

## 建置會擋下的情況（看到就修來源或模板，不要繞過）

- `目錄.tpl` 連到不存在的講義，或有講義沒列在目錄。
- 講義檔名不是 `R0-*`、`L<數字>-*`、`目錄`。
- 站內連結對不上任何講義；圖片找不到。
- `<main>` 前面有內容，或 `</main>` 後面有 `<script>` 以外的內容。
- 各頁 CSS 有無法自動轉換的 `box-shadow`／`gradient`（repo lint 禁用）。圓角大於 8px 會自動改成 8px。

## 各頁 CSS 怎麼處理

講義每頁自帶 `<style>`。通用外觀規則（`body`、`h1`～`h3`、`.step`、`.see`、`.box`、`.eg`、表格、`details`、`.btn` 等）一律丟掉，改用 `theme.css`；`.toc`、`.stage`、`.checker` 由 `theme.css` 整組重新定義；其他規則（手機畫面示意圖 `.ba`／`.three`／`.phone`、色票 `.sw`、複製框 `.copy` 的換行設定等）照原樣保留，因為它們畫的是學員在 Figma 做的設計，顏色是課程內容。新章若出現新的示意圖 class，會自動保留；若出現新的通用元件，需要在 `theme.css` 補樣式。
