import copy
import json
import tempfile
import unittest
from pathlib import Path

from src.course_contract import begin_gate, new_contract
from src.course_evidence import materialize_json_evidence
from src.course_requirements import (
    REQUIREMENTS_REQUIRED_FIELDS,
    validate_requirements_record,
)
from src.course_requirements_routes import route_requirements_to_g0


class CourseRequirementsTests(unittest.TestCase):
    def valid_record(self):
        return {
            "schema_version": 1,
            "requirements_id": "campaign-brief-requirements",
            "target_profile": {
                "id": "junior-marketer",
                "learner": "第一次獨立整理付費廣告成效的行銷專員。",
                "baseline": "能讀取試算表欄位，也能完成基本加減乘除。",
                "prerequisites": ["能下載課程提供的 CSV，並以試算表開啟。"],
            },
            "work_context": {
                "situation": "每週例會前，需要把三個活動的成效整理給行銷主管。",
                "problem": "目前只有平台匯出的原始數字，主管無法判斷哪個活動需要調整。",
                "use": "完成品會作為例會中的預算調整依據。",
            },
            "final_artifact": {
                "name": "活動成效決策簡報",
                "format": "一份包含指標表與建議的 Markdown 簡報",
                "observable_result": "學員能獨立算出指標、指出未達標活動，並提出可驗證的下一步。",
                "use": "交給行銷主管審核下一週的預算調整。",
            },
            "delivery": {
                "mode": "三小時同步工作坊，課後可重做相同素材。",
                "available_minutes": 180,
                "break_buffer_policy": "單元之間保留十分鐘休息，結尾保留十分鐘處理操作落差。",
            },
            "environment": {
                "tools": ["可編輯公式並匯出檔案的試算表工具。"],
                "accounts": ["課程素材不需登入；學員以既有試算表帳號操作。"],
                "permissions": ["學員具有下載、編輯及另存課程素材的權限。"],
                "device": "可同時檢視教材與試算表的筆記型電腦。",
                "locale": "繁體中文介面、Asia/Taipei 時區與新臺幣金額。",
            },
            "constraints": [
                {
                    "id": "constraint-no-live-data",
                    "description": "課程只使用去識別化資料，不登入真實廣告帳號。",
                    "impact": "示範與評量都必須使用可下載的固定資料集。",
                }
            ],
            "acceptance_criteria": [
                {
                    "id": "criterion-decision-brief",
                    "statement": "簡報能支持主管判斷活動表現與下一步。",
                    "capabilities": [
                        {
                            "id": "capability-calculate",
                            "statement": "根據原始欄位正確計算 CTR、CPC、CPA 與 ROAS。",
                        },
                        {
                            "id": "capability-recommend",
                            "statement": "根據門檻指出未達標活動並提出可觀察的後續測試。",
                        },
                    ],
                }
            ],
            "known_facts": ["練習資料固定包含曝光、點擊、花費、轉換與營收欄位。"],
            "assumptions": [
                {
                    "id": "assumption-formulas",
                    "statement": "學員可依畫面提示輸入基本除法公式。",
                    "material": False,
                    "validation_plan": "開場以一題公式輸入檢查確認。",
                }
            ],
            "unknowns": [
                {
                    "id": "unknown-export",
                    "question": "學員使用的試算表版本是否能匯出 PDF？",
                    "material": False,
                    "impact_domains": ["non-core"],
                    "status": "RESOLVED",
                    "resolution": "已確認課程環境可匯出 PDF；Markdown 仍保留為教學內的恢復路徑。",
                    "fallback": None,
                }
            ],
            "decisions": [
                {
                    "id": "decision-fixed-data",
                    "decision": "使用固定的去識別化活動資料，不連接真實平台。",
                    "rationale": "可讓每位學員在相同欄位與門檻下完成可比較的成果。",
                }
            ],
        }

    def test_complete_contextual_requirements_are_valid(self):
        self.assertEqual(validate_requirements_record(self.valid_record()), [])

    def test_empty_or_generic_requirements_fail_semantic_validation(self):
        cases = (
            ("target_profile.learner", "一般學員"),
            ("work_context.problem", ""),
            ("final_artifact.observable_result", "完成課程"),
            ("environment.tools", ["任何工具"]),
            ("acceptance_criteria.0.capabilities.0.statement", "了解概念"),
        )
        for dotted_path, replacement in cases:
            with self.subTest(path=dotted_path):
                record = self.valid_record()
                target = record
                parts = dotted_path.split(".")
                for part in parts[:-1]:
                    target = target[int(part)] if part.isdigit() else target[part]
                target[parts[-1]] = replacement
                self.assertTrue(validate_requirements_record(record))

    def test_padded_generic_language_and_self_downgraded_material_unknown_fail(self):
        vague = self.valid_record()
        vague["target_profile"]["learner"] = "一般學員都可以參加這門課"
        self.assertIn(
            "vague_requirement",
            {issue.code for issue in validate_requirements_record(vague)},
        )

        unknown = self.valid_record()
        unknown["unknowns"][0] = {
            "id": "unknown-core-permission",
            "question": "學員是否具有完成最終成果所需工具的帳號與編輯權限？",
            "material": False,
            "impact_domains": ["tools", "accounts", "permissions", "artifact"],
            "status": "OPEN",
            "resolution": "課程開始後再詢問學員使用哪個帳號。",
            "fallback": None,
        }
        self.assertIn(
            "material_unknown",
            {issue.code for issue in validate_requirements_record(unknown)},
        )

    def test_open_material_unknown_blocks_g0(self):
        record = self.valid_record()
        record["unknowns"][0] = {
            "id": "unknown-required-account",
            "question": "學員能否登入完成核心任務所需的平台？",
            "material": True,
            "impact_domains": ["accounts", "permissions"],
            "status": "OPEN",
            "resolution": "尚未確認帳號與權限。",
            "fallback": None,
        }

        codes = {issue.code for issue in validate_requirements_record(record)}

        self.assertIn("material_unknown", codes)

    def test_materiality_is_derived_and_fallback_must_be_verified_structure(self):
        for fallback in ("use an alternative", {
            "description": "改用另一個工具完成核心成果。",
            "verification_status": "UNVERIFIED",
            "evidence_ref": "fallback-tool",
            "preserves_acceptance": True,
        }):
            with self.subTest(fallback=fallback):
                record = self.valid_record()
                record["unknowns"][0].update({
                    "material": False, "impact_domains": ["tools", "artifact"],
                    "status": "OPEN", "fallback": fallback,
                })
                self.assertIn(
                    "material_unknown",
                    {issue.code for issue in validate_requirements_record(record)},
                )

    def test_cross_field_duplicate_and_repeated_padding_are_rejected(self):
        repeated = "學員將使用固定資料完成一份主管可以逐項檢查的決策簡報。"
        record = self.valid_record()
        record["target_profile"]["learner"] = repeated
        record["work_context"]["situation"] = repeated
        self.assertIn("duplicate_requirement_text", {issue.code for issue in validate_requirements_record(record)})
        padded = self.valid_record()
        padded["work_context"]["problem"] = repeated + repeated
        self.assertIn("padded_requirement", {issue.code for issue in validate_requirements_record(padded)})

    def test_open_or_deferred_unknown_requires_governed_verified_fallback(self):
        for status in ("OPEN", "DEFERRED"):
            with self.subTest(status=status):
                record = self.valid_record()
                record["unknowns"][0].update({
                    "status": status,
                    "material": False,
                    "impact_domains": ["non-core"],
                    "fallback": None,
                })
                self.assertIn(
                    "unresolved_unknown",
                    {issue.code for issue in validate_requirements_record(record, known_support_evidence_ids=set())},
                )
        record = self.valid_record()
        record["unknowns"][0].update({
            "status": "OPEN",
            "fallback": {
                "description": "改交付可由同一 rubric 驗收的 Markdown 檔案。",
                "verification_status": "VERIFIED_FALLBACK",
                "evidence_ref": "g0-fallback-support",
                "preserves_acceptance": True,
            },
        })
        self.assertTrue(validate_requirements_record(record, known_support_evidence_ids=set()))
        self.assertEqual(validate_requirements_record(record, known_support_evidence_ids={"g0-fallback-support"}), [])

    def test_numbered_boilerplate_cannot_fill_distinct_requirement_fields(self):
        record = self.valid_record()
        stem = "學員使用固定資料完成主管可以逐項檢查的決策成果版本"
        record["target_profile"]["learner"] = stem + " 001"
        record["work_context"]["situation"] = stem + " 002"
        self.assertIn(
            "duplicate_requirement_text",
            {issue.code for issue in validate_requirements_record(record)},
        )

    def test_duplicate_stable_ids_are_rejected(self):
        record = self.valid_record()
        record["acceptance_criteria"][0]["capabilities"].append(
            copy.deepcopy(record["acceptance_criteria"][0]["capabilities"][0])
        )

        self.assertIn(
            "duplicate_id", {issue.code for issue in validate_requirements_record(record)}
        )

    def test_self_declared_pass_field_is_not_part_of_canonical_g0(self):
        record = self.valid_record()
        record["validation"] = {"status": "PASS", "validator_id": "producer"}

        self.assertIn(
            "unsupported_field",
            {issue.code for issue in validate_requirements_record(record)},
        )

    def test_schema_required_fields_match_runtime(self):
        schema = json.loads(
            (Path(__file__).parents[1] / "contracts" / "course-requirements-record.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(set(schema["required"]), set(REQUIREMENTS_REQUIRED_FIELDS))

    def test_g0_route_materializes_evidence_and_uses_central_dispatcher(self):
        contract = new_contract(
            "campaign-brief", "活動成效簡報", "course-run", "2026-10-18T09:00:00+08:00"
        )
        begin_gate(contract, "G0", "course-run", "2026-10-18T09:01:00+08:00")
        with tempfile.TemporaryDirectory() as temporary:
            status = route_requirements_to_g0(
                contract,
                self.valid_record(),
                "evidence/g0-requirements.json",
                "course-run",
                "2026-10-18T09:02:00+08:00",
                workspace_root=temporary,
            )

        self.assertEqual(status, "PASS")
        self.assertEqual(contract["gates"]["G0"]["evidence"][-1]["validator_id"], "course-requirements-validator")

    def test_g0_route_accepts_fallback_only_with_consumed_typed_support(self):
        contract = new_contract("fallback-course", "Fallback Course", "course-run", "2026-10-18T09:00:00+08:00")
        begin_gate(contract, "G0", "course-run", "2026-10-18T09:01:00+08:00")
        record = self.valid_record()
        record["unknowns"][0].update({
            "status": "OPEN",
            "fallback": {
                "description": "改交付可由同一 rubric 驗收的 Markdown 檔案。",
                "verification_status": "VERIFIED_FALLBACK",
                "evidence_ref": "g0-fallback-support",
                "preserves_acceptance": True,
            },
        })
        with tempfile.TemporaryDirectory() as temporary:
            support = materialize_json_evidence(
                temporary, evidence_id="g0-fallback-support", gate_id="G0",
                kind="requirements_support", relative_path="evidence/fallback-support.json",
                value={"result": "PASS", "fallback": "Markdown export"},
            )
            contract["evidence_index"].append(support)
            status = route_requirements_to_g0(
                contract, record, "evidence/g0-requirements.json", "course-run",
                "2026-10-18T09:02:00+08:00", workspace_root=temporary,
                support_evidence_ids=[support["id"]],
            )
        self.assertEqual(status, "PASS")


if __name__ == "__main__":
    unittest.main()
