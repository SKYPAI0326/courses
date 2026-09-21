# 全站課程導覽修正報告

日期：2026-09-21
範圍：`courses/` 下 27 門課程、723 個正式 learner-facing HTML。排除 `_` 開頭目錄與 `assets/`。

## 已完成

- 44 個頁面將 logo 相對路徑統一解析到 repo 根目錄 `index.html`；包含 5 個原本斷鏈與 39 個可開啟但規格不一致的路徑。
- 18 個單元頁的頂部返回連結改回可確認存在的課程／Part／Module 總覽；`make-ai-workflow` 沒有獨立 module 頁的頁面回到課程首頁。
- 571 個頁尾導覽容器補上 `nav-prev`／`nav-next`、`aria-label` 與 `data-nav-role`。
- 第二輪修正 108 個先前被停用的位置：107 個原本有有效目標的「返回課程／Module／Part 總覽」連結，恢復 `href` 並移到獨立的 `.nav-return` 區，不再佔用上一／下一單元欄位；1 個真正沒有上一頁的首頁狀態改為非連結 `<span>`，保留原有文字並明確呈現邊界狀態。
- 底部順序導覽現在只保留真正的 `prev`／`next` 連結；有效返回動作仍可操作，不再出現引導文字存在但無法點擊的返回連結。
- 18 個複合返回標籤拆成「說明文字」與獨立可點擊返回連結；保留原文字序列，並以返回區的 CSS 間距維持閱讀分隔，避免使用者把課程名稱或完成提示誤當成連結。
- 修正巢狀 `div/nav` 導覽容器解析，並保留容器內非連結內容。
- 共 576 個正式 HTML 相對修改前 backup 有差異；正文、標題、案例、教學步驟與學習成果保持不變。

## 保留的特殊頁面

- `gen-image/CH6-supplement-typography.html` 仍有 4 個導覽按鈕。它同時包含速查站、方法論、B2 卡片與首頁入口，無法安全猜定哪兩個應成為順序導覽，因此保留並列警告。
- 18 個 n8n 舊課程頁的頂部返回連結指向 workflow tour／post-LLM overview，不是標準 `index.html` 或 `moduleN.html`；未猜改。
- 21 個舊課程特殊頁沒有明確 `.back-link`／`.breadcrumb`；未憑檔名新增返回路徑。
- 明確寫成「前往下一 Part／Module」的跨段入口保留，因為它們是現存課程路徑，不是單純返回首頁。

## 驗證結果

- `test_navigation_rewriter.py`：PASS；巢狀導覽內容保留。
- `test_navigation_action_repair.py`：PASS；返回動作恢復有效連結，真正邊界改為非連結狀態。
- `test_navigation_action_repair.py`：PASS；另驗證複合返回文字拆分後仍保留原文字序列。
- `test_navigation_content_preservation.py`：PASS；723 頁導覽外文字差異 0。
- `test_navigation_contract.py`：PASS；`broken_logos=0`、`unlabelled_two_button_nav=0`、`return_in_sequence=0`、`broken_local_refs=0`。特殊頁以 WARN 列出。
- 107 個返回區文字內容稽核：`text_content_mismatches=0`；複合標籤拆分沒有新增或刪除原文字。
- 完整相對 `href/src` 掃描：723 個正式頁現行相對引用中有 13 個既存圖片／CSS／JS 資源缺口；與修正前 backup 比對，本次 `introduced=0`，並未新增斷鏈。
- `docs/lint-page.py courses/ --summary --baseline`：BLOCKER 0、ERROR 0；WARN 2,415 條，baseline 壓掉 473 條。
- `git diff --check`：PASS。
- 本地預覽抽查：`gen-ai-36h/part3/PRAC3.html`、`gen-image/CH1-1.html`；確認複合返回區已分開顯示、返回動作可點擊、上一／下一欄位語意正確，真正首頁邊界為非連結狀態。

## 回復

修改前 723 個正式 HTML 已保存於：

`_backup/2026-09-21-pre-navigation/`

還原腳本：

`_tools/restore-2026-09-21-navigation.sh`

第二輪 108 頁修正前備份：

`_backup/2026-09-21-pre-navigation-actions/`

第二輪回復腳本：

`_tools/restore-2026-09-21-navigation-actions.sh`

本次未執行 commit 或 push。
