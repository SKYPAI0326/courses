---
name: course-html-contract
description: Use when editing, generating, repairing, reviewing, or validating learner-facing course HTML where content must remain inside its existing layout wrappers.
---

# 課程講義 HTML 編輯保護契約

這是所有課程 HTML 產製、文案修補、排版修補、課程修復、運維注入與驗收角色共用的安全邊界。先判斷任務範圍，再決定能不能改文字、能不能改 DOM；沒有明確範圍時停止，不用猜測補內容。

## 1. 先分類任務

每次動 HTML 前，先在工作紀錄寫出一個 `task_scope`：

- `syntax-only`：只修 HTML、CSS、JS、編碼或語法錯誤；不得改可見學習文字、課程順序或教學事實。
- `layout-only`：只修寬度、間距、排版、RWD、導覽位置或 CSS；不得改可見學習文字、課程順序或教學事實。
- `content-change`：新增、刪除或改寫學習內容。只有使用者明確要求或已核准的修復計畫可以使用，並先列出目標檔案、新增／修改文字、原因、對既有版面與導覽的影響。

使用者說「不變更文字內容」時，只能用 `syntax-only` 或 `layout-only`。排版或語法問題不能被解讀成內容缺口；缺內容要回交內容責任角色。

## 2. DOM 容器不變式

既有頁面維持原有內容根節點與父子關係；目前採 `.lesson-body` 的頁面必須繼續把主要課程內容放在該容器內：

```html
<section class="lesson-hero">...</section>
<div class="lesson-body">
  <div class="lesson-section">...</div>
</div>
```

- `.lesson-section`、`.body-text`、`.step-list`、`.prac-box` 等內容節點必須是 `.lesson-body` 的後代。
- 不得把內容節點放在 `.lesson-body` 外，不得在 `.lesson-hero` 與 `.lesson-body` 之間插入新段落。
- 不得改既有 wrapper 的層級、順序或寬度責任；不得為了插入內容新增全寬度外層容器。
- 除非任務明確是 `content-change` 且計畫列出影響，不得更換既有 HTML 標籤或 class 名稱。
- `.lesson-nav`、footer、gate、script 等頁面殼層不能被內容插入點截斷。
- 新課可依已驗證的 course visual decision 設計自己的內容根節點與 class，不必複製 `.lesson-body`。但必須有唯一 `<main id="main">`、可定位的 learner-content 根節點、正確 landmark、完整導覽與可供驗證器設定的 root selector；不得為了通過舊檢查器臨時新增無語意 wrapper。
- index/module 等非講義頁可以使用自己的既有 wrapper；既有頁只有出現上述講義內容 class 時才套用 `.lesson-body` 規則。

## 3. 只能用有上下文的 DOM 編輯

修改前先保存原檔、建立內容／結構快照，並以 HTML parser 找到明確的目標節點與父鏈：

```python
body = soup.select_one('.lesson-body')
target = body.select_one('[data-section="target"]')
assert target is not None and target.find_parent(class_='lesson-body') is body
```

禁止：

- 找到第一個 `</div>`、第一個 `.lesson-section` 或第一個相同字串後直接插入。
- 用全域正規表示式取代所有相同字串。
- 假設檔案中第一個 class、第一個表格或第一個 `</section>` 就是目標。
- 以字串拼接取代 DOM 上下文，導致內容跑到 `.lesson-body` 外或 wrapper 提前結束。

新節點只能插入明確指定的 `.lesson-body` 子樹；若只是改文案，維持原文字節點的標籤、class、連結與父節點。

## 4. 變更後必做的驗收

1. `syntax-only`／`layout-only`：比較可見文字快照；若文字、href、課程順序或教學區塊數量改變，停止並回復。
   可直接執行 `python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/check_content_unchanged.py BEFORE.html AFTER.html`；非內容任務必須得到 `content unchanged`。
2. 所有範圍：以 parser 檢查未配對標籤、visual decision 指定的內容根節點、main／nav／footer 順序與目標節點父鏈；既有 `.lesson-body` 頁另外檢查其後代關係。
3. 執行 `python3 docs/lint-page.py <file.html> --summary`，再對受影響頁跑 `python3 docs/audit-course-substance.py <slug> --page <file.html>`。
4. 檢查 `git diff --check` 與目標檔的 diff；看見 wrapper 大段移動、內容漂移、全域取代或非預期文字變更時，先停止，不以 lint 通過掩蓋。
5. 任一檢查失敗：使用備份還原、標記 `BLOCK`，不要繼續堆疊修補。

既有 `.lesson-body` 頁面使用共用檢查器：

```bash
python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/validate_html_structure.py <file.html>
```

## 5. 角色邊界

- `course-typography-fixer`、`course-ops`、`course-register` 預設只能 `syntax-only`／`layout-only`；需要內容變更就交回內容角色。
- `course-copywriter` 的 `content-change` 只允許改文字節點，不可改 wrapper、class、href 或操作行為。
- `build-course-page` 可依已通過 G3 的正文與 G4 visual decision 建立新頁；修改既有頁時保留原 wrapper。兩種情況都不能臨場補寫缺失事實。
- `course-repair` 只有在 fix 計畫明列時才能做 `content-change`；單純排版修補不得新增段落、任務或 `(00)`。
- `course-reviewer`／`course-validator` 不改頁面；看到內容節點在 wrapper 外、wrapper 斷裂或任務範圍不符時，列為 Issue／BLOCK。

