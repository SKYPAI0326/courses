# 排版修正報告：ai-beginner-practical

## Scope

- 影響頁面：`index.html`、`module1.html`、`CH1-1.html`、`CH2-1.html`、`CH3-1.html`、`CH4-1.html`
- 主要修改：`assets/layout-redesign.css`
- 可見文字、表格內容、欄位 ID、工作台與收合互動流程均未改動。

## Changed

- lesson/module 內容欄改為較窄的編輯式欄位，增加章節上下留白。
- 正文與操作說明統一到既有字級階梯，中文正文維持約 15px 與寬鬆行距。
- 標題使用 `word-break: keep-all`；表格使用 CJK 按詞換行、英文長字串仍可安全斷行。
- 表格短標籤欄保持單行，資料列增加上下 padding，手機與平板在表格區域內水平捲動。
- 一般卡片、完成線與 callout 的粗色條降為 hairline，圓角收斂為 4px，保留暖紙色、墨色與藍灰主色。
- 768px／1024px 的寬表格納入局部捲動範圍，避免平板頁面級橫向溢出。

## Verification

- Restore script：`bash -n` 通過。
- Page lint：7 頁；`BLOCKER 0`、`ERROR 0`、`WARN 0`。
- `git diff --check`：通過。
- RWD 瀏覽器檢查：6 頁 × 320、360、390、414、768、1024、1440px，共 42 次載入；頁面級橫向溢出 `0`。
- 字體狀態：各尺寸檢查均為 `loaded`。
- 手機表格：維持區塊內 `overflow-x: auto`，未造成頁面級溢出。
- 本地連結檢查：6 頁、76 個相對連結、缺失 `0`。
- 六個正式 HTML 與本次修正前備份逐一比對，內容檔案未被修改。

## Restore

- Backup：`_backup/2026-09-21-pre-typography-layout/`
- Restore script：`_tools/restore-2026-09-21-pre-typography-layout.sh`
