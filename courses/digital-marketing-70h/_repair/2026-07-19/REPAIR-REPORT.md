# Repair Report：digital-marketing-70h

## Result

- 判定：`CONDITIONAL PASS`
- BLOCKER：0
- ERROR：0
- 既有 WARN：135（本次為學習路徑修復，未擴張到視覺／排版修復）

## Changed

### 文案基礎與策略輸入

- `m2c-1-text.html`：從多渠道完成課改為 AI 文案共通基礎，新增 `copy-workflow.md`。
- `m3-2-audience.html`：新增可跨模組引用的 `audience-brief.md`，禁止每頁重生 Persona。
- `m3-4-positioning.html`：新增 `message-brief.md`，統一 Persona、定位、核心訊息與可信證據。

### 渠道深化

- `m4-1-attention.html`：限定為自然內容停留／觀看，明示 M8 才進入付費測試。
- `m4-3-shortform.html`：明示承接 M2C-3 製作流程，本節新增情緒弧線、Hook、CTA 與平台決策。
- `m5-4-onpage.html`：SEO 文案強制引用 Persona、核心訊息、搜尋意圖與關鍵字群。
- `m8-2-copywriting.html`：由 Hook 重教改為付費廣告深化，新增漏斗、版位、KPI、唯一變因與 A/B 假設。
- `m9-2-email-psychology.html`：將 M2C Email 定位為流程預覽，本節加入名單來源、行為訊號與真實指標。
- `m9-3-lead-magnet.html`：Landing Page 強制引用 Lead Magnet、Persona、核心訊息與轉換目標。

### M10 整合

- `m10-1-kickoff.html`：Persona 與旅程由重新教授改成匯入、證據校正、缺口選擇與版本鎖定。
- `m10-2-strategy.html`：strategy brief 新增來源版本、旅程缺口與渠道取捨理由。
- `m10-3-execution.html`：execution pack 新增 M3～M7 來源產物與內容／CTA／事件／KPI 對齊檢查。
- `m10-4-presentation.html`：final A3 新增關鍵假設、AI 任務、人工修改、採納理由與下一輪重查項目。

## Verification

- 單頁 lint：13 個修改頁皆為 0 BLOCKER、0 ERROR。
- 全課 lint：63 頁，0 BLOCKER、0 ERROR、135 WARN。
- `git diff --check`：通過。
- Search index：已重建，649 筆。
- Sitemap：已重建，42 筆 URL。
- Learner-path anchors：已確認 `copy-workflow.md`、`audience-brief.md`、`message-brief.md`、`來源產物`、`A/B 假設`、`關鍵假設與 AI 使用紀錄` 跨模組存在。

## Remaining

- 135 條 WARN 屬既有技術／視覺提醒，不在本次學習路徑修復範圍。
- 本次沒有刪除或合併既有段落；若下一輪要實際壓縮重複 Hook／Persona／旅程教材，需先列出逐段刪除清單再核准。
- 尚未執行真人學員試走；正式授課前建議以零基礎 Persona 完成一次 M2C→M3→M4→M8→M10 的產物接力。

## Restore

- Backup：`digital-marketing-70h/_backup/2026-07-19-pre-repair/`
- Restore script：`digital-marketing-70h/_tools/restore-2026-07-19-pre-repair.sh`
- Syntax check：`bash -n` 通過。

---

## 課後素材包全面修復（2026-07-19）

### Changed

- `回家30分鐘復跑手冊.pdf`：M6～M10 補齊準備、完成物、操作判準、快速檢查與卡關處理；固定績效數字改為示範門檻。
- `全課程Prompt工具箱.pdf`：M10-1～M10-4 由占位說明改為可直接使用的完整 Prompt。
- `Persona樣板與練習表.pdf`：加入證據狀態示範，CAC／LTV 等策略敘述改為待驗證假設。
- `Persona研究與受眾簡報.xlsx`：新增 Persona 主檔、訪談紀錄、證據狀態與 Audience Brief，共 4 分頁。
- `整合行銷企劃工作簿.xlsx`：新增 Copy Workflow、Audience／Message Brief、M10 四階段與 AI 使用紀錄，共 9 分頁。
- `index.html`：素材包由 4 份擴充為 6 份，區分 PDF 閱讀範例與 Excel 可填寫工作簿。

### Verification

- 兩份新 Excel：13 個分頁全部渲染檢查，無截字、重疊或不可見欄位。
- 公式錯誤掃描：0 筆；XLSX 壓縮結構檢查通過。
- PDF：Persona 3 頁、Prompt 8 頁、復跑手冊 6 頁，已重新渲染並抽查所有新增區段。
- 內容掃描：無 M10 占位說明、`.md`、Markdown 或固定門檻冒充通用標準。
- 整課 lint：63 頁，0 BLOCKER、0 ERROR。
- Search index：649 筆；sitemap：42 筆 URL，均已重建。
- 6 個首頁下載連結皆有非空實體檔案；`git diff --check` 通過。

### Restore

- Backup：`digital-marketing-70h/_backup/2026-07-19-pre-materials-repair/`
- Restore script：`digital-marketing-70h/_tools/restore-2026-07-19-pre-materials-repair.sh`
