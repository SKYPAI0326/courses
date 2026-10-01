---
slug: ai-short-video-editing
name: AI 短影音剪輯實戰：從逐字稿到 Premiere 成片
color: "#7a9ea3"
audience: 具備 Premiere 基本剪輯能力、想提升口播／訪談／活動影片剪輯效率的學生
institution: 弄一下工作室
duration: 2h
tools: WhisperDesktop 或 Subtitle Edit、校方核准的免費生成式 AI、Clipchamp 免費版、Premiere Pro 2024
prac: false
course_type: skill-operation
pilot: false
platform_version: Premiere Pro 2024；WhisperDesktop／Subtitle Edit；Clipchamp（課前驗證版）
---

## 課程定位（Positioning）

用免費或學校提供的工具，把 3–5 分鐘中文口播／訪談素材轉成一支 45–60 秒、1080 × 1920 的直式短影音：AI 負責逐字稿、精華候選、片段排序與停頓偵測；你在 Premiere 2024 中做語意、節奏、品牌視覺與輸出的最後判斷。

本課不把 AI 當成一鍵成片按鈕。每個 AI 結果都要保留原始時間碼、剪輯理由與人工取捨，讓成片能被檢查、修改與重做。

## 受眾畫像（Audience Profile）

- **職業／身分**：大專校院學生，或需要製作社群影片的初階內容工作者
- **技術底子**：會匯入素材、操作 Premiere 基本時間軸、裁切片段並輸出 H.264；不要求 Python 或前端開發能力
- **現有工具棧**：Premiere Pro 2024、瀏覽器、學校帳號；其他工具依教室環境採免費方案或講師預製結果
- **痛點 3 條**：
  1. 看完長口播後仍不知道哪一句適合當前三秒鉤子。
  2. 自動字幕能產生文字，卻沒有交代哪些內容該刪、該留或重排。
  3. 免費 AI 工具的額度、登入、浮水印與作業系統差異，可能讓全班無法完成同一個成果。

## Brand Brief（品牌調性）

- **tone_register**：技術友善
- **mood_keywords**：清楚、可控、實務
- **differentiation**：把 AI 的分析結果轉成可核對的剪輯決策，再交由 Premiere 完成可控的成片；課程成果不是 AI 報告，而是可交付的短影音與取捨紀錄。

## 學習成果（Outcomes）

1. 能使用課前準備好的 Whisper 工具或講師提供的轉錄結果，取得含時間碼的逐字稿與 SRT。
2. 能用校方核准的免費生成式 AI，從逐字稿找出鉤子、核心觀點、可刪段落與片段順序。
3. 能完成一張含原始時間碼、剪輯動作、理由與畫面建議的剪輯決策表。
4. 能使用 Clipchamp 免費版或講師提供的處理結果，辨識停頓移除對節奏的影響。
5. 能依決策表在 Premiere Pro 2024 完成 45–60 秒、1080 × 1920 的直式短影音，整合字幕、文字卡、B-roll、Logo 與背景音樂。
6. 能指出至少一項採納與一項拒絕的 AI 建議，並以原意、節奏或畫面安全範圍說明理由。

## 前置知識依賴鏈（Prerequisite Chain）

```yaml
dependencies:
  CH1-1: []
  CH1-2: [CH1-1]
  CH1-3: [CH1-1, CH1-2]
  CH2-1: [CH1-2, CH1-3]
  CH2-2: [CH1-3, CH2-1]
  CH2-3: [CH1-3, CH2-1, CH2-2]
```

## 試跑包交付規格（Verification Assets）

本課是 `skill-operation`，每個單元的試跑包不含個人帳號或付費連線設定，改以固定素材、提示詞、預期輸出與恢復路徑驗證。

- `assets/ai-short-video-editing/ai-short-video-demo-01.mp4`：3–5 分鐘、中文口播或訪談、無個資、具教學授權。
- `assets/ai-short-video-editing/ai-short-video-demo-01-transcript-v1.txt`：與影片同一版本的原始逐字稿，含說話者標記（若適用）。
- `assets/ai-short-video-editing/ai-short-video-demo-01-v1.srt`：教師預製的含時間碼字幕，作為 Whisper 不可用時的 fallback。
- `assets/ai-short-video-editing/whisper-model-v1`：教師在 Windows 課前驗證的模型資料夾，不要求學員現場下載。
- `assets/ai-short-video-editing/decision-table-template.csv`：欄位固定為順序、原始時間碼、內容用途、剪輯動作、保留理由、畫面建議、人工審核。
- `assets/ai-short-video-editing/prompt-card.md`：校方核准的免費生成式 AI 提示詞與固定輸出格式。
- `assets/ai-short-video-editing/approved-ai-service-card.md`：教師填寫唯一指定服務、網址、登入方式、免費界線與 fallback。
- `assets/ai-short-video-editing/decision-table-fixed-output-v1.md`：AI 無法使用時的固定候選與人工確認清單。
- `assets/ai-short-video-editing/subtitle-correction-log-template.md`：字幕修正與時序抽查紀錄。
- `assets/ai-short-video-editing/subtitle-error-fixture-v1.md`：人名／數字／否定詞與過長字幕列的課前驗證條件。
- `assets/ai-short-video-editing/ai-short-video-demo-01-fixture-v1.srt`：文字介面練習用 SRT；無音訊佐證，不得取代正式 fallback。
- `assets/ai-short-video-editing/decision-tradeoff-log-template.md`：AI 建議採納／拒絕／修改的交付紀錄。
- `assets/ai-short-video-editing/subtitle-edit-settings-v1.md`：教師填寫實際版本與 Subtitle Edit 操作路徑。
- `assets/ai-short-video-editing/premiere-project-starter/`：Premiere 2024 起始專案、直式序列設定、字幕安全範圍與示範素材連結。
- `assets/ai-short-video-editing/checklist.md`：環境檢查、素材完整性、匯出設定與成果檢核表。

