from __future__ import annotations

import errno
import json
import os
import secrets
import stat
import time
from pathlib import Path
from typing import Any, Callable, MutableMapping

try:  # Windows and other unsupported hosts must fail closed at call time.
    import fcntl
except ImportError:  # pragma: no cover - exercised only on unsupported platforms
    fcntl = None  # type: ignore[assignment]


class TransactionError(RuntimeError):
    pass


class UnsupportedPlatformError(TransactionError):
    pass


class UnsafeContractPathError(TransactionError):
    pass


class RevisionConflictError(TransactionError):
    pass


class LockTimeoutError(TransactionError):
    pass


ContractOperation = Callable[[MutableMapping[str, Any]], Any]


def _require_supported_platform() -> None:
    if (
        os.name != "posix"
        or fcntl is None
        or not hasattr(os, "O_NOFOLLOW")
        or not hasattr(os, "O_DIRECTORY")
    ):
        raise UnsupportedPlatformError(
            "contract transactions require POSIX flock, O_NOFOLLOW, and O_DIRECTORY"
        )


def _absolute_path_without_symlinks(path: Path) -> Path:
    candidate = path if path.is_absolute() else Path.cwd() / path
    candidate = Path(os.path.abspath(candidate))
    if candidate.name in {"", ".", ".."}:
        raise UnsafeContractPathError("contract path must name a file")
    current = Path(candidate.anchor)
    for part in candidate.parts[1:]:
        current = current / part
        if current.is_symlink():
            # macOS exposes root-owned compatibility aliases such as /var ->
            # /private/var.  They are outside the caller-controlled path while
            # symlinks at any deeper component can redirect the transaction.
            if current.parent == Path(candidate.anchor):
                continue
            raise UnsafeContractPathError(
                f"contract path must not contain symbolic links: {current}"
            )
    return candidate


def _open_regular_at(parent_fd: int, name: str, flags: int, mode: int = 0o600) -> int:
    try:
        descriptor = os.open(
            name,
            flags | os.O_NOFOLLOW,
            mode,
            dir_fd=parent_fd,
        )
    except OSError as error:
        if error.errno in {errno.ELOOP, errno.ENOTDIR}:
            raise UnsafeContractPathError(
                f"transaction path is not a regular non-symlink file: {name}"
            ) from error
        raise
    if not stat.S_ISREG(os.fstat(descriptor).st_mode):
        os.close(descriptor)
        raise UnsafeContractPathError(f"transaction path is not a regular file: {name}")
    return descriptor


def _acquire_lock(lock_fd: int, timeout: float) -> None:
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout < 0:
        raise ValueError("lock_timeout must be a non-negative number")
    deadline = time.monotonic() + float(timeout)
    while True:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except BlockingIOError as error:
            if time.monotonic() >= deadline:
                raise LockTimeoutError(
                    f"timed out after {float(timeout):g}s waiting for contract lock"
                ) from error
            time.sleep(min(0.01, max(0.0, deadline - time.monotonic())))


def _load_from_fd(descriptor: int) -> dict[str, Any]:
    with os.fdopen(os.dup(descriptor), "r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TransactionError("course contract root must be an object")
    return value


def _write_atomic_at(parent_fd: int, name: str, contract: dict[str, Any]) -> None:
    temporary_name: str | None = None
    temporary_fd: int | None = None
    for _ in range(100):
        candidate = f".{name}.{secrets.token_hex(8)}.tmp"
        try:
            temporary_fd = _open_regular_at(
                parent_fd, candidate, os.O_WRONLY | os.O_CREAT | os.O_EXCL
            )
        except FileExistsError:
            continue
        temporary_name = candidate
        break
    if temporary_fd is None or temporary_name is None:
        raise TransactionError("could not allocate a same-directory transaction file")
    try:
        with os.fdopen(temporary_fd, "w", encoding="utf-8") as handle:
            json.dump(contract, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        temporary_fd = None
        os.replace(
            temporary_name,
            name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        os.fsync(parent_fd)
        temporary_name = None
    finally:
        if temporary_fd is not None:
            os.close(temporary_fd)
        if temporary_name is not None:
            try:
                os.unlink(temporary_name, dir_fd=parent_fd)
            except FileNotFoundError:
                pass


def _validation_error(contract: MutableMapping[str, Any]) -> str | None:
    from src.course_contract import validate_contract

    issues = validate_contract(contract)
    if not issues:
        return None
    return "; ".join(f"{issue.path}: {issue.message}" for issue in issues)


def mutate_contract_atomic(
    path: Path | str,
    operation: ContractOperation,
    *,
    expected_revision: int | None = None,
    lock_timeout: float = 10.0,
) -> dict[str, Any]:
    """Apply one validated contract mutation under a same-directory POSIX lock."""

    _require_supported_platform()
    if not callable(operation):
        raise TypeError("operation must be callable")
    if expected_revision is not None and (
        isinstance(expected_revision, bool)
        or not isinstance(expected_revision, int)
        or expected_revision < 0
    ):
        raise ValueError("expected_revision must be a non-negative integer")

    contract_path = _absolute_path_without_symlinks(Path(path))
    parent_fd = os.open(
        contract_path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    )
    lock_fd: int | None = None
    contract_fd: int | None = None
    try:
        lock_name = f".{contract_path.name}.lock"
        for attempt in range(5):
            try:
                lock_fd = _open_regular_at(
                    parent_fd, lock_name, os.O_RDWR | os.O_CREAT, mode=0o600
                )
                break
            except FileNotFoundError:
                if attempt == 4:
                    raise
                time.sleep(0.001)
        if lock_fd is None:  # defensive; the bounded loop either opens or raises
            raise TransactionError("could not open contract lock file")
        _acquire_lock(lock_fd, lock_timeout)
        contract_fd = _open_regular_at(parent_fd, contract_path.name, os.O_RDONLY)
        contract = _load_from_fd(contract_fd)

        schema_version = contract.get("schema_version")
        original_revision = contract.get("revision")
        legacy = schema_version in {1, 2} and original_revision is None
        if not legacy:
            if (
                isinstance(original_revision, bool)
                or not isinstance(original_revision, int)
                or original_revision < 0
            ):
                raise TransactionError("contract revision must be a non-negative integer")
            details = _validation_error(contract)
            if details:
                raise TransactionError(f"refusing to mutate invalid contract: {details}")
            base_revision = original_revision
        else:
            base_revision = -1

        if expected_revision is not None and base_revision != expected_revision:
            raise RevisionConflictError(
                f"revision conflict: expected {expected_revision}, found {base_revision}"
            )

        operation(contract)
        after_operation_revision = contract.get("revision")
        if legacy:
            if after_operation_revision not in {None, 0}:
                raise TransactionError("legacy migration attempted to own contract revision")
        elif after_operation_revision != base_revision:
            raise TransactionError(
                "operation changed revision; the transaction is the single revision owner"
            )
        contract["revision"] = base_revision + 1

        details = _validation_error(contract)
        if details:
            raise TransactionError(f"mutation produced an invalid contract: {details}")

        _write_atomic_at(parent_fd, contract_path.name, contract)
        return contract
    finally:
        if contract_fd is not None:
            os.close(contract_fd)
        if lock_fd is not None:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            finally:
                os.close(lock_fd)
        os.close(parent_fd)
