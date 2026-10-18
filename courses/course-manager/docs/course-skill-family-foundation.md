# 課程 Skill 母群基礎操作手冊

本輪完成 G0–G2 的可運行垂直切片：課程契約、Gate 狀態機、外部研究驗證、母 Skill、研究 Skill、架構 Skill 與可回復安裝器。這份手冊記錄既有基礎操作；後續完整系統以 [完整課程設計系統設計](superpowers/specs/2026-10-18-complete-course-design-system-design.md) 為準。

以下命令都從 courses/course-manager 執行。

## 1. 建立契約

~~~bash
python3 scripts/course_contract.py init \
  --root /absolute/path/to/course-root \
  --slug fictional-sheets \
  --title '虛構試算表實作課' \
  --created-by '課程團隊' \
  --at '2026-10-18T12:00:00+08:00'
~~~

契約位置為 COURSE_ROOT/_design/fictional-sheets/course-contract.json。course-run 把完整 G0 問答寫入 G0_requirements；長篇訪談或附件留在外部檔案，以相對路徑與 SHA-256 登錄。

## 2. 驗證、送審與核准 G0

~~~bash
python3 scripts/course_contract.py validate --contract COURSE_CONTRACT
python3 scripts/course_contract.py status --contract COURSE_CONTRACT
python3 scripts/course_contract.py submit \
  --contract COURSE_CONTRACT --gate G0 \
  --actor course-run --at ISO8601
python3 scripts/course_contract.py approve \
  --contract COURSE_CONTRACT --gate G0 \
  --approved-by USER_NAME --at ISO8601 \
  --note '使用者對本次 G0 交付物的明確核准內容'
~~~

approve 只能在使用者看過交付物、證據、風險及未知後執行。

## 3. 驗證 G1 研究紀錄

course-researcher 依 contracts/course-research-record.schema.json 產出研究 JSON 與 adaptation JSON。下列命令列出所有問題；沒有輸出且 exit 0 才代表 readiness 通過。

~~~bash
python3 - RESEARCH_RECORD ADAPTATION_JSON <<'PY'
import json
import sys
from pathlib import Path
from src.course_research import validate_research_record

record = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
adaptation = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
issues = validate_research_record(record, adaptation)
for issue in issues:
    print(f"{issue.code} {issue.path}: {issue.message}")
raise SystemExit(1 if issues else 0)
PY
~~~

高工具依賴卻缺少實測、高變動卻缺複查日期或責任人、失敗實測及 blocking unknown 都會阻擋 readiness。來源數量不構成通過條件。

## 4. 將研究結果路由到 G1

route_research_to_gate 會在驗證通過時把 G1 送到 REVIEW；缺必要證據時寫入研究索引並把 G1 設為 BLOCKED。

~~~bash
python3 - COURSE_CONTRACT RESEARCH_RECORD ADAPTATION_JSON RECORD_PATH SHA256 ACTOR ISO8601 <<'PY'
import json
import sys
from pathlib import Path
from src.course_contract import load_contract, save_contract_atomic
from src.course_research import route_research_to_gate

contract_path = Path(sys.argv[1])
record = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
adaptation = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
contract = load_contract(contract_path)
status = route_research_to_gate(
    contract,
    record,
    adaptation,
    sys.argv[4],
    sys.argv[5],
    sys.argv[6],
    sys.argv[7],
)
save_contract_atomic(contract_path, contract)
print(status)
PY
~~~

G1 成為 REVIEW 後，由 course-run 呈現研究包再取得使用者核准：

~~~bash
python3 scripts/course_contract.py approve \
  --contract COURSE_CONTRACT --gate G1 \
  --approved-by USER_NAME --at ISO8601 \
  --note '使用者對研究證據、適配與限制的明確核准內容'
~~~

## 5. G2 架構交接

course-pm 只讀取已核准的 G0、G1 與 adaptation，寫出一份主藍圖。它把路徑、SHA-256、來源 revision、G1 evidence IDs、風險及 open questions 寫入 G2_architecture 與 G2 Gate 後，執行：

~~~bash
python3 scripts/course_contract.py validate --contract COURSE_CONTRACT
python3 scripts/course_contract.py submit \
  --contract COURSE_CONTRACT --gate G2 \
  --actor course-pm --at ISO8601
python3 scripts/course_contract.py approve \
  --contract COURSE_CONTRACT --gate G2 \
  --approved-by USER_NAME --at ISO8601 \
  --note '使用者對單一課程藍圖的明確核准內容'
~~~

## 6. 狀態與變更

~~~bash
python3 scripts/course_contract.py status --contract COURSE_CONTRACT
~~~

實質變更要指定最早受影響 Gate：

~~~bash
python3 scripts/course_contract.py change \
  --contract COURSE_CONTRACT --gate G0 \
  --reason '學員條件或成果要求改變' \
  --actor course-run --at ISO8601 --semantic
~~~

純錯字或不改語義的排版調整省略 --semantic，但仍執行相關技術回歸。

## 7. 本機 Skill 安裝與回復

~~~bash
python3 scripts/install_course_skill_foundation.py \
  --dry-run --skills-root /Users/paichenwei/.agents/skills
python3 scripts/install_course_skill_foundation.py \
  --apply --skills-root /Users/paichenwei/.agents/skills
python3 operations/course-skill-foundation/OPERATION_ID/rollback.py
~~~

rollback 會先核對目前已安裝內容仍等於 manifest 的 after_hash；若任何檔案已被後續修改，整次回復在改檔前停止。

## 範圍

此基礎層尚未完成 G3–G5 教學正文、代表單元、HTML 與內容驗證整合，也未完成 G6 register、ops、refresh 與 repair 整併。後續計畫必須直接使用本契約與 Gate 介面，不重開平行狀態。
