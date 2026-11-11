# ACP Premiere Pro 模擬試題來源對照表

- 日期：2026-11-03
- 用途：重製模擬試題時，每題的英文原文、選項、題圖要從哪個檔案取。配合 [`MOCK-EXAM-LAYOUT-SPEC.md`](MOCK-EXAM-LAYOUT-SPEC.md) 使用。
- 建表方式：108 張考試截圖用 macOS Vision OCR 抽文字後比對題目關鍵字，辨識不到的再目視確認；主檔 PPT 用 python-pptx 抽文字與內嵌圖。OCR 全文存在 `tmp/exam-screenshots-ocr.txt`（不進 repo）。

## 來源代號

| 代號 | 檔案 |
|---|---|
| 主檔 S## | `04-ARCHIVES/課程/ACP PR CC 2024/ACP PR CC 2024.pptx` 第 ## 張 |
| 補充 S## | 同資料夾 `ACP PR CC 2024（抽換補充）.pptx` 第 ## 張（術科 1–30 的英文，與主檔 S69–S99 內容相同） |
| `IMG_####` | `01-PROJECTS/專案/課程相關參考資料/ACP PR考試畫面截圖/` 手機翻拍（75 張） |
| `HHMMSS.png` | 同資料夾 `螢幕擷取畫面 2026-10-22 HHMMSS.png`（33 張） |

## 取用原則

1. **文字來源**欄是逐字轉錄的依據。有考試截圖的題目以截圖為準，主檔 PPT 只當對照，因為主檔的文字是早期手打的，和考試畫面有出入（見文末「已發現的落差」）。
2. 同一題有多張截圖時，優先序：PNG > 第一次作答 JPEG > 第二次作答 JPEG。
3. **考試每次作答的選項順序不同**（例如綠幕題：`IMG_4781` 的 A 是 Adjustment Layer，`IMG_0595` 的 A 是 Ultra Key）。題本與解答本的選項字母一律以「文字來源」那張為準。
4. **題圖**欄寫「無」代表原題不需要看圖作答。

## 學科題 A01–A38

