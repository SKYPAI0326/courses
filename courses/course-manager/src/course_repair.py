from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class RepairRoute:
    owner_gate: str
    requires_new_course: bool
    revalidation_scope: tuple[str, ...]


def classify_repair_finding(
    code: str, policy: Mapping[str, Any]
) -> RepairRoute:
    if not isinstance(code, str) or not code.strip():
        raise ValueError("repair finding code must contain text")
    new_course = policy.get("new_course_triggers")
    if isinstance(new_course, Mapping) and code in new_course:
        item = new_course[code]
        if not isinstance(item, Mapping):
            raise ValueError(f"invalid new-course route for {code}")
        scope = item.get("revalidation_scope")
        if not isinstance(scope, list) or not all(isinstance(value, str) for value in scope):
            raise ValueError(f"invalid revalidation scope for {code}")
        if item.get("owner_gate") != "G0":
            raise ValueError(f"new-course reframe must start at G0: {code}")
        return RepairRoute("G0", True, tuple(scope))

    routes = policy.get("finding_routes")
    if not isinstance(routes, Mapping) or code not in routes:
        raise ValueError(f"unclassified repair finding: {code}")
    item = routes[code]
    if not isinstance(item, Mapping):
        raise ValueError(f"invalid repair route for {code}")
    owner_gate = item.get("owner_gate")
    scope = item.get("revalidation_scope")
    if owner_gate not in {f"G{index}" for index in range(7)}:
        raise ValueError(f"repair route requires one valid owner Gate: {code}")
    if not isinstance(scope, list) or not scope or not all(
        isinstance(value, str) and value.strip() for value in scope
    ):
        raise ValueError(f"invalid revalidation scope for {code}")
    return RepairRoute(owner_gate, False, tuple(scope))
