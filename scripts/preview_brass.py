"""Preview script for Brass condenser (adattato da preview_reeds.py)."""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from music21 import converter, metadata, stream  # noqa: E402

from bigband_condenser.classifier import classify_score, SECTION_BRASS  # noqa: E402
from bigband_condenser.condenser import BrassCondenser  # noqa: E402
from bigband_condenser.preprocessor import preprocess  # noqa: E402

EXTRACT_PATH = REPO_ROOT / "samples" / "kronos_kai_kairos_extract.musicxml"
OUT_PATH = REPO_ROOT / "samples" / "preview_brass.musicxml"


def main() -> int:
    if not EXTRACT_PATH.exists():
        print(f"Extract not found: {EXTRACT_PATH}")
        return 2
    print(f"Loading: {EXTRACT_PATH.name}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        score = converter.parse(str(EXTRACT_PATH))
    print("Preprocessing...")
    result = preprocess(score, EXTRACT_PATH)
    print(f"  parts stripped: {result.parts_stripped}, classes forced: {result.classes_forced}")
    print("Selecting Brass parts...")
    classifications = classify_score(EXTRACT_PATH)
    brass_names = {c.part_name for c in classifications
                   if c.section == SECTION_BRASS and not c.is_hidden}
    brass_parts = [p for p in result.score.parts if (p.partName or "") in brass_names]
    print(f"  brass parts: {len(brass_parts)} ({', '.join(p.partName for p in brass_parts)})")
    print("Running BrassCondenser.condense()...")
    upper, lower = BrassCondenser().condense(brass_parts, source_score=result.score)
    print(f"  upper notes: {sum(1 for _ in upper.recurse().notes)}, "
          f"lower notes: {sum(1 for _ in lower.recurse().notes)}")

    out = stream.Score()
    if score.metadata is not None:
        out.metadata = metadata.Metadata()
        out.metadata.title = score.metadata.title or "Brass Condensed"
        movement = score.metadata.movementName or "Brass"
        out.metadata.movementName = f"{movement} - Brass Condensed (M5)"
        out.metadata.composer = score.metadata.composer
    out.insert(0, upper)
    out.insert(0, lower)
    print(f"Writing: {OUT_PATH.name}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out.write("musicxml", fp=str(OUT_PATH))
    print(f"OK ({OUT_PATH.stat().st_size:,} bytes)")
    print(f"\nOpen in Dorico/Finale: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
