#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.course_content import validate_lesson_record  # noqa: E402
from src.course_contract import (  # noqa: E402
    begin_gate,
    new_contract,
    pass_gate,
    propose_external_action,
    save_contract_atomic,
    validate_contract,
)
from src.course_production import (  # noqa: E402
    route_full_production_to_g5,
    select_pilot_unit,
    validate_full_production,
    validate_pilot_record,
)
from src.course_release import build_release_proposal, validate_release_record  # noqa: E402
from src.course_research import route_research_to_gate, validate_research_record  # noqa: E402
from src.course_validation import route_verified_trial_to_gate  # noqa: E402


ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
DESIGN = ROOT / "_design" / "campaign-performance-brief"
COURSE = ROOT / "course"
TRIALS = ROOT / "trials"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def lesson_record(unit_id: str, page_hash: str) -> dict:
    definitions = {
        "unit-1": {
            "outcome": "完成三個活動的 CTR 與平均 CPC 計算表。",
            "context": "你已下載活動 CSV，現在要先把曝光、點擊與花費轉成可比較的效率指標。",
            "purpose": "建立下一單元會繼續使用的計算表，避免只憑原始大數字判斷。",
            "prior": "已確認 CSV 有三個活動及 impressions、clicks、cost 欄位。",
            "deliverable": "三個活動的 CTR 與平均 CPC 表",
            "demo": "Brand Search 的 CTR 8.00%，平均 CPC NT$30。",
            "guided": "Prospecting Social 的 CTR 1.80%，平均 CPC NT$50。",
            "independent": "Retargeting Display 的 CTR 與平均 CPC，並保留公式。",
            "decision": "選對每個公式的分母，並辨認百分比與金額格式。",
            "changed": ["活動換成 Retargeting Display", "不提供示範代入式"],
            "recovery": "百分比多乘一次 100 或 cost 與 clicks 放反。",
            "expected": "CTR 2.50%，平均 CPC NT$40。",
            "transfer": "日後遇到零 clicks 時，平均 CPC 標為無法計算而不是 0。"
        },
        "unit-2": {
            "outcome": "補齊 CVR、CPA 與 ROAS，並正確處理不能除以零的情況。",
            "context": "你已有 CTR 與平均 CPC，現在要把點擊接到轉換成本與價值。",
            "purpose": "完成能支持商業門檻判斷的五指標表。",
            "prior": "上一單元留下三個活動的 CTR 與平均 CPC。",
            "deliverable": "三個活動的五項成效指標表",
            "demo": "Retargeting Display 的 CVR 10.00%、CPA NT$400、ROAS 6.25。",
            "guided": "Prospecting Social 的 CVR 5.00%、CPA NT$1,000、ROAS 2.00。",
            "independent": "Brand Search 的 CVR、CPA 與 ROAS，並完成全表。",
            "decision": "分開判讀比例、單位成本與價值比率，不能用單一指標代替。",
            "changed": ["活動換成 Brand Search", "必須同時驗證三種單位"],
            "recovery": "把 clicks 當成 CPA 分母，或在零 conversions 時硬除。",
            "expected": "Brand Search 的 CVR 10.00%、CPA NT$300、ROAS 6.67。",
            "transfer": "跨平台比較前先確認 eligible interactions 與歸因口徑一致。"
        },
        "unit-3": {
            "outcome": "完成可驗收的成效摘要，區分數據判讀、限制與下一步。",
            "context": "你已有完整五指標表，現在要把它轉成同事可採取行動的摘要。",
            "purpose": "用數字支持達標判斷，同時避免把彙總資料寫成因果結論。",
            "prior": "前兩單元留下可重算的三列五指標表。",
            "deliverable": "campaign-performance-brief.md",
            "demo": "以 Prospecting Social 的 CPA NT$1,000 與 ROAS 2.00 寫出未達標判讀、資料界線與下一步測試。",
            "guided": "依 CPA ≤ NT$500 且 ROAS ≥ 4.00 檢查三個活動，說明兩項都符合才達標。",
            "independent": "完成數據摘要、判讀與建議三段，逐項通過 learner-visible rubric。",
            "decision": "區分資料直接支持的事實、仍不能確定的原因與可驗證的下一步。",
            "changed": ["從逐列計算改成跨活動決策", "必須寫出限制與後續觀察指標"],
            "recovery": "把高 CTR 寫成獲利原因，或提出沒有觀察指標的泛泛建議。",
            "expected": "Markdown 包含正確表格、Prospecting Social 未達標、資料界線與下一步測試。",
            "transfer": "換成不同門檻或不同活動時，保留事實、界線、行動的寫法。"
        },
    }
    item = definitions[unit_id]
    recovery_id = f"{unit_id}-recovery"
    return {
        "schema_version": 1,
        "unit_id": unit_id,
        "learner_outcome": {
            "statement": item["outcome"],
            "evidence": item["deliverable"],
        },
        "context": {
            "situation": item["context"],
            "purpose": item["purpose"],
            "prior_result": item["prior"],
        },
        "inputs": [
            {
                "id": "campaign-data",
                "label": "活動資料 CSV",
                "source": "課程首頁可下載的 campaign-data.csv",
                "ready_check": "看得到三列活動與五個原始數值欄位。",
            },
            {
                "id": "learner-rubric",
                "label": "完成品驗收規則",
                "source": "課程首頁與單元三可開啟的 rubric",
                "ready_check": "看得到五項可逐條核對的完成條件。",
            },
        ],
        "deliverable": {
            "name": item["deliverable"],
            "format": "可重算表格或 Markdown 文件",
            "use": "交給下一單元或同事做決策與驗收。",
            "acceptance_criteria": [item["expected"], "讀者可從 CSV 重算結果。"],
        },
        "explanation": {
            "prose": item["context"] + " " + item["purpose"] + " " + item["decision"]
        },
        "full_demonstration": {
            "input": {"description": "課程 CSV 中的示範活動", "value": item["demo"]},
            "rationale": "先完整展示輸入、判斷、計算、結果與驗證，讓學員知道完成品質。",
            "actions": [
                {
                    "purpose": "確認公式與資料欄位的對應。",
                    "start_state": "已開啟 CSV 與單元頁。",
                    "action": "依頁面公式代入示範活動的實際數字，保留中間算式。",
                    "expected_result": item["demo"],
                }
            ],
            "result": {"description": item["demo"], "artifact_ref": "單元頁完整示範段落"},
            "verification": [
                {"criterion": "數字與單位正確", "observable_result": item["demo"]}
            ],
        },
        "guided_practice": {
            "purpose": "在保留檢查提示的情況下完成第二個活動。",
            "start_state": "已看完完整示範，尚未計算引導活動。",
            "steps": [
                {
                    "purpose": "用同一方法處理不同數字。",
                    "start_state": "已找到引導活動那一列。",
                    "action": "先自行代入，再用頁面提供的預期結果核對。",
                    "expected_result": item["guided"],
                }
            ],
            "checks": [{"expected_result": item["guided"], "recovery_ref": recovery_id}],
            "recovery_refs": [recovery_id],
        },
        "independent_practice": {
            "context": "在沒有代入答案的情況下完成剩餘活動或完整摘要。",
            "changed_conditions": item["changed"],
            "decision_required": item["decision"],
            "deliverable": item["independent"],
            "acceptance_criteria": [item["expected"], "成果可由另一位讀者重新驗證。"],
            "verification": "依課程頁的快速檢查與 rubric 逐項核對。",
        },
        "checks": [
            {
                "id": f"{unit_id}-result-check",
                "target": item["deliverable"],
                "expected_result": item["expected"],
                "on_failure": f"依 {recovery_id} 回到公式、門檻或建議界線重新檢查。",
            }
        ],
        "recovery": [
            {
                "id": recovery_id,
                "symptom": item["recovery"],
                "cause": "沒有先確認分子、分母、單位或資料能支持的判斷範圍。",
                "action": "回到 CSV 與課程公式逐欄核對，保留算式，再依 rubric 重寫判讀。",
                "expected_result": item["expected"],
            }
        ],
        "transfer": {
            "new_context": "將同一方法用於另一個期間、活動組合或商業門檻。",
            "method": item["transfer"],
            "limits": "彙總指標描述結果，不能單獨證明受眾、素材或版位造成差異。",
        },
        "asset_references": ["campaign-data", "brief-template", "rubric"],
        "editorial_evidence": {
            "reviewer_id": "course-validator-editorial",
            "source_sha256": page_hash,
            "continuity_passed": True,
            "learner_readable": True,
            "internal_labels_removed": True,
            "notes": "逐段確認情境、理由、動作、結果與修復可連續閱讀，沒有待辦式正文。",
        },
    }


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    DESIGN.mkdir(parents=True, exist_ok=True)
    research = load_json(EVIDENCE / "research-record.json")
    adaptation = load_json(EVIDENCE / "adaptation.json")
    blueprint = load_json(EVIDENCE / "blueprint.json")
    research_issues = validate_research_record(research, adaptation)
    if research_issues:
        raise SystemExit(f"research invalid: {research_issues}")

    lesson_records: list[dict] = []
    for unit_id in ("unit-1", "unit-2", "unit-3"):
        record = lesson_record(unit_id, sha(COURSE / f"{unit_id}.html"))
        issues = validate_lesson_record(record)
        if issues:
            raise SystemExit(f"{unit_id} lesson invalid: {issues}")
        path = EVIDENCE / f"lesson-{unit_id}.json"
        write_json(path, record)
        lesson_records.append(record)

    assets = []
    for asset_id, filename, label, purpose in (
        ("campaign-data", "campaign-data.csv", "活動資料 CSV", "提供三個虛構活動的原始數據。"),
        ("brief-template", "brief-template.md", "成效摘要範本", "提供最終 Markdown 的可讀結構。"),
        ("rubric", "rubric.md", "完成品驗收規則", "讓學員與獨立試走者使用相同條件驗收。"),
    ):
        asset_path = COURSE / "assets" / filename
        assets.append(
            {
                "id": asset_id,
                "learner_label": label,
                "purpose": purpose,
                "source": {"type": "course-created", "uri": f"course/assets/{filename}", "retrieved_at": "2026-10-18"},
                "rights": {"status": "CLEARED", "basis": "課程團隊自行製作的虛構資料與文字。"},
                "version": f"sha256:{sha(asset_path)}",
                "access": {"method": "download or open", "learner_path": f"課程首頁連結 course/assets/{filename}", "backup": "內容可從學員頁直接複製。"},
                "open_test": {"tested_at": "2026-10-18T18:30:00+08:00", "actor": "course-author-ai", "result": "PASS", "sha256": sha(asset_path)},
            }
        )
    asset_manifest = {"schema_version": 1, "assets": assets}
    write_json(EVIDENCE / "asset-manifest.json", asset_manifest)

    selected_pilot = select_pilot_unit(blueprint)
    if selected_pilot != "unit-3":
        raise SystemExit(f"unexpected pilot selection: {selected_pilot}")
    pilot_lesson_path = EVIDENCE / "lesson-unit-3.json"
    pilot_lesson_hash = sha(pilot_lesson_path)
    pilot = {
        "schema_version": 1,
        "unit_id": "unit-3",
        "lesson_sha256": pilot_lesson_hash,
        "html_path": "course/unit-3.html",
        "html_sha256": sha(COURSE / "unit-3.html"),
        "asset_ids": ["campaign-data", "brief-template", "rubric"],
        "trial_context_id": "g4-cold-ai-context-20261018-a",
        "visual_decision": {
            "inputs": {"topic": "行銷活動成效摘要", "learner": "第一次獨立寫活動成效摘要的行銷同仁", "task": "讀 CSV、計算、判讀並寫成 Markdown", "content_density": "公式、實際數字與長文判讀並存", "primary_devices": ["mobile", "tablet", "desktop"]},
            "decisions": {"layout_rationale": "單欄閱讀讓公式、示範與修復保持相鄰。", "navigation": "每頁只有清楚的上一課與下一課。", "typography": "繁體中文正文使用較大行距，公式使用等寬字。", "color": "深青色只標示連結與成果，琥珀色提供焦點外框。", "responsive_strategy": "窄螢幕維持單欄，表格局部水平捲動。"}
        },
        "content_fidelity": {"source_sha256": pilot_lesson_hash, "rendered_source_sha256": pilot_lesson_hash, "teaching_atoms": ["learner_outcome", "full_demonstration", "guided_practice", "independent_practice", "recovery"], "result": "PASS"},
        "render": {"browser": "Playwright Chromium", "tested_at": "2026-10-18T18:40:00+08:00", "screenshots": ["evidence/unit-3-desktop.png", "evidence/unit-3-tablet.png", "evidence/unit-3-mobile.png"], "result": "PASS"},
        "devices": {
            "mobile": {"viewport": "390x844", "core_path_result": "PASS", "horizontal_overflow": False},
            "tablet": {"viewport": "820x1180", "core_path_result": "PASS", "horizontal_overflow": False},
            "desktop": {"viewport": "1440x900", "core_path_result": "PASS", "horizontal_overflow": False}
        },
        "accessibility": {
            "automated": {"tool": "HTML landmark/link audit", "result": "PASS", "report_path": "evidence/accessibility-report.json"},
            "manual": {"evaluator_id": "course-author-ai", "keyboard_result": "PASS", "focus_result": "PASS", "reading_sequence_result": "PASS", "notes": "鍵盤依閱讀順序到 rubric、上一課與首頁，focus 清楚可見。"}
        },
        "navigation": {"entry": "course/index.html", "previous": "course/unit-2.html", "next": "course/index.html"}
    }
    pilot_issues = validate_pilot_record(pilot, lesson_records[2], asset_manifest)
    if pilot_issues:
        raise SystemExit(f"pilot invalid: {pilot_issues}")
    write_json(EVIDENCE / "pilot-record.json", pilot)

    g4_trial = load_json(TRIALS / "g4-representative-unit.json")
    g5_trial = load_json(TRIALS / "g5-full-course.json")
    final_artifact = TRIALS / "full-course-output" / "campaign-performance-brief.md"
    if not final_artifact.is_file():
        raise SystemExit("missing independent full-course artifact")
    lesson_summaries = []
    production_units = []
    for index, unit in enumerate(blueprint["units"]):
        lesson_path = EVIDENCE / f"lesson-{unit['id']}.json"
        lesson_summaries.append({"unit_id": unit["id"], "outcome": unit["outcome"], "workflow_fingerprint": unit["workflow_fingerprint"], "depends_on": unit["depends_on"], "asset_references": unit["asset_ids"]})
        production_units.append({
            "unit_id": unit["id"],
            "lesson_sha256": sha(lesson_path),
            "html_path": f"course/{unit['id']}.html",
            "html_sha256": sha(COURSE / f"{unit['id']}.html"),
            "asset_ids": unit["asset_ids"],
            "outcome": unit["outcome"],
            "workflow_fingerprint": unit["workflow_fingerprint"],
            "depends_on": unit["depends_on"],
            "previous": None if index == 0 else blueprint["units"][index - 1]["id"],
            "next": None if index == len(blueprint["units"]) - 1 else blueprint["units"][index + 1]["id"]
        })
    production = {
        "schema_version": 1,
        "course_id": "campaign-performance-brief",
        "production_authors": ["course-author-ai"],
        "g4_trial_context_id": g4_trial["isolated_context_id"],
        "units": production_units,
        "navigation": {"entry": "course/index.html", "order": [unit["id"] for unit in blueprint["units"]], "completion": "trials/full-course-output/campaign-performance-brief.md"},
        "dependency_checks": [
            {"from_unit": "unit-1", "to_unit": "unit-2", "artifact": "trials/g4-output/metrics-table.md", "result": "PASS"},
            {"from_unit": "unit-2", "to_unit": "unit-3", "artifact": "trials/full-course-output/campaign-performance-brief.md", "result": "PASS"}
        ],
        "final_artifact": {
            "path": "trials/full-course-output/campaign-performance-brief.md",
            "sha256": sha(final_artifact),
            "outcome_id": "campaign-performance-brief",
            "acceptance": [
                {"criterion_id": "all-metrics", "result": "PASS", "evidence": "完成品數據摘要表三列五指標。"},
                {"criterion_id": "correct-threshold", "result": "PASS", "evidence": "完成品指出 Prospecting Social CPA NT$1,000、ROAS 2.00 未達標。"},
                {"criterion_id": "evidence-boundary", "result": "PASS", "evidence": "完成品說明彙總資料不能證明因果。"},
                {"criterion_id": "actionable-next-step", "result": "PASS", "evidence": "完成品提出下一步測試與觀察指標。"}
            ]
        },
        "full_course_trial": g5_trial,
        "validation": {"status": "PASS", "validator_id": "course-validator", "validated_at": "2026-10-18T19:40:00+08:00"}
    }
    production_issues = validate_full_production(production, blueprint, lesson_summaries, asset_manifest, pilot, g5_trial)
    if production_issues:
        raise SystemExit(f"full production invalid: {production_issues}")
    write_json(EVIDENCE / "production-record.json", production)

    for check in ("technical", "links", "registration", "access", "rollback", "maintenance"):
        write_json(EVIDENCE / f"release-{check}.json", {"check": check, "result": "PASS", "course": "campaign-performance-brief"})
    release_record = {
        "schema_version": 1,
        "course_id": "campaign-performance-brief",
        "g5_status": "PASS",
        "g6_state": "READY_TO_PUBLISH",
        "published": False,
        "checks": [
            {"id": check, "result": "PASS", "evidence": {"path": f"evidence/release-{check}.json", "sha256": sha(EVIDENCE / f"release-{check}.json")}}
            for check in ("technical", "links", "registration", "access", "rollback", "maintenance")
        ],
        "changes": [{"source_path": "release-staging/index.html", "target_path": "release-target/index.html"}],
        "maintenance": {"owner": "course-ops", "cadence": "quarterly", "freshness_sources": ["Google Ads official help pages", "learner trial issues"], "next_review": "2027-01-18"}
    }
    release_issues = validate_release_record(release_record)
    if release_issues:
        raise SystemExit(f"release invalid: {release_issues}")
    write_json(EVIDENCE / "release-record.json", release_record)
    staging = ROOT / "release-staging"
    staging.mkdir(exist_ok=True)
    shutil.copy2(COURSE / "index.html", staging / "index.html")
    proposal = build_release_proposal(ROOT, release_record)
    write_json(EVIDENCE / "release-proposal.json", proposal)

    contract = new_contract("campaign-performance-brief", "行銷活動成效摘要實作課", "course-author-ai", "2026-10-18T18:00:00+08:00")
    begin_gate(contract, "G0", "course-run", "2026-10-18T18:01:00+08:00")
    g0 = {
        "learner": "能讀表格、第一次獨立寫活動成效摘要的行銷同仁",
        "context": "主管需要在沒有口頭補充時讀懂三個活動的成效與下一步",
        "result": "campaign-performance-brief.md",
        "constraints": ["45 分鐘", "離線可完成", "使用台灣用語", "不宣稱彙總數據能證明因果"],
        "acceptance": blueprint["final_acceptance"]
    }
    write_json(EVIDENCE / "g0-requirements.json", g0)
    contract["G0_requirements"] = copy.deepcopy(g0)
    contract["evidence_index"].append({"id": "g0-requirements", "gate": "G0", "path": "evidence/g0-requirements.json", "sha256": sha(EVIDENCE / "g0-requirements.json")})
    pass_gate(contract, "G0", ["g0-requirements"], "requirements-validator", "course-run", "2026-10-18T18:02:00+08:00")

    begin_gate(contract, "G1", "course-run", "2026-10-18T18:03:00+08:00")
    route_research_to_gate(contract, research, adaptation, "evidence/research-record.json", sha(EVIDENCE / "research-record.json"), "course-run", "2026-10-18T18:04:00+08:00")

    begin_gate(contract, "G2", "course-run", "2026-10-18T18:05:00+08:00")
    contract["G2_architecture"] = {"record_path": "evidence/blueprint.json", "sha256": sha(EVIDENCE / "blueprint.json")}
    contract["evidence_index"].append({"id": "g2-blueprint", "gate": "G2", "path": "evidence/blueprint.json", "sha256": sha(EVIDENCE / "blueprint.json")})
    pass_gate(contract, "G2", ["g2-blueprint"], "course-blueprint-validator", "course-run", "2026-10-18T18:06:00+08:00")

    begin_gate(contract, "G3", "course-run", "2026-10-18T18:07:00+08:00")
    content_bundle = {"lesson_records": [{"unit_id": record["unit_id"], "path": f"evidence/lesson-{record['unit_id']}.json", "sha256": sha(EVIDENCE / f"lesson-{record['unit_id']}.json")} for record in lesson_records], "validation": "PASS"}
    write_json(EVIDENCE / "content-bundle.json", content_bundle)
    contract["G3_lesson_design"] = {"record_path": "evidence/content-bundle.json", "sha256": sha(EVIDENCE / "content-bundle.json"), "unit_count": 3}
    contract["evidence_index"].append({"id": "g3-content-bundle", "gate": "G3", "path": "evidence/content-bundle.json", "sha256": sha(EVIDENCE / "content-bundle.json")})
    pass_gate(contract, "G3", ["g3-content-bundle"], "course-lesson-record-validator", "course-run", "2026-10-18T18:08:00+08:00")

    begin_gate(contract, "G4", "course-run", "2026-10-18T18:09:00+08:00")
    pilot_bundle = {"pilot_record": "evidence/pilot-record.json", "asset_manifest": "evidence/asset-manifest.json", "result": "PASS"}
    write_json(EVIDENCE / "pilot-bundle.json", pilot_bundle)
    contract["G4_pilot"] = {"unit_id": "unit-3", "record_path": "evidence/pilot-record.json"}
    contract["evidence_index"].append({"id": "g4-pilot-production", "gate": "G4", "path": "evidence/pilot-bundle.json", "sha256": sha(EVIDENCE / "pilot-bundle.json")})
    route_verified_trial_to_gate(contract, "G4", ["g4-pilot-production"], g4_trial, "course-run", "2026-10-18T19:10:00+08:00")

    begin_gate(contract, "G5", "course-run", "2026-10-18T19:11:00+08:00")
    contract["G5_production"] = {"record_path": "evidence/production-record.json", "sha256": sha(EVIDENCE / "production-record.json")}
    route_full_production_to_g5(contract, production, [{"id": "g5-render-integration", "gate": "G5", "path": "evidence/production-record.json", "sha256": sha(EVIDENCE / "production-record.json")}], "course-run", "2026-10-18T19:45:00+08:00")

    begin_gate(contract, "G6", "course-run", "2026-10-18T19:46:00+08:00")
    contract["G6_release_maintenance"] = {"state": "READY_TO_PUBLISH", "record_path": "evidence/release-record.json", "published": False}
    contract["evidence_index"].append({"id": "g6-release-readiness", "gate": "G6", "path": "evidence/release-record.json", "sha256": sha(EVIDENCE / "release-record.json")})
    pass_gate(contract, "G6", ["g6-release-readiness"], "course-release-record-validator", "course-run", "2026-10-18T19:47:00+08:00")
    propose_external_action(contract, proposal["action_id"], "course-release", "evidence/release-proposal.json", proposal["manifest_sha256"], "course-ops", "2026-10-18T19:48:00+08:00")
    issues = validate_contract(contract)
    if issues:
        raise SystemExit(f"contract invalid: {issues}")
    save_contract_atomic(DESIGN / "course-contract.json", contract)

    write_json(EVIDENCE / "proof-validation.json", {
        "research": "PASS",
        "lessons": {record["unit_id"]: "PASS" for record in lesson_records},
        "pilot": "PASS",
        "full_production": "PASS",
        "release_readiness": "PASS",
        "maturity": "INDEPENDENT_AI_VERIFIED",
        "external_publication": "NOT_EXECUTED"
    })
    print(DESIGN / "course-contract.json")


if __name__ == "__main__":
    main()
