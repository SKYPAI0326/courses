---
course: uiux-designer
date: 2026-09-17
purpose: 记录本轮「掃描 → 修正 → 驗證」循環
status: MACHINE_READY_PENDING_HUMAN
---

# 2026-09-17 內容與路徑循環檢查

## 循環 1：內容實質性

檢查範圍：16 個 learner-facing 單元頁、16 份教案、入口頁、起始材料與完成檢查表。

發現：B6、B7、B8 的頁面只有六段主要內容，示範、完成物與修復責任沒有前五個單元清楚；B7、B8 的主要導覽按鈕曾回到自己；B6 的上一堂跳過 B5。

修正：

- B6 增加情境五問、固定測試欄位、失敗輸入到回歸結果的示範、八步跟做、Checkpoint、單一變因 Solo、B7 交接與自我測驗。
- B7 增加接手者五問、來源／輸出／Inspect 概念表、三份輸出的示範、八步 Handoff、尺寸與權限邊界、版本變化練習與 B8 交接。
- B8 增加本機成果五問、Git 五步驗證表、Chrome／手機 Checkpoint、錯誤回修表、標題單一變因練習、可回復停止點與總覽回入口。
- B6 上一堂改為 B5；B7 下一堂改為 B8；B8 導回課程總覽。

## 循環 2：靜態與文案

結果：

- `lint-page.py courses/uiux-designer/ --summary`：50 頁、0 BLOCKER、0 ERROR、0 WARN。
- `lint-page.py courses/uiux-designer/ --by-bucket`：0 BLOCKER、0 ERROR、0 WARN。
- `audit-copy-patterns.py --strict`：0 finding（0 BLOCK、0 REVIEW）。
- `audit_copy_continuity.py`：16 個單元頁均 0 warning。
- B6／B7／B8 `audit_teaching_evidence.py --artifact 完成物 --artifact 檢查`：3 頁均 0 finding。
- `git diff --check`：通過。

## 循環 3：路徑與實際瀏覽器

結果：

- 本地連結掃描：185 個相對連結、0 missing。
- Chrome localhost 載入入口頁，入口顯示 16 堂清單、42h／57h／99h 區段、完成物與單元接續欄位。
- Chrome 載入 B6，確認 B5 上一堂與 B7 下一堂均可見。
- Chrome 載入 B7，確認 B6 上一堂、B8 下一堂與 B7 完成物均可見。
- Chrome 載入 B8，確認 B7 上一堂與課程總覽回入口均可見。
- Chrome 載入 `web-starter/index.html`，按下「標記完成」後確認狀態顯示「已完成」、按鈕 disabled、回饋文字「確認完成：任務狀態已更新」，瀏覽器錯誤／警告為 0。

## 循環 4：正式驗證系統

`course-validator` preflight 通過 23 項，只有 `datasets/` 不存在的概念課警告。L1-L3 通過；L0 因本課是工具操作課、沒有 truth-table dataset，保留 `MANUAL_REQUIRED`。L4a、L4b、L5 仍是 `PROMPT_USER`，需要後續人工／Codex consult 與 verdict，不能標記 READY。

## 目前仍未放行的 Gate

- Figma Starter 的固定元素與滾動聯合行為仍需真人跟做與跨帳號重跑。
- Swap、Smart Animate 完整效果、Form 多欄位、List 動態增刪仍受方案或未測狀態限制。
- Photoshop 實際開檔／色彩／回存、GitHub push、公開部署尚未執行。
- 16 單元的真人冷讀、連續微序列與跨帳號重建尚未完成。

因此本輪判定為 `MACHINE_READY_PENDING_HUMAN`：課程檔案、內容結構、相對路徑與本機網頁互動已通過；真人學員仍可在人工 Gate 前發現工具版本或操作差異，狀態不能升為 `READY`。

## 循環 5：30 秒學員入口修復（2026-09-17）

上一輪的檔案存在性掃描沒有辨識兩種語意問題：B6、B7、B8 頁首把學員送到製作層 Blueprint；起始材料連結晚於第一個操作。本輪建立備份與還原腳本後完成最小修補：

- 三頁頁首改回課程總覽，不再連到 `_design/COURSE-BLUEPRINT.md`。
- B6、B7、B8 的核心起始材料都在第一次操作前出現，並附用途與本機備援路徑。
- 新增 `uiux-designer/_tools/learner-entry-smoke.py`，掃描 16 個 learner-facing 頁面，鎖定內部文件目標與起始材料順序。
- 語意入口掃描：PASS；171 個 learner／asset／web-starter 相對連結：0 missing；Chrome B6 → B7 → B8 → 課程總覽：PASS。

本輪結論：入口層的立即 `BLOCK` 已解除，可以安排聚焦人工試讀；整門課仍維持 `MACHINE_READY_PENDING_HUMAN`，不得宣稱 Figma、Photoshop、GitHub、部署或真人冷讀已放行。

## 循環 6：內容證據掃描修復與人工審查入口（2026-09-17）

上一輪內容掃描器只看課程根目錄，曾把位於 `part1/`、`part2/`、`part3/` 的正式頁面誤判成 0 頁。這會產生假綠，因此先修正共用掃描器的遞迴頁面發現，再重新產出證據清單；同時補上 B4 的起始材料說明。

- `audit-course-substance.py --build-evidence-manifest`：16 pages、0 BLOCK、0 REVIEW、16 READY_FOR_HUMAN、0 missing_assets。
- B4 第一段明確列出 Host／Overlay 參考圖、Starter 檔案與 B4 起始頁；B6、B7、B8 維持第一次操作前可取得材料。
- `learner-entry-smoke.py`、HTML lint、文案風險掃描、相對連結掃描與 `git diff --check` 重新執行後仍通過。

本輪結論：可把 B4 → B5 → B6 交給人工做第一階段冷讀；整門課仍維持 `MACHINE_READY_PENDING_HUMAN`，L0、L4a、L4b、L5 與平台／外部服務 Gate 不得以靜態證據代替。
