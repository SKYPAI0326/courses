# AI 入門即戰力｜內容扎實度修整報告

日期：2026-09-16
範圍：`ai-beginner-practical`

## 結論

CH1-1 已完成本輪內容修整：五個核心練習現在都有正常閱讀路徑中的完整案例，並且加入半成品引導後才進入個人題目。CH2-1、CH3-1、CH4-1 經同步抽查，保留現有完整案例與操作路徑；另修正 CH2 分享預覽標題與 CH3／CH4 的版面檢查警告。

本輪內容判定：**本地課程內容 gate PASS；真人／外部平台驗收待你執行**。本輪沒有內容 blocker，但不把靜態通過擴大宣稱為正式發布驗收。

## 實質變更

### CH1-1

- 新增「先看五種成品」範例庫，正常路徑包含：
  - 自我介紹：三類可協助工作、需要確認的內容、過度承諾錯例與修正。
  - 最新天氣：無即時資料時的合格停損輸出、無時間／來源的錯例與修正。
  - 晚餐規劃：保留原本完整示範，並標為案例 3。
  - ETF：一句定義、生活例子、三個待查問題、錯誤推薦與修正。
  - 通知整理：原文、三個完整條列、五項資訊核對、漏掉行動與時間的錯例。
- 四個新增案例固定呈現「輸入 → 完整示範輸出 → 怎麼判斷 → 合理錯例 → 修正方式」。
- 個人變化由空白起步改為三個 starter：週末安排、通知整理、陌生名詞；學員先補三格並完成條件版，再轉移到自己的問題。
- Checkpoint 1 改為要求學員寫出案例判準，不只確認回答存在。
- Coverage ledger 更新至穩定 anchor，保留 `CH1-A01`–`CH1-A10` 的 ID 與 classification。

### CH2-1 至 CH4-1

- CH2-1 的 Email、訊息、自我介紹已有完整輸入／輸出／錯例／檢核，未重複改寫內容；修正 Twitter 分享標題，使其與頁面標題一致。
- CH3-1 的 NotebookLM 來源、摘要、白話公文、書籍筆記與引用判讀已具備完整案例；將引用說明由提示框改為段落帶，清除提示框數量警告；維持 NotebookLM 為唯一固定平台。
- CH4-1 的京都規劃、商品比較與 30 張生活提示詞卡已有完整案例；將操作邊界改為段落帶，並在應用卡範本檢核前加入「請填寫」引導，清除版面與文案連續性警告；維持「工具箱，不要求 30 張全做」的正確定位。

## 回復點

- 備份：`_backup/2026-09-16-pre-content-substance/`
- 回復腳本：`_tools/restore-2026-09-16-pre-content-substance.sh`
- 第二階段備份：`_backup/2026-09-16-pre-remaining-pass/`
- 第二階段回復腳本：`_tools/restore-2026-09-16-pre-remaining-pass.sh`
- 本輪只修改課程內容、教案、coverage ledger、CH2 分享預覽標題、CH3／CH4 版面文案與生成索引；未動其他 dirty worktree。

## 驗證結果

| 檢查 | 結果 |
|---|---|
| CH1-1 page lint | PASS；0 blocker、0 error、0 warning |
| CH2-1 page lint | PASS；0 blocker、0 error、0 warning |
| CH3-1／CH4-1 page lint | PASS；0 blocker、0 error、0 warning |
| copy continuity（四頁） | PASS；0 warning |
| teaching evidence（四頁） | PASS；每頁 0 finding |
| 課程本地連結 | PASS；89 個本地檔案連結、0 broken（不含頁內錨點） |
| cold-follow contract | PASS |
| UI／practicality contract | PASS |
| L0 contract | PASS |
| learner-agent evidence manifest | PASS；6 頁、20 個 learner assets |
| course-validator preflight | PASS；24 PASS、0 WARN、0 FAIL |
| course-validator L1-L3 | PASS；0 blocker、0 error、0 warning |
| CH1 learner-read checks | PASS；13/13 錨點與必要內容存在 |
| restore script syntax | PASS |

## 尚待處理

1. 全站 `check-integrity.py --strict` 仍被既有未登錄目錄擋住（18 errors、17 warnings），不是本輪課程內容造成；需另開全站治理修整。
2. 本機瀏覽器安全政策拒絕重新開啟 `file://` 頁面，因此本輪未完成原生瀏覽器畫面檢視；已以 HTML lint、連結解析、頁面契約與冷讀檢查替代。
3. 外部 LLM／NotebookLM 真實橋接與真人學員測試不在本輪重新執行；本輪可交給你做真人檢視，但不能直接宣稱正式發布 PASS。
