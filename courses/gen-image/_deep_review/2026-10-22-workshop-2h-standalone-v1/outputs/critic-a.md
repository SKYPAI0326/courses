# Critic A Report

verdict: `NOT_READY`

## A-001

- claim: HTML 的時間標籤與 120 分鐘路線圖互相矛盾；依頁面數字加總為 140 分鐘。
- evidence: HTML 160 行把版型與線稿合併排在 0–20 分；178、201 行又分別標為 20 分鐘。其餘數字標籤為 30、20、10、25、15 分，合計 140 分。Markdown 85、92 行則把兩者合併為同一個 20 分鐘單元。
- impact: 學員與講師無法依 HTML 判斷每段實際配速，兩小時流程與 Markdown 忠實度未成立。
- severity: MAJOR
- confidence: HIGH
- proposed_check: 讓每個時間徽章對應唯一且不重疊的分鐘區間，程式加總為 120，再逐段對照 Markdown。

## A-002

- claim: 獨立課程命名修復未完成，且 token 驗證產生偽陰性。
- evidence: HTML 271 行仍有 `(05) · MODULE C`；HTML 400、467 行及 Markdown 241、280 行仍有 `C＿＿＿＿`、`正確的 C 類型`；execution-output 卻回報 `visible_bad_tokens=[]`。
- impact: 違反 standalone audience constraint，且 token scan 未涵蓋英文同義詞與殘留代號。
- severity: MAJOR
- confidence: HIGH
- proposed_check: 掃描 `MODULE C`、`模組 C`、`C[1-6]`、`C＿`、`C 類型`，再人工逐段確認只使用六個獨立名稱。

## A-003

- claim: RWD／互動驗收尚未成立，且既定補驗尺寸不符合凍結契約。
- evidence: course-html-contract 要求 1440、820、390 px；execution-output 顯示 browser smoke PENDING；repair report 預定 1440、390、430 px，漏掉 820 px。
- impact: 靜態 PASS 不能支持 responsive usability，平板版沒有驗收證據。
- severity: MAJOR
- confidence: HIGH
- proposed_check: 依契約在 1440、820、390 px 實測頂端、中段、底部、下載、導覽與 localStorage 狀態。

## A-004

- claim: `local_refs=33 missing=0` 無法在凍結基線重現。
- evidence: 在 frozen bundle 重播 33 個相對 href/src 得到 3 個 missing occurrences、2 個唯一目標：`../../index.html` 一次、`index.html` 兩次；來源是 HTML 106、117、537 行。
- impact: 凍結成品若獨立交付，品牌首頁與課程首頁連結失效；link check 是在較大的工作樹執行。
- severity: MINOR
- confidence: HIGH
- proposed_check: 對實際交付 root 重跑，或明示這些是部署依賴並納入快照。

## A-005

- claim: 圖片獨立設計且未重用參考 PDF 圖像，目前只有作者聲明，沒有獨立 provenance 證據。
- evidence: image manifest 只有生成方式及未使用 PDF 圖片／提示詞／具體版面的自述；execution output 沒有生成事件、reference-input 清單、相似度檢查或獨立素材比對。
- impact: 明示的原創素材邊界無法由凍結證據獨立確認。
- severity: MAJOR
- confidence: HIGH
- proposed_check: 保存每張資產的生成事件、實際 reference inputs、輸出 hash，並逐張比對 PDF 圖像，記錄 exact/perceptual reuse。

## A-006

- claim: Markdown 與 HTML 對應留下的成果定義不一致。
- evidence: Markdown 71–77 行要求任務句、六段式視覺 brief 等五項成果；HTML 530 行只要求兩張 PNG、prompt 與檢核表。
- impact: 學員可能缺少兩項學習證據，驗收者也沒有單一交付清單。
- severity: MINOR
- confidence: HIGH
- proposed_check: 凍結唯一 learner deliverables contract，逐項映射到 HTML 開場、工作紙與最後收件清單。

findings_count: 6

unknowns:

- 120 分鐘實際可完成性。
- 1440／820／390 px 實際排版、下載與 localStorage。
- 開課日 ChatGPT、Gemini、Canva 帳號流程。
- PDF 與十個視覺之間是否完全沒有直接資產重用。
- 部署環境是否另有可解析的 `index.html`。
- fresh-context 隔離機制未驗證。
