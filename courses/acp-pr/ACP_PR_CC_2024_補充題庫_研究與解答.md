# ACP Premiere Pro CC 2024 補充題庫：研究與解答

- 整理日期：2026-10-22
- 本地題庫來源：`QUESTION-BANK-DIFF.md`、本次考試畫面照片、`ACP_PR_CC_2024_獨立核實解題本_v2_統一題號.pptx`
- 網路查核原則：Premiere Pro 操作優先使用 Adobe 官方文件；無障礙使用 W3C WAI；姓名標示使用 Creative Commons 官方建議。
- 整併結果：前批新增 A23–A31、B27–B34；本批再新增 A32–A38、B35–B42，合併後共 80 題／任務。
- Deep Review 介面修正：A10 以 Premiere 25.0+ 的 Properties panel 為主，Essential Graphics 僅作舊版說明；B36 依題圖使用 Markers 選單名稱；B40 的 2026 介面入口仍列 `PENDING`。

## 學科題

### A23｜標題可讀性與無障礙

- 正解：在文字後方加入與文字具足夠對比的實色背景框。
- 理由：固定背景可以讓文字在複雜畫面上維持可預測的對比；改影格率無關可讀性，同色陰影無法提供對比，改為襯線字體也不會自動解決對比不足。
- 來源：[W3C WAI：文字與背景對比](https://www.w3.org/WAI/WCAG22/Techniques/general/G145)、[W3C WAI：實色背景與強對比](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o3p11-unobscured-foreground/)
- 狀態：已核實。

### A24｜16:9 Ultra HD 4K 影格大小

- 正解：`3840 × 2160`。
- 理由：4K UHD 的 16:9 尺寸為 3840 × 2160；4096 × 2160 是 4K Cinema，不是本題的 16:9 UHD。
- 來源：[Adobe：Generative Extend 影像來源解析度](https://helpx.adobe.com/ph_en/premiere/desktop/edit-projects/edit-with-generative-ai/generative-extend-faq.html)
- 狀態：已核實。

### A25｜需姓名標示的音樂授權

- 正解：在片尾加入創作者姓名、曲名、來源與授權條款。
- 理由：Creative Commons 建議使用 TASL（Title、Author、Source、License）。僅口頭感謝不足；只寫 metadata 也不等於依授權條件對觀眾完成標示。
- 來源：[Creative Commons：TASL attribution](https://creativecommons.org/course/cc-cert-edu/unit-4-using-cc-licenses-and-cc-licensed-works/4-1-choosing-and-applying-a-cc-license/)
- 狀態：已核實；實際使用時仍須以該音軌的具體授權條款為準。

### A26｜移除綠幕背景

- 正解：`Ultra Key`。
- 理由：Ultra Key 用於將綠色或藍色的單色背景轉為透明區域。
- 來源：[Adobe：使用 Ultra Key 製作 Chromakey](https://helpx.adobe.com/au/premiere/desktop/add-video-effects/effects-and-transitions-library/apply-and-customize-chromakey-using-the-ultra-key-effect.html)
- 狀態：已核實。

### A27｜序列當來源時的置入結果

- 正解：`As Individual Clips`。
- 理由：Timeline 的 `Insert And Overwrite Sequences As Nest Or Individual Clips` 按鈕關閉時，把序列編輯到另一個序列會放入其個別 clips，而非一個 nested sequence clip。
- 來源：[Adobe：Nest a sequence](https://helpx.adobe.com/ph_fil/premiere-pro/how-to/premiere-pro-nesting-sequence-cc.html)
- 狀態：已核實。

### A28｜Captions 的 True／False

- 正解：`False／False／True`。
- 理由：
  1. 不只能在 Text panel 的 transcript 修改；caption track 可在 Timeline 用編輯工具調整，字幕文字也可在 Captions 介面或 Program Monitor 修改。
  2. Filler words 是 transcript 的偵測／過濾項目，不是「字幕只顯示 `[...]`」的規則。
  3. 序列的第一條 caption track 為 `C1`。
- 來源：[Adobe：Captions overview](https://helpx.adobe.com/premiere/desktop/add-text-images/insert-captions/about-captions.html)、[Adobe：偵測 filler words 與 pauses](https://helpx.adobe.com/premiere/desktop/edit-projects/edit-video-using-text-based-editing/detect-and-delete-pauses-in-transcripts.html)、[Adobe Community Expert：第一條 caption track 是 C1](https://community.adobe.com/questions-729/can-i-attach-the-srt-files-to-the-original-video-clips-1391234)
- 狀態：已核實。`C1` 為 Timeline 字幕軌標籤，不要與 CEA-608 的 `CC1` stream 混淆。

### A29｜保存只顯示 Timeline 與 Program Monitor 的介面

- 正解：`Use Workspaces`。
- 理由：先排列需要的 panels，再用 `Window > Workspaces > Save as New Workspace`保存，可以在後續專案與重開 Premiere 後重用。
- 來源：[Adobe：Save custom workspaces](https://helpx.adobe.com/premiere/desktop/organize-media/create-projects/save-workspace-when-editing-multiple-projects-simultaneously.html)
- 狀態：已核實。

### A30｜移除 In／Out 區間且不留 gap

- 正解：`Extract`。
- 理由：Extract 移除 In／Out 範圍後會使後方素材向前補位；Lift 移除後會留下空隙。
- 來源：[Adobe：Source 與 Program Monitor 按鈕](https://helpx.adobe.com/ie/premiere/desktop/get-started/source-and-program-monitor-adjustments/about-source-monitor-and-program-monitor.html)、[Adobe：Extract 與 Lift 的刪除行為](https://community.adobe.com/announcements-732/now-in-beta-filler-words-and-other-text-based-editing-updates-in-premiere-pro-313483)
- 狀態：已核實。

### A31｜大量 Media Offline 的效率處理

- 正解：`Link Media`。
- 理由：對離線 clips 執行 Link Media，定位第一個相符檔案後，可透過檔名、副檔名與路徑結構自動連結其他素材。
- 來源：[Adobe：Relink offline clips](https://helpx.adobe.com/premiere/desktop/organize-media/ingest-proxy-workflow/relink-offline-clips.html)
- 狀態：已核實。

## 術科任務

### B27｜Africa 2：將 Jackal.mp4 解讀為 24 fps

- 操作：在 Project panel 右鍵 `Jackal.mp4` → `Modify > Interpret Footage` → 勾選 `Assume this frame rate` → 輸入 `24.00` → `OK`。
- 驗收：Project panel 顯示該 clip 以 24 fps 解讀，duration 會依新影格率對應變化。
- 來源：[Adobe：Change clip frame rate](https://helpx.adobe.com/premiere/desktop/edit-projects/modify-clip-properties/change-the-frame-rate-of-a-clip.html)
- 狀態：流程已核實；專案結果待原始素材驗證。

### B28｜Africa 2：建立 Rough Cut 並覆寫音訊

- 題目條件：
  - `Elephant.mp4`：`00:00:01:00–00:00:03:00`
  - `Hippos.mp4`：`00:00:02:09–00:00:03:24`
  - `Giraffe.mp4`：`00:00:00:00–00:00:03:12`
  - `AFRICAN T 120.WAV`：`00:00:03:27–00:00:10:27`
- 操作：依 Clip Order 逐段在 Source Monitor 設 In／Out，從 sequence `00:00:00:00` 開始連續置入 V1，不留 gap；再將 WAV 設定 In／Out，只將 audio patch 到 A1，使用 Overwrite 覆寫三段現有音訊。
- 驗收：三段畫面依表格順序連續；A1 只有指定 WAV 範圍；序列起點與所有 In／Out 無誤。
- 來源：[Adobe：Set In and Out points](https://helpx.adobe.com/premiere/desktop/get-started/source-and-program-monitor-adjustments/set-in-and-out-points-in-the-source-monitor.html)、[Adobe：Source Patching 與 Overwrite](https://helpx.adobe.com/premiere/desktop/edit-projects/intro-to-editing/add-media-to-the-timeline-using-source-patching.html)
- 狀態：流程已核實；照片中簡寫時間碼已補為 `hh:mm:ss:ff`，仍須在題目專案驗收。

### B29｜Kittens：加入指定影像與音樂

- 題目條件：`Kitten1_Adopt.mp4` In `00:00:00:10`、Out `00:00:04:03`；僅影像置於 V1，接在 `Kitten1_Pet1.mp4` 之後。`CutePianoStrings.mp3` In `00:00:00:20`，置於 A3，從序列起點到 `00:00:20:00`。
- 操作：在 Source Monitor 設定影片 In／Out，使用 Drag Video Only 放到 V1；音樂設 In 後 patch 到 A3，從序列起點覆寫／置入，再修剪結尾至 `00:00:20:00`。
- 驗收：V1、A2、A3 所需素材皆在 `00:00:20:00` 結束；新增影片沒有帶入音訊。
- 來源：[Adobe：Source Monitor](https://helpx.adobe.com/ie/premiere/desktop/get-started/source-and-program-monitor-adjustments/about-source-monitor-and-program-monitor.html)、[Adobe：Set In and Out points](https://helpx.adobe.com/premiere/desktop/get-started/source-and-program-monitor-adjustments/set-in-and-out-points-in-the-source-monitor.html)
- 狀態：流程已核實；時間碼來自照片且以 `hh:mm:ss:ff` 補齊，待專案驗證。

### B30｜Kittens：管理 clips 與 tracks

- 操作：
  1. 用 Alt（Windows）／Option（macOS）選取 `Kitten1_Bath.mp4` 的 video component，只刪影像。
  2. 保持 In／Out 不變，將 `Kitten1_BathWB.mp4` 的 video 移到 V1。
  3. 選取 `Kitten1_BathWB.mp4` video 與 `Kitten1_Bath.mp4` audio，用 `Clip > Link`。
  4. 確認 V3、A4 無需保留的 clips 後，用 `Sequence > Delete Tracks` 移除指定 tracks。
- 驗收：新影像在 V1 且與舊音訊同起訖、已 Link；V3 與 A4 已移除；其他軌道不變。
- 來源：[Adobe：Select clip components](https://helpx.adobe.com/premiere/desktop/edit-projects/change-clip-sequence/select-clips.html)、[Adobe：Link／Unlink clips](https://helpx.adobe.com/sg/premiere/desktop/add-audio-effects/basic-audio-editing/link-audio-and-video-clips.html)、[Adobe：Delete tracks](https://helpx.adobe.com/premiere/desktop/edit-projects/change-clip-sequence/delete-tracks.html)
- 狀態：流程已核實；待專案驗證 clip 起訖與軌道結果。

### B31｜Fitness World：Auto Reframe

- 操作：在 Project panel 選 sequence → `Sequence > Auto Reframe Sequence` → Target Aspect Ratio 選 `Vertical 4:5` → Motion Tracking 選 `Slower Motion` → Clip Nesting 選 `Don't Nest Clips` → 保留預設名稱 → `Create`。
- 驗收：產生新的 4:5 序列；每個 clip 個別套用 Auto Reframe；未被合併為 nest。
- 來源：[Adobe：Add Auto Reframe to sequences](https://helpx.adobe.com/sg/premiere/desktop/add-video-effects/commonly-used-effects/add-auto-reframe-effect-to-a-sequence.html)
- 狀態：流程已核實；實際追蹤結果待專案驗證。

### B32｜Commute：改名並 Unlink audio

- 操作：在 Project panel 將序列改名 `Daily Commute`；在 Timeline 選 `commute1` 的 linked clip，用 `Clip > Unlink`。
- 驗收：序列名稱正確；選取／移動 `commute1` 影像時不會同時帶動 audio。
- 來源：[Adobe：Link／Unlink clips](https://helpx.adobe.com/sg/premiere/desktop/add-audio-effects/basic-audio-editing/link-audio-and-video-clips.html)
- 狀態：流程已核實；待專案驗證。

### B33｜Africa：刪除 Hyena-Rock 的所有停頓

- 操作：開啟 `Hyena-Rock` sequence 與 Text panel 的 Transcript；在 Transcript View Options 把 Minimum Pause Length 設為 `1.0 s`；開啟 Filter 選 `Pauses`；確認為 `Extract`，再選 `Delete all`。
- 驗收：所有大於等於 1 秒的停頓已移除，Timeline 同步 ripple 補位，沒有留 gap。
- 來源：[Adobe：Detect and delete pauses](https://helpx.adobe.com/premiere/desktop/edit-projects/edit-video-using-text-based-editing/detect-and-delete-pauses-in-transcripts.html)、[Adobe Classroom in a Book 2026 範例](https://ptgmedia.pearsoncmg.com/images/9780135561270/samplepages/9780135561270_Sample.pdf)
- 狀態：流程已核實；素材與刪除點待專案驗證。

### B34｜School：加入並調整音樂軌

- 操作：在 `Study Session` sequence 將 `StudyMusic.mp3` 放到 A2 並對齊序列起點；以 Selection tool 拖曳音樂 clip 的 Out edge，對齊最後一段影片的結尾；在 A1 track header 開啟 `M`。
- 驗收：A2 音樂與影像同起訖；A1 已 mute；預覽與輸出不會聽到 A1。
- 來源：[Adobe：Trim a clip](https://helpx.adobe.com/premiere/desktop/edit-projects/trim-clips/trim-a-clip.html)、[Adobe：Exclude／Mute tracks](https://helpx.adobe.com/premiere/desktop/edit-projects/change-clip-sequence/edit-track-appearance.html)
- 狀態：流程已核實；音樂實際 Out point 待專案影片長度驗證。

## 本批新增學科題

### A32｜三項 Pre-production 活動

- 正解：`Location scouting`、`Creating a shot list`、`Storyboarding`。
- 理由：三者都在正式拍攝前完成規劃；ingesting、reviewing dailies 與 color grading 都以已拍攝素材為前提。
- 來源：[Adobe：Filmmaking stages](https://www.adobe.com/creativecloud/video/discover/filmmaking.html)、[Adobe：Shot list](https://www.adobe.com/creativecloud/video/discover/shot-list.html)、[Adobe：Shooting script](https://www.adobe.com/creativecloud/video/discover/shooting-script.html)
- 狀態：已核實。

### A33｜大型專案 Scratch Disk 位置

- 正解：`A local non-OS/project SSD`。
- 理由：本機高速且與 OS／主要專案讀寫分離的 SSD 可降低磁碟競用；microSD、一般網路磁碟與系統碟不是本題的效能最佳選項。
- 來源：[Adobe：Storage recommendations](https://helpx.adobe.com/premiere/desktop/get-started/technical-requirements/storage-recommendations.html)
- 狀態：已核實；企業共享儲存仍應以實際吞吐與延遲評估。

### A34｜公共場所人像與音樂授權

- 正解：`C`；取得歌曲商業使用所需授權或將該段靜音，並取得可辨識人物的 talent／model releases。
- 理由：把音樂同步到影音作品通常涉及另行授權；可辨識人物的商業使用也涉及肖像、隱私或 publicity rights。公共場所拍攝不會自動免除兩者。
- 來源：[U.S. Copyright Office：Music licensing](https://www.copyright.gov/music-modernization/educational-materials/musicians-income.pdf)、[Adobe Stock：Model release overview](https://helpx.adobe.com/stock/contributor/content-policies-guidelines/model-property-releases/model-release-overview.html)
- 狀態：考題最佳答案已核實；實務法律適用依司法管轄、用途與發行方式而異。

### A35｜分層 PSD 保留個別圖層

- 正解：在 Import dialog 選 `Sequence`。
- 理由：Sequence 會把選取圖層各自匯入為 clip，並建立分軌 sequence；Merge Layers 會扁平化。
- 來源：[Adobe：Import Photoshop files](https://helpx.adobe.com/premiere/desktop/organize-media/import-files/import-photoshop-and-illustrator-files.html)
- 狀態：已核實。

### A36｜視障觀眾的畫面資訊

- 正解：`Insert an audio description track that explains the visuals.`
- 理由：audio description 以聲音說明理解影片所需的動作、場景變化與畫面文字；captions 主要把語音與聲音轉成文字。
- 來源：[W3C WAI：Description of visual information](https://www.w3.org/WAI/media/av/description/)
- 狀態：已核實。

### A37｜使用 Proxy Files 的目的

- 正解：`To improve playback performance`。
- 理由：Proxy 是較低解析度的替身媒體，降低剪輯時的解碼與 I/O 負擔；final export 通常重新連回原始媒體。
- 來源：[Adobe：Create proxies](https://helpx.adobe.com/premiere/desktop/organize-media/ingest-proxy-workflow/create-proxies.html)、[Adobe：Ingest and Proxy workflow](https://helpx.adobe.com/premiere/desktop/organize-media/ingest-proxy-workflow/ingest-and-proxy-workflow.html)
- 狀態：已核實。

### A38｜寬幅照片的畫面比例

- 正解：`16:9`。
- 理由：原始題圖為寬幅橫式，寬度約為高度的 1.78 倍；720p 與 1080p 是解析度，1:1 是正方形，9:16 是直式比例。本題圖不同於 A01 的 4:3 圖片，不能去重。
- 來源：`螢幕擷取畫面 2026-10-22 144945.png`、[Adobe：Sequence settings reference](https://helpx.adobe.com/premiere/desktop/edit-projects/change-clip-sequence/sequence-settings-reference.html)
- 狀態：已核實。

## 本批新增術科任務

### B35｜Pizza Time：移除指定區段

- 操作：在 `all clips` sequence 設 In `00:02:43:00`、Out `00:02:48:00`；確認所需 tracks 未鎖且 targeting／sync lock 正確；執行 `Sequence > Extract`。
- 驗收：指定範圍已移除，後方 clips 整體前移補位，沒有 gap，也沒有延長 clips。
- 來源：[Adobe：Ripple edits](https://helpx.adobe.com/premiere/desktop/edit-projects/trim-clips/perform-ripple-edits.html)
- 狀態：流程已核實；專案結果待原始素材驗證。

### B36｜Pizza Time：管理 Timeline Markers

- 操作：開啟 `pizza build`，取消選取 clips；在題圖顯示的 `Markers` 選單執行 `Clear Markers`；在 `00:00:17:06` 建立 sequence marker，名稱 `cutting overhead`，duration `00:00:05:00`，顏色 White。
- 驗收：只剩指定的白色 5 秒 marker，位置與名稱完全相符。
- 來源：[Adobe：Find, move, and delete markers](https://helpx.adobe.com/sg/premiere/desktop/organize-media/apply-labeling/find-move-and-delete-markers.html)、[Adobe：Default keyboard shortcuts](https://helpx.adobe.com/premiere/desktop/get-started/keyboard-shortcuts/default-keyboard-shortcuts.html)
- 狀態：流程已核實；選單標籤可能依版本顯示 Marker／Markers，專案結果待原始素材驗證。

### B37｜Social：建立 Nested Sequence

- 操作：在 `Social Title for Nesting` 將指定 bin 最長 clip 放 V1 並從 00:00 開始；中等放 V2、最短放 V3，移動 V2／V3 使三者同時結束；全選後 `Clip > Nest`，命名 `Nested Name + Title`；在 Project panel 將新 sequence label 設為 `Cerulean`。
- 驗收：Timeline 為單一 nest；開啟後三層原 duration 不變且 Out 對齊；Project panel 名稱與 label 正確。
- 來源：[Adobe Premiere Pro Reference：Nest and label](https://helpx.adobe.com/archive/en/premiere-pro/cc/2015/premiere_pro_reference.pdf)
- 狀態：流程已核實；clip 長短與專案結果待原始素材驗證。

### B38｜Africa：Auto Reframe 為 9:16

- 操作：在 Project panel 選 `African Animals` → `Sequence > Auto Reframe Sequence` → Target Aspect Ratio 選 `Vertical 9:16` → 題目未指定的選項保留預設 → `Create`。
- 驗收：新增 9:16 sequence，原 sequence 保留。
- 來源：[Adobe：Auto Reframe Sequence](https://helpx.adobe.com/premiere/desktop/add-video-effects/commonly-used-effects/add-auto-reframe-effect-to-a-sequence.html)
- 狀態：流程已核實；實際追蹤結果待專案驗證。

### B39｜Africa：重整 Maasai Mara

- 操作：在 Project panel 將 `Maasai Mara` 改名 `Zebras`；開啟 sequence，使用 `Sequence > Delete Tracks` 刪除全部 empty video／audio tracks；Alt／Option-click `Zebras.mp4` audio component，取消 `Clip > Enable`。
- 驗收：名稱正確、空軌已刪、只有 Zebras.mp4 audio 被停用，其他音訊不受影響。
- 來源：[Adobe：Delete tracks](https://helpx.adobe.com/premiere/desktop/edit-projects/change-clip-sequence/delete-tracks.html)、[Adobe：Enable or disable a clip](https://helpx.adobe.com/sg/premiere/desktop/edit-projects/change-clip-sequence/enable-or-disable-a-clip.html)
- 狀態：流程已核實；專案結果待原始素材驗證。

### B40｜Fitness World：移除未使用素材

- 操作：啟用 Project panel，先檢查 panel 選單是否有 `Remove Unused`；若考試版本沒有該命令，改在 List View 依 `Video Usage`／`Audio Usage` 找出未使用項目並刪除，再檢查及儲存專案。
- 驗收：未在任何 Timeline 使用的 project items 已移除；使用中的素材與 sequences 保留；硬碟原始檔未刪除。
- 來源：[Adobe Premiere Pro Reference：Remove unused assets](https://helpx.adobe.com/archive/en/premiere-pro/cc/2015/premiere_pro_reference.pdf)
- 狀態：`PENDING`；移除邏輯已核實，但題圖所示 2026 介面沒有上方 Project 選單，`Remove Unused` 的實際入口與 CertPREP 評分仍待原始專案驗證。

### B41｜Commute：刪除 commute3 並補滿 Gap

- 操作：在 `Daily Commute` 刪除 linked `commute3`；用 Selection tool 將 `commute4` 的左側 In edge 向左延伸，吸附到前一段 clip 的 Out；不可使用 Generative Extend 或 Rate Stretch。
- 驗收：沒有 gap；commute4 的 duration 增加、原 Out 不變、Speed 仍為 100%，影音保持同步。
- 來源：[Adobe：Trim a clip](https://helpx.adobe.com/premiere/desktop/edit-projects/trim-clips/trim-a-clip.html)、[Adobe：Ripple edits](https://helpx.adobe.com/premiere/desktop/edit-projects/trim-clips/perform-ripple-edits.html)
- 狀態：流程已核實；source handles 與專案結果待原始素材驗證。

### B42｜Aspirations：建立 Promo Sequence

- 操作：選 `File > New > Sequence`；在 `Sequence Presets` 選 `HDV > HDV 1080p25`；到 `Tracks` 分頁設定三條 video tracks、兩條 audio tracks；名稱輸入 `Promo`，建立後保持空白。
- 驗收：Project panel 出現 `Promo`；序列為 1080p／25 fps；Timeline 有 V1–V3、A1–A2，且沒有內容。
- 來源：`螢幕擷取畫面 2026-10-22 152118.png`、[Adobe：Sequence presets and settings](https://helpx.adobe.com/premiere/desktop/edit-projects/change-clip-sequence/sequence-presets-and-settings.html)
- 狀態：建立流程與設定欄位已核實；實際 CertPREP 評分待原始專案驗證。

## 限制

- 本次沒有 CertPREP／ACP 原始專案與素材包，因此 B27–B42 的介面操作邏輯可查核，但不能宣稱已在考試專案通過自動評分。
- B28、B29 的時間碼由照片中簡寫格式補為 `hh:mm:ss:ff`；簡報會同時保留原題數字與「需以專案驗證」狀態。
