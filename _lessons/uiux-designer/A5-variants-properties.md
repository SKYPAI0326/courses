---
slug: uiux-designer
unit_id: A5-variants-properties
title: 把主次按鈕與狀態做成可選的元件
course_type: skill-operation
duration: 6h
prerequisites: [A4-component-instance]
revision: 2026-11-02
style_guide: ../../_outlines/uiux-designer.style-guide.md
platform_version: 官方文件 2026-11-02 查證（_review/2026-11-02/platform-*.md）
---

## 內部設計（不進學員頁）

本課新增能力：設計互相獨立的Variant軸、四種狀態組合與可維持的Label屬性。依 `_design/COURSE-BLUEPRINT.md` 的同檔案整合路徑；保留 99h 行政配置，未以真人試跑鎖定分鐘。

| 活動 | 素材／產物 | 操作與決策 | 認知工作／支援 |
|---|---|---|---|
| Demo | 正文提供的完整輸入／方法示範 | 講師建模本課首次方法與可見結果 | 完整理由及步驟 |
| Together | 同一工作室任務清單／學員自己的完成物 | 正文「跟著做」需自行選層、設定與判斷 | 支援遞減，自己定位欄位、解釋檢查結果 |
| Solo | 本課不同條件／修正後完成物 | 正文「自己完成」依新限制選擇方法 | 獨立診斷與遷移，依完成條件判斷 |

素材：正式正文的可複製資料、每課 START-HERE、完成檢查表、共用視覺參考，B7 有 PSD，B8 有下載 ZIP。素材存在／版本由驗證紀錄確認，不以本段自填 PASS。

<!-- learner-content:start -->
# 把主次按鈕與狀態做成可選的元件
副標：登入、取消與確認都要共用按鈕，設計者還要能選主要或次要角色，並呈現滑過、按下、焦點與停用狀態。
本堂完成物：十種角色與狀態組合的按鈕元件；可開關與交換的按鈕圖示；一組符合題目資料的狀態標籤

## 從上次的按鈕來源接著做

工作室的登入畫面需要醒目的「登入」，確認彈窗需要「確認完成」與「取消」。同一顆按鈕還會經過滑鼠移上、按下和暫時無法操作等狀態；若每遇到一種情況就另做一顆按鈕，外觀很快就會分歧。這堂要把同一家族整理成可選版本，讓設計者能選角色、選狀態，也能決定是否顯示圖示。

這項工作會接著使用上次放在 `Components` 裡的按鈕來源與巢狀圖示。開始前先看[本堂起始材料](../../courses/uiux-designer/assets/A5-variants-properties/START-HERE.html)，確認按鈕仍保有 Auto Layout（自動排版）、`Label` 文字層與圖示使用處；做完後再開[完成檢查表](../../courses/uiux-designer/assets/A5-variants-properties/reference/EXPECTED-CHECK.html)，逐一切換十種組合。沒有上次成果時，先回到[改一次來源，讓多個按鈕一起更新](CH4-component-instance.html)，依該頁規格表補做主要按鈕、兩個使用處與巢狀圖示，約需 20～30 分鐘。

先選取兩個既有使用處，確認它們仍能跟著主元件的圓角更新。接著回到主元件，檢查按鈕的高度、左右內距、字級、圓角與圖示位置。可靠的來源會成為十個 Variant 的共同結構，避免每個狀態長成不同尺寸。

## 先分清楚：角色和互動狀態回答不同問題

Variant（變體）把同一元件在不同條件下的版本整理成可選組合。Type 表示按鈕在畫面中的角色；State 表示使用者現在如何接觸它，或它能否操作；Label 則說明按下後會發生什麼。三者分開後，設計者可以直接依用途選擇設定。

例如，確認彈窗裡的「確認完成」是 Primary（主要角色），平常顯示 Default，游標移上時變成 Hover，手指或滑鼠按下時變成 Pressed。旁邊的「取消」是 Secondary（次要角色），而且仍可操作，所以 State 維持 Default。若登入資料尚未填齊，「登入」依舊是 Primary，只是 State 暫時選 Disabled。