## 6. 排版任務的文字保護

`syntax-only` 或 `layout-only` 不得自行新增 `(00)`、任務區塊、教學段落、提示、範例或學習成果；不得改寫原文、調整課程順序，也不得把「缺少內容」解讀成可以自動補寫。若確實需要 `content-change`，先建立「允許變更文字清單」，列出：

1. 目標檔案。
2. 準備新增或修改的完整文字。
3. 每一項變更的原因。
4. 對既有版面與導覽的影響。

沒有這份清單時，內容差異就是 `BLOCK`。語法或排版修正允許調整 tag、class、CSS 與空白格式，但可見中文、英文、數字、提示文字、連結文字、href、課程順序與學習區塊數量必須完全一致。

## 7. 插入前的四項確認

每次插入前，先記錄並確認：

1. 目標 `.lesson-body` 的開始與結束位置。
2. 目標頁是否已存在相同區塊。
3. 新內容是否確實應位於該 `.lesson-body` 內。
4. 修改是否會產生重複 `id` 或重複內容。

優先使用 DOM/parser；若只能文字處理，先確認完整容器範圍，再做局部修改。不可用第一個 `</div>`、第一個 `.lesson-section`、第一個 class 或全域正規表示式決定插入點。

完整 shell、正確／錯誤插入例、桌面與手機檢查表放在 `references/layout-contract.md`。

## 8. 結構、CSS 與祖先關係驗證

每個被修改的 HTML 都要執行：

```bash
python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py FILE.html
```

批次掃描可使用：

```bash
python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py --batch office-ai
```

`office-ai` 固定回歸頁可使用：

```bash
python3 /Users/paichenwei/.agents/skills/course-html-contract/scripts/validate-course-structure.py --office-ai-regression office-ai
```

既有頁檢查器至少阻擋：`.lesson-body` 缺失或數量不符合預期、每個 `.lesson-section` 不在 `.lesson-body` 內、第一個 `.lesson-section` 在 body 之前、重複 `id`、未關閉或錯置 HTML 標籤、`.lesson-nav` 順序錯誤，以及 CSS media query 的括號不完整。新課依 visual decision 提供 root selector，驗證唯一 main、learner-content ancestor、導覽順序、重複 id 與標籤配對。解析成功本身不足以通過驗收；內容寬度與水平捲軸仍要靠瀏覽器 smoke test 確認。

最低斷言是：

```text
lesson_body_exists
lesson_body_count == expected_count
every_lesson_section_has_lesson_body_ancestor
first_lesson_section_is_inside_lesson_body
no_duplicate_ids
visible_text_is_unchanged_when_scope_is_layout_or_syntax_only
```

若是 `layout-only`，使用 `--before` 或 `check_content_unchanged.py` 比較修改前後的可見文字與 href；結果不是 `content unchanged` 就停止，不得提交。

## 9. RWD、sticky header 與瀏覽器驗證

靜態 lint 通過後，仍要對代表頁執行 browser smoke test。桌面檢查 `1440px`（頂端、修改區塊、中段、底部），平板檢查 `820px`，行動檢查 `390px`。確認內容寬度符合本課 visual decision、沒有非預期水平捲軸、裁切或異常斷行，卡片／表格／程式碼區塊沒有超出容器，導覽仍可用，且 sticky header 沒遮住標題。

若有 `localStorage` scroll state，先清除舊 state，再測試首次從頂端進入、重新整理與從中段直接載入；不能用保留上次捲動位置掩蓋錯誤。錨點跳轉必須保留 header 高度，優先使用 `scroll-margin-top` 或 `scroll-padding-top`；未確認跨頁影響前不得用負 margin 或任意 top offset。

沒有瀏覽器證據時只能標記 `PENDING`／`BLOCK`，不可宣告完成。

## 10. 標準修正流程與報告

所有課程頁面修正依序執行：

```text
scan → classify scope → backup → inspect target container →
plan insertion point → apply minimal change → structural validation →
visible-text diff → HTML/CSS lint → browser smoke test → report → commit/push
```

報告必須包含：修改檔案清單、實際修改的 HTML/CSS/JS 範圍、是否變更可見文字、結構檢查結果、RWD 檢查尺寸、尚未驗證項目，以及是否允許 commit/push。`commit/push` 不是 lint 的推論，必須有明確授權與完整報告。

## 11. 停止條件與回復

出現以下任一情況立即停止提交：`.lesson-section` 在 `.lesson-body` 外、未授權的可見文字差異、內容變成滿版、桌面或手機水平捲軸、sticky header 遮住標題／正文、瀏覽器畫面異常、無法判斷插入位置、重複內容／id 或導覽錯誤。流程失敗時回復該次修改或使用備份，標記 `BLOCK`；不能用「lint 已通過」取代畫面驗證。

## 12. office-ai 回歸測試

以下頁面固定納入回歸測試：

```text
office-ai/ch1/CH1-1.html
office-ai/ch1/CH1-2.html
office-ai/ch6/CH6-2.html
office-ai/ch6/CH6-3.html
```

每頁須確認 `lesson_section_count >= 1`、每個 `.lesson-section` 都有 `.lesson-body` ancestor、layout-only 的可見文字不變，且內容寬度與鄰近 section 一致。任一項失敗都維持 `BLOCK`，另行建立最小範圍修復，不在排版任務中補寫課程內容。
