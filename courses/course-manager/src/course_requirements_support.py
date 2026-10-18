from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from src.schema_runtime import validate_schema_file


@dataclass(frozen=True)
class RequirementsSupportIssue:
    code: str
    path: str
    message: str


def validate_requirements_support_record(
    record: Mapping[str, Any], known_artifact_sha256: Mapping[str, str]
) -> list[RequirementsSupportIssue]:
    issues = [
        RequirementsSupportIssue(issue.code, issue.path, issue.message)
        for issue in validate_schema_file("course-requirements-support.schema.json", record)
    ]
    acceptance = record.get("acceptance_criterion_ids")
    preserved = record.get("preserved_acceptance_ids")
    if not isinstance(acceptance, list) or not acceptance or preserved != acceptance:
        issues.append(RequirementsSupportIssue(
            "support_acceptance_mismatch", "$.preserved_acceptance_ids",
            "verified fallback must preserve every affected acceptance criterion in the same order",
        ))
    artifacts = record.get("artifacts")
    seen: set[str] = set()
    if not isinstance(artifacts, list) or not artifacts:
        issues.append(RequirementsSupportIssue(
            "support_artifact_required", "$.artifacts",
            "verified fallback requires at least one replayed support artifact",
        ))
    else:
        for index, artifact in enumerate(artifacts):
            evidence_id = artifact.get("evidence_id") if isinstance(artifact, Mapping) else None
            digest = artifact.get("sha256") if isinstance(artifact, Mapping) else None
            if (
                not isinstance(evidence_id, str) or evidence_id in seen
                or known_artifact_sha256.get(evidence_id) != digest
            ):
                issues.append(RequirementsSupportIssue(
                    "support_artifact_mismatch", f"$.artifacts[{index}]",
                    "support artifact id and SHA-256 must match a safely consumed G0 artifact",
                ))
            if isinstance(evidence_id, str):
                seen.add(evidence_id)
    return issues


__all__ = ["RequirementsSupportIssue", "validate_requirements_support_record"]
