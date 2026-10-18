import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from src.course_contract import (
    ContractStateError,
    GATE_ORDER,
    GATE_STATUSES,
    assert_external_action_authorized,
    authorize_external_action,
    begin_gate,
    block_gate,
    fail_gate,
    load_contract,
    migrate_contract_v1,
    migrate_contract_v2,
    new_contract,
    propose_external_action,
    record_change,
    save_contract_atomic,
    validate_contract,
)
from tests.gate_test_support import _commit_gate_pass


FIXTURES = Path(__file__).resolve().parent / "fixtures"

REQUIRED_SECTIONS = {
    "schema_version",
    "revision",
    "contract_instance_id",
    "identity",
    "governance",
    "gates",
    "G0_requirements",
    "G1_research",
    "adaptation",
    "G2_architecture",
    "G3_lesson_design",
    "G4_pilot",
    "G5_production",
    "G6_release_maintenance",
    "changes",
    "evidence_index",
    "evidence_archive",
    "external_actions",
    "maintenance",
    "consumed_trial_receipts",
}

REQUIRED_GATE_FIELDS = {
    "status",
    "owner",
    "inputs",
    "deliverables",
    "evidence",
    "risks",
    "open_questions",
    "source_revision",
    "affected_downstream",
}


class CourseContractModelTests(unittest.TestCase):
    def make_contract(self):
        return new_contract(
            slug="practical-ai",
            title="實用生成式 AI",
            created_by="課程團隊",
            created_at="2026-10-18T12:00:00+08:00",
        )

    def test_new_contract_uses_v3_revision_gate_states_and_external_action_sections(self):
        contract = self.make_contract()

        self.assertEqual(GATE_ORDER, tuple(f"G{index}" for index in range(7)))
        self.assertEqual(
            GATE_STATUSES,
            frozenset(
                {"NOT_STARTED", "IN_PROGRESS", "PASS", "FAIL", "BLOCKED", "STALE"}
            ),
        )
        self.assertEqual(contract["schema_version"], 3)
        self.assertEqual(contract["revision"], 0)
        self.assertEqual(set(contract), REQUIRED_SECTIONS)
        self.assertEqual(tuple(contract["gates"]), GATE_ORDER)
        self.assertTrue(
            all(
                set(record) == REQUIRED_GATE_FIELDS
                for record in contract["gates"].values()
            )
        )
        self.assertTrue(
            all(
                record["status"] == "NOT_STARTED"
                for record in contract["gates"].values()
            )
        )
        self.assertEqual(contract["external_actions"], [])
        self.assertEqual(contract["maintenance"], {})
        self.assertEqual(
            contract["governance"]["gate_authority"],
            "course-run-with-validated-evidence",
        )
        self.assertEqual(
            contract["governance"]["external_action_authority"],
            "explicit-user-authorization",
        )

    def test_validate_rejects_unknown_gate_status(self):
        contract = self.make_contract()
        contract["gates"]["G3"]["status"] = "DONE"

        issues = validate_contract(contract)

        self.assertIn("unknown_gate_status", {issue.code for issue in issues})
        self.assertIn("$.gates.G3.status", {issue.path for issue in issues})

    def test_validate_rejects_missing_required_gate_fields(self):
        contract = self.make_contract()
        del contract["gates"]["G2"]["evidence"]

        issues = validate_contract(contract)

        self.assertIn("missing_gate_field", {issue.code for issue in issues})
        self.assertIn("$.gates.G2.evidence", {issue.path for issue in issues})

    def test_validate_rejects_invalid_section_and_gate_collection_types(self):
        mutations = {
            "governance": lambda contract: contract.update(governance=None),
            "changes": lambda contract: contract.update(changes="not-a-list"),
            "evidence_index": lambda contract: contract.update(evidence_index={}),
            "external_actions": lambda contract: contract.update(external_actions={}),
            "maintenance": lambda contract: contract.update(maintenance=[]),
            "payload": lambda contract: contract.update(G1_research=[]),
            "gate risks": lambda contract: contract["gates"]["G0"].update(
                risks={"blocking": True, "resolved": False}
            ),
            "gate evidence": lambda contract: contract["gates"]["G0"].update(
                evidence={}
            ),
        }

        for label, mutate in mutations.items():
            with self.subTest(label=label):
                contract = self.make_contract()
                mutate(contract)
                self.assertTrue(validate_contract(contract))

    def test_new_contract_rejects_path_traversal_slug(self):
        invalid_slugs = ("../outside", "nested/course", "Uppercase", "two words", "")

        for slug in invalid_slugs:
            with self.subTest(slug=slug):
                with self.assertRaises(ValueError):
                    new_contract(slug, "課程", "作者", "2026-10-18T12:00:00+08:00")

    def test_atomic_save_round_trips_utf8_prose_without_rewriting(self):
        prose = "先看懂工作情境，再完成一份可交付、可驗收的成果。\n保留完整推理，不改成待辦清單。"
        contract = self.make_contract()
        contract["G0_requirements"]["learner_context"] = prose
        expected = copy.deepcopy(contract)

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "nested" / "course-contract.json"
            save_contract_atomic(path, contract)
            loaded = load_contract(path)

            self.assertEqual(loaded, expected)
            self.assertEqual(
                loaded["G0_requirements"]["learner_context"].encode("utf-8"),
                prose.encode("utf-8"),
            )
            self.assertEqual(list(path.parent.glob(f".{path.name}.*.tmp")), [])


