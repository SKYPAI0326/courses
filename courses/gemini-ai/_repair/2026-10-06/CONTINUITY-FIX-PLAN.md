# Gemini AI 邏輯銜接回修計畫

日期：2026-10-06（Asia/Taipei）
task_scope：`content-change`
依據：`_review/2026-10-06-LOGIC-CONTINUITY-REVIEW.md` 的 B01、M01–M09、N01–N02。
授權：使用者「設定完成，執行課程修正」。範圍限本課教材、素材和本課驗證紀錄；不提交、不 push、不部署、不改其他課或站台根目錄。

## 修正原則

- 不刪除既有頁面或範例；直接修正原文規則，避免舊指令繼續傳播矛盾。
- 同步正式來源片段、HTML、可下載指令、答案、學員素材表與 ZIP。
- 讓每個實測都有版本、資料條件、預期答案、實際觀察與修復後重測紀錄。
- 未登入 AI Studio，不寫死沒有官方文件支持的按鈕名稱；以專案網址書籤、標題、關閉／重開、A 測試為觀察步驟，平台實測仍如實待驗。
- 改動以正文節點內文字與既有素材為主，不變更頁面骨架、CSS 或導覽結構；N01 只改錯誤的導覽文字。

## 逐項修正範圍與預期影響

| Issue | 明確目標 | 修改與理由 | 版面／導覽影響 |
|---|---|---|---|
| B01 | `_source/fragments/part3-PRAC3-3.fragment`、`part3/PRAC3-3.html` | 2 天狀態改寫為已達標、較上期縮短 50%；輸出前核對判讀和數字 | 只改既有 core-2 文字及步驟，不動區塊 |
| M01 | `part1/CH1-3.html`、`_source/fragments/part1-CH1-3.fragment`、`_source/fragments/part4-CH4-1.fragment`、`part4/CH4-1.html`、`assets/materials/README.md` | 收尾選用每項工具最後通過的版本，記錄真實檔名；舊版留在歷史資料夾 | 只改既有步驟與 README 範例 |
| M02 | `_source/fragments/part3-PRAC3-3.fragment`、`part3/PRAC3-3.html`、`_source/fragments/part4-CH4-1.fragment`、`part4/CH4-1.html` | KPI 學員具名下載 JSON、做還原核對；第9站指明還原此檔 | core-2／core-1、2 既有段落內增加操作 |
| M03 | `_source/fragments/part6-CH6-1.fragment`、`part6/CH6-1.html`、`part6/PRAC6-1.html`、`_source/fragments/part4-CH4-1.fragment`、`part4/CH4-1.html` | 記錄專案標題與網址、加書籤、關閉重開、檢查預覽並重跑 A；以官方文件連結作失敗回復入口 | 在既有 Build／交付步驟補可觀察檢查，不寫死平台按鈕 |
| M04 | `part1/CH1-3.html`、`_source/fragments/part1-CH1-3.fragment`、`part2/PRAC2-1.html`、`_source/fragments/part2-PRAC2-1.fragment`、`part3/PRAC3-3.html`、`_source/fragments/part3-PRAC3-3.fragment`、`assets/materials/acceptance-template.csv`、`assets/materials/README.md` | 中文欄位；每種正常、變更、例外、修復與重開各有待測列；先填預期、後填觀察，README 給一列完整格式示例 | 僅既有正文加一段記錄指引，表格不嵌入講義 |
| M05 | `_source/fragments/part4-PRAC4-3.fragment`、`part4/PRAC4-3.html`、`assets/materials/prompt-solo-meeting.txt`、`assets/materials/meeting-c.txt`、`assets/materials/reference-answers.json`、`assets/materials/README.md`、ZIP | 為 KPI 與 AI 路線各定一項可測新規則及答案；預算沿用既有低餘額規則 | 在 capstone 原步驟內補三條路徑與連結，不新增頁面 |
| M06 | `part3/PRAC3-3.html` | 改寫 legacy KPI 指令原本的輸入／狀態規格，以 higher/lower 與缺值／零目標規則為唯一判準，移除附加覆寫造成的雙重規則 | 只改既有折疊區指令文字與一段說明 |
| M07 | `part3/PRAC3-2.html` | 將入口、摘要與選修目標收斂到輸入日期、比較重疊與時程溝通；不宣稱此版本推導關鍵路徑 | 只改 meta 與既有文案，版面不變；產生站台索引候選，不直接碰站台根目錄 |
| M08 | `part5/PRAC5-11.html` | 進階挑戰先排除忙碌與未知，只在明確全員空閒中排序；不足三筆按實數呈現、零筆明示 | 修改原挑戰文字，不動工具介面 |
| M09 | `part4/PRAC4-2.html` | JSON 匯出／驗證匯入及錯誤保留納入基礎功能與測試；把選做中重複的備份項改成別的擴充 | 修改既有生成指令和步驟，版面不變 |
| N01 | `part2/PRAC2-2.html`、`part4/CH4-1.html` | 修正上一頁導覽的過期標題，並在 Part6 接回 Part4 的第9站說明必修依站號銜接；連結位置不變 | 改一處導航標籤與一處既有路線提示 |
| N02 | `_source/fragments/part6-PRAC6-1.fragment`、`assets/materials/prompt-meeting.txt`、`part6/PRAC6-1.html`、`assets/materials/reference-answers.json`、`assets/tools/meeting-reference.html`、ZIP | A/B 答案補唯一 task_id 範例，明示識別碼需非空且不重複、語意驗收不比對固定字串 | 既有 schema／材料增欄位；答案表只加欄位，不改外框 |

## 備份、實作與驗證

1. 將所有既存目標檔案逐一備份至 `_backup/2026-10-06-pre-continuity-fix/`，保存相對路徑與 SHA-256；新增素材記錄為原先不存在。備份後才開始編輯。
2. 依 issue 分批修改，HTML 正文節點與 source fragment 對照；重新打包 materials.zip。
3. 執行課程 HTML 結構檢查、靜態連結／片段／fragment 保真驗證、課程 lint，以及引用與素材 ZIP 一致性檢查。
4. 重讀所有受影響的正文、原始指令、答案、CSV 與 README，逐項核對 B01、M01–M09、N01–N02；追加新的作者自檢與版本雜湊，不改寫前次審查歷史。
5. 重跑課程驗證器；保留 AI Studio 帳號內生成／重開實測、真人跟做及站台根目錄索引同步為待驗，除非本機實際取得證據。
6. Restore script 僅還原本表列出的原有檔案、移除本次明定新增的兩項素材，不操作其他工作樹狀態。
