# 參考素材索引

本目錄先記錄素材位置與用途，不直接複製含 credential 或個資的原始檔。

## 已確認素材

1. **Make 藍圖：Google Sheets＋Gemini（4 模組基準）**
   - 課程資產：`../assets/CH1-1-reference-4module.sanitized.blueprint.json`
   - 原始檔（教師核對用）：`/Users/paichenwei/Downloads/Integration Google Sheets, Google Gemini AI.blueprint.json`
   - 教學用途：資料來源、位置鍵、單一 `result` 輸出、文件與通知映射。
2. **Gmail 收信類來源替換**
   - 課程資產：CH1-1 只使用欄位轉移註記，不要求匯入第二份 Blueprint。
   - 教學用途：比較 `sender`、`subject`、`body` 如何取代 Sheets 來源欄位，同時保留後續 `result` 映射。
3. **淡江大學生成式 AI 工作坊素材資料夾**
   - 位置：`/Users/paichenwei/Library/CloudStorage/GoogleDrive-sky8697@gmail.com/我的雲端硬碟/2026_淡江大學生成式AI工作坊/初階工作坊（雲端）`
   - 教學用途：確認初階受眾、免費工具前提與工作坊情境。
4. **課程招生文案**
   - 位置：`淡江大學生成式AI工作坊-招生頁課程介紹與課程大綱.md`
   - 教學用途：招生定位與學習成果參考，不取代正式教案。

## 素材處理規則

- 任何匯入課程的 JSON 必須先移除 credential、token、固定帳號、固定資料夾 ID 與個資。
- 原始藍圖只作為教師核對案例；學員使用 `assets/` 的去敏版本與本頁示範，不直接開啟含工作區識別的原始檔。
- 若無法提供真實連線，改用教師提供的去敏 JSON、測試資料與固定輸出完成練習。
