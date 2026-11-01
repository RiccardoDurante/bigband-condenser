import warnings; warnings.simplefilter("ignore")
import sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, "src")
from music21 import converter, stream
from bigband_condenser.preprocessor import preprocess
from bigband_condenser.classifier import classify_score, SECTION_REEDS
from bigband_condenser.condenser import ReedsCondenser

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("samples/kronos_kai_kairos_extract.musicxml")
TOL = 0.25
EPS = 1e-6


def merge(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1] + EPS:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def total(intervals):
    return sum(e - s for s, e in intervals)


def clip(intervals, lo, hi):
    res = []
    for s, e in intervals:
        s2, e2 = max(s, lo), min(e, hi)
        if e2 > s2 + EPS:
            res.append([s2, e2])
    return res


def intersect(a, b):
    i = j = 0
    res = []
    while i < len(a) and j < len(b):
        s = max(a[i][0], b[j][0])
        e = min(a[i][1], b[j][1])
        if e > s + EPS:
            res.append([s, e])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return res


def collect(part, into):
    for n in part.recurse().notes:
        start = float(n.getOffsetInHierarchy(part))
        end = start + float(n.duration.quarterLength)
        for p in n.pitches:
            into[p.midi].append((start, end))


score = converter.parse(str(path))
result = preprocess(score, path)
cls = classify_score(path)
names = {c.part_name for c in cls if c.section == SECTION_REEDS and not c.is_hidden}
parts = [p for p in result.score.parts if (p.partName or "") in names]
upper, lower = ReedsCondenser().condense(parts, source_score=result.score)

src, out = defaultdict(list), defaultdict(list)
for p in parts:
    collect(p.toSoundingPitch(inPlace=False), src)
collect(upper, out)
collect(lower, out)
src_m = {k: merge(v) for k, v in src.items()}
out_m = {k: merge(v) for k, v in out.items()}

bounds = [
    (m.number, float(m.offset), float(m.offset) + float(m.duration.quarterLength))
    for m in result.score.parts[0].getElementsByClass(stream.Measure)
]

total_src = sum(total(v) for v in src_m.values())
tot_missing = tot_extra = 0.0
bad = 0
print(f"file: {path.name} | tolerance per measure: {TOL}")
print(f"{'measure':>8} {'missing':>9} {'extra':>9}")
for num, ms, me in bounds:
    missing = extra = 0.0
    for midi in set(src_m) | set(out_m):
        s_i = clip(src_m.get(midi, []), ms, me)
        o_i = clip(out_m.get(midi, []), ms, me)
        inter = total(intersect(s_i, o_i))
        missing += total(s_i) - inter
        extra += total(o_i) - inter
    tot_missing += missing
    tot_extra += extra
    if missing > TOL or extra > TOL:
        bad += 1
        print(f"{'m' + str(num):>8} {missing:9.2f} {extra:9.2f}")

print()
print(f"source sounding total: {total_src:.1f} pitch-quarters")
print(f"missing: {tot_missing:.1f} ({100 * tot_missing / total_src:.1f}%) | extra: {tot_extra:.1f} ({100 * tot_extra / total_src:.1f}%)")
print(f"measures outside tolerance: {bad}/{len(bounds)}")
print("FIDELITY:", "PASS" if bad == 0 else "FAIL")
