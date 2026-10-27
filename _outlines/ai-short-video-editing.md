---
slug: ai-short-video-editing
name: ACP Premiere 證照基礎與 AI 輔助剪輯
color: "#7a9ea3"
audience: 完全沒有 Premiere 操作經驗、第二天要進入 ACP Premiere 題庫講解與證照考試的學員
institution: 弄一下工作室
duration: 5h（300 分鐘，含兩次各 10 分鐘休息）
tools: Premiere Pro 2024、課前驗證的 WhisperDesktop 或 Subtitle Edit、校方核准的生成式 AI
prac: false
course_type: skill-operation
pilot: false
platform_version: Premiere Pro 2024；AI 與字幕工具依課前服務卡
---

## 課程定位（Positioning）

本課是 12 小時 ACP Premiere 課程中的前 5 小時。後續另有 4 小時題庫講解與 3 小時證照考試；因此本課的首要任務，是讓零基礎學員先建立 Premiere 的運作心智模型，能看懂題目在改什麼物件、到哪個面板或選單找功能、如何檢查操作後的狀態。

本課不逐題預教，也不要求先記住所有功能。180 分鐘建立專案、序列、素材、時間軸、效果控制、音訊、文字字幕、輸出與素材管理的功能地圖；100 分鐘讓學員體驗 AI 如何把逐字稿轉成可執行的剪輯決策，再回到 Premiere 完成一段短片。另有 20 分鐘休息。

## 受眾畫像（Audience Profile）

- **身分**：準備參加 ACP Premiere 證照課程與考試的大專校院學生或初階內容工作者。
- **技術底子**：完全沒有 Premiere 經驗；能在 Windows 開啟資料夾、另存檔案與使用瀏覽器。
- **近期任務**：第二天先理解題庫，再在指定環境完成證照考試。
- **主要風險**：只背答案卻不知道作用物件；看到陌生介面便失去定位；AI 示範過多而壓縮證照基礎。

## Brand Brief（品牌調性）

- **tone_register**：技術友善、考試導向但不死背。
- **mood_keywords**：看得懂、找得到、做得出、查得到。
- **differentiation**：以「物件 → 功能位置 → 目標狀態 → 驗證」建立可遷移的 Premiere 找路能力，再用一個短 AI 工作流展示現代剪輯方法。

## 學習成果（Outcomes）

完成 5 小時後，學員能：

1. 說明 Project、Source Monitor、Program Monitor、Timeline、Sequence 與原始媒體之間的關係。
2. 建立並儲存專案、匯入素材、建立序列，完成基本裁切、Ripple 補位、影音連結、軌道控制與 H.264 測試輸出。
3. 面對一段操作題文字，先辨認作用物件，再判斷應到面板、選單、工具列或時間軸尋找功能。
4. 辨認題庫常見功能家族：專案與媒體、序列與軌道、時間軸剪輯、效果控制與關鍵影格、音訊、文字字幕、輸出與封存。
5. 依題目的目標狀態自行完成操作後檢查，而不是只確認「按過某個按鈕」。
6. 使用預先驗證的語音辨識或教師提供的 SRT，取得含時間碼的逐字稿並修正關鍵錯字。
7. 用核准的生成式 AI 或教師固定候選建立剪輯決策表，人工核對原意、時間碼與可執行性。
8. 在 Premiere 依決策表完成 20–30 秒直式迷你短片，並說明一項採納與一項修改或拒絕的 AI 建議。

## 時數配置與邊界

| 區塊 | 教學時間 | 角色 |
|---|---:|---|
| Premiere／證照共同基礎 | 180 分鐘 | 主幹；建立第二天題庫所需的介面、物件、操作與驗證語言 |
| AI 輔助剪輯 | 100 分鐘 | 延伸；完成逐字稿、決策表與短片，保留人工判斷 |
| 休息 | 20 分鐘 | 兩次各 10 分鐘 |
| 合計 | 300 分鐘 | 5 小時 |

AI 不取代題庫講解，也不把考試變成生成式 AI 課。AI 段只保留一條可完成的主線：「語音轉文字 → AI 選段 → 人工核對 → Premiere 執行」。Premiere 仍是剪接、版面、字幕、聲音與輸出的執行環境。

