# L5 模擬學員與流程機制驗證報告

**日期**：2026-09-16
**課程**：ai-beginner-practical
**驗證方式**：4 個獨立 Agent 平行唯讀檢核
**本次結論**：`BLOCKED / PROXY_ONLY`，不可宣稱正式上線

## 本次分派

| 角色 | 驗證範圍 | 結果 |
|---|---|---|
| 零基礎模擬學員 | 從 `index.html` 走到四個單元與課後整合 | `BLOCKED` |
| 內容實質 Reviewer | 課程正文、worked example、可跟做性、素材可發現性 | `BLOCK` |
| Learner Agent 機制驗證 | manifest、hash、頁面證據邊界、L5 產出契約 | `PROXY_ONLY` |
| 課程驗收與流程整合 | G1–G5、skills 串接、上線條件 | `BLOCKED` |

## 已確認

- 四個單元頁不是單純投影片，均有操作步驟、部分示範、checkpoint 與錯誤恢復內容。
- 6 個頁面與 19 個學員素材的 manifest 證據完整，頁面與素材 hash 相符。
- 頁面內部連結目前可找到，未發現 broken link。
- 課程具有從設計、教案、HTML、learner-agent 到 Gate 的基本流程骨架。

## 主要阻塞

### P0：零基礎學員無法穩定開始

1. 密碼關卡沒有提供取得密碼、申請授權或遺失密碼路徑。若密碼採課前另行發送，入口需明確說明；若要求完全自學，這是 BLOCKER。
2. CH1、CH2、CH4 只寫「開啟可輸入文字的 LLM」，沒有通用的登入、無帳號替代、第一個畫面與送出方式。
3. CH3 需要 NotebookLM 實際帳號與權限，但沒有完整的準備路徑；離線備援不能取代正式引用驗收。

### P1：內容完成物與流程閉環不足

1. CH1 的單一變因修訂缺少完整第二版輸出。
2. CH2 的 LINE 訊息與三版自我介紹缺少完整 worked output。
3. CH3 目前只有人工段落編號示例，沒有可觀察的 NotebookLM 點擊引用證據。
4. CH4 的冷氣比較與京都修訂缺少完整結果表格。
5. CH3 離線備援的 500 字要求，與正式路徑 300–350 字規格不一致。
6. 課後整合尚未明確列出 CH1–CH4 完成物、必取欄位、進入條件、回修位置與最終交付格式。
7. CH4 頁尾缺少直接前往課後整合的連結。

### P1：驗證機制本身仍是代理驗證

- manifest 已能固定實際 HTML 與素材版本，但目前主要是提示詞約束，沒有執行層強制 Agent 只能讀 learner-facing 內容。
- 素材紀錄只有 `path + sha256`，缺少來源頁面、連結位置與段落錨點。
- manifest 內含完整 `visible_text`，存在 Agent 只讀 manifest、未重新開啟頁面的風險。
- 尚無三 persona 的實際 L5 結果、完成物、分數與回頭使用率。

### 流程與 SSOT

- course-designer、builder、reviewer、validator 使用的內容實質與 learner action 規範路徑需正式統一，避免不同 Agent 讀到不同替代檔案。
- 最新驗證紀錄仍缺完整 L0、L4a、L4b、L5 與 FINAL-REPORT 閉環。
- G4 的 sitemap／course-ops 狀態需重新確認；本次模擬未把靜態通過誤當成正式發布通過。

## 建議的自我優化循環

1. 先修 P0：入口授權說明、通用 LLM 起始路徑、NotebookLM 準備與備援界線。
2. 補齊 P1 worked examples 與課後整合產物鏈。
3. 將 manifest 增加 `source_pages`、section anchor 與不寫回的 `--check` 模式。
4. 重新產生 manifest，執行三 persona L5；每個 persona 必須引用實際頁面與素材證據。
5. 執行 NotebookLM 實機 sentinel；若環境允許，再執行 L4a 外部案例測試。
6. 只有 G3、G4、L4a、L4b、L5 全部具備可追溯證據後，才更新 FINAL-REPORT、部署並做線上 smoke check。

## 驗證邊界

本次 Agent 全程唯讀，沒有修改課程頁面、教案或既有素材。模擬學員結果可用來發現自學阻塞，但不能取代真人學員、NotebookLM 實機引用或外部模型案例測試。
