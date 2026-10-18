from __future__ import annotations

import errno
import hashlib
import json
import os
import re
import secrets
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Mapping


GATE_IDS: tuple[str, ...] = tuple(f"G{index}" for index in range(7))
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
REFERENCE_FIELDS = frozenset(
    {"id", "gate", "kind", "path", "sha256", "maturity", "metadata"}
)
REQUIRED_REFERENCE_FIELDS = frozenset({"id", "gate", "kind", "path", "sha256"})


@dataclass(frozen=True)
class EvidenceIssue:
    code: str
    path: str
    message: str


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _unsafe_relative_path(value: Any) -> bool:
    if not _is_text(value):
        return True
    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    return (
        posix.is_absolute()
        or windows.is_absolute()
        or bool(windows.drive)
        or "\\" in value
        or ".." in posix.parts
        or ".." in windows.parts
        or posix == PurePosixPath(".")
    )


def _workspace_root(workspace_root: Path | str) -> Path:
    if os.name != "posix" or not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise ValueError(
            "secure evidence filesystem operations require POSIX dirfd and O_NOFOLLOW support"
        )
    root = Path(workspace_root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("workspace_root must be an existing directory")
    return root


class _EvidenceFileError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _directory_flags() -> int:
    return os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)


def _open_parent_dir(
    root: Path, relative_path: str, *, create: bool
) -> tuple[int, str]:
    parts = PurePosixPath(relative_path).parts
    current_fd = os.open(root, _directory_flags())
    try:
        for part in parts[:-1]:
            try:
                next_fd = os.open(part, _directory_flags(), dir_fd=current_fd)
            except FileNotFoundError:
                if not create:
                    raise _EvidenceFileError(
                        "missing_file", f"evidence parent does not exist: {relative_path}"
                    )
                os.mkdir(part, mode=0o755, dir_fd=current_fd)
                next_fd = os.open(part, _directory_flags(), dir_fd=current_fd)
            except OSError as error:
                if error.errno in {errno.ELOOP, errno.ENOTDIR}:
                    raise _EvidenceFileError(
                        "symlink_path",
                        f"evidence path contains a symlink or non-directory parent: {relative_path}",
                    ) from error
                raise _EvidenceFileError("unreadable_file", str(error)) from error
            if not stat.S_ISDIR(os.fstat(next_fd).st_mode):
                os.close(next_fd)
                raise _EvidenceFileError(
                    "symlink_path",
                    f"evidence parent is not a real directory: {relative_path}",
                )
            os.close(current_fd)
            current_fd = next_fd
        return current_fd, parts[-1]
    except BaseException:
        os.close(current_fd)
        raise


def _open_regular_file(root: Path, relative_path: str) -> int:
    parent_fd, name = _open_parent_dir(root, relative_path, create=False)
    try:
        flags = (
            os.O_RDONLY
            | os.O_NOFOLLOW
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NONBLOCK", 0)
        )
        try:
            file_fd = os.open(name, flags, dir_fd=parent_fd)
        except FileNotFoundError as error:
            raise _EvidenceFileError(
                "missing_file", f"evidence file does not exist: {relative_path}"
            ) from error
        except OSError as error:
            if error.errno in {errno.ELOOP, errno.ENOTDIR}:
                raise _EvidenceFileError(
                    "symlink_path", f"evidence path must not be a symlink: {relative_path}"
                ) from error
            raise _EvidenceFileError("unreadable_file", str(error)) from error
        if not stat.S_ISREG(os.fstat(file_fd).st_mode):
            os.close(file_fd)
            raise _EvidenceFileError(
                "not_regular_file",
                f"evidence path is not a regular file: {relative_path}",
            )
        return file_fd
    finally:
        os.close(parent_fd)


def _fd_sha256(file_fd: int) -> str:
    digest = hashlib.sha256()
    os.lseek(file_fd, 0, os.SEEK_SET)
    while True:
        chunk = os.read(file_fd, 1024 * 1024)
        if not chunk:
            break
        digest.update(chunk)
    return digest.hexdigest()


def _base_reference(
    *,
    evidence_id: str,
    gate_id: str,
    kind: str,
    relative_path: str,
    sha256: str,
    maturity: str | None,
    metadata: Mapping[str, Any] | None,
) -> dict[str, Any]:
    if not _is_text(evidence_id):
        raise ValueError("evidence_id must contain text")
    if gate_id not in GATE_IDS:
        raise ValueError(f"invalid evidence gate: {gate_id!r}")
    if not _is_text(kind):
        raise ValueError("evidence kind must contain text")
    if _unsafe_relative_path(relative_path):
        raise ValueError("evidence path must be a safe relative path")
    if maturity is not None and not _is_text(maturity):
        raise ValueError("evidence maturity must contain text when provided")
    if metadata is not None and not isinstance(metadata, Mapping):
        raise ValueError("evidence metadata must be an object when provided")

    reference: dict[str, Any] = {
        "id": evidence_id,
        "gate": gate_id,
        "kind": kind,
        "path": PurePosixPath(relative_path).as_posix(),
        "sha256": sha256,
    }
    if maturity is not None:
        reference["maturity"] = maturity
    if metadata is not None:
        reference["metadata"] = dict(metadata)
    return reference


