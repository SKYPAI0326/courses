#!/usr/bin/env python3
"""Backward-compatible entry point for validate-course-structure.py."""
from __future__ import annotations

import runpy
from pathlib import Path

_IMPLEMENTATION = Path(__file__).with_name("validate-course-structure.py")


def main() -> int:
    namespace = runpy.run_path(str(_IMPLEMENTATION))
    return int(namespace["cli"]())


if __name__ == "__main__":
    raise SystemExit(main())
