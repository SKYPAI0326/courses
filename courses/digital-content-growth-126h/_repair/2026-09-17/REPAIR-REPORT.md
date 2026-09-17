# Repair Report: digital-content-growth-126h

## 2026-09-17 第二批：人工審查前置修整

本批把課程從「可由機器讀取」推進到「可以交給人工冷讀」。內容證據檢查原先指出 15 個硬缺口；目前已清零。

### 本批修正

- `PRAC1`：新增從 CH1-1～CH1-3 三張卡建立 Brief 的 8 步跟做表、檢查與變化題。
- `PRAC4`：新增從 CH4-2／3／5／7 建立 SEO 與追蹤決策包的 8 步跟做表、資料狀態修復與變化題。
- 調整內容實質檢查器：正確辨識有序步驟與學員跟做表，避免把完整步驟誤判為缺漏。
- 下載流程：學員頁與附件頁統一提供 HTML 閱讀版／HTML 工作版；學員可見文字不再要求處理 Markdown 或 `.md` 檔案。
- 生成器：同步修正，避免下一次重建頁面時復原舊的 Markdown 下載連結；新增 favicon，消除瀏覽器預設圖示 404。
- 回歸測試：加入 HTML 工作版下載、favicon、學員可見文字與 Markdown 隔離檢查。

### 本批驗證

- 內容實質檢查：40／40 核心單元頁 `READY_FOR_HUMAN`；`BLOCK 0`、`REVIEW 0`、缺少素材 0。
- learner render regression：19 tests passed。
- 全課 lint：174 頁，`BLOCKER 0`、`ERROR 0`。
- 本機相對連結：572 條，缺少目標 0。
- 學員頁 Markdown 附件連結：0；學員可見文字 Markdown／`.md`：0。
- 瀏覽器冷啟動：入口、Part 1、CH1-1、附件、PRAC1、PRAC4、CH5-7 均 HTTP 200；無水平溢出、無 console error。
- 搜尋索引：891 筆；sitemap：266 筆 URL。

### 最新狀態

**人工審查前置門檻：READY。** 現在可以由人工以學員身分開始冷讀；這不等於正式販售或正式上線通過。人工冷讀仍需確認初學者能否只依學員頁與可取得附件完成產物，並記錄第一次卡住的位置。

### 回復

- 本批來源備份：`_backup/2026-09-17-substance-repair/lessons/`
- 本批來源回復：`_tools/restore-2026-09-17-substance-repair.sh`
- 前一批 learner 格式回復：`_tools/restore-2026-09-17-learner-format.sh`

## 本批結果

本批完成 Part 6 整合交付與 Part 1 產物銜接的內容修整。LocalWP／GTM 依使用者確認保留原始教學，環境供應改列課前運維檢查，沒有被當成教材內容阻塞。

## Changed

- `PRAC6.html`：加入完整成果包 HTML 入口、00–08 檔案來源／判斷／驗收表、CTA 衝突裁決、AI 跟做、學員跟做檢查表、Solo 變化題與三題提案追問。
- `assets/templates/PRAC6-完整成果包參考完成品.html`：新增完整 learner-facing 參考成果，包含案例輸入、八份檔案內容、證據目錄、五分鐘提案、追問與修訂。
- `CH6-1.html`、`CH6-2.html`、`CH6-3.html`：補上游輸入判斷、成本／工時算例、回饋邀請與紀錄算例，以及具體 AI prompt。
- `CH1-1.html`、`CH1-2.html`、`CH1-3.html`：補逐欄跟做、實際示例、存檔命名、檢查與下一單元交接。
- 對應 `_lessons/digital-content-growth-126h/*.md`：同步補入相同教學內容。
- `assets/README.md`：登錄完整成果包 HTML 與新的閱讀／下載規則。
- `_review/adversarial-learner-report.md`：把 LocalWP／GTM 重新分類為運維前置條件，更新內容判定。

## Verification

- 全課 lint：174 頁，`BLOCKER 0`、`ERROR 0`（`--no-warn`）。
- learner render regression：15/15 tests passed。
- PRAC6 新成果包連結：目標檔案存在，頁面與資產索引均有入口。
- restore script：`bash -n` passed。
- `git diff --check`：passed。
- 搜尋索引：891 筆；sitemap：266 筆 URL。
- 內容標記檢查：Part 6 上游摘要、成本算例、回饋算例、Part 1 三頁跟做段落均存在於 learner-facing HTML。

## Current gate

**本批內容修整：完成，待冷讀。**

**整門課程：尚未 READY。** 仍需以學員身分實際走完至少三條微序列，確認附件下載、頁面閱讀、檔案建立與交付包重做不需要講師補話。LocalWP／GTM 則另依正式班課前檢查表確認教室環境。

## Remaining

1. 以 Windows 教室或等效瀏覽器做 PRAC6 完整成果包冷讀，記錄第一次卡住的位置與耗時。
2. 以自己的題目完成 CH1-1 → CH1-2 → CH1-3 → PRAC1，確認欄位交接不是只能照阿凱案例複製。
3. 抽查 Part 2～5 的原始教學與 learner-facing HTML 忠實度；本批沒有順手重寫這些頁面。
4. 進行一次人工視覺檢查，特別看長表格、窄視窗與新成果包的閱讀密度。

## Restore

- Backup：`_backup/2026-09-17-content-repair/`
- Restore：`_tools/restore-2026-09-17-content-repair.sh`
