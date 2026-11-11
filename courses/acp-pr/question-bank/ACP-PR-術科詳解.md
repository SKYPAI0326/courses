# ACP Premiere Pro 術科詳解（截圖支撐 33 題）

- 日期：2026-11-03
- 範圍：有考試截圖支撐的術科任務，題號沿用 [`../MOCK-EXAM-SOURCE-MAP.md`](../MOCK-EXAM-SOURCE-MAP.md)，依考試專案分組。
- 題目是英文原文，照「來源」那張截圖逐字轉錄。正解操作和講解用中文，選單、面板、按鈕名稱保留英文原名，方便對照考試畫面。
- 正解操作以 Windows 版為準。macOS 把 Alt 換成 Option、Ctrl 換成 Cmd；Preferences 在 Premiere Pro > Settings。
- 操作步驟以現行解題本為底稿，該版已在 B01–B42 Windows 題目專案上實機驗證。這次依考試截圖的條件逐題核對，有出入的地方都在講解裡註明。
- 配圖：只有 B11 的原題附參考圖；B28 的原題表格已轉成文字表格。其他任務的原題沒有附圖。

---

## Drone 專案

### B01｜Create a sequence
來源：`IMG_4805`；對照 `IMG_4836`

Use the Lighthouse_93.mp4 clip to create a sequence. Rename the new sequence Oregon Coast.

Note: You can click the underlined text to copy it. If a dialog is opened during the task, the text must be copied before the dialog is opened.

**正解操作**
1. 在 Project panel 對 Lighthouse_93.mp4 按右鍵，選 New Sequence From Clip。也可以把 clip 拖到 Project panel 右下角的 New Item 圖示上。
2. Project panel 會出現一個和 clip 同名的新 sequence，對它按右鍵 Rename，輸入 Oregon Coast。

**講解**：create a sequence from a clip 的重點是讓 Sequence Settings 自動跟著素材走，不要自己 File > New > Sequence 挑 preset。考試版只要求改名；主檔 PPT 版本另外要求移進 sequence bin，考試畫面沒有這條，不用做。

### B02｜Trim a clip
來源：`IMG_4800`；對照 `IMG_4838`

On track V1 of the Lighthouse sequence, trim the Lighthouse_99.mp4 clip so it ends at the same time as the clip on track V2, and the sequence duration changes.

Do not change the length of any other clip. Ensure that there are no gaps in the sequence.

**正解操作**
1. 開啟 Lighthouse sequence，開啟 Snapping（S）。
2. 選 Ripple Edit Tool（B）。
3. 拖曳 V1 上 Lighthouse_99.mp4 的尾端（Out point），吸附到 V2 clip 的結尾。

**講解**：the sequence duration changes 加上 no gaps，就是要用 Ripple Edit：修剪後後方內容會跟著移動，不留 gap，sequence 長度也跟著變。用一般 Selection Tool 拖尾端，可能會在後面留下 gap。Rolling Edit 會改到相鄰 clip 的長度，違反 do not change the length of any other clip。

### B03｜Create a clip marker
來源：`IMG_4802`；對照 `IMG_4839`

On the clip Lighthouse01, create a clip marker named Establishing Shot that starts at 00:00:01:00 and has a duration of 00:00:09:18

Note: You can click the underlined text to copy it. If a dialog is opened during the task, the text must be copied before the dialog is opened.

**正解操作**
1. 在 Project panel 雙擊 Lighthouse01，在 Source Monitor 開啟。
2. 把 Source Monitor 的 playhead 移到 00:00:01:00。
3. 按 M 新增 marker，再按一次 M（或雙擊 marker）開啟設定視窗。
4. Name 輸入 Establishing Shot，Duration 輸入 00:00:09:18，按 OK。

**講解**：clip marker 標在 clip 本身，在 Source Monitor 建立；在 Timeline 沒選 clip 時按 M，建立的是 sequence marker，會判錯。時間要用 clip 自己的時間碼（從 clip 開頭算）。名稱和時間建議在開對話框之前，先點題目底線文字複製。

### B04｜Organize clips
來源：`IMG_4801`；對照 `IMG_4840`

Create a top-level bin named sequences and move all existing sequences into the sequences bin. Rename the Drone_05 sequence as Drone View.

Note: You can click the underlined text to copy it. If a dialog is opened during the task, the text must be copied before the dialog is opened.

