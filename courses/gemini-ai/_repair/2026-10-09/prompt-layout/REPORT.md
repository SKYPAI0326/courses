# 提示詞欄位排版修補結果

task_scope: layout-only。已套用本機，未commit／push。

40個教材頁的提示詞欄位套用coldtone-prompt-layout樣式；另同步_source/coldtone-styles.json與_tools/coldtone_styles.py，重新產生時會保留。桌機外層24px、手機18px／16px內距；標題16px／700、說明14px，字距改為.02em；預格式文字及複製列各有自己的間距。原本4組prompt-header去除重複padding，DOM不動。

40頁文字快照／pre全文／script／metadata／連結與資源比對PASS；兩套結構檢查各40頁0 blocked。40頁lint修前及修後均為0 BLOCKER／0 ERROR／32 WARN；語意審查原狀保留。

代表頁CH1、CH2、CH3、CH4、PRAC1-1、SUPP4-3、PG01，各1440／390／430，21組檢查無整頁或提示詞欄位溢出，所有說明欄位的標題皆大於說明。7個實際複製操作，剪貼簿文字逐字相同。手機截圖取測試分頁，量測innerWidth=390、clientWidth=375、提示詞335px；桌機截圖取目前使用者本機CH1分頁。viewport已重設。

備份42檔：_backup/2026-10-09-prompt-layout-pre；before/after SHA與精確範圍在changed-files.json。coldtone靜態比對JSON在/private/tmp/gemini-prompt-layout-review-20261009。人工版面確認待使用者檢視截圖；未測頁未冒稱逐頁瀏覽器通過。
