from __future__ import annotations

import copy
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, MutableMapping, Sequence

from src.course_contract import ContractStateError


SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
TRIAL_SCOPES = {"representative_unit", "full_course"}
PARTICIPANT_TYPES = {"independent-ai", "human"}
LEARNER_INPUT_KINDS = {"learner-page", "learner-asset"}
DISALLOWED_ROLE_MARKERS = (
    "author",
    "validator",
    "designer",
    "reviewer",
    "builder",
    "course-run",
)
FORBIDDEN_INPUT_MARKERS = (
    "author-note",
    "author_note",
    "course-contract",
    "course_contract",
    "answer-key",
    "answer_key",
    "solution-key",
    "solution_key",
)


@dataclass(frozen=True)
class TrialIssue:
    code: str
    path: str
    message: str
    return_gate: str


_FAILURE_GATE_EXACT = {
    "source_mismatch": "G1",
    "tool_behavior_mismatch": "G1",
    "sequence_overload": "G2",
    "difficulty_mismatch": "G2",
    "explanation_gap": "G3",
    "practice_instruction_gap": "G3",
    "interface_block": "G4",
    "asset_missing": "G4",
    "full_course_integration": "G5",
    "access_denied": "G6",
    "deployment_failure": "G6",
}

_FAILURE_GATE_PREFIXES = (
    (("source_", "research_", "tool_"), "G1"),
    (("sequence_", "difficulty_", "architecture_"), "G2"),
    (("explanation_", "practice_", "content_", "instruction_"), "G3"),
    (("interface_", "asset_", "layout_", "pilot_"), "G4"),
    (("full_course_", "cross_unit_", "production_"), "G5"),
    (("access_", "deployment_", "release_"), "G6"),
)


def route_trial_failure(issue_code: str) -> str:
    if issue_code in _FAILURE_GATE_EXACT:
        return _FAILURE_GATE_EXACT[issue_code]
    for prefixes, gate_id in _FAILURE_GATE_PREFIXES:
        if issue_code.startswith(prefixes):
            return gate_id
    raise ValueError(f"unclassified trial failure code: {issue_code}")


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _add(
    issues: list[TrialIssue],
    code: str,
    path: str,
    message: str,
    return_gate: str | None = None,
) -> None:
    if return_gate is None:
        try:
            return_gate = route_trial_failure(code)
        except ValueError:
            return_gate = "G3"
    issues.append(TrialIssue(code, path, message, return_gate))


def _validate_collection(value: Any, path: str, issues: list[TrialIssue]) -> list[Any] | None:
    if not isinstance(value, list):
        _add(issues, "trial_record_incomplete", path, f"{path} must be a list")
        return None
    return value


def production_role_ids(
    production_roles: Sequence[str] | Mapping[str, Any],
) -> tuple[str, ...]:
    if isinstance(production_roles, Mapping):
        if production_roles.get("schema_version") != 1:
            raise ValueError("production role roster schema_version must be 1")
        role_ids: list[str] = []
        for field in ("authors", "validators"):
            values = production_roles.get(field)
            if not isinstance(values, list) or not values or not all(
                _text(item) for item in values
            ):
                raise ValueError(
                    f"production role roster {field} must be a non-empty text list"
                )
            role_ids.extend(item.strip() for item in values)
        normalized = [item.casefold() for item in role_ids]
        if len(normalized) != len(set(normalized)):
            raise ValueError("production role roster identities must be unique")
        return tuple(role_ids)
    if isinstance(production_roles, (str, bytes)):
        raise ValueError("production roles must be a roster or a sequence of identities")
    return tuple(str(item).strip() for item in production_roles if _text(item))


