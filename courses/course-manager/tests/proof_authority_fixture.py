"""Test-only external authority harness for deterministic proof rebuilds.

Production proof code receives this provider as a dependency.  It does not own,
generate, or persist runner signing authority.
"""

from pathlib import Path

from tests.runner_authority_fixture import TestRunnerAuthority


_AUTHORITY = TestRunnerAuthority(
    "test-proof-runner-authority",
    {
        "independent-ai-representative-unit": {
            "role": "isolated-learner-runner",
            "sessions": {
                "session-representative-unit": {
                    "assertion_id": "assertion-proof-g4",
                    "context_id": "context-representative-unit",
                }
            },
        },
        "independent-ai-full-course": {
            "role": "isolated-learner-runner",
            "sessions": {
                "session-full-course": {
                    "assertion_id": "assertion-proof-g5",
                    "context_id": "context-full-course",
                }
            },
        },
    },
    key_slot=3,
)


def rebuild_proof(output_root: Path) -> None:
    from proofs.campaign_performance_brief_loader import load_builder

    builder = load_builder()
    builder["main"](authority_provider=_AUTHORITY, output_root=Path(output_root))
