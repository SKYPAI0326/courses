"""Import the hyphenated campaign proof builder without duplicating it."""

import runpy
from pathlib import Path


def load_builder():
    return runpy.run_path(
        str(Path(__file__).resolve().parent / "campaign-performance-brief/build_proof.py")
    )
