# gen-image 來源到 HTML 忠實度自審

- 審查時間：2026-10-16（Asia/Taipei）
- 執行者：author-self-check
- 範圍：CH1-1、CH1-2、CH2-1、CH2-2、PRAC2、CH3-1、CH3-2、PRAC3、CH4-1、CH4-2、CH4-3、PRAC4、CH5-1
- 方法：逐單元以正式 `_lessons/gen-image/{id}.md` 對照 `courses/gen-image/{id}.html`，再核對 HTML 實際連結的學員素材。

## 對照結果

- 學習成果、Demo／Together／Solo 任務、必要停止條件與人工驗收未被模板省略。
- CH1 的 AI 線索與人類證據、CH1-2 的主路徑／備援／離線路徑均保留。
- CH2 與 PRAC2 的素材來源、商業使用五問、平台能力檢查與可下載 brief／prompt 素材均保留。
- CH3 與 PRAC3 的自有／授權 reference、角色分工、禁止第三方任意下載與人類判讀均保留。
- CH4 與 PRAC4 的 reference-first、多參考圖、局部編修、差異辨識與人工 QA 均保留。
- CH5-1 的品牌系列整合、健康宣稱佔位符、來源／權利／同意／來源訊號／無障礙／偏見／人工 release gate 均保留。
- 新增下載素材與 course-only reference pack 的路徑可由頁面到達，沒有把審查用備份暴露為學員主流程。

## 結論與限制

來源到 learner-facing HTML 的核心教學內容與必要安全閘門可判為 PASS。這是作者自審，只證明版本忠實度；不替代 fresh reviewer 的內容審查、真人跟做或登入平台實測。

最終補充：PRAC4 的 inline 模板 F／G 已與 `assets/downloads/prompt-templates.md` 對齊；fresh reviewer 在最終穩定快照判定 BLOCKER 0、MAJOR 0、MINOR 0。真人跟做與平台實測仍維持待辦。

