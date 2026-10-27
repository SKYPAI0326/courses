# 課程 Skill 母群操作入口

本系統已涵蓋從需求釐清、外部研究、課程架構、教學正文、代表單元、全課製作、獨立試學到發布治理的 G0–G6 流程。完整角色、證據與命令請讀 [完整課程設計系統](complete-course-design-system.md)。

先明確設定四個彼此分離的 root。installer 與 `course_run.py` 使用下方 absolute script path 時，可從任意工作目錄執行；其餘相對路徑範例以 design-system root 為工作目錄：

```bash
export COURSE_DESIGN_SYSTEM_ROOT=/absolute/path/to/course-design-system
export COURSE_WEB_ROOT=/absolute/path/to/managed-courses
export SKILLS_ROOT=/absolute/path/to/skills
export COURSE_DESIGN_STATE_ROOT=/absolute/path/to/course-design-state
```

## 建立或恢復新課

```bash
python3 scripts/course_contract.py init \
  --root /absolute/path/to/course-root \
  --slug practical-ai \
  --title '實用生成式 AI' \
  --created-by course-run \
  --at '2026-10-18T12:00:00+08:00'

python3 scripts/course_contract.py status \
  --contract COURSE_ROOT/_design/practical-ai/course-contract.json
```

`course-run` 從第一個不是 `PASS` 的 Gate 繼續。Gate 依有效證據自動通過，不需要逐關請使用者核准。

contract 建立後、任何 Gate 工作開始前，由受治理操作者明確綁定外部 approval authority 的驗章公鑰：

```bash
python3 scripts/course_contract.py enroll-approval-authority \
  --contract COURSE_CONTRACT \
  --authority-id OPERATOR_GOVERNED_AUTHORITY \
  --public-key APPROVAL_PUBLIC_KEY_JSON \
  --expected-revision 0
```

這是一次性的 trust-root enrollment 治理步驟。`course-run` 與其他 course producer 不會自動產生、選擇、簽發或綁定 authority；production 只保存受治理公鑰並驗章。

## Gate 生命週期

```bash
python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/course_run.py" resume \
  --contract COURSE_CONTRACT \
  --actor course-run --at ISO8601

python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/course_run.py" complete \
  --contract COURSE_CONTRACT --gate G0 \
  --evidence-id g0-requirements \
  --actor course-run --at ISO8601

python3 scripts/course_contract.py block \
  --contract COURSE_CONTRACT --gate G1 \
  --reason '缺少必要平台存取權' \
  --actor course-run --at ISO8601
```

狀態只有 `NOT_STARTED`、`IN_PROGRESS`、`PASS`、`FAIL`、`BLOCKED`、`STALE`。`STATIC_VALIDATED`、`EXECUTION_VALIDATED`、`INDEPENDENT_AI_VERIFIED`、`HUMAN_VERIFIED` 是證據成熟度，不是 Gate 狀態。

## 語意變更

```bash
python3 scripts/course_contract.py change \
  --contract COURSE_CONTRACT --gate G2 \
  --reason '單元依賴與最終成果改變' \
  --actor course-run --at ISO8601 --semantic
```

語意變更會讓最早受影響 Gate 回到 `IN_PROGRESS`，下游變成 `STALE`。純錯字或不改意義的排版調整省略 `--semantic`，但仍要執行對應回歸。

## 發布授權

G6 `PASS` 只代表 `READY_TO_PUBLISH`。發布前先建立 exact-target proposal，再把 manifest hash 登錄為 external action：

```bash
python3 scripts/course_release.py propose \
  --root COURSE_ROOT --record RELEASE_RECORD \
  --output RELEASE_PROPOSAL

python3 scripts/course_contract.py propose-action \
  --contract COURSE_CONTRACT \
  --action-id ACTION_ID --kind course-release \
  --manifest-path RELEASE_PROPOSAL \
  --manifest-sha256 SHA256 \
  --actor course-ops --at ISO8601
```

使用者在外部受治理互動邊界核准同一份 manifest 後，以簽章 receipt 授權，再執行 release apply：

```bash
python3 scripts/course_contract.py authorize-action \
  --contract COURSE_CONTRACT --action-id ACTION_ID \
  --receipt SIGNED_APPROVAL_RECEIPT_JSON --at ISO8601

python3 scripts/course_release.py apply \
  --proposal RELEASE_PROPOSAL --contract COURSE_CONTRACT
```

套用前會重驗來源、目標與授權雜湊；開始套用即消耗該次授權。

## 本機 Skill 安裝與回復

```bash
python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/install_course_skill_foundation.py" \
  --verify-source

python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/install_course_skill_foundation.py" \
  --dry-run --skills-root "$SKILLS_ROOT"

python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/install_course_skill_foundation.py" \
  --apply --skills-root "$SKILLS_ROOT" \
  --allow-update course-run \
  --allow-update course-validator

python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/install_course_skill_foundation.py" \
  --verify-installed --skills-root "$SKILLS_ROOT"

python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/course_run.py" doctor

# 若 apply 被中斷，先以 operation path 回復，再重跑相同授權的 apply。
python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/install_course_skill_foundation.py" \
  --recover-operation "$COURSE_DESIGN_STATE_ROOT/operations/course-skill-foundation/OPERATION_ID"
```

安裝器以 package manifest 判斷 `ADD`、`UPDATE`、`UNCHANGED`，更新前建立備份。Recovery 與 rollback 會以呼叫端提供的 package root、skills root、operations root 和透過 no-follow directory handle 建立的唯讀 authority receipt，核對 operation identity、package set、target、hash 與精確暫存路徑；任何不相符都停止，不覆蓋使用者變更或觸碰非授權目標。

安裝 operations、catalog、report 與 backup 預設寫在 repo 外的 `COURSE_DESIGN_STATE_ROOT`。doctor 在 POSIX macOS/Linux 回報各 root 與依賴的 `READY`／`BLOCKED`；Windows lock 尚未支援，會 fail closed。

## 既有課程

既有課程使用 `course-repair`，不補造新課 Gate 歷史。修復維持 `scan → plan → backup → fix → verify`；若重新定義學員、核心成果或整門課架構，改開新的 G0 contract。

```bash
python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/course_run.py" repair-fix \
  --course-root COURSE_ROOT --proof REPAIR_PROOF

python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/course_run.py" repair-recover \
  --course-root COURSE_ROOT --operation OPERATION_DIR
```

`repair-fix` 在第一次寫入前重驗 approved plan hash、所有 target before hash、完整 backup 與 isolated restore proof；中斷時依 durable journal 回復。任何證據缺失、hash 漂移或路徑越界都會 fail closed。

## 獨立系統匯出

```bash
python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/export_standalone.py" \
  --destination /absolute/path/to/course-design-system
```

輸出是只含設計系統的獨立 Git repo，排除 learner-facing courses 與 runtime 個人資料。clone 後先執行 `--verify-source`，再設定四個 root 並安裝 Skill。
