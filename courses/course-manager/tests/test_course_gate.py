import tempfile
import unittest
from pathlib import Path

from src.course_contract import ContractStateError, begin_gate, new_contract, pass_gate
from src.course_evidence import materialize_json_evidence
from src.course_gate import validate_and_transition_gate


class CourseGateTransitionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.workspace_root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def contract_at_g0(self):
        contract = new_contract(
            "practical-ai",
            "實用 AI 課程",
            "course-run",
            "2026-10-18T12:00:00+08:00",
        )
        contract["G0_requirements"] = {
            "learner_context": "第一次獨立完成工作任務的學員",
            "observable_outcome": "完成可驗收的工作成果",
        }
        begin_gate(contract, "G0", "course-run", "2026-10-18T12:01:00+08:00")
        return contract

    def add_requirements_evidence(self, contract, value=None):
        reference = materialize_json_evidence(
            self.workspace_root,
            evidence_id="g0-requirements",
            gate_id="G0",
            kind="requirements_record",
            relative_path="evidence/g0-requirements.json",
            value=value if value is not None else contract["G0_requirements"],
        )
        contract["evidence_index"].append(reference)
        return reference

    def test_generic_pass_gate_cannot_bypass_gate_registry(self):
        contract = self.contract_at_g0()
        self.add_requirements_evidence(contract)

        with self.assertRaisesRegex(ContractStateError, "validate_and_transition_gate"):
            pass_gate(
                contract,
                "G0",
                ["g0-requirements"],
                "caller-declared-validator",
                "course-run",
                "2026-10-18T12:02:00+08:00",
            )

        self.assertEqual(contract["gates"]["G0"]["status"], "IN_PROGRESS")

    def test_dispatcher_replays_file_hash_at_transition_boundary(self):
        contract = self.contract_at_g0()
        reference = self.add_requirements_evidence(contract)
        evidence_path = self.workspace_root / reference["path"]
        evidence_path.write_text('{"tampered":true}\n', encoding="utf-8")

        with self.assertRaisesRegex(ContractStateError, "sha256"):
            validate_and_transition_gate(
                contract,
                "G0",
                ["g0-requirements"],
                self.workspace_root,
                "course-run",
                "2026-10-18T12:02:00+08:00",
            )

        self.assertEqual(contract["gates"]["G0"]["status"], "IN_PROGRESS")

    def test_registry_rejects_wrong_kind_instead_of_trusting_an_id(self):
        contract = self.contract_at_g0()
        reference = materialize_json_evidence(
            self.workspace_root,
            evidence_id="g0-generic",
            gate_id="G0",
            kind="test_record",
            relative_path="evidence/g0-generic.json",
            value={"looks": "plausible"},
        )
        contract["evidence_index"].append(reference)

        with self.assertRaisesRegex(ContractStateError, "requirements_record"):
            validate_and_transition_gate(
                contract,
                "G0",
                ["g0-generic"],
                self.workspace_root,
                "course-run",
                "2026-10-18T12:02:00+08:00",
            )

        self.assertEqual(contract["gates"]["G0"]["status"], "IN_PROGRESS")

    def test_registry_executes_g0_validator_before_committing_pass(self):
        contract = self.contract_at_g0()
        self.add_requirements_evidence(contract, {"learner_context": ""})

        status = validate_and_transition_gate(
            contract,
            "G0",
            ["g0-requirements"],
            self.workspace_root,
            "course-run",
            "2026-10-18T12:02:00+08:00",
        )

        self.assertEqual(status, "BLOCKED")
        self.assertEqual(contract["gates"]["G0"]["status"], "BLOCKED")

    def test_valid_g0_evidence_passes_through_registered_validator(self):
        contract = self.contract_at_g0()
        self.add_requirements_evidence(contract)

        status = validate_and_transition_gate(
            contract,
            "G0",
            ["g0-requirements"],
            self.workspace_root,
            "course-run",
            "2026-10-18T12:02:00+08:00",
        )

        self.assertEqual(status, "PASS")
        event = contract["gates"]["G0"]["evidence"][-1]
        self.assertEqual(event["validator_id"], "course-requirements-validator")


if __name__ == "__main__":
    unittest.main()
