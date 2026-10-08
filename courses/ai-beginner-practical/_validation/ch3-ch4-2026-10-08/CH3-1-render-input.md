
## 把三份工作文件變成同事能使用的答覆

新同仁問R教室能收幾人，公告寫18人，較新的會議紀錄卻寫20人。若直接使用摘要，未核准的數字就可能變成對外承諾。這一章讓你從自己的三份來源出發，在NotebookLM生成一份FAQ、交接摘要或會議待辦，逐句回查重要主張，保留矛盾與未知，最後留下可交給承辦人的修正版。

每人獨立選一組素材和一種成品，不需要同學文件，也不需要先完成Gamma。你可用教育行政A、服務交接B，或自己已有的同情境三文件。若選原新聞／公告／書籍來源，仍只需選一份有讀者的摘要成果，遵循相同引用查核；原三類完整作業列選做。

先展開下方A或B的三份原文，再[開啟NotebookLM／Gemini Notebook](https://notebook.google.com/)，在自己的帳號建立筆記本，分別加入三份文字，保留DA1／DA2／DA3或DB1／DB2／DB3的名稱。第一個可觀察結果是來源列表有三個可辨認名稱、能打開讀到段落。沒有三份就回來源加入步驟，先不要讓AI回答。

### 選自己的完整材料

A適合教務、行政或活動承辦：一般規範、核准公告與會議紀錄；要辨認同一欄位的數字差異。B適合服務、客服或業務支援：案件規範、首次回覆公告與案件交接；要分清回覆、結案與尚待執行。兩組是教學模擬，資料不互相混用。

<details class="workbench-disclosure"><summary>A1排課規範（展開完整內容）</summary>
<p><a href="assets/workplace/documents/case-a/01-sop.txt" download>下載原檔</a>；<button type="button" data-gamma-copy="case-a-1">複製A1排課規範</button></p>
<div data-raw-token="0"></div>
</details>

<details class="workbench-disclosure"><summary>A2試辦公告（展開完整內容）</summary>
<p><a href="assets/workplace/documents/case-a/02-notice.txt" download>下載原檔</a>；<button type="button" data-gamma-copy="case-a-2">複製A2試辦公告</button></p>
<div data-raw-token="1"></div>
</details>

<details class="workbench-disclosure"><summary>A3協調會議（展開完整內容）</summary>
<p><a href="assets/workplace/documents/case-a/03-meeting.txt" download>下載原檔</a>；<button type="button" data-gamma-copy="case-a-3">複製A3協調會議</button></p>
<div data-raw-token="2"></div>
</details>
<details class="workbench-disclosure"><summary>B1案件規範（展開完整內容）</summary>
<p><a href="assets/workplace/documents/case-b/01-sop.txt" download>下載原檔</a>；<button type="button" data-gamma-copy="case-b-1">複製B1案件規範</button></p>
<div data-raw-token="3"></div>
</details>

<details class="workbench-disclosure"><summary>B2首次回覆公告（展開完整內容）</summary>
<p><a href="assets/workplace/documents/case-b/02-notice.txt" download>下載原檔</a>；<button type="button" data-gamma-copy="case-b-2">複製B2首次回覆公告</button></p>
<div data-raw-token="4"></div>
</details>

<details class="workbench-disclosure"><summary>B3交接會議（展開完整內容）</summary>
<p><a href="assets/workplace/documents/case-b/03-meeting.txt" download>下載原檔</a>；<button type="button" data-gamma-copy="case-b-3">複製B3交接會議</button></p>
<div data-raw-token="5"></div>
</details>

### 引用支持哪一句，版本適用哪裡

來源是加入筆記本的原文；主張是文件中一個可以核對的說法；引用是回答中可點回原文的位置。看到引用後仍要讀支持段落。例如「1工作天首次回覆」支持回覆期限，無法支持「1工作天結案」。一句同時寫期限與成效時，引用若只支持期限，就拆成兩句，把成效標為來源未提及。

先看文件狀態與適用範圍，再看日期。一般SOP可以被核准公告明示取代；只寫在較新會議中的提議，仍未取得變更核准。A的公告明示R教室期間內3個工作天取代一般5天，其他教室維持5天；18／20人的差異未附變更核准，須並列版本待確認。B的首次回覆1天取代2天，沒有改結案期限。這些是不同判斷，不能用「最新文件優先」一口氣處理。

主張核對時分成「原文明確支持／只支持部分／來源未提及／來源矛盾待確認」。合理推論可以保留在建議區，但必須標你的推論，不能當成已核准規定。成品至少含三個已回查的重要主張，以及一個矛盾或缺資料；直接在文件標註，不另抄三張閱讀表。

### 短示範：看一筆原文如何改變答覆

這是獨立微型素材，僅觀察，不加入自己的案例筆記本、不交示範副本。

```text
M1 一般通知：報名須提前5個工作天。
M2 核准試辦公告：只適用R教室2026-10-15至11-14，報名提前3個工作天；明示取代一般期限。
提問：R教室在試辦期間要提前多久？其他教室也改3天嗎？
```

處理時先對齊「教室、期間、期限、取代關係」。中間判斷是M2只覆蓋R教室與指定期間；M1仍支持其他教室。可使用的完成句為：「R教室試辦期間至少提前3個工作天（M2）；其他教室維持5個工作天（M1）。」錯句「所有教室都提前3天」丟掉適用範圍；修正時補回教室與期間。M代號只是示範定位，正式成品要點NotebookLM的實際引用。

### 先選用途，再送一份成品提示詞

選FAQ是讓新進同仁快速找到答覆；選交接摘要是讓接手者知道現在做到哪裡；選待辦是讓承辦人知道動作、負責角色、期限與前置確認。三種提示詞只選一份，已完成一份就不追加另外兩份。把下面所選提示詞送到自己加入三來源的筆記本，保存實際送出文字與第一版。

<details class="workbench-disclosure"><summary>六題FAQ提示詞（展開完整內容）</summary>
<p><a href="assets/workplace/documents/prompts/faq.txt" download>下載原檔</a>；<button type="button" data-gamma-copy="prompt-faq">複製六題FAQ提示詞</button></p>
<div data-raw-token="6"></div>
</details>

<details class="workbench-disclosure"><summary>一頁交接提示詞（展開完整內容）</summary>
<p><a href="assets/workplace/documents/prompts/handoff.txt" download>下載原檔</a>；<button type="button" data-gamma-copy="prompt-handoff">複製一頁交接提示詞</button></p>
<div data-raw-token="7"></div>
</details>

<details class="workbench-disclosure"><summary>會議待辦提示詞（展開完整內容）</summary>
<p><a href="assets/workplace/documents/prompts/actions.txt" download>下載原檔</a>；<button type="button" data-gamma-copy="prompt-actions">複製會議待辦提示詞</button></p>
<div data-raw-token="8"></div>
</details>

### 跟著操作自己的來源，接著獨立修成可用版本

1. **U3-SOURCE：建立自己的筆記本。** 加入所選同案例三份來源，填工作台中的筆記本與三個來源名稱。結果應是三份都可開啟；讀不到時下載原文重新加入，保留原回答，不混另一組資料。
2. **U3-CLAIM：生成自己的第一版。** 送一份成品提示詞，把實際提示詞與回答貼進工作台「第一版」。結果應只有所選的一種成品，重要主張附引用；若只剩長摘要，指定所選欄位重問，保存錯版。
3. **U3-CITE：點引用回查。** 在自己的文件挑三個重要主張，點各引用讀原文，核對數字、期間、角色和狀態。把筆記本連結、來源名稱、引用標記、原文短摘及支持判斷存入「實際引用回查」。匯出文字中的引用數字不保證可點，接手者要依筆記本連結與原文短摘再回查。三個都不能只看回答文字或手寫DA／DB代號。對不上的句子拆短、改未知或矛盾。
4. **U3-COMPARE：作自己的交付判斷。** A至少檢查18／20與R教室3／一般5天；B至少檢查首次回覆／結案與已登記／尚未回覆。直接在成品保留差異、適用範圍、至少一項待確認、詢問角色和確認前能做的事。資料沒有給回覆日就不補造。
5. **U3-REPAIR：修訂自己的成品。** 送下方修訂提示詞，對一個實際錯句或模糊句記錄原句、修句與依據。第一版若正確，就挑一個語意過寬的句子加上期間／角色／條件，說明理由；不能虛構一個錯誤交差。將最終文件貼入「修訂成品」，簡短理由與仍待確認問題留在「修訂理由」。
6. **U3-SAVE：匯出並重開。** 匯出`unit3-notebooklm-reading-pack-complete.md`，在下載資料夾重開；確認自己能找到來源、第一版、三筆真引用回查、修正版與未解問題。未填的選做欄不影響保存。檔案找不到先檢查下載位置，不能暫存就立即匯出或列印，勿清除其他紀錄。

<details class="workbench-disclosure"><summary>來源查核修訂提示詞（展開完整內容）</summary>
<p><a href="assets/workplace/documents/prompts/repair.txt" download>下載原檔</a>；<button type="button" data-gamma-copy="prompt-repair">複製來源查核修訂提示詞</button></p>
<div data-raw-token="9"></div>
</details>

<span data-gamma-copy-status role="status" aria-live="polite">展開材料後可直接複製完整原文或提示詞。</span>

### 完成自己的版本後才對照參考

下方為作者依原文編製的完整參考。它們讓你判斷內容與邊界，不能代替自己的NotebookLM回答或引用實跑。A的FAQ與B的交接都可直接看出怎麼保留未解問題；選待辦時依同一份來源抽取動作，不把詢問期限推成對方回覆期限。

<details class="workbench-disclosure"><summary>A完整FAQ參考（展開完整內容）</summary>
<p><a href="assets/workplace/documents/case-a/reference-faq.md" download>下載原檔</a>；<button type="button" data-gamma-copy="reference-a">複製A完整FAQ參考</button></p>
<div aria-label="材料閱讀預覽" class="material-preview">
<h4>案例A參考成品｜新進教務同仁FAQ（作者示例）</h4>
<p>本檔是作者依原文編製的參考答案。以下DA代號只作人工定位，不能當成NotebookLM實跑引用。</p>
<table>
<thead>
<tr>
<th>問題</th>
<th>可使用的答覆</th>
<th>原文定位</th>
<th>待確認</th>
</tr>
</thead>
<tbody><tr>
<td>1. 試辦適用哪裡、何時？</td>
<td>只適用R教室，2026-10-15至11-14；其他教室維持v1。</td>
<td>DA2-P01、DA1-P02</td>
<td>期滿後安排尚未公告。</td>
</tr>
<tr>
<td>2. R教室可收幾人？</td>
<td>核准公告列18人；較新的會議列20人但未附變更核准。必須先確認，不能對外宣稱20人已核准。</td>
<td>DA2-P02、DA3-P01/P03</td>
<td>教務窗口應於10-22前向中心主管確認；回覆日期未提供。</td>
</tr>
<tr>
<td>3. 要提前多久、怎麼送？</td>
<td>期間內R教室提前至少3個工作天送至教務信箱；其他教室原則為5個工作天。</td>
<td>DA2-P02、DA1-P01/P03</td>
<td>需查中心行事曆；電話預約仍是未決議提議（DA3-P02）。</td>
</tr>
<tr>
<td>4. 送件後就能開課嗎？</td>
<td>須由教務窗口確認場地才成立；本次會議未核准特定課程。</td>
<td>DA1-P03、DA2-P02、DA3-P05</td>
<td>各課程是否確認須另查，來源未提供。</td>
</tr>
<tr>
<td>5. 有協助需求怎麼辦？</td>
<td>在申請註記，交教務窗口彙整並由中心主管確認。</td>
<td>DA1-P04、DA2-P04、DA3-P04</td>
<td>設備、支援人員、預算未提供，不能保證特定服務。</td>
</tr>
<tr>
<td>6. 試辦之後仍用18人和3天嗎？</td>
<td>目前公告只涵蓋試辦期間，不能延伸成永久規定。</td>
<td>DA2-P03</td>
<td>期滿容量與期限待正式公告。</td>
</tr>
</tbody></table>
<p>現在可做：收齊課名、日期、時段、人數、講師聯絡方式，註記協助需求，送交教務窗口；等待場地確認。容量矛盾未解前暫停對外承諾20人。
修訂示例：「R教室已核准20人」→「公告18人與會議20人不一致，變更核准未附，待教務窗口確認」。理由：DA3日期較新不足以證明核准。</p>
</div>
<details class="raw-material"><summary>原始文字（保留完整貼入格式）</summary>
<div data-raw-token="10"></div>
</details>
</details>
<details class="workbench-disclosure"><summary>B完整交接參考（展開完整內容）</summary>
<p><a href="assets/workplace/documents/case-b/reference-handoff.md" download>下載原檔</a>；<button type="button" data-gamma-copy="reference-b">複製B完整交接參考</button></p>
<div aria-label="材料閱讀預覽" class="material-preview">
<h4>案例B參考成品｜C017一頁交接摘要（作者示例）</h4>
<p>以下DB代號為人工定位，未代表NotebookLM平台已實跑。</p>
<ul>
<li>任務與讀者：接手服務窗口處理C017告示內容不清案件。10-20 15:00收件，屬10-15至11-14新受理案件試辦期間（DB3-P01、DB2-P01）。</li>
<li>已完成：已登記。尚待處理：首次回覆未寄出；照片待補，先受理並註記原因（DB3-P01、DB1-P03、DB2-P02）。</li>
<li>期限與條件：首次回覆1個工作天內；一般規範2個工作天在試辦範圍被明示變更。這是首次回覆，結案期限未提供。假日／夜間起算與行事曆待確認，不能補造確切到期時間（DB1-P01/P04、DB2-P01/P03、DB3-P02）。</li>
<li>負責窗口：服務窗口。下一步：查既有表單聯絡資料，確認告示位置與不清楚之處，寄首次回覆並補記交接狀態；不能先勾已寄（DB3-P01/P02）。</li>
<li>管道：既有表單。新共用看板仍為提議，權限、日期未核准；切換應暫停（DB1-P04、DB2-P02、DB3-P03）。</li>
<li>人工確認：服務窗口於10-22前詢問站主任假日收件起算與代理輪值。10-22是詢問期限，站主任回覆日期未提供（DB3-P04）。</li>
<li>成效：結案時間與改善結果來源未提及（DB3-P05）。</li>
</ul>
<p>修訂示例：「C017已回覆且必須10-22結案」→「C017首次回覆尚未寄出，適用1工作天首次回覆規定；結案期限未提供」。理由：DB3-P01明示未寄，DB3-P04的10-22是另一項詢問期限。</p>
</div>
<details class="raw-material"><summary>原始文字（保留完整貼入格式）</summary>
<div data-raw-token="11"></div>
</details>
</details>

### 一份成品怎麼驗收、怎麼帶回單位

成品中有同一情境三來源、明確讀者及選定格式；至少三個重要主張已點引用回到原文；一個矛盾或缺漏留在正文並有下一步；有第一版、一次具體修訂與重開的匯出檔。進度條只表示必做欄位已填，不代表引用正確或成果已能使用。

自己隔開提示詞，只看成品回答「根據在哪裡、哪些還不能答、接手者現在能做什麼」。答不出時回U3-CITE或U3-COMPARE；驗收不用同桌，也不用其他學員的檔案。下次到自己的單位，替換可使用的SOP、公告、會議文件，先確認同一業務與版本，不把課程模擬規定帶回當成真規定。

NotebookLM不可用時，下載所選三份原文，使用[工作文件離線備援](assets/workplace/documents/fallback.md)人工回查，成品首行寫「平台待重跑」。工具恢復後加入相同三來源、送已保存提示詞、點實際引用再匯出；備援完成不勾正式引用驗收。現行介面依當期功能名稱找建立筆記本、加入來源與查看引用，本教材不指定固定按鈕位置。Google說明已使用Gemini Notebook名稱；可貼上文字建立來源，短來源可能引用整份文件，這時仍要打開原文找支持句。[新增來源說明](https://support.google.com/gemininotebook/answer/16215270?hl=zh-Hant)、[對話與引用說明](https://support.google.com/gemininotebook/answer/16179559?hl=zh-Hant)（2026-10-08文件查核；帳號實機仍待重跑）。
