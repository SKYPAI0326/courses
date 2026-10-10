# 教學審查缺口修正報告

日期：2026-10-11；task_scope：content-change；審查：author-self-check。
使用者授權：依前輪兩項MAJOR、一項MINOR執行修改。

## 已修正

- CH2把同一客戶改口吻統一稱為語氣調整；示範前後、標題與檢查同步。真正讀者轉換保留客戶→主管及不同請求。
- CH4自備資料的起點、第一輪指令、验算、排序、改限制、重算均使用自己的值。增加change-own.txt、頁內完整複製指令與已填替換示例。示例由作者驗算，沒有新增實作作業或全班共同任務。
- 課後整合允許第一版已符合，記下支持原文／算式，再確認無差異；檢查清單同步，不要求製造錯誤。
- CH2／CH4教案learner-content與HTML同步，CH4比較指令下載原檔同步。

學員檔案共7份：CH2-1.html、CH4-1.html、對應兩份教案、compare.txt、change-own.txt、course-capstone-handoff.md。完整SHA與本輪改動邊界見changed-files.json。

## 驗證結果

- HTML結構：2頁，blocked=0。
- lint：2頁，BLOCKER=0、ERROR=0、WARN=2；未修改無關樣式或原示例。
- substance：各頁missing_assets=0、block=0；機器semantic_review仍為PENDING，不作語意通過證據。
- 教案正文與HTML可見文字一致；提示詞區與可下載原檔全文一致；既有工作台欄位／資料鍵、CSS及JS未改；既有連結保留，新連結可取得。
- 原補訓／交接資料與既有第二輪提示詞保留。新示例人工重算：4,800−4,500=超300；4,500−4,000=餘500；36席滿足36人；交通差10分鐘。數值均屬教學模擬，未冒稱實際報價。
- CH2／CH4各1440、390、430px，共6組：無水平溢出，既有步驟錨點避開固定頁首。桌面頂端／修改區／中段／底部與手機修改區，留12張截圖。
- 新增自備案例複製按鈕實際操作，複製文字與完整原檔相符；瀏覽器pageerror=0。
- 人工查看CH2桌面與CH4手機截圖，新增文字保持原內容寬度與折疊結構。
- 差異檢查與還原腳本語法檢查通過。

新證據：_validation/review-findings-2026-10-11/source-checks.json、browser-results.json及截圖。本次CH2／CH4新hash取代舊step-by-step相關頁面文字證據；未改頁面不重跑。

## 檢查器修正

第一次lint使用錯誤相對路径，未掃到頁面；substance第一次工作目錄路徑錯誤。修正呼叫後各通過。隔離Chrome首次啟動被沙箱阻擋，經允許後啟動。畫面檢查器第一次誤用不存在的lesson-nav，改為頁面實際nav-footer後通過。這些是驗證工具呼叫問題，不列作講義缺口。

## 可重現與回復

在課程目錄：

```bash
python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py CH2-1.html CH4-1.html
/Users/paichenwei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node _tools/verify-2026-10-11-review-findings.cjs
bash -n _tools/restore-2026-10-11-pre-review-findings.sh
```

需回復時執行還原腳本；只恢復本輪六份原檔並移除新增change-own.txt，保留先前修正及其他課程改動。備份在_backup/2026-10-11-pre-review-findings/。

## 範圍與未驗事項

本輪未commit／push，未重建課程以外的全站搜尋索引。沒有使用個人帳號、送提示詞到外部平台，亦無新增真人跟做證據。LLM、NotebookLM、Gamma與Google文件的新版平台驗證，以及12小時／CH2三小時節奏仍待真人實跑。本次完成的是三項已授權內容修正與本機驗證。