| 要判斷的事 | 可選內容 | 回答的問題 | 判斷線索 |
|---|---|---|---|
| Type | Primary、Secondary | 這個動作在目前畫面有多重要？ | 一個畫面通常只有一個最醒目的主要動作 |
| State | Default、Hover、Pressed、Focus、Disabled | 使用者目前如何接觸它，或現在能否執行？ | Hover 是滑鼠經過，Pressed 是按下當下，Focus 是鍵盤焦點，Disabled 是條件尚未完成 |
| Label | 登入、取消、確認完成等 | 使用者按下後會發生什麼？ | 用動詞與對象說清楚結果 |
| Show icon | True、False | 這個情境需要圖示輔助嗎？ | 文字已很清楚時可關閉，快速掃讀或圖示慣例明確時可顯示 |
| Icon | Check、Plus、Arrow Left 等 | 顯示哪一個圖示？ | 圖示要和動作一致，仍以文字說明為主 |

Hover 與 Pressed 是短暫回饋。Hover 適合桌面上的滑鼠游標，手機沒有滑鼠經過的狀態；Pressed 則對桌面和手機都有意義，因為它讓使用者在按下那一刻知道系統收到動作。Focus 服務鍵盤操作；使用者按 Tab 移動時，靠按鈕外的焦點圈辨認目前停在哪裡。之後建立原型時，這些 Variant 會成為互動的目標，現在先把視覺差異與命名準備好。

同一個 State 在兩種 Type 上可以有不同外觀，但回饋強度要一致。Primary 的 Hover 改用 `Primary Hover` 底色，Pressed 改用較深的 `Primary Pressed`；Secondary 的 Hover 使用 `Primary Soft` 底色，Pressed 也以淺底搭配較明顯外框。兩種角色的 Focus 都在按鈕外加 2 px `Focus Ring`，並與按鈕保留 2 px 間隔；可用 Stroke 的 Outside 呈現。所有狀態都保留原本尺寸，使用者不會因滑過、按下或取得焦點看到按鈕跳動。

## 示範：建立十種按鈕與可改文字

這一節會把按鈕來源擴成一個元件集。先看完整規格，再依序處理外觀、屬性與文字；數值集中在表格，操作時只要引用名稱即可。

| Type | State | 填色與文字 | 外框與用途 |
|---|---|---|---|
| Primary | Default | `Primary` 底、白字 | 可操作的主要動作 |
| Primary | Hover | `Primary Hover` 底、白字 | 滑鼠移上回饋 |
| Primary | Pressed | `Primary Pressed` 底、白字 | 按下當下的主要動作 |
| Primary | Focus | `Primary` 底、白字 | 外加 2 px `Focus Ring`，與按鈕保留 2 px 間隔 |
| Primary | Disabled | `Disabled` 底、`Disabled Text` 字 | 條件未完成的主要動作 |
| Secondary | Default | `Card` 底、`Text` 字 | `Control Border` 1 px 外框，可操作的次要動作 |
| Secondary | Hover | `Primary Soft` 底、`Primary` 字 | `Control Border` 1 px 外框，滑鼠移上回饋 |
| Secondary | Pressed | `Primary Soft` 底、`Text` 字 | `Control Border` 1 px 外框，按下當下回饋 |
| Secondary | Focus | `Card` 底、`Text` 字 | 外加 2 px `Focus Ring`，與按鈕保留 2 px 間隔 |
| Secondary | Disabled | `Disabled` 底、`Disabled Text` 字 | `Control Border` 1 px 外框，暫時停用 |

共同結構：元件集命名為 `Button`；每個版本高度 48、水平內距 16、圓角 8；`Label` 套用 `Type / Label`；文字屬性預設值為「登入」。Primary 的五個 Variant 都使用白色 `Card` 圖示；Secondary 的圖示維持 `Text`。Secondary 的 Default、Hover、Pressed、Disabled 外框都套用 `Control Border` 變數，與表單控制項的邊界規則一致。

1. 在元件區的 `Button / Primary` 上按右鍵，選 **Main component → Add variant**。完成後它會變成紫色虛線框住的元件集，裡面有原本版本和一個新版本，既有使用處仍留在各自畫面。

![右鍵 → Main component → Add variant（紅框）](../../courses/uiux-designer/assets/shared/ui/figma-add-variant-menu.webp)

2. 點虛線框下方的 **＋** 繼續增加版本，直到共有十個。完成後十個版本都從相同結構開始。

![元件集外框是紫色虛線，下方 ＋ 可再加版本；右側 Properties 顯示屬性（紅框）](../../courses/uiux-designer/assets/shared/ui/figma-component-set.webp)

3. 將元件集命名為 `Button`；完成後，Layers（圖層面板）與 Assets（元件資產面板）會顯示一致的家族名稱。
4. 選取元件集，在 Properties（屬性區塊）點 **＋**，選 **Variant**，把新屬性命名為 State；完成後，元件集會有兩個可整理的 Variant 屬性。

