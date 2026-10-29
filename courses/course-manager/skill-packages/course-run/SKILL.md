---
name: course-run
description: Use when creating a new course from initial requirements through staged production, especially when several course capabilities need one contract, evidence gates, external-action authorization, or change control.
---

# Course Run

## Overview

Use one course contract to move a new course through G0–G6. Ask only questions that can change the design, preserve full teaching prose, and advance each Gate automatically when its required evidence passes validation. Require explicit user authorization only for publishing, deployment, access changes, registration, or other external mutations.

Read [gate-routing.json](references/gate-routing.json) for deterministic authority and prerequisites. Read [course-contract-routing.md](references/course-contract-routing.md) for commands and child return fields.

## Start or Resume

1. Locate _design/{slug}/course-contract.json.
2. If absent, begin G0 with an adaptive interview covering learner and baseline, work context, observable artifact, duration and delivery, tools, accounts, permissions, device, locale, prerequisites, constraints, acceptance criteria with child capabilities, assumptions, unknowns, and decisions. Save a requirements record conforming to `contracts/course-requirements-record.schema.json`; unresolved material unknowns keep G0 BLOCKED. Do not repeat facts already supplied.
3. Create the contract with the CLI init command in the routing reference.
4. 執行 `python3 "$COURSE_DESIGN_SYSTEM_ROOT/scripts/course_run.py" resume --contract CONTRACT --actor course-run --at ISO8601`。CLI 會以 transaction 開始第一個未通過 Gate，並在 `COURSE_DESIGN_STATE_ROOT` 產生可重播的單一 dispatch envelope。

A G0 work record may preserve unknowns. Important unknowns keep the Gate BLOCKED until resolved.

G2 consumes the canonical G0 record and writes a blueprint conforming to `contracts/course-blueprint-record.schema.json`. It returns one evidence-backed main path, stable outcome and criterion IDs, a dependency DAG, exact duration reconciliation, and complete unit plans. Only the central Gate dispatcher records G0 or G2 PASS; producer-declared validator names or PASS flags are not evidence.

## Gate Cycle

For the current Gate:

1. Confirm every prerequisite is PASS.
2. Dispatch the producer and require the structured return defined in the routing reference.
3. Keep detailed research, prose, media, and test records in external files. Put paths and SHA-256 evidence references in the contract.
4. If required information, material, permission, environment, hands-on execution, or evidence is missing, record the reason and set the Gate to BLOCKED. Preserve failed attempts as evidence.
5. 以 `course_run.py complete --contract CONTRACT --gate GATE --evidence-id ID --actor course-run --at ISO8601` 完成。它在同一 transaction 內呼叫中央 Gate dispatcher；成功時開始下一 Gate，缺證據時保存 BLOCKED envelope。不得改回只輸出 JSON、沒有呼叫 validator 的假調度。
6. Gate PASS 後自動開始下一個 Gate，不要求使用者逐關核准。Show the user the actual deliverables, evidence, blockers, risks, open questions, and next action at meaningful decision points. Do not replace their prose with an abbreviated summary.
7. Before an external mutation, create an exact action manifest, request explicit user authorization, and verify the authorized hash immediately before execution.

A producer returns deliverables and evidence. Only course-run records Gate PASS. Never infer authorization for an external mutation from silence, a Gate PASS, previous authorization, or permission to continue a different action.

## 何時詢問使用者

一般資料蒐集、內容撰寫、版型選擇、素材製作、驗證與 Gate 間調度由系統繼續執行。只有下列五種情況暫停並詢問，判準以 `gate-routing.json` 為準：

1. 缺少的資訊會實質改變學員、成果、範圍、順序、評量、授課方式或時數。
2. 有兩個以上都有證據支持、但會導向不同課程成果的重大判斷。
3. 下一步會購買、訂閱或使用付費服務。
4. 下一步需要帳號憑證、私人資料、存取權、授權或著作權確認。
5. 下一步會發布、部署、註冊、改變存取權、對外傳訊或修改外部系統。

資料雖不完整但不會改變設計時，清楚記錄假設與風險後繼續。Gate 內驗證失敗時保留證據並依失敗原因回送責任 Gate，不把可自行修復的問題丟回使用者決定。

## G0 and Adaptation

G0 is a conversation, not a fixed questionnaire. Ask the smallest next question that changes the course architecture. G1 derives adaptation from learner gap, task nature, tool dependency, volatility, failure risk, and evidence type. Subject labels such as AI, marketing, or software do not select a fixed template.

## Change Control

For a semantic change, record the earliest affected Gate with change --semantic. Rework that Gate from IN_PROGRESS; treat every downstream STALE Gate as unusable until revalidated. Record typo or layout-only changes without --semantic and run the relevant technical regression.

## G5 全課整合

G4 代表單元連同獨立 AI 試走通過後，才展開全課量產。G5 必須逐一核對藍圖單元、正式 lesson、學員 HTML 與所有素材，不得因檔案存在就視為完成。

全課紀錄必須證明：每個單元有不同且可追溯的學習成果與工作流程；前後單元的產物依賴已有實際交接；首頁、上一課、下一課與完成頁導覽完整；最終成果逐項符合 G0 驗收條件。完成後以新的隔離情境，由未參與製作或驗證的 AI 只使用學員可見頁面與素材走完整門課。G5 試走不得沿用 G4 情境或製作對話。

覆蓋矩陣逐一串接 G0 acceptance criterion 的每個 child capability、G2 outcome／criterion／unit、G3 lesson 的教學／練習／評量證據，以及 G5 artifact criterion／trial evidence。父 outcome 存在不能代替遺漏的 child capability。

只有全課製作證據、最終成果驗收與 `full_course` 獨立試走同時通過，G5 才能 PASS。缺口依實際原因回送 G0–G5；修正後重算受影響檔案與證據雜湊。

## Boundaries

Use this Skill only for new courses. Route diagnosis or repair of an existing course to course-repair. Do not enter G4 batch production before the representative unit passes. Do not treat evidence maturity labels as Gate lifecycle states.

目前 orchestrator 不執行 `course-repair fix`。repair mutation 必須另有受治理 transaction，驗證 approved plan hash、所有 before hashes、完整 backup manifest 與隔離 restore proof；整合完成前一律 fail closed。
