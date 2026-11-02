"""Preview script for Rhythm condenser (M6)."""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from music21 import converter, metadata, stream  # noqa: E402

from bigband_condenser.classifier import classify_score, SECTION_RHYTHM  # noqa: E402
from bigband_condenser.condenser import RhythmCondenser  # noqa: E402
from bigband_condenser.preprocessor import preprocess  # noqa: E402

EXTRACT_PATH = REPO_ROOT / "samples" / "kronos_kai_kairos.musicxml"
OUT_PATH = REPO_ROOT / "samples" / "preview_rhythm.musicxml"


def main() -> int:
    if not EXTRACT_PATH.exists():
        print(f"Not found: {EXTRACT_PATH}")
        return 2
    print(f"Loading: {EXTRACT_PATH.name}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        score = converter.parse(str(EXTRACT_PATH))
    print("Preprocessing...")
    result = preprocess(score, EXTRACT_PATH)
    print(f"  parts stripped: {result.parts_stripped}")
    print("Selecting Rhythm parts...")
    cls = classify_score(EXTRACT_PATH)
    rhythm_names = {c.part_name for c in cls
                    if c.section == SECTION_RHYTHM and not c.is_hidden}
    rhythm_parts = [p for p in result.score.parts if (p.partName or "") in rhythm_names]
    print(f"  rhythm parts (visible, non-hidden): {len(rhythm_parts)} "
          f"({', '.join(p.partName for p in rhythm_parts)})")
    # Also need Piano even if hidden, for chord symbols
    piano_parts = [p for p in result.score.parts if "piano" in (p.partName or "").lower()]
    for p in piano_parts:
        if p not in rhythm_parts:
            rhythm_parts.append(p)
    print(f"  (including Piano for chord symbols) -> {len(rhythm_parts)} parts")

    print("Running RhythmCondenser.condense()...")
    upper, lower = RhythmCondenser(source_xml_path=EXTRACT_PATH).condense(
        rhythm_parts, source_score=result.score
    )
    print(f"  upper notes: {sum(1 for _ in upper.recurse().notes)}")
    print(f"  lower notes: {sum(1 for _ in lower.recurse().notes) if lower else 'N/A'}")

    out = stream.Score()
    if score.metadata is not None:
        out.metadata = metadata.Metadata()
        out.metadata.title = score.metadata.title or "Rhythm"
        movement = score.metadata.movementName or "Rhythm"
        out.metadata.movementName = f"{movement} - Rhythm Condensed (M6)"
        out.metadata.composer = score.metadata.composer
    out.insert(0, upper)
    if lower is not None:
        out.insert(0, lower)
    print(f"Writing: {OUT_PATH.name}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out.write("musicxml", fp=str(OUT_PATH))
    print(f"OK ({OUT_PATH.stat().st_size:,} bytes)")
    print(f"Open in Dorico/Finale: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
