# gen-image 來源到 HTML 忠實度自審

- 審查時間：2026-10-22（Asia/Taipei）
- 執行者：author-self-check
- 範圍：CH1-1、CH1-2、CH2-1、CH2-2、PRAC2、CH3-1、CH3-2、PRAC3、CH4-1、CH4-2、CH4-3、PRAC4、CH5-1
- 方法：逐單元對照正式 `_lessons/gen-image/{id}.md`、learner-facing HTML 與實際連結素材；本輪重點核對 Deep Review 修補涉及的 4 份來源與 9 個 HTML

## 對照結果

- PRAC2／3／4 的核心任務、離線路徑與完成門檻未因加入保存／匯出控制而改寫；來源同步提醒換裝置前下載或複製紀錄。
- CH5-1 來源與 HTML 都要求 3 張系列完稿、由 A 反推 L2 線稿、以 L2 產出／核對 B／C、執行一次局部修改、完成系列 QA 與 release gate。
- CH5-1 主路徑與 OFFLINE-01 都保留相同必要證據；時間不足只可標記未完成，不能降為單張體驗。
- 案例 D 在來源與 HTML 均使用「島嶼慢旅（虛構品牌）」及虛構路線，沒有以合成地景暗示真實目的地。
- 學員頁的可填內容、複製與 JSON 下載控制都位於既有 `.lesson-body` 內，沒有把審查、備份或內部檔案暴露為學員主流程。
- index 對 module1–module5 的入口、Markdown 文件連結文字與實際 href 已同步；未用不存在的 fragment 假裝能定位。

## 結論與限制

來源到 learner-facing HTML 的本輪變更可判為 PASS。這是作者自審，只證明版本忠實度；不替代獨立內容複審、真人 cold follow-along 或登入第三方平台實測。
