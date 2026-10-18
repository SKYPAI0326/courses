import copy
import tempfile
import unittest
from pathlib import Path

from src.course_contract import ContractStateError, begin_gate, new_contract, validate_contract
from src.course_evidence import materialize_json_evidence
from src.course_governance import consume_passed_gate
from tests.gate_test_support import _commit_gate_pass


class GovernedReplayTests(unittest.TestCase):
    def passed_contract(self, root: Path, through: str):
        contract = new_contract("replay-course", "Replay Course", "test", "2026-10-18T10:00:00+08:00")
        for number in range(int(through[1:]) + 1):
            gate_id = f"G{number}"
            begin_gate(contract, gate_id, "test", f"2026-10-18T10:0{number}:00+08:00")
            reference = materialize_json_evidence(
                root, evidence_id=f"{gate_id.lower()}-record", gate_id=gate_id,
                kind="test_record", relative_path=f"evidence/{gate_id.lower()}.json",
                value={"gate": gate_id},
            )
            contract["evidence_index"].append(reference)
            _commit_gate_pass(contract, gate_id, [reference["id"]], "fixture", "test", f"2026-10-18T10:1{number}:00+08:00")
        return contract

    def test_g0_g2_g3_replay_rejects_file_index_and_event_tampering(self):
        for gate_id, tamper in (("G0", "file"), ("G2", "index"), ("G3", "event")):
            with self.subTest(gate=gate_id, tamper=tamper), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                contract = self.passed_contract(root, gate_id)
                event = contract["gates"][gate_id]["evidence"][-1]
                reference = next(item for item in contract["evidence_index"] if item["id"] == f"{gate_id.lower()}-record")
                if tamper == "file":
                    (root / reference["path"]).write_text('{"tampered":true}\n', encoding="utf-8")
                elif tamper == "index":
                    reference["kind"] = "swapped_record"
                else:
                    event["consumed_evidence"][0].pop("sha256")
                with self.assertRaises(ContractStateError):
                    consume_passed_gate(contract, gate_id, root)

    def test_contract_validation_rejects_missing_duplicate_extra_or_swapped_pass_bindings(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            base = self.passed_contract(root, "G0")
            mutations = []
            missing = copy.deepcopy(base)
            missing["gates"]["G0"]["evidence"][-1]["consumed_evidence"] = []
            mutations.append(missing)
            duplicate = copy.deepcopy(base)
            duplicate["gates"]["G0"]["evidence"][-1]["consumed_evidence"] *= 2
            mutations.append(duplicate)
            extra = copy.deepcopy(base)
            extra["gates"]["G0"]["evidence"][-1]["consumed_evidence"].append({
                "id": "extra", "gate": "G0", "kind": "test_record", "path": "evidence/extra.json", "sha256": "a" * 64,
            })
            mutations.append(extra)
            swapped = copy.deepcopy(base)
            swapped["evidence_index"][0]["path"] = "evidence/swapped.json"
            mutations.append(swapped)
            for contract in mutations:
                with self.subTest():
                    self.assertIn("invalid_pass_evidence_binding", {issue.code for issue in validate_contract(contract)})


if __name__ == "__main__":
    unittest.main()
