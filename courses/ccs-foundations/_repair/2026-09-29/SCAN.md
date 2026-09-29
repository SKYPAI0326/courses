# CCS Foundations 導覽切換 Scan

- 日期：2026-09-29
- 範圍：課程首頁、CH4 舊頁下一步導覽、舊 CH5-1 至 CH5-4 HTML 與 Markdown、9 個新版 v2 單元連結。
- 使用者決策：新版 9 小時課程成為首頁主線；舊 CH5 資料另行封存。

## 發現

1. `index.html` 仍列舊版 13 單元、模擬測驗、範本庫與 CH5 延伸篇；舊核心單元連至非 v2 HTML。首頁時數與單元數不符合新版大綱。
2. 舊 CH5-1 至 CH5-4 HTML 由首頁連入，CH4.html 的下一單元也指向 CH5-1.html；這組頁面須一併封存，並改掉仍在根目錄保留的 CH4 前進連結。
3. `_lessons/ccs-foundations/CH5-1.md` 至 `CH5-4.md` 與新版大綱不一致，且不屬今日 9 單元主線；封存副本保留原始內容。
4. 新版主線為 CH1-1、CH1-2、CH1-3、CH1-4、PRAC1、CH2-1 至 CH2-4；合計 6 小時核心內容與 3 小時 Q1–Q80 題庫講解。
5. 9 個新版頁面的內部順序導覽已互連。全課 RWD、初學者冷讀、真實平台操作仍待驗；本次不發布、不提交、不重建全站搜尋索引或 sitemap。

## Activity Identity Audit

本次為導覽與檔案歸位修復，不變更課堂活動、學員產物或提示詞內容。9 個新版單元仍按大綱及其既有教案執行；本次不重新設計 Demo / Together / Solo。

## Shared Copy Audit

本次不改寫單元正文。首頁摘要與單元卡片會按新版課程定位重整；新版頁面提示詞、警語及示例正文均不改。

## 保留範圍

- CH0、舊 CH1-1 至 CH1-5、CH2-1 至 CH2-4、CH3、CH4 其餘舊內容不刪除。
- 其中 CH4.html 僅調整下一單元連結，使封存 CH5 後不留下失效路徑。
- 目前沒有官方題庫答案鍵；首頁與課程正文應沿用「題庫預期答案」措辭。

## 追加盤點：舊版 CH1-1 HTML

- 使用者同意將仍保留的 `CH1-1.html` 納入修復，範圍限定為 HTML 結構，不改可見文字、連結或教學內容。
- 修復前課程結構批次掃描在此頁回報 `misnested closing tag </span> before <div>`，並連鎖出現未配對 `</div>`；位置集中於兩組 `.compare-grid` 的 16 個比較項目。
- 根因：`<span><div class="compare-dot"></span></div>` 的巢狀與關閉順序相反。依同課程其他頁面使用的結構，改為 `<span class="compare-dot" aria-hidden="true"></span>`。
- 修復後整個課程目錄結構檢查為 `checked=22 blocked=0`；文字與 href 快照完全一致。舊頁 RWD 尚待瀏覽器驗收。
