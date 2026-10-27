# ACP After Effects 素材與驗證計畫

## Gate 原則

素材名稱出現在講義前，實際檔案必須存在、可下載、可在指定版本開啟，並說明第一次使用時機與用途。空白檔、教師電腦上的私人路徑或「稍後提供」不算可取得素材。

目前專案只有參考 PDF、題庫簡報與研習申請表，沒有學員可用的 `.aep`、圖片、影片、音訊、字型包或完成版工程。因此所有需要指定起始狀態的操作實作維持 `BLOCKED`。

## 必要資產

| 資產 ID | 建議交付路徑 | 用途與第一次使用 | 必要內容 | 驗證方式 | 狀態 |
|---|---|---|---|---|---|
| PRE-01 | `assets/downloads/acp-ae-preflight.zip` | 課前診斷 | 可開啟 `.aep`、一張圖片、一段短影片、Relink 練習 | 開檔、播放、另存、Relink 全部成功 | BLOCKED |
| CH1-BASE | `assets/downloads/acp-ae-foundations.zip` | CH1-1 至 CH1-5 | 自製背景、Logo、文字規格、Shape 參考、短音訊、輸出規格卡 | 每單元從乾淨副本重跑 | BLOCKED |
| PRAC1-S | `assets/downloads/acp-ae-prac1-starter.zip` | PRAC1 開始前 | 起始工程、授權素材、完成預覽、驗收表 | 冷啟動後 30 分鐘內可完成主路徑 | BLOCKED |
| PRAC1-C | `assets/downloads/acp-ae-prac1-complete.zip` | PRAC1 訂正 | 完成版 `.aep`、預覽輸出、圖層結構說明 | 與驗收表逐項一致，無離線素材 | BLOCKED |
| OPS-A | `assets/downloads/acp-ae-ops-01-13.zip` | CH3-1 | 題 1、7、10 起始工程與復原點 | 三題各自可重設，不互相污染 | BLOCKED |
| OPS-B | `assets/downloads/acp-ae-ops-14-27.zip` | CH3-2 | 題 14、17、27 起始工程與復原點 | Time Remap、Parent、Effect 動畫可重跑 | BLOCKED |
| OPS-C | `assets/downloads/acp-ae-ops-28-40.zip` | CH3-3 | 題 29、38、40 起始工程與復原點 | 輸出、Transform、Matte 可重跑 | BLOCKED |
| Q-CARDS | `assets/downloads/acp-ae-question-cards.pdf` | Part 2 與 Part 3 | 13 題判斷表、40 題操作卡、答案與版本欄 | 題號、能力與講義錨點一致 | 待產製 |
| RECOVERY | `assets/downloads/acp-ae-recovery-cards.pdf` | 第一次發生錯誤前 | 面板復位、離線素材、錯圖層、多餘 Keyframe、輸出錯誤 | 使用錯誤工程逐張測試 | 待產製 |

## 自製素材規格

### 六秒標題動畫

- 畫布：1920 × 1080，29.97 fps，6 秒。
- 圖層：背景、Logo 或 Shape、主標題、副標題、Adjustment Layer、音訊。
- 動畫：Position、Scale 或 Rotation 至少兩種；Opacity 淡出；Easy Ease。
- 合成：Mask 或 Track Matte 擇一；一項可動畫化 Effect。
- 輸出：課堂使用短預覽格式；完成版另保留可檢查的 Render Queue 設定。

### 代表題工程

- 每題有 `START`、`CHECKPOINT`、`COMPLETE` 三種工程狀態。
- 圖層名稱使用題目卡中的名稱，避免講義與工程不一致。
- 每題只放完成任務所需素材，降低零基礎學員尋找負擔。
- 題目完成後留下至少一個可截圖的屬性、設定或時間軸證據。
- 不把原參考書配套工程假設成已取得；代表題使用合法自製素材重建同能力條件。

## 授權 Gate

| 項目 | 需確認內容 | 未確認時的處理 |
|---|---|---|
| 原書題目文字 | 課堂投影、講義引用與完整重製範圍 | 學員版改寫成自製同能力題目 |
| 原書截圖 | 可裁切、標註與發送給學員的範圍 | 只保留教師研究用途，學員版使用自製 AE 畫面 |
| 簡報內容 | 是否可作學員下載材料 | 先作講師示範底稿，不提供下載 |
| 圖片與影片 | 商用、教育使用與再散布條件 | 使用 CC0、自製或取得明確授權的替代素材 |
| 字型與音訊 | 教室安裝與素材包再散布權 | 使用系統字型與可再散布音訊 |

## 平台驗證矩陣

開課前 14 天在實際授課環境填寫：

| 項目 | 驗證紀錄 |
|---|---|
| AE 完整版本 | 待填 |
| 作業系統與版本 | 待填 |
| 顯示語言 | 待填 |
| GPU 與記憶體條件 | 待填 |
| 一人一機或共用方式 | 待填 |
| 代表題 1、7、10 | 待重跑 |
| 代表題 14、17、27 | 待重跑 |
| 代表題 29、38、40 | 待重跑 |
| Render Queue 與輸出權限 | 待重跑 |
| 素材解壓縮與寫入權限 | 待重跑 |

## 每題驗證紀錄格式

| 欄位 | 內容 |
|---|---|
| 題號與能力 | 例如 Q14 Time Remapping 停格 |
| 起始工程 | 檔名、hash、AE 版本 |
| 起始狀態 | 圖層、時間、既有 Keyframe 與必要素材 |
| 操作路徑 | 選單、面板、屬性與快捷鍵；記錄 Windows／macOS 差異 |
| 完成狀態 | 畫面、值、時間軸與輸出證據 |
| 復原測試 | 錯誤現象、Undo 或重設位置、重跑起點 |
| 結論 | PLATFORM_VERIFIED 或 BLOCKED，附日期與執行者 |

## 放行順序

1. 確認授課版本、作業系統與一人一機條件。
2. 確認題目與截圖授權範圍。
3. 製作 CH1 基礎素材與 PRAC1 起始／完成版。
4. 製作 9 題代表工程與復原點。
5. 在授課環境逐題重跑並保存證據。
6. 依已驗證工程撰寫正式學員正文。
7. 做內容審查、HTML 轉製、真人冷讀與完整跟做。