def validate_trial_record(
    record: Mapping[str, Any],
    production_roles: Sequence[str] | Mapping[str, Any],
    expected_scope: str,
) -> list[TrialIssue]:
    issues: list[TrialIssue] = []
    if expected_scope not in TRIAL_SCOPES:
        raise ValueError(f"unsupported expected trial scope: {expected_scope}")
    if record.get("schema_version") != 1:
        _add(
            issues,
            "trial_record_incomplete",
            "$.schema_version",
            "trial record schema_version must be 1",
        )
    scope = record.get("scope")
    if scope != expected_scope:
        _add(
            issues,
            "trial_scope_mismatch",
            "$.scope",
            f"trial scope must be {expected_scope}",
            "G4" if expected_scope == "representative_unit" else "G5",
        )

    participant = record.get("participant")
    if not isinstance(participant, Mapping):
        _add(
            issues,
            "independent_participant_required",
            "$.participant",
            "trial participant identity and role are required",
        )
    else:
        participant_id = participant.get("id")
        participant_type = participant.get("type")
        roles = participant.get("roles")
        normalized_authors = {
            item.casefold() for item in production_role_ids(production_roles)
        }
        if not _text(participant_id):
            _add(
                issues,
                "independent_participant_required",
                "$.participant.id",
                "participant id is required",
            )
        elif participant_id.strip().casefold() in normalized_authors:
            _add(
                issues,
                "independent_participant_required",
                "$.participant.id",
                "trial participant cannot be a course author or validator",
            )
        if participant_type not in PARTICIPANT_TYPES:
            _add(
                issues,
                "independent_participant_required",
                "$.participant.type",
                "participant type must be independent-ai or human",
            )
        if not isinstance(roles, list) or not roles or not all(_text(role) for role in roles):
            _add(
                issues,
                "independent_participant_required",
                "$.participant.roles",
                "participant roles must identify the isolated learner-trial role",
            )
        elif any(
            marker in role.casefold()
            for role in roles
            for marker in DISALLOWED_ROLE_MARKERS
        ):
            _add(
                issues,
                "independent_participant_required",
                "$.participant.roles",
                "course production and validation roles cannot perform the trial",
            )

    if not _text(record.get("isolated_context_id")):
        _add(
            issues,
            "independent_participant_required",
            "$.isolated_context_id",
            "an isolated context id is required",
        )
    if not _text(record.get("runner_session_id")):
        _add(
            issues,
            "trial_record_incomplete",
            "$.runner_session_id",
            "a runner session id is required",
        )

    allowed_inputs = _validate_collection(
        record.get("allowed_inputs"), "$.allowed_inputs", issues
    )
    if allowed_inputs is not None:
        if not allowed_inputs:
            _add(
                issues,
                "non_learner_input_accessed",
                "$.allowed_inputs",
                "trial requires at least one learner-visible input",
            )
        for index, item in enumerate(allowed_inputs):
            path = f"$.allowed_inputs[{index}]"
            if not isinstance(item, Mapping):
                _add(issues, "non_learner_input_accessed", path, "input must be an object")
                continue
            kind = item.get("kind")
            input_path = item.get("path")
            combined = f"{kind or ''} {input_path or ''}".casefold()
            if kind not in LEARNER_INPUT_KINDS or any(
                marker in combined for marker in FORBIDDEN_INPUT_MARKERS
            ):
                _add(
                    issues,
                    "non_learner_input_accessed",
                    path,
                    "only learner pages and learner assets may enter the trial context",
                )
            if not _text(input_path):
                _add(issues, "non_learner_input_accessed", f"{path}.path", "input path is required")
            if not SHA256_PATTERN.fullmatch(str(item.get("sha256", ""))):
                _add(
                    issues,
                    "non_learner_input_accessed",
                    f"{path}.sha256",
                    "input must be bound to a lowercase SHA-256",
                )

    forbidden_access = _validate_collection(
        record.get("forbidden_inputs_accessed"),
        "$.forbidden_inputs_accessed",
        issues,
    )
    if forbidden_access:
        _add(
            issues,
            "non_learner_input_accessed",
            "$.forbidden_inputs_accessed",
            "trial accessed production-only material",
        )

    entry = record.get("entry")
    if not isinstance(entry, Mapping):
        _add(issues, "trial_record_incomplete", "$.entry", "entry observation is required")
    else:
        for field in ("started_at", "page"):
            if not _text(entry.get(field)):
                _add(
                    issues,
                    "trial_record_incomplete",
                    f"$.entry.{field}",
                    f"entry {field} is required",
                )
        for field in ("goal_understood", "materials_found"):
            if not isinstance(entry.get(field), bool):
                _add(
                    issues,
                    "trial_record_incomplete",
                    f"$.entry.{field}",
                    f"entry {field} must be observed as true or false",
                )

    actions = _validate_collection(record.get("actions"), "$.actions", issues)
    if actions is not None:
        if not actions:
            _add(issues, "trial_record_incomplete", "$.actions", "chronological actions are required")
        sequences: list[int] = []
        for index, action in enumerate(actions):
            path = f"$.actions[{index}]"
            if not isinstance(action, Mapping):
                _add(issues, "trial_record_incomplete", path, "action must be an object")
                continue
            sequence = action.get("sequence")
            if isinstance(sequence, bool) or not isinstance(sequence, int):
                _add(issues, "actions_not_chronological", f"{path}.sequence", "action sequence must be an integer")
            else:
                sequences.append(sequence)
            for field in ("action", "observable_result", "at"):
                if not _text(action.get(field)):
                    _add(
                        issues,
                        "trial_record_incomplete",
                        f"{path}.{field}",
                        f"action {field} is required",
                    )
        if sequences and sequences != list(range(1, len(actions) + 1)):
            _add(
                issues,
                "actions_not_chronological",
                "$.actions",
                "actions must use a unique chronological sequence starting at 1",
            )

    hints = _validate_collection(record.get("hints"), "$.hints", issues)
    if hints is not None:
        for index, hint in enumerate(hints):
            path = f"$.hints[{index}]"
            if not isinstance(hint, Mapping):
                _add(issues, "trial_record_incomplete", path, "hint must be an object")
                continue
            if hint.get("source") not in {"learner-page", "learner-asset", "none"}:
                _add(
                    issues,
                    "non_learner_input_accessed",
                    f"{path}.source",
                    "hint source must be learner-visible or none",
                )
            if not _text(hint.get("detail")):
                _add(issues, "trial_record_incomplete", f"{path}.detail", "hint detail is required")

    blocks = _validate_collection(record.get("blocks"), "$.blocks", issues)
    recovery = _validate_collection(record.get("recovery"), "$.recovery", issues)
    recovery_codes: set[str] = set()
    if recovery is not None:
        for index, item in enumerate(recovery):
            path = f"$.recovery[{index}]"
            if not isinstance(item, Mapping):
                _add(issues, "trial_record_incomplete", path, "recovery must be an object")
                continue
            code = item.get("block_code")
            if not _text(code):
                _add(issues, "trial_record_incomplete", f"{path}.block_code", "recovery block_code is required")
            else:
                recovery_codes.add(code)
            for field in ("action", "result"):
                if not _text(item.get(field)):
                    _add(issues, "trial_record_incomplete", f"{path}.{field}", f"recovery {field} is required")
    if blocks is not None:
        for index, block in enumerate(blocks):
            path = f"$.blocks[{index}]"
            if not isinstance(block, Mapping):
                _add(issues, "trial_record_incomplete", path, "block must be an object")
                continue
            code = block.get("code")
            if not _text(code):
                _add(issues, "trial_record_incomplete", f"{path}.code", "block code is required")
            if not _text(block.get("detail")):
                _add(issues, "trial_record_incomplete", f"{path}.detail", "block detail is required")
            if not isinstance(block.get("recovered"), bool):
                _add(issues, "trial_record_incomplete", f"{path}.recovered", "block recovery status is required")
            elif block.get("recovered") is True and _text(code) and code not in recovery_codes:
                _add(
                    issues,
                    "recovery_evidence_missing",
                    path,
                    "a recovered block requires a matching recovery record",
                )

    artifact = record.get("artifact")
    if not isinstance(artifact, Mapping):
        _add(issues, "artifact_not_verified", "$.artifact", "completed artifact evidence is required")
    else:
        if not _text(artifact.get("path")):
            _add(issues, "artifact_not_verified", "$.artifact.path", "artifact path is required")
        if not SHA256_PATTERN.fullmatch(str(artifact.get("sha256", ""))):
            _add(issues, "artifact_not_verified", "$.artifact.sha256", "artifact must have a lowercase SHA-256")
        if artifact.get("complete") is not True:
            _add(issues, "artifact_not_verified", "$.artifact.complete", "artifact must be complete")
        if artifact.get("verifiable") is not True:
            _add(issues, "artifact_not_verified", "$.artifact.verifiable", "artifact must be independently verifiable")
        if artifact.get("acceptance_result") != "PASS":
            _add(issues, "artifact_not_verified", "$.artifact.acceptance_result", "artifact must pass acceptance checks")

    result = record.get("result")
    if not isinstance(result, Mapping):
        _add(issues, "trial_record_incomplete", "$.result", "trial result is required")
    else:
        if result.get("status") not in {"PASS", "FAIL"}:
            _add(issues, "trial_record_incomplete", "$.result.status", "trial result must be PASS or FAIL")
        for field in ("completed_at", "notes"):
            if not _text(result.get(field)):
                _add(issues, "trial_record_incomplete", f"$.result.{field}", f"result {field} is required")
        if result.get("status") == "PASS" and isinstance(blocks, list):
            for index, block in enumerate(blocks):
                if isinstance(block, Mapping) and block.get("recovered") is not True:
                    code = str(block.get("code", "practice_instruction_gap"))
                    try:
                        gate_id = route_trial_failure(code)
                    except ValueError:
                        gate_id = "G3"
                    _add(
                        issues,
                        "unrecovered_trial_block",
                        f"$.blocks[{index}]",
                        "a trial with an unrecovered block cannot pass",
                        gate_id,
                    )

    if isinstance(participant, Mapping) and participant.get("type") == "human":
        human = record.get("human_participant_evidence")
        if not isinstance(human, Mapping):
            _add(
                issues,
                "human_participant_evidence_missing",
                "$.human_participant_evidence",
                "human verification requires explicit participant evidence",
            )
        else:
            for field in ("consent_record", "observer_id"):
                if not _text(human.get(field)):
                    _add(
                        issues,
                        "human_participant_evidence_missing",
                        f"$.human_participant_evidence.{field}",
                        f"human evidence {field} is required",
                    )
            if not SHA256_PATTERN.fullmatch(
                str(human.get("session_recording_sha256", ""))
            ):
                _add(
                    issues,
                    "human_participant_evidence_missing",
                    "$.human_participant_evidence.session_recording_sha256",
                    "human session evidence must have a lowercase SHA-256",
                )

    return issues


