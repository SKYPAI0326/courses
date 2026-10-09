# 既有 AI 秘書藍圖：講師延伸範例

講師提供的五份 Make 藍圖已有完整的逐步進階設計，本課不用重新製作相同的 AI 秘書流程。下表依原始 JSON 的模組結構整理；原檔保留在講師自己的資料夾，不隨學員講義附上。

| 原有檔案 | 流程重點 | 建議使用時機 |
|---|---|---|
| `00_AI秘書_邏輯.blueprint.json` | Webhook → Router → Gmail／Telegram | 講師示範事件與分支的概念 |
| `01_AI 秘書_雛形.blueprint.json` | Gmail新信 → Gemini → JSON解析 → Router → Telegram／Gmail／Google Docs | 學員完成本課分流主線後，觀察AI如何接上輸入與輸出 |
| `02_AI秘書_基礎.blueprint.json` | Gmail搜尋 → 彙整 → Gemini → JSON解析 → 分流 → Gmail | 延伸練習批次彙整與信件回覆 |
| `03_AI秘書_進階.blueprint.json` | 在批次流程加入Telegram、Google Docs與HTTP | 跨工具進階課，不列入零基礎必做 |
| `04_AI秘書_信件彙報.blueprint.json` | Gmail搜尋 → 文字彙整 → Gemini → Gmail寄送 | 延伸練習信件摘要與彙報 |

這五份原檔含原帳號的連線參照，且部分分支會寄信或傳送 Telegram 訊息。講師示範時應先複製並去識別、改用虛構測試資料與自己的收件位置，確認排程停用及每個輸出模組的對象，再逐一試跑。尚未完成這些檢查時，只展示結構，不把原檔交給學員匯入。

本課 Part 5 的必做成果仍用[人工覆核後分流 Blueprint](reference-make-blueprint.json)：先學新列、Filter、防重、Router、紀錄與未寄出草稿，再由講師帶看 AI 秘書進階範例。兩條流程的輸入與風險不同，驗收證據不可互相代替。
