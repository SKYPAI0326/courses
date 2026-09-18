# Review Report：AI 入門即戰力

日期：2026-09-17

## 結論

內容與可操作性已達 `MACHINE_READY_PENDING_HUMAN`：四個單元的實務案例沒有被卡片化修飾取代，且每頁都能從契約、材料、完整示範一路走到保存、驗收、修復與下一次使用。正式標示 `HUMAN_READY` 前，仍需真人零基礎冷跟做與課堂環境複核。

## 本輪實質修整

1. 四份教案與四頁講義補上同一份八欄學員任務契約：角色／問題後果／起始材料／完成物／下一位使用者與用途／第一個動作／第一個可觀察結果／失敗回復位置。
2. CH1 保留五欄提示詞、五個完整案例、單一變因修改與實務紀錄；明確說明失敗會造成什麼後果。
3. CH2 保留 Email、訊息、自我介紹三類成品與前後版本；補上素材頁、讀者差異、未知值標記與下一步承接。
4. CH3 固定使用 NotebookLM，保留新聞、公文、書籍三類來源；明確要求引用、來源未提及、來源衝突與回到來源核對。
5. CH4 保留五大生活情境與 30 套提示詞，加入冷氣比較真值與人工確認邊界；完成物為可再利用的個人生活應用卡。
6. 入口頁與模組頁已經由搜尋索引重建；CH2 素材改為可閱讀 HTML wrapper，原始 Markdown 仍可下載。

## 驗證結果

| 檢查 | 結果 |
|---|---|
| 四頁 `lint-page.py` | 4/4：0 BLOCKER、0 ERROR、0 WARN |
| `audit-course-substance.py` | 4 pages、0 block、0 review、4 ready_for_human、0 missing_assets |
| 課程 validator preflight | 24 PASS、0 WARN、0 FAIL |
| L1–L3 | 7 頁、0 BLOCKER、0 ERROR、0 WARN；L3 因無 `prompts-*.md` 而合理跳過 |
| cold-follow contract | PASS |
| UI／實用性 contract | PASS |
| L0 冷氣真值表 | PASS；2 筆產品、3 個人工確認問題、不得直接宣布唯一答案 |
| learner-agent evidence manifest | PASS；6 pages、19 learner assets |
| copy continuity | CH1–CH4 均 0 warning，仍保留 human review required |
| teaching evidence | CH1–CH4 均 0 finding |
| 本地連結解析 | 98 條 checked、全部存在 |
| 搜尋索引 | 已重建，949 筆 |
| restore script syntax | `bash -n` PASS |

## 未宣告為完全通關的項目

- 真人零基礎學員能否在實際瀏覽器、實際發放素材與實際 NotebookLM 帳號下完成，仍需人工冷跟做。
- 手機窄版目前有 CSS 的表格可控橫向閱讀規則與程式區塊換行規則，屬機器檢查完成；本環境的瀏覽器 URL policy 阻擋重新開啟本機檔案做視覺截圖，因此不把它誤標成真人視覺驗收。
- L4a 外部模型審查仍受既有 bridge timeout 影響；不能用靜態通過代替這項證據。
