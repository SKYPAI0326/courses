from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import secrets
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Mapping, MutableMapping, Sequence

from src.course_evidence import (
    canonical_json_bytes,
    consume_evidence_reference,
    verify_evidence_reference,
)
from src.verification_authority import (
    ALGORITHM as APPROVAL_ALGORITHM,
    VerificationKeyError,
    public_key_fingerprint,
    verify_rsa_sha256_signature,
)


GATE_ORDER: tuple[str, ...] = tuple(f"G{index}" for index in range(7))
GATE_STATUSES: frozenset[str] = frozenset(
    {"NOT_STARTED", "IN_PROGRESS", "PASS", "FAIL", "BLOCKED", "STALE"}
)
EXTERNAL_ACTION_STATUSES: frozenset[str] = frozenset(
    {
        "PUBLISH_APPROVAL_REQUIRED",
        "AUTHORIZED",
        "EXECUTING",
        "CONSUMED",
        "FAILED",
        "INVALIDATED",
    }
)
EXTERNAL_ACTION_FIELDS: frozenset[str] = frozenset(
    {
        "id",
        "kind",
        "status",
        "manifest_path",
        "manifest_sha256",
        "proposed_by",
        "proposed_at",
        "approval_basis_sha256",
        "authorized_revision",
        "authorization",
        "execution",
    }
)
EXTERNAL_ACTION_REQUIRED_FIELDS: frozenset[str] = frozenset(
    {
        "id", "kind", "status", "manifest_path", "manifest_sha256",
        "proposed_by", "proposed_at", "authorization",
    }
)
APPROVAL_RECEIPT_FIELDS: frozenset[str] = frozenset(
    {
        "schema_version",
        "receipt_id",
        "authority_id",
        "algorithm",
        "contract_instance_id",
        "contract_revision",
        "g6_source_revision",
        "g6_evidence_set_sha256",
        "action_id",
        "manifest_sha256",
        "approval_basis_sha256",
        "interaction",
        "nonce",
        "issued_at",
        "expires_at",
        "signature",
    }
)
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

REQUIRED_SECTIONS = (
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
)

REQUIRED_GATE_FIELDS = (
    "status",
    "owner",
    "inputs",
    "deliverables",
    "evidence",
    "risks",
    "open_questions",
    "source_revision",
    "affected_downstream",
)

_PAYLOAD_SECTIONS = (
    "G0_requirements",
    "G1_research",
    "adaptation",
    "G2_architecture",
    "G3_lesson_design",
    "G4_pilot",
    "G5_production",
    "G6_release_maintenance",
)

_GATE_LIST_FIELDS = (
    "inputs",
    "deliverables",
    "evidence",
    "risks",
    "open_questions",
    "affected_downstream",
)

_GATE_OWNERS = {
    "G0": "course-run",
    "G1": "course-researcher",
    "G2": "course-pm",
    "G3": "course-designer",
    "G4": "build-course-page",
    "G5": "course-run",
    "G6": "course-ops",
}

_SECTION_BY_GATE = {
    "G0": "G0_requirements",
    "G1": "G1_research",
    "G2": "G2_architecture",
    "G3": "G3_lesson_design",
    "G4": "G4_pilot",
    "G5": "G5_production",
    "G6": "G6_release_maintenance",
}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str


class ContractStateError(ValueError):
    pass


def new_contract(slug: str, title: str, created_by: str, created_at: str) -> dict[str, Any]:
    if not SLUG_PATTERN.fullmatch(slug):
        raise ValueError("slug must use lowercase letters, digits, and single hyphens")
    for name, value in (
        ("title", title),
        ("created_by", created_by),
        ("created_at", created_at),
    ):
        if not value.strip():
            raise ValueError(f"{name} must not be empty")

    gates: dict[str, dict[str, Any]] = {}
    for index, gate_id in enumerate(GATE_ORDER):
        gates[gate_id] = {
            "status": "NOT_STARTED",
            "owner": _GATE_OWNERS[gate_id],
            "inputs": list(GATE_ORDER[:index]),
            "deliverables": [],
            "evidence": [],
            "risks": [],
            "open_questions": [],
            "source_revision": 0,
            "affected_downstream": list(GATE_ORDER[index + 1 :]),
        }

    return {
        "schema_version": 3,
        "revision": 0,
        "contract_instance_id": f"ci-{secrets.token_hex(16)}",
        "identity": {"slug": slug, "title": title},
        "governance": {
            "created_by": created_by,
            "created_at": created_at,
            "gate_authority": "course-run-with-validated-evidence",
            "external_action_authority": "explicit-user-authorization",
            "production_role_roster": None,
            "runner_authority": None,
            "approval_authority": None,
        },
        "gates": gates,
        "G0_requirements": {},
        "G1_research": {},
        "adaptation": {},
        "G2_architecture": {},
        "G3_lesson_design": {},
        "G4_pilot": {},
        "G5_production": {},
        "G6_release_maintenance": {},
        "changes": [],
        "evidence_index": [],
        "evidence_archive": [],
        "external_actions": [],
        "maintenance": {},
        "consumed_trial_receipts": [],
    }


def _append_issue(
    issues: list[ValidationIssue], code: str, path: str, message: str
) -> None:
    issues.append(ValidationIssue(code, path, message))


def _validate_governance(contract: Mapping[str, Any], issues: list[ValidationIssue]) -> None:
    governance = contract.get("governance")
    path = "$.governance"
    if not isinstance(governance, Mapping):
        _append_issue(issues, "invalid_governance", path, "governance must be an object")
        return
    expected = {
        "created_by",
        "created_at",
        "gate_authority",
        "external_action_authority",
        "production_role_roster",
        "runner_authority",
        "approval_authority",
    }
    for field in expected - {"production_role_roster", "runner_authority", "approval_authority"}:
        value = governance.get(field)
        if not isinstance(value, str) or not value.strip():
            _append_issue(
                issues,
                "invalid_governance_field",
                f"{path}.{field}",
                f"{field} must contain text",
            )
    if "production_role_roster" not in governance:
        _append_issue(
            issues,
            "invalid_governance_field",
            f"{path}.production_role_roster",
            "production_role_roster must be present and may be null until fixed",
        )
    if "runner_authority" not in governance:
        _append_issue(
            issues,
            "invalid_governance_field",
            f"{path}.runner_authority",
            "runner_authority must be present and may be null until fixed",
        )
    if governance.get("gate_authority") != "course-run-with-validated-evidence":
        _append_issue(
            issues,
            "invalid_gate_authority",
            f"{path}.gate_authority",
            "gate_authority must require validated evidence through course-run",
        )
    if governance.get("external_action_authority") != "explicit-user-authorization":
        _append_issue(
            issues,
            "invalid_external_action_authority",
            f"{path}.external_action_authority",
            "external actions must require explicit user authorization",
        )
    roster = governance.get("production_role_roster")
    if roster is not None:
        if not isinstance(roster, Mapping) or set(roster) != {"evidence_id", "sha256"}:
            _append_issue(
                issues,
                "invalid_production_role_roster_binding",
                f"{path}.production_role_roster",
                "production role roster binding must contain only evidence_id and sha256",
            )
        else:
            evidence_id = roster.get("evidence_id")
            digest = roster.get("sha256")
            if not isinstance(evidence_id, str) or not evidence_id.strip():
                _append_issue(issues, "invalid_production_role_roster_binding", f"{path}.production_role_roster.evidence_id", "governed roster evidence id must contain text")
            if not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest):
                _append_issue(issues, "invalid_production_role_roster_binding", f"{path}.production_role_roster.sha256", "governed roster sha256 must be lowercase hexadecimal")
    authority = governance.get("runner_authority")
    authority_fields = {
        "authority_id", "algorithm", "public_key", "public_key_fingerprint",
        "runner_registry_sha256",
    }
    if authority is not None:
        if not isinstance(authority, Mapping) or set(authority) != authority_fields:
            _append_issue(issues, "invalid_runner_authority", f"{path}.runner_authority", "runner authority binding has missing or unknown fields")
        else:
            if not isinstance(authority.get("authority_id"), str) or not authority["authority_id"].strip():
                _append_issue(issues, "invalid_runner_authority", f"{path}.runner_authority.authority_id", "runner authority id must contain text")
            if authority.get("algorithm") != "RSASSA-PKCS1-v1_5-SHA256":
                _append_issue(issues, "invalid_runner_authority", f"{path}.runner_authority.algorithm", "runner authority algorithm must be RSASSA-PKCS1-v1_5-SHA256")
            public_key = authority.get("public_key")
            if (
                not isinstance(public_key, Mapping)
                or set(public_key) != {"kty", "n", "e"}
                or public_key.get("kty") != "RSA"
                or not isinstance(public_key.get("n"), str)
                or re.fullmatch(r"[0-9a-f]+", public_key["n"]) is None
                or public_key.get("e") != 65537
            ):
                _append_issue(issues, "invalid_runner_authority", f"{path}.runner_authority.public_key", "runner authority public key must be canonical RSA verification material")
            for field in ("public_key_fingerprint", "runner_registry_sha256"):
                digest = authority.get(field)
                if not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest):
                    _append_issue(issues, "invalid_runner_authority", f"{path}.runner_authority.{field}", f"{field} must be lowercase SHA-256")
    approval_authority = governance.get("approval_authority")
    approval_fields = {
        "authority_id", "algorithm", "public_key", "public_key_fingerprint"
    }
    if approval_authority is not None:
        if not isinstance(approval_authority, Mapping) or set(approval_authority) != approval_fields:
            _append_issue(
                issues,
                "invalid_approval_authority",
                f"{path}.approval_authority",
                "approval authority binding has missing or unknown fields",
            )
        else:
            if not isinstance(approval_authority.get("authority_id"), str) or not approval_authority["authority_id"].strip():
                _append_issue(issues, "invalid_approval_authority", f"{path}.approval_authority.authority_id", "approval authority id must contain text")
            if approval_authority.get("algorithm") != APPROVAL_ALGORITHM:
                _append_issue(issues, "invalid_approval_authority", f"{path}.approval_authority.algorithm", "approval authority algorithm is unsupported")
            try:
                fingerprint = public_key_fingerprint(approval_authority.get("public_key"))
            except (VerificationKeyError, TypeError):
                _append_issue(issues, "invalid_approval_authority", f"{path}.approval_authority.public_key", "approval authority public key is invalid")
            else:
                if fingerprint != approval_authority.get("public_key_fingerprint"):
                    _append_issue(issues, "invalid_approval_authority", f"{path}.approval_authority.public_key_fingerprint", "approval authority public key fingerprint is invalid")
    for field in set(governance) - expected:
        _append_issue(
            issues,
            "unknown_governance_field",
            f"{path}.{field}",
            f"unknown governance field: {field}",
        )


