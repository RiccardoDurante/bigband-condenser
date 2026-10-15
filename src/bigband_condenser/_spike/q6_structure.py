"""Q6 - 4-staff output structure skeleton.

Produces a minimal MusicXML output with the 4-section structure required by
Charter 3.2: Reeds, Brass, Rhythm, Drums. Placeholder content (4 quarter notes
per part). This is NOT the actual condensation logic - just structural validation
that music21 can produce the required 4-pentagram shape.

Grand staff refinement (2 staves for Reeds/Brass/Rhythm, 1 for Drums) and
chord symbol placement are deferred to M4-M6.
"""
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from bigband_condenser._spike.common import setup_logging  # noqa: E402

TMP_DIR = Path(__file__).resolve().parent / "_tmp"
TMP_DIR.mkdir(exist_ok=True)
OUT_FILE = TMP_DIR / "q6_skeleton.musicxml"


def build_skeleton():
    from music21 import stream, note, clef, meter, metadata

    score = stream.Score()
    score.metadata = metadata.Metadata()
    score.metadata.title = "Big Band Condenser - Structural Skeleton"
    score.metadata.movementName = "Q6 Skeleton (4 pentagrammi, placeholder content)"
    score.metadata.composer = "Big Band Condenser v1 (spike)"

    def make_part(name, use_percussion_clef=False, pitches=("C4", "D4", "E4", "F4")):
        p = stream.Part()
        p.partName = name
        p.insert(0, clef.PercussionClef() if use_percussion_clef else clef.TrebleClef())
        p.insert(0, meter.TimeSignature("4/4"))
        for pitch_name in pitches:
            p.append(note.Note(pitch_name, quarterLength=1.0))
        return p

    score.append(make_part("Reeds"))
    score.append(make_part("Brass", pitches=("G4", "A4", "B4", "C5")))
    score.append(make_part("Rhythm", pitches=("E3", "G3", "B3", "D4")))
    score.append(make_part("Drums", use_percussion_clef=True, pitches=("C4", "C4", "C4", "C4")))

    return score


def main():
    from music21 import converter

    logger = setup_logging()
    logger.info("=" * 70)
    logger.info("Q6 STRUCTURE SKELETON - 4 pentagrammi minimal output")
    logger.info("=" * 70)

    logger.info("Building skeleton Score...")
    score = build_skeleton()
    logger.info(f"Parts built: {len(list(score.parts))}")

    logger.info(f"Writing: {OUT_FILE.name}")
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            score.write("musicxml", fp=str(OUT_FILE))
        size = OUT_FILE.stat().st_size
        logger.info(f"WRITE OK: {size:,} bytes")
    except Exception as e:
        logger.error(f"WRITE FAILED: {type(e).__name__}: {e}")
        return 1

    logger.info("")
    logger.info("Verifying via reparse...")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        verify = converter.parse(str(OUT_FILE))

    parts = list(verify.parts)
    logger.info(f"Reparsed parts: {len(parts)}")
    for i, p in enumerate(parts, 1):
        notes_count = sum(1 for _ in p.recurse().notes)
        logger.info(f"  [{i}] {p.partName or '<unnamed>'}: {notes_count} notes")

    logger.info("")
    logger.info("=" * 70)
    expected_names = {"Reeds", "Brass", "Rhythm", "Drums"}
    got_names = {p.partName for p in parts}
    if len(parts) == 4 and got_names == expected_names:
        logger.info("Q6 VERDICT: PASS - 4 pentagrammi structure produced and round-tripped")
        return 0
    else:
        logger.warning(f"Q6 VERDICT: FAIL - got {len(parts)} parts {got_names}, expected {expected_names}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
