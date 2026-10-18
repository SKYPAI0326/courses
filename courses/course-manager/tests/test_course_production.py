import hashlib
import unittest

from src.course_contract import ContractStateError, begin_gate, new_contract, pass_gate
from src.course_production import (
    select_pilot_unit,
    validate_asset_manifest,
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


if __name__ == "__main__":
    unittest.main()
