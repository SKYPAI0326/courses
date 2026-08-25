# Platform Audit：NotebookLM／Gemini 手機與雙向路徑

查證日期：2026-08-25
課程 slug：`simple-ai`
查證範圍：Google 官方說明頁、公開手機版操作說明；未登入學員個別帳號，因此不把某一帳號當成所有學員的保證。

## Confirmed

| 主題 | 官方目前可確認的內容 | 教材採用方式 |
|---|---|---|
| NotebookLM 手機來源 | 目前官方手機說明頁使用「Gemini Notebook」名稱；手機版可加入 PDF、網站、YouTube、音訊檔與複製文字，繁體中文列在支援語言；手機版仍可能因地區／版本逐步開放而不同。 | 教材保留學員熟悉的 NotebookLM 稱呼，並提醒畫面可能顯示 Gemini Notebook；核心示範以三份可複製文字完成。 |
| NotebookLM 來源查核 | Notebook／NotebookLM 的聊天回應以來源為 grounding，會提供引用；來源未出現的內容不應自行補齊。 | 先在 NotebookLM 產生有引用的品牌摘要，再把草稿帶回逐句查核。 |
| Gemini 手機輸入 | Gemini Android App 可在輸入框點「Add files」加入檔案、照片、Drive 或 Notebook；iOS App 可從「Add files」加入檔案／圖片。登入與學校／工作帳號權限可能影響可用功能。 | 整合入口存在時可選同一個 Notebook；不依賴特定圖示位置，保留貼文字備援。 |
| Notebook 跨 Gemini | 官方說明目前寫明：Notebook 會出現在 Gemini 導覽中，Notebook 的名稱、來源與自訂指令可跨產品同步；整合仍受支援地區與帳號條件限制，部分 Gemini Apps 入口目前以個人 Google 帳號為主。 | 教材提供「整合路徑」但使用條件句，不宣稱每位學員都會看到同一入口。 |
| Grounding 差異 | NotebookLM 回應只根據 Notebook 來源；Gemini 中的 Notebook 回應可能同時使用 Notebook 來源、網路搜尋或其他工具。 | Gemini 只負責改寫草稿；所有可發佈事實都回 NotebookLM 查核。 |

## Not claimed

- 不宣稱 NotebookLM／Gemini 的原生同步對所有手機、地區、帳號都已開放。
- 不宣稱 Gemini 的草稿天然只來自 Notebook 來源；即使同一個 Notebook 可見，也要回來源查核。
- 不固定寫死「+ 新 Notebook」「Notebooks」或其他按鈕位置；App 版本與語言可能不同。
- 不承諾特定免費帳號的每日問答次數或長文字上限；教材採小型來源包與分段貼上。
- 不把複製貼上備援說成產品自動同步；它是學員手動搬運摘要、來源摘錄與草稿的可重現路徑。

## Fallback

當學員看不到 Notebook 整合入口、手機版尚未開放或畫面與教材不同時：

1. 在 NotebookLM 選取三份來源，複製含引用的品牌摘要與五段來源摘錄。
2. 開 Gemini 新對話，貼上摘要、來源摘錄與完整社群 Prompt；不重新上傳含個資的原始評論。
3. 複製 Gemini 草稿回 NotebookLM，勾選三份來源，貼上逐句查核 Prompt。
4. 只保留能找到來源的句子；「來源中未出現」的句子刪除、改寫或標示待確認。
5. 保存品牌摘要、Gemini 草稿、查核結果與修正版四張截圖／一份備忘錄。

## Official sources

- Gemini Notebook mobile：<https://support.google.com/gemininotebook/answer/16296687>
- Notebooks in Gemini Apps：<https://support.google.com/gemininotebook/answer/17003757>
- Gemini Android 上傳檔案：<https://support.google.com/gemini/answer/14903178?co=GENIE.Platform%3DAndroid&hl=en>
- Gemini iPhone／iPad：<https://support.google.com/gemini/answer/13275745?co=GENIE.Platform%3DiOS&hl=en>
- Gemini Notebook 來源 grounding：<https://support.google.com/gemininotebook/answer/16179559>