| 題號 | 題目焦點 | 文字來源 | 題圖 | 其他對照 | 備註 |
|---|---|---|---|---|---|
| A01 | 照片長寬比 | 主檔 S46 | 主檔 S46 照片（485×363） | — | |
| A02 | 影片 codec／container 三選 | `145435.png` | 無 | 主檔 S47、`IMG_4785` | 三版選項順序都不同 |
| A03 | 輸出錯誤與修正工具配對 | 主檔 S48 | 主檔 S48 工具圖 ×4（約 170×38） | — | 圖解析度低，照原尺寸放 |
| A04 | Full HD 電影解析度與影格率 | 主檔 S49 | 無 | — | 現行版英文多了 "traditional … released in theaters"，主檔沒有，重製時要刪 |
| A05 | 分割 audio clip 的工具 | 主檔 S50 | 主檔 S50 工具列圖（432×70） | — | 選項是圖片，題本要在工具上加編號 |
| A06 | 修剪工具與描述配對 | 主檔 S51 | 主檔 S51 工具圖 ×3（約 82×58） | — | 主檔文字被截斷，描述要從原 PPT 逐格補齊 |
| A07 | 暫時只聽 A2 | `145309.png` | `145309.png` 音軌標頭熱點圖（主檔 S52 軌道圖 ×3 為舊版） | 主檔 S52 | 點選介面題；PNG 版有「可能不只一種正確方法」說明，主檔沒有 |
| A08 | 影像數值填空 | 主檔 S53 | 無 | — | |
| A09 | Creative Commons 符號 | 主檔 S54 | 主檔 S54 授權符號圖 | — | |
| A10 | 多行文字行距 | `144809.png` | `144809.png` 題圖 | 主檔 S55 | PNG 為新版 Properties panel，主檔為舊版 Essential Graphics |
| A11 | 前期製作兩項 | 主檔 S56 | 無 | — | |
| A12 | 客戶前期三問 | `IMG_4777` | 無 | 主檔 S57 | |
| A13 | Shot type 與圖片配對 | 主檔 S58 | 主檔 S58 圖（378×474） | — | |
| A14 | Bins 與 Media Offline 填空 | 主檔 S59 | 主檔 S59 圖 | — | |
| A15 | Insert 按鈕 | `145459.png` | `145459.png` Source Monitor 熱點圖 | 主檔 S60 | 點選介面題，圖就是作答區 |
| A16 | `THAI` 字元間距兩項設定 | `IMG_4775` | `IMG_4775` THAI 標誌＋Text 面板熱點 | 主檔 S61、`IMG_4819` | 點選介面題；OCR 誤讀成 THAT，實為 THAI |
| A17 | Accessibility feature | 主檔 S62 | 無 | — | |
| A18 | Project Manager 封存設定 | 主檔 S63 | 主檔 S63 參照圖（467×119） | — | 原題 4 條條列，現行版被壓成一句 |
| A19 | image 1 → image 2 色偏 | `IMG_4787` | 主檔 S64 比較圖（882×299） | 主檔 S64 | 考試選項順序為 A) aperture B) white balance C) resolution…，與主檔不同 |
| A20 | Shot type 與畫面配對 | 主檔 S65 | 主檔 S65 群組內題圖（`image48.png`，953×312，4 張畫面） | — | 配對題：5 個 shot type（Extreme Close Up、Extreme Wide Shot、Mid Shot、Over the Shoulder、Point of View）對 4 張畫面，多 1 個干擾項。題圖包在群組裡，用 python-pptx 逐層抽圖會漏，要從 `ppt/media/image48.png` 取。曾於 2026-11-03 誤判殘缺而移除，同日放回 |
| A21 | 音訊術語配對 | `145031.png` | `145031.png` 拖曳配對畫面 | 主檔 S66 | |
| A22 | PSD 只匯入圖層 1、2 | `IMG_4778` | `IMG_4778` PSD 預覽＋Import Layered File 對話框 | 主檔 S67 | 點選介面題，翻拍需透視校正 |
| A23 | 標題可讀性（行動裝置、低視能） | `IMG_4776` | 無 | `IMG_4817` | 補充 S02 |
| A24 | 16:9 Ultra HD 4K frame size | `IMG_4779` | 無 | — | 補充 S05；OCR 幾乎讀不到，需目視轉錄 |
| A25 | 商用音樂 attribution | `IMG_4780` | 無 | `IMG_4820` | 補充 S06 |
| A26 | 移除綠幕背景 | `145240.png` | 無 | `IMG_4781`、`IMG_0595` | 補充 S07 |
| A27 | 關閉 nests 選項時的置入結果 | `IMG_4782` | `IMG_4782` Timeline 按鈕狀態圖 | `IMG_4816` | 補充 S08 |
| A28 | Captions True／False | `145337.png` | 無 | `IMG_4783`、`IMG_4818` | 補充 S09 |
| A29 | 保存只有 Timeline＋Program 的 workspace | `IMG_4784` | 無 | `IMG_4815` | 補充 S10 |
| A30 | 移除 In／Out 範圍不留 gap 的按鈕 | `IMG_4786` | `IMG_4786` Program Monitor 按鈕列熱點 | — | 補充 S12；點選介面題 |
| A31 | 大量 Media Offline 處理 | `IMG_4788` | 無 | — | 補充 S14 |
| A32 | 前期製作三選 | `144724.png` | 無 | — | OCR 只讀到部分選項，需目視轉錄 |
| A33 | Scratch disk 位置 | `144907.png` | 無 | — | |
| A34 | 公共場所人像與熱門歌曲 | `145112.png` | 無 | — | |
| A35 | PSD 保留個別圖層 | `145146.png` | 無 | — | |
| A36 | 視障觀眾的畫面資訊 | `145215.png` | 無 | — | OCR 只讀到選項 A，需目視轉錄 |
| A37 | Proxy files 用途 | `145408.png` | 無 | — | |
| A38 | 16:9 照片長寬比 | `144945.png` | `144945.png` 題目照片 | — | 與 A01（4:3）是不同題 |

