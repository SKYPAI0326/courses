from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from src.schema_runtime import validate_schema_file
from src.course_evidence import ConsumedEvidence


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
TRANSFER_ROLES = frozenset({
    "held-out-input", "held-out-output", "demonstration-input",
    "demonstration-output", "guided-practice-input", "guided-practice-output",
    "answer-key-input", "answer-key-output", "action-state",
})
REQUIRED_TRANSFER_ROLES = TRANSFER_ROLES - {"action-state"}


def trial_action_id(action: Mapping[str, Any]) -> str:
    payload = {
        key: action.get(key)
        for key in (
            "task_id", "operation", "decision",
            "affected_criterion_id", "input_evidence_id", "output_evidence_id", "result",
        )
    }
    observable = action.get("observable_result")
    payload["observable_result"] = (
        {key: observable.get(key) for key in (
            "evidence_id", "criterion_id", "expected_result", "actual_result",
            "actual_sha256",
        )}
        if isinstance(observable, Mapping) else observable
    )
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"act-{hashlib.sha256(encoded).hexdigest()[:20]}"


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


def _compare_numeric(left: Any, comparator: Any, right: Any) -> bool | None:
    if (
        isinstance(left, bool) or not isinstance(left, (int, float))
        or isinstance(right, bool) or not isinstance(right, (int, float))
    ):
        return None
    operations = {
        "lt": lambda: left < right, "lte": lambda: left <= right,
        "gt": lambda: left > right, "gte": lambda: left >= right,
        "eq": lambda: left == right, "neq": lambda: left != right,
    }
    operation = operations.get(comparator)
    return operation() if operation is not None else None