class CourseContractStateTests(unittest.TestCase):
    def make_contract(self):
        return new_contract(
            slug="practical-ai",
            title="實用生成式 AI",
            created_by="課程團隊",
            created_at="2026-10-18T12:00:00+08:00",
        )

    def index_evidence(self, contract, evidence_id, gate_id):
        contract["evidence_index"].append(
            {
                "id": evidence_id,
                "gate": gate_id,
                "kind": "test_record",
                "path": f"evidence/{evidence_id}.json",
                "sha256": hashlib.sha256(evidence_id.encode("utf-8")).hexdigest(),
            }
        )

    def pass_gates_through(self, contract, final_gate):
        for gate_id in GATE_ORDER:
            begin_gate(contract, gate_id, "course-run", "2026-10-18T13:00:00+08:00")
            evidence_id = f"{gate_id.lower()}-evidence"
            self.index_evidence(contract, evidence_id, gate_id)
            _commit_gate_pass(
                contract,
                gate_id,
                [evidence_id],
                f"{gate_id.lower()}-validator",
                "course-run",
                "2026-10-18T13:05:00+08:00",
            )
            if gate_id == final_gate:
                return

    def test_pass_requires_all_previous_gates_passed_and_indexed_evidence(self):
        contract = self.make_contract()
        begin_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")

        with self.assertRaises(ContractStateError):
            _commit_gate_pass(
                contract,
                "G0",
                ["missing-evidence"],
                "requirements-validator",
                "course-run",
                "2026-10-18T13:05:00+08:00",
            )

        self.index_evidence(contract, "g0-evidence", "G0")
        _commit_gate_pass(
            contract,
            "G0",
            ["g0-evidence"],
            "requirements-validator",
            "course-run",
            "2026-10-18T13:05:00+08:00",
        )
        self.assertEqual(contract["gates"]["G0"]["status"], "PASS")

        contract["gates"]["G0"]["status"] = "IN_PROGRESS"
        with self.assertRaises(ContractStateError):
            begin_gate(contract, "G1", "course-run", "2026-10-18T13:10:00+08:00")

    def test_pass_rejects_evidence_indexed_for_another_gate(self):
        contract = self.make_contract()
        begin_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")
        self.index_evidence(contract, "wrong-gate-evidence", "G1")

        with self.assertRaises(ContractStateError):
            _commit_gate_pass(
                contract,
                "G0",
                ["wrong-gate-evidence"],
                "requirements-validator",
                "course-run",
                "2026-10-18T13:05:00+08:00",
            )

    def test_validate_rejects_duplicate_or_untyped_evidence_references(self):
        contract = self.make_contract()
        self.index_evidence(contract, "same-id", "G0")
        duplicate = copy.deepcopy(contract["evidence_index"][0])
        duplicate["path"] = "evidence/other.json"
        contract["evidence_index"].append(duplicate)
        contract["evidence_index"].append(
            {
                "id": "bad-kind",
                "gate": "G0",
                "kind": 9,
                "path": "evidence/bad-kind.json",
                "sha256": "a" * 64,
            }
        )

        codes = {issue.code for issue in validate_contract(contract)}

        self.assertIn("duplicate_evidence_id", codes)
        self.assertIn("invalid_evidence_kind", codes)

    def test_pass_rejects_unresolved_blockers(self):
        contract = self.make_contract()
        begin_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")
        self.index_evidence(contract, "g0-evidence", "G0")
        contract["gates"]["G0"]["risks"].append(
            {
                "id": "risk-1",
                "blocking": True,
                "resolved": False,
                "description": "時數未確認",
            }
        )

        with self.assertRaises(ContractStateError):
            _commit_gate_pass(
                contract,
                "G0",
                ["g0-evidence"],
                "requirements-validator",
                "course-run",
                "2026-10-18T13:05:00+08:00",
            )

        self.assertEqual(contract["gates"]["G0"]["status"], "IN_PROGRESS")

    def test_fail_preserves_issues_and_allows_restart(self):
        contract = self.make_contract()
        begin_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")

        fail_gate(
            contract,
            "G0",
            [{"code": "missing-outcome", "message": "缺少可觀察成果"}],
            "requirements-validator",
            "2026-10-18T13:05:00+08:00",
        )

        self.assertEqual(contract["gates"]["G0"]["status"], "FAIL")
        self.assertEqual(
            contract["gates"]["G0"]["evidence"][-1]["issues"][0]["code"],
            "missing-outcome",
        )
        begin_gate(contract, "G0", "course-run", "2026-10-18T13:10:00+08:00")
        self.assertEqual(contract["gates"]["G0"]["status"], "IN_PROGRESS")

    def test_semantic_change_sets_affected_gate_in_progress_and_downstream_stale(self):
        contract = self.make_contract()
        self.pass_gates_through(contract, "G2")
        original_g0 = copy.deepcopy(contract["gates"]["G0"])

        invalidated = record_change(
            contract,
            "G1",
            "代表工具改版，研究與架構需重驗",
            "course-run",
            "2026-10-19T09:00:00+08:00",
            semantic=True,
        )

        self.assertEqual(invalidated, ["G1", "G2", "G3", "G4", "G5", "G6"])
        self.assertEqual(contract["gates"]["G0"], original_g0)
        self.assertEqual(contract["gates"]["G1"]["status"], "IN_PROGRESS")
        self.assertTrue(
            all(
                contract["gates"][gate_id]["status"] == "STALE"
                for gate_id in GATE_ORDER[2:]
            )
        )

    def test_nonsemantic_change_preserves_gate_states(self):
        contract = self.make_contract()
        self.pass_gates_through(contract, "G1")
        before = {
            gate_id: contract["gates"][gate_id]["status"] for gate_id in GATE_ORDER
        }

        invalidated = record_change(
            contract,
            "G1",
            "修正錯字",
            "編輯",
            "2026-10-19T09:00:00+08:00",
            semantic=False,
        )

        self.assertEqual(invalidated, [])
        self.assertEqual(
            {gate_id: contract["gates"][gate_id]["status"] for gate_id in GATE_ORDER},
            before,
        )

    def test_blocked_gate_can_restart_but_cannot_skip_validation(self):
        contract = self.make_contract()
        begin_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")
        block_gate(
            contract,
            "G0",
            "缺少學員使用情境",
            "course-run",
            "2026-10-18T13:05:00+08:00",
        )
        self.assertEqual(contract["gates"]["G0"]["status"], "BLOCKED")

        begin_gate(contract, "G0", "course-run", "2026-10-18T14:00:00+08:00")
        self.assertEqual(contract["gates"]["G0"]["status"], "IN_PROGRESS")
        with self.assertRaises(ContractStateError):
            _commit_gate_pass(
                contract,
                "G0",
                [],
                "requirements-validator",
                "course-run",
                "2026-10-18T14:05:00+08:00",
            )


