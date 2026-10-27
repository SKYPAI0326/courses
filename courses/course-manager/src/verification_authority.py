"""Small verification-only RSA primitive shared by governed authorities.

The module deliberately has no key generation, private-key, issuance, or signing
API.  Production code can bind and verify externally issued receipts only.
"""

from __future__ import annotations

import base64
import binascii
import hashlib
import secrets
from typing import Any, Mapping

from src.course_evidence import canonical_json_bytes


ALGORITHM = "RSASSA-PKCS1-v1_5-SHA256"
PUBLIC_KEY_FIELDS = frozenset({"kty", "n", "e"})
_DIGEST_INFO_PREFIX = bytes.fromhex("3031300d060960864801650304020105000420")


class VerificationKeyError(ValueError):
    pass


def validated_rsa_public_key(value: Mapping[str, Any]) -> tuple[int, int]:
    if not isinstance(value, Mapping) or set(value) != PUBLIC_KEY_FIELDS:
        raise VerificationKeyError("public key has missing or unknown fields")
    if value.get("kty") != "RSA" or not isinstance(value.get("e"), int):
        raise VerificationKeyError("public key must be RSA")
    try:
        modulus = int(str(value.get("n", "")), 16)
    except ValueError as error:
        raise VerificationKeyError("RSA modulus must be hexadecimal") from error
    exponent = value["e"]
    if modulus.bit_length() < 2048 or exponent != 65537:
        raise VerificationKeyError(
            "RSA key requires a 2048-bit-or-larger modulus and exponent 65537"
        )
    return modulus, exponent


def public_key_fingerprint(public_key: Mapping[str, Any]) -> str:
    validated_rsa_public_key(public_key)
    return hashlib.sha256(canonical_json_bytes(dict(public_key))).hexdigest()


def verify_rsa_sha256_signature(
    payload: Mapping[str, Any], signature_text: Any, public_key: Mapping[str, Any]
) -> bool:
    try:
        modulus, exponent = validated_rsa_public_key(public_key)
        signature = base64.b64decode(signature_text, validate=True)
    except (VerificationKeyError, ValueError, TypeError, binascii.Error):
        return False
    size = (modulus.bit_length() + 7) // 8
    if len(signature) != size:
        return False
    recovered = pow(int.from_bytes(signature, "big"), exponent, modulus).to_bytes(
        size, "big"
    )
    digest_info = _DIGEST_INFO_PREFIX + hashlib.sha256(
        canonical_json_bytes(dict(payload))
    ).digest()
    padding_length = size - len(digest_info) - 3
    if padding_length < 8:
        return False
    expected = b"\x00\x01" + b"\xff" * padding_length + b"\x00" + digest_info
    return secrets.compare_digest(recovered, expected)