def _expected_trial_criteria(
    requirements: Mapping[str, Any],
    blueprint: Mapping[str, Any],
    representative_unit_id: str | None,
) -> dict[str, dict[str, str]]:
    capability_to_g0 = {
        str(capability.get("id")): str(criterion.get("id"))
        for criterion in requirements.get("acceptance_criteria", [])
        if isinstance(criterion, Mapping)
        for capability in criterion.get("capabilities", [])
        if isinstance(capability, Mapping)
        and _text(criterion.get("id"))
        and _text(capability.get("id"))
    }
    unit_by_capability = {
        str(capability_id): str(unit.get("id"))
        for unit in blueprint.get("units", [])
        if isinstance(unit, Mapping) and _text(unit.get("id"))
        for capability_id in unit.get("capability_ids", [])
        if _text(capability_id)
    }
    expected: dict[str, dict[str, str]] = {}
    for criterion in blueprint.get("criteria", []):
        if not isinstance(criterion, Mapping):
            continue
        capability_id = criterion.get("capability_id")
        if not _text(capability_id):
            continue
        capability_id = str(capability_id)
        unit_id = unit_by_capability.get(capability_id)
        if representative_unit_id is not None and unit_id != representative_unit_id:
            continue
        if capability_id not in capability_to_g0 or not _text(unit_id):
            continue
        expected[capability_id] = {
            "g0_criterion_id": capability_to_g0[capability_id],
            "capability_id": capability_id,
            "outcome_id": str(criterion.get("outcome_id", "")),
            "criterion_id": str(criterion.get("id", "")),
            "unit_id": str(unit_id),
        }
    return expected


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
    *,
    requirements: Mapping[str, Any] | None = None,
    requirements_sha256: str | None = None,
    blueprint: Mapping[str, Any] | None = None,
    representative_unit_id: str | None = None,
    runner_authority_id: str | None = None,
    transfer_artifacts: Sequence[ConsumedEvidence] | None = None,
) -> list[TrialIssue]:
    issues: list[TrialIssue] = []
    if expected_scope not in TRIAL_SCOPES:
        raise ValueError(f"unsupported expected trial scope: {expected_scope}")
    current_gate = "G4" if expected_scope == "representative_unit" else "G5"
    issues.extend(
        TrialIssue(issue.code, issue.path, issue.message, current_gate)
        for issue in validate_schema_file("course-trial-record.schema.json", record)
    )
    if record.get("schema_version") != 4:
        _add(
            issues,
            "trial_record_incomplete",
            "$.schema_version",
            "trial record schema_version must be 4",
            current_gate,
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

    requirements_digest = record.get("requirements_sha256")
    if not SHA256_PATTERN.fullmatch(str(requirements_digest or "")):
        _add(
            issues,
            "requirements_binding_mismatch",
            "$.requirements_sha256",
            "trial must bind a lowercase SHA-256 for canonical G0 requirements",
            "G0",
        )
    elif requirements_sha256 is not None and requirements_digest != requirements_sha256:
        _add(
            issues,
            "requirements_binding_mismatch",
            "$.requirements_sha256",
            "trial requirements hash does not match canonical G0 evidence",
            "G0",
        )

    if runner_authority_id is not None and record.get("runner_authority_id") != runner_authority_id:
        _add(
            issues,
            "runner_authority_mismatch",
            "$.runner_authority_id",
            "trial runner authority must match governed contract authority",
            current_gate,
        )

    target_profile = requirements.get("target_profile") if isinstance(requirements, Mapping) else None
    environment = requirements.get("environment") if isinstance(requirements, Mapping) else None
    if isinstance(target_profile, Mapping):
        if record.get("target_profile_id") != target_profile.get("id"):
            _add(
                issues,
                "target_profile_mismatch",
                "$.target_profile_id",
                "trial target profile must match canonical G0",
                "G0",
            )
    elif not _text(record.get("target_profile_id")):
        _add(
            issues,
            "target_profile_mismatch",
            "$.target_profile_id",
            "trial target profile id is required",
            "G0",
        )
    allowed_tools = record.get("allowed_tools")
    if not isinstance(allowed_tools, list) or not allowed_tools or not all(
        _text(item) for item in allowed_tools
    ):
        _add(
            issues,
            "allowed_tools_mismatch",
            "$.allowed_tools",
            "trial must declare the learner tools it used",
            current_gate,
        )
    elif isinstance(environment, Mapping) and allowed_tools != environment.get("tools"):
        _add(
            issues,
            "allowed_tools_mismatch",
            "$.allowed_tools",
            "trial tools must exactly match canonical G0 learner tools",
            "G0",
        )

    readiness = record.get("entry_readiness")
    if not isinstance(readiness, Mapping):
        _add(
            issues,
            "entry_readiness_failed",
            "$.entry_readiness",
            "trial must record baseline, prerequisites, tools, and input readiness",
            current_gate,
        )
    else:
        for field in (
            "baseline_confirmed",
            "prerequisites_confirmed",
            "tools_confirmed",
            "inputs_confirmed",
        ):
            if readiness.get(field) is not True:
                _add(
                    issues,
                    "entry_readiness_failed",
                    f"$.entry_readiness.{field}",
                    "false or missing entry readiness blocks the learner trial",
                    current_gate,
                )
        if isinstance(target_profile, Mapping):
            if readiness.get("baseline_statement") != target_profile.get("baseline"):
                _add(
                    issues,
                    "target_profile_mismatch",
                    "$.entry_readiness.baseline_statement",
                    "trial baseline declaration must match canonical target profile",
                    "G0",
                )
            if readiness.get("prerequisite_statements") != target_profile.get("prerequisites"):
                _add(
                    issues,
                    "target_profile_mismatch",
                    "$.entry_readiness.prerequisite_statements",
                    "trial prerequisite declarations must match canonical target profile",
                    "G0",
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
    allowed_input_paths: set[str] = set()
    allowed_input_hashes: set[str] = set()
    allowed_input_bindings: set[tuple[str, str]] = set()
    learner_page_paths: set[str] = set()
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
            else:
                normalized_path = str(input_path).strip()
                if normalized_path in allowed_input_paths:
                    _add(
                        issues,
                        "non_learner_input_accessed",
                        f"{path}.path",
                        "learner-visible input paths must be unique",
                    )
                allowed_input_paths.add(normalized_path)
                if kind == "learner-page":
                    learner_page_paths.add(normalized_path)
            if not SHA256_PATTERN.fullmatch(str(item.get("sha256", ""))):
                _add(
                    issues,
                    "non_learner_input_accessed",
                    f"{path}.sha256",
                    "input must be bound to a lowercase SHA-256",
                )
            else:
                allowed_input_hashes.add(str(item["sha256"]))
                if _text(input_path):
                    allowed_input_bindings.add((str(input_path).strip(), str(item["sha256"])))

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
            elif entry.get(field) is not True:
                _add(
                    issues,
                    "entry_readiness_failed",
                    f"$.entry.{field}",
                    "the trial cannot begin when the goal or required materials are not ready",
                    current_gate,
                )
        if _text(entry.get("page")) and entry.get("page") not in learner_page_paths:
            _add(
                issues,
                "entry_readiness_failed",
                "$.entry.page",
                "trial entry page must be one of the securely bound learner pages",
                current_gate,
            )

    binding_by_id: dict[str, Mapping[str, Any]] = {}
    role_bindings: dict[str, list[Mapping[str, Any]]] = {}
    bindings = record.get("evidence_bindings")
    if not isinstance(bindings, list):
        _add(issues, "transfer_evidence_unbound", "$.evidence_bindings", "trial transfer requires typed evidence bindings", current_gate)
    else:
        for index, binding in enumerate(bindings):
            path = f"$.evidence_bindings[{index}]"
            if not isinstance(binding, Mapping):
                _add(issues, "transfer_evidence_unbound", path, "evidence binding must be an object", current_gate)
                continue
            evidence_id = binding.get("evidence_id")
            role = binding.get("role")
            if not _text(evidence_id) or evidence_id in binding_by_id:
                _add(issues, "transfer_evidence_unbound", f"{path}.evidence_id", "evidence binding ids must be present and unique", current_gate)
                continue
            binding_by_id[str(evidence_id)] = binding
            if role not in TRANSFER_ROLES:
                _add(issues, "transfer_evidence_unbound", f"{path}.role", "unknown transfer evidence role", current_gate)
            else:
                role_bindings.setdefault(str(role), []).append(binding)
        if any(len(role_bindings.get(role, [])) != 1 for role in REQUIRED_TRANSFER_ROLES):
            _add(issues, "transfer_evidence_unbound", "$.evidence_bindings", "trial requires exactly one binding for each governed transfer role", current_gate)
        required_digests = [
            str(role_bindings[role][0].get("sha256", ""))
            for role in REQUIRED_TRANSFER_ROLES if len(role_bindings.get(role, [])) == 1
        ]
        if len(required_digests) == len(REQUIRED_TRANSFER_ROLES) and len(set(required_digests)) != len(required_digests):
            _add(issues, "transfer_hash_reused", "$.evidence_bindings", "held-out, demonstration, guided-practice, and answer-key files must have distinct bytes", current_gate)

    if transfer_artifacts is not None:
        consumed_by_id = {str(item.reference.get("id")): item for item in transfer_artifacts}
        if set(consumed_by_id) != set(binding_by_id):
            _add(issues, "transfer_evidence_unbound", "$.evidence_bindings", "consumed transfer artifact set must exactly match trial bindings", current_gate)
        for evidence_id, binding in binding_by_id.items():
            item = consumed_by_id.get(evidence_id)
            metadata = item.reference.get("metadata") if item is not None else None
            if (
                item is None
                or item.reference.get("kind") != "trial_transfer_artifact"
                or item.reference.get("path") != binding.get("path")
                or item.sha256 != binding.get("sha256")
                or not isinstance(metadata, Mapping)
                or metadata.get("role") != binding.get("role")
            ):
                _add(issues, "transfer_evidence_binding_mismatch", f"$.evidence_bindings.{evidence_id}", "typed evidence id, path, hash, role, and actual bytes must match", current_gate)

    transfer = record.get("transfer_task")
    transfer_task_id: str | None = None
    held_out_input_hash: str | None = None
    held_out_output_hash: str | None = None
    held_out_input_id = ""
    held_out_output_id = ""
    condition_by_id: dict[str, Mapping[str, Any]] = {}
    if not isinstance(transfer, Mapping):
        _add(
            issues,
            "transfer_conditions_missing",
            "$.transfer_task",
            "a structured held-out transfer task is required",
            current_gate,
        )
    else:
        if _text(transfer.get("task_id")):
            transfer_task_id = str(transfer["task_id"])
        if not transfer_task_id or transfer_task_id == transfer.get("source_task_id"):
            _add(
                issues,
                "transfer_conditions_missing",
                "$.transfer_task.task_id",
                "held-out and source tasks require distinct stable ids",
                current_gate,
            )
        changed_conditions = transfer.get("changed_conditions")
        if not isinstance(changed_conditions, list) or not changed_conditions:
            _add(
                issues,
                "transfer_conditions_missing",
                "$.transfer_task.changed_conditions",
                "transfer task must change data, threshold, or context",
                current_gate,
            )
        else:
            for index, condition in enumerate(changed_conditions):
                path = f"$.transfer_task.changed_conditions[{index}]"
                if not isinstance(condition, Mapping):
                    _add(issues, "transfer_conditions_missing", path, "changed condition must be an object", current_gate)
                    continue
                condition_id = condition.get("condition_id")
                dimension = condition.get("dimension")
                affected = condition.get("affected_criterion_id")
                if not _text(condition_id) or condition_id in condition_by_id:
                    _add(issues, "transfer_conditions_missing", f"{path}.condition_id", "changed condition id must be present and unique", current_gate)
                else:
                    condition_by_id[str(condition_id)] = condition
                if dimension not in {"data", "threshold", "context"} or not _text(affected):
                    _add(
                        issues,
                        "transfer_conditions_missing",
                        path,
                        "changed condition must materially change data, threshold, or context",
                        current_gate,
                    )
                if dimension == "data":
                    before_binding = binding_by_id.get(str(condition.get("before_input_evidence_id", "")))
                    after_binding = binding_by_id.get(str(condition.get("after_input_evidence_id", "")))
                    if (
                        before_binding is None or after_binding is None
                        or not str(before_binding.get("role", "")).endswith("input")
                        or not str(after_binding.get("role", "")).endswith("input")
                        or before_binding.get("sha256") == after_binding.get("sha256")
                    ):
                        _add(issues, "transfer_conditions_missing", path, "data changes must bind distinct before/after typed input bytes", current_gate)
                    before_evaluation = _compare_numeric(condition.get("before_observed_value"), condition.get("comparator"), condition.get("target_value"))
                    after_evaluation = _compare_numeric(condition.get("after_observed_value"), condition.get("comparator"), condition.get("target_value"))
                elif dimension == "threshold":
                    before_evaluation = _compare_numeric(condition.get("observed_value"), condition.get("comparator"), condition.get("before_value"))
                    after_evaluation = _compare_numeric(condition.get("observed_value"), condition.get("comparator"), condition.get("after_value"))
                    basis = binding_by_id.get(str(condition.get("basis_evidence_id", "")))
                    if condition.get("before_value") == condition.get("after_value") or basis is None:
                        _add(issues, "transfer_conditions_missing", path, "threshold changes require distinct numeric thresholds and typed basis evidence", current_gate)
                elif dimension == "context":
                    before_context = condition.get("before_context")
                    after_context = condition.get("after_context")
                    required_constraint = condition.get("required_constraint")
                    before_evaluation = (
                        required_constraint in before_context.get("constraints", [])
                        if isinstance(before_context, Mapping) else None
                    )
                    after_evaluation = (
                        required_constraint in after_context.get("constraints", [])
                        if isinstance(after_context, Mapping) else None
                    )
                    if before_context == after_context:
                        _add(issues, "transfer_conditions_missing", path, "context changes require distinct profile constraints", current_gate)
                else:
                    before_evaluation = after_evaluation = None
                if (
                    before_evaluation is None or after_evaluation is None
                    or condition.get("before_rule_passed") != before_evaluation
                    or condition.get("after_rule_passed") != after_evaluation
                ):
                    _add(issues, "transfer_conditions_missing", path, "changed condition rule results must be reproducible from structured values", current_gate)
                if before_evaluation == after_evaluation or condition.get("before_outcome") == condition.get("after_outcome"):
                    _add(
                        issues,
                        "transfer_judgment_unchanged",
                        path,
                        "held-out conditions must force a different learner judgment",
                        current_gate,
                    )
        held_out_input_id = str(transfer.get("held_out_input_evidence_id", ""))
        held_out_output_id = str(transfer.get("held_out_output_evidence_id", ""))
        held_out_input = binding_by_id.get(held_out_input_id)
        held_out_output = binding_by_id.get(held_out_output_id)
        if held_out_input not in role_bindings.get("held-out-input", []) or held_out_output not in role_bindings.get("held-out-output", []):
            _add(issues, "transfer_evidence_unbound", "$.transfer_task", "held-out task must bind the governed input/output evidence roles", current_gate)
        elif (str(held_out_input.get("path", "")), str(held_out_input.get("sha256", ""))) not in allowed_input_bindings:
            _add(issues, "transfer_input_unbound", "$.transfer_task.held_out_input_evidence_id", "held-out input evidence must exactly match a securely bound learner-visible input", current_gate)
        reference_evidence = transfer.get("reference_evidence")
        if isinstance(reference_evidence, Mapping):
            for phase in ("demonstration", "guided_practice", "answer_key"):
                pair = reference_evidence.get(phase)
                for side in ("input", "output"):
                    evidence_id = pair.get(f"{side}_evidence_id") if isinstance(pair, Mapping) else None
                    expected_role = f"{phase.replace('_', '-')}-{side}"
                    if binding_by_id.get(str(evidence_id or "")) not in role_bindings.get(expected_role, []):
                        _add(issues, "transfer_evidence_unbound", f"$.transfer_task.reference_evidence.{phase}.{side}_evidence_id", "reference phase must bind its exact typed evidence role", current_gate)

    actions = _validate_collection(record.get("actions"), "$.actions", issues)
    action_by_id: dict[str, Mapping[str, Any]] = {}
    transfer_actions: list[Mapping[str, Any]] = []
    if actions is not None:
        if not actions:
            _add(issues, "trial_record_incomplete", "$.actions", "chronological actions are required")
        sequences: list[int] = []
        for index, action in enumerate(actions):
            path = f"$.actions[{index}]"
            if not isinstance(action, Mapping):
                _add(issues, "trial_record_incomplete", path, "action must be an object")
                continue
            action_id = action.get("id")
            if not _text(action_id) or action_id in action_by_id:
                _add(
                    issues,
                    "trial_record_incomplete",
                    f"{path}.id",
                    "action id must be present and unique",
                    current_gate,
                )
            else:
                action_by_id[str(action_id)] = action
            if transfer_task_id is not None and action.get("task_id") == transfer_task_id:
                transfer_actions.append(action)
            sequence = action.get("sequence")
            if isinstance(sequence, bool) or not isinstance(sequence, int):
                _add(issues, "actions_not_chronological", f"{path}.sequence", "action sequence must be an integer")
            else:
                sequences.append(sequence)
            if not _text(action.get("at")):
                _add(issues, "trial_record_incomplete", f"{path}.at", "action at is required")
            for field in ("operation", "decision", "observable_result"):
                if not isinstance(action.get(field), Mapping):
                    _add(
                        issues,
                        "trial_record_incomplete",
                        f"{path}.{field}",
                        f"action {field} must be a structured object",
                    )
            for field in ("input_evidence_id", "output_evidence_id"):
                if action.get(field) not in binding_by_id:
                    _add(
                        issues,
                        "trial_record_incomplete",
                        f"{path}.{field}",
                        "trial action input and output must bind typed evidence",
                        current_gate,
                    )
            operation = action.get("operation")
            decision = action.get("decision")
            observable = action.get("observable_result")
            condition = (
                condition_by_id.get(str(decision.get("condition_id", "")))
                if isinstance(decision, Mapping) else None
            )
            output_binding = binding_by_id.get(str(action.get("output_evidence_id", "")))
            if (
                not isinstance(operation, Mapping)
                or operation.get("subject_evidence_id") != action.get("input_evidence_id")
                or not isinstance(operation.get("transformation"), Mapping)
                or operation["transformation"].get("rule_id") != (
                    decision.get("condition_id") if isinstance(decision, Mapping) else None
                )
            ):
                _add(issues, "generic_trial_action", f"{path}.operation", "operation must bind its input subject and a governed changed-condition rule", current_gate)
            if (
                condition is None
                or not isinstance(decision, Mapping)
                or decision.get("criterion_id") != action.get("affected_criterion_id")
                or decision.get("rule_passed") != condition.get("after_rule_passed")
                or decision.get("outcome") != condition.get("after_outcome")
            ):
                _add(issues, "generic_trial_action", f"{path}.decision", "decision must reproduce the governed changed-condition result", current_gate)
            if (
                not isinstance(observable, Mapping)
                or observable.get("evidence_id") != action.get("output_evidence_id")
                or observable.get("criterion_id") != action.get("affected_criterion_id")
                or observable.get("expected_result") != "PASS"
                or observable.get("actual_result") != action.get("result")
                or output_binding is None
                or observable.get("actual_sha256") != output_binding.get("sha256")
            ):
                _add(issues, "generic_trial_action", f"{path}.observable_result", "observable result must compare expected PASS with the actual typed output evidence and hash", current_gate)
            if action_id != trial_action_id(action):
                _add(issues, "trial_action_id_invalid", f"{path}.id", "action id must be derived from the canonical action payload", current_gate)
            changed_criteria = {
                item.get("affected_criterion_id") for item in transfer.get("changed_conditions", [])
                if isinstance(item, Mapping)
            } if isinstance(transfer, Mapping) else set()
            if action.get("affected_criterion_id") not in changed_criteria:
                _add(issues, "generic_trial_action", f"{path}.affected_criterion_id", "trial action must address a changed governed criterion", current_gate)
            if action.get("result") not in {"PASS", "FAIL"}:
                _add(
                    issues,
                    "trial_record_incomplete",
                    f"{path}.result",
                    "trial action result must be PASS or FAIL",
                    current_gate,
                )
        if sequences and sequences != list(range(1, len(actions) + 1)):
            _add(
                issues,
                "actions_not_chronological",
                "$.actions",
                "actions must use a unique chronological sequence starting at 1",
            )
        ordered_transfer = sorted(
            transfer_actions,
            key=lambda item: item.get("sequence") if isinstance(item.get("sequence"), int) else 0,
        )
        if (
            not ordered_transfer
            or ordered_transfer[0].get("input_evidence_id") != held_out_input_id
            or ordered_transfer[-1].get("output_evidence_id") != held_out_output_id
            or any(
                current.get("output_evidence_id") != following.get("input_evidence_id")
                for current, following in zip(ordered_transfer, ordered_transfer[1:])
            )
        ):
            _add(
                issues,
                "transfer_action_chain_invalid",
                "$.actions",
                "held-out actions must consume the held-out input and produce the held-out output",
                current_gate,
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
    artifact_evidence_id: str | None = None
    if not isinstance(artifact, Mapping):
        _add(issues, "artifact_not_verified", "$.artifact", "completed artifact evidence is required")
    else:
        if not _text(artifact.get("evidence_id")):
            _add(issues, "artifact_not_verified", "$.artifact.evidence_id", "artifact evidence id is required")
        else:
            artifact_evidence_id = str(artifact["evidence_id"])
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
        artifact_binding = binding_by_id.get(str(artifact_evidence_id or ""))
        if (
            artifact_binding is None
            or artifact_binding not in role_bindings.get("held-out-output", [])
            or artifact.get("path") != artifact_binding.get("path")
            or artifact.get("sha256") != artifact_binding.get("sha256")
            or artifact_evidence_id != held_out_output_id
        ):
            _add(
                issues,
                "artifact_not_verified",
                "$.artifact.sha256",
                "trial artifact must exactly match the consumed held-out output evidence",
                current_gate,
            )

    criterion_rows = record.get("criterion_evidence")
    expected_criteria = (
        _expected_trial_criteria(requirements, blueprint, representative_unit_id)
        if isinstance(requirements, Mapping) and isinstance(blueprint, Mapping)
        else {}
    )
    expected_criterion_ids = {item["criterion_id"] for item in expected_criteria.values()}
    if expected_criterion_ids and isinstance(transfer, Mapping):
        for index, condition in enumerate(transfer.get("changed_conditions", [])):
            if isinstance(condition, Mapping) and condition.get("affected_criterion_id") not in expected_criterion_ids:
                _add(issues, "transfer_conditions_missing", f"$.transfer_task.changed_conditions[{index}].affected_criterion_id", "changed condition must affect a governed criterion in trial scope", current_gate)
    seen_capabilities: set[str] = set()
    covered_capabilities: set[str] = set()
    if not isinstance(criterion_rows, list) or not criterion_rows:
        _add(
            issues,
            "criterion_evidence_incomplete",
            "$.criterion_evidence",
            "trial requires criterion-level evidence",
            current_gate,
        )
    else:
        for index, row in enumerate(criterion_rows):
            path = f"$.criterion_evidence[{index}]"
            if not isinstance(row, Mapping):
                _add(issues, "criterion_evidence_incomplete", path, "criterion evidence must be an object", current_gate)
                continue
            capability_id = row.get("capability_id")
            if not _text(capability_id):
                _add(issues, "criterion_evidence_incomplete", f"{path}.capability_id", "capability id is required", current_gate)
                continue
            capability_id = str(capability_id)
            if capability_id in seen_capabilities:
                _add(
                    issues,
                    "criterion_evidence_duplicate",
                    f"{path}.capability_id",
                    "each governed capability may appear only once in trial evidence",
                    current_gate,
                )
            seen_capabilities.add(capability_id)
            expected = expected_criteria.get(capability_id)
            if expected_criteria and (
                expected is None
                or any(row.get(field) != value for field, value in expected.items())
            ):
                _add(
                    issues,
                    "criterion_evidence_unknown",
                    path,
                    "trial criterion tuple does not match governed G0/G2 coverage",
                    current_gate,
                )
                continue
            if expected is not None:
                covered_capabilities.add(capability_id)
            action = action_by_id.get(str(row.get("action_id", "")))
            if (
                not isinstance(action, Mapping)
                or action.get("result") != "PASS"
                or action.get("task_id") != transfer_task_id
                or action.get("affected_criterion_id") != row.get("criterion_id")
                or row.get("result") != "PASS"
            ):
                _add(
                    issues,
                    "criterion_action_invalid",
                    f"{path}.action_id",
                    "criterion evidence must reference a passing action from the held-out task",
                    current_gate,
                )
            if row.get("artifact_evidence_id") != artifact_evidence_id:
                _add(
                    issues,
                    "criterion_artifact_invalid",
                    f"{path}.artifact_evidence_id",
                    "criterion evidence must reference the verified trial artifact",
                    current_gate,
                )
    if expected_criteria and covered_capabilities != set(expected_criteria):
        _add(
            issues,
            "criterion_evidence_incomplete",
            "$.criterion_evidence",
            "trial evidence must exactly cover every governed capability in scope",
            current_gate,
        )

    result = record.get("result")
    if not isinstance(result, Mapping):
        _add(issues, "trial_record_incomplete", "$.result", "trial result is required")
    else:
        if result.get("status") not in {"PASS", "FAIL"}:
            _add(issues, "trial_record_incomplete", "$.result.status", "trial result must be PASS or FAIL")
        elif result.get("status") == "FAIL":
            _add(
                issues,
                "trial_result_failed",
                "$.result.status",
                "a failed trial cannot pass a Gate",
                "G4" if expected_scope == "representative_unit" else "G5",
            )
        for field in ("completed_at", "notes"):
            if not _text(result.get(field)):
                _add(issues, "trial_record_incomplete", f"$.result.{field}", f"result {field} is required")
        if isinstance(blocks, list):
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

    maturity_claims = record.get("maturity_claims")
    participant_type = participant.get("type") if isinstance(participant, Mapping) else None
    expected_ai_claim = "INDEPENDENT_AI_VERIFIED" if participant_type == "independent-ai" else "NOT_APPLICABLE"
    if (
        not isinstance(maturity_claims, Mapping)
        or maturity_claims.get("ai_trial") != expected_ai_claim
        or any(
            maturity_claims.get(field) != "PENDING_HUMAN"
            for field in ("human_duration", "human_readability", "target_learner_independence")
        )
    ):
        _add(
            issues,
            "invalid_maturity_claim",
            "$.maturity_claims",
            "AI trials may claim only independent AI verification; human duration, readability, and independence remain pending",
            current_gate,
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
        return "PENDING_HUMAN"
    if participant.get("type") == "independent-ai":
        return "INDEPENDENT_AI_VERIFIED"
    return "EXECUTION_VALIDATED"


def derived_trial_reference_maturity(record: Mapping[str, Any]) -> str:
    participant = record.get("participant")
    claims = record.get("maturity_claims")
    if (
        isinstance(participant, Mapping)
        and participant.get("type") == "independent-ai"
        and isinstance(claims, Mapping)
        and claims.get("ai_trial") == "INDEPENDENT_AI_VERIFIED"
        and all(claims.get(field) == "PENDING_HUMAN" for field in (
            "human_duration", "human_readability", "target_learner_independence"
        ))
    ):
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
