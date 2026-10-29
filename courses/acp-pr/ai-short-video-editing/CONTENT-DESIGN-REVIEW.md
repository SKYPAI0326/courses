# ACP Premiere 證照基礎與 AI 輔助剪輯：內容設計審查

審查日期：2026-10-24

## 結論

[UPDATE 2026-10-24] 新版內容、固定素材、8 份正式網頁講義與課程首頁已完成。核心操作已在 Windows Premiere Pro 26.0.0 Build 72 實機重跑；這不等於 Premiere Pro 2024 介面完全相同，也不取代零基礎真人跟做。正式狀態為 `MACHINE_READY_PENDING_HUMAN`，尚未達到 `HUMAN_READY`。

## 敘事主線

新版只有一條主線：先理解 Premiere 的物件與介面，學會時間軸基本操作，再建立題庫功能地圖與讀題方法；完成證照共同基礎後，才進入一條縮短的 AI 工作流，最後把 AI 建議重新翻成 Premiere 的可執行、可驗證狀態。

這條主線對應使用者確認的優先序：證照考試是核心，AI 是重要但不能反客為主的延伸。

## 時數審查

| 區塊 | 單元 | 分鐘 |
|---|---|---:|
| 證照共同基礎 | CH0-1～CH0-4 | 180 |
| AI 輔助剪輯 | CH1-1～CH1-4 | 100 |
| 休息 | 兩次 | 20 |
| 合計 |  | 300 |

比例為教學時間的 64.3% 用於 Premiere／證照共同基礎、35.7% 用於 AI 輔助剪輯。這比舊版把大部分時間放在 AI 產物與成片更符合第二天題庫與考試需求。

## 題庫對齊

現行 77 頁簡報顯示，考查範圍分布在專案與素材、序列與軌道、時間軸剪輯、Properties／Effect Controls、音訊、文字字幕、色彩效果、輸出與封存。新版 CH0-3 用七個功能家族建立導航，CH0-4 用作用物件、動作、功能位置、目標狀態、限制與驗證拆題。

設計刻意沒有在 5 小時內重講 B01–B42：詳細指定專案、數值、路徑與評分條件仍留給後續 4 小時題庫講解。這可避免重複，也保留零基礎學員先建立架構的認知空間。

已移除的舊版 B08、B09、B19 沒有被列回大綱或教案。

## AI 比重審查

AI 段從舊版的多工具、多產物流程，縮成一條 100 分鐘主線：

1. 語音轉文字或使用同版本 SRT。
2. AI 提出精華與順序候選。
3. 人工核對原意、時間碼、長度與可執行性。
4. Premiere 完成 20–30 秒迷你短片。
5. 記錄一項採納與一項修改或拒絕。

Clipchamp 停頓比較、85 分鐘完整 45–60 秒成片、B-roll、音樂與多層二次 AI 審查不再是必要主線。這些內容不是錯誤，但在 5 小時且證照優先的條件下會排擠基礎，因此已從正式單元移除；舊內容保存在備份中。

## 零基礎可學性

- CH0-1 先區分原始媒體、Project item、source clip、sequence 與 timeline clip，避免把操作名稱直接丟給新手。
- CH0-2 每組操作都用「改變位置、長度、速度或後方內容」比較結果，並保留副本與 Undo 路徑。
- CH0-3 只實做三組代表任務，其餘以定位與問答完成，降低 60 分鐘內的操作負荷。
- CH0-4 先分析作用物件與限制，再找路徑，避免死背介面。
- AI 段固定 fallback，不讓登入、模型下載或服務失效阻斷教學成果。

## 交付與評量

新版的核心證據不是單一成片，而是五件相互對照的成果：

- `foundation-check-v1.md`
- `practice-cut-v1.mp4`
- `decision-table-v1.csv`
- `decision-tradeoff-log-v1.md`
- `ai-mini-cut-v1.mp4`

這些成果可分別證明找功能、基本操作、AI 候選、人工判斷與實際成片；避免只看一支漂亮影片卻無法確認學員是否理解 Premiere 或 AI 取捨。

## 靜態驗證結果

- 8 個單元，教學時間 280 分鐘，結構驗證 0 errors。
- prerequisite 全部有效且只指向先前單元。
- 8 份教案皆有 learner-content start／end 邊界。
- 8 份教案的 copy continuity audit 均為 0 warnings。
- 正式課程目錄不再含 CH2-1、CH2-2、CH2-3；舊版已移到可回復備份。

## 阻塞與風險

- **RESOLVED：固定素材缺失。** 基礎媒體、時間碼答案、概念圖、功能地圖、SRT、固定 AI 候選與參考成片已建立；規格與證據見 `assets/ai-short-video-editing/asset-manifest.json`。
- **RESOLVED WITH VERSION LIMIT：Windows 實機路徑。** CH0-1、CH0-2、CH0-3、CH1-1、CH1-3 已在 Premiere Pro 26.0.0 Build 72 通過；Premiere Pro 2024 介面差異仍須依面板名稱與可觀察結果處理。
- **NON-BLOCKING DECISION：AI 服務未定版。** 核准服務與登入仍須決定；固定候選已能完成同一學習成果，因此不再阻塞試跑。
- **BLOCK：無零基礎 cold follow-along。** 靜態規則通過不能證明節奏真的適合完全新手。
- **STALE：Word 大綱。** `AI短影音剪輯實戰-課程大綱.docx` 仍是舊 2 小時版本。

## 來源 SHA-256

```text
8eff373a1a87354cbf1df2efbb733bff50fd12fb0602f903f45ccb7a42f84f9e  _outlines/ai-short-video-editing.md
54157b9ee081c694e41504449cf721dd13f0c9758a1fd2ae1308ed2401665c0d  _outlines/ai-short-video-editing.style-guide.md
608e524555f07d3233afe8fcb837bff5fee71ad820dd5439fc8757327757e5b4  _lessons/ai-short-video-editing/CH0-1.md
c3a32bea1af7f5b24419e6719f90e94d2c084b49499147c92816015bf2c7dcee  _lessons/ai-short-video-editing/CH0-2.md
b85fed556552db8e1e74dd5b8534eecdb88d99b073b6b4397a9739f88b57a6f1  _lessons/ai-short-video-editing/CH0-3.md
d91432ce62eb2f008bb8064aa80493dcf58d0bf52b0265b06f2df4e3683ecb0d  _lessons/ai-short-video-editing/CH0-4.md
a1dd90bb37bf6eb35e2ab3b1fc36b92563d78345a8c0bf72ca5fd94ab53a372e  _lessons/ai-short-video-editing/CH1-1.md
bf0c5a94b2f3dc1b8825cd1732e245af3e4f78875d886c8f044f8de0f38fb77f  _lessons/ai-short-video-editing/CH1-2.md
830f8f6c4c0776420837fd07058dba45416a9f202eda06a62d6d86d6ceb82850  _lessons/ai-short-video-editing/CH1-3.md
64876c3cf7b35686df154bf76c9afbe68f9ccd41a37bc31a45e477602ce785f4  _lessons/ai-short-video-editing/CH1-4.md
```
