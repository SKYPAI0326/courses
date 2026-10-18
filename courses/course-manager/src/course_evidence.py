from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
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
        or ".." in posix.parts
        or ".." in windows.parts
        or posix == PurePosixPath(".")
    )


def _workspace_root(workspace_root: Path | str) -> Path:
    root = Path(workspace_root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("workspace_root must be an existing directory")
    return root


def _resolved_candidate(root: Path, relative_path: str) -> Path:
    candidate = root / PurePosixPath(relative_path)
    resolved = candidate.resolve(strict=False)
    if not resolved.is_relative_to(root):
        raise ValueError("evidence path escapes workspace_root")
    return resolved


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
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
    path = _resolved_candidate(root, reference["path"])
    if not path.exists():
        raise ValueError(f"evidence file does not exist: {relative_path}")
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError(f"evidence path is not a regular file: {relative_path}")
    reference["sha256"] = _file_sha256(path)
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
    target = root / PurePosixPath(reference["path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    resolved_parent = target.parent.resolve(strict=True)
    if not resolved_parent.is_relative_to(root):
        raise ValueError("evidence path escapes workspace_root")
    if target.exists() and not target.resolve(strict=True).is_relative_to(root):
        raise ValueError("evidence path escapes workspace_root")

    encoded = (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=resolved_parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, target)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    return register_evidence_file(
        root,
        evidence_id=evidence_id,
        gate_id=gate_id,
        kind=kind,
        relative_path=reference["path"],
        maturity=maturity,
        metadata=metadata,
    )


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
        path = _resolved_candidate(root, str(relative_path))
    except (OSError, ValueError) as error:
        code = "path_escape" if "escapes" in str(error) else "invalid_workspace_root"
        issues.append(EvidenceIssue(code, "$.path", str(error)))
        return issues

    if not path.exists():
        issues.append(
            EvidenceIssue("missing_file", "$.path", f"evidence file does not exist: {relative_path}")
        )
        return issues
    try:
        mode = path.stat().st_mode
    except OSError as error:
        issues.append(EvidenceIssue("unreadable_file", "$.path", str(error)))
        return issues
    if not stat.S_ISREG(mode):
        issues.append(
            EvidenceIssue(
                "not_regular_file", "$.path", f"evidence path is not a regular file: {relative_path}"
            )
        )
        return issues
    if isinstance(expected_sha, str) and SHA256_PATTERN.fullmatch(expected_sha):
        try:
            actual_sha = _file_sha256(path)
        except OSError as error:
            issues.append(EvidenceIssue("unreadable_file", "$.path", str(error)))
        else:
            if actual_sha != expected_sha:
                issues.append(
                    EvidenceIssue(
                        "hash_mismatch",
                        "$.sha256",
                        f"evidence hash mismatch: expected {expected_sha}, got {actual_sha}",
                    )
                )
    return issues
