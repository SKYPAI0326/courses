import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.course_architecture import (
    BLUEPRINT_REQUIRED_FIELDS,
    validate_course_blueprint,
    validate_learning_coverage,
)
from src.course_architecture_routes import route_blueprint_to_g2
from src.course_contract import begin_gate, new_contract
from src.course_evidence import materialize_json_evidence
from tests.gate_test_support import _commit_gate_pass


class CourseArchitectureTests(unittest.TestCase):
    def requirements(self):
        from tests.test_course_requirements import CourseRequirementsTests

        return CourseRequirementsTests().valid_record()

    def bind_g0_requirements(self, root, contract):
        reference = materialize_json_evidence(
            root, evidence_id="g0-governed", gate_id="G0", kind="requirements_record",
            relative_path="evidence/g0-governed.json", value=self.requirements(),
        )
        contract["evidence_index"].append(reference)
        event = contract["gates"]["G0"]["evidence"][-1]
        event["evidence_ids"] = [reference["id"]]
        event["consumed_evidence_ids"] = [reference["id"]]
        event["consumed_evidence"] = [{field: reference[field] for field in ("id", "gate", "kind", "path", "sha256")}]
        g1_reference = materialize_json_evidence(
            root, evidence_id="g1-fixture", gate_id="G1", kind="test_record",
            relative_path="evidence/g1-fixture.json", value={"research": "governed"},
        )
        index = next(index for index, item in enumerate(contract["evidence_index"]) if item["id"] == "g1-fixture")
        contract["evidence_index"][index] = g1_reference
        g1_event = contract["gates"]["G1"]["evidence"][-1]
        g1_event["consumed_evidence_ids"] = [g1_reference["id"]]
        g1_event["consumed_evidence"] = [{field: g1_reference[field] for field in ("id", "gate", "kind", "path", "sha256")}]

    def valid_blueprint(self):
        return {
            "schema_version": 1,
            "blueprint_id": "campaign-brief-blueprint",
            "requirements_id": "campaign-brief-requirements",
            "decision_narrative": {
                "recommended_path": "先用固定資料完成指標計算，再把判讀寫成主管可採用的決策簡報。",
                "rationale": "研究顯示新手的主要風險是公式錯誤與把相關性寫成因果，因此先穩定計算，再練習判讀與證據邊界。",
                "constraint_fit": "兩個八十分鐘單元加上十分鐘休息與十分鐘緩衝，能在三小時內完成並驗收成品。",
                "g1_evidence_refs": ["g1-fixture"],
            },
            "outcomes": [
                {
                    "id": "outcome-calculate",
                    "statement": "學員能從固定欄位計算四項活動成效指標。",
                    "criterion_ids": ["g2-criterion-calculate"],
                },
                {
                    "id": "outcome-recommend",
                    "statement": "學員能依門檻提出有證據邊界的後續建議。",
                    "criterion_ids": ["g2-criterion-recommend"],
                },
            ],
            "criteria": [
                {
                    "id": "g2-criterion-calculate",
                    "outcome_id": "outcome-calculate",
                    "g0_criterion_id": "criterion-decision-brief",
                    "capability_id": "capability-calculate",
                    "statement": "四項指標的公式、數值與單位都正確。",
                    "assessment_evidence": "提交含公式與結果的指標表，並逐欄核對。",
                },
                {
                    "id": "g2-criterion-recommend",
                    "outcome_id": "outcome-recommend",
                    "g0_criterion_id": "criterion-decision-brief",
                    "capability_id": "capability-recommend",
                    "statement": "建議指出未達門檻的活動、限制與下一個可觀察測試。",
                    "assessment_evidence": "提交主管可讀的判讀段落與測試指標。",
                },
            ],
            "units": [
                self.unit(
                    "unit-calculate",
                    "建立可信的指標表",
                    "outcome-calculate",
                    "g2-criterion-calculate",
                    "capability-calculate",
                    [],
                    "calculate-four-metrics-from-raw-columns",
                    "g1-fixture",
                ),
                self.unit(
                    "unit-recommend",
                    "把指標轉成決策簡報",
                    "outcome-recommend",
                    "g2-criterion-recommend",
                    "capability-recommend",
                    ["unit-calculate"],
                    "compare-thresholds-and-propose-test",
                    "g1-fixture",
                ),
            ],
            "duration": {
                "available_minutes": 180,
                "break_minutes": 10,
                "buffer_minutes": 10,
                "policy": "單元間安排休息；緩衝用於公式輸入或匯出失敗的恢復，不刪除獨立練習。",
            },
            "materials": [
                "去識別化活動資料 CSV、指標公式速查表、完成簡報範例與驗收規準。"
            ],
            "risks": [
                {
                    "id": "risk-spreadsheet-version",
                    "description": "不同試算表版本的匯出介面可能不同。",
                    "owner_gate": "G3",
                    "mitigation": "教材提供通用另存步驟及 Markdown 備援交付方式。",
                }
            ],
        }

    def unit(self, unit_id, title, outcome_id, criterion_id, capability_id, deps, workflow, evidence_ref):
        return {
            "id": unit_id,
            "title": title,
            "context": "學員正在準備每週例會，需要把上一階段成果轉成可交付內容。",
            "output": "完成一份可直接銜接下一階段的課程產物。",
            "prerequisite_unit_ids": deps,
            "outcome_ids": [outcome_id],
            "criterion_ids": [criterion_id],
            "capability_ids": [capability_id],
            "teaching_approach": "先解釋判斷依據，再示範完整輸入、選擇理由、操作結果與驗證。",
            "worked_example_plan": {
                "input": "使用課程提供的一列活動資料與明確門檻。",
                "rationale": "示範每個動作如何連回主管要做的決策。",
                "actions": ["完成計算或判讀，保留中間依據並核對結果。"],
                "result": "得到可供主管閱讀、且能追溯來源的階段產物。",
                "verification": "依該單元 criterion 檢查公式、理由與可觀察結果。",
            },
            "guided_practice": {
                "activity": "學員用第二筆資料跟做，並在關鍵步驟停下核對。",
                "feedback": "檢核表指出錯誤位於欄位、公式或判讀門檻。",
                "check": "學員能說明目前結果與示範不同的原因。",
                "recovery": "回到原始欄位或門檻，修正後重新計算與核對。",
            },
            "independent_practice": {
                "changed_conditions": ["改用第三個活動資料", "改變其中一項成效門檻"],
                "decision": "學員自行判斷要使用的公式或建議。",
                "deliverable": "一份未複製示範答案、可獨立驗收的階段成果。",
                "check": "依 criterion 逐項核對，且保留失敗後修正紀錄。",
                "recovery": "若未通過，先定位資料、公式或推論錯誤，再重做受影響部分。",
            },
            "assessment_evidence": [
                {"criterion_id": criterion_id, "evidence": "保存獨立練習成品與逐項檢核結果。"}
            ],
            "materials": ["課程資料 CSV、階段成果模板與檢核表。"],
            "duration_minutes": 80,
            "g1_evidence_refs": [evidence_ref],
            "workflow_fingerprint": workflow,
        }

    def lesson(self, unit_id, outcome_id, criterion_id, capability_id):
        return {
            "unit_id": unit_id,
            "outcome_ids": [outcome_id],
            "criterion_ids": [criterion_id],
            "capability_ids": [capability_id],
            "learning_coverage": [
                {
                    "outcome_id": outcome_id,
                    "criterion_id": criterion_id,
                    "capability_id": capability_id,
                    "teaching_evidence": ["explanation", "full_demonstration"],
                    "practice_evidence": ["guided_practice", "independent_practice"],
                    "assessment_evidence": ["checks"],
                }
            ],
            "explanation": {},
            "full_demonstration": {},
            "guided_practice": {},
            "independent_practice": {},
            "checks": [{"id": f"{unit_id}-check"}],
        }

    def production(self):
        return {
            "learning_coverage": [
                {
                    "g0_criterion_id": "criterion-decision-brief",
                    "capability_id": "capability-calculate",
                    "outcome_id": "outcome-calculate",
                    "criterion_id": "g2-criterion-calculate",
                    "unit_id": "unit-calculate",
                    "lesson_unit_id": "unit-calculate",
                    "artifact_criterion_id": "criterion-decision-brief",
                    "artifact_evidence_id": "criterion-decision-brief",
                    "trial_evidence_id": "action-1",
                },
                {
                    "g0_criterion_id": "criterion-decision-brief",
                    "capability_id": "capability-recommend",
                    "outcome_id": "outcome-recommend",
                    "criterion_id": "g2-criterion-recommend",
                    "unit_id": "unit-recommend",
                    "lesson_unit_id": "unit-recommend",
                    "artifact_criterion_id": "criterion-decision-brief",
                    "artifact_evidence_id": "criterion-decision-brief",
                    "trial_evidence_id": "action-1",
                },
            ],
            "final_artifact": {
                "acceptance": [{"criterion_id": "criterion-decision-brief"}]
            },
            "full_course_trial": {
                "actions": [{"id": "action-1", "sequence": 1, "result": "PASS"}]
            },
        }

    def test_complete_blueprint_is_valid_and_uses_one_reasoned_path(self):
        self.assertEqual(validate_course_blueprint(self.valid_blueprint(), self.requirements()), [])

    def test_g1_evidence_refs_must_belong_to_governed_known_set(self):
        blueprint = self.valid_blueprint()
        blueprint["units"][0]["g1_evidence_refs"] = ["g1-does-not-exist"]
        codes = {
            issue.code for issue in validate_course_blueprint(
                blueprint, self.requirements(), known_g1_evidence_ids={"g1-fixture"}
            )
        }
        self.assertIn("unknown_g1_evidence", codes)

    def test_runtime_enforces_closed_schema_and_owner_gate_enum(self):
        blueprint = self.valid_blueprint()
        blueprint["producer_validation"] = {"status": "PASS"}
        blueprint["risks"][0]["owner_gate"] = "producer"
        codes = {issue.code for issue in validate_course_blueprint(blueprint, self.requirements())}
        self.assertIn("schema_additional_property", codes)
        self.assertIn("schema_pattern", codes)

    def test_title_only_or_todo_like_unit_cannot_pass(self):
        blueprint = self.valid_blueprint()
        blueprint["units"][0]["teaching_approach"] = "介紹 CTR、CPC、CPA、ROAS"
        blueprint["units"][0]["worked_example_plan"]["actions"] = ["完成示範"]

        codes = {issue.code for issue in validate_course_blueprint(blueprint, self.requirements())}

        self.assertIn("non_executable_unit", codes)

        padded = self.valid_blueprint()
        padded["units"][0]["teaching_approach"] = "TODO：之後補上完整示範與練習。"
        self.assertIn(
            "non_executable_unit",
            {issue.code for issue in validate_course_blueprint(padded, self.requirements())},
        )

    def test_duration_must_fit_g0_time_with_explicit_break_and_buffer(self):
        blueprint = self.valid_blueprint()
        blueprint["duration"]["buffer_minutes"] = 0

        codes = {issue.code for issue in validate_course_blueprint(blueprint, self.requirements())}

        self.assertIn("duration_mismatch", codes)

        blueprint = self.valid_blueprint()
        blueprint["duration"]["break_minutes"] = True
        blueprint["duration"]["buffer_minutes"] = 19
        codes = {issue.code for issue in validate_course_blueprint(blueprint, self.requirements())}
        self.assertIn("duration_mismatch", codes)

    def test_dependency_cycle_unknown_dependency_and_orphan_outcome_fail(self):
        cycle = self.valid_blueprint()
        cycle["units"][0]["prerequisite_unit_ids"] = ["unit-recommend"]
        self.assertIn("dependency_cycle", {i.code for i in validate_course_blueprint(cycle, self.requirements())})

        unknown = self.valid_blueprint()
        unknown["units"][1]["prerequisite_unit_ids"] = ["missing-unit"]
        self.assertIn("unknown_reference", {i.code for i in validate_course_blueprint(unknown, self.requirements())})

        orphan = self.valid_blueprint()
        orphan["units"][1]["outcome_ids"] = []
        self.assertIn("orphan_outcome", {i.code for i in validate_course_blueprint(orphan, self.requirements())})

        disconnected = self.valid_blueprint()
        disconnected["units"][1]["prerequisite_unit_ids"] = []
        self.assertIn(
            "orphan_unit",
            {i.code for i in validate_course_blueprint(disconnected, self.requirements())},
        )

    def test_every_child_capability_requires_its_own_g2_criterion(self):
        blueprint = self.valid_blueprint()
        blueprint["criteria"].pop()
        blueprint["outcomes"][1]["criterion_ids"] = []
        blueprint["units"][1]["criterion_ids"] = []
        blueprint["units"][1]["capability_ids"] = []

        codes = {issue.code for issue in validate_course_blueprint(blueprint, self.requirements())}

        self.assertIn("uncovered_capability", codes)

    def test_duplicate_workflow_or_unknown_stable_reference_fails_closed(self):
        blueprint = self.valid_blueprint()
        blueprint["units"][1]["workflow_fingerprint"] = blueprint["units"][0]["workflow_fingerprint"]
        blueprint["units"][1]["criterion_ids"] = ["missing-criterion"]
        blueprint["units"][0]["g1_evidence_refs"].append(
            blueprint["units"][0]["g1_evidence_refs"][0]
        )

        codes = {issue.code for issue in validate_course_blueprint(blueprint, self.requirements())}

        self.assertIn("duplicate_workflow", codes)
        self.assertIn("unknown_reference", codes)
        self.assertIn("duplicate_reference", codes)

    def test_self_declared_pass_field_is_not_part_of_canonical_g2(self):
        blueprint = self.valid_blueprint()
        blueprint["validation"] = {"status": "PASS", "validator_id": "producer"}

        self.assertIn(
            "unsupported_field",
            {issue.code for issue in validate_course_blueprint(blueprint, self.requirements())},
        )

    def test_unit_cannot_mix_an_outcome_with_another_capability(self):
        blueprint = self.valid_blueprint()
        blueprint["units"][0]["capability_ids"] = ["capability-recommend"]

        codes = {issue.code for issue in validate_course_blueprint(blueprint, self.requirements())}

        self.assertIn("inconsistent_unit_coverage", codes)

    def test_child_capability_cannot_be_claimed_by_multiple_units(self):
        blueprint = self.valid_blueprint()
        blueprint["units"][1]["outcome_ids"].append("outcome-calculate")
        blueprint["units"][1]["criterion_ids"].append("g2-criterion-calculate")
        blueprint["units"][1]["capability_ids"].append("capability-calculate")
        blueprint["units"][1]["assessment_evidence"].append(
            {"criterion_id": "g2-criterion-calculate", "evidence": "保存重複驗收的指標表。"}
        )

        codes = {issue.code for issue in validate_course_blueprint(blueprint, self.requirements())}

        self.assertIn("duplicate_unit_coverage", codes)

    def test_every_unit_criterion_requires_its_own_assessment_evidence(self):
        requirements = self.requirements()
        requirements["acceptance_criteria"][0]["capabilities"].append(
            {"id": "capability-audit", "statement": "逐項稽核簡報中的門檻與建議。"}
        )
        blueprint = self.valid_blueprint()
        blueprint["outcomes"][1]["criterion_ids"].append("g2-criterion-audit")
        blueprint["criteria"].append(
            {
                "id": "g2-criterion-audit",
                "outcome_id": "outcome-recommend",
                "g0_criterion_id": "criterion-decision-brief",
                "capability_id": "capability-audit",
                "statement": "簡報的門檻與建議能逐項通過稽核。",
                "assessment_evidence": "保存逐項稽核結果。",
            }
        )
        blueprint["units"][1]["criterion_ids"].append("g2-criterion-audit")
        blueprint["units"][1]["capability_ids"].append("capability-audit")

        codes = {issue.code for issue in validate_course_blueprint(blueprint, requirements)}

        self.assertIn("assessment_evidence_required", codes)

    def test_duration_policy_must_explain_break_and_buffer(self):
        blueprint = self.valid_blueprint()
        blueprint["duration"]["policy"] = "課程會依時間安排進行。"

        self.assertIn(
            "duration_policy_required",
            {issue.code for issue in validate_course_blueprint(blueprint, self.requirements())},
        )

    def test_end_to_end_matrix_requires_teaching_practice_assessment_artifact_and_trial_evidence(self):
        blueprint = self.valid_blueprint()
        lessons = [
            self.lesson("unit-calculate", "outcome-calculate", "g2-criterion-calculate", "capability-calculate"),
            self.lesson("unit-recommend", "outcome-recommend", "g2-criterion-recommend", "capability-recommend"),
        ]
        production = self.production()
        self.assertEqual(validate_learning_coverage(self.requirements(), blueprint, lessons, production), [])

        broken = copy.deepcopy(production)
        broken["learning_coverage"].pop()
        codes = {
            issue.code
            for issue in validate_learning_coverage(self.requirements(), blueprint, lessons, broken)
        }
        self.assertIn("uncovered_capability", codes)

        broken_lesson = copy.deepcopy(lessons)
        broken_lesson[0]["learning_coverage"][0]["practice_evidence"] = []
        codes = {
            issue.code
            for issue in validate_learning_coverage(self.requirements(), blueprint, broken_lesson, production)
        }
        self.assertIn("incomplete_lesson_coverage", codes)

    def test_schema_required_fields_match_runtime(self):
        schema = json.loads(
            (Path(__file__).parents[1] / "contracts" / "course-blueprint-record.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(schema["required"]), set(BLUEPRINT_REQUIRED_FIELDS))

    def test_g2_route_materializes_blueprint_and_uses_central_dispatcher(self):
        contract = new_contract(
            "campaign-brief", "活動成效簡報", "course-run", "2026-10-18T09:00:00+08:00"
        )
        contract["G0_requirements"] = self.requirements()
        for gate_id in ("G0", "G1"):
            begin_gate(contract, gate_id, "course-run", "2026-10-18T09:01:00+08:00")
            evidence_id = f"{gate_id.lower()}-fixture"
            contract["evidence_index"].append(
                {
                    "id": evidence_id,
                    "gate": gate_id,
                    "kind": "test_record",
                    "path": f"evidence/{evidence_id}.json",
                    "sha256": hashlib.sha256(evidence_id.encode()).hexdigest(),
                }
            )
            _commit_gate_pass(
                contract, gate_id, [evidence_id], "test-fixture", "course-run", "2026-10-18T09:02:00+08:00"
            )
        begin_gate(contract, "G2", "course-run", "2026-10-18T09:03:00+08:00")
        with tempfile.TemporaryDirectory() as temporary:
            self.bind_g0_requirements(temporary, contract)
            status = route_blueprint_to_g2(
                contract,
                self.valid_blueprint(),
                "evidence/g2-blueprint.json",
                "course-pm",
                "2026-10-18T09:04:00+08:00",
                workspace_root=temporary,
            )

        self.assertEqual(status, "PASS")
        self.assertEqual(contract["gates"]["G2"]["evidence"][-1]["validator_id"], "course-blueprint-validator")

    def test_g2_route_rejects_empty_self_declared_pass(self):
        contract = new_contract(
            "campaign-brief", "活動成效簡報", "course-run", "2026-10-18T09:00:00+08:00"
        )
        contract["G0_requirements"] = self.requirements()
        for gate_id in ("G0", "G1"):
            begin_gate(contract, gate_id, "course-run", "2026-10-18T09:01:00+08:00")
            evidence_id = f"{gate_id.lower()}-fixture"
            contract["evidence_index"].append(
                {
                    "id": evidence_id,
                    "gate": gate_id,
                    "kind": "test_record",
                    "path": f"evidence/{evidence_id}.json",
                    "sha256": hashlib.sha256(evidence_id.encode()).hexdigest(),
                }
            )
            _commit_gate_pass(
                contract, gate_id, [evidence_id], "test-fixture", "course-run", "2026-10-18T09:02:00+08:00"
            )
        begin_gate(contract, "G2", "course-run", "2026-10-18T09:03:00+08:00")

        with tempfile.TemporaryDirectory() as temporary:
            self.bind_g0_requirements(temporary, contract)
            status = route_blueprint_to_g2(
                contract,
                {"schema_version": 1, "validation": {"status": "PASS", "validator_id": "self-declared"}},
                "evidence/g2-blueprint.json",
                "course-pm",
                "2026-10-18T09:04:00+08:00",
                workspace_root=temporary,
            )

        self.assertEqual(status, "BLOCKED")
        self.assertEqual(contract["gates"]["G2"]["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
