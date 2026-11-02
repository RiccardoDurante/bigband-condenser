"""Preview script for Drums preserver (M7)."""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from music21 import converter, metadata, stream  # noqa: E402

from bigband_condenser.classifier import classify_score, SECTION_DRUMS  # noqa: E402
from bigband_condenser.condenser import DrumsCondenser  # noqa: E402
from bigband_condenser.preprocessor import preprocess  # noqa: E402

EXTRACT_PATH = REPO_ROOT / "samples" / "kronos_kai_kairos_extract.musicxml"
OUT_PATH = REPO_ROOT / "samples" / "preview_drums.musicxml"


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
    print(f"  parts stripped: {result.parts_stripped}")
    print("Selecting Drum parts...")
    classifications = classify_score(EXTRACT_PATH)
    drum_names = {c.part_name for c in classifications
                  if c.section == SECTION_DRUMS and not c.is_hidden}
    drum_parts = [p for p in result.score.parts if (p.partName or "") in drum_names]
    print(f"  drum parts: {len(drum_parts)} ({', '.join(p.partName for p in drum_parts)})")
    if not drum_parts:
        print("No drum parts found")
        return 2
    print("Running DrumsCondenser.condense()...")
    output, _ = DrumsCondenser(source_xml_path=EXTRACT_PATH).condense(drum_parts, source_score=result.score)
    print(f"  output notes: {sum(1 for _ in output.recurse().notes)}")

    out = stream.Score()
    if score.metadata is not None:
        out.metadata = metadata.Metadata()
        out.metadata.title = score.metadata.title or "Drums"
        movement = score.metadata.movementName or "Drums"
        out.metadata.movementName = f"{movement} - Drums Preserved (M7)"
        out.metadata.composer = score.metadata.composer
    out.insert(0, output)
    print(f"Writing: {OUT_PATH.name}")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out.write("musicxml", fp=str(OUT_PATH))
    print(f"OK ({OUT_PATH.stat().st_size:,} bytes)")
    print(f"\nOpen in Dorico/Finale: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