![Properties 的 ＋ 開啟 Create property 選單：Variant、Text、Boolean、Instance swap、Slot（紅框）](../../courses/uiux-designer/assets/shared/ui/figma-create-property-menu.webp)

5. 將原有屬性（Figma 預設叫 Property 1）命名為 Type；完成後，右側會以 Type 與 State 描述版本。
6. 逐一選取十個版本，填入規格表中的角色與狀態；完成後，每一組 Type 與 State 只出現一次。
7. 依規格表調整十個版本的顏色、圖示與外框；完成後，主要與次要的層級差異仍清楚，Hover、Pressed 與 Focus 也能被辨認。
8. 選取元件集，在 Properties 點 **＋** 選 **Text**，名稱填 Label，預設值填「登入」，再按 **Create property**；完成後，元件集會出現可編輯的文字屬性。

![Create property 視窗：填 Name 與 Value，按 Create property（紅框）](../../courses/uiux-designer/assets/shared/ui/figma-text-property-dialog.webp)

9. 逐一選取十個版本內的 `Label` 文字層，在右側最上方 Content 欄旁點 **Apply variable/property** 圖示，綁定 Label；完成後，十個版本會使用同一個文字欄位。

![選文字層後，Content 欄旁的 Apply variable/property 圖示 → 選 Label（紅框）](../../courses/uiux-designer/assets/shared/ui/figma-apply-property.webp)

10. 從 Assets 拖入一個 Button 使用處，將 Label 改成「標記完成」；完成後，按鈕顯示新文字，元件來源與其他使用處的文字維持原狀。
11. 依序切換 Type 與 State；完成後，十種外觀都能選到，而且「標記完成」在切換後仍保留。

元件集解決版本選擇，文字屬性解決內容改寫。若切換後文字回到「登入」，表示至少一個 Variant 的文字層尚未綁定 Label；回到該版本補上綁定，再從使用處重試。

接著製造一次可恢復的組合衝突。把其中一個 Secondary／Default 暫時改成 Primary／Default，Figma 會標示組合衝突，警告文字以你看到的畫面為準。重新填回 Secondary／Default 後，十種組合各自唯一，警告也會消失；這比只看顏色更能確認屬性完整。

## 跟著做：用情境選對角色與狀態

這一節把來源用回工作室畫面。每次先說出「角色、狀態、內容」三個答案，再到右側找對設定。

1. 為登入畫面插入一顆按鈕，讓它成為可操作的主要動作；完成後會看到 Primary／Default 的「登入」，並能直接編輯 Label。
2. 為確認彈窗準備一顆「取消」，讓它保持可操作但視覺次要；完成後會看到 Secondary／Default，外框採用 `Control Border`。
3. 再準備一顆「確認完成」，讓它成為彈窗中的主要動作；完成後兩顆按鈕的角色有清楚差異。
4. 依序把確認完成切到 Hover、Pressed 與 Focus；完成後會看到底色、按下與焦點圈回饋，文字和尺寸保持穩定。
5. 複製登入按鈕，設定成必填資料尚未齊全的狀態，並在旁邊加入原因「請先填寫帳號與密碼」；完成後會同時看見停用外觀與可理解的原因。
6. 將「確認完成」改成較長的「確認這筆任務已完成」，再切換十種組合；完成後文字不會遺失，所有版本高度也維持一致。
7. 選取其中一個使用處，把 Label 改為「返回清單」，再點右側元件名稱列的 **⋯** 選 **Reset instance**；完成後文字會回到來源預設值。

完成後，用三欄寫一筆判斷紀錄：「情境是什麼」「選了哪個 Type 與 State」「使用者從外觀和文字知道什麼」。例如，取消是次要動作，但它能讓人安全離開彈窗，因此 Type 是 Secondary，State 保持 Default。

## 讓圖示能顯示、隱藏，也能交換來源

同一個按鈕元件有時需要圖示，有時只需要文字。這一節為按鈕加入兩個元件屬性：`Show icon` 控制圖示層是否顯示，`Icon` 控制要使用哪個巢狀圖示。設計者在使用處右側就能調整，不必進入多層結構尋找圖示。

| 屬性 | 類型 | 預設值 | 使用結果 |
|---|---|---|---|
| `Show icon` | Boolean | True | 開關圖示層可見性 |
| `Icon` | Instance swap | `Icon / Check` | 在既有圖示元件之間交換 |

