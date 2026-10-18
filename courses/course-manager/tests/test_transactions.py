import copy
import importlib
import json
import multiprocessing
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.course_contract import new_contract, save_contract_atomic


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

    def test_invalid_result_leaves_original_bytes_unchanged(self):
        transactions = self.transactions()
        before = self.path.read_bytes()

        with self.assertRaises(transactions.TransactionError):
            transactions.mutate_contract_atomic(
                self.path, lambda contract: contract.update(changes="invalid")
            )

        self.assertEqual(self.path.read_bytes(), before)

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
