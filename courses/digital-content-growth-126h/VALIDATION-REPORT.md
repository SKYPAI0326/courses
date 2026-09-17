# 數位內容與成長行銷人才培訓｜整合驗收報告

> **最新狀態（2026-09-17 11:01）**：人工審查前置門檻 `READY_FOR_HUMAN_REVIEW`。請先看 [HUMAN-REVIEW-READY.md](HUMAN-REVIEW-READY.md)。以下 2026-09-16 內容保留作為歷史驗收紀錄；不應覆蓋最新結果。

## 2026-09-17 最新驗證摘要

| 項目 | 結果 |
|---|---|
| Content Substance audit | 40／40 核心單元頁 `READY_FOR_HUMAN`；BLOCK 0、REVIEW 0、缺少素材 0 |
| Learner render regression | 19 tests passed |
| 全課 HTML lint | 174 頁；BLOCKER 0、ERROR 0 |
| 本機連結與附件入口 | 619 條檢查；缺少目標 0；Markdown 附件 href 0 |
| 學員可見格式 | `Markdown`、`.md`、`原始模板` 文字 0 |
| 瀏覽器冷啟動 | 入口、模組、單元、附件、PRAC1、PRAC4、CH5-7 HTTP 200；無水平溢出與 console error |
| 搜尋索引／sitemap | 891 筆／266 筆 URL |

本狀態只允許開始人工以學員身分冷讀，不代表正式販售或正式上線通過。LocalWP、GTM、GA4 Demo 與外部廣告平台仍依課前環境契約驗證。

**驗收日期：** 2026-09-16  
**範圍：** `digital-content-growth-126h/`、對應 `_lessons/`、搜尋索引與 sitemap

## 已確認

| 項目 | 結果 | 證據 |
|---|---|---|
| 教案單元 | PASS | 40 份、總時數 126 小時、依賴鏈存在 |
| 本機資產 | PASS／部分 BLOCK | 40 份核心工作表、M1–M6 文字案例／示例／評量資產、3 組合成 CSV、環境與權限說明；外部平台資產列為 BLOCK |
| learner-facing HTML | PASS（結構） | 40 單元頁、6 Part 導覽頁、1 課程入口，共 47 頁 |
| 課程範圍 lint | PASS／WARN | 173 頁掃描，BLOCKER 0、ERROR 0；WARN 127，主要為 126 個附件閱讀頁被通用規則當成單元頁，以及 1 個 callout 數量提醒 |
| 相對連結 | PASS | 0 個不存在的本機目標 |
| 佔位連結 | PASS | `#`、前後頁佔位符與 `{{...}}` 均為 0 |
| 模板可發現性 | PASS | 40/40 單元頁都有核心模板連結；首次使用的 M1–M6 文字資產另有閱讀版與 UTF-8 下載入口 |
| 文案連貫性 heuristic | PASS／需人工確認 | 40/40 單元頁結構可連續閱讀；仍需人工冷跟做確認初學者能否獨立完成 |
| 搜尋索引 | PASS | `../search-index.json`，719 筆 |
| Sitemap | PASS | `../sitemap.xml`，94 個 URL |

## 尚未放行的項目

- LocalWP 示範網站、GTM 測試容器、GA4 Demo Account 與正式 Search Console 權限尚未完成課前驗證。
- Google Ads、Meta Ads、LINE 的示範帳號、平台畫面、正式事件與付費投放權限尚未提供；課程只使用企劃、合成資料與紙面／本機模擬。
- M2–M6 的文字案例卡、參考完成品、資料包與共同評量規準已補入閱讀版；Affinity／OpenShot 實機、平台帳號、正式資料與 DOCX／PDF／PPTX／試算表格式仍需確認。
- 40 個核心頁已將教學流程拆成可定位的情境、概念、示範、操作與檢核段落；15 項內容契約與結構回歸測試通過。
- `audit-course-substance.py` 不存在於本專案，因此沒有以該腳本宣稱內容實質通過；本報告同時記錄模組內容契約測試與人工冷跟做待辦，仍不把機器檢查當成教學完成。

## 人工下一步

請從 [MANUAL-LEARNER-RUN.md](MANUAL-LEARNER-RUN.md) 開始，依入口逐單元實跑。對每個 `REVISE` 或 `BLOCK` 記錄：

1. 你當下手上的材料與頁面位置。
2. 第一次卡住的句子、欄位、檔案或操作。
3. 你最後採用的修復方式，或仍缺少的外部條件。
4. 是否能產出頁面承諾的成果並回答檢核題。

全域建置器目前仍會被其他既有課程的 3 個舊 blocker 擋住；這不改變本課程上述 scoped validation 的結果，也不代表本課程已完成正式平台試教。

## 2026-09-16 追加：學員視角邊界修復

人工閱讀 CH1-1 時發現，部分 HTML 把教案內部註記轉成了可見文字。這些內容包括教案標題、素材狀態、`course_type`、`Verification Asset Spec`、密碼模板提示與 `BLOCK` 狀態；它們屬於課程製作／驗收資訊，不屬於學員講義。

- ☑ 清理 47 頁 learner-facing HTML 的內部 HTML 註記與製作標記。
- ☑ 將 CH1–CH2 的可見註記改寫為「情境與任務」段落，保留學員需要的工作情境、任務與完成物。
- ☑ 移除 `Verification Asset Spec`／練習資產需求清單；可取得模板與備援路徑保留在學員真正需要的位置。
- ☑ 將平台尚未具備的狀態改寫為「待課前確認」，保留限制與備援，不把內部 Gate 名稱交給學員。
- ☑ 重新驗證：47/47 lint 通過、相對連結 0 failures、佔位連結 0、40/40 continuity heuristic 無警告。

教案 Markdown 仍保留內部素材與 Gate 資訊，供課程設計、教師準備與人工驗收使用；本次修復只針對學員可見輸出。