**正解操作**
1. 在 Project panel 最上層（不要進到任何 bin 裡）按 New Bin，命名 sequences。
2. 選取所有既有的 sequence，拖進 sequences bin。
3. 在 bin 內把 Drone_05 改名為 Drone View。

**講解**：top-level 是 Project panel 的根目錄，不要建在其他 bin 裡。all existing sequences 要全部搬，可以用 List View 的 Type 欄位排序，找出所有 Sequence 類型的項目。

### B25｜Apply an effect
來源：`IMG_4804`；對照 `IMG_4837`

In the Lighthouse sequence, create an adjustment layer and apply an SL Blue Ice Lumetri Color creative look to change the appearance of the entire Lighthouse02 clip.

Keep the adjustment layer name and creative look settings at default.

**正解操作**
1. 在 Project panel 選 New Item > Adjustment Layer，設定保持預設，按 OK。
2. 把 Adjustment Layer 拖到 Lighthouse sequence 中 Lighthouse02 上方的 track，起點和終點都對齊 Lighthouse02。
3. 選取 Adjustment Layer，開啟 Lumetri Color panel，在 Creative > Look 選 SL BLUE ICE。

**講解**：entire Lighthouse02 clip 代表 Adjustment Layer 要完整蓋住 Lighthouse02，不能短、也不要蓋到其他 clip。effect 要套在 Adjustment Layer 上，不是直接套在 Lighthouse02。名稱和 Look 的 Intensity 都不要改。

### B26｜Add and scale a graphic
來源：`IMG_4803`；對照 `IMG_4841`

In the Lighthouse sequence, add the LighthouseTitle.ai title graphic to the beginning of track V2 and scale it to 70%. Do not move the existing footage on the timeline.

**正解操作**
1. 把 LighthouseTitle.ai 從 Project panel 拖到 Lighthouse sequence 的 V2，起點吸附在 00:00:00:00。
2. 選取這個圖形，在 Effect Controls > Motion 把 Scale 設為 70。

**講解**：直接拖曳到空的 V2 等同 Overwrite，不會推動其他 track。不要按住 Ctrl 拖曳，那是 Insert，會把後方內容往右推，違反 do not move the existing footage。

## Getaway 專案

### B05｜Manage settings
來源：`152831.png`

Configure Premiere to automatically save open projects every 5 minutes, and to save a maximum of 30 project versions.

**正解操作**
1. 選 Edit > Preferences > Auto Save。
2. 勾選 Automatically save projects。
3. Automatically Save Every 設 5 minutes。
4. Maximum Project Versions 設 30，按 OK。

**講解**：Auto Save 屬於軟體層級的 Preferences，不在 Project Settings 或 Sequence Settings 裡。題目兩個數字都要改，只改一個會判錯。

### B07｜Adjust opacity
來源：`152637.png`

Adjust the opacity of the Mountain Getaway graphic so that it fades in from 0.0 to 100.0 percent over the first three seconds, then fades out from 100.0 to 0.0 percent over the last three seconds.

**正解操作**
1. 選取 Mountain Getaway graphic，開啟 Effect Controls > Opacity。
2. playhead 移到 graphic 起點，Opacity 設 0，建立 keyframe。
3. 往後 3 秒，Opacity 設 100。
4. 移到 graphic 結尾前 3 秒，建立一個 100 的 keyframe。
5. 移到 graphic 最後一格，Opacity 設 0。

**講解**：共 4 個 keyframe：0 → 100（前 3 秒）、100 → 0（後 3 秒），中間維持 100。first three seconds 和 last three seconds 都以 graphic 本身的起訖計算，不是 sequence 的起訖。

## Food Around the World 專案

### B10｜Apply color correction
來源：`150722.png`

Use the Lumetri Color tools to set the white balance in the Tiramisu sequence. Select the neutral gray swatch in the Tiramisu video, circled in green at 00:00:00:00, as the spectrally neutral point.

Do not add any effects.

**正解操作**
1. 開啟 Tiramisu sequence，playhead 移到 00:00:00:00。
2. 選取 Tiramisu video，開啟 Lumetri Color panel，展開 Basic Correction > White Balance。
3. 按 WB Selector，在 Program Monitor 點綠色圓圈裡的灰色色塊。

**講解**：spectrally neutral point 是「應該呈現無色偏的參考點」，所以 WB Selector 要點灰色，不能點彩色區域。Do not add any effects：只用 Lumetri Color 做 White Balance，不要另外從 Effects panel 加其他 effect。clip 上如果已經有 Lumetri Color，直接在既有的 effect 上調。

