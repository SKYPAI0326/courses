---
slug: uiux-designer
unit_id: B7-figma-handoff-export
title: 把設計整理成能重開、能量測的交付包
course_type: skill-operation
duration: 6h
prerequisites: [B6-prototype-task-test]
revision: 2026-10-11
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方檔案 2026-10-09 查證；實際帳號與桌面軟體另記平台證據
---

## 內部設計（不進學員頁）

本課新增能力：免費Design量測／Figma輸出、真實PSD操作與透明PNG，以及可重開的完整handoff。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 把設計整理成能重開、能量測的交付包

接手者需要知道尺寸、色碼、狀態與檔案用途，而不只是看到幾張PNG。本堂以免費Design面板讀規格、完成Figma匯出，再用真正分層PSD練習儲存與透明PNG輸出，整理成完整交付包。

## 開始前，先找到材料與起點

前堂作品至少主線無阻斷，並有測試紀錄。選一個Row能說出父框和文字層不同即可開始。Photoshop工作站與PSD在第一次使用前取得；無軟體請保留待補操作，不能換成PNG假冒。

先開啟[本堂起始材料（HTML）](../../courses/uiux-designer/assets/B7-figma-handoff-export/START-HERE.html)，讀取輸入與圖層名稱；操作在你的 Figma 檔或本堂指定工具完成。完成後到[本堂完成檢查表（可儲存／下載）](../../courses/uiux-designer/assets/B7-figma-handoff-export/reference/HANDOFF-CHECK.html)記錄實際結果。

## 先取得PSD與參考輸出

現在下載[status-badge.psd（512×512、三個點陣圖層）](../../courses/uiux-designer/assets/shared/status-badge.psd)，用於Photoshop練習；[status-badge.png（透明背景參考）](../../courses/uiux-designer/assets/shared/status-badge.png)用來核對匯出；[圖層說明](../../courses/uiux-designer/assets/shared/PSD-README.html)說明Background、Card、Check的內容。全部是本課製作的示範素材，不含客戶資料。

第一次使用前先開啟[Photoshop桌面版準備與啟動](../../courses/uiux-designer/assets/shared/PHOTOSHOP-START.html)：已有授權者依Adobe官方入口安裝並開啟；使用教室工作站者須取得實際地點／時段、登入方式與儲存位置，再確認能開啟512×512的三層PSD。沒有軟體仍可檢查PNG尺寸與透明效果，但那不等於完成PSD重開／修改／匯出；在完成檢查表記「Photoshop操作待補」及所缺條件，可先整理Figma輸出，取得可用工作站後回本堂補做。不要把一張扁平PNG改副檔名為.psd來交作業。

## 示範：Starter用Design面板讀規格

1. 在Figma開啟修正版檔案，選T01 Row外框。用右側Design讀W、H、Padding、Gap、Corner radius與Fill，記Row W354、Padding16、Gap8與當時高度。
2. 再選Row / Title，記實際字型、字級18、行高28、字重、Fill色碼；不要從匯出圖片猜文字尺寸。
3. 在可讀取檔案的情況，用Alt（Windows）／Option（Mac）檢視選取層到相鄰層的距離，並與已設定Gap核對。看不到距離先選正確層與Design面板，也可以用本課Auto Layout欄位讀明確值。
4. Starter沒有Dev Mode，本課不要求點選Inspect／Dev Mode開關。付費且有適合seat的學員可補做Dev Mode，但本堂核心交付仍是Design可讀的規格表。
5. 記一份Button：來源Button、Hierarchy Primary、State Default、Label「確認完成」、H48、圓角8與填色。需要的是可辨認的規格，不是任意複製CSS後就當工程完成。

## Figma匯出：格式跟用途一起選

| 格式 | 本課用途 | 不包含什麼 |
|---|---|---|
| PNG | 確認Dialog／狀態徽章等點陣圖預覽，可有透明背景 | 元件來源與Prototype互動 |
| SVG | 簡單圖示等向量素材 | 自動保留Figma元件或Prototype，不會 |
| PDF | 多張畫面供人審閱 | 可點原型或可編輯PSD圖層 |
| .fig本機副本 | 儲存Figma可編輯內容 | 帳號分享權限；仍要確認接手者能開 |
| PSD | Photoshop分層原稿 | FigmaAuto Layout或程式互動 |

1. 選Overlay / Confirm的Frame，在Design底部Export按＋，選PNG、1x，Export所選Frame，檔名用 `dialog-confirm.png`。預期W320、高度依當時內容，不能拿舊320×200參考圖當作本次真實匯出。
2. 選主線Login／List Long／Detail／List Done等Frame匯出PNG，按畫面命名。若做PDF，用檔案選單的Export frames to PDF（當前介面提供時），確認頁序與畫面清單；沒有入口可用PNG附清單作審閱備援。
3. 用檔案選單Save local copy另存 `studio-tasks.fig`，並儲存Prototype view連結。接手者必須能重開設計與預覽，單有截圖不夠。

## 跟著做：Photoshop儲存分層與透明PNG

