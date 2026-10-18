import hashlib
import tempfile
import unittest
from pathlib import Path

import src.course_contract as course_contract
from src.course_contract import ContractStateError, begin_gate, new_contract
from src.course_evidence import (
    consume_evidence_reference,
    materialize_json_evidence,
    register_evidence_file,
)
from src.course_gate import validate_and_transition_gate
from tests.gate_test_support import _commit_gate_pass


class CourseGateHardeningTests(unittest.TestCase):
    def contract_at_g6(self):
        contract = new_contract("release-course", "Release Course", "course-run", "2026-10-18T12:00:00+08:00")
        for gate_id in ("G0", "G1", "G2", "G3", "G4", "G5"):
            begin_gate(contract, gate_id, "test", "2026-10-18T12:01:00+08:00")
            evidence_id = f"{gate_id.lower()}-fixture"
            contract["evidence_index"].append({"id": evidence_id, "gate": gate_id, "kind": "test_record", "path": f"fixtures/{evidence_id}.json", "sha256": hashlib.sha256(evidence_id.encode()).hexdigest()})
            _commit_gate_pass(contract, gate_id, [evidence_id], "test-fixture", "test", "2026-10-18T12:02:00+08:00")
        begin_gate(contract, "G6", "test", "2026-10-18T12:03:00+08:00")
        return contract

    def release_evidence(self, root, contract, *, omit=None):
        checks = []
        ids = []
        for name in ("technical", "links", "registration", "access", "rollback", "maintenance"):
            path = f"checks/{name}.txt"
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(f"{name}: PASS\n", encoding="utf-8")
            reference = register_evidence_file(root, evidence_id=f"g6-{name}", gate_id="G6", kind="release_check", relative_path=path, metadata={"check_id": name})
            checks.append({"id": name, "result": "PASS", "evidence": {"path": path, "sha256": reference["sha256"]}})
            if name != omit:
                contract["evidence_index"].append(reference)
                ids.append(reference["id"])
        record = {
            "schema_version": 1, "course_id": "release-course", "g5_status": "PASS",
            "g6_state": "READY_TO_PUBLISH", "published": False, "checks": checks,
            "changes": [{"source_path": "staged/index.html", "target_path": "public/index.html"}],
            "maintenance": {"owner": "course-ops", "cadence": "quarterly", "freshness_sources": ["official notes"], "next_review": "2027-01-18"},
        }
        release_ref = materialize_json_evidence(root, evidence_id="g6-release", gate_id="G6", kind="release_record", relative_path="evidence/release.json", value=record)
        contract["evidence_index"].append(release_ref)
        return [release_ref["id"], *ids]

    def test_course_contract_does_not_expose_raw_pass_mutator(self):
        self.assertFalse(hasattr(course_contract, "_commit_gate_pass"))
        source_root = Path(__file__).parents[1] / "src"
        offenders = [
            path.name for path in source_root.glob("*.py")
            if path.name != "course_gate.py" and "_commit_gate_pass" in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(offenders, [])

    def test_dispatcher_is_only_registry_consume_and_transition_coordinator(self):
        source_root = Path(__file__).parents[1] / "src"
        dispatcher = (source_root / "course_gate.py").read_text(encoding="utf-8")
        validators = (source_root / "course_gate_validators.py").read_text(encoding="utf-8")
        self.assertLess(len(dispatcher.splitlines()), 250)
        self.assertNotIn("def _validate_g4", dispatcher)
        self.assertNotIn("def _validate_g5_artifact_bindings", dispatcher)
        self.assertNotIn("from src.course_gate import", validators)
        self.assertNotIn("route_verified_trial_to_gate", validators)
        self.assertNotIn("route_full_production_to_g5", validators)
        route_sources = "\n".join(
            (source_root / name).read_text(encoding="utf-8")
            for name in ("course_validation.py", "course_production.py")
        )
        self.assertNotIn("issue_trial_receipt", route_sources)

    def test_secure_consume_returns_bytes_and_parsed_json_from_bound_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            reference = materialize_json_evidence(
                root,
                evidence_id="g0-record",
                gate_id="G0",
                kind="requirements_record",
                relative_path="evidence/g0.json",
                value={"answer": 42},
            )

            consumed = consume_evidence_reference(
                root, reference, expected_gate="G0", parse_json=True
            )

            self.assertEqual(consumed.sha256, reference["sha256"])
            self.assertEqual(hashlib.sha256(consumed.data).hexdigest(), reference["sha256"])
            self.assertEqual(consumed.value, {"answer": 42})

    def test_roster_binding_is_governed_and_immutable_after_work_begins(self):
        contract = new_contract(
            "governed-course", "Governed Course", "course-run", "2026-10-18T12:00:00+08:00"
        )
        reference = {
            "id": "role-roster",
            "gate": "G0",
            "kind": "production_role_roster",
            "path": "evidence/role-roster.json",
            "sha256": "a" * 64,
        }
        contract["evidence_index"].append(reference)
        course_contract.bind_production_role_roster(contract, "role-roster")

        self.assertEqual(
            contract["governance"]["production_role_roster"],
            {"evidence_id": "role-roster", "sha256": "a" * 64},
        )
        contract["gates"]["G0"]["status"] = "IN_PROGRESS"
        with self.assertRaisesRegex(ContractStateError, "fixed before Gate work"):
            course_contract.bind_production_role_roster(contract, "role-roster")

    def test_g6_requires_every_nested_check_file(self):
        contract = self.contract_at_g6()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence_ids = self.release_evidence(root, contract, omit="rollback")
            result = validate_and_transition_gate(contract, "G6", evidence_ids, root, "course-ops", "2026-10-18T12:04:00+08:00")
        self.assertEqual(result, "BLOCKED")
        self.assertIn("each G6 check requires", contract["gates"]["G6"]["risks"][-1]["reason"])

    def test_g6_rejects_nested_check_hash_that_does_not_match_file(self):
        contract = self.contract_at_g6()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence_ids = self.release_evidence(root, contract)
            rollback = next(item for item in contract["evidence_index"] if item.get("id") == "g6-rollback")
            rollback["sha256"] = "0" * 64
            with self.assertRaisesRegex(ContractStateError, "hash_mismatch"):
                validate_and_transition_gate(contract, "G6", evidence_ids, root, "course-ops", "2026-10-18T12:04:00+08:00")

    def test_g6_pass_consumes_every_nested_check_file(self):
        contract = self.contract_at_g6()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            evidence_ids = self.release_evidence(root, contract)
            result = validate_and_transition_gate(contract, "G6", evidence_ids, root, "course-ops", "2026-10-18T12:04:00+08:00")
        self.assertEqual(result, "PASS")
        consumed = contract["gates"]["G6"]["evidence"][-1]["consumed_evidence"]
        self.assertEqual(len(consumed), 7)


if __name__ == "__main__":
    unittest.main()
