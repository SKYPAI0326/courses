import base64
import copy
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.course_contract import ContractStateError, begin_gate, new_contract
from src.course_evidence import consume_evidence_reference, materialize_json_evidence
from src.course_runner_authority import (
    bind_runner_authority,
    consume_trial_inputs,
    issue_trial_receipt,
    verify_trial_receipt,
)


class CourseRunnerAuthorityTests(unittest.TestCase):
    authority_id = "independent-lab"
    secret = b"independent authority test secret material 2026"

    def authority_environment(self):
        return {
            "COURSE_RUNNER_REQUIRED_AUTHORITY_ID": self.authority_id,
            "COURSE_RUNNER_AUTHORITY_INDEPENDENT_LAB_SECRET": base64.b64encode(self.secret).decode(),
            "COURSE_RUNNER_AUTHORITY_INDEPENDENT_LAB_RUNNERS": json.dumps(
                {"cold-runner-01": "isolated-learner-runner"}, sort_keys=True
            ),
        }

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

    def test_preissued_receipt_verifies_against_fixed_authority_and_files(self):
        with patch.dict(os.environ, self.authority_environment(), clear=False), tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract = new_contract("authority-course", "Authority Course", "course-run", "2026-10-18T12:00:00+08:00")
            roster, trial = self.evidence(root)
            contract["evidence_index"].append(roster)
            contract["governance"]["production_role_roster"] = {"evidence_id": roster["id"], "sha256": roster["sha256"]}
            bind_runner_authority(contract, self.authority_id)
            receipt_ref = issue_trial_receipt(
                root, authority_id=self.authority_id, gate_id="G4",
                trial_reference=trial, roster_reference=roster,
                runner_id="cold-runner-01", session_id="session-01",
                issued_at="2026-10-18T12:10:00+08:00", nonce="nonce-01",
                evidence_id="g4-receipt", relative_path="receipts/g4.json",
            )
            receipt = consume_evidence_reference(root, receipt_ref, expected_gate="G4", parse_json=True).value
            consumed_trial = consume_evidence_reference(root, trial, expected_gate="G4", parse_json=True)
            issues = verify_trial_receipt(
                receipt, contract["governance"]["runner_authority"], gate_id="G4",
                learner_inputs=consume_trial_inputs(root, consumed_trial.value),
                trial=consumed_trial,
                roster=consume_evidence_reference(root, roster, expected_gate="G0", parse_json=True),
            )
            self.assertEqual(issues, [])

    def test_receipt_tamper_and_untrusted_signature_are_rejected(self):
        with patch.dict(os.environ, self.authority_environment(), clear=False), tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            contract = new_contract("authority-course", "Authority Course", "course-run", "2026-10-18T12:00:00+08:00")
            roster, trial = self.evidence(root)
            contract["evidence_index"].append(roster)
            contract["governance"]["production_role_roster"] = {"evidence_id": roster["id"], "sha256": roster["sha256"]}
            bind_runner_authority(contract, self.authority_id)
            receipt_ref = issue_trial_receipt(
                root, authority_id=self.authority_id, gate_id="G4", trial_reference=trial,
                roster_reference=roster, runner_id="cold-runner-01", session_id="session-01",
                issued_at="2026-10-18T12:10:00+08:00", nonce="nonce-01",
                evidence_id="g4-receipt", relative_path="receipts/g4.json",
            )
            receipt = consume_evidence_reference(root, receipt_ref, expected_gate="G4", parse_json=True).value
            consumed_trial = consume_evidence_reference(root, trial, expected_gate="G4", parse_json=True)
            consumed_roster = consume_evidence_reference(root, roster, expected_gate="G0", parse_json=True)
            consumed_inputs = consume_trial_inputs(root, consumed_trial.value)
            tampered = copy.deepcopy(receipt)
            tampered["runner"]["id"] = "author-alias"
            self.assertTrue(verify_trial_receipt(tampered, contract["governance"]["runner_authority"], learner_inputs=consumed_inputs, gate_id="G4", trial=consumed_trial, roster=consumed_roster))
            forged = copy.deepcopy(receipt)
            forged["signature"] = "0" * 64
            self.assertTrue(verify_trial_receipt(forged, contract["governance"]["runner_authority"], learner_inputs=consumed_inputs, gate_id="G4", trial=consumed_trial, roster=consumed_roster))

    def test_authority_binding_cannot_change_after_gate_work_begins(self):
        with patch.dict(os.environ, self.authority_environment(), clear=False):
            contract = new_contract("authority-course", "Authority Course", "course-run", "2026-10-18T12:00:00+08:00")
            bind_runner_authority(contract, self.authority_id)
            begin_gate(contract, "G0", "course-run", "2026-10-18T12:01:00+08:00")
            with self.assertRaisesRegex(ContractStateError, "before Gate work"):
                bind_runner_authority(contract, self.authority_id)


if __name__ == "__main__":
    unittest.main()
