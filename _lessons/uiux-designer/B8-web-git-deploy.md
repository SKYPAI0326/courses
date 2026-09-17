---
slug: uiux-designer
unit_id: B8-web-git-deploy
title: 用最小網頁完成版本化交付
course_type: skill-operation
duration: 13h
learning_objective: 接手 B7 Handoff 包，在本機完成可驗收的 HTML/CSS/最小 JavaScript 網頁與 Git 版本紀錄，並能指出 GitHub／部署仍待 release gate。
prerequisites: [A3, B6, B7]
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: Google Chrome、VS Code、Git（2026-09-16 本機路徑）
---

## 教學流程（Teaching Flow）

### 破題 / Hook

B7 的 Handoff 包讓人看懂 Figma 成果，雯姊還需要一個能在瀏覽器開啟的最小網頁。B8 將 HTML/CSS/JavaScript 控制在本次交付所需的範圍：頁面內容清楚、按鈕結果可觀察、檔案可重建、版本可回復。

### 概念 / Concepts

- **HTML** 定義內容與結構；**CSS** 定義視覺與手機寬度；**JavaScript** 只處理本例的完成事件。
- **本機通過** 代表在 Chrome 可開啟、點擊後有可見結果；不代表資料庫、登入或雲端保存。
- **Git commit** 記錄一個可回復版本；GitHub push 與公開部署是外部 release gate。

### 操作示範 / Demo

先使用課程提供的 `uiux-designer/web-starter/` 起始專案。你會先在 Chrome 看到靜態任務卡片，再確認一個按鈕事件，再用 Git 留下變更；每一步都保留原始檔案，方便回到上一個可運作版本。

1. 開啟 `uiux-designer/web-starter/index.html`，先看靜態任務卡片。
2. 在 Chrome 點擊「標記完成」，確認狀態、按鈕與回饋文字同時變化。
3. 讀 `styles.css` 找到手機 breakpoint，縮窄視窗確認按鈕變成滿寬。
4. 讀 `app.js`，指出事件只更新現有 DOM，不宣稱資料被保存。
5. 在 Git 查看 diff，提交一個小而可回復的 commit。

### 動手 / Hands-on

#### 起始狀態

- B7 Handoff 清單已標示來源與未驗證邊界。
- `uiux-designer/web-starter/` 有 `index.html`、`styles.css`、`app.js`、`README.md`。
- Chrome 與 Git 可使用；不需要 GitHub push 或部署權限才能完成本節。

#### 同步演練與 Checkpoint

| 步驟 | 模式 | 操作 | 預期結果 |
|---:|---|---|---|
| 1 | Together | 開啟 index.html | 標題、任務卡片、按鈕可見 |
| 2 | Demo | 點擊「標記完成」 | 狀態、按鈕、回饋文字更新 |
| 3 | Checkpoint | 重整頁面 | 讀者知道目前沒有雲端保存 |
| 4 | Solo | 只改任務標題 | 結構與互動仍正常 |
| 5 | Check | 執行 `git diff` 與 `git status` | 只看得到預期三檔變更 |
| 6 | Check | 建立 commit | 有可回復版本訊息 |

### 檢核 / Verification

- [ ] Chrome 能開啟頁面，沒有依賴遠端服務。
- [ ] 點擊後顯示「已完成」與「確認完成：任務狀態已更新」。
- [ ] 手機寬度下內容仍可讀，按鈕不被切掉。
- [ ] `git diff` 只包含這次有意義的變更。
- [ ] commit 訊息描述結果，不把 GitHub／部署寫成已通過。

### 商業情境案例（Case）

阿凱要交一個可讓客戶點開的任務清單雛形。客戶目前只需要確認「按鈕會不會回饋」與「手機能不能讀」，不需要假裝已經有帳號系統。這個小交付先讓回饋因果可驗收，再決定是否進入 GitHub 與部署。

### 動手練習題（Hands-on Exercise）

只改 `index.html` 的任務標題，保持 `styles.css` 與 `app.js` 不變；在 Chrome 回歸點擊；再用 Git 記錄。若頁面依賴網路才顯示，回到本機相對路徑檢查，不新增套件。

### 常見錯誤 3 條（Common Pitfalls）

1. **把雙擊 HTML 當作部署**：本機開啟不等於公開網址。解法：分開記錄 local pass 與 release gate。
2. **一次改三個檔案卻不看 diff**：無法知道哪個變更造成結果。解法：先 `git diff`，再小步 commit。
3. **宣稱資料已保存**：本例只更新 DOM。解法：在頁面與紀錄都寫明沒有資料庫。

### 檢核題 2 條（Quiz）

**Q1**：本例的 JavaScript 完成了什麼？
**答案要點**：監聽按鈕事件並更新狀態、按鈕與回饋文字；沒有處理登入或雲端保存。

**Q2**：什麼條件下才能進入 GitHub／部署？
**答案要點**：本機通過、diff 可審計、commit 可回復，且使用者在 release gate 明確確認外部發布。

### 講師授課筆記（不進講義）

本機 Git 與 HTML 可由 Codex 驗證；GitHub push、Pages 或其他部署需第二階段取得發布確認。若缺 VS Code，可用文字編輯器完成，但保留相同檔案與 Git 證據。
