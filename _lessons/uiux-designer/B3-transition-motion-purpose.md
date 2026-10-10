---
slug: uiux-designer
unit_id: B3-transition-motion-purpose
title: 用轉場說明方向，再做出可觀察的Smart Animate
course_type: skill-operation
duration: 6h
prerequisites: [B2-trigger-navigation-action]
revision: 2026-10-11
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方檔案 2026-10-09 查證；實際帳號與桌面軟體另記平台證據
---

## 內部設計（不進學員頁）

本課新增能力：依用途選轉場與引數，製作同名同層級的前後狀態並診斷Smart Animate配對。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 用轉場說明方向，再做出可觀察的Smart Animate

動畫應幫人理解畫面關係。本堂先比較進入詳情與回清單的方向，再用相同名稱與層級的物件做出真正的Smart Animate。選到動畫名稱只完成設定，看到物件連續變化才算效果成立。

## 開始前，先找到材料與起點

前堂基本連線能真點成功才開始。先用Instant確認List→Detail→返回；如果Destination錯誤，回第10堂修，動畫不會修好錯的目的地。

先開啟[本堂起始材料（HTML）](../../courses/uiux-designer/assets/B3-transition-motion-purpose/START-HERE.html)，讀取輸入與圖層名稱；操作在你的 Figma 檔或本堂指定工具完成。完成後到[本堂完成檢查表（可儲存／下載）](../../courses/uiux-designer/assets/B3-transition-motion-purpose/reference/EXPECTED-CHECK.html)記錄實際結果。

## 選動畫前，先說要表達什麼

| 用途 | 本課範例設定 | 要觀察的效果 |
|---|---|---|
| 進入較深一層詳情 | Navigate to、Move in、從右進入、Ease out、200ms | Detail從右進來，表示向前深入 |
| 返回清單 | Navigate to、Move out、往右離開、Ease out、200ms | Detail退出，顯露List；方向與進入相反 |
| 一般不需空間關係的切換 | Instant或短Dissolve | 資訊清楚、不用每個動作都滑動 |
| 同物件狀態改變 | Smart animate、Ease out、200ms | 形狀、位置、尺寸或透明度連續變化 |

200ms是本例起點，不是通用正確值。Duration控制花多久，Easing控制速度如何變化；Ease out是先快後慢，讓物件較柔和停下。太長會讓頻繁操作等待，太短可能看不出方向。為容易暈動或不需要動畫的使用者，保留Instant比較版。

## 示範：在現有連線比較兩種轉場

1. 選List的Row / T01連線，保留On click與Destination Detail，只把Animation改Move in，方向選從右進入，Duration200ms、Easing Ease out。不同UI的箭頭圖示可能不寫方向文字，用Preview確認從哪邊開始。
2. 在Detail的Button / Back連線選Move out，讓Detail往右退出，Destination仍List。不要同時把Destination改到另一張畫面，才能比較轉場。
3. Preview從Login進到List再點T01與返回。應能說出「前進進入詳情、返回退回清單」，不是所有畫面都由同一側跳進。
4. 將這兩條連線各改Dissolve跑一次，記錄感受：哪一種更能表達層級、哪一種較少動態負擔。最終主線保留你能說明理由的版本，不為了展示功能用最花俏設定。

## Smart Animate：先準備配對物件

Smart Animate會尋找兩張Frame裡同名且層級對應的物件，把可動畫屬性的前後值連起來。文字內容更換不是所有字形都會平順變形；本堂用尺寸與透明度，結果更容易檢查。

1. 在畫布外新建 `Motion / Before` Frame，402×300。裡面建立 `Status / Badge` Frame，x24、y70、W160、H48、主要綠底、圓角8；放文字Label「待處理」。另建文字 `Status / Check`「✓」，放在x300、y85，Opacity0%。
2. 複製整張Frame為 `Motion / After`，保留內部層名與階層。將Badge W改280、填色改Success；Check Opacity改100%。不要重新畫兩份同樣外觀但名字不同的Badge。
3. 在Before中建立名為 `Button / Animate` 的測試Button「看看變化」，放y180。複製到After相同位置，保留名字。
4. Before的Animate Button設On click→Navigate to→After→Smart animate、Ease out、200ms；After的Animate Button連回Before，同樣設定。兩個不同熱區各有一個動作，不需要同trigger多動作。
5. 給Before單獨Flow起點 `MOTION-01`，Preview來回點。Badge應寬度連續增加／縮小，Check淡入／淡出，沒有整張畫面只瞬間切換。

| 配對檢查 | Before | After |
|---|---|---|
| Badge路徑 | Motion / Before → Status / Badge | Motion / After → Status / Badge |
| Badge尺寸 | W160、H48 | W280、H48 |
| Check層名 | Status / Check | Status / Check |
| Check透明度 | 0% | 100% |
| 動畫 | Smart animate 200ms／Ease out | 返回同設定 |

## 跟著做：診斷不能配對的效果

把After的Status / Badge暫時改名為 `Different / Badge`，再Preview比較。物件可能以淡入淡出替代連續寬度變化。你要先指出是哪一層不匹配，再把名與階層恢復。接著不改名字，只將Duration改600ms，觀察等待時間；最後回200ms。一次只改一個條件，避免把命名與速度問題混在一起。

**卡住時：**完全沒反應先查連線與起點；畫面會切換但Badge只淡入，查名稱／父層；Badge跳動，確認兩端同一屬性確實有不同值且沒有被另一層蓋住；效果太慢，查Duration；Smart Animate控制元件看得到卻無變化，代表選項存在，尚不能證明配對成功。

這個Motion分支用於學動畫，不必把所有動效塞進主線。後面交付仍需說明原型選擇的動畫與不用動畫的理由。

## 自己完成：改變條件再檢查

讓Check位置從x300移到x260，同時用Opacity0→100；保留一份同內容的Instant版本。自己在Preview依相同起點各播放一次，記錄動畫版是否從右側移入並淡入、Instant是否直接出現，以及兩版的完成文字與最終位置是否一致。依能否看清狀態變化與設定Duration說明你的選擇，不把200ms引數當成人的實際等待感。有同學時另記他對理解與等待的回饋，未邀請就標待補。交出前後值表、兩版比較、正確配對結果、故意改名失敗與修復，以及主線兩種轉場理由。

## 完成條件與理解檢查

- 主線進入／返回轉場方向與用途明確，200ms及Easing有記錄。
- Smart Animate的同名同層級物件確實改變尺寸與透明度，Preview可見連續變化。
- 能用一次改名故障解釋配對條件，修復後重新測試，並保留Instant比較。

**想一想：**兩張Frame都有綠色矩形，為什麼仍可能沒有連續伸縮？

<details><summary>展開參考答案與理由</summary><p>外觀相似不等於同一物件配對。Smart Animate需要名稱與層級對應，並且可動畫屬性的前後值有差異；若名稱不同或父層不同，可能以淡入淡出替代。</p></details>

## 本堂查證來源

- [Figma：Smart Animate的名稱與層級配對](https://help.figma.com/hc/en-us/articles/360039818874-Smart-animate-layers-between-frames)
- [Figma：Prototype actions](https://help.figma.com/hc/en-us/articles/360040035874-Prototype-actions)

來源查證：2026-10-09。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
