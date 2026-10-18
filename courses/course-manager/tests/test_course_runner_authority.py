import copy
import hashlib
import tempfile
import unittest
from pathlib import Path

from src.course_contract import ContractStateError, begin_gate, new_contract
from src.course_evidence import consume_evidence_reference, materialize_json_evidence
from src.course_runner_authority import (
    consume_trial_inputs,
    transition_evidence_sha256,
    verify_trial_receipt,
)
from tests.runner_authority_fixture import TestRunnerAuthority


class CourseRunnerAuthorityTests(unittest.TestCase):
    def authority(self, *, key_slot=0):
        return TestRunnerAuthority(
            "independent-lab",
            {
                "cold-runner-01": {
                    "role": "isolated-learner-runner",
                    "sessions": {
                        "session-01": {
                            "assertion_id": "assertion-session-01",
                            "context_id": "context-01",
                        }
                    },
                }
            },
            key_slot=key_slot,
        )

    def evidence(self, root):
        learner_input = root / "course" / "unit.html"
        learner_input.parent.mkdir(parents=True, exist_ok=True)
        learner_input.write_text("learner page", encoding="utf-8")
        learner_sha = hashlib.sha256(learner_input.read_bytes()).hexdigest()
        roster = materialize_json_evidence(
            root, evidence_id="role-roster", gate_id="G0",
            kind="production_role_roster", relative_path="evidence/roster.json",
            value={"schema_version": 1, "authors": ["author-01"], "validators": ["validator-01"]},
        )
        trial = materialize_json_evidence(
            root, evidence_id="g4-trial", gate_id="G4",
            kind="independent_course_trial", relative_path="trials/g4.json",
            value={
                "schema_version": 1, "scope": "representative_unit",
                "participant": {"id": "cold-runner-01", "type": "independent-ai", "roles": ["learner-trial"]},
                "runner_session_id": "session-01",
                "isolated_context_id": "context-01",
                "allowed_inputs": [{"kind": "learner-page", "path": "course/unit.html", "sha256": learner_sha}],
            },
        )
        return roster, trial

    def verify(self, root, contract, roster, trial, receipt_ref):
        receipt = consume_evidence_reference(root, receipt_ref, expected_gate="G4", parse_json=True).value
        consumed_trial = consume_evidence_reference(root, trial, expected_gate="G4", parse_json=True)
        return verify_trial_receipt(
            receipt,
            contract["governance"]["runner_authority"],
            contract=contract,
            expected_evidence_set_sha256=transition_evidence_sha256([trial, roster]),
            receipt_reference=receipt_ref,
            learner_inputs=consume_trial_inputs(root, consumed_trial.value),
            gate_id="G4",
            trial=consumed_trial,
            roster=consume_evidence_reference(root, roster, expected_gate="G0", parse_json=True),
        )

    def test_preissued_receipt_verifies_with_public_key_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            authority = self.authority()
            contract = new_contract("authority-course", "Authority Course", "course-run", "2026-10-18T12:00:00+08:00")
            roster, trial = self.evidence(root)
            authority.bind(contract)
            receipt_ref = authority.issue(
                root, contract=contract, gate_id="G4", trial_reference=trial,
                roster_reference=roster, transition_references=[trial, roster],
                runner_id="cold-runner-01", session_id="session-01",
                issued_at="2026-10-18T12:10:00+08:00", nonce="nonce-01",
                receipt_id="g4-receipt", relative_path="receipts/g4.json",
            )
            self.assertEqual(self.verify(root, contract, roster, trial, receipt_ref), [])

    def test_receipt_tamper_and_untrusted_self_signed_key_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            authority = self.authority()
            attacker = self.authority(key_slot=1)
            contract = new_contract("authority-course", "Authority Course", "course-run", "2026-10-18T12:00:00+08:00")
            roster, trial = self.evidence(root)
            authority.bind(contract)
            receipt_ref = authority.issue(
                root, contract=contract, gate_id="G4", trial_reference=trial,
                roster_reference=roster, transition_references=[trial, roster],
                runner_id="cold-runner-01", session_id="session-01",
                issued_at="2026-10-18T12:10:00+08:00", nonce="nonce-01",
                receipt_id="g4-receipt", relative_path="receipts/g4.json",
            )
            receipt = consume_evidence_reference(root, receipt_ref, expected_gate="G4", parse_json=True).value
            receipt["runner"]["id"] = "author-alias"
            tampered_ref = materialize_json_evidence(
                root, evidence_id="tampered", gate_id="G4", kind="independent_trial_receipt",
                relative_path="receipts/tampered.json", value=receipt,
            )
            self.assertTrue(self.verify(root, contract, roster, trial, tampered_ref))

            attacker_ref = attacker.issue(
                root, contract=contract, gate_id="G4", trial_reference=trial,
                roster_reference=roster, transition_references=[trial, roster],
                runner_id="cold-runner-01", session_id="session-01",
                issued_at="2026-10-18T12:11:00+08:00", nonce="attacker-nonce",
                receipt_id="attacker-receipt", relative_path="receipts/attacker.json",
            )
            self.assertIn(
                "invalid_receipt_signature",
                {issue.code for issue in self.verify(root, contract, roster, trial, attacker_ref)},
            )

    def test_receipt_rejects_cross_contract_and_cross_revision_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            authority = self.authority()
            contract = new_contract("authority-course", "Authority Course", "course-run", "2026-10-18T12:00:00+08:00")
            roster, trial = self.evidence(root)
            authority.bind(contract)
            receipt_ref = authority.issue(
                root, contract=contract, gate_id="G4", trial_reference=trial,
                roster_reference=roster, transition_references=[trial, roster],
                runner_id="cold-runner-01", session_id="session-01",
                issued_at="2026-10-18T12:10:00+08:00", nonce="nonce-01",
                receipt_id="g4-receipt", relative_path="receipts/g4.json",
            )
            other = copy.deepcopy(contract)
            other["contract_instance_id"] = "ci-" + "f" * 32
            self.assertIn("contract_replay", {issue.code for issue in self.verify(root, other, roster, trial, receipt_ref)})
            revised = copy.deepcopy(contract)
            revised["revision"] += 1
            self.assertIn("contract_replay", {issue.code for issue in self.verify(root, revised, roster, trial, receipt_ref)})

    def test_external_authority_requires_registered_session_ownership(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            authority = self.authority()
            contract = new_contract("authority-course", "Authority Course", "course-run", "2026-10-18T12:00:00+08:00")
            roster, trial = self.evidence(root)
            authority.bind(contract)
            with self.assertRaisesRegex(ContractStateError, "no assertion"):
                authority.issue(
                    root, contract=contract, gate_id="G4", trial_reference=trial,
                    roster_reference=roster, transition_references=[trial, roster],
                    runner_id="cold-runner-01", session_id="caller-chosen-session",
                    issued_at="2026-10-18T12:10:00+08:00", nonce="nonce-01",
                    receipt_id="g4-receipt", relative_path="receipts/g4.json",
                )

    def test_authority_binding_cannot_change_after_gate_work_begins(self):
        authority = self.authority()
        contract = new_contract("authority-course", "Authority Course", "course-run", "2026-10-18T12:00:00+08:00")
        authority.bind(contract)
        begin_gate(contract, "G0", "course-run", "2026-10-18T12:01:00+08:00")
        with self.assertRaisesRegex(ContractStateError, "before Gate work"):
            contract["governance"]["runner_authority"] = None
            authority.bind(contract)


if __name__ == "__main__":
    unittest.main()
