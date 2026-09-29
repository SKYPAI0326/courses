# CCS 9 小時新版主線切換報告

- 日期：2026-09-29
- 狀態：本地導覽切換已完成；課程整體驗收仍未完成。
- 決策依據：使用者指示「擴大範圍，以今天新版為主」，並同意將舊 CH5 另行封存。

## 執行內容

1. `index.html` 改以今日新版作為入口：5 個 AI 核心／實作單元共 6 小時，4 個題庫單元共 3 小時，合計 9 小時、Q1–Q80；卡片連結到 9 個 `-v2.html`。
2. `CH4.html` 舊頁的下一步連結改回課程首頁，避免前往已封存的 CH5。
3. 舊 `CH5-1.html` 至 `CH5-4.html` 與對應 4 份 Markdown 教案移入 `_archive/2026-09-29-legacy-ch5/`；原始內容另有 pre-switch 備份。其他舊頁仍保留。
4. 更新 `_gates.md`，明確區分首頁已切換與 G3/G4 尚待驗收。
5. 備份 11 個修改前檔案；還原腳本位於 `_tools/restore-2026-09-29-pre-primary-switch.sh`。

## 驗證結果

- 9 個新版單元檔案存在；首頁列出且只將新版 9 單元作為課程主線入口。
- `audit-course-substance.py` 對首頁及 CH4 的 deterministic checks：`block=0`、`missing_assets=0`；教學語意審查仍為 `PENDING`。
- `validate-course-structure.py` 對首頁、CH4 及 9 個新版單元：`checked=11 blocked=0`。
- 初次全課掃描發現舊版 `CH1-1.html` 有巢狀／未配對標籤錯誤；使用者同意後已另立 syntax-only 修復附錄並修正，詳見下方追加紀錄。
- `lint-page.py`：9 個新版單元無警示；首頁有 1 個 hover 屬性數量警示；CH4 有缺 platform metadata、非標準字級及缺少 lesson-section 容器等 3 個警示，均無 BLOCKER/ERROR。
- 還原腳本 `bash -n` 通過；目標檔案 `git diff --check` 通過。
- 已確認 4 個舊 CH5 HTML 與 4 份 Markdown 均在封存目錄。
- 本地內容錨點抽查大綱與 CH1-1、CH1-4、題庫單元：文字接龍、模型不具主動／共同個人記憶、應用程式需帶入上下文、生活／工作／多模態提示詞及分工檢核、6+3 小時與 Q1–Q80、工具中立、題庫預期答案，以及不設短影音主線，皆可找到對應內容。這是抽查，不替代獨立全課內容審查或真人試教。

## 尚未完成／邊界

- 使用者授權的獨立只讀 agent 審查遭執行環境的 `resource-guard:approval_required` 阻擋，因此本次沒有派出 agent，也不以本地靜態檢查冒充獨立內容審查。
- 瀏覽器 RWD smoke、真人初學者冷讀／跟做、LLM 平台實測仍為 `PENDING`；首頁切換不代表 G3/G4 或發布驗收通過。
- 本報告初版時，全站搜尋索引與 sitemap 尚未重建；其後依負責人發布授權，以乾淨基準加 CCS 當前頁面產生輸出，只替換 CCS 索引項目、只新增 CCS sitemap 頁面，其他課程索引項目保持不變。
- 本報告初版時未發布、未提交 Git；其後負責人明確授權以目前版本上架，本次按此新決議處理。

## 追加修復：舊版 CH1-1 HTML 語法

- 變更：`CH1-1.html` 兩組比較卡中的 16 個裝飾點改為正確的同層 `<span class="compare-dot" aria-hidden="true">`。沒有更改可見文字、href、區塊順序或課程內容。
- 根因證據：原標記 `<span><div class="compare-dot"></span></div>` 在 `</span>` 時仍開著內層 `<div>`，導致 parser 報錯並使其後標籤結構連鎖錯位。
- 修復前／後：`validate-course-structure.py` 由單頁 `blocked=1` 變為 `blocked=0`；全課批次 `checked=22 blocked=0`。`check_content_unchanged.py` 回報 `content unchanged`。
- `lint-page.py` 全課 26 頁：0 BLOCKER、0 ERROR、38 WARN；本頁 2 WARN（缺 `data-platform-version`、非標準字級），本次不擴大處理。
- 備份：`_backup/2026-09-29-pre-ch1-1-syntax-fix/pages/CH1-1.html`，SHA-256 記於同目錄 `BACKUP-MANIFEST.md`；還原腳本為 `_tools/restore-2026-09-29-ch1-1-syntax-fix.sh`。
- 此舊頁 RWD 瀏覽器驗收仍為 `PENDING`；沒有瀏覽器畫面證據，不宣告視覺驗收完成。

## 後續發布決議（2026-09-29）

- 負責人明確授權推送目前版本上架；本次提交範圍限 CCS 課程及必要索引輸出。
- RWD 瀏覽器實測與真人初學者冷讀／跟做仍為 `PENDING`，發布不視為通過該等驗收。
