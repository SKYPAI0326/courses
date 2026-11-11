# 講義套用：將確認候選銜接回原HTML

在course-manager對話使用「講義套用：課程／章節，先做預覽」。若來源是HTML且預計沿用該頁版型，先依下方流程做H3前相容性預檢；通過後再讀取既有run，確認候選H3、目前章節complete及來源未變。不重新潤稿、不增加文案候選版數。這個階段只建立隔離HTML預覽，不包含正式替換或發布。

## 輸入與產出

輸入為單章state、其中已確認的Markdown候選、原HTML及明確的區段映射。產出包含原HTML快照、候選快照、preview.html、來源／候選／H3／映射／預覽雜湊manifest、檢查紀錄及畫面證據。HTML預覽版本與文案版本分開記錄；同一候選可以為排版修正產生另一份預覽，但不能藉此改寫候選。

## H3前相容性預檢

若候選來源是HTML，且預計沿用該頁版型，在接受H3前先比對原頁與候選：

```bash
python3 scripts/course_handout_apply.py --preflight \
  --source '/完整路徑/原講義.html' \
  --candidate '/完整路徑/候選.md' \
  --output '/隔離工作目錄/preflight.json'
```

預檢檢查H1、`.lesson-body`、候選區塊支援情況、H2與原區段數差異，並列出原頁需保留的複合元件數量。H1不一致、頁型不符或有不支援區塊會回報`blocked`，表示候選不能直接套入這份HTML；若同一版本要同時做H3認可與後續套用，先完成對齊，並讓H3綁定對齊後的檔案。其他差異列為映射注意事項。報告只綁定來源與候選雜湊，不判文案品質、不寫HTML、不呼叫模型、不改run的H3狀態，也不代表套用授權；即使`passed`，後續仍要完成明確映射、預覽及桌機／手機互動檢查。

沿用唯一`.lesson-body`頁型，使用BeautifulSoup與markdown-it-py（本機已可用，列於pyproject的handout額外依賴）。既有`--state`模式保持原有p/h2/pre支援；追加候選的`--confirmation`模式支援有序／無序清單、Markdown表格及頁首內容的明確映射。遇到其他未支援區塊、頁首標題變動或其他頁型時停止，不丟掉內容或改成通用版型。

既有教材批次套用可在映射中明列`extended_blocks: true`，支援h3／h4、引言、水平線、折疊答案及頁首成果清單；不接受候選新增程式或操作元件。`preserve_prompt_controls: true`逐一沿用原pre或data-policy-prompt節點及對應複製控制，避免把含下一段提示詞的整個父層重複複製。候選將原提示詞寫成同文段落時仍保留原提示詞容器。`preserve_dom`只接受唯一且位於已映射正文區段內的selector，用來保留原可操作參考工具；未映射、不唯一或提示詞遺漏仍拒絕。原CSS／JS、section殼層、錨點及控制屬性須另外逐項核對。上述選項未啟用時，歷史映射行為不變。

候選在第一個二級標題前同時包含導言、完成物與任務清單時，可用`intro_groups`將這些原始區塊依零起算索引分組，再在`groups`逐組指定原頁首容器。索引必須依序完整覆蓋，不可重複或遺漏；不改候選檔。實作頁的完成物可能位於`.howto`而非`.outcomes`，須依實際DOM明確映射。`markdown_label`只將明列的頁首`**標籤**`解析為粗體HTML，保留標籤與後文，不是改寫文字。

## 追加候選的獨立H3入口

使用者明確接受追加候選時，另存原話與`handout-confirmation-1`確認JSON，包含`status: confirmed`、`actor`及`source`／`candidate`／`feedback`三份實際檔案的path與sha256。這是指定版本的內容認可，不把仍停在compare的歷史run改成complete、不重算版數，也不包含正式覆寫或發布。任一輸入變更即拒絕沿用H3。

使用`--confirmation H3.json --mapping mapping.json --output preview-v1`，不可同時帶`--state`。映射的`groups`按候選順序列`intro`及每個二級標題，每項指定唯一`selector`與`mode`（intro／outcomes／agenda／section）；section須位於原lesson-body內。保留原五區段與eyebrow，不以缺少id為由重建殼層；需要新增錨點可明訂`id`，既有id不得更改。頁首導言、完成物與任務留在原容器，不重複塞入正文。提示詞以原文唯一匹配沿用原容器與複製控制；同目的地連結保留target／rel等行為。表格完整渲染並有局部捲動保護，清單保留語意。

