# n8n Lite Pack · LLM 改寫教學專用版（clean）

> **本 zip 是教學用版本，不是生產用版本。**
>
> 給 post-llm 系列「用 LLM 改寫 workflow」教學使用。內含 5 個 walkthrough 用的代表 workflow，
> jsCode 已清掉版本標記、Bug 修補註解、Codex review 痕跡，學員把 JSON 貼給 LLM 改寫時，
> LLM 不會被歷史包袱誤導。

---

## 與生產版 lite-pack 的差異

| 項目 | 生產版 lite-pack | 教學版 lite-pack-clean |
|---|---|---|
| workflow 數量 | 14 個（完整使用情境） | 5 個（最具代表性的 walkthrough 範例） |
| sticky note | 「使用說明 only」（S1 後乾淨）| 同生產版（已乾淨） |
| jsCode 註解 | 含 LP helper 骨架說明（給 ops 看）| 加「BEGIN: 共用骨架 — 請勿修改」+「業務邏輯 — 改這裡」分隔 marker |
| LP helper 內版本 / Bug refs | 保留歷史脈絡 | 全清 |
| 內含 setup-wizard | 是 | **否**（教學版只供 LLM 改寫練習，不用真的 import 跑） |
| 內含 README + _change-log | 是 | 此 README + 不放 _change-log |
| 主用途 | 學員真實 import 跑 workflow | 學員學「用 LLM 改 workflow」六步流程的練習素材 |

---

## 內含 5 個 workflow

| 檔案 | 對應教學情境 |
|---|---|
| `02-pdf-ai-rename.json` | post-llm-6 walkthrough 主例（PDF 改名 → 發票處理）|
| `03-batch-error-recovery.json` | 學「批次處理 + 失敗分流」改寫範例 |
| `04-daily-ai-report.json` | 學「Switch by extension」分流 + Aggregate 範例 |
| `10-folder-organize.json` | 學「per-file fallback + dedup map」進階範例 |
| `12-knowledge-rag.json` | 學「RAG 索引 + webhook」範例（含 binary handler、tokenizer）|

---

## 怎麼用

### 情境 A：跟著 post-llm-6 walkthrough 改 #02

1. 解壓本 zip
2. 打開 `02-pdf-ai-rename.json` 用 VS Code 看
3. 找 `Code: 切 chunk + 組 JSONL` node 的 `jsCode` 欄位
4. 你會看到清晰的 marker：
   ```
   // BEGIN: 共用骨架 — 請勿修改這段
   ...
   // END: 共用骨架

   // 業務邏輯 — 改這裡（LLM 改寫時針對下方內容調整）
   const today = ...
   ```
5. 貼給 LLM 改寫時，告訴它「只改業務邏輯區段，骨架保留」

### 情境 B：把改寫好的 JSON import 回 n8n 試跑

1. **不要** import 本 zip 內的 workflow — 它們是教學素材，不該污染你的生產 n8n
2. 改寫好的 JSON 走標準流程：
   - n8n UI → Workflows → 點原本 workflow（如 02 · PDF AI 改名）→ ⋯ → Duplicate
   - Duplicate 後改名加 `-edit` 後綴
   - 在 -edit 版本上替換被改的節點
   - Execute 測試
3. 詳細流程見 post-llm-3「6 步真詳解」

### 情境 C：作為 LLM 改寫的 reference

如果你已經改寫好一份 workflow JSON 但不確定結構對不對，可以拿本 zip 內對應的 clean 版做 diff，確認你沒誤動骨架。

---

## 為何不直接用生產版做 LLM 改寫教學？

生產版 workflow JSON 內：
- jsCode 含「`// v1.3 (Bug #2): 用 helper 取代手動 base64 decode...`」這類修補註解
- 含「`// Lite Pack v1.2 · LLM Helper（共用骨架，下面業務邏輯維持原樣）`」這類版本標記
- 含「`// Codex 第二意見整合 ...`」這類 review 痕跡

LLM 看到這些註解會：
- 誤以為「v1.3 修了 Bug #2」是現在要做的事 → 亂改現代碼
- 把「共用骨架」當成可動範圍 → 砍掉 lpCall 換成自己的實作
- 學習到「workflow 應該保留所有歷史修補痕跡」的壞習慣

教學版砍掉這些，讓 LLM 看到「現在的程式碼」+ 清晰的可改 / 不可改 marker。

---

## 維護原則

本 zip 由 `n8n-lite-pack-source/build_lite_pack_clean.py` 從生產版 workflow 衍生產生。
**不要直接編輯本 zip 內的 workflow** — 改生產版（lite-pack/workflows/），重跑生產 script 即可重生。

如果生產版有重大結構變動（例如砍掉某個 workflow / 新增 walkthrough 場景），
記得同步更新本 zip 的 SELECTED 清單與本 README。
