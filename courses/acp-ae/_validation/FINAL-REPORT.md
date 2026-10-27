# ACP-AE 網頁版講義驗收報告

驗收日期：2026-10-16

## 結論

網頁版講義已完成並通過機器與瀏覽器層驗證。成品包含 14 個 HTML、10 份正式學員正文、40 張操作題路徑卡、13 題概念題與 9 題代表實作。讀題方法與完成檢查直接放在使用它們的課程頁內。

零基礎文案修復已完成：10 課都有清楚的 Step by Step 操作；核心操作會交代要做什麼、應看到什麼，以及畫面不符時回到哪裡。題數、時數、技術數值與原有課程邊界均未改變。

目前狀態為 `MACHINE_CHECKED` + `BROWSER_CHECKED`。由於驗證電腦未安裝 After Effects，`PLATFORM_VERIFIED` 保持 `BLOCKED`；真人跟做尚未執行，`HUMAN_READY` 保持 `PENDING`。

## 自動檢查

```text
python3 _tools/validate-handout.py
PASS — 10 lessons, 14 HTML files, 40 operation cards,
       13 concept questions, 9 representative practices

python3 docs/lint-page.py courses/acp-ae/
PASS — BLOCKER 0, ERROR 0, WARN 0

validate-course-structure.py [10 lesson HTML files]
PASS — checked 10, blocked 0

audit_copy_continuity.py [10 lesson HTML files]
PASS — 每頁 0 warning；語意審查仍需人工

python3 docs/audit-course-substance.py acp-ae
PASS — pages 10, block 0；semantic review 保持 PENDING

python3 docs/build-search-index.py
PASS — 根目錄 search-index.json 含本課 14 個頁面
```

## 瀏覽器驗證

- 首頁：1440 × 1000，搜尋 `Matte` 正確回報 1 個單元並隱藏另外兩張卡。
- CH1-5：390 × 844 手機版含 11 個逐步操作區塊，頁面無水平溢位。
- CH2-1：430 × 932 手機版含 13 題與四步判斷法，頁面無水平溢位。
- CH3-3：390 × 844 與 1440 × 900 均可讀，含六步讀題法、13 張題卡、3 題代表實作，console 無 error／warning。
- 瀏覽器測試曾抓到首頁搜尋卡片未實際隱藏，已在共用 CSS 補上 `[hidden]{display:none!important}` 並以新分頁重測通過。

## 交付入口

- 課程首頁：`index.html`
- Part 1：`module1.html`
- Part 2：`module2.html`
- Part 3：`module3.html`
- 本輪修復報告：`_repair/2026-10-16-beginner-step-by-step/REPAIR-REPORT.md`

## 上線前剩餘工作

1. 在授課機的 After Effects v25.x 依 10 課完整重做並留下實際輸出證據。
2. 修正因版本或語系造成的介面名稱差異。
3. 由目標學員執行 cold follow-along，確認不需口頭補充即可完成。
4. 通過後再執行課程註冊、密碼關卡與部署流程。
