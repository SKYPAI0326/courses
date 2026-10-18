import copy
import hashlib
import unittest

from src.course_contract import GATE_ORDER, begin_gate, new_contract, pass_gate
from src.course_validation import (
    evidence_maturity,
    route_trial_failure,
    route_verified_trial_to_gate,
    validate_trial_context_is_new,
    validate_trial_record,
)


class CourseTrialValidationTests(unittest.TestCase):
    def valid_trial(self, participant_type="independent-ai", scope="representative_unit"):
        record = {
            "schema_version": 1,
            "scope": scope,
            "participant": {
                "id": "cold-learner-ai-01",
                "type": participant_type,
                "roles": ["learner-trial"],
            },
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

    def test_trial_actor_cannot_be_any_course_author_or_validator(self):
        authors = ["course-author-01", "course-validator-01"]
        for participant_id in authors:
            with self.subTest(participant_id=participant_id):
                record = self.valid_trial()
                record["participant"]["id"] = participant_id
                codes = {
                    issue.code
                    for issue in validate_trial_record(
                        record, authors, "representative_unit"
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
            pass_gate(
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
        contract = self.make_contract_at_g4()

        result = route_verified_trial_to_gate(
            contract,
            "G4",
            ["g4-pilot-production"],
            self.valid_trial(),
            "course-validator",
            "2026-10-18T15:15:00+08:00",
        )

        self.assertEqual(result, "PASS")
        self.assertEqual(contract["gates"]["G4"]["status"], "PASS")
        event = contract["gates"]["G4"]["evidence"][-1]
        self.assertEqual(event["maturity"], "INDEPENDENT_AI_VERIFIED")
        self.assertIn("g4-pilot-production", event["evidence_ids"])
        self.assertTrue(
            any(
                item.get("kind") == "independent_course_trial"
                for item in contract["evidence_index"]
            )
        )

        no_production = self.make_contract_at_g4()
        with self.assertRaises(ValueError):
            route_verified_trial_to_gate(
                no_production,
                "G4",
                [],
                self.valid_trial(),
                "course-validator",
                "2026-10-18T15:15:00+08:00",
            )


if __name__ == "__main__":
    unittest.main()
