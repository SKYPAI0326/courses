from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


ROOT_ENVIRONMENTS = {
    "design_system_root": "COURSE_DESIGN_SYSTEM_ROOT",
    "course_web_root": "COURSE_WEB_ROOT",
    "skills_root": "SKILLS_ROOT",
    "state_root": "COURSE_DESIGN_STATE_ROOT",
}
DESIGN_SYSTEM_REQUIRED_PATHS = (
    "contracts/course-contract.schema.json",
    "scripts/course_contract.py",
    "src",
    "skill-packages",
)


class RuntimeConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True)
class RuntimePaths:
    design_system_root: Path
    course_web_root: Path
    skills_root: Path
    state_root: Path


def _absolute_lexical_path(name: str, value: object) -> Path:
    if not isinstance(value, (str, os.PathLike)) or not str(value).strip():
        raise RuntimeConfigurationError(f"{name} is required")
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        raise RuntimeConfigurationError(f"{name} must be an absolute path")
    return Path(os.path.abspath(candidate))


def _reject_symlink_components(name: str, path: Path) -> None:
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if current.is_symlink():
            if current.parent == Path(path.anchor):
                # macOS compatibility aliases such as /var -> /private/var are
                # outside the caller-controlled portion of a configured root.
                continue
            raise RuntimeConfigurationError(
                f"{name} must not contain symbolic links: {current}"
            )


def _configured_root(
    environment: Mapping[str, str],
    field: str,
    *,
    allow_absent: bool = False,
) -> Path:
    variable = ROOT_ENVIRONMENTS[field]
    return validate_root_path(
        variable,
        environment.get(variable),
        allow_absent=allow_absent,
    )


def validate_root_path(
    name: str,
    value: object,
    *,
    allow_absent: bool = False,
) -> Path:
    """Validate one explicit root without resolving through symbolic links."""

    path = _absolute_lexical_path(name, value)
    _reject_symlink_components(name, path)
    if path.exists() and not path.is_dir():
        raise RuntimeConfigurationError(f"{name} must name a directory")
    if not allow_absent and not path.is_dir():
        raise RuntimeConfigurationError(f"{name} directory does not exist: {path}")
    return path


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validate_non_overlapping_roots(roots: Mapping[str, Path]) -> None:
    """Reject equality or containment between every configured root pair."""

    items = tuple((name, path, path.resolve(strict=False)) for name, path in roots.items())
    for index, (left_name, left, safe_left) in enumerate(items):
        for right_name, right, safe_right in items[index + 1 :]:
            if _is_within(safe_left, safe_right) or _is_within(safe_right, safe_left):
                raise RuntimeConfigurationError(
                    f"runtime roots overlap: {left_name}={left} and "
                    f"{right_name}={right}"
                )


def resolve_runtime_paths(
    environment: Mapping[str, str] | None = None,
) -> RuntimePaths:
    """Resolve the four explicit runtime roots without cwd/HOME fallbacks."""

    values = os.environ if environment is None else environment
    paths = RuntimePaths(
        design_system_root=_configured_root(values, "design_system_root"),
        course_web_root=_configured_root(values, "course_web_root"),
        skills_root=_configured_root(values, "skills_root"),
        state_root=_configured_root(values, "state_root", allow_absent=True),
    )
    validate_non_overlapping_roots(
        {
            "COURSE_DESIGN_SYSTEM_ROOT": paths.design_system_root,
            "COURSE_WEB_ROOT": paths.course_web_root,
            "SKILLS_ROOT": paths.skills_root,
            "COURSE_DESIGN_STATE_ROOT": paths.state_root,
        }
    )
    return paths


def source_root_from_module(module_file: Path | str = __file__) -> Path:
    """Locate this checkout by structure, never by its directory name or cwd."""

    anchor = _absolute_lexical_path("module_file", module_file)
    candidates = (anchor.parent, *anchor.parents)
    for candidate in candidates:
        if all((candidate / relative).exists() for relative in DESIGN_SYSTEM_REQUIRED_PATHS):
            return candidate
    raise RuntimeConfigurationError(
        f"cannot locate course design system root from module: {anchor}"
    )


def _check(status: str, detail: str, path: Path | None = None) -> dict[str, str]:
    item = {"status": status, "detail": detail}
    if path is not None:
        item["path"] = str(path)
    return item


def doctor(
    *,
    environment: Mapping[str, str] | None = None,
    platform: str | None = None,
) -> dict[str, object]:
    """Return a read-only readiness report; never creates configured paths."""

    values = os.environ if environment is None else environment
    checks: dict[str, dict[str, str]] = {}
    resolved: dict[str, Path] = {}
    for field, variable in ROOT_ENVIRONMENTS.items():
        try:
            path = _configured_root(
                values,
                field,
                allow_absent=field == "state_root",
            )
            resolved[field] = path
            if path.is_dir():
                checks[field] = _check("READY", f"{variable} is a directory", path)
            else:
                checks[field] = _check("BLOCKED", f"{variable} does not exist", path)
        except RuntimeConfigurationError as error:
            checks[field] = _check("BLOCKED", str(error))

    try:
        resolve_runtime_paths(values)
        checks["root_topology"] = _check(
            "READY", "runtime roots are distinct and state is external"
        )
    except RuntimeConfigurationError as error:
        checks["root_topology"] = _check("BLOCKED", str(error))

    host = sys.platform if platform is None else platform
    if host.startswith(("linux", "darwin")) and os.name == "posix":
        checks["platform_lock"] = _check(
            "READY", "POSIX contract locking is supported"
        )
    else:
        checks["platform_lock"] = _check(
            "BLOCKED",
            "unsupported platform: Windows and non-POSIX contract locks fail closed",
        )

    system_root = resolved.get("design_system_root")
    if system_root is not None:
        missing = [
            relative
            for relative in DESIGN_SYSTEM_REQUIRED_PATHS
            if not (system_root / relative).exists()
        ]
        checks["design_dependencies"] = _check(
            "BLOCKED" if missing else "READY",
            "missing: " + ", ".join(missing) if missing else "required runtime files present",
            system_root,
        )
    else:
        checks["design_dependencies"] = _check(
            "BLOCKED", "COURSE_DESIGN_SYSTEM_ROOT is unresolved"
        )

    status = "READY" if all(item["status"] == "READY" for item in checks.values()) else "BLOCKED"
    return {
        "schema_version": 1,
        "status": status,
        "supported_platforms": ["macOS", "Linux"],
        "checks": checks,
    }
