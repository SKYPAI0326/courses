# Scan：ai-beginner-practical

**日期**：2026-09-16  
**本輪範圍**：入口環境、四個單元的完整示範、CH3 備援規格、課後整合、終點導航。  
**觸發來源**：L5 模擬學員與流程機制驗證報告。

## 盤點結論

頁面已有可跟做的基本骨架，但零基礎學員在「開始前」仍缺少通用工具啟動契約；四個單元另有部分核心操作只有提示或摘要，沒有完整可對照成品。課後整合工作表也沒有把四個上游完成物接成明確的輸入與交付鏈。

## 本輪問題

| 嚴重度 | 類別 | 位置 | 問題 | 本輪處理 |
|---|---|---|---|---|
| BLOCKER | LEARNER_PATH / Environment Contract | index、module1、CH1–CH4 gate | 密碼由課程提供者發送的條件未說明，零基礎學員無法判斷如何取得授權 | 補入口說明，不取消保護機制 |
| BLOCKER | LEARNER_PATH / Environment Contract | CH1、CH2、CH4 第一個操作前 | 沒有通用的文字型 LLM 起始畫面、登入／免登入分流與工具不可用時的終態 | 新增共用啟動卡與頁面契約 |
| BLOCKER | LEARNER_PATH / Environment Contract | CH3 第一個操作前 | NotebookLM 帳號、來源加入、引用驗收與離線備援界線不夠明確 | 補 NotebookLM 準備契約 |
| BLOCKER | CONTENT_SUBSTANCE | CH1 demo | 單一變因修訂缺少完整第二版輸出 | 補前後完整示範 |
| BLOCKER | CONTENT_SUBSTANCE | CH2 demo | LINE 訊息與三版自我介紹只有操作要求，缺少完整示範成品 | 補具體輸入、輸出與判準 |
| BLOCKER | CONTENT_SUBSTANCE | CH4 demo | 購物比較與京都修訂缺少完整表格結果 | 補完整比較表與四天修正版 |
| MAJOR | RECOVERY / CONTENT_ALIGNMENT | CH3 fallback | 備援寫「約 500 字」，與正式 300–350 字規格衝突 | 統一輸出規格並保留無正式引用限制 |
| BLOCKER | ARTIFACT_CHAIN | course-capstone-handoff.md | 未列四個上游完成物、必取欄位、回修位置、工具不可用時的處理 | 重建整合工作表欄位契約 |
| MAJOR | NAV_OPS | CH4-1 頁尾 | 無法直接從最後一單元前往課後整合 | 補 `module1.html#course-capstone` |

## Activity Identity Audit

| 活動 | 素材 | 產物 | 操作路徑 | 學員決策 | 重複判定 |
|---|---|---|---|---|---|
| CH1 Demo | 晚餐五欄案例 | 三選項初稿與單一變因版本 | 模糊輸入 → 條件化 → 檢查 → 修訂 | 判斷條件是否進入結果 | 保留；本輪補完整版本 |
| CH2 Demo | 客戶方案與固定溝通資料 | Email、訊息、三版自介示範 | 四段式 → 讀者／目的調整 → 保存 | 判斷事實與讀者差異 | 保留；補缺失 teaching atoms |
| CH3 Demo | 三份課程來源 | 摘要、引用回查與閱讀包 | 加來源 → 提問 → 點引用 → 保存 | 判斷來源是否支持句子 | 實機引用仍需 L4b |
| CH4 Demo | 京都條件與冷氣共同素材 | 行程表、比較表與修訂版 | 五欄 → 四段式 → 產生 → 只改一個條件 | 判斷唯一變因與待確認事項 | 保留；補完整結果 |

## Shared Copy Audit

本輪不複製四頁完整操作段落。新增的文字型 LLM 啟動契約集中於一份可點擊的共用 Markdown 資產，各頁只保留本頁的起始狀態、用途與分流說明；避免把同一套登入文案散落成四份不一致版本。

