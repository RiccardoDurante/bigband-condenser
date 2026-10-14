"""Shared helpers for the M2 feasibility spike."""
from pathlib import Path
import logging

REPO_ROOT = Path(__file__).resolve().parents[3]
SAMPLES_DIR = REPO_ROOT / "samples"
KRONOS_FULL = SAMPLES_DIR / "kronos_kai_kairos.musicxml"
KRONOS_EXTRACT = SAMPLES_DIR / "kronos_kai_kairos_extract.musicxml"

SECTION_REEDS = "Reeds"
SECTION_BRASS = "Brass"
SECTION_RHYTHM = "Rhythm"
SECTION_DRUMS = "Drums"
SECTION_UNKNOWN = "UNKNOWN"


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure a simple console logger for spike scripts."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    return logging.getLogger("spike")
