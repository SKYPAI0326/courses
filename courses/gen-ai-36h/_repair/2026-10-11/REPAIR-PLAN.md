# Repair Plan — 2026-10-11

task_scope: content-change
授權：使用者已閱讀全課診斷後要求「執行修正作業」。依既有 17 項診斷修復，不新增課程架構或刪除單元。舊教學重複要求改為有不同目的的練習；答案移至完成後核對區，完整舊文保留於備份。
基準：ac6e061caef847332ad2fe303db9530fc638e0ce。原工作目錄是較早版；兩邊已獨立備份。

## Files and acceptance
- `_repair/2026-10-09/lesson-plans/{CH1-1..PRAC7}.md`：28 份逐章檢核；保留完整已有示範，補首次推論／可交付成品／練習新增判斷。
- `part1/` 至 `part7/` 對應 28 HTML：僅替換 .lesson-body 及相關 metadata/完成物；保留 shell、gate、導航與新分頁。
- `assets/workplace-cases/part2/*`、`part3-demo/*`、`part3-solo/*`、`assets/capstone/*`：修來源指向、示範／答案時機及測試 ID；不改已核准業務事實。
- `assets/START-HERE.md`、新增操作指南／流程卡／獨立變更包／九欄測試資料／核對答案：每份具體輸入、輸出、核對及備援，單元首次使用處有連結。
- `assets/reference-chart.html`：補各區域有效筆數，與原始交易清理規則一致。
- `_tools/render-lessons.py`、`_repair/2026-10-09/lesson-meta.json`：保留新分頁，完成物改實際檔案；避免固定比例假議程。
- `index.html`、同課 `_lessons/gen-ai-36h/`、全站搜尋與 sitemap：僅同步必要同課內容；在乾淨發布副本先產製，以免混入他課工作。
- `_repair/2026-10-11/*`：issue closure、Activity Identity、Shared Copy、來源保真、結構／lint／browser 證據。

## Execution order
1. 保留 scan 與 17 項根因；保存兩份 baseline、manifest 與 restore script，bash -n。
2. 逐 Part 修正式教案與依賴素材：B01/B02/B03、M01..M11、N01..N03。
3. content review 後每 1–3 頁轉製，檢查 source atoms、links、gate/nav、新分頁與結構/lint。
4. 檢查可算值、表單欄位／JSON、連續課產物；重建同課鏡像與索引。
5. browser 1440/390/430 smoke；真人與私有 SaaS 執行仍標未驗，不據靜態結果宣布開課就緒。
6. 同步回工作目錄；只處理本課檔案。依既有 push main 授權，僅在本輪驗證結果可交付且工作副本乾淨可審核時發布，不混入其他課程。

## Layout / removal
保留既有外層、字型、配色、導航、關卡。新增內容置於 .lesson-body；表格沿用橫向捲動容器。
不刪除單元或既有素材；將解答提示移到同頁核對區／答案檔，過時錯誤說法修正，重複練習新增真實條件。不是移除教學能力。
