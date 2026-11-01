import warnings; warnings.simplefilter("ignore")
import sys
from pathlib import Path
sys.path.insert(0, "src")
from music21 import converter, stream
from bigband_condenser.preprocessor import preprocess
from bigband_condenser.classifier import classify_score, SECTION_REEDS

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("samples/kronos_kai_kairos_extract.musicxml")
WINDOW = int(sys.argv[2]) if len(sys.argv) > 2 else 8

score = converter.parse(str(path))
result = preprocess(score, path)
classifications = classify_score(path)
names = {c.part_name for c in classifications if c.section == SECTION_REEDS and not c.is_hidden}
parts = [p for p in result.score.parts if (p.partName or "") in names]
measure_lists = [list(p.getElementsByClass(stream.Measure)) for p in parts]
n_meas = min(len(ml) for ml in measure_lists)

active = [0] * n_meas   # how many of the reed parts play in measure i
onsets = [0] * n_meas   # total note/chord events in measure i
for ml in measure_lists:
    for i in range(n_meas):
        notes = list(ml[i].recurse().notes)
        if notes:
            active[i] += 1
            onsets[i] += len(notes)

numbers = [measure_lists[0][i].number for i in range(n_meas)]
print(f"reed parts: {len(parts)}, measures: {n_meas}, window: {WINDOW}")
print("measure: active parts / events")
print("  ".join(f"m{numbers[i]}:{active[i]}/{onsets[i]}" for i in range(n_meas)))
print()

ranked = []
for s in range(0, n_meas - WINDOW + 1):
    full = sum(1 for i in range(s, s + WINDOW) if active[i] == len(parts))
    ranked.append((full, sum(active[s:s + WINDOW]), sum(onsets[s:s + WINDOW]), s))
ranked.sort(reverse=True)

print("Top windows (measures with all parts playing, sum active, sum events):")
for full, act, ons, s in ranked[:3]:
    print(f"  m{numbers[s]}-m{numbers[s + WINDOW - 1]}: full={full}/{WINDOW}, active={act}, events={ons}")