def evidence_maturity(record: Mapping[str, Any]) -> str:
    scope = record.get("scope")
    if scope not in TRIAL_SCOPES:
        return "EXECUTION_VALIDATED"
    issues = validate_trial_record(record, (), scope)
    result = record.get("result")
    passed = isinstance(result, Mapping) and result.get("status") == "PASS"
    if issues or not passed:
        return "EXECUTION_VALIDATED"
    participant = record.get("participant")
    if not isinstance(participant, Mapping):
        return "EXECUTION_VALIDATED"
    if participant.get("type") == "human":
        return "HUMAN_VERIFIED"
    if participant.get("type") == "independent-ai":
        return "INDEPENDENT_AI_VERIFIED"
    return "EXECUTION_VALIDATED"


def validate_trial_context_is_new(
    record: Mapping[str, Any], prior_context_ids: Sequence[str]
) -> list[TrialIssue]:
    context_id = record.get("isolated_context_id")
    if not _text(context_id):
        return [
            TrialIssue(
                "g5_trial_context_invalid",
                "$.isolated_context_id",
                "trial requires an isolated context id",
                "G5",
            )
        ]
    prior = {item.strip() for item in prior_context_ids if _text(item)}
    if context_id in prior:
        return [
            TrialIssue(
                "g5_trial_context_invalid",
                "$.isolated_context_id",
                "full-course trial cannot reuse a pilot or production context",
                "G5",
            )
        ]
    return []


