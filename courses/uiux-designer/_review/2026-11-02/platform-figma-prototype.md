# Part B 平台現況核對（Figma 原型、交付、Photoshop）

核對：fresh-context 子代理，2026-11-02，唯讀。範圍：part2 CH1～CH7、B1～B7 素材頁、shared PHOTOSHOP／PSD 說明。Adobe helpx 擋抓取，Photoshop 部分只靠搜尋摘要。

## 需修改

| 頁 | 講義原句 | 現況 | 來源 | 嚴重度 |
|---|---|---|---|---|
| B1、B2、B5、B6 | Present／播放預覽混用 | **Preview** 在編輯器內播放（⇧Space）；**Present** 另開分頁。選 flow：Preview 點起點標籤旁藍色圖示或 Prototype 分頁 Flows 清單；Present 在左側欄選 | help.figma.com/hc/en-us/articles/360040318013、/360039823894 | 誤導 |
| B1 | 入口出現在頂端播放圖示旁 | 起點標籤在畫布上該 Frame 旁 | /360039823894 | 輕微 |
| B2 | Trigger 為 On click | 官方名「On click / On tap」，手機裝置可能顯示 On tap | /360040315773 | 輕微 |
| B3、B5 | 給 Before 單獨的 Flow 起點 | 連接兩個未連線 Frame 時 Figma 自動建立「Flow N」，應寫「改名」 | /360039823894 | 誤導 |
| B4 | 用 Manual 設在畫面內 x98、y96 | Manual 是相對觸發物件的偏移，不是畫面座標 | developers.figma.com/docs/plugins/api/Overlay | 阻斷 |
| B5 | 名稱可能顯示 Vertical scrolling | Prototype › Scroll behavior › **Overflow**：No scrolling／Horizontal／Vertical／Both directions | /360039818734 | 輕微 |
| B5 | On click → Scroll to → List 內第一個 Row | 下拉只能選可捲動 Frame 的直接子層；深層物件要拖曳連線，且目標不能被 Clip 裁掉 | /360040035874 | 阻斷 |
| B5 | 設 Fixed（未提圖層變化） | Fixed 物件移到圖層上方，Layers 出現「Fixed」標示 | /360039818734 | 輕微 |
| B6 | 確認 Prototype view 權限 | Starter 沒有原型分享與連結存取控制，只能分享整份檔 can view | /360040328273 | 誤導 |
| B7 | 檔案選單 Save local copy | Main menu › File › Save local copy；.fig 不含留言與版本歷史 | /8403626871063 | 誤導 |
| B7 | Export frames to PDF | 官方文件查不到，論壇說在 Main menu › File | forum.figma.com | 無法確證 |
| B7 | Create new › Import | 還要點「Import from computer」 | /360041003114 | 輕微 |
| B7 | 切換至 Design 面板量距 | 只有檢視權限時右側是 Properties 分頁 | /22012921621015 | 輕微 |
| B7 | Photoshop Export As「PNG、Transparency、W512 H512」 | Photoshop 27 起是新版 Export As，舊版要在 Preferences › Export 勾 Use legacy；新版欄位名無法確證 | helpx（擋抓取）、community.adobe.com | 誤導，需實機 |

## Starter 原型與交付限制

基本原型可用；無變數、條件、多動作、變數模式；無原型分享控制、連結存取控制、密碼保護；無 Dev Mode、Team library；版本歷史 30 天；草稿只能邀請 can view。

## 待實機確認

Move in 方向箭頭呈現；On click／On tap 顯示；Destination 能否選 None；Overlay 位置選項名稱；Manual 偏移的設定畫面；圖層名含「/」匯出的檔名；File 選單有無 Export frames to PDF；Starter 已滿 3 檔時 Duplicate／匯入 .fig 落在哪；Photoshop 27 Export As 欄位；Save As 的 Layers 勾選。
