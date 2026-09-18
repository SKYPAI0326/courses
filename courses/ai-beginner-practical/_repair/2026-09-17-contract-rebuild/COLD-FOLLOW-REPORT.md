# Cold Follow Report：AI 入門即戰力

日期：2026-09-17

## 模擬學員入口檢查

以只讀 learner-facing HTML 與頁面列出的素材為範圍，逐頁核對 30 秒入口六題；四頁均能在第一個工具動作前找到答案。

| 單元 | 起始材料 | 完成物 | 第一個動作與結果 | 失敗回復 |
|---|---|---|---|---|
| CH1 | 實務紀錄表、文字型 LLM；工具不可用有離線備援 | `unit1-practice-sheet-complete.md` | 複製工作表、另存、填姓名日期；看到五題欄位 | `U1-START`、`U1-ASK`、`U1-REVISE` |
| CH2 | 日常溝通素材頁、可保存筆記、文字型 LLM | `unit2-communication-pack-complete.md` | 複製素材包、確認三區與索引；再開啟新對話 | `U2-START`、`U2-PROMPT`、`U2-EMAIL`、`U2-MESSAGE`、`U2-ITERATE` |
| CH3 | NotebookLM、課程來源包、來源索引、三類閱讀素材 | `unit3-notebooklm-reading-pack-complete.md` 與 NotebookLM 筆記本 | 建立筆記本並加入來源；看到三類來源與來源名稱 | `U3-SOURCE`、`U3-SUMMARY`、`U3-ANNOUNCE`、`U3-CITE` |
| CH4 | 30 套提示詞卡、個人化工作表、冷氣資料、文字型 LLM | `unit4-lifestyle-application-card.md` | 選一張卡並填五欄；看到自己的任務條件 | `U4-SELECT`、`U4-PROMPT`、`U4-CHECK-1`、`U4-REVISE`、`U4-SAVE-2` |

## 冷讀判定

- `test_cold_follow_contract.py`：PASS
- `test_ui_practicality_contract.py`：PASS
- 四頁 teaching evidence：0 finding
- 四頁 copy continuity：0 warning；工具仍要求 human review，故不把 heuristic 直接升格為真人通關。

## 人工冷跟做腳本

真人驗證時，請每單元只發：對應 HTML、該頁列出的核心素材與一個可保存文字位置；記錄學員是否能在不口頭補充的情況下完成第一個可觀察結果，再讓學員完成核心產物。若停住，優先回到契約中的「起始材料／第一個動作／失敗回復」欄位，不補寫第二套說明。