1. 回到元件集，選取 Primary／Default 裡的圖示使用處；完成後，右側會顯示該圖示的元件名稱與 Appearance（外觀）區塊。
2. 在 Appearance 標題列找到眼睛旁的 **Apply variable/property** 圖示，點 **＋**；完成後會開啟「Create property or variable」視窗。

![Appearance 標題列的 Apply variable/property 圖示，按 ＋ 開啟 Create property 視窗，預設值 True（紅框）](../../courses/uiux-designer/assets/shared/ui/figma-boolean-property.webp)

3. 選 Create 為 Property，把 Name 改成 `Show icon`，Value 保持 True，再按建立；完成後，元件集 Properties 會出現 Boolean 屬性。
4. 將其他九個 Variant 的對應圖示層連到同一個 `Show icon`；完成後，切換狀態時會保留使用處的顯示選擇。
5. 選取其中一個 Variant 的圖示使用處，在 Properties 點 **＋** 選 **Instance swap**，命名為 `Icon`；完成後，按鈕來源會有可交換巢狀元件的屬性。
6. 將其餘 Variant 的圖示使用處連到同一個 `Icon` 屬性；完成後，十個版本會共享圖示選擇。
7. 從 Assets 插入新的 Button 使用處；完成後，右側會同時出現 `Show icon` 開關與 `Icon` 下拉。
8. 關閉 `Show icon`；完成後，圖示消失，Auto Layout 會收回圖示與文字之間的 Gap，Label 仍置中。
9. 再打開 `Show icon`，把 `Icon` 從 `Icon / Check` 換成 `Icon / Plus`；完成後，只有這個使用處換圖示，其他按鈕維持原選擇。
10. 切換 Type 與 State 逐一檢查；完成後，圖示的顯示與來源選擇不會因切換 Variant 而被重設。

若某個狀態切換後圖示突然恢復，先檢查該 Variant 的圖示層是否連到相同屬性。十個版本的層級與命名一致，Boolean 與 Instance swap 才能在使用處維持同一組選擇。

## 看兩種圖示策略，判斷各自適合的情境

這一節是取捨題，兩個版本都可能合理。版本一的主要按鈕一律顯示圖示，例如勾選搭配「確認完成」、加號搭配「新增任務」；使用者能快速掃到動作類型，但按鈕較容易顯得擁擠。版本二預設關閉圖示，只在空間充足或動作需要額外辨識時打開；畫面較安靜，但相似按鈕只能靠文字區分。

請回答：工作室的「新增任務」與確認彈窗的「確認完成」各適合哪一版？若同一列已有多顆短按鈕，該如何選？理由要同時考慮文字清楚度、可用寬度與圖示是否具有熟悉含義。

<details><summary>查看取捨理由</summary><p>「新增任務」搭配加號很常見，空間足夠時可採版本一；「確認完成」的文字已很明確，彈窗較窄時可採版本二。多顆按鈕並列時，先保留清楚文字，再只替最需要快速辨識的動作顯示圖示；兩版的判斷重點是情境，不是固定哪一版較好。</p></details>

## 卡住時，先查組合再查屬性

這一節整理最常見的失敗現象。先找到出錯層級，再改對應來源，能避免把十個版本逐顆修成不同結果。

| 看到的現象 | 通常的原因 | 怎麼修 |
|---|---|---|
| 只看到 Variant 1、2 等預設名稱 | 屬性名稱尚未整理 | 選元件集，把角色命名為 Type，再新增 State |
| 元件集顯示組合衝突 | 兩個版本使用相同屬性值 | 對照十列表格，補回缺少的組合 |
| 切換狀態後文字回到「登入」 | 某個版本的文字層尚未綁 Label | 選該版本的 `Label`，用 Apply variable/property 綁定 |
| Secondary 外框與色彩規則不一致 | 外框仍是手填顏色 | 將 Default、Hover、Pressed、Disabled 外框套用 `Control Border` 變數 |
| Hover 時按鈕尺寸跳動 | 外框改變物件尺寸或結構 | 保持相同高度與內距，讓外框效果不推動內容 |
| 使用處沒有 Show icon | 顯示屬性建在錯誤圖層 | 選元件內的圖示層，從 Appearance 建立 Boolean 屬性 |
| 換圖示後切狀態又恢復 | 只有部分 Variant 綁定 Instance swap | 把十個對應圖示層連到同一個 `Icon` 屬性 |

