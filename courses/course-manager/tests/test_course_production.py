import copy
import hashlib
import unittest

from src.course_contract import ContractStateError, begin_gate, new_contract, pass_gate
from src.course_production import (
    route_full_production_to_g5,
    select_pilot_unit,
    validate_asset_manifest,
    validate_full_production,
    validate_pilot_record,
)


class CourseProductionTests(unittest.TestCase):
    def valid_asset_manifest(self):
        return {
            "schema_version": 1,
            "assets": [
                {
                    "id": "asset-product-brief",
                    "learner_label": "商品資料簡報",
                    "purpose": "提供示範與練習所需的商品特色、預算與日期。",
                    "source": {
                        "type": "course-created",
                        "uri": "assets/product-brief.pdf",
                        "retrieved_at": "2026-10-18",
                    },
                    "rights": {
                        "status": "CLEARED",
                        "basis": "課程團隊以去識別化資料製作。",
                    },
                    "version": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    "access": {
                        "method": "download",
                        "learner_path": "單元第一段的下載連結",
                        "backup": "頁面同時提供可複製的純文字資料。",
                    },
                    "open_test": {
                        "tested_at": "2026-10-18T14:00:00+08:00",
                        "actor": "build-course-page",
                        "result": "PASS",
                        "sha256": "a" * 64,
                    },
                },
                {
                    "id": "asset-demo-plan",
                    "learner_label": "完成企劃範例",
                    "purpose": "讓學員在操作前看到可驗收的完整成果。",
                    "source": {
                        "type": "course-created",
                        "uri": "assets/demo-plan.pdf",
                        "retrieved_at": "2026-10-18",
                    },
                    "rights": {
                        "status": "CLEARED",
                        "basis": "課程團隊自行製作。",
                    },
                    "version": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                    "access": {
                        "method": "download",
                        "learner_path": "完整示範結果旁的下載連結",
                        "backup": "頁面保留完整表格。",
                    },
                    "open_test": {
                        "tested_at": "2026-10-18T14:05:00+08:00",
                        "actor": "build-course-page",
                        "result": "PASS",
                        "sha256": "b" * 64,
                    },
                },
            ],
        }

    def valid_visual_decision(self):
        return {
            "inputs": {
                "topic": "行銷企劃實作",
                "learner": "第一次獨立提案的行銷同仁",
                "task": "邊讀資料邊完成可交付企劃",
                "content_density": "高密度表格與逐步判斷並存",
                "primary_devices": ["mobile", "tablet", "desktop"],
            },
            "decisions": {
                "layout_rationale": "正文維持單欄，寬表格使用局部水平捲動。",
                "navigation": "固定顯示單元進度與上一個已完成結果。",
                "typography": "內文以清楚的繁體中文字級與行距為主。",
                "color": "用高對比主色標記檢查與修復，不以顏色單獨傳意。",
                "responsive_strategy": "手機改為單欄，操作與預期結果保持相鄰。",
            },
        }

    def valid_pilot(self):
        return {
            "schema_version": 1,
            "unit_id": "unit-1",
            "lesson_sha256": "c" * 64,
            "html_path": "courses/marketing-practice/unit-1.html",
            "html_sha256": "d" * 64,
            "asset_ids": ["asset-product-brief", "asset-demo-plan"],
            "visual_decision": self.valid_visual_decision(),
            "content_fidelity": {
                "source_sha256": "c" * 64,
                "rendered_source_sha256": "c" * 64,
                "teaching_atoms": [
                    "learner_outcome",
                    "full_demonstration",
                    "guided_practice",
                    "independent_practice",
                    "recovery",
                ],
                "result": "PASS",
            },
            "render": {
                "browser": "Chromium 141",
                "tested_at": "2026-10-18T15:00:00+08:00",
                "screenshots": [
                    "evidence/unit-1-desktop.png",
                    "evidence/unit-1-mobile.png",
                ],
                "result": "PASS",
            },
            "devices": {
                "mobile": {
                    "viewport": "390x844",
                    "core_path_result": "PASS",
                    "horizontal_overflow": False,
                },
                "tablet": {
                    "viewport": "820x1180",
                    "core_path_result": "PASS",
                    "horizontal_overflow": False,
                },
                "desktop": {
                    "viewport": "1440x900",
                    "core_path_result": "PASS",
                    "horizontal_overflow": False,
                },
            },
            "accessibility": {
                "automated": {
                    "tool": "axe-core",
                    "result": "PASS",
                    "report_path": "evidence/axe.json",
                },
                "manual": {
                    "evaluator_id": "accessibility-review-1",
                    "keyboard_result": "PASS",
                    "focus_result": "PASS",
                    "reading_sequence_result": "PASS",
                    "notes": "從 skip link 到完成檢核可依序操作。",
                },
            },
            "navigation": {
                "entry": "course index",
                "previous": "course index",
                "next": "next unit placeholder",
            },
        }

    def lesson_record(self):
        return {
            "unit_id": "unit-1",
            "asset_references": ["asset-product-brief", "asset-demo-plan"],
        }

    def full_blueprint(self):
        return {
            "units": [
                {
                    "id": "unit-1",
                    "outcome": "從商品資料找出企劃限制與可用證據。",
                    "workflow_fingerprint": "extract-source-constraints",
                    "depends_on": [],
                    "asset_ids": ["asset-product-brief"],
                },
                {
                    "id": "unit-2",
                    "outcome": "依限制完成可交付的行銷企劃初稿。",
                    "workflow_fingerprint": "build-plan-from-constraints",
                    "depends_on": ["unit-1"],
                    "asset_ids": ["asset-demo-plan"],
                },
                {
                    "id": "unit-3",
                    "outcome": "依驗收條件檢查並修訂完整企劃。",
                    "workflow_fingerprint": "audit-plan-against-criteria",
                    "depends_on": ["unit-2"],
                    "asset_ids": ["asset-product-brief", "asset-demo-plan"],
                },
            ],
            "final_acceptance": {
                "outcome_id": "g0-marketing-plan",
                "criteria_ids": ["uses-source-facts", "complete-plan", "passes-audit"],
            },
        }

    def full_lessons(self):
        return [
            {
                "unit_id": unit["id"],
                "outcome": unit["outcome"],
                "workflow_fingerprint": unit["workflow_fingerprint"],
                "depends_on": list(unit["depends_on"]),
                "asset_references": list(unit["asset_ids"]),
            }
            for unit in self.full_blueprint()["units"]
        ]

    def full_trial(self):
        return {
            "schema_version": 1,
            "scope": "full_course",
            "participant": {
                "id": "full-course-cold-ai-01",
                "type": "independent-ai",
                "roles": ["learner-trial"],
            },
            "isolated_context_id": "full-course-run-20261018-01",
            "allowed_inputs": [
                {
                    "kind": "learner-page",
                    "path": "courses/demo/index.html",
                    "sha256": "1" * 64,
                },
                {
                    "kind": "learner-asset",
                    "path": "courses/demo/assets/product-brief.pdf",
                    "sha256": "2" * 64,
                },
            ],
            "forbidden_inputs_accessed": [],
            "entry": {
                "started_at": "2026-10-18T16:00:00+08:00",
                "page": "courses/demo/index.html",
                "goal_understood": True,
                "materials_found": True,
            },
            "actions": [
                {
                    "sequence": 1,
                    "action": "依序完成三個單元並保存每一階段產物。",
                    "observable_result": "完成資料摘錄、企劃初稿與修訂稿。",
                    "at": "2026-10-18T16:10:00+08:00",
                }
            ],
            "hints": [{"source": "none", "detail": "未使用額外提示。"}],
            "blocks": [],
            "recovery": [],
            "artifact": {
                "path": "trial-output/full-course-run/final-plan.pdf",
                "sha256": "3" * 64,
                "complete": True,
                "verifiable": True,
                "acceptance_result": "PASS",
            },
            "result": {
                "status": "PASS",
                "completed_at": "2026-10-18T17:00:00+08:00",
                "notes": "只使用學員可見頁面與素材完成全課。",
            },
        }

    def full_production(self):
        units = []
        blueprint_units = self.full_blueprint()["units"]
        for index, unit in enumerate(blueprint_units):
            units.append(
                {
                    "unit_id": unit["id"],
                    "lesson_sha256": str(index + 4) * 64,
                    "html_path": f"courses/demo/{unit['id']}.html",
                    "html_sha256": str(index + 7) * 64,
                    "asset_ids": list(unit["asset_ids"]),
                    "outcome": unit["outcome"],
                    "workflow_fingerprint": unit["workflow_fingerprint"],
                    "depends_on": list(unit["depends_on"]),
                    "previous": None if index == 0 else blueprint_units[index - 1]["id"],
                    "next": None if index == len(blueprint_units) - 1 else blueprint_units[index + 1]["id"],
                }
            )
        return {
            "schema_version": 1,
            "course_id": "marketing-practice",
            "production_authors": ["course-author-01", "page-builder-01"],
            "g4_trial_context_id": "pilot-cold-run-20261018-01",
            "units": units,
            "navigation": {
                "entry": "courses/demo/index.html",
                "order": [unit["id"] for unit in blueprint_units],
                "completion": "courses/demo/complete.html",
            },
            "dependency_checks": [
                {
                    "from_unit": "unit-1",
                    "to_unit": "unit-2",
                    "artifact": "evidence/source-constraints.json",
                    "result": "PASS",
                },
                {
                    "from_unit": "unit-2",
                    "to_unit": "unit-3",
                    "artifact": "evidence/plan-draft.pdf",
                    "result": "PASS",
                },
            ],
            "final_artifact": {
                "path": "courses/demo/examples/final-plan.pdf",
                "sha256": "f" * 64,
                "outcome_id": "g0-marketing-plan",
                "acceptance": [
                    {"criterion_id": "uses-source-facts", "result": "PASS", "evidence": "page 1"},
                    {"criterion_id": "complete-plan", "result": "PASS", "evidence": "pages 2-4"},
                    {"criterion_id": "passes-audit", "result": "PASS", "evidence": "audit report"},
                ],
            },
            "full_course_trial": self.full_trial(),
            "validation": {
                "status": "PASS",
                "validator_id": "course-validator",
                "validated_at": "2026-10-18T17:05:00+08:00",
            },
        }

    def test_pilot_selector_chooses_highest_combined_risk_then_dependency(self):
        blueprint = {
            "units": [
                {
                    "id": "intro",
                    "risk": {
                        "failure_cost": 2,
                        "tool_uncertainty": 1,
                        "asset_dependency": 1,
                        "layout_complexity": 1,
                        "downstream_dependency": 5,
                    },
                },
                {
                    "id": "integration",
                    "risk": {
                        "failure_cost": 4,
                        "tool_uncertainty": 4,
                        "asset_dependency": 3,
                        "layout_complexity": 5,
                        "downstream_dependency": 2,
                    },
                },
                {
                    "id": "integration-hub",
                    "risk": {
                        "failure_cost": 4,
                        "tool_uncertainty": 4,
                        "asset_dependency": 3,
                        "layout_complexity": 5,
                        "downstream_dependency": 6,
                    },
                },
            ]
        }

        self.assertEqual(select_pilot_unit(blueprint), "integration-hub")

    def test_asset_requires_purpose_source_rights_version_access_and_open_result(self):
        fields = ("purpose", "source", "rights", "version", "access", "open_test")
        for field in fields:
            with self.subTest(field=field):
                manifest = self.valid_asset_manifest()
                del manifest["assets"][0][field]
                codes = {item.code for item in validate_asset_manifest(manifest)}
                self.assertIn("incomplete_asset", codes)

    def test_visual_decision_uses_topic_learner_task_density_and_device(self):
        for field in ("topic", "learner", "task", "content_density", "primary_devices"):
            with self.subTest(field=field):
                pilot = self.valid_pilot()
                del pilot["visual_decision"]["inputs"][field]
                codes = {
                    item.code
                    for item in validate_pilot_record(
                        pilot, self.lesson_record(), self.valid_asset_manifest()
                    )
                }
                self.assertIn("incomplete_visual_decision", codes)

    def test_pilot_requires_content_fidelity_and_real_render_evidence(self):
        cases = (
            ("rendered_source_sha256", "e" * 64),
            ("teaching_atoms", []),
            ("result", "FAIL"),
        )
        for field, value in cases:
            with self.subTest(field=field):
                pilot = self.valid_pilot()
                pilot["content_fidelity"][field] = value
                codes = {
                    item.code
                    for item in validate_pilot_record(
                        pilot, self.lesson_record(), self.valid_asset_manifest()
                    )
                }
                self.assertIn("content_fidelity_failed", codes)

        pilot = self.valid_pilot()
        pilot["render"]["screenshots"] = []
        codes = {
            item.code
            for item in validate_pilot_record(
                pilot, self.lesson_record(), self.valid_asset_manifest()
            )
        }
        self.assertIn("render_evidence_required", codes)

    def test_pilot_requires_mobile_tablet_desktop_core_path_results(self):
        for device in ("mobile", "tablet", "desktop"):
            with self.subTest(device=device):
                pilot = self.valid_pilot()
                del pilot["devices"][device]
                codes = {
                    item.code
                    for item in validate_pilot_record(
                        pilot, self.lesson_record(), self.valid_asset_manifest()
                    )
                }
                self.assertIn("device_evidence_required", codes)

    def test_automated_accessibility_check_cannot_replace_manual_evaluation(self):
        pilot = self.valid_pilot()
        pilot["accessibility"]["manual"] = None

        codes = {
            item.code
            for item in validate_pilot_record(
                pilot, self.lesson_record(), self.valid_asset_manifest()
            )
        }

        self.assertIn("manual_accessibility_required", codes)

    def test_g5_cannot_begin_until_g4_passes(self):
        contract = new_contract(
            "marketing-practice",
            "行銷企劃實作",
            "課程團隊",
            "2026-10-18T12:00:00+08:00",
        )
        for gate_id in ("G0", "G1", "G2", "G3"):
            begin_gate(contract, gate_id, "course-run", "2026-10-18T12:05:00+08:00")
            evidence_id = f"{gate_id.lower()}-evidence"
            contract["evidence_index"].append(
                {
                    "id": evidence_id,
                    "gate": gate_id,
                    "path": f"evidence/{evidence_id}.json",
                    "sha256": hashlib.sha256(evidence_id.encode()).hexdigest(),
                }
            )
            pass_gate(
                contract,
                gate_id,
                [evidence_id],
                f"{gate_id.lower()}-validator",
                "course-run",
                "2026-10-18T12:10:00+08:00",
            )

        with self.assertRaises(ContractStateError):
            begin_gate(contract, "G5", "course-run", "2026-10-18T16:00:00+08:00")

    def test_full_production_requires_every_blueprint_unit_and_asset(self):
        production = self.full_production()
        production["units"].pop()
        codes = {
            issue.code
            for issue in validate_full_production(
                production,
                self.full_blueprint(),
                self.full_lessons(),
                self.valid_asset_manifest(),
                {"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"},
                self.full_trial(),
            )
        }
        self.assertIn("production_unit_coverage", codes)

        production = self.full_production()
        production["units"][1]["asset_ids"] = []
        codes = {
            issue.code
            for issue in validate_full_production(
                production,
                self.full_blueprint(),
                self.full_lessons(),
                self.valid_asset_manifest(),
                {"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"},
                self.full_trial(),
            )
        }
        self.assertIn("production_asset_coverage", codes)

    def test_units_with_duplicate_outcomes_and_workflows_fail_integration(self):
        production = self.full_production()
        production["units"][1]["outcome"] = production["units"][0]["outcome"]
        production["units"][1]["workflow_fingerprint"] = production["units"][0]["workflow_fingerprint"]

        issues = validate_full_production(
            production,
            self.full_blueprint(),
            self.full_lessons(),
            self.valid_asset_manifest(),
            {"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"},
            self.full_trial(),
        )

        self.assertIn("duplicate_unit_learning", {issue.code for issue in issues})

    def test_navigation_and_cross_unit_dependencies_are_complete(self):
        production = self.full_production()
        production["units"][1]["previous"] = None
        production["dependency_checks"].pop()

        codes = {
            issue.code
            for issue in validate_full_production(
                production,
                self.full_blueprint(),
                self.full_lessons(),
                self.valid_asset_manifest(),
                {"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"},
                self.full_trial(),
            )
        }

        self.assertIn("navigation_incomplete", codes)
        self.assertIn("dependency_continuity_failed", codes)

    def test_g5_passes_only_after_final_artifact_matches_g0_acceptance(self):
        production = self.full_production()
        production["final_artifact"]["outcome_id"] = "different-outcome"
        production["final_artifact"]["acceptance"].pop()

        codes = {
            issue.code
            for issue in validate_full_production(
                production,
                self.full_blueprint(),
                self.full_lessons(),
                self.valid_asset_manifest(),
                {"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"},
                self.full_trial(),
            )
        }

        self.assertIn("g0_acceptance_mismatch", codes)

    def test_full_production_route_passes_g5_with_indexed_evidence_and_trial(self):
        contract = new_contract(
            "marketing-practice",
            "行銷企劃實作",
            "course-run",
            "2026-10-18T12:00:00+08:00",
        )
        for gate_id in ("G0", "G1", "G2", "G3", "G4"):
            begin_gate(contract, gate_id, "course-run", "2026-10-18T12:05:00+08:00")
            evidence_id = f"{gate_id.lower()}-evidence"
            contract["evidence_index"].append(
                {
                    "id": evidence_id,
                    "gate": gate_id,
                    "path": f"evidence/{evidence_id}.json",
                    "sha256": hashlib.sha256(evidence_id.encode()).hexdigest(),
                }
            )
            pass_gate(
                contract,
                gate_id,
                [evidence_id],
                f"{gate_id.lower()}-validator",
                "course-run",
                "2026-10-18T12:10:00+08:00",
            )
        begin_gate(contract, "G5", "course-run", "2026-10-18T17:10:00+08:00")

        result = route_full_production_to_g5(
            contract,
            self.full_production(),
            [
                {
                    "id": "g5-render-and-integration",
                    "gate": "G5",
                    "path": "evidence/g5-render-and-integration.json",
                    "sha256": "a" * 64,
                }
            ],
            "course-run",
            "2026-10-18T17:15:00+08:00",
        )

        self.assertEqual(result, "PASS")
        self.assertEqual(contract["gates"]["G5"]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