def register_evidence_file(
    workspace_root: Path | str,
    *,
    evidence_id: str,
    gate_id: str,
    kind: str,
    relative_path: str,
    maturity: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    reference = _base_reference(
        evidence_id=evidence_id,
        gate_id=gate_id,
        kind=kind,
        relative_path=relative_path,
        sha256="0" * 64,
        maturity=maturity,
        metadata=metadata,
    )
    root = _workspace_root(workspace_root)
    file_fd = _open_regular_file(root, reference["path"])
    try:
        reference["sha256"] = _fd_sha256(file_fd)
    finally:
        os.close(file_fd)
    return reference


def materialize_json_evidence(
    workspace_root: Path | str,
    *,
    evidence_id: str,
    gate_id: str,
    kind: str,
    relative_path: str,
    value: Any,
    maturity: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    reference = _base_reference(
        evidence_id=evidence_id,
        gate_id=gate_id,
        kind=kind,
        relative_path=relative_path,
        sha256="0" * 64,
        maturity=maturity,
        metadata=metadata,
    )
    root = _workspace_root(workspace_root)
    encoded = canonical_json_bytes(value)
    parent_fd, name = _open_parent_dir(root, reference["path"], create=True)
    temporary_name: str | None = None
    try:
        try:
            existing = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            existing = None
        if existing is not None and not stat.S_ISREG(existing.st_mode):
            kind = "symlink" if stat.S_ISLNK(existing.st_mode) else "non-regular file"
            raise ValueError(f"evidence target is a {kind}: {reference['path']}")

        for _ in range(100):
            temporary_name = f".{name}.{secrets.token_hex(8)}.tmp"
            try:
                temporary_fd = os.open(
                    temporary_name,
                    os.O_WRONLY
                    | os.O_CREAT
                    | os.O_EXCL
                    | os.O_NOFOLLOW
                    | getattr(os, "O_CLOEXEC", 0),
                    0o600,
                    dir_fd=parent_fd,
                )
                break
            except FileExistsError:
                continue
        else:
            raise ValueError("could not allocate a secure temporary evidence file")
        try:
            remaining = memoryview(encoded)
            while remaining:
                written = os.write(temporary_fd, remaining)
                remaining = remaining[written:]
            os.fsync(temporary_fd)
        finally:
            os.close(temporary_fd)
        os.replace(
            temporary_name,
            name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        temporary_name = None
        os.fsync(parent_fd)
    finally:
        if temporary_name is not None:
            try:
                os.unlink(temporary_name, dir_fd=parent_fd)
            except FileNotFoundError:
                pass
        os.close(parent_fd)

    reference["sha256"] = hashlib.sha256(encoded).hexdigest()
    return reference


def verify_evidence_reference(
    workspace_root: Path | str,
    reference: Mapping[str, Any],
    *,
    expected_gate: str | None = None,
) -> list[EvidenceIssue]:
    issues: list[EvidenceIssue] = []
    if not isinstance(reference, Mapping):
        return [EvidenceIssue("invalid_reference", "$", "evidence reference must be an object")]

    for field in sorted(REQUIRED_REFERENCE_FIELDS - set(reference)):
        issues.append(
            EvidenceIssue(
                "missing_field", f"$.{field}", f"missing evidence reference field: {field}"
            )
        )
    for field in sorted(set(reference) - REFERENCE_FIELDS):
        issues.append(
            EvidenceIssue(
                "unknown_field", f"$.{field}", f"unknown evidence reference field: {field}"
            )
        )

    if not _is_text(reference.get("id")):
        issues.append(EvidenceIssue("invalid_id", "$.id", "evidence id must contain text"))
    gate = reference.get("gate")
    if gate not in GATE_IDS:
        issues.append(
            EvidenceIssue("invalid_gate", "$.gate", "evidence gate must be G0 through G6")
        )
    elif expected_gate is not None and gate != expected_gate:
        issues.append(
            EvidenceIssue(
                "wrong_gate",
                "$.gate",
                f"evidence belongs to {gate}, not expected gate {expected_gate}",
            )
        )
    if not _is_text(reference.get("kind")):
        issues.append(
            EvidenceIssue("invalid_kind", "$.kind", "evidence kind must contain text")
        )
    if "maturity" in reference and not _is_text(reference.get("maturity")):
        issues.append(
            EvidenceIssue(
                "invalid_maturity", "$.maturity", "evidence maturity must contain text"
            )
        )
    if "metadata" in reference and not isinstance(reference.get("metadata"), Mapping):
        issues.append(
            EvidenceIssue("invalid_metadata", "$.metadata", "evidence metadata must be an object")
        )

    relative_path = reference.get("path")
    if _unsafe_relative_path(relative_path):
        issues.append(
            EvidenceIssue("unsafe_path", "$.path", "evidence path must be a safe relative path")
        )
        return issues
    expected_sha = reference.get("sha256")
    if not isinstance(expected_sha, str) or not SHA256_PATTERN.fullmatch(expected_sha):
        issues.append(
            EvidenceIssue(
                "invalid_sha256",
                "$.sha256",
                "evidence sha256 must be 64 lowercase hexadecimal characters",
            )
        )

    try:
        root = _workspace_root(workspace_root)
        file_fd = _open_regular_file(root, str(relative_path))
    except _EvidenceFileError as error:
        issues.append(EvidenceIssue(error.code, "$.path", str(error)))
        return issues
    except (OSError, ValueError) as error:
        issues.append(EvidenceIssue("invalid_workspace_root", "$.path", str(error)))
        return issues
    try:
        if isinstance(expected_sha, str) and SHA256_PATTERN.fullmatch(expected_sha):
            actual_sha = _fd_sha256(file_fd)
            if actual_sha != expected_sha:
                issues.append(
                    EvidenceIssue(
                        "hash_mismatch",
                        "$.sha256",
                        f"evidence hash mismatch: expected {expected_sha}, got {actual_sha}",
                    )
                )
    except OSError as error:
        issues.append(EvidenceIssue("unreadable_file", "$.path", str(error)))
    finally:
        os.close(file_fd)
    return issues
