# 個人 Gamma 提案演練素材入口

你要把一份完整企劃轉為主管能閱讀與核准的十頁簡報。每人選自己的素材、操作與保存，不需要共同企劃或同學成果。建議預留九十至一百二十分鐘；工具登入與素材準備先完成。

先開啟 [實際成品預覽](examples/README.md)，看一份十頁 PDF 的封面與核准頁，再選自己的企劃。初稿與修訂成品分開提供，方便回查模型如何改變內容。

## 先選一份完整企劃

| 選擇 | 第一次要開啟的材料 | 適合用途 | 後續參考 |
|---|---|---|---|
| A 報表改善 | [case-a/proposal.md](case-a/proposal.md)，完整企劃 Markdown | 業務、財務、報表與主管提案 | [10頁來源對照](case-a/outline-reference.md)、[貼入參考文字](case-a/gamma-text.txt) |
| B 文件交接 | [case-b/proposal.md](case-b/proposal.md)，完整企劃 Markdown | 行政、教育、服務、人資與文件交接 | [10頁來源對照](case-b/outline-reference.md)、[貼入參考文字](case-b/gamma-text.txt) |
| 自己的企劃 | 開啟自己的完整文字檔，先確認讀者、方法、資源、時程與核准事項 | 已有現成工作企劃者 | 缺件先補，或改選 A／B；不套用模擬資料作自己的事實 |

A、B 均為教學模擬、尚未執行。兩份企劃已包含本演練所需資訊；A 的原始 CSV 只供追溯，不要求先做 Excel 分析。B 的真實單位文件是核准後要取得的材料，不是本次簡報的前置條件。

## 操作時依序取用

1. 複製 [outline.txt](prompts/outline.txt)，接上所選企劃全文，交給你正在使用的 LLM。保存自己的十頁大綱，再用所選案例的來源對照檢查。
2. 複製 [gamma-text.txt](prompts/gamma-text.txt)，接上已核對大綱，整理成十段正式簡報文字。
3. 在 Gamma 使用 [gamma-generate.txt](prompts/gamma-generate.txt) 與十段文字；確認生成前大綱有十張卡片後再生成。
4. 修訂自己的簡報，依 [quick-check.md](checks/quick-check.md) 檢查、匯出全部卡片，重新開啟 PDF。

完整操作與錯誤恢復見 [PRAC2-1-LESSON-PLAN.md](../../../PRAC2-1-LESSON-PLAN.md) 的學員正文。先讀開頭與示範，再開始自己的操作。

Markdown（`.md`）與純文字（`.txt`）可用文字編輯器開啟，複製內容到工具；格式沒有顯示時仍可讀取文字。若無法複製來源全文，先下載檔案再開啟。工具不可用時保留自己的企劃與大綱，Gamma 成品列待補。

## 來源與成品身分

案例 A 改編自 2026-10-07 隔離包，原文快照與雜湊保存於本課 `_sources/2026-10-07-practical-expansion/`。案例 B 為本課新製作的模擬企劃。兩組 `outline-reference.md` 與 `gamma-text.txt` 都是作者整理的參考，不代表學員已操作或特定 LLM 已成功。

實際試跑與 Gamma 匯出檔另存於本課 `_validation/gamma-2026-10-07/`；測試狀態以驗證紀錄為準，不將參考與試跑成品混為同一證據。