## 術科題 B01–B42

術科任務在考試畫面右側的 Certification Test 面板。手機翻拍裡面板字很小，轉錄時要放大原圖逐字讀。

| 題號 | 專案／任務 | 文字來源 | 參考圖 | 其他對照 | 備註 |
|---|---|---|---|---|---|
| B01 | Drone：建立 Oregon Coast sequence | `IMG_4805` | 無 | `IMG_4836`、主檔 S69、補充 S2 | 考試版面板末尾有 Note（OCR 只讀到 "…copied before the dialog is opened."，全文見 `IMG_4802`），主檔沒有 |
| B02 | Drone：修剪 Lighthouse_99 | `IMG_4800` | 無 | `IMG_4838`、主檔 S70、補充 S3 | 考試版開頭為 "On track V1 of the Lighthouse sequence"，主檔漏了 sequence 名 |
| B03 | Drone：Establishing Shot clip marker | `IMG_4802` | 無 | `IMG_4839`、主檔 S71/S99、補充 S4/S32 | |
| B04 | Drone：sequences bin 與改名 Drone View | `IMG_4801` | 無 | `IMG_4840`、主檔 S72、補充 S5 | |
| B05 | Getaway：Auto Save 每 5 分鐘、30 版 | `152831.png` | 無 | 主檔 S73/S88、補充 S6/S21 | 考試版為 "Configure Premiere to…"，主檔為 "Configure Premiere Pro to…" |
| B06 | Fireplace2 放大 200% | 主檔 S74 | 無 | 補充 S7 | 無考試截圖 |
| B07 | Getaway：Mountain Getaway 透明度淡入淡出 | `152637.png` | 無 | 主檔 S75、補充 S8 | |
| B08 | Tuning 多機位序列 | 主檔 S76 | 無 | 補充 S9 | 無考試截圖 |
| B09 | Jamming 新增 Face Cam 軌道 | 主檔 S77 | 無 | 主檔 S91、補充 S10/S24 | 無考試截圖 |
| B10 | Food：Tiramisu 白平衡 | `150722.png` | 無 | 主檔 S78、補充 S11 | 考試版為 "Use the Lumetri Color tools…"，主檔為 "WB Selector"，措辭不同 |
| B11 | Food：THAI Track Matte Key | `IMG_4809` | `IMG_4809` 面板內參考圖（THAI FOOD 結果圖），可辨識但有摩爾紋與偏色 | `IMG_4832`、主檔 S79、補充 S12 | 主檔沒有這張參考圖 |
| B12 | Food：Thai Curry 音樂 1 秒淡出 | `150823.png` | 無 | `IMG_4808`、`IMG_4834`、主檔 S80、補充 S13 | 考試版為 "Use an effect to fade out the music on track A1…"，主檔較短 |
| B13 | Food：Sushi 音訊移至 A2 | `IMG_4807` | 無 | `IMG_4831`、主檔 S81、補充 S14 | |
| B14 | Food：Thai Curry 輸出前整理 | `IMG_4810` | 無 | `IMG_4833`、主檔 S82、補充 S15 | |
| B15 | Transportation：InsideTrain 插入 | `151408.png` | 無 | 主檔 S83/S86、補充 S16/S19 | 考試版只有 2 條要求；主檔有第 3 條（"The resu…"，現行版寫成結束於 00:00:15:06）。需確認是版本差異還是面板未捲動 |
| B16 | NYCstreet 音訊位移 | 主檔 S84 | 無 | 補充 S17 | 無考試截圖 |
| B17 | Transportation：airshow 兩秒 frame hold | `151242.png` | 無 | `151250.png`、主檔 S85、補充 S18 | 考試版有 "Note: Use a method other than time remapping."，主檔沒有 |
| B18 | Intro bin 合併剪輯 | 主檔 S87 | 無 | 補充 S20 | 無考試截圖 |
| **B19** | **Playing：用 Clap 標記對齊音訊** | 主檔 S89 | 無 | 主檔 S90、補充 S22/S23 | **現行版漏掉這題** |
| B20 | ArtistInterview Ultra Key | 主檔 S92 | 無 | 補充 S25 | 無考試截圖 |
| B21 | Aspirations：ArtistInterview 前 30 秒 | `152309.png` | 無 | 主檔 S93、補充 S26 | |
| B22 | Aspirations：images／videos bins | `152423.png` | 無 | 主檔 S94、補充 S27 | |
| B23 | 建立 Promo（HDV 720p30） | 主檔 S95 | 無 | 補充 S28 | 無考試截圖；與 B42 不同題 |
| B24 | ArtistInterview Crop | 主檔 S96 | 主檔 S96 結果圖（404×213） | 補充 S29 | |
| B25 | Drone：SL Blue Ice 調整圖層 | `IMG_4804` | 無 | `IMG_4837`、主檔 S97、補充 S30 | |
| B26 | Drone：LighthouseTitle.ai 縮放 70% | `IMG_4803` | 無 | `IMG_4841`、主檔 S98、補充 S31 | |
| B27 | Africa 2：Jackal.mp4 解讀為 24 fps | `IMG_4789` | 無 | `IMG_4847` | 補充 P01 |
| B28 | Africa 2：依表格建 rough cut | `IMG_4790` | 原題表格（In／Out 時間），從照片轉成表格 | `IMG_4846`、`IMG_4791` | 補充 P02；現行版英文漏掉表格 |
| B29 | Kittens：加入 Kitten1_Adopt 與音樂 | `IMG_4793` | 無 | `IMG_4843` | 補充 P03 |
| B30 | Kittens：管理 clips 與 tracks | `IMG_4794` | 無 | `IMG_4844` | 補充 P04 |
| B31 | Fitness World：Auto Reframe | `IMG_4824` | 無 | `IMG_4795`、`IMG_4796`、`IMG_4823` | 補充 P05；`IMG_4796` 拍到 "Slower Motion／Do not nest clips／Leave the default name" 等條件 |
| B32 | Commute：改名 Daily Commute 並 unlink | `152925.png` | 無 | `IMG_4798`、`IMG_4822`、`IMG_4797` | 補充 P06 |
| B33 | Africa：Hyena-Rock 刪除停頓 | `IMG_4812` | 無 | `IMG_4826`、`IMG_4827`（transcript 面板）、`151644.png`、`IMG_4811`、`IMG_4825` | 補充 P17 |
| B34 | School：Study Session 調整音訊 | `IMG_4814` | 無 | `IMG_4829`、`IMG_4813`、`IMG_4828` | 補充 P18 |
| B35 | Pizza Time：移除指定區段 | `150430.png` | 無 | — | |
| B36 | Pizza Time：管理 timeline markers | `150605.png` | 無 | — | |
| B37 | Social：建立巢狀序列 | `150955.png` | 無 | — | |
| B38 | Africa：Auto Reframe 9:16 | `151516.png` | 無 | — | |
| B39 | Africa：重整 Maasai Mara 序列 | `151854.png` | 無 | — | |
| B40 | Fitness World：移除未使用素材 | `152541.png` | 無 | — | |
| B41 | Commute：刪除 commute3 並補滿 gap | `153009.png` | 無 | `IMG_4821`（Generative Extend 提示） | |
| B42 | Aspirations：建立 Promo（HDV 1080p25） | `152118.png` | 無 | — | 與 B23 不同題 |

