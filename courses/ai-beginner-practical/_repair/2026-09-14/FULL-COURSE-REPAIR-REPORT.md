# AI 入門即戰力｜全課檢視與修正報告

日期：2026-09-14  
範圍：`CH1-1.html`、`CH2-1.html`、`CH3-1.html`、`CH4-1.html`、`module1.html`，四份 lesson plan、課程藍圖與學員素材。

## 結論

四個內容單元原先都能看到操作骨架，但學員單獨閱讀時會在「可編輯完成物、共同練習素材、平台入口、前後版本契約」處中斷，因此全課基線判定為 BLOCK。本次已完成跨單元修正，讓每個單元都有：起始材料、第一個操作結果、可直接複製的輸入、預期結果、快速檢查、卡住時的回復路徑與可保存的完成物。

版面沿用既有 2026-09-14 layout redesign；本次只補內容與學員路徑，不改回先前已確認的視覺系統。

## 修正內容

### CH1｜LLM 基礎操作

- 工作表改成「複製到自己的文字／Markdown 編輯器，再另存為 `unit1-practice-sheet-complete.md`」的可執行路徑，原始素材不被覆寫。
- 補上個人生活／工作問題的 Solo 練習：模糊版 → 至少三個條件與輸出格式 → 只改一個條件。
- 同步 HTML、教案、工作表的五題、五項通知資訊、五欄檢查與完成檔名。
- 天氣等即時問題增加保留第一版、記錄資料限制與安全停止點。

### CH2｜日常文書

- 統一完成物為 `unit2-communication-pack-complete.md`。
- Email、訊息、自我介紹三類都要求保存實際提示詞與第一版；至少兩份迭代，其中一份必須是 Email。
- 修正示範輸出，保留原始背景的價格、交付內容與開始時間，避免示範自行改動輸入事實。
- 自我介紹改為學員先自行判斷讀者／場合／目的，再用檢查表對照。

### CH3｜NotebookLM 閱讀實務

- 補上固定平台官方入口：`https://notebooklm.google.com/`。
- 明確拆成課堂必做 3 份來源（新聞、公告、書籍節錄）與 6 份課後延伸來源。
- 補上離線文字備援的直接連結與限制：備援可練習，但不會產生 NotebookLM 正式引用，恢復後需重跑。
- 統一新聞摘要為一句話、約 200 字、約 300–350 字；同步教師示範、HTML、教案與工作表。
- 將公告白話卡、書籍行動筆記改為獨立操作步驟，並要求各欄／各重點保留正式引用。
- 區分講義手寫段落編號與 NotebookLM 正式可點擊引用，避免學員誤把示範編號當成引用。
- 完成物統一為 `unit3-notebooklm-reading-pack-complete.md`，保存後重新開啟確認。

### CH4｜生活化應用

- 新增固定 Together 素材 `assets/datasets/unit4-air-conditioner-comparison.md`，避免學員找不到兩款冷氣比較資料。
- 新增可保存的 `assets/worksheets/unit4-lifestyle-application-card.md`，統一完成物為同名檔案。
- 京都示範補上教學用預算區間表，並明確標示非即時報價、機票未計入與需要人工確認的項目。
- 單一變因示範只改「每天主要景點上限」，保留其餘條件；轉移練習也固定同一張卡，只替換時間或預算其中一項。
- 健康與購物內容保留整理／比較／待確認位置，不替學員或專業人員做最後判定。

## 驗收證據

| 檢查 | 結果 |
|---|---|
| `python3 docs/lint-page.py courses/ai-beginner-practical/ --summary` | PASS：5 頁，0 BLOCKER、0 ERROR、0 WARN |
| 本機 `href`／`src` 連結 | PASS：68 條，0 缺漏 |
| CH1／CH2／CH4 平台中立 | PASS：未出現 ChatGPT、Gemini、Claude 學員操作 |
| 學員頁資安專題檢查 | PASS：未出現資安、身分證、銀行帳號、病歷內容 |
| NotebookLM 固定入口 | PASS：CH3 有官方入口與離線備援路徑 |
| CH4 提示詞資產 | PASS：30 張卡全部存在，新增共同冷氣素材 |
| 官方 validator preflight | PASS：23 PASS、0 FAIL、1 WARN（大綱檔名未被預設掃描器辨識） |
| 官方 validator L1–L3 | PASS：lint 全綠；L2/L3 因未指定關鍵字／找不到 `prompts-*.md` 而依規範跳過 |
| 搜尋索引 | PASS：已重新產生 `search-index.json`，666 筆 |

## 尚未宣告正式上線的項目

- 官方 validator 的 L0 尚未建立本課專用 `L0-generate.py`，目前為 `MANUAL_REQUIRED`。
- 官方 validator 的 L4a、L4b、L5 仍需依規範執行人工 consult／persona verdict；本次的三個學員視角 Agent 報告已納入修正依據，但不替代正式 gate。
- 尚未用真實外部 LLM 與 NotebookLM 帳號完成一次完整冷讀；NotebookLM 的實際引用顯示、登入狀態與當期介面仍需課前確認。
- 上述項目不影響本次檔案、內容、連結與頁面結構修正，但在完成真人試跑前，課程狀態應維持「可進入試跑」，不標記為最終發布。

## 回復方式

若要回到本次修正前的內容，執行：

```bash
bash ai-beginner-practical/_tools/restore-2026-09-14-pre-full-course-repair.sh
```

此腳本只回復本次備份列出的課程檔案，並移除本次新增的 CH4 兩份素材；既有其他備份與工作區未納入回復範圍。
