# 零基礎講義修訂結果

日期：2026-10-09。內容修訂已完成；瀏覽器操作、平台新提示詞實跑、真人理解與時間驗證仍待完成。本次沒有commit或push。

## 改了什麼

| 範圍 | 結果 |
|---|---|
| 課程入口／單元頁 | 以作品與第一步介紹各章，刪減密集的規格與時間說明 |
| CH1 | 精簡開場、示範與操作；主線先用白話說明LLM與搜尋用途；補工具送出／複製／保存啟動卡；完成檢查集中最後 |
| CH2 | 八列契約縮成三件開始資訊；必做整理為五步；選做集中課後區；必答題改用Email；一次補限制後仍錯可依原文人工收尾 |
| CH3 | 補第一份文字來源的加入方法（依[Google官方新增來源說明](https://support.google.com/gemininotebook/answer/16215270?hl=zh-Hant)確認），以及一筆回原文核對示範；分清來源沒寫和原文明說尚未做；備援與恢復拆開 |
| CH4 | 主要說明與提示使用案例／方案名稱；字數只作模型縮稿參考，學員核對列印一頁、算式和待確認；保留完整原資料與計算 |
| Gamma | 新增一個文字下載區，選用途後保存來源／大綱／貼入文字；自帶企劃可用小標題或原句定位；保留十頁生成、修訂與PDF重開流程 |
| 教案／支援文件 | 同步五份正式學員正文、Style Guide、Blueprint、啟動卡及五個提示／檢查原檔；舊平台觀察移教師區並明示是歷史記錄 |
| 示範PDF | 加入資料夾內精確忽略例外，兩份PDF已可被Git納入；仍需提交、push及線上取用確認 |

二十個既有檔案在動手前完整備份。原共享CSS與情境素材頁的使用者修改保持原樣。案例原文、數字與作者參考未刪減。

## 驗證

- 七頁HTML結構通過，包括CH2原先兩處無效`</br>`已修正。
- 七頁lint為0 BLOCKER、0 ERROR；剩3 WARN：CH1範例信件的「您」、CH1與CH2既有hover效果。敬稱保留於客戶信件；這次不更動視覺樣式。
- 五頁素材檢查沒有缺檔；機器的semantic_review仍是PENDING，不能用它取代真人理解測試。
- 185個頁內／相對連結檢查沒有檔案或錨點缺失。
- 五項改過的頁內提示／檢查與下載原檔一致；五份教案學員正文與HTML文字一致。
- 原案例、示範與參考的文字payload保留；只更動核准範圍內的五個提示／檢查payload。
- 原工作台輸入欄位、必做checkbox、既有腳本均保留；暫存鍵沒有更動。共享CSS與情境素材頁的雜湊未變。
- Gamma下載腳本測試通過：空白輸入會停止；中文與換行完整保留；依用途選檔名；下載物件URL釋放。這是腳本測試，尚未完成當前瀏覽器點擊／下載測試。
- 以站內搜尋產生器核對七筆title／description，與現有索引相同；未改寫全站索引或其他課程。
- 主要說明段落的跨頁完整重複審查：沒有同一段落出現在超過兩頁；Activity Identity仍是五種不同作品與判斷。
- `git diff --check`通過。具體前後文字及DOM位置見[具體文字變更](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/_repair/2026-10-09-readability/CONTENT-CHANGES.json>)；當次檔案版本見[當次檔案版本](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/_repair/2026-10-09-readability/final-manifest.json>)。

## 本次審查問題對應

| 審查項目 | 本次狀態 |
|---|---|
| B01 發放PDF | 本機設定已修；發布後取用驗證待辦 |
| M01 工具、來源、存檔橋接 | 教學步驟已補；逐人帳號與入口可用性待講師確認 |
| M02 重複成果與內部規格 | 已精簡主線，版次與歷史觀察留教師區 |
| M03 選做與必答不一致 | 已對齊必做Email；選做集中 |
| M04 人工收尾矛盾 | 已統一為補限制一次後可依原文人工完成並保存 |
| M05 案例／方案重名 | 主要解說與提示使用完整名稱；原資料字母編號保留供對照 |
| M06 術語過密 | 操作改中文動詞；必要名詞先定義與示範 |
| M07 自帶企劃來源編號 | 大綱提示與檢查已支持標題／原句定位 |
| M08 初學者時間 | 待真人試跑，已備講師清單，沒有宣稱時間已通過 |
| N01–N04 | 已調整字數驗收、選做標題、殘句、長段及無效br |

## 未完成與負責人

1. 講師：用[講師試跑清單](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/_repair/2026-10-09-readability/HUMAN-TRIAL.md>)安排零基礎者各自完成。保留十二小時與每人獨立原則，不增加學員測試表。
2. 當前瀏覽器／實際帳號：驗桌面1440px及手機390／430px、剪貼簿、文字下載、暫存恢復、NotebookLM來源加入與引用、Gamma生成與PDF匯出。受本次本機頁面存取限制，沒有browser smoke證據。
3. 新提示詞：改過的Gamma大綱與CH4提示需平台實跑；舊帳號成功記錄不當成新版PASS。
4. 發布：尚未commit／push；兩份PDF須隨本批提交。發布後從實際網址開啟，確認十頁可讀。

## 操作文件與還原

- 計畫：[修訂計畫](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/_repair/2026-10-09-readability/REPAIR-PLAN.md>)。
- 教師試跑：[講師試跑清單](</Users/paichenwei/Library/Mobile Documents/com~apple~CloudDocs/01-PROJECTS/課程專用網頁/courses/ai-beginner-practical/_repair/2026-10-09-readability/HUMAN-TRIAL.md>)。
- 備份：`_backup/2026-10-09-pre-readability/`。
- 還原：`bash _tools/restore-2026-10-09-pre-readability.sh --dry-run`先看範圍；要回復時使用`--apply`。還原會保留修訂前的使用者修改，不會重設Git或其他課程。