### B11｜Apply an effect
來源：`IMG_4809`；對照 `IMG_4832`

At the start of the Thai Curry sequence, apply the Track Matte Key effect to reveal the Thai_Food_06 clip on track V2 through the word THAI on track V4. Your result should look like the following image at 00:00:01:10.

![B11 參考圖：THAI 字樣內透出 Thai_Food_06 畫面，下方為 FOOD](img/B11.jpg)

**正解操作**
1. 在 Effects panel 搜尋 Track Matte Key，拖到 V2 的 Thai_Food_06 上。
2. 在 Effect Controls 的 Track Matte Key，Matte 選 Video 4。
3. Composite Using 保持 Matte Alpha。
4. playhead 移到 00:00:01:10，對照參考圖。

**講解**：effect 要套在「被看見的 video」（V2），Matte 指定「當 matte 的文字 track」（V4）。常見錯誤是把 effect 套在 V4 的文字上。THAI 字樣有透明背景，用 Matte Alpha，video 只會出現在字的形狀裡。

### B12｜Adjust audio
來源：`150823.png`；對照 `IMG_4808`、`IMG_4834`

Use an effect to fade out the music on track A1 at the end of the Thai Curry sequence over a one-second time span.

**正解操作**
1. 在 Effects panel 展開 Audio Transitions > Crossfade。
2. 把 Exponential Fade（或 Constant Power）拖到 A1 music clip 的結尾。
3. 雙擊 transition，確認 Duration 是 00:00:01:00。

**講解**：use an effect 指的是用 Audio Transitions 裡的 transition，不是刪掉音樂或手動調整 audio track 音量。transition 放在 clip 尾端，就是淡出。Premiere 預設 audio transition 長度是 1 秒，但仍要確認 Duration。

### B13｜Manage clips on the timeline
來源：`IMG_4807`；對照 `IMG_4831`

Adjust the Sushi sequence so that the audio clips for Sushi Pan and Sushi Pan 3 meet the following requirements:

- The audio clips for Sushi Pan and Sushi Pan 3 are located on track A2.
- Each audio clip is aligned with its corresponding video clip.
- Without grouping, ensure that each audio clip will move with its corresponding video clip.

**正解操作**
1. 按住 Alt 點 Sushi Pan 的 audio，只選取 audio，往下拖到 A2，起點保持和 video 對齊。
2. Sushi Pan 3 照同樣方式處理。
3. Shift 點選 Sushi Pan 的 video 和它的 audio，選 Clip > Link。
4. Sushi Pan 3 照同樣方式 Link。

**講解**：without grouping 是關鍵：Group 和 Link 都能讓 video 和 audio 一起移動，但題目指定不能用 Group，所以要用 Link。兩組要分開 Link，不要四個一起選。拖到 A2 時要垂直移動，不能改變時間位置。

### B14｜Prepare for export
來源：`IMG_4810`；對照 `IMG_4833`

Prepare the Thai Curry sequence for export by ensuring that it meets the following specifications:

- There are no gaps in the video. (Do not change the duration of any clip.)
- The Welcome title clip is visible from 00:00:08:29 to 00:00:12:07. (Do not delete any clips or change their opacity.)

Note: Do not export the sequence.

**正解操作**
1. 確認所有 track 的 Sync Lock 都開啟。
2. 在 video track 找到 gap。題目專案實測：gap 在 00:00:05:21–00:00:06:12，共 21 個 frame。
3. 在 gap 上按右鍵，選 Ripple Delete。
4. 檢查 Welcome title 跟著左移，起點在 00:00:08:29，最後一格在 00:00:12:07。

**講解**：兩個條件其實用同一個動作解決。刪掉 gap，後方所有內容一起往前移，Welcome title 就剛好落在指定時間。所以不要手動修剪 Welcome，也不要改 opacity。Sync Lock 沒開的 track 不會跟著移，title 就會錯位。最後不要按 Export。

## Transportation 專案

### B15｜Place a clip on the timeline
來源：`151408.png`

In the Subway sequence, place the InsideTrain clip at 00:00:03:20 on the same tracks as the OutsideTrain clip to meet the following requirements:

- Use the existing In and Out points on the InsideTrain clip.
- Do not delete any frames in the OutsideTrain clip.

