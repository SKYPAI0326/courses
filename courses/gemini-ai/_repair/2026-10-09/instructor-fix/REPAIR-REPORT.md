# Gemini AI 講師視角修復報告

日期：2026-10-09。授權：使用者「進行修正」。
狀態：本機內容修復及技術／瀏覽器檢查完成；未commit、未push，正式站仍顯示上次部署版本。五章＋29例遊樂園＋13份延伸參考保留。

## 修正內容

| 原問題 | 本次處理 | 可定位位置 |
|---|---|---|
| I01 版本矛盾 | v1生成→v2第三章測過→v3第四章新增；第五章用v3保存A-v3/B-v3新備份，失敗回v2及適用舊備份 | CH3結尾、CH4開頭/修復/結尾、CH5資料夾/還原/README、core-acceptance.csv |
| I02 第1章延伸壓過主線 | 3份完整延伸提示詞移入既有SUPP4-3；原文逐字保留，複製按鈕可用，章內只留入口 | CH1#snake-extensions；SUPP4-3#snake-extensions |
| I03 初次保存缺辨認示例 | 程式起訖與複製範圍表；普通回覆/Canvas分開；Windows/Mac各讀一路；檔名/本機畫面/故障返回點 | CH1#save-open |
| I04 制式重複提醒 | 核心提示詞前改為當次貼回/生成/修改操作短說明；案例旁只留當次設定用途 | 各核心prompt-wrap |
| I05 第2章主線分散 | 一句預算需求→找缺漏→完整規格→立即寫自己需求；另兩完整例選讀，圓點導航只顯主線7區 | CH2#write-own；#calculation-vs-rules |
| I06 案例複製含答案 | 通關、預算、請款案例只留輸入；原答案保留在核對區；E02及預算TXT相依同步 | CH2各case；E02#prompt-budget-case |
| I07 作者備份相容性 | 自製v3只讀自己的相容備份；作者參考品按A/B文字重新填入，再下載它自己的備份 | CH4#ch4-section-3 |
| I08 修復模板薄弱 | 兩份完整假設錯誤紀錄，另附實際/預期與理由，再原資料/另一資料回測；CH4模板包含新增設定 | CH3#ch3-section-6；CH4#repair |
| I09 課內/課後完成點不清 | 課內交付排班；必做課後CSV清理的完整交付不計入45分鐘；期限由講師宣布，完成條件明列 | CH5#handover、#transfer；大綱/入口/素材說明 |
| I10 抽象文案 | 標題改為取程式、存檔、填資料、自己寫需求；英雄區成果與版本明確 | 五章英雄區與正文 |
| I11 詞彙層次與繁中 | CSV表格檔、JSON資料備份、README使用說明就地解釋；必要程式名詞留在給AI的規格 | CH1/3/5首次使用處 |

SOURCE正文、7份HTML、入口文字、相關TXT及兩個ZIP同步。預算示範與請款判斷的長規格保留在選讀區；沒有靠刪掉規則或核對內容縮短篇幅。第二章課內主要交付改為自己寫的需求，不要求生成全部對照例。

## 驗證證據

- fidelity.json：7份正文/HTML逐字、pre、prompt及連結一致。
- static-results.json：9個受影響頁的內部連結/錨點/複製目標/重複id有效；CSS style塊、互動script、密碼關卡script及前後章導覽與備份相同。新增表格沿用core-table-scroll，僅新表格單元格設間距。
- 兩個共用HTML結構檢查器：各7份，0 blocked。
- lint.log：9頁，0 BLOCKER、0 ERROR、5 WARN；5條既有warn未擴增。
- *.substance.log：各頁MACHINE_CHECKED、缺本機素材0；工具語意審查標PENDING，不以它當教學通過。
- browser/results.json：7份×390/430/1440，共21組無整頁橫向溢出；sticky頂欄保留。9個實際複製操作與pre完全相同；預算複製沒有總額答案；新修復提示詞包含開關/班種/上限。五章依序導覽至入口、CH1閱讀位置重開還原均通過。桌面頁首/存檔/修改/頁尾及手機代表畫面已保存。
- copy-audit.json：7份範圍內，超過兩頁的完整共用段落0。Activity Identity表在REPAIR-PLAN.md；五章認知工作分別為操作、需求寫作、查核、修改回測、交付與獨立遷移。
- changed-files.json及*.text.diff：與本次備份比較，不把其他代理人或歷史工作區修改冒稱本次修復。
- git diff --check：本次範圍無空白錯誤。
- 完整TXT/核心ZIP/遊樂園ZIP逐檔字節一致；29例下載提示詞及A/B/答案素材有效，案例總數不變。
- Canvas及Mac保存指引已重對官方文件：
  - https://support.google.com/gemini/answer/16047321?hl=zh-Hant
  - https://support.apple.com/zh-tw/guide/textedit/txted0b6cd61/mac

## 仍待驗與部署

實際Gemini生成、零基礎真人跟做、第三至第五章連續工具交接、CSV獨立製作與360分鐘試教未執行。I03的辨認示例不是實際學員帳號回覆截圖，兩份錯誤紀錄明示假設。課內/課後期限應在授課時宣布。

全站search-index.json位於此課程外，本次未覆蓋；已按現有build-search-index.py產生只更新Gemini、保留其他課程記錄的search-index-candidate.json（74條，含正式講義、入口、工具及既有公開別名），供下次部署檢核後套用。整體教學就緒仍為PENDING，不能由本次機器通過宣告可授課。

## 回復

備份：_backup/2026-10-09-instructor-pre（66檔）。
還原：bash _tools/restore-2026-10-09-instructor-pre.sh。
該腳本只回復本次動過的原有檔，新增2份素材只有內容仍符合本次指紋才移除，已被他人更動則保留。其他修改與本次證據檔不刪。
