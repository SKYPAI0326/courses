# Canva Deep Review 修復報告

日期：2026-10-22

## 結果

Deep Review Judge 接受的六項已在機器可驗證範圍內修正：

1. 證據：更新 outline 與 153 個 artifact snapshot，新增 7 筆現行紀錄。validator 由 `BLOCKED` 改為 `MACHINE_READY_PENDING_HUMAN`，0 error、4 筆有效 PASS 證據。
2. 38 秒分支：CH2-3 改讀學員的實際片段起點，分開說明 36 秒、38 秒與較短版本；36 秒配樂不再被描述為必然覆蓋全片。
3. EXT1：改為 `platform_required: true`，平台狀態維持 PENDING。
4. 離線包：依目前 28 個 HTML、搜尋索引、CSS、JavaScript、素材與下載重建；排除已由個別素材完整包含的巢狀 `canva-media-pack.zip`，避免離線包重複膨脹。
5. 無 v1 路徑：CH2-1 加入現有 36 秒 MP4 平面備援，可接續聲音、字幕與匯出；頁面明示不能分層修改原文字與背景。完整分層重建改列為單元前置工作，不塞入 10 分鐘。
6. Gate：更新為 2026-10-22 的實際內容、技術、證據、平台、真人與 Git 狀態。

## 驗證證據

- 修正前驗收：46 項失敗，涵蓋六項裁決。
- 修正後裁決驗收：`PASS: all Deep Review machine-verifiable acceptance checks`。
- 靜態檢查：28 頁；25 個來源對照頁；676 個本地連結；0 issue；lint、結構、substance 皆 exit 0。
- ZIP：離線包 128 entries、媒體包 53、練習包 8、文字包 16；CRC 均通過。
- 備援影片：`footage-v1.mp4` 為 36.0 秒。
- 還原演練：14 個備份檔在隔離目錄逐一通過 SHA-256。
- `git diff --check`：通過。

瀏覽器工具因安全政策不允許開啟 `file://`，所以沒有把 GUI 截圖當成完成證據；HTML 結構、來源保真與本地連結已由上述工具驗證。

## 尚待驗證

- CH2-1 平面備援在 Canva 的實際匯入時間與零基礎跟做。
- 38 秒版本的 Canva 全流程操作。
- EXT1 WhisperDesktop 安裝、模型下載與實作。
- 真人冷讀、連續跟做、計時、理解、轉用與接收者權限。

## 回復方式

備份：`_backup/2026-10-22-deep-review-fixes-pre-repair/`

還原：`python3 _tools/restore-2026-10-22-deep-review-fixes-pre-repair.py`

本次修復檔案採顯式 staging；提交與推送結果以本報告所屬 Git 歷史及 `origin/main` 為準。未重新執行網站發布驗證。