def _route_verified_trial_to_gate(
    contract: MutableMapping[str, Any],
    gate_id: str,
    production_evidence_ids: Sequence[str],
    trial_evidence_id: str,
    trial_receipt_evidence_id: str,
    actor: str,
    at: str,
    *,
    workspace_root: Path | str,
) -> str:
    expected_scope = {"G4": "representative_unit", "G5": "full_course"}.get(gate_id)
    if expected_scope is None:
        raise ValueError("independent course trials may pass only G4 or G5")
    if not production_evidence_ids or any(not _text(item) for item in production_evidence_ids):
        raise ValueError("production evidence is required before a trial can pass a gate")
    evidence_index = contract.get("evidence_index")
    if not isinstance(evidence_index, list):
        raise ContractStateError("contract evidence index is missing")
    indexed = {
        item.get("id"): item
        for item in evidence_index
        if isinstance(item, Mapping) and _text(item.get("id"))
    }
    requested_ids = [*production_evidence_ids, trial_evidence_id, trial_receipt_evidence_id]
    missing = [item for item in requested_ids if item not in indexed]
    if missing:
        raise ContractStateError(
            f"trial route references unindexed production evidence: {', '.join(missing)}"
        )
    governance = contract.get("governance")
    roster_binding = governance.get("production_role_roster") if isinstance(governance, Mapping) else None
    if not isinstance(roster_binding, Mapping):
        raise ContractStateError("trial route requires a governed production role roster")
    roster_id = roster_binding.get("evidence_id")
    supplied_rosters = [
        item for item in production_evidence_ids
        if isinstance(indexed.get(item), Mapping) and indexed[item].get("kind") == "production_role_roster"
    ]
    if supplied_rosters != [roster_id]:
        raise ContractStateError("trial route must use the exact governed production role roster")
    transition_ids = [item for item in production_evidence_ids if item != roster_id]
    trial_reference = indexed.get(trial_evidence_id)
    receipt_reference = indexed.get(trial_receipt_evidence_id)
    if (
        not isinstance(trial_reference, Mapping)
        or trial_reference.get("gate") != gate_id
        or trial_reference.get("kind") != "independent_course_trial"
    ):
        raise ContractStateError("trial route requires an existing typed trial reference")
    if (
        not isinstance(receipt_reference, Mapping)
        or receipt_reference.get("gate") != gate_id
        or receipt_reference.get("kind") != "independent_trial_receipt"
    ):
        raise ContractStateError("trial route requires an existing authority-issued receipt reference")
    wrong_gate = [
        item
        for item in transition_ids
        if indexed[item].get("gate") != gate_id
    ]
    if wrong_gate:
        raise ContractStateError(
            f"production evidence belongs to another gate: {', '.join(wrong_gate)}"
        )

    from src.course_gate import validate_and_transition_gate

    result = validate_and_transition_gate(
        contract,
        gate_id,
        [*transition_ids, trial_evidence_id, trial_receipt_evidence_id],
        workspace_root,
        actor,
        at,
    )
    if result == "PASS":
        contract["gates"][gate_id]["evidence"][-1]["maturity"] = trial_reference.get("maturity")
    return result


def route_verified_trial_to_gate(
    contract: MutableMapping[str, Any], gate_id: str,
    production_evidence_ids: Sequence[str], trial_evidence_id: str,
    trial_receipt_evidence_id: str,
    actor: str, at: str, *, workspace_root: Path | str,
) -> str:
    staged = copy.deepcopy(contract)
    result = _route_verified_trial_to_gate(
        staged, gate_id, production_evidence_ids, trial_evidence_id,
        trial_receipt_evidence_id, actor, at, workspace_root=workspace_root,
    )
    contract.clear()
    contract.update(staged)
    return result
