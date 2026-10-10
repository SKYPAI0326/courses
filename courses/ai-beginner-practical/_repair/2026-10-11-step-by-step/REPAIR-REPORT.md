# 全課逐步跟做修正報告

日期：2026-10-11。狀態：**本機內容修正與作者檢查完成；平台帳號實跑及真人跟做 PENDING。未 commit／push。**

## 改了什麼

|範圍|具體修正|
|---|---|
|index／module1|工具準備、各人選一案、示範與操作的閱讀順序；合併重複 CH2 卡，課後整合改成實際工作說明|
|CH1|八個操作階段；三案已填五欄完整提示詞，含各案原文；逐欄保存、修正下拉選單及完整下載重開流程|
|CH2|八階段；補客戶→主管的真正讀者轉換與工作短訊息；欄位名稱／範例同步，首屏先看示範；舊數字引用改為具名入口；新按鈕載入既有複製腳本|
|CH3|八階段；前段只看示範；建立筆記本、三來源、生成回答、點引用、另查兩筆、修訂、保存依正確順序；一筆核對完整寫法|
|CH4|九階段；補訓與交接完整原／新限制驗算；只重算受影響部分；一頁文件、PDF及過程紀錄用途分開|
|Gamma|每階段先指出輸入檔、產出與動作；來源→十頁大綱→十段文字→卡片→PDF；經典入口折疊，修訂與全部卡片匯出／重開明確|
|來源與操作素材|五份教案 learner-content 與 HTML 正文同步；大綱／藍圖、啟動卡、一頁模板、CH2素材包／viewer 同步；新增六份可開啟／下載提示詞|

沒有新增全班共同作業。原案例原文、作者參考、課後選做、工作台資料鍵及原有 inline script 保留。完整新檔及變更 manifest 見 `../../_validation/step-by-step-2026-10-11/changed-files.json`。

## 驗證

|檢查|結果與實際範圍|
|---|---|
|HTML結構|七個主要頁面無阻擋；body／ID／祖先關係／CSS括號檢查通過|
|lint|八個頁面（含素材viewer）：0 BLOCKER、0 ERROR、4 WARN。WARN為既有信件「您」及hover樣式，未改示例用字或無關CSS|
|substance|五份講義：missing_assets=0、block=0；工具本身的 semantic_review 仍為 PENDING，不能當作教學通過|
|連結、複製來源與教案|八頁本機連結及錨點無斷鏈；原 pre[id] 材料保留（工作台兩份示例提示詞依計畫改為新完整輸入）；六份新提示詞與頁面文字相符；五份教案正文保真|
|保存相容性|工作台欄位ID、資料鍵及必填旗標未改；四章實際填入隔離自查資料、按保存、重整復原並下載，重新讀取檔案確認必填內容都在|
|瀏覽器|七頁×1440／390／430＝21組檢查；無水平溢出。五份講義步驟錨點避開頁首與次導覽；CH2桌面四位置、各章／Gamma手機留截圖，共10張|
|複製與文字下載|CH1完整提示詞、CH2工作訊息各實測複製全文；Gamma來源／大綱／貼入文字三種下載均重讀驗全文，共5項|
|瀏覽器程式錯誤|0；使用獨立暫存Chrome及測試通行狀態，未操作個人帳號，不表示密碼流程或外部平台驗證|
|文案與活動審查|author-self-check；全課不同實務判斷保留。超過兩頁的共用長段只有兩種必要工作台提醒，沒有新增重抄作業|
|差異與回復|git diff --check通過；還原腳本bash -n通過。Git diff含本輪前既有改動，本次邊界以備份manifest與changed-files為準|

完整證據位於 `_validation/step-by-step-2026-10-11/`：`source-checks.json`、`browser-results.json`、`substance.json`、`shared-copy.json`、畫面及測試匯出檔。自查檔中的測試文字不是學員成果或模型實跑。

## 可重現檢查

在課程目錄：

```bash
python3 _tools/check-2026-10-11-step-by-step.py
python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py index.html module1.html CH1-1.html CH2-1.html CH3-1.html CH4-1.html PRAC2-1.html
/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node _tools/verify-2026-10-11-step-by-step.cjs
```

最後一項需允許啟動隔離Chrome。技術驗證不會送提示詞到LLM或使用Gamma／NotebookLM帳號。

## 未驗項目與發布

- 新提示詞需在授課用LLM實跑；NotebookLM三來源→引用、Gamma十頁生成／修改／匯出、Google文件一頁PDF需用授課帳號走完。官方說明核對不能取代帳號測試。
- 請零基礎學員只依新版講義走完，記錄需要講師補充的位置；CH2文字90分鐘＋Gamma90分鐘及各章3小時仍是規劃，待真人節奏確認。
- 本輪沒有新平台成果PDF。Gamma兩份既有示例屬先前實跑，企劃原文未改，保留其原始證據。
- 未重建全站search-index、sitemap或發布；那些位於課程以外且不在本次發布範圍。沒有把本機完成當成網站已更新。

## 官方操作參考

- [NotebookLM／Gemini Notebook 加入文字來源](https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en)：複製文字、來源標題及勾選來源。
- [Gamma 貼入與保留原文](https://help.gamma.app/en/articles/11047840-how-can-i-import-slides-or-content-into-gamma)：Agent保留文字、經典貼入替代路徑。
- [Gamma 匯出](https://help.gamma.app/en/articles/8022861-what-s-the-easiest-way-to-export-my-gamma)：全部卡片與播放視圖。
- [Google 文件列印](https://support.google.com/docs/answer/143346?hl=en)：列印及瀏覽器／PDF差異。

## 回復

19份原檔備份：`_backup/2026-10-11-pre-step-by-step/`，含manifest SHA-256。還原指令：

```bash
bash _tools/restore-2026-10-11-pre-step-by-step.sh
```

還原只處理本次備份檔與新增六份提示詞；既有其他課程改動不動，內部驗證與修正紀錄保留。
