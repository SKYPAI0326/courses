import copy
import json
import tempfile
import unittest
from pathlib import Path

from src import course_requirements
from src.course_contract import begin_gate, new_contract
from src.course_evidence import materialize_json_evidence, register_evidence_file
from src.course_requirements import (
    REQUIREMENTS_REQUIRED_FIELDS,
    validate_requirements_record,
)
from src.course_requirements_routes import route_requirements_to_g0


def _required_free_prose_policy(schema, node=None, selector=()):
    node = schema if node is None else node
    reference = node.get("$ref")
    if reference == "#/$defs/text":
        return {selector: "required_text"}
    if reference == "#/$defs/textList":
        return {selector + ("*",): "required_text_list_item"}
    if reference is not None:
        definition = schema["$defs"][reference.rsplit("/", 1)[-1]]
        return _required_free_prose_policy(schema, definition, selector)

    policy = {}
    for field in node.get("required", []):
        property_schema = node.get("properties", {}).get(field)
        if property_schema is not None:
            policy.update(
                _required_free_prose_policy(schema, property_schema, selector + (field,))
            )
    if "items" in node:
        policy.update(_required_free_prose_policy(schema, node["items"], selector + ("*",)))
    return policy


def _replace_selector(record, selector, replacement):
    target = record
    rendered_path = "$"
    for segment in selector[:-1]:
        if segment == "*":
            target = target[0]
            rendered_path += "[0]"
        else:
            target = target[segment]
            rendered_path += f".{segment}"
    final = selector[-1]
    if final == "*":
        target[0] = replacement
        rendered_path += "[0]"
    else:
        target[final] = replacement
        rendered_path += f".{final}"
    return rendered_path


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
                    {issue.code for issue in validate_requirements_record(record, verified_support_records={})},
                )
        record = self.valid_record()
        record["unknowns"][0].update({
            "status": "OPEN",
            "fallback": {
                "fallback_id": "fallback-markdown-export",
                "description": "改交付可由同一 rubric 驗收的 Markdown 檔案。",
                "verification_status": "VERIFIED_FALLBACK",
                "evidence_ref": "g0-fallback-support",
                "acceptance_criterion_ids": ["criterion-decision-brief"],
                "preserves_acceptance": True,
            },
        })
        self.assertTrue(validate_requirements_record(record, verified_support_records={}))
        support = {
            "support_id": "g0-fallback-support",
            "requirements_id": record["requirements_id"],
            "unknown_id": record["unknowns"][0]["id"],
            "fallback_id": "fallback-markdown-export",
            "acceptance_criterion_ids": ["criterion-decision-brief"],
            "preserved_acceptance_ids": ["criterion-decision-brief"],
            "alternative_path": {"description": "改交付可由同一 rubric 驗收的 Markdown 檔案。"},
        }
        self.assertEqual(validate_requirements_record(record, verified_support_records={"g0-fallback-support": support}), [])
        for field, value in (
            ("unknown_id", "wrong-unknown"),
            ("fallback_id", "wrong-fallback"),
            ("acceptance_criterion_ids", ["unknown-criterion"]),
            ("preserved_acceptance_ids", []),
        ):
            with self.subTest(field=field):
                mismatched = copy.deepcopy(support)
                mismatched[field] = value
                self.assertIn(
                    "invalid_fallback",
                    {issue.code for issue in validate_requirements_record(
                        record, verified_support_records={"g0-fallback-support": mismatched}
                    )},
                )

    def test_numbered_boilerplate_cannot_fill_distinct_requirement_fields(self):
        record = self.valid_record()
        stem = "學員使用固定資料完成主管可以逐項檢查的決策成果版本"
        record["target_profile"]["learner"] = stem + " 001"
        record["work_context"]["situation"] = stem + " 002"
        self.assertIn(
            "duplicate_requirement_text",
            {issue.code for issue in validate_requirements_record(record)},
        )

    def test_numbered_boilerplate_cannot_fill_known_facts_list_items(self):
        record = self.valid_record()
        stem = "課程已確認固定資料包含每個驗收步驟需要的完整來源欄位版本"
        record["known_facts"] = [stem + " 001", stem + " 002"]

        issues = validate_requirements_record(record)

        self.assertIn("duplicate_requirement_text", {issue.code for issue in issues})

    def test_required_free_prose_policy_matches_schema_and_every_path_reaches_walker(self):
        schema = json.loads(
            (Path(__file__).parents[1] / "contracts" / "course-requirements-record.schema.json").read_text(
                encoding="utf-8"
            )
        )
        expected_policy = _required_free_prose_policy(schema)
        actual_policy = getattr(course_requirements, "REQUIREMENTS_PROSE_POLICY", {})
        self.assertEqual(actual_policy, expected_policy)
        self.assertNotIn(("unknowns", "*", "status"), actual_policy)
        self.assertNotIn(("unknowns", "*", "fallback", "verification_status"), actual_policy)

        padding = "這一段自由文案必須由需求驗證器辨識並拒絕重複填充內容"
        for selector in expected_policy:
            with self.subTest(selector=selector):
                record = self.valid_record()
                record["unknowns"][0]["fallback"] = {
                    "fallback_id": "fallback-markdown-export",
                    "description": "改交付可由同一 rubric 驗收的 Markdown 檔案。",
                    "verification_status": "VERIFIED_FALLBACK",
                    "evidence_ref": "g0-fallback-support",
                    "acceptance_criterion_ids": ["criterion-decision-brief"],
                    "preserves_acceptance": True,
                }
                expected_path = _replace_selector(record, selector, padding + padding)

                issues = validate_requirements_record(record)

                self.assertIn(
                    expected_path,
                    {issue.path for issue in issues if issue.code == "padded_requirement"},
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

    def test_g0_route_accepts_two_unknowns_with_two_independent_verified_support_chains(self):
        contract = new_contract("fallback-course", "Fallback Course", "course-run", "2026-10-18T09:00:00+08:00")
        begin_gate(contract, "G0", "course-run", "2026-10-18T09:01:00+08:00")
        record = self.valid_record()
        record["unknowns"] = []
        support_ids = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for number, label in ((1, "markdown"), (2, "html")):
                unknown_id = f"unknown-export-{number}"
                fallback_id = f"fallback-export-{number}"
                support_id = f"g0-fallback-support-{number}"
                artifact_id = f"g0-fallback-artifact-{number}"
                record["unknowns"].append({
                    "id": unknown_id,
                    "question": f"第 {number} 套環境能否輸出指定格式？",
                    "material": False,
                    "impact_domains": ["non-core"],
                    "status": "OPEN",
                    "resolution": f"已實測 {label} 替代路徑並保留全部驗收條件。",
                    "fallback": {
                        "fallback_id": fallback_id,
                        "description": f"改用 {label} 格式完成相同交付內容。",
                        "verification_status": "VERIFIED_FALLBACK",
                        "evidence_ref": support_id,
                        "acceptance_criterion_ids": ["criterion-decision-brief"],
                        "preserves_acceptance": True,
                    },
                })
                artifact_path = root / "evidence" / f"fallback-{number}.txt"
                artifact_path.parent.mkdir(parents=True, exist_ok=True)
                artifact_path.write_text(f"verified {label} artifact\n", encoding="utf-8")
                artifact = register_evidence_file(
                    root, evidence_id=artifact_id, gate_id="G0",
                    kind="requirements_support_artifact",
                    relative_path=f"evidence/fallback-{number}.txt",
                )
                support_value = {
                    "schema_version": 1, "support_id": support_id,
                    "requirements_id": record["requirements_id"],
                    "unknown_id": unknown_id, "fallback_id": fallback_id,
                    "acceptance_criterion_ids": ["criterion-decision-brief"],
                    "alternative_path": {
                        "description": f"改用 {label} 格式完成相同交付內容。",
                        "steps": [f"依課程範本完成 {label} 檔並另存。"],
                        "expected_result": "交付物保留指標表、判讀與後續測試。",
                    },
                    "verification": {
                        "executed": True, "verifier_id": f"validator-{number}",
                        "verified_at": f"2026-10-18T09:0{number}:30+08:00",
                        "environment": f"隔離測試環境 {number}，繁體中文介面。",
                        "method": f"由空白範本完整執行 {label} 替代路徑。",
                        "observed_result": "成品可開啟且全部驗收欄位有結果。",
                    },
                    "preserved_acceptance_ids": ["criterion-decision-brief"],
                    "artifacts": [{"evidence_id": artifact_id, "sha256": artifact["sha256"]}],
                }
                support = materialize_json_evidence(
                    root, evidence_id=support_id, gate_id="G0", kind="requirements_support",
                    relative_path=f"evidence/support-{number}.json", value=support_value,
                )
                contract["evidence_index"].extend([artifact, support])
                support_ids.extend([support_id, artifact_id])
            status = route_requirements_to_g0(
                contract, record, "evidence/g0-requirements.json", "course-run",
                "2026-10-18T09:02:00+08:00", workspace_root=temporary,
                support_evidence_ids=support_ids,
            )
        self.assertEqual(status, "PASS")

    def test_g0_dispatcher_rejects_empty_self_declared_support(self):
        contract = new_contract("fallback-course", "Fallback Course", "course-run", "2026-10-18T09:00:00+08:00")
        begin_gate(contract, "G0", "course-run", "2026-10-18T09:01:00+08:00")
        record = self.valid_record()
        record["unknowns"][0].update({
            "status": "OPEN",
            "fallback": {
                "fallback_id": "fallback-markdown-export",
                "description": "改交付可由同一 rubric 驗收的 Markdown 檔案。",
                "verification_status": "VERIFIED_FALLBACK",
                "evidence_ref": "g0-empty-support",
                "acceptance_criterion_ids": ["criterion-decision-brief"],
                "preserves_acceptance": True,
            },
        })
        with tempfile.TemporaryDirectory() as temporary:
            support = materialize_json_evidence(
                temporary, evidence_id="g0-empty-support", gate_id="G0",
                kind="requirements_support", relative_path="evidence/empty-support.json",
                value={},
            )
            contract["evidence_index"].append(support)
            status = route_requirements_to_g0(
                contract, record, "evidence/g0-requirements.json", "course-run",
                "2026-10-18T09:02:00+08:00", workspace_root=temporary,
                support_evidence_ids=[support["id"]],
            )
        self.assertEqual(status, "BLOCKED")


if __name__ == "__main__":
    unittest.main()