## 主檔概念投影片（S6–S44）的圖片

主檔共 50 張圖，題目區（S46–S99）以外的 25 張都在概念投影片。評估結果：**不能當題本題圖**，部分可放解答本輔助說明。

| 投影片 | 內容 | 用途評估 |
|---|---|---|
| S44 | 英文版 Window > Workspaces 選單 | 可放 A29 解答本 |
| S28 | 新建序列對話框（簡中介面） | 可放 B23、B42 解答本；介面語言與考試不同 |
| S22–S27 | Source／Program Monitor、Project、Timeline、Effects、Effect Controls 面板（簡中介面，舊版） | 只適合當面板位置示意；介面語言與版本都與考試不同 |
| S6 | 解析度比較圖 | 不建議：把 4K 標成 4096×2160，和 A24 的 UHD 3840×2160 會混淆 |
| S15 | 鏡頭景別示意（法文標籤） | 不建議：用詞與考題的 shot type 名稱不同 |
| S10–S14 | PowerDirector 介面截圖 | 不能用：不是 Premiere |
| 其他（S7–S9、S16、S18–S21） | 幀數示意、分鏡表、起始畫面等 | 與題目無直接對應 |

主檔沒有備忘稿（speaker notes），不能當答案來源。

## 不是題目的檔案