**正解操作**
1. 在 Source Monitor 開啟 InsideTrain，不要改它原本的 In／Out。
2. Timeline 的 playhead 移到 00:00:03:20。
3. 把 source patching（track 左側的 V1、A1 指派）設到和 OutsideTrain 同一組 track。
4. 按 Insert（快捷鍵 `,`）。

**講解**：do not delete any frames in the OutsideTrain clip 的意思是不能覆蓋，所以用 Insert。OutsideTrain 會在 00:00:03:20 被切開，後段往右推，所有 frame 都保留。用 Overwrite 會蓋掉 OutsideTrain 的 frame。主檔 PPT 版本還有第 3 條要求（現行解題本寫成 sequence 結束於 00:00:15:06），考試截圖沒有這條，待補拍確認。

### B17｜Create a frame hold
來源：`151242.png`；對照 `151250.png`

In the airshow sequence, create a two-second frame hold segment of the airshow footage at 00:00:03:00 so that the video continues when the freeze frame ends. Do not remove any of the original footage.

Note: Use a method other than time remapping.

**正解操作**
1. playhead 移到 00:00:03:00，選取 airshow clip。
2. 按右鍵，選 Insert Frame Hold Segment。
3. frame hold segment 預設是 2 秒，確認長度是 00:00:02:00。

**講解**：Insert Frame Hold Segment 會在指定位置插入一段 frame hold，frame hold 結束後原 video 接著播，後段往後推，原始畫面一格都不少。Add Frame Hold 會讓 playhead 之後全部變成 frame hold，不符合 video continues。題目的 Note 明確禁止 Time Remapping；現行解題本把它列為替代做法，這裡已刪除。

## Aspirations 專案

### B21｜Prepare for publishing
來源：`152309.png`

You need to prepare to export the first 30 seconds of the ArtistInterview. Ensure the sequence meets the following specifications:

- Only the audio from tracks A2 and A3 is audible.
- Use sequence in and out points to ensure only the first 30 seconds of the sequence will export.

Do not delete any content from the project or the timeline.

Note: Do not export the sequence.

**正解操作**
1. 在 A1 和其他 A2、A3 以外的 audio track 按 M（Mute）。也可以改按 A2、A3 的 S（Solo）。
2. 在 Timeline 把 playhead 移到 00:00:00:00，按 I 設 In point。
3. playhead 移到 00:00:30:00，按 O 設 Out point。

**講解**：only audible 用 Mute／Solo 處理，不能刪除 audio（do not delete any content）。sequence in and out points 要在 Timeline 或 Program Monitor 設定，不是在 Source Monitor 設 clip 的 In／Out。最後不要按 Export。

### B22｜Organize assets
來源：`152423.png`

Create bins named images and videos. Place images in the images bin and videos in the videos bin.

Note: You can click the underlined text to copy it. If a dialog is opened during the task, the text must be copied before the dialog is opened.

**正解操作**
1. 在 Project panel 建兩個 New Bin，分別命名 images 和 videos。
2. 把 still image 拖進 images，把 video 拖進 videos。

**講解**：bin 名稱要和題目完全一樣，都是小寫。分不出類型時，切到 List View 看 Media Type 或 Frame Rate 欄位：still image 沒有 frame rate。sequence 不屬於 images，也不屬於 videos，留在原處。

### B42｜Create a sequence
來源：`152118.png`

Create a sequence that meets the following requirements:

- Name: Promo
- Preset: HD 1080p 25 fps (HDV 1080p25)
- Tracks: Three video and two audio tracks.

You do not need to add content to the sequence.

Note: You can click the underlined text to copy it. If a dialog is opened during the task, the text must be copied before the dialog is opened.

**正解操作**
1. 選 File > New > Sequence。
2. Sequence Presets 分頁選 HDV > HDV 1080p25。
3. 切到 Tracks 分頁，Video 設 3，Audio 設 2。
4. Sequence Name 輸入 Promo，按 OK。

**講解**：preset、track 數、名稱三項都要對。track 數在 Tracks 分頁設定，建立後再手動加 track 也行，但最容易出錯。同專案另一題 B23（主檔版本）是 HDV 720p30，兩題很像，不要記混。

## Africa 2 專案

### B27｜Interpret the clip
來源：`IMG_4789`；對照 `IMG_4847`

Interpret Jackal.mp4 so that the new frame rate is 24.

**正解操作**
1. 在 Project panel 對 Jackal.mp4 按右鍵，選 Modify > Interpret Footage。
2. Frame Rate 選 Assume this frame rate，輸入 24，按 OK。

