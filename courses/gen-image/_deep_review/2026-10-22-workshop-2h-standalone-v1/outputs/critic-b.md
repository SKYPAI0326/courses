# Critic B Report

## B-01

- claim: 學員頁的可見時間標示至少合計 140 分鐘，與 120 分鐘課程及路線圖衝突。
- evidence: HTML 160–165 行將版型與線稿共同排在 0–20 分；178、201 行卻各標 20 分鐘；再加 30、20、10、25、15 分已達 140 分，尚未計入未標時間的完整示範與完稿檢核。
- impact: 按章節標示授課會超時；按路線圖授課則章節時間提示誤導。
- severity: MAJOR
- confidence: HIGH
- proposed_check: 依學員頁做 120 分鐘冷排演，納入下載、登入、生成等待、匯出與轉場，逐一校正章節時間。

## B-02

- claim: 無生圖權限備援無法依現有步驟完成必交的 1:1 延展圖。
- evidence: HTML 139–153 行宣稱 READY PNG 可完成 1:1 延展；`c1-bento-campaign.png` 是 1122×1402 扁平 PNG；HTML 498–506 行卻要求複製並重排 4:5 的「元素」；Markdown 295–299 行禁止硬裁或壓扁。
- impact: 備援學員無法個別重排內部五個區塊，只能硬裁、縮小整張圖，或使用未教且可能需付費的分離功能。
- severity: BLOCKER
- confidence: HIGH
- proposed_check: 用全新 Canva 免費帳號，只提供 READY PNG，禁止 AI 生圖與付費分離工具，完成 4:5 與 1:1 並確認能個別重排。

## B-03

- claim: 學員頁仍殘留來源課程的模組代號，命名修復與驗證出現偽陰性。
- evidence: HTML 271 行仍顯示 `(05) · MODULE C`；400 行要求填 `C＿＿＿＿`；467 行要求確認 `正確的 C 類型`；execution-output 卻回報 `visible_bad_tokens=[]`。
- impact: 學員可能誤以為六種結構隸屬未提供的 C 模組，並把用途版型中的 C 社群版與六種結構混淆。
- severity: MAJOR
- confidence: HIGH
- proposed_check: 對 learner-content 做大小寫不敏感的語意掃描，涵蓋上述模式，再由無來源背景的冷讀者解釋每個代號。

## B-04

- claim: Learner Task Contract 所定義的第一個動作未出現在學員頁開場，實際學習路徑延後任務界定。
- evidence: Markdown 27–29 行指定先填目的、讀者、唯一重點、發布尺寸；HTML 138–153 行開場先準備工具與下載素材；第一個可填任務句到 HTML 395–408 行才出現。
- impact: 學員在大量看例子前沒有自己的任務基準，容易只模仿案例，且無法使用早期回復點。
- severity: MINOR
- confidence: HIGH
- proposed_check: 讓首次使用者只看開頭，3 分鐘內找出並完成四格與任務句。

findings_count: 4

unknowns:

- 15 分鐘內完成 Canva 中文排版、4:5、1:1、檢查及匯出的可行性。
- 圖片是否只抽象轉譯參考 PDF，沒有直接或衍生重用。
- 真人能否從下載素材完成兩張 PNG 與檢核。
- 響應式顯示、下載行為與實際瀏覽器操作。