| 檔案 | 內容 |
|---|---|
| `IMG_0594` | 「尚須等待 1 天才能再次應試」錯誤畫面 |
| `IMG_4792`、`IMG_4799`、`IMG_4806`、`IMG_4830`、`IMG_4835`、`IMG_4842`、`IMG_4845` | 專案總覽，只列出任務標題，沒有展開任務內容 |
| 主檔 S1–S44 | 基礎概念與軟體介紹投影片，不是題目 |

## 截圖數量核對

| 批次 | 張數 | 組成 |
|---|---:|---|
| 前批 JPEG | 75 | 第一次作答：學科 14（`IMG_4775`–`4788`）＋術科 26（`IMG_4789`–`4814`）；第二次作答：學科 7（`IMG_0595`、`IMG_4815`–`4820`）＋術科 27（`IMG_4821`–`4847`）；錯誤畫面 1（`IMG_0594`） |
| 本批 PNG | 33 | 學科 14（`144724`–`145459`）＋術科 19（`150430`–`153009`） |

## 已發現的落差

1. **現行版漏了 B19。** 主檔 S89–S90 的 Playing／Clap 任務沒有出現在現行模擬試題裡，B 題號從 B18 直接跳到 B20。
2. **主檔 PPT 的文字和考試畫面不一致。** B01、B02、B10、B12、B17 的考試版有主檔沒有的條件或 Note，而且措辭不同。所以「有截圖就以截圖為準」這條規則不能省。
3. **現行版自己加字。** A04 英文多了主檔沒有的 "traditional … released in theaters"。
4. **選項順序每次作答都不同。** 字母要以選定的那張文字來源為準，不能混用不同截圖的字母。
5. 同一份 PNG 批次裡 `145435.png` 和 `145459.png` 都標示 "Question 13 of 14"，內容分別是 A02 和 A15，應該是重拍或作答時翻回同一題，不影響對照。

## 截圖品質檢查（2026-11-03）

檢查方式：任務面板以 OCR 定位後裁切放大目視；學科題逐張看題目區。判定「完整」的依據是任務面板底部的 Mark as Complete 按鈕有入鏡（面板沒有被捲動截斷），學科題則是題幹與全部選項都入鏡。

- **文字全部可讀**：58 題的文字來源截圖，題幹、選項、任務條件都能逐字讀出。第一次轉錄時 OCR 讀不到的 7 張（`IMG_4779`、`IMG_4785`、`IMG_0595`、`IMG_4781`、`144724.png`、`145215.png`、`145435.png`），改用定位 OCR 或目視後都讀得到。
- **B28 表格完整**：`IMG_4790` 四列 In／Out 表格全部清楚。
- **畫質可用但印刷效果差**（翻拍有摩爾紋或小字）：
  - A22 `IMG_4778`：右側 Import Layered File 對話框清楚；左側 Photoshop 圖層面板字太小，圖層名稱勉強可辨。Import As 下拉選單沒有展開，選項文字要以主檔 S67 為準。
  - B11 `IMG_4809`：參考圖可辨識，但有摩爾紋與偏色。
  - A16、A19、A27、A30：翻拍題圖可用，印成題本會比螢幕擷取模糊。
- **拍攝缺漏**：
  - PNG 那次作答的學科 Question 14 沒有截圖（`145435.png`、`145459.png` 都是 Question 13），不知道是哪一題。
  - 三次術科作答各 18 項任務都有拍到展開畫面，沒有缺。
  - 第二次 JPEG 學科作答只拍了 7 題，但題目都與第一次相同，不影響內容。