實際範例：[CH2-2獨立H3與映射](../operations/course-content-scoring/handout-apply-gen-ai-36h-ch2-2-extension-2/H3.json)、[mapping.json](../operations/course-content-scoring/handout-apply-gen-ai-36h-ch2-2-extension-2/mapping.json)。仍須完成下列內容、結構及三尺寸互動檢查，才可登記預覽就緒。

### 候選需沿用原有複合元件時

若一般`section`映射會清除或攤平原頁的圖卡、步驟卡、callout、表格、提示詞控制或內嵌圖片，改用`layout_strategy: preserve-existing-components`，由`src/course_handout_component_overlay.py`處理。映射須逐區指定既有元件與候選內容位置，並列出必須維持的元件數量；標題中的段號／時間標籤可映射回原eyebrow，頁尾文案仍留在頁面殼層。產製時核對元件數、提示詞、圖片、錨點、連結目的地及候選區塊對應；任一對應不唯一或元件數變動即停止。此策略只在既有容器內更新文字或加入候選要求的內容節點，不重建頁面殼層、不新增操作元件，也不授權改寫正式來源。完成後仍須依一般流程做瀏覽器檢查；結構與連結檢查不能代替畫面驗收。

## 套用步驟

1. 讀取course-html-contract並記錄`task_scope: content-change`。以確認候選全文作文字依據，列出段落對應及DOM影響；無必要不改殼層。
2. 建立映射JSON：`intro_id`對應候選標題後、第一個二級標題前的導言；`sections`依候選二級標題順序指定原區段id，新增區段須記原因，原錨點不可默默移除。沒有合適對應時先停，不猜。
3. 執行產製：

```bash
python3 scripts/course_handout_apply.py \
  --state '/既有run/units/章節/state.json' \
  --mapping '/本次套用/mapping.json' \
  --output '/本次套用/preview-v1'
```

輸出目錄須不存在，既有預覽不覆寫。程式只替換正文子樹，維持外層容器、原CSS／JS及導覽；原pre全文與copy控制節點依唯一內容對應沿用。連結重算相對位置，但保持目的地。每個候選區塊有可追溯標記；不一致、重複id、遺失原pre、未取得H3或來源變更均拒絕。

4. 執行結構、文字對應與本機連結核對，再於瀏覽器檢查桌機1440、平板820、手機390，含頂部／修改區／結尾、複製、導覽、錨點與捲動恢復。原頁若有登入門檻，保持正式存取程式；本機測試狀態須記錄及清除，不改正式認證。畫面有問題就修正預覽並重新驗證受影響部分。
5. 保存檢查JSON，以`--output ... --checks .../checks.json`登記。必須綁定目前預覽SHA、內容與互動通過、必要尺寸無整頁溢出，以及可核對雜湊的畫面檔；來源、候選、state、mapping或預覽變更即拒收舊證據。程式確認證據完整及版本，不代替執行者判讀畫面。

檢查JSON格式可參考[本次實際紀錄](../operations/course-content-scoring/handout-apply-gemini-ch2-2/preview-v2/checks.json)。`grid_pre_indices`是可選的原pre零起算索引，僅在實際發現文字表格換行錯位時使用，增加該區塊的保留行列與區內橫向捲動，不更動文字。

套用會額外核對原form、input、textarea、select、button及`data-gen36-form`動態容器的數量與識別屬性；任一遺失就在寫出預覽前拒絕。動態容器即使原始碼內沒有欄位，也不能因候選只有文字而省略；在支援的映射中以`preserve_dom`明確保留，不支援時回報具體元件。此檢查不能取代瀏覽器填寫、保存與匯出測試。

## 停止與人工位置

產製後狀態為`pending_browser_checks`；完整證據登記後為`preview_ready_for_review`，意義是可交使用者比較版面，不代表使用者已接受預覽。使用者確認正式套用後，才另行備份並替換明確指定正式檔；本版沒有正式覆寫或發布命令，也不因先前H3而自動發布。

若修版面需要改文案，返回原候選流程重新確認，不在HTML內偷偷改寫。若原稿、候選或H3版本已變，先辨認差異，不把舊認可沿用到新稿。

上述預設不縮減使用者本次已明確給予的套用或發布授權。整課要求須逐頁記錄實際套用與未完成項；發布則確認網站來源分支、部署結果及公開內容版本，工作分支push不是網站已更新。

## 已完成示範

[Gemini CH2-2預覽與核對紀錄](../operations/course-content-scoring/handout-apply-gemini-ch2-2/套用結果.md)：沿用已確認的第一版文案，原版型在手機表格發現換行問題，僅加局部捲動保護後產生preview-v2。正式HTML、原run、候選與CH1-3狀態均未改。
