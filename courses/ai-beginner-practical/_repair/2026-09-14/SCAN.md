# 冷跟做修復掃描：ai-beginner-practical

## Scope

- CH1-1.html
- module1.html
- assets/worksheets/unit1-practice-sheet.md
- assets/fallback/unit1-dialogue-simulator.md

## 冷跟做結論

**BLOCK**：初學者能找到課程主題與第一份工作表，但第一步缺少清楚的文字型 LLM 取得／開始方式；另有一個 checkpoint 順序、工作表保存欄位與首頁連結問題。

## Findings

1. CH1-1.html:111 要求同時開啟文字型 LLM 對話畫面，卻沒有提供平台中立的開始說明或無法取得時的明確替代路徑。
2. CH1-1.html:115 的 U1-CHECK-1 要求前三題及晚餐表格已完成，但第 3 題晚餐操作在 CH1-1.html:117 才出現。
3. unit1-practice-sheet.md:31,37,43,53 主要只有摘要欄位，沒有讓學員貼上第 2–5 題完整回答的欄位；頁面卻要求保存五題完整回答。
4. 通知原文與備援含「下午 5 點再次公告」，頁面 CH1-1.html:119 與工作表完成條件沒有把它列為必保留資訊。
5. CH1-1.html:40 與 module1.html:34 的首頁連結使用 ../../../index.html，實際目標多一層；課程網站首頁位於 ../../index.html。

## Activity Identity Audit

| 活動 | 角色 | 素材 | 產物 | 操作路徑 | 學員決策 | 重複判定 |
|---|---|---|---|---|---|---|
| 完整示範 | Demo | 晚餐條件與五欄提示詞 | 可檢查的晚餐初稿 | 看模糊輸入→補欄位→對照條件 | 判斷輸出是否回應四項條件 | 與 Solo 不同 |
| 五題練習 | Together/Solo | 工作表五個日常問題 | 五題回答與一次修改 | 複製提示詞→保存→檢查→迭代 | 判斷可用性與要保留的資訊 | 未發現同素材重播 |
| 完成驗證 | Check | 填寫版工作表 | 可重做紀錄 | 對照輸入、輸出與版本 | 判斷是否達到保存標準 | 不產生第二份成品 |

## Shared Copy Audit

本次 scope 未發現需要合併的跨頁完整共用教學段落；首頁與代表頁的課程定位屬必要導覽文案，保留。

## Verification baseline

- 修復前 learner-path 冷跟做：BLOCK
- 修復前課程 HTML lint：已通過，未涵蓋上述語意與路徑問題
