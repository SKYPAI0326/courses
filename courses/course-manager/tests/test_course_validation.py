import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.course_contract import (
    ContractStateError,
    GATE_ORDER,
    begin_gate,
    new_contract,
    resolve_gate_blocker,
    validate_contract,
)
from tests.gate_test_support import _commit_gate_pass
from src.course_evidence import ConsumedEvidence, materialize_json_evidence, register_evidence_file, verify_evidence_reference
from src.course_gate_validators import validated_trial_reference_maturity
from src.course_validation import (
    evidence_maturity,
    route_trial_failure,
    trial_action_id,
    validate_trial_context_is_new,
    validate_trial_record,
)
from src.course_validation_routes import route_verified_trial_to_gate
from tests.runner_authority_fixture import TestRunnerAuthority


class CourseTrialValidationTests(unittest.TestCase):
    def setUp(self):
        self.authority_id = "test-independent-lab"
        self.authority = TestRunnerAuthority(
            self.authority_id,
            {
                "cold-learner-ai-01": {
                    "role": "isolated-learner-runner",
                    "sessions": {
                        "cold-session-20261018-01": {
                            "assertion_id": "assertion-cold-session-01",
                            "context_id": "cold-run-20261018-01",
                        }
                    },
                }
            },
        )

    def valid_trial(self, participant_type="independent-ai", scope="representative_unit"):
        record = {
            "schema_version": 3,
            "requirements_sha256": "9" * 64,
            "target_profile_id": "target-marketing-practitioner",
            "runner_authority_id": self.authority_id,
            "scope": scope,
            "participant": {
                "id": "cold-learner-ai-01",
                "type": participant_type,
                "roles": ["learner-trial"],
            },
            "runner_session_id": "cold-session-20261018-01",
            "isolated_context_id": "cold-run-20261018-01",
            "allowed_tools": ["Spreadsheet application", "Markdown editor"],
            "allowed_inputs": [
                {
                    "kind": "learner-page",
                    "path": "courses/demo/unit-1.html",
                    "sha256": "a" * 64,
                },
                {
                    "kind": "learner-asset",
                    "path": "courses/demo/assets/product-brief.pdf",
                    "sha256": "b" * 64,
                },
            ],
            "evidence_bindings": [
                {"evidence_id": "held-out-input", "path": "courses/demo/unit-1.html", "sha256": "a" * 64, "role": "held-out-input"},
                {"evidence_id": "trial-final-plan", "path": "trial-output/cold-run-20261018-01/marketing-plan.pdf", "sha256": "c" * 64, "role": "held-out-output"},
                {"evidence_id": "demo-input", "path": "trial-evidence/demo-input.csv", "sha256": "1" * 64, "role": "demonstration-input"},
                {"evidence_id": "demo-output", "path": "trial-evidence/demo-output.pdf", "sha256": "2" * 64, "role": "demonstration-output"},
                {"evidence_id": "guided-input", "path": "trial-evidence/guided-input.csv", "sha256": "3" * 64, "role": "guided-practice-input"},
                {"evidence_id": "guided-output", "path": "trial-evidence/guided-output.pdf", "sha256": "4" * 64, "role": "guided-practice-output"},
                {"evidence_id": "answer-input", "path": "trial-evidence/answer-input.csv", "sha256": "5" * 64, "role": "answer-key-input"},
                {"evidence_id": "answer-output", "path": "trial-evidence/answer-output.pdf", "sha256": "6" * 64, "role": "answer-key-output"},
                {"evidence_id": "action-state-budget", "path": "trial-evidence/action-state-budget.json", "sha256": "d" * 64, "role": "action-state"},
            ],
            "forbidden_inputs_accessed": [],
            "entry_readiness": {
                "baseline_statement": "Can inspect tabular campaign data and perform basic arithmetic.",
                "prerequisite_statements": ["Can download, open, edit, and save the learner files."],
                "baseline_confirmed": True,
                "prerequisites_confirmed": True,
                "tools_confirmed": True,
                "inputs_confirmed": True,
            },
            "entry": {
                "started_at": "2026-10-18T15:00:00+08:00",
                "page": "courses/demo/unit-1.html",
                "goal_understood": True,
                "materials_found": True,
            },
            "actions": [
                {
                    "id": "pending",
                    "sequence": 1,
                    "task_id": "held-out-marketing-plan",
                    "action": "開啟商品資料並找出預算與截止日。",
                    "decision": "依新的預算與截止日重新判斷企劃限制。",
                    "observable_result": "在資料表中找到預算 20 萬元與截止日。",
                    "affected_criterion_id": "g2-plan",
                    "input_evidence_id": "held-out-input",
                    "output_evidence_id": "action-state-budget",
                    "result": "PASS",
                    "at": "2026-10-18T15:01:00+08:00",
                },
                {
                    "id": "pending",
                    "sequence": 2,
                    "task_id": "held-out-marketing-plan",
                    "action": "依講義步驟完成企劃表。",
                    "decision": "依新的門檻選擇符合限制的預算拆分與時程。",
                    "observable_result": "產出含目標、受眾、時程與預算的企劃表。",
                    "affected_criterion_id": "g2-plan",
                    "input_evidence_id": "action-state-budget",
                    "output_evidence_id": "trial-final-plan",
                    "result": "PASS",
                    "at": "2026-10-18T15:08:00+08:00",
                },
            ],
            "transfer_task": {
                "task_id": "held-out-marketing-plan",
                "source_task_id": "guided-marketing-plan",
                "changed_conditions": [
                    {
                        "dimension": "threshold",
                        "rule": "總預算不得超過指定上限並須依渠道轉換門檻配置。",
                        "comparator": "lte",
                        "before_value": 300000,
                        "after_value": 200000,
                        "affected_criterion_id": "g2-plan",
                        "before_decision": "三個渠道平均分配預算。",
                        "after_decision": "依轉換門檻縮減未達標渠道預算。",
                        "decision_basis": "預算門檻與渠道成效同時改變，必須重新計算後判斷。",
                    }
                ],
                "held_out_input_evidence_id": "held-out-input",
                "held_out_output_evidence_id": "trial-final-plan",
                "reference_evidence": {
                    "demonstration": {"input_evidence_id": "demo-input", "output_evidence_id": "demo-output"},
                    "guided_practice": {"input_evidence_id": "guided-input", "output_evidence_id": "guided-output"},
                    "answer_key": {"input_evidence_id": "answer-input", "output_evidence_id": "answer-output"},
                },
            },
            "criterion_evidence": [
                {
                    "g0_criterion_id": "criterion-plan",
                    "capability_id": "capability-plan",
                    "outcome_id": "outcome-plan",
                    "criterion_id": "g2-plan",
                    "unit_id": "unit-1",
                    "action_id": "pending",
                    "artifact_evidence_id": "trial-final-plan",
                    "result": "PASS",
                }
            ],
            "hints": [
                {
                    "source": "learner-page",
                    "detail": "使用講義中『資料不完整時』的修復提示。",
                }
            ],
            "blocks": [
                {
                    "code": "practice_instruction_gap",
                    "detail": "第一次未注意到預算必須拆分。",
                    "recovered": True,
                }
            ],
            "recovery": [
                {
                    "block_code": "practice_instruction_gap",
                    "action": "依頁面提示回到商品資料核對預算欄。",
                    "result": "修正預算拆分並重新通過頁面檢查。",
                }
            ],
            "artifact": {
                "evidence_id": "trial-final-plan",
                "path": "trial-output/cold-run-20261018-01/marketing-plan.pdf",
                "sha256": "c" * 64,
                "complete": True,
                "verifiable": True,
                "acceptance_result": "PASS",
            },
            "result": {
                "status": "PASS",
                "completed_at": "2026-10-18T15:10:00+08:00",
                "notes": "只依學員頁與學員素材完成，未使用作者說明。",
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
        record["criterion_evidence"][0]["action_id"] = record["actions"][-1]["id"]
        if participant_type == "human":
            record["participant"]["id"] = "human-trial-01"
            record["maturity_claims"]["ai_trial"] = "NOT_APPLICABLE"
            record["human_participant_evidence"] = {
                "consent_record": "evidence/human-trial-01-consent.json",
                "observer_id": "observer-02",
                "session_recording_sha256": "d" * 64,
            }
        return record

    def materialize_trial_inputs(self, root, trial):
        for index, item in enumerate(trial["allowed_inputs"]):
            target = root / item["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            payload = f"learner-visible input {index}\n".encode()
            target.write_bytes(payload)
            item["sha256"] = hashlib.sha256(payload).hexdigest()
        next(item for item in trial["evidence_bindings"] if item["role"] == "held-out-input")["sha256"] = trial["allowed_inputs"][0]["sha256"]

    def materialize_transfer_artifacts(self, root, trial):
        gate_id = "G4" if trial["scope"] == "representative_unit" else "G5"
        refs = []
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
            refs.append(ref)
        final = next(item for item in trial["evidence_bindings"] if item["role"] == "held-out-output")
        trial["artifact"]["path"] = final["path"]
        trial["artifact"]["sha256"] = final["sha256"]
        return refs

    def governed_requirements(self):
        return {
            "target_profile": {
                "id": "target-marketing-practitioner",
                "baseline": "Can inspect tabular campaign data and perform basic arithmetic.",
                "prerequisites": ["Can download, open, edit, and save the learner files."],
            },
            "environment": {
                "tools": ["Spreadsheet application", "Markdown editor"],
            },
            "acceptance_criteria": [
                {
                    "id": "criterion-plan",
                    "capabilities": [
                        {"id": "capability-plan", "statement": "Create a constrained plan."}
                    ],
                }
            ],
        }

    def governed_blueprint(self):
        return {
            "criteria": [
                {
                    "id": "g2-plan",
                    "g0_criterion_id": "criterion-plan",
                    "capability_id": "capability-plan",
                    "outcome_id": "outcome-plan",
                }
            ],
            "units": [
                {
                    "id": "unit-1",
                    "outcome_ids": ["outcome-plan"],
                    "criterion_ids": ["g2-plan"],
                    "capability_ids": ["capability-plan"],
                }
            ],
        }

    def validate_bound_trial(self, trial, *, scope="representative_unit"):
        return validate_trial_record(
            trial,
            [],
            scope,
            requirements=self.governed_requirements(),
            requirements_sha256="9" * 64,
            blueprint=self.governed_blueprint(),
            representative_unit_id="unit-1" if scope == "representative_unit" else None,
            runner_authority_id=self.authority_id,
        )

    def bind_governed_trial_design(self, root, contract, trial):
        requirements_ref = materialize_json_evidence(
            root,
            evidence_id="governed-g0-requirements",
            gate_id="G0",
            kind="requirements_record",
            relative_path="governed/g0-requirements.json",
            value=self.governed_requirements(),
        )
        blueprint_ref = materialize_json_evidence(
            root,
            evidence_id="governed-g2-blueprint",
            gate_id="G2",
            kind="course_blueprint",
            relative_path="governed/g2-blueprint.json",
            value=self.governed_blueprint(),
        )
        for gate_id, ref in (("G0", requirements_ref), ("G2", blueprint_ref)):
            old_id = f"{gate_id.lower()}-evidence"
            contract["evidence_index"] = [
                item for item in contract["evidence_index"] if item.get("id") != old_id
            ]
            contract["evidence_index"].append(ref)
            event = contract["gates"][gate_id]["evidence"][-1]
            event["evidence_ids"] = [ref["id"]]
            event["consumed_evidence_ids"] = [ref["id"]]
            event["consumed_evidence"] = [
                {field: ref[field] for field in ("id", "gate", "kind", "path", "sha256")}
            ]
        contract["G0_requirements"] = self.governed_requirements()
        contract["G2_architecture"] = self.governed_blueprint()
        trial["requirements_sha256"] = requirements_ref["sha256"]
        return requirements_ref, blueprint_ref

    def test_trial_binds_canonical_profile_readiness_tools_and_authority(self):
        self.assertEqual(self.validate_bound_trial(self.valid_trial()), [])

        mutations = (
            ("requirements_sha256", "8" * 64, "requirements_binding_mismatch"),
            ("target_profile_id", "wrong-profile", "target_profile_mismatch"),
            ("runner_authority_id", "wrong-authority", "runner_authority_mismatch"),
            ("allowed_tools", ["Generic browser"], "allowed_tools_mismatch"),
        )
        for field, value, expected_code in mutations:
            with self.subTest(field=field):
                trial = self.valid_trial()
                trial[field] = value
                self.assertIn(expected_code, {item.code for item in self.validate_bound_trial(trial)})

        for field in (
            "baseline_confirmed",
            "prerequisites_confirmed",
            "tools_confirmed",
            "inputs_confirmed",
        ):
            with self.subTest(readiness=field):
                trial = self.valid_trial()
                trial["entry_readiness"][field] = False
                self.assertIn(
                    "entry_readiness_failed",
                    {item.code for item in self.validate_bound_trial(trial)},
                )

    def test_transfer_task_rejects_filename_swaps_same_decision_and_hash_reuse(self):
        cases = []
        missing_change = self.valid_trial()
        missing_change["transfer_task"]["changed_conditions"] = []
        cases.append((missing_change, "transfer_conditions_missing"))

        filename_only = self.valid_trial()
        condition = filename_only["transfer_task"]["changed_conditions"][0]
        condition["before_decision"] = "Approve the same campaign."
        condition["after_decision"] = "Approve the same campaign."
        cases.append((filename_only, "transfer_judgment_unchanged"))

        renamed_file = self.valid_trial()
        condition = renamed_file["transfer_task"]["changed_conditions"][0]
        condition["before_value"] = condition["after_value"]
        cases.append((renamed_file, "transfer_conditions_missing"))

        reused = self.valid_trial()
        held_out = next(item for item in reused["evidence_bindings"] if item["role"] == "held-out-output")
        next(item for item in reused["evidence_bindings"] if item["role"] == "answer-key-output")["sha256"] = held_out["sha256"]
        cases.append((reused, "transfer_hash_reused"))

        chain_gap = self.valid_trial()
        chain_gap["actions"][1]["input_evidence_id"] = "demo-input"
        chain_gap["actions"][1]["id"] = trial_action_id(chain_gap["actions"][1])
        chain_gap["criterion_evidence"][0]["action_id"] = chain_gap["actions"][1]["id"]
        cases.append((chain_gap, "transfer_action_chain_invalid"))

        sequence_id = self.valid_trial()
        sequence_id["actions"][1]["id"] = "action-2"
        sequence_id["criterion_evidence"][0]["action_id"] = "action-2"
        cases.append((sequence_id, "trial_action_id_invalid"))

        generic = self.valid_trial()
        generic["actions"][1]["action"] = "complete task"
        generic["actions"][1]["decision"] = "do the thing"
        generic["actions"][1]["observable_result"] = "done"
        cases.append((generic, "generic_trial_action"))

        generic_words = self.valid_trial()
        generic_words["actions"][1]["action"] = "Complete the assigned task successfully now."
        generic_words["actions"][1]["decision"] = "Do the assigned work successfully now."
        generic_words["actions"][1]["observable_result"] = "Finish the assigned task successfully now."
        cases.append((generic_words, "generic_trial_action"))

        for trial, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                self.assertIn(expected_code, {item.code for item in self.validate_bound_trial(trial)})

    def test_criterion_evidence_exactly_covers_governed_capabilities_and_real_actions(self):
        cases = []
        missing = self.valid_trial()
        missing["criterion_evidence"] = []
        cases.append((missing, "criterion_evidence_incomplete"))

        duplicate = self.valid_trial()
        duplicate["criterion_evidence"].append(copy.deepcopy(duplicate["criterion_evidence"][0]))
        cases.append((duplicate, "criterion_evidence_duplicate"))

        unknown = self.valid_trial()
        unknown["criterion_evidence"][0]["criterion_id"] = "unknown-criterion"
        cases.append((unknown, "criterion_evidence_unknown"))

        unknown_action = self.valid_trial()
        unknown_action["criterion_evidence"][0]["action_id"] = "missing-action"
        cases.append((unknown_action, "criterion_action_invalid"))

        failed_action = self.valid_trial()
        failed_action["actions"][1]["result"] = "FAIL"
        cases.append((failed_action, "criterion_action_invalid"))

        for trial, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                self.assertIn(expected_code, {item.code for item in self.validate_bound_trial(trial)})

    def prepared_g4_route(self, root, *, pilot_actor_ids=None, trial=None):
        from tests.test_course_production import CourseProductionTests

        helper = CourseProductionTests("test_pilot_selector_chooses_highest_combined_risk_then_dependency")
        contract = self.make_contract_at_g4()
        trial = self.valid_trial() if trial is None else copy.deepcopy(trial)
        self.bind_governed_trial_design(root, contract, trial)
        self.materialize_trial_inputs(root, trial)
        transfer_refs = self.materialize_transfer_artifacts(root, trial)
        pilot = helper.valid_pilot()
        pilot["trial_context_id"] = trial["isolated_context_id"]
        _, accessibility_ref, pilot["accessibility_report"] = helper.materialize_accessibility_report(
            root,
            "G4",
            [{"id": pilot["unit_id"], "path": pilot["html_path"]}],
            "accessibility-g4-unit-1",
        )
        if pilot_actor_ids is not None:
            pilot["production_actor_ids"] = pilot_actor_ids
        pilot_ref = materialize_json_evidence(
            root, evidence_id="attack-pilot", gate_id="G4", kind="pilot_record",
            relative_path="evidence/attack-pilot.json",
            value={"pilot": pilot, "lesson": helper.lesson_record(), "asset_manifest": helper.valid_asset_manifest()},
        )
        roster_ref = materialize_json_evidence(
            root, evidence_id="attack-roster", gate_id="G0", kind="production_role_roster",
            relative_path="evidence/attack-roster.json",
            value={"schema_version": 1, "authors": ["course-author-01", "page-builder-01"], "validators": ["course-validator"]},
        )
        trial_ref = materialize_json_evidence(
            root, evidence_id="attack-trial", gate_id="G4", kind="independent_course_trial",
            relative_path="trials/attack.json", value=trial, maturity="INDEPENDENT_AI_VERIFIED",
        )
        receipt_ref = self.authority.issue(
            root, contract=contract, gate_id="G4",
            trial_reference=trial_ref, roster_reference=roster_ref,
            transition_references=[pilot_ref, accessibility_ref, *transfer_refs, trial_ref, roster_ref],
            runner_id=trial["participant"]["id"], session_id=trial["runner_session_id"],
            issued_at="2026-10-18T15:14:00+08:00", nonce="attack-base-nonce",
            receipt_id="attack-receipt", relative_path="receipts/attack.json",
        )
        contract["evidence_index"] = [
            item for item in contract["evidence_index"]
            if item.get("id") != "g4-pilot-production"
        ]
        contract["evidence_index"].extend([pilot_ref, accessibility_ref, *transfer_refs, roster_ref, trial_ref, receipt_ref])
        contract["governance"]["production_role_roster"] = {
            "evidence_id": roster_ref["id"], "sha256": roster_ref["sha256"]
        }
        return contract, pilot_ref, roster_ref, trial_ref, receipt_ref, trial

    def test_g4_dispatcher_replays_canonical_trial_profile_and_authority_bindings(self):
        for field, value in (
            ("target_profile_id", "wrong-profile"),
            ("runner_authority_id", "wrong-authority"),
            ("requirements_sha256", "8" * 64),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                trial = self.valid_trial()
                contract, pilot_ref, roster_ref, trial_ref, receipt_ref, bound = (
                    self.prepared_g4_route(root, trial=trial)
                )
                bound[field] = value
                trial_ref = materialize_json_evidence(
                    root,
                    evidence_id=f"bad-{field}-trial",
                    gate_id="G4",
                    kind="independent_course_trial",
                    relative_path=f"trials/bad-{field}.json",
                    value=bound,
                    maturity="INDEPENDENT_AI_VERIFIED",
                )
                receipt_ref = self.authority.issue(
                    root,
                    contract=contract,
                    gate_id="G4",
                    trial_reference=trial_ref,
                    roster_reference=roster_ref,
                    transition_references=[
                        pilot_ref,
                        next(
                            item for item in contract["evidence_index"]
                            if item.get("id") == "accessibility-g4-unit-1"
                        ),
                        *[
                            item for item in contract["evidence_index"]
                            if item.get("kind") == "trial_transfer_artifact"
                        ],
                        trial_ref,
                        roster_ref,
                    ],
                    runner_id=bound["participant"]["id"],
                    session_id=bound["runner_session_id"],
                    issued_at="2026-10-18T15:14:00+08:00",
                    nonce=f"bad-{field}-nonce",
                    receipt_id=f"bad-{field}-receipt",
                    relative_path=f"receipts/bad-{field}.json",
                )
                contract["evidence_index"].extend([trial_ref, receipt_ref])

                result = route_verified_trial_to_gate(
                    contract,
                    "G4",
                    [pilot_ref["id"], roster_ref["id"]],
                    trial_ref["id"],
                    receipt_ref["id"],
                    "course-validator",
                    "2026-10-18T15:15:00+08:00",
                    workspace_root=root,
                )

                self.assertEqual(result, "BLOCKED")
                self.assertNotEqual(contract["gates"]["G4"]["status"], "PASS")

    def test_g4_accessibility_report_must_exist_and_match_indexed_hash(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, pilot_ref, roster_ref, trial_ref, receipt_ref, _ = (
                self.prepared_g4_route(root)
            )
            accessibility_ref = next(
                item for item in contract["evidence_index"]
                if item.get("kind") == "accessibility_report"
            )
            report_path = root / accessibility_ref["path"]
            report_path.write_text(
                report_path.read_text(encoding="utf-8") + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ContractStateError, "invalid Gate evidence"):
                route_verified_trial_to_gate(
                    contract,
                    "G4",
                    [pilot_ref["id"], roster_ref["id"]],
                    trial_ref["id"],
                    receipt_ref["id"],
                    "course-validator",
                    "2026-10-18T15:15:00+08:00",
                    workspace_root=root,
                )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, pilot_ref, roster_ref, trial_ref, receipt_ref, _ = (
                self.prepared_g4_route(root)
            )
            contract["evidence_index"] = [
                item for item in contract["evidence_index"]
                if item.get("kind") != "accessibility_report"
            ]
            with self.assertRaisesRegex(
                ContractStateError, "exactly one typed accessibility report"
            ):
                route_verified_trial_to_gate(
                    contract,
                    "G4",
                    [pilot_ref["id"], roster_ref["id"]],
                    trial_ref["id"],
                    receipt_ref["id"],
                    "course-validator",
                    "2026-10-18T15:15:00+08:00",
                    workspace_root=root,
                )

    def test_failed_signed_trial_routes_to_earliest_responsible_gate_atomically(self):
        trial = self.valid_trial()
        trial["result"] = {
            "status": "FAIL",
            "completed_at": "2026-10-18T15:10:00+08:00",
            "notes": "來源已改版，依現有教材無法完成。",
        }
        trial["blocks"] = [
            {
                "code": "source_mismatch",
                "detail": "教材來源與實際工具行為不一致。",
                "recovered": False,
            }
        ]
        trial["recovery"] = []

        blocker_ids = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (
                base_contract,
                pilot_ref,
                roster_ref,
                trial_ref,
                receipt_ref,
                materialized_trial,
            ) = self.prepared_g4_route(root, trial=trial)
            for run in range(2):
                with self.subTest(run=run):
                    contract = copy.deepcopy(base_contract)
                    indexed_before = copy.deepcopy(contract["evidence_index"])

                    result = route_verified_trial_to_gate(
                        contract,
                        "G4",
                        [pilot_ref["id"], roster_ref["id"]],
                        trial_ref["id"],
                        receipt_ref["id"],
                        "course-validator",
                        "2026-10-18T15:15:00+08:00",
                        workspace_root=root,
                    )

                    self.assertEqual(result, "BLOCKED")
                    self.assertEqual(contract["evidence_index"], indexed_before)
                    self.assertEqual(materialized_trial["result"]["status"], "FAIL")
                    self.assertEqual(contract["gates"]["G1"]["status"], "IN_PROGRESS")
                    self.assertTrue(
                        all(
                            contract["gates"][gate_id]["status"] == "STALE"
                            for gate_id in GATE_ORDER[2:]
                        )
                    )
                    blockers = [
                        risk
                        for risk in contract["gates"]["G1"]["risks"]
                        if risk.get("kind") == "gate_blocker"
                        and risk.get("resolved") is False
                    ]
                    self.assertEqual(len(blockers), 1)
                    blocker_ids.append(blockers[0]["id"])

                    event = contract["gates"]["G1"]["evidence"][-1]
                    self.assertEqual(event["kind"], "gate_validation")
                    self.assertEqual(event["outcome"], "FAIL")
                    self.assertEqual(event["source_gate"], "G4")
                    self.assertEqual(event["return_gate"], "G1")
                    self.assertIn(
                        {
                            "code": "unrecovered_trial_block",
                            "path": "$.blocks[0]",
                            "message": "a trial with an unrecovered block cannot pass",
                            "return_gate": "G1",
                        },
                        event["issues"],
                    )
                    self.assertEqual(
                        set(event["evidence_ids"]),
                        {
                            pilot_ref["id"],
                            "accessibility-g4-unit-1",
                            *{item["evidence_id"] for item in trial["evidence_bindings"]},
                            trial_ref["id"],
                            receipt_ref["id"],
                        },
                    )
                    self.assertEqual(
                        {item["id"] for item in event["consumed_evidence"]},
                        {
                            "governed-g0-requirements",
                            "governed-g2-blueprint",
                            pilot_ref["id"],
                            "accessibility-g4-unit-1",
                            *{item["evidence_id"] for item in trial["evidence_bindings"]},
                            roster_ref["id"],
                            trial_ref["id"],
                            receipt_ref["id"],
                        },
                    )
                    self.assertEqual(
                        event["trial_result"],
                        materialized_trial["result"],
                    )
                    self.assertEqual(
                        contract["consumed_trial_receipts"][0]["receipt_id"],
                        receipt_ref["id"],
                    )
                    self.assertEqual(validate_contract(contract), [])

                    resolution_ref = materialize_json_evidence(
                        root,
                        evidence_id=f"g1-route-resolution-{run}",
                        gate_id="G1",
                        kind="blocker_resolution",
                        relative_path=f"evidence/g1-route-resolution-{run}.json",
                        value={"resolution": "重新研究來源並更新教材。"},
                    )
                    contract["evidence_index"].append(resolution_ref)
                    resolve_gate_blocker(
                        contract,
                        "G1",
                        blockers[0]["id"],
                        "已更新來源與教材。",
                        [resolution_ref["id"]],
                        "course-researcher",
                        "2026-10-18T15:30:00+08:00",
                        workspace_root=root,
                    )
                    self.assertEqual(contract["gates"]["G1"]["status"], "IN_PROGRESS")
                    self.assertTrue(blockers[0]["resolved"])
                    self.assertIn(event, contract["gates"]["G1"]["evidence"])
                    self.assertEqual(validate_contract(contract), [])

        self.assertEqual(blocker_ids[0], blocker_ids[1])

    def test_failed_trial_generic_issue_stays_at_current_trial_gate(self):
        for scope, block_code, expected_gate in (
            ("representative_unit", "interface_block", "G4"),
            ("full_course", "full_course_integration", "G5"),
        ):
            with self.subTest(scope=scope):
                trial = self.valid_trial(scope=scope)
                trial["result"]["status"] = "FAIL"
                trial["blocks"] = [
                    {
                        "code": block_code,
                        "detail": "本 Gate 的 trial failure。",
                        "recovered": False,
                    }
                ]
                trial["recovery"] = []

                issues = validate_trial_record(trial, [], scope)
                by_code = {issue.code: issue for issue in issues}

                self.assertEqual(
                    by_code["trial_result_failed"].return_gate,
                    expected_gate,
                )
                self.assertEqual(
                    by_code["unrecovered_trial_block"].return_gate,
                    expected_gate,
                )

    def test_failed_signed_interface_trial_blocks_g4_without_rewinding_g3(self):
        trial = self.valid_trial()
        trial["result"]["status"] = "FAIL"
        trial["blocks"] = [
            {
                "code": "interface_block",
                "detail": "學員介面阻擋操作。",
                "recovered": False,
            }
        ]
        trial["recovery"] = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, pilot_ref, roster_ref, trial_ref, receipt_ref, _ = (
                self.prepared_g4_route(root, trial=trial)
            )

            result = route_verified_trial_to_gate(
                contract,
                "G4",
                [pilot_ref["id"], roster_ref["id"]],
                trial_ref["id"],
                receipt_ref["id"],
                "course-validator",
                "2026-10-18T15:15:00+08:00",
                workspace_root=root,
            )

        self.assertEqual(result, "BLOCKED")
        self.assertEqual(contract["gates"]["G3"]["status"], "PASS")
        self.assertEqual(contract["gates"]["G4"]["status"], "BLOCKED")

    def test_failed_trial_route_exception_leaves_original_contract_unchanged(self):
        trial = self.valid_trial()
        trial["result"]["status"] = "FAIL"
        trial["blocks"][0]["recovered"] = False
        trial["recovery"] = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, pilot_ref, roster_ref, trial_ref, receipt_ref, _ = (
                self.prepared_g4_route(root, trial=trial)
            )
            before = copy.deepcopy(contract)
            with patch(
                "src.course_gate_failure.record_gate_blocker",
                side_effect=ContractStateError("injected mutation failure"),
            ):
                with self.assertRaisesRegex(ContractStateError, "injected mutation failure"):
                    route_verified_trial_to_gate(
                        contract,
                        "G4",
                        [pilot_ref["id"], roster_ref["id"]],
                        trial_ref["id"],
                        receipt_ref["id"],
                        "course-validator",
                        "2026-10-18T15:15:00+08:00",
                        workspace_root=root,
                    )
            self.assertEqual(contract, before)

    def assert_g4_security_rejected_without_mutation(
        self, contract, root, pilot_ref, roster_ref, trial_id, receipt_id
    ):
        before = copy.deepcopy(contract)
        with self.assertRaises(ContractStateError):
            route_verified_trial_to_gate(
                contract, "G4", [pilot_ref["id"], roster_ref["id"]],
                trial_id, receipt_id, "course-validator",
                "2026-10-18T15:15:00+08:00", workspace_root=root,
            )
        self.assertEqual(contract, before)

    def test_trial_actor_cannot_be_any_course_author_or_validator(self):
        production_roles = {
            "schema_version": 1,
            "authors": ["course-author-01"],
            "validators": ["course-validator-01"],
        }
        for participant_id in ("course-author-01", "course-validator-01"):
            with self.subTest(participant_id=participant_id):
                record = self.valid_trial()
                record["participant"]["id"] = participant_id
                codes = {
                    issue.code
                    for issue in validate_trial_record(
                        record, production_roles, "representative_unit"
                    )
                }
                self.assertIn("independent_participant_required", codes)

        record = self.valid_trial()
        record["participant"]["roles"] = ["learner-trial", "course-validator"]
        codes = {
            issue.code
            for issue in validate_trial_record(record, [], "representative_unit")
        }
        self.assertIn("independent_participant_required", codes)

    def test_trial_rejects_author_notes_contract_or_answer_key_access(self):
        forbidden = (
            ("author-notes", "internal/author-notes.md"),
            ("course-contract", "course-contract.json"),
            ("answer-key", "internal/answer-key.pdf"),
        )
        for kind, path in forbidden:
            with self.subTest(kind=kind):
                record = self.valid_trial()
                record["allowed_inputs"].append(
                    {"kind": kind, "path": path, "sha256": "d" * 64}
                )
                codes = {
                    issue.code
                    for issue in validate_trial_record(
                        record, [], "representative_unit"
                    )
                }
                self.assertIn("non_learner_input_accessed", codes)

    def test_trial_records_entry_actions_hints_blocks_recovery_artifact_and_result(self):
        required = (
            "entry",
            "actions",
            "hints",
            "blocks",
            "recovery",
            "artifact",
            "result",
        )
        for field in required:
            with self.subTest(field=field):
                record = self.valid_trial()
                del record[field]
                paths = {
                    issue.path
                    for issue in validate_trial_record(
                        record, [], "representative_unit"
                    )
                }
                self.assertTrue(any(path.startswith(f"$.{field}") for path in paths))

        record = self.valid_trial()
        record["actions"][1]["sequence"] = 1
        codes = {
            issue.code
            for issue in validate_trial_record(record, [], "representative_unit")
        }
        self.assertIn("actions_not_chronological", codes)

    def test_incomplete_or_unverifiable_artifact_fails_trial(self):
        mutations = (
            ("complete", False),
            ("verifiable", False),
            ("acceptance_result", "FAIL"),
            ("sha256", "not-a-hash"),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                record = self.valid_trial()
                record["artifact"][field] = value
                codes = {
                    issue.code
                    for issue in validate_trial_record(
                        record, [], "representative_unit"
                    )
                }
                self.assertIn("artifact_not_verified", codes)

    def test_failure_code_routes_to_responsible_g1_through_g6_gate(self):
        expected = {
            "source_mismatch": "G1",
            "tool_behavior_mismatch": "G1",
            "sequence_overload": "G2",
            "difficulty_mismatch": "G2",
            "explanation_gap": "G3",
            "practice_instruction_gap": "G3",
            "interface_block": "G4",
            "asset_missing": "G4",
            "full_course_integration": "G5",
            "access_denied": "G6",
            "deployment_failure": "G6",
        }
        self.assertEqual(
            {code: route_trial_failure(code) for code in expected}, expected
        )
        with self.assertRaises(ValueError):
            route_trial_failure("unclassified_problem")

    def test_ai_trial_can_only_reach_independent_ai_verified(self):
        self.assertEqual(
            evidence_maturity(self.valid_trial()), "INDEPENDENT_AI_VERIFIED"
        )

        record = self.valid_trial()
        record["result"]["status"] = "FAIL"
        self.assertEqual(evidence_maturity(record), "EXECUTION_VALIDATED")

    def test_human_claims_remain_pending_without_governed_target_profile_evidence(self):
        record = self.valid_trial(participant_type="human")
        self.assertEqual(evidence_maturity(record), "PENDING_HUMAN")

        del record["human_participant_evidence"]
        self.assertEqual(evidence_maturity(record), "EXECUTION_VALIDATED")

    def test_ai_completion_time_does_not_claim_human_duration_or_readability(self):
        record = self.valid_trial()
        record["entry"]["started_at"] = "2026-10-18T15:00:00+08:00"
        record["result"]["completed_at"] = "2026-10-18T15:01:00+08:00"

        self.assertEqual(evidence_maturity(record), "INDEPENDENT_AI_VERIFIED")
        self.assertEqual(record["maturity_claims"]["human_duration"], "PENDING_HUMAN")
        self.assertEqual(record["maturity_claims"]["human_readability"], "PENDING_HUMAN")
        self.assertEqual(
            record["maturity_claims"]["target_learner_independence"],
            "PENDING_HUMAN",
        )

    def test_g4_g5_trial_reference_maturity_is_derived_and_cannot_be_polluted(self):
        trial = self.valid_trial()
        for gate_id in ("G4", "G5"):
            for maturity in (None, "HUMAN_VERIFIED", "PENDING_HUMAN"):
                with self.subTest(gate_id=gate_id, maturity=maturity):
                    reference = {
                        "id": f"trial-{gate_id.lower()}", "gate": gate_id,
                        "kind": "independent_course_trial", "path": "trial.json",
                        "sha256": "a" * 64,
                    }
                    if maturity is not None:
                        reference["maturity"] = maturity
                    consumed = ConsumedEvidence(reference, b"{}", "a" * 64, trial)
                    with self.assertRaisesRegex(ValueError, "must exactly match"):
                        validated_trial_reference_maturity(
                            trial, {"independent_course_trial": [consumed]}
                        )

    def test_g4_secure_transfer_artifact_missing_or_wrong_hash_blocks_without_mutation(self):
        for mutation in ("missing", "wrong-hash"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                contract, pilot_ref, roster_ref, trial_ref, receipt_ref, trial = self.prepared_g4_route(root)
                final_binding = next(item for item in trial["evidence_bindings"] if item["role"] == "held-out-output")
                if mutation == "missing":
                    (root / final_binding["path"]).unlink()
                else:
                    indexed = next(item for item in contract["evidence_index"] if item.get("id") == final_binding["evidence_id"])
                    indexed["sha256"] = "f" * 64
                before = copy.deepcopy(contract)
                with self.assertRaises(ContractStateError):
                    route_verified_trial_to_gate(
                        contract, "G4", [pilot_ref["id"], roster_ref["id"]],
                        trial_ref["id"], receipt_ref["id"], "course-validator",
                        "2026-10-18T15:15:00+08:00", workspace_root=root,
                    )
                self.assertEqual(contract, before)

    def test_g5_trial_uses_new_isolated_context_and_full_course_scope(self):
        record = self.valid_trial(scope="full_course")
        record["isolated_context_id"] = "pilot-cold-run-20261018-01"

        issues = validate_trial_record(record, [], "full_course")
        self.assertEqual(issues, [])

        context_issues = validate_trial_context_is_new(
            record, ["pilot-cold-run-20261018-01"]
        )
        self.assertIn(
            "g5_trial_context_invalid", {issue.code for issue in context_issues}
        )

        record["isolated_context_id"] = "full-course-cold-run-20261018-02"
        self.assertEqual(
            validate_trial_context_is_new(record, ["pilot-cold-run-20261018-01"]),
            [],
        )

        record["scope"] = "representative_unit"
        codes = {
            issue.code for issue in validate_trial_record(record, [], "full_course")
        }
        self.assertIn("trial_scope_mismatch", codes)

    def make_contract_at_g4(self):
        contract = new_contract(
            "trial-course",
            "試走課程",
            "course-run",
            "2026-10-18T12:00:00+08:00",
        )
        self.authority.bind(contract)
        for gate_id in GATE_ORDER[:4]:
            begin_gate(contract, gate_id, "course-run", "2026-10-18T12:01:00+08:00")
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
                "2026-10-18T12:02:00+08:00",
            )
        begin_gate(contract, "G4", "course-run", "2026-10-18T15:00:00+08:00")
        contract["evidence_index"].append(
            {
                "id": "g4-pilot-production",
                "gate": "G4",
                "kind": "pilot_production",
                "path": "evidence/g4-pilot-production.json",
                "sha256": "e" * 64,
            }
        )
        return contract

    def test_g4_pass_requires_composed_production_and_independent_trial_evidence(self):
        from tests.test_course_production import CourseProductionTests

        helper = CourseProductionTests("test_pilot_selector_chooses_highest_combined_risk_then_dependency")
        contract = self.make_contract_at_g4()
        trial = self.valid_trial()
        pilot = helper.valid_pilot()
        pilot["trial_context_id"] = trial["isolated_context_id"]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.bind_governed_trial_design(root, contract, trial)
            self.materialize_trial_inputs(root, trial)
            transfer_refs = self.materialize_transfer_artifacts(root, trial)
            _, accessibility_ref, pilot["accessibility_report"] = helper.materialize_accessibility_report(
                root,
                "G4",
                [{"id": pilot["unit_id"], "path": pilot["html_path"]}],
                "accessibility-g4-unit-1",
            )
            pilot_ref = materialize_json_evidence(
                root,
                evidence_id="g4-pilot-record",
                gate_id="G4",
                kind="pilot_record",
                relative_path="evidence/g4-pilot-record.json",
                value={
                    "pilot": pilot,
                    "lesson": helper.lesson_record(),
                    "asset_manifest": helper.valid_asset_manifest(),
                },
            )
            roster_ref = materialize_json_evidence(
                root,
                evidence_id="g4-production-role-roster",
                gate_id="G0",
                kind="production_role_roster",
                relative_path="evidence/g4-production-role-roster.json",
                value={
                    "schema_version": 1,
                    "authors": ["course-author-01", "page-builder-01"],
                    "validators": ["course-validator"],
                },
            )
            contract["evidence_index"] = [
                item
                for item in contract["evidence_index"]
                if item.get("id") != "g4-pilot-production"
            ]
            contract["evidence_index"].extend([pilot_ref, roster_ref])
            contract["governance"]["production_role_roster"] = {
                "evidence_id": roster_ref["id"], "sha256": roster_ref["sha256"]
            }
            trial_ref = materialize_json_evidence(
                root,
                evidence_id="g4-trial-source",
                gate_id="G4",
                kind="independent_course_trial",
                relative_path="trials/g4-representative-unit.json",
                value=trial,
                maturity="INDEPENDENT_AI_VERIFIED",
            )
            receipt_ref = self.authority.issue(
                root, contract=contract, gate_id="G4",
                trial_reference=trial_ref, roster_reference=roster_ref,
                transition_references=[pilot_ref, accessibility_ref, *transfer_refs, trial_ref, roster_ref],
                runner_id=trial["participant"]["id"],
                session_id=trial["runner_session_id"],
                issued_at="2026-10-18T15:14:00+08:00", nonce="g4-positive-nonce",
                receipt_id="g4-trial-receipt", relative_path="receipts/g4.json",
            )
            contract["evidence_index"].extend([accessibility_ref, *transfer_refs, trial_ref, receipt_ref])

            result = route_verified_trial_to_gate(
                contract,
                "G4",
                [pilot_ref["id"], roster_ref["id"]],
                trial_ref["id"],
                receipt_ref["id"],
                "course-validator",
                "2026-10-18T15:15:00+08:00",
                workspace_root=root,
            )

            self.assertEqual(result, "PASS")
            self.assertEqual(contract["gates"]["G4"]["status"], "PASS")
            self.assertEqual(contract["revision"], 0)
            self.assertEqual(
                contract["consumed_trial_receipts"],
                [{
                    "receipt_id": receipt_ref["id"],
                    "nonce": "g4-positive-nonce",
                    "gate": "G4",
                    "consumed_at": "2026-10-18T15:15:00+08:00",
                }],
            )
            event = contract["gates"]["G4"]["evidence"][-1]
            self.assertEqual(event["maturity"], "INDEPENDENT_AI_VERIFIED")
            self.assertNotIn("human_duration", event)
            self.assertNotIn("human_readability", event)
            self.assertNotIn("target_learner_independence", event)
            self.assertIn("g4-pilot-record", event["evidence_ids"])
            self.assertEqual(
                event["consumed_inputs"],
                [
                    {"path": item["path"], "sha256": item["sha256"]}
                    for item in sorted(trial["allowed_inputs"], key=lambda item: (item["kind"], item["path"], item["sha256"]))
                ],
            )
            trial_refs = [
                item
                for item in contract["evidence_index"]
                if item.get("kind") == "independent_course_trial"
            ]
            self.assertEqual(len(trial_refs), 1)
            self.assertEqual(
                verify_evidence_reference(root, trial_refs[0], expected_gate="G4"),
                [],
            )

            replay_contract = copy.deepcopy(contract)
            replay_contract["revision"] = 0
            replay_contract["gates"]["G4"]["status"] = "IN_PROGRESS"
            replay_before = copy.deepcopy(replay_contract)
            with self.assertRaisesRegex(ContractStateError, "already consumed"):
                route_verified_trial_to_gate(
                    replay_contract, "G4", [pilot_ref["id"], roster_ref["id"]],
                    trial_ref["id"], receipt_ref["id"], "course-validator",
                    "2026-10-18T15:16:00+08:00", workspace_root=root,
                )
            self.assertEqual(replay_contract, replay_before)

            author_trial = self.valid_trial()
            author_trial["participant"]["id"] = "course-author-01"
            self.materialize_trial_inputs(root, author_trial)
            pilot["trial_context_id"] = author_trial["isolated_context_id"]
            author_contract = self.make_contract_at_g4()
            author_contract["evidence_index"] = [
                item
                for item in author_contract["evidence_index"]
                if item.get("id") != "g4-pilot-production"
            ]
            author_pilot_ref = materialize_json_evidence(
                root,
                evidence_id="g4-author-pilot-record",
                gate_id="G4",
                kind="pilot_record",
                relative_path="evidence/g4-author-pilot-record.json",
                value={
                    "pilot": pilot,
                    "lesson": helper.lesson_record(),
                    "asset_manifest": helper.valid_asset_manifest(),
                },
            )
            author_roster_ref = materialize_json_evidence(
                root,
                evidence_id="g4-author-production-role-roster",
                gate_id="G0",
                kind="production_role_roster",
                relative_path="evidence/g4-author-production-role-roster.json",
                value={
                    "schema_version": 1,
                    "authors": ["course-author-01"],
                    "validators": ["course-validator"],
                },
            )
            author_contract["evidence_index"].extend(
                [author_pilot_ref, author_roster_ref]
            )
            author_contract["governance"]["production_role_roster"] = {
                "evidence_id": author_roster_ref["id"], "sha256": author_roster_ref["sha256"]
            }
            author_trial_ref = materialize_json_evidence(
                root,
                evidence_id="g4-author-trial-source",
                gate_id="G4",
                kind="independent_course_trial",
                relative_path="trials/g4-author-representative-unit.json",
                value=author_trial,
                maturity="INDEPENDENT_AI_VERIFIED",
            )
            forged_receipt = {
                "schema_version": 1, "authority_id": self.authority_id,
                "algorithm": "HMAC-SHA256", "gate": "G4",
                "trial_evidence_id": author_trial_ref["id"], "trial_sha256": author_trial_ref["sha256"],
                "roster_sha256": author_roster_ref["sha256"],
                "learner_input_manifest": sorted(author_trial["allowed_inputs"], key=lambda item: (item["kind"], item["path"], item["sha256"])),
                "runner": {"id": "course-author-01", "role": "isolated-learner-runner"},
                "participant": author_trial["participant"],
                "session_id": author_trial["runner_session_id"],
                "isolated_context_id": author_trial["isolated_context_id"],
                "issuer": self.authority_id, "nonce": "forged", "issued_at": "2026-10-18T15:15:00+08:00",
                "signature": "0" * 64,
            }
            author_receipt_ref = materialize_json_evidence(
                root, evidence_id="g4-author-forged-receipt", gate_id="G4",
                kind="independent_trial_receipt", relative_path="receipts/g4-author.json",
                value=forged_receipt,
            )
            author_contract["evidence_index"].extend([author_trial_ref, author_receipt_ref])

            author_before = copy.deepcopy(author_contract)
            with self.assertRaises(ContractStateError):
                route_verified_trial_to_gate(
                    author_contract,
                    "G4",
                    [author_pilot_ref["id"], author_roster_ref["id"]],
                    author_trial_ref["id"],
                    author_receipt_ref["id"],
                    "course-validator",
                    "2026-10-18T15:16:00+08:00",
                    workspace_root=root,
                )
            self.assertEqual(author_contract, author_before)

        no_production = self.make_contract_at_g4()
        with self.assertRaises(ValueError):
            route_verified_trial_to_gate(
                no_production,
                "G4",
                [],
                "missing-trial",
                "missing-receipt",
                "course-validator",
                "2026-10-18T15:15:00+08:00",
                workspace_root=Path("."),
            )

    def test_forged_author_alias_and_self_signed_receipt_leave_contract_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, pilot_ref, roster_ref, _, _, trial = self.prepared_g4_route(root)
            trial["participant"]["id"] = "author-new-alias"
            forged_trial = materialize_json_evidence(
                root, evidence_id="forged-alias-trial", gate_id="G4",
                kind="independent_course_trial", relative_path="trials/forged-alias.json",
                value=trial, maturity="INDEPENDENT_AI_VERIFIED",
            )
            forged_receipt = materialize_json_evidence(
                root, evidence_id="forged-alias-receipt", gate_id="G4",
                kind="independent_trial_receipt", relative_path="receipts/forged-alias.json",
                value={
                    "schema_version": 1, "authority_id": self.authority_id,
                    "algorithm": "HMAC-SHA256", "gate": "G4",
                    "trial_evidence_id": forged_trial["id"], "trial_sha256": forged_trial["sha256"],
                    "roster_sha256": roster_ref["sha256"],
                    "learner_input_manifest": sorted(trial["allowed_inputs"], key=lambda item: (item["kind"], item["path"], item["sha256"])),
                    "runner": {"id": "author-new-alias", "role": "isolated-learner-runner"},
                    "participant": trial["participant"], "session_id": trial["runner_session_id"],
                    "isolated_context_id": trial["isolated_context_id"], "issuer": self.authority_id,
                    "nonce": "attacker-nonce", "issued_at": "2026-10-18T15:14:00+08:00",
                    "signature": "0" * 64,
                },
            )
            contract["evidence_index"].extend([forged_trial, forged_receipt])
            self.assert_g4_security_rejected_without_mutation(
                contract, root, pilot_ref, roster_ref, forged_trial["id"], forged_receipt["id"]
            )

    def test_receipt_and_trial_file_tamper_leave_contract_unchanged(self):
        for target_kind in ("receipt", "trial"):
            with self.subTest(target_kind=target_kind), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                contract, pilot_ref, roster_ref, trial_ref, receipt_ref, _ = self.prepared_g4_route(root)
                target_ref = receipt_ref if target_kind == "receipt" else trial_ref
                (root / target_ref["path"]).write_text('{"tampered":true}\n', encoding="utf-8")
                self.assert_g4_security_rejected_without_mutation(
                    contract, root, pilot_ref, roster_ref, trial_ref["id"], receipt_ref["id"]
                )

    def test_learner_input_tamper_after_receipt_leaves_contract_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, pilot_ref, roster_ref, trial_ref, receipt_ref, trial = self.prepared_g4_route(root)
            (root / trial["allowed_inputs"][0]["path"]).write_text(
                "tampered learner input\n", encoding="utf-8"
            )
            self.assert_g4_security_rejected_without_mutation(
                contract, root, pilot_ref, roster_ref, trial_ref["id"], receipt_ref["id"]
            )

    def test_cross_session_receipt_replay_leaves_contract_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, pilot_ref, roster_ref, _, receipt_ref, trial = self.prepared_g4_route(root)
            trial["runner_session_id"] = "different-session"
            replay_trial = materialize_json_evidence(
                root, evidence_id="replay-trial", gate_id="G4",
                kind="independent_course_trial", relative_path="trials/replay.json",
                value=trial, maturity="INDEPENDENT_AI_VERIFIED",
            )
            contract["evidence_index"].append(replay_trial)
            self.assert_g4_security_rejected_without_mutation(
                contract, root, pilot_ref, roster_ref, replay_trial["id"], receipt_ref["id"]
            )

    def test_contract_instance_and_revision_replay_leave_contract_unchanged(self):
        for field, replacement in (
            ("contract_instance_id", "ci-" + "f" * 32),
            ("revision", 1),
            ("contract_instance_id", None),
        ):
            with self.subTest(field=field, replacement=replacement), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                contract, pilot_ref, roster_ref, trial_ref, receipt_ref, _ = self.prepared_g4_route(root)
                contract[field] = replacement
                self.assert_g4_security_rejected_without_mutation(
                    contract, root, pilot_ref, roster_ref, trial_ref["id"], receipt_ref["id"]
                )

    def test_receipt_rejects_changed_transition_evidence_set_without_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, pilot_ref, roster_ref, trial_ref, receipt_ref, _ = self.prepared_g4_route(root)
            extra = materialize_json_evidence(
                root, evidence_id="unexpected-g4-evidence", gate_id="G4",
                kind="test_record", relative_path="evidence/unexpected.json",
                value={"unexpected": True},
            )
            contract["evidence_index"].append(extra)
            before = copy.deepcopy(contract)
            with self.assertRaisesRegex(ContractStateError, "exact transition evidence set"):
                route_verified_trial_to_gate(
                    contract, "G4", [pilot_ref["id"], extra["id"], roster_ref["id"]],
                    trial_ref["id"], receipt_ref["id"], "course-validator",
                    "2026-10-18T15:15:00+08:00", workspace_root=root,
                )
            self.assertEqual(contract, before)

    def test_cross_gate_receipt_replay_leaves_contract_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, pilot_ref, roster_ref, trial_ref, receipt_ref, _ = self.prepared_g4_route(root)
            replay_receipt = copy.deepcopy(receipt_ref)
            replay_receipt["id"] = "cross-gate-receipt"
            replay_receipt["gate"] = "G5"
            contract["evidence_index"].append(replay_receipt)
            self.assert_g4_security_rejected_without_mutation(
                contract, root, pilot_ref, roster_ref, trial_ref["id"], replay_receipt["id"]
            )

    def test_pilot_actor_outside_governed_roster_leaves_contract_unchanged(self):
        for actors in (["unlisted-author"], ["course-author-01"]):
            with self.subTest(actors=actors), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                contract, pilot_ref, roster_ref, trial_ref, receipt_ref, _ = self.prepared_g4_route(
                    root, pilot_actor_ids=actors
                )
                self.assert_g4_security_rejected_without_mutation(
                    contract, root, pilot_ref, roster_ref, trial_ref["id"], receipt_ref["id"]
                )

    def test_missing_receipt_leaves_contract_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract, pilot_ref, roster_ref, trial_ref, _, _ = self.prepared_g4_route(root)
            self.assert_g4_security_rejected_without_mutation(
                contract, root, pilot_ref, roster_ref, trial_ref["id"], "missing-receipt"
            )


if __name__ == "__main__":
    unittest.main()
