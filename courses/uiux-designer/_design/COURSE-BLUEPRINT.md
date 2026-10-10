# Course Blueprint：工作室任務清單

修訂2026-10-09。本文是學員起點、能力增量與依賴的目前設計來源。正式正文在專案 `_lessons/uiux-designer/`，HTML由同一來源轉製。歷史Probe保留觀察，不沿用錯誤的「Starter一檔一action」推論或Dev Mode免費主張。

## 學員起點與補救

受眾能操作瀏覽器、鍵盤及下載檔案，不預設Figma、Photoshop、程式或Git經驗。入口診斷與補救在[課前速查](../assets/COURSE-START.html)，各堂正文先檢查必要前提。時數42h＋57h保留為行政配置；未經真人班級試跑，不宣稱已鎖定學習分鐘。

## 真實作品依賴

同一份課程Figma檔：視覺規則→402／1440格線→Auto Layout卡片→Button來源與四種Variant→双欄Login→三筆List與Detail→Confirm、Toast、Nav→線框與起點→完整基本Flow→轉場與動畫分支→Overlay／Swap→長List與Fixed→任務測試→交付包→對應網站。

主線：Login→List Long→T01 Detail→Confirm；取消留Detail，確認到List Done並見Toast。T02／空狀態／Swap／Smart Animate／Sticky／Horizontal是有明確用途的測試分支。所有核心基本互動在同一檔；不用同trigger多actions或條件變數。網站保留核心任務，未實作的動畫分支需明示，不能宣稱全原型等價。

## 能力與正式正文

| 單元／配置 | 新能力 | 核心可觀察證據 | 正式頁面 |
|---|---|---|---|
| A1／5h | 依用途建立視覺規則，說明對比與非顏色線索，並在長句下檢查閱讀層級 | 色彩表有角色、色碼與用途，錯誤／警告／成功都包含文字線索。 | [讓畫面看得清楚：色彩、字型與閱讀順序](../part1/CH1-visual-foundations.html) |
| A2／6h | 計算跨欄寬度，從桌面雙區轉成手機閱讀順序 | 402 與 1440 版面各有正確欄數、邊界、溝槽及跨欄區。 | [用格線安排手機與桌面版面](../part1/CH2-grid-layout.html) |
| A3／6h | 建立真正的Auto Layout階層，以文字／容器不同尺寸模式處理長句、增刪與寬度變化 | 卡片真的有Vertical、Padding16、Gap12、W354／Height Hug設定。 | [讓文字變長時，容器與按鈕一起排好](../part1/CH3-auto-layout-pressure.html) |
| A4／5h | 驗證主元件同步、個別Override及錯誤修復，讓來源與使用處關係可觀察 | 主元件有完整Label與Auto Layout，Assets能找到來源。 | [改一次來源，讓多個按鈕一起更新](../part1/CH4-component-instance.html) |
| A5／6h | 設計互相獨立的Variant軸、四種狀態組合與可維持的Label屬性 | 四個Variant有唯一的Hierarchy／State組合，Default與Disabled能辨認。 | [把主次按鈕與停用狀態做成可選的元件](../part1/CH5-variants-properties.html) |
| A6／6h | 組成多欄表單，分辨正常／錯誤／修正狀態，以Auto Layout處理長提示 | 正常／錯誤／修正後三張畫面有帳號與密碼兩欄，Label、Input、Helper齊全。 | [完成兩個欄位的登入表單與錯誤修正](../part1/CH6-button-form.html) |
| A7／4h | 完整Row父子層級、清單增刪與空狀態，並建立真實Detail畫面供原型串接 | 三筆主線Row都有Title、Meta、Link與自己的Auto Layout，List能隨增刪重排。 | [把任務做成會增高、可增刪的清單](../part1/CH7-list-content.html) |
| A8／4h | 依情境選擇回饋，建立能包子層的Dialog與Actions，設計Nav選中規則 | Toast包含結果文字；Dialog包含標題、説明與取消／確認兩個完整Button。 | [設計能讓人知道下一步的回饋、彈窗與導覽](../part1/CH8-toast-dialog-navigation.html) |
| B1／7h | 從任務規劃低細節線框，對映到真實元件與一致命名，指定Prototype入口 | 任務卡與五個主線畫面名稱對得上，畫面內容使用前課元件。 | [把需求畫成線框，再組成可測試的流程](../part2/CH1-wireframe-prototype-entry.html) |
| B2／6h | 建立同檔多步基本Flow，檢查熱區、目的地與返回，分辨方案限制及故障 | 同一檔案至少完成Login→List→T01 Detail→返回，T02顯示不同內容。 | [連好登入、清單、詳情與返回](../part2/CH2-trigger-navigation-action.html) |
| B3／6h | 依用途選轉場與引數，製作同名同層級的前後狀態並診斷Smart Animate配對 | 主線進入／返回轉場方向與用途明確，200ms及Easing有記錄。 | [用轉場說明方向，再做出可觀察的Smart Animate](../part2/CH3-transition-motion-purpose.html) |
| B4／7h | 完整Overlay開關／確認、可取消規則與在已開彈層內Swap的實際路徑 | Open／Cancel／outside／Confirm四種結果都在Preview實際檢查，目的地與表格一致。 | [讓確認彈窗能開啟、取消、確認與交換](../part2/CH4-overlay-single-action.html) |
| B5／6h | 建立視窗／長內容關係，實測Vertical、Fixed、Sticky及遮擋，在完整Flow使用長列表 | 874視窗內能Vertical捲到最後一筆，外Frame沒有為長內容增高。 | [讓長清單能捲動，導覽與漂浮按鈕不擋內容](../part2/CH5-scroll-fixed-floating.html) |
| B6／6h | 用整段任務測內容、導航、Overlay、Scroll及Swap，記錄失敗並回歸，完成新情境capstone | T01–T08都有實際觀察或明確未執行原因，包含長列表與前課固定元素成果。 | [讓別人跑完整任務，修正後再測一次](../part2/CH6-prototype-task-test.html) |
| B7／6h | 免費Design量測／Figma輸出、真實PSD操作與透明PNG，以及可重開的完整handoff | 免費Design規格表含尺寸、間距、字型、行高、色碼與元件狀態，不依賴Dev Mode。 | [把設計整理成能重開、能量測的交付包](../part2/CH7-figma-handoff-export.html) |
| B8／13h | 從完整可執行程式理解與修改網站，實作獨立Git基準／差異／遠端與公開部署更新 | 解壓的獨立專案本機可開，完整取消／確認／清單狀態與長內容正確；理解三檔與id／class分工。 | [把設計做成網站，留下版本與公開網址](../part3/CH8-web-git-deploy.html) |

## 環境、素材與驗收

環境唯一入口見[Environment Contract](ENVIRONMENT-CONTRACT.md)；操作型單元有材料、結果、修復與獨立條件練習。SVG為視覺參考，不假稱含Auto Layout或Prototype。真實PSD與可下載Web專案存在，來源由本課製作。

Demo展示首次方法；Together在同作品減少提示，要求選層／判斷／修復；Solo改變有意義的尺寸、資料、狀態或任務。逐課Activity Identity與Shared Copy審查見本輪修復／驗證紀錄。

目前狀態由 `_validation/evidence.json` 和本輪REPAIR-REPORT記錄。作者自審、機器檢查、平台及真人跟做分開，不由靜態PASS推論HUMAN_READY。
