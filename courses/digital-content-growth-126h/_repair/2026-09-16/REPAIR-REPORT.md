# 2026-09-16 課程模組化修復報告

## 本輪判定

目前狀態：`MACHINE_READY / COLD_FOLLOW_PENDING`。

這份報告只確認學員頁、文字資產與機器驗證已完成；沒有把它當成可販售、可正式上線或已通過人工試教的證明。

## 已完成

- 以 `_lessons/digital-content-growth-126h/*.md` 作為教學內容來源，修正生成器不應從舊 HTML 回讀的問題。
- 重建課程首頁、6 個 Part 導覽、40 個核心單元頁與附件閱讀版；所有附件可在瀏覽器閱讀，也能下載 UTF-8 Markdown。
- 清理學員頁的講師筆記、Verification Asset Spec、製作狀態、來源路徑與不存在的 BLOCK 文案。
- M1–M6 分批補上學員可用的工作表、案例卡、合成資料、參考完成品、同伴檢核與評量規準。
- M6 補上上游產物對照、整合價值、方案交付、能力證據、30 天行動、證據矩陣與提案交付索引。
- 修正生成器的教學流程分段；40 個核心頁現在都把情境、概念、示範、操作與檢核拆成可定位段落，不再把整段流程擠在單一區塊。
- 修正附件頁返回連結，統一回到所屬單元，避免同名附件造成 404。
- 建立／保留每個模組的冷跟做紀錄與課程級人工試跑清單。

## 驗證結果

- `test_learner_render_contract.py`：15 tests OK；包含 40 個核心頁的教學階段結構檢查。
- `py_compile`：生成器與回歸測試通過。
- `git diff --check`：通過。
- 已發布範圍：173 個 HTML（47 個核心／導覽頁、126 個附件頁）。
- 本地連結：0 個不存在目標。
- 學員頁內部製作語句：0 筆。
- 核心單元重複 h2：0 頁。
- `lint-page.py`：BLOCKER 0、ERROR 0、WARN 127；核心頁的 lesson-section 警告已清除，剩餘主要來自附件閱讀頁被通用 lint 當成單元頁檢查，另有 1 個既有 callout 數量提醒。
- 搜尋索引：878 筆；sitemap：253 個 URL。

## 尚未放行

1. 人工冷跟做尚未完成，尚未確認初學者只靠頁面與附件即可開始、跟做、驗收及恢復。
2. Affinity／OpenShot 的 Windows 實機版本、安裝、完整影音素材與實際輸出仍需課前確認。
3. LocalWP／GTM／GA4 Demo、Search Console 合成資料與正式權限的教室路徑仍需實機試跑；正式 Search Console 與廣告平台不以本機模擬冒充。
4. Google Ads／Meta Ads／LINE 的正式帳號、介面與付費投放維持 BLOCK；目前只提供企劃、預算護欄與合成資料判讀。
5. 正式販售格式（DOCX、PDF、PPTX、試算表）尚未完成跨 Windows 實機驗收；目前交付承諾是瀏覽器閱讀版與 UTF-8 Markdown。
6. 5 分鐘提案與同伴回饋尚未由人工實際執行，M6 不升級為 `CONDITIONAL_READY` 或 `READY`。

## 人工冷跟做入口

從 [MANUAL-LEARNER-RUN.md](../../MANUAL-LEARNER-RUN.md) 開始，依 `index.html → module → CH/PRAC → 附件` 路徑逐單元記錄。遇到任何需要猜檔名、找不到輸入、無法判斷通過或不知道如何恢復的地方，標記 `REVISE` 或 `BLOCK`，不要用講師口頭補充掩蓋。

## 復原

- 頁面修復前備份：`_backup/2026-09-16-pre-repair/`
- 頁面還原腳本：`_tools/restore-2026-09-16-pre-repair.sh`
- 附件資產修復備份：`_backup/2026-09-16-asset-attachments/`
- 附件資產還原腳本：`_tools/restore-2026-09-16-asset-attachments.sh`

## 提交結論

目前有資格提交的是「已完成機器驗證的模組化修復版本」，沒有資格提交為「已通過人工教學驗收的販售版」。下一個必要動作是人工冷跟做，之後再依實際卡點逐模組修正。
