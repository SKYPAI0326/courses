import copy
import errno
import hashlib
import importlib
import json
import multiprocessing
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.course_contract import (
    ContractStateError,
    begin_gate,
    block_gate,
    new_contract,
    resolve_gate_blocker,
    save_contract_atomic,
)
from src.course_evidence import canonical_json_bytes, materialize_json_evidence


def _stale_writer(path, start, results):
    start.wait()
    try:
        transactions = importlib.import_module("src.transactions")

        def operation(contract):
            contract["changes"].append(
                {"kind": "concurrency_probe", "pid": os.getpid()}
            )

        value = transactions.mutate_contract_atomic(
            Path(path), operation, expected_revision=0
        )
    except Exception as error:  # pragma: no cover - result is asserted by parent
        results.put(("error", type(error).__name__, str(error)))
    else:
        results.put(("ok", value["revision"]))


class ContractTransactionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.path = self.root / "course-contract.json"
        save_contract_atomic(
            self.path,
            new_contract(
                "transaction-course",
                "Transaction Course",
                "test",
                "2026-10-18T12:00:00+08:00",
            ),
        )

    def tearDown(self):
        self.temporary.cleanup()

    def transactions(self):
        return importlib.import_module("src.transactions")

    def read(self):
        return json.loads(self.path.read_text(encoding="utf-8"))

    def unresolved_contract_with_resolution(self, *, evidence_id="resolution"):
        contract = new_contract(
            "transaction-course",
            "Transaction Course",
            "test",
            "2026-10-18T12:00:00+08:00",
        )
        block_gate(
            contract,
            "G0",
            "missing source",
            "test",
            "2026-10-18T12:01:00+08:00",
        )
        reference = materialize_json_evidence(
            self.root,
            evidence_id=evidence_id,
            gate_id="G0",
            kind="blocker_resolution",
            relative_path=f"evidence/{evidence_id}.json",
            value={"fixed": True},
        )
        contract["evidence_index"].append(reference)
        save_contract_atomic(self.path, contract)
        return contract["gates"]["G0"]["risks"][0]["id"], reference

    def test_successful_mutation_increments_revision_exactly_once(self):
        transactions = self.transactions()

        def operation(contract):
            contract["maintenance"]["owner"] = "course-ops"

        result = transactions.mutate_contract_atomic(self.path, operation)

        self.assertEqual(result["revision"], 1)
        self.assertEqual(self.read(), result)

    def test_mutator_cannot_claim_revision_ownership(self):
        transactions = self.transactions()
        before = self.path.read_bytes()

        def operation(contract):
            contract["revision"] += 1

        with self.assertRaisesRegex(transactions.TransactionError, "revision"):
            transactions.mutate_contract_atomic(self.path, operation)

        self.assertEqual(self.path.read_bytes(), before)

    def test_two_stale_writers_have_one_winner_and_no_lost_update(self):
        transactions = self.transactions()
        context = multiprocessing.get_context("spawn")
        start = context.Event()
        results = context.Queue()
        workers = [
            context.Process(target=_stale_writer, args=(str(self.path), start, results))
            for _ in range(2)
        ]
        for worker in workers:
            worker.start()
        start.set()
        outcomes = [results.get(timeout=10) for _ in workers]
        for worker in workers:
            worker.join(timeout=10)
            self.assertEqual(worker.exitcode, 0)

        self.assertEqual(sum(item[0] == "ok" for item in outcomes), 1)
        errors = [item for item in outcomes if item[0] == "error"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][1], "RevisionConflictError", outcomes)
        persisted = self.read()
        self.assertEqual(persisted["revision"], 1)
        self.assertEqual(len(persisted["changes"]), 1)
        self.assertTrue(issubclass(transactions.RevisionConflictError, Exception))

    @unittest.skipUnless(os.name == "posix", "POSIX advisory lock test")
    def test_lock_timeout_is_explicit_and_does_not_write(self):
        import fcntl

        transactions = self.transactions()
        before = self.path.read_bytes()
        lock_path = self.path.with_name(f".{self.path.name}.lock")
        with lock_path.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(transactions.LockTimeoutError):
                transactions.mutate_contract_atomic(
                    self.path,
                    lambda contract: contract["maintenance"].update(owner="x"),
                    lock_timeout=0.05,
                )

        self.assertEqual(self.path.read_bytes(), before)

    def test_operation_exception_leaves_original_bytes_unchanged(self):
        transactions = self.transactions()
        before = self.path.read_bytes()

        def operation(contract):
            contract["maintenance"]["owner"] = "partial"
            raise RuntimeError("boom")

        with self.assertRaisesRegex(RuntimeError, "boom"):
            transactions.mutate_contract_atomic(self.path, operation)

        self.assertEqual(self.path.read_bytes(), before)

    def test_directory_fsync_failure_reports_committed_revision(self):
        transactions = self.transactions()

        def operation(contract):
            contract["maintenance"]["owner"] = "course-ops"

        with mock.patch.object(
            transactions.os,
            "fsync",
            side_effect=[None, OSError(errno.EIO, "directory fsync failed")],
        ):
            with self.assertRaises(
                transactions.TransactionCommittedDurabilityError
            ) as raised:
                transactions.mutate_contract_atomic(self.path, operation)

        error = raised.exception
        persisted = self.read()
        self.assertTrue(error.committed)
        self.assertEqual(error.path, self.path)
        self.assertEqual(error.revision, 1)
        self.assertEqual(error.contract, persisted)
        self.assertEqual(persisted["revision"], 1)
        self.assertEqual(persisted["maintenance"]["owner"], "course-ops")

    def test_temporary_file_fsync_failure_is_precommit_and_does_not_write(self):
        transactions = self.transactions()
        before = self.path.read_bytes()

        with mock.patch.object(
            transactions.os,
            "fsync",
            side_effect=OSError(errno.EIO, "temporary file fsync failed"),
        ):
            with self.assertRaises(OSError) as raised:
                transactions.mutate_contract_atomic(
                    self.path,
                    lambda contract: contract["maintenance"].update(
                        owner="course-ops"
                    ),
                )

        self.assertNotIsInstance(
            raised.exception,
            transactions.TransactionCommittedDurabilityError,
        )
        self.assertEqual(self.path.read_bytes(), before)

    def test_invalid_result_leaves_original_bytes_unchanged(self):
        transactions = self.transactions()
        before = self.path.read_bytes()

        with self.assertRaises(transactions.TransactionError):
            transactions.mutate_contract_atomic(
                self.path, lambda contract: contract.update(changes="invalid")
            )

        self.assertEqual(self.path.read_bytes(), before)

    def test_existing_audit_collections_are_append_only(self):
        contract = new_contract(
            "transaction-course",
            "Transaction Course",
            "test",
            "2026-10-18T12:00:00+08:00",
        )
        begin_gate(contract, "G0", "test", "2026-10-18T12:01:00+08:00")
        contract["changes"].extend([{"id": "change-1"}, {"id": "change-2"}])
        contract["evidence_archive"].extend(
            [{"id": "archive-1"}, {"id": "archive-2"}]
        )
        contract["evidence_index"].extend(
            [
                {
                    "id": f"evidence-{index}",
                    "gate": "G0",
                    "kind": "test_record",
                    "path": f"evidence/{index}.json",
                    "sha256": str(index) * 64,
                }
                for index in (1, 2)
            ]
        )
        contract["consumed_trial_receipts"].extend(
            [
                {
                    "receipt_id": f"receipt-{index}",
                    "nonce": f"nonce-{index}",
                    "gate": "G4",
                    "consumed_at": f"2026-10-18T12:0{index}:00+08:00",
                }
                for index in (1, 2)
            ]
        )
        tamper_operations = {
            "gate event modification": lambda value: value["gates"]["G0"][
                "evidence"
            ][0].update(actor="attacker"),
            "change deletion": lambda value: value["changes"].pop(0),
            "archive reorder": lambda value: value["evidence_archive"].reverse(),
            "evidence reference modification": lambda value: value[
                "evidence_index"
            ][0].update(path="evidence/rewritten.json"),
            "receipt deletion": lambda value: value[
                "consumed_trial_receipts"
            ].pop(0),
        }

        for label, operation in tamper_operations.items():
            with self.subTest(label=label):
                save_contract_atomic(self.path, copy.deepcopy(contract))
                before = self.path.read_bytes()

                with self.assertRaisesRegex(
                    self.transactions().TransactionError, "append-only|history"
                ):
                    self.transactions().mutate_contract_atomic(self.path, operation)

                self.assertEqual(self.path.read_bytes(), before)
                self.assertEqual(self.read()["revision"], 0)

    def test_resolved_blocker_and_resolution_audit_cannot_be_rewritten(self):
        contract = new_contract(
            "transaction-course",
            "Transaction Course",
            "test",
            "2026-10-18T12:00:00+08:00",
        )
        block_gate(
            contract,
            "G0",
            "missing source",
            "test",
            "2026-10-18T12:01:00+08:00",
        )
        blocker = contract["gates"]["G0"]["risks"][0]
        resolution_ref = materialize_json_evidence(
            self.root,
            evidence_id="g0-resolution",
            gate_id="G0",
            kind="blocker_resolution",
            relative_path="evidence/g0-resolution.json",
            value={"fixed": True},
        )
        contract["evidence_index"].append(resolution_ref)
        resolve_gate_blocker(
            contract,
            "G0",
            blocker["id"],
            "source added",
            [resolution_ref["id"]],
            "test",
            "2026-10-18T12:02:00+08:00",
            workspace_root=self.root,
        )
        tamper_operations = {
            "resolved blocker": lambda value: value["gates"]["G0"]["risks"][
                0
            ].update(reason="rewritten"),
            "resolution event": lambda value: value["gates"]["G0"]["evidence"][
                -1
            ].update(resolution="rewritten"),
        }

        for label, operation in tamper_operations.items():
            with self.subTest(label=label):
                save_contract_atomic(self.path, copy.deepcopy(contract))
                before = self.path.read_bytes()
                with self.assertRaisesRegex(
                    self.transactions().TransactionError, "append-only|history"
                ):
                    self.transactions().mutate_contract_atomic(self.path, operation)
                self.assertEqual(self.path.read_bytes(), before)

    def test_direct_forged_unresolved_to_resolved_transition_is_rejected(self):
        contract = new_contract(
            "transaction-course",
            "Transaction Course",
            "test",
            "2026-10-18T12:00:00+08:00",
        )
        block_gate(
            contract,
            "G0",
            "missing source",
            "test",
            "2026-10-18T12:01:00+08:00",
        )
        blocker_id = contract["gates"]["G0"]["risks"][0]["id"]
        resolution_ref = materialize_json_evidence(
            self.root,
            evidence_id="forged-resolution",
            gate_id="G0",
            kind="blocker_resolution",
            relative_path="evidence/forged-resolution.json",
            value={"fixed": True},
        )
        contract["evidence_index"].append(resolution_ref)
        save_contract_atomic(self.path, contract)
        before = self.path.read_bytes()

        def forge_resolution(value):
            payload = {
                "blocker_id": blocker_id,
                "resolution": "forged",
                "evidence_ids": [resolution_ref["id"]],
                "actor": "attacker",
                "at": "2026-10-18T12:02:00+08:00",
            }
            resolution_id = "resolution-" + hashlib.sha256(
                canonical_json_bytes(payload)
            ).hexdigest()[:24]
            value["gates"]["G0"]["risks"][0].update(
                resolved=True, resolution_id=resolution_id
            )
            value["gates"]["G0"]["evidence"].append(
                {
                    "id": resolution_id,
                    "kind": "gate_blocker_resolution",
                    **payload,
                    "consumed_evidence": [
                        {
                            "id": resolution_ref["id"],
                            "sha256": resolution_ref["sha256"],
                        }
                    ],
                }
            )

        with self.assertRaisesRegex(
            self.transactions().TransactionError, "resolution API"
        ):
            self.transactions().mutate_contract_atomic(self.path, forge_resolution)

        self.assertEqual(self.path.read_bytes(), before)

    def test_generic_transaction_does_not_expose_resolution_intent_marker(self):
        blocker_id, _ = self.unresolved_contract_with_resolution()
        before = self.path.read_bytes()

        def call_old_marker(contract):
            contract._record_blocker_resolution_transition(  # type: ignore[attr-defined]
                "G0", blocker_id, "resolution-" + "0" * 24
            )

        with self.assertRaises(AttributeError):
            self.transactions().mutate_contract_atomic(self.path, call_old_marker)

        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.read()["revision"], 0)

    def test_generic_transaction_rejects_calling_in_memory_resolution_api(self):
        blocker_id, reference = self.unresolved_contract_with_resolution()
        before = self.path.read_bytes()

        def call_resolution_api(contract):
            resolve_gate_blocker(
                contract,
                "G0",
                blocker_id,
                "source added",
                [reference["id"]],
                "test",
                "2026-10-18T12:02:00+08:00",
                workspace_root=self.root,
            )

        with self.assertRaisesRegex(
            self.transactions().TransactionError,
            "dedicated atomic resolution API",
        ):
            self.transactions().mutate_contract_atomic(
                self.path, call_resolution_api
            )

        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.read()["revision"], 0)

    def test_dedicated_atomic_resolution_succeeds_once(self):
        blocker_id, reference = self.unresolved_contract_with_resolution()

        result = self.transactions().resolve_gate_blocker_atomic(
            self.path,
            "G0",
            blocker_id,
            "source added",
            [reference["id"]],
            "test",
            "2026-10-18T12:02:00+08:00",
            workspace_root=self.root,
            expected_revision=0,
        )

        self.assertEqual(result["revision"], 1)
        blocker = result["gates"]["G0"]["risks"][0]
        self.assertTrue(blocker["resolved"])
        self.assertEqual(self.read(), result)

    def test_dedicated_atomic_resolution_wrong_evidence_and_cas_do_not_write(self):
        blocker_id, reference = self.unresolved_contract_with_resolution()
        before = self.path.read_bytes()

        with self.assertRaisesRegex(
            self.transactions().RevisionConflictError, "revision conflict"
        ):
            self.transactions().resolve_gate_blocker_atomic(
                self.path,
                "G0",
                blocker_id,
                "source added",
                [reference["id"]],
                "test",
                "2026-10-18T12:02:00+08:00",
                workspace_root=self.root,
                expected_revision=9,
            )
        self.assertEqual(self.path.read_bytes(), before)

        (self.root / reference["path"]).write_text(
            '{"tampered":true}\n', encoding="utf-8"
        )
        with self.assertRaisesRegex(ContractStateError, "resolution evidence"):
            self.transactions().resolve_gate_blocker_atomic(
                self.path,
                "G0",
                blocker_id,
                "source added",
                [reference["id"]],
                "test",
                "2026-10-18T12:02:00+08:00",
                workspace_root=self.root,
                expected_revision=0,
            )
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.read()["revision"], 0)

    def test_missing_posix_lock_capability_fails_closed(self):
        transactions = self.transactions()
        before = self.path.read_bytes()

        with mock.patch.object(transactions, "fcntl", None):
            with self.assertRaises(transactions.UnsupportedPlatformError):
                transactions.mutate_contract_atomic(
                    self.path,
                    lambda contract: contract["maintenance"].update(owner="x"),
                )

        self.assertEqual(self.path.read_bytes(), before)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlink support required")
    def test_contract_symlink_is_rejected_without_touching_target(self):
        transactions = self.transactions()
        target = self.root / "outside.json"
        target.write_bytes(self.path.read_bytes())
        link = self.root / "linked-contract.json"
        link.symlink_to(target)
        before = target.read_bytes()

        with self.assertRaises(transactions.UnsafeContractPathError):
            transactions.mutate_contract_atomic(
                link, lambda contract: contract["maintenance"].update(owner="x")
            )

        self.assertEqual(target.read_bytes(), before)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlink support required")
    def test_parent_symlink_is_rejected_without_touching_target(self):
        transactions = self.transactions()
        outside = self.root / "outside"
        outside.mkdir()
        target = outside / "course-contract.json"
        target.write_bytes(self.path.read_bytes())
        linked_parent = self.root / "linked-parent"
        linked_parent.symlink_to(outside, target_is_directory=True)
        before = target.read_bytes()

        with self.assertRaises(transactions.UnsafeContractPathError):
            transactions.mutate_contract_atomic(
                linked_parent / target.name,
                lambda contract: contract["maintenance"].update(owner="x"),
            )

        self.assertEqual(target.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
