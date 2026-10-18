import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.course_contract import ContractStateError, GATE_ORDER, begin_gate, new_contract
from tests.gate_test_support import _commit_gate_pass
from src.course_evidence import materialize_json_evidence, verify_evidence_reference
from src.course_validation import (
    evidence_maturity,
    route_trial_failure,
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
            "schema_version": 1,
            "scope": scope,
            "participant": {
                "id": "cold-learner-ai-01",
                "type": participant_type,
                "roles": ["learner-trial"],
            },
            "runner_session_id": "cold-session-20261018-01",
            "isolated_context_id": "cold-run-20261018-01",
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
            "forbidden_inputs_accessed": [],
            "entry": {
                "started_at": "2026-10-18T15:00:00+08:00",
                "page": "courses/demo/unit-1.html",
                "goal_understood": True,
                "materials_found": True,
            },
            "actions": [
                {
                    "sequence": 1,
                    "action": "開啟商品資料並找出預算與截止日。",
                    "observable_result": "在資料表中找到預算 20 萬元與截止日。",
                    "at": "2026-10-18T15:01:00+08:00",
                },
                {
                    "sequence": 2,
                    "action": "依講義步驟完成企劃表。",
                    "observable_result": "產出含目標、受眾、時程與預算的企劃表。",
                    "at": "2026-10-18T15:08:00+08:00",
                },
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
        }
        if participant_type == "human":
            record["participant"]["id"] = "human-trial-01"
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

    def prepared_g4_route(self, root, *, pilot_actor_ids=None):
        from tests.test_course_production import CourseProductionTests

        helper = CourseProductionTests("test_pilot_selector_chooses_highest_combined_risk_then_dependency")
        contract = self.make_contract_at_g4()
        trial = self.valid_trial()
        self.materialize_trial_inputs(root, trial)
        pilot = helper.valid_pilot()
        pilot["trial_context_id"] = trial["isolated_context_id"]
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
            transition_references=[pilot_ref, trial_ref, roster_ref],
            runner_id=trial["participant"]["id"], session_id=trial["runner_session_id"],
            issued_at="2026-10-18T15:14:00+08:00", nonce="attack-base-nonce",
            receipt_id="attack-receipt", relative_path="receipts/attack.json",
        )
        contract["evidence_index"] = [
            item for item in contract["evidence_index"]
            if item.get("id") != "g4-pilot-production"
        ]
        contract["evidence_index"].extend([pilot_ref, roster_ref, trial_ref, receipt_ref])
        contract["governance"]["production_role_roster"] = {
            "evidence_id": roster_ref["id"], "sha256": roster_ref["sha256"]
        }
        return contract, pilot_ref, roster_ref, trial_ref, receipt_ref, trial

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

    def test_human_verified_requires_explicit_human_participant_evidence(self):
        record = self.valid_trial(participant_type="human")
        self.assertEqual(evidence_maturity(record), "HUMAN_VERIFIED")

        del record["human_participant_evidence"]
        self.assertNotEqual(evidence_maturity(record), "HUMAN_VERIFIED")

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
            self.materialize_trial_inputs(root, trial)
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
                transition_references=[pilot_ref, trial_ref, roster_ref],
                runner_id=trial["participant"]["id"],
                session_id=trial["runner_session_id"],
                issued_at="2026-10-18T15:14:00+08:00", nonce="g4-positive-nonce",
                receipt_id="g4-trial-receipt", relative_path="receipts/g4.json",
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

            self.assertEqual(result, "PASS")
            self.assertEqual(contract["gates"]["G4"]["status"], "PASS")
            self.assertEqual(contract["revision"], 1)
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
