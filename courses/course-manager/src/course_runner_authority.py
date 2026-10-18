"""Verification-only boundary for externally issued independent-runner receipts.

This module contains public-key binding and RSA signature verification only.
Receipt issuance, runner-registry ownership checks, and signing material belong
to a separately controlled authority process. Local receipt consumption is
recorded in the contract; an external authority ledger remains responsible for
preventing replay across rolled-back contract snapshots. Verification is
deliberately limited to RSA keys of at least 2048 bits, exponent 65537, and
RSASSA-PKCS1-v1_5 with SHA-256; certificate chains and key revocation are out
of scope and must be governed by the surrounding deployment.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import re
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Sequence

from src.course_contract import ContractStateError
from src.course_evidence import ConsumedEvidence, canonical_json_bytes, consume_evidence_reference


ALGORITHM = "RSASSA-PKCS1-v1_5-SHA256"
_DIGEST_INFO_PREFIX = bytes.fromhex("3031300d060960864801650304020105000420")
PUBLIC_KEY_FIELDS = frozenset({"kty", "n", "e"})
AUTHORITY_FIELDS = frozenset(
    {"authority_id", "algorithm", "public_key", "public_key_fingerprint", "runner_registry_sha256"}
)
RECEIPT_FIELDS = frozenset(
    {
        "schema_version", "receipt_id", "authority_id", "algorithm", "gate",
        "contract_instance_id", "contract_revision", "evidence_set_sha256",
        "trial_evidence_id", "trial_sha256", "roster_sha256",
        "runner_registry_sha256", "learner_input_manifest", "runner",
        "participant", "session_id", "session_assertion_id",
        "isolated_context_id", "issuer", "nonce", "issued_at", "signature",
    }
)


@dataclass(frozen=True)
class AuthorityIssue:
    code: str
    message: str


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validated_public_key(value: Mapping[str, Any]) -> tuple[int, int]:
    if not isinstance(value, Mapping) or set(value) != PUBLIC_KEY_FIELDS:
        raise ContractStateError("runner authority public key has missing or unknown fields")
    if value.get("kty") != "RSA" or not isinstance(value.get("e"), int):
        raise ContractStateError("runner authority public key must be RSA")
    try:
        modulus = int(str(value.get("n", "")), 16)
    except ValueError as error:
        raise ContractStateError("runner authority RSA modulus must be hexadecimal") from error
    exponent = value["e"]
    if modulus.bit_length() < 2048 or exponent != 65537:
        raise ContractStateError("runner authority requires a 2048-bit-or-larger RSA key with exponent 65537")
    return modulus, exponent


def public_key_fingerprint(public_key: Mapping[str, Any]) -> str:
    _validated_public_key(public_key)
    return hashlib.sha256(canonical_json_bytes(dict(public_key))).hexdigest()


def bind_runner_authority(
    contract: MutableMapping[str, Any],
    authority_id: str,
    public_key: Mapping[str, Any],
    runner_registry_sha256: str,
) -> None:
    if not _text(authority_id):
        raise ContractStateError("runner authority id is required")
    if (
        not isinstance(runner_registry_sha256, str)
        or re.fullmatch(r"[0-9a-f]{64}", runner_registry_sha256) is None
    ):
        raise ContractStateError("runner registry digest must be lowercase SHA-256")
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
    governance["runner_authority"] = {
        "authority_id": authority_id,
        "algorithm": ALGORITHM,
        "public_key": dict(public_key),
        "public_key_fingerprint": public_key_fingerprint(public_key),
        "runner_registry_sha256": runner_registry_sha256,
    }


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
        manifest.append({field: str(item[field]) for field in ("kind", "path", "sha256")})
    return sorted(manifest, key=lambda item: (item["kind"], item["path"], item["sha256"]))


def consume_trial_inputs(
    workspace_root: Path | str, trial: Mapping[str, Any]
) -> list[ConsumedEvidence]:
    consumed: list[ConsumedEvidence] = []
    for index, item in enumerate(_input_manifest(trial)):
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


def transition_evidence_sha256(references: Sequence[Mapping[str, Any]]) -> str:
    records: list[dict[str, Any]] = []
    for reference in references:
        if not isinstance(reference, Mapping) or any(
            not _text(reference.get(field)) for field in ("id", "gate", "kind", "path", "sha256")
        ):
            raise ContractStateError("transition evidence digest requires complete typed references")
        if reference.get("kind") == "independent_trial_receipt":
            continue
        records.append(
            {
                key: reference[key]
                for key in ("id", "gate", "kind", "path", "sha256", "maturity", "metadata")
                if key in reference
            }
        )
    records.sort(key=lambda item: (str(item["gate"]), str(item["kind"]), str(item["id"])))
    return hashlib.sha256(canonical_json_bytes(records)).hexdigest()


def _unsigned_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {key: receipt[key] for key in sorted(set(receipt) - {"signature"})}


def _verify_signature(
    receipt: Mapping[str, Any], public_key: Mapping[str, Any]
) -> bool:
    try:
        modulus, exponent = _validated_public_key(public_key)
        signature = base64.b64decode(receipt.get("signature", ""), validate=True)
    except (ContractStateError, ValueError, TypeError, binascii.Error):
        return False
    size = (modulus.bit_length() + 7) // 8
    if len(signature) != size:
        return False
    recovered = pow(int.from_bytes(signature, "big"), exponent, modulus).to_bytes(size, "big")
    digest_info = _DIGEST_INFO_PREFIX + hashlib.sha256(
        canonical_json_bytes(_unsigned_receipt(receipt))
    ).digest()
    expected = b"\x00\x01" + b"\xff" * (size - len(digest_info) - 3) + b"\x00" + digest_info
    return secrets.compare_digest(recovered, expected)


def verify_trial_receipt(
    receipt: Mapping[str, Any],
    authority_binding: Mapping[str, Any],
    *,
    contract: Mapping[str, Any],
    expected_evidence_set_sha256: str,
    receipt_reference: Mapping[str, Any],
    learner_inputs: Sequence[ConsumedEvidence],
    gate_id: str,
    trial: ConsumedEvidence,
    roster: ConsumedEvidence,
) -> list[AuthorityIssue]:
    issues: list[AuthorityIssue] = []
    if not isinstance(receipt, Mapping) or set(receipt) != RECEIPT_FIELDS:
        return [AuthorityIssue("invalid_receipt", "receipt has missing or unknown fields")]
    if not isinstance(authority_binding, Mapping) or set(authority_binding) != AUTHORITY_FIELDS:
        return [AuthorityIssue("invalid_authority_binding", "contract authority binding is invalid")]
    public_key = authority_binding.get("public_key")
    try:
        fingerprint = public_key_fingerprint(public_key)
    except (ContractStateError, TypeError):
        return [AuthorityIssue("invalid_authority_binding", "contract authority public key is invalid")]
    if fingerprint != authority_binding.get("public_key_fingerprint"):
        return [AuthorityIssue("authority_binding_mismatch", "governed public key fingerprint is invalid")]
    if not _verify_signature(receipt, public_key):
        return [AuthorityIssue("invalid_receipt_signature", "receipt signature is invalid")]

    authority_id = authority_binding.get("authority_id")
    if receipt.get("schema_version") != 2 or receipt.get("algorithm") != ALGORITHM:
        issues.append(AuthorityIssue("invalid_receipt", "receipt schema or algorithm is unsupported"))
    if receipt.get("authority_id") != authority_id or receipt.get("issuer") != authority_id:
        issues.append(AuthorityIssue("wrong_receipt_authority", "receipt authority does not match contract governance"))
    if receipt.get("runner_registry_sha256") != authority_binding.get("runner_registry_sha256"):
        issues.append(AuthorityIssue("runner_binding_mismatch", "receipt runner registry does not match contract governance"))
    if receipt.get("gate") != gate_id:
        issues.append(AuthorityIssue("receipt_replay", "receipt belongs to another Gate"))
    if receipt.get("receipt_id") != receipt_reference.get("id"):
        issues.append(AuthorityIssue("receipt_replay", "receipt id does not match its typed evidence reference"))
    if receipt.get("contract_instance_id") != contract.get("contract_instance_id"):
        issues.append(AuthorityIssue("contract_replay", "receipt belongs to another contract instance"))
    if receipt.get("contract_revision") != contract.get("revision"):
        issues.append(AuthorityIssue("contract_replay", "receipt belongs to another contract revision"))
    if receipt.get("evidence_set_sha256") != expected_evidence_set_sha256:
        issues.append(AuthorityIssue("evidence_set_replay", "receipt does not bind the exact transition evidence set"))
    if receipt.get("trial_evidence_id") != trial.reference.get("id") or receipt.get("trial_sha256") != trial.sha256:
        issues.append(AuthorityIssue("trial_binding_mismatch", "receipt does not bind the consumed trial file"))
    if receipt.get("roster_sha256") != roster.sha256:
        issues.append(AuthorityIssue("roster_binding_mismatch", "receipt does not bind the governed roster snapshot"))

    ledger = contract.get("consumed_trial_receipts")
    if not isinstance(ledger, list):
        issues.append(AuthorityIssue("receipt_ledger_invalid", "contract receipt ledger is invalid"))
    elif any(
        isinstance(item, Mapping)
        and (
            item.get("receipt_id") == receipt.get("receipt_id")
            or item.get("nonce") == receipt.get("nonce")
        )
        for item in ledger
    ):
        issues.append(AuthorityIssue("receipt_replay", "receipt id or nonce was already consumed"))

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
        or not _text(runner_id)
        or runner.get("role") != "isolated-learner-runner"
        or not isinstance(participant, Mapping)
        or participant.get("id") != runner_id
        or not _text(receipt.get("session_assertion_id"))
    ):
        issues.append(AuthorityIssue("runner_binding_mismatch", "receipt lacks a governed external runner/session assertion"))
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