def bind_production_role_roster(
    contract: MutableMapping[str, Any], evidence_id: str
) -> None:
    """Fix the authoritative author/validator roster before any Gate work begins."""
    gates = contract.get("gates")
    if not isinstance(gates, Mapping) or any(
        not isinstance(record, Mapping) or record.get("status") != "NOT_STARTED"
        for record in gates.values()
    ):
        raise ContractStateError("production role roster must be fixed before Gate work begins")
    references = _indexed_evidence_by_id(contract)
    reference = references.get(evidence_id)
    if reference is None:
        raise ContractStateError("production role roster must reference indexed evidence")
    if reference.get("kind") != "production_role_roster" or reference.get("gate") != "G0":
        raise ContractStateError("governed roster evidence must be G0 production_role_roster")
    digest = reference.get("sha256")
    if not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest):
        raise ContractStateError("governed roster evidence requires a valid sha256")
    governance = contract.get("governance")
    if not isinstance(governance, MutableMapping):
        raise ContractStateError("contract governance is missing")
    if governance.get("production_role_roster") is not None:
        raise ContractStateError("production role roster is already fixed")
    governance["production_role_roster"] = {"evidence_id": evidence_id, "sha256": digest}


def bind_external_approval_authority(
    contract: MutableMapping[str, Any],
    authority_id: str,
    public_key: Mapping[str, Any],
) -> None:
    """Bind verification-only user-interaction authority material.

    Receipt issuance and private signing keys stay outside production code.
    """

    if not isinstance(authority_id, str) or not authority_id.strip():
        raise ContractStateError("approval authority id is required")
    gates = contract.get("gates")
    if not isinstance(gates, Mapping) or any(
        not isinstance(record, Mapping) or record.get("status") != "NOT_STARTED"
        for record in gates.values()
    ):
        raise ContractStateError(
            "approval authority must be fixed before Gate work begins"
        )
    governance = contract.get("governance")
    if not isinstance(governance, MutableMapping):
        raise ContractStateError("contract governance is missing")
    if governance.get("approval_authority") is not None:
        raise ContractStateError("approval authority is already fixed")
    try:
        fingerprint = public_key_fingerprint(public_key)
    except VerificationKeyError as error:
        raise ContractStateError(f"approval authority {error}") from error
    governance["approval_authority"] = {
        "authority_id": authority_id,
        "algorithm": APPROVAL_ALGORITHM,
        "public_key": dict(public_key),
        "public_key_fingerprint": fingerprint,
    }


