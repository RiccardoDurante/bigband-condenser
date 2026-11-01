import warnings; warnings.simplefilter("ignore")
import sys
from pathlib import Path
sys.path.insert(0, "src")
from music21 import converter, stream, note, chord
from bigband_condenser.preprocessor import preprocess
from bigband_condenser.classifier import classify_score, SECTION_REEDS
from bigband_condenser.condenser import ReedsCondenser

path = Path("samples/kronos_kai_kairos_extract.musicxml")
targets = [int(a) for a in sys.argv[1:]] or [6]

score = converter.parse(str(path))
result = preprocess(score, path)
cls = classify_score(path)
names = {c.part_name for c in cls if c.section == SECTION_REEDS and not c.is_hidden}
parts = [p for p in result.score.parts if (p.partName or "") in names]
upper, lower = ReedsCondenser().condense(parts, source_score=result.score)


def label(el):
    if isinstance(el, note.Rest):
        return "R"
    if isinstance(el, chord.Chord):
        return "+".join(p.nameWithOctave for p in el.pitches)
    return el.pitch.nameWithOctave


def dump(part, n):
    for m in part.getElementsByClass(stream.Measure):
        if m.number == n:
            items = sorted(m.notesAndRests, key=lambda e: float(e.offset))
            return "  ".join(
                f"@{float(e.offset):g}:{label(e)}({float(e.duration.quarterLength):g})"
                for e in items
            ) or "(empty)"
    return "(measure not found)"


for n in targets:
    print(f"===== measure {n} =====")
    print("SOURCE (concert pitch):")
    for p in parts:
        sp = p.toSoundingPitch(inPlace=False)
        print(f"  {p.partName}: {dump(sp, n)}")
    print("CONDENSED upper:", dump(upper, n))
    print("CONDENSED lower:", dump(lower, n))
    print()
