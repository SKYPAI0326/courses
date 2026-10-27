# Course Design System

這是課程設計與產製的控制系統，負責從需求確認、外部研究、課程藍圖、教學內容、學員網頁、獨立試學到發布準備的 G0–G6 流程。

本儲存庫保存系統程式、Skill、契約、驗證與示範證據；不作為 learner-facing 課程的上架位置。正式課程與公開網頁仍由 [`SKYPAI0326/courses`](https://github.com/SKYPAI0326/courses) 管理。

## 目前狀態

- 系統版本為 `0.1.0`，需要 Python 3.11 以上；支援 macOS 與 Linux。
- G0–G6 端到端流程已完成。
- 16 個課程 Skill 已通過套件與安裝雜湊驗證。
- 代表單元與完整課程已由不同的獨立 AI 情境完成試學。
- 證據成熟度為 `INDEPENDENT_AI_VERIFIED`；尚未宣稱 `HUMAN_READY`。
- G6 `PASS` 代表 `READY_TO_PUBLISH`，不代表已對外發布。

詳細結果見 [`docs/verification/2026-10-18-course-design-system-verification.md`](docs/verification/2026-10-18-course-design-system-verification.md)。

## 使用入口

建立新課程時，要求 Codex 使用 `course-run`，並提供目前已知的學員、情境、成果、時間、授課方式與工具限制。未知項目可保留，G0 只會追問會改變設計的條件。

```text
請使用 course-run 建立一門新課程。

主題：生成式 AI 行銷內容製作
學員：沒有 AI 經驗的行銷企劃
情境：需要獨立完成可發布的社群內容
最終成果：一份貼文、圖片與檢查紀錄
時間：6 小時
形式：完整網頁講義，學員可獨立閱讀、操作並完成成果
```

系統會依證據自動推進 G0–G6。遇到會改變課程成果的未知、重大設計分歧、付費、帳號或權利需求，以及發布等外部變更時才會暫停詢問。

既有課程的診斷與修復使用 `course-repair`，依 `scan → plan → backup → fix → verify` 執行，不會假裝既有課程已走過完整的新課 Gate。

完整操作方式見 [`docs/complete-course-design-system.md`](docs/complete-course-design-system.md)。

## 驗證

```bash
python3 -m unittest discover -s tests -v
python3 scripts/install_course_skill_foundation.py --verify-source
python3 scripts/course_run.py doctor
```

`--verify-source` 驗證 clone 內的 16 個 Skill 來源；`--verify-installed` 驗證指定 Skill 目錄的安裝結果；`doctor` 只讀檢查四個 runtime root 與平台鎖。CI 會在 Linux/Python 3.11、Linux/Python 3.12 與 macOS/Python 3.12 執行全套測試、編譯、JSON／shell 檢查、portable path 掃描、clean HOME 安裝、proof replay 與獨立 repo clean clone。Windows 的交易鎖尚未支援，會 fail closed。

安裝前可先預覽差異：

```bash
export COURSE_DESIGN_SYSTEM_ROOT="/absolute/path/to/course-design-system"
export COURSE_WEB_ROOT="/absolute/path/to/managed-course-root"
export SKILLS_ROOT="/absolute/path/to/agent-skills"
export COURSE_DESIGN_STATE_ROOT="/absolute/path/to/course-design-state"

python3 scripts/install_course_skill_foundation.py \
  --dry-run \
  --skills-root "$SKILLS_ROOT"

python3 scripts/install_course_skill_foundation.py \
  --apply \
  --skills-root "$SKILLS_ROOT" \
  --allow-update course-run \
  --allow-update course-validator

python3 scripts/install_course_skill_foundation.py \
  --verify-installed \
  --skills-root "$SKILLS_ROOT"

python3 scripts/install_course_skill_foundation.py \
  --recover-operation "$COURSE_DESIGN_STATE_ROOT/operations/course-skill-foundation/OPERATION_ID"
```

套件更新必須以 `--allow-update PACKAGE_NAME` 逐項授權；安裝程式會先備份並建立 rollback 紀錄。Recovery 與 rollback 會重新核對呼叫端提供的 package root、skills root、operations root，以及 operations root 下以 no-follow directory handle 建立的唯讀 authority receipt。暫存路徑由 receipt 內的 operation/package identity 精確綁定；operation manifest 的 target、hash、container 或 recovery container 若被改寫就 fail closed。

## 專案結構

- `skill-packages/`：16 個可安裝的課程 Skill。
- `contracts/`：課程契約與各 Gate 的 JSON Schema。
- `src/`、`scripts/`：Gate、研究、內容、驗證與發行控制程式。
- `proofs/`：端到端示範課與獨立試學證據。
- `docs/`：完整設計、操作手冊與驗證報告。
- `COURSE_DESIGN_STATE_ROOT/operations/`：repo 外的安裝備份、manifest 與 rollback 證據。runtime operations、掃描報告與 registry 快照不提交進原始碼。

`manager.py` 是原有的課程資料夾盤點與安全搬移工具，保留為附屬管理能力；它不是 G0–G6 新課程產製入口。

`python3 scripts/course_run.py doctor` 只讀檢查四個 runtime root、必要依賴與平台 lock。支援 macOS／Linux；Windows 交易鎖尚未支援並會 fail closed。

## 獨立儲存庫匯出

目前來源仍可位於既有工作樹的 `course-manager` 子目錄；正式建立獨立 repo 前，先輸出可稽核的 Git 邊界：

```bash
python3 scripts/export_standalone.py \
  --destination /absolute/path/to/course-design-system
```

輸出只包含課程設計系統，不包含 learner-facing `courses`、operations、reports 或個人 registry 快照；程式會建立 Git commit 與逐檔 SHA-256 `EXPORT-MANIFEST.json`。clone 該輸出後執行 `--verify-source`，可重現相同的 16 套 Skill。
