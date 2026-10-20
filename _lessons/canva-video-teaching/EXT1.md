---
slug: canva-video-teaching
unit_id: EXT1
title: 用 WhisperDesktop 保存逐字稿與字幕
course_type: skill-operation
duration_minutes: 0
learning_objective: "以既有母片完成本機轉錄、字幕校訂與字幕燒錄，保留來源檔案。"
prerequisites: ["CH2-6"]
style_guide: ../../_outlines/canva-video-teaching.style-guide.md
platform_version: "WhisperDesktop v3.0.1 官方文件 2026-10-11；僅撰寫教案，未實測應用程式"
revision: 2026-10-11
status: DESIGN_COMPLETE_PLATFORM_PENDING
---

## 內部設計（不進學員頁）

能力進展、成果規格與環境繼承自[正式大綱](../../_outlines/canva-video-teaching.md)。本文為正式講義的學員正文來源，平台操作圖與媒體依[資產規格](../../courses/canva-video-teaching/_design/ASSET-SPEC.md)補齊並實測後發布。

本單元成果：以既有母片完成本機轉錄、字幕校訂與字幕燒錄，保留來源檔案。

<!-- learner-content:start -->
# 用 WhisperDesktop 保存逐字稿與字幕

當你需要可另外修改的字幕檔，或想把自己的講解變成文字教材，可以把已完成的有聲母片交給 WhisperDesktop。本課使用 [AtomicError/whisper-desktop](https://github.com/AtomicError/whisper-desktop)。這是課後練習，從你保存的 `姓名_主題_母片.mp4` 開始。

SRT 記錄每段字幕的文字及顯示時間；TXT 保存文字內容。燒錄字幕會將文字固定做進影片畫面，輸出後仍要保留原母片。

## 準備程式與模型

本頁以官方 [v3.0.1 下載頁](https://github.com/AtomicError/whisper-desktop/releases/tag/v3.0.1)作為版本入口。

1. macOS 下載 `WhisperDesktop_3.0.1_universal.dmg`；Windows 一般筆電下載 Universal 版安裝檔或 portable 壓縮檔。確認選的是應用程式，不是 Source code。
2. Mac 開啟 DMG，將 Whisper Desktop 拖入 Applications，再由應用程式開啟。Windows portable 版先解壓縮整個資料夾，再開啟 `whisper-desktop.exe`。
3. 開啟 Model Hub，下載一個支援錄音語言的模型。
4. 中英混合錄音先選多語 `small`；名稱帶 `.en` 的模型只適用英文。記憶體不足時改用多語 `base`。
5. 等模型下載完成，再開始轉錄。之後可重複使用已下載的模型。

**判斷方式：** 模型大小會影響記憶體需求與處理時間；先以能在目前設備完成轉錄的多語模型為準。

**卡住時：** 如果學校裝置限制安裝，先向設備管理人員確認可用方式。保留母片，待可執行程式的設備準備好再轉錄。

## 從母片產生字幕

先指定母片、模型與輸出格式，再開始本機轉錄。

1. 開啟 Transcription Studio，選取你的有聲母片。
2. 選已下載的模型；依錄音設定語言。中英混合內容轉錄後逐句核對兩種語言。
3. 在 Whisper task 選轉錄原語言（Transcribe），保留原本中英文內容。先在「Settings → Outputs」勾選 SRT 與 TXT，確認輸出資料夾；預設會放在母片旁。回到轉錄頁開始處理。
4. 完成後開啟輸出資料夾，找到與母片對應的檔案。
5. 一邊播放母片，一邊檢查字幕文字；把修訂結果另存為 `姓名_主題_校訂.srt`，保留原始輸出。

下面是本課參考母片前兩句的字幕格式。請播放母片核對這兩段時間：

```srt
1
00:00:01,000 --> 00:00:02,291
Where is the library?

2
00:00:04,291 --> 00:00:06,064
It's next to the cafeteria.
```

序號下方是開始與結束時間，最後一行是顯示文字。你的字幕時間必須對應自己的錄音。若某句提早出現，回到該字幕片段修正時間，再重播確認。

下載[字幕校訂練習.srt](../../courses/canva-video-teaching/downloads/字幕校訂練習.srt)，依[操作與檔案技術卡](../../courses/canva-video-teaching/resources/操作與檔案技術卡.md)修正 cafeteria、繁體字與第三句時間，另存後與完整參考字幕核對。

## 製作字幕影片

校訂 SRT 後，把字幕與母片放進 Hardsub Studio，輸出字幕固定在畫面中的版本。

1. 開啟 Hardsub Studio，在影片欄位選 `姓名_主題_母片.mp4`，字幕欄位選 `姓名_主題_校訂.srt`。
2. 確認影片預覽旁出現字幕句子清單；點一句，畫面應跳到相應時間。
3. 選支援繁體中文的字型，位置設為底部中央，先用白字、深色外框及適合影片的字級。
4. 預覽第一句、中央場景及最後一句，確認中英文能顯示，而且沒有遮住教學內容。
5. 輸出設定選 MP4、H.264 及保留原尺寸，檔名設為 `姓名_主題_字幕版.mp4`，開始輸出。
6. 完成後按「Play Exported Video」或到輸出資料夾開啟 MP4，核對開頭、中間及結尾。

**完成檢查：** 輸出的 MP4 有聲音、字幕與完整畫面，字幕時間對應講解而且沒有遮住教材重點。

**卡住時：** 若作業系統阻止開啟程式，先停在提示畫面，請裝置管理人員確認官方來源與可用方式。若找不到模型，回 Model Hub 查看下載是否完成。轉錄太慢時，可依官方硬體說明改用較小模型；結果仍需人工校訂。字幕顯示方框時，更換支援該語言的字型再輸出。

程式的轉錄與影片編碼在本機進行；額外 AI 翻譯使用自行設定的服務，費用和傳送內容依該服務而定。本練習使用本機轉錄與字幕輸出。[功能與資料處理說明](https://github.com/AtomicError/whisper-desktop#privacy)

把 TXT 改成學生可使用的例句或聽力文字前，先對照錄音核對。用學生錄音做字幕練習時，辨識結果有錯要先回聽，再判斷語言表達。

## 先認識一份字幕檔

若還沒有自己的轉錄結果，先用本課參考檔熟悉 SRT 的時間與文字結構。

1. 下載[參考母片](../../courses/canva-video-teaching/assets/media/library-master.mp4)、[對應 SRT](../../courses/canva-video-teaching/assets/media/library-corrected.srt)與[文字稿](../../courses/canva-video-teaching/assets/media/library-transcript.txt)。
2. 用文字編輯器開啟 SRT，對照參考母片讀取字幕時間與文字。
3. 第一次操作時，先用一支短片完成轉錄與播放。
4. 記下程式版本、模型名稱與輸出檔名；自己的轉錄結果另存，不覆蓋參考檔。

**用途：** 保存版本、模型與檔名後，下一次可以從相同設定開始，也能分辨參考字幕與自己的校訂結果。

<!-- learner-content:end -->

## 講師授課筆記（不進講義）

修復：官方 v3.0.1 文件核對；Chrome 阻擋官方安裝檔下載 ERR_BLOCKED_BY_CLIENT，已交由使用者處理，未宣稱應用程式或模型實測完成。
