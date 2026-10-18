# 課程網頁講義製作系統 · 使用說明

## 這套系統是什麼

以 HTML 靜態網頁取代 PowerPoint / PDF 講義，以瀏覽器為課堂展示介面。頁面風格採「無印良品」極簡美學（米白底、明朝體標題、細緻排版），讓學員在課後直接用瀏覽器閱讀操作步驟。

**核心分工**：
- Gemini 負責生成教學內容（步驟說明、程式碼範例、常見問題）
- Claude 負責組裝 HTML、確保設計一致性與代碼品質

---

## 頁面架構

```
課程專案/
├── index.html              ← 課程首頁（Landing Page）
└── course/
    ├── index.html          ← 課程總覽（Module 列表）
    ├── module1.html        ← Module 1 總覽頁
    ├── module2.html        ← Module 2 總覽頁
    ├── m1-1-setup.html     ← 1.1 步驟操作頁
    ├── m1-2-tunnel.html    ← 1.2 步驟操作頁
    └── ...
```

每個 Module 總覽頁包含「概念卡片」(Concept Cards)，每個卡片連結到對應的步驟操作頁。

---

## 開始建立一門新課程

告訴 Claude 以下資訊，他會引導你完成：

1. **課程名稱** — 例：「Make.com 自動化入門」
2. **目標學員** — 例：「大學生，無程式背景」
3. **使用工具** — 例：「Make.com、Google Forms、Airtable」
4. **課程模組** — 例：「4 個 Module，每個 Module 3 節」
5. **授課機構** — 例：「淡江大學 · 生成式AI工作坊」

說法範例：
> 「我要為淡江大學建立一個 Make.com 工作坊課程，4個模組，目標是讓學員能夠建立自動化工作流程。」

---

## 新增單一頁面

### 建立步驟操作頁

```
/build-course-page step 2.1 "If/Else 條件判斷"
```

Claude 需要知道：
- Section 編號（如 2.1）
- 這節要教什麼（標題）
- 使用什麼工具（如有特別需求）

### 建立模組總覽頁

```
/build-course-page overview module2
```

### 更新卡片連結

當步驟頁建好後，更新總覽頁的卡片讓它們變成可點擊的連結：

```
/build-course-page update-cards module2.html
```

---

## 設計規格速查

| 項目 | 值 |
|------|-----|
| 背景色 | `#f5f3ee`（米白） |
| 主題色 | `#6b7fa3`（藍灰，可依課程調整） |
| 標題字型 | Shippori Mincho（明朝體） |
| 內文字型 | Noto Sans TC |
| 最大內容寬度 | 780px |
| Code Block | 深色背景 `#2c2b28` |

---

## 常見問題

**Q：可以調整主題色嗎？**
A：可以。建立課程時告訴 Claude「這門課的主題色用 #xxx」，所有頁面都會套用。

**Q：步驟頁的程式碼要怎麼加語法著色？**
A：Claude 會在 `<div class="code-block">` 內用 `<span>` 加上對應的 class：
- `.cm`（注解，綠）、`.ky`（關鍵字，藍）
- `.st`（字串，淡綠）、`.vr`（變數，金黃）

**Q：一個 Module 可以有幾個 Section？**
A：依課程能力路徑與導覽需要決定。每個 Section 都要有明確目的與可追溯內容；概念卡片數量依素材與學習成果決定，不用固定張數，也不能用「建置中」卡片填版面。

**Q：部署到哪裡？**
A：GitHub Pages（靜態網站免費部署），把整個課程資料夾推上 GitHub 並開啟 Pages 即可。
