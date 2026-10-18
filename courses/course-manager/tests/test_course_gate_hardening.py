import ast
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
    def test_production_runner_authority_is_verification_only(self):
        import src.course_runner_authority as authority

        source = (Path(__file__).parents[1] / "src" / "course_runner_authority.py").read_text(encoding="utf-8")
        self.assertFalse(hasattr(authority, "issue_trial_receipt"))
        with self.assertRaises(ImportError):
            exec("from src.course_runner_authority import issue_trial_receipt", {})
        self.assertNotIn("hmac", source)
        self.assertNotIn("_SECRET", source)
        self.assertNotIn("private_key", source)
        self.assertNotIn("_private_exponent", source)

    def test_src_dependency_graph_has_no_multi_module_cycle(self):
        source_root = Path(__file__).parents[1] / "src"

        modules = {path.stem for path in source_root.glob("*.py")}

        def imports(module_name):
            tree = ast.parse(
                (source_root / f"{module_name}.py").read_text(encoding="utf-8")
            )
            dependencies = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    if node.level and node.module:
                        imported = node.module.split(".", 1)[0]
                        if imported in modules:
                            dependencies.add(imported)
                    elif node.level:
                        dependencies.update(
                            alias.name for alias in node.names if alias.name in modules
                        )
                    elif node.module == "src":
                        dependencies.update(
                            alias.name for alias in node.names if alias.name in modules
                        )
                    elif isinstance(node.module, str) and node.module.startswith("src."):
                        imported = node.module.removeprefix("src.").split(".", 1)[0]
                        if imported in modules:
                            dependencies.add(imported)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith("src."):
                            imported = alias.name.removeprefix("src.").split(".", 1)[0]
                            if imported in modules:
                                dependencies.add(imported)
            return dependencies

        validator_imports = imports("course_gate_validators")
        self.assertIn("course_validation", validator_imports)
        self.assertIn("course_production", validator_imports)
        for route_module in (
            "course_validation_routes",
            "course_production_routes",
            "course_research_routes",
            "course_content_routes",
        ):
            self.assertIn("course_gate", imports(route_module))
        for pure_module in (
            "course_validation",
            "course_production",
            "course_research",
            "course_content",
        ):
            self.assertNotIn("course_gate", imports(pure_module))

        graph = {module: imports(module) for module in modules}

        def reaches(start, target, seen=None):
            seen = set() if seen is None else seen
            if start in seen:
                return False
            seen.add(start)
            return any(
                dependency == target or reaches(dependency, target, seen)
                for dependency in graph.get(start, set())
            )

        index = 0
        indexes = {}
        lowlinks = {}
        stack = []
        on_stack = set()
        strongly_connected = []

        def visit(module):
            nonlocal index
            indexes[module] = index
            lowlinks[module] = index
            index += 1
            stack.append(module)
            on_stack.add(module)

            for dependency in graph[module]:
                if dependency not in indexes:
                    visit(dependency)
                    lowlinks[module] = min(lowlinks[module], lowlinks[dependency])
                elif dependency in on_stack:
                    lowlinks[module] = min(lowlinks[module], indexes[dependency])

            if lowlinks[module] == indexes[module]:
                component = []
                while True:
                    dependency = stack.pop()
                    on_stack.remove(dependency)
                    component.append(dependency)
                    if dependency == module:
                        break
                strongly_connected.append(tuple(sorted(component)))

        for module in sorted(graph):
            if module not in indexes:
                visit(module)

        import_cycles = sorted(
            component for component in strongly_connected if len(component) > 1
        )
        self.assertEqual(import_cycles, [], f"local import cycles: {import_cycles}")
        self.assertFalse(reaches("course_gate_validators", "course_gate"))

    def test_catalog_discovery_dependency_graph_is_one_way(self):
        source_root = Path(__file__).parents[1] / "src"

        def relative_imports(module_name):
            tree = ast.parse(
                (source_root / f"{module_name}.py").read_text(encoding="utf-8")
            )
            return {
                node.module
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom)
                and node.level
                and isinstance(node.module, str)
            }

        self.assertIn("discover", relative_imports("catalog"))
        self.assertNotIn("catalog", relative_imports("discover"))

    def test_new_contract_has_immutable_instance_and_local_receipt_ledger(self):
        contract = new_contract("receipt-course", "Receipt Course", "test", "2026-10-18T12:00:00+08:00")
        self.assertRegex(contract["contract_instance_id"], r"^ci-[0-9a-f]{32}$")
        self.assertEqual(contract["consumed_trial_receipts"], [])

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
            for name in ("course_validation_routes.py", "course_production_routes.py")
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
