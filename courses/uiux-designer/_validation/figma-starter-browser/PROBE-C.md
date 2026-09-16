# Probe C：輸出與交付

**課程**：`uiux-designer`  
**Run ID**：`20260916-figma-starter-browser-001`  
**測試日期**：2026-09-16  
**工具**：Google Chrome（Figma 網頁版）＋本地 Git 工作樹  
**方案**：Figma Starter／Free  
**測試檔**：`Codex Figma Starter Audit - Probe B Overlay`  
**工作檔 URL**：`https://www.figma.com/design/OdwdoNhWJCsC9a8wq17Dy3/Codex-Figma-Starter-Audit---Probe-B-Overlay?node-id=1-6&t=jtKgRBGCgpow3bxF-0`  
**整體判定**：`CONDITIONAL`

## 實測步驟與結果

| Step | 操作 | 實際觀察 | 判定 |
|---|---|---|---|
| C-01 | 選取 `Screen / Host`，加入 Export settings | 右側建立 Export row；預設 `1x`、檔案類型 `PNG`，出現 `Export Host` 按鈕 | `MACHINE_PASS` |
| C-02 | 打開 Export file type 下拉選單 | 實際提供 `PNG`、`JPEG`、`SVG`、`PDF` | `MACHINE_PASS` |
| C-03 | 匯出 Host PNG 與 PDF | Chrome 下載兩個 zip；內含 `Screen/Host.png`（402×874）與 `Screen/Host.pdf`（PDF 1.7、1 page）；已複製到本紀錄的 `exports/` 並檢查檔案類型 | `MACHINE_PASS` |
| C-04 | 選取 `Dialog / Overlay`，匯出 PNG | Chrome 下載 zip；內含 `Dialog/Overlay.png`（320×200）；用影像檢查確認文字 `確認完成` 存在 | `MACHINE_PASS` |
| C-05 | 切換 Figma `Dev Mode` | 右側顯示 `Inspect`、`Layer properties`、`List／Code`、`Language: CSS`、Layout／Colors／Assets；可看到程式碼檢視入口 | `MACHINE_PASS` |
| C-06 | 檢查分享與版本交付入口 | `Share` 按鈕存在；本輪沒有點擊或改變分享權限。工作樹已有本次稽核 commit，`origin` GitHub remote 存在；本輪不執行 push／公開部署 | `CONDITIONAL` |

## 交付檔案

- [Probe B Host PNG](./exports/probe-b-screen-host.png)：402×874 PNG，實際從 Figma 匯出。
- [Probe B Host PDF](./exports/probe-b-screen-host.pdf)：一頁 PDF，實際從 Figma 匯出。
- [Probe B Overlay PNG](./exports/probe-b-dialog-overlay.png)：320×200 PNG，含 `確認完成` 文字。
- 原始 zip 也保留在同一個 `exports/` 目錄，方便追查下載封裝行為。

## 對課程設計的影響

- Figma 免費方案的輸出主線可以教 PNG／JPEG／SVG／PDF 與 Dev Mode CSS 檢查。
- 「分享權限」應在講義中拆成檢查步驟，並明確要求學員確認權限後再交付；本機器階段不代替使用者改成公開連結。
- Git/GitHub 可作為課程外部交付的必要流程：本地 commit、檔案清單、復原步驟先驗收；`git push` 與公開部署列為之後真人／發布階段，避免把本機已 commit 誤寫成已公開。

## Probe C 結論

免費瀏覽器版的輸出與 Inspect 可以形成可驗收成品；分享權限、GitHub push 與公開部署涉及外部狀態，本輪保留為 `CONDITIONAL`。課程可以先設計「本地交付包」與 export 檢查，等人工階段再確認實際帳號的分享權限與公開網址。