def _unresolved_blockers(record: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    risks = record.get("risks", [])
    if not isinstance(risks, list):
        return []
    return [
        risk
        for risk in risks
        if isinstance(risk, Mapping)
        and risk.get("blocking") is True
        and risk.get("resolved") is not True
    ]


def validate_contract(contract: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for section in sorted(set(contract) - set(REQUIRED_SECTIONS)):
        _append_issue(
            issues,
            "unknown_section",
            f"$.{section}",
            f"unknown top-level section: {section}",
        )
    for section in REQUIRED_SECTIONS:
        if section not in contract:
            _append_issue(
                issues,
                "missing_section",
                f"$.{section}",
                f"missing required section: {section}",
            )

    if contract.get("schema_version") != 3:
        _append_issue(
            issues,
            "unsupported_schema_version",
            "$.schema_version",
            "schema_version must be 3",
        )

    contract_revision = contract.get("revision")
    if (
        isinstance(contract_revision, bool)
        or not isinstance(contract_revision, int)
        or contract_revision < 0
    ):
        _append_issue(
            issues,
            "invalid_revision",
            "$.revision",
            "revision must be a non-negative integer",
        )

    instance_id = contract.get("contract_instance_id")
    if instance_id is not None and (
        not isinstance(instance_id, str)
        or re.fullmatch(r"ci-[0-9a-f]{32}", instance_id) is None
    ):
        _append_issue(
            issues,
            "invalid_contract_instance_id",
            "$.contract_instance_id",
            "contract_instance_id must be null for a legacy migration or a generated immutable id",
        )

    identity = contract.get("identity")
    if not isinstance(identity, Mapping):
        _append_issue(issues, "invalid_identity", "$.identity", "identity must be an object")
    else:
        slug = identity.get("slug")
        if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug):
            _append_issue(issues, "invalid_slug", "$.identity.slug", "slug has an invalid format")
        title = identity.get("title")
        if not isinstance(title, str) or not title.strip():
            _append_issue(issues, "invalid_title", "$.identity.title", "title must not be empty")
        for field in set(identity) - {"slug", "title"}:
            _append_issue(
                issues,
                "unknown_identity_field",
                f"$.identity.{field}",
                f"unknown identity field: {field}",
            )

    _validate_governance(contract, issues)

    for section in _PAYLOAD_SECTIONS + ("maintenance",):
        if section in contract and not isinstance(contract.get(section), Mapping):
            _append_issue(
                issues,
                "invalid_section_type",
                f"$.{section}",
                f"{section} must be an object",
            )

    for section in ("changes", "evidence_index", "evidence_archive", "external_actions", "consumed_trial_receipts"):
        value = contract.get(section)
        if not isinstance(value, list):
            _append_issue(
                issues,
                "invalid_section_type",
                f"$.{section}",
                f"{section} must be a list",
            )
        else:
            for index, item in enumerate(value):
                if not isinstance(item, Mapping):
                    _append_issue(
                        issues,
                        "invalid_record",
                        f"$.{section}[{index}]",
                        f"{section} items must be objects",
                    )

    receipt_ledger = contract.get("consumed_trial_receipts")
    seen_receipt_ids: set[str] = set()
    seen_nonces: set[str] = set()
    if isinstance(receipt_ledger, list):
        required_receipt_fields = {"receipt_id", "nonce", "gate", "consumed_at"}
        for index, item in enumerate(receipt_ledger):
            path = f"$.consumed_trial_receipts[{index}]"
            if not isinstance(item, Mapping):
                continue
            if set(item) != required_receipt_fields or any(
                not isinstance(item.get(field), str) or not item[field].strip()
                for field in required_receipt_fields
            ) or item.get("gate") not in {"G4", "G5"}:
                _append_issue(
                    issues, "invalid_receipt_ledger", path,
                    "consumed receipt must contain receipt_id, nonce, G4/G5 gate, and consumed_at",
                )
                continue
            if item["receipt_id"] in seen_receipt_ids or item["nonce"] in seen_nonces:
                _append_issue(
                    issues, "duplicate_consumed_receipt", path,
                    "consumed receipt ids and nonces must be unique",
                )
            seen_receipt_ids.add(item["receipt_id"])
            seen_nonces.add(item["nonce"])

    evidence_ids: set[str] = set()
    evidence_by_id: dict[str, Mapping[str, Any]] = {}
    evidence_index = contract.get("evidence_index")
    if isinstance(evidence_index, list):
        for index, item in enumerate(evidence_index):
            if not isinstance(item, Mapping):
                continue
            evidence_id = item.get("id")
            if not isinstance(evidence_id, str) or not evidence_id.strip():
                _append_issue(
                    issues,
                    "invalid_evidence_id",
                    f"$.evidence_index[{index}].id",
                    "evidence id must contain text",
                )
            elif evidence_id in evidence_ids:
                _append_issue(
                    issues,
                    "duplicate_evidence_id",
                    f"$.evidence_index[{index}].id",
                    f"duplicate evidence id: {evidence_id}",
                )
            else:
                evidence_ids.add(evidence_id)
                evidence_by_id[evidence_id] = item

            reference_path = f"$.evidence_index[{index}]"
            expected_fields = {
                "id",
                "gate",
                "kind",
                "path",
                "sha256",
                "maturity",
                "metadata",
            }
            required_fields = {"id", "gate", "kind", "path", "sha256"}
            for field in sorted(required_fields - set(item)):
                _append_issue(
                    issues,
                    "missing_evidence_field",
                    f"{reference_path}.{field}",
                    f"evidence reference is missing required field: {field}",
                )
            for field in sorted(set(item) - expected_fields):
                _append_issue(
                    issues,
                    "unknown_evidence_field",
                    f"{reference_path}.{field}",
                    f"unknown evidence reference field: {field}",
                )
            if item.get("gate") not in GATE_ORDER:
                _append_issue(
                    issues,
                    "invalid_evidence_gate",
                    f"{reference_path}.gate",
                    "evidence gate must be G0 through G6",
                )
            kind = item.get("kind")
            if not isinstance(kind, str) or not kind.strip():
                _append_issue(
                    issues,
                    "invalid_evidence_kind",
                    f"{reference_path}.kind",
                    "evidence kind must contain text",
                )
            path_value = item.get("path")
            if not isinstance(path_value, str) or not path_value.strip():
                invalid_path = True
            else:
                posix_path = PurePosixPath(path_value)
                windows_path = PureWindowsPath(path_value)
                invalid_path = (
                    posix_path.is_absolute()
                    or windows_path.is_absolute()
                    or bool(windows_path.drive)
                    or "\\" in path_value
                    or ".." in posix_path.parts
                    or ".." in windows_path.parts
                    or posix_path == PurePosixPath(".")
                )
            if invalid_path:
                _append_issue(
                    issues,
                    "invalid_evidence_path",
                    f"{reference_path}.path",
                    "evidence path must be a safe relative path",
                )
            sha256 = item.get("sha256")
            if not isinstance(sha256, str) or not SHA256_PATTERN.fullmatch(sha256):
                _append_issue(
                    issues,
                    "invalid_evidence_sha256",
                    f"{reference_path}.sha256",
                    "evidence sha256 must be 64 lowercase hexadecimal characters",
                )
            if "maturity" in item and (
                not isinstance(item.get("maturity"), str)
                or not item["maturity"].strip()
            ):
                _append_issue(
                    issues,
                    "invalid_evidence_maturity",
                    f"{reference_path}.maturity",
                    "evidence maturity must contain text",
                )
            if "metadata" in item and not isinstance(item.get("metadata"), Mapping):
                _append_issue(
                    issues,
                    "invalid_evidence_metadata",
                    f"{reference_path}.metadata",
                    "evidence metadata must be an object",
                )

    governance = contract.get("governance")
    binding = governance.get("production_role_roster") if isinstance(governance, Mapping) else None
    if isinstance(binding, Mapping):
        bound = evidence_by_id.get(binding.get("evidence_id"))
        if (
            bound is None
            or bound.get("kind") != "production_role_roster"
            or bound.get("gate") != "G0"
            or bound.get("sha256") != binding.get("sha256")
        ):
            _append_issue(
                issues,
                "invalid_production_role_roster_binding",
                "$.governance.production_role_roster",
                "governed roster binding must match an indexed G0 production_role_roster reference",
            )

    gates = contract.get("gates")
    if not isinstance(gates, Mapping):
        _append_issue(issues, "invalid_gates", "$.gates", "gates must be an object")
        return issues

    blocker_ids: set[str] = set()
    for gate_id in GATE_ORDER:
        record = gates.get(gate_id)
        gate_path = f"$.gates.{gate_id}"
        if not isinstance(record, Mapping):
            _append_issue(issues, "missing_gate", gate_path, f"missing gate record: {gate_id}")
            continue
        for field in REQUIRED_GATE_FIELDS:
            if field not in record:
                _append_issue(
                    issues,
                    "missing_gate_field",
                    f"{gate_path}.{field}",
                    f"{gate_id} is missing required field: {field}",
                )
        for field in set(record) - set(REQUIRED_GATE_FIELDS):
            _append_issue(
                issues,
                "unknown_gate_field",
                f"{gate_path}.{field}",
                f"unknown gate field: {field}",
            )

        status = record.get("status")
        if status not in GATE_STATUSES:
            _append_issue(
                issues,
                "unknown_gate_status",
                f"{gate_path}.status",
                f"unknown gate status: {status!r}",
            )
        owner = record.get("owner")
        if not isinstance(owner, str) or not owner.strip():
            _append_issue(
                issues,
                "invalid_gate_owner",
                f"{gate_path}.owner",
                "gate owner must contain text",
            )

        for field in _GATE_LIST_FIELDS:
            value = record.get(field)
            if not isinstance(value, list):
                _append_issue(
                    issues,
                    "invalid_gate_field_type",
                    f"{gate_path}.{field}",
                    f"{field} must be a list",
                )
                continue
            if field in {"deliverables", "evidence", "risks", "open_questions"}:
                for index, item in enumerate(value):
                    if not isinstance(item, Mapping):
                        _append_issue(
                            issues,
                            "invalid_gate_record",
                            f"{gate_path}.{field}[{index}]",
                            f"{field} items must be objects",
                        )
                    elif field == "risks" and item.get("kind") == "gate_blocker":
                        blocker_id = item.get("id")
                        blocker_path = f"{gate_path}.risks[{index}].id"
                        if (
                            not isinstance(blocker_id, str)
                            or re.fullmatch(r"blocker-g[0-6]-[0-9a-f]{24}", blocker_id)
                            is None
                        ):
                            _append_issue(
                                issues,
                                "invalid_blocker_id",
                                blocker_path,
                                "gate blocker id must be stable and well formed",
                            )
                        elif blocker_id in blocker_ids:
                            _append_issue(
                                issues,
                                "duplicate_blocker_id",
                                blocker_path,
                                f"duplicate blocker id: {blocker_id}",
                            )
                        else:
                            blocker_ids.add(blocker_id)
            elif field == "inputs":
                for index, item in enumerate(value):
                    if not isinstance(item, str):
                        _append_issue(
                            issues,
                            "invalid_gate_reference",
                            f"{gate_path}.inputs[{index}]",
                            "input references must be strings",
                        )
            else:
                for index, item in enumerate(value):
                    if item not in GATE_ORDER:
                        _append_issue(
                            issues,
                            "invalid_gate_reference",
                            f"{gate_path}.affected_downstream[{index}]",
                            f"unknown downstream gate: {item!r}",
                        )

        risk_records = record.get("risks")
        evidence_records = record.get("evidence")
        if isinstance(risk_records, list) and isinstance(evidence_records, list):
            gate_blockers = {
                item.get("id"): item
                for item in risk_records
                if isinstance(item, Mapping)
                and item.get("kind") == "gate_blocker"
                and isinstance(item.get("id"), str)
            }
            indexed_resolution_events = [
                (index, item)
                for index, item in enumerate(evidence_records)
                if isinstance(item, Mapping)
                and item.get("kind") == "gate_blocker_resolution"
            ]
            resolution_events = [item for _, item in indexed_resolution_events]
            resolution_ids: set[str] = set()
            for event_index, event in indexed_resolution_events:
                event_path = f"{gate_path}.evidence[{event_index}]"
                resolution_id = event.get("id")
                if (
                    not isinstance(resolution_id, str)
                    or re.fullmatch(r"resolution-[0-9a-f]{24}", resolution_id)
                    is None
                ):
                    _append_issue(
                        issues,
                        "invalid_blocker_resolution_audit",
                        f"{event_path}.id",
                        "blocker resolution audit id must be stable and well formed",
                    )
                elif resolution_id in resolution_ids:
                    _append_issue(
                        issues,
                        "duplicate_blocker_resolution_audit",
                        f"{event_path}.id",
                        f"duplicate blocker resolution audit id: {resolution_id}",
                    )
                else:
                    resolution_ids.add(resolution_id)
                blocker_id = event.get("blocker_id")
                if blocker_id not in gate_blockers:
                    _append_issue(
                        issues,
                        "orphan_blocker_resolution_audit",
                        f"{event_path}.blocker_id",
                        "blocker resolution audit must reference one blocker in the same Gate",
                    )
                event_evidence_ids = event.get("evidence_ids")
                consumed = event.get("consumed_evidence")
                if (
                    not isinstance(event_evidence_ids, list)
                    or not event_evidence_ids
                    or len(set(event_evidence_ids)) != len(event_evidence_ids)
                    or not isinstance(consumed, list)
                    or len(consumed) != len(event_evidence_ids)
                ):
                    _append_issue(
                        issues,
                        "invalid_blocker_resolution_evidence",
                        f"{event_path}.evidence_ids",
                        "resolution audit requires unique evidence ids and matching consumed hashes",
                    )
                    continue
                consumed_by_id = {
                    item.get("id"): item.get("sha256")
                    for item in consumed
                    if isinstance(item, Mapping)
                }
                for evidence_id in event_evidence_ids:
                    indexed = evidence_by_id.get(evidence_id)
                    if (
                        indexed is None
                        or indexed.get("gate") != gate_id
                        or indexed.get("kind") != "blocker_resolution"
                        or consumed_by_id.get(evidence_id) != indexed.get("sha256")
                    ):
                        _append_issue(
                            issues,
                            "invalid_blocker_resolution_evidence",
                            f"{event_path}.consumed_evidence",
                            f"resolution evidence is missing or no longer matches: {evidence_id}",
                        )

            for blocker_id, blocker in gate_blockers.items():
                if blocker.get("resolved") is not True:
                    continue
                resolution_id = blocker.get("resolution_id")
                matches = [
                    event
                    for event in resolution_events
                    if event.get("id") == resolution_id
                    and event.get("blocker_id") == blocker_id
                ]
                if len(matches) != 1:
                    _append_issue(
                        issues,
                        "missing_blocker_resolution_audit",
                        f"{gate_path}.risks",
                        f"resolved blocker lacks exactly one matching audit event: {blocker_id}",
                    )

        revision = record.get("source_revision")
        if revision is not None and (
            isinstance(revision, bool) or not isinstance(revision, (str, int))
        ):
            _append_issue(
                issues,
                "invalid_source_revision",
                f"{gate_path}.source_revision",
                "source_revision must be text, integer, or null",
            )

        if status == "PASS":
            gate_index = GATE_ORDER.index(gate_id)
            missing = [
                prior
                for prior in GATE_ORDER[:gate_index]
                if not isinstance(gates.get(prior), Mapping)
                or gates[prior].get("status") != "PASS"
            ]
            if missing:
                _append_issue(
                    issues,
                    "unpassed_prerequisite",
                    f"{gate_path}.status",
                    f"passed gate has unpassed prerequisites: {', '.join(missing)}",
                )
            if _unresolved_blockers(record):
                _append_issue(
                    issues,
                    "passed_with_blocker",
                    f"{gate_path}.risks",
                    "passed gate cannot have unresolved blocking risks",
                )
            pass_events = [
                event
                for event in record.get("evidence", [])
                if isinstance(event, Mapping)
                and event.get("kind") == "gate_validation"
                and event.get("outcome") == "PASS"
            ]
            if not pass_events:
                _append_issue(
                    issues,
                    "pass_evidence_required",
                    f"{gate_path}.evidence",
                    "passed gate requires a PASS validation event",
                )
            for event_index, event in enumerate(pass_events):
                for evidence_id in event.get("evidence_ids", []):
                    if evidence_id not in evidence_ids:
                        _append_issue(
                            issues,
                            "unknown_pass_evidence",
                            f"{gate_path}.evidence[{event_index}].evidence_ids",
                            f"unknown evidence id: {evidence_id}",
                        )
                    elif evidence_by_id[evidence_id].get("gate") != gate_id:
                        _append_issue(
                            issues,
                            "wrong_gate_evidence",
                            f"{gate_path}.evidence[{event_index}].evidence_ids",
                            f"evidence {evidence_id} does not belong to {gate_id}",
                        )

    for gate_id in gates:
        if gate_id not in GATE_ORDER:
            _append_issue(
                issues,
                "unknown_gate",
                f"$.gates.{gate_id}",
                f"unknown gate id: {gate_id}",
            )

    external_actions = contract.get("external_actions")
    if isinstance(external_actions, list):
        action_ids: set[str] = set()
        for index, action in enumerate(external_actions):
            if not isinstance(action, Mapping):
                continue
            action_path = f"$.external_actions[{index}]"
            for field in EXTERNAL_ACTION_REQUIRED_FIELDS - set(action):
                _append_issue(
                    issues,
                    "missing_external_action_field",
                    f"{action_path}.{field}",
                    f"external action is missing required field: {field}",
                )
            for field in set(action) - EXTERNAL_ACTION_FIELDS:
                _append_issue(
                    issues,
                    "unknown_external_action_field",
                    f"{action_path}.{field}",
                    f"unknown external action field: {field}",
                )
            action_id = action.get("id")
            if not isinstance(action_id, str) or not action_id.strip():
                _append_issue(issues, "invalid_action_id", f"{action_path}.id", "action id must contain text")
            elif action_id in action_ids:
                _append_issue(issues, "duplicate_action_id", f"{action_path}.id", f"duplicate action id: {action_id}")
            else:
                action_ids.add(action_id)
            if action.get("status") not in EXTERNAL_ACTION_STATUSES:
                _append_issue(
                    issues,
                    "invalid_external_action_status",
                    f"{action_path}.status",
                    "external action status is invalid",
                )
            manifest_sha256 = action.get("manifest_sha256")
            if not isinstance(manifest_sha256, str) or not SHA256_PATTERN.fullmatch(manifest_sha256):
                _append_issue(
                    issues,
                    "invalid_manifest_sha256",
                    f"{action_path}.manifest_sha256",
                    "manifest_sha256 must be 64 lowercase hexadecimal characters",
                )
            for field in ("kind", "manifest_path", "proposed_by", "proposed_at"):
                value = action.get(field)
                if not isinstance(value, str) or not value.strip():
                    _append_issue(
                        issues,
                        "invalid_external_action_field",
                        f"{action_path}.{field}",
                        f"{field} must contain text",
                    )
            authorization = action.get("authorization")
            basis_hash = action.get("approval_basis_sha256")
            authorized_revision = action.get("authorized_revision")
            execution = action.get("execution")
            if action.get("status") == "PUBLISH_APPROVAL_REQUIRED":
                if any(
                    value is not None
                    for value in (
                        authorization,
                        basis_hash,
                        authorized_revision,
                        execution,
                    )
                ):
                    _append_issue(
                        issues,
                        "invalid_external_authorization",
                        f"{action_path}.authorization",
                        "an action awaiting approval cannot contain authorization state",
                    )
            else:
                if (
                    not isinstance(authorization, Mapping)
                    or set(authorization) != APPROVAL_RECEIPT_FIELDS
                    or not isinstance(basis_hash, str)
                    or not SHA256_PATTERN.fullmatch(basis_hash)
                    or authorization.get("approval_basis_sha256") != basis_hash
                    or isinstance(authorized_revision, bool)
                    or not isinstance(authorized_revision, int)
                    or authorized_revision < 1
                ):
                    _append_issue(
                        issues,
                        "invalid_external_authorization",
                        f"{action_path}.authorization",
                        "authorized action requires one complete signed approval receipt",
                    )
                if action.get("status") in {"EXECUTING", "CONSUMED", "FAILED"}:
                    if not isinstance(execution, Mapping):
                        _append_issue(
                            issues,
                            "invalid_external_execution",
                            f"{action_path}.execution",
                            "execution lifecycle state requires execution metadata",
                        )
                elif execution is not None:
                    _append_issue(
                        issues,
                        "invalid_external_execution",
                        f"{action_path}.execution",
                        "non-executing action cannot contain execution metadata",
                    )

    return issues


def _require_valid_contract(contract: MutableMapping[str, Any]) -> None:
    issues = validate_contract(contract)
    if issues:
        joined = "; ".join(f"{issue.path}: {issue.message}" for issue in issues)
        raise ContractStateError(f"contract is invalid: {joined}")


def _gate_record(
    contract: MutableMapping[str, Any], gate_id: str
) -> MutableMapping[str, Any]:
    if gate_id not in GATE_ORDER:
        raise ContractStateError(f"unknown gate: {gate_id}")
    gates = contract.get("gates")
    if not isinstance(gates, MutableMapping):
        raise ContractStateError("contract gates are missing or invalid")
    record = gates.get(gate_id)
    if not isinstance(record, MutableMapping):
        raise ContractStateError(f"gate record is missing or invalid: {gate_id}")
    return record


def _require_previous_passes(
    contract: MutableMapping[str, Any], gate_id: str
) -> None:
    gate_index = GATE_ORDER.index(gate_id)
    gates = contract["gates"]
    missing = [
        prior
        for prior in GATE_ORDER[:gate_index]
        if gates[prior].get("status") != "PASS"
    ]
    if missing:
        raise ContractStateError(
            f"{gate_id} requires passed previous gates: {', '.join(missing)}"
        )


def begin_gate(
    contract: MutableMapping[str, Any], gate_id: str, actor: str, at: str
) -> None:
    if not actor.strip() or not at.strip():
        raise ContractStateError("begin requires actor and timestamp")
    _require_valid_contract(contract)
    _require_previous_passes(contract, gate_id)
    record = _gate_record(contract, gate_id)
    if record.get("status") not in {
        "NOT_STARTED",
        "FAIL",
        "BLOCKED",
        "STALE",
    }:
        raise ContractStateError(f"cannot begin a gate in {record.get('status')!r} state")
    if _unresolved_blockers(record):
        raise ContractStateError(f"cannot begin {gate_id} with an unresolved blocker")
    record["status"] = "IN_PROGRESS"
    record["evidence"].append({"kind": "gate_begin", "actor": actor, "at": at})


def _indexed_evidence_ids(contract: Mapping[str, Any]) -> set[str]:
    evidence_index = contract.get("evidence_index", [])
    if not isinstance(evidence_index, list):
        return set()
    return {
        item["id"]
        for item in evidence_index
        if isinstance(item, Mapping)
        and isinstance(item.get("id"), str)
        and item["id"].strip()
    }


def _indexed_evidence_by_id(
    contract: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    evidence_index = contract.get("evidence_index", [])
    if not isinstance(evidence_index, list):
        return {}
    return {
        item["id"]: item
        for item in evidence_index
        if isinstance(item, Mapping)
        and isinstance(item.get("id"), str)
        and item["id"].strip()
    }


def pass_gate(
    contract: MutableMapping[str, Any],
    gate_id: str,
    evidence_ids: Sequence[str],
    validator_id: str,
    actor: str,
    at: str,
) -> None:
    raise ContractStateError(
        "raw Gate PASS is unavailable; use validate_and_transition_gate with replayable evidence"
    )


def fail_gate(
    contract: MutableMapping[str, Any],
    gate_id: str,
    issues: Sequence[Mapping[str, Any]],
    actor: str,
    at: str,
) -> None:
    if not actor.strip() or not at.strip() or not issues:
        raise ContractStateError("failure requires issues, actor, and timestamp")
    if any(not isinstance(issue, Mapping) for issue in issues):
        raise ContractStateError("failure issues must be objects")
    _require_valid_contract(contract)
    record = _gate_record(contract, gate_id)
    if record.get("status") != "IN_PROGRESS":
        raise ContractStateError(f"cannot fail a gate in {record.get('status')!r} state")
    record["status"] = "FAIL"
    record["evidence"].append(
        {
            "kind": "gate_validation",
            "outcome": "FAIL",
            "actor": actor,
            "at": at,
            "issues": [dict(issue) for issue in issues],
        }
    )


def _append_gate_blocker(
    contract: MutableMapping[str, Any],
    gate_id: str,
    reason: str,
    actor: str,
    at: str,
) -> str:
    record = _gate_record(contract, gate_id)
    blocker_payload = {
        "contract_instance_id": contract.get("contract_instance_id"),
        "gate": gate_id,
        "reason": reason,
        "actor": actor,
        "at": at,
    }
    blocker_id = (
        f"blocker-{gate_id.lower()}-"
        f"{hashlib.sha256(canonical_json_bytes(blocker_payload)).hexdigest()[:24]}"
    )
    existing_ids = {
        risk.get("id")
        for gate in contract.get("gates", {}).values()
        if isinstance(gate, Mapping)
        for risk in gate.get("risks", [])
        if isinstance(risk, Mapping)
    }
    if blocker_id in existing_ids:
        raise ContractStateError(f"blocker id already exists: {blocker_id}")
    record["risks"].append(
        {
            "id": blocker_id,
            "kind": "gate_blocker",
            "blocking": True,
            "resolved": False,
            "reason": reason,
            "actor": actor,
            "at": at,
        }
    )
    return blocker_id


def record_gate_blocker(
    contract: MutableMapping[str, Any],
    gate_id: str,
    reason: str,
    actor: str,
    at: str,
) -> str:
    """Record an unresolved blocker while keeping a routed Gate in progress."""

    if not reason.strip() or not actor.strip() or not at.strip():
        raise ContractStateError("blocking requires reason, actor, and timestamp")
    _require_valid_contract(contract)
    record = _gate_record(contract, gate_id)
    if record.get("status") != "IN_PROGRESS":
        raise ContractStateError(
            f"cannot record an in-progress blocker in {record.get('status')!r} state"
        )
    return _append_gate_blocker(contract, gate_id, reason, actor, at)


def block_gate(
    contract: MutableMapping[str, Any],
    gate_id: str,
    reason: str,
    actor: str,
    at: str,
) -> None:
    if not reason.strip() or not actor.strip() or not at.strip():
        raise ContractStateError("blocking requires reason, actor, and timestamp")
    _require_valid_contract(contract)
    record = _gate_record(contract, gate_id)
    if record.get("status") not in {
        "NOT_STARTED",
        "IN_PROGRESS",
        "FAIL",
        "STALE",
    }:
        raise ContractStateError(f"cannot block a gate in {record.get('status')!r} state")
    _append_gate_blocker(contract, gate_id, reason, actor, at)
    record["status"] = "BLOCKED"


def resolve_gate_blocker(
    contract: MutableMapping[str, Any],
    gate_id: str,
    blocker_id: str,
    resolution: str,
    evidence_ids: Sequence[str],
    actor: str,
    at: str,
    *,
    workspace_root: Path | str | None = None,
) -> None:
    """Resolve one blocker with same-Gate evidence consumed from real files.

    ``workspace_root`` is required so this operation can fail closed on a missing,
    escaped, or hash-mismatched evidence file.  The positional interface remains
    the contract API; callers must provide the verification root explicitly.
    """

    if not all(
        isinstance(value, str) and value.strip()
        for value in (blocker_id, resolution, actor, at)
    ):
        raise ContractStateError(
            "blocker resolution requires blocker id, resolution, actor, and timestamp"
        )
    if workspace_root is None:
        raise ContractStateError(
            "blocker resolution requires workspace_root for replayable evidence"
        )
    if not evidence_ids or any(
        not isinstance(evidence_id, str) or not evidence_id.strip()
        for evidence_id in evidence_ids
    ):
        raise ContractStateError("blocker resolution requires evidence ids")
    if len(set(evidence_ids)) != len(evidence_ids):
        raise ContractStateError("blocker resolution evidence ids must be unique")

    _require_valid_contract(contract)
    record = _gate_record(contract, gate_id)
    if record.get("status") not in {"BLOCKED", "IN_PROGRESS"}:
        raise ContractStateError(
            f"cannot resolve a blocker in {record.get('status')!r} state"
        )
    blockers = [
        risk
        for risk in record.get("risks", [])
        if isinstance(risk, MutableMapping)
        and risk.get("kind") == "gate_blocker"
        and risk.get("id") == blocker_id
    ]
    if len(blockers) != 1:
        raise ContractStateError(f"blocker not found for {gate_id}: {blocker_id}")
    blocker = blockers[0]
    if blocker.get("resolved") is True:
        raise ContractStateError(f"blocker is already resolved: {blocker_id}")

    references = _indexed_evidence_by_id(contract)
    missing = [
        evidence_id for evidence_id in evidence_ids if evidence_id not in references
    ]
    if missing:
        raise ContractStateError(
            "blocker resolution references unindexed evidence: " + ", ".join(missing)
        )
    consumed: list[dict[str, str]] = []
    for evidence_id in evidence_ids:
        reference = references[evidence_id]
        if reference.get("gate") != gate_id:
            raise ContractStateError(
                f"blocker resolution evidence {evidence_id} must belong to {gate_id}"
            )
        if reference.get("kind") != "blocker_resolution":
            raise ContractStateError(
                f"blocker resolution evidence {evidence_id} must be typed blocker_resolution"
            )
        try:
            item = consume_evidence_reference(
                workspace_root, reference, expected_gate=gate_id, parse_json=False
            )
        except (OSError, ValueError) as error:
            raise ContractStateError(
                f"invalid blocker resolution evidence: {error}"
            ) from error
        consumed.append({"id": evidence_id, "sha256": item.sha256})

    resolution_payload = {
        "blocker_id": blocker_id,
        "resolution": resolution,
        "evidence_ids": list(evidence_ids),
        "actor": actor,
        "at": at,
    }
    resolution_id = (
        "resolution-"
        + hashlib.sha256(canonical_json_bytes(resolution_payload)).hexdigest()[:24]
    )
    if any(
        isinstance(event, Mapping) and event.get("id") == resolution_id
        for event in record.get("evidence", [])
    ):
        raise ContractStateError(f"blocker resolution id already exists: {resolution_id}")

    blocker["resolved"] = True
    blocker["resolution_id"] = resolution_id
    record["evidence"].append(
        {
            "id": resolution_id,
            "kind": "gate_blocker_resolution",
            "blocker_id": blocker_id,
            "resolution": resolution,
            "evidence_ids": list(evidence_ids),
            "consumed_evidence": consumed,
            "actor": actor,
            "at": at,
        }
    )


def record_change(
    contract: MutableMapping[str, Any],
    affected_gate: str,
    reason: str,
    actor: str,
    at: str,
    semantic: bool,
) -> list[str]:
    if not reason.strip() or not actor.strip() or not at.strip():
        raise ContractStateError("change record requires reason, actor, and timestamp")
    _require_valid_contract(contract)
    record = _gate_record(contract, affected_gate)
    affected_index = GATE_ORDER.index(affected_gate)
    invalidated = list(GATE_ORDER[affected_index:]) if semantic else []
    changes = contract.get("changes")
    if not isinstance(changes, list):
        raise ContractStateError("contract changes must be a list")
    changes.append(
        {
            "kind": "course_change",
            "affected_gate": affected_gate,
            "reason": reason,
            "actor": actor,
            "at": at,
            "semantic": semantic,
            "invalidated_gates": invalidated,
        }
    )
    if semantic:
        record["status"] = "IN_PROGRESS"
        for gate_id in GATE_ORDER[affected_index + 1 :]:
            contract["gates"][gate_id]["status"] = "STALE"
    return invalidated


def _find_external_action(
    contract: MutableMapping[str, Any], action_id: str
) -> MutableMapping[str, Any]:
    actions = contract.get("external_actions")
    if not isinstance(actions, list):
        raise ContractStateError("external actions are missing or invalid")
    matches = [
        action
        for action in actions
        if isinstance(action, MutableMapping) and action.get("id") == action_id
    ]
    if len(matches) != 1:
        raise ContractStateError(f"external action not found: {action_id}")
    return matches[0]


def propose_external_action(
    contract: MutableMapping[str, Any],
    action_id: str,
    kind: str,
    manifest_path: str,
    manifest_sha256: str,
    actor: str,
    at: str,
) -> None:
    values = (action_id, kind, manifest_path, actor, at)
    if any(not value.strip() for value in values):
        raise ContractStateError("external action proposal fields must contain text")
    if not SHA256_PATTERN.fullmatch(manifest_sha256):
        raise ContractStateError("manifest_sha256 must be a lowercase SHA-256")
    manifest = PurePosixPath(manifest_path)
    if (
        manifest.is_absolute()
        or manifest == PurePosixPath(".")
        or ".." in manifest.parts
        or "\\" in manifest_path
    ):
        raise ContractStateError("manifest_path must be a safe POSIX relative path")
    _require_valid_contract(contract)
    if contract["gates"]["G6"].get("status") != "PASS":
        raise ContractStateError("external action proposal requires G6 PASS")
    if any(
        isinstance(action, Mapping) and action.get("id") == action_id
        for action in contract["external_actions"]
    ):
        raise ContractStateError(f"external action id already exists: {action_id}")
    contract["external_actions"].append(
        {
            "id": action_id,
            "kind": kind,
            "status": "PUBLISH_APPROVAL_REQUIRED",
            "manifest_path": manifest_path,
            "manifest_sha256": manifest_sha256,
            "proposed_by": actor,
            "proposed_at": at,
            "approval_basis_sha256": None,
            "authorized_revision": None,
            "authorization": None,
            "execution": None,
        }
    )


def _all_gates_pass(contract: Mapping[str, Any]) -> bool:
    gates = contract.get("gates")
    return isinstance(gates, Mapping) and all(
        isinstance(gates.get(gate_id), Mapping)
        and gates[gate_id].get("status") == "PASS"
        for gate_id in GATE_ORDER
    )


def _g6_evidence_set_sha256(contract: Mapping[str, Any]) -> str:
    gate = contract.get("gates", {}).get("G6")
    if not isinstance(gate, Mapping):
        raise ContractStateError("G6 record is missing")
    events = gate.get("evidence")
    if not isinstance(events, list):
        raise ContractStateError("G6 evidence history is invalid")
    pass_events = [
        event
        for event in events
        if isinstance(event, Mapping)
        and event.get("kind") == "gate_validation"
        and event.get("outcome") == "PASS"
    ]
    if not pass_events or not isinstance(pass_events[-1].get("evidence_ids"), list):
        raise ContractStateError("G6 PASS evidence set is missing")
    indexed = {
        item.get("id"): item
        for item in contract.get("evidence_index", [])
        if isinstance(item, Mapping)
    }
    references: list[dict[str, Any]] = []
    for evidence_id in pass_events[-1]["evidence_ids"]:
        reference = indexed.get(evidence_id)
        if not isinstance(reference, Mapping) or reference.get("gate") != "G6":
            raise ContractStateError("G6 PASS evidence set is not replayable")
        references.append(
            {
                key: reference[key]
                for key in (
                    "id",
                    "gate",
                    "kind",
                    "path",
                    "sha256",
                    "maturity",
                    "metadata",
                )
                if key in reference
            }
        )
    references.sort(key=lambda item: str(item["id"]))
    return hashlib.sha256(canonical_json_bytes(references)).hexdigest()


def _approval_basis(
    contract: Mapping[str, Any],
    action: Mapping[str, Any],
    *,
    contract_revision: int,
) -> dict[str, Any]:
    gate = contract.get("gates", {}).get("G6")
    if not isinstance(gate, Mapping):
        raise ContractStateError("G6 record is missing")
    basis = {
        "contract_instance_id": contract.get("contract_instance_id"),
        "contract_revision": contract_revision,
        "g6_source_revision": gate.get("source_revision"),
        "g6_evidence_set_sha256": _g6_evidence_set_sha256(contract),
        "action_id": action.get("id"),
        "manifest_sha256": action.get("manifest_sha256"),
    }
    if (
        not isinstance(basis["contract_instance_id"], str)
        or isinstance(basis["contract_revision"], bool)
        or not isinstance(basis["contract_revision"], int)
        or isinstance(basis["g6_source_revision"], bool)
        or not isinstance(basis["g6_source_revision"], (int, str))
        or not isinstance(basis["action_id"], str)
        or not isinstance(basis["manifest_sha256"], str)
    ):
        raise ContractStateError("approval basis is incomplete")
    basis["approval_basis_sha256"] = hashlib.sha256(
        canonical_json_bytes(basis)
    ).hexdigest()
    return basis


def external_action_approval_basis(
    contract: MutableMapping[str, Any], action_id: str
) -> dict[str, Any]:
    _require_valid_contract(contract)
    if not _all_gates_pass(contract):
        raise ContractStateError("external authorization requires all Gates PASS")
    action = _find_external_action(contract, action_id)
    if action.get("status") != "PUBLISH_APPROVAL_REQUIRED":
        raise ContractStateError("approval basis requires a pending external action")
    revision = contract.get("revision")
    if isinstance(revision, bool) or not isinstance(revision, int):
        raise ContractStateError("approval basis requires an exact contract revision")
    return _approval_basis(contract, action, contract_revision=revision)


def _parse_timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ContractStateError(f"approval receipt {field} is required")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ContractStateError(
            f"approval receipt {field} must be ISO-8601"
        ) from error
    if parsed.tzinfo is None:
        raise ContractStateError(f"approval receipt {field} requires a timezone")
    return parsed


def _verify_approval_receipt_signature(
    contract: Mapping[str, Any], receipt: Mapping[str, Any]
) -> None:
    governance = contract.get("governance")
    authority = (
        governance.get("approval_authority")
        if isinstance(governance, Mapping)
        else None
    )
    if not isinstance(authority, Mapping):
        raise ContractStateError("governed approval authority is not configured")
    if (
        receipt.get("schema_version") != 1
        or receipt.get("authority_id") != authority.get("authority_id")
        or receipt.get("algorithm") != APPROVAL_ALGORITHM
        or authority.get("algorithm") != APPROVAL_ALGORITHM
    ):
        raise ContractStateError("approval receipt authority is invalid")
    unsigned = {
        key: receipt[key] for key in sorted(set(receipt) - {"signature"})
    }
    if not verify_rsa_sha256_signature(
        unsigned, receipt.get("signature"), authority.get("public_key")
    ):
        raise ContractStateError("approval receipt signature is invalid")


def authorize_external_action(
    contract: MutableMapping[str, Any],
    action_id: str,
    receipt: Mapping[str, Any] | Any,
    authorized_at: str,
    *legacy_caller_fields: Any,
) -> None:
    if legacy_caller_fields or not isinstance(receipt, Mapping):
        raise ContractStateError("external authorization requires a signed receipt")
    _require_valid_contract(contract)
    if not _all_gates_pass(contract):
        raise ContractStateError("external authorization requires all Gates PASS")
    action = _find_external_action(contract, action_id)
    if action.get("status") != "PUBLISH_APPROVAL_REQUIRED":
        raise ContractStateError(
            f"cannot authorize external action in {action.get('status')!r} state"
        )
    if set(receipt) != APPROVAL_RECEIPT_FIELDS:
        raise ContractStateError("approval receipt has missing or unknown fields")
    _verify_approval_receipt_signature(contract, receipt)
    basis = external_action_approval_basis(contract, action_id)
    if any(receipt.get(field) != value for field, value in basis.items()):
        raise ContractStateError("approval receipt does not match the exact approval basis")
    interaction = receipt.get("interaction")
    if (
        not isinstance(interaction, Mapping)
        or set(interaction) != {"kind", "user_id", "session_id", "confirmed_at"}
        or interaction.get("kind") != "explicit_user_approval"
        or any(
            not isinstance(interaction.get(field), str)
            or not interaction[field].strip()
            for field in ("user_id", "session_id", "confirmed_at")
        )
    ):
        raise ContractStateError(
            "approval receipt lacks an explicit verified user interaction boundary"
        )
    authorized_time = _parse_timestamp(authorized_at, "authorized_at")
    confirmed_time = _parse_timestamp(interaction["confirmed_at"], "confirmed_at")
    issued_time = _parse_timestamp(receipt.get("issued_at"), "issued_at")
    expires_time = _parse_timestamp(receipt.get("expires_at"), "expires_at")
    if not (confirmed_time <= issued_time <= authorized_time <= expires_time):
        raise ContractStateError("approval receipt is expired or has invalid time ordering")
    receipt_id = receipt.get("receipt_id")
    nonce = receipt.get("nonce")
    if not isinstance(receipt_id, str) or not receipt_id.strip() or not isinstance(nonce, str) or not nonce.strip():
        raise ContractStateError("approval receipt id and nonce are required")
    for existing in contract.get("external_actions", []):
        prior = existing.get("authorization") if isinstance(existing, Mapping) else None
        if isinstance(prior, Mapping) and (
            prior.get("receipt_id") == receipt_id or prior.get("nonce") == nonce
        ):
            raise ContractStateError("approval receipt id or nonce was already used")
    action["status"] = "AUTHORIZED"
    action["approval_basis_sha256"] = basis["approval_basis_sha256"]
    action["authorized_revision"] = basis["contract_revision"] + 1
    action["authorization"] = copy.deepcopy(dict(receipt))


def assert_external_action_authorized(
    contract: MutableMapping[str, Any],
    action_id: str,
    manifest_sha256: str,
    at: str | None = None,
) -> None:
    _require_valid_contract(contract)
    action = _find_external_action(contract, action_id)
    if action.get("status") != "AUTHORIZED":
        raise ContractStateError(f"external action is not authorized: {action_id}")
    if action.get("manifest_sha256") != manifest_sha256:
        raise ContractStateError("authorized manifest hash does not match")
    if not _all_gates_pass(contract):
        raise ContractStateError("authorized action requires all Gates PASS")
    receipt = action.get("authorization")
    if not isinstance(receipt, Mapping):
        raise ContractStateError("authorized action receipt is missing")
    _verify_approval_receipt_signature(contract, receipt)
    expires = _parse_timestamp(receipt.get("expires_at"), "expires_at")
    execution_time = (
        _parse_timestamp(at, "execution_at")
        if at is not None
        else datetime.now(expires.tzinfo)
    )
    if execution_time > expires:
        raise ContractStateError("approval receipt has expired")
    revision = contract.get("revision")
    if revision != action.get("authorized_revision"):
        raise ContractStateError("authorized contract revision is no longer current")
    receipt_revision = receipt.get("contract_revision")
    if isinstance(receipt_revision, bool) or not isinstance(receipt_revision, int):
        raise ContractStateError("authorized receipt revision is invalid")
    basis = _approval_basis(
        contract, action, contract_revision=receipt_revision
    )
    if (
        basis.get("approval_basis_sha256")
        != action.get("approval_basis_sha256")
        or any(receipt.get(field) != value for field, value in basis.items())
    ):
        raise ContractStateError("authorized approval basis is no longer current")


def begin_external_action_execution(
    contract: MutableMapping[str, Any],
    action_id: str,
    manifest_sha256: str,
    proposal_revision: int,
    at: str,
) -> None:
    assert_external_action_authorized(contract, action_id, manifest_sha256, at)
    action = _find_external_action(contract, action_id)
    action["status"] = "EXECUTING"
    action["execution"] = {
        "proposal_revision": proposal_revision,
        "started_at": at,
        "finished_at": None,
        "outcome": "IN_PROGRESS",
        "modified_targets": [],
        "error": None,
    }


def finish_external_action_execution(
    contract: MutableMapping[str, Any],
    action_id: str,
    status: str,
    modified_targets: Sequence[str],
    at: str,
    error: str | None = None,
) -> None:
    action = _find_external_action(contract, action_id)
    if action.get("status") != "EXECUTING" or status not in {"CONSUMED", "FAILED"}:
        raise ContractStateError("external action execution transition is invalid")
    execution = action.get("execution")
    if not isinstance(execution, MutableMapping):
        raise ContractStateError("external action execution metadata is missing")
    action["status"] = status
    execution["finished_at"] = at
    execution["outcome"] = "PASS" if status == "CONSUMED" else "FAIL_ROLLED_BACK"
    execution["modified_targets"] = list(modified_targets)
    execution["error"] = error


def _legacy_gate_has_complete_evidence(record: Mapping[str, Any]) -> bool:
    evidence = record.get("evidence")
    return (
        isinstance(evidence, list)
        and bool(evidence)
        and not _unresolved_blockers(record)
    )


def _legacy_evidence_reference(
    gate_id: str, legacy_evidence: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    encoded = canonical_json_bytes(list(legacy_evidence))
    return {
        "id": f"legacy-{gate_id.lower()}-evidence",
        "gate": gate_id,
        "kind": "legacy_evidence_bundle",
        "path": f"migration/{gate_id.lower()}-legacy-evidence.json",
        "sha256": hashlib.sha256(encoded).hexdigest(),
    }


def migrate_contract_v1(
    contract: Mapping[str, Any],
    actor: str,
    at: str,
    *,
    workspace_root: Path | str | None = None,
) -> dict[str, Any]:
    if contract.get("schema_version") != 1:
        raise ContractStateError("migration requires schema_version 1")
    if not actor.strip() or not at.strip():
        raise ContractStateError("migration requires actor and timestamp")
    migrated = copy.deepcopy(dict(contract))
    governance = migrated.get("governance")
    if not isinstance(governance, MutableMapping):
        raise ContractStateError("legacy governance is missing or invalid")
    governance["gate_authority"] = "course-run-with-validated-evidence"
    governance["external_action_authority"] = "explicit-user-authorization"
    governance["production_role_roster"] = None
    governance["runner_authority"] = None
    governance["approval_authority"] = None
    migrated["schema_version"] = 2
    migrated["external_actions"] = []
    migrated["maintenance"] = {}
    if not isinstance(migrated.get("evidence_index"), list):
        migrated["evidence_index"] = []
    if not isinstance(migrated.get("changes"), list):
        migrated["changes"] = []

    gates = migrated.get("gates")
    if not isinstance(gates, MutableMapping):
        raise ContractStateError("legacy gates are missing or invalid")
    for index, gate_id in enumerate(GATE_ORDER):
        record = gates.get(gate_id)
        if not isinstance(record, MutableMapping):
            raise ContractStateError(f"legacy gate is missing or invalid: {gate_id}")
        legacy_status = record.get("status")
        legacy_evidence = [
            item for item in record.get("evidence", []) if isinstance(item, Mapping)
        ]
        approved_by = record.pop("approved_by", None)
        approved_at = record.pop("approved_at", None)
        if approved_by or approved_at:
            record["evidence"].append(
                {
                    "kind": "legacy_user_approval",
                    "approved_by": approved_by,
                    "approved_at": approved_at,
                }
            )

        previous_passed = all(
            gates[prior].get("status") == "PASS" for prior in GATE_ORDER[:index]
        )
        if (
            legacy_status == "APPROVED"
            and bool(legacy_evidence)
            and not _unresolved_blockers(record)
            and previous_passed
        ):
            reference = _legacy_evidence_reference(gate_id, legacy_evidence)
            migrated["evidence_index"].append(reference)
            record["evidence"].append(
                {
                    "kind": "gate_validation",
                    "outcome": "PASS",
                    "validator_id": "migration-v1-evidence-check",
                    "actor": actor,
                    "at": at,
                    "evidence_ids": [reference["id"]],
                }
            )
            record["status"] = "PASS"
        elif legacy_status == "BLOCKED":
            record["status"] = "BLOCKED"
        elif legacy_status == "STALE":
            record["status"] = "STALE"
        elif legacy_status == "DRAFT":
            payload = migrated.get(_SECTION_BY_GATE[gate_id])
            has_work = bool(payload) or bool(record.get("deliverables")) or bool(
                record.get("evidence")
            )
            record["status"] = "IN_PROGRESS" if has_work else "NOT_STARTED"
        else:
            record["status"] = "IN_PROGRESS"

    migrated["changes"].append(
        {
            "kind": "schema_migration",
            "from_schema_version": 1,
            "to_schema_version": 2,
            "actor": actor,
            "at": at,
        }
    )
    return migrate_contract_v2(migrated, workspace_root, actor, at)


def migrate_contract_v2(
    contract: Mapping[str, Any],
    workspace_root: Path | str | None,
    actor: str,
    at: str,
) -> dict[str, Any]:
    if contract.get("schema_version") != 2:
        raise ContractStateError("migration requires schema_version 2")
    if not actor.strip() or not at.strip():
        raise ContractStateError("migration requires actor and timestamp")

    migrated = copy.deepcopy(dict(contract))
    migrated["schema_version"] = 3
    migrated["revision"] = 0
    migrated["contract_instance_id"] = None
    migrated["consumed_trial_receipts"] = []
    governance = migrated.get("governance")
    if not isinstance(governance, MutableMapping):
        raise ContractStateError("legacy governance is missing or invalid")
    governance.setdefault("production_role_roster", None)
    governance.setdefault("runner_authority", None)
    governance.setdefault("approval_authority", None)
    original_evidence = migrated.get("evidence_index")
    if not isinstance(original_evidence, list):
        original_evidence = []
    archive = migrated.get("evidence_archive")
    if not isinstance(archive, list):
        archive = []
    migrated["evidence_archive"] = archive

    allowed_fields = {
        "id",
        "gate",
        "kind",
        "path",
        "sha256",
        "maturity",
        "metadata",
    }
    normalized: list[tuple[Mapping[str, Any], dict[str, Any] | None, str | None]] = []
    id_counts: dict[str, int] = {}
    for item in original_evidence:
        reference: dict[str, Any] | None = None
        reason: str | None = None
        if not isinstance(item, Mapping):
            reason = "legacy evidence record is not an object"
        else:
            evidence_id = item.get("id")
            gate = item.get("gate")
            kind = item.get("kind", "legacy_evidence")
            path = item.get("path")
            sha256 = item.get("sha256")
            maturity = item.get("maturity")
            metadata = item.get("metadata")
            if not isinstance(evidence_id, str) or not evidence_id.strip():
                reason = "legacy record is not a typed file reference"
            elif gate not in GATE_ORDER:
                reason = "legacy record has no valid Gate"
            elif not isinstance(kind, str) or not kind.strip():
                reason = "legacy record has no valid kind"
            elif not isinstance(path, str) or not path.strip():
                reason = "legacy record has no file path"
            else:
                posix_path = PurePosixPath(path)
                windows_path = PureWindowsPath(path)
                if (
                    posix_path.is_absolute()
                    or windows_path.is_absolute()
                    or bool(windows_path.drive)
                    or "\\" in path
                    or ".." in posix_path.parts
                    or ".." in windows_path.parts
                    or posix_path == PurePosixPath(".")
                ):
                    reason = "legacy record has an unsafe file path"
                elif not isinstance(sha256, str) or not SHA256_PATTERN.fullmatch(sha256):
                    reason = "legacy record has no valid SHA-256"
                elif maturity is not None and (
                    not isinstance(maturity, str) or not maturity.strip()
                ):
                    reason = "legacy record has invalid maturity"
                elif metadata is not None and not isinstance(metadata, Mapping):
                    reason = "legacy record has invalid metadata"
                else:
                    reference = {
                        "id": evidence_id,
                        "gate": gate,
                        "kind": kind,
                        "path": posix_path.as_posix(),
                        "sha256": sha256,
                    }
                    merged_metadata = dict(metadata) if isinstance(metadata, Mapping) else {}
                    legacy_fields = {
                        key: copy.deepcopy(value)
                        for key, value in item.items()
                        if key not in allowed_fields
                    }
                    if legacy_fields:
                        if "legacy_fields" in merged_metadata:
                            merged_metadata["legacy_fields"] = {
                                "metadata_value": copy.deepcopy(
                                    merged_metadata["legacy_fields"]
                                ),
                                "top_level_fields": legacy_fields,
                            }
                        else:
                            merged_metadata["legacy_fields"] = legacy_fields
                    if maturity is not None:
                        reference["maturity"] = maturity
                    if merged_metadata:
                        reference["metadata"] = merged_metadata
                    id_counts[evidence_id] = id_counts.get(evidence_id, 0) + 1
        normalized.append((item if isinstance(item, Mapping) else {"value": item}, reference, reason))

    evidence_index: list[dict[str, Any]] = []
    for original, reference, reason in normalized:
        if reference is not None and id_counts.get(reference["id"]) == 1:
            evidence_index.append(reference)
            continue
        if reference is not None:
            reason = "legacy evidence id is duplicated"
        archive.append(
            {
                "kind": "legacy_evidence_record",
                "archived_at": at,
                "reason": reason or "legacy record is not a typed file reference",
                "record": copy.deepcopy(dict(original)),
            }
        )
    migrated["evidence_index"] = evidence_index

    evidence_by_id: dict[str, list[Mapping[str, Any]]] = {}
    for reference in evidence_index:
        if isinstance(reference, Mapping) and isinstance(reference.get("id"), str):
            evidence_by_id.setdefault(reference["id"], []).append(reference)

    gates = migrated.get("gates")
    if not isinstance(gates, MutableMapping):
        raise ContractStateError("legacy gates are missing or invalid")
    earliest_stale: str | None = None
    for gate_id in GATE_ORDER:
        record = gates.get(gate_id)
        if not isinstance(record, MutableMapping) or record.get("status") != "PASS":
            continue
        pass_events = [
            event
            for event in record.get("evidence", [])
            if isinstance(event, Mapping)
            and event.get("kind") == "gate_validation"
            and event.get("outcome") == "PASS"
        ]
        evidence_ids = pass_events[-1].get("evidence_ids", []) if pass_events else []
        replayable = bool(evidence_ids) and workspace_root is not None
        if replayable:
            for evidence_id in evidence_ids:
                matches = evidence_by_id.get(evidence_id, [])
                if len(matches) != 1 or verify_evidence_reference(
                    workspace_root, matches[0], expected_gate=gate_id
                ):
                    replayable = False
                    break
        if not replayable:
            earliest_stale = gate_id
            break

    if earliest_stale is not None:
        stale_index = GATE_ORDER.index(earliest_stale)
        for gate_id in GATE_ORDER[stale_index:]:
            record = gates.get(gate_id)
            if isinstance(record, MutableMapping):
                record["status"] = "STALE"

    changes = migrated.get("changes")
    if not isinstance(changes, list):
        changes = []
        migrated["changes"] = changes
    migration_record: dict[str, Any] = {
        "kind": "schema_migration",
        "from_schema_version": 2,
        "to_schema_version": 3,
        "actor": actor,
        "at": at,
    }
    if earliest_stale is not None:
        migration_record["earliest_stale_gate"] = earliest_stale
    changes.append(migration_record)

    issues = validate_contract(migrated)
    if issues:
        joined = "; ".join(f"{issue.path}: {issue.message}" for issue in issues)
        raise ContractStateError(f"migration produced an invalid contract: {joined}")
    return migrated


def _reference_label(item: Any) -> str:
    if not isinstance(item, Mapping):
        return str(item)
    parts = [
        str(item[key])
        for key in ("id", "kind", "path", "sha256")
        if item.get(key) not in (None, "")
    ]
    return " | ".join(parts) if parts else "(record in contract)"


def _risk_label(item: Any) -> str:
    if not isinstance(item, Mapping):
        return str(item)
    identifier = item.get("id") or item.get("kind") or "risk"
    detail = item.get("description") or item.get("reason") or "(see contract)"
    return f"{identifier}: {detail}"


def _question_label(item: Any) -> str:
    if not isinstance(item, Mapping):
        return str(item)
    identifier = item.get("id") or "question"
    detail = item.get("text") or item.get("question") or "(see contract)"
    return f"{identifier}: {detail}"


def _append_list(lines: list[str], heading: str, items: list[Any], formatter) -> None:
    lines.append(f"{heading}:")
    if not items:
        lines.append("- none")
        return
    lines.extend(f"- {formatter(item)}" for item in items)


def render_gate_summary(contract: Mapping[str, Any]) -> str:
    gates = contract.get("gates", {})
    current_gate = next(
        (gate_id for gate_id in GATE_ORDER if gates[gate_id]["status"] != "PASS"),
        "G6",
    )
    gate = gates[current_gate]
    section_refs = {
        "G0": ["$.G0_requirements"],
        "G1": ["$.G1_research", "$.adaptation"],
        "G2": ["$.G2_architecture"],
        "G3": ["$.G3_lesson_design"],
        "G4": ["$.G4_pilot"],
        "G5": ["$.G5_production"],
        "G6": ["$.G6_release_maintenance"],
    }
    blockers = _unresolved_blockers(gate)
    nonblocking_risks = [
        item for item in gate.get("risks", []) if item not in blockers
    ]
    lines = [
        f"Course: {contract['identity']['title']} ({contract['identity']['slug']})",
        f"Current gate: {current_gate}",
        f"State: {gate['status']}",
        f"Source sections: {', '.join(section_refs[current_gate])}",
    ]
    _append_list(lines, "Deliverables", gate.get("deliverables", []), _reference_label)
    _append_list(lines, "Evidence", gate.get("evidence", []), _reference_label)
    _append_list(lines, "Blockers", blockers, _risk_label)
    _append_list(lines, "Risks", nonblocking_risks, _risk_label)
    _append_list(lines, "Open questions", gate.get("open_questions", []), _question_label)

    state = gate["status"]
    if blockers:
        next_action = "resolve blocking risks before validation"
    elif state == "NOT_STARTED":
        next_action = f"begin {current_gate}"
    elif state == "IN_PROGRESS":
        next_action = f"complete {current_gate} deliverables and run validation"
    elif state == "FAIL":
        next_action = f"repair {current_gate} issues and run validation again"
    elif state == "BLOCKED":
        next_action = f"resolve blockers before resuming {current_gate}"
    elif state == "STALE":
        next_action = f"refresh {current_gate} from passed upstream inputs"
    elif current_gate == "G6":
        next_action = "course is ready; external actions require explicit authorization"
    else:
        next_action = f"begin {GATE_ORDER[GATE_ORDER.index(current_gate) + 1]}"
    lines.append(f"Next action: {next_action}")
    return "\n".join(lines)


def load_contract(path: Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        contract = json.load(handle)
    if not isinstance(contract, dict):
        raise ValueError("course contract root must be an object")
    return contract


def save_contract_atomic(path: Path, contract: Mapping[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            json.dump(contract, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
