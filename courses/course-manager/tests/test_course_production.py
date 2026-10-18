import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.course_contract import ContractStateError, begin_gate, new_contract
from tests.gate_test_support import _commit_gate_pass
from src.course_evidence import canonical_json_bytes, materialize_json_evidence, register_evidence_file, verify_evidence_reference
from src.course_production import (
    PRODUCTION_COVERAGE_FIELD,
    PRODUCTION_UNIT_STABLE_FIELDS,
    select_pilot_unit,
    validate_asset_manifest,
    validate_full_production,
    validate_pilot_record,
)
from src.course_production_routes import route_full_production_to_g5
from src.course_validation import trial_action_id
from tests.runner_authority_fixture import TestRunnerAuthority


class CourseProductionTests(unittest.TestCase):
    def setUp(self):
        self.authority_id = "test-independent-lab"
        self.authority = TestRunnerAuthority(
            self.authority_id,
            {
                "full-course-cold-ai-01": {
                    "role": "isolated-learner-runner",
                    "sessions": {
                        "full-course-session-20261018-01": {
                            "assertion_id": "assertion-full-course-session-01",
                            "context_id": "full-course-run-20261018-01",
                        }
                    },
                }
            },
        )

    def g5_artifact_refs(self, root, production, lessons, assets):
        refs = []

        def write(path, data):
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            return hashlib.sha256(data).hexdigest()

        for unit, lesson in zip(production["units"], lessons):
            unit_id = unit["unit_id"]
            lesson_path = f"lessons/{unit_id}.json"
            unit["lesson_sha256"] = write(lesson_path, repr(lesson).encode())
            refs.append({"id": f"g5-lesson-{unit_id}", "kind": "lesson_source", "path": lesson_path, "metadata": {"unit_id": unit_id}})
            unit["html_sha256"] = write(unit["html_path"], f"<html>{unit_id}</html>".encode())
            refs.append({"id": f"g5-page-{unit_id}", "kind": "learner_page", "path": unit["html_path"], "metadata": {"unit_id": unit_id}})

        for asset in assets["assets"]:
            path = asset["source"]["uri"]
            digest = write(path, f"asset:{asset['id']}".encode())
            asset["open_test"]["sha256"] = digest
            asset["version"] = f"sha256:{digest}"
            refs.append({"id": f"g5-asset-{asset['id']}", "kind": "course_asset", "path": path, "metadata": {"asset_id": asset["id"]}})

        for index, check in enumerate(production["dependency_checks"]):
            write(check["artifact"], f"dependency:{index}".encode())
            refs.append({"id": f"g5-dependency-{index}", "kind": "dependency_artifact", "path": check["artifact"], "metadata": {"dependency": f"{check['from_unit']}->{check['to_unit']}"}})

        for role in ("entry", "completion"):
            path = production["navigation"][role]
            write(path, f"navigation:{role}".encode())
            refs.append({"id": f"g5-navigation-{role}", "kind": "navigation_artifact", "path": path, "metadata": {"role": role}})

        final = production["final_artifact"]
        final["sha256"] = write(final["path"], b"final course artifact")
        refs.append({"id": "g5-final-artifact", "kind": "final_artifact", "path": final["path"], "metadata": {"role": "final"}})
        pages = [
            {"id": "course-entry", "path": production["navigation"]["entry"]},
            *[
                {"id": unit["unit_id"], "path": unit["html_path"]}
                for unit in production["units"]
            ],
            {"id": "course-completion", "path": production["navigation"]["completion"]},
        ]
        _, accessibility_ref, production["accessibility_report"] = (
            self.materialize_accessibility_report(
                root, "G5", pages, "accessibility-g5-full-course"
            )
        )
        refs.append({
            "id": accessibility_ref["id"],
            "kind": accessibility_ref["kind"],
            "path": accessibility_ref["path"],
        })
        return refs

    def basic_accessibility_report(self, gate_scope, pages, report_id):
        return {
            "schema_version": 1,
            "report_id": report_id,
            "gate_scope": gate_scope,
            "coverage_scope": "representative_page" if gate_scope == "G4" else "full_course",
            "claim": {
                "scope": "basic_accessibility_smoke",
                "standard": "COURSE_ACCESSIBILITY_SMOKE",
                "version": "1.0",
                "level": "basic",
            },
            "pages": copy.deepcopy(pages),
            "applicable_criteria": [
                {"criterion_id": item, "level": "basic"}
                for item in ("keyboard", "focus", "reading-order", "horizontal-overflow")
            ],
            "automated_checks": [{
                "check_id": f"automated-overflow-{page['id']}",
                "method": "automated",
                "tool": "Playwright",
                "tool_version": "1.56.1",
                "user_agent": "Chromium 141",
                "page_id": page["id"], "criterion_id": "horizontal-overflow",
                "status": "PASS", "evidence": "No horizontal page overflow at tested viewports.",
            } for page in pages],
            "manual_checks": [{
                "check_id": f"manual-{item}-{page['id']}",
                "method": "manual",
                "evaluator_id": "accessibility-review-1",
                "method_description": "Keyboard traversal, focus inspection, and reading-order review.",
                "user_agent": "Safari 20",
                "assistive_technology": ["VoiceOver 17"],
                "page_id": page["id"], "criterion_id": item, "status": "PASS",
                "evidence": f"Observed {item} on {page['id']}.",
            } for page in pages for item in ("keyboard", "focus", "reading-order")],
            "findings": [],
        }

    def materialize_accessibility_report(self, root, gate_scope, pages, report_id):
        report = self.basic_accessibility_report(gate_scope, pages, report_id)
        ref = materialize_json_evidence(
            root,
            evidence_id=report_id,
            gate_id=gate_scope,
            kind="accessibility_report",
            relative_path=f"evidence/{report_id}.json",
            value=report,
        )
        declared = {
            "evidence_id": ref["id"],
            "path": ref["path"],
            "sha256": ref["sha256"],
            "claim_scope": report["claim"]["scope"],
        }
        return report, ref, declared

    def bind_trial_inputs(self, root, trial, production=None):
        for index, item in enumerate(trial["allowed_inputs"]):
            target = root / item["path"]
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(f"learner-visible input {index}\n".encode())
            item["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
        next(item for item in trial["evidence_bindings"] if item["role"] == "held-out-input")["sha256"] = trial["allowed_inputs"][0]["sha256"]
        refs = []
        gate_id = "G4" if trial["scope"] == "representative_unit" else "G5"
        for binding in trial["evidence_bindings"]:
            target = root / binding["path"]
            if binding["role"] != "held-out-input":
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(f"{binding['role']}:{binding['evidence_id']}\n".encode())
            ref = register_evidence_file(
                root, evidence_id=binding["evidence_id"], gate_id=gate_id,
                kind="trial_transfer_artifact", relative_path=binding["path"],
                metadata={"role": binding["role"]},
            )
            binding["sha256"] = ref["sha256"]
            refs.append({"id": ref["id"], "kind": ref["kind"], "path": ref["path"], "metadata": ref["metadata"]})
        by_id = {item["evidence_id"]: item for item in trial["evidence_bindings"]}
        for action in trial["actions"]:
            action["observable_result"]["actual_sha256"] = by_id[action["output_evidence_id"]]["sha256"]
            action["id"] = trial_action_id(action)
        for row, action in zip(trial["criterion_evidence"], trial["actions"]):
            row["action_id"] = action["id"]
        if production is not None:
            for row, action in zip(production["learning_coverage"], trial["actions"]):
                row["trial_evidence_id"] = action["id"]
        final = next(item for item in trial["evidence_bindings"] if item["role"] == "held-out-output")
        trial["artifact"]["path"] = final["path"]
        trial["artifact"]["sha256"] = final["sha256"]
        return refs

    def bind_governed_course(self, root, contract, blueprint, lessons):
        requirements = self.full_requirements()
        values = {
            "G0": [("governed-requirements", "requirements_record", requirements)],
            "G2": [("governed-blueprint", "course_blueprint", blueprint)],
            "G3": [
                (f"governed-lesson-{lesson['unit_id']}", "lesson_record", lesson)
                for lesson in lessons
            ],
        }
        for gate_id, entries in values.items():
            refs = [
                materialize_json_evidence(
                    root, evidence_id=evidence_id, gate_id=gate_id, kind=kind,
                    relative_path=f"governed/{evidence_id}.json", value=value,
                )
                for evidence_id, kind, value in entries
            ]
            contract["evidence_index"].extend(refs)
            event = next(
                item for item in contract["gates"][gate_id]["evidence"]
                if item.get("kind") == "gate_validation" and item.get("outcome") == "PASS"
            )
            event["evidence_ids"] = [ref["id"] for ref in refs]
            event["consumed_evidence_ids"] = [ref["id"] for ref in refs]
            event["consumed_evidence"] = [
                {field: ref[field] for field in ("id", "gate", "kind", "path", "sha256")}
                for ref in refs
            ]
        contract["G2_architecture"] = blueprint

    def planned_g5_references(self, root, artifact_refs, bundle, record_path):
        planned = [
            register_evidence_file(
                root,
                evidence_id=ref["id"],
                gate_id="G5",
                kind=ref["kind"],
                relative_path=ref["path"],
                maturity=ref.get("maturity"),
                metadata=ref.get("metadata"),
            )
            for ref in artifact_refs
        ]
        digest = hashlib.sha256(canonical_json_bytes(bundle)).hexdigest()
        planned.append(
            materialize_json_evidence(
                root,
                evidence_id=f"g5-full-production-{digest[:12]}",
                gate_id="G5",
                kind="full_course_production",
                relative_path=record_path,
                value=bundle,
                maturity="EXECUTION_VALIDATED",
            )
        )
        return planned

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
        record = {
            "schema_version": 2,
            "unit_id": "unit-1",
            "trial_context_id": "pilot-cold-run-20261018-01",
            "production_actor_ids": ["course-author-01", "page-builder-01"],
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
            "accessibility_report": {
                "evidence_id": "accessibility-g4-unit-1",
                "path": "evidence/accessibility-g4-unit-1.json",
                "sha256": "a" * 64,
                "claim_scope": "basic_accessibility_smoke",
            },
            "navigation": {
                "entry": "course index",
                "previous": "course index",
                "next": "next unit placeholder",
            },
        }
        return record

    def lesson_record(self):
        return {
            "unit_id": "unit-1",
            "asset_references": ["asset-product-brief", "asset-demo-plan"],
        }

    def full_blueprint(self):
        return {
            "outcomes": [
                {"id": "outcome-source", "criterion_ids": ["criterion-source"]},
                {"id": "outcome-plan", "criterion_ids": ["criterion-plan"]},
                {"id": "outcome-audit", "criterion_ids": ["criterion-audit"]},
            ],
            "criteria": [
                {"id": "criterion-source", "outcome_id": "outcome-source", "g0_criterion_id": "uses-source-facts", "capability_id": "capability-source"},
                {"id": "criterion-plan", "outcome_id": "outcome-plan", "g0_criterion_id": "complete-plan", "capability_id": "capability-plan"},
                {"id": "criterion-audit", "outcome_id": "outcome-audit", "g0_criterion_id": "passes-audit", "capability_id": "capability-audit"},
            ],
            "units": [
                {
                    "id": "unit-1",
                    "outcome": "從商品資料找出企劃限制與可用證據。",
                    "workflow_fingerprint": "extract-source-constraints",
                    "depends_on": [],
                    "asset_ids": ["asset-product-brief"],
                    "outcome_ids": ["outcome-source"],
                    "criterion_ids": ["criterion-source"],
                    "capability_ids": ["capability-source"],
                },
                {
                    "id": "unit-2",
                    "outcome": "依限制完成可交付的行銷企劃初稿。",
                    "workflow_fingerprint": "build-plan-from-constraints",
                    "depends_on": ["unit-1"],
                    "asset_ids": ["asset-demo-plan"],
                    "outcome_ids": ["outcome-plan"],
                    "criterion_ids": ["criterion-plan"],
                    "capability_ids": ["capability-plan"],
                },
                {
                    "id": "unit-3",
                    "outcome": "依驗收條件檢查並修訂完整企劃。",
                    "workflow_fingerprint": "audit-plan-against-criteria",
                    "depends_on": ["unit-2"],
                    "asset_ids": ["asset-product-brief", "asset-demo-plan"],
                    "outcome_ids": ["outcome-audit"],
                    "criterion_ids": ["criterion-audit"],
                    "capability_ids": ["capability-audit"],
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
                "outcome_ids": list(unit["outcome_ids"]),
                "criterion_ids": list(unit["criterion_ids"]),
                "capability_ids": list(unit["capability_ids"]),
                "learning_coverage": [
                    {
                        "outcome_id": unit["outcome_ids"][0],
                        "criterion_id": unit["criterion_ids"][0],
                        "capability_id": unit["capability_ids"][0],
                        "teaching_evidence": ["explanation", "full_demonstration"],
                        "practice_evidence": ["guided_practice", "independent_practice"],
                        "assessment_evidence": ["checks"],
                    }
                ],
                "explanation": {},
                "full_demonstration": {},
                "guided_practice": {},
                "independent_practice": {},
                "checks": [{"id": f"{unit['id']}-check"}],
            }
            for unit in self.full_blueprint()["units"]
        ]

    def full_trial(self):
        requirements_sha256 = hashlib.sha256(
            canonical_json_bytes(self.full_requirements())
        ).hexdigest()
        record = {
            "schema_version": 4,
            "scope": "full_course",
            "requirements_sha256": requirements_sha256,
            "target_profile_id": "target-marketing-practitioner",
            "runner_authority_id": self.authority_id,
            "participant": {
                "id": "full-course-cold-ai-01",
                "type": "independent-ai",
                "roles": ["learner-trial"],
            },
            "runner_session_id": "full-course-session-20261018-01",
            "isolated_context_id": "full-course-run-20261018-01",
            "allowed_tools": ["Spreadsheet application", "Markdown editor"],
            "allowed_inputs": [
                {
                    "kind": "learner-page",
                    "path": "courses/demo/index.html",
                    "sha256": "1" * 64,
                },
                {
                    "kind": "learner-asset",
                    "path": "assets/product-brief.pdf",
                    "sha256": "2" * 64,
                },
            ],
            "evidence_bindings": [
                {"evidence_id": "heldout-full-input", "path": "courses/demo/index.html", "sha256": "1" * 64, "role": "held-out-input"},
                {"evidence_id": "trial-full-course-final-plan", "path": "trial-output/full-course-run/final-plan.pdf", "sha256": "3" * 64, "role": "held-out-output"},
                {"evidence_id": "full-action-state-1", "path": "trial-evidence/full-action-state-1.json", "sha256": "4" * 64, "role": "action-state"},
                {"evidence_id": "full-action-state-2", "path": "trial-evidence/full-action-state-2.json", "sha256": "5" * 64, "role": "action-state"},
                {"evidence_id": "full-demo-input", "path": "trial-evidence/full-demo-input.csv", "sha256": "6" * 64, "role": "demonstration-input"},
                {"evidence_id": "full-demo-output", "path": "trial-evidence/full-demo-output.pdf", "sha256": "7" * 64, "role": "demonstration-output"},
                {"evidence_id": "full-guided-input", "path": "trial-evidence/full-guided-input.csv", "sha256": "8" * 64, "role": "guided-practice-input"},
                {"evidence_id": "full-guided-output", "path": "trial-evidence/full-guided-output.pdf", "sha256": "9" * 64, "role": "guided-practice-output"},
                {"evidence_id": "full-answer-input", "path": "trial-evidence/full-answer-input.csv", "sha256": "a" * 64, "role": "answer-key-input"},
                {"evidence_id": "full-answer-output", "path": "trial-evidence/full-answer-output.pdf", "sha256": "b" * 64, "role": "answer-key-output"},
            ],
            "forbidden_inputs_accessed": [],
            "entry_readiness": {
                "baseline_statement": "Can inspect tabular campaign data and perform basic arithmetic.",
                "prerequisite_statements": ["Can download, open, edit, and save learner files."],
                "baseline_confirmed": True,
                "prerequisites_confirmed": True,
                "tools_confirmed": True,
                "inputs_confirmed": True,
            },
            "entry": {
                "started_at": "2026-10-18T16:00:00+08:00",
                "page": "courses/demo/index.html",
                "goal_understood": True,
                "materials_found": True,
            },
            "actions": [
                {
                    "id": "pending",
                    "sequence": 1,
                    "task_id": "heldout-full-course-plan",
                    "operation": {"subject_evidence_id": "heldout-full-input", "kind": "extract", "transformation": {"rule_kind": "field-extraction", "rule_id": "source-threshold-change"}},
                    "decision": {"condition_id": "source-threshold-change", "criterion_id": "criterion-source", "rule_passed": False, "outcome": "reject"},
                    "affected_criterion_id": "criterion-source",
                    "input_evidence_id": "heldout-full-input",
                    "output_evidence_id": "full-action-state-1",
                    "observable_result": {"evidence_id": "full-action-state-1", "criterion_id": "criterion-source", "expected_result": "PASS", "actual_result": "PASS", "actual_sha256": "4" * 64},
                    "result": "PASS",
                    "at": "2026-10-18T16:10:00+08:00",
                },
                {
                    "id": "pending",
                    "sequence": 2,
                    "task_id": "heldout-full-course-plan",
                    "operation": {"subject_evidence_id": "full-action-state-1", "kind": "calculate", "transformation": {"rule_kind": "numeric-calculation", "rule_id": "plan-threshold-change"}},
                    "decision": {"condition_id": "plan-threshold-change", "criterion_id": "criterion-plan", "rule_passed": False, "outcome": "reallocate"},
                    "affected_criterion_id": "criterion-plan",
                    "input_evidence_id": "full-action-state-1",
                    "output_evidence_id": "full-action-state-2",
                    "observable_result": {"evidence_id": "full-action-state-2", "criterion_id": "criterion-plan", "expected_result": "PASS", "actual_result": "PASS", "actual_sha256": "5" * 64},
                    "result": "PASS",
                    "at": "2026-10-18T16:30:00+08:00",
                },
                {
                    "id": "pending",
                    "sequence": 3,
                    "task_id": "heldout-full-course-plan",
                    "operation": {"subject_evidence_id": "full-action-state-2", "kind": "validate", "transformation": {"rule_kind": "criterion-validation", "rule_id": "audit-threshold-change"}},
                    "decision": {"condition_id": "audit-threshold-change", "criterion_id": "criterion-audit", "rule_passed": False, "outcome": "revise"},
                    "affected_criterion_id": "criterion-audit",
                    "input_evidence_id": "full-action-state-2",
                    "output_evidence_id": "trial-full-course-final-plan",
                    "observable_result": {"evidence_id": "trial-full-course-final-plan", "criterion_id": "criterion-audit", "expected_result": "PASS", "actual_result": "PASS", "actual_sha256": "3" * 64},
                    "result": "PASS",
                    "at": "2026-10-18T16:50:00+08:00",
                }
            ],
            "transfer_task": {
                "task_id": "heldout-full-course-plan",
                "source_task_id": "guided-course-plan",
                "changed_conditions": [
                    {
                        "dimension": "threshold",
                        "condition_id": "source-threshold-change", "metric_id": "channel-cost", "unit": "twd",
                        "comparator": "lte", "before_value": 50000, "after_value": 30000, "observed_value": 40000,
                        "basis_evidence_id": "heldout-full-input",
                        "affected_criterion_id": "criterion-source",
                        "before_rule_passed": True, "after_rule_passed": False,
                        "before_outcome": "accept", "after_outcome": "reject",
                    },
                    {"condition_id": "plan-threshold-change", "dimension": "threshold", "metric_id": "total-budget", "unit": "twd", "comparator": "lte", "before_value": 500000, "after_value": 300000, "observed_value": 400000, "basis_evidence_id": "full-action-state-1", "affected_criterion_id": "criterion-plan", "before_rule_passed": True, "after_rule_passed": False, "before_outcome": "accept", "after_outcome": "reallocate"},
                    {"condition_id": "audit-threshold-change", "dimension": "threshold", "metric_id": "channel-limit", "unit": "twd", "comparator": "lte", "before_value": 50000, "after_value": 30000, "observed_value": 40000, "basis_evidence_id": "full-action-state-2", "affected_criterion_id": "criterion-audit", "before_rule_passed": True, "after_rule_passed": False, "before_outcome": "accept", "after_outcome": "revise"}
                ],
                "held_out_input_evidence_id": "heldout-full-input",
                "held_out_output_evidence_id": "trial-full-course-final-plan",
                "reference_evidence": {
                    "demonstration": {"input_evidence_id": "full-demo-input", "output_evidence_id": "full-demo-output"},
                    "guided_practice": {"input_evidence_id": "full-guided-input", "output_evidence_id": "full-guided-output"},
                    "answer_key": {"input_evidence_id": "full-answer-input", "output_evidence_id": "full-answer-output"},
                },
            },
            "criterion_evidence": [
                {
                    "g0_criterion_id": g0_id,
                    "capability_id": capability_id,
                    "outcome_id": outcome_id,
                    "criterion_id": criterion_id,
                    "unit_id": unit_id,
                    "action_id": "pending",
                    "artifact_evidence_id": "trial-full-course-final-plan",
                    "result": "PASS",
                }
                for g0_id, capability_id, outcome_id, criterion_id, unit_id in (
                    ("uses-source-facts", "capability-source", "outcome-source", "criterion-source", "unit-1"),
                    ("complete-plan", "capability-plan", "outcome-plan", "criterion-plan", "unit-2"),
                    ("passes-audit", "capability-audit", "outcome-audit", "criterion-audit", "unit-3"),
                )
            ],
            "hints": [{"source": "none", "detail": "未使用額外提示。"}],
            "blocks": [],
            "recovery": [],
            "artifact": {
                "evidence_id": "trial-full-course-final-plan",
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
            "maturity_claims": {
                "ai_trial": "INDEPENDENT_AI_VERIFIED",
                "human_duration": "PENDING_HUMAN",
                "human_readability": "PENDING_HUMAN",
                "target_learner_independence": "PENDING_HUMAN",
            },
        }
        for action in record["actions"]:
            action["id"] = trial_action_id(action)
        for row, action in zip(record["criterion_evidence"], record["actions"]):
            row["action_id"] = action["id"]
        return record

    def full_requirements(self):
        return {
            "target_profile": {
                "id": "target-marketing-practitioner",
                "baseline": "Can inspect tabular campaign data and perform basic arithmetic.",
                "prerequisites": ["Can download, open, edit, and save learner files."],
            },
            "environment": {
                "tools": ["Spreadsheet application", "Markdown editor"],
            },
            "acceptance_criteria": [
                {"id": "uses-source-facts", "capabilities": [{"id": "capability-source", "statement": "Use source facts."}]},
                {"id": "complete-plan", "capabilities": [{"id": "capability-plan", "statement": "Complete the plan."}]},
                {"id": "passes-audit", "capabilities": [{"id": "capability-audit", "statement": "Pass the audit."}]},
            ],
        }

    def full_production(self):
        units = []
        blueprint_units = self.full_blueprint()["units"]
        trial = self.full_trial()
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
                    "outcome_ids": list(unit["outcome_ids"]),
                    "criterion_ids": list(unit["criterion_ids"]),
                    "capability_ids": list(unit["capability_ids"]),
                    "previous": None if index == 0 else blueprint_units[index - 1]["id"],
                    "next": None if index == len(blueprint_units) - 1 else blueprint_units[index + 1]["id"],
                }
            )
        return {
            "schema_version": 2,
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
            "learning_coverage": [
                {
                    "g0_criterion_id": criterion["g0_criterion_id"],
                    "capability_id": criterion["capability_id"],
                    "outcome_id": criterion["outcome_id"],
                    "criterion_id": criterion["id"],
                    "unit_id": unit["id"],
                    "lesson_unit_id": unit["id"],
                    "artifact_criterion_id": criterion["g0_criterion_id"],
                    "artifact_evidence_id": criterion["g0_criterion_id"],
                    "trial_evidence_id": action_id,
                }
                for unit, criterion, action_id in zip(
                    blueprint_units,
                    self.full_blueprint()["criteria"],
                    tuple(action["id"] for action in trial["actions"]),
                )
            ],
            "accessibility_report": {
                "evidence_id": "accessibility-g5-full-course",
                "path": "evidence/accessibility-g5-full-course.json",
                "sha256": "a" * 64,
                "claim_scope": "basic_accessibility_smoke",
            },
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
            "full_course_trial": trial,
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

    def test_pilot_binds_the_independent_trial_context(self):
        pilot = self.valid_pilot()
        del pilot["trial_context_id"]

        codes = {
            item.code
            for item in validate_pilot_record(
                pilot, self.lesson_record(), self.valid_asset_manifest()
            )
        }

        self.assertIn("pilot_trial_context_required", codes)

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

    def test_pilot_requires_typed_accessibility_report_reference(self):
        pilot = self.valid_pilot()
        del pilot["accessibility_report"]

        codes = {
            item.code
            for item in validate_pilot_record(
                pilot, self.lesson_record(), self.valid_asset_manifest()
            )
        }

        self.assertIn("schema_required", codes)

    def test_g5_cannot_begin_until_g4_passes(self):
        contract = new_contract(
            "marketing-practice",
            "行銷企劃實作",
            "課程團隊",
            "2026-10-18T12:00:00+08:00",
        )
        self.authority.bind(contract)
        for gate_id in ("G0", "G1", "G2", "G3"):
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

    def test_g5_rejects_missing_or_unknown_child_capability_coverage(self):
        production = self.full_production()
        production["learning_coverage"].pop()
        production["learning_coverage"][0]["capability_id"] = "unknown-capability"

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

        self.assertIn("uncovered_capability", codes)
        self.assertIn("unknown_reference", codes)

    def test_g5_coverage_rejects_fake_artifact_and_trial_evidence_ids(self):
        production = self.full_production()
        production["learning_coverage"][0]["artifact_evidence_id"] = "fake"
        production["learning_coverage"][1]["trial_evidence_id"] = "fake"
        codes = {
            issue.code for issue in validate_full_production(
                production, self.full_blueprint(), self.full_lessons(),
                self.valid_asset_manifest(),
                {"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"},
                self.full_trial(),
            )
        }
        self.assertIn("invalid_coverage_row", codes)

    def test_production_schema_stable_refs_match_runtime(self):
        schema = json.loads(
            (Path(__file__).parents[1] / "contracts" / "course-production-record.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn(PRODUCTION_COVERAGE_FIELD, schema["required"])
        self.assertTrue(
            set(PRODUCTION_UNIT_STABLE_FIELDS).issubset(schema["$defs"]["unit"]["required"])
        )

    def test_production_runtime_rejects_schema_closed_shape_bypass(self):
        production = self.full_production()
        production["producer_validation"] = {"status": "PASS"}
        self.assertIn(
            "schema_additional_property",
            {issue.code for issue in validate_full_production(
                production, self.full_blueprint(), self.full_lessons(),
                self.valid_asset_manifest(),
                {"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"},
                self.full_trial(),
            )},
        )

    def test_governed_role_roster_prevents_self_declared_g5_independence(self):
        production = self.full_production()
        production["production_authors"] = ["self-declared-unrelated-author"]
        trial = self.full_trial()
        trial["participant"]["id"] = "course-author-01"
        production["full_course_trial"] = trial
        production_roles = {
            "schema_version": 1,
            "authors": ["course-author-01", "page-builder-01"],
            "validators": ["course-validator"],
        }

        codes = {
            issue.code
            for issue in validate_full_production(
                production,
                self.full_blueprint(),
                self.full_lessons(),
                self.valid_asset_manifest(),
                {"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"},
                trial,
                production_roles=production_roles,
            )
        }

        self.assertIn("production_role_roster_mismatch", codes)
        self.assertIn("independent_participant_required", codes)

    def test_g5_requires_independent_ai_even_when_human_trial_evidence_is_complete(self):
        trial = self.full_trial()
        trial["participant"]["id"] = "human-trial-01"
        trial["participant"]["type"] = "human"
        trial["human_participant_evidence"] = {
            "consent_record": "evidence/human-consent.json",
            "observer_id": "observer-01",
            "session_recording_sha256": "d" * 64,
        }
        production = self.full_production()
        production["full_course_trial"] = trial

        codes = {
            issue.code
            for issue in validate_full_production(
                production,
                self.full_blueprint(),
                self.full_lessons(),
                self.valid_asset_manifest(),
                {"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"},
                trial,
            )
        }

        self.assertIn("independent_participant_required", codes)

    def test_full_production_route_passes_g5_with_indexed_evidence_and_trial(self):
        contract = new_contract(
            "marketing-practice",
            "行銷企劃實作",
            "course-run",
            "2026-10-18T12:00:00+08:00",
        )
        self.authority.bind(contract)
        for gate_id in ("G0", "G1", "G2", "G3", "G4"):
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
        begin_gate(contract, "G5", "course-run", "2026-10-18T17:10:00+08:00")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact_path = root / "evidence" / "g5-render-and-integration.json"
            artifact_path.parent.mkdir(parents=True)
            artifact_path.write_text('{"result":"PASS"}\n', encoding="utf-8")
            roster_ref = materialize_json_evidence(
                root,
                evidence_id="g5-production-role-roster",
                gate_id="G0",
                kind="production_role_roster",
                relative_path="evidence/g5-production-role-roster.json",
                value={
                    "schema_version": 1,
                    "authors": ["course-author-01", "page-builder-01"],
                    "validators": ["course-validator"],
                },
            )
            contract["evidence_index"].append(roster_ref)
            contract["governance"]["production_role_roster"] = {
                "evidence_id": roster_ref["id"], "sha256": roster_ref["sha256"]
            }
            production = self.full_production()
            lessons = self.full_lessons()
            self.bind_governed_course(root, contract, self.full_blueprint(), lessons)
            assets = self.valid_asset_manifest()
            artifact_refs = self.g5_artifact_refs(root, production, lessons, assets)
            artifact_refs.extend(self.bind_trial_inputs(root, production["full_course_trial"], production))
            production_bundle = {
                "record": production,
                "blueprint": self.full_blueprint(),
                "lessons": lessons,
                "assets": assets,
                "pilot": {
                    "unit_id": "unit-1",
                    "trial_context_id": "pilot-cold-run-20261018-01",
                },
            }
            planned_refs = self.planned_g5_references(
                root, artifact_refs, production_bundle, "production/full-course.json"
            )
            trial_ref = materialize_json_evidence(
                root,
                evidence_id="g5-trial-source",
                gate_id="G5",
                kind="independent_course_trial",
                relative_path="trials/g5-full-course.json",
                value=production["full_course_trial"],
                maturity="INDEPENDENT_AI_VERIFIED",
            )
            receipt_ref = self.authority.issue(
                root, contract=contract, gate_id="G5",
                trial_reference=trial_ref, roster_reference=roster_ref,
                transition_references=[*planned_refs, trial_ref, roster_ref],
                runner_id=production["full_course_trial"]["participant"]["id"],
                session_id=production["full_course_trial"]["runner_session_id"],
                issued_at="2026-10-18T17:14:00+08:00", nonce="g5-positive-nonce",
                receipt_id="g5-trial-receipt", relative_path="receipts/g5.json",
            )
            contract["evidence_index"].extend([trial_ref, receipt_ref])

            before_subset = copy.deepcopy(contract)
            subset_result = route_full_production_to_g5(
                contract, production, artifact_refs, "course-run",
                "2026-10-18T17:15:00+08:00", workspace_root=root,
                blueprint=self.full_blueprint(), lessons=lessons[:-1], assets=assets,
                pilot={"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"},
                production_role_evidence_id=roster_ref["id"],
                production_record_path="production/full-course.json",
                trial_evidence_id=trial_ref["id"],
                trial_receipt_evidence_id=receipt_ref["id"],
            )
            self.assertEqual(subset_result, "BLOCKED")
            self.assertEqual(contract, before_subset)

            result = route_full_production_to_g5(
                contract,
                production,
                artifact_refs,
                "course-run",
                "2026-10-18T17:15:00+08:00",
                workspace_root=root,
                blueprint=self.full_blueprint(),
                lessons=lessons,
                assets=assets,
                pilot={
                    "unit_id": "unit-1",
                    "trial_context_id": "pilot-cold-run-20261018-01",
                },
                production_role_evidence_id=roster_ref["id"],
                production_record_path="production/full-course.json",
                trial_evidence_id=trial_ref["id"],
                trial_receipt_evidence_id=receipt_ref["id"],
            )

            self.assertEqual(result, "PASS")
            self.assertEqual(contract["gates"]["G5"]["status"], "PASS")
            event = contract["gates"]["G5"]["evidence"][-1]
            self.assertEqual(event["maturity"], "INDEPENDENT_AI_VERIFIED")
            self.assertNotIn("human_duration", event)
            self.assertNotIn("human_readability", event)
            self.assertNotIn("target_learner_independence", event)
            g5_refs = [
                item for item in contract["evidence_index"] if item.get("gate") == "G5"
            ]
            self.assertTrue(
                all(
                    not verify_evidence_reference(root, item, expected_gate="G5")
                    for item in g5_refs
                )
            )

    def test_g5_route_runs_complete_validator_instead_of_trusting_pass_status(self):
        contract = new_contract(
            "marketing-practice",
            "行銷企劃實作",
            "course-run",
            "2026-10-18T12:00:00+08:00",
        )
        self.authority.bind(contract)
        for gate_id in ("G0", "G1", "G2", "G3", "G4"):
            contract["gates"][gate_id]["status"] = "PASS"
            contract["gates"][gate_id]["source_revision"] = 1
            evidence_id = f"{gate_id.lower()}-setup"
            contract["evidence_index"].append(
                {
                    "id": evidence_id,
                    "gate": gate_id,
                    "kind": "test_record",
                    "path": f"evidence/{evidence_id}.json",
                    "sha256": hashlib.sha256(evidence_id.encode()).hexdigest(),
                }
            )
            contract["gates"][gate_id]["evidence"].append(
                {
                    "kind": "gate_validation",
                    "outcome": "PASS",
                    "validator_id": "test-setup",
                    "actor": "test-setup",
                    "at": "2026-10-18T17:00:00+08:00",
                    "evidence_ids": [evidence_id],
                    "consumed_evidence_ids": [evidence_id],
                    "consumed_evidence": [
                        {
                            "id": evidence_id,
                            "gate": gate_id,
                            "kind": "test_record",
                            "path": f"evidence/{evidence_id}.json",
                            "sha256": hashlib.sha256(evidence_id.encode()).hexdigest(),
                        }
                    ],
                }
            )
        begin_gate(contract, "G5", "course-run", "2026-10-18T17:10:00+08:00")
        production = self.full_production()
        production["units"].pop()

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            artifact_path = root / "evidence" / "g5-integration.json"
            artifact_path.parent.mkdir(parents=True)
            artifact_path.write_text('{"result":"PASS"}\n', encoding="utf-8")
            roster_ref = materialize_json_evidence(
                root,
                evidence_id="g5-role-roster",
                gate_id="G0",
                kind="production_role_roster",
                relative_path="evidence/g5-role-roster.json",
                value={
                    "schema_version": 1,
                    "authors": ["course-author-01", "page-builder-01"],
                    "validators": ["course-validator"],
                },
            )
            contract["evidence_index"].append(roster_ref)
            contract["governance"]["production_role_roster"] = {
                "evidence_id": roster_ref["id"], "sha256": roster_ref["sha256"]
            }
            transfer_refs = self.bind_trial_inputs(root, production["full_course_trial"], production)
            self.bind_governed_course(root, contract, self.full_blueprint(), self.full_lessons())
            pages = [
                {"id": "course-entry", "path": production["navigation"]["entry"]},
                *[{"id": unit["unit_id"], "path": unit["html_path"]} for unit in production["units"]],
                {"id": "course-completion", "path": production["navigation"]["completion"]},
            ]
            _, accessibility_ref, production["accessibility_report"] = (
                self.materialize_accessibility_report(
                    root, "G5", pages, "accessibility-g5-invalid-course"
                )
            )
            production_bundle = {
                "record": production,
                "blueprint": self.full_blueprint(),
                "lessons": self.full_lessons(),
                "assets": self.valid_asset_manifest(),
                "pilot": {
                    "unit_id": "unit-1",
                    "trial_context_id": "pilot-cold-run-20261018-01",
                },
            }
            invalid_artifact_refs = [
                {
                    "id": "g5-integration",
                    "kind": "production_artifact",
                    "path": "evidence/g5-integration.json",
                },
                {
                    "id": accessibility_ref["id"],
                    "kind": accessibility_ref["kind"],
                    "path": accessibility_ref["path"],
                },
            ]
            invalid_artifact_refs.extend(transfer_refs)
            planned_refs = self.planned_g5_references(
                root, invalid_artifact_refs, production_bundle,
                "production/invalid-full-course.json",
            )
            trial_ref = materialize_json_evidence(
                root,
                evidence_id="g5-invalid-trial-source",
                gate_id="G5",
                kind="independent_course_trial",
                relative_path="trials/g5-invalid-full-course.json",
                value=production["full_course_trial"],
                maturity="INDEPENDENT_AI_VERIFIED",
            )
            receipt_ref = self.authority.issue(
                root, contract=contract, gate_id="G5",
                trial_reference=trial_ref, roster_reference=roster_ref,
                transition_references=[*planned_refs, trial_ref, roster_ref],
                runner_id=production["full_course_trial"]["participant"]["id"],
                session_id=production["full_course_trial"]["runner_session_id"],
                issued_at="2026-10-18T17:14:00+08:00", nonce="g5-invalid-production-nonce",
                receipt_id="g5-invalid-trial-receipt", relative_path="receipts/g5-invalid.json",
            )
            contract["evidence_index"].extend([trial_ref, receipt_ref])

            result = route_full_production_to_g5(
                contract,
                production,
                invalid_artifact_refs,
                "course-run",
                "2026-10-18T17:15:00+08:00",
                workspace_root=root,
                blueprint=self.full_blueprint(),
                lessons=self.full_lessons(),
                assets=self.valid_asset_manifest(),
                pilot={
                    "unit_id": "unit-1",
                    "trial_context_id": "pilot-cold-run-20261018-01",
                },
                production_role_evidence_id=roster_ref["id"],
                production_record_path="production/invalid-full-course.json",
                trial_evidence_id=trial_ref["id"],
                trial_receipt_evidence_id=receipt_ref["id"],
            )

        self.assertEqual(result, "BLOCKED")
        self.assertEqual(contract["gates"]["G5"]["status"], "IN_PROGRESS")

    def test_g5_wrong_governed_roster_kind_leaves_contract_unchanged(self):
        contract = new_contract("transactional-course", "Transactional Course", "course-run", "2026-10-18T12:00:00+08:00")
        self.authority.bind(contract)
        for gate_id in ("G0", "G1", "G2", "G3", "G4"):
            begin_gate(contract, gate_id, "test", "2026-10-18T12:01:00+08:00")
            evidence_id = f"{gate_id.lower()}-fixture"
            contract["evidence_index"].append({"id": evidence_id, "gate": gate_id, "kind": "test_record", "path": f"fixtures/{evidence_id}.json", "sha256": hashlib.sha256(evidence_id.encode()).hexdigest()})
            _commit_gate_pass(contract, gate_id, [evidence_id], "test", "test", "2026-10-18T12:02:00+08:00")
        begin_gate(contract, "G5", "test", "2026-10-18T12:03:00+08:00")

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wrong = materialize_json_evidence(root, evidence_id="wrong-roster", gate_id="G0", kind="test_record", relative_path="evidence/wrong-roster.json", value={"authors": []})
            self.bind_governed_course(root, contract, self.full_blueprint(), self.full_lessons())
            contract["evidence_index"].append(wrong)
            contract["governance"]["production_role_roster"] = {"evidence_id": wrong["id"], "sha256": wrong["sha256"]}
            artifact = root / "evidence" / "artifact.txt"
            artifact.write_text("artifact", encoding="utf-8")
            production = self.full_production()
            bundle = {"record": production, "blueprint": self.full_blueprint(), "lessons": self.full_lessons(), "assets": self.valid_asset_manifest(), "pilot": {"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"}}
            materialize_json_evidence(root, evidence_id="source", gate_id="G5", kind="full_course_production", relative_path="production/full.json", value=bundle)
            trial_ref = materialize_json_evidence(root, evidence_id="trial", gate_id="G5", kind="independent_course_trial", relative_path="trials/full.json", value=production["full_course_trial"])
            receipt_ref = materialize_json_evidence(root, evidence_id="receipt", gate_id="G5", kind="independent_trial_receipt", relative_path="receipts/full.json", value={"invalid": True})
            contract["evidence_index"].extend([trial_ref, receipt_ref])
            before = copy.deepcopy(contract)
            with self.assertRaisesRegex(ContractStateError, "governed roster binding"):
                route_full_production_to_g5(
                    contract, production,
                    [{"id": "artifact", "kind": "production_artifact", "path": "evidence/artifact.txt"}],
                    "course-run", "2026-10-18T12:04:00+08:00",
                    workspace_root=root, blueprint=self.full_blueprint(), lessons=self.full_lessons(),
                    assets=self.valid_asset_manifest(), pilot={"unit_id": "unit-1", "trial_context_id": "pilot-cold-run-20261018-01"},
                    production_role_evidence_id=wrong["id"], production_record_path="production/full.json",
                    trial_evidence_id=trial_ref["id"], trial_receipt_evidence_id=receipt_ref["id"],
                )
        self.assertEqual(contract, before)


if __name__ == "__main__":
    unittest.main()
