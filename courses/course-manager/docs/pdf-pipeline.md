# 課程 PDF 轉製與管理

技能原始套件位於 `skill-packages/course-pdf/`；本機入口安裝至 `/Users/paichenwei/.agents/skills/course-pdf/`。引擎只保留在 course-manager，launcher 不複製引擎。

使用者已於 2026-10-11 授權比對與更新現存 PDF。來源準備、登錄、指紋／狀態、候選建置、全頁驗收與前版回復使用同一流程；本次實際結果見 reports/pdf-sync/2026-10-11/。沒有配置 watcher 或排程。

## 可直接使用的非產製命令

在本資料夾執行：

```sh
python3 scripts/pdf_pipeline.py doctor
python3 scripts/pdf_pipeline.py inventory
python3 scripts/pdf_pipeline.py status
python3 scripts/pdf_pipeline.py sync --course admin-ai-assistant
python3 scripts/pdf_pipeline.py plan --recipe registry/pdf/recipes/admin-ai-ch01.json
```

或從任何資料夾使用安裝入口：

```sh
python3 /Users/paichenwei/.agents/skills/course-pdf/scripts/run.py status
```

`--root` 為 courses 資料夾，放在引擎子命令之前。doctor 只檢查套件、Chromium bytes 與 pdftoppm 位置，不宣稱已成功啟動瀏覽器。無依賴時回報缺件；本機已確認 Python 3.12 有 BeautifulSoup、Playwright、pypdf，bundled Python 缺少前兩項，不直接用它執行轉製。需要時以 `COURSE_PDF_PYTHON` 指定其他已確認可用的 Python。

inventory、plan、status、sync 預設唯讀；前三者可在 course-manager 內用 `--write reports/pdf/...` 保存 JSON 報告；其他工作目錄請指定完整報告路徑，路徑以執行時 cwd 解析。register-existing 只寫登錄與 INDEX，不搬檔或產 PDF。bind 只寫已核對的配方對應，不證明舊成品一致。

## 檔案與來源狀態

- `registry/pdf/catalog.json`：38 份已集中成品的登錄。原有資料夾 catalog.json 不受影響。
- `registry/pdf/recipes/`：一份 PDF 對應一份明確配方。配方的範圍與批次建置清單見 operations/pdf-sync/2026-10-11/build-plan.json；沒有配方的編輯摘錄及來源缺失成品須另外處理。
- `pdf-profiles/default.css`：A4 列印配置。不同閱讀版面可另存 CSS 並由配方指向，不改教材內容。
- `../output/pdf/INDEX.md`：按課程提供取用與最後登錄狀態。它是快照；最新來源狀態以 status 計算為準。
- `operations/pdf-build/`：每次候選、來源快照、驗收、提升交易與前版備份。

UNVERIFIED＝沒有有效已驗收建置證據。CURRENT＝來源／依賴／環境指紋、成品與已提升證據一致。STALE＝有效前版的來源有變動。BLOCKED＝缺件／不完整提升／不支援來源。最新建置的 FAILED 或 PENDING_REVIEW 另記，不掩蓋前版狀態。

HTML、遞迴 CSS 資產、圖片、素材檔、字型、配方及引擎 bytes 都納入指紋。來源 script 檔列依賴，轉製副本不執行 script；inline JS 由 HTML hash 覆蓋。配方 static_content_confirmed 須由實際閱讀正文及腳本的人確認，不能批次推論。未顯式宣告的動態／JS 運算依賴不具備完整追蹤保證。

外部渲染資產使用 URL → 本地檔與 hash 的 pin；CSS 的不支援 import、未 pin 的外部圖像或腳本阻擋轉製。Google 字型 CSS 只有在宣告本地字型時才替換並記錄。講義庫內的 PDF 下載連結是輸出參照，不自動列輸入 bytes，避免合冊與模組互相連結造成循環過期；其他素材 PDF 或明確宣告的輸入仍可列依賴。

## 配方

格式見 `registry/pdf/recipe-schema.json`；程式另檢查工作區路徑、成品位置、selector 重疊、來源順序及缺失資產。

