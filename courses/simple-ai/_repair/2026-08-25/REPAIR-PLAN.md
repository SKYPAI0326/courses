# Repair Plan: simple-ai deliverables

日期：2026-08-25

## Scope

- slug：`simple-ai`
- 既有頁面：`CH2-1.html`、`module2.html`、`index.html`、`CH2-4.html`
- 新增來源：`handbook.html`、`quick-reference.html`
- 新增工具：`_tools/build-deliverables.js`
- 新增交付物：`assets/創業-AI-實戰手冊.pdf`、`assets/創業-AI-實戰-10則Prompt精選.pdf`
- 查證與報告：`PLATFORM-AUDIT.md`、`REPAIR-REPORT.md`
- 不修改：其他課程、`simple-ai` 其餘六個單元、既有 55 條 `prompt-library.html`

## Risk

- near-term class：unknown
- backup required：yes
- execution mode：單一 agent，A、B、C、D 各包完成後停止等待使用者驗收
- platform drift：NotebookLM／Gemini 手機功能必須在工作包 C 以官方資料與實際介面查證
- publication dependency：沒有已驗證公開網址時，不建立 QR Code

## BLOCKER

### [DELIVERABLE] 完整版 PDF 實檔缺失

- 問題：課程宣稱提供完整版 PDF，但 `simple-ai` 目前沒有可下載的 PDF 實檔。
- 修法：建立 `handbook.html` 與固定 PDF 建置腳本，輸出 55–65 頁正式 PDF。
- 驗證：`pdfinfo` 頁數、`pdftotext` 內容錨點、`pdftoppm` 逐頁視覺檢查。

### [DELIVERABLE] A4 雙面 Prompt 精華版缺失

- 問題：課程規格要求 A4 雙面 10 則 Prompt，但資料夾沒有來源檔或 PDF。
- 修法：建立 `quick-reference.html`，固定收錄 EF-08、EF-01、EF-02、EF-04、NB-01、TK-02、MK-01、MK-02、MK-03、CS-01。
- 驗證：`pdfinfo` 必須恰為 2 頁，`pdftotext` 必須找到全部 10 個代碼，彩色與灰階渲染均可讀。

## MAJOR

### [LEARNER_PATH] NotebookLM 與 Gemini 雙向流程缺失

- 問題：現有 CH2-1 有品牌知識庫教學，但沒有完整的 NotebookLM → Gemini → NotebookLM 來源查核閉環。
- 修法：加入三份完整來源、NotebookLM 輸出、Gemini 完整草稿、回送查核、修正成品、手機步驟及複製貼上備援。
- 驗證：完整範例八項契約、免費手機路徑、官方功能查證與 lint。

### [NAV_OPS] 尚未落地的 QR／Google Form 承諾

- 問題：`module2.html` 宣稱完整版 PDF QR Code；`CH2-4.html` 宣稱 QR 落地頁有 Google Form，但目前沒有對應實檔或已驗證網址。
- 修法：兩份 PDF 完成後改為真實相對下載連結；只有公開 URL 驗證成功才加入 QR。移除沒有證據的 Google Form 與逐一回覆承諾。
- 驗證：三入口頁連結、stale copy 搜尋、PDF 非空、三頁 lint。

## Complete Example Contract

每個核心範例必須具有：

1. 明確情境。
2. 可直接使用的完整素材。
3. 填妥的完整 Prompt。
4. 手機逐步操作。
5. 完整預期輸出。
6. 合格與不合格判讀。
7. 常見錯誤、原因與可執行修復。
8. 學員可保存或提交的完成證據。

核心案例只使用 Style Guide 已核准的咖啡館與手工皂創業者。其他產業只能作短篇臨演對照，不得形成第三條固定主線。

## Activity Identity Audit

| page / deliverable | section | role | material | artifact | path | learner decision | overlap verdict |
|---|---|---|---|---|---|---|---|
| handbook CH1-1 | AI 助理設定 | Together | 手工皂業務設定 | 個人化 AI 助理設定 | EF-08 → 確認 → 截圖 | 選擇語氣與禁用詞 | distinct |
| handbook CH1-2 | 會議處理 | Together | 手工皂兩角色逐字稿 | 摘要與三欄待辦 | EF-01 → 查日期 → 修正 | 判斷待確認資訊 | distinct |
| handbook CH1-3 | 報價與回信 | Together | 供應商報價 | 結構化表格與 Email | EF-02 → 核數字 → EF-04 | 選擇可寄出的語氣 | distinct |
| handbook CH2-1 | 品牌知識庫 | Together | 咖啡館三份來源 | 品牌摘要與來源查核 | NotebookLM → Gemini → NotebookLM | 刪除無依據敘述 | distinct |
| handbook CH2-2 | 品牌定位 | Solo | CH2-1 品牌摘要 | 三版定位與最終句 | TK-02 → 三問判讀 → 人工改寫 | 選擇最符合策略的版本 | distinct |
| handbook CH2-3 | 社群內容 | Solo | 已核准定位 | 七則骨架、標題與腳本 | MK-01 → MK-02 → MK-03 | 選擇發佈角度 | distinct |
| handbook CH2-4 | FAQ 與把關 | Solo | 真實常見問題 | 15 則 FAQ 與修正版 | CS-01 → 發佈三問 → 修正 | 判斷事實、個資與語氣 | distinct |

## Shared Copy Audit

| repeated copy | pages | allowed reason | action |
|---|---|---|---|
| 三條資安紅線 | handbook CH1-4、quick-reference 頁尾、CH2-4 檢查 | 課程級安全 checkpoint | 保留短版，其他章節不重複全文 |
| 十則精選 Prompt | handbook、quick-reference | 兩份正式交付物需一致 | 以 handbook 文字為來源，禁止另寫變體 |
| 雙向工作流 | CH2-1、handbook CH2-1、module2 | 詳細教學與導覽摘要用途不同 | CH2-1／handbook 放完整示範；module2 只放一句目標 |

## Execution Order

1. 建立備份與可執行還原腳本。
2. 工作包 A：完整版手冊 HTML、PDF、文字與逐頁渲染驗證；等待核准。
3. 工作包 B：A4 雙面精華版、彩色與灰階驗證；等待核准。
4. 工作包 C：平台查證、雙向完整示範、手冊同步；等待核准。
5. 工作包 D：三頁真實下載入口與 stale promise 清理；等待核准。
6. 整課 lint、search index、sitemap、冷啟動走讀與 `REPAIR-REPORT.md`。

## Stop Conditions

- 任何核心素材缺失：停止，不用敘事補洞。
- PDF 頁數不符或逐頁渲染第二次仍失敗：停止並回報。
- 手機免費版功能無法由官方資料或實際介面確認：採固定複製備援，不猜 UI。
- 正式公開網址不存在或不可讀：本輪只交付相對下載連結，QR 列為 remaining。
- 任一工作包未取得使用者核准：不得提前進入下一包。
