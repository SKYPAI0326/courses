# Deep Review 修復掃描

日期：2026-10-22
範圍：`uiux-designer` 現行凍結成果；不含其他課程。

## 可重現 findings

| finding | routing | root cause | current evidence | owner |
|---|---|---|---|---|
| 驗證狀態仍顯示 machine ready | full_course_integration | 2026-10-11 內容與素材變更已使舊 hash／PASS 失效，但 FINAL-REPORT、validation-result 與 gates 未以目前 evidence 重產一致狀態 | live validator exit 1、BLOCKED、valid 0；evidence 六層 PENDING | G5／validator |
| B6 總覽寫 T01–T07 | explanation_gap | 2026-10-11 已把正式來源改為 T01–T08，但 index 未同步 | `index.html` 對照 B6 source／檢查表 | G3 |
| 零基礎 B8 缺 VS Code 取得與成功判準 | practice_instruction_gap | 課前頁與 B8 直接使用 VS Code，只補 Git 安裝；工具入口鏈不完整 | COURSE-START、B8 source／HTML | G3 |
| 現行 HTML 無 fresh browser smoke | interface_block | 既有 browser evidence 綁舊 hash且缺 820px | Deep Review CA-03 | G4 |
| Figma 無可編輯 checkpoint | asset_missing | 課程設計要求個人同檔累積，沒有可安全生成／驗證的 `.fig` 基準檔 | `rg --files assets | rg '\.fig$'` 無結果 | G4，外部素材阻塞 |
| Photoshop／GitHub Pages／真人／現行 live hash | tool_behavior_mismatch / deployment_failure | 缺指定帳號、授權工作站、真人與發布授權 | Environment Contract、validator pending | G1/G6，外部阻塞 |

## 不採用的假修復

- 不把歷史 PASS 換 hash 後沿用。
- 不建立假的 `.fig`、Photoshop 或 GitHub 證據。
- 不因靜態 structure 56/56 通過就宣稱 browser、平台或真人通過。
- 不發布、不 push、不更動其他課程。
