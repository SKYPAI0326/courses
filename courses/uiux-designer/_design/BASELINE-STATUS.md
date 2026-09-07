# UI/UX 課程基線狀態

日期：2026-09-07  
對應設計規格：`uiux-designer/_design/2026-09-07-99h-course-rescope-design.md`  
判定：`REBUILD_FROM_NEW_BASELINE`

## 盤點範圍

本次依計畫檢查：

- 工作樹中的 `uiux-designer/`
- 專案 `_outlines/`
- 專案 `_lessons/`
- `courses/uiux-designer/`
- Git 全部可見 refs 的相關路徑與歷史

正式授課來源仍是使用者提供的兩張圖片：

- `/Users/paichenwei/Downloads/1788509783989.jpg`：介面元素與設計，42h
- `/Users/paichenwei/Downloads/1788509797593.jpg`：UI/UX 原型製作與資料打包，57h

## 目前找到的檔案

### 可作為新設計控制面的檔案

- `uiux-designer/_design/2026-09-07-99h-course-rescope-design.md`
- `docs/superpowers/plans/2026-09-07-uiux-99h-rescope.md`

### 殘留的試跑材料

- `uiux-designer/_review/CH1-1-ZERO-BEGINNER-TRIAL.md`
- `uiux-designer/assets/CH1-1/CH1-1-layer-structure-reference.pdf`
- `uiux-designer/assets/CH1-1/CH1-1-structure-checklist.pdf`

這些檔案只能作為歷史試跑材料候選，不足以代表完整正式課程基線，也不能單獨放行新課程。

## 未找到的基線

目前沒有在工作樹或可見 Git history 找到：

- `_outlines/uiux-designer.md`
- `_lessons/uiux-designer/` 正式教案集合
- `courses/uiux-designer/` 正式 HTML 講義與 index
- `uiux-designer/_gates.md`
- 舊版完整來源索引與正式課程狀態檔

因此無法安全執行「在既有課程上局部修正」。不應把殘留的 CH1-1 試跑材料、過往對話摘要或舊記憶當成可直接恢復的完整課程。

## 舊 Photoshop 42h 判定

「Photoshop 42h＋UI/UX 57h」只保留為先前設計脈絡。它不列入新 99h coverage matrix 的正式來源，也不控制新課程的 Part、時數或 Gate。

新基線只承認：

1. 42h「介面元素與設計」：色彩、字型、格線、Auto Layout、Component、Button、Form、List、Toast、Dialog、Navigation、Variants。
2. 57h「UI/UX 原型製作與資料打包」：線框／原型／工具介紹／手機介面／元件與動畫互動、互動與轉場、Overlay／Swap、滾動／置頂／漂浮、Smart Animation、Figma／PS 發布與輸出、網頁入門、雲端部署。

## 執行判定

- 基線類型：`重建`，不是 `局部修正`。
- 下一步：執行 Gate 0，建立 42h／57h 正式 coverage matrix。
- 暫停項目：時間分配、正式 outline、教案、HTML、部署。
- 風險：若未把兩張圖片保存為專案來源副本，後續只能依 Downloads 路徑與人工記錄追溯；建立 coverage matrix 時必須保留來源路徑與逐項摘錄。

## 盤點證據

執行過的唯讀命令：

```bash
rg --files .. | rg -i 'uiux|photoshop|prototype|interface|outline|lesson|gate'
git log --all --name-status -- uiux-designer _outlines _lessons courses/uiux-designer
```

結果未顯示舊 `uiux-designer` 正式課程檔案或相關歷史 commit；目前唯一可辨識的新課程控制檔案是本次 2026-09-07 設計規格與執行計畫。
