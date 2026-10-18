from __future__ import annotations

import base64
import hashlib
import math
import random
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Sequence

from src.course_contract import ContractStateError
from src.course_evidence import (
    canonical_json_bytes,
    consume_evidence_reference,
    materialize_json_evidence,
)
from src.course_runner_authority import (
    ALGORITHM,
    bind_runner_authority,
    consume_trial_inputs,
    transition_evidence_sha256,
)


_DIGEST_INFO_PREFIX = bytes.fromhex("3031300d060960864801650304020105000420")


def _is_probable_prime(candidate: int, rng: random.Random, rounds: int = 32) -> bool:
    if candidate < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if candidate == prime:
            return True
        if candidate % prime == 0:
            return False
    d = candidate - 1
    power = 0
    while d % 2 == 0:
        power += 1
        d //= 2
    for _ in range(rounds):
        base = rng.randrange(2, candidate - 1)
        value = pow(base, d, candidate)
        if value in (1, candidate - 1):
            continue
        for _ in range(power - 1):
            value = pow(value, 2, candidate)
            if value == candidate - 1:
                break
        else:
            return False
    return True


def _prime(bits: int, rng: random.Random) -> int:
    while True:
        candidate = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if _is_probable_prime(candidate, rng):
            return candidate


@lru_cache(maxsize=4)
def _keypair(slot: int) -> tuple[int, int, int]:
    seed = int.from_bytes(
        hashlib.sha256(f"course-proof-test-key:{slot}".encode("utf-8")).digest(),
        "big",
    )
    rng = random.Random(seed)
    exponent = 65537
    while True:
        p = _prime(1024, rng)
        q = _prime(1024, rng)
        if p == q:
            continue
        phi = (p - 1) * (q - 1)
        if math.gcd(exponent, phi) == 1:
            modulus = p * q
            if modulus.bit_length() < 2048:
                continue
            private_exponent = pow(exponent, -1, phi)
            return modulus, exponent, private_exponent


class TestRunnerAuthority:
    __test__ = False

    def __init__(
        self,
        authority_id: str,
        runners: Mapping[str, Mapping[str, Any]],
        *,
        key_slot: int = 0,
    ) -> None:
        self.authority_id = authority_id
        self.runners = {runner_id: dict(record) for runner_id, record in runners.items()}
        self._modulus, self._exponent, self._private_exponent = _keypair(key_slot)
        self.public_key = {
            "kty": "RSA",
            "n": format(self._modulus, "x"),
            "e": self._exponent,
        }
        self.runner_registry_sha256 = hashlib.sha256(
            canonical_json_bytes(self.runners)
        ).hexdigest()

    def bind(self, contract: dict[str, Any]) -> None:
        bind_runner_authority(
            contract,
            self.authority_id,
            self.public_key,
            self.runner_registry_sha256,
        )

    def _sign(self, payload: Mapping[str, Any]) -> str:
        digest_info = _DIGEST_INFO_PREFIX + hashlib.sha256(canonical_json_bytes(payload)).digest()
        size = (self._modulus.bit_length() + 7) // 8
        encoded = b"\x00\x01" + b"\xff" * (size - len(digest_info) - 3) + b"\x00" + digest_info
        signature = pow(int.from_bytes(encoded, "big"), self._private_exponent, self._modulus)
        return base64.b64encode(signature.to_bytes(size, "big")).decode("ascii")

    def issue(
        self,
        workspace_root: Path | str,
        *,
        contract: Mapping[str, Any],
        gate_id: str,
        trial_reference: Mapping[str, Any],
        roster_reference: Mapping[str, Any],
        transition_references: Sequence[Mapping[str, Any]],
        runner_id: str,
        session_id: str,
        issued_at: str,
        nonce: str,
        receipt_id: str,
        relative_path: str,
    ) -> dict[str, Any]:
        runner = self.runners.get(runner_id)
        if not isinstance(runner, Mapping):
            raise ContractStateError("external authority runner is not registered")
        sessions = runner.get("sessions")
        assertion = sessions.get(session_id) if isinstance(sessions, Mapping) else None
        if not isinstance(assertion, Mapping):
            raise ContractStateError("external authority has no assertion for this runner session")
        trial = consume_evidence_reference(
            workspace_root, trial_reference, expected_gate=gate_id, parse_json=True
        )
        roster = consume_evidence_reference(
            workspace_root, roster_reference, expected_gate="G0", parse_json=True
        )
        if not isinstance(trial.value, Mapping) or not isinstance(roster.value, Mapping):
            raise ContractStateError("external authority requires trial and roster objects")
        participant = trial.value.get("participant")
        if (
            not isinstance(participant, Mapping)
            or participant.get("id") != runner_id
            or participant.get("type") != "independent-ai"
            or trial.value.get("runner_session_id") != session_id
            or assertion.get("context_id") != trial.value.get("isolated_context_id")
        ):
            raise ContractStateError("external session assertion does not own this trial")
        role_ids = {
            str(item).casefold()
            for field in ("authors", "validators")
            for item in roster.value.get(field, [])
            if isinstance(item, str) and item.strip()
        }
        if runner_id.casefold() in role_ids:
            raise ContractStateError("external authority refuses production actors")
        consumed_inputs = consume_trial_inputs(workspace_root, trial.value)
        manifest = [
            {
                "kind": str(item.reference["kind"]),
                "path": str(item.reference["path"]),
                "sha256": item.sha256,
            }
            for item in consumed_inputs
        ]
        instance_id = contract.get("contract_instance_id")
        revision = contract.get("revision")
        if not isinstance(instance_id, str) or not isinstance(revision, int):
            raise ContractStateError("external authority requires trusted contract instance/revision")
        receipt: dict[str, Any] = {
            "schema_version": 2,
            "receipt_id": receipt_id,
            "authority_id": self.authority_id,
            "algorithm": ALGORITHM,
            "gate": gate_id,
            "contract_instance_id": instance_id,
            "contract_revision": revision,
            "evidence_set_sha256": transition_evidence_sha256(transition_references),
            "trial_evidence_id": trial_reference["id"],
            "trial_sha256": trial.sha256,
            "roster_sha256": roster.sha256,
            "runner_registry_sha256": self.runner_registry_sha256,
            "learner_input_manifest": manifest,
            "runner": {"id": runner_id, "role": runner.get("role")},
            "participant": dict(participant),
            "session_id": session_id,
            "session_assertion_id": assertion.get("assertion_id"),
            "isolated_context_id": trial.value.get("isolated_context_id"),
            "issuer": self.authority_id,
            "nonce": nonce,
            "issued_at": issued_at,
        }
        receipt["signature"] = self._sign(receipt)
        return materialize_json_evidence(
            workspace_root,
            evidence_id=receipt_id,
            gate_id=gate_id,
            kind="independent_trial_receipt",
            relative_path=relative_path,
            value=receipt,
            maturity="AUTHORITY_SIGNED",
            metadata={"authority_id": self.authority_id},
        )
