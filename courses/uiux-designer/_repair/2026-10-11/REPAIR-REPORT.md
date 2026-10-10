# 修復報告：學員獨立閱讀與跟做

## 結論

本輪內容修正已完成並同步來源與HTML。8堂教案、8個正式頁面及相關材料／檢查表已更新；未新增測驗題或強制問題數。課程仍需平台與真人實跑，不能宣稱全課已完成教學驗收。

## 修改內容

| 單元／材料 | 已修正 |
|---|---|
| A1 | 文字角色的選層、字級／行高／字重與檢查均可自行執行。 |
| A4 | 本人可觀察來源同步與Label覆寫，並恢復測試值。 |
| A5 | 在命名的元件集副本植入重複Variant，定位缺失組合、修復及確認正式來源。 |
| B1 | Login→List→T01走讀、T02期限核對可獨立完成；正文、hero、完成檢查表條件一致。 |
| B2 | EMPTY-TEST起點與Empty→List→T03→返回可自行執行；更正新增連線為三條，核對星期五17:00。 |
| B3 | 相同內容的Smart Animate／Instant自行比較，分開引數與他人的等待感。 |
| B6 | 補可編輯副本取得、None故障／無互動備援、JSON重現與完整回歸；同儕結果另列。 |
| B6評分 | 保留20／20／25／15／20共100分與80分門檻；20項各5或0分、附證據，必要路徑未測或阻斷不能通過。新增可保存／下載逐項評分表。 |
| B7 | 補Photoshop授權軟體安裝／啟動入口；教室地點、時段、登入與儲存條件未提供就待確認。補.fig匯入、PSD重開與缺檔放回核對。 |
| Blueprint | T01–T07同步為T01–T08；現有測試表的T08保留。 |

教案為內容來源；只在原section的DOM錨點內同步，head、CSS、章節id、順序與導覽保留。8頁修訂日期改2026-10-11，原平台查證日期保留。相關入口首次使用前即有可點連結，沒有虛構教室或帳號。

## 驗證證據

- 結構：本輪15個HTML全數通過，0 BLOCK；見structure.txt。
- lint：本課56個公開HTML，BLOCKER／ERROR／WARN均0；見lint.txt。最初相對`.`指令意外掃到全站，已改絕對課程路徑重跑，本結論以56頁紀錄為準。
- 同源：8堂所有正文section與教案渲染文字一致；0缺失本地連結，head／CSS／導覽／section id／既有理解問題數不變。見content-link-check.json與前後文字快照。
- 實際browser smoke：B6、B7於1440×900核對起點、示範／材料、評分／交付、完成條件／導覽；390×844與430×932核對閱讀。整頁無水平溢出，B6寬表格留在auto捲動容器；sticky topbar在頂端。見browser-smoke.json，圖像與DOM觀察另見本次工具紀錄。
- 評分表：保存、重開回填與JSON下載成功，51個具名欄位、20個通過checkbox；保存用紀錄明標頁面核對，未勾學員評分，核對後清空回填資料。JSON匯入本輪未實際操作，保留待核對。
- Photoshop入口：從B7實際點到準備頁，頁內PSD與圖層說明連結可解析；桌面軟體尚未操作。
- Activity Identity：保留各堂不同產物、決策與認知工作，Demo／Together／Solo支援遞減；見SCAN.md。
- Shared Copy：16堂共有1個完整重複段落，是本堂材料與保存檢查表的必要導航；各頁href不同且有效，保留。未新增共用結尾或固定題量；見shared-copy-check.json。
- 搜尋索引：採既有產生器的extract／classify規則，只同步本輪15頁，新增2筆，其他條目逐項保持原樣。見search-index-check.json；未全站重建以免混入其他未提交內容。
- 差異：相對本輪備份的scoped-diff.patch；git diff --check核對本輪目標。既有mixed worktree變更保留，未staging、commit或push。

## 尚待真實環境與學員驗收

1. Figma Starter實際登入、編輯、Prototype與可編輯副本全路徑，含整合作品逐項證據。
2. Photoshop可用授權／教室實際資訊，以及桌面開PSD、獨立圖層、另存重開、透明匯出。
3. 新學員的理解、獨立完成、遷移與接手者驗收；本人自測只記本人結果。
4. 全課原驗證hash已變動，5筆受影響的舊PASS改PENDING、保留舊hash與原判定；validation-result改PENDING_REVALIDATION。本輪scope證據另存scoped-evidence.json，未讓舊PASS代表目前版本。

## 回復

29個既有檔案備份：`_backup/2026-10-11-pre-repair/`，含原未提交內容與站內搜尋索引，hash逐一核對。
還原腳本：`_tools/restore-2026-10-11-pre-repair.sh`，bash -n通過；需寫回教案／站根索引。腳本還原既有檔，新增的兩個材料頁保留，清單見manifest.json；本輪沒有刪檔。
