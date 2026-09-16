# UI/UX 課程跨平台驗證矩陣（Pass 1）

| 能力 | Chrome／Figma Starter | 本地 HTML 講義 | Photoshop | Git／部署 |
|---|---|---|---|---|
| Frame、圖層、命名 | `MACHINE_PASS`（Probe A/B） | 有尺寸與層級步驟 | `NOT_RUN` | 可由本地檔案審計 |
| On click → Open overlay | `MACHINE_PASS`（Probe B 預覽顯示確認完成） | 有 8 步與 Checkpoint | `NOT_RUN` | 證據檔已納入版本控管 |
| 一檔一核心 action 邊界 | `CONDITIONAL`（Starter 第二 action 顯示升級） | 有拆檔備援 | `NOT_RUN` | 未 push |
| PNG／PDF 匯出 | `MACHINE_PASS`（Probe C，尺寸已驗證） | 有完成品對照圖 | `NOT_RUN` | 匯出包在 evidence/exports |
| CSS Inspect／Dev Mode | `MACHINE_PASS`（Probe C） | 有交付說明 | `NOT_RUN` | 未建立自動部署 |
| Photoshop 開啟、色彩與修復 | `NOT_RUN` | 已明確標註後續範圍 | `BLOCKED_PENDING_TEST` | 不應宣稱通過 |
| 公開分享與 GitHub Pages | `CONDITIONAL`（未執行） | 本機網站與 local Git 已驗證 | `NOT_RUN` | `CONDITIONAL`，等待 release gate |

## 解讀

本矩陣是課程設計的邊界，不是完整產品驗收。Figma／Chrome 的單一 Overlay 路徑已具機器證據；Photoshop、真人跟做、外部分享與公開部署仍是後續 Gate。
