# 提示詞欄位排版修補

task_scope: layout-only

使用者指出提示詞色塊邊緣無留白，標題小於說明。現況CH1外層padding=0，標題11.2px／500，說明14.4px。依course-html-contract與coldtone-html保留可見文字、提示詞逐字內容、DOM、連結、腳本與門禁。

範圍：40個非转向教材頁的.lesson-body .prompt-wrap，以及樣式設定和套用工具。保留各頁既有配色，僅調整元件padding、標題字級／字重／字距、說明間距、正文內距及複製列間距。既有標題內包prompt-header的4組去除重複內距；不移動節點。

先CH1試作，驗證標題16px大於14px说明，桌機24px外層內距、手機18px／16px。再套用同類頁。全部做文字／pre／script／href保護及結構檢查；按直接標題、header標題、舊案例與新遊樂園四種結構選桌機1440與手機390／430瀏覽器檢查，實際測複製。

備份：_backup/2026-10-09-prompt-layout-pre。當次修改未另獲push指示，先提供本機修正版。
