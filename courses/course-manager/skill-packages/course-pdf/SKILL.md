---
name: course-pdf
description: "依現有課程 HTML 轉製 PDF 講義，設計紙本版面、核對完整內容、登錄集中講義庫，並在網頁或素材變更後檢查與同步 PDF。用於課程講義轉 PDF、既有成品來源盤點及版本更新。"
---

# 課程講義 PDF 轉製

先讀適用 AGENTS.md，確認使用者要盤點、設計、登錄、產製、同步、驗收或回復。
沿用已授權範圍；使用者要求「先不產 PDF」時只執行非產製模式。
詳細命令、配方、狀態與驗收資料見 [workflow](references/workflow.md)。

## 入口與能力檢查

使用 `python3 <本技能目錄>/scripts/run.py doctor` 定位專案與檢查依賴。
launcher 支援 `--root <courses 絕對路徑>`；從目前目錄向上找專案，最後使用本機既有課程路徑。
使用能載入 BeautifulSoup、Playwright、pypdf 的 Python；doctor 未找到依賴時先回報，不把通用 PDF 套件存在當作轉製環境已完整。
先前未完成的引擎／配方／驗收缺口如實報告，不虛構命令或引用不存在的成品。

## 內容與版面邊界

- 正式 HTML 是教學內容來源。核對頁面、完整內容 selector 與來源順序；教案／大綱只用於定位，不補寫網頁缺失內容。
- 保留正文、示範、Prompt、公式、程式碼、練習、答案、圖片及素材連結。不摘要、不潤飾、不新增教材。
- 在暫存副本套列印 CSS 與可追溯的 UI 轉換；不修改正式網頁。需另修網頁時遵循 course-html-contract。
- details 使用原文展開；有標籤的 radio／checkbox 僅移除 widget，保留全部選項文字。隱藏教材需明列展開 selector 與原因。
- 原生表單使用明列的 print-source-values 轉製路徑，只保留來源值與標籤；其他必要互動／srcset／動態內容沒有已確認的來源轉製路徑時回報 BLOCKED，交回來源責任人；不能撰寫替代教材。
- 封面、目錄、頁碼、作者及版本資訊須來自來源或已確認登錄。保留原文符號、數字及程式碼；網址重映射保留目標並記錄。
- PDF 設計只改閱讀呈現。通用 PDF／kami 的改寫、摘要、新增圖表及字元替換預設不能覆蓋內容忠實要求。

## 標準流程

1. `inventory`／`register-existing`：盤點與登錄；素材／備份／驗收檔保留原位。無有效建置證據的舊成品保持 UNVERIFIED。
2. 讀來源及所用資產，建立明確且按教學順序排列的配方；以 `plan` 檢查 selector、依賴、網址及指紋，再 `bind` 登錄。候選來源不能直接填成已確認來源。
3. `status`／`sync`：查看過期及受影響成品。`sync` 預設只提出清單；不帶 `--create-pdf` 就不產製。
4. 已授權產製才執行 `build --create-pdf` 或 `sync --create-pdf`。來源快照、載入檢查或機器驗收失敗時保留前版。
5. 建置成功僅為 PENDING_REVIEW。讀 machine-verification，逐頁檢視產出的 PNG；使用 PDF 工具放大問題區，檢查字型、裁切、重疊、表格、程式碼、圖片及連結。
6. 依實際檢視結果填 review-template 的副本，記錄執行者種類及身分；未看過的頁面不得填 reviewed，未完成的檢查不得勾選通過。
7. `verify --review` 檢查精確成品、來源與全頁證據；通過後 `promote --review` 才更新集中 PDF、登錄與取用索引。
8. 回報來源、輸出、最後檢查時間、版本狀態、證據及未驗項目。格式通過或檔案存在不能當作內容／畫面驗收。

## 管理與聯動

成品放 `courses/output/pdf/<slug>/`；配方、操作與驗收保存在 course-manager。
維持穩定下載名稱；新增網頁入口、變更來源內容或發布依當次授權辦理。
HTML／CSS／圖片／字型／配方／引擎改動後使用同一套指紋重新判定；自我 PDF 下載目標不作輸入 bytes 依賴。
網頁 builder 與運維可呼叫 launcher 的 `sync --course <slug>` 作唯讀交接；沒有 watcher／排程時不能宣稱持續自動同步。
回復預設 dry-run，先核對 hash；後續改動或證據缺失時停止，保留新工作。
PDF-only 指南及編輯／節錄版保留來源類型，不逆向生成網頁，不被完整版本悄悄取代。