**講解**：interpret 是改變 Premiere 解讀素材的方式，作用在 Project panel 的原始 clip。Timeline 上的 Speed/Duration 只改那一次使用，不是本題要的。

### B28｜Create a rough cut
來源：`IMG_4790`；對照 `IMG_4846`

Set In and Out points on the clips based on the table.

Starting at 00:00 place the clips on track V1 in the Rough Cut sequence by Clip Order with no gaps between the clips

AFRICAN T 120.WAV should replace audio for all three clips on A1.

| Clip # | File Name | Source Timecode Used | Notes |
|---|---|---|---|
| Clip 1 | Elephant.mp4 | 01:00 – 03:00 | Add to timeline |
| Clip 2 | Hippos.mp4 | 02:09 – 03:24 | Add to timeline |
| Clip 3 | Giraffe.mp4 | 00:00 – 03:12 | Add to timeline |
| Audio | AFRICAN T 120.WAV | 03:27 – 10:27 | Overwrite existing audio |

**正解操作**
1. 依表格逐一在 Source Monitor 開啟三段 video，設 In／Out。
2. 從 Rough Cut sequence 的 00:00 開始，依 Clip 1 → 2 → 3 的順序接在 V1 上，中間不留 gap。
3. 在 Source Monitor 開啟 AFRICAN T 120.WAV，設 In 03:27、Out 10:27。
4. source patching 只開 audio、指到 A1，playhead 回到 00:00，按 Overwrite（快捷鍵 `.`）。

**講解**：表格 Notes 寫 Overwrite existing audio，所以音樂用 Overwrite 蓋掉三段 video 原本的聲音，不能用 Insert。video 的 source patching 要關掉，否則會連 video 一起蓋掉。

## Kittens 專案

### B29｜Adding Clips to a Rough Cut
來源：`IMG_4793`；對照 `IMG_4843`

Using the FosterIntro sequence:

- Set the source video Kitten1_Adopt.mp4 to have an in point at 00:10 and an out point of 4:03.
- Put only the video clip on track V1 after clip Kitten1_Pet1.mp4.
- Set the source audio CutePianoStrings.mp3 to have an In point of 00:20.
- Place CutePianoStrings.mp3 on track A3 so that it starts at the beginning and ends at 20:00.

Note: Both video and audio for V1, A2, and A3 on the timeline should end at 20:00.

**正解操作**
1. 在 Source Monitor 開啟 Kitten1_Adopt.mp4，In 設 00:10、Out 設 4:03。
2. 拖曳 Source Monitor 下方的 Drag Video Only 圖示，把 video 接在 V1 的 Kitten1_Pet1.mp4 後面。
3. 在 Source Monitor 開啟 CutePianoStrings.mp3，In 設 00:20。
4. 把音樂放到 A3，起點在 sequence 開頭 00:00。
5. 修剪音樂尾端到 sequence 的 20:00。

**講解**：put only the video clip 要用 Drag Video Only，不要帶入 Adopt 的 audio。ends at 20:00 指的是 sequence 時間碼，不是音樂素材本身的時間。Note 提醒 V1、A2、A3 三條 track 最後都要在 20:00 結束，做完要檢查。

### B30｜Manage clips and tracks
來源：`IMG_4794`；對照 `IMG_4844`

In the sequence FosterIntro:

- Delete only the video of the Kitten1_Bath.mp4 clip.
- Keeping the same start and end times, move the Kitten1_BathWB.mp4 video clip to track V1.
- Link the video clip for Kitten1_BathWB.mp4 to the audio clip for Kitten1_Bath.mp4.
- Remove tracks V3 and A4

**正解操作**
1. 按住 Alt 點 Kitten1_Bath.mp4 的 video，只選 video，按 Delete。
2. 把 Kitten1_BathWB.mp4 的 video 垂直拖到 V1，時間位置不變。
3. Shift 點選 BathWB 的 video 和 Bath 的 audio，選 Clip > Link。
4. 在 V3 track header 按右鍵選 Delete Track；A4 照同樣方式刪除。

**講解**：delete only the video 要用 Alt 只選 video，直接點會連 audio 一起刪。移動 BathWB 時只能上下移，不能左右偏移。Link 的對象是 BathWB 的 video 和原本 Bath 的 audio，兩個不同 clip 的零件組成一組。

## Fitness World 專案

