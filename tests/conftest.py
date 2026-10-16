"""Shared pytest fixtures for Big Band Condenser tests."""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import pytest

# Make src importable without pip install -e .
REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def kronos_extract_path(repo_root) -> Path:
    """Path to the Kronos 32-bar extract (fast iteration sample)."""
    return repo_root / "samples" / "kronos_kai_kairos_extract.musicxml"


@pytest.fixture(scope="session")
def kronos_full_path(repo_root) -> Path:
    """Path to the Kronos full score (slow, use sparingly)."""
    return repo_root / "samples" / "kronos_kai_kairos.musicxml"


@pytest.fixture
def kronos_extract_score(kronos_extract_path):
    """Freshly parsed music21 Score of the Kronos extract.

    Not session-scoped: each test gets a new copy to mutate freely.
    """
    from music21 import converter
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return converter.parse(str(kronos_extract_path))
