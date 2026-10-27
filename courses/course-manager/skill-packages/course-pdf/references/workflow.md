# course-pdf 命令與責任

技能是操作入口；引擎由 `COURSE_PDF_ENGINE` 明確指定，或使用 `COURSE_DESIGN_SYSTEM_ROOT/scripts/pdf_pipeline.py`。課程根目錄由 `COURSE_WEB_ROOT` 指定，狀態與配方由 `COURSE_DESIGN_STATE_ROOT` 指定；缺少任一必要設定時 fail closed。

先執行 `python3 <skill>/scripts/run.py doctor`；本文 `<skill>` 指當前已讀取的技能目錄，不是可直接貼上的路徑。

| 命令 | 行為 |
| --- | --- |
| `inventory` | 唯讀列出整個 courses 的 PDF，按講義庫／素材待判／備份／驗收／worktree 分類 |
| `register-existing` | 只登錄講義庫現有 PDF，重跑不重複登錄；寫 catalog 及 INDEX.md |
| `plan --recipe FILE` | 唯讀檢查配方、選取內容、依賴及網址，計算指紋 |
| `bind --recipe FILE` | 登錄已閱讀且檢查通過的 HTML 配方；不將舊 PDF 升為 CURRENT |
| `status [--course SLUG] [--artifact ID]` | 即時比較來源／成品／驗收證據，不改成品 |
| `sync [--course SLUG]` | 預設 PLAN_ONLY；列出有配方的受影響成品 |
| `build --recipe FILE --create-pdf` | 明確授權後產候選 PDF；永不直接替換現行版本 |
| `sync --course SLUG --create-pdf` | 產受影響候選，逐份保持待驗；不自動提升 |
| `verify --manifest FILE [--review FILE]` | 核對來源、成品和證據；沒有全頁 review 時仍是 PENDING_REVIEW |
| `promote --manifest FILE --review FILE` | 通過全頁驗收後更新 PDF、catalog、INDEX，保留前版回復資料 |
| `rollback --manifest FILE [--apply]` | 預設 dry-run；支援已提升或提升中斷的交易，拒絕覆蓋後續改動 |

配方至少含 schema_version=1、artifact_id、course、output、profile、sources。sources 的 path、selectors、source_url、static_content_confirmed 必須逐一核對；最後一項是執行者讀過來源的聲明，程式不會自動證明動態內容完整。

現有配方見專案 `registry/pdf/recipes/`。新增或修訂配方時逐一核對來源，不以其他配方已通過為理由批次複製確認旗標。跨課程合冊需在 source_courses 明列實際來源課程；來源順序依現有網頁入口及原成品用途確認。

CURRENT 必須有已提升 manifest、相同來源／環境指紋、成品 hash 及有效全頁 review。來源異動為 STALE；未建置或證據不明為 UNVERIFIED；缺件／不完整提升為 BLOCKED。最近建置結果另記 PENDING_REVIEW／FAILED，不能掩蓋前版過期狀態。

外部渲染資產必須先有已確認的本地快照與 SHA256；remote_assets 使用 URL → {path, sha256}。引擎不自動下載／補圖，網路渲染請求會被阻擋。Google 字型 CSS 僅在已宣告本地字型時替換，保留轉換紀錄。外部教材連結保留網址，但存活性驗證需另外取得實際證據；不得把「URI 存在」說成連結已可達。

建置輸出包含 original-N.html、print-source.html、manifest.json、candidate.pdf、machine-verification.json、每頁 PNG 及 review-template.json。保留模板原檔，將實際檢查結果另存為 review.json；缺頁、修改過的圖像、不同 PDF hash、未解決問題或未完成品質檢查都不能提升。

是否產製及更新依當次使用者授權；「檢查差異，有差異就更新」包含候選產製、驗收及保留備份後提升。來源不明的 PDF-only、編輯版或節錄版保留原成品並報告缺口。

原生 input／textarea／select 如需印出來源值，配方須明列已確認的 paper_fallback=print-source-values；只保留來源既有 value、placeholder、options 及標籤，不代填答案。password 類型阻擋。

文字驗收先比較列印 DOM 的完整內容及順序，再比較 PDF 原文片段及字元數量；PDF 擷取閱讀順序不同時保留機器證據，不能以移除教學文字使驗收通過。全頁視覺驗收可重用與已實際檢視頁面逐像素完全相同的圖像證據；僅容許獨立確認無教材文字的原生頁碼區遮罩，必須記錄參照頁、圖像 SHA256 及方法。

來源網頁 CSS 導致合冊列印失敗時，可在專用紙本 profile 使用優先層級及明確重設樣式。先確認選定原文與列印 DOM 完全一致，再核對表格、程式碼、連結及每頁畫面；不得藉改寫 HTML 或刪除教材避開問題。

引擎指紋變更預設重新建置。若變更僅限驗收器，且可證明列印／提升程式 AST、全部其他依賴及環境、來源快照、正式 PDF、接受的逐頁 review 與圖像均未變，才可用有備份的專項重新驗收保留既有成品。必須重新執行機器及全頁證據驗證，記錄原 render_fingerprint、render_dependencies、render_environment 與 validation_revisions；不能只改指紋或把重新驗收說成重新渲染。範例：`operations/pdf-sync/2026-10-11/revalidate_validator.py`。