class CourseContractExternalActionTests(unittest.TestCase):
    def make_ready_contract(self):
        contract = new_contract(
            "practical-ai",
            "實用生成式 AI",
            "課程團隊",
            "2026-10-18T12:00:00+08:00",
        )
        CourseContractStateTests().pass_gates_through(contract, "G6")
        return contract

    def test_external_authorization_is_separate_from_gate_pass(self):
        contract = self.make_ready_contract()
        manifest_hash = "a" * 64

        propose_external_action(
            contract,
            "publish-1",
            "publish-course",
            "evidence/release-manifest.json",
            manifest_hash,
            "course-ops",
            "2026-10-18T18:00:00+08:00",
        )

        self.assertEqual(contract["gates"]["G6"]["status"], "PASS")
        self.assertEqual(
            contract["external_actions"][0]["status"], "PUBLISH_APPROVAL_REQUIRED"
        )
        with self.assertRaises(ContractStateError):
            assert_external_action_authorized(contract, "publish-1", manifest_hash)

        authorize_external_action(
            contract,
            "publish-1",
            "使用者",
            "2026-10-18T18:05:00+08:00",
            "核准依 manifest 發布",
        )
        assert_external_action_authorized(contract, "publish-1", manifest_hash)

    def test_authorization_rejects_changed_manifest_hash(self):
        contract = self.make_ready_contract()
        propose_external_action(
            contract,
            "publish-1",
            "publish-course",
            "evidence/release-manifest.json",
            "a" * 64,
            "course-ops",
            "2026-10-18T18:00:00+08:00",
        )
        authorize_external_action(
            contract,
            "publish-1",
            "使用者",
            "2026-10-18T18:05:00+08:00",
            "核准依 manifest 發布",
        )

        with self.assertRaises(ContractStateError):
            assert_external_action_authorized(contract, "publish-1", "b" * 64)

    def test_validation_rejects_incomplete_or_inconsistent_external_action(self):
        contract = self.make_ready_contract()
        propose_external_action(
            contract,
            "publish-1",
            "publish-course",
            "evidence/release-manifest.json",
            "a" * 64,
            "course-ops",
            "2026-10-18T18:00:00+08:00",
        )
        del contract["external_actions"][0]["kind"]

        codes = {issue.code for issue in validate_contract(contract)}
        self.assertIn("missing_external_action_field", codes)

        contract["external_actions"][0]["kind"] = "publish-course"
        contract["external_actions"][0]["status"] = "AUTHORIZED"
        codes = {issue.code for issue in validate_contract(contract)}
        self.assertIn("invalid_external_authorization", codes)


