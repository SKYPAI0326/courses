# Gate Record：AI 入門即戰力

## G1 大綱

- **status**：PASS（依使用者 2026-09-14 明確確認的課程範圍）
- **受眾**：零基礎成人學習者
- **總時數**：12 小時，4 × 3 小時
- **固定平台**：NotebookLM
- **其他工具**：LLM 通用方法，不指定平台
- **明確移除**：獨立資安內容、ChatGPT／Gemini 指定操作與平台比較
- **最需要新製作的範圍**：第 4 單元 30 套生活化提示詞與各單元指定練習素材

## G2 全課教案與頁面

- **status**：PASS（四份 lesson plan、四個 learner-facing HTML、工作表與來源素材已完成）
- **證據**：本課 6 頁 HTML lint 為 0 BLOCKER、0 ERROR；四頁均有完成物、步驟、checkpoint、預期結果與回復路徑。
- **保留事項**：內容實質自動審查依賴的部分規範檔目前未在本專案中，仍須以 L4a／L5 真跑補足證據。

## G3 代表頁

- **status**：CONDITIONAL
- **條件**：內部 learner-path 檢查已完成；頁面已標明「講師發放密碼後自學」及原報名／課堂通知管道的申請／重發路徑。仍需使用者或真人零基礎學員只拿講義與列出的素材進行冷跟做，不以作者自述代替；正式上線端也要確保該發放管道實際存在。

## G4 網頁運維

- **status**：PASS
- **證據**：入口頁、模組頁、四個內容頁已加入課程導覽；本課本地連結 89 條無缺漏；正式 HTML 閘門完整；搜尋索引與 sitemap 已重建。密碼保護頁未列入 sitemap，符合目前建置規則。

## G5 真跑驗收

- **status**：IN_PROGRESS
- **已完成**：L0 冷氣案例真值表、L1–L3 靜態檢查、L5 學員 Agent 設計與 6 頁／20 素材 evidence manifest、模擬學員重跑（0 頁 BLOCK）；另完成一次 NotebookLM 實機 sentinel：3 個來源加入、依來源回答、引用點擊回查均成功（詳見 `_validation/L4B-NOTEBOOKLM-REAL-2026-09-16.md`）。
- **已執行但降級**：使用者已授權資料傳輸；L4a case1／case2 已送出，但 Codex bridge 均在 300 秒 timeout，無模型輸出、無分數（詳見 `_validation/L4A-MANUAL-REVIEW.md`）。
- **待完成**：L4a case3／case4、L4b 多情境／環境覆蓋、L5 真人／零基礎 persona journey。
- **限制**：目前 Codex bridge 外部模型服務連續兩案不可用；在服務恢復或改用使用者可控外部模型環境前，不宣告 L4a／L5 PASS。