決策表、層次表、提示詞卡、服務卡、環境檢查表與 Subtitle Edit 設定說明已放入工作區；核心影片、同版本逐字稿／SRT、Whisper 模型與 Premiere 起始專案仍待補入，服務卡也要由教師填寫。在素材補齊並於實際教室電腦試跑前，這門課只能視為內容草稿，不能宣告可上課。

## 單元矩陣

### Part 1：先讓 AI 參與內容判斷（預計 60 分鐘）

- CH1-1：AI 剪輯的三個層次 — 區分字幕、技術剪輯與內容剪輯，說出本課每個 AI 步驟的可驗證產物（10 分鐘）
- CH1-2：Whisper 語音辨識與 SRT — 取得含時間碼的逐字稿，修正專有名詞、數字與斷句並輸出 SRT（20 分鐘）
- CH1-3：讓 AI 產生剪輯決策表 — 用固定格式取得鉤子、45–60 秒精華、刪除段落、片段排序與畫面建議，完成人工審核（30 分鐘）

### Part 2：把決策落到可交付成片（預計 60 分鐘）

- CH2-1：AI 停頓移除與節奏判斷 — 比較 Clipchamp 處理前後的節奏，恢復不該刪除的思考停頓與情緒留白（20 分鐘）
- CH2-2：Premiere 2024 執行剪輯決策 — 依時間碼粗剪、修正跳接與音訊斷點，整合 SRT、直式版面、文字卡與 B-roll（30 分鐘）
- CH2-3：成果檢核 — 以鉤子、單一主題、字幕可讀性、原意與畫面安全範圍檢查 45–60 秒成片，記錄一採納一拒絕（10 分鐘）

## 補充說明（不列為必要工具）

### OpusClip

OpusClip 適合示範「長影片自動選精華、重組短片、動態字幕與 9:16 版型」的另一種產品路徑；免費版的浮水印、點數、保存期限與方案變動，不適合作為全班必要工具。課程只在收束時比較：OpusClip 省下哪些操作、哪些判斷仍需要人工、以及它如何與 Premiere 的精修控制不同。

### 本機 AI 字幕工具案例

FastAPI＋faster-whisper＋OpenCC＋React 的本機工具可作為課後「用 Vibe Coding 打造字幕工具」專題。它目前只負責逐字稿與 SRT，不負責精華選段、影片剪接或 MP4 成片；本課不要求學員安裝、開發或提交程式碼。

## 課前環境契約

- **本班確認**：學校教室使用 Windows；WhisperDesktop／Subtitle Edit 與模型可作為字幕製作主線，但必須由講師在課前於實際教室電腦完成一次轉錄與 SRT 匯出試跑。
- **Windows 路徑**：教室為 64 位元 Windows，且已預先安裝可輸出 SRT 的 WhisperDesktop／Subtitle Edit 與模型；不在課堂下載大型模型。
- **macOS 或工具不可用路徑**：由講師提供同一素材版本的 `ai-short-video-demo-01-transcript-v1.txt` 與 `ai-short-video-demo-01-v1.srt`；學員仍完成逐字稿修正、AI 決策表與 Premiere 成片，學習成果不變。
- **Clipchamp**：課前以學校 Microsoft 帳號登入，確認可上傳測試影片、可執行停頓偵測／移除，並確認輸出條件；若不可用，使用講師預先處理的前後版本做節奏比較。
- **生成式 AI**：只使用校方核准、可登入且可在課前測試的免費方案；不得把未驗證的網站或個人付費帳號列為門檻。

## G1 待確認

正式進入其餘單元前，請確認：

1. 六個單元中最沒把握的是哪一個？
2. 受眾是否確實具備 Premiere 基本時間軸能力？
3. 哪一條學習成果仍太浮泛，需要改成更可檢查的產物？
4. 「清楚、可控、實務」是否符合這門課與既有課程的差異？