### B31｜Auto reframe the sequence
來源：`IMG_4824`；對照 `IMG_4796`

Auto Reframe the sequence with the following settings:

- Vertical 4:5
- Slower Motion
- Do not nest clips.
- Leave the default name.

**正解操作**
1. 在 Project panel 選取 sequence，選 Sequence > Auto Reframe Sequence。
2. Target Aspect Ratio 選 Vertical 4:5。
3. Motion Tracking 選 Slower Motion。
4. Clip Nesting 選 Don't nest clips。
5. Sequence Name 不改，按 Create。

**講解**：三個設定剛好對應對話框的三個欄位，照順序選即可。Auto Reframe 會另外建立一個新 sequence，原 sequence 保留。

### B40｜Remove unused assets
來源：`152541.png`

Remove all the unused assets from the project.

**正解操作**
1. 點一下 Project panel，讓它成為作用中的面板。
2. 選 Edit > Remove Unused。

**講解**：Remove Unused 會移除沒有被任何 sequence 使用的 project item，只是從專案中移除，硬碟裡的檔案不會被刪。不要一個一個手動刪，容易漏掉或誤刪。

## Commute 專案

### B32｜Modify the timeline
來源：`152925.png`；對照 `IMG_4798`、`IMG_4822`

Rename the sequence to Daily Commute and unlink the audio from the commute1 clip.

**正解操作**
1. 在 Project panel 對 sequence 按右鍵 Rename，輸入 Daily Commute。
2. 在 Timeline 選取 commute1，選 Clip > Unlink。

**講解**：改名要改 Project panel 裡的 sequence 項目。Unlink 後 video 和 audio 可以分開選取，位置不變。

### B41｜Fill the timeline gap
來源：`153009.png`

Delete the commute3 clip from the timeline.

Lengthen the commute4 clip to fill the gap on the timeline without using generative extend.

**正解操作**
1. 選取 commute3（video 和 audio），按 Delete。gap 會留著，不要用 Ripple Delete。
2. 開啟 Snapping，把 commute4 整段往左拖，貼齊前一段 clip 的結尾。
3. 拖曳 commute4 右側的 Out 邊緣往右延長，貼齊後一段 clip 的開頭。

**講解**：lengthen 是把 clip 拉長，所以不能用 Ripple Delete 直接合上 gap。commute4 的 In point 已經在素材最開頭，左邊沒有多餘畫面可以拉，所以先整段左移，再從右邊延長。不能用 Rate Stretch 改速度，也不能用題目禁止的 Generative Extend。

## Africa 專案

### B33｜Delete pauses
來源：`IMG_4812`；對照 `IMG_4826`、`151644.png`

Open the Sequence named Hyena-Rock.

In the transcript, set minimum pause length to 1 second.

Filter and delete all pauses.

**正解操作**
1. 開啟 Hyena-Rock sequence，到 Text panel 的 Transcript 分頁。
2. 從 ⋯ 圖示開啟 Transcript view options，把 Minimum pause length 設為 1 秒。
3. 按 Filter 圖示，選 Pauses。
4. 按 Delete all，選 Extract。

**講解**：minimum pause length 決定多長的停頓才會被列為 pause，題目指定 1 秒。刪除時選 Extract 會讓後方內容往前補；選 Lift 會留下 gap。要在 sequence 的 transcript 操作，Source Monitor 的 transcript 是唯讀的，不能刪除。

### B38｜Change the sequence
來源：`151516.png`

Use auto reframe to create a 9:16 version of the African Animals sequence.

**正解操作**
1. 在 Project panel 選取 African Animals，選 Sequence > Auto Reframe Sequence。
2. Target Aspect Ratio 選 Vertical 9:16，其他欄位保持預設，按 Create。

**講解**：create a 9:16 version 是另外產生一個新版本，原 sequence 保留。題目沒指定的 Motion Tracking 和 Nesting 都用預設值。

### B39｜Reconfigure the sequence
來源：`151854.png`

Rename the sequence Maasai Mara to Zebras.

In the timeline:

- Delete all unused tracks.
- Mute the Zebras.mp4 audio.

**正解操作**
1. 在 Project panel 把 Maasai Mara 改名為 Zebras。
2. 開啟 sequence，選 Sequence > Delete Tracks，勾選 Video Tracks 和 Audio Tracks 的 All Empty Tracks，按 OK。
3. 在 Zebras.mp4 所在 audio track 的 track header 按 M。

