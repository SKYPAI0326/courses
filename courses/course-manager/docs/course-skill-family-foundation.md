# 課程 Skill 母群操作入口

本系統已涵蓋從需求釐清、外部研究、課程架構、教學正文、代表單元、全課製作、獨立試學到發布治理的 G0–G6 流程。完整角色、證據與命令請讀 [完整課程設計系統](complete-course-design-system.md)。

以下命令都從 `courses/course-manager` 執行。

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

## Gate 生命週期

```bash
python3 scripts/course_contract.py begin \
  --contract COURSE_CONTRACT --gate G0 \
  --actor course-run --at ISO8601

python3 scripts/course_contract.py pass \
  --contract COURSE_CONTRACT --gate G0 \
  --evidence-id g0-requirements \
  --validator-id requirements-validator \
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

使用者核准同一份 manifest 後，再執行 `authorize-action` 與：

```bash
python3 scripts/course_release.py apply \
  --proposal RELEASE_PROPOSAL --contract COURSE_CONTRACT
```

套用前會重驗來源、目標與授權雜湊；開始套用即消耗該次授權。

## 本機 Skill 安裝與回復

```bash
python3 scripts/install_course_skill_foundation.py \
  --dry-run --skills-root /Users/paichenwei/.agents/skills

python3 scripts/install_course_skill_foundation.py \
  --apply --allow-update \
  --skills-root /Users/paichenwei/.agents/skills
```

安裝器以 package manifest 判斷 `ADD`、`UPDATE`、`UNCHANGED`，更新前建立備份。rollback 會先確認已安裝內容沒有被後續修改；不相符就停止，不覆蓋使用者變更。

## 既有課程

既有課程使用 `course-repair`，不補造新課 Gate 歷史。修復維持 `scan → plan → backup → fix → verify`；若重新定義學員、核心成果或整門課架構，改開新的 G0 contract。
