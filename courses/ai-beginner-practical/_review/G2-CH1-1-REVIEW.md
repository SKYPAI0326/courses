# G2 Review：CH1-1 代表單元

**reviewed_at**：2026-09-14
**reviewer**：Codex
**status**：CONDITIONAL
**target**：`CH1-1-LESSON-PLAN.md`、`CH1-1.html`

## Evidence summary

- 完成物與起始狀態：`CH1-1.html:60-69`
- 白話概念與完整五欄示例：`CH1-1.html:74-86`
- 完整示範含模糊輸入、改寫提示詞、表格輸出與判斷理由：`CH1-1.html:91-101`
- 8 個同步演練階段與 2 個 checkpoint：`CH1-1.html:106-125`
- 完成驗證與通過標準：`CH1-1.html:130-136`
- 核心素材在首次使用前可取得，且有離線備援：`CH1-1.html:63-65,141-144`
- 常見錯誤與兩題自我檢核：`CH1-1.html:148-160`
- `python3 docs/lint-page.py courses/ai-beginner-practical/CH1-1.html`：0 BLOCKER、0 ERROR、0 WARN
- `python3 docs/lint-page.py courses/ai-beginner-practical/module1.html`：0 BLOCKER、0 ERROR、0 WARN

## Issue list

### MAJOR

1. **[Release readiness] 代表頁尚未完成使用者冷跟做**
   - **位置**：`_gates.md` G3
   - **問題**：靜態檢查只能證明結構與連結存在，還不能證明零基礎讀者能在三分鐘內找到材料、第一個動作、預期結果與修復位置。
   - **建議**：由使用者只拿 `CH1-1.html` 與兩份資產進行三分鐘冷跟做，將結果回填 G3；在此之前不批次產製後三頁。

2. **[Release readiness] 目前沒有中央課程入口註冊**
   - **位置**：`courses/index.html`、中央課程清單
   - **問題**：新課程尚未加入正式入口與註冊流程；這不影響代表頁預覽，但不能視為已上線。
   - **建議**：四頁與素材完成、G5 通過後，再由 course-register／course-ops 處理入口、索引與部署。

### MINOR

3. **[Content scope] CH1-1 的「即時資訊」目前以提示詞要求查明時間與依據呈現**
   - **位置**：`CH1-1.html:113`
   - **問題**：不同 LLM 的即時資料能力可能不同，實際回答不會一致。
   - **建議**：正式課前保留一個課堂當日的實機示例；頁面目前的「能取得或明確說明無法取得」判準可保留。

## Verdict

代表頁內容與靜態結構可進入使用者冷跟做，但尚未達到 G3 PASS，也不代表整門 12 小時課程完成。後續單元尚未製作，中央課程註冊與 G5 真跑驗收保持未開始。
