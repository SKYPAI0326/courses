# M2 審查紀錄：攝影與影片編修（CH2-1～CH2-7、PRAC2）

**檢查日期**：2026-09-16

**目前狀態**：MACHINE_READY（文字工作流與下載／閱讀資產）；人工冷跟做 PENDING；Affinity／OpenShot 實機與影音示範仍 BLOCK。

## 本輪完成

- 8 個單元主頁改由 `_lessons/digital-content-growth-126h/` 的 Markdown 來源重建。
- 8 個核心學員工作表改成與影像企劃、素材來源、剪輯決策及交付索引對應的欄位。
- 建立 20 個可在瀏覽器閱讀、也能下載 UTF-8 原始檔的附件頁。
- 補上影像任務案例卡、素材來源／AI 紀錄、受眾訊息案例、平台格式卡、授權條件案例、工具課前檢查、輸出檢核、剪輯音訊參考與 PRAC2 評量規準。
- 修正附件頁的返回路徑：附件會回到所屬單元，不會回到不存在的同名頁面。

## 自動證據

- `python3 _tools/test_learner_render_contract.py`：6 tests OK。
- `python3 -m py_compile _tools/rebuild-learner-shell.py _tools/test_learner_render_contract.py`：通過。
- 26 個 M2 主頁／附件頁：本地連結 0 錯誤、內部製作語句 0 筆、重複 h2 0 筆。
- `git diff --check`：通過。

## 尚不能提交的部分

以下內容不能以文字模板取代，仍維持 BLOCK：

1. Affinity Windows 的實際版本、安裝／取得路徑、個人帳號啟動與重開測試。
2. Affinity 可編輯 starter file、圖層、示例素材與輸出檔。
3. OpenShot Windows 的實際版本、素材匯入、字幕、音訊、主版／短版輸出與專案重開測試。
4. 可播放的 15／30 秒影音示範、音訊示例與課程端來源紀錄。
5. 人工冷跟做：從 CH2-1 開始，依附件閱讀版與下載檔完成一輪，再由下一單元接手。

## 人工冷跟做順序

1. CH2-1：用備援 Brief 完成影像任務判斷表，對照四項任務案例卡。
2. CH2-2：把 CH2-1 的任務轉成受眾定位卡，檢查核心訊息、證據與內容角度是否一致。
3. CH2-3～CH2-4：完成分鏡、格式選擇與素材來源判斷；任何來源不明項目先標待確認。
4. CH2-5～CH2-7：先走文字／檢核備援，再依課前實測結果決定是否進入 Affinity／OpenShot 本機操作。
5. PRAC2：只採用狀態可追溯的資產，完成 README、交付索引、同儕接手與修正紀錄。

人工跑完以前，本模組不標示為可販售或可正式上線。
