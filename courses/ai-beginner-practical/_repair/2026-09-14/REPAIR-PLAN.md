# Repair Plan: ai-beginner-practical

## Scope

- slug: ai-beginner-practical
- pages: CH1-1.html, module1.html
- learner materials: assets/worksheets/unit1-practice-sheet.md, assets/fallback/unit1-dialogue-simulator.md

## Risk

- near-term class: unknown
- backup required: yes
- no content deletion is planned

## BLOCKER

### [LEARNER_PATH] CH1-1.html:111

- 問題：第一步要求學員開啟文字型 LLM 對話畫面，但平台中立的起始方式不夠明確。
- 修法：把第一步改成「開啟你目前可使用的文字型 LLM 對話頁面」，並明確說明先使用工作表第 1 題；若暫時沒有可用工具，先依備援文件完成觀察，再於工具可用時重跑五題。
- 驗證：冷跟做者能說出第一個操作、第一份輸入與暫時不可用時的替代路徑。

## MAJOR

### [LEARNER_PATH] CH1-1.html:115,117

- 問題：U1-CHECK-1 在第 3 題晚餐操作前要求晚餐表格已存在。
- 修法：將 checkpoint 改成只檢查前兩題，並把「晚餐表格」移至下一個 checkpoint。
- 驗證：依頁面順序操作時，任何 checkpoint 都不要求尚未完成的成果。

### [ASSET_DISCOVERABILITY] unit1-practice-sheet.md

- 問題：第 2–5 題缺少完整回答保存欄位，完成物要求與實際工作表不一致。
- 修法：每題增加「完整回答貼在這裡」與「我判斷是否可用／理由」欄位；不刪除既有的重點觀察欄位。
- 驗證：學員能在同一份工作表保存五題原始提示詞、完整回答與判斷。

### [LEARNER_PATH] notice preservation

- 問題：通知素材含「下午 5 點再次公告」，頁面與工作表的必保留欄位未同步。
- 修法：統一保留五項資訊：週三晚上 7 點、下午 6 點前移車、雨天週四同一時間、下午 5 點再次公告、住戶需採取的行動。
- 驗證：頁面、工作表與備援文件的通知條件一致。

### [NAV_OPS] CH1-1.html, module1.html

- 問題：首頁相對連結多一層。
- 修法：將 ../../../index.html 改為 ../../index.html。
- 驗證：兩頁的首頁連結目標存在。

## Activity Identity Audit

本次只修 learner path、素材保存與導覽，不改變 Demo、Together、Solo 的素材、產物或學員決策；不新增重複活動。

## Shared Copy Audit

不刪除必要導覽文案；本次沒有需要合併的非必要共用段落。

## Follow-up findings added after second cold follow-along

- 工作表的修改區補上實際使用的指令、修改後完整回答／第二版與保留重點。
- 將「改成表格，只改變呈現格式，保留原本所有資訊」定義為單一格式變因。
- 離線備援擴充到五題，新增自我介紹、即時天氣與 ETF 的示例判讀；頁面同步說明五題備援範圍。
- 入口頁的課程級說明改為平台中立，NotebookLM 僅保留在第 3 單元固定平台說明。
- 入口頁與 CH1-1 的備援導語改為一致描述五題示例判讀，降低學員對照成本。
- 備援文件新增工作表題號對照表，讓五題與示例的對應不依賴文件排列順序。

## Execution Order

1. 已建立修復掃描與本計畫。
2. 已建立 scope 備份與 restore script。
3. 修補第一步、checkpoint、工作表欄位、通知必保留資訊與首頁連結。
4. 跑 HTML lint、連結與資產檢查、政策字詞掃描。
5. 重新執行六題冷跟做；若 BLOCK，再保留問題並不宣稱完成。