修完後再插入一個新的使用處驗證。新的使用處能選到十種組合，也能開關與交換圖示，代表來源已修好。

## 換你做：你的題目

從你的畫面清單挑出這次對應的畫面。接著把資料裡的狀態做成標籤元件，再讓主要確認按鈕具備五種 State、顯示開關與圖示交換。下面三欄提供可採用的狀態與動作對應；若你的畫面清單採用不同名稱或拆法，以自己的需求初稿為準。

### 三個題目的建議對應

| 預約 | 點餐 | 會員 |
|---|---|---|
| 狀態標籤使用「可預約／本週額滿」；「送出預約」按鈕具備 Default、Hover、Pressed、Focus、Disabled，並可顯示勾選或日期圖示。 | 狀態標籤使用「供應中／售完」；「送出訂單」按鈕具備五種 State，並可顯示勾選或購物車圖示。 | 狀態標籤使用「可兌換／點數不足／已兌完」；「確認兌換」按鈕具備五種 State，並可顯示勾選或星號圖示。 |

要達成的條件：

- 這次做的畫面在你的畫面清單上；清單沒有的，先補進清單並寫一句理由。
- 狀態標籤的 Variant 值完全照題目資料，文字與顏色一起傳達狀態。
- 主要確認按鈕具有 Default、Hover、Pressed、Focus、Disabled 五種 State。
- Pressed 使用較深的主色，Hover 有可看見但不改變尺寸的回饋。
- 按鈕右側可以直接開關 `Show icon`，也能從 `Icon` 下拉交換圖示。
- 十個按鈕 Variant 的文字層、圖示層與 Auto Layout 階層一致。

合格的結果要能通過的自我檢查：

- 我能從右側切換所有 Type 與 State，不必進入內層重做外觀。
- 狀態標籤只使用需求頁與資料表裡實際存在的狀態值。
- Hover、Pressed、Focus 與 Disabled 各自回答不同情況，尺寸保持穩定。
- 關閉圖示後，文字仍置中且沒有留下多餘空隙。
- 交換圖示後再切換 State，使用處仍保留所選圖示。

<details><summary>真的卡住再看：提示</summary><p>先完成十種 Type 與 State 組合，再處理屬性；若切換後文字或圖示恢復，逐一檢查每個 Variant 的對應圖層是否綁到同一個屬性。</p></details>

## 收好按鈕家族，下一步做完整表單

這堂把工作室裡零散的登入、取消與確認動作，整理成十種可選組合的 Button 元件集。你現在能分開判斷 Type、State、Label 與 Icon，也能用組合表找出重複或缺少的版本；自己的題目則多了一個依真實資料切換的狀態標籤來源。

下一次會把 Button 放進完整表單，並建立文字欄、勾選、單選、下拉與開關元件。今天保持一致的圖層階層與 Auto Layout，會直接影響表單控制項切換狀態時能否穩定。

完成條件：

- Button 元件集具有十個唯一的 Type 與 State 組合。
- 每個 Variant 的文字層都綁定 Label，使用處可直接改字。
- 使用處可開關圖示並交換巢狀圖示來源。
- 自選題目的狀態標籤使用素材中的正確狀態值。

想一想：一顆「取消」按鈕外觀比較低調，是否代表它應該設成 Disabled？

<details><summary>查看答案</summary><p>不代表。低調描述的是 Secondary 角色；Disabled 描述的是目前無法操作。取消通常是次要但可操作的安全出口，因此應選 Secondary 與 Default。</p></details>

## 本堂查證來源

- [Figma：建立與使用 Variants](https://help.figma.com/hc/en-us/articles/360056440594)
- [Figma：Component properties](https://help.figma.com/hc/en-us/articles/5579474826519)
- [Figma：插入元件使用處](https://help.figma.com/hc/en-us/articles/360039150173)
- [Figma：重設使用處的變更](https://help.figma.com/hc/en-us/articles/360039150733)

來源查證：2026-11-02。
<!-- learner-content:end -->

## 講師授課筆記（不進講義）

先用正文入口題檢查前提，再以短示範讓學員同步操作。每次核心狀態改變立即檢查；主要時間用於自行製作、同儕解釋、錯誤修復與新條件作品。先核對學員真實工具權限與檔案；未達完成條件回到本堂修復位置，不以教師代做當成完成。此稿為作者設計與自審，真人理解／遷移與平台實測須另留證據。
