# UI/UX 共學講義：網頁建置

講義文字的唯一真相源在 `01-PROJECTS/UIUX共學講義/<章>/`。這個資料夾只負責外觀與上架，不改講義文字。

講義來源有兩種，**以篇為單位**判斷，同一章可以混用：

| 來源 | 位置 | 用在 |
|---|---|---|
| `.tpl` | `<章>/_src/<篇>.tpl`，`{{IMG:圖/…}}` 引圖 | 第一章全部、第二章開場（共學專案制度前的格式） |
| 定稿 | `<章>/定稿/<篇>.v<N>.html`，取 N 最大的一版；`<img src="圖/…">` 的路徑相對於**章資料夾** | 第二章起的新篇。格式見 `共學專案/範本/定稿格式.md` |
| 修飾稿 | `<章>/修飾/<篇>.v<N>.m<M>.html`：選定的定稿版本（pin 或最大 N）有同一個 N 的修飾稿時，改用 M 最大的一份 | 定稿通過文案修飾後（2026-11-25 起，第二章） |

同一篇兩種都有就失敗。每章的目錄一律是 `_src/目錄.tpl`（導覽，不在定稿範圍）。

| 檔案 | 用途 |
|---|---|
| `chapters.json` | 課程名稱與首頁文字、兩個階段（`phases`）、16 章清單、每章是否開放（`open`／`soon`，`soon` 在總目錄顯示「陸續開放中」）、來源資料夾與輸出資料夾 |
| `theme.css` | 外殼，沿用舊版正式講義的冷色版面（Shippori Mincho 標題、`#167D8D` 主色、頂部列、上下頁按鈕、首頁總覽表），加上步驟卡、複製框、檢查器與手機寬度規則；後段是定稿頁的 `data-kind` 樣式與示意圖 class |
| `contrast-checker.js` | 定稿 `<figure data-kind="互動" data-value="對比檢查器">` 的執行時元件（計算與介面文字照搬第一章 L7） |
| `build.py` | 讀 `_src` 與 `定稿`、套外殼、內嵌圖片、產出課程首頁與各章頁面，逐頁比對 `<main>` 和來源一致，並替每頁補上密碼關卡 |

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

定稿頁建好後，再用共學專案的工具確認正文逐字一致，結果要「通過」（`build.py` 自己的比對更嚴，這一步是制度要求的驗證）：

```bash
python3 "../共學專案/工具/網頁比對.py" "../UIUX共學講義/CH02-A2/定稿/<篇>.v<N>.html" courses/uiux-designer/ch02/CH2-<k>.html
```

## 密碼關卡

本課有密碼關卡（repo commit `b493933e`；key `uiux_auth`，雜湊在 repo 根目錄 `inject_gate.py` 的 `COURSES["uiux-designer"]`，明文記在 `_規範/課程密碼對照表.md`，不進 git）。

- `build.py` 每次都重寫整頁，所以**每寫出一頁就只對那一頁注入關卡**（呼叫 `inject_gate.inject()`，key 與雜湊直接讀 `inject_gate.COURSES`，不另抄一份），並檢查每頁剛好一個 `<div id="_gate">`，不是就失敗。重建後**不用、也不要**再跑注入。
- 不要跑 `python3 inject_gate.py`：它會掃全部課程，改到其他課的頁面。
- 換密碼：改 `inject_gate.py` 的雜湊與對照表，重跑 `build.py`（講義頁與首頁）。`assets/`、`web-starter/` 不是 `build.py` 產生的，要照共學專案製作流程「八之二」第 5 步只對本課另外處理，且只處理還沒有關卡或需要換關卡的頁面。
- 換密碼、重建都會改到大量頁面；push 等於上線，push 前要使用者同意。

## 開放新的一章

1. 共學端把該章做完：`UIUX共學講義/CH0N-XX/` 裡有 `_src/目錄.tpl`，每一篇是 `_src/<篇>.tpl` 或 `定稿/<篇>.v<N>.html`（篇名 `R0-*`、`L<數字>-*`），圖片在 `CH0N-XX/圖/`。
2. 改 `chapters.json` 那一章：`"status": "open"`，補上 `"src": "CH0N-XX"`、`"dir": "ch0N"`；標題若和大綱不同就改 `title`。
3. 跑上面的建置指令。檔名規則：`目錄.tpl → ch0N/index.html`、`R0-* → CH{N}-0.html`、`L{k}-* → CH{N}-{k}.html`。課程總目錄會自動把這章從「陸續開放中」改成「已開放」，並列出它的每一份講義連結。
4. 跑 `python3 docs/lint-page.py courses/uiux-designer/` 確認無 BLOCKER，再 `python3 docs/build-search-index.py`、`python3 docs/build-sitemap.py`。

## 建置會擋下的情況（看到就修來源或模板，不要繞過）

- `目錄.tpl` 連到不存在的講義，或有講義沒列在目錄。
- 講義檔名不是 `R0-*`、`L<數字>-*`、`目錄`。
- 站內連結對不上任何講義；圖片找不到。
- `<main>` 前面有內容，或 `</main>` 後面有 `<script>` 以外的內容。
- 各頁 CSS 有無法自動轉換的 `box-shadow`／`gradient`（repo lint 禁用）。圓角大於 8px 會自動改成 8px。
- 同一篇同時有 `.tpl` 和定稿；定稿檔名不是 `<篇>.v<N>.html`；目錄寫成定稿。
- 定稿不是片段（有 html/head/body/main/style）、h1 不是剛好一個、有 script 或事件屬性。
- 定稿用了模板還沒畫的 `data-kind`（例如長條）；示意用了 `theme.css` 沒定義的 class；互動名稱沒有對應的 script；色票的 `data-value` 不是色碼。
- 某一頁的密碼關卡不是剛好一個。

## 定稿頁怎麼畫

定稿檔開頭的審核註解（`<!-- 定稿｜…｜通過:… -->`）是共學紀錄，建置時拿掉、不上架；其餘正文原樣放進 `<main id="main" data-正文>`，**不加任何字**（`網頁比對.py` 要逐字一致）：

- 步驟編號：`section[data-kind="步驟"]::before{content:attr(data-label)}`。
- 色票：建置掃 `data-value`，在該頁 `<style>` 產生 `[data-value="E8F0EC"]{background:#E8F0EC}`。
- 互動元件：在 `</main>` 後面附上對應的 script，執行時才畫出介面文字。新元件放成 `_build/<名稱>.js`，登記到 `build.py` 的 `INTERACTIVE`。
- 示意圖的 class：寫在 `theme.css` 後段，選擇器一律是 `figure[data-kind="示意"] .<class>`，不影響第一章同名 class。顏色、大小是課程內容，照原樣搬，不在這裡改。
- 其餘 `data-kind` 的外觀對照第一章同類 class，全部限定在 `main[data-正文]` 裡。

## 各頁 CSS 怎麼處理（.tpl）

講義每頁自帶 `<style>`。通用外觀規則（`body`、`h1`～`h3`、`.step`、`.see`、`.box`、`.eg`、表格、`details`、`.btn` 等）一律丟掉，改用 `theme.css`；`.toc`、`.stage`、`.checker` 由 `theme.css` 整組重新定義；其他規則（手機畫面示意圖 `.ba`／`.three`／`.phone`、色票 `.sw`、複製框 `.copy` 的換行設定等）照原樣保留，因為它們畫的是學員在 Figma 做的設計，顏色是課程內容。新章若出現新的示意圖 class，會自動保留；若出現新的通用元件，需要在 `theme.css` 補樣式。
