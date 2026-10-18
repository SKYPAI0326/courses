from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Mapping, MutableMapping, Sequence

from src.course_evidence import canonical_json_bytes, verify_evidence_reference


GATE_ORDER: tuple[str, ...] = tuple(f"G{index}" for index in range(7))
GATE_STATUSES: frozenset[str] = frozenset(
    {"NOT_STARTED", "IN_PROGRESS", "PASS", "FAIL", "BLOCKED", "STALE"}
)
EXTERNAL_ACTION_STATUSES: frozenset[str] = frozenset(
    {"PUBLISH_APPROVAL_REQUIRED", "AUTHORIZED"}
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
        "authorization",
    }
)
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

REQUIRED_SECTIONS = (
    "schema_version",
    "revision",
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
        "identity": {"slug": slug, "title": title},
        "governance": {
            "created_by": created_by,
            "created_at": created_at,
            "gate_authority": "course-run-with-validated-evidence",
            "external_action_authority": "explicit-user-authorization",
            "production_role_roster": None,
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
    }
    for field in expected - {"production_role_roster"}:
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

    for section in ("changes", "evidence_index", "evidence_archive", "external_actions"):
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
            for field in EXTERNAL_ACTION_FIELDS - set(action):
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
            if action.get("status") == "PUBLISH_APPROVAL_REQUIRED":
                if authorization is not None:
                    _append_issue(
                        issues,
                        "invalid_external_authorization",
                        f"{action_path}.authorization",
                        "an action awaiting approval cannot contain authorization",
                    )
            elif action.get("status") == "AUTHORIZED":
                required = {"approved_by", "approved_at", "note"}
                if not isinstance(authorization, Mapping) or any(
                    not isinstance(authorization.get(field), str)
                    or not authorization[field].strip()
                    for field in required
                ):
                    _append_issue(
                        issues,
                        "invalid_external_authorization",
                        f"{action_path}.authorization",
                        "authorized action requires approver, timestamp, and note",
                    )
                elif set(authorization) != required:
                    _append_issue(
                        issues,
                        "invalid_external_authorization",
                        f"{action_path}.authorization",
                        "authorization contains unknown fields",
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
    record["status"] = "BLOCKED"
    record["risks"].append(
        {
            "kind": "gate_blocker",
            "blocking": True,
            "resolved": False,
            "reason": reason,
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
            "authorization": None,
        }
    )


def authorize_external_action(
    contract: MutableMapping[str, Any],
    action_id: str,
    approved_by: str,
    approved_at: str,
    note: str,
) -> None:
    if not approved_by.strip() or not approved_at.strip() or not note.strip():
        raise ContractStateError(
            "external authorization requires approver, timestamp, and note"
        )
    _require_valid_contract(contract)
    action = _find_external_action(contract, action_id)
    if action.get("status") != "PUBLISH_APPROVAL_REQUIRED":
        raise ContractStateError(
            f"cannot authorize external action in {action.get('status')!r} state"
        )
    action["status"] = "AUTHORIZED"
    action["authorization"] = {
        "approved_by": approved_by,
        "approved_at": approved_at,
        "note": note,
    }


def assert_external_action_authorized(
    contract: MutableMapping[str, Any], action_id: str, manifest_sha256: str
) -> None:
    _require_valid_contract(contract)
    action = _find_external_action(contract, action_id)
    if action.get("status") != "AUTHORIZED":
        raise ContractStateError(f"external action is not authorized: {action_id}")
    if action.get("manifest_sha256") != manifest_sha256:
        raise ContractStateError("authorized manifest hash does not match")


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
    governance.pop("approval_authority", None)
    governance["gate_authority"] = "course-run-with-validated-evidence"
    governance["external_action_authority"] = "explicit-user-authorization"
    governance["production_role_roster"] = None
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
    governance = migrated.get("governance")
    if not isinstance(governance, MutableMapping):
        raise ContractStateError("legacy governance is missing or invalid")
    governance.setdefault("production_role_roster", None)
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