1. 在Photoshop選File → Open，開本堂status-badge.psd。Layers應看到三個獨立圖層Background、Card、Check；檔案512×512、RGB。Card是綠色圓角底，Check是白色勾號，Background是可切換的白底。
2. 點Background的眼睛隱藏／顯示。隱藏時四角應見透明棋盤格；點Check隱藏，白色勾號消失但Card仍在。這證明可以獨立修改，不能只看扁平預覽。
3. 還原Check可見、Background隱藏。儲存副本 `status-badge-working.psd`：File → Save As，選Photoshop PSD並保留圖層；若版本入口為Save a Copy，選PSD並確認圖層保留。關閉副本後重新Open，三層和可見性應仍存在。
4. 要練習修改，選Card圖層，使用Hue/Saturation等適合點陣層的調整改色，或用本課綠色保持規格；只改Card，不把Check一起染色。另存修改版，不覆蓋原素材。
5. File → Export → Export As，選PNG、Transparency勾選、W512 H512、Scale1x，匯出 `status-badge.png`。這份透明PNG用於網站，PSD用於後續修改；用途不同。
6. 用瀏覽器或圖片檢視器把PNG放在非白底上，確認四角透明；在Photoshop重開PNG也應見透明區域。JPG不支援同樣透明用途，若出現白底先檢查Background是否隱藏與Transparency選項。
7. 若需單層輸出，可用File → Export → Layers to Files，設命名字首與格式，但交付清單應說明每張圖屬於哪個層；本課主線只需PSD與一個透明PNG，避免產出一堆不知用途的圖。

## 整理交付資料夾與驗收清單

在自己的電腦建立 `studio-tasks-handoff`，包含 `source/`、`exports/`、`spec/`、`tests/`。source放.fig與working.psd；exports放畫面PNG、dialog與badge；spec放規則表、畫面清單、元件狀態表；tests放第14堂測試JSON／截圖。下載[交付清單範例（JSON）](../../courses/uiux-designer/assets/shared/handoff-example.json)並照你的實際檔案修改，不交含不存在檔名的清單。

接手說明寫：作品用途、如何開Prototype、哪個Frame為起點、圖檔尺寸／格式、哪些只是模擬狀態、未完成什麼。Smart Animate可附第11堂Before／After層名與引數列，不能只說「有動畫」而不說明如何預覽。

**驗收方法：**獨讀時先關閉作品編輯分頁與檔案，只照交付資料夾內自己的README重新找到.fig、Prototype連結、PSD及PNG。重開.fig時，回Figma首頁檔案瀏覽器，從Create new選單選Import／匯入並選source/studio-tasks.fig，或將.fig拖進檔案瀏覽器；匯入後開啟新檔，核對Layers及Prototype。入口可依[Figma官方匯入說明](https://help.figma.com/hc/en-us/articles/360041003114-Import-files-to-the-file-browser)定位。分享設計與Preview則開README內的實際連結；PSD在Photoshop用File → Open選source/status-badge-working.psd。再核對起點Login、PSD三層，以及PNG的512×512與透明角落。把exports/dialog-confirm.png暫移到交付資料夾外的missing-test資料夾，再只照清單確認它缺少；記缺檔位置，放回後重查。有同學時可請他依同一清單操作，另記結果；自己核對記「本人重開」，不能當成接手者已驗收。若Photoshop不可用，PSD項仍待補。這個練習測試交付是否真的可用，不是把資料夾截圖當成通過。第16堂網站會使用本堂badge與同一套視覺規則。

## 自己完成：改變條件再檢查

將badge的Background顯示，先匯出錯誤白底PNG；再隱藏與重新透明匯出，留下兩版比較。將Dialog文字加長並重新匯出，更新清單的實際高度，不沿用舊值。關閉已開檔案後，自己只照README找到Prototype、PSD與徽章，核對實際檔名／路徑及新版Dialog高度，將找不到或數值不符的項目修正後再重開。有同學時另記他的閱讀與重開結果，沒有同學就標「他人交付驗收待補」，不杜撰誤解。Photoshop未可用時，白底／透明匯出練習與PSD核對保留待補。

## 完成條件與理解檢查

- 免費Design規格表含尺寸、間距、字型、行高、色碼與元件狀態，不依賴Dev Mode。
- PS原稿可重開且有三個獨立圖層；透明PNG尺寸512×512、檔名與清單一致。
- 交付包有來源、輸出、規格與測試，缺檔練習已恢復；網站素材可取得。

**想一想：**為什麼PNG匯出成功，仍不能宣稱「PSD交付已完成」？

<details><summary>展開參考答案與理由</summary><p>PNG是點陣輸出，通常沒有原PSD的獨立圖層。PSD交付需真實分層檔能重開、圖層可分別操作且儲存正確；兩者解決不同用途。</p></details>

## 本堂查證來源

- [Figma：Design與檢視規格](https://help.figma.com/hc/en-us/articles/22012921621015-Guide-to-inspecting)
- [Figma：Starter範圍](https://help.figma.com/hc/en-us/articles/13838684089751-Starter-plan-overview)
- [Adobe：Export As](https://helpx.adobe.com/photoshop/desktop/save-and-export/export-files-to-different-formats/fine-tune-your-export-settings-using-the-export-as-option.html)
- [Adobe：PSD與格式](https://helpx.adobe.com/photoshop/desktop/save-and-export/export-files-to-different-formats/photoshop-file-formats-overview.html)

來源查證：2026-10-09。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
