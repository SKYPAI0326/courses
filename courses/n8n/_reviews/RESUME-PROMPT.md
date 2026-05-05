# n8n Classroom Pack 恢復 Prompt（兩個版本）

任何時候要恢復這份工作（不論在 Claude Code 還是 Claude Desktop），複製對應 prompt 整段貼上即可。**不要用「繼續 lite pack」這種短觸發詞**——新 session 的 AI 不會自動找檔案。

---

## 版本 A：給 Claude Code 新 session

適用：在終端機 cd 到 `~/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/` 後跑 `claude`。

```
請讀以下三個檔案恢復 n8n classroom pack 設計工作的脈絡：

1. courses/n8n/_reviews/session-standby-2026-05-04.md（當前狀態 + 12 連發卡關清單 + 已產出檔案 + 下一步計畫）
2. courses/n8n/_reviews/lite-pack-cli-verify.html（全鏈路驗證頁，含 Phase A/B/C 完整動線）
3. courses/n8n/_reviews/n8n-credentials-api-research-2026-05-02.md（CLI 自動化研究報告，含 GitHub schema 驗證）

讀完三份後，告訴我：
(a) 當前卡在哪一步
(b) 立即可做的下一步是什麼
(c) Phase C step 5 通過後還有哪些工作要做

我會接著告訴你我在 Claude Desktop 那邊跑出的結果（Phase C 是否通過），然後我們繼續推進 7 個 workflow JSON / setup-wizard 補完 / Lite Pack 收尾。

關鍵環境變數（Phase C 用）：
- Docker container 名：n8n-starter-kit-n8n-1
- 課程專案路徑：courses/n8n/
- Lite pack 開發路徑：courses/n8n/assets/n8n-lite-pack/

哲學原則（不要違反）：
- 商業培訓學員要結果不要原理 → 設計優先序：能落地 > 提供原理
- 禁止給學員 patch 指令（重下 + 雙擊 為唯一允許指引）
- 課程指令禁用 heredoc 與長 echo（終端機 paste 會斷行）
```

---

## 版本 B：給 Claude Desktop 新對話

適用：Claude Desktop 沒有檔案讀取權，所有 context 必須 inline 在 prompt 內。

```
我正在驗證一個 n8n classroom pack 設計（讓商業培訓學員下載即用，
不需學原理）。當前在 Claude Desktop 是為了截圖記錄驗證過程。

【背景脈絡】
- 課程：n8n「AI 資料工廠」，學員是行銷企劃 / 營運 / 知識工作者，
  不是工程師。設計哲學「能落地 > 提供原理」，學員要結果。
- 連發 12 個學員實測卡關（zip 不存在 → port 衝突 → Cloudflare 綁卡
  → QUIC 被擋 → n8n credentials schema id 欄位 NOT NULL → 終端機 paste 斷行）
- 三層 classroom pack 設計：Lite Pack 30 分鐘必成 / Google Pack OAuth /
  原理文件（折疊給有心學員）

【當下卡關（Phase C step 5）】
我用 docker exec 跑 n8n import:credentials 報「Bad control character in
string literal at position 196」。根因是貼上的長 echo 指令被終端機斷成
2 行，JSON 字串內含實際換行字元。

【Claude Code 給我的立即解（5 行極簡，每行 ≤95 字元）】
echo '[{"id":"t1","name":"Test1","type":"httpHeaderAuth","data":{"name":"x-api-key","value":"k1"}}]' > /tmp/c.json
cat /tmp/c.json
docker cp /tmp/c.json $CONTAINER:/tmp/c.json
docker exec -u node $CONTAINER n8n import:credentials --input=/tmp/c.json
docker exec -u node $CONTAINER n8n list:credentials | grep Test1

預期看到 Successfully imported 1 credentials. + Test1 出現在 list。

【$CONTAINER 變數】n8n-starter-kit-n8n-1

【請協助】
1. 不要寫新指令——我用 Claude Code 那邊給的 5 行
2. 解讀我貼回來的截圖 / 終端機輸出
3. 如果 import 成功 → 告訴我「Phase C 通過 = setup-wizard v0.2 可行」
4. 如果 import 失敗 → 分析錯誤訊息可能原因

我接下來會貼終端機截圖給你。
```

---

## 使用流程

### 場景 1：晚點回 Claude Code 繼續

1. cd 到課程專案目錄：
   ```bash
   cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/
   claude
   ```
2. 開啟 `courses/n8n/_reviews/RESUME-PROMPT.md`，複製「**版本 A**」整段貼到新 session

### 場景 2：去 Claude Desktop 截圖記錄

1. 打開 Claude Desktop
2. 開啟 `courses/n8n/_reviews/RESUME-PROMPT.md`，複製「**版本 B**」整段貼到新對話
3. 開始截圖

### 場景 3：手機 / 其他裝置

複製版本 B（self-contained，含所有必要 context）。

---

## 為什麼短觸發詞行不通

我之前寫「繼續 lite pack 驗證」這種觸發詞，假設了 AI 會自動：

- 找到對應的 status 檔案（不會，新 session 沒有 memory）
- 知道是哪個專案的 lite pack（vault 內可能有多個）
- 推測當下卡在哪（不知道）

正確設計：把所有恢復需要的資訊放在**一份完整 prompt** 裡，使用者複製貼上 = 立即接續。檔案路徑就是 prompt 的「持久化」（永遠在固定位置可拿）。
