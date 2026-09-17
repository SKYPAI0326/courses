# 數位內容與成長行銷人才培訓：學員資產可用性修復計畫

## Scope

- slug: `digital-content-growth-126h`
- target: 47 個主課程 HTML、126 份 Markdown 資產及其 252 份 HTML 閱讀／工作頁
- focus: 學員資產分類、可填寫欄位、草稿保存、完成版匯出、下一單元交接

## Confirmed problem

目前 126 份 `*-工作版.html` 的學習正文與閱讀版完全相同。0 份具備文字輸入欄位、表單或 `contenteditable`；48 份只有 checkbox，78 份沒有任何控制項。40 個主課頁把學員送到 Word／記事本等外部工具。這使「HTML 工作版」只有外觀與下載功能，沒有完成學習產物的能力。

## Principle-level repair

### 1. Asset type is explicit

生成器依 `_tools/asset-contracts.json` 的集中式契約與少量明確例外判定兩種 learner asset：

- `worksheet`：需要學員輸入、比較、判斷、記錄或交接的資產。預設生成可填寫工作版。
- `reference`：案例、參考完成品、示例、術語、資料、規則與評量規準。只生成可攜式閱讀／參考版，不偽裝成工作表。

worksheet 與 reference 都保留原始閱讀版；差異只發生在下載的 learner asset，不改掉原始教學正文。
站內檔名也區分為 `-工作版.html` 與 `-參考版.html`，不讓參考資料沿用會誤導學員的工作版檔名。

### 2. Worksheet has a complete action loop

每份 worksheet 必須具備：

1. 這份資產要完成的成果與使用位置。
2. 可輸入的文字欄位與可勾選的檢查項。
3. 「儲存草稿」：優先使用 localStorage；本機限制時顯示可理解的備援訊息。
4. 「下載完成版 HTML」：把學員輸入轉成可攜式完成品，不依賴伺服器。
5. 完成檢查與下一單元／下一個使用位置。

### 3. Reference does not claim to be editable

reference 的下載文字、頁面標題與說明都改為「參考版」。它仍可下載、列印與複製，但不會出現空白輸入欄位或假的工作表控制項。

### 4. Generation is the source of truth

不手工修改 126 份產物。所有欄位、工具列、儲存、匯出與 asset-kind 標記由 `_tools/rebuild-learner-shell.py` 生成，測試直接檢查生成後的 HTML contract。

## BLOCKER

### [LEARNER_PATH] 所有 worksheet 資產

- 問題：學員無法在交付的 HTML 中輸入答案或取得完成品。
- 修法：依表頭與空白欄位契約保留示範／預期結果，僅把學員回答欄轉成 textarea／checkbox，加入儲存與完成版匯出。
- 驗證：每份 worksheet 有 `data-workbook-kind="worksheet"`、至少一個 `data-workbook-field`、save/export controls 與 inline runtime。

### [ASSET_CONTRACT] 參考資產被標示為工作版

- 問題：案例與參考完成品被放在同一種「工作版」下載語意下，學員無法知道哪些要填、哪些只需閱讀。
- 修法：生成 reference badge、參考版下載名稱與只讀說明。
- 驗證：reference 不得有 worksheet save/export controls。

### [ARTIFACT_CHAIN] 產物無法交接

- 問題：講義宣稱有完成物並交給下一單元，但目前完成物要人工複製到外部工具才可能產生。
- 修法：worksheet 匯出完成版包含學員輸入、核對狀態與下一單元摘要。
- 驗證：冷跟做可在單一下載檔完成填寫、保存與匯出。

## MAJOR

- 既有 lint 與內容審計沒有檢查工作資產是否可輸入；新增產物 contract tests，避免再次被外觀綠燈放行。
- 目前講義中的「複製到 Word／記事本」需改成可選備援，而非主要完成路徑。

## Execution order

1. 備份與 restore script
2. 先寫產物 contract tests，確認目前失敗
3. 實作 asset classification 與 worksheet runtime
4. CH1-1 重新生成與冷跟做
5. 全課生成、lint、內容審計、工作資產統計
6. 產出 repair report，再決定是否發布

## Non-goals

- 不把每個參考案例改成可編輯表格。
- 不新增外部帳號、雲端資料庫或付費工具。
- 不以 CSS 或改檔名宣稱工作版已完成。