```json
{
  "schema_version": 1,
  "artifact_id": "admin-ai-ch01",
  "course": "admin-ai-assistant",
  "output": "output/pdf/admin-ai-assistant/ADMIN-AI-CH01-從-AI-工具到行政虛擬助理方案.pdf",
  "profile": "course-manager/pdf-profiles/default.css",
  "sources": [{
    "path": "admin-ai-assistant/CH1.html",
    "selectors": ["main#main"],
    "source_url": "https://skypai0326.github.io/courses/courses/admin-ai-assistant/CH1.html",
    "static_content_confirmed": true
  }],
  "font_files": ["/Library/Fonts/Arial Unicode.ttf"],
  "exclude": [], "expand": [], "dependencies": [], "remote_assets": {}
}
```

sources 按確認過的教學順序排列；每個來源的 selectors 按 DOM 順序處理，禁止重疊。一般正文不排除。exclude 僅支援按鈕／導覽容器，包含教材就阻擋；expand 須指定既有隱藏教材及原因。details 展開、有 label 的 radio／checkbox 只移除 widget。跨課合冊以 source_courses 顯式列出允許的課程來源。原生表單可在逐一確認後宣告 paper_fallbacks，mode=print-source-values：僅印原始 value、placeholder 或 option 文字；隱藏控制參數留紀錄而不加入教材，密碼欄阻擋。沒有宣告則維持阻擋。canvas、影片、iframe、srcset 或未知隱藏內容先回來源處理，不自動補教材。

每單元 id 加前綴，同冊內的 href 與 SVG／ARIA 引用一起映射；其他網址依各來源 source_url 轉為可用於 PDF 的絕對網址。外部網址不自動做存活性驗證。來源 CSS 以 Chromium CSS scope 隔離；不支援 scope 的瀏覽器阻擋產製。

## 產製與驗收

以下命令建立候選 PDF；每次產製須有使用者授權：

```sh
python3 scripts/pdf_pipeline.py build --recipe registry/pdf/recipes/admin-ai-ch01.json --create-pdf
```

輸出候選及全頁 PNG 後，每頁實際檢視，另存 review.json，再依輸出的真實 manifest 路徑執行 verify、promote。未檢視頁面不得填通過。verify 的一般結果是唯讀；promote 必須再次核對來源指紋、PDF bytes 及全頁 review，才替換現行成品與索引。

review 必須同時具備：精確 PDF hash、執行者種類／身分、每頁圖像 hash 與 reviewed=true、零未解決問題、字型／裁切／重疊／表格程式碼／圖片／連結各項實際通過。程式只驗證紀錄一致性，不能代替閱讀或自動證明教學語意。

列印 DOM 在轉製前須與原文順序相同。PDF 以 pypdf／Poppler 兩種讀取順序核對每個來源文字片段，另檢查字元出現次數；數字、標點及提示詞不改寫。只忽略排版空白、行政頁碼及沒有獨立可見字形的 emoji VS16 呈現控制字元。原文保留 VS16。變更數字或句意的實際回歸檢查必須被攔下；結果見 fidelity-regression.json。機器驗收仍不能代替逐頁閱讀。

提升 PDF、catalog、INDEX 為逐檔原子替換的可回復交易。manifest 在整批完成後才標 PROMOTED；交易中斷時 status 不回報 CURRENT，rollback 可依 journal 回復。rollback 預設 dry-run，--apply 才執行；若任何檔案有後續改動或備份被修改，拒絕回復。

歷史版本先保留在每次操作目錄，未建立自動清理機制。大量批次前先安排容量與保存範圍；既有備份不混入現行取用清單。產製流程不改正式來源、Git staging／忽略政策或發布。

## 聯動方式

build-course-page 完成 HTML 更新後及 course-ops 交付前，以安裝入口 `sync --course <slug>` 做唯讀狀態交接。有 PDF 登錄才報告該課程成品；沒有配方的舊 PDF 繼續顯示未驗。這是 agent 工作流程中的觸發，不能涵蓋未走該流程的人工編輯；交付前再查 status。

持續 watcher／排程沒有被建立。將來配置持續觸發時仍使用相同 sync／驗收介面；產出的候選不能跳過全頁驗收自動提升。

## 實作依據

渲染介面依 [Playwright Page PDF API](https://playwright.dev/python/docs/api/class-page#page-pdf)，隔離上下文依 [Browser API](https://playwright.dev/python/docs/api/class-browser#browser-new-context)。內容規則與整合取捨見本專案技能設計文件。
