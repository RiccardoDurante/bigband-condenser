"""Fidelity gate for Drums preserver: notes must be identical in count,
offset, and duration (unpitched -> no MIDI equivalence check)."""
import warnings; warnings.simplefilter("ignore")
import sys
from pathlib import Path
sys.path.insert(0, "src")
from music21 import converter
from bigband_condenser.preprocessor import preprocess
from bigband_condenser.classifier import classify_score, SECTION_DRUMS
from bigband_condenser.condenser import DrumsCondenser

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("samples/kronos_kai_kairos_extract.musicxml")
EPS = 1e-6


def collect(part):
    recs = []
    for n in part.recurse().notes:
        try:
            start = float(n.getOffsetInHierarchy(part))
        except Exception:
            start = float(n.offset)
        dur = float(n.duration.quarterLength)
        recs.append((round(start, 3), round(dur, 3)))
    return sorted(recs)


score = converter.parse(str(path))
result = preprocess(score, path)
cls = classify_score(path)
drum_names = {c.part_name for c in cls if c.section == SECTION_DRUMS and not c.is_hidden}
drum_parts = [p for p in result.score.parts if (p.partName or "") in drum_names]
if not drum_parts:
    print("No drum parts found")
    sys.exit(2)

source_set = collect(drum_parts[0])
output, _ = DrumsCondenser(source_xml_path=path).condense(drum_parts, source_score=result.score)
output_set = collect(output)

print(f"file: {path.name} | section: DRUMS")
print(f"source notes: {len(source_set)} | output notes: {len(output_set)}")

missing = [n for n in source_set if n not in output_set]
extra = [n for n in output_set if n not in source_set]
print(f"missing in output: {len(missing)}")
if missing:
    for m in missing[:5]:
        print(f"  @{m[0]} dur={m[1]}")
print(f"extra in output: {len(extra)}")
if extra:
    for e in extra[:5]:
        print(f"  @{e[0]} dur={e[1]}")

print("FIDELITY:", "PASS" if not missing and not extra else "FAIL")
