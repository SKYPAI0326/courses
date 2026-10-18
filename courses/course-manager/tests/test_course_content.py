import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.course_content import REQUIRED_SECTIONS, validate_lesson_record
from src.course_content_routes import route_content_to_g3
from src.course_contract import begin_gate, new_contract
from src.course_evidence import materialize_json_evidence
from tests.gate_test_support import _commit_gate_pass


class CourseContentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary.cleanup()

    def valid_record(self):
        return {
            "schema_version": 1,
            "unit_id": "unit-1",
            "outcome_ids": ["outcome-plan"],
            "criterion_ids": ["criterion-plan"],
            "capability_ids": ["capability-plan"],
            "learning_coverage": [
                {
                    "outcome_id": "outcome-plan",
                    "criterion_id": "criterion-plan",
                    "capability_id": "capability-plan",
                    "teaching_evidence": ["explanation", "full_demonstration"],
                    "practice_evidence": ["guided_practice", "independent_practice"],
                    "assessment_evidence": ["checks"],
                }
            ],
            "learner_outcome": {
                "statement": "學員能把商品資料整理成可供主管審核的活動企劃。",
                "evidence": "完成一份含受眾、渠道、理由與檢核結果的企劃。",
            },
            "context": {
                "situation": "你剛接手一項新品上市任務，主管要在今天確認活動方向。",
                "purpose": "先建立可追溯的企劃，才能讓主管判斷預算是否值得投入。",
                "prior_result": "你已取得去識別化的商品資料與活動限制。",
            },
            "inputs": [
                {
                    "id": "asset-product-brief",
                    "label": "商品資料簡報",
                    "source": "課程素材區的商品資料簡報",
                    "ready_check": "能看到商品特色、預算上限與活動日期。",
                }
            ],
            "deliverable": {
                "name": "新品活動企劃",
                "format": "HTML 表單匯出的 PDF",
                "use": "交給主管審核活動方向與預算。",
                "acceptance_criteria": [
                    "受眾與商品特色相符",
                    "渠道選擇附有可追溯理由",
                ],
            },
            "explanation": {
                "prose": (
                    "活動企劃先回答要影響誰，再決定在哪裡接觸對方。"
                    "這個順序能讓渠道選擇回到商品資料，而不是只列熱門平台。\n\n"
                    "等受眾與渠道的關係清楚後，再把理由寫成主管能檢查的句子。"
                    "你稍後會沿用同一套判斷處理新的商品限制。"
                )
            },
            "full_demonstration": {
                "input": {
                    "description": "一款低糖常溫點心的商品資料與十萬元預算限制。",
                    "value": "主要賣點是方便攜帶，首波客群是通勤上班族。",
                },
                "rationale": "先鎖定使用情境，才能避免把所有社群平台都列入。",
                "actions": [
                    {
                        "purpose": "把商品特色轉成可觀察的受眾需求。",
                        "start_state": "企劃表的受眾欄仍是空白。",
                        "action": "填入通勤上班族，並註明需要方便攜帶的早餐替代品。",
                        "expected_result": "受眾欄同時出現角色與需求，不只剩年齡標籤。",
                    }
                ],
                "result": {
                    "description": "完成的企劃清楚連結受眾、渠道與商品特色。",
                    "artifact_ref": "asset-demo-plan",
                },
                "verification": [
                    {
                        "criterion": "每個渠道都有商品或受眾依據。",
                        "observable_result": "理由欄能指出商品資料中的對應內容。",
                    }
                ],
            },
            "guided_practice": {
                "purpose": "沿用示範的判斷順序，完成另一項渠道選擇。",
                "start_state": "你已有相同商品資料，但尚未處理午間試吃活動。",
                "steps": [
                    {
                        "purpose": "確認午間活動真正能接觸的對象。",
                        "start_state": "渠道欄仍沿用示範的通勤情境。",
                        "action": "根據活動時間改寫受眾需求，再選一個可執行渠道。",
                        "expected_result": "新渠道的理由反映午間時段，而非複製示範答案。",
                    }
                ],
                "checks": [
                    {
                        "expected_result": "理由能同時指出時段、對象與商品特色。",
                        "recovery_ref": "recovery-missing-reason",
                    }
                ],
                "recovery_refs": ["recovery-missing-reason"],
            },
            "independent_practice": {
                "context": "改為替需要冷藏的點心規劃校園活動。",
                "changed_conditions": ["保存限制", "接觸對象", "活動地點"],
                "decision_required": "重新判斷哪些渠道能維持冷藏並接觸學生。",
                "deliverable": "一份可供校園合作窗口審核的活動企劃。",
                "acceptance_criteria": [
                    "渠道符合冷藏限制",
                    "企劃保留選擇與排除渠道的理由",
                ],
                "verification": "用商品限制逐項核對渠道理由與活動流程。",
            },
            "checks": [
                {
                    "id": "check-plan",
                    "target": "新品活動企劃",
                    "expected_result": "企劃包含受眾、渠道、理由與兩項驗收結果。",
                    "on_failure": "回到受眾需求，再檢查渠道是否有資料依據。",
                }
            ],
            "recovery": [
                {
                    "id": "recovery-missing-reason",
                    "symptom": "渠道欄有平台名稱，但理由欄無法連回商品資料。",
                    "cause": "先選平台，沒有先確認受眾使用情境。",
                    "action": "回到商品特色，補寫受眾在該情境下的具體需求。",
                    "expected_result": "渠道理由能指出一項商品特色與一項受眾需求。",
                }
            ],
            "transfer": {
                "new_context": "之後規劃不同商品時，仍先確認使用情境與限制。",
                "method": "用受眾需求連接商品特色，再選擇可執行渠道。",
                "limits": "法規、醫療或高風險宣稱仍需交由專業人員審查。",
            },
            "asset_references": ["asset-product-brief", "asset-demo-plan"],
            "editorial_evidence": {
                "reviewer_id": "course-copywriter-review-1",
                "source_sha256": "a" * 64,
                "continuity_passed": True,
                "learner_readable": True,
                "internal_labels_removed": True,
                "notes": "從情境、示範、跟做到獨立練習可連續閱讀。",
            },
        }

    def ready_contract(self):
        contract = new_contract(
            "marketing-practice",
            "行銷企劃實作",
            "課程團隊",
            "2026-10-18T12:00:00+08:00",
        )
        for gate_id in ("G0", "G1"):
            begin_gate(contract, gate_id, "course-run", "2026-10-18T12:05:00+08:00")
            evidence_id = f"{gate_id.lower()}-evidence"
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
                contract,
                gate_id,
                [evidence_id],
                f"{gate_id.lower()}-validator",
                "course-run",
                "2026-10-18T12:10:00+08:00",
            )
        begin_gate(contract, "G2", "course-run", "2026-10-18T12:05:00+08:00")
        lesson = self.valid_record()
        blueprint = {
            "criteria": [
                {"id": "criterion-plan", "outcome_id": "outcome-plan", "capability_id": "capability-plan"}
            ],
            "units": [
                {
                    "id": "unit-1",
                    "outcome_ids": lesson["outcome_ids"],
                    "criterion_ids": lesson["criterion_ids"],
                    "capability_ids": lesson["capability_ids"],
                }
            ],
        }
        contract["G2_architecture"] = blueprint
        reference = materialize_json_evidence(
            self.temporary.name,
            evidence_id="g2-blueprint",
            gate_id="G2",
            kind="course_blueprint",
            relative_path="evidence/g2-blueprint.json",
            value=blueprint,
        )
        contract["evidence_index"].append(reference)
        _commit_gate_pass(
            contract, "G2", ["g2-blueprint"], "g2-validator", "course-run",
            "2026-10-18T12:10:00+08:00",
        )
        begin_gate(contract, "G3", "course-run", "2026-10-18T12:15:00+08:00")
        return contract

    def test_complete_lesson_record_can_pass_g3(self):
        contract = self.ready_contract()

        status = route_content_to_g3(
            contract,
            self.valid_record(),
            "evidence/unit-1.json",
            "b" * 64,
            "course-designer",
            "2026-10-18T13:00:00+08:00",
            workspace_root=self.temporary.name,
        )

        self.assertEqual(status, "PASS")
        self.assertEqual(contract["gates"]["G3"]["status"], "PASS")

    def test_instruction_requires_purpose_start_action_and_expected_result(self):
        for field in ("purpose", "start_state", "action", "expected_result"):
            with self.subTest(field=field):
                record = self.valid_record()
                del record["guided_practice"]["steps"][0][field]
                issues = validate_lesson_record(record)
                self.assertIn("incomplete_instruction", {item.code for item in issues})

    def test_demo_requires_input_reason_action_result_and_verification(self):
        sections = ("input", "rationale", "actions", "result", "verification")
        for section in sections:
            with self.subTest(section=section):
                record = self.valid_record()
                record["full_demonstration"][section] = [] if section.endswith("s") else None
                issues = validate_lesson_record(record)
                self.assertIn("incomplete_demonstration", {item.code for item in issues})

    def test_solo_task_requires_changed_context_and_real_deliverable(self):
        record = self.valid_record()
        record["independent_practice"]["changed_conditions"] = []
        record["independent_practice"]["deliverable"] = ""

        codes = {item.code for item in validate_lesson_record(record)}

        self.assertIn("independent_transfer_required", codes)
        self.assertIn("independent_deliverable_required", codes)

    def test_missing_recovery_or_asset_reference_blocks_g3(self):
        for field in ("recovery", "asset_references"):
            with self.subTest(field=field):
                contract = self.ready_contract()
                record = self.valid_record()
                record[field] = []

                status = route_content_to_g3(
                    contract,
                    record,
                    "evidence/unit-1.json",
                    "b" * 64,
                    "course-designer",
                    "2026-10-18T13:00:00+08:00",
                    workspace_root=self.temporary.name,
                )

                self.assertEqual(status, "BLOCKED")
                self.assertEqual(contract["gates"]["G3"]["status"], "IN_PROGRESS")

    def test_placeholder_internal_filename_and_checklist_prose_fail_editorial_gate(self):
        cases = (
            ("TODO：之後補完整說明", "placeholder_prose"),
            ("請開啟 CH1-1.md 再開始。", "internal_filename"),
            ("- 開啟工具\n- 上傳檔案\n- 匯出結果", "editorial_evidence_failed"),
        )
        for prose, expected in cases:
            with self.subTest(expected=expected):
                record = self.valid_record()
                record["explanation"]["prose"] = prose
                if expected == "editorial_evidence_failed":
                    record["editorial_evidence"]["continuity_passed"] = False
                codes = {item.code for item in validate_lesson_record(record)}
                self.assertIn(expected, codes)

    def test_readable_continuous_prose_is_not_rewritten_by_validator(self):
        record = self.valid_record()
        before = copy.deepcopy(record)

        issues = validate_lesson_record(record)

        self.assertEqual(issues, [])
        self.assertEqual(record, before)

    def test_lesson_requires_stable_outcome_criterion_and_capability_coverage(self):
        for field in ("outcome_ids", "criterion_ids", "capability_ids", "learning_coverage"):
            with self.subTest(field=field):
                record = self.valid_record()
                record[field] = []
                codes = {item.code for item in validate_lesson_record(record)}
                self.assertIn("learning_coverage_required", codes)

    def test_lesson_rejects_duplicate_or_incomplete_child_capability_coverage(self):
        record = self.valid_record()
        record["learning_coverage"].append(copy.deepcopy(record["learning_coverage"][0]))
        record["learning_coverage"][0]["practice_evidence"] = []

        codes = {item.code for item in validate_lesson_record(record)}

        self.assertIn("duplicate_learning_coverage", codes)
        self.assertIn("incomplete_learning_coverage", codes)

    def test_lesson_coverage_rejects_fake_atom_ids(self):
        record = self.valid_record()
        record["learning_coverage"][0]["teaching_evidence"] = ["fake"]
        self.assertIn("unknown_lesson_evidence", {issue.code for issue in validate_lesson_record(record)})

    def test_lesson_runtime_rejects_schema_closed_shape_bypass(self):
        record = self.valid_record()
        record["producer_validation"] = {"status": "PASS"}
        record["full_demonstration"]["alternate_paths"] = ["skip validation"]
        self.assertIn(
            "schema_additional_property",
            {issue.code for issue in validate_lesson_record(record)},
        )

    def test_g3_does_not_pass_with_one_of_two_governed_lessons(self):
        contract = self.ready_contract()
        blueprint = copy.deepcopy(contract["G2_architecture"])
        second = copy.deepcopy(blueprint["units"][0])
        second["id"] = "unit-2"
        blueprint["units"].append(second)
        reference = materialize_json_evidence(
            self.temporary.name, evidence_id="g2-blueprint-two", gate_id="G2",
            kind="course_blueprint", relative_path="evidence/g2-blueprint-two.json", value=blueprint,
        )
        contract["evidence_index"].append(reference)
        contract["G2_architecture"] = blueprint
        event = contract["gates"]["G2"]["evidence"][-1]
        event["evidence_ids"] = [reference["id"]]
        event["consumed_evidence_ids"] = [reference["id"]]
        event["consumed_evidence"] = [{field: reference[field] for field in ("id", "gate", "kind", "path", "sha256")}]
        before = copy.deepcopy(contract)
        status = route_content_to_g3(
            contract, self.valid_record(), "evidence/unit-1.json", "b" * 64,
            "course-designer", "2026-10-18T13:00:00+08:00",
            workspace_root=self.temporary.name,
        )
        self.assertEqual(status, "BLOCKED")
        self.assertEqual(contract, before)
        second_record = self.valid_record()
        second_record["unit_id"] = "unit-2"
        status = route_content_to_g3(
            contract, [self.valid_record(), second_record],
            ["evidence/unit-1.json", "evidence/unit-2.json"], ["b" * 64, "c" * 64],
            "course-designer", "2026-10-18T13:01:00+08:00",
            workspace_root=self.temporary.name,
        )
        self.assertEqual(status, "PASS")

    def test_lesson_coverage_rows_must_preserve_blueprint_criterion_pairs(self):
        record = self.valid_record()
        record["outcome_ids"].append("outcome-audit")
        record["criterion_ids"].append("criterion-audit")
        record["capability_ids"].append("capability-audit")
        record["learning_coverage"].append(
            {
                "outcome_id": "outcome-audit",
                "criterion_id": "criterion-audit",
                "capability_id": "capability-audit",
                "teaching_evidence": ["示範如何稽核企劃。"],
                "practice_evidence": ["以不同企劃完成獨立稽核。"],
                "assessment_evidence": ["保存逐項稽核結果。"],
            }
        )
        blueprint = {
            "criteria": [
                {"id": "criterion-plan", "outcome_id": "outcome-plan", "capability_id": "capability-plan"},
                {"id": "criterion-audit", "outcome_id": "outcome-audit", "capability_id": "capability-audit"},
            ],
            "units": [
                {
                    "id": "unit-1",
                    "outcome_ids": list(record["outcome_ids"]),
                    "criterion_ids": list(record["criterion_ids"]),
                    "capability_ids": list(record["capability_ids"]),
                }
            ],
        }
        record["learning_coverage"][0]["outcome_id"] = "outcome-audit"
        record["learning_coverage"][1]["outcome_id"] = "outcome-plan"

        codes = {issue.code for issue in validate_lesson_record(record, blueprint)}

        self.assertIn("blueprint_learning_mismatch", codes)

    def test_lesson_schema_required_fields_match_runtime(self):
        schema = json.loads(
            (Path(__file__).parents[1] / "contracts" / "course-lesson-record.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(schema["required"]), set(REQUIRED_SECTIONS))


if __name__ == "__main__":
    unittest.main()
