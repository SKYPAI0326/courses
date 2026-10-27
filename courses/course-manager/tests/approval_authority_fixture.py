from __future__ import annotations

import base64
import hashlib

from src.course_contract import (
    bind_external_approval_authority,
    external_action_approval_basis,
)
from src.course_evidence import canonical_json_bytes
from tests.runner_authority_fixture import _DIGEST_INFO_PREFIX, _keypair


class TestApprovalAuthority:
    __test__ = False

    def __init__(self, *, key_slot=3):
        self.authority_id = "test-user-interaction-authority"
        self.modulus, self.exponent, self.private_exponent = _keypair(key_slot)
        self.public_key = {
            "kty": "RSA",
            "n": format(self.modulus, "x"),
            "e": self.exponent,
        }

    def bind(self, contract):
        bind_external_approval_authority(
            contract, self.authority_id, self.public_key
        )

    def issue(
        self,
        contract,
        action_id,
        *,
        nonce="approval-nonce-01",
        expires_at="2027-10-18T18:20:00+00:00",
    ):
        basis = external_action_approval_basis(contract, action_id)
        receipt = {
            "schema_version": 1,
            "receipt_id": f"receipt-{nonce}",
            "authority_id": self.authority_id,
            "algorithm": "RSASSA-PKCS1-v1_5-SHA256",
            **basis,
            "interaction": {
                "kind": "explicit_user_approval",
                "user_id": "course-owner-verified",
                "session_id": "ui-session-20261018",
                "confirmed_at": "2026-10-18T18:04:00+00:00",
            },
            "nonce": nonce,
            "issued_at": "2026-10-18T18:04:01+00:00",
            "expires_at": expires_at,
        }
        digest_info = _DIGEST_INFO_PREFIX + hashlib.sha256(
            canonical_json_bytes(receipt)
        ).digest()
        size = (self.modulus.bit_length() + 7) // 8
        encoded = (
            b"\x00\x01"
            + b"\xff" * (size - len(digest_info) - 3)
            + b"\x00"
            + digest_info
        )
        signature = pow(
            int.from_bytes(encoded, "big"), self.private_exponent, self.modulus
        )
        receipt["signature"] = base64.b64encode(
            signature.to_bytes(size, "big")
        ).decode("ascii")
        return receipt