## 前置知識依賴鏈（Prerequisite Chain）

```yaml
dependencies:
  CH0-1: []
  CH0-2: [CH0-1]
  CH0-3: [CH0-1, CH0-2]
  CH0-4: [CH0-3]
  CH1-1: [CH0-2]
  CH1-2: [CH1-1]
  CH1-3: [CH0-2, CH1-2]
  CH1-4: [CH0-4, CH1-3]
```

## 證照題庫銜接原則

現行教學來源為 77 頁的 `ACP_PR_修正版_移除舊版題目.pptx`。B08、B09、B19 已移除，不納入課程。題庫的詳細答案、指定專案與評分條件留在後續 4 小時逐題講解；本課只建立以下共通找路能力：

1. **先圈作用物件**：Project item、source clip、timeline clip、sequence、track、marker、caption 或 export file。
2. **再找功能位置**：Project panel、Source Monitor、Timeline、Effect Controls／Properties、Text、Effects、Lumetri、Export 或上方選單。
3. **翻成目標狀態**：名稱、起訖、軌道、數值、連結、可見性、輸出範圍或檔案格式。
4. **最後驗證限制**：是否不能留 gap、不能改 duration、不能刪來源、必須保留原序列或只能改單一 component。

## 試跑包交付規格（Verification Assets）

### 證照基礎主線

- `assets/ai-short-video-editing/premiere-foundation-starter/`：供學員從空白專案開始匯入的三段短影片、一段音訊、三張圖片與一個文字素材。
- `assets/ai-short-video-editing/print/premiere-workspace-map-v2.svg`：Project、Source Monitor、Program Monitor、Timeline、Effect Controls／Properties、Text、Effects、Export 的概念定位圖；不是 Premiere 實機截圖。
- `assets/ai-short-video-editing/object-panel-function-map-v1.pdf`：作用物件、常見動詞、功能位置與驗證方式對照表。
- `assets/ai-short-video-editing/foundation-practice-card-v1.md`：序列、Ripple、Insert／Overwrite、Link／Unlink、軌道、Keyframe、字幕與輸出的小型練習。
- `assets/ai-short-video-editing/question-decoding-card-v1.md`：題幹拆解六欄模板與四題判分依據。
- `assets/ai-short-video-editing/foundation-recovery-card-v1.md`：Undo、序列副本、Media Offline、工作區重設與找回面板。

### AI 延伸主線

- `assets/ai-short-video-editing/ai-demo/ai-short-video-demo-01.mp4`：120 秒中文口播、無個資且由本專案生成。
- `assets/ai-short-video-editing/ai-demo/ai-short-video-demo-01-raw-practice.srt`：含三個刻意錯誤的校正練習版。
- `assets/ai-short-video-editing/ai-demo/ai-short-video-demo-01-v1.srt`：同版本教師答案，作為轉錄工具不可用時的最終 fallback。
- `assets/ai-short-video-editing/transcript-check-card-v1.md`：人名、數字、否定詞與斷句抽查表。
- `assets/ai-short-video-editing/prompt-card.md`：固定輸入欄位與輸出格式。
- `assets/ai-short-video-editing/decision-table-template.csv`：順序、時間碼、用途、剪輯動作、理由、人工審核。
- `assets/ai-short-video-editing/decision-table-fixed-output-v1.md`：AI 服務不可用時的固定候選。
- `assets/ai-short-video-editing/ai-demo/ai-mini-cut-reference.mp4`：25.1 秒、1080 × 1920 完成品參考。
- `assets/ai-short-video-editing/asset-manifest.json`：素材來源、規格、SHA-256、已驗證項目與阻塞清冊。

以上固定材料已建立並完成檔案層檢查，但仍須在指定 Windows 教室完成 Premiere 操作試跑與 cold follow-along。通過前，本課仍不可宣告可直接開課。

## 最終交付與評量

學員在本 5 小時模組交付：

