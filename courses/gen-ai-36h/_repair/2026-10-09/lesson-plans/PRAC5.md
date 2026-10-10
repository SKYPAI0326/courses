---
slug: gen-ai-36h
unit_id: PRAC5
title: 交付人工覆核後分流的流程
course_type: integration-capstone
platform_version: 2026-10-09，教學工作區已實跑；開課當日須重查介面
learning_objective: 分別驗收新業務分類案例與原T01–T07流程執行及恢復證據。
---

# 交付人工覆核後分流的流程

<!-- learner-content:start -->
## 同時驗收業務判斷和 Make 路由
Make 工作流主線與[既有 T01–T07](../assets/part5-test-cases.csv)維持原樣。本次另用[未分類原文批次](../assets/part5-unclassified-messages.csv)驗收業務判斷，查[答案鍵](../assets/part5-classification-answer-key.md)前先自行分類。兩類證據分開保存：分類正確不能代替流程執行，流程成功也不能證明分類合理。

## 第一關：完成候選列與人工覆核
對 U01–U07 逐筆記錄主要分類、九欄完整性、來源鍵、需補問或人工接手的理由、是否可覆核。多重意圖要說明選擇；U02不可沿用引用的舊營業時間；U03/U04是同鍵重複；U05資料不足需停止；U06走客服人工處理；U07雖可分類，答案仍待查。先把所有列標為待覆核，答案鍵核對後由人決定哪些有足夠資訊可轉成已覆核。禁止猜缺值。

## 第二關：按 T01–T07 重建或重跑流程
依[表格配置](../assets/part5-sheet-layout.md)和[九欄規格](../assets/part5-input-contract.md)確認 Source、ReviewedQueue、ProcessingLog、Drafts。只有人工核准且九欄完整的新列才進 ReviewedQueue。保持現有四分類、去重鍵、狀態、路由和「只寫未寄出草稿」行為；不要為新案例改動 T01–T07。匯入 Blueprint 後重連自己的帳號與試算表；無權限則只交欄位決策與流程設計，外部執行標 `NOT_RUN`。

| 測試 | 預期路由／狀態 | Drafts 預期 | 驗收點 |
|---|---|---|---|
| T01 inquiry | 業務 | 1 份未寄出 | source_key 與分類正確 |
| T02 complaint | 客服人工處理 | 0 份 | 不建立通知草稿 |
| T03 partnership | 合作 | 1 份未寄出 | 收件人只用自己的測試地址 |
| T04 other | 待處理 | 0 份 | ProcessingLog 有紀錄 |
| T05 待覆核／無效分類 | 阻擋 | 0 份 | 不分流、不寫草稿 |
| T06 重複 source_key | duplicate／不新增 | 0 份新增 | 既有紀錄與草稿不重複 |
| T07 Drafts 表名錯誤後恢復 | 保留錯誤，再從失敗步驟恢復原分類 | 最多 1 份有效草稿 | 不重跑全流程造成重複 |

逐案記輸入、execution ID／截圖、結果列、草稿數和判定。T05必須被擋；T06不新增；T07從失敗步驟恢復並最多留一份有效草稿。未跑就填 `PENDING`，不能把教學工作區證據當個人執行結果。

## 交付
交付 U01–U07 的業務分類表與理由、自己的人工覆核標記、T01–T07執行紀錄和恢復說明。答案鍵核對後如有不同判斷，保留證據與修正理由。不得讓任何新列在人工核准前進 ReviewedQueue；不得啟用寄信或把草稿當已寄出。
<!-- learner-content:end -->

## 教師與版本紀錄（不轉製學員正文）
- 正文為本版學員契約：段落交代起始材料、完成物、步驟、核對及修復；素材於首次使用處連結。
- 授課：示範後讓學員同步做；遇來源不支持、保存失敗或無權限時停在該步修復。
- 內容審查：本次單一 agent 自審；無獨立 reviewer 或真人試走證據。平台／瀏覽器待驗項目見 ENVIRONMENT.md。
- 靜態來源與素材存在檢查在轉製前執行；未驗證的SaaS能力不據此宣告PASS。
