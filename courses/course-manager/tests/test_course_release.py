import copy
import hashlib
import io
import json
import signal
import subprocess
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

from src.course_contract import (
    ContractStateError,
    GATE_ORDER,
    authorize_external_action,
    begin_external_action_execution,
    begin_gate,
    load_contract,
    new_contract,
    propose_external_action,
    record_change,
    save_contract_atomic,
    validate_contract,
)
from src.transactions import (
    TransactionError,
    authorize_external_action_atomic,
    bind_external_approval_authority_atomic,
    finish_external_action_execution_atomic,
    mutate_contract_atomic,
)
from tests.approval_authority_fixture import TestApprovalAuthority
from tests.gate_test_support import _commit_gate_pass
from src.course_release import (
    ReleaseAuthorizationError,
    ReleaseCommittedDurabilityError,
    apply_release_proposal,
    build_release_proposal,
    recover_release_proposal,
    scan_course_freshness,
    validate_release_record,
)
from src.verification_authority import public_key_fingerprint
from scripts.course_contract import build_parser as build_contract_parser


class CourseReleaseTests(unittest.TestCase):
    def sha(self, value):
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def make_course_root(self, root: Path):
        (root / "staged").mkdir(parents=True)
        (root / "public").mkdir()
        (root / "staged" / "index.html").write_text(
            "<html>new course</html>", encoding="utf-8"
        )
        (root / "staged" / "search-index.json").write_text(
            '{"course":"new"}\n', encoding="utf-8"
        )
        (root / "public" / "index.html").write_text(
            "<html>old course</html>", encoding="utf-8"
        )
        (root / "untouched.txt").write_text("preserve me", encoding="utf-8")

    def valid_release_record(self):
        checks = []
        for name in (
            "technical",
            "links",
            "registration",
            "access",
            "rollback",
            "maintenance",
        ):
            checks.append(
                {
                    "id": name,
                    "result": "PASS",
                    "evidence": {
                        "path": f"evidence/{name}.json",
                        "sha256": self.sha(name),
                    },
                }
            )
        return {
            "schema_version": 1,
            "course_id": "demo-course",
            "g5_status": "PASS",
            "g6_state": "READY_TO_PUBLISH",
            "published": False,
            "checks": checks,
            "changes": [
                {
                    "source_path": "staged/index.html",
                    "target_path": "public/index.html",
                },
                {
                    "source_path": "staged/search-index.json",
                    "target_path": "public/search-index.json",
                },
            ],
            "maintenance": {
                "owner": "course-ops",
                "cadence": "quarterly",
                "freshness_sources": ["official release notes", "learner reports"],
                "next_review": "2027-01-18",
            },
        }

    def write_authorized_contract(self, path: Path, proposal, *, expires_at=None):
        authority = TestApprovalAuthority()
        contract = new_contract(
            "demo-course",
            "示範課程",
            "course-run",
            "2026-10-18T12:00:00+08:00",
        )
        authority.bind(contract)
        for gate_id in GATE_ORDER:
            begin_gate(
                contract, gate_id, "course-run", "2026-10-18T17:00:00+08:00"
            )
            evidence_id = f"{gate_id.casefold()}-evidence"
            contract["evidence_index"].append(
                {
                    "id": evidence_id,
                    "gate": gate_id,
                    "kind": "test_record",
                    "path": f"evidence/{evidence_id}.json",
                    "sha256": self.sha(evidence_id),
                }
            )
            _commit_gate_pass(
                contract,
                gate_id,
                [evidence_id],
                f"{gate_id.casefold()}-validator",
                "course-run",
                "2026-10-18T17:05:00+08:00",
            )
        save_contract_atomic(path, contract)
        proposed = mutate_contract_atomic(
            path,
            lambda current: propose_external_action(
                current,
                proposal["action_id"],
                "course-release",
                "release-proposal.json",
                proposal["manifest_sha256"],
                "course-ops",
                "2026-10-18T18:00:00+08:00",
            ),
            expected_revision=0,
        )
        receipt_kwargs = {"expires_at": expires_at} if expires_at else {}
        receipt = authority.issue(proposed, proposal["action_id"], **receipt_kwargs)
        authorize_external_action_atomic(
            path,
            proposal["action_id"],
            receipt,
            "2026-10-18T18:05:00+00:00",
            expected_revision=proposed["revision"],
        )

    def test_g6_pass_means_ready_not_published(self):
        record = self.valid_release_record()

        self.assertEqual(validate_release_record(record), [])
        self.assertEqual(record["g6_state"], "READY_TO_PUBLISH")
        self.assertFalse(record["published"])

        published = copy.deepcopy(record)
        published["published"] = True
        codes = {issue.code for issue in validate_release_record(published)}
        self.assertIn("g6_cannot_claim_published", codes)

    def test_release_proposal_lists_exact_targets_hashes_backup_and_rollback(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)

            proposal = build_release_proposal(root, self.valid_release_record())

            self.assertEqual(proposal["status"], "PUBLISH_APPROVAL_REQUIRED")
            self.assertEqual(len(proposal["manifest"]["targets"]), 2)
            target = proposal["manifest"]["targets"][0]
            self.assertEqual(target["before_sha256"], self.sha("<html>old course</html>"))
            self.assertEqual(target["after_sha256"], self.sha("<html>new course</html>"))
            self.assertTrue(target["backup_path"].startswith(".release-backups/"))
            self.assertEqual(
                proposal["manifest_sha256"],
                self.sha(
                    json.dumps(
                        proposal["manifest"],
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                ),
            )
            self.assertEqual(
                {item["target_path"] for item in proposal["manifest"]["rollback"]["targets"]},
                {"public/index.html", "public/search-index.json"},
            )

    def test_release_paths_require_unambiguous_posix_relative_syntax(self):
        for unsafe in ("C:staged-index.html", "staged\\index.html"):
            with self.subTest(path=unsafe):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    self.make_course_root(root)
                    (root / unsafe).write_text("new", encoding="utf-8")
                    record = self.valid_release_record()
                    record["changes"] = [
                        {
                            "source_path": unsafe,
                            "target_path": "public/index.html",
                        }
                    ]

                    with self.assertRaisesRegex(ValueError, "POSIX relative"):
                        build_release_proposal(root, record)

    def test_apply_refuses_missing_mismatched_or_consumed_authorization(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            save_contract_atomic(
                contract_path,
                new_contract(
                    "demo-course",
                    "示範課程",
                    "course-run",
                    "2026-10-18T12:00:00+08:00",
                ),
            )
            with self.assertRaises(ReleaseAuthorizationError):
                apply_release_proposal(proposal_path, contract_path)

    def test_caller_supplied_approver_string_is_not_authority(self):
        contract = new_contract(
            "demo-course",
            "示範課程",
            "course-run",
            "2026-10-18T12:00:00+08:00",
        )
        for gate_id in GATE_ORDER:
            begin_gate(contract, gate_id, "course-run", "2026-10-18T17:00:00+08:00")
            evidence_id = f"{gate_id.casefold()}-evidence"
            contract["evidence_index"].append(
                {
                    "id": evidence_id,
                    "gate": gate_id,
                    "kind": "test_record",
                    "path": f"evidence/{evidence_id}.json",
                    "sha256": self.sha(evidence_id),
                }
            )
            _commit_gate_pass(
                contract,
                gate_id,
                [evidence_id],
                f"{gate_id.casefold()}-validator",
                "course-run",
                "2026-10-18T17:05:00+08:00",
            )
        propose_external_action(
            contract,
            "course-release-deadbeef",
            "course-release",
            "release-proposal.json",
            "a" * 64,
            "course-ops",
            "2026-10-18T18:00:00+08:00",
        )

        with self.assertRaisesRegex(ContractStateError, "receipt"):
            authorize_external_action(
                contract,
                "course-release-deadbeef",
                "caller-controlled-name",
                "2026-10-18T18:05:00+08:00",
                "caller-controlled-note",
            )

    def test_contract_mutation_after_authorization_invalidates_apply(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)

            mutated = mutate_contract_atomic(
                contract_path,
                lambda contract: record_change(
                    contract,
                    "G5",
                    "authorization snapshot is no longer current",
                    "course-run",
                    "2026-10-18T18:06:00+08:00",
                    True,
                ),
            )

            self.assertEqual(mutated["gates"]["G6"]["status"], "STALE")
            self.assertEqual(
                mutated["external_actions"][0]["status"], "INVALIDATED"
            )

            with self.assertRaises(ReleaseAuthorizationError):
                apply_release_proposal(proposal_path, contract_path)

            self.write_authorized_contract(contract_path, proposal)
            mismatched = json.loads(proposal_path.read_text(encoding="utf-8"))
            mismatched["manifest"]["targets"][0]["after_sha256"] = "0" * 64
            proposal_path.write_text(json.dumps(mismatched), encoding="utf-8")
            with self.assertRaises(ReleaseAuthorizationError):
                apply_release_proposal(proposal_path, contract_path)

            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            apply_release_proposal(proposal_path, contract_path)
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            with self.assertRaises(ReleaseAuthorizationError):
                apply_release_proposal(proposal_path, contract_path)

    def test_apply_modifies_only_manifest_targets_and_records_result(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)
            untouched_before = (root / "untouched.txt").read_bytes()

            apply_release_proposal(proposal_path, contract_path)

            self.assertEqual(
                (root / "public" / "index.html").read_text(encoding="utf-8"),
                "<html>new course</html>",
            )
            self.assertEqual(
                (root / "public" / "search-index.json").read_text(encoding="utf-8"),
                '{"course":"new"}\n',
            )
            self.assertEqual((root / "untouched.txt").read_bytes(), untouched_before)
            applied = json.loads(proposal_path.read_text(encoding="utf-8"))
            self.assertEqual(applied["status"], "CONSUMED")
            self.assertEqual(applied["result"]["outcome"], "PASS")
            self.assertEqual(
                set(applied["result"]["modified_targets"]),
                {"public/index.html", "public/search-index.json"},
            )
            for target in proposal["manifest"]["targets"]:
                if target["before_sha256"] is not None:
                    self.assertTrue((root / target["backup_path"]).is_file())

    def test_authorization_binds_revision_g6_evidence_manifest_and_expiry(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            contract_path = root / "course-contract.json"
            self.write_authorized_contract(contract_path, proposal)
            contract = load_contract(contract_path)
            authorization = contract["external_actions"][0]["authorization"]

            self.assertEqual(
                authorization["contract_instance_id"],
                contract["contract_instance_id"],
            )
            self.assertEqual(
                authorization["g6_source_revision"],
                contract["gates"]["G6"]["source_revision"],
            )
            self.assertEqual(authorization["action_id"], proposal["action_id"])
            self.assertEqual(
                authorization["manifest_sha256"], proposal["manifest_sha256"]
            )
            self.assertRegex(authorization["approval_basis_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(
                authorization["interaction"]["kind"], "explicit_user_approval"
            )

    def test_execute_reverifies_receipt_signature_from_disk(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)
            tampered = load_contract(contract_path)
            tampered["external_actions"][0]["authorization"]["signature"] = "AAAA"
            save_contract_atomic(contract_path, tampered)

            with self.assertRaisesRegex(ReleaseAuthorizationError, "signature"):
                apply_release_proposal(proposal_path, contract_path)
            self.assertEqual(
                (root / "public/index.html").read_text(encoding="utf-8"),
                "<html>old course</html>",
            )

    def test_execute_rejects_receipt_after_its_expiry(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            contract_path = root / "course-contract.json"
            self.write_authorized_contract(
                contract_path,
                proposal,
                expires_at="2026-10-18T18:05:30+00:00",
            )
            contract = load_contract(contract_path)

            with self.assertRaisesRegex(ContractStateError, "expired"):
                begin_external_action_execution(
                    contract,
                    proposal["action_id"],
                    proposal["manifest_sha256"],
                    proposal["revision"],
                    "2026-10-18T18:06:00+00:00",
                )

    def test_two_parallel_apply_calls_have_one_execution_owner(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)
            barrier = threading.Barrier(2)

            def attempt():
                barrier.wait()
                try:
                    apply_release_proposal(proposal_path, contract_path)
                    return "executed"
                except ReleaseAuthorizationError:
                    return "rejected"

            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(lambda _: attempt(), range(2)))

            self.assertEqual(sorted(results), ["executed", "rejected"])
            contract = load_contract(contract_path)
            self.assertEqual(contract["external_actions"][0]["status"], "CONSUMED")

    def test_two_parallel_processes_have_one_execution_owner(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            start_path = root / "start-race"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)
            script = (
                "import sys,time\n"
                "from pathlib import Path\n"
                "from src.course_release import apply_release_proposal,ReleaseAuthorizationError\n"
                "while not Path(sys.argv[3]).exists(): time.sleep(0.001)\n"
                "try:\n"
                "    apply_release_proposal(Path(sys.argv[1]),Path(sys.argv[2]))\n"
                "except ReleaseAuthorizationError:\n"
                "    raise SystemExit(3)\n"
            )
            command = [
                sys.executable,
                "-c",
                script,
                str(proposal_path),
                str(contract_path),
                str(start_path),
            ]
            children = [
                subprocess.Popen(
                    command,
                    cwd=Path(__file__).resolve().parents[1],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                for _ in range(2)
            ]
            start_path.write_text("go", encoding="utf-8")
            results = [child.communicate(timeout=20) for child in children]
            codes = [child.returncode for child in children]
            self.assertEqual(sorted(codes), [0, 3], results)

    def test_generic_contract_callback_cannot_claim_release_execution(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)
            contract = load_contract(contract_path)

            with self.assertRaisesRegex(TransactionError, "dedicated"):
                mutate_contract_atomic(
                    contract_path,
                    lambda current: begin_external_action_execution(
                        current,
                        proposal["action_id"],
                        proposal["manifest_sha256"],
                        proposal["revision"],
                        "2026-10-18T18:06:00+00:00",
                    ),
                    expected_revision=contract["revision"],
                )

    def test_generic_contract_callback_cannot_replace_governed_approval_key(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            contract_path = root / "course-contract.json"
            self.write_authorized_contract(contract_path, proposal)
            attacker = TestApprovalAuthority(key_slot=2)

            with self.assertRaisesRegex(TransactionError, "governance"):
                mutate_contract_atomic(
                    contract_path,
                    lambda current: current["governance"].update(
                        {
                            "approval_authority": {
                                "authority_id": attacker.authority_id,
                                "algorithm": "RSASSA-PKCS1-v1_5-SHA256",
                                "public_key": attacker.public_key,
                                "public_key_fingerprint": public_key_fingerprint(
                                    attacker.public_key
                                ),
                            }
                        }
                    ),
                )

    def test_approval_authority_enrollment_requires_no_actions_or_receipts(self):
        authority = TestApprovalAuthority()
        for field, value in (
            (
                "external_actions",
                [
                    {
                        "id": "pending-release",
                        "kind": "course-release",
                        "status": "PUBLISH_APPROVAL_REQUIRED",
                        "manifest_path": "release-proposal.json",
                        "manifest_sha256": "a" * 64,
                        "proposed_by": "course-ops",
                        "proposed_at": "2026-10-18T18:00:00+08:00",
                        "approval_basis_sha256": None,
                        "authorized_revision": None,
                        "authorization": None,
                        "execution": None,
                    }
                ],
            ),
            (
                "consumed_trial_receipts",
                [
                    {
                        "receipt_id": "historical-receipt",
                        "nonce": "historical-nonce",
                        "gate": "G4",
                        "consumed_at": "2026-10-18T17:00:00+08:00",
                    }
                ],
            ),
        ):
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as temp_dir:
                    contract_path = Path(temp_dir) / "course-contract.json"
                    contract = new_contract(
                        "demo-course",
                        "示範課程",
                        "course-run",
                        "2026-10-18T12:00:00+08:00",
                    )
                    contract[field] = copy.deepcopy(value)
                    save_contract_atomic(contract_path, contract)
                    before = contract_path.read_bytes()

                    with self.assertRaisesRegex(
                        ContractStateError, "no actions or receipts"
                    ):
                        bind_external_approval_authority_atomic(
                            contract_path,
                            authority.authority_id,
                            authority.public_key,
                            expected_revision=0,
                        )

                    self.assertEqual(contract_path.read_bytes(), before)
                    self.assertEqual(load_contract(contract_path)["revision"], 0)

    def test_generic_transaction_cannot_append_preauthorized_or_dirty_action(self):
        authority = TestApprovalAuthority()
        contract = new_contract(
            "demo-course",
            "示範課程",
            "course-run",
            "2026-10-18T12:00:00+08:00",
        )
        authority.bind(contract)
        for gate_id in GATE_ORDER:
            begin_gate(
                contract, gate_id, "course-run", "2026-10-18T17:00:00+08:00"
            )
            evidence_id = f"{gate_id.casefold()}-evidence"
            contract["evidence_index"].append(
                {
                    "id": evidence_id,
                    "gate": gate_id,
                    "kind": "test_record",
                    "path": f"evidence/{evidence_id}.json",
                    "sha256": self.sha(evidence_id),
                }
            )
            _commit_gate_pass(
                contract,
                gate_id,
                [evidence_id],
                f"{gate_id.casefold()}-validator",
                "course-run",
                "2026-10-18T17:05:00+08:00",
            )
        propose_external_action(
            contract,
            "forged-release",
            "course-release",
            "release-proposal.json",
            "a" * 64,
            "course-ops",
            "2026-10-18T18:00:00+08:00",
        )
        pending = copy.deepcopy(contract["external_actions"].pop())
        forged = copy.deepcopy(contract)
        forged["external_actions"].append(copy.deepcopy(pending))
        receipt = authority.issue(forged, "forged-release")
        authorize_external_action(
            forged,
            "forged-release",
            receipt,
            "2026-10-18T18:05:00+00:00",
        )
        authorized = copy.deepcopy(forged["external_actions"][0])
        execution = {
            "proposal_revision": 1,
            "started_at": "2026-10-18T18:06:00+00:00",
            "finished_at": None,
            "outcome": "IN_PROGRESS",
            "modified_targets": [],
            "error": None,
        }
        cases = {}
        for status in ("AUTHORIZED", "EXECUTING", "CONSUMED", "FAILED", "INVALIDATED"):
            action = copy.deepcopy(authorized)
            action["status"] = status
            if status in {"EXECUTING", "CONSUMED", "FAILED"}:
                action["execution"] = copy.deepcopy(execution)
                if status != "EXECUTING":
                    action["execution"].update(
                        {
                            "finished_at": "2026-10-18T18:07:00+00:00",
                            "outcome": (
                                "PASS" if status == "CONSUMED" else "FAIL_ROLLED_BACK"
                            ),
                        }
                    )
            cases[f"direct-{status.casefold()}"] = action
        cases["pending-with-authorization"] = copy.deepcopy(authorized)
        cases["pending-with-authorization"]["status"] = "PUBLISH_APPROVAL_REQUIRED"
        pending_execution = copy.deepcopy(pending)
        pending_execution["execution"] = execution
        cases["pending-with-execution"] = pending_execution

        for name, action in cases.items():
            with self.subTest(case=name):
                with tempfile.TemporaryDirectory() as temp_dir:
                    contract_path = Path(temp_dir) / "course-contract.json"
                    save_contract_atomic(contract_path, contract)
                    before = contract_path.read_bytes()
                    with self.assertRaisesRegex(TransactionError, "initial|invalid"):
                        mutate_contract_atomic(
                            contract_path,
                            lambda current, value=action: current[
                                "external_actions"
                            ].append(copy.deepcopy(value)),
                            expected_revision=0,
                        )
                    self.assertEqual(contract_path.read_bytes(), before)
                    self.assertEqual(load_contract(contract_path)["revision"], 0)

    def test_runtime_rejects_malformed_authorization_and_execution_shapes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            contract_path = root / "course-contract.json"
            self.write_authorized_contract(contract_path, proposal)
            authorized = load_contract(contract_path)

            bad_receipt = copy.deepcopy(authorized)
            bad_receipt["external_actions"][0]["authorization"][
                "contract_revision"
            ] = True
            self.assertIn(
                "invalid_external_authorization",
                {issue.code for issue in validate_contract(bad_receipt)},
            )

            bad_execution = copy.deepcopy(authorized)
            action = bad_execution["external_actions"][0]
            action["status"] = "EXECUTING"
            action["execution"] = {"proposal_revision": 1}
            self.assertIn(
                "invalid_external_execution",
                {issue.code for issue in validate_contract(bad_execution)},
            )

    def test_sigkill_before_and_after_each_target_recovers_once_without_replay(self):
        checkpoints = [
            ("before_replace", 0),
            ("after_replace", 0),
            ("before_replace", 1),
            ("after_replace", 1),
        ]
        for phase, target_index in checkpoints:
            with self.subTest(phase=phase, target_index=target_index):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    self.make_course_root(root)
                    proposal = build_release_proposal(root, self.valid_release_record())
                    proposal_path = root / "release-proposal.json"
                    contract_path = root / "course-contract.json"
                    proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
                    self.write_authorized_contract(contract_path, proposal)
                    script = (
                        "import os,signal,sys\n"
                        "from pathlib import Path\n"
                        "import src.course_release as release\n"
                        f"phase={phase!r}; index={target_index!r}\n"
                        "def crash(p,i):\n"
                        "    if (p,i)==(phase,index): os.kill(os.getpid(), signal.SIGKILL)\n"
                        "release._crash_checkpoint=crash\n"
                        "release.apply_release_proposal(Path(sys.argv[1]), Path(sys.argv[2]))\n"
                    )
                    completed = subprocess.run(
                        [
                            sys.executable,
                            "-c",
                            script,
                            str(proposal_path),
                            str(contract_path),
                        ],
                        cwd=Path(__file__).resolve().parents[1],
                        check=False,
                    )
                    self.assertEqual(completed.returncode, -signal.SIGKILL)

                    recover_release_proposal(proposal_path, contract_path)
                    recover_release_proposal(proposal_path, contract_path)

                    self.assertEqual(
                        (root / "public/index.html").read_text(encoding="utf-8"),
                        "<html>old course</html>",
                    )
                    self.assertFalse((root / "public/search-index.json").exists())
                    recovered = json.loads(proposal_path.read_text(encoding="utf-8"))
                    self.assertEqual(recovered["status"], "FAILED")
                    contract = load_contract(contract_path)
                    self.assertEqual(
                        contract["external_actions"][0]["status"], "FAILED"
                    )
                    proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
                    with self.assertRaises(ReleaseAuthorizationError):
                        apply_release_proposal(proposal_path, contract_path)

    def test_recover_uses_contract_authority_when_proposal_status_is_tampered(self):
        for tampered_status in (
            "FAILED",
            "CONSUMED",
            "PUBLISH_APPROVAL_REQUIRED",
        ):
            with self.subTest(status=tampered_status):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    self.make_course_root(root)
                    proposal = build_release_proposal(root, self.valid_release_record())
                    proposal_path = root / "release-proposal.json"
                    contract_path = root / "course-contract.json"
                    proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
                    self.write_authorized_contract(contract_path, proposal)

                    def crash_after_first_target(phase, index):
                        if (phase, index) == ("after_replace", 0):
                            raise SystemExit("injected interruption")

                    import src.course_release as release

                    with mock.patch.object(
                        release,
                        "_crash_checkpoint",
                        side_effect=crash_after_first_target,
                    ):
                        with self.assertRaises(SystemExit):
                            apply_release_proposal(proposal_path, contract_path)
                    tampered = json.loads(proposal_path.read_text(encoding="utf-8"))
                    tampered["status"] = tampered_status
                    if tampered_status == "FAILED":
                        tampered["result"] = {
                            "outcome": "FAIL_ROLLED_BACK",
                            "modified_targets": [],
                            "finished_at": "attacker-controlled",
                            "authorization_consumed": True,
                        }
                    proposal_path.write_text(json.dumps(tampered), encoding="utf-8")

                    recover_release_proposal(proposal_path, contract_path)
                    recover_release_proposal(proposal_path, contract_path)

                    self.assertEqual(
                        (root / "public/index.html").read_text(encoding="utf-8"),
                        "<html>old course</html>",
                    )
                    self.assertFalse((root / "public/search-index.json").exists())
                    self.assertEqual(
                        load_contract(contract_path)["external_actions"][0]["status"],
                        "FAILED",
                    )
                    recovered = json.loads(
                        proposal_path.read_text(encoding="utf-8")
                    )
                    self.assertEqual(recovered["status"], "FAILED")
                    self.assertEqual(
                        recovered["result"]["modified_targets"],
                        ["public/index.html"],
                    )

    def test_recover_failed_contract_overrides_consumed_proposal_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)

            def crash_after_first_target(phase, index):
                if (phase, index) == ("after_replace", 0):
                    raise SystemExit("injected interruption")

            import src.course_release as release

            with mock.patch.object(
                release, "_crash_checkpoint", side_effect=crash_after_first_target
            ):
                with self.assertRaises(SystemExit):
                    apply_release_proposal(proposal_path, contract_path)
            contract = load_contract(contract_path)
            finish_external_action_execution_atomic(
                contract_path,
                proposal["action_id"],
                "FAILED",
                ["public/index.html"],
                "2026-10-18T18:07:00+00:00",
                "injected external failure record",
                expected_revision=contract["revision"],
            )
            tampered = json.loads(proposal_path.read_text(encoding="utf-8"))
            tampered["status"] = "CONSUMED"
            proposal_path.write_text(json.dumps(tampered), encoding="utf-8")

            recover_release_proposal(proposal_path, contract_path)

            self.assertEqual(
                (root / "public/index.html").read_text(encoding="utf-8"),
                "<html>old course</html>",
            )
            self.assertEqual(
                json.loads(proposal_path.read_text(encoding="utf-8"))["status"],
                "FAILED",
            )

    def test_recover_fails_closed_when_executing_journal_is_tampered(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)

            def crash_after_first_target(phase, index):
                if (phase, index) == ("after_replace", 0):
                    raise SystemExit("injected interruption")

            import src.course_release as release

            with mock.patch.object(
                release, "_crash_checkpoint", side_effect=crash_after_first_target
            ):
                with self.assertRaises(SystemExit):
                    apply_release_proposal(proposal_path, contract_path)
            tampered = json.loads(proposal_path.read_text(encoding="utf-8"))
            tampered["journal"]["targets"] = []
            tampered["status"] = "FAILED"
            proposal_path.write_text(json.dumps(tampered), encoding="utf-8")

            with self.assertRaisesRegex(ReleaseAuthorizationError, "journal"):
                recover_release_proposal(proposal_path, contract_path)

            self.assertEqual(
                load_contract(contract_path)["external_actions"][0]["status"],
                "EXECUTING",
            )
            self.assertEqual(
                (root / "public/index.html").read_text(encoding="utf-8"),
                "<html>new course</html>",
            )

    def test_recover_fails_closed_when_required_backup_is_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)

            def crash_after_first_target(phase, index):
                if (phase, index) == ("after_replace", 0):
                    raise SystemExit("injected interruption")

            import src.course_release as release

            with mock.patch.object(
                release, "_crash_checkpoint", side_effect=crash_after_first_target
            ):
                with self.assertRaises(SystemExit):
                    apply_release_proposal(proposal_path, contract_path)
            current = json.loads(proposal_path.read_text(encoding="utf-8"))
            backup = root / current["manifest"]["targets"][0]["backup_path"]
            backup.unlink()

            with self.assertRaisesRegex(ReleaseAuthorizationError, "backup"):
                recover_release_proposal(proposal_path, contract_path)

            self.assertEqual(
                load_contract(contract_path)["external_actions"][0]["status"],
                "EXECUTING",
            )
            self.assertEqual(
                json.loads(proposal_path.read_text(encoding="utf-8"))["status"],
                "EXECUTING",
            )

    def test_recover_fails_closed_when_contract_and_proposal_identity_diverge(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)

            def crash_after_first_target(phase, index):
                if (phase, index) == ("after_replace", 0):
                    raise SystemExit("injected interruption")

            import src.course_release as release

            with mock.patch.object(
                release, "_crash_checkpoint", side_effect=crash_after_first_target
            ):
                with self.assertRaises(SystemExit):
                    apply_release_proposal(proposal_path, contract_path)
            tampered = json.loads(proposal_path.read_text(encoding="utf-8"))
            tampered["manifest"]["course_id"] = "different-course"
            tampered["manifest_sha256"] = self.sha(
                json.dumps(
                    tampered["manifest"],
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
            )
            proposal_path.write_text(json.dumps(tampered), encoding="utf-8")

            with self.assertRaisesRegex(ReleaseAuthorizationError, "identity"):
                recover_release_proposal(proposal_path, contract_path)

            self.assertEqual(
                load_contract(contract_path)["external_actions"][0]["status"],
                "EXECUTING",
            )
            self.assertEqual(
                (root / "public/index.html").read_text(encoding="utf-8"),
                "<html>new course</html>",
            )

    def test_recovery_uses_journal_and_backups_when_staged_sources_are_gone(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)
            script = (
                "import os,signal,sys\n"
                "from pathlib import Path\n"
                "import src.course_release as release\n"
                "def crash(phase,index):\n"
                "    if (phase,index)==('after_replace',0): "
                "os.kill(os.getpid(), signal.SIGKILL)\n"
                "release._crash_checkpoint=crash\n"
                "release.apply_release_proposal(Path(sys.argv[1]), Path(sys.argv[2]))\n"
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    script,
                    str(proposal_path),
                    str(contract_path),
                ],
                cwd=Path(__file__).resolve().parents[1],
                check=False,
            )
            self.assertEqual(completed.returncode, -signal.SIGKILL)
            (root / "staged/index.html").unlink()
            (root / "staged/search-index.json").unlink()

            recover_release_proposal(proposal_path, contract_path)

            self.assertEqual(
                (root / "public/index.html").read_text(encoding="utf-8"),
                "<html>old course</html>",
            )
            self.assertFalse((root / "public/search-index.json").exists())
            self.assertEqual(
                load_contract(contract_path)["external_actions"][0]["status"],
                "FAILED",
            )

    def test_normal_replace_exception_rolls_back_and_consumes_authorization(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)
            import src.course_release as release

            original = release._atomic_replace_from_source
            calls = 0

            def fail_second_target(source, target):
                nonlocal calls
                if ".release-backups" not in str(target):
                    calls += 1
                    if calls == 2:
                        raise OSError("injected normal failure")
                return original(source, target)

            with mock.patch.object(
                release, "_atomic_replace_from_source", side_effect=fail_second_target
            ):
                with self.assertRaisesRegex(OSError, "injected normal failure"):
                    apply_release_proposal(proposal_path, contract_path)

            self.assertEqual(
                (root / "public/index.html").read_text(encoding="utf-8"),
                "<html>old course</html>",
            )
            self.assertFalse((root / "public/search-index.json").exists())
            self.assertEqual(
                load_contract(contract_path)["external_actions"][0]["status"],
                "FAILED",
            )
            self.assertEqual(
                json.loads(proposal_path.read_text(encoding="utf-8"))["status"],
                "FAILED",
            )

    def test_manifest_is_rechecked_immediately_before_each_target_replace(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)
            import src.course_release as release

            tampered = False

            def tamper_at_checkpoint(phase, index):
                nonlocal tampered
                if not tampered and (phase, index) == ("before_replace", 0):
                    current = json.loads(proposal_path.read_text(encoding="utf-8"))
                    current["manifest"]["course_id"] = "attacker-changed"
                    proposal_path.write_text(json.dumps(current), encoding="utf-8")
                    tampered = True

            with mock.patch.object(
                release, "_crash_checkpoint", side_effect=tamper_at_checkpoint
            ):
                with self.assertRaisesRegex(ReleaseAuthorizationError, "manifest"):
                    apply_release_proposal(proposal_path, contract_path)
            self.assertEqual(
                (root / "public/index.html").read_text(encoding="utf-8"),
                "<html>old course</html>",
            )

    def test_target_directory_fsync_failure_is_committed_uncertain_then_recoverable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            proposal = build_release_proposal(root, self.valid_release_record())
            proposal_path = root / "release-proposal.json"
            contract_path = root / "course-contract.json"
            proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
            self.write_authorized_contract(contract_path, proposal)
            import src.course_release as release

            original = release._fsync_directory
            public_directory = (root / "public").resolve()

            def fail_public_directory(path):
                if Path(path).resolve() == public_directory:
                    raise OSError("injected directory fsync failure")
                return original(path)

            with mock.patch.object(
                release, "_fsync_directory", side_effect=fail_public_directory
            ):
                with self.assertRaises(ReleaseCommittedDurabilityError) as raised:
                    apply_release_proposal(proposal_path, contract_path)
            self.assertTrue(raised.exception.committed)
            self.assertEqual(
                json.loads(proposal_path.read_text(encoding="utf-8"))["status"],
                "EXECUTING",
            )

            recover_release_proposal(proposal_path, contract_path)
            self.assertEqual(
                (root / "public/index.html").read_text(encoding="utf-8"),
                "<html>old course</html>",
            )
            self.assertFalse((root / "public/search-index.json").exists())
            self.assertEqual(
                load_contract(contract_path)["external_actions"][0]["status"],
                "FAILED",
            )

    def test_contract_cli_accepts_receipt_not_approved_by_string(self):
        parser = build_contract_parser()
        args = parser.parse_args(
            [
                "authorize-action",
                "--contract",
                "contract.json",
                "--action-id",
                "release-1",
                "--receipt",
                "approval-receipt.json",
                "--at",
                "2026-10-18T18:05:00+00:00",
            ]
        )
        self.assertEqual(args.receipt, Path("approval-receipt.json"))
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parser.parse_args(
                    [
                        "authorize-action",
                        "--contract",
                        "contract.json",
                        "--action-id",
                        "release-1",
                        "--approved-by",
                        "caller-controlled",
                        "--at",
                        "2026-10-18T18:05:00+00:00",
                    ]
                )

    def test_operator_enrollment_and_receipt_boundary_are_documented(self):
        project_root = Path(__file__).resolve().parents[1]
        documents = [
            project_root
            / "skill-packages/course-run/references/course-contract-routing.md",
            project_root / "docs/course-skill-family-foundation.md",
        ]
        for path in documents:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn("enroll-approval-authority", text)
                self.assertIn("--receipt", text)
                self.assertNotIn("--approved-by", text)
                self.assertIn("course producer", text)

    def test_proposal_path_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            outside = root.parent / f"outside-{root.name}.json"
            proposal = build_release_proposal(root, self.valid_release_record())
            outside.write_text(json.dumps(proposal), encoding="utf-8")
            proposal_path = root / "release-proposal.json"
            proposal_path.symlink_to(outside)
            contract_path = root / "course-contract.json"
            self.write_authorized_contract(contract_path, proposal)
            try:
                with self.assertRaises(ReleaseAuthorizationError):
                    apply_release_proposal(proposal_path, contract_path)
            finally:
                outside.unlink(missing_ok=True)

    def test_proposal_path_with_symlinked_parent_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_course_root(root)
            real_parent = root / "proposals"
            real_parent.mkdir()
            proposal = build_release_proposal(root, self.valid_release_record())
            real_path = real_parent / "release-proposal.json"
            real_path.write_text(json.dumps(proposal), encoding="utf-8")
            alias = root / "proposal-alias"
            alias.symlink_to(real_parent, target_is_directory=True)
            contract_path = root / "course-contract.json"
            self.write_authorized_contract(contract_path, proposal)

            with self.assertRaisesRegex(ReleaseAuthorizationError, "symbolic"):
                apply_release_proposal(alias / real_path.name, contract_path)

    def test_register_compatibility_entry_dispatches_to_course_ops(self):
        project_root = Path(__file__).resolve().parents[1]
        text = (project_root / "skill-packages/course-register/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("相容入口", text)
        self.assertIn("course-ops", text)
        self.assertNotIn("Step 6：更新 `inject_gate.py`", text)

    def test_refresh_scan_is_read_only_and_routes_stale_items_to_gate(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            html = root / "unit-1.html"
            html.write_text(
                '<main data-platform-version="tool-v1" data-built-at="2026-01-01">課程</main>',
                encoding="utf-8",
            )
            before = html.read_bytes()

            report = scan_course_freshness(root, "2026-10-18")

            self.assertEqual(html.read_bytes(), before)
            self.assertEqual(report["items"][0]["severity"], "STALE")
            self.assertEqual(report["items"][0]["affected_gate"], "G1")
            self.assertIn("recommended_action", report["items"][0])

    def test_refresh_never_edits_metadata_or_republishes(self):
        project_root = Path(__file__).resolve().parents[1]
        skill = (project_root / "skill-packages/course-refresh/SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("Edit", skill.split("---", 2)[1])
        self.assertNotIn("Write", skill.split("---", 2)[1])
        self.assertNotIn("bump-metadata", skill)
        self.assertNotIn("git commit", skill)
        self.assertIn("affected_gate", skill)


if __name__ == "__main__":
    unittest.main()