class CourseContractMigrationTests(unittest.TestCase):
    def load_v1(self):
        return json.loads(
            (FIXTURES / "course-contracts" / "v1-approved-through-g2.json").read_text(
                encoding="utf-8"
            )
        )

    def test_v1_approved_gate_without_replayable_files_migrates_to_stale(self):
        migrated = migrate_contract_v1(
            self.load_v1(), "course-run", "2026-10-18T19:00:00+08:00"
        )

        self.assertEqual(migrated["schema_version"], 3)
        self.assertEqual(migrated["revision"], 0)
        self.assertTrue(
            all(migrated["gates"][gate_id]["status"] == "STALE" for gate_id in GATE_ORDER)
        )

    def test_v1_unverifiable_gate_stales_from_the_earliest_prior_pass(self):
        legacy = self.load_v1()
        legacy["gates"]["G2"]["evidence"] = []

        migrated = migrate_contract_v1(
            legacy, "course-run", "2026-10-18T19:00:00+08:00"
        )

        self.assertEqual(migrated["gates"]["G2"]["status"], "STALE")

    def test_v1_migration_preserves_approval_history_and_revalidates_review_state(self):
        legacy = self.load_v1()
        legacy["gates"]["G2"]["status"] = "REVIEW"
        legacy["gates"]["G2"]["approved_by"] = None
        legacy["gates"]["G2"]["approved_at"] = None

        migrated = migrate_contract_v1(
            legacy, "course-run", "2026-10-18T19:00:00+08:00"
        )

        self.assertEqual(migrated["schema_version"], 3)
        self.assertEqual(migrated["gates"]["G2"]["status"], "STALE")
        approval_history = [
            item
            for item in migrated["gates"]["G0"]["evidence"]
            if item.get("kind") == "legacy_user_approval"
        ]
        self.assertEqual(approval_history[0]["approved_by"], "使用者")
        self.assertTrue(
            any(change.get("kind") == "schema_migration" for change in migrated["changes"])
        )
        self.assertEqual(validate_contract(migrated), [])

    def test_v2_migration_preserves_replayable_pass(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "evidence" / "g0.json"
            path.parent.mkdir()
            path.write_bytes(b"g0")
            contract = CourseContractStateTests().make_contract()
            begin_gate(contract, "G0", "course-run", "2026-10-18T13:00:00+08:00")
            contract["evidence_index"].append(
                {
                    "id": "g0-evidence",
                    "gate": "G0",
                    "kind": "requirements_record",
                    "path": "evidence/g0.json",
                    "sha256": hashlib.sha256(b"g0").hexdigest(),
                }
            )
            _commit_gate_pass(
                contract,
                "G0",
                ["g0-evidence"],
                "requirements-validator",
                "course-run",
                "2026-10-18T13:05:00+08:00",
            )
            contract["schema_version"] = 2
            del contract["revision"]

            migrated = migrate_contract_v2(
                contract, root, "course-run", "2026-10-18T19:00:00+08:00"
            )

        self.assertEqual(migrated["schema_version"], 3)
        self.assertEqual(migrated["revision"], 0)
        self.assertEqual(migrated["gates"]["G0"]["status"], "PASS")
        self.assertEqual(migrated["gates"]["G1"]["status"], "NOT_STARTED")
        self.assertEqual(validate_contract(migrated), [])

    def test_v2_migration_stales_from_earliest_unverifiable_pass(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            contract = CourseContractStateTests().make_contract()
            for gate_id in GATE_ORDER[:3]:
                begin_gate(contract, gate_id, "course-run", "2026-10-18T13:00:00+08:00")
                evidence_id = f"{gate_id.lower()}-evidence"
                path = root / "evidence" / f"{evidence_id}.json"
                path.parent.mkdir(exist_ok=True)
                content = evidence_id.encode("utf-8")
                path.write_bytes(content)
                contract["evidence_index"].append(
                    {
                        "id": evidence_id,
                        "gate": gate_id,
                        "kind": "test_record",
                        "path": f"evidence/{evidence_id}.json",
                        "sha256": hashlib.sha256(content).hexdigest(),
                    }
                )
                _commit_gate_pass(
                    contract,
                    gate_id,
                    [evidence_id],
                    f"{gate_id.lower()}-validator",
                    "course-run",
                    "2026-10-18T13:05:00+08:00",
                )
            contract["evidence_index"][1]["sha256"] = "f" * 64
            contract["schema_version"] = 2
            del contract["revision"]

            migrated = migrate_contract_v2(
                contract, root, "course-run", "2026-10-18T19:00:00+08:00"
            )

        self.assertEqual(migrated["gates"]["G0"]["status"], "PASS")
        self.assertTrue(
            all(migrated["gates"][gate_id]["status"] == "STALE" for gate_id in GATE_ORDER[1:])
        )
        migration = migrated["changes"][-1]
        self.assertEqual(migration["earliest_stale_gate"], "G1")

    def test_v2_migration_archives_non_reference_history_without_aborting(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            contract = CourseContractStateTests().make_contract()
            contract["schema_version"] = 2
            del contract["revision"]
            contract.pop("evidence_archive", None)
            legacy_history = {
                "kind": "review_note",
                "message": "舊版一般歷史紀錄，沒有檔案路徑。",
                "actor": "reviewer",
            }
            contract["evidence_index"].append(legacy_history)

            migrated = migrate_contract_v2(
                contract, root, "course-run", "2026-10-18T19:00:00+08:00"
            )

        self.assertEqual(migrated["evidence_index"], [])
        self.assertEqual(migrated["evidence_archive"][0]["record"], legacy_history)
        self.assertEqual(validate_contract(migrated), [])

    def test_v2_migration_preserves_metadata_and_same_named_legacy_extra(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            contract = CourseContractStateTests().make_contract()
            contract["schema_version"] = 2
            del contract["revision"]
            contract.pop("evidence_archive", None)
            contract["evidence_index"].append(
                {
                    "id": "g1-history",
                    "gate": "G1",
                    "kind": "research_record",
                    "path": "evidence/g1-history.json",
                    "sha256": "a" * 64,
                    "metadata": {"source": "existing-metadata", "owner": "researcher"},
                    "source": "legacy-top-level",
                }
            )

            migrated = migrate_contract_v2(
                contract, root, "course-run", "2026-10-18T19:00:00+08:00"
            )

        metadata = migrated["evidence_index"][0]["metadata"]
        self.assertEqual(metadata["source"], "existing-metadata")
        self.assertEqual(metadata["owner"], "researcher")
        self.assertEqual(metadata["legacy_fields"]["source"], "legacy-top-level")


if __name__ == "__main__":
    unittest.main()
