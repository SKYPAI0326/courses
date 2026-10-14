# Canva 教學短片製作

兩場各 150 分（140 學習＋10 休息）。第一場實拍剪接；第二場真人／Canva AI 配音、音量、字幕及學生任務。

## 講義與素材

- [課程總覽](index.html)、[第一場](module1.html)、[第二場](module2.html)。
- [時間軸與字幕實作](resources/時間軸與字幕實作.html)：真實物件選取、改片長重排、獨立 WAV 字幕與實際 Canva 成品。
- [Canva 功能與技巧](resources/Canva功能與技巧.html)：21 工具、六技巧與免費替代。
- [配音與聲音製作](resources/配音與聲音製作.html)：子晴／彥廷同稿短樣、Lisa 英文、九句 WAV 及接句修復。
- [四片段底稿接續](resources/三頁起始檔.html)、[概念比較完整案例](resources/案例與腳本.html)、[學生工具操作規準](resources/學生製作任務.html)。
- [素材與成品](resources/素材與成品.html)：Canva 直接匯出四片段 MP4 與先前本機合成對照。
- [實拍包](downloads/canva-stock-practice.zip)、[文字包](downloads/canva-text-pack.zip)、[影音包](downloads/canva-media-pack.zip)、[離線講義](downloads/canva-handouts-offline.zip)。

## 本地預覽

從本課目錄執行 `python3 _tools/serve-preview.py --port 8765`，再開啟 `http://127.0.0.1:8765/index.html`。這個預覽工具支援影片所需的 HTTP byte-range；不要以 `python3 -m http.server` 驗收本課影片播放。

28 個學員頁：總覽三頁、12 核心、EXT1、12 資源。所有修改目前只在本地。

## 狀態與證據

七項內容修正已同步正式來源與 HTML。已在 Canva 直接完成四片段實拍、獨立 WAV 生成及校訂字幕、1080p MP4 匯出；四頁 PPTX 匯入改字、轉影片和時間設定已核對。其餘平台全課、真人自然度與跟做仍 PENDING。本輪未執行程式測試或完整技術驗證，不沿用前輪 PASS。

[總報告](_validation/FINAL-REPORT.md)｜[內容](_review/CONTENT-CONTINUITY-2026-10-11.md)｜[平台](_validation/PLATFORM-CONTINUITY-2026-10-11.md)｜[產物](_validation/TECHNICAL-CONTINUITY-2026-10-11.md)｜[證據](_validation/evidence.json)。EXT1 依原要求只撰寫課後教案。

正式來源：[大綱](../../_outlines/canva-video-teaching.md)、[教案](../../_lessons/canva-video-teaching/INDEX.md)。本輪備份 150 檔；以 `bash _tools/restore-2026-10-11-continuity-pre-repair.sh` 還原清單內檔案並保留新增素材。未提交、推送、發布或全站註冊。
