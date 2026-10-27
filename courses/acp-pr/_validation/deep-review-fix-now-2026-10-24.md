# Deep Review `fix_now` 修正紀錄

- 日期：2026-10-24（Asia/Taipei）
- 裁決：`_review/deep-review/2026-10-24-production-handout/judge-ruling.md`
- 執行範圍：只處理 Judge 判為 `ACCEPT + fix_now` 的七項；未做第二輪 Deep Review。
- 整體狀態：`BLOCKED`

## 已完成修正

1. 將原有基礎 starter 原樣封裝為 `assets/ai-short-video-editing/premiere-foundation-starter.zip`，首頁與 CH0-1 提供實際下載入口。
2. CH0-2 在複製練習副本前，明示建立與核對三段、36 秒起始序列。
3. CH0-2 與練習卡依 inclusive Out 校正為 `00:00:03:01`、`00:00:02:01`。
4. CH1-3 保留 SRT 毫秒來源標記，另列三組 Windows 實測的 25 fps Premiere 影格時間碼。
5. CH0-3 的平台聲明縮限為六類介面入口，未宣稱固定五題與代表練習終態均已通過。
6. CH0-4、完成紀錄與 CH1-4 統一為 Q1～Q4 全數完成並通過。
7. CH1-2、CH1-4 明示外部生成式 AI 服務待核准，目前使用教師固定輸出。

## 確定性驗證

- ZIP：解壓至暫存目錄後以 `diff -r` 比對原 starter，9 個檔案完全一致；ZIP 內無絕對路徑或 `..`。
- 時間碼算術：25 fps 下 `02:00–05:00` 為 76 格＝`03:01`；`14:00–16:00` 為 51 格＝`02:01`；固定三段各 208 格，共 624 格＝`24:24`。
- V4 lint：正式 9 頁，BLOCKER 0、ERROR 0、WARN 0。
- HTML structure：正式 9 頁，`checked=9 blocked=0`。
- Substance：正式 9 頁逐頁 `block=0`、`missing_assets=0`；此檢查不替代語意審查。
- Copy continuity：正式 9 頁均 0 warnings；仍保留人工判斷責任。
- Browser smoke：390×844、820×1180、1440×900，9 頁共 27 組全部通過；無頁面級水平溢位、header 遮擋、缺少唯一 main／learner root／h1 或 skip-link 失效。
- 搜尋索引：執行 `python3 docs/build-search-index.py`，寫入 2211 筆。
- ZIP SHA-256：`ebaf37e16caf09c335813da3d0a556138403f78788d649f92fdea6712bcaf4c5`。

## 仍未解除的阻擋

1. CH1-2 允許修改起訖或重排候選，但 CH1-3 尚無一個客製決策後字幕重映射的完整方法與完成證據。
2. CH0-3 代表練習仍缺完整軌道數、圖片與 Scale／Opacity 數值、可用音訊與對齊依據，以及相應終態證據。

另有未知：凍結材料未含原始題庫 PPTX，不能獨立確認 77 頁與 B08／B09／B19 刪題狀態；零基礎 5 小時 cold follow-along 尚未執行。

## 證據邊界

既有 Windows Premiere 平台紀錄保留為修正前版本的歷史路徑證據。這次只完成文字、封裝、算術、連結與瀏覽器檢查，未把新文字版本標成已重新完成 Premiere 平台重跑。