**講解**：unused tracks 是沒有任何 clip 的 empty track，Delete Tracks 對話框可以一次刪掉全部 empty track。題目專案刪完 empty track 後，那條 audio track 只剩 Zebras.mp4，所以按該 track 的 M 即可。

## School 專案

### B34｜Adjust Audio Tracks in a Sequence
來源：`IMG_4814`；對照 `IMG_4829`

In Study Session sequence:

- Add StudyMusic.mp3 to track A2
- Adjust the length of the StudyMusic.mp3 clip on the timeline to match the length of the video clips.
- Mute the audio on track A1.

**正解操作**
1. 把 StudyMusic.mp3 拖到 A2，起點對齊第一段 video。
2. 開啟 Snapping，拖曳音樂的尾端，貼齊最後一段 video 的結尾。
3. 按 A1 track header 的 M。

**講解**：adjust the length 是修剪音樂長度，不是改播放速度，所以不要用 Rate Stretch。mute the audio on track A1 是按 track 的 M，不是刪除 A1 的 audio。

## Pizza Time 專案

### B35｜Remove section
來源：`150430.png`

Change the all clips sequence as follows:

- Set an in point at 2:43:00 seconds and set an out point at 2:48:00 seconds.
- Remove that section of the timeline.
- Do not leave any gap or extend any clip.

**正解操作**
1. 開啟 all clips sequence，playhead 移到 00:02:43:00，按 I。
2. playhead 移到 00:02:48:00，按 O。
3. 按 Program Monitor 的 Extract（快捷鍵 `'`）。

**講解**：do not leave any gap 就是 Extract，和學科 A30 是同一個觀念。Lift（`;`）會留下 gap。題目的 2:43:00 是 2 分 43 秒，all clips sequence 全長約 2 分 49 秒。

### B36｜Manage clip markers
來源：`150605.png`

On sequence pizza build, complete the following tasks:

1. Delete all the current markers.
2. Add a timeline marker named cutting overhead at 17:06 and set the marker duration to 5 seconds.
3. Change the marker color to white (#FFFFFF).

Note: You can click the underlined text to copy it. If a dialog is opened during the task, the text must be copied before the dialog is opened.

**正解操作**
1. 開啟 pizza build sequence，點一下 Timeline 讓它成為作用中面板，選 Markers > Clear All Markers。
2. 取消選取所有 clip，playhead 移到 00:00:17:06，按 M。
3. 雙擊 marker 開啟 Marker 對話框，Name 輸入 cutting overhead，Duration 輸入 00:00:05:00，Color 選 White，按 OK。

**講解**：題目要的是 timeline marker（sequence marker），所以要在沒有選取 clip 的狀態下按 M。選了 clip 再按，會變成 clip marker。marker 名稱建議在開對話框前先複製題目底線文字。

## Social 專案

### B37｜Nest the clips
來源：`150955.png`

Open the sequence Social Title for Nesting.

- In the Sequence for Nesting bin, place the clips from the Keith_Company_Role 1920x1080 bin on the timeline.
- Place the longest clip on track V1, beginning at 00:00, the shortest clip on V3, and the medium length clip on V2.
- Position the clips on V2 and V3 so that they end at the same timecode as the clip on V1.
- Nest the clips and name the nested sequence Nested Name + Title.
- In the bin, change the label color of the nested sequence to Cerulean.

Note: You can click the underlined text to copy it. If a dialog is opened during the task, the text must be copied before the dialog is opened.

**正解操作**
1. 開啟 Social Title for Nesting sequence。
2. 在 Keith_Company_Role 1920x1080 bin 用 List View 看 Duration，找出最長、中等、最短的 clip。
3. 最長放 V1，起點 00:00；中等放 V2；最短放 V3。
4. 開啟 Snapping，整段移動 V2、V3 的 clip，讓結尾都對齊 V1 的結尾。
5. 框選三個 clip，按右鍵選 Nest，名稱輸入 Nested Name + Title。
6. 在 Project panel 找到新的 nested sequence，按右鍵 Label > Cerulean。

**講解**：對齊結尾要移動整段 clip，不能修剪長度。label 顏色要改 Project panel（bin）裡的 sequence 項目，Timeline 上那段 nested clip 的顏色不算。

---

## 未收錄（只有主檔 PPT，待補拍）

術科 9 題：B06、B08、B09、B16、B18、B19、B20、B23、B24