- `foundation-check-v1.md`：能指出作用物件、功能位置、目標狀態與驗證方式的四題紀錄。
- `practice-cut-v1.mp4`：證明能完成基本剪接與 H.264 輸出。
- `decision-table-v1.csv`：AI 精華候選與人工核對結果。
- `decision-tradeoff-log-v1.md`：至少一項採納與一項修改或拒絕。
- `ai-mini-cut-v1.mp4`：20–30 秒、1080 × 1920、可在 Premiere 外播放的短片。

通過條件不是記住所有選單位置，而是遇到新題目時能先判斷「改誰、去哪裡改、要變成什麼、如何證明」。

## 單元矩陣

### Part 0：Premiere 與證照共同基礎（180 分鐘）

- CH0-1：看懂 Premiere 的工作流程 — 建立專案、匯入素材、區分 source／sequence／timeline clip，辨認核心面板（40 分鐘）
- CH0-2：掌握時間軸基本操作 — 播放頭、時間碼、軌道、選取、裁切、Razor、Ripple、Link／Unlink、復原與測試輸出（55 分鐘）
- CH0-3：建立題庫功能地圖 — 串起專案與媒體、序列與軌道、效果控制與關鍵影格、音訊、文字字幕、效果、輸出與封存（60 分鐘）
- CH0-4：把題目翻成操作路徑 — 用題幹拆解卡判斷物件、動詞、位置、目標狀態、限制與驗證（25 分鐘）

### Part 1：AI 輔助剪輯延伸（100 分鐘）

- CH1-1：從聲音取得可用逐字稿 — 認識 AI 角色，取得或開啟 SRT，抽查人名、數字、否定詞與時間碼（25 分鐘）
- CH1-2：把逐字稿變成剪輯決策表 — 產生鉤子、保留段落、刪除建議與順序，逐筆核對原意與時間碼（30 分鐘）
- CH1-3：在 Premiere 執行 AI 決策 — 依決策表完成 20–30 秒粗剪、直式版面與字幕，輸出可播放版本（35 分鐘）
- CH1-4：保留人工判斷並銜接題庫 — 比較 AI 建議與實際結果，記錄一項採納、一項修改或拒絕，回扣「物件 → 位置 → 狀態 → 驗證」（10 分鐘）

### 休息與轉場（20 分鐘）

- CH0-2 完成後休息 10 分鐘。
- CH0-4 完成後休息 10 分鐘。

## 課前環境契約

- 教室為 64 位元 Windows，Premiere Pro 2024 已安裝並能開啟指定練習專案。
- 教師需先在實際教室驗證 New Project、Sequence、Effect Controls／Properties、Text、Export 與題庫涉及的面板路徑。
- WhisperDesktop／Subtitle Edit 與模型若作為主線，必須課前完成一次 SRT 匯出；現場不下載大型模型。
- 轉錄工具不可用時，直接發放同素材版本 SRT，學員仍完成校正、AI 決策與 Premiere 執行。
- 生成式 AI 只使用校方核准且課前可登入的服務；不可用時使用固定輸出，不改變學習成果。

## 已確認決策與待驗證事項

已確認：

1. 12 小時總課程由 5 小時基礎與 AI、4 小時題庫講解、3 小時考試組成。
2. 第二天證照考試是核心；本 5 小時先建立理解題庫所需的 Premiere 基礎。
3. 學員完全零基礎，不假設知道專案、序列、片段、面板或軌道。
4. AI 輔助剪輯是重要賣點，但配置為 100 分鐘延伸，不壓縮 180 分鐘證照共同基礎。
5. 現行題庫簡報已移除缺檔的舊版 B08、B09、B19。
6. 證照基礎固定素材、功能地圖、練習卡、SRT、決策表 fallback 與參考成片已建立；來源與檢查記錄於 `asset-manifest.json`。

仍待完成：

1. 以現行 77 頁簡報、指定題目專案與 Windows Premiere Pro 2024 核對 CH0-1～CH1-3 的版本敏感介面與操作結果。
2. 補教室版面板截圖；現有 `premiere-workspace-map-v2.svg` 只能作為概念圖。
3. 決定校方核准的生成式 AI 服務、登入方式與隱私界線；若未核准，固定輸出維持正式主線。
4. 在實際 Windows 教室完成全流程與復原路徑試跑。
5. 由零基礎真人完成一次 5 小時 cold follow-along，再決定是否微調節奏。
