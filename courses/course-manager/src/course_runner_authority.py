"""Host-provisioned authority for pre-issued independent-runner receipts.

The trust boundary assumes the course route caller cannot read or replace the
authority secret/runner registry in the host process environment. HMAC detects
receipt or workspace-file tampering; it does not defend against the machine or
process-environment owner.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, MutableMapping

from src.course_contract import ContractStateError
from src.course_evidence import (
    ConsumedEvidence,
    canonical_json_bytes,
    consume_evidence_reference,
    materialize_json_evidence,
)


ALGORITHM = "HMAC-SHA256"
AUTHORITY_FIELDS = frozenset(
    {"authority_id", "algorithm", "key_fingerprint", "runner_registry_sha256"}
)
RECEIPT_FIELDS = frozenset(
    {
        "schema_version", "authority_id", "algorithm", "gate",
        "trial_evidence_id", "trial_sha256", "roster_sha256",
        "learner_input_manifest", "runner", "participant",
        "session_id", "isolated_context_id", "issuer", "nonce",
        "issued_at", "signature",
    }
)


@dataclass(frozen=True)
class AuthorityIssue:
    code: str
    message: str


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _environment_prefix(authority_id: str) -> str:
    if not _text(authority_id):
        raise ValueError("authority_id must contain text")
    suffix = re.sub(r"[^A-Z0-9]+", "_", authority_id.upper()).strip("_")
    if not suffix:
        raise ValueError("authority_id has no environment-safe characters")
    return f"COURSE_RUNNER_AUTHORITY_{suffix}"


def _required_authority_id() -> str:
    authority_id = os.environ.get("COURSE_RUNNER_REQUIRED_AUTHORITY_ID")
    if not _text(authority_id):
        raise ContractStateError("COURSE_RUNNER_REQUIRED_AUTHORITY_ID is not provisioned")
    return str(authority_id)


def _load_authority(authority_id: str) -> tuple[bytes, dict[str, str], dict[str, str]]:
    prefix = _environment_prefix(authority_id)
    encoded_secret = os.environ.get(f"{prefix}_SECRET")
    encoded_runners = os.environ.get(f"{prefix}_RUNNERS")
    if not _text(encoded_secret) or not _text(encoded_runners):
        raise ContractStateError(
            f"runner authority {authority_id!r} is not provisioned in the process environment"
        )
    try:
        secret = base64.b64decode(encoded_secret, validate=True)
    except (ValueError, TypeError) as error:
        raise ContractStateError("runner authority secret must be valid base64") from error
    if len(secret) < 32:
        raise ContractStateError("runner authority secret must contain at least 32 bytes")
    try:
        runners = json.loads(encoded_runners)
    except json.JSONDecodeError as error:
        raise ContractStateError("runner authority registry must be valid JSON") from error
    if (
        not isinstance(runners, dict)
        or not runners
        or not all(_text(key) and _text(value) for key, value in runners.items())
    ):
        raise ContractStateError("runner authority registry must map runner ids to roles")
    normalized = {str(key): str(value) for key, value in runners.items()}
    binding = {
        "authority_id": authority_id,
        "algorithm": ALGORITHM,
        "key_fingerprint": hashlib.sha256(secret).hexdigest(),
        "runner_registry_sha256": hashlib.sha256(canonical_json_bytes(normalized)).hexdigest(),
    }
    return secret, normalized, binding


def bind_runner_authority(
    contract: MutableMapping[str, Any], authority_id: str
) -> None:
    if authority_id != _required_authority_id():
        raise ContractStateError("runner authority does not match the process verification root")
    gates = contract.get("gates")
    if not isinstance(gates, Mapping) or any(
        not isinstance(record, Mapping) or record.get("status") != "NOT_STARTED"
        for record in gates.values()
    ):
        raise ContractStateError("runner authority must be fixed before Gate work begins")
    governance = contract.get("governance")
    if not isinstance(governance, MutableMapping):
        raise ContractStateError("contract governance is missing")
    if governance.get("runner_authority") is not None:
        raise ContractStateError("runner authority is already fixed")
    _, _, binding = _load_authority(authority_id)
    governance["runner_authority"] = binding


def _input_manifest(trial: Mapping[str, Any]) -> list[dict[str, str]]:
    inputs = trial.get("allowed_inputs")
    if not isinstance(inputs, list) or not inputs:
        raise ContractStateError("trial requires learner-visible inputs")
    manifest: list[dict[str, str]] = []
    for item in inputs:
        if not isinstance(item, Mapping) or any(
            not _text(item.get(field)) for field in ("kind", "path", "sha256")
        ):
            raise ContractStateError("trial learner-visible input is incomplete")
        manifest.append(
            {field: str(item[field]) for field in ("kind", "path", "sha256")}
        )
    return sorted(manifest, key=lambda item: (item["kind"], item["path"], item["sha256"]))


def consume_trial_inputs(
    workspace_root: Path | str, trial: Mapping[str, Any]
) -> list[ConsumedEvidence]:
    manifest = _input_manifest(trial)
    consumed: list[ConsumedEvidence] = []
    for index, item in enumerate(manifest):
        reference = {
            "id": f"runner-input-{index}",
            "gate": "G0",
            "kind": item["kind"],
            "path": item["path"],
            "sha256": item["sha256"],
        }
        try:
            consumed.append(consume_evidence_reference(workspace_root, reference))
        except (OSError, ValueError) as error:
            raise ContractStateError(
                f"runner authority could not verify learner-visible input {item['path']}: {error}"
            ) from error
    return consumed


def _unsigned_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {key: receipt[key] for key in sorted(set(receipt) - {"signature"})}


def issue_trial_receipt(
    workspace_root: Path | str,
    *,
    authority_id: str,
    gate_id: str,
    trial_reference: Mapping[str, Any],
    roster_reference: Mapping[str, Any],
    runner_id: str,
    session_id: str,
    issued_at: str,
    nonce: str,
    evidence_id: str,
    relative_path: str,
) -> dict[str, Any]:
    if authority_id != _required_authority_id():
        raise ContractStateError("receipt issuer does not match the process authority")
    if gate_id not in {"G4", "G5"}:
        raise ContractStateError("independent trial receipts may be issued only for G4 or G5")
    secret, runners, _ = _load_authority(authority_id)
    if runner_id not in runners:
        raise ContractStateError("runner is not registered by the configured authority")
    if any(not _text(value) for value in (session_id, issued_at, nonce)):
        raise ContractStateError("receipt session, issued_at, and nonce are required")
    trial = consume_evidence_reference(
        workspace_root, trial_reference, expected_gate=gate_id, parse_json=True
    )
    roster = consume_evidence_reference(
        workspace_root, roster_reference, expected_gate="G0", parse_json=True
    )
    if not isinstance(trial.value, Mapping) or not isinstance(roster.value, Mapping):
        raise ContractStateError("trial and roster evidence must be JSON objects")
    participant = trial.value.get("participant")
    if (
        not isinstance(participant, Mapping)
        or participant.get("id") != runner_id
        or participant.get("type") != "independent-ai"
    ):
        raise ContractStateError("authority may issue only for its registered independent participant")
    if trial.value.get("runner_session_id") != session_id:
        raise ContractStateError("receipt session must match the trial runner_session_id")
    role_ids = {
        str(item).casefold()
        for field in ("authors", "validators")
        for item in roster.value.get(field, [])
        if _text(item)
    }
    if runner_id.casefold() in role_ids:
        raise ContractStateError("production authors and validators cannot receive independent runner receipts")

    learner_input_manifest = _input_manifest(trial.value)
    consume_trial_inputs(workspace_root, trial.value)
    receipt: dict[str, Any] = {
        "schema_version": 1,
        "authority_id": authority_id,
        "algorithm": ALGORITHM,
        "gate": gate_id,
        "trial_evidence_id": trial_reference["id"],
        "trial_sha256": trial.sha256,
        "roster_sha256": roster.sha256,
        "learner_input_manifest": learner_input_manifest,
        "runner": {"id": runner_id, "role": runners[runner_id]},
        "participant": {
            "id": participant.get("id"),
            "type": participant.get("type"),
            "roles": list(participant.get("roles", [])),
        },
        "session_id": session_id,
        "isolated_context_id": trial.value.get("isolated_context_id"),
        "issuer": authority_id,
        "nonce": nonce,
        "issued_at": issued_at,
    }
    receipt["signature"] = hmac.new(
        secret, canonical_json_bytes(receipt), hashlib.sha256
    ).hexdigest()
    return materialize_json_evidence(
        workspace_root,
        evidence_id=evidence_id,
        gate_id=gate_id,
        kind="independent_trial_receipt",
        relative_path=relative_path,
        value=receipt,
        maturity="AUTHORITY_SIGNED",
        metadata={"authority_id": authority_id},
    )


def verify_trial_receipt(
    receipt: Mapping[str, Any],
    authority_binding: Mapping[str, Any],
    *,
    learner_inputs: list[ConsumedEvidence],
    gate_id: str,
    trial: ConsumedEvidence,
    roster: ConsumedEvidence,
) -> list[AuthorityIssue]:
    issues: list[AuthorityIssue] = []
    if not isinstance(receipt, Mapping) or set(receipt) != RECEIPT_FIELDS:
        return [AuthorityIssue("invalid_receipt", "receipt has missing or unknown fields")]
    if not isinstance(authority_binding, Mapping) or set(authority_binding) != AUTHORITY_FIELDS:
        return [AuthorityIssue("invalid_authority_binding", "contract authority binding is invalid")]
    authority_id = authority_binding.get("authority_id")
    try:
        required_authority_id = _required_authority_id()
    except ContractStateError as error:
        return [AuthorityIssue("authority_unavailable", str(error))]
    if authority_id != required_authority_id:
        return [AuthorityIssue("authority_binding_mismatch", "contract authority does not match the process verification root")]
    try:
        secret, runners, current_binding = _load_authority(str(authority_id))
    except (ContractStateError, ValueError) as error:
        return [AuthorityIssue("authority_unavailable", str(error))]
    if current_binding != dict(authority_binding):
        issues.append(AuthorityIssue("authority_binding_mismatch", "configured authority does not match the governed verification root"))
        return issues
    signature = receipt.get("signature")
    expected = hmac.new(
        secret, canonical_json_bytes(_unsigned_receipt(receipt)), hashlib.sha256
    ).hexdigest()
    if not isinstance(signature, str) or not hmac.compare_digest(signature, expected):
        issues.append(AuthorityIssue("invalid_receipt_signature", "receipt signature is invalid"))
        return issues
    if receipt.get("schema_version") != 1 or receipt.get("algorithm") != ALGORITHM:
        issues.append(AuthorityIssue("invalid_receipt", "receipt schema or algorithm is unsupported"))
    if receipt.get("authority_id") != authority_id or receipt.get("issuer") != authority_id:
        issues.append(AuthorityIssue("wrong_receipt_authority", "receipt authority does not match contract governance"))
    if receipt.get("gate") != gate_id:
        issues.append(AuthorityIssue("receipt_replay", "receipt belongs to another Gate"))
    if receipt.get("trial_evidence_id") != trial.reference.get("id") or receipt.get("trial_sha256") != trial.sha256:
        issues.append(AuthorityIssue("trial_binding_mismatch", "receipt does not bind the consumed trial file"))
    if receipt.get("roster_sha256") != roster.sha256:
        issues.append(AuthorityIssue("roster_binding_mismatch", "receipt does not bind the governed roster snapshot"))
    trial_value = trial.value
    if not isinstance(trial_value, Mapping):
        issues.append(AuthorityIssue("invalid_trial", "consumed trial is not an object"))
        return issues
    try:
        manifest = _input_manifest(trial_value)
    except ContractStateError as error:
        issues.append(AuthorityIssue("input_binding_mismatch", str(error)))
        manifest = []
    if receipt.get("learner_input_manifest") != manifest:
        issues.append(AuthorityIssue("input_binding_mismatch", "receipt learner-visible inputs do not match the trial"))
    consumed_manifest = [
        {
            "kind": str(item.reference.get("kind", "")),
            "path": str(item.reference.get("path", "")),
            "sha256": item.sha256,
        }
        for item in learner_inputs
    ]
    if consumed_manifest != manifest:
        issues.append(AuthorityIssue("input_binding_mismatch", "receipt inputs do not match the securely consumed learner-visible files"))
    participant = trial_value.get("participant")
    runner = receipt.get("runner")
    if receipt.get("participant") != participant:
        issues.append(AuthorityIssue("participant_binding_mismatch", "receipt participant does not match the trial"))
    runner_id = runner.get("id") if isinstance(runner, Mapping) else None
    if (
        not isinstance(runner, Mapping)
        or runners.get(runner_id) != runner.get("role")
        or not isinstance(participant, Mapping)
        or participant.get("id") != runner_id
    ):
        issues.append(AuthorityIssue("runner_binding_mismatch", "receipt runner is not registered for this participant"))
    if receipt.get("session_id") != trial_value.get("runner_session_id"):
        issues.append(AuthorityIssue("receipt_replay", "receipt session does not match the trial"))
    if receipt.get("isolated_context_id") != trial_value.get("isolated_context_id"):
        issues.append(AuthorityIssue("receipt_replay", "receipt context does not match the trial"))
    roster_value = roster.value
    role_ids = {
        str(item).casefold()
        for field in ("authors", "validators")
        for item in (roster_value.get(field, []) if isinstance(roster_value, Mapping) else [])
        if _text(item)
    }
    if isinstance(runner_id, str) and runner_id.casefold() in role_ids:
        issues.append(AuthorityIssue("runner_not_independent", "runner is a governed author or validator"))
    return issues
