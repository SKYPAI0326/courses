from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, MutableMapping


GATE_ORDER: tuple[str, ...] = tuple(f"G{index}" for index in range(7))
GATE_STATUSES: frozenset[str] = frozenset(
    {"DRAFT", "REVIEW", "APPROVED", "BLOCKED", "STALE"}
)
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

REQUIRED_SECTIONS = (
    "schema_version",
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
)

REQUIRED_GATE_FIELDS = (
    "status",
    "owner",
    "inputs",
    "deliverables",
    "evidence",
    "risks",
    "open_questions",
    "approved_by",
    "approved_at",
    "source_revision",
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

_TRANSITIONS = {
    "submit": {"DRAFT": "REVIEW"},
    "approve": {"REVIEW": "APPROVED"},
    "block": {"DRAFT": "BLOCKED", "REVIEW": "BLOCKED", "STALE": "BLOCKED"},
    "semantic_change": {
        "DRAFT": "DRAFT",
        "REVIEW": "DRAFT",
        "APPROVED": "DRAFT",
        "BLOCKED": "DRAFT",
        "STALE": "DRAFT",
    },
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
    if not title.strip():
        raise ValueError("title must not be empty")
    if not created_by.strip():
        raise ValueError("created_by must not be empty")
    if not created_at.strip():
        raise ValueError("created_at must not be empty")

    gates: dict[str, dict[str, Any]] = {}
    for index, gate_id in enumerate(GATE_ORDER):
        gates[gate_id] = {
            "status": "DRAFT",
            "owner": _GATE_OWNERS[gate_id],
            "inputs": list(GATE_ORDER[:index]),
            "deliverables": [],
            "evidence": [],
            "risks": [],
            "open_questions": [],
            "approved_by": None,
            "approved_at": None,
            "source_revision": 0,
            "affected_downstream": list(GATE_ORDER[index + 1 :]),
        }

    return {
        "schema_version": 1,
        "identity": {"slug": slug, "title": title},
        "governance": {
            "created_by": created_by,
            "created_at": created_at,
            "approval_authority": "course-run-with-explicit-user-approval",
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
    }


def validate_contract(contract: Mapping[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for section in REQUIRED_SECTIONS:
        if section not in contract:
            issues.append(
                ValidationIssue("missing_section", f"$.{section}", f"missing required section: {section}")
            )

    if contract.get("schema_version") != 1:
        issues.append(
            ValidationIssue("unsupported_schema_version", "$.schema_version", "schema_version must be 1")
        )

    identity = contract.get("identity")
    if not isinstance(identity, Mapping):
        issues.append(ValidationIssue("invalid_identity", "$.identity", "identity must be an object"))
    else:
        slug = identity.get("slug")
        if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug):
            issues.append(
                ValidationIssue("invalid_slug", "$.identity.slug", "slug has an invalid format")
            )
        title = identity.get("title")
        if not isinstance(title, str) or not title.strip():
            issues.append(
                ValidationIssue("invalid_title", "$.identity.title", "title must not be empty")
            )

    gates = contract.get("gates")
    if not isinstance(gates, Mapping):
        issues.append(ValidationIssue("invalid_gates", "$.gates", "gates must be an object"))
        return issues

    for gate_id in GATE_ORDER:
        record = gates.get(gate_id)
        if not isinstance(record, Mapping):
            issues.append(
                ValidationIssue("missing_gate", f"$.gates.{gate_id}", f"missing gate record: {gate_id}")
            )
            continue
        for field in REQUIRED_GATE_FIELDS:
            if field not in record:
                issues.append(
                    ValidationIssue(
                        "missing_gate_field",
                        f"$.gates.{gate_id}.{field}",
                        f"{gate_id} is missing required field: {field}",
                    )
                )
        status = record.get("status")
        if status not in GATE_STATUSES:
            issues.append(
                ValidationIssue(
                    "unknown_gate_status",
                    f"$.gates.{gate_id}.status",
                    f"unknown gate status: {status!r}",
                )
            )

    for gate_id in gates:
        if gate_id not in GATE_ORDER:
            issues.append(
                ValidationIssue("unknown_gate", f"$.gates.{gate_id}", f"unknown gate id: {gate_id}")
            )

    return issues


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


def _transition(record: MutableMapping[str, Any], action: str) -> None:
    current = record.get("status")
    target = _TRANSITIONS[action].get(current)
    if target is None:
        raise ContractStateError(f"cannot {action} a gate in {current!r} state")
    record["status"] = target


def _require_previous_approvals(
    contract: MutableMapping[str, Any], gate_id: str
) -> None:
    gate_index = GATE_ORDER.index(gate_id)
    gates = contract["gates"]
    missing = [
        prior
        for prior in GATE_ORDER[:gate_index]
        if gates[prior].get("status") != "APPROVED"
    ]
    if missing:
        raise ContractStateError(
            f"{gate_id} requires approved previous gates: {', '.join(missing)}"
        )


def submit_gate(
    contract: MutableMapping[str, Any], gate_id: str, actor: str, at: str
) -> None:
    if not actor.strip() or not at.strip():
        raise ContractStateError("submission requires actor and timestamp")
    record = _gate_record(contract, gate_id)
    _require_previous_approvals(contract, gate_id)
    _transition(record, "submit")
    revision = record.get("source_revision")
    record["source_revision"] = revision + 1 if isinstance(revision, int) else 1
    record["evidence"].append(
        {"kind": "gate_submission", "actor": actor, "at": at}
    )


def approve_gate(
    contract: MutableMapping[str, Any],
    gate_id: str,
    approved_by: str,
    approved_at: str,
    approval_note: str,
) -> None:
    if not approved_by.strip() or not approved_at.strip() or not approval_note.strip():
        raise ContractStateError(
            "approval requires approver, timestamp, and explicit approval note"
        )
    record = _gate_record(contract, gate_id)
    _require_previous_approvals(contract, gate_id)
    unresolved = [
        risk
        for risk in record.get("risks", [])
        if isinstance(risk, Mapping)
        and risk.get("blocking") is True
        and risk.get("resolved") is not True
    ]
    if unresolved:
        raise ContractStateError(f"{gate_id} has unresolved blocking risks")
    _transition(record, "approve")
    record["approved_by"] = approved_by
    record["approved_at"] = approved_at
    record["evidence"].append(
        {
            "kind": "user_approval",
            "approved_by": approved_by,
            "approved_at": approved_at,
            "note": approval_note,
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
    record = _gate_record(contract, gate_id)
    _transition(record, "block")
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
    record = _gate_record(contract, affected_gate)
    affected_index = GATE_ORDER.index(affected_gate)
    invalidated = list(GATE_ORDER[affected_index:]) if semantic else []
    change_record = {
        "affected_gate": affected_gate,
        "reason": reason,
        "actor": actor,
        "at": at,
        "semantic": semantic,
        "invalidated_gates": invalidated,
    }
    changes = contract.get("changes")
    if not isinstance(changes, list):
        raise ContractStateError("contract changes must be a list")
    changes.append(change_record)

    if semantic:
        _transition(record, "semantic_change")
        record["approved_by"] = None
        record["approved_at"] = None
        for gate_id in GATE_ORDER[affected_index + 1 :]:
            contract["gates"][gate_id]["status"] = "STALE"
    return invalidated


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
