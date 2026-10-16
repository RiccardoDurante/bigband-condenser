"""Preview script: run the pipeline on Kronos extract and emit a MusicXML.

Open the output file in Dorico/Finale/MuseScore to visually inspect how the
Reeds section condenses. Used during M4 iterations as the primary feedback
loop with the Music Expert hat.

Usage (from repo root):
    python scripts/preview_reeds.py
Output: samples/preview_reeds_r1.musicxml
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from music21 import converter, stream  # noqa: E402

from bigband_condenser.classifier import classify_score, SECTION_REEDS  # noqa: E402
from bigband_condenser.condenser import ReedsCondenser  # noqa: E402
from bigband_condenser.preprocessor import preprocess  # noqa: E402


EXTRACT_PATH = REPO_ROOT / "samples" / "kronos_kai_kairos_extract.musicxml"
OUT_PATH = REPO_ROOT / "samples" / "preview_reeds_r1.musicxml"


def main() -> int:
    if not EXTRACT_PATH.exists():
        print(f"Extract not found: {EXTRACT_PATH}")
        return 2

    print(f"Loading: {EXTRACT_PATH.name}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        score = converter.parse(str(EXTRACT_PATH))

    print("Preprocessing (strip hidden + force class + filter drums)...")
    result = preprocess(score, EXTRACT_PATH)
    print(f"  parts stripped: {result.parts_stripped}, classes forced: {result.classes_forced}, drum notes filtered: {result.drum_notes_filtered}")

    print("Selecting Reeds parts via classifier...")
    classifications = classify_score(EXTRACT_PATH)
    reed_names = {c.part_name for c in classifications if c.section == SECTION_REEDS and not c.is_hidden}
    reed_parts = [p for p in result.score.parts if (p.partName or "") in reed_names]
    print(f"  reed parts: {len(reed_parts)} ({', '.join(p.partName for p in reed_parts)})")

    print("Running ReedsCondenser.condense()...")
    upper, lower = ReedsCondenser().condense(reed_parts)
    upper_notes = sum(1 for _ in upper.recurse().notes)
    lower_notes = sum(1 for _ in lower.recurse().notes)
    print(f"  upper notes: {upper_notes}, lower notes: {lower_notes}")

    print(f"Writing: {OUT_PATH.name}")
    out = stream.Score()
    out.insert(0, upper)
    out.insert(0, lower)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out.write("musicxml", fp=str(OUT_PATH))
    print(f"OK ({OUT_PATH.stat().st_size:,} bytes)")
    print()
    print(f"Open in Dorico/Finale: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
